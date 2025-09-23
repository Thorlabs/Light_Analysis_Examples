"""
Example Thorlabs Power Meter raw ethernet socket communication
Example Date of Creation                            2024-08-07
Example Date of Last Modification on Github         2024-08-07
Version of Python                                   3.11.2
Version of the Thorlabs SDK used                    none
==================
This examples shows how to communicate with a Thorlabs ethernet capable
Power Meter using raw python socket communication. The sample implements
the binary framing protocol to transfer SCPI request and response data
as payload.
"""
import struct
import socket

#Maximal size of a TCP segment of the Thorlabs power meter
TCP_MAX_SEG_SIZE = 1440
#Size of the header in bytes of a TCP segment of the Thorlabs power meter
TL_TCP_SEG_HEADER_SIZE = 4
#Maximal amount of payload bytes for a single frame
MAX_FRAME_LEN = TCP_MAX_SEG_SIZE - TL_TCP_SEG_HEADER_SIZE

def TL_TCP_frame_transmit_bin(socket: socket, request: bytearray):
    """
    Transmits a binary request to the Thorlabs power meter. 
    The request is split into multiple frames if it is too large.

    :param socket: The openend socket to use for transmission
    :param request: The binary request to transmit to power meter
    """
    reqLen = len(request)
    writtenBytes = 0
    frameCnt = 0
    while writtenBytes < reqLen:
        #Limit max lenth of request
        frameLen = reqLen - writtenBytes
        if frameLen > MAX_FRAME_LEN:
            frameLen = MAX_FRAME_LEN

        binReq = []
        if frameCnt == 0:
            binReq = struct.pack('<cch', bytes([0xCA]), bytes([frameCnt]), reqLen)
            binReq = binReq + request[writtenBytes : frameLen]
        else:
            binReq = struct.pack('<cch', bytes([0xCB]), bytes([frameCnt]), frameLen)
            binReq = binReq + request[writtenBytes : writtenBytes+frameLen]

        #Send segment to server
        socket.sendall(binReq)

        frameCnt += 1
        writtenBytes += frameLen

def TL_TCP_frame_receive_bin(socket: socket):
    """
    Receives a binary response from the Thorlabs power meter.
    The response is assembled from multiple frames.
    You might want to set the timeout of the socket 
    to avoid endless blocking. See socket.settimeout().
    If there has been an enour request send before, the 
    function will also return a timeout error.

    :param socket: The openend socket to use for reception
    :return: The binary response from power meter
    """
    resp = bytearray()
    respIdx = 0
    
    respHeader = bytearray(TL_TCP_SEG_HEADER_SIZE)
    respHeaderLen = 0
    respHeadSeq = 0

    respBinSegLen = 0
    respBinTotalLen = 0

    while True:
        data = socket.recv(1500)
        #Iterate all received bytes
        for d in data:
            #Already parsed frame start header?
            if respBinTotalLen == 0:
                #Waiting for start of frame header
                if d != 0xCA and respHeaderLen == 0:
                    continue
                respHeader[respHeaderLen] = d
                respHeaderLen += 1
                
                #Parsed entire header?
                if respHeaderLen == TL_TCP_SEG_HEADER_SIZE:
                    #Verify header?
                    if respHeader[1] != 0:
                        respBinSegLen = respBinTotalLen = 0
                    else:
                        respBinSegLen = respBinTotalLen = struct.unpack('<h', respHeader[2:4])[0]
                        if respBinSegLen > MAX_FRAME_LEN:
                            respBinSegLen = MAX_FRAME_LEN
                        respHeadSeq = 1
                        resp = bytearray(respBinTotalLen)
                        respIdx = 0
                    
                    #Finally reset header parsing memory
                    respHeaderLen = 0
            else:
                #Wait for start of conintous header?
                if respBinSegLen == 0:
                    #Wait for start of continous frame
                    if d != 0xCB and respHeaderLen == 0:
                        continue
                    respHeader[respHeaderLen] = d
                    respHeaderLen += 1
                    
                    #Parsed entire header?
                    if respHeaderLen == TL_TCP_SEG_HEADER_SIZE:
                        #Verify header sequence number
                        if respHeader[1] != respHeadSeq:
                            respBinSegLen = respBinTotalLen = 0
                        else:
                            respBinSegLen = struct.unpack('<h', respHeader[2:4])[0]
                            respHeadSeq += 1

                            #Ensure segment size is not larger than expected total payload
                            if respBinSegLen > respBinTotalLen:
                                respBinSegLen = respBinTotalLen = 0

                            #Empty header? We are done -> go back to init
                            if respBinSegLen == 0:
                                respBinSegLen = respBinTotalLen = 0

                        #Finally reset header parsing memory
                        respHeaderLen = 0

                else:
                    #Append data to response
                    resp[respIdx] = d
                    respIdx += 1
                    respBinSegLen -= 1
                    respBinTotalLen -= 1

                    if respBinTotalLen == 0:
                        return resp

def TL_TCP_frame_receive(socket: socket):
    """
    Receives a text response from the Thorlabs power meter.
    The response is assembled from multiple frames.
    For closer details read TL_TCP_frame_receive_bin() 
    comments.

    :param socket: The openend socket to use for reception
    """
    binResp = TL_TCP_frame_receive_bin(socket)
    return binResp.decode('ASCII')

def TL_TCP_frame_transmit(socket: socket, req:str):
    """
    Transmits a text request to the Thorlabs power meter..
    The request is split into multiple frames if it is too large.
    
    :param socket: The openend socket to use for transmission
    :param req: The text request to transmit to power meter
    """
    return TL_TCP_frame_transmit_bin(socket, req.encode('ASCII'))

def TL_TCP_query(socket: socket, req:str):
    """
     Sends a text request to the Thorlabs power meter and returns the text response.

    :param socket: The openend socket to use for transmission
    :param req: The text request to transmit to power meter
    """
    TL_TCP_frame_transmit(socket, req)
    return TL_TCP_frame_receive(socket).strip()

def TL_TCP_query_bin(socket: socket, req:str):
    """
    Sends a text request to the Thorlabs power meter and returns the binary response.

    :param socket: The openend socket to use for transmission
    :param req: The text request to transmit to power meter
    """    
    TL_TCP_frame_transmit(socket, req)
    return TL_TCP_frame_receive_bin(socket)

if __name__ == '__main__':
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        #Set connection timeout
        s.settimeout(2)
        #Connect to PM with given IP and port number. Default port is 2000.
        s.connect(("10.10.4.22", 2000))
        
        #Set read timeout
        s.settimeout(1)
        print(TL_TCP_query(s,"*IDN?\n"))
        print(TL_TCP_query(s,"SYST:ERR?\n"))