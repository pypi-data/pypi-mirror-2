/******************************************************************************
*
*  NSSDC/CDF                                           CDF `close' operations.
*
*  Version 1.4, 20-Jul-95, Hughes STX.
*
*  Modification history:
*
*   V1.0  20-May-92, J Love     Original version (was part of `cdflib.c').
*   V1.1  21-Aug-92, J Love     CDF V2.3 (shareable/NeXT/zVar).
*   V1.2   7-Dec-93, J Love     CDF V2.4.  Added zMode.
*   V1.3  15-Nov-94, J Love     CDF V2.5.
*   V1.3a 24-Feb-95, J Love	Solaris 2.3 IDL i/f.
*   V1.4  20-Jul-95, J Love	CDFexport-related changes.
*
******************************************************************************/

#include "cdflib.h"

/******************************************************************************
* CDFclo.
******************************************************************************/

STATICforIDL CDFstatus CDFclo (Va, Cur)
struct VAstruct *Va;
struct CURstruct *Cur;
{
  CDFstatus pStatus = CDF_OK;
  switch (Va->item) {
    /**************************************************************************
    * CDF_
    *   Close a CDF.  Note that the memory associated with the CDF is freed
    * before checking the status code from `CloseCDFfiles'.
    **************************************************************************/
    case CDF_: {
      struct cdfSTRUCT *CDF;
      SelectCDF (Cur->cdf, CDF, NO_CDF_SELECTED)
      sX (CloseCDFfiles(CDF,NULL), &pStatus);
      FreeCDFid (CDF);
      Cur->cdf = NULL;
      if (StatusBAD(pStatus)) return pStatus;
      break;
    }
    /**************************************************************************
    * CDFwithSTATS_
    *   Close a CDF and pass back the statistics for the `.cdf' file.  Note
    * that the memory associated with the CDF is freed before checking the
    * status code from `CloseCDFfiles'.
    **************************************************************************/
    case CDFwithSTATS_: {
      vSTATS *vStats = va_arg (Va->ap, vSTATS *);
      struct cdfSTRUCT *CDF;
      SelectCDF (Cur->cdf, CDF, NO_CDF_SELECTED)
      sX (CloseCDFfiles(CDF,vStats), &pStatus);
      FreeCDFid (CDF);
      Cur->cdf = NULL;                         /* No "current" CDF anymore. */
      if (StatusBAD(pStatus)) return pStatus;
      break;
    }
    /**************************************************************************
    * rVAR_/zVAR_
    *    Close the current r/zVariable file.
    **************************************************************************/
    case rVAR_:
    case zVAR_: {
      Logical zOp = (Va->item == zVAR_ ? TRUE : FALSE);
      struct cdfSTRUCT *CDF;
      struct varSTRUCT *Var;
      SelectCDF (Cur->cdf, CDF, NO_CDF_SELECTED)
      if (BADzOP(CDF,!zOp)) return ILLEGAL_IN_zMODE;
      if (!CURRENTvarSELECTED(CDF,zOp)) return NO_VAR_SELECTED;
      if (!sX(LocateCurrentVar(CDF,zOp,NULL,NULL,&Var),&pStatus)) {
	AbortAccess (CDF, FALSE, Cur);
	return pStatus;
      }
      if (CDF->singleFile) {
	if (!sX(SINGLE_FILE_FORMAT,&pStatus)) return pStatus;
      }
      else {
	if (Var != NULL)
	  if (Var->status == VAR_OPENED) {
	    if (!CLOSEv(Var->fp,NULL)) {
	      AbortAccess (CDF, FALSE, Cur);
	      return VAR_CLOSE_ERROR;
	    }
	    Var->status = VAR_CLOSED;
	  }
	  else {
	    if (!sX(VAR_ALREADY_CLOSED,&pStatus)) return pStatus;
	  }
	else {
	  if (!sX(VAR_ALREADY_CLOSED,&pStatus)) return pStatus;
	}
      }
      break;
    }
    /**************************************************************************
    * Unknown item, must be the next function.
    **************************************************************************/
    default: {
      Va->fnc = Va->item;
      break;
    }
  }
  return pStatus;
}
