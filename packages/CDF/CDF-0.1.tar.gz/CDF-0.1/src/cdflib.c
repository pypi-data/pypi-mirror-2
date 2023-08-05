/******************************************************************************
*
*  NSSDC/CDF                                    INTERNAL interface to CDF.
*
*  Version 2.7a, 22-Sep-95, Hughes STX.
*
*  Modification history:
*
*   V1.0  22-Jan-91, R Kulkarni/J Love  Original version (for CDF V2.0).
*
*   V2.0   6-Jun-91, J Love             Renamed (was cdfcore.c). Modified for 
*                                       V2.1 style INTERNAL interface (and
*                                       fixes to CDF V2.0 distribution).  Also
*                                       renamed some symbols for clarity.
*   V2.1  24-Jun-91, J Love             Fixed PUT_,VAR_INITIALRECS.  Stripped
*                                       trailing blanks off of CDF names. 
*                                       Allow variable data type to be changed
*                                       if "equivalent".  Added CDF_EPOCH as
*                                       a data type.
*   V2.2   8-Aug-91, J Love             Don't use #elif (for SGi port) and
*                                       added support for Cray/UNICOS.
*                                       INTERNAL i/f function renamed 'CDFlib'.
*                                       Different numbers of CACHE buffers for
*                                       different file types (VIO).  Modified
*                                       hyper access (and fixed part of it).
*                                       Changed attribute entry access.  Check
*                                       for supported encoding when opening a
*                                       CDF.
*   V2.3  20-May-92, J Love             Changed for IBM-PC port (split into
*                                       smaller source files, etc.).  Made
*                                       shareable.
*   V2.4  21-Aug-92, J Love             CDF V2.3 (shareable/NeXT/zVar).
*   V2.5  19-Jan-94, J Love             CDF V2.4.
*   V2.6  15-Dec-94, J Love             CDF V2.5.
*   V2.6a 24-Feb-95, J Love		Solaris 2.3 IDL i/f.
*   V2.7  19-Jul-95, J Love		Virtual memory (Microsoft C 7.00).
*   V2.7a 22-Sep-95, J Love		Changed virtual memory control.
*
******************************************************************************/

#define CDFLIB
#include "cdflib.h"

static struct CURstruct Cur = { RESERVED_CDFID, RESERVED_CDFSTATUS };

#if defined(MICROSOFTC_700) && INCLUDEvMEMORY
static Logical first = TRUE;
#endif

/******************************************************************************
*  Interface to CDF internal structures and data/meta-data.
******************************************************************************/

#if defined(STDARG)
STATICforIDL CDFstatus CDFlib (long requiredFnc, ...)
#else
STATICforIDL CDFstatus CDFlib (va_alist)
va_dcl
#endif
{
CDFstatus pStatus = CDF_OK;
struct VAstruct Va;

/******************************************************************************
*  Process variable length argument list.
******************************************************************************/

#if defined(STDARG)
va_start (Va.ap, requiredFnc);
Va.fnc = requiredFnc;
#else
VA_START (Va.ap);
Va.fnc = va_arg (Va.ap, long);
#endif

#if defined(MICROSOFTC_700) && INCLUDEvMEMORY
if (first) {
  char *vsize = getenv("CDF_VSIZE");
  if (vsize != NULL) {
    long nBytes;
    if (sscanf(vsize,"%ld",&nBytes) == 1) {
      switch (nBytes) {
	case 0:
	  useVmem = FALSE;
	  break;
	case DEFAULT_vMEMSIZE:
	  useVmem = TRUE;
	  vMemSize = DEFAULT_vMEMSIZE;
	  break;
	default:
	  useVmem = FALSE;	/* Until the mystery is solved... */
	  vMemSize = nBytes;
      }
      if (useVmem) {
	char *vmask = getenv("CDF_VMASK");
	if (vmask != NULL) {
	  unsigned int tMask = 0;
	  if (strstr(vmask,"EMS") != NULL ||
	      strstr(vmask,"ems") != NULL) tMask |= _VM_EMS;
	  if (strstr(vmask,"XMS") != NULL ||
	      strstr(vmask,"xms") != NULL) tMask |= _VM_XMS;
	  if (strstr(vmask,"DISK") != NULL ||
	      strstr(vmask,"disk") != NULL) tMask |= _VM_DISK;
	  if (tMask != 0) vMemMask = tMask;
        }
      }
    }
  }
  first = FALSE;
}
#endif

while (Va.fnc != NULL_) {
  switch (Va.fnc) {
    case CREATE_:
      for (;;) {
	 Va.item = va_arg (Va.ap, long);
	 if (!sX(CDFcre(&Va,&Cur),&pStatus)) return pStatus;
	 if (Va.fnc == Va.item) break;
      }
      break;

    case OPEN_:
      for (;;) {
	 Va.item = va_arg (Va.ap, long);
	 if (!sX(CDFope(&Va,&Cur),&pStatus)) return pStatus;
	 if (Va.fnc == Va.item) break;
      }
      break;
 
    case DELETE_:
      for (;;) {
	 Va.item = va_arg (Va.ap, long);
	 if (!sX(CDFdel(&Va,&Cur),&pStatus)) return pStatus;
	 if (Va.fnc == Va.item) break;
      }
      break;

    case CLOSE_:
      for (;;) {
	 Va.item = va_arg (Va.ap, long);
	 if (!sX(CDFclo(&Va,&Cur),&pStatus)) return pStatus;
	 if (Va.fnc == Va.item) break;
      }
      break;

    case SELECT_:
      for (;;) {
	 Va.item = va_arg (Va.ap, long);
	 if (!sX(CDFsel(&Va,&Cur),&pStatus)) return pStatus;
	 if (Va.fnc == Va.item) break;
      }
      break;

    case CONFIRM_:
      for (;;) {
	 Va.item = va_arg (Va.ap, long);
	 if (!sX(CDFcon(&Va,&Cur),&pStatus)) return pStatus;
	 if (Va.fnc == Va.item) break;
      }
      break;

    case GET_:
      for (;;) {
	 Va.item = va_arg (Va.ap, long);
	 if (!sX(CDFget(&Va,&Cur),&pStatus)) return pStatus;
	 if (Va.fnc == Va.item) break;
      }
      break;

    case PUT_:
      for (;;) {
	 Va.item = va_arg (Va.ap, long);
	 if (!sX(CDFput1(&Va,&Cur),&pStatus)) return pStatus;
	 if (Va.fnc == Va.item) break;
      }
      break;

    default: {
      va_end (Va.ap);
      return BAD_FNC_OR_ITEM;
    }
  }
}
va_end (Va.ap);
return pStatus;
}
