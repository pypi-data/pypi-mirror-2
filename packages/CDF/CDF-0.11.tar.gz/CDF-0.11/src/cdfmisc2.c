/******************************************************************************
*
*  NSSDC/CDF                     CDF library miscellaneous functions, 1 of 2.
*
*  Version 1.2c, 7-Sep-95, Hughes STX.
*
*  Modification history:
*
*   V1.0  15-Dec-94, J Love     Original version.
*   V1.1   6-Jan-95, J Love	Encode/decode changes.  More cache-residency.
*   V1.1a 20-Jan-95, J Love	IRIX 6.0 (64-bit).
*   V1.1b 15-Mar-95, J Love	Solaris 2.3 IDL i/f.  Fixed `recNum' parameter
*				of `LastAllocatedRecord'.  Gnu C on OSF/1.
*   V1.2  21-Mar-95, J Love	POSIX.
*   V1.2a 18-Apr-95, J Love	More POSIX.
*   V1.2b 13-Jun-95, J Love	Linux.
*   V1.2c  7-Sep-95, J Love	CDFexport-related changes.  Fixed possible
*				memory leak.
*
******************************************************************************/

#include "cdflib.h"

/******************************************************************************
* sX.
*   Determine what should be done with a status code.  For each call to
* `CDFlib', status is returned as follows...
*
*  1. The first ERROR encountered terminates the call and is returned.  This
*     routine will not overwrite an existing error code.
*  2. The last WARNING encountered is returned.  INFOs encountered after a
*     WARNING are ignored.
*  3. In the absence of any WARNINGs, the last INFO is returned.
*  4. In the absence of any WARNINGs or INFOs, CDF_OK is returned.
*
* This routine returns FALSE if the pending status code is an ERROR; otherwise
* it returns TRUE.
*
******************************************************************************/

STATICforIDL Logical sX (cStatus, pStatus)
CDFstatus cStatus;      /* Status code to be checked. */
CDFstatus *pStatus;     /* Pending status code. */
{
  if (cStatus == CDF_OK) return TRUE;           /* Ok, do nothing. */
  if (cStatus < CDF_WARN) {                     /* Error. */
    if (*pStatus > CDF_WARN) *pStatus = cStatus;
    return FALSE;
  }
  if (cStatus > CDF_OK) {                       /* Info. */
    if (CDF_OK <= *pStatus) *pStatus = cStatus;
    return TRUE;
  }
  *pStatus = cStatus;                           /* Warning. */
  return TRUE;
}

/******************************************************************************
* LocateCurrentVar.
******************************************************************************/

STATICforIDL CDFstatus LocateCurrentVar (CDF, zOp, offset, zVar, Var)
struct cdfSTRUCT *CDF;          /* In: Pointer to CDF. */
Logical zOp;                    /* In: TRUE if current zVariable is to be
				   accessed; FALSE if current rVariable.  N/A
				   if zMode is on (since the current zVariable
				   number will always be used). */
Int32 *offset;                  /* Out: Offset of the current variable's VDR.
				   This may be a NULL pointer. */
Logical *zVar;                  /* Out: TRUE if a true zVariable; FALSE if
				   a true rVariable.  This may be a NULL
				   pointer. */
struct varSTRUCT **Var;         /* Out: Pointer to variable.  This will be NULL
				   if the variable has yet to be initialized.
				   This may be a NULL pointer. */
{
  CDFstatus tStatus;
  /****************************************************************************
  * Pass back the offset of the VDR.
  ****************************************************************************/
  if (zModeON(CDF)) {
    if (CDF->CURzVarNum < CDF->NrVars) {
      ASSIGNnotNULL (zVar, FALSE)
      tStatus = FindVarByNumber (CDF, CDF->CURzVarNum, offset, FALSE);
      if (StatusOK(tStatus)) {
	ASSIGNnotNULL (Var, CDF->rVars[(int)CDF->CURzVarNum])
      }
    }
    else {
      ASSIGNnotNULL(zVar, TRUE)
      tStatus = FindVarByNumber (CDF, CDF->CURzVarNum - CDF->NrVars, offset,
				 TRUE);
      if (StatusOK(tStatus)) {
	ASSIGNnotNULL (Var, CDF->zVars[(int)(CDF->CURzVarNum - CDF->NrVars)])
      }
    }
  }
  else {
    ASSIGNnotNULL (zVar, zOp)
    tStatus = FindVarByNumber (CDF,BOO(zOp,CDF->CURzVarNum,
					   CDF->CURrVarNum),offset,zOp);
    if (StatusOK(tStatus)) {
      ASSIGNnotNULL (Var, BOO(zOp,CDF->zVars[(int)CDF->CURzVarNum],
				  CDF->rVars[(int)CDF->CURrVarNum]))
    }
  }
  return tStatus;
}

/******************************************************************************
* InitCurrentVar.
******************************************************************************/

STATICforIDL CDFstatus InitCurrentVar (CDF, zOp, Var)
struct cdfSTRUCT *CDF;          /* In: Pointer to CDF. */
Logical zOp;                    /* In: TRUE if current zVariable is to be
				   accessed; FALSE if current rVariable.  N/A
				   if zMode is on (since the current zVariable
				   number will always be used [even when a real
				   rVariable is being accessed]). */
struct varSTRUCT **Var;         /* Out: Pointer to variable. */
{
  CDFstatus tStatus;
  /****************************************************************************
  * Pass back the pointer to its variable structure.  The variable will
  * be initialized for access if necessary.
  ****************************************************************************/
  if (zModeON(CDF))
    if (CDF->CURzVarNum < CDF->NrVars)
      tStatus = InitVar (CDF, CDF->CURzVarNum, FALSE, Var);
    else
      tStatus = InitVar (CDF, CDF->CURzVarNum - CDF->NrVars, TRUE, Var);
  else
    tStatus = InitVar (CDF,BOO(zOp,CDF->CURzVarNum,CDF->CURrVarNum),zOp,Var);
  return tStatus;
}

/******************************************************************************
* InitVar.
******************************************************************************/

STATICforIDL CDFstatus InitVar (CDF, varN, zVar, Var)
struct cdfSTRUCT *CDF;          /* In: Pointer to CDF. */
long varN;                      /* In: Real variable number (ignoring the
				   zMode). */
Logical zVar;                   /* In: TRUE if a real zVariable (ignoring
				   the zMode). */
struct varSTRUCT **Var;         /* Out: Pointer to variable. */
{
  CDFstatus pStatus = CDF_OK;
  int dimN;
  /****************************************************************************
  * Check if the variable has already been initialized.  If not, allocate and
  * initialize its variable structure.
  ****************************************************************************/
  if (BOO(zVar,CDF->zVars[(int)varN],CDF->rVars[(int)varN]) == NULL) {
    /**************************************************************************
    * Allocate a variable structure.
    **************************************************************************/
    struct varSTRUCT *tVar = (struct varSTRUCT *)
			     AllocateMemory (sizeof(struct varSTRUCT), NULL);
    if (tVar == NULL) return BAD_MALLOC;
    /**************************************************************************
    * Determine offset of the VDR in the `.cdf' file.
    **************************************************************************/
    if (!sX(FindVarByNumber(CDF,varN,&(tVar->VDRoffset),zVar),&pStatus)) return
								       pStatus;
    /**************************************************************************
    * Initialize miscellaneous fields of the variable structure.
    **************************************************************************/
    tVar->zVar = zVar;
    tVar->varN = varN;
    if (CDF->singleFile) {
      tVar->fp = CDF->fp;
      tVar->status = NO_VAR_FILE;
      tVar->nCacheBuffers = 0;
    }
    else {
      tVar->fp = NULL;
      tVar->status = VAR_CLOSED;
      tVar->nCacheBuffers = MAXcacheVAR;
    }
    tVar->accessed_at = CDF->pseudo_clock++;
    if (CDF->singleFile) {
      tVar->sFile.firstRecInVVR = -1;
      tVar->sFile.lastRecInVVR = -1;
      tVar->sFile.offsetOfVVR = -1;
    }
    /**************************************************************************
    * Read fields to be held in memory for efficiency.
    **************************************************************************/
    if (!sX(ReadVDR(CDF,tVar->VDRoffset,tVar->zVar,
		    VDR_MAXREC,&(tVar->maxRec),
		    VDR_NULL),&pStatus)) return pStatus;
    if (CDF->singleFile) {
      if (!sX(LastAllocatedRecord(CDF,tVar->VDRoffset,tVar->zVar,
				  &(tVar->sFile.maxAllocated)),&pStatus)) {
	return pStatus;
      }
      tVar->sFile.maxWritten = tVar->sFile.maxAllocated;
    }
    /**************************************************************************
    * Calculate variable parameters (depending on zMode).
    **************************************************************************/
    if (!sX(CalcVarParms(CDF,tVar),&pStatus)) return pStatus;
    /**************************************************************************
    * Initialize current positioning.
    **************************************************************************/
    tVar->seqValueOffset = 0;
    tVar->zRD.recNumber = 0;
    tVar->zRD.recCount = 1;
    tVar->zRD.recInterval = 1;
    for (dimN = 0; dimN < tVar->numDims; dimN++) {
       tVar->zRD.dimIndices[dimN] = 0;
       tVar->zRD.dimCounts[dimN] = tVar->dimSizes[dimN];
       tVar->zRD.dimIntervals[dimN] = 1;
    }
    /**************************************************************************
    * Store pointer to variable structure.
    **************************************************************************/
    if (zVar)
      CDF->zVars[(int)varN] = tVar;
    else
      CDF->rVars[(int)varN] = tVar;
  }
  /****************************************************************************
  * Pass back pointer to variable.
  ****************************************************************************/
  ASSIGNnotNULL (Var, BOO(zVar,CDF->zVars[(int)varN],CDF->rVars[(int)varN]))
  return pStatus;
}

/******************************************************************************
* VarIdentity.
*    Returns information about the real identity of a variable.
******************************************************************************/

STATICforIDL CDFstatus VarIdentity (CDF, varN, zOp, varNt, zVar, Var)
struct cdfSTRUCT *CDF;          /* In: Pointer to CDF. */
long varN;                      /* In: Variable number - zModed. */
Logical zOp;                    /* In: TRUE if zVariable; FALSE if rVariable.
				       This is also zModed. */
long *varNt;                    /* Out: Real variable number. */
Logical *zVar;                  /* Out: Real variable type: TRUE if a
					zVariable; FALSE if an rVariable. */
struct varSTRUCT **Var;         /* Out: Pointer to variable. */
{
  if (zModeON(CDF))
    if (0 <= varN && varN < CDF->NrVars) {
      ASSIGNnotNULL (varNt, varN)
      ASSIGNnotNULL (zVar, FALSE)
      ASSIGNnotNULL (Var, CDF->rVars[(int)varN])
    }
    else
      if (varN < CDF->NrVars + CDF->NzVars) {
	ASSIGNnotNULL (varNt, varN - CDF->NrVars)
	ASSIGNnotNULL (zVar, TRUE)
	ASSIGNnotNULL (Var, CDF->zVars[(int)varN])
      }
      else
	return NO_SUCH_VAR;
  else
    if (0 <= varN && varN < BOO(zOp,CDF->NzVars,CDF->NrVars)) {
      ASSIGNnotNULL (varNt, varN)
      ASSIGNnotNULL (zVar, zOp)
      ASSIGNnotNULL (Var, BOO(zOp,CDF->zVars[(int)varN],
				  CDF->rVars[(int)varN]))
    }
    else
      return NO_SUCH_VAR;
  return CDF_OK;
}

/******************************************************************************
* ReadWriteVar.
*   Open a variable for read/write access (if this is a multi-file CDF and
* the variable file is closed).  It is assumed that the variable has been
* initialized for access and that the variable is closed (and in a multi-file
* CDF).
******************************************************************************/

STATICforIDL CDFstatus ReadWriteVar (CDF, Var)
struct cdfSTRUCT *CDF;
struct varSTRUCT *Var;
{
  CDFstatus pStatus = CDF_OK;
  char a_mode[MAX_aMODE_LEN+1];
  char pathname[DU_MAX_PATH_LEN+1];
  /****************************************************************************
  * Try to open the variable file.
  ****************************************************************************/
  BuildFilePath (BOO(Var->zVar,Zt,Vt), CDF->cdfname, CDF->no_append,
		 CDF->upper_case_ext, CDF->version_numbers, Var->varN,
		 VERSION_2, pathname);
  if (CDF->status == CDF_READ_WRITE)
    strcpyX (a_mode, READ_PLUS_a_mode, MAX_aMODE_LEN);
  else
    strcpyX (a_mode, READ_ONLY_a_mode, MAX_aMODE_LEN);
  Var->fp = V_open (pathname, a_mode);
  /****************************************************************************
  * If the open was successful, set the proper cache size...
  ****************************************************************************/
  if (Var->fp != NULL) {
    if (!CACHEv(Var->fp,Var->nCacheBuffers)) {
      V_close (Var->fp, NULL);
      return BAD_CACHE_SIZE;
    }
    Var->status = VAR_OPENED;
    return pStatus;
  }
  /****************************************************************************
  * The open failed, close a variable file and try again...
  ****************************************************************************/
  if (!sX(CloseLRUvar(CDF),&pStatus)) return pStatus;
  Var->fp = V_open (pathname, a_mode);
  if (Var->fp != NULL) {
    if (!CACHEv(Var->fp,Var->nCacheBuffers)) {
      V_close (Var->fp, NULL);
      return BAD_CACHE_SIZE;
    }
    Var->status = VAR_OPENED;
    return pStatus;
  }
  /****************************************************************************
  * The second attempt failed also, return an error.
  ****************************************************************************/
  return VAR_OPEN_ERROR;
}

/******************************************************************************
* LastAllocatedRecord.
******************************************************************************/

STATICforIDL CDFstatus LastAllocatedRecord (CDF, VDRoffset, zVar, recNum)
struct cdfSTRUCT *CDF;  /* In: Pointer to CDF. */
Int32 VDRoffset;        /* In: Offset of VDR. */
Logical zVar;           /* In: TRUE if a real zVariable; FALSE if rVariable. */
Int32 *recNum;          /* Out: Last record allocated. */
{
  CDFstatus pStatus = CDF_OK;
  Int32 VXRoffset, nUsedEntries, lastRecs[NUM_VXR_ENTRIES];
  if (!sX(ReadVDR(CDF,VDRoffset,zVar,VDR_VXRTAIL,
		  &VXRoffset,VDR_NULL),&pStatus)) return pStatus;
  if (VXRoffset == 0)
    *recNum = -1;
  else {
    if (!sX(ReadVXR(CDF,VXRoffset,VXR_NUSEDENTRIES,&nUsedEntries,
				  VXR_LASTREC,lastRecs,
				  VXR_NULL),&pStatus)) return pStatus;
    *recNum = lastRecs[(int)nUsedEntries-1];
  }
  return pStatus;
}

/******************************************************************************
* IndicesValueOffset.
******************************************************************************/

STATICforIDL long IndicesValueOffset (numDims, dimIndices, dimVarys,
				      nPhyDimValues)
long numDims;
long *dimIndices;
long *dimVarys;
long *nPhyDimValues;
{
  long offset = 0;
  int dimN;
  for (dimN = 0; dimN < numDims; dimN++)
     if (dimVarys[dimN]) offset += (dimIndices[dimN] * nPhyDimValues[dimN]);
  return offset;
}

/******************************************************************************
* ValueOffsetIndices.
******************************************************************************/

STATICforIDL void ValueOffsetIndices (offset, rowMajor, numDims, dimVarys,
				      nPhyDimValues, indices)
long offset;
Logical rowMajor;
long numDims;
long *dimVarys;
long *nPhyDimValues;
long *indices;
{
  int dimN, i;
  for (i = 0, dimN = (rowMajor ? 0 : (int)(numDims-1));
       i < numDims; 
       i++, (rowMajor ? dimN++ : dimN--))
     if (dimVarys[dimN]) {
       indices[dimN] = offset / nPhyDimValues[dimN];
       offset = offset % nPhyDimValues[dimN];
     }
     else
       indices[dimN] = 0;
  return;
}

/******************************************************************************
* SeqValueByteOffset.
*    Calculates the byte offset of the current sequential value for a variable.
******************************************************************************/

STATICforIDL Int32 SeqValueByteOffset (CDF, Var)
struct cdfSTRUCT *CDF;          /* In: Pointer to CDF. */
struct varSTRUCT *Var;          /* In: Pointer to variable. */
{
  long phyRecNum = Var->seqValueOffset / Var->NphyRecValues;
  long valueOffsetInRecord = Var->seqValueOffset % Var->NphyRecValues;
  return (Int32) (RecordByteOffset(CDF,Var,phyRecNum) +
		  (valueOffsetInRecord * Var->NvalueBytes));
}

/******************************************************************************
* RecordByteOffset.
******************************************************************************/

STATICforIDL Int32 RecordByteOffset (CDF, Var, phyRecN)
struct cdfSTRUCT *CDF;
struct varSTRUCT *Var;
long phyRecN;
{
  CDFstatus pStatus = CDF_OK;
  if (CDF->singleFile) {
    /**************************************************************************
    * A single-file CDF.  If a different VVR is being accessed, search through
    * the VXRs until the record number is found.
    **************************************************************************/
    if (Var->sFile.firstRecInVVR <= phyRecN &&
	phyRecN <= Var->sFile.lastRecInVVR) {
      return (Int32) (Var->sFile.offsetOfVVR +
		      VVR_BASE_SIZE +
		      (Var->NphyRecBytes *
		       (phyRecN - Var->sFile.firstRecInVVR)));
    }
    else {
      Int32 offset; int entryN;
      if (!sX(ReadVDR(CDF,Var->VDRoffset,Var->zVar,
		      VDR_VXRHEAD,&offset,VDR_NULL),&pStatus)) return (-1);
      while (offset != 0) {
	struct VXRstruct VXR;
	if (!sX(ReadVXR(CDF,offset,VXR_RECORD,&VXR,VXR_NULL),&pStatus))
	  return (-1);
	if (phyRecN <= VXR.LastRec[(int)(VXR.NusedEntries-1)]) {
	  for (entryN = 0; entryN < VXR.NusedEntries; entryN++) {
	     if (phyRecN <= VXR.LastRec[entryN]) {
	       Var->sFile.firstRecInVVR = VXR.FirstRec[entryN];
	       Var->sFile.lastRecInVVR = VXR.LastRec[entryN];
	       Var->sFile.offsetOfVVR = VXR.VVRoffset[entryN];
	       return (Int32) (Var->sFile.offsetOfVVR + VVR_BASE_SIZE +
			       (Var->NphyRecBytes *
				(phyRecN - VXR.FirstRec[entryN])));
	     }
	  }
	}
	offset = VXR.VXRnext;
      }
      return ((Int32) (-1));
    }
  }
  else {
    /**************************************************************************
    * A multi-file CDF, calculate offset (no indexing).
    **************************************************************************/
    return (Int32) (phyRecN * Var->NphyRecBytes);
  }
}

/******************************************************************************
* ValueByteOffset.
******************************************************************************/

STATICforIDL Int32 ValueByteOffset (CDF, Var, phyRecN, dimIndices)
struct cdfSTRUCT *CDF;
struct varSTRUCT *Var;
long phyRecN;
long dimIndices[];
{
  Int32 recByteOffset, valueOffset;
  int dimN;
  /****************************************************************************
  * Calculate byte offset for record.
  ****************************************************************************/
  recByteOffset = RecordByteOffset (CDF, Var, phyRecN);
  /****************************************************************************
  * Calculate value offset into record.
  ****************************************************************************/
  valueOffset = 0;
  for (dimN = 0; dimN < Var->numDims; dimN++)
     if (Var->dimVarys[dimN]) {
       valueOffset += (Int32) (dimIndices[dimN] * Var->nPhyDimValues[dimN]);
     }
  /****************************************************************************
  * Return byte offset for value.
  ****************************************************************************/
  return (Int32) (recByteOffset + (valueOffset * Var->NvalueBytes));
}

/******************************************************************************
* ContiguousRecords.
******************************************************************************/

STATICforIDL CDFstatus ContiguousRecords (CDF, Var, firstRec, lastRec, contig)
struct cdfSTRUCT *CDF;          /* In: Pointer to CDF. */
struct varSTRUCT *Var;          /* In: Pointer to variable. */
long firstRec;                  /* In: First record in range. */
long lastRec;                   /* In: Last record in range. */
Logical *contig;                /* Out: TRUE if contiguous. */
{
  CDFstatus pStatus = CDF_OK;
  if (CDF->singleFile) {
    /**************************************************************************
    * Single-file: search VXRs.  But first check if the range of records is
    * within the most recently accessed VVR.
    **************************************************************************/
    Int32 offset; int eN;
    if (Var->sFile.firstRecInVVR <= firstRec &&
	lastRec <= Var->sFile.lastRecInVVR) {
      *contig = TRUE;
      return pStatus;
    }
    if (!sX(ReadVDR(CDF,Var->VDRoffset,Var->zVar,
		    VDR_VXRHEAD,&offset,VDR_NULL),&pStatus)) return pStatus;
    while (offset != 0) {
      Int32 nUsedEntries, firstRecs[NUM_VXR_ENTRIES],lastRecs[NUM_VXR_ENTRIES];
      if (!sX(ReadVXR(CDF,offset,VXR_NUSEDENTRIES,&nUsedEntries,
				 VXR_FIRSTREC,firstRecs,
				 VXR_LASTREC,lastRecs,
				 VXR_NULL),&pStatus)) return pStatus;
      for (eN = 0; eN < nUsedEntries; eN++) {
	 if (firstRecs[eN] <= firstRec && firstRec <= lastRecs[eN]) {
	   *contig = (firstRecs[eN] <= lastRec && lastRec <= lastRecs[eN]);
	   return pStatus;
	 }
      }
      if (!sX(ReadVXR(CDF,offset,VXR_VXRNEXT,&offset,VXR_NULL),&pStatus))
	return pStatus;
    }
    *contig = FALSE;
    return pStatus;
  }
  else {
    /**************************************************************************
    * Multi-file: contiguous if all records exist.
    **************************************************************************/
    *contig = (lastRec <= Var->maxRec);
    return pStatus;
  }
}

/******************************************************************************
* ConfigureNEWzMode.
******************************************************************************/

STATICforIDL CDFstatus ConfigureNEWzMode (CDF)
struct cdfSTRUCT *CDF;
{
  CDFstatus pStatus = CDF_OK;
  if (!sX(UpdateInitializedVars(CDF),&pStatus)) return pStatus;
  InitCURobjectsStates (CDF);
  return pStatus;
}

/******************************************************************************
* InitCURobjectsStates.
*     Note that initializing is done regardless of the current zMode.
******************************************************************************/

