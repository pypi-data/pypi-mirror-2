/******************************************************************************
*
*  NSSDC/CDF                 EPOCH utility routines for Fortran applications.
*
*  Version 1.1, 13-Jun-95, Hughes STX.
*
*  Modification history:
*
*   V1.0   7-Nov-94, J Love	Original version.
*   V1.1  13-Jun-95, J Love	EPOCH custom format.  Linux.
*
******************************************************************************/

#include "cdflib.h"

/******************************************************************************
* parse_EPOCH (FORTRAN equivalent of parseEPOCH).
******************************************************************************/

Fif_PREFIXa
void
Fif_PREFIXb
Fif_ENTRYPOINT(parse_epoch__,parse_epoch_,parse_epoch,PARSE_EPOCH)
(string, epoch Fif_GHOSTARG(string_len))
void *string;
double *epoch;
Fif_GHOSTDEF(string_len)
{
  struct STRINGstruct *ssh = NULL;
#if defined(Fif_DESCR)
  *epoch = parseEPOCH (DESCRtoREFnul(string,EPOCH_STRING_LEN,&ssh));
#endif
#if defined(Fif_GHOSTLEN)
  *epoch = parseEPOCH (NULterminate(string,Fif_GHOSTUSE(string_len),&ssh));
#endif
#if defined(Fif_NOLEN)
  *epoch = parseEPOCH (FindEndNUL(string,EPOCH_STRING_LEN,&ssh));
#endif
  FreeStrings (ssh);
  return;
}

/******************************************************************************
* encode_EPOCH (FORTRAN equivalent of encodeEPOCH).
******************************************************************************/

Fif_PREFIXa
void
Fif_PREFIXb
Fif_ENTRYPOINT(encode_epoch__,encode_epoch_,encode_epoch,ENCODE_EPOCH)
(epoch, string Fif_GHOSTARG(string_len))
double *epoch;
void *string;
Fif_GHOSTDEF(string_len)
{
  char tString[EPOCH_STRING_LEN+1];
  encodeEPOCH (*epoch, tString);
#if defined(Fif_GHOSTLEN)
  CtoFORTstring (tString, string, Fif_GHOSTUSE(string_len));
#else
  CtoFORTstring (tString, string, EPOCH_STRING_LEN);
#endif
  return;
}

/******************************************************************************
* encode_EPOCH1 (FORTRAN equivalent of encodeEPOCH1).
******************************************************************************/

Fif_PREFIXa
void
Fif_PREFIXb
Fif_ENTRYPOINT(encode_epoch1__,encode_epoch1_,encode_epoch1,ENCODE_EPOCH1)
(epoch, string Fif_GHOSTARG(string_len))
double *epoch;
void *string;
Fif_GHOSTDEF(string_len)
{
  char tString[EPOCH1_STRING_LEN+1];
  encodeEPOCH1 (*epoch, tString);
#if defined(Fif_GHOSTLEN)
  CtoFORTstring (tString, string, Fif_GHOSTUSE(string_len));
#else
  CtoFORTstring (tString, string, EPOCH1_STRING_LEN);
#endif
  return;
}

/******************************************************************************
* encode_EPOCH2 (FORTRAN equivalent of encodeEPOCH2).
******************************************************************************/

Fif_PREFIXa
void
Fif_PREFIXb
Fif_ENTRYPOINT(encode_epoch2__,encode_epoch2_,encode_epoch2,ENCODE_EPOCH2)
(epoch, string Fif_GHOSTARG(string_len))
double *epoch;
void *string;
Fif_GHOSTDEF(string_len)
{
  char tString[EPOCH2_STRING_LEN+1];
  encodeEPOCH2 (*epoch, tString);
#if defined(Fif_GHOSTLEN)
  CtoFORTstring (tString, string, Fif_GHOSTUSE(string_len));
#else
  CtoFORTstring (tString, string, EPOCH2_STRING_LEN);
#endif
  return;
}

/******************************************************************************
* encode_EPOCH3 (FORTRAN equivalent of encodeEPOCH3).
******************************************************************************/

