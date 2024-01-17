## Included Example

### WFS_Matlab
This example shows how to initialize the wavefront sensor and configure the attached microlens array. This also goes through the suggested process for acquiring spotfield images and outputting calculation data like centroid and wavefront values. 

The code uses the C library DLL file for the Wavefront Sensor.

In order to avoid error messages, comment out the “__fastcall” and “signed” calling conventions in the header file “visatype.h”
in the folder: C:\Program Files\IVI Foundation\VISA\Win64\Include

```C
/*---------------------------------------------------------------------------*/
/* Distributed by IVI Foundation Inc. */
/* */
/* Do not modify the contents of this file. */
/*---------------------------------------------------------------------------*/
/* */
/* Title : VISATYPE.H */
/* Date : 05-12-2009 */
/* Purpose : Fundamental VISA data types and macro definitions */
/* */
/*---------------------------------------------------------------------------*/
#ifndef __VISATYPE_HEADER__
#define __VISATYPE_HEADER__
#if defined(_WIN64)
#define _VI_FAR
#define _VI_FUNC                     //__fastcall
#define _VI_FUNCC                    //__fastcall
#define _VI_FUNCH                    //__fastcall
#define _VI_SIGNED                   //signed
#elif (defined(WIN32) || defined(_WIN32) || defined(__WIN32__) || defined(__NT__)) &&
!defined(_NI_mswin16_)
#define _VI_FAR
.
.
.

```