STATICforIDL void InitCURobjectsStates (CDF)
struct cdfSTRUCT *CDF;
{
  struct varSTRUCT *Var;
  int dimN, varNum;
  /****************************************************************************
  * Initialize current attributes/entries/variables.
  ****************************************************************************/
  CDF->CURattrOffset = RESERVED_ATTROFFSET;
  CDF->CURgrEntryNum = RESERVED_ENTRYNUM;
  CDF->CURgrEntryOffset = RESERVED_ENTRYOFFSET;
  CDF->CURzEntryNum = RESERVED_ENTRYNUM;
  CDF->CURzEntryOffset = RESERVED_ENTRYOFFSET;
  CDF->CURrVarNum = RESERVED_VARNUM;
  CDF->CURzVarNum = RESERVED_VARNUM;
  /****************************************************************************
  * Initialize current positioning for EACH rVariable.
  ****************************************************************************/
  for (varNum = 0; varNum < CDF->NrVars; varNum++) {
     Var = CDF->rVars[varNum];
     if (Var != NULL) {
       Var->seqValueOffset = 0;
       Var->zRD.recNumber = 0;
       Var->zRD.recCount = 1;
       Var->zRD.recInterval = 1;
       for (dimN = 0; dimN < Var->numDims; dimN++) {
	  Var->zRD.dimIndices[dimN] = 0;
	  Var->zRD.dimCounts[dimN] = Var->dimSizes[dimN];
	  Var->zRD.dimIntervals[dimN] = 1;
       }
     }
  }
  /****************************************************************************
  * Initialize current positioning for EACH zVariable.
  ****************************************************************************/
  for (varNum = 0; varNum < CDF->NzVars; varNum++) {
     Var = CDF->zVars[varNum];
     if (Var != NULL) {
       Var->seqValueOffset = 0;
       Var->zRD.recNumber = 0;
       Var->zRD.recCount = 1;
       Var->zRD.recInterval = 1;
       for (dimN = 0; dimN < Var->numDims; dimN++) {
	  Var->zRD.dimIndices[dimN] = 0;
	  Var->zRD.dimCounts[dimN] = Var->dimSizes[dimN];
	  Var->zRD.dimIntervals[dimN] = 1;
       }
     }
  }
  /****************************************************************************
  * Initialize current positioning for ALL rVariables.
  ****************************************************************************/
  CDF->rRD.recNumber = 0;
  CDF->rRD.recCount = 1;
  CDF->rRD.recInterval = 1;
  for (dimN = 0; dimN < CDF->rNumDims; dimN++) {
     CDF->rRD.dimIndices[dimN] = 0;
     CDF->rRD.dimCounts[dimN] = CDF->rDimSizes[dimN];
     CDF->rRD.dimIntervals[dimN] = 1;
  }
  return;
}

/******************************************************************************
* FindAttrByName.
******************************************************************************/

STATICforIDL CDFstatus FindAttrByName (CDF, searchName, offset)
struct cdfSTRUCT *CDF;          /* In: Pointer to CDF. */
char *searchName;               /* In: Attribute name to find. */
Int32 *offset;                  /* Out: Offset of ADR that was found. */
{
  Int32 numAttrs, tOffset;
  char attrName[CDF_ATTR_NAME_LEN+1];
  CDFstatus pStatus = CDF_OK;
  int attrN;
  /****************************************************************************
  * Read number of attributes and the offset of the first ADR from the GDR.
  ****************************************************************************/
  if (!sX(ReadGDR(CDF,GDR_NUMATTR,&numAttrs,
		      GDR_ADRHEAD,&tOffset,
		      GDR_NULL),&pStatus)) return pStatus;
  /****************************************************************************
  * Read from ADRs until a matching attribute name is found.
  *   Note that if this is a V2.0 CDF, the last ADR will not have an
  * offset of zero for the next ADR.  For that reason, we will loop
  * through the number of attributes read from the GDR (and then stop).
  ****************************************************************************/
  for (attrN = 0; attrN < numAttrs; attrN++) {
     if (!sX(ReadADR(CDF,tOffset,ADR_NAME,attrName,ADR_NULL),&pStatus))
       return pStatus;
     if (!strcmpITB(attrName,searchName)) {
       ASSIGNnotNULL (offset, tOffset)
       return CDF_OK;
     }
     if (!sX(ReadADR(CDF,tOffset,ADR_ADRNEXT,&tOffset,ADR_NULL),&pStatus))
       return pStatus;
  }
  /****************************************************************************
  * Attribute name not found, return error.
  ****************************************************************************/
  return NO_SUCH_ATTR;
}

/******************************************************************************
* FindAttrByNumber.
******************************************************************************/

STATICforIDL CDFstatus FindAttrByNumber (CDF, searchNum, offset)
struct cdfSTRUCT *CDF;          /* In: Pointer to the CDF. */
long searchNum;                 /* In: The attribute number to be found. */
Int32 *offset;                  /* Out: The offset of the located ADR. */
{
  Int32 numAttrs, tOffset, attrNum;
  CDFstatus pStatus = CDF_OK;
  int attrN;
  /****************************************************************************
  * Validate.
  ****************************************************************************/
  if (searchNum < 0) return BAD_ATTR_NUM;
  /****************************************************************************
  * First check if the next attribute is the one being searched for.  For this
  * to be the case, an attribute must currently be selected, the next attribute
  * must exist, and the next attribute's number must be the attribute number
  * being searched for.  But don't try this if a V2.0 CDF because of the bad
  * terminating offset of the ADR linked list in those CDFs.
  ****************************************************************************/
  if (!CDF->badTerminatingOffsets) {
    if (CDF->CURattrOffset != RESERVED_ATTROFFSET) {
      Int32 nextOffset;
      if (!sX(ReadADR(CDF,CDF->CURattrOffset,
		      ADR_ADRNEXT,&nextOffset,
		      ADR_NULL),&pStatus)) return pStatus;
      if (nextOffset != 0) {
	Int32 nextNum;
	if (!sX(ReadADR(CDF,nextOffset,
			ADR_NUM,&nextNum,
			ADR_NULL),&pStatus)) return pStatus;
	if (nextNum == searchNum) {
	  *offset = nextOffset;
	  return pStatus;
	}
      }
    }
  }
  /****************************************************************************
  * The next attribute isn't the one being searched for.  First read the
  * number of attributes and the offset of the first ADR from the GDR.
  ****************************************************************************/
  if (!sX(ReadGDR(CDF,GDR_NUMATTR,&numAttrs,
		      GDR_ADRHEAD,&tOffset,
		      GDR_NULL),&pStatus)) return pStatus;
  if (numAttrs <= searchNum) return NO_SUCH_ATTR;
  /****************************************************************************
  * Read from ADRs until a matching attribute number is found.
  *   Note that if this is a V2.0 CDF, the last ADR will not have an
  * offset of zero for the next ADR.  For that reason, we will loop
  * through the number of attributes read from the GDR (and then stop).
  ****************************************************************************/
  for (attrN = 0; attrN < numAttrs; attrN++) {
     if (!sX(ReadADR(CDF,tOffset,ADR_NUM,&attrNum,ADR_NULL),&pStatus))
       return pStatus;
     if (attrNum == searchNum) {
       ASSIGNnotNULL (offset, tOffset)
       return CDF_OK;
     }
     if (!sX(ReadADR(CDF,tOffset,ADR_ADRNEXT,&tOffset,ADR_NULL),&pStatus))
       return pStatus;
  }
  /****************************************************************************
  * Attribute number not found, internal error or corrupted CDF.
  ****************************************************************************/
  return CORRUPTED_V2_CDF;
}

/******************************************************************************
* FindEntryByNumber.
******************************************************************************/

STATICforIDL CDFstatus FindEntryByNumber (CDF, ADRoffset, zEntry, entryN,
					  offset)
struct cdfSTRUCT *CDF;          /* In: Pointer to the CDF. */
Int32 ADRoffset;                /* In: Offset of attribute's ADR. */
Logical zEntry;			/* In: TRUE if AzEDR list to be searched.
				       FALSE if AgrEDR list to be searched. */
long entryN;                    /* In: The entry number being searched for. */
Int32 *offset;                  /* Out: The offset of the located AEDR. */
{
  Int32 numEntries, tOffset, entryNum;
  CDFstatus pStatus = CDF_OK;
  int entryX;
  /****************************************************************************
  * Read number of entries and the offset of the first AEDR from the ADR.
  ****************************************************************************/
  if (!sX(ReadADR(CDF,ADRoffset,
		  BOO(zEntry,ADR_NzENTRIES,ADR_NgrENTRIES),&numEntries,
		  BOO(zEntry,ADR_AzEDRHEAD,ADR_AgrEDRHEAD),&tOffset,
		  ADR_NULL),&pStatus)) return pStatus;
  /****************************************************************************
  * Read from AEDRs until a matching entry number is found.
  *   Note that if this is a V2.0 CDF, the last AEDR will not have an
  * offset of zero for the next AEDR.  For that reason, we will loop
  * through the number of entries read from the ADR (and then stop).
  ****************************************************************************/
  for (entryX = 0; entryX < numEntries; entryX++) {
     if (!sX(ReadAEDR(CDF,tOffset,AEDR_NUM,
		      &entryNum,AEDR_NULL),&pStatus)) return pStatus;
     if (entryNum == entryN) {
       ASSIGNnotNULL (offset, tOffset)
       return CDF_OK;
     }
     if (!sX(ReadAEDR(CDF,tOffset,AEDR_AEDRNEXT,
		      &tOffset,AEDR_NULL),&pStatus)) return pStatus;
  }
  /****************************************************************************
  * Entry number not found.
  ****************************************************************************/
  return NO_SUCH_ENTRY;
}

/******************************************************************************
* FindLastAttr.
******************************************************************************/

STATICforIDL CDFstatus FindLastAttr (CDF, lastOffset)
struct cdfSTRUCT *CDF;          /* In: Pointer to the CDF. */
Int32 *lastOffset;              /* Out: Offset of last attribute's ADR. */
{
  CDFstatus pStatus = CDF_OK;
  Int32 nAttrs, offset;
  int attrN;
  /****************************************************************************
  * Read number of attributes and the offset of the first ADR.  If there are
  * no attributes, return an offset of zero.
  ****************************************************************************/
  if (!sX(ReadGDR(CDF,GDR_NUMATTR,&nAttrs,GDR_NULL),&pStatus)) return pStatus;
  if (nAttrs == 0) {
    *lastOffset = 0;
    return pStatus;
  }
  /****************************************************************************
  * There is at least one attribute.
  *   Note that if this is a V2.0 CDF, the last ADR will not have an offset of
  * zero for the next ADR.  For that reason, we will loop through the number
  * of attributes read from the GDR (and then stop).
  ****************************************************************************/
  if (!sX(ReadGDR(CDF,GDR_ADRHEAD,&offset,GDR_NULL),&pStatus)) return pStatus;
  for (attrN = 0; attrN < nAttrs - 1; attrN++) {
     if (!sX(ReadADR(CDF,offset,ADR_ADRNEXT,&offset,ADR_NULL),&pStatus))
       return pStatus;
  }
  *lastOffset = offset;
  return pStatus;
}

/******************************************************************************
* FindLastEntry.
******************************************************************************/

STATICforIDL CDFstatus FindLastEntry (CDF, ADRoffset, zEntry, lastOffset)
struct cdfSTRUCT *CDF;          /* In: Pointer to the CDF. */
Int32 ADRoffset;                /* In: Offset of attribute's ADR. */
Logical zEntry;                 /* In: TRUE if (real) zEntry is being searched
				   for; FALSE if gEntry/rEntry. */
Int32 *lastOffset;              /* Out: The offset of the last AEDR. */
{
  CDFstatus pStatus = CDF_OK;
  Int32 offset, nEntries;
  int entryX;
  /****************************************************************************
  * Read offset of first AEDR and determine if there are any entries (of the
  * specified type).  If there are none, pass back an offset of zero.
  ****************************************************************************/
  if (!sX(ReadADR(CDF,ADRoffset,
		  BOO(zEntry,ADR_AzEDRHEAD,ADR_AgrEDRHEAD),
		  &offset,ADR_NULL),&pStatus)) return pStatus;
  if (offset == 0) {
    *lastOffset = 0;
    return pStatus;
  }
  /****************************************************************************
  * There is at least one entry.  Read the actual number of entries and then
  * scan through to the last one.
  *   Note that if this is a V2.0 CDF, the last AEDR will not have an
  * offset of zero for the next AEDR.  For that reason, we will loop
  * through the number of entries (minus one) read from the ADR (and then
  * stop).
  ****************************************************************************/
  if (!sX(ReadADR(CDF,ADRoffset,
		  BOO(zEntry,ADR_NzENTRIES,ADR_NgrENTRIES),
		  &nEntries,ADR_NULL),&pStatus)) return pStatus;
  for (entryX = 0; entryX < nEntries - 1; entryX++) {
     if (!sX(ReadAEDR(CDF,offset,AEDR_AEDRNEXT,&offset,AEDR_NULL),&pStatus))
       return pStatus;
  }
  *lastOffset = offset;
  return pStatus;
}