Fif_PREFIXa
void
Fif_PREFIXb
Fif_ENTRYPOINT(encode_epoch3__,encode_epoch3_,encode_epoch3,ENCODE_EPOCH3)
(epoch, string Fif_GHOSTARG(string_len))
double *epoch;
void *string;
Fif_GHOSTDEF(string_len)
{
  char tString[EPOCH3_STRING_LEN+1];
  encodeEPOCH3 (*epoch, tString);
#if defined(Fif_GHOSTLEN)
  CtoFORTstring (tString, string, Fif_GHOSTUSE(string_len));
#else
  CtoFORTstring (tString, string, EPOCH3_STRING_LEN);
#endif
  return;
}

/******************************************************************************
* encode_EPOCHx (FORTRAN equivalent of encodeEPOCHx).
******************************************************************************/

Fif_PREFIXa
void
Fif_PREFIXb
Fif_ENTRYPOINT(encode_epochx__,encode_epochx_,encode_epochx,ENCODE_EPOCHX)
(epoch, format, string Fif_GHOSTARG(format_len) Fif_GHOSTARG(string_len))
double *epoch;
void *format;
void *string;
Fif_GHOSTDEF(format_len)
Fif_GHOSTDEF(string_len)
{
  struct STRINGstruct *ssh = NULL;
  char tString[EPOCHx_STRING_MAX+1];
#if defined(Fif_DESCR)
  encodeEPOCHx (*epoch, DESCRtoREFnul(format,EPOCHx_FORMAT_MAX,&ssh), tString);
#endif
#if defined(Fif_GHOSTLEN)
  encodeEPOCHx (*epoch, NULterminate(format,Fif_GHOSTUSE(format_len),&ssh),
		tString);
#endif
#if defined(Fif_NOLEN)
  encodeEPOCHx (*epoch, FindEndNUL(format,EPOCHx_FORMAT_MAX,&ssh), tString);
#endif
#if defined(Fif_GHOSTLEN)
  CtoFORTstring (tString, string, Fif_GHOSTUSE(string_len));
#else
  CtoFORTstring (tString, string, EPOCHx_STRING_MAX);
#endif
  return;
}

/******************************************************************************
* EPOCH_breakdown (FORTRAN equivalent of EPOCHbreakdown).
*   Callable from FORTRAN -- conforms to Fortran version of this function as
* described in CDF version 1 Implementer's Guide.
******************************************************************************/

Fif_PREFIXa
void
Fif_PREFIXb
Fif_ENTRYPOINT(epoch_breakdown__,
	       epoch_breakdown_,
	       epoch_breakdown,
	       EPOCH_BREAKDOWN)
(epoch, year, month, day, hour, minute, second, msec)
double *epoch;
Int32 *year;
Int32 *month;
Int32 *day;
Int32 *hour;
Int32 *minute;
Int32 *second;
Int32 *msec;
{
  double tEpoch = *epoch;
  long tYear, tMonth, tDay, tHour, tMinute, tSecond, tMsec;
  EPOCHbreakdown (tEpoch, &tYear, &tMonth, &tDay, &tHour, &tMinute, &tSecond,
		  &tMsec);
  *year = (Int32) tYear;
  *month = (Int32) tMonth;
  *day = (Int32) tDay;
  *hour = (Int32) tHour;
  *minute = (Int32) tMinute;
  *second = (Int32) tSecond;
  *msec = (Int32) tMsec;
  return;
}

/******************************************************************************
* compute_EPOCH (FORTRAN equivalent of computeEPOCH).
*   Callable from FORTRAN -- conforms to Fortran version of this function as
* described in CDF version 1 Implementer's Guide.
******************************************************************************/

Fif_PREFIXa
void
Fif_PREFIXb
Fif_ENTRYPOINT(compute_epoch__,compute_epoch_,compute_epoch,COMPUTE_EPOCH)
(year, month, day, hour, minute, second, msec, epoch)
Int32 *year;
Int32 *month;
Int32 *day;
Int32 *hour;
Int32 *minute;
Int32 *second;
Int32 *msec;
double *epoch;
{
  *epoch = computeEPOCH ((long) *year, (long) *month, (long) *day,
			 (long) *hour, (long) *minute, (long) *second,
			 (long) *msec);
  return;
}
