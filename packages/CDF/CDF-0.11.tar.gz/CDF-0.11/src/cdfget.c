/******************************************************************************
*
*  NSSDC/CDF                                       CDF `get' operations.
*
*  Version 1.3c, 4-Aug-95, Hughes STX.
*
*  Modification history:
*
*   V1.0  20-May-92, J Love     Original version (was part of `cdflib.c').
*   V1.1  16-Sep-92, J Love     CDF V2.3 (shareable/NeXT/zVar).
*   V1.2  13-Dec-93, J Love     CDF V2.4.
*   V1.3  15-Dec-94, J Love     CDF V2.5.
*   V1.3a  9-Jan-95, J Love	Encode/decode changes.  More cache-residency.
*   V1.3b 24-Feb-95, J Love	Solaris 2.3 IDL i/f.
*   V1.3c  4-Aug-95, J Love	CDFexport-related changes.
*
******************************************************************************/

#include "cdflib.h"
#include "cdfrev.h"

/******************************************************************************
* CDFget.
******************************************************************************/

STATICforIDL CDFstatus CDFget (Va, Cur)
struct VAstruct *Va;
struct CURstruct *Cur;
{
CDFstatus tStatus, pStatus = CDF_OK;

switch (Va->item) {
  /****************************************************************************
  * STATUS_TEXT_, 
  ****************************************************************************/

  case STATUS_TEXT_: {
    char *textPtr;
    textPtr = va_arg (Va->ap, char *);
    CDFstatusText (Cur->status, textPtr);
    break;
  }

  /****************************************************************************
  * DATATYPE_SIZE_, 
  ****************************************************************************/

  case DATATYPE_SIZE_: {
    long dataType = va_arg (Va->ap, long);
    long *numBytes = va_arg (Va->ap, long *);
    if (!ValidDataType(dataType)) return BAD_DATA_TYPE;
    *numBytes = (long) CDFelemSize (dataType);
    break;
  }

  /****************************************************************************
  * rVARs_NUMDIMS_/zVAR_NUMDIMS_
  *    Note that inquiring the number of rVariable dimensions is allowed while
  * in zMode.
  ****************************************************************************/

  case rVARs_NUMDIMS_: {
    struct cdfSTRUCT *CDF;
    long *numDims = va_arg (Va->ap, long *);
    SelectCDF (Cur->cdf, CDF, NO_CDF_SELECTED)
    *numDims = CDF->rNumDims;
    break;
  }

  case zVAR_NUMDIMS_: {
    struct cdfSTRUCT *CDF;
    long *numDims = va_arg (Va->ap, long *);
    Logical zVar;
    Int32 offset;
    SelectCDF (Cur->cdf, CDF, NO_CDF_SELECTED)
    if (!CURRENTvarSELECTED(CDF,TRUE)) return NO_VAR_SELECTED;
    if (!sX(LocateCurrentVar(CDF,TRUE,&offset,&zVar,NULL),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    if (!sX(CalcNumDims(CDF,offset,zVar,numDims),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    break;
  }

  /****************************************************************************
  * rVARs_DIMSIZES_/zVAR_DIMSIZES_
  *    Note that inquiring the rVariable dimension sizes is allowed while in
  * zMode.
  ****************************************************************************/

  case rVARs_DIMSIZES_: {
    struct cdfSTRUCT *CDF;
    int dimN;
    long *dimsize = va_arg (Va->ap, long *);
    SelectCDF (Cur->cdf, CDF, NO_CDF_SELECTED)
    for (dimN = 0; dimN < CDF->rNumDims; dimN++) {
       dimsize[dimN] = CDF->rDimSizes[dimN];
    }
    break;
  }

  case zVAR_DIMSIZES_: {
    struct cdfSTRUCT *CDF;
    Logical zVar;
    long *dimSizes = va_arg (Va->ap, long *);
    Int32 offset;
    SelectCDF (Cur->cdf, CDF, NO_CDF_SELECTED)
    if (!CURRENTvarSELECTED(CDF,TRUE)) return NO_VAR_SELECTED;
    if (!sX(LocateCurrentVar(CDF,TRUE,&offset,&zVar,NULL),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    if (!sX(CalcDimSizes(CDF,offset,zVar,dimSizes),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    break;
  }

  /****************************************************************************
  * CDF_ENCODING_, 
  ****************************************************************************/

  case CDF_ENCODING_: {
    struct cdfSTRUCT *CDF;
    long *encoding = va_arg (Va->ap, long *);
    SelectCDF (Cur->cdf, CDF, NO_CDF_SELECTED)
    *encoding = (long) CDF->encoding;
    break;
  }

  /****************************************************************************
  * CDF_MAJORITY_, 
  ****************************************************************************/

  case CDF_MAJORITY_: {
    struct cdfSTRUCT *CDF;
    long *majority = va_arg (Va->ap, long *);
    SelectCDF (Cur->cdf, CDF, NO_CDF_SELECTED)
    *majority = BOO(CDF->rowMajor,ROW_MAJOR,COL_MAJOR);
    break;
  }

  /****************************************************************************
  * CDF_FORMAT_, 
  ****************************************************************************/

  case CDF_FORMAT_: {
    struct cdfSTRUCT *CDF;
    long *format = va_arg (Va->ap, long *);
    SelectCDF (Cur->cdf, CDF, NO_CDF_SELECTED)
    *format = BOO(CDF->singleFile,SINGLE_FILE,MULTI_FILE);
    break;
  }

  /****************************************************************************
  * CDF_COPYRIGHT_
  ****************************************************************************/

  case CDF_COPYRIGHT_: {
    struct cdfSTRUCT *CDF;
    char *copyRight = va_arg (Va->ap,  char *);
    SelectCDF (Cur->cdf, CDF, NO_CDF_SELECTED)
    if (!sX(ReadCDR(CDF,CDR_COPYRIGHT,copyRight,CDR_NULL),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    copyRight[CDF_COPYRIGHT_LEN] = NUL;
    break;
  }

  /****************************************************************************
  * LIB_COPYRIGHT_
  ****************************************************************************/

  case LIB_COPYRIGHT_: {
    char *copyRight = va_arg (Va->ap, char *);
    CDFcopyRight (copyRight);
    break;
  }

  /****************************************************************************
  * CDF_NUMrVARS_/CDF_NUMzVARS_
  *    Inquire number of r/z variables.  When in zMode, the number of
  * rVariables is always zero (0).  (Inquiring the number of rVariables
  * while in zMode is one of the few legal rVariable operations).
  ****************************************************************************/

  case CDF_NUMrVARS_:
  case CDF_NUMzVARS_: {
    Logical zOp = (Va->item == CDF_NUMzVARS_);
    struct cdfSTRUCT *CDF;
    long *numVars = va_arg (Va->ap, long *);
    SelectCDF (Cur->cdf, CDF, NO_CDF_SELECTED)
    if (zModeON(CDF))
      *numVars = BOO(zOp,CDF->NrVars + CDF->NzVars,0);
    else
      *numVars = BOO(zOp,CDF->NzVars,CDF->NrVars);
    break;
  }

  /****************************************************************************
  * CDF_NUMATTRS_, 
  ****************************************************************************/

  case CDF_NUMATTRS_: {
    struct cdfSTRUCT *CDF;
    long *numAttrs = va_arg (Va->ap, long *);
    Int32 tNumAttrs;
    SelectCDF (Cur->cdf, CDF, NO_CDF_SELECTED)
    if (!sX(ReadGDR(CDF,GDR_NUMATTR,&tNumAttrs,GDR_NULL),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    *numAttrs = tNumAttrs;
    break;
  }

  /****************************************************************************
  * CDF_NUMgATTRS_/CDF_NUMvATTRS_
  ****************************************************************************/

  case CDF_NUMvATTRS_:
  case CDF_NUMgATTRS_: {
    Logical gOp = (Va->item == CDF_NUMgATTRS_);
    struct cdfSTRUCT *CDF;
    long *numAttrs = va_arg (Va->ap, long *);
    Int32 totalAttrs, offset, scope;
    int attrX;
    SelectCDF (Cur->cdf, CDF, NO_CDF_SELECTED)
    *numAttrs = 0;
    if (!sX(ReadGDR(CDF,GDR_NUMATTR,&totalAttrs,
			GDR_ADRHEAD,&offset,
			GDR_NULL),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    for (attrX = 0; attrX < totalAttrs; attrX++) {
       if (!sX(ReadADR(CDF,offset,ADR_SCOPE,&scope,ADR_NULL),&pStatus)) {
	 AbortAccess (CDF, FALSE, Cur);
	 return pStatus;
       }
       if ((gOp && GLOBALscope(scope)) ||
	   (!gOp && VARIABLEscope(scope))) (*numAttrs)++;
       if (!sX(ReadADR(CDF,offset,ADR_ADRNEXT,&offset,ADR_NULL),&pStatus)) {
	 AbortAccess (CDF, FALSE, Cur);
	 return pStatus;
       }
    }
    break;
  }

  /****************************************************************************
  * rVARs_MAXREC_/zVARs_MAXREC_
  *    Maximum record number of all of the rVariables/zVariables.  Note that
  * inquiring the maximum rVariable record number is allowed while in zMode.
  ****************************************************************************/

  case rVARs_MAXREC_: {
    struct cdfSTRUCT *CDF;
    long *maxRec = va_arg (Va->ap, long *);
    SelectCDF (Cur->cdf, CDF, NO_CDF_SELECTED)
    if (zModeON(CDF))
      *maxRec = -1;
    else
      *maxRec = CDF->rMaxRec;
    break;
  }

  case zVARs_MAXREC_: {
    struct cdfSTRUCT *CDF;
    long *maxRec = va_arg (Va->ap, long *);
    int varN;
    Int32 offset, tMaxRec;
    SelectCDF (Cur->cdf, CDF, NO_CDF_SELECTED)
    /**************************************************************************
    * If zMode is on, check both rVariables and zVariables.  If zMode is not
    * on, only check the zVariables.
    **************************************************************************/
    if (zModeON(CDF)) {
      if (!sX(ReadGDR(CDF,GDR_zVDRHEAD,&offset,
			  GDR_NULL),&pStatus)) {
	AbortAccess (CDF, FALSE, Cur);
	return pStatus;
      }
      for (varN = 0, *maxRec = CDF->rMaxRec; varN < CDF->NzVars; varN++) {
	 if (CDF->zVars[varN] == NULL) {
	   if (!sX(ReadVDR(CDF,offset,TRUE,
			   VDR_MAXREC,&tMaxRec,VDR_NULL),&pStatus)) {
	     AbortAccess (CDF, FALSE, Cur);
	     return pStatus;
	   }
	   *maxRec = MAXIMUM (*maxRec, tMaxRec);
	 }
	 else
	   *maxRec = MAXIMUM (*maxRec, CDF->zVars[varN]->maxRec);
	 if (!sX(ReadVDR(CDF,offset,TRUE,
			 VDR_VDRNEXT,&offset,VDR_NULL),&pStatus)) {
	   AbortAccess (CDF, FALSE, Cur);
	   return pStatus;
	 }
      }
    }
    else {
      if (!sX(ReadGDR(CDF,GDR_zVDRHEAD,&offset,GDR_NULL),&pStatus)) {
	AbortAccess (CDF, FALSE, Cur);
	return pStatus;
      }
      for (varN = 0, *maxRec = -1; varN < CDF->NzVars; varN++) {
	 if (CDF->zVars[varN] == NULL) {
	   if (!sX(ReadVDR(CDF,offset,TRUE,
			   VDR_MAXREC,&tMaxRec,VDR_NULL),&pStatus)) {
	     AbortAccess (CDF, FALSE, Cur);
	     return pStatus;
	   }
	   *maxRec = MAXIMUM (*maxRec, tMaxRec);
	 }
	 else
	   *maxRec = MAXIMUM (*maxRec, CDF->zVars[varN]->maxRec);
	 if (!sX(ReadVDR(CDF,offset,TRUE,
			 VDR_VDRNEXT,&offset,VDR_NULL),&pStatus)) {
	   AbortAccess (CDF, FALSE, Cur);
	   return pStatus;
	 }
      }
    }
    break;
  }

  /****************************************************************************
  * CDF_VERSION_, 
  ****************************************************************************/

  case CDF_VERSION_: {
    struct cdfSTRUCT *CDF;
    long *version = va_arg (Va->ap, long *);
    Int32 tVersion;
    SelectCDF (Cur->cdf, CDF, NO_CDF_SELECTED)
    if (!sX(ReadCDR(CDF,CDR_VERSION,&tVersion,CDR_NULL),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    *version = tVersion;
    break;
  }

  /****************************************************************************
  * CDF_RELEASE_, 
  ****************************************************************************/

  case CDF_RELEASE_: {
    struct cdfSTRUCT *CDF;
    long *release = va_arg (Va->ap, long *);
    Int32 tRelease;
    SelectCDF (Cur->cdf, CDF, NO_CDF_SELECTED)
    if (!sX(ReadCDR(CDF,CDR_RELEASE,&tRelease,CDR_NULL),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    *release = tRelease;
    break;
  }

  /****************************************************************************
  * CDF_INCREMENT_, 
  ****************************************************************************/

  case CDF_INCREMENT_: {
    struct cdfSTRUCT *CDF;
    long *increment = va_arg (Va->ap, long *);
    Int32 tIncrement;
    SelectCDF (Cur->cdf, CDF, NO_CDF_SELECTED)
    if (!sX(ReadCDR(CDF,CDR_INCREMENT,&tIncrement,CDR_NULL),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    *increment = tIncrement;
    break;
  }

  /****************************************************************************
  * LIB_VERSION_, 
  ****************************************************************************/

  case LIB_VERSION_: {
    long *version = va_arg (Va->ap, long *);
    *version = CDF_LIBRARY_VERSION;
    break;
  }

  /****************************************************************************
  * LIB_RELEASE_, 
  ****************************************************************************/

  case LIB_RELEASE_: {
    long *release = va_arg (Va->ap, long *);
    *release = CDF_LIBRARY_RELEASE;
    break;
  }

  /****************************************************************************
  * LIB_INCREMENT_, 
  ****************************************************************************/

  case LIB_INCREMENT_: {
    long *increment = va_arg (Va->ap, long *);
    *increment = CDF_LIBRARY_INCREMENT;
    break;
  }

  /****************************************************************************
  * LIB_subINCREMENT_, 
  ****************************************************************************/

  case LIB_subINCREMENT_: {
    char *subincrement = va_arg (Va->ap, char *);
    *subincrement = CDF_LIBRARY_subINCREMENT;
    break;
  }

  /****************************************************************************
  * rVAR_NAME_/zVAR_NAME_
  *    Note that a temporary variable is used when reading the variable name.
  * This is because the caller may have only allocated enough memory for the
  * size name they expect (ie., less than CDF_VAR_NAME_LEN characters).  Since
  * the variable name is NUL-terminated in the CDF, only the actual characters
  * of the name will be copied to the caller's buffer.
  ****************************************************************************/

  case rVAR_NAME_:
  case zVAR_NAME_: {
    Logical zOp = (Va->item == zVAR_NAME_), zVar;
    struct cdfSTRUCT *CDF;
    char *varName = va_arg (Va->ap,  char *), tName[CDF_VAR_NAME_LEN+1];
    Int32 offset;
    SelectCDF (Cur->cdf, CDF, NO_CDF_SELECTED)
    if (BADzOP(CDF,!zOp)) return ILLEGAL_IN_zMODE;
    if (!CURRENTvarSELECTED(CDF,zOp)) return NO_VAR_SELECTED;
    if (!sX(LocateCurrentVar(CDF,zOp,&offset,&zVar,NULL),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    if (!sX(ReadVDR(CDF,offset,zVar,VDR_NAME,tName,VDR_NULL),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    strcpyX (varName, tName, CDF_VAR_NAME_LEN);
    break;
  }

  /****************************************************************************
  * rVAR_DATATYPE_/zVAR_DATATYPE_
  *    If this for an rVarible named "EPOCH" in a CDF prior to CDF V2.1.1,
  * then return the CDF_EPOCH data type if the actual data type is CDF_REAL8
  * or CDF_DOUBLE.  (The CDF_EPOCH data type was not introduced until CDF
  * V2.1.1).  Note that only rVariables were supported prior to CDF V2.3.
  ****************************************************************************/

  case rVAR_DATATYPE_:
  case zVAR_DATATYPE_: {
    Logical zOp = (Va->item == zVAR_DATATYPE_), zVar;
    struct cdfSTRUCT *CDF;
    long *dataType = va_arg (Va->ap, long *);
    Int32 tDataType, offset;
    SelectCDF (Cur->cdf, CDF, NO_CDF_SELECTED)
    if (BADzOP(CDF,!zOp)) return ILLEGAL_IN_zMODE;
    if (!CURRENTvarSELECTED(CDF,zOp)) return NO_VAR_SELECTED;
    if (!sX(LocateCurrentVar(CDF,zOp,&offset,&zVar,NULL),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    if (!sX(ReadVDR(CDF,offset,zVar,VDR_DATATYPE,
		    &tDataType,VDR_NULL),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    if (!zVar && CDF->fakeEPOCH) {
      char varName[CDF_VAR_NAME_LEN+1];
      if (!sX(ReadVDR(CDF,offset,zVar,VDR_NAME,varName,VDR_NULL),&pStatus)) {
	AbortAccess (CDF, FALSE, Cur);
	return pStatus;
      }
      if (!strcmpITB(varName,"EPOCH") && FLOAT8dataType(tDataType)) {
	tDataType = CDF_EPOCH;
      }
    }
    *dataType = tDataType;
    break;
  }

  /****************************************************************************
  * rVAR_NUMELEMS_/zVAR_NUMELEMS_, 
  ****************************************************************************/

  case rVAR_NUMELEMS_:
  case zVAR_NUMELEMS_: {
    Logical zOp = (Va->item == zVAR_NUMELEMS_), zVar;
    struct cdfSTRUCT *CDF;
    long *numElements = va_arg (Va->ap, long *);
    Int32 offset, tNumElems;
    SelectCDF (Cur->cdf, CDF, NO_CDF_SELECTED)
    if (BADzOP(CDF,!zOp)) return ILLEGAL_IN_zMODE;
    if (!CURRENTvarSELECTED(CDF,zOp)) return NO_VAR_SELECTED;
    if (!sX(LocateCurrentVar(CDF,zOp,&offset,&zVar,NULL),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    if (!sX(ReadVDR(CDF,offset,zVar,VDR_NUMELEMS,
		    &tNumElems,VDR_NULL),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    *numElements = tNumElems;
    break;
  }

  /****************************************************************************
  * rVAR_RECVARY_/zVAR_RECVARY_, 
  ****************************************************************************/

  case rVAR_RECVARY_:
  case zVAR_RECVARY_: {
    Logical zOp = (Va->item == zVAR_RECVARY_), zVar;
    struct cdfSTRUCT *CDF;
    long *recVary = va_arg (Va->ap, long *);
    Int32 flags, offset;
    SelectCDF (Cur->cdf, CDF, NO_CDF_SELECTED)
    if (BADzOP(CDF,!zOp)) return ILLEGAL_IN_zMODE;
    if (!CURRENTvarSELECTED(CDF,zOp)) return NO_VAR_SELECTED;
    if (!sX(LocateCurrentVar(CDF,zOp,&offset,&zVar,NULL),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    if (!sX(ReadVDR(CDF,offset,zVar,VDR_FLAGS,&flags,VDR_NULL),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    *recVary = BOO(RECvaryBITset(flags),VARY,NOVARY);
    break;
  }

  /****************************************************************************
  * rVAR_DIMVARYS_/zVAR_DIMVARYS_, 
  ****************************************************************************/

  case rVAR_DIMVARYS_:
  case zVAR_DIMVARYS_: {
    Logical zOp = (Va->item == zVAR_DIMVARYS_), zVar;
    struct cdfSTRUCT *CDF;
    long *dimVarys = va_arg (Va->ap, long *);
    Int32 offset;
    SelectCDF (Cur->cdf, CDF, NO_CDF_SELECTED)
    if (BADzOP(CDF,!zOp)) return ILLEGAL_IN_zMODE;
    if (!CURRENTvarSELECTED(CDF,zOp)) return NO_VAR_SELECTED;
    if (!sX(LocateCurrentVar(CDF,zOp,&offset,&zVar,NULL),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    if (!sX(CalcDimVarys(CDF,offset,zVar,dimVarys),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    break;
  }

  /****************************************************************************
  * rVAR_MAXREC_/zVAR_MAXREC_, 
  ****************************************************************************/

  case rVAR_MAXREC_:
  case zVAR_MAXREC_: {
    Logical zOp = (Va->item == zVAR_MAXREC_), zVar;
    struct cdfSTRUCT *CDF;
    struct varSTRUCT *Var;
    long *maxRec = va_arg (Va->ap, long *);
    Int32 offset;
    SelectCDF (Cur->cdf, CDF, NO_CDF_SELECTED)
    if (BADzOP(CDF,!zOp)) return ILLEGAL_IN_zMODE;
    if (!CURRENTvarSELECTED(CDF,zOp)) return NO_VAR_SELECTED;
    if (!sX(LocateCurrentVar(CDF,zOp,&offset,&zVar,&Var),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    if (Var == NULL) {
      Int32 tMaxRec;
      if (!sX(ReadVDR(CDF,offset,zVar,VDR_MAXREC,
		      &tMaxRec,VDR_NULL),&pStatus)) {
       AbortAccess (CDF, FALSE, Cur);
	return pStatus;
      }
      *maxRec = (long) tMaxRec;
    }
    else
      *maxRec = (long) Var->maxRec;
    break;
  }

  /****************************************************************************
  * rVAR_MAXallocREC_/zVAR_MAXallocREC_, 
  ****************************************************************************/

  case rVAR_MAXallocREC_:
  case zVAR_MAXallocREC_: {
    Logical zOp = (Va->item == zVAR_MAXallocREC_), zVar;
    struct cdfSTRUCT *CDF;
    struct varSTRUCT *Var;
    long *recN = va_arg (Va->ap, long *);
    Int32 offset;
    SelectCDF (Cur->cdf, CDF, NO_CDF_SELECTED)
    if (BADzOP(CDF,!zOp)) return ILLEGAL_IN_zMODE;
    if (!CURRENTvarSELECTED(CDF,zOp)) return NO_VAR_SELECTED;
    if (!sX(LocateCurrentVar(CDF,zOp,&offset,&zVar,&Var),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    /**************************************************************************
    * If a single-file CDF, pass back the maximum record number allocated.
    * If a multi-file CDF, pass back the maximum record number written.
    * Additional records are never allocated in multi-file CDFs.
    **************************************************************************/
    if (CDF->singleFile) {
      if (Var == NULL) {
	Int32 vxrTail;
	if (!sX(ReadVDR(CDF,offset,zVar,VDR_VXRTAIL,
			&vxrTail,VDR_NULL),&pStatus)) {
	  AbortAccess (CDF, FALSE, Cur);
	  return pStatus;
	}
	if (vxrTail == 0)
	  *recN = -1;
	else {
	  Int32 nUsed, lastRecs[NUM_VXR_ENTRIES];
	  if (!sX(ReadVXR(CDF,(long)vxrTail,
			  VXR_NUSEDENTRIES,&nUsed,
			  VXR_LASTREC,lastRecs,
			  VXR_NULL),&pStatus)) {
	    AbortAccess (CDF, FALSE, Cur);
	    return pStatus;
	  }
	  *recN = (long) lastRecs[(int)(nUsed-1)];
	}
      }
      else
	*recN = Var->sFile.maxAllocated;
    }
    else
      if (Var == NULL) {
	Int32 tMaxRec;
	if (!sX(ReadVDR(CDF,offset,zVar,VDR_MAXREC,
			&tMaxRec,VDR_NULL),&pStatus)) {
	  AbortAccess (CDF, FALSE, Cur);
	  return pStatus;
	}
	*recN = (long) tMaxRec;
      }
      else
	*recN = (long) Var->maxRec;
    break;
  }

  /****************************************************************************
  * rVAR_NUMBER_/zVAR_NUMBER_
  *    Determines the variable number for a specified variable name.
  ****************************************************************************/

  case rVAR_NUMBER_:
  case zVAR_NUMBER_: {
    Logical zOp = (Va->item == zVAR_NUMBER_), zVar;
    struct cdfSTRUCT *CDF;
    char *varName = va_arg (Va->ap, char *);
    long *varNum = va_arg (Va->ap,  long *);
    Int32 varN, offset;
    SelectCDF (Cur->cdf, CDF, NO_CDF_SELECTED)
    if (BADzOP(CDF,!zOp)) return ILLEGAL_IN_zMODE;
    tStatus = FindVarByName (CDF, varName, &offset, &zVar, NULL);
    switch (tStatus) {
      case CDF_OK:
	break;
      case NO_SUCH_VAR:
	return tStatus;
      default:
	AbortAccess (CDF, FALSE, Cur);
	return tStatus;
    }
    if (!sX(ReadVDR(CDF,offset,zVar,VDR_NUM,&varN,VDR_NULL),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    if (zModeON(CDF))
      *varNum = BOO(zVar,CDF->NrVars,0) + varN;
    else
      if (zOp)
	if (zVar)
	  *varNum = varN;
	else
	  return NO_SUCH_VAR;                   /* Wrong type of variable. */
      else
	if (zVar)
	  return NO_SUCH_VAR;                   /* Wrong type of variable. */
	else
	  *varNum = varN;
    break;
  }

  /****************************************************************************
  * rVAR_EXTENDRECS_/zVAR_EXTENDRECS_, 
  ****************************************************************************/

  case rVAR_EXTENDRECS_:
  case zVAR_EXTENDRECS_: {
    Logical zOp = (Va->item == zVAR_EXTENDRECS_), zVar;
    struct cdfSTRUCT *CDF;
    long *nExtendRecs = va_arg (Va->ap, long *);
    Int32 tRecs, offset;
    SelectCDF (Cur->cdf, CDF, NO_CDF_SELECTED)
    if (BADzOP(CDF,!zOp)) return ILLEGAL_IN_zMODE;
    if (!CURRENTvarSELECTED(CDF,zOp)) return NO_VAR_SELECTED;
    if (!sX(LocateCurrentVar(CDF,zOp,&offset,&zVar,NULL),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    if (!sX(ReadVDR(CDF,offset,zVar,
		    VDR_NEXTENDRECS,&tRecs,VDR_NULL),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    *nExtendRecs = tRecs;
    break;
  }

  /****************************************************************************
  * rVAR_nINDEXRECORDS_/zVAR_nINDEXRECORDS_,
  * rVAR_nINDEXENTRIES_/zVAR_nINDEXENTRIES_,
  ****************************************************************************/

  case rVAR_nINDEXRECORDS_:
  case zVAR_nINDEXRECORDS_:
  case rVAR_nINDEXENTRIES_:
  case zVAR_nINDEXENTRIES_: {
    Logical zOp = (Va->item == zVAR_nINDEXRECORDS_ ||
		   Va->item == zVAR_nINDEXENTRIES_), zVar;
    Logical entryOp = (Va->item == rVAR_nINDEXENTRIES_ ||
		       Va->item == zVAR_nINDEXENTRIES_);
    struct cdfSTRUCT *CDF;
    long *count = va_arg (Va->ap, long *);
    Int32 offset;
    SelectCDF (Cur->cdf, CDF, NO_CDF_SELECTED)
    if (BADzOP(CDF,!zOp)) return ILLEGAL_IN_zMODE;
    if (!CURRENTvarSELECTED(CDF,zOp)) return NO_VAR_SELECTED;
    if (!sX(LocateCurrentVar(CDF,zOp,&offset,&zVar,NULL),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    /**************************************************************************
    * If a multi-file CDF, pass back a count of zero (0) and an info/warning
    * status code.  If a single-file CDF, scan through the linked list of VXRs
    * counting the parameter requested.
    **************************************************************************/
    *count = 0;
    if (!CDF->singleFile) {
      if (!sX(MULTI_FILE_FORMAT,&pStatus)) return pStatus;
    }
    else {
      if (!sX(ReadVDR(CDF,offset,zVar,
		      VDR_VXRHEAD,&offset,VDR_NULL),&pStatus)) {
	AbortAccess (CDF, FALSE, Cur);
	return pStatus;
      }
      while (offset != 0) {
	if (entryOp) {
	  Int32 nUsed;
	  if (!sX(ReadVXR(CDF,offset,VXR_NUSEDENTRIES,
			  &nUsed,VXR_NULL),&pStatus)) {
	    AbortAccess (CDF, FALSE, Cur);
	    return pStatus;
	  }
	  *count += nUsed;
	}
	else
	  (*count)++;
	if (!sX(ReadVXR(CDF,offset,VXR_VXRNEXT,&offset,VXR_NULL),&pStatus)) {
	  AbortAccess (CDF, FALSE, Cur);
	  return pStatus;
	}
      }
    }
    break;
  }

  /****************************************************************************
  * rVAR_PADVALUE_/zVAR_PADVALUE_
  ****************************************************************************/

  case rVAR_PADVALUE_:
  case zVAR_PADVALUE_: {
    Logical zOp = (Va->item == zVAR_PADVALUE_), zVar;
    struct cdfSTRUCT *CDF;
    void *padValue = va_arg (Va->ap, void *);
    Int32 offset, dataType, numElems, flags;
    SelectCDF (Cur->cdf, CDF, NO_CDF_SELECTED)
    if (BADzOP(CDF,!zOp)) return ILLEGAL_IN_zMODE;
    if (!CURRENTvarSELECTED(CDF,zOp)) return NO_VAR_SELECTED;
    if (!sX(LocateCurrentVar(CDF,zOp,&offset,&zVar,NULL),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    if (!sX(ReadVDR(CDF,offset,zVar,VDR_FLAGS,&flags,
				    VDR_DATATYPE,&dataType,
				    VDR_NUMELEMS,&numElems,
				    VDR_NULL),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    if (PADvalueBITset(flags)) {
      if (!sX(ReadVDR(CDF,offset,zVar,VDR_PADVALUE,
		      padValue,VDR_NULL),&pStatus)) {
	AbortAccess (CDF, FALSE, Cur);
	return pStatus;
      }
      if (!sX(ConvertBuffer((long)CDF->encoding,CDF->decoding,
			    CDF->negToPosFp0mode,dataType,
			    numElems,padValue,padValue),&pStatus)) {
	AbortAccess (CDF, FALSE, Cur);
	return pStatus;
      }
    }
    else {
      DefaultPadValue (dataType, numElems, padValue);
      if (!sX(ConvertBuffer(HostEncoding(),CDF->decoding,
			    CDF->negToPosFp0mode,dataType,
			    numElems,padValue,padValue),&pStatus)) {
	AbortAccess (CDF, FALSE, Cur);
	return pStatus;
      }
      sX (NO_PADVALUE_SPECIFIED, &pStatus);
    }
    break;
  }

  /****************************************************************************
  * rVAR_DATA_/zVAR_DATA_, 
  ****************************************************************************/

  case rVAR_DATA_:
  case zVAR_DATA_: {
    Logical zOp = (Va->item == zVAR_DATA_);
    struct cdfSTRUCT *CDF;
    struct varSTRUCT *Var;
    long phyRecNum;
    Int32 offset;
    struct rdSTRUCT *rd;
    char *value = va_arg (Va->ap, char *);
    SelectCDF (Cur->cdf, CDF, NO_CDF_SELECTED)
    if (BADzOP(CDF,!zOp)) return ILLEGAL_IN_zMODE;
    if (!CURRENTvarSELECTED(CDF,zOp)) return NO_VAR_SELECTED;
    if (!sX(InitCurrentVar(CDF,zOp,&Var),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    rd = BOO(zModeON(CDF),&(Var->zRD),BOO(zOp,&(Var->zRD),&(CDF->rRD)));
    if (Var->status == VAR_CLOSED) {
      if (!sX(ReadWriteVar(CDF,Var),&pStatus)) {
	AbortAccess (CDF, FALSE, Cur);
	return pStatus;
      }
    }
    phyRecNum = BOO(Var->recVary,rd->recNumber,0);
    if (phyRecNum > Var->maxRec) {
      /************************************************************************
      * The value is in a virtual record.  Copy the pad value for the variable
      * into the caller's buffer and decode into the desired decoding.
      ************************************************************************/
      if (!sX(PadBuffer(CDF,Var,1L,value),&pStatus)) {
	AbortAccess (CDF, FALSE, Cur);
	return pStatus;
      }
      if (!sX(VIRTUAL_RECORD_DATA,&pStatus)) return pStatus;
    }
    else {
      /************************************************************************
      * The value physically exists.  Read the value into the caller's buffer
      * and decode into the desired decoding.
      ************************************************************************/
      offset = ValueByteOffset (CDF, Var, phyRecNum, rd->dimIndices);
      if (!SEEKv(Var->fp,(long)offset,vSEEK_SET)) {
	AbortAccess (CDF, FALSE, Cur);
	return VAR_READ_ERROR;
      }
      if (!READv(value,(size_t)Var->NvalueBytes,1,Var->fp)) {
	AbortAccess (CDF, FALSE, Cur);
	return VAR_READ_ERROR;
      }
      if (!sX(DECODE(Var->DecodeFunction,value,Var->NvalueElems),&pStatus)) {
        AbortAccess (CDF, FALSE, Cur);
        return pStatus;
      }
    }
    Var->accessed_at = CDF->pseudo_clock++;
    break;
  }

  /****************************************************************************
  * rVAR_HYPERDATA_/zVAR_HYPERDATA_, 
  ****************************************************************************/

  case rVAR_HYPERDATA_:
  case zVAR_HYPERDATA_: {
    Logical zOp = (Va->item == zVAR_HYPERDATA_);
    struct cdfSTRUCT *CDF;
    struct varSTRUCT *Var;
    int dimN;
    struct rdSTRUCT *rd;
#if LIMITof64K
    long Nvalues, Nbytes;
#endif
    char *buffer = va_arg (Va->ap, char *);
    SelectCDF (Cur->cdf, CDF, NO_CDF_SELECTED)
    if (BADzOP(CDF,!zOp)) return ILLEGAL_IN_zMODE;
    if (!CURRENTvarSELECTED(CDF,zOp)) return NO_VAR_SELECTED;
    if (!sX(InitCurrentVar(CDF,zOp,&Var),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    rd = BOO(zModeON(CDF),&(Var->zRD),BOO(zOp,&(Var->zRD),&(CDF->rRD)));
    for (dimN = 0; dimN < Var->numDims; dimN++) {
       long maxIndex = rd->dimIndices[dimN] +
		       ((rd->dimCounts[dimN] - 1) * rd->dimIntervals[dimN]);
       if (maxIndex >= Var->dimSizes[dimN]) return BAD_DIM_INDEX;
    }
#if LIMITof64K
    Nvalues = rd->recCount;
    for (dimN = 0; dimN < Var->numDims; dimN++) Nvalues *= rd->dimCounts[dimN];
    Nbytes = Nvalues * Var->NvalueBytes;
    if (TOObigIBMpc(Nbytes)) return IBM_PC_OVERFLOW;
#endif
    if (Var->status == VAR_CLOSED) {
      if (!sX(ReadWriteVar(CDF,Var),&pStatus)) {
	AbortAccess (CDF, FALSE, Cur);
	return pStatus;
      }
    }
    if (!sX(HyperRead(CDF,Var,rd,buffer),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    Var->accessed_at = CDF->pseudo_clock++;
    break;
  }

  /****************************************************************************
  * rVAR_SEQDATA_/zVAR_SEQDATA_, 
  ****************************************************************************/

  case rVAR_SEQDATA_:
  case zVAR_SEQDATA_: {
    Logical zOp = (Va->item == zVAR_SEQDATA_);
    struct cdfSTRUCT *CDF;
    struct varSTRUCT *Var;
    long recNum;
    void *value = va_arg (Va->ap, char *);
    SelectCDF (Cur->cdf, CDF, NO_CDF_SELECTED)
    if (BADzOP(CDF,!zOp)) return ILLEGAL_IN_zMODE;
    if (!CURRENTvarSELECTED(CDF,zOp)) return NO_VAR_SELECTED;
    if (!sX(InitCurrentVar(CDF,zOp,&Var),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    if (Var->status == VAR_CLOSED) {
      if (!sX(ReadWriteVar(CDF,Var),&pStatus)) {
	AbortAccess (CDF, FALSE, Cur);
	return pStatus;
      }
    }
    recNum = Var->seqValueOffset / Var->NphyRecValues;
    if (recNum > Var->maxRec) return END_OF_VAR;
    if (!SEEKv(Var->fp,(long)SeqValueByteOffset(CDF,Var),vSEEK_SET)) {
      AbortAccess (CDF, FALSE, Cur);
      return VAR_READ_ERROR;
    }
    if (!READv(value,(size_t)Var->NvalueBytes,1,Var->fp)) {
      AbortAccess (CDF, FALSE, Cur);
      return VAR_READ_ERROR;
    }
    if (!sX(DECODE(Var->DecodeFunction,value,Var->NvalueElems),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    Var->seqValueOffset++;
    Var->accessed_at = CDF->pseudo_clock++;
    break;
  }

  /****************************************************************************
  * rVARs_RECDATA_/zVARs_RECDATA_
  *    Read data records for up to all of the rVariables/zVariables.
  ****************************************************************************/

  case rVARs_RECDATA_:
  case zVARs_RECDATA_: {
    Logical zOp = (Va->item == zVARs_RECDATA_), zVar;
    struct varSTRUCT *Var;
    struct cdfSTRUCT *CDF;
    long recNum, varNt;
    Int32 offset;
    Byte *tBuffer;
    int varX;
    long nVars = va_arg (Va->ap, long);
    long *varNs = va_arg (Va->ap, long *);
    void *buffer = va_arg (Va->ap, char *);
#if LIMITof64K
    long nBytes;
#endif
    SelectCDF (Cur->cdf, CDF, NO_CDF_SELECTED)
    if (BADzOP(CDF,!zOp)) return ILLEGAL_IN_zMODE;
    if (nVars < 1) return BAD_NUM_VARS;
    for (varX = 0; varX < nVars; varX++) {
       if (!sX(VarIdentity(CDF,varNs[varX],zOp,&varNt,&zVar,NULL),&pStatus)) {
	 return pStatus;
       }
       if (!sX(InitVar(CDF,varNt,zVar,NULL),&pStatus)) {
	 AbortAccess (CDF, FALSE, Cur);
	 return pStatus;
       }
    }
#if LIMITof64K
    for (varX = 0, nBytes = 0; varX < nVars; varX++) {
       if (!sX(VarIdentity(CDF,varNs[varX],zOp,NULL,NULL,&Var),&pStatus)) {
	 return pStatus;
       }
       nBytes += Var->NphyRecBytes;
    }
    if (TOObigIBMpc(nBytes)) return IBM_PC_OVERFLOW;
#endif
    for (varX = 0, tBuffer = buffer; varX < nVars; varX++) {
       if (!sX(VarIdentity(CDF,varNs[varX],zOp,NULL,NULL,&Var),&pStatus)) {
	 return pStatus;
       }
       if (Var->status == VAR_CLOSED) {
	 if (!sX(ReadWriteVar(CDF,Var),&pStatus)) {
	   AbortAccess (CDF, FALSE, Cur);
	   return pStatus;
	 }
       }
       recNum = BOO(Var->recVary,BOO(zOp,Var->zRD.recNumber,
					 CDF->rRD.recNumber),0);
       if (recNum <= Var->maxRec) {
	 offset = RecordByteOffset (CDF, Var, recNum);
	 if (!SEEKv(Var->fp,(long)offset,vSEEK_SET)) {
	   AbortAccess (CDF, FALSE, Cur);
	   return VAR_READ_ERROR;
	 }
	 if (!READv(tBuffer,(size_t)Var->NphyRecBytes,1,Var->fp)) {
	   AbortAccess (CDF, FALSE, Cur);
	   return VAR_READ_ERROR;
	 }
	 if (!sX(DECODE(Var->DecodeFunction,
			tBuffer,Var->NphyRecElems),&pStatus)) {
	   AbortAccess (CDF, FALSE, Cur);
	   return pStatus;
	 }
       }
       else {
	 if (!sX(PadBuffer(CDF,Var,Var->NphyRecValues,tBuffer),&pStatus)) {
	   AbortAccess (CDF, FALSE, Cur);
	   return pStatus;
	 }
	 if (!sX(VIRTUAL_RECORD_DATA,&pStatus)) return pStatus;
       }
       tBuffer += (size_t) Var->NphyRecBytes;
       Var->accessed_at = CDF->pseudo_clock++;
    }

    break;
  }

  /****************************************************************************
  * ATTR_NAME_, 
  *    Note that a temporary variable is used when reading the attribute name.
  * This is because the caller may have only allocated enough memory for the
  * size name they expect (ie., less than CDF_ATTR_NAME_LEN characters).  Since
  * the attribute name is NUL-terminated in the CDF, only the actual characters
  * of the name will be copied to the caller's buffer.
  ****************************************************************************/

  case ATTR_NAME_: {
    struct cdfSTRUCT *CDF;
    char *attrName = va_arg (Va->ap,  char *), tName[CDF_ATTR_NAME_LEN+1];
    SelectCDF (Cur->cdf, CDF, NO_CDF_SELECTED)
    if (!CURRENTattrSELECTED(CDF)) return NO_ATTR_SELECTED;
    if (!sX(ReadADR(CDF,CDF->CURattrOffset,ADR_NAME,tName,ADR_NULL),&pStatus)){
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    strcpyX (attrName, tName, CDF_ATTR_NAME_LEN);
    break;
  }

  /****************************************************************************
  * ATTR_NUMBER_, 
  ****************************************************************************/

  case ATTR_NUMBER_: {
    struct cdfSTRUCT *CDF;
    char *attrName = va_arg (Va->ap, char *);
    long *attrNum = va_arg (Va->ap,  long *);
    Int32 attrNumT, offset;
    SelectCDF (Cur->cdf, CDF, NO_CDF_SELECTED)
    tStatus = FindAttrByName (CDF, attrName, &offset);
    switch (tStatus) {
      case CDF_OK:
	break;
      case NO_SUCH_ATTR:
	return tStatus;
      default:
	AbortAccess (CDF, FALSE, Cur);
	return tStatus;
    }
    if (!sX(ReadADR(CDF,offset,ADR_NUM,&attrNumT,ADR_NULL),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    *attrNum = attrNumT;
    break;
  }

  /****************************************************************************
  * ATTR_SCOPE_, 
  ****************************************************************************/

  case ATTR_SCOPE_: {
    struct cdfSTRUCT *CDF;
    long *scope = va_arg (Va->ap, long *);
    Int32 tScope;
    SelectCDF (Cur->cdf, CDF, NO_CDF_SELECTED)
    if (!CURRENTattrSELECTED(CDF)) return NO_ATTR_SELECTED;
    if (!sX(ReadADR(CDF,CDF->CURattrOffset,
		    ADR_SCOPE,&tScope,ADR_NULL),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    *scope = DEFINITEscope(tScope);
    break;
  }

  /****************************************************************************
  * ATTR_MAXgENTRY_/ATTR_MAXrENTRY_/ATTR_MAXzENTRY_
  * ATTR_NUMgENTRIES_/ATTR_NUMrENTRIES_/ATTR_NUMzENTRIES_
  ****************************************************************************/

  case ATTR_MAXgENTRY_:
  case ATTR_NUMgENTRIES_:
  case ATTR_MAXrENTRY_:
  case ATTR_NUMrENTRIES_:
  case ATTR_MAXzENTRY_:
  case ATTR_NUMzENTRIES_: {
    Logical maxOp = ONEof3(Va->item,ATTR_MAXgENTRY_,
				    ATTR_MAXrENTRY_,
				    ATTR_MAXzENTRY_);
    int entryType = BOO(maxOp,E3p(Va->item,ATTR_MAXgENTRY_,
					   ATTR_MAXrENTRY_,
					   ATTR_MAXzENTRY_),
			      E3p(Va->item,ATTR_NUMgENTRIES_,
					   ATTR_NUMrENTRIES_,
					   ATTR_NUMzENTRIES_));
    struct cdfSTRUCT *CDF;
    long *value = va_arg (Va->ap, long *);
    Int32 scope, gr, z;
    SelectCDF (Cur->cdf, CDF, NO_CDF_SELECTED)
    if (!CURRENTattrSELECTED(CDF)) return NO_ATTR_SELECTED;
    if (!sX(ReadADR(CDF,CDF->CURattrOffset,
		    ADR_SCOPE,&scope,ADR_NULL),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    if (GLOBALscope(scope)) {
      if (entryType != gENTRYt) return ILLEGAL_FOR_SCOPE;
    }
    else {
      if (entryType == gENTRYt) return ILLEGAL_FOR_SCOPE;
    }
    if (!sX(ReadADR(CDF,CDF->CURattrOffset,
		    BOO(maxOp,ADR_MAXgrENTRY,ADR_NgrENTRIES),&gr,
		    BOO(maxOp,ADR_MAXzENTRY,ADR_NzENTRIES),&z,
		    ADR_NULL),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    if (GLOBALscope(scope))
      *value = (long) gr;
    else
      if (zModeON(CDF))
	if (entryType == rENTRYt)
	  *value = (long) BOO(maxOp,-1,0);   /* Never any rEntries in zMode. */
	else
	  *value = (long) BOO(maxOp,BOO(z > -1,CDF->NrVars+z,gr),gr+z);
      else
	*value = (long) E3(entryType,BOO(maxOp,-1,0),gr,z);
    break;
  }

  /****************************************************************************
  * gENTRY_DATATYPE_/rENTRY_DATATYPE_/zENTRY_DATATYPE_
  * gENTRY_NUMELEMS_/rENTRY_NUMELEMS_/zENTRY_NUMELEMS_
  *    If this CDF is prior to CDF V2.1.1, the current attribute is named
  * "VALIDMIN", "VALIDMAX", "SCALEMIN", or "SCALEMAX", this is a true rEntry,
  * and the rEntry corresponds to an rVariable named "EPOCH", then return
  * the CDF_EPOCH data type if the actual data type is CDF_REAL8 or CDF_DOUBLE.
  * (The CDF_EPOCH data type was not introduced until CDF V2.1.1).  Note that
  * only rVariables were supported prior to CDF V2.3.
  ****************************************************************************/

  case gENTRY_DATATYPE_:
  case gENTRY_NUMELEMS_:
  case rENTRY_DATATYPE_:
  case rENTRY_NUMELEMS_:
  case zENTRY_DATATYPE_:
  case zENTRY_NUMELEMS_: {
    Logical dataOp = ONEof3(Va->item,gENTRY_DATATYPE_,
				     rENTRY_DATATYPE_,
				     zENTRY_DATATYPE_);
    int entryType = BOO(dataOp,E3p(Va->item,gENTRY_DATATYPE_,
					    rENTRY_DATATYPE_,
					    zENTRY_DATATYPE_),
			       E3p(Va->item,gENTRY_NUMELEMS_,
					    rENTRY_NUMELEMS_,
					    zENTRY_NUMELEMS_));
    struct cdfSTRUCT *CDF;
    long *value = va_arg (Va->ap, long *);
    Int32 tValue, eOffset;
    SelectCDF (Cur->cdf, CDF, NO_CDF_SELECTED)
    if (!CURRENTattrSELECTED(CDF)) return NO_ATTR_SELECTED;
    if (E3(entryType,
	   CDF->CURgrEntryNum,
	   CDF->CURgrEntryNum,
	   CDF->CURzEntryNum) == RESERVED_ENTRYNUM) return NO_ENTRY_SELECTED;
    if (!sX(CheckEntryOp(CDF,entryType,Cur),&pStatus)) return pStatus;
    eOffset = E3(entryType,CDF->CURgrEntryOffset,
			   CDF->CURgrEntryOffset,
			   CDF->CURzEntryOffset);
    if (eOffset == RESERVED_ENTRYOFFSET) return NO_SUCH_ENTRY;
    if (!sX(ReadAEDR(CDF,eOffset,BOO(dataOp,AEDR_DATATYPE,AEDR_NUMELEMS),
		     &tValue,AEDR_NULL),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    if (dataOp && CDF->fakeEPOCH) {
      char aName[CDF_ATTR_NAME_LEN+1];
      if (!sX(ReadADR(CDF,CDF->CURattrOffset,
		      ADR_NAME,aName,ADR_NULL),&pStatus)) {
	AbortAccess (CDF, FALSE, Cur);
	return pStatus;
      }
      if (!strcmpITB(aName,"VALIDMIN") || !strcmpITB(aName,"VALIDMAX") ||
	  !strcmpITB(aName,"SCALEMIN") || !strcmpITB(aName,"SCALEMAX")) {
	Int32 vOffset;
	tStatus = FindVarByNumber (CDF, E3(entryType, CDF->CURgrEntryNum,
						      CDF->CURgrEntryNum,
						      CDF->CURzEntryNum),
				   &vOffset, FALSE);
	switch (tStatus) {
	  case CDF_OK: {
	    char vName[CDF_VAR_NAME_LEN+1];
	    if (!sX(ReadVDR(CDF,vOffset,FALSE,VDR_NAME,
			    vName,VDR_NULL),&pStatus)) {
	      AbortAccess (CDF, FALSE, Cur);
	      return pStatus;
	    }
	    if (!strcmpITB(vName,"EPOCH") &&
		FLOAT8dataType(tValue)) tValue = CDF_EPOCH;
	    break;
	  }
	  case NO_SUCH_VAR:
	    break;
	  default:
	    AbortAccess (CDF, FALSE, Cur);
	    return tStatus;
	}
      }
    }
    *value = tValue;
    break;
  }

  /****************************************************************************
  * gENTRY_DATA_/rENTRY_DATA_/zENTRY_DATA_, 
  ****************************************************************************/

  case gENTRY_DATA_:
  case rENTRY_DATA_:
  case zENTRY_DATA_: {
    int entryType = E3p(Va->item,gENTRY_DATA_,rENTRY_DATA_,zENTRY_DATA_);
    struct cdfSTRUCT *CDF;
    Int32 offset, dataType, numElems;
    void *value = va_arg (Va->ap, void *);
    SelectCDF (Cur->cdf, CDF, NO_CDF_SELECTED)
    if (!CURRENTattrSELECTED(CDF)) return NO_ATTR_SELECTED;
    if (E3(entryType,
	   CDF->CURgrEntryNum,
	   CDF->CURgrEntryNum,
	   CDF->CURzEntryNum) == RESERVED_ENTRYNUM) return NO_ENTRY_SELECTED;
    if (!sX(CheckEntryOp(CDF,entryType,Cur),&pStatus)) return pStatus;
    offset = E3(entryType,CDF->CURgrEntryOffset,
			  CDF->CURgrEntryOffset,
			  CDF->CURzEntryOffset);
    if (offset == RESERVED_ENTRYOFFSET) return NO_SUCH_ENTRY;
    if (!sX(ReadAEDR(CDF,offset,AEDR_DATATYPE,&dataType,
				AEDR_NUMELEMS,&numElems,
				AEDR_VALUE,value,
				AEDR_NULL),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    if (!sX(ConvertBuffer((long)CDF->encoding,CDF->decoding,
			  CDF->negToPosFp0mode,(long)dataType,
			  (long)numElems,value,value),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    break;
  }

  /****************************************************************************
  * Unknown item, must be the next function.
  ****************************************************************************/

  default: {
    Va->fnc = Va->item;
    break;
  }
}

return pStatus;
}