/******************************************************************************
* FindPrevEntry.
******************************************************************************/

STATICforIDL CDFstatus FindPrevEntry (CDF, ADRoffset, searchOffset, zEntry,
				      prevOffset)
struct cdfSTRUCT *CDF;          /* Pointer to the CDF. */
Int32 ADRoffset;                /* Offset of attribute's ADR. */
Int32 searchOffset;             /* The entry offset being searched for. */
Logical zEntry;                 /* TRUE if (real) zEntry is being searched for;
				   FALSE if gEntry/rEntry. */
Int32 *prevOffset;              /* The offset of the previous AEDR. */
{
  CDFstatus pStatus = CDF_OK;
  Int32 offset, nEntries, nextOffset;
  int entryX;
  /****************************************************************************
  * Read the offset of the first AEDR.  If that offset is the same as the
  * search offset, return an offset of zero.
  ****************************************************************************/
  if (!sX(ReadADR(CDF,ADRoffset,
		  BOO(zEntry,ADR_AzEDRHEAD,ADR_AgrEDRHEAD),
		  &offset,ADR_NULL),&pStatus)) return pStatus;
  if (offset == searchOffset) {
    *prevOffset = 0;
    return pStatus;
  }
  /****************************************************************************
  * The first AEDR is not at the search offset.  Read the actual number of
  * entries and then scan through them looking for the AEDR offset being
  * searched for.  If the search offset is not found, then either the CDF is
  * corrupted or an internal logic error has occurred.
  *   Note that if this is a V2.0 CDF, the last AEDR will not have an
  * offset of zero for the next AEDR.  For that reason, we will loop
  * through the number of entries read from the ADR (and then stop).
  ****************************************************************************/
  if (!sX(ReadADR(CDF,ADRoffset,
		  BOO(zEntry,ADR_NzENTRIES,ADR_NgrENTRIES),
		  &nEntries,ADR_NULL),&pStatus)) return pStatus;
  for (entryX = 0; entryX < nEntries; entryX++) {
     if (!sX(ReadAEDR(CDF,offset,AEDR_AEDRNEXT,
		      &nextOffset,AEDR_NULL),&pStatus)) return pStatus;
     if (nextOffset == searchOffset) {
       *prevOffset = offset;
       return pStatus;
     }
     offset = nextOffset;
  }
  return CORRUPTED_V2_CDF;
}

/******************************************************************************
* FindVarByName.
*    Both the rVariable and zVariable lists are searched (since variable names
* are unique in a CDF).
******************************************************************************/

STATICforIDL CDFstatus FindVarByName (CDF, searchName, offset, zVar, Var)
struct cdfSTRUCT *CDF;  /* In: Pointer to the CDF. */
char *searchName;       /* In: The variable name being searched for. */
Int32 *offset;          /* Out: Offset of the zVDR/rVDR. */
Logical *zVar;          /* Out: TRUE if a zVariable. */
struct varSTRUCT **Var; /* Out: Pointer to variable structure. */
{
  int varN;
  char varName[CDF_VAR_NAME_LEN+1];  
  CDFstatus pStatus = CDF_OK;
  Int32 tOffset;
  /****************************************************************************
  * Read from rVDRs until a matching variable name is found.
  *   Note that if this is a V2.0 CDF, the last rVDR will not have an
  * offset of zero for the next rVDR.  For that reason, we will loop
  * through the number of rVariables (and then stop).
  ****************************************************************************/
  if (!sX(ReadGDR(CDF,GDR_rVDRHEAD,&tOffset,GDR_NULL),&pStatus)) return
								 pStatus;
  for (varN = 0; varN < CDF->NrVars; varN++) {
     if (!sX(ReadVDR(CDF,tOffset,FALSE,VDR_NAME,
		     varName,VDR_NULL),&pStatus)) return pStatus;
     if (!strcmpITB(varName,searchName)) {
       ASSIGNnotNULL (offset, tOffset)
       ASSIGNnotNULL (zVar, FALSE)
       ASSIGNnotNULL (Var, CDF->rVars[varN])
       return CDF_OK;
     }
     if (!sX(ReadVDR(CDF,tOffset,FALSE,VDR_VDRNEXT,
		     &tOffset,VDR_NULL),&pStatus)) return pStatus;
  }
  /****************************************************************************
  * Read from zVDRs until a matching variable name is found.
  ****************************************************************************/
  if (!sX(ReadGDR(CDF,GDR_zVDRHEAD,&tOffset,GDR_NULL),&pStatus)) return
								 pStatus;
  for (varN = 0; varN < CDF->NzVars; varN++) {
     if (!sX(ReadVDR(CDF,tOffset,TRUE,VDR_NAME,
		     varName,VDR_NULL),&pStatus)) return pStatus;
     if (!strcmpITB(varName,searchName)) {
       ASSIGNnotNULL (offset, tOffset)
       ASSIGNnotNULL (zVar, TRUE)
       ASSIGNnotNULL (Var, CDF->zVars[varN])
       return CDF_OK;
     }
     if (!sX(ReadVDR(CDF,tOffset,TRUE,
		     VDR_VDRNEXT,&tOffset,VDR_NULL),&pStatus)) return pStatus;
  }
  /****************************************************************************
  * Variable name not found, return error.
  ****************************************************************************/
  return NO_SUCH_VAR;
}

/******************************************************************************
* FindVarByNumber.
******************************************************************************/

STATICforIDL CDFstatus FindVarByNumber (CDF, searchNum, offset, zVar)
struct cdfSTRUCT *CDF;  /* In: Pointer to CDF. */
long searchNum;         /* In: Variable number to be searched for. */
Int32 *offset;          /* Out: offset of the VDR. */
Logical zVar;           /* In: TRUE if a (real) zVariable number should be
			   found. */
{
  CDFstatus pStatus = CDF_OK;
  long nVars = BOO(zVar,CDF->NzVars,CDF->NrVars);
  Int32 tOffset, varNum;
  int varN;
  /****************************************************************************
  * Read offset of first VDR.
  ****************************************************************************/
  if (searchNum < 0) return BAD_VAR_NUM;
  if (!sX(ReadGDR(CDF,BOO(zVar,GDR_zVDRHEAD,GDR_rVDRHEAD),
		  &tOffset,GDR_NULL),&pStatus)) return pStatus;
  if (nVars <= searchNum) return NO_SUCH_VAR;
  /****************************************************************************
  * Read from VDRs until a matching variable number is found.
  *   Note that if this is a V2.0 CDF, the last VDR will not have an
  * offset of zero for the next VDR.  For that reason, we will loop
  * through the number of variables (and then stop).
  ****************************************************************************/
  for (varN = 0; varN < nVars; varN++) {
     if (!sX(ReadVDR(CDF,tOffset,zVar,VDR_NUM,&varNum,VDR_NULL),&pStatus))
       return pStatus;
     if (varNum == searchNum) {
       ASSIGNnotNULL (offset, tOffset)
       return CDF_OK;
     }
     if (!sX(ReadVDR(CDF,tOffset,zVar,
		     VDR_VDRNEXT,&tOffset,VDR_NULL),&pStatus)) return pStatus;
  }
  /****************************************************************************
  * Variable number not found, return error.
  ****************************************************************************/
  return CORRUPTED_V2_CDF;
}

/******************************************************************************
* VerifyNoRecordsWritten.
*    Verifies that no records have been written.  Both the rVariable and
* zVariable lists are searched.
******************************************************************************/

STATICforIDL CDFstatus VerifyNoRecordsWritten (CDF, no)
struct cdfSTRUCT *CDF;          /* In: Pointer to the CDF. */
Logical *no;                    /* Out: If TRUE, no records written. */
{
  CDFstatus pStatus = CDF_OK;
  Int32 tOffset, maxRec;
  int varN;
  /****************************************************************************
  * Read from rVDRs until a maximum record greater than -1 is found.
  *   Note that if this is a V2.0 CDF, the last rVDR will not have an
  * offset of zero for the next rVDR.  For that reason, we will loop
  * through the number of rVariables (and then stop).
  ****************************************************************************/
  if (!sX(ReadGDR(CDF,GDR_rVDRHEAD,&tOffset,GDR_NULL),&pStatus)) return
								 pStatus;
  for (varN = 0; varN < CDF->NrVars; varN++) {
     if (CDF->rVars[varN] == NULL) {
       if (!sX(ReadVDR(CDF,tOffset,FALSE,VDR_MAXREC,
		       &maxRec,VDR_NULL),&pStatus)) return pStatus;
     }
     else
       maxRec = CDF->rVars[varN]->maxRec;
     if (maxRec > -1) {
       *no = FALSE;
       return pStatus;
     }
     if (!sX(ReadVDR(CDF,tOffset,FALSE,VDR_VDRNEXT,
		     &tOffset,VDR_NULL),&pStatus)) return pStatus;
  }
  /****************************************************************************
  * Read from zVDRs until a maximum record greater than -1 is found.
  ****************************************************************************/
  if (!sX(ReadGDR(CDF,GDR_zVDRHEAD,&tOffset,GDR_NULL),&pStatus)) return
								 pStatus;
  for (varN = 0; varN < CDF->NzVars; varN++) {
     if (CDF->zVars[varN] == NULL) {
       if (!sX(ReadVDR(CDF,tOffset,TRUE,VDR_MAXREC,&maxRec,VDR_NULL),&pStatus))
	 return pStatus;
     }
     else
       maxRec = CDF->zVars[varN]->maxRec;
     if (maxRec > -1) {
       *no = FALSE;
       return pStatus;
     }
     if (!sX(ReadVDR(CDF,tOffset,TRUE,VDR_VDRNEXT,&tOffset,VDR_NULL),&pStatus))
       return pStatus;
  }
  /****************************************************************************
  * No records written.
  ****************************************************************************/
  *no = TRUE;
  return pStatus;
}

/******************************************************************************
* VerifyNoPadsSpecified.
*    Verifies that no pad values have been specified.  Both the rVariable
* and zVariable lists are searched.
******************************************************************************/

STATICforIDL CDFstatus VerifyNoPadsSpecified (CDF, no)
struct cdfSTRUCT *CDF;          /* In: Pointer to the CDF. */
Logical *no;                    /* Out: If TRUE, no pad values written. */
{
  CDFstatus pStatus = CDF_OK;
  Int32 tOffset, flags32;
  int varN;
  /****************************************************************************
  * Read from rVDRs until a pad value is found.
  *   Note that if this is a V2.0 CDF, the last rVDR will not have an
  * offset of zero for the next rVDR.  For that reason, we will loop
  * through the number of rVariables (and then stop).
  ****************************************************************************/
  if (!sX(ReadGDR(CDF,GDR_rVDRHEAD,&tOffset,GDR_NULL),&pStatus)) return
								 pStatus;
  for (varN = 0; varN < CDF->NrVars; varN++) {
     if (!sX(ReadVDR(CDF,tOffset,FALSE,VDR_FLAGS,
		     &flags32,VDR_NULL),&pStatus)) return pStatus;
     if (PADvalueBITset(flags32)) {
       *no = FALSE;
       return pStatus;
     }
     if (!sX(ReadVDR(CDF,tOffset,FALSE,VDR_VDRNEXT,
		     &tOffset,VDR_NULL),&pStatus)) return pStatus;
  }
  /****************************************************************************
  * Read from zVDRs until a pad value is found.
  ****************************************************************************/
  if (!sX(ReadGDR(CDF,GDR_zVDRHEAD,&tOffset,GDR_NULL),&pStatus)) return
								 pStatus;
  for (varN = 0; varN < CDF->NzVars; varN++) {
     if (!sX(ReadVDR(CDF,tOffset,TRUE,VDR_FLAGS,
		     &flags32,VDR_NULL),&pStatus)) return pStatus;
     if (PADvalueBITset(flags32)) {
       *no = FALSE;
       return pStatus;
     }
     if (!sX(ReadVDR(CDF,tOffset,TRUE,VDR_VDRNEXT,&tOffset,VDR_NULL),&pStatus))
       return pStatus;
  }
  /****************************************************************************
  * No pad values specified.
  ****************************************************************************/
  *no = TRUE;
  return pStatus;
}

/******************************************************************************
* VerifyNoEntriesWritten.
******************************************************************************/

STATICforIDL CDFstatus VerifyNoEntriesWritten (CDF, no)
struct cdfSTRUCT *CDF;
Logical *no;
{
  CDFstatus pStatus = CDF_OK;
  Int32 numAttrs, tOffset, nEntries;
  int attrN;
  /****************************************************************************
  * Read number of attributes and the offset of the first ADR from the GDR.
  ****************************************************************************/
  if (!sX(ReadGDR(CDF,GDR_NUMATTR,&numAttrs,
		      GDR_ADRHEAD,&tOffset,
		      GDR_NULL),&pStatus)) return pStatus;
  /****************************************************************************
  * Read from ADRs until an entry is found.
  *   Note that if this is a V2.0 CDF, the last ADR will not have an
  * offset of zero for the next ADR.  For that reason, we will loop
  * through the number of attributes read from the GDR (and then stop).
  ****************************************************************************/
  for (attrN = 0; attrN < numAttrs; attrN++) {
     if (!sX(ReadADR(CDF,tOffset,ADR_NgrENTRIES,&nEntries,ADR_NULL),&pStatus))
       return pStatus;
     if (nEntries > 0) {
       *no = FALSE;
       return pStatus;
     }
     if (!sX(ReadADR(CDF,tOffset,ADR_NzENTRIES,&nEntries,ADR_NULL),&pStatus))
       return pStatus;
     if (nEntries > 0) {
       *no = FALSE;
       return pStatus;
     }
     if (!sX(ReadADR(CDF,tOffset,ADR_ADRNEXT,&tOffset,ADR_NULL),&pStatus))
       return pStatus;
  }
  /****************************************************************************
  * No entries detected.
  ****************************************************************************/
  *no = TRUE;
  return pStatus;
}

/******************************************************************************
* DefaultPadValue.
*    `memmove' is used rather than an assignment statement (for the data
* types greater in size than one byte) because there is no guarantee that the
* address which receives the pad value is aligned properly.  If it isn't, a
* bus error could occur on some computers.
******************************************************************************/

STATICforIDL void DefaultPadValue (dataType, numElems, padValue)
long dataType;
long numElems;
void *padValue;
{
  size_t nBytes = CDFelemSize (dataType);
  Byte *ptr = padValue;
  double padE;                  /* The "largest" data type element. */
  int i;
  switch (dataType) {
    case CDF_BYTE: *((Schar *) &padE) = DEFAULT_BYTE_PADVALUE; break;
    case CDF_INT1: *((Schar *) &padE) = DEFAULT_INT1_PADVALUE; break;
    case CDF_UINT1: *((Uchar *) &padE) = DEFAULT_UINT1_PADVALUE; break;
    case CDF_INT2: *((Int16 *) &padE) = DEFAULT_INT2_PADVALUE; break;
    case CDF_UINT2: *((uInt16 *) &padE) = DEFAULT_UINT2_PADVALUE; break;
    case CDF_INT4: *((Int32 *) &padE) = DEFAULT_INT4_PADVALUE; break;
    case CDF_UINT4: *((uInt32 *) &padE) = DEFAULT_UINT4_PADVALUE; break;
    case CDF_REAL4: *((float *) &padE) = DEFAULT_REAL4_PADVALUE; break;
    case CDF_FLOAT: *((float *) &padE) = DEFAULT_FLOAT_PADVALUE; break;
    case CDF_REAL8: *((double *) &padE) = DEFAULT_REAL8_PADVALUE; break;
    case CDF_DOUBLE: *((double *) &padE) = DEFAULT_DOUBLE_PADVALUE; break;
    case CDF_EPOCH: *((double *) &padE) = DEFAULT_EPOCH_PADVALUE; break;
    case CDF_CHAR: *((Schar *) &padE) = DEFAULT_CHAR_PADVALUE; break;
    case CDF_UCHAR: *((Uchar *) &padE) = DEFAULT_UCHAR_PADVALUE; break;
  }
  for (i = 0; i < numElems; i++, ptr += nBytes) memmove (ptr, &padE, nBytes);
  return;
}

/******************************************************************************
* DefaultPadBuffer.
******************************************************************************/

STATICforIDL CDFstatus DefaultPadBuffer (CDF, Var, nValues, buffer)
struct cdfSTRUCT *CDF;
struct varSTRUCT *Var;
long nValues;
void *buffer;
{
  CDFstatus pStatus = CDF_OK;
  Byte *tBuffer = buffer; long i; Int32 dataType, numElems;
  if (!sX(ReadVDR(CDF,Var->VDRoffset,Var->zVar,VDR_DATATYPE,&dataType,
					       VDR_NUMELEMS,&numElems,
					       VDR_NULL),&pStatus)) return
								    pStatus;
  for (i = 0; i < nValues; i++, tBuffer += (int) Var->NvalueBytes) {
     DefaultPadValue ((long) dataType, (long) numElems, tBuffer);
  }
  return pStatus;
}

/******************************************************************************
* PadBuffer.
******************************************************************************/

STATICforIDL CDFstatus PadBuffer (CDF, Var, nValues, buffer)
struct cdfSTRUCT *CDF;          /* Pointer to CDF. */
struct varSTRUCT *Var;          /* Pointer to variable. */
long nValues;                   /* Number of values in buffer. */
void *buffer;                   /* Buffer to pad. */
{
  CDFstatus pStatus = CDF_OK;
  Int32 flags, dataType, numElems;
  /****************************************************************************
  * Read the flags, data type, and number of elements fields of the VDR.
  ****************************************************************************/
  if (!sX(ReadVDR(CDF,Var->VDRoffset,Var->zVar,VDR_FLAGS,&flags,
					       VDR_DATATYPE,&dataType,
					       VDR_NUMELEMS,&numElems,
					       VDR_NULL),&pStatus)) return
								    pStatus;
  /****************************************************************************
  * If a pad value has been specified for the variable, read the pad value
  * from the VDR and duplicate for the desired number of values.  Otherwise,
  * copy the desired number of default pad values into the buffer.  Then
  * convert the padded buffer into the desired decoding.
  ****************************************************************************/
  if (PADvalueBITset(flags)) {
    Byte *tBuffer = buffer; long valueN;
    if (!sX(ReadVDR(CDF,Var->VDRoffset,Var->zVar,
		    VDR_PADVALUE,tBuffer,VDR_NULL),&pStatus)) return pStatus;
    for (valueN = 1; valueN < nValues; valueN++) {
       memmove (tBuffer + ((size_t) Var->NvalueBytes), tBuffer,
		(size_t) Var->NvalueBytes);
       tBuffer += (size_t) Var->NvalueBytes;
    }
    if (!sX(ConvertBuffer(CDF->encoding,CDF->decoding,
			  CDF->negToPosFp0mode,
			  (long) dataType,(long) (nValues * numElems),
			  buffer,buffer),&pStatus)) return pStatus;
  }
  else {
    if (!sX(DefaultPadBuffer(CDF,Var,nValues,buffer),&pStatus)) return pStatus;
    if (!sX(ConvertBuffer(HostEncoding(),CDF->decoding,
			  CDF->negToPosFp0mode,
			  (long) dataType,(long) (nValues * numElems),
			  buffer,buffer),&pStatus)) return pStatus;
  }
  return pStatus;
}

/******************************************************************************
* HostEncoding.
*    Returns encoding type of host machine.
******************************************************************************/

STATICforIDL long HostEncoding ()
{
#if defined(sun)
  return SUN_ENCODING;
#endif
#if defined(vax)
  return VAX_ENCODING;
#endif
#if defined(MIPSEL)
  return DECSTATION_ENCODING;
#endif
#if defined(MIPSEB)
  return SGi_ENCODING;
#endif
#if defined(IBMPC)
  return IBMPC_ENCODING;
#endif
#if defined(IBMRS)
  return IBMRS_ENCODING;
#endif
#if defined(HP)
  return HP_ENCODING;
#endif
#if defined(NeXT)
  return NeXT_ENCODING;
#endif
#if defined(alphaosf)
  return ALPHAOSF1_ENCODING;
#endif
#if defined(alphavmsD) || defined(posixSHELLalphaD)
  return ALPHAVMSd_ENCODING;
#endif
#if defined(alphavmsG) || defined(posixSHELLalphaG)
  return ALPHAVMSg_ENCODING;
#endif
#if defined(mac)
  return MAC_ENCODING;
#endif
}

/******************************************************************************
* HostDecoding.  Returns decoding type of host machine.
******************************************************************************/

STATICforIDL long HostDecoding ()
{
#if defined(sun)
  return SUN_DECODING;
#endif
#if defined(vax)
  return VAX_DECODING;
#endif
#if defined(MIPSEL)
  return DECSTATION_DECODING;
#endif
#if defined(MIPSEB)
  return SGi_DECODING;
#endif
#if defined(IBMPC)
  return IBMPC_DECODING;
#endif
#if defined(IBMRS)
  return IBMRS_DECODING;
#endif
#if defined(HP)
  return HP_DECODING;
#endif
#if defined(NeXT)
  return NeXT_DECODING;
#endif
#if defined(alphaosf)
  return ALPHAOSF1_DECODING;
#endif
#if defined(alphavmsD) || defined(posixSHELLalphaD)
  return ALPHAVMSd_DECODING;
#endif
#if defined(alphavmsG) || defined(posixSHELLalphaG)
  return ALPHAVMSg_DECODING;
#endif
#if defined(mac)
  return MAC_DECODING;
#endif
}

/******************************************************************************
* IntegerOrder.
*    Returns integer order based on encoding (decoding).
******************************************************************************/

STATICforIDL int IntegerOrder (ed)
long ed;                /* Encoding/decoding. */
{
  switch (ed) {
    case NETWORK_ENCODING:
    case SUN_ENCODING:
    case SGi_ENCODING:
    case IBMRS_ENCODING:
    case HP_ENCODING:
    case NeXT_ENCODING:
    case MAC_ENCODING:
      return BIGendianORDER;
    case DECSTATION_ENCODING:
    case ALPHAOSF1_ENCODING:
    case ALPHAVMSd_ENCODING:
    case ALPHAVMSg_ENCODING:
    case IBMPC_ENCODING:
    case VAX_ENCODING:
      return LITTLEendianORDER;
    default:
      return 0;                 /* Internal error. */
  }
}

/******************************************************************************
* FpType.
*    Returns floating-point type based on encoding (decoding).
******************************************************************************/

STATICforIDL int FpType (ed)
long ed;                /* Encoding/decoding. */
{
  switch (ed) {
    case NETWORK_ENCODING:
    case SUN_ENCODING:
    case SGi_ENCODING:
    case IBMRS_ENCODING:
    case HP_ENCODING:
    case NeXT_ENCODING:
    case MAC_ENCODING:
      return FP_1;
    case DECSTATION_ENCODING:
    case ALPHAOSF1_ENCODING:
    case IBMPC_ENCODING:
      return FP_2;
    case VAX_ENCODING:
    case ALPHAVMSd_ENCODING:
      return FP_3;
    case ALPHAVMSg_ENCODING:
      return FP_4;
    default:
      return 0;
  }
}

/******************************************************************************
* CDFelemSize.
******************************************************************************/

STATICforIDL int CDFelemSize (dataType)
long dataType;
{
switch (dataType) {
  case CDF_BYTE:   return 1;
  case CDF_INT1:   return 1;
  case CDF_INT2:   return 2;
  case CDF_INT4:   return 4;
  case CDF_UINT1:  return 1;
  case CDF_UINT2:  return 2;
  case CDF_UINT4:  return 4;
  case CDF_REAL4:  return 4;
  case CDF_REAL8:  return 8;
  case CDF_FLOAT:  return 4;
  case CDF_DOUBLE: return 8;
  case CDF_EPOCH:  return 8;
  case CDF_CHAR:   return 1;
  case CDF_UCHAR:  return 1;
}
return 0;
}

/******************************************************************************
* EquivDataTypes.
******************************************************************************/

STATICforIDL Logical EquivDataTypes (dataType1, dataType2)
long dataType1;
long dataType2;
{
switch (dataType1) {
  case CDF_BYTE:
  case CDF_INT1:
  case CDF_UINT1:
  case CDF_CHAR:
  case CDF_UCHAR:
    switch (dataType2) {
      case CDF_BYTE:
      case CDF_INT1:
      case CDF_UINT1:
      case CDF_CHAR:
      case CDF_UCHAR:
	return TRUE;
      default:
	return FALSE;
    }
  case CDF_INT2:
  case CDF_UINT2:
    switch (dataType2) {
      case CDF_INT2:
      case CDF_UINT2:
	return TRUE;
      default:
	return FALSE;
    }
  case CDF_INT4:
  case CDF_UINT4:
    switch (dataType2) {
      case CDF_INT4:
      case CDF_UINT4:
	return TRUE;
      default:
	return FALSE;
    }
  case CDF_REAL4:
  case CDF_FLOAT:
    switch (dataType2) {
      case CDF_REAL4:
      case CDF_FLOAT:
	return TRUE;
      default:
	return FALSE;
    }
  case CDF_REAL8:
  case CDF_DOUBLE:
  case CDF_EPOCH:
    switch (dataType2) {
      case CDF_REAL8:
      case CDF_DOUBLE:
      case CDF_EPOCH:
	return TRUE;
      default:
	return FALSE;
    }
}

return FALSE;   /* Internal error, what should we do? */
}

/******************************************************************************
* strcmpITB.  Do a STRing CoMPare Ignoring any Trailing Blanks.
******************************************************************************/

STATICforIDL int strcmpITB (string1, string2)
char *string1;
char *string2;
{
size_t len1 = strlen(string1);
size_t len2 = strlen(string2);
while (len1 > 0 && string1[len1-1] == ' ') len1--;
while (len2 > 0 && string2[len2-1] == ' ') len2--;
if (len1 == len2)
  return strncmp (string1, string2, len1);
else
  return strcmp (string1, string2);
}


/******************************************************************************
* FreeCDFid.
*    Free a CDF's dynamically allocated memory.
******************************************************************************/

STATICforIDL void FreeCDFid (CDF)
struct cdfSTRUCT *CDF;
{
  int varNum;
  /****************************************************************************
  * Free rVariable structures.
  ****************************************************************************/
  if (CDF->rVars != NULL) {
    for (varNum = 0; varNum < CDF->NrVars; varNum++) {
       if (CDF->rVars[varNum] != NULL) FreeMemory (CDF->rVars[varNum], NULL);
    }
    FreeMemory (CDF->rVars, NULL);
  }
  /****************************************************************************
  * Free zVariable structures.
  ****************************************************************************/
  if (CDF->zVars != NULL) {
    for (varNum = 0; varNum < CDF->NzVars; varNum++) {
       if (CDF->zVars[varNum] != NULL) FreeMemory (CDF->zVars[varNum], NULL);
    }
    FreeMemory (CDF->zVars, NULL);
  }
  /****************************************************************************
  * Free CDF structure.  The CDF structure's magic number is "killed" just in
  * case the application tries to use the CDFid again.
  ****************************************************************************/
  CDF->struct_magic_number = KILLid_MAGIC_NUMBER;
  FreeMemory (CDF, NULL);
  return;
}

/******************************************************************************
* CloseLRUvar.
*    Close a variable/zVariable file to free a file pointer. Note that if a
* CDF is SINGLE file, each variable's `status' will be NO_VAR_FILE (so that
* variable will not be considered for closing).
******************************************************************************/

STATICforIDL CDFstatus CloseLRUvar (CDF)
struct cdfSTRUCT *CDF;
{
  struct varSTRUCT *Var;
  struct varSTRUCT *oldestVar = NULL;
  long oldest_access = CDF->pseudo_clock;
  int varNum;
  /****************************************************************************
  * Scan through rVariables looking for oldest access.
  ****************************************************************************/
  for (varNum = 0; varNum < CDF->NrVars; varNum++) {
    Var = CDF->rVars[varNum];
    if (Var != NULL)
      if (Var->status == VAR_OPENED)
	if (Var->accessed_at < oldest_access) {
	  oldest_access = Var->accessed_at;
	  oldestVar = Var;
	}
  }
  /****************************************************************************
  * Scan through zVariables looking for oldest access.
  ****************************************************************************/
  for (varNum = 0; varNum < CDF->NzVars; varNum++) {
    Var = CDF->zVars[varNum];
    if (Var != NULL)
      if (Var->status == VAR_OPENED)
	if (Var->accessed_at < oldest_access) {
	  oldest_access = Var->accessed_at;
	  oldestVar = Var;
	}
  }
  /****************************************************************************
  * If a variable was found, close the associated file.
  ****************************************************************************/
  if (oldestVar != NULL) {
    if (!CLOSEv(oldestVar->fp,NULL)) return VAR_CLOSE_ERROR;
    oldestVar->status = VAR_CLOSED;
  }
  return CDF_OK;
}

/******************************************************************************
* CalcVarParms.
*   Calculate parameters needed to access a variable.
******************************************************************************/

STATICforIDL CDFstatus CalcVarParms (CDF, Var)
struct cdfSTRUCT *CDF;
struct varSTRUCT *Var;
{
  int dimN, dimNx;
  Int32 flags, explicitExtendRecs, dataType, numElems;
  CDFstatus pStatus = CDF_OK;
  /****************************************************************************
  * Read necessary fields from the VDR.
  ****************************************************************************/
  if (!sX(ReadVDR(CDF,Var->VDRoffset,Var->zVar,
		  VDR_FLAGS,&flags,
		  VDR_DATATYPE,&dataType,
		  VDR_NUMELEMS,&numElems,
		  VDR_NEXTENDRECS,&explicitExtendRecs,
		  VDR_NULL),&pStatus)) return pStatus;
  /****************************************************************************
  * Calculate the dimensionality and variances of the variable based on the
  * current zMode.
  ****************************************************************************/
  if (!sX(CalcNumDims(CDF,Var->VDRoffset,
		      Var->zVar,&(Var->numDims)),&pStatus)) return pStatus;
  if (!sX(CalcDimSizes(CDF,Var->VDRoffset,
		       Var->zVar,Var->dimSizes),&pStatus)) return pStatus;
  if (!sX(CalcDimVarys(CDF,Var->VDRoffset,
		       Var->zVar,Var->dimVarys),&pStatus)) return pStatus;
  Var->recVary = BOO(RECvaryBITset(flags),VARY,NOVARY);
  /****************************************************************************
  * Calculate the number of values for each physical dimension.
  ****************************************************************************/
  if (!CDF->rowMajor) {
     for (dimN = 0; dimN < Var->numDims; dimN++) {
	Var->nPhyDimValues[dimN] = 1;
	for (dimNx = 0; dimNx < dimN; dimNx++)
	   if (Var->dimVarys[dimNx])
	     Var->nPhyDimValues[dimN] *= Var->dimSizes[dimNx];
     }
  }
  else {
     for (dimN = 0; dimN < Var->numDims; dimN++) {
	Var->nPhyDimValues[dimN] = 1;
	for (dimNx = dimN + 1; dimNx < Var->numDims; dimNx++)
	   if (Var->dimVarys[dimNx])
	     Var->nPhyDimValues[dimN] *= Var->dimSizes[dimNx];
     }
  }
  /****************************************************************************
  * Calculate the element and value sizes.
  ****************************************************************************/
  Var->NvalueElems = numElems;
  Var->NelemBytes = CDFelemSize ((long) dataType);
  Var->NvalueBytes = Var->NvalueElems * Var->NelemBytes;
  /****************************************************************************
  * Calculate the number of physical and virtual values per record.
  ****************************************************************************/
  Var->NphyRecValues = 1;
  Var->NvirtRecValues = 1;
  for (dimN = 0; dimN < Var->numDims; dimN++) {
     Var->NvirtRecValues *= Var->dimSizes[dimN];
     if (Var->dimVarys[dimN]) Var->NphyRecValues *= Var->dimSizes[dimN];
  }
  /****************************************************************************
  * Calculate the number of elements and the size (in bytes) of physical and
  * conceptual records.
  ****************************************************************************/
  Var->NphyRecElems = Var->NphyRecValues * Var->NvalueElems;
  Var->NvirtRecElems = Var->NvirtRecValues * Var->NvalueElems;
  Var->NphyRecBytes = Var->NphyRecValues * Var->NvalueBytes;
  Var->NvirtRecBytes = Var->NvirtRecValues * Var->NvalueBytes;
  /****************************************************************************
  * Calculate the number of extend records if a single-file CDF.
  ****************************************************************************/
  if (CDF->singleFile) {
    if (Var->recVary)
      if (explicitExtendRecs == 0) {
	long minRecs = ((MIN_nEXTEND_BYTES_single-1)/Var->NphyRecBytes) + 1;
	Var->sFile.nExtendRecs = MAXIMUM (minRecs, MIN_nEXTEND_RECS_single);
      }
      else
	Var->sFile.nExtendRecs = explicitExtendRecs;
    else
      Var->sFile.nExtendRecs = 1;
  }
  /****************************************************************************
  * Determine the encoding and decoding functions to be used.
  ****************************************************************************/
  if (!sX(ConversionFunction((long)dataType,(long)HostEncoding(),
			     (long)CDF->encoding,(long)CDF->negToPosFp0mode,
			     &(Var->EncodeFunction)),&pStatus)) return pStatus;
  if (!sX(ConversionFunction((long)dataType,(long)CDF->encoding,
			     (long)CDF->decoding,(long)CDF->negToPosFp0mode,
			     &(Var->DecodeFunction)),&pStatus)) return pStatus;
  return pStatus;
}

/******************************************************************************
* PadRecords.
*     For single-file CDFs all records have already been allocated.
******************************************************************************/

STATICforIDL CDFstatus PadRecords (CDF, Var, firstRec, lastRec)
struct cdfSTRUCT *CDF;
struct varSTRUCT *Var;
long firstRec;
long lastRec;
{
  CDFstatus pStatus = CDF_OK;
  /****************************************************************************
  * First check if no records need to be padded because the last record
  * is before the first record.  This could happen because of logic used
  * elsewhere...
  ****************************************************************************/
  if (lastRec < firstRec) return pStatus;
  /****************************************************************************
  * Pad the records.
  ****************************************************************************/
  if (CDF->singleFile) {
    /**************************************************************************
    * Single-file: check for contiguous records.
    **************************************************************************/
    Logical contig;
    if (!sX(ContiguousRecords(CDF,Var,firstRec,
			      lastRec,&contig),&pStatus)) return pStatus;
    if (contig) {
      Int32 offset = RecordByteOffset (CDF, Var, firstRec);
      long nRecords = lastRec - firstRec + 1;
      if (!sX(PadContiguousRecords(CDF,Var,offset,nRecords),&pStatus))
	return pStatus;
    }
    else {
      long recN;
      for (recN = firstRec; recN <= lastRec; recN++) {
	 Int32 offset = RecordByteOffset (CDF, Var, recN);
	 if (!sX(PadContiguousRecords(CDF,Var,offset,1L),&pStatus)) return
								    pStatus;
      }
    }
    Var->sFile.maxWritten = MAXIMUM (Var->sFile.maxWritten, lastRec);
  }
  else {
    /**************************************************************************
    * Multi-file: records are always contiguous.
    **************************************************************************/
    Int32 offset = RecordByteOffset (CDF, Var, firstRec);
    long nRecords = lastRec - firstRec + 1;
    if (!sX(PadContiguousRecords(CDF,Var,offset,nRecords),&pStatus)) return
								     pStatus;
  }
  return pStatus;
}

