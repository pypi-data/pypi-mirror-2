/******************************************************************************
*
*  NSSDC/CDF                                    CDF `put' operations, part 1.
*
*  Version 1.4a, 4-Aug-95, Hughes STX.
*
*  Modification history:
*
*   V1.0  20-May-92, J Love     Original version (was part of `cdflib.c').
*   V1.1  16-Sep-92, J Love     CDF V2.3 (shareable/NeXT/zVar).
*   V1.1  16-Sep-92, J Love     CDF V2.3 (shareable/NeXT/zVar).
*   V1.2  10-Dec-93, J Love     CDF V2.4.  Added readonly mode and zMode.
*   V1.3  15-Dec-94, J Love     CDF V2.5.
*   V1.3a  6-Jan-95, J Love	Encode/decode changes.  More cache-residency.
*   V1.3b 15-Mar-95, J Love	Solaris 2.3 IDL i/f.  Fixed `recNum' argument
*				to `LastAllocatedRecord'.
*   V1.4  30-May-95, J Love	Fixed bug in <PUT_,r/zVAR_PADVALUE_> involving
*				use of old VDR offset after the VDR was moved.
*   V1.4a  4-Aug-95, J Love	CDFexport-related changes.
*
******************************************************************************/

#include "cdflib.h"

/******************************************************************************
* CDFput1.
******************************************************************************/

