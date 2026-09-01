//Example Date of Creation(YYYY - MM - DD) 2026 - 08 - 26
//Example Date of Last Modification on Github 2026 - 08 - 26
//Version of Rust used for Testing: rustc 1.97.1
//Example Description: This example shows how to read a Thorlabs PMxxx series
//power meter with SCPI commands from Rust on Linux. It is a port of the C++
//VISA example (scpi/PMXXX_SCPI.cpp): instead of NI-VISA it talks to the
//kernel USBTMC driver (/dev/usbtmc*), so it needs no proprietary driver; the
//only third-party crate is `nix`, used for the USBTMC ioctls.

use std::collections::HashSet;
use std::fs::{self, OpenOptions};
use std::io::{self, Read, Write};
use std::path::{Path, PathBuf};
use std::thread::sleep;
use std::time::{Duration, SystemTime, UNIX_EPOCH};

/// USB vendor id used by all Thorlabs instruments.
const THORLABS_USB_VENDOR_ID: &str = "1313";

// ---------------------------------------------------------------------------
// Minimal SCPI-over-USBTMC transport
// ---------------------------------------------------------------------------

/// A SCPI instrument reachable through a `/dev/usbtmcN` device node.
struct ScpiInstrument {
    dev: fs::File,
    path: PathBuf,
}

impl ScpiInstrument {
    /// Open a USBTMC device node with read+write access and a 15 s timeout.
    fn open(path: &Path) -> io::Result<Self> {
        use std::os::fd::AsRawFd;
        let dev = OpenOptions::new().read(true).write(true).open(path)?;
        let timeout_ms: u32 = 15_000;
        // SAFETY: fd is open; timeout_ms outlives the call (copied immediately).
        unsafe { usbtmc_set_timeout(dev.as_raw_fd(), &timeout_ms) }
            .map_err(|e| io::Error::from_raw_os_error(e as i32))?;
        Ok(Self {
            dev,
            path: path.to_path_buf(),
        })
    }

    /// Send one SCPI command (no response expected). Every `write()` becomes
    /// one USBTMC message; the kernel appends the message-end marker for us.
    fn command(&mut self, cmd: &str) -> io::Result<()> {
        self.dev.write_all(cmd.as_bytes())?;
        self.dev.write_all(b"\n")
    }

    /// Send a query and return the response without the trailing newline.
    fn query(&mut self, cmd: &str) -> io::Result<String> {
        self.command(cmd)?;
        let mut buf = [0u8; 256];
        let n = self.dev.read(&mut buf)?;
        if n == 0 {
            return Err(io::Error::other(format!(
                "{}: no response to '{}'",
                self.path.display(),
                cmd
            )));
        }
        Ok(String::from_utf8_lossy(&buf[..n])
            .trim_end_matches(['\r', '\n'])
            .to_string())
    }

    /// Convenience wrapper for queries that answer with a single number.
    fn query_f64(&mut self, cmd: &str) -> io::Result<f64> {
        let text = self.query(cmd)?;
        text.trim()
            .parse()
            .map_err(|e| io::Error::other(format!("cannot parse '{text}' as a number: {e}")))
    }

    /// Send one SCPI query and return the raw binary response bytes.
    fn query_bytes(&mut self, cmd: &str) -> std::io::Result<Vec<u8>> {
        // Send the command (with a trailing newline).
        let formatted_cmd = if cmd.ends_with('\n') {
            cmd.to_string()
        } else {
            format!("{cmd}\n")
        };
        self.dev.write_all(formatted_cmd.as_bytes())?;
        self.dev.flush()?;

        // Read the binary response. The kernel USBTMC driver delivers one
        // message per read(), so a fixed-size buffer is sufficient.
        let mut buf = [0u8; 64];
        let n = self.dev.read(&mut buf)?;

        Ok(buf[..n].to_vec())
    }
}

impl Drop for ScpiInstrument {
    /// Close the session the same way NI-VISA does (observed in a USB capture
    /// of a Windows host): GOTO_LOCAL, then deassert REN. Without this closing
    /// ritual the PM100D2 firmware state machine can wedge after a few
    /// sessions that all started with a bare REN(1).
    fn drop(&mut self) {
        use std::os::fd::AsRawFd;
        let fd = self.dev.as_raw_fd();
        // SAFETY: fd of the still-open device file; results are best-effort.
        unsafe {
            let _ = usbtmc488_goto_local(fd);
            let off: u8 = 0;
            let _ = usbtmc488_ren_control(fd, &off);
        }
    }
}

// ---------------------------------------------------------------------------
// Device discovery
// ---------------------------------------------------------------------------

/// USB vendor id behind a usbtmc sysfs node, or `None` if it cannot be read.
fn usb_vendor_of(sysfs_node: &Path) -> Option<String> {
    // "<node>/device" links to the USB interface; walk up towards the root
    // of the USB tree until a directory carrying "idVendor" is found.
    let mut dir = sysfs_node.join("device").canonicalize().ok()?;
    for _ in 0..8 {
        if let Ok(vendor) = fs::read_to_string(dir.join("idVendor")) {
            return Some(vendor.trim().to_ascii_lowercase());
        }
        dir = dir.parent()?.to_path_buf();
    }
    None
}

/// Enumerate `/dev/usbtmc*` nodes that belong to Thorlabs instruments. Nodes
/// whose vendor id cannot be read are kept as a fallback so they can still be
/// selected manually with `--device`.
fn find_thorlabs_devices() -> Vec<PathBuf> {
    let mut seen: HashSet<std::ffi::OsString> = HashSet::new();
    let mut found = Vec::new();
    // Depending on the kernel the class directory is "usbtmc" or "usbmisc".
    for class_dir in ["/sys/class/usbtmc", "/sys/class/usbmisc"] {
        let Ok(entries) = fs::read_dir(class_dir) else {
            continue;
        };
        for entry in entries.flatten() {
            if !seen.insert(entry.file_name()) {
                continue; // both class directories may expose the same node
            }
            let is_thorlabs = usb_vendor_of(&entry.path())
                .is_none_or(|v| v == THORLABS_USB_VENDOR_ID);
            if is_thorlabs {
                found.push(PathBuf::from("/dev").join(entry.file_name()));
            }
        }
    }
    found.sort();
    found
}

// ---------------------------------------------------------------------------
// Command line options
// ---------------------------------------------------------------------------

struct Options {
    device: Option<PathBuf>, // -d / --device
    wavelength_nm: f64,      // -w / --wavelength
    average: u16,            // -a / --average
    samples: usize,          // -n / --samples
    interval: Duration,      // -i / --interval-ms
    configure: bool,         // --skip-config disables the wavelength/average setup
}

impl Default for Options {
    fn default() -> Self {
        Self {
            device: None,
            wavelength_nm: 800.0,
            average: 1000,
            samples: 10,
            interval: Duration::from_millis(0),
            configure: true,
        }
    }
}

const USAGE: &str = "\
Thorlabs PMxxx power meter - Rust/SCPI reading example (Linux USBTMC)

Usage: thorlabs-pm-scpi [OPTIONS]

Options:
  -d, --device <PATH>      USBTMC device to use (default: auto-detect
                           Thorlabs instruments, e.g. /dev/usbtmc0)
  -w, --wavelength <NM>    Sensor correction wavelength in nm (default: 800)
  -a, --average <N>        Averaging rate (default: 1000; the continuous-mode
                           queue produces one sample every AVG milliseconds)
  -n, --samples <N>        Number of power readings to take (default: 10)
  -i, --interval-ms <MS>   Delay between readings in ms (default: 0)
      --skip-config        Do not change wavelength/averaging, just read
  -h, --help               Show this help
";