/******************************************************************************
* PadContiguousRecords.  
******************************************************************************/

STATICforIDL CDFstatus PadContiguousRecords (CDF, Var, offset, nRecs)
struct cdfSTRUCT *CDF;
struct varSTRUCT *Var;
Int32 offset;                   /* File offset at which to begin writting. */
long nRecs;                     /* Number of records to write at the offset. */
{
  Byte *padBuffer, *ptr;
  long nBytes, nValues, recN, valueN;
  void *padValue;
  Int32 flags, dataType, numElems;
  CDFstatus pStatus = CDF_OK;
  /****************************************************************************
  * Determine pad value (and encode it if necessary).
  ****************************************************************************/
  padValue = (void *) AllocateMemory ((size_t) Var->NvalueBytes, NULL);
  if (padValue == NULL) return BAD_MALLOC;
  if (!sX(ReadVDR(CDF,Var->VDRoffset,Var->zVar,
		  VDR_FLAGS,&flags,
		  VDR_DATATYPE,&dataType,
		  VDR_NUMELEMS,&numElems,
		  VDR_NULL),&pStatus)) {
    FreeMemory (padValue, NULL);
    return pStatus;
  }
  if (PADvalueBITset(flags)) {
    if (!sX(ReadVDR(CDF,Var->VDRoffset,Var->zVar,
		    VDR_PADVALUE,padValue,VDR_NULL),&pStatus)) {
      FreeMemory (padValue, NULL);
      return pStatus;
    }
  }
  else {
    DefaultPadValue ((long) dataType, (long) numElems, padValue);
    if (!sX(ConvertBuffer(HostEncoding(),CDF->encoding,CDF->negToPosFp0mode,
			  ((long) dataType),((long) numElems),padValue,
			  padValue),&pStatus)) {
      FreeMemory (padValue, NULL);
      return pStatus;
    }
  }
  /****************************************************************************
  * Seek to desired offset.
  ****************************************************************************/
  if (!SEEKv(Var->fp,(long)offset,vSEEK_SET)) {
    FreeMemory (padValue, NULL);
    return VAR_WRITE_ERROR;
  }
  /****************************************************************************
  * Try to write all of the records at once...
  ****************************************************************************/
  nValues = nRecs * Var->NphyRecValues;
  nBytes = nValues * Var->NvalueBytes;
#if LIMITof64K
  if (nBytes < (long) 65536) {
#endif
    padBuffer = (Byte *) AllocateMemory ((size_t) nBytes, NULL);
    if (padBuffer != NULL) {
      for (valueN = 0, ptr = (Byte *) padBuffer;
	   valueN < nValues; valueN++, ptr += (size_t) Var->NvalueBytes) {
	 memmove (ptr, padValue, (size_t) Var->NvalueBytes);
      }
      if (!WRITEv(padBuffer,(size_t)nBytes,1,Var->fp)) {
	FreeMemory (padValue, NULL);
	FreeMemory (padBuffer, NULL);
	return VAR_WRITE_ERROR;
      }
      FreeMemory (padValue, NULL);
      FreeMemory (padBuffer, NULL);
      return pStatus;
    }
#if LIMITof64K
  }
#endif
  /****************************************************************************
  * Not enough memory for that, try writing one record at a time...
  ****************************************************************************/
#if LIMITof64K
  if (Var->NphyRecBytes < (long) 65536) {
#endif
    padBuffer = (Byte *) AllocateMemory ((size_t) Var->NphyRecBytes, NULL);
    if (padBuffer != NULL) {
      for (valueN = 0, ptr = (Byte *) padBuffer;
	   valueN < Var->NphyRecValues;
	   valueN++, ptr += (size_t) Var->NvalueBytes) {
	 memmove (ptr, padValue, (size_t) Var->NvalueBytes);
      }
      for (recN = 0; recN < nRecs; recN++) {
	 if (!WRITEv(padBuffer,(size_t)Var->NphyRecBytes,1,Var->fp)) {
	   FreeMemory (padValue, NULL);
	   FreeMemory (padBuffer, NULL);
	   return VAR_WRITE_ERROR;
	 }
      }
      FreeMemory (padValue, NULL);
      FreeMemory (padBuffer, NULL);
      return pStatus;
    }
#if LIMITof64K
  }
#endif
  /****************************************************************************
  * Not enough memory for that either, write one value at a time...
  ****************************************************************************/
  for (recN = 0; recN < nRecs; recN++) {
     for (valueN = 0; valueN < Var->NphyRecValues; valueN++) {
	if (!WRITEv(padValue,(size_t)Var->NvalueBytes,1,Var->fp)) {
	  FreeMemory (padValue, NULL);
	  return VAR_WRITE_ERROR;
	}
     }  
  }
  FreeMemory (padValue, NULL);
  return pStatus;
}

/******************************************************************************
* NumberOfCacheBuffers.
******************************************************************************/

STATICforIDL int NumberOfCacheBuffers (CDF)
struct cdfSTRUCT *CDF;
{
  int nBuffers;
  if (CDF->explicitCache)
    nBuffers = CDF->nCacheBuffers;
  else
    if (CDF->singleFile) {
      nBuffers = PERvarSINGLE * (int) (CDF->NrVars + CDF->NzVars);
      nBuffers = MINIMUM (nBuffers, MAXcacheSINGLE);
      nBuffers = MAXIMUM (nBuffers, MINcacheSINGLE);
    }
    else
      nBuffers = NUMcacheMULTI;
  return nBuffers;
}

/******************************************************************************
* ROWtoCOL.
******************************************************************************/

STATICforIDL void ROWtoCOL (iBuffer, oBuffer, numDims, dimSizes, nValueBytes)
void *iBuffer;
void *oBuffer;
long numDims;
long dimSizes[];
long nValueBytes;
{
  switch (numDims) {
    case 0:
    case 1: {
      long nValues; int dimN;
      for (dimN = 0, nValues = 1; dimN < numDims; dimN++) {
	 nValues *= dimSizes[dimN];
      }
      memmove (oBuffer, iBuffer, (size_t) (nValues * nValueBytes));
      break;
    }
    default: {
      long products[CDF_MAX_DIMS];        /* Products, what each dimension is
					     `worth'. */
      long iBoffset;                      /* Input buffer, byte offset. */
      long oBoffset;                      /* Output buffer, byte offset. */
      long oVoffset;                      /* Output buffer, value offset. */
      int dimN;                           /* Dimension number. */
      for (dimN = 1, products[0] = 1; dimN < numDims; dimN++) {
         products[dimN] = products[dimN-1] * dimSizes[dimN-1];
      }
      switch (numDims) {
        case 2: {
	  long d0, d1;                    /* Indices... */
	  for (d0 = 0, iBoffset = 0; d0 < dimSizes[0]; d0++) {
	     for (d1 = 0; d1 < dimSizes[1]; d1++) {
	        oVoffset = (d0 * products[0]) + (d1 * products[1]);
	        oBoffset = oVoffset * nValueBytes;
	        memmove ((Byte *) oBuffer + (size_t) oBoffset,
		         (Byte *) iBuffer + (size_t) iBoffset,
		         (size_t) nValueBytes);
	        iBoffset += nValueBytes;
	     }
	  }
	  break;
        }
        case 3: {
	  long d0, d1, d2;                /* Indices... */
	  for (d0 = 0, iBoffset = 0; d0 < dimSizes[0]; d0++) {
	     for (d1 = 0; d1 < dimSizes[1]; d1++) {
	        for (d2 = 0; d2 < dimSizes[2]; d2++) {
		   oVoffset = (d0 * products[0]) + (d1 * products[1]) +
			      (d2 * products[2]);
		   oBoffset = oVoffset * nValueBytes;
		   memmove ((Byte *) oBuffer + (size_t) oBoffset,
			    (Byte *) iBuffer + (size_t) iBoffset,
			    (size_t) nValueBytes);
		   iBoffset += nValueBytes;
	        }
	     }
	  }
	  break;
        }
        default: {
	  long indices[CDF_MAX_DIMS]; long nValues; long i;
	  for (dimN = 0; dimN < numDims; dimN++) indices[dimN] = 0;
	  for (dimN = 0, nValues = 1; dimN < numDims; dimN++) {
	     nValues *= dimSizes[dimN];
	  }
	  for (i = 0, iBoffset = 0; i < nValues; i++) {
	     for (oVoffset = 0, dimN = 0; dimN < numDims; dimN++) {
	        oVoffset += indices[dimN] * products[dimN];
	     }
	     oBoffset = oVoffset * nValueBytes;
	     memmove ((Byte *) oBuffer + (size_t) oBoffset,
		      (Byte *) iBuffer + (size_t) iBoffset,
		      (size_t) nValueBytes);
	     iBoffset += nValueBytes;
	     INCRindicesROW (numDims, dimSizes, indices);
	  }
	  break;
        }
      }
      break;
    }
  }
  return;
}

/******************************************************************************
* COLtoROW.
******************************************************************************/

STATICforIDL void COLtoROW (iBuffer, oBuffer, numDims, dimSizes, nValueBytes)
void *iBuffer;
void *oBuffer;
long numDims;
long dimSizes[];
long nValueBytes;
{
  switch (numDims) {
    case 0:
    case 1: {
      long nValues; int dimN;
      for (dimN = 0, nValues = 1; dimN < numDims; dimN++) {
         nValues *= dimSizes[dimN];
      }
      memmove (oBuffer, iBuffer, (size_t) (nValues * nValueBytes));
      break;
    }
    default: {
      long products[CDF_MAX_DIMS];        /* Products, what each dimension is
					     `worth'. */
      long iBoffset;                      /* Input buffer, byte offset. */
      long oBoffset;                      /* Output buffer, byte offset. */
      long oVoffset;                      /* Output buffer, value offset. */
      int dimN;                           /* Dimension number. */
      products[(int)(numDims-1)] = 1;
      for (dimN = (int) (numDims - 2); dimN >= 0; dimN--) {
         products[dimN] = products[dimN+1] * dimSizes[dimN+1];
      }
      switch (numDims) {
        case 2: {
	  long d0, d1;                    /* Indices... */
	  for (d1 = 0, iBoffset = 0; d1 < dimSizes[1]; d1++) {
	     for (d0 = 0; d0 < dimSizes[0]; d0++) {
	        oVoffset = (d0 * products[0]) + (d1 * products[1]);
	        oBoffset = oVoffset * nValueBytes;
	        memmove ((Byte *) oBuffer + (size_t) oBoffset,
		         (Byte *) iBuffer + (size_t) iBoffset,
		         (size_t) nValueBytes);
	        iBoffset += nValueBytes;
	     }
	  }
	  break;
        }
        case 3: {
	  long d0, d1, d2;                /* Indices... */
	  for (d2 = 0, iBoffset = 0; d2 < dimSizes[2]; d2++) {
	     for (d1 = 0; d1 < dimSizes[1]; d1++) {
	        for (d0 = 0; d0 < dimSizes[0]; d0++) {
		   oVoffset = (d0 * products[0]) + (d1 * products[1]) +
			      (d2 * products[2]);
		   oBoffset = oVoffset * nValueBytes;
		   memmove ((Byte *) oBuffer + (size_t) oBoffset,
			    (Byte *) iBuffer + (size_t) iBoffset,
			    (size_t) nValueBytes);
		   iBoffset += nValueBytes;
	        }
	     }
	  }
	  break;
        }
        default: {
	  long indices[CDF_MAX_DIMS]; long nValues; long i;
	  for (dimN = 0; dimN < numDims; dimN++) indices[dimN] = 0;
	  for (dimN = 0, nValues = 1; dimN < numDims; dimN++) {
	     nValues *= dimSizes[dimN];
	  }
	  for (i = 0, iBoffset = 0; i < nValues; i++) {
	     for (oVoffset = 0, dimN = 0; dimN < numDims; dimN++) {
	        oVoffset += indices[dimN] * products[dimN];
	     }
	     oBoffset = oVoffset * nValueBytes;
	     memmove ((Byte *) oBuffer + (size_t) oBoffset,
		      (Byte *) iBuffer + (size_t) iBoffset,
		      (size_t) nValueBytes);
	     iBoffset += nValueBytes;
	     INCRindicesCOL (numDims, dimSizes, indices);
	  }
	  break;
        }
      }
      break;
    }
  }
  return;
}

