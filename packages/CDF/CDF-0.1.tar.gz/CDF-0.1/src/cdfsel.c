/******************************************************************************
*
*  NSSDC/CDF                                     CDF `select' operations.
*
*  Version 1.3c, 24-Feb-95, Hughes STX.
*
*  Modification history:
*
*   V1.0  20-May-92, J Love     Original version (was part of `cdflib.c').
*   V1.1  21-Aug-92, J Love     CDF V2.3 (shareable/NeXT/zVar).
*   V1.2   4-Jan-94, J Love     CDF V2.4.
*   V1.3  15-Dec-94, J Love     CDF V2.5.
*   V1.3a  4-Jan-95, J Love	Encode/decode changes.
*   V1.3b 19-Jan-95, J Love	IRIX 6.0 (64-bit).
*   V1.3c 24-Feb-95, J Love	Solaris 2.3 IDL i/f.
*
******************************************************************************/

#include "cdflib.h"

/******************************************************************************
* CDFsel.
******************************************************************************/

STATICforIDL CDFstatus CDFsel (Va, Cur)
struct VAstruct *Va;
struct CURstruct *Cur;
{
CDFstatus tStatus, pStatus = CDF_OK;

switch (Va->item) {
  /****************************************************************************
  * CDF_, select the current CDF.
  ****************************************************************************/

  case CDF_: {
    CDFid id = va_arg (Va->ap, CDFid);
    /**************************************************************************
    * Check if the reserved CDFid (used by IDL interface and Windows DLL).
    **************************************************************************/
    if (id == RESERVED_CDFID) {
      Cur->cdf = (struct cdfSTRUCT *) RESERVED_CDFID;
      break;
    }
    /**************************************************************************
    * Check if the CDFid points to a valid CDF structure.
    **************************************************************************/
    if (((struct cdfSTRUCT *) id)->struct_magic_number != CDFid_MAGIC_NUMBER) {
      return BAD_CDF_ID;
    }
    /**************************************************************************
    * Set the current CDF.
    **************************************************************************/
    Cur->cdf = (struct cdfSTRUCT *) id;
    break;
  }

  /****************************************************************************
  * CDF_STATUS_, select the current CDFstatus.
  ****************************************************************************/

  case CDF_STATUS_: {
    Cur->status = va_arg (Va->ap, CDFstatus);
    break;
  }

  /****************************************************************************
  * CDF_READONLY_MODE_, select a readonly mode for the current CDF.
  ****************************************************************************/

  case CDF_READONLY_MODE_: {
    long mode;
    struct cdfSTRUCT *CDF;
    mode = va_arg (Va->ap, long);
    SelectCDF (Cur->cdf, CDF, NO_CDF_SELECTED)
    switch (mode) {
      case READONLYon:
	CDF->readonlyMode = READONLYon;
	break;
      case READONLYoff:
	CDF->readonlyMode = READONLYoff;
	break;
      default:
	return BAD_READONLY_MODE;
    }
    break;
  }

  /****************************************************************************
  * CDF_zMODE_, select a zMode for the current CDF.  Changing the zMode causes
  *             all "current" objects/states to be reset (sort of like
  *             reopening the CDF).
  ****************************************************************************/

  case CDF_zMODE_: {
    long mode;
    struct cdfSTRUCT *CDF;
    mode = va_arg (Va->ap, long);
    SelectCDF (Cur->cdf, CDF, NO_CDF_SELECTED)
    switch (mode) {
      /************************************************************************
      * zMODEoff, turn off zMode.
      ************************************************************************/
      case zMODEoff:
	CDF->zMode = zMODEoff;
	break;
      /************************************************************************
      * zMODEon1, turn on zMode/1.  The rVariables become a zGroup (ie. they
      * all have the same dimensionality [that of the rVariables] with their
      * original record/dimension variances).
      ************************************************************************/
      case zMODEon1:
	CDF->zMode = zMODEon1;
	break;
      /************************************************************************
      * zMODEon2, turn on zMode/2.  The dimensionality of each rVariable is
      * determined based on their dimension variances (dimensions with a
      * NOVARY variance are eliminated).
      ************************************************************************/
      case zMODEon2:
	CDF->zMode = zMODEon2;
	break;
      /************************************************************************
      * Unknown zMode.
      ************************************************************************/
      default:
	return BAD_zMODE;
    }
    if (!sX(ConfigureNEWzMode(CDF),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    break;
  }

  /****************************************************************************
  * CDF_DECODING_, selects the decoding for attribute entry and variable data
  * values read from the current CDF.
  ****************************************************************************/

  case CDF_DECODING_: {
    struct cdfSTRUCT *CDF;
    long decoding = va_arg (Va->ap, long);
    SelectCDF (Cur->cdf, CDF, NO_CDF_SELECTED)
    if (!ValidDecoding(decoding)) return BAD_DECODING;
    CDF->decoding = decoding;
    if (!sX(UpdateInitializedVars(CDF),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    break;
  }

  /****************************************************************************
  * CDF_NEGtoPOSfp0_MODE_, select a negative to positive floating point zero
  * mode for the current CDF.
  ****************************************************************************/

  case CDF_NEGtoPOSfp0_MODE_: {
    struct cdfSTRUCT *CDF;
    long mode = va_arg (Va->ap, long);
    SelectCDF (Cur->cdf, CDF, NO_CDF_SELECTED)
    switch (mode) {
      case NEGtoPOSfp0on:
	CDF->negToPosFp0mode = NEGtoPOSfp0on;
	break;
      case NEGtoPOSfp0off:
	CDF->negToPosFp0mode = NEGtoPOSfp0off;
	break;
      default:
	return BAD_NEGtoPOSfp0_MODE;
    }
    if (!sX(UpdateInitializedVars(CDF),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    break;
  }

  /****************************************************************************
  * CDF_CACHESIZE_
  *     Select a new cache size for the `.cdf' file.  A cache size of zero is
  * ignored.
  ****************************************************************************/

  case CDF_CACHESIZE_: {
    struct cdfSTRUCT *CDF;
    int nBuffers = (int) va_arg (Va->ap, long);
    if (nBuffers == 0) break;
    SelectCDF (Cur->cdf, CDF, NO_CDF_SELECTED)
    if (!CACHEv(CDF->fp,nBuffers)) return BAD_CACHE_SIZE;
    CDF->nCacheBuffers = nBuffers;
    CDF->explicitCache = TRUE;
    break;
  }

  /****************************************************************************
  * rVARs_CACHESIZE_/zVARs_CACHESIZE_
  *   Selects a new cache size for all of the r/zVariable files.  N/A if a
  * single-file CDF.  A cache size of zero is ignored.
  ****************************************************************************/

  case rVARs_CACHESIZE_:
  case zVARs_CACHESIZE_: {
    Logical zOp = (Va->item == zVARs_CACHESIZE_);
    struct cdfSTRUCT *CDF;
    struct varSTRUCT *Var;
    int nBuffers = (int) va_arg (Va->ap, long), varN;
    if (nBuffers == 0) break;
    SelectCDF (Cur->cdf, CDF, NO_CDF_SELECTED)
    if (BADzOP(CDF,!zOp)) return ILLEGAL_IN_zMODE;
    if (CDF->singleFile) {
      if (!sX(SINGLE_FILE_FORMAT,&pStatus)) return pStatus;
    }
    else {
      if (zModeON(CDF)) {
	for (varN = 0; varN < CDF->NrVars; varN++) {
	   if (!sX(InitVar(CDF,varN,FALSE,&Var),&pStatus)) {
	     AbortAccess (CDF, FALSE, Cur);
	     return pStatus;
	   }
	   if (Var->status == VAR_OPENED) {
	     if (!CACHEv(Var->fp,nBuffers)) return BAD_CACHE_SIZE;
	   }
	   Var->nCacheBuffers = nBuffers;
	}
	for (varN = 0; varN < CDF->NzVars; varN++) {
	   if (!sX(InitVar(CDF,varN,TRUE,&Var),&pStatus)) {
	     AbortAccess (CDF, FALSE, Cur);
	     return pStatus;
	   }
	   if (Var->status == VAR_OPENED) {
	     if (!CACHEv(Var->fp,nBuffers)) return BAD_CACHE_SIZE;
	   }
	   Var->nCacheBuffers = nBuffers;
	}
      }
      else {
	long nVars = BOO(zOp,CDF->NzVars,CDF->NrVars);
	for (varN = 0; varN < nVars; varN++) {
	   if (!sX(InitVar(CDF,varN,zOp,&Var),&pStatus)) {
	     AbortAccess (CDF, FALSE, Cur);
	     return pStatus;
	   }
	   if (Var->status == VAR_OPENED) {
	     if (!CACHEv(Var->fp,nBuffers)) return BAD_CACHE_SIZE;
	   }
	   Var->nCacheBuffers = nBuffers;
	}
      }
    }
    break;
  }

  /****************************************************************************
  * rVAR_CACHESIZE_/zVAR_CACHESIZE_, selects a new cache size for the current
  * r/zVariable's file.  N/a if a single-file CDF.  A cache size of zero is
  * ignored.
  ****************************************************************************/

  case rVAR_CACHESIZE_:
  case zVAR_CACHESIZE_: {
    Logical zOp = (Va->item == zVAR_CACHESIZE_);
    struct cdfSTRUCT *CDF;
    struct varSTRUCT *Var;
    int nBuffers = (int) va_arg (Va->ap, long);
    if (nBuffers == 0) break;
    SelectCDF (Cur->cdf, CDF, NO_CDF_SELECTED)
    if (BADzOP(CDF,!zOp)) return ILLEGAL_IN_zMODE;
    if (CDF->singleFile) {
      if (!sX(SINGLE_FILE_FORMAT,&pStatus)) return pStatus;
    }
    else {
      if (!CURRENTvarSELECTED(CDF,zOp)) return NO_VAR_SELECTED;
      if (!sX(InitCurrentVar(CDF,zOp,&Var),&pStatus)) {
	AbortAccess (CDF, FALSE, Cur);
	return pStatus;
      }
      if (Var->status == VAR_OPENED) {
	if (!CACHEv(Var->fp,nBuffers)) return BAD_CACHE_SIZE;
      }
      Var->nCacheBuffers = nBuffers;
    }
    break;
  }

  /****************************************************************************
  * rVAR_/zVAR_
  *    Select (by number) the current rVariable/zVariable for the current CDF.
  ****************************************************************************/

  case rVAR_:
  case zVAR_: {
    Logical zOp = (Va->item == zVAR_);
    struct cdfSTRUCT *CDF;
    long varNum = va_arg (Va->ap, long);
    SelectCDF (Cur->cdf, CDF, NO_CDF_SELECTED)
    if (BADzOP(CDF,!zOp)) return ILLEGAL_IN_zMODE;
    if (varNum < 0) return BAD_VAR_NUM;
    if (zModeON(CDF))
      if (varNum < CDF->NrVars)
	CDF->CURzVarNum = varNum;
      else {
	long varNumT = varNum - CDF->NrVars;
	if (varNumT < CDF->NzVars)
	  CDF->CURzVarNum = varNum;
	else
	  return NO_SUCH_VAR;
      }
    else
      if (varNum < BOO(zOp,CDF->NzVars,CDF->NrVars))
	if (zOp)
	  CDF->CURzVarNum = varNum;
	else
	  CDF->CURrVarNum = varNum;
      else
	return NO_SUCH_VAR;
    break;
  }

  /****************************************************************************
  * rVAR_NAME_/zVAR_NAME_
  *    Select (by name) the current rVariable/zVariable for the current CDF.
  ****************************************************************************/

  case rVAR_NAME_:
  case zVAR_NAME_: {
    Logical zOp = (Va->item == zVAR_NAME_), zVar;
    struct cdfSTRUCT *CDF;
    char *varName = va_arg (Va->ap, char *);
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
      CDF->CURzVarNum = (zVar ? CDF->NrVars + varN : varN);
    else {
      if (zOp)
	if (zVar)
	  CDF->CURzVarNum = varN;
	else
	  return NO_SUCH_VAR;                   /* Wrong type of variable. */
      else
	if (zVar)
	  return NO_SUCH_VAR;                   /* Wrong type of variable. */
	else
	  CDF->CURrVarNum = varN;
    }
    break;
  }

  /****************************************************************************
  * rVARs_RECNUMBER_/rVARs_RECCOUNT_/rVARs_RECINTERVAL_
  ****************************************************************************/

  case rVARs_RECNUMBER_:
  case rVARs_RECCOUNT_:
  case rVARs_RECINTERVAL_: {
    struct cdfSTRUCT *CDF;
    long value = va_arg (Va->ap, long);
    SelectCDF (Cur->cdf, CDF, NO_CDF_SELECTED)
    if (BADzOP(CDF,TRUE)) return ILLEGAL_IN_zMODE;
    if (CDF->NrVars == 0) {
      if (!sX(NO_VARS_IN_CDF,&pStatus)) return pStatus;
    }
    switch (Va->item) {
      case rVARs_RECNUMBER_:
	if (value < 0) return BAD_REC_NUM;
	CDF->rRD.recNumber = value;
	break;
      case rVARs_RECCOUNT_:
	if (value < 0) return BAD_REC_COUNT;
	CDF->rRD.recCount = value;
	break;
      case rVARs_RECINTERVAL_:
	if (value < 1) return BAD_REC_INTERVAL;
	CDF->rRD.recInterval = value;
	break;
    }
    break;
  }

  /****************************************************************************
  * zVAR_RECNUMBER_/zVAR_RECCOUNT_/zVAR_RECINTERVAL_
  ****************************************************************************/

  case zVAR_RECNUMBER_:
  case zVAR_RECCOUNT_:
  case zVAR_RECINTERVAL_: {
    struct cdfSTRUCT *CDF;
    struct varSTRUCT *Var;
    long value = va_arg (Va->ap, long);
    SelectCDF (Cur->cdf, CDF, NO_CDF_SELECTED)
    if (!CURRENTvarSELECTED(CDF,TRUE)) return NO_VAR_SELECTED;
    if (!sX(InitCurrentVar(CDF,TRUE,&Var),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    switch (Va->item) {
      case zVAR_RECNUMBER_:
	if (value < 0) return BAD_REC_NUM;
	Var->zRD.recNumber = value;
	break;
      case zVAR_RECCOUNT_:
	if (value < 1) return BAD_REC_COUNT;
	Var->zRD.recCount = value;
	break;
      case zVAR_RECINTERVAL_:
	if (value < 1) return BAD_REC_INTERVAL;
	Var->zRD.recInterval = value;
	break;
    }
    break;
  }

  /****************************************************************************
  * zVARs_RECNUMBER_
  ****************************************************************************/

  case zVARs_RECNUMBER_: {
    struct cdfSTRUCT *CDF;
    struct varSTRUCT *Var;
    long recNumber = va_arg (Va->ap, long), varN;
    SelectCDF (Cur->cdf, CDF, NO_CDF_SELECTED)
    if (zModeON(CDF)) {
      if (CDF->NrVars + CDF->NzVars == 0) {
	if (!sX(NO_VARS_IN_CDF,&pStatus)) return pStatus;
      }
      for (varN = 0; varN < CDF->NrVars; varN++) {
	 if (!sX(InitVar(CDF,varN,FALSE,&Var),&pStatus)) {
	   AbortAccess (CDF, FALSE, Cur);
	   return pStatus;
	 }
	 Var->zRD.recNumber = recNumber;
      }
      for (varN = 0; varN < CDF->NzVars; varN++) {
	 if (!sX(InitVar(CDF,varN,TRUE,&Var),&pStatus)) {
	   AbortAccess (CDF, FALSE, Cur);
	   return pStatus;
	 }
	 Var->zRD.recNumber = recNumber;
      }
    }
    else {
      if (CDF->NzVars == 0) {
	if (!sX(NO_VARS_IN_CDF,&pStatus)) return pStatus;
      }
      for (varN = 0; varN < CDF->NzVars; varN++) {
	 if (!sX(InitVar(CDF,varN,TRUE,&Var),&pStatus)) {
	   AbortAccess (CDF, FALSE, Cur);
	   return pStatus;
	 }
	 Var->zRD.recNumber = recNumber;
      }
    }
    break;
  }

  /****************************************************************************
  * rVARs_DIMINDICES_/rVARs_DIMCOUNTS_/rVARs_DIMINTERVALS_
  ****************************************************************************/

  case rVARs_DIMINDICES_:
  case rVARs_DIMCOUNTS_:
  case rVARs_DIMINTERVALS_: {
    struct cdfSTRUCT *CDF;
    long *values = va_arg (Va->ap, long *);
    int dimN;
    SelectCDF (Cur->cdf, CDF, NO_CDF_SELECTED)
    if (BADzOP(CDF,TRUE)) return ILLEGAL_IN_zMODE;
    if (CDF->NrVars == 0) {
      if (!sX(NO_VARS_IN_CDF,&pStatus)) return pStatus;
    }
    switch (Va->item) {
      case rVARs_DIMINDICES_: {
	for (dimN = 0; dimN < CDF->rNumDims; dimN++)
	   if (values[dimN] < 0 || CDF->rDimSizes[dimN] <= values[dimN])
	     return BAD_DIM_INDEX;
	   else
	     CDF->rRD.dimIndices[dimN] = values[dimN];
	break;
      }
      case rVARs_DIMCOUNTS_:
	for (dimN = 0; dimN < CDF->rNumDims; dimN++)
	   if (values[dimN] < 1)
	     return BAD_DIM_COUNT;
	   else
	     CDF->rRD.dimCounts[dimN] = values[dimN];
	break;
      case rVARs_DIMINTERVALS_:
	for (dimN = 0; dimN < CDF->rNumDims; dimN++)
	   if (values[dimN] < 1)
	     return BAD_DIM_INTERVAL;
	   else
	     CDF->rRD.dimIntervals[dimN] = values[dimN];
	break;
    }
    break;
  }

  /****************************************************************************
  * zVAR_DIMINDICES_/zVAR_DIMCOUNTS_/zVAR_DIMINTERVALS_
  ****************************************************************************/

  case zVAR_DIMINDICES_:
  case zVAR_DIMCOUNTS_:
  case zVAR_DIMINTERVALS_: {
    struct cdfSTRUCT *CDF;
    struct varSTRUCT *Var;
    long *values = va_arg (Va->ap, long *);
    int dimN;
    SelectCDF (Cur->cdf, CDF, NO_CDF_SELECTED)
    if (!CURRENTvarSELECTED(CDF,TRUE)) return NO_VAR_SELECTED;
    if (!sX(InitCurrentVar(CDF,TRUE,&Var),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    switch (Va->item) {
      case zVAR_DIMINDICES_:
	for (dimN = 0; dimN < Var->numDims; dimN++)
	   if (values[dimN] < 0 || Var->dimSizes[dimN] <= values[dimN])
	     return BAD_DIM_INDEX;
	   else
	     Var->zRD.dimIndices[dimN] = values[dimN];
	break;
      case zVAR_DIMCOUNTS_:
	for (dimN = 0; dimN < Var->numDims; dimN++)
	   if (values[dimN] < 1)
	     return BAD_DIM_COUNT;
	   else
	     Var->zRD.dimCounts[dimN] = values[dimN];
	break;
      case zVAR_DIMINTERVALS_:
	for (dimN = 0; dimN < Var->numDims; dimN++)
	   if (values[dimN] < 1)
	     return BAD_DIM_INTERVAL;
	   else
	     Var->zRD.dimIntervals[dimN] = values[dimN];
	break;
    }
    break;
  }

  /****************************************************************************
  * rVAR_SEQPOS_/zVAR_SEQPOS_, 
  ****************************************************************************/

  case rVAR_SEQPOS_:
  case zVAR_SEQPOS_: {
    Logical zOp = (Va->item == zVAR_SEQPOS_);
    struct cdfSTRUCT *CDF;
    struct varSTRUCT *Var;
    long iVoffset;               /* Value offset within record. */
    int dimN;
    long recNumber = va_arg (Va->ap, long);
    long *dimIndices = va_arg (Va->ap, long *);
    SelectCDF (Cur->cdf, CDF, NO_CDF_SELECTED)
    if (BADzOP(CDF,!zOp)) return ILLEGAL_IN_zMODE;
    if (recNumber < 0) return BAD_REC_NUM;
    if (!CURRENTvarSELECTED(CDF,zOp)) return NO_VAR_SELECTED;
    if (!sX(InitCurrentVar(CDF,zOp,&Var),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    for (dimN = 0; dimN < Var->numDims; dimN++)
       if (dimIndices[dimN] < 0 ||
	   dimIndices[dimN] >= Var->dimSizes[dimN]) return BAD_DIM_INDEX;
    iVoffset = IndicesValueOffset (Var->numDims, dimIndices, Var->dimVarys,
				   Var->nPhyDimValues);
    Var->seqValueOffset = (Var->recVary ? recNumber * Var->NphyRecValues : 0) +
			  iVoffset;
    break;
  }

  /****************************************************************************
  * ATTR_/ATTR_NAME_
  *   Select the current attribute by number/name.
  ****************************************************************************/

  case ATTR_:
  case ATTR_NAME_: {
    Logical nameOp = (Va->item == ATTR_NAME_);
    long attrNum; char *attrName; struct cdfSTRUCT *CDF;
    CDFstatus tStatus; Int32 offset;
    if (nameOp)
      attrName = va_arg (Va->ap, char *);
    else {
      attrNum = va_arg (Va->ap, long);
      if (attrNum < 0) return BAD_ATTR_NUM;
    }
    /**************************************************************************
    * Determine current attribute offset.
    **************************************************************************/
    SelectCDF (Cur->cdf, CDF, NO_CDF_SELECTED)
    tStatus = BOO(nameOp,FindAttrByName(CDF,attrName,&offset),
			 FindAttrByNumber(CDF,attrNum,&offset));
    switch (tStatus) {
      case CDF_OK:
	CDF->CURattrOffset = offset;
	break;
      case NO_SUCH_ATTR:
	return tStatus;
      default:
	AbortAccess (CDF, FALSE, Cur);
	return tStatus;
    }
    /**************************************************************************
    * Reset current entry offsets.
    **************************************************************************/
    if (!sX(SetCURgrEntry(CDF,FALSE,CDF->CURgrEntryNum),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    if (!sX(SetCURzEntry(CDF,FALSE,CDF->CURzEntryNum),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    break;
  }

  /****************************************************************************
  * gENTRY_/rENTRY_/zENTRY_, select the current g/r/zEntry by number.
  ****************************************************************************/

  case gENTRY_:
  case rENTRY_:
  case zENTRY_: {
    struct cdfSTRUCT *CDF; Logical zOp = (Va->item == zENTRY_);
    long entryNum = va_arg (Va->ap, long);
    /**************************************************************************
    * Setup/validate operation.
    **************************************************************************/
    SelectCDF (Cur->cdf, CDF, NO_CDF_SELECTED)
    if (BADzOP(CDF,Va->item==rENTRY_)) return ILLEGAL_IN_zMODE;
    if (entryNum < 0) return BAD_ENTRY_NUM;
    /**************************************************************************
    * Set current entry number and offset.
    **************************************************************************/
    if (!sX(BOO(zOp,SetCURzEntry(CDF,TRUE,entryNum),
		    SetCURgrEntry(CDF,TRUE,entryNum)),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    break;
  }

  /****************************************************************************
  * rENTRY_NAME_/zENTRY_NAME_, select the current r/zEntry number by variable
  * name.
  ****************************************************************************/

  case rENTRY_NAME_:
  case zENTRY_NAME_: {
    void *varName = va_arg (Va->ap, void *);
    Logical zOp = (Va->item == zENTRY_NAME_), zVar;
    struct cdfSTRUCT *CDF;
    Int32 offset, varN;
    long entryNum;
    /**************************************************************************
    * Setup/validate operation.
    **************************************************************************/
    SelectCDF (Cur->cdf, CDF, NO_CDF_SELECTED)
    if (BADzOP(CDF,Va->item == rENTRY_NAME_)) return ILLEGAL_IN_zMODE;
    /**************************************************************************
    * Locate the VDR.
    **************************************************************************/
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
    /**************************************************************************
    * Read the variable number.
    **************************************************************************/
    if (!sX(ReadVDR(CDF,offset,zVar,VDR_NUM,&varN,VDR_NULL),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    /**************************************************************************
    * Determine the new entry number.
    **************************************************************************/
    if (zModeON(CDF))
      if (zVar)
	entryNum = CDF->NrVars + varN;
      else
	entryNum = varN;
    else
      if (zVar)
	if (zOp)
	  entryNum = varN;
	else
	  return NO_SUCH_VAR;                   /* Wrong type of variable. */
      else
	if (zOp)
	  return NO_SUCH_VAR;                   /* Wrong type of variable. */
	else
	  entryNum = varN;
    /**************************************************************************
    * Set the current entry number and offset.
    **************************************************************************/
    if (!sX(BOO(zOp,SetCURzEntry(CDF,FALSE,entryNum),
		    SetCURgrEntry(CDF,FALSE,entryNum)),&pStatus)) {
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