fn parse_args(args: &[String]) -> Result<Options, String> {
    let mut opts = Options::default();
    let mut it = args.iter();
    let value = |it: &mut std::slice::Iter<String>, flag: &str| -> Result<String, String> {
        it.next()
            .cloned()
            .ok_or_else(|| format!("missing value for '{flag}'"))
    };
    while let Some(arg) = it.next() {
        match arg.as_str() {
            "-d" | "--device" => opts.device = Some(PathBuf::from(value(&mut it, arg)?)),
            "-w" | "--wavelength" => {
                opts.wavelength_nm = value(&mut it, arg)?
                    .parse()
                    .map_err(|e| format!("invalid wavelength: {e}"))?
            }
            "-a" | "--average" => {
                opts.average = value(&mut it, arg)?
                    .parse()
                    .map_err(|e| format!("invalid averaging rate: {e}"))?
            }
            "-n" | "--samples" => {
                opts.samples = value(&mut it, arg)?
                    .parse()
                    .map_err(|e| format!("invalid sample count: {e}"))?
            }
            "-i" | "--interval-ms" => {
                let ms: u64 = value(&mut it, arg)?
                    .parse()
                    .map_err(|e| format!("invalid interval: {e}"))?;
                opts.interval = Duration::from_millis(ms);
            }
            "--skip-config" => opts.configure = false,
            _ => return Err(format!("unknown argument '{arg}'")),
        }
    }
    Ok(opts)
}

// ---------------------------------------------------------------------------
// Remote enable (REN) — required by PM100D2 and other battery-powered meters
// ---------------------------------------------------------------------------

// USBTMC/488 ioctls from <linux/usb/tmc.h>. The ioctl group id ("magic") is
// USBTMC_IOC_NR = 91 = 0x5B = b'['. The kernel REN_CONTROL handler copies one
// byte from userspace via copy_from_user(), so the argument is a *const u8.
nix::ioctl_write_ptr!(usbtmc488_ren_control, b'[', 19, u8); // _IOW('[', 19, u8)
nix::ioctl_none!(usbtmc488_goto_local, b'[', 20); // _IO('[', 20)

// USBTMC_IOCTL_SET_TIMEOUT = _IOW(91, 10, __u32). The kernel driver's default
// read timeout is 5 s, but MEASure?/FETCh? may block the remote interface for
// up to 10 s (SCPI manual), so raise it.
nix::ioctl_write_ptr!(usbtmc_set_timeout, b'[', 10, u32);

/// Assert USB488 Remote Enable on a `/dev/usbtmcN` device.
///
/// Handheld battery-powered meters (PM100D2/PM100D3, firmware 1.0.7) ignore all
/// SCPI traffic until the host asserts REN, exactly like NI-VISA does on
/// Windows when a session is opened. After a cold boot the firmware needs a
/// settle delay before it processes commands (NI-VISA waits ~350-600 ms);
/// when the meter is already in remote mode the extra sleep is harmless.
fn enable_remote_mode(dev: &fs::File) -> io::Result<()> {
    use std::os::fd::AsRawFd;
    let enable: u8 = 1; // 1 = ASSERT remote enable
                        // SAFETY: the fd is open and `enable` is a valid, outliving pointer.
    unsafe { usbtmc488_ren_control(dev.as_raw_fd(), &enable) }
        .map_err(|e| io::Error::from_raw_os_error(e as i32))?;
    println!("Remote enable (REN) asserted.");
    sleep(Duration::from_millis(600));
    Ok(())
}

// ---------------------------------------------------------------------------
// Example flow
// ---------------------------------------------------------------------------

fn main() {
    let args: Vec<String> = std::env::args().skip(1).collect();
    if args.iter().any(|a| a == "-h" || a == "--help") {
        print!("{USAGE}");
        return;
    }
    let opts = match parse_args(&args) {
        Ok(opts) => opts,
        Err(e) => {
            eprintln!("error: {e}\n\n{USAGE}");
            std::process::exit(2);
        }
    };
    if let Err(e) = run(&opts) {
        eprintln!("error: {e}");
        std::process::exit(1);
    }
}