/******************************************************************************
* INCRindicesROW.
*    Increment to next set of indices, row majority.  When at the last set of
* indices, roll over to 0,0,0,...
******************************************************************************/

STATICforIDL void INCRindicesROW (numDims, dimSizes, indices)
long numDims;
long dimSizes[];
long indices[];
{
  int dimN;
  for (dimN = (int) (numDims - 1); dimN >= 0; dimN--)
     if (indices[dimN] == dimSizes[dimN] - 1)
       indices[dimN] = 0;
     else {
       indices[dimN]++;
       break;
     }
  return;
}

/******************************************************************************
* INCRindicesCOL.
*    Increment to next set of indices, column majority.  When at the last set
* of indices, roll over to 0,0,0,...
******************************************************************************/

STATICforIDL void INCRindicesCOL (numDims, dimSizes, indices)
long numDims;
long dimSizes[];
long indices[];
{
  int dimN;
  for (dimN = 0; dimN < numDims; dimN++)
     if (indices[dimN] == dimSizes[dimN] - 1)
       indices[dimN] = 0;
     else {
       indices[dimN]++;
       break;
     }
  return;
}

/******************************************************************************
* CheckEntryOp.
******************************************************************************/

STATICforIDL CDFstatus CheckEntryOp (CDF, entryType, Cur)
struct cdfSTRUCT *CDF;
int entryType;
struct CURstruct *Cur;
{
  Int32 scope; CDFstatus pStatus = CDF_OK;
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
    if (BADzOP(CDF,entryType == rENTRYt)) return ILLEGAL_IN_zMODE;
  }
  return pStatus;
}

/******************************************************************************
* SetCURgrEntry.
******************************************************************************/

STATICforIDL CDFstatus SetCURgrEntry (CDF, useCurrent, entryNum)
struct cdfSTRUCT *CDF;
Logical useCurrent;	/* TRUE if current g/rEntry offset can be used to speed
			   up the search. */
long entryNum;		/* The new g/rEntry number. */
{
  CDFstatus pStatus = CDF_OK, tStatus;
  Int32 scope, offset, attrNum, attrNumX, entryNumX, nextOffset;
  /****************************************************************************
  * Check if the new g/rEntry number is the reserved entry number.
  ****************************************************************************/
  if (entryNum == RESERVED_ENTRYNUM) {
    CDF->CURgrEntryNum = RESERVED_ENTRYNUM;
    CDF->CURgrEntryOffset = RESERVED_ENTRYOFFSET;
    return pStatus;
  }
  /****************************************************************************
  * Check that a current attribute is selected.
  ****************************************************************************/
  if (CDF->CURattrOffset == RESERVED_ATTROFFSET) {
    CDF->CURgrEntryNum = entryNum;
    CDF->CURgrEntryOffset = RESERVED_ENTRYOFFSET;
    return pStatus;
  }
  /****************************************************************************
  * Read the scope and number of the current attribute.
  ****************************************************************************/
  if (!sX(ReadADR(CDF,CDF->CURattrOffset,
		  ADR_SCOPE,&scope,
		  ADR_NUM,&attrNum,
		  ADR_NULL),&pStatus)) return pStatus;
  /****************************************************************************
  * If the current attribute is variable-scoped and zMode is on, then the
  * current g/rEntry offset is n/a.
  ****************************************************************************/
  if (VARIABLEscope(scope) && zModeON(CDF)) {
    CDF->CURgrEntryNum = entryNum;
    CDF->CURgrEntryOffset = RESERVED_ENTRYOFFSET;
    return pStatus;
  }
  /****************************************************************************
  * Check if the next entry is the one being searched for.  For this to
  * be the case, an entry must currently be selected and must be associated
  * with the current attribute, the next entry must exist, and the next
  * entry's number must be the entry number being searched for.  But don't try
  * this if a V2.0 CDF because of the bad terminating offset of the AEDR
  * linked lists in those CDFs.
  ****************************************************************************/
  if (useCurrent && !CDF->badTerminatingOffsets) {
    if (CDF->CURgrEntryOffset != RESERVED_ENTRYOFFSET) {
      if (!sX(ReadAEDR(CDF,CDF->CURgrEntryOffset,
		       AEDR_ATTRNUM,&attrNumX,
		       AEDR_AEDRNEXT,&nextOffset,
		       AEDR_NULL),&pStatus)) return pStatus;
      if (attrNumX == attrNum && nextOffset != 0) {
	if (!sX(ReadAEDR(CDF,nextOffset,AEDR_NUM,
			 &entryNumX,AEDR_NULL),&pStatus)) return pStatus;
	if (entryNumX == entryNum) {
	  CDF->CURgrEntryNum = entryNum;
	  CDF->CURgrEntryOffset = nextOffset;
	  return pStatus;
	}
      }
    }
  }
  /****************************************************************************
  * Search the list of AEDRs for the entry.
  ****************************************************************************/
  tStatus = FindEntryByNumber (CDF, CDF->CURattrOffset, FALSE, entryNum,
			       &offset);
  switch (tStatus) {
    case CDF_OK:
      break;
    case NO_SUCH_ENTRY:
      offset = RESERVED_ENTRYOFFSET;
      break;
    default:
      return tStatus;
  }
  CDF->CURgrEntryNum = entryNum;
  CDF->CURgrEntryOffset = offset;
  return pStatus;
}

/******************************************************************************
* SetCURzEntry.
******************************************************************************/

STATICforIDL CDFstatus SetCURzEntry (CDF, useCurrent, entryNum)
struct cdfSTRUCT *CDF;
Logical useCurrent;	/* TRUE if current zEntry offset can be used to speed
			   up the search. */
long entryNum;		/* The new zEntry number. */
{
  CDFstatus pStatus = CDF_OK, tStatus;
  Int32 scope, offset, attrNum, attrNumX, entryNumX, nextOffset;
  Logical zEntry;
  long entryN;
  /****************************************************************************
  * Check if the new zEntry number is the reserved entry number.
  ****************************************************************************/
  if (entryNum == RESERVED_ENTRYNUM) {
    CDF->CURzEntryNum = RESERVED_ENTRYNUM;
    CDF->CURzEntryOffset = RESERVED_ENTRYOFFSET;
    return pStatus;
  }
  /****************************************************************************
  * Check that a current attribute is selected.
  ****************************************************************************/
  if (CDF->CURattrOffset == RESERVED_ATTROFFSET) {
    CDF->CURzEntryNum = entryNum;
    CDF->CURzEntryOffset = RESERVED_ENTRYOFFSET;
    return pStatus;
  }
  /****************************************************************************
  * Read the scope and number of the current attribute.
  ****************************************************************************/
  if (!sX(ReadADR(CDF,CDF->CURattrOffset,
		  ADR_SCOPE,&scope,
		  ADR_NUM,&attrNum,
		  ADR_NULL),&pStatus)) return pStatus;
  /****************************************************************************
  * If the current attribute is global-scoped, then the current zEntry offset
  * is n/a.
  ****************************************************************************/
  if (GLOBALscope(scope)) {
    CDF->CURzEntryNum = entryNum;
    CDF->CURzEntryOffset = RESERVED_ENTRYOFFSET;
    return pStatus;
  }
  /****************************************************************************
  * Determine if a AgrEDR or AzEDR and the true entry number.
  ****************************************************************************/
  if (zModeON(CDF)) {
    if (entryNum < CDF->NrVars) {
      zEntry = FALSE;
      entryN = entryNum;
    }
    else {
      zEntry = TRUE;
      entryN = entryNum - CDF->NrVars;
    }
  }
  else {
    zEntry = TRUE;
    entryN = entryNum;
  }
  /****************************************************************************
  * Check if the next entry is the one being searched for.  For this to
  * be the case, an entry must currently be selected and must be associated
  * with the current attribute, the next entry must exist, and the next
  * entry's number must be the entry number being searched for.  But don't try
  * this if a V2.0 CDF because of the bad terminating offset of the AEDR
  * linked lists in those CDFs.
  ****************************************************************************/
  if (useCurrent && !CDF->badTerminatingOffsets) {
    if (CDF->CURzEntryOffset != RESERVED_ENTRYOFFSET) {
      if (!sX(ReadAEDR(CDF,CDF->CURzEntryOffset,
		       AEDR_ATTRNUM,&attrNumX,
		       AEDR_AEDRNEXT,&nextOffset,
		       AEDR_NULL),&pStatus)) return pStatus;
      if (attrNumX == attrNum && nextOffset != 0) {
	if (!sX(ReadAEDR(CDF,nextOffset,AEDR_NUM,
			 &entryNumX,AEDR_NULL),&pStatus)) return pStatus;
	if (entryNumX == entryN) {
	  CDF->CURzEntryNum = entryNum;
	  CDF->CURzEntryOffset = nextOffset;
	  return pStatus;
	}
      }
    }
  }
  /****************************************************************************
  * Search the list of AEDRs for the entry.
  ****************************************************************************/
  tStatus = FindEntryByNumber (CDF, CDF->CURattrOffset, zEntry, entryN,
			       &offset);
  switch (tStatus) {
    case CDF_OK:
      break;
    case NO_SUCH_ENTRY:
      offset = RESERVED_ENTRYOFFSET;
      break;
    default:
      return tStatus;
  }
  CDF->CURzEntryNum = entryNum;
  CDF->CURzEntryOffset = offset;
  return pStatus;
}

/******************************************************************************
* UpdateInitializedVars.
******************************************************************************/

STATICforIDL CDFstatus UpdateInitializedVars (CDF)
struct cdfSTRUCT *CDF;
{
  CDFstatus pStatus = CDF_OK;
  int varNum;
  for (varNum = 0; varNum < CDF->NrVars; varNum++) {
     if (CDF->rVars[varNum] != NULL) {
       if (!sX(CalcVarParms(CDF,CDF->rVars[varNum]),&pStatus)) return pStatus;
     }
  }
  for (varNum = 0; varNum < CDF->NzVars; varNum++) {
     if (CDF->zVars[varNum] != NULL) {
       if (!sX(CalcVarParms(CDF,CDF->zVars[varNum]),&pStatus)) return pStatus;
     }
  }
  return pStatus;
}

/******************************************************************************
* Int32toCDFid.
******************************************************************************/

STATICforIDL CDFid Int32toCDFid (id)
Int32 id;
{
#if defined(alphaosf) || defined(IRIX64bit)
#if defined(alphaosf)
  if (id == 0)
    return RESERVED_CDFID;
  else
    return ((CDFid) ((long) id | (long) 0x100000000));
#else
  union {
    CDFid id;
    Int32 i[2];
  } u;
  u.i[0] = 0;
  u.i[1] = id;
  return u.id;
#endif
#else
  return ((CDFid) id);
#endif
}

/******************************************************************************
* CDFidToInt32.
*    On 64-bit machines (OSF/1 and IRIX 6.x in 64-bit mode), truncation may
* occur when the pointer (CDFid) is assigned to a 32-bit integer.
******************************************************************************/

STATICforIDL Int32 CDFidToInt32 (id)
CDFid id;
{
#if defined(alphaosf) || defined(IRIX64bit)
  union {
    CDFid id;
    Int32 i[2];
  } u;
  u.id = id;
#if defined(alphaosf)
  return u.i[0];
#endif
#if defined(IRIX64bit)
  return u.i[1];
#endif
#else
  return ((Int32) id);
#endif
}
