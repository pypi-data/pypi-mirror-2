/******************************************************************************
*
*  NSSDC/CDF                                        CDF `delete' operations.
*
*  Version 1.3b, 24-Feb-95, Hughes STX.
*
*  Modification history:
*
*   V1.0  20-May-92, J Love     Original version (was part of `cdflib.c').
*   V1.1  21-Aug-92, J Love     CDF V2.3 (shareable/NeXT,zVar).
*   V1.2  30-Nov-93, J Love     CDF V2.4.  Readonly mode, deleting V1 CDFs on
*                               all machines.
*   V1.3   5-Dec-94, J Love     CDF V2.5.
*   V1.3a  6-Jan-95, J Love	More cache-residency.
*   V1.3b 24-Feb-95, J Love	Solaris 2.3 IDL i/f.
*
******************************************************************************/

#include "cdflib.h"

/******************************************************************************
* CDFdel.
******************************************************************************/

STATICforIDL CDFstatus CDFdel (Va, Cur)
struct VAstruct *Va;
struct CURstruct *Cur;
{
CDFstatus tStatus, pStatus = CDF_OK;

switch (Va->item) {
  /****************************************************************************
  * CDF_, delete an open CDF.
  ****************************************************************************/
  case CDF_: {
    struct cdfSTRUCT *CDF;
    SelectCDF (Cur->cdf, CDF, NO_CDF_SELECTED)
    if (CDF->status != CDF_READ_WRITE) {
      if (!DeleteAccess(CDF,Cur,&pStatus)) return pStatus;
    }
    AbortAccess (CDF, TRUE, Cur);
    break;
  }

  /****************************************************************************
  * zVAR_/rVAR_
  ****************************************************************************/

  case zVAR_:
  case rVAR_: {
    Logical zOp = (Va->item == zVAR_), zVar;
    struct cdfSTRUCT *CDF;
    struct VDRstruct VDR, VDRt;
    struct VXRstruct VXRt;
    Int32 vOffset, tOffset, recordSize, rMaxRec = -1, aOffset, eOffset,
	  scope, entryN, VDRhead, nVars;
    int entryX, varN;
    /**************************************************************************
    * Get pointer to current CDF and locate the current r/zVariable.
    **************************************************************************/
    SelectCDF (Cur->cdf, CDF, NO_CDF_SELECTED)
    if (!CDF->singleFile) return UNSUPPORTED_OPERATION;
    if (BADzOP(CDF,!zOp)) return ILLEGAL_IN_zMODE;
    if (!CURRENTvarSELECTED(CDF,zOp)) return NO_VAR_SELECTED;
    if (!sX(LocateCurrentVar(CDF,zOp,&vOffset,&zVar,NULL),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    /**************************************************************************
    * Read GDR field(s).
    **************************************************************************/
    if (!sX(ReadGDR(CDF,BOO(zVar,GDR_zVDRHEAD,GDR_rVDRHEAD),&VDRhead,
			BOO(zVar,GDR_NzVARS,GDR_NrVARS),&nVars,
			GDR_NULL),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    /**************************************************************************
    * Read the VDR.
    **************************************************************************/
    if (!sX(ReadVDR(CDF,vOffset,zVar,VDR_RECORD,&VDR,NULL,VDR_NULL),&pStatus)){
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    /**************************************************************************
    * Switch to write access.
    **************************************************************************/
    if (CDF->status != CDF_READ_WRITE) {
      if (!WriteAccess(CDF,Cur,&pStatus)) return pStatus;
    }
    /**************************************************************************
    * Remove the VDR from the list of r/zVariables and decrement the number
    * of r/zVariables.  If this is a true rVariable, check for the maximum
    * record number written for the rVariables up to the one being deleted.
    **************************************************************************/
    if (VDRhead == vOffset)
      VDRhead = VDR.VDRnext;
    else {
      tOffset = VDRhead;
      while (tOffset != 0) {
	if (!sX(ReadVDR(CDF,tOffset,zVar,VDR_RECORD,
			&VDRt,NULL,VDR_NULL),&pStatus)){
	  AbortAccess (CDF, FALSE, Cur);
	  return pStatus;
	}
	if (!zVar) {
	  Int32 maxRec = BOO(CDF->rVars[(int)VDRt.Num] == NULL,
			     VDRt.MaxRec,CDF->rVars[(int)VDRt.Num]->maxRec);
	  rMaxRec = MAXIMUM (rMaxRec, maxRec);
	}
	if (VDRt.VDRnext == vOffset) {
	  VDRt.VDRnext = VDR.VDRnext;
	  if (!sX(WriteVDR(CDF,tOffset,zVar,
			   VDR_RECORD,&VDRt,NULL,VDR_NULL),&pStatus)) {
	    AbortAccess (CDF, FALSE, Cur);
	    return pStatus;
	  }
	  break;
	}
	tOffset = VDRt.VDRnext;
      }
      if (tOffset == 0) {
	AbortAccess (CDF, FALSE, Cur);
	return CORRUPTED_V2_CDF;
      }
    }
    nVars--;
    /**************************************************************************
    * Renumber following VDRs.  If this is a true rVariable, continue checking
    * for the maximum record number written.
    **************************************************************************/
    tOffset = VDR.VDRnext;
    while (tOffset != 0) {
      if (!sX(ReadVDR(CDF,tOffset,zVar,VDR_RECORD,
		      &VDRt,NULL,VDR_NULL),&pStatus)) {
	AbortAccess (CDF, FALSE, Cur);
	return pStatus;
      }
      if (!zVar) {
	Int32 maxRec = BOO(CDF->rVars[(int)VDRt.Num] == NULL,
			   VDRt.MaxRec,CDF->rVars[(int)VDRt.Num]->maxRec);
	rMaxRec = MAXIMUM (rMaxRec, maxRec);
      }
      VDRt.Num--;
      if (!sX(WriteVDR(CDF,tOffset,zVar,VDR_RECORD,
		       &VDRt,NULL,VDR_NULL),&pStatus)) {
	AbortAccess (CDF, FALSE, Cur);
	return pStatus;
      }
      tOffset = VDRt.VDRnext;
    }
    /**************************************************************************
    * Write/store the GDR fields that may have changed.
    **************************************************************************/
    if (!zVar) CDF->rMaxRec = rMaxRec;
    if (!sX(WriteGDR(CDF,BOO(zVar,GDR_zVDRHEAD,GDR_rVDRHEAD),&VDRhead,
			 BOO(zVar,GDR_NzVARS,GDR_NrVARS),&nVars,
			 GDR_NULL),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    /**************************************************************************
    * Waste VDR, VXRs, and VVRs.
    **************************************************************************/
    if (!sX(WasteInternalRecord(CDF,vOffset,VDR.RecordSize),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    tOffset = VDR.VXRhead;
    while (tOffset != 0) {
      if (!sX(ReadVXR(CDF,tOffset,VXR_RECORD,&VXRt,VXR_NULL),&pStatus)) {
	AbortAccess (CDF, FALSE, Cur);
	return pStatus;
      }
      if (!sX(WasteInternalRecord(CDF,tOffset,VXRt.RecordSize),&pStatus)) {
	AbortAccess (CDF, FALSE, Cur);
	return pStatus;
      }
      for (entryX = 0; entryX < VXRt.NusedEntries; entryX++) {
	 if (!sX(ReadVVR(CDF,VXRt.VVRoffset[entryX],
			 VVR_RECORDSIZE,&recordSize,VVR_NULL),&pStatus)) {
	   AbortAccess (CDF, FALSE, Cur);
	   return pStatus;
	 }
	 if (!sX(WasteInternalRecord(CDF,VXRt.VVRoffset[entryX],
				     recordSize),&pStatus)) {
	   AbortAccess (CDF, FALSE, Cur);
	   return pStatus;
	 }
      }
      tOffset = VXRt.VXRnext;
    }
    /**************************************************************************
    * Free/adjust variable data structures kept in memory.  Note that the
    * number of z/rVariables has already been decremented.
    **************************************************************************/
    if (zVar) {
      if (CDF->zVars[(int)VDR.Num] != NULL) {
	FreeMemory (CDF->zVars[(int)VDR.Num], NULL);
      }
      for (varN = (int) VDR.Num; varN < nVars; varN++) {
	 CDF->zVars[varN] = CDF->zVars[varN+1];
	 if (CDF->zVars[varN] != NULL) CDF->zVars[varN]->varN = varN;
      }
      CDF->zVars[varN] = NULL;
    }
    else {
      if (CDF->rVars[(int)VDR.Num] != NULL) {
	FreeMemory (CDF->rVars[(int)VDR.Num], NULL);
      }
      for (varN = (int) VDR.Num; varN < nVars; varN++) {
	 CDF->rVars[varN] = CDF->rVars[varN+1];
	 if (CDF->rVars[varN] != NULL) CDF->rVars[varN]->varN = varN;
      }
      CDF->rVars[varN] = NULL;
    }
    /**************************************************************************
    * Reset the current r/zVariable number.
    **************************************************************************/
    if (zOp)
      CDF->CURzVarNum = RESERVED_VARNUM;
    else
      CDF->CURrVarNum = RESERVED_VARNUM;
    /**************************************************************************
    * Delete the associated attribute entries and renumber the entries that
    * are associated with the variables that followed the variable that was
    * deleted.
    **************************************************************************/
    if (!sX(ReadGDR(CDF,GDR_ADRHEAD,&aOffset,GDR_NULL),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    while (aOffset != 0) {
      /************************************************************************
      * Read the scope of the attribute.
      ************************************************************************/
      if (!sX(ReadADR(CDF,aOffset,ADR_SCOPE,&scope,ADR_NULL),&pStatus)) {
	AbortAccess (CDF, FALSE, Cur);
	return pStatus;
      }
      if (VARIABLEscope(scope)) {
	Int32 maxEntry = -1;
	/**********************************************************************
	* Delete associated entry.
	**********************************************************************/
	tStatus = FindEntryByNumber (CDF, aOffset, zVar, (long) VDR.Num,
				     &eOffset);
	switch (tStatus) {
	  case CDF_OK:
	    if (!sX(DeleteEntry(CDF,aOffset,eOffset),&pStatus)) {
	      AbortAccess (CDF, FALSE, Cur);
	      return pStatus;
	    }
	    break;
	  case NO_SUCH_ENTRY:
	    break;
	  default:
	    AbortAccess (CDF, FALSE, Cur);
	    return tStatus;
	}
	/**********************************************************************
	* Renumber entries.  Note that the entry numbers are not necessarily
	* increasing.  (The entries may have been written in any order.)  Also
	* determine the new maximum entry number.
	**********************************************************************/
	if (!sX(ReadADR(CDF,aOffset,
			BOO(zVar,ADR_AzEDRHEAD,ADR_AgrEDRHEAD),
			&eOffset,ADR_NULL),&pStatus)) {
	  AbortAccess (CDF, FALSE, Cur);
	  return pStatus;
	}
	while (eOffset != 0) {
	  if (!sX(ReadAEDR(CDF,eOffset,AEDR_NUM,&entryN,AEDR_NULL),&pStatus)) {
	    AbortAccess (CDF, FALSE, Cur);
	    return pStatus;
	  }
	  if (entryN > VDR.Num) {
	    entryN--;
	    if (!sX(WriteAEDR(CDF,eOffset,AEDR_NUM,
			      &entryN,AEDR_NULL),&pStatus)) {
	      AbortAccess (CDF, FALSE, Cur);
	      return pStatus;
	    }
	  }
	  maxEntry = MAXIMUM (maxEntry, entryN);
	  if (!sX(ReadAEDR(CDF,eOffset,AEDR_AEDRNEXT,
			   &eOffset,AEDR_NULL),&pStatus)) {
	    AbortAccess (CDF, FALSE, Cur);
	    return pStatus;
	  }
	}
	/**********************************************************************
	* Write new maximum entry number to the ADR.
	**********************************************************************/
	if (!sX(WriteADR(CDF,aOffset,
			 BOO(zVar,ADR_MAXzENTRY,ADR_MAXgrENTRY),
			 &maxEntry,ADR_NULL),&pStatus)) {
	  AbortAccess (CDF, FALSE, Cur);
	  return pStatus;
	}
      }
      /************************************************************************
      * Read offset of next ADR.
      ************************************************************************/
      if (!sX(ReadADR(CDF,aOffset,ADR_ADRNEXT,&aOffset,ADR_NULL),&pStatus)) {
	AbortAccess (CDF, FALSE, Cur);
	return pStatus;
      }
    }
    /**************************************************************************
    * Reset the current entry offset (in case it was affected).
    **************************************************************************/
    if (!sX(BOO(zOp,SetCURzEntry(CDF,FALSE,CDF->CURzEntryNum),
		    SetCURgrEntry(CDF,FALSE,CDF->CURgrEntryNum)),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    /**************************************************************************
    * Update the appropriate variable count held in memory for efficiency.
    **************************************************************************/
    if (zVar)
      CDF->NzVars = nVars;
    else
      CDF->NrVars = nVars;
    break;
  }

  /****************************************************************************
  * ATTR_
  ****************************************************************************/
  case ATTR_: {
    struct cdfSTRUCT *CDF;
    Int32 tOffset;
    struct GDRstruct GDR;
    struct ADRstruct ADR, ADRt;
    struct AEDRstruct AEDRt;
    /**************************************************************************
    * Get pointer to current CDF and locate the current attribute.
    **************************************************************************/
    SelectCDF (Cur->cdf, CDF, NO_CDF_SELECTED)
    if (!CURRENTattrSELECTED(CDF)) return NO_ATTR_SELECTED;
    /**************************************************************************
    * Read the GDR and ADR.
    **************************************************************************/
    if (!sX(ReadGDR(CDF,GDR_RECORD,&GDR,GDR_NULL),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    if (!sX(ReadADR(CDF,CDF->CURattrOffset,
		    ADR_RECORD,&ADR,ADR_NULL),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    /**************************************************************************
    * Switch to write access.
    **************************************************************************/
    if (CDF->status != CDF_READ_WRITE) {
      if (!WriteAccess(CDF,Cur,&pStatus)) return pStatus;
    }
    /**************************************************************************
    * Remove the ADR from the list of attributes and decrement the number of
    * attributes.
    **************************************************************************/
    if (GDR.ADRhead == CDF->CURattrOffset)
      GDR.ADRhead = ADR.ADRnext;
    else {
      tOffset = GDR.ADRhead;
      while (tOffset != 0) {
	if (!sX(ReadADR(CDF,tOffset,ADR_RECORD,&ADRt,ADR_NULL),&pStatus)) {
	  AbortAccess (CDF, FALSE, Cur);
	  return pStatus;
	}
	if (ADRt.ADRnext == CDF->CURattrOffset) break;
	tOffset = ADRt.ADRnext;
      }
      if (tOffset == 0) {
	AbortAccess (CDF, FALSE, Cur);
	return CORRUPTED_V2_CDF;
      }
      ADRt.ADRnext = ADR.ADRnext;
      if (!sX(WriteADR(CDF,tOffset,ADR_RECORD,&ADRt,ADR_NULL),&pStatus)) {
	AbortAccess (CDF, FALSE, Cur);
	return pStatus;
      }
    }
    GDR.NumAttr--;
    if (!sX(WriteGDR(CDF,GDR_RECORD,&GDR,GDR_NULL),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    /**************************************************************************
    * Renumber each of the following attributes.
    **************************************************************************/
    tOffset = ADR.ADRnext;
    while (tOffset != 0) {
      if (!sX(ReadADR(CDF,tOffset,ADR_RECORD,&ADRt,ADR_NULL),&pStatus)) {
	AbortAccess (CDF, FALSE, Cur);
	return pStatus;
      }
      ADRt.Num--;
      if (!sX(WriteADR(CDF,tOffset,ADR_RECORD,&ADRt,ADR_NULL),&pStatus)) {
	AbortAccess (CDF, FALSE, Cur);
	return pStatus;
      }
      tOffset = ADRt.ADRnext;
    }
    /**************************************************************************
    * Waste the ADR and each of the AgrEDR and AzEDR's for the attribute.
    **************************************************************************/
    if (!sX(WasteInternalRecord(CDF,CDF->CURattrOffset,
				ADR.RecordSize),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    tOffset = ADR.AgrEDRhead;
    while (tOffset != 0) {
      if (!sX(ReadAEDR(CDF,tOffset,AEDR_RECORD,
		       &AEDRt,NULL,AEDR_NULL),&pStatus)) {
	AbortAccess (CDF, FALSE, Cur);
	return pStatus;
      }
      if (!sX(WasteInternalRecord(CDF,tOffset,AEDRt.RecordSize),&pStatus)) {
	AbortAccess (CDF, FALSE, Cur);
	return pStatus;
      }
      tOffset = AEDRt.AEDRnext;
    }
    tOffset = ADR.AzEDRhead;
    while (tOffset != 0) {
      if (!sX(ReadAEDR(CDF,tOffset,AEDR_RECORD,
		       &AEDRt,NULL,AEDR_NULL),&pStatus)) {
	AbortAccess (CDF, FALSE, Cur);
	return pStatus;
      }
      if (!sX(WasteInternalRecord(CDF,tOffset,AEDRt.RecordSize),&pStatus)) {
	AbortAccess (CDF, FALSE, Cur);
	return pStatus;
      }
      tOffset = AEDRt.AEDRnext;
    }
    /**************************************************************************
    * Reset the current attribute offset and current entry offsets.
    **************************************************************************/
    CDF->CURattrOffset = RESERVED_ATTROFFSET;
    CDF->CURgrEntryOffset = RESERVED_ENTRYOFFSET;
    CDF->CURzEntryOffset = RESERVED_ENTRYOFFSET;
    break;
  }

  /****************************************************************************
  * gENTRY_/zENTRY_/rENTRY_
  ****************************************************************************/
  case gENTRY_:
  case zENTRY_:
  case rENTRY_: {
    int entryType = E3p(Va->item,gENTRY_,rENTRY_,zENTRY_);
    struct cdfSTRUCT *CDF;
    Int32 eOffset;
    /**************************************************************************
    * Get pointer to current CDF, locate the current attribute, and verify
    * that a current entry number has been selected.
    **************************************************************************/
    SelectCDF (Cur->cdf, CDF, NO_CDF_SELECTED)
    if (!CURRENTattrSELECTED(CDF)) return NO_ATTR_SELECTED;
    if (E3(entryType,
	   CDF->CURgrEntryNum,
	   CDF->CURgrEntryNum,
	   CDF->CURzEntryNum) == RESERVED_ENTRYNUM) return NO_ENTRY_SELECTED;
    /**************************************************************************
    * Verify that the operation being performed is legal for the attribute's
    * scope.
    **************************************************************************/
    if (!sX(CheckEntryOp(CDF,entryType,Cur),&pStatus)) return pStatus;
    /**************************************************************************
    * Switch to write access.
    **************************************************************************/
    if (CDF->status != CDF_READ_WRITE) {
      if (!WriteAccess(CDF,Cur,&pStatus)) return pStatus;
    }
    /**************************************************************************
    * Locate the entry to be deleted.
    **************************************************************************/
    eOffset = E3(entryType,CDF->CURgrEntryOffset,
			   CDF->CURgrEntryOffset,
			   CDF->CURzEntryOffset);
    if (eOffset == RESERVED_ENTRYOFFSET) return NO_SUCH_ENTRY;
    /**************************************************************************
    * Delete the entry.
    **************************************************************************/
    if (!sX(DeleteEntry(CDF,CDF->CURattrOffset,eOffset),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    /**************************************************************************
    * Reset the current entry offset (to indicate the entry no longer exists).
    **************************************************************************/
    switch (entryType) {
      case gENTRYt:
      case rENTRYt:
	CDF->CURgrEntryOffset = RESERVED_ENTRYOFFSET;
	break;
      case zENTRYt:
	CDF->CURzEntryOffset = RESERVED_ENTRYOFFSET;
	break;
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