STATICforIDL CDFstatus CDFput1 (Va, Cur)
struct VAstruct *Va;
struct CURstruct *Cur;
{
CDFstatus tStatus, pStatus = CDF_OK;

switch (Va->item) {
  /****************************************************************************
  * rVAR_NAME_/zVAR_NAME_, rename the current variable.  A variable with the
  * same name must not already exist in the CDF.
  ****************************************************************************/
  case rVAR_NAME_:
  case zVAR_NAME_: {
    Logical zOp = (Va->item == zVAR_NAME_), zVarCur;
    struct cdfSTRUCT *CDF;
    char *varName = va_arg (Va->ap, char *), tmpName[CDF_VAR_NAME_LEN+1];
    Int32 offsetCur, offsetFound;
    SelectCDF (Cur->cdf, CDF, NO_CDF_SELECTED)
    if (BADzOP(CDF,!zOp)) return ILLEGAL_IN_zMODE;
    if (!CURRENTvarSELECTED(CDF,zOp)) return NO_VAR_SELECTED;
    if (!sX(LocateCurrentVar(CDF,zOp,&offsetCur,&zVarCur,NULL),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    if (strlen(varName) > (size_t) CDF_VAR_NAME_LEN) {
      if (!sX(VAR_NAME_TRUNC,&pStatus)) return pStatus;
    }
    strcpyX (tmpName, varName, CDF_VAR_NAME_LEN);
    if (!ValidVarName(tmpName)) return BAD_VAR_NAME;
    /**************************************************************************
    * Check that the new variable name is not already in use.  Don't flag as
    * an error if the new name is the same as the old name (ignoring trailing
    * blanks).  Trailing blanks may be being eliminated.
    **************************************************************************/
    tStatus = FindVarByName (CDF, tmpName, &offsetFound, NULL, NULL);
    switch (tStatus) {
      case CDF_OK:
	if (offsetFound != offsetCur) return VAR_EXISTS;
	break;
      case NO_SUCH_VAR:
	break;
      default:
	AbortAccess (CDF, FALSE, Cur);
	return tStatus;
    }
    if (CDF->status != CDF_READ_WRITE) {
      if (!WriteAccess(CDF,Cur,&pStatus)) return pStatus;
    }
    NulPad (tmpName, CDF_VAR_NAME_LEN);
    if (!sX(WriteVDR(CDF,offsetCur,zVarCur,VDR_NAME,
		     tmpName,VDR_NULL),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    break;
  }

  /****************************************************************************
  * rVAR_DATASPEC_/zVAR_DATASPEC_, 
  *   If the data types are not equivalent or the number of elements are
  *   different, then check for the following:
  *     1) if any records have been written
  *     2) if a pad value has been specified
  *   If either is true, then the data specification cannot be changed.
  ****************************************************************************/

  case rVAR_DATASPEC_:
  case zVAR_DATASPEC_: {
    Logical zOp = (Va->item == zVAR_DATASPEC_), zVar;
    struct cdfSTRUCT *CDF;
    struct varSTRUCT *Var;
    long newDataType = va_arg (Va->ap, long);
    long newNumElems = va_arg (Va->ap, long);
    Int32 offset, flags, dataType, numElems, maxRec;
    SelectCDF (Cur->cdf, CDF, NO_CDF_SELECTED)
    if (BADzOP(CDF,!zOp)) return ILLEGAL_IN_zMODE;
    if (!CURRENTvarSELECTED(CDF,zOp)) return NO_VAR_SELECTED;
    if (!sX(LocateCurrentVar(CDF,zOp,&offset,&zVar,&Var),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    if (!ValidDataType(newDataType)) return BAD_DATA_TYPE;
    if (newNumElems < 1) return BAD_NUM_ELEMS;
    if (!STRINGdataType(newDataType)) {
      if (newNumElems != 1) return BAD_NUM_ELEMS;
    }
    if (!sX(ReadVDR(CDF,offset,zVar,VDR_FLAGS,&flags,
				    VDR_DATATYPE,&dataType,
				    VDR_NUMELEMS,&numElems,
				    VDR_NULL),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    /**************************************************************************
    * If this variable has not yet been initialized, read the maximum record
    * number written.
    **************************************************************************/
    if (Var == NULL) {
      if (!sX(ReadVDR(CDF,offset,zVar,VDR_MAXREC,&maxRec,VDR_NULL),&pStatus)) {
	AbortAccess (CDF, FALSE, Cur);
	return pStatus;
      }
    }
    else
      maxRec = Var->maxRec;
    /**************************************************************************
    * If the data specifications are not equivalent, check if any records have
    * been written or a pad value has been specified.
    **************************************************************************/
    if (!EquivDataTypes(newDataType,dataType) || (newNumElems != numElems)) {
      if (maxRec > -1) return CANNOT_CHANGE;
      if (PADvalueBITset(flags)) return CANNOT_CHANGE;
    }
    if (CDF->status != CDF_READ_WRITE) {
      if (!WriteAccess(CDF,Cur,&pStatus)) return pStatus;
    }
    /**************************************************************************
    * Update the VDR with the new data specification and update the data
    * specification in memory if the variable has been initialized.
    **************************************************************************/
    dataType = newDataType;
    numElems = newNumElems;
    if (!sX(WriteVDR(CDF,offset,zVar,VDR_DATATYPE,&dataType,
				     VDR_NUMELEMS,&numElems,
				     VDR_NULL),&pStatus)){
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    /**************************************************************************
    * If this variable has been initialized, recalculate its parameters.
    **************************************************************************/
    if (Var != NULL) {
      if (!sX(CalcVarParms(CDF,Var),&pStatus)) {
	AbortAccess (CDF, FALSE, Cur);
	return pStatus;
      }
    }
    break;
  }

  /****************************************************************************
  * rVAR_RECVARY_/zVAR_RECVARY_, 
  *   Can't change if any records have been written.
  ****************************************************************************/

  case rVAR_RECVARY_:
  case zVAR_RECVARY_: {
    Logical zOp = (Va->item == zVAR_RECVARY_), zVar;
    struct cdfSTRUCT *CDF;
    struct varSTRUCT *Var;
    long recVariance = va_arg (Va->ap, long);
    struct VDRstruct VDR;
    Int32 offset;
    SelectCDF (Cur->cdf, CDF, NO_CDF_SELECTED)
    if (BADzOP(CDF,!zOp)) return ILLEGAL_IN_zMODE;
    if (!CURRENTvarSELECTED(CDF,zOp)) return NO_VAR_SELECTED;
    if (!sX(LocateCurrentVar(CDF,zOp,&offset,&zVar,&Var),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    if (!sX(ReadVDR(CDF,offset,zVar,VDR_RECORD,&VDR,NULL,VDR_NULL),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    if (BOO(Var == NULL,VDR.MaxRec,Var->maxRec) > -1) return CANNOT_CHANGE;
    if (CDF->status != CDF_READ_WRITE) {
      if (!WriteAccess(CDF,Cur,&pStatus)) return pStatus;
    }
    if (recVariance)
      SetBit32 (&VDR.Flags,VDR_RECVARY_BIT);
    else
      ClearBit32 (&VDR.Flags,VDR_RECVARY_BIT);
    if (!sX(WriteVDR(CDF,offset,zVar,VDR_RECORD,&VDR,NULL,VDR_NULL),&pStatus)){
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    /**************************************************************************
    * If this variable has been initialized, recalculate its parameters.
    **************************************************************************/
    if (Var != NULL) {
      if (!sX(CalcVarParms(CDF,Var),&pStatus)) {
	AbortAccess (CDF, FALSE, Cur);
	return pStatus;
      }
    }
    break;
  }

  /****************************************************************************
  * rVAR_DIMVARYS_/zVAR_DIMVARYS_
  *     Respecify dimension variances for current rVariable/zVariable.  Can't
  * change if any records have been written or if zMode/2 and really an
  * rVariable.
  ****************************************************************************/

  case rVAR_DIMVARYS_:
  case zVAR_DIMVARYS_: {
    Logical zOp = (Va->item == zVAR_DIMVARYS_), zVar;
    struct cdfSTRUCT *CDF;
    struct varSTRUCT *Var;
    int dimN;
    struct VDRstruct VDR;
    long *dimVarys = va_arg (Va->ap, long *);
    Int32 offset, numDims;
    SelectCDF (Cur->cdf, CDF, NO_SUCH_CDF);
    if (BADzOP(CDF,!zOp)) return ILLEGAL_IN_zMODE;
    if (!CURRENTvarSELECTED(CDF,zOp)) return NO_VAR_SELECTED;
    if (!sX(LocateCurrentVar(CDF,zOp,&offset,&zVar,&Var),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    if (CDF->zMode == zMODEon2 && !zVar) return CANNOT_CHANGE;
    if (!sX(ReadVDR(CDF,offset,zVar,VDR_RECORD,&VDR,NULL,VDR_NULL),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    if (BOO(Var == NULL,VDR.MaxRec,Var->maxRec) > -1) return CANNOT_CHANGE;
    if (CDF->status != CDF_READ_WRITE) {
      if (!WriteAccess(CDF,Cur,&pStatus)) return pStatus;
    }
    numDims = BOO(zVar,VDR.zNumDims,CDF->rNumDims);
    for (dimN = 0; dimN < numDims; dimN++) {
       VDR.DimVarys[dimN] = BOO(dimVarys[dimN],VARY,NOVARY);
    }
    if (!sX(WriteVDR(CDF,offset,zVar,VDR_RECORD,&VDR,NULL,VDR_NULL),&pStatus)){
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    /**************************************************************************
    * If this variable has been initialized, recalculate its parameters.
    *************************************************************************/
    if (Var != NULL) {
      if (!sX(CalcVarParms(CDF,Var),&pStatus)) {
	AbortAccess (CDF, FALSE, Cur);
	return pStatus;
      }
    }
    break;
  }

  /****************************************************************************
  * rVAR_ALLOCATERECS_/zVAR_ALLOCATERECS_,
  *    Allocate a number of records for the current variable.
  * Can't set if any records have been written already.
  ****************************************************************************/

  case rVAR_ALLOCATERECS_:
  case zVAR_ALLOCATERECS_: {
    Logical zOp = (Va->item == zVAR_ALLOCATERECS_);
    struct cdfSTRUCT *CDF;
    struct varSTRUCT *Var;
    long NallocateRecs = va_arg (Va->ap, long);
    SelectCDF (Cur->cdf, CDF, NO_CDF_SELECTED)
    if (BADzOP(CDF,!zOp)) return ILLEGAL_IN_zMODE;
    if (!CURRENTvarSELECTED(CDF,zOp)) return NO_VAR_SELECTED;
    if (!CDF->singleFile) {
      if (!sX(SINGLE_FILE_FORMAT,&pStatus)) return pStatus;
      break;
    }
    if (!sX(InitCurrentVar(CDF,zOp,&Var),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    if (Var->sFile.maxAllocated > -1) return CANNOT_CHANGE;
    if (NallocateRecs < 1) return BAD_ALLOCATE_RECS;
    if (!Var->recVary && NallocateRecs > 1) return BAD_ALLOCATE_RECS;
    if (CDF->status != CDF_READ_WRITE) {
      if (!WriteAccess(CDF,Cur,&pStatus)) return pStatus;
    }
    if (!sX(SingleAllocateRecords(CDF,Var,NallocateRecs-1,TRUE),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    break;
  }

  /****************************************************************************
  * rVAR_INITIALRECS_/zVAR_INITIALRECS_,
  *    Specify (write) an initial number of records for the current variable.
  * Can't set if any records have been written already.
  ****************************************************************************/

  case rVAR_INITIALRECS_:
  case zVAR_INITIALRECS_: {
    Logical zOp = (Va->item == zVAR_INITIALRECS_);
    struct cdfSTRUCT *CDF;
    struct varSTRUCT *Var;
    long phyRecNum;
    long NinitialRecs = va_arg (Va->ap, long);
    SelectCDF (Cur->cdf, CDF, NO_CDF_SELECTED)
    if (BADzOP(CDF,!zOp)) return ILLEGAL_IN_zMODE;
    if (!CURRENTvarSELECTED(CDF,zOp)) return NO_VAR_SELECTED;
    if (!sX(InitCurrentVar(CDF,zOp,&Var),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    if (Var->maxRec > -1) return CANNOT_CHANGE;
    if (CDF->singleFile && Var->sFile.maxAllocated > -1) return CANNOT_CHANGE;
    if (NinitialRecs < 1) return BAD_INITIAL_RECS;
    if (!Var->recVary && NinitialRecs > 1) return BAD_INITIAL_RECS;
    if (CDF->status != CDF_READ_WRITE) {
      if (!WriteAccess(CDF,Cur,&pStatus)) return pStatus;
    }
    if (Var->status == VAR_CLOSED) {
      if (!sX(ReadWriteVar(CDF,Var),&pStatus)) {
	AbortAccess (CDF, FALSE, Cur);
	return pStatus;
      }
    }
    phyRecNum = NinitialRecs - 1;
    if (CDF->singleFile) {
      if (!sX(SingleAllocateRecords(CDF,Var,phyRecNum,TRUE),&pStatus)) {
	AbortAccess (CDF, FALSE, Cur);
	return pStatus;
      }
    }
    if (!sX(PadRecords(CDF,Var,0L,phyRecNum),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    UpdateMaxRec (CDF, Var, phyRecNum);
    break;
  }

  /****************************************************************************
  * rVAR_EXTENDRECS_/zVAR_EXTENDRECS_, specifies the number of records to
  * extend a variable when necessary.  A value may be specified regardless of
  * whether or not it will be used.  This value is ignored for NRV variables
  * and for multi-file CDFs.  In all cases the value is stored in the CDF
  * and may be inquired at a later time.
  ****************************************************************************/

  case rVAR_EXTENDRECS_:
  case zVAR_EXTENDRECS_: {
    Logical zOp = (Va->item == zVAR_EXTENDRECS_), zVar;
    struct cdfSTRUCT *CDF;
    struct varSTRUCT *Var;
    Int32 nExtRecs32 = (Int32) va_arg (Va->ap, long), offset;
    SelectCDF (Cur->cdf, CDF, NO_CDF_SELECTED)
    if (BADzOP(CDF,!zOp)) return ILLEGAL_IN_zMODE;
    if (!CURRENTvarSELECTED(CDF,zOp)) return NO_VAR_SELECTED;
    if (!sX(LocateCurrentVar(CDF,zOp,&offset,&zVar,&Var),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    /**************************************************************************
    * Validate number of extend records.  Zero (0) is valid meaning that the
    * default is to be used.
    **************************************************************************/
    if (nExtRecs32 < 0) return BAD_EXTEND_RECS;
    if (CDF->status != CDF_READ_WRITE) {
      if (!WriteAccess(CDF,Cur,&pStatus)) return pStatus;
    }
    if (!sX(WriteVDR(CDF,offset,zVar,VDR_NEXTENDRECS,
		     &nExtRecs32,VDR_NULL),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    /**************************************************************************
    * If this variable has been initialized, recalculate its parameters.
    *************************************************************************/
    if (Var != NULL) {
      if (!sX(CalcVarParms(CDF,Var),&pStatus)) {
	AbortAccess (CDF, FALSE, Cur);
	return pStatus;
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
    struct varSTRUCT *Var;
    struct VDRstruct VDR;
    void *padValue = va_arg (Va->ap, void *);
    Int32 offset,	/* Offset of VDR. */
	  newOffset,	/* Offset of VDR after "possibly" being moved. */
	  lastAllocated;
    SelectCDF (Cur->cdf, CDF, NO_CDF_SELECTED)
    if (BADzOP(CDF,!zOp)) return ILLEGAL_IN_zMODE;
    if (!CURRENTvarSELECTED(CDF,zOp)) return NO_VAR_SELECTED;
    if (!sX(LocateCurrentVar(CDF,zOp,&offset,&zVar,&Var),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    if (CDF->status != CDF_READ_WRITE) {
      if (!WriteAccess(CDF,Cur,&pStatus)) return pStatus;
    }
    if (!sX(ReadVDR(CDF,offset,zVar,VDR_RECORD,&VDR,NULL,VDR_NULL),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    if (PADvalueBITset(VDR.Flags)) {
      /************************************************************************
      * A pad value has already been specified - simply overwrite the existing
      * pad value.
      ************************************************************************/
      if (!sX(WriteVDR(CDF,offset,zVar,VDR_PADVALUE,
		       padValue,VDR_NULL),&pStatus)) {
	AbortAccess (CDF, FALSE, Cur);
	return pStatus;
      }
      newOffset = offset;
    }
    else {
      /************************************************************************
      * A pad value has not yet been specified.
      ************************************************************************/
      int nBytes = (int) (CDFelemSize(VDR.DataType) * VDR.NumElems);
      SetBit32 (&VDR.Flags,VDR_PADVALUE_BIT);
      if (!sX(ResizeInternalRecord(CDF,VDR.RecordSize,offset,
				   VDR.RecordSize+nBytes,&newOffset,
				   TRUE,NULL),&pStatus)) {
	AbortAccess (CDF, FALSE, Cur);
	return pStatus;
      }
      VDR.RecordSize += nBytes;
      if (!sX(WriteVDR(CDF,newOffset,zVar,VDR_RECORD,&VDR,padValue,
					  VDR_NULL),&pStatus)){
	AbortAccess (CDF, FALSE, Cur);
	return pStatus;
      }
      if (newOffset != offset) {
	if (VDR.Num > 0) {
	  Int32 prevOffset;
	  if (!sX(FindVarByNumber(CDF,(VDR.Num-1),
				  &prevOffset,zVar),&pStatus)) {
	    AbortAccess (CDF, FALSE, Cur);
	    return pStatus;
	  }
	  if (!sX(WriteVDR(CDF,prevOffset,zVar,
			   VDR_VDRNEXT,&newOffset,VDR_NULL),&pStatus)) {
	    AbortAccess (CDF, FALSE, Cur);
	    return pStatus;
	  }
	}
	else {
	  if (!sX(WriteGDR(CDF,BOO(zVar,GDR_zVDRHEAD,GDR_rVDRHEAD),
			   &newOffset,GDR_NULL),&pStatus)) {
	    AbortAccess (CDF, FALSE, Cur);
	    return pStatus;
	  }
	}
	if (Var != NULL) Var->VDRoffset = newOffset;
      }
    }
    /**************************************************************************
    * If a single-file CDF, indicate that allocated records may have to be
    * padded when the CDF is closed.
    **************************************************************************/
    if (CDF->singleFile) {
      if (Var == NULL) {
	if (!sX(LastAllocatedRecord(CDF,newOffset,
				    zVar,&lastAllocated),&pStatus)) {
	  AbortAccess (CDF, FALSE, Cur);
	  return pStatus;
	}
	if (lastAllocated > VDR.MaxRec) {
	  if (!sX(InitVar(CDF,VDR.Num,zVar,&Var),&pStatus)) {
	    AbortAccess (CDF, FALSE, Cur);
	    return pStatus;
	  }
	  Var->sFile.maxWritten = Var->maxRec;
	}
      }
      else {
	if (Var->sFile.maxAllocated > Var->maxRec) {
	  Var->sFile.maxWritten = Var->maxRec;
	}
      }
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
    void *value = va_arg (Va->ap, char *);
    SelectCDF (Cur->cdf, CDF, NO_CDF_SELECTED)
    if (BADzOP(CDF,!zOp)) return ILLEGAL_IN_zMODE;
    if (!CURRENTvarSELECTED(CDF,zOp)) return NO_VAR_SELECTED;
    if (!sX(InitCurrentVar(CDF,zOp,&Var),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    if (CDF->status != CDF_READ_WRITE) {
      if (!WriteAccess(CDF,Cur,&pStatus)) return pStatus;
    }
    if (Var->status == VAR_CLOSED) {
      if (!sX(ReadWriteVar(CDF,Var),&pStatus)) {
	AbortAccess (CDF, FALSE, Cur);
	return pStatus;
      }
    }
    rd = BOO(zModeON(CDF),&(Var->zRD),BOO(zOp,&(Var->zRD),&(CDF->rRD)));
    /**************************************************************************
    * Compute physical record number and allocate/pad additional records if
    * necessary.
    **************************************************************************/
    phyRecNum = (Var->recVary ? rd->recNumber : 0);
    if (phyRecNum > Var->maxRec) {
      if (!CDF->singleFile) {
	if (!sX(PadRecords(CDF,Var,Var->maxRec+1,
			   BOO(Var->NphyRecValues == 1,
			       phyRecNum-1,phyRecNum)),&pStatus)) {
	  AbortAccess (CDF, FALSE, Cur);
	  return pStatus;
	}
      }
      else {
	if (phyRecNum > Var->sFile.maxAllocated) {
	  if (!sX(SingleAllocateRecords(CDF,Var,phyRecNum,
					(Var->recVary ? FALSE : TRUE)),
								  &pStatus)) {
	    AbortAccess (CDF, FALSE, Cur);
	    return pStatus;
	  }
	}
	if (!sX(PadRecords(CDF,Var,Var->sFile.maxWritten+1,
			   BOO(Var->NphyRecValues == 1,
			       phyRecNum-1,phyRecNum)),&pStatus)) {
	  AbortAccess (CDF, FALSE, Cur);
	  return pStatus;
	}
      }
      UpdateMaxRec (CDF, Var, phyRecNum);
    }
    /**************************************************************************
    * Put variable data value.
    **************************************************************************/
    offset = ValueByteOffset (CDF, Var, phyRecNum, rd->dimIndices);
    if (!SEEKv(Var->fp,(long)offset,vSEEK_SET)) {
      AbortAccess (CDF, FALSE, Cur);
      return VAR_WRITE_ERROR;
    }
    if (!sX(WriteVarElems(Var,Var->NvalueElems,value),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
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
    int dimN;
    struct cdfSTRUCT *CDF;
    struct varSTRUCT *Var;
    struct rdSTRUCT *rd;
#if LIMITof64K
    long Nvalues, Nbytes;
#endif
    void *buffer = va_arg (Va->ap, char *);
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
    if (CDF->status != CDF_READ_WRITE) {
      if (!WriteAccess(CDF,Cur,&pStatus)) return pStatus;
    }
    if (Var->status == VAR_CLOSED) {
      if (!sX(ReadWriteVar(CDF,Var),&pStatus)) {
	AbortAccess (CDF, FALSE, Cur);
	return pStatus;
      }
    }
    if (!sX(HyperWrite(CDF,Var,rd,buffer),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    Var->accessed_at = Cur->cdf->pseudo_clock++;
    break;
  }

  /****************************************************************************
  * rVAR_SEQDATA_/zVAR_SEQDATA_, 
  ****************************************************************************/

  case rVAR_SEQDATA_:
  case zVAR_SEQDATA_: {
    Logical zOp = (Va->item == zVAR_SEQDATA_);
    struct varSTRUCT *Var;
    struct cdfSTRUCT *CDF;
    long phyRecNum;
    Int32 offset;
    void *value = va_arg (Va->ap, char *);
    SelectCDF (Cur->cdf, CDF, NO_CDF_SELECTED)
    if (BADzOP(CDF,!zOp)) return ILLEGAL_IN_zMODE;
    if (!CURRENTvarSELECTED(CDF,zOp)) return NO_VAR_SELECTED;
    if (!sX(InitCurrentVar(CDF,zOp,&Var),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    /**************************************************************************
    * Compute physical record number and determine if this is a legal write.
    **************************************************************************/
    phyRecNum = Var->seqValueOffset / Var->NphyRecValues;
    if ((!Var->recVary) && (phyRecNum > 0)) return END_OF_VAR;
    if (CDF->status != CDF_READ_WRITE) {
      if (!WriteAccess(CDF,Cur,&pStatus)) return pStatus;
    }
    if (Var->status == VAR_CLOSED) {
      if (!sX(ReadWriteVar(CDF,Var),&pStatus)) {
	AbortAccess (CDF, FALSE, Cur);
	return pStatus;
      }
    }
    /**************************************************************************
    * Allocate/pad additional records if necessary.
    **************************************************************************/
    if (phyRecNum > Var->maxRec) {
      if (!CDF->singleFile) {
	if (!sX(PadRecords(CDF,Var,Var->maxRec+1,
			   BOO(Var->NphyRecValues == 1,
			       phyRecNum-1,phyRecNum)),&pStatus)) {
	  AbortAccess (CDF, FALSE, Cur);
	  return pStatus;
	}
      }
      else {
	if (phyRecNum > Var->sFile.maxAllocated) {
	  if (!sX(SingleAllocateRecords(CDF,Var,phyRecNum,
					(Var->recVary ? FALSE : TRUE)),
								  &pStatus)) {
	    AbortAccess (CDF, FALSE, Cur);
	    return pStatus;
	  }
	}
	if (!sX(PadRecords(CDF,Var,Var->sFile.maxWritten+1,
			   BOO(Var->NphyRecValues == 1,
			       phyRecNum-1,phyRecNum)),&pStatus)) {
	  AbortAccess (CDF, FALSE, Cur);
	  return pStatus;
	}
      }
      UpdateMaxRec (CDF, Var, phyRecNum);
    }
    /**************************************************************************
    * Put variable data value.
    **************************************************************************/
    offset = SeqValueByteOffset (CDF, Var);
    if (!SEEKv(Var->fp,(long)offset,vSEEK_SET)) {
      AbortAccess (CDF, FALSE, Cur);
      return VAR_WRITE_ERROR;
    }
    if (!sX(WriteVarElems(Var,Var->NvalueElems,value),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    Var->seqValueOffset++;
    Var->accessed_at = Cur->cdf->pseudo_clock++;
    break;
  }

  /****************************************************************************
  * rVARs_RECDATA_/zVARs_RECDATA_, write physical data records for up to all
  * of the rVariables/zVariables.
  ****************************************************************************/

  case rVARs_RECDATA_:
  case zVARs_RECDATA_: {
    Logical zOp = (Va->item == zVARs_RECDATA_), zVar;
    struct varSTRUCT *Var;
    struct cdfSTRUCT *CDF;
    long recNum, varNt;
    Byte *tBuffer;
    int varX;
    Int32 offset;
    long nVars = va_arg (Va->ap, long);
    long *varNs = va_arg (Va->ap, long *);
    void *buffer = va_arg (Va->ap, char *);
#if LIMITof64K
    long nBytes;
#endif
    SelectCDF (Cur->cdf, CDF, NO_CDF_SELECTED)
    if (BADzOP(CDF,!zOp)) return ILLEGAL_IN_zMODE;
    if (nVars < 1) return BAD_NUM_VARS;
    if (CDF->status != CDF_READ_WRITE) {
      if (!WriteAccess(CDF,Cur,&pStatus)) return pStatus;
    }
    for (varX = 0; varX < nVars; varX++) {
       if (!sX(VarIdentity(CDF,varNs[varX],zOp,
			   &varNt,&zVar,NULL),&pStatus)) return pStatus;
       if (!sX(InitVar(CDF,varNt,zVar,NULL),&pStatus)) {
	 AbortAccess (CDF, FALSE, Cur);
	 return pStatus;
       }
    }
#if LIMITof64K
    for (varX = 0, nBytes = 0; varX < nVars; varX++) {
       if (!sX(VarIdentity(CDF,varNs[varX],zOp,
			   NULL,NULL,&Var),&pStatus)) return pStatus;
       nBytes += Var->NphyRecBytes;
    }
    if (TOObigIBMpc(nBytes)) return IBM_PC_OVERFLOW;
#endif
    /**************************************************************************
    * Write to each selected variable.
    **************************************************************************/
    for (varX = 0, tBuffer = buffer; varX < nVars; varX++) {
       if (!sX(VarIdentity(CDF,varNs[varX],zOp,
			   NULL,NULL,&Var),&pStatus)) return pStatus;
       if (Var->status == VAR_CLOSED) {
	 if (!sX(ReadWriteVar(CDF,Var),&pStatus)) {
	   AbortAccess (CDF, FALSE, Cur);
	   return pStatus;
	 }
       }
       recNum = BOO(Var->recVary,BOO(zOp,Var->zRD.recNumber,
					 CDF->rRD.recNumber),0);
       if (!CDF->singleFile) {
	 if (recNum - 1 > Var->maxRec) {
	   if (!sX(PadRecords(CDF,Var,Var->maxRec+1,recNum-1),&pStatus)) {
	     AbortAccess (CDF, FALSE, Cur);
	     return pStatus;
	   }
	 }
       }
       else {
	 if (recNum > Var->sFile.maxAllocated) {
	   if (!sX(SingleAllocateRecords(CDF,Var,recNum,
					 (Var->recVary ? FALSE:TRUE)),
								  &pStatus)) {
	     AbortAccess (CDF, FALSE, Cur);
	     return pStatus;
	   }
	 }
	 if (!sX(PadRecords(CDF,Var,Var->sFile.maxWritten+1,
			    recNum-1),&pStatus)) {
	   AbortAccess (CDF, FALSE, Cur);
	   return pStatus;
	 }
       }
       offset = RecordByteOffset (CDF, Var, recNum);
       if (!SEEKv(Var->fp,(long)offset,vSEEK_SET)) {
	 AbortAccess (CDF, FALSE, Cur);
	 return VAR_WRITE_ERROR;
       }
       if (!sX(WriteVarElems(Var,Var->NphyRecElems,tBuffer),&pStatus)) {
	 AbortAccess (CDF, FALSE, Cur);
	 return pStatus;
       }
       UpdateMaxRec (CDF, Var, recNum);
       tBuffer += (size_t) Var->NphyRecBytes;
       Var->accessed_at = CDF->pseudo_clock++;
    }

    break;
  }

  /****************************************************************************
  * Look in `cdfput2.c' for these items.
  ****************************************************************************/

  case CDF_ENCODING_:
  case CDF_MAJORITY_:
  case CDF_FORMAT_:
  case ATTR_NAME_:
  case ATTR_SCOPE_:
  case gENTRY_DATA_:
  case rENTRY_DATA_:
  case zENTRY_DATA_:
  case gENTRY_DATASPEC_:
  case rENTRY_DATASPEC_:
  case zENTRY_DATASPEC_:
    return CDFput2 (Va, Cur);

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