fn run(opts: &Options) -> io::Result<()> {
    // Find the power meter(s), mirroring viFindRsrc("USB0::0x1313?*INSTR").
    let candidates = match &opts.device {
        Some(path) => vec![path.clone()],
        None => find_thorlabs_devices(),
    };
    if candidates.is_empty() {
        return Err(io::Error::other(
            "no USBTMC device found - is the power meter connected? \
             (if it is, see README.md for the udev permissions rule)",
        ));
    }

    // Connect the only device, or let the user pick among several.
    let device = if candidates.len() == 1 {
        candidates[0].clone()
    } else {
        println!("Several USBTMC devices found:");
        for (i, path) in candidates.iter().enumerate() {
            println!("  {i}. {}", path.display());
        }
        print!("Select device [0]: ");
        io::stdout().flush()?;
        let mut line = String::new();
        io::stdin().read_line(&mut line)?;
        let index = line.trim().parse::<usize>().unwrap_or(0);
        candidates[index.min(candidates.len() - 1)].clone()
    };

    let mut meter = ScpiInstrument::open(&device)?;
    println!("{} connected.", device.display());

    // Battery-powered handheld meters stay in local mode (ignoring SCPI)
    // until the host asserts USB488 Remote Enable.
    if let Err(e) = enable_remote_mode(&meter.dev) {
        println!("warning: REN not asserted ({e}); continuing anyway");
    }

    // Read the identification string.
    let idn = meter.query("*IDN?")?;
    println!("IDN: {idn}");

    if opts.configure {
        // Set the wavelength (unit: nm) and verify it was accepted.
        meter.command(&format!(
            "SENSE:CORRECTION:WAVELENGTH {}",
            opts.wavelength_nm
        ))?;
        let wavelength = meter.query_f64("SENSE:CORRECTION:WAVELENGTH?")?;
        if (wavelength - opts.wavelength_nm).abs() < 0.5 {
            println!("The wavelength is set to {wavelength} nm");
        } else {
            println!("Fail to set the wavelength.");
            check_error(&mut meter);
        }

        // Set the averaging rate and verify it was accepted.
        meter.command(&format!("SENSE:AVERAGE {}", opts.average))?;
        let average = meter.query_f64("SENSE:AVERAGE?")?;
        if average == f64::from(opts.average) {
            println!("The average rate is set to {average}");
        } else {
            println!("Fail to set the average rate.");
            check_error(&mut meter);
        }
    }

    // ---------------------------------------------------------------------------
    // 1. Blocking one-shot acquisition (MEASure?)
    //    Re-triggers the ADC for every sample and blocks until data is ready.
    // ---------------------------------------------------------------------------
    println!("--- [1/2] Blocking one-shot acquisition (MEASure?) ---");
    println!("Reading {} power samples...", opts.samples);
    let mut raw_powers = Vec::with_capacity(opts.samples);

    for i in 0..opts.samples {
        let power = meter.query_f64("MEASURE:POWER?")?;
        raw_powers.push(power);

        // Read the temperature non-invasively (last value, ~1-2 Hz refresh)
        // with SENS1:TEMP:DATA?. Firmware quirk: the short-form spelling
        // with an explicit suffix ("SENS1:TEMP:DATA?") is mandatory. The
        // long form SENSe:TEMPerature:DATA? (no suffix) or a non-existent
        // channel (e.g. SENS3) never answers on PM100D2 fw 1.0.7, and the
        // resulting read timeout wedges the whole remote interface.
        let temperature = meter.query_f64("SENS1:TEMP:DATA?")?;
        let millis = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .expect("Time went backwards")
            .as_millis();

        println!("Sample [{millis}] {i:>2}: {power:12.6e} W temp:{temperature:.2}");

        if i + 1 < opts.samples && opts.interval > Duration::ZERO {
            sleep(opts.interval);
        }
    }
    print_stats("MEAS?  ", &raw_powers);

    // ---------------------------------------------------------------------------
    // 2. Continuous non-blocking acquisition (INITiate:CONTinuous + FETCh?)
    //    Standard flow from the manual's "Continuous Measurements" section:
    //    ABOR → CONF:POW → INIT:CONT → loop { poll FETC:STAT?, fetch } → ABOR
    // ---------------------------------------------------------------------------

    println!("\n--- [2/2] Continuous non-blocking acquisition (INIT:CONT + FETC:BINA?) ---");

    // A. Stop any running measurement and flush the result queue (the device
    //    queues at most 10 results).
    meter.command("ABORT")?;

    // B. Explicitly configure the measurement unit to power. This is required:
    //    FETCh returns data for whatever unit was configured last, so without
    //    it the loop would fetch the temperature left over from part 1!
    meter.command("CONF:POW")?;

    // C. Start continuous acquisition: the meter keeps pushing results into an
    //    internal queue (INIT:CONT is a start action without an ON/OFF
    //    parameter; stopping is done with ABOR).
    meter.command("INIT:CONT")?;

    println!(
        "Reading {} power samples in continuous mode...",
        opts.samples
    );
    let mut powers = Vec::with_capacity(opts.samples);

    for i in 0..opts.samples {
        // D.1 Poll FETC:STAT? until the queue holds a result (5 s guard timeout).
        let mut ready = false;
        for _ in 0..250 {
            if meter.query_f64("FETC:STAT?")? == 1.0 {
                ready = true;
                break;
            }
            sleep(Duration::from_millis(20));
        }
        if !ready {
            eprintln!("  [Warn] Sample {i}: no data ready within 5 s, aborting");
            break;
        }
        let temperature = meter.query_f64("SENS1:TEMP:DATA?")?;
        // D.2 Binary fetch: offset=0, timeout=1000 ms, bitmask=0 → just a
        //     4-byte IEEE 754 little-endian float. Use bitmask=1 to also get
        //     a timestamp (4-byte uint32 µs + 4-byte float).
        let raw_bytes: Vec<u8> = meter.query_bytes("FETC:BINA? 0,1000,0")?;

        // D.3 Validate the length and convert the little-endian float, mapping
        //     out-of-range (Inf) / invalid (NaN) readings to None.
        let power = if raw_bytes.len() >= 4 {
            let le_bytes: [u8; 4] = raw_bytes[0..4].try_into().unwrap();
            let raw_val = f32::from_le_bytes(le_bytes) as f64;
            if raw_val.is_finite() {
                Some(raw_val)
            } else {
                eprintln!("  [Warning] Sample {i}: out of range / invalid (Inf/NaN)");
                None
            }
        } else {
            eprintln!(
                "  [Error] Sample {i}: short binary response ({} bytes)",
                raw_bytes.len()
            );
            None
        };

        if let Some(p) = power {
            powers.push(p);
        }

        let millis = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .expect("Time went backwards")
            .as_millis();

        // Power and temperature are printed together: the power comes from the
        // measurement queue (timestamped), the temperature is the last value
        // from SENS1:TEMP:DATA? (~1-2 Hz refresh, quasi-synchronous).
        match power {
            Some(p) => println!("Sample [{millis}] {i:>2}: {p:.6E} W temp: {temperature}"),
            None => println!("Sample [{millis}] {i:>2}: [OVERRANGE/INVALID]"),
        }

        // E. In continuous mode the host controls the sampling pace with sleep
        //    (the queue only holds 10 results, so sleeping too long drops
        //    data; remove the sleep for high-speed acquisition).
        if i + 1 < opts.samples && opts.interval > Duration::ZERO {
            sleep(opts.interval);
        }
    }

    // G. Acquisition done: ABOR stops the continuous measurement and flushes
    //    the queue.
    meter.command("ABORT")?;

    print_stats("INIT:CONT", &powers);

    println!("Program finishes.");
    Ok(())
}

/// Print mean/min/max statistics for a set of power samples.
fn print_stats(tag: &str, powers: &[f64]) {
    if powers.is_empty() {
        return;
    }
    let mean = powers.iter().sum::<f64>() / powers.len() as f64;
    let min = powers.iter().cloned().fold(f64::INFINITY, f64::min);
    let max = powers.iter().cloned().fold(f64::NEG_INFINITY, f64::max);
    println!(
        "\n[{tag}] Mean power: {mean:.6e} W (min {min:.6e}, max {max:.6e}, n={})",
        powers.len()
    );
}
/// Print the oldest entry of the instrument's error queue for diagnostics.
fn check_error(meter: &mut ScpiInstrument) {
    match meter.query("SYSTem:ERRor?") {
        Ok(resp) => println!("  SYST:ERR? -> {resp}"),
        Err(e) => println!("  (SYST:ERR? failed: {e})"),
    }
}
