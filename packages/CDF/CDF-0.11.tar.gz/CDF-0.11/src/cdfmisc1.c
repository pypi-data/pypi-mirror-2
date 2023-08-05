/******************************************************************************
*
*  NSSDC/CDF                     CDF library miscellaneous functions, 1 of 2.
*
*  Version 1.3, 10-Sep-96, Hughes STX.
*
*  Modification history:
*
*   V1.0  19-Dec-94, J Love     Original version.
*   V1.0a 29-Dec-94, J Love     WriteBuffer: increment buffer pointer in the
*                               case where the memory allocation failed.
*   V1.1  13-Jan-95, J Love     Encode/decode changes.  More cache-residency.
*                               Allow all possible extensions on all machines.
*   V1.1a 19-Jan-95, J Love     IRIX 6.x (64-bit).
*   V1.1b 24-Feb-95, J Love     Solaris 2.3 IDL i/f.
*   V1.2  21-Mar-95, J Love     POSIX.
*   V1.2a 18-Apr-95, J Love     More POSIX.  MEMLOG_.
*   V1.2b 19-Apr-95, J Love     Memory functions moved to `cdfmem.c'.
*   V1.2c  7-Sep-95, J Love	Corrected status codes being returned.  Try
*				progressively smaller temporary buffers in
*				`WriteVarElems'.
*   V1.3  10-Sep-96, J Love	Fixed bug in `ResizeInternalRecord' involving
*				the reading of UIRs when it isn't safe.
*
******************************************************************************/

#include "cdflib.h"
#include "cdfrev.h"

/******************************************************************************
* SingleAllocateRecords.
*   Allocate variable data records (VVRs) in a single-file CDF.  Don't call
* this routine if the records have already been allocated.
******************************************************************************/

STATICforIDL CDFstatus SingleAllocateRecords (CDF, Var, toRecNum,
					      ignoreExtendRecs)
struct cdfSTRUCT *CDF;          /* Pointer to CDF. */
struct varSTRUCT *Var;          /* Pointer to variable. */
long toRecNum;                  /* Allocate to this record number. */
Logical ignoreExtendRecs;       /* If TRUE, additional records based on the
				   number of extend records will not be
				   allocated. */
{
  CDFstatus pStatus = CDF_OK;
  long nRecs;
  Int32 vxrOffsetLast, vxrOffsetNew, vvrOffset, vvrRecordSize,
	vvrRecordType = VVR_, vxrRecordType = VXR_, vxrRecordSize;
  int entryN;
  /****************************************************************************
  * Read offset of last VXR.
  ****************************************************************************/
  if (!sX(ReadVDR(CDF,Var->VDRoffset,Var->zVar,
		  VDR_VXRTAIL,&vxrOffsetLast,VDR_NULL),&pStatus)) return
								  pStatus;
  /****************************************************************************
  * Allocate to at least the needed record.
  ****************************************************************************/
  if (vxrOffsetLast == 0) {
    /**************************************************************************
    * No records allocated yet for the variable.  First calculate the number
    * of records to allocate.
    **************************************************************************/
    struct VXRstruct newVXR;
    if (ignoreExtendRecs)
      nRecs = toRecNum + 1;
    else
      nRecs = MAXIMUM (toRecNum + 1, Var->sFile.nExtendRecs);
    /**************************************************************************
    * Allocate the new VXR.  The VXR's record size and type are written here
    * so that the allocation of the VVR will be performed correctly.
    **************************************************************************/
    vxrRecordSize = VXR_BASE_SIZE;
    if (!sX(AllocateInternalRecord(CDF,vxrRecordSize,&vxrOffsetNew),&pStatus))
      return pStatus;
    if (!sX(WriteVXR(CDF,vxrOffsetNew,
		     VXR_RECORDSIZE,&vxrRecordSize,
		     VXR_RECORDTYPE,&vxrRecordType,
		     VXR_NULL),&pStatus)) return pStatus;
    /**************************************************************************
    * Allocate and write the size and type fields of the VVR.  It is assumed
    * that all of the records will be written during this call to the CDF
    * library.
    **************************************************************************/
    vvrRecordSize = VVR_BASE_SIZE + (nRecs * Var->NphyRecBytes);
    if (!sX(AllocateInternalRecord(CDF,vvrRecordSize,&vvrOffset),&pStatus))
      return pStatus;
    if (!sX(WriteVVR(CDF,vvrOffset,VVR_RECORDSIZE,&vvrRecordSize,
				   VVR_RECORDTYPE,&vvrRecordType,
				   VVR_NULL),&pStatus)) return pStatus;
    /**************************************************************************
    * Write the VXR.
    **************************************************************************/
    newVXR.RecordSize = vxrRecordSize;
    newVXR.RecordType = VXR_;
    newVXR.VXRnext = 0;
    newVXR.Nentries = NUM_VXR_ENTRIES;
    newVXR.NusedEntries = 1;
    newVXR.FirstRec[0] = 0;
    newVXR.LastRec[0] = nRecs - 1;
    newVXR.VVRoffset[0] = vvrOffset;
    for (entryN = 1; entryN < NUM_VXR_ENTRIES; entryN++) {
       newVXR.FirstRec[entryN] = -1;
       newVXR.LastRec[entryN] = -1;
       newVXR.VVRoffset[entryN] = -1;
    }
    if (!sX(WriteVXR(CDF,vxrOffsetNew,VXR_RECORD,
		     &newVXR,VXR_NULL),&pStatus)) return pStatus;
    Var->sFile.maxAllocated = newVXR.LastRec[0];
    Var->sFile.firstRecInVVR = newVXR.FirstRec[0];
    Var->sFile.lastRecInVVR = newVXR.LastRec[0];
    Var->sFile.offsetOfVVR = newVXR.VVRoffset[0];
    /**************************************************************************
    * Point the VDR to the new VXR.
    **************************************************************************/
    if (!sX(WriteVDR(CDF,Var->VDRoffset,Var->zVar,
		     VDR_VXRHEAD,&vxrOffsetNew,
		     VDR_VXRTAIL,&vxrOffsetNew,
		     VDR_NULL),&pStatus)) return pStatus;
  }
  else {
    /**************************************************************************
    * Already some records for the variable.  First read the last VXR and
    * calculate the number of records to allocate.
    **************************************************************************/
    Int32 lastRecAllocated; Logical success;
    struct VXRstruct lastVXR;
    if (!sX(ReadVXR(CDF,vxrOffsetLast,VXR_RECORD,&lastVXR,VXR_NULL),&pStatus))
      return pStatus;
    lastRecAllocated = lastVXR.LastRec[(int)(lastVXR.NusedEntries-1)];
    if (ignoreExtendRecs)
      nRecs = toRecNum - lastRecAllocated;
    else
      nRecs = MAXIMUM (toRecNum - lastRecAllocated, Var->sFile.nExtendRecs);
    /**************************************************************************
    * Then check if the last VVR can be extended.
    **************************************************************************/
    vvrOffset = lastVXR.VVRoffset[(int)(lastVXR.NusedEntries-1)];
    if (!sX(ReadVVR(CDF,vvrOffset,VVR_RECORDSIZE,
		    &vvrRecordSize,VVR_NULL),&pStatus)) return pStatus;
    if (!sX(ResizeInternalRecord(CDF,vvrRecordSize,vvrOffset,
				 vvrRecordSize + (nRecs * Var->NphyRecBytes),
				 &vvrOffset,FALSE,&success),&pStatus)) return
								       pStatus;
    if (success) {
      /************************************************************************
      * The last VVR has been extended.
      ************************************************************************/
      vvrRecordSize += nRecs * Var->NphyRecBytes;
      if (!sX(WriteVVR(CDF,vvrOffset,VVR_RECORDSIZE,
		       &vvrRecordSize,VVR_NULL),&pStatus)) return pStatus;
      /************************************************************************
      * Update the last VXR entry (which points to the last VVR).
      ************************************************************************/
      entryN = (int) (lastVXR.NusedEntries - 1);
      lastVXR.LastRec[entryN] += nRecs;
      if (!sX(WriteVXR(CDF,vxrOffsetLast,VXR_LASTREC,
		       lastVXR.LastRec,VXR_NULL),&pStatus)) return pStatus;
      Var->sFile.maxAllocated = lastVXR.LastRec[entryN];
      Var->sFile.firstRecInVVR = lastVXR.FirstRec[entryN];
      Var->sFile.lastRecInVVR = lastVXR.LastRec[entryN];
      Var->sFile.offsetOfVVR = lastVXR.VVRoffset[entryN];
    }
    else {
      /************************************************************************
      * Can't extend last VVR, create another VVR.  The VVR's record size and
      * type fields are written here so that a possible allocation of a new
      * VXR will be performed correctly.
      ************************************************************************/
      vvrRecordSize = VVR_BASE_SIZE + (nRecs * Var->NphyRecBytes);
      if (!sX(AllocateInternalRecord(CDF,vvrRecordSize,&vvrOffset),&pStatus))
	return pStatus;
      if (!sX(WriteVVR(CDF,vvrOffset,VVR_RECORDSIZE,&vvrRecordSize,
				     VVR_RECORDTYPE,&vvrRecordType,
				     VVR_NULL),&pStatus)) return pStatus;
      /************************************************************************
      * Add an entry to the last VXR (or create a new VXR if the last VXR is
      * full).
      ************************************************************************/
      if (lastVXR.NusedEntries < lastVXR.Nentries) {
	/**********************************************************************
	* Add an entry to the last VXR.
	**********************************************************************/
	entryN = (int) lastVXR.NusedEntries;
	lastVXR.FirstRec[entryN] = lastRecAllocated+1;
	lastVXR.LastRec[entryN] = lastRecAllocated+nRecs;
	lastVXR.VVRoffset[entryN] = vvrOffset;
	lastVXR.NusedEntries++;
	if (!sX(WriteVXR(CDF,vxrOffsetLast,VXR_RECORD,
			 &lastVXR,VXR_NULL),&pStatus)) return pStatus;
	Var->sFile.maxAllocated = lastVXR.LastRec[entryN];
	Var->sFile.firstRecInVVR = lastVXR.FirstRec[entryN];
	Var->sFile.lastRecInVVR = lastVXR.LastRec[entryN];
	Var->sFile.offsetOfVVR = lastVXR.VVRoffset[entryN];
      }
      else {
	/**********************************************************************
	* Create a new VXR.
	**********************************************************************/
	struct VXRstruct newVXR;
	newVXR.RecordSize = VXR_BASE_SIZE;
	newVXR.RecordType = VXR_;
	newVXR.VXRnext = 0;
	newVXR.Nentries = NUM_VXR_ENTRIES;
	newVXR.NusedEntries = 1;
	newVXR.FirstRec[0] = lastRecAllocated + 1;
	newVXR.LastRec[0] = lastRecAllocated + nRecs;
	newVXR.VVRoffset[0] = vvrOffset;
	for (entryN = 1; entryN < NUM_VXR_ENTRIES; entryN++) {
	   newVXR.FirstRec[entryN] = -1;
	   newVXR.LastRec[entryN] = -1;
	   newVXR.VVRoffset[entryN] = -1;
	}
	if (!sX(AllocateInternalRecord(CDF,newVXR.RecordSize,
				       &vxrOffsetNew),&pStatus)) return
								 pStatus;
	if (!sX(WriteVXR(CDF,vxrOffsetNew,VXR_RECORD,
			 &newVXR,VXR_NULL),&pStatus)) return pStatus;
	Var->sFile.maxAllocated = newVXR.LastRec[0];
	Var->sFile.firstRecInVVR = newVXR.FirstRec[0];
	Var->sFile.lastRecInVVR = newVXR.LastRec[0];
	Var->sFile.offsetOfVVR = newVXR.VVRoffset[0];
	/**********************************************************************
	* Point last VXR to the new VXR.
	**********************************************************************/
	if (!sX(WriteVXR(CDF,vxrOffsetLast,VXR_VXRNEXT,
			 &vxrOffsetNew,VXR_NULL),&pStatus)) return pStatus;
	/**********************************************************************
	* Point VDR to the new VXR.
	**********************************************************************/
	if (!sX(WriteVDR(CDF,Var->VDRoffset,Var->zVar,VDR_VXRTAIL,
			 &vxrOffsetNew,VDR_NULL),&pStatus)) return pStatus;
      }
    }
  }
  return pStatus;
}

/******************************************************************************
* CorrectV20eof.
******************************************************************************/

STATICforIDL CDFstatus CorrectV20eof (CDF)
struct cdfSTRUCT *CDF;
{
  CDFstatus pStatus = CDF_OK;
  Int32 eof = 0, size, vOffset, aOffset, eOffset, nAttrs, nEntries;
  int varX, attrX, entryX;
  /****************************************************************************
  * Check if CDR is last internal record.
  ****************************************************************************/
  if (!sX(ReadCDR(CDF,CDR_RECORDSIZE,&size,CDR_NULL),&pStatus)) return pStatus;
  eof = MAXIMUM (eof, CDF->CDRoffset + size);
  /****************************************************************************
  * Check if GDR is last internal record.
  ****************************************************************************/
  if (!sX(ReadGDR(CDF,GDR_RECORDSIZE,&size,GDR_NULL),&pStatus)) return pStatus;
  eof = MAXIMUM (eof, CDF->GDRoffset + size);
  /****************************************************************************
  * Scan through rVDRs checking if each is the last internal record.  Note
  * that V2.0 CDFs won't have zVDRs, VXRs, or VVRs.
  ****************************************************************************/
  if (!sX(ReadGDR(CDF,GDR_rVDRHEAD,&vOffset,GDR_NULL),&pStatus)) return
								 pStatus;
  for (varX = 0; varX < CDF->NrVars; varX++) {
     if (!sX(ReadVDR(CDF,vOffset,FALSE,
		     VDR_RECORDSIZE,&size,VDR_NULL),&pStatus)) return pStatus;
     eof = MAXIMUM (eof, vOffset + size);
     if (!sX(ReadVDR(CDF,vOffset,FALSE,
		     VDR_VDRNEXT,&vOffset,VDR_NULL),&pStatus)) return pStatus;
  }
  /****************************************************************************
  * Scan through the ADRs checking if each is the last internal record.
  ****************************************************************************/
  if (!sX(ReadGDR(CDF,GDR_NUMATTR,&nAttrs,
		      GDR_ADRHEAD,&aOffset,
		      GDR_NULL),&pStatus)) return pStatus;
  for (attrX = 0; attrX < nAttrs; attrX++) {
     if (!sX(ReadADR(CDF,aOffset,ADR_RECORDSIZE,&size,ADR_NULL),&pStatus))
       return pStatus;
     eof = MAXIMUM (eof, aOffset + size);
     /*************************************************************************
     * Scan through the ArEDRs checking if each is the last internal record.
     * Note that V2.0 CDFs won't have AzEDRs.
     *************************************************************************/
     if (!sX(ReadADR(CDF,aOffset,ADR_AgrEDRHEAD,&eOffset,
				 ADR_NgrENTRIES,&nEntries,
				 ADR_NULL),&pStatus)) return pStatus;
     for (entryX = 0; entryX < nEntries; entryX++) {
	if (!sX(ReadAEDR(CDF,eOffset,AEDR_RECORDSIZE,
			 &size,AEDR_NULL),&pStatus)) return pStatus;
	eof = MAXIMUM (eof, eOffset + size);
	if (!sX(ReadAEDR(CDF,eOffset,AEDR_AEDRNEXT,
			 &eOffset,AEDR_NULL),&pStatus)) return pStatus;
     }
     if (!sX(ReadADR(CDF,aOffset,ADR_ADRNEXT,
		     &aOffset,ADR_NULL),&pStatus)) return pStatus;
  }
  /****************************************************************************
  * Save correct EOF and return.
  ****************************************************************************/
  if (!sX(WriteGDR(CDF,GDR_EOF,&eof,GDR_NULL),&pStatus)) return pStatus;
  return pStatus;
}

/******************************************************************************
* CorrectV20offsets.
******************************************************************************/

STATICforIDL CDFstatus CorrectV20offsets (CDF)
struct cdfSTRUCT *CDF;
{
  CDFstatus pStatus = CDF_OK;
  Int32 zero = 0, size, vOffset, aOffset, eOffset, nAttrs, nEntries;
  int varX, attrX, entryX;
  /****************************************************************************
  * Scan through rVDRs fixing the next VDR field of the last one (setting it
  * to an offset of zero).  Note that V2.0 CDFs won't have zVDRs, VXRs, or
  * VVRs.
  ****************************************************************************/
  if (!sX(ReadGDR(CDF,GDR_rVDRHEAD,&vOffset,GDR_NULL),&pStatus)) return
								 pStatus;
  for (varX = 0; varX < CDF->NrVars; varX++) {
     if (!sX(ReadVDR(CDF,vOffset,FALSE,
		     VDR_RECORDSIZE,&size,VDR_NULL),&pStatus)) return pStatus;
     if (varX == CDF->NrVars - 1) {
       if (!sX(WriteVDR(CDF,vOffset,FALSE,VDR_VDRNEXT,
			&zero,VDR_NULL),&pStatus)) return pStatus;
     }
     else {
       if (!sX(ReadVDR(CDF,vOffset,FALSE,
		       VDR_VDRNEXT,&vOffset,VDR_NULL),&pStatus)) return
								 pStatus;
     }
  }
  /****************************************************************************
  * Scan through the ADRs fixing the next ADR field of the last one (setting
  * it to an offset of zero).
  ****************************************************************************/
  if (!sX(ReadGDR(CDF,GDR_NUMATTR,&nAttrs,
		      GDR_ADRHEAD,&aOffset,
		      GDR_NULL),&pStatus)) return pStatus;
  for (attrX = 0; attrX < nAttrs; attrX++) {
     if (!sX(ReadADR(CDF,aOffset,ADR_RECORDSIZE,&size,ADR_NULL),&pStatus))
       return pStatus;
     /*************************************************************************
     * Scan through the ArEDRs fixing the next ArEDR field of the last one
     * (setting it to an offset of zero).  Note that V2.0 CDFs won't have
     * AzEDRs.
     *************************************************************************/
     if (!sX(ReadADR(CDF,aOffset,ADR_AgrEDRHEAD,&eOffset,
				 ADR_NgrENTRIES,&nEntries,
				 ADR_NULL),&pStatus)) return pStatus;
     for (entryX = 0; entryX < nEntries; entryX++) {
	if (!sX(ReadAEDR(CDF,eOffset,AEDR_RECORDSIZE,
			 &size,AEDR_NULL),&pStatus)) return pStatus;
	if (entryX == nEntries - 1) {
	  if (!sX(WriteAEDR(CDF,eOffset,AEDR_AEDRNEXT,
			    &zero,AEDR_NULL),&pStatus)) return pStatus;
	}
	else {
	  if (!sX(ReadAEDR(CDF,eOffset,AEDR_AEDRNEXT,
			   &eOffset,AEDR_NULL),&pStatus)) return pStatus;
	}
     }
     if (attrX == nAttrs - 1) {
       if (!sX(WriteADR(CDF,aOffset,ADR_ADRNEXT,&zero,ADR_NULL),&pStatus))
	 return pStatus;
     }
     else {
       if (!sX(ReadADR(CDF,aOffset,ADR_ADRNEXT,&aOffset,ADR_NULL),&pStatus))
	 return pStatus;
     }
  }
  return pStatus;
}

/******************************************************************************
* CloseCDFfiles.
*     Close the open files of the specified CDF.  This routine closes all of
* the open files regardless of the number of errors detected.  The fields
* maintained in memory for efficiency are written to the `.cdf' before it is
* closed (if the CDF had been modified).
*     Because this routine is called when aborting a CDF, we cannot assume
* that the CDF structure is complete.  Eg., it may have been only partially
* initialized when the CDF was aborted.
******************************************************************************/

STATICforIDL CDFstatus CloseCDFfiles (CDF, vStats)
struct cdfSTRUCT *CDF;
vSTATS *vStats;
{
  CDFstatus pStatus = CDF_OK;
  struct varSTRUCT *Var;
  int varN;
  /****************************************************************************
  * If a multi-file CDF, close the variable files.
  ****************************************************************************/
  if (!CDF->singleFile) {
    /**************************************************************************
    * Close rVariable files.  If the pointer to the rVariable is NULL, then
    * the rVariable has yet to be initialized (and is obviously closed).
    **************************************************************************/
    if (CDF->rVars != NULL) {
      for (varN = 0; varN < CDF->NrVars; varN++) {
         Var = CDF->rVars[varN];
         if (Var != NULL) {
	   if (Var->status == VAR_OPENED) {
	     if (!CLOSEv(Var->fp,NULL)) {
	       sX (VAR_CLOSE_ERROR, &pStatus);
	     }
	     Var->status = VAR_CLOSED;
	   }
	 }
      }
    }
    /**************************************************************************
    * Close zVariable files.  If the pointer to the zVariable is NULL, then
    * the zVariable has yet to be initialized (and is obviously closed).
    **************************************************************************/
    if (CDF->zVars != NULL) {
      for (varN = 0; varN < CDF->NzVars; varN++) {
         Var = CDF->zVars[varN];
         if (Var != NULL) {
	   if (Var->status == VAR_OPENED) {
	     if (!CLOSEv(Var->fp,NULL)) {
	       sX (VAR_CLOSE_ERROR, &pStatus);
	     }
	     Var->status = VAR_CLOSED;
	   }
	 }
      }
    }
  }
  /****************************************************************************
  * Update fields held in memory for efficiency (if the CDF has been modified).
  * Also pad newly allocated records in a single-file CDF that have not yet
  * been written to.
  ****************************************************************************/
  if (CDF->status == CDF_READ_WRITE) {
    /**************************************************************************
    * Update GDR fields.
    **************************************************************************/
    sX (WriteGDR(CDF,GDR_rMAXREC,&(CDF->rMaxRec),
		     GDR_NULL), &pStatus);
    /**************************************************************************
    * Update rVDR fields.  Also pad any newly allocated records beyond the
    * last record actually written (in a single-file CDF).
    **************************************************************************/
    if (CDF->rVars != NULL) {
      for (varN = 0; varN < CDF->NrVars; varN++) {
         Var = CDF->rVars[varN];
         if (Var != NULL) {
	   sX (WriteVDR(CDF,Var->VDRoffset,FALSE,VDR_MAXREC,&(Var->maxRec),
					         VDR_NULL), &pStatus);
	   if (CDF->singleFile &&
	       Var->sFile.maxWritten < Var->sFile.maxAllocated) {
	     sX (PadRecords(CDF,Var,Var->sFile.maxWritten+1,
			    Var->sFile.maxAllocated), &pStatus);
	   }
         }
      }
    }
    /**************************************************************************
    * Update zVDR fields.  Also pad any newly allocated records beyond the
    * last record actually written (in a single-file CDF).
    **************************************************************************/
    if (CDF->zVars != NULL) {
      for (varN = 0; varN < CDF->NzVars; varN++) {
         Var = CDF->zVars[varN];
         if (Var != NULL) {
	   sX (WriteVDR(CDF,Var->VDRoffset,TRUE,VDR_MAXREC,&(Var->maxRec),
					        VDR_NULL), &pStatus);
	   if (CDF->singleFile &&
	       Var->sFile.maxWritten < Var->sFile.maxAllocated) {
	     sX (PadRecords(CDF,Var,Var->sFile.maxWritten+1,
			    Var->sFile.maxAllocated), &pStatus);
	   }
         }
      }
    }
  }
  /****************************************************************************
  * Close the `.cdf' file.
  ****************************************************************************/
  if (!CLOSEv(CDF->fp,vStats)) sX (CDF_CLOSE_ERROR, &pStatus);
  CDF->status = CDF_CLOSED;
  return pStatus;
}

/******************************************************************************
* WriteAccess.
*     Close and then reopen a CDF for read/write access (it was opened with
* read-only access initially).  If the CDF is earlier than CDF V2.5, then some
* of the fields will have to been fixed and the CDR will be truncated for a
* shorter copyright length.
*
* Don't worry about a CD-ROM on a UNIX system (uppercase case file extensions).
* You can't have write access to a file on a CD-ROM.
* 
******************************************************************************/

STATICforIDL Logical WriteAccess (CDF, Cur, pStatus)
struct cdfSTRUCT *CDF;
struct CURstruct *Cur;
CDFstatus *pStatus;
{
   Int32 versionNew = CDF_LIBRARY_VERSION,      /* New version... */
	 releaseNew = CDF_LIBRARY_RELEASE,
	 incrementNew = CDF_LIBRARY_INCREMENT;
   /***************************************************************************
   * Check if distribution is read-only.  The call to `sX' is may only to
   * keep compilers quite.  If just the `return' was made, some compilers
   * would display a warning about unreachable code.
   ***************************************************************************/
#if BUILD_READ_ONLY_DISTRIBUTION
   if (!sX(READ_ONLY_DISTRIBUTION,pStatus)) return FALSE;
#endif
   /***************************************************************************
   * Check if this CDF is in read-only mode.
   ***************************************************************************/
   if (CDF->readonlyMode) {
     *pStatus = READ_ONLY_MODE;
     return FALSE;
   }
   /***************************************************************************
   * Close all open files.
   ***************************************************************************/
   if (!sX(CloseCDFfiles(CDF,NULL),pStatus)) {
     AbortAccess (CDF, FALSE, Cur);
     return FALSE;
   }
   /***************************************************************************
   * Open `.cdf' file with read-write access.  If read-write access not
   * allowed, try to return to read-only access.  If reopening with read-only
   * access fails, free CDF structures as if CDF had been closed.
   ***************************************************************************/
   CDF->fp = V_open (CDF->pathname, READ_PLUS_a_mode);
   if (CDF->fp == NULL) {
     CDF->fp = V_open (CDF->pathname, READ_ONLY_a_mode);
     if (CDF->fp == NULL) {
       AbortAccess (CDF, FALSE, Cur);
       *pStatus = NO_MORE_ACCESS;
       return FALSE;
     }
     else {
       CDF->status = CDF_READ_ONLY;
       *pStatus = NO_WRITE_ACCESS;                      /* Don't return yet. */
     }
   }
   else
     CDF->status = CDF_READ_WRITE;
   /***************************************************************************
   * Fix various fields (if write access was obtained).
   ***************************************************************************/
   if (CDF->status == CDF_READ_WRITE) {
     char copyRight[CDF_COPYRIGHT_LEN+1];        /* Copyright text. */
     /*************************************************************************
     * If a V2.0 CDF, correct the EOF field.
     *************************************************************************/
     if (CDF->badEOF) {
       if (!sX(CorrectV20eof(CDF),pStatus)) {
	 AbortAccess (CDF, FALSE, Cur);
	 return FALSE;
       }
       CDF->badEOF = FALSE;
     }
     /*************************************************************************
     * If a V2.0 CDF, correct the terminating offset fields.  NOTE: Fix these
     * fields before the other "fixing" routines (which may depend on these
     * fields).
     *************************************************************************/
     if (CDF->badTerminatingOffsets) {
       if (!sX(CorrectV20offsets(CDF),pStatus)) {
	 AbortAccess (CDF, FALSE, Cur);
	 return FALSE;
       }
       CDF->badTerminatingOffsets = FALSE;
     }
     /*************************************************************************
     * If prior to CDF V2.1.1, then change the data type associated with the
     * "EPOCH" rVariable/rEntries to CDF_EPOCH.
     *************************************************************************/
     if (CDF->fakeEPOCH) {
       if (!sX(CorrectEPOCH(CDF),pStatus)) {
	 AbortAccess (CDF, FALSE, Cur);
	 return FALSE;
       }
       CDF->fakeEPOCH = FALSE;
     }
     /*************************************************************************
     * If prior to CDF V2.5, then truncate the CDR for a shorter copyright
     * field and shorten each VDR to reclaim the wasted space.
     *************************************************************************/
     if (CDF->wastedSpace) {
       if (!sX(ShortenCDR(CDF),pStatus)) {
	 AbortAccess (CDF, FALSE, Cur);
	 return FALSE;
       }
       if (!sX(ShortenVDRs(CDF),pStatus)) {
	 AbortAccess (CDF, FALSE, Cur);
	 return FALSE;
       }
       CDF->wastedSpace = FALSE;
     }
     /*************************************************************************
     * If prior to CDF V2.5, then convert all assumed scopes to definite
     * scopes.
     *************************************************************************/
     if (CDF->assumedScopes) {
       if (!sX(CorrectScopes(CDF),pStatus)) {
	 AbortAccess (CDF, FALSE, Cur);
	 return FALSE;
       }
       CDF->assumedScopes = FALSE;
     }
     /*************************************************************************
     * Update version/release/increment.
     *************************************************************************/
     if (!sX(WriteCDR(CDF,CDR_VERSION,&versionNew,
			  CDR_RELEASE,&releaseNew,
			  CDR_INCREMENT,&incrementNew,
			  CDR_NULL),pStatus)) {
       AbortAccess (CDF, FALSE, Cur);
       return FALSE;
     }
     /*************************************************************************
     * Update copyright.
     *************************************************************************/
     CDFcopyRight (copyRight);
     NulPad (copyRight, CDF_COPYRIGHT_LEN);
     if (!sX(WriteCDR(CDF,CDR_COPYRIGHT,copyRight,CDR_NULL),pStatus)) {
       AbortAccess (CDF, FALSE, Cur);
       return FALSE;
     }
   }
   /***************************************************************************
   * Set the proper number of cache buffers.
   ***************************************************************************/
   if (!CACHEv(CDF->fp,CDF->nCacheBuffers)) {
     *pStatus = BAD_CACHE_SIZE;
     AbortAccess (CDF, FALSE, Cur);
     return FALSE;
   }
   /***************************************************************************
   * If single-file, point the variable file pointers to the (new) `.cdf' file
   * pointer (for those variables that have been initialized).
   ***************************************************************************/
   if (CDF->singleFile) {
     struct varSTRUCT *Var;
     int varN;
     for (varN = 0; varN < CDF->NrVars; varN++) {
	Var = CDF->rVars[varN];
	if (Var != NULL) Var->fp = CDF->fp;
     }
     for (varN = 0; varN < CDF->NzVars; varN++) {
	Var = CDF->zVars[varN];
	if (Var != NULL) Var->fp = CDF->fp;
     }
   }
   return (CDF->status == CDF_READ_WRITE);
}

/******************************************************************************
* DeleteAccess.
*     Close and then reopen a CDF for delete access (it was opened with read-
* only access initially).
*
*     - Don't worry about a CD-ROM on a UNIX system (uppercase case file
*       extensions).  You can't have delete access to a file on a CD-ROM.
*
******************************************************************************/

STATICforIDL Logical DeleteAccess (CDF, Cur, pStatus)
struct cdfSTRUCT *CDF;
struct CURstruct *Cur;
CDFstatus *pStatus;
{
   /***************************************************************************
   * Check if distribution is read-only.  The call to `sX' is may only to
   * keep compilers quite.  If just the `return' was made, some compilers
   * would display a warning about unreachable code.
   ***************************************************************************/
#if BUILD_READ_ONLY_DISTRIBUTION
   if (!sX(READ_ONLY_DISTRIBUTION,pStatus)) return FALSE;
#endif
   /***************************************************************************
   * Check if this CDF is in read-only mode.
   ***************************************************************************/
   if (CDF->readonlyMode) {
     *pStatus = READ_ONLY_MODE;
     return FALSE;
   }
   /***************************************************************************
   * Close all open files.
   ***************************************************************************/
   if (!sX(CloseCDFfiles(CDF,NULL),pStatus)) {
     AbortAccess (CDF, FALSE, Cur);
     return FALSE;
   }
   /***************************************************************************
   * Open `.cdf' file with read-write access.  If read-write access not
   * allowed, try to return to read-only access.  If reopening with read-only
   * access fails, free CDF structures as if CDF had been closed.
   ***************************************************************************/
   CDF->fp = V_open (CDF->pathname, READ_PLUS_a_mode);
   if (CDF->fp == NULL) {
     CDF->fp = V_open (CDF->pathname, READ_ONLY_a_mode);
     if (CDF->fp == NULL) {
       AbortAccess (CDF, FALSE, Cur);
       *pStatus = NO_MORE_ACCESS;
       return FALSE;
     }
     else {
       CDF->status = CDF_READ_ONLY;
       *pStatus = NO_DELETE_ACCESS;                     /* Don't return yet. */
     }
   }
   else
     CDF->status = CDF_READ_WRITE;
   /***************************************************************************
   * If single-file, point the variable file pointers to the `.cdf' file
   * pointer.
   ***************************************************************************/
   if (CDF->singleFile) {
     int varN;
     for (varN = 0; varN < CDF->NrVars; varN++) {
	struct varSTRUCT *Var = CDF->rVars[varN];
	if (Var != NULL) Var->fp = CDF->fp;
     }
     for (varN = 0; varN < CDF->NzVars; varN++) {
	struct varSTRUCT *Var = CDF->zVars[varN];
	if (Var != NULL) Var->fp = CDF->fp;
     }
   }
   return (CDF->status == CDF_READ_WRITE);
}

/******************************************************************************
* WriteVarElems.
*    Write occurs at current offset (assumed to have been set before this
* routine is called).  On IBM PCs, it is assumed that `nBytes' will not
* exceed 65535.
******************************************************************************/

STATICforIDL CDFstatus WriteVarElems (Var, numElems, buffer)
struct varSTRUCT *Var;
long numElems;
void *buffer;
{
  CDFstatus pStatus = CDF_OK;
  long elemCount;
  /****************************************************************************
  * If no encoding is necessary, simply write the buffer.
  ****************************************************************************/
  if (Var->EncodeFunction == NULL) {
    long nBytes = numElems * Var->NelemBytes;
    if (!WRITEv(buffer,1,(size_t)nBytes,Var->fp)) return VAR_WRITE_ERROR;
    return pStatus;
  }
  /****************************************************************************
  * Use as large a temporary buffer as possible for the encoding conversion.
  * Start at the full number of elements and then halve that number until an
  * allocation succeeds.
  ****************************************************************************/
  elemCount = numElems;
  for (;;) {
     size_t nBytes = (size_t) (elemCount * Var->NelemBytes);
     void *tBuffer = AllocateMemory (nBytes, NULL);
     if (tBuffer != NULL) {
       long elemN = 0; Byte *bOffset = buffer;
       while (elemN < numElems) {
	 long thisElemCount = MINIMUM (elemCount, numElems - elemN);
	 size_t thisByteCount = (size_t) (thisElemCount * Var->NelemBytes);
	 memmove (tBuffer, bOffset, thisByteCount);
	 if (!sX(Var->EncodeFunction(tBuffer,thisElemCount),&pStatus)) {
	   FreeMemory (tBuffer, NULL);
	   return pStatus;
	 }
	 if (!WRITEv(tBuffer,1,thisByteCount,Var->fp)) {
	   FreeMemory (tBuffer, NULL);
	   return VAR_WRITE_ERROR;
	 }
	 elemN += thisElemCount;
	 bOffset += thisByteCount;
       }
       FreeMemory (tBuffer, NULL);
       return pStatus;
     }
     if (elemCount == 1) break;
     elemCount = (elemCount + 1) / 2;
  }
  return BAD_MALLOC;
}

/******************************************************************************
* WriteBuffer.
*    Write occurs at current offset (assumed to have been set before this
* routine is called).  On IBM PCs, it is assumed that `nBytes' will not
* exceed 65535.
******************************************************************************/

STATICforIDL CDFstatus WriteBuffer (CDF, dataType, numElems, buffer)
struct cdfSTRUCT *CDF;
long dataType;
long numElems;
void *buffer;
{
  CDFstatus pStatus = CDF_OK;
  size_t nElemBytes = CDFelemSize(dataType);
  size_t nBytes = (size_t) (numElems * nElemBytes);
  double eValue; long elemN; Byte *ptr; void *tBuffer;
  /****************************************************************************
  * Try to encode/write entire buffer.
  ****************************************************************************/
  tBuffer = AllocateMemory (nBytes, NULL);
  if (tBuffer != NULL) {
    if (!sX(ConvertBuffer(HostEncoding(),CDF->encoding,CDF->negToPosFp0mode,
			  dataType,numElems,buffer,tBuffer),&pStatus)) {
      FreeMemory (tBuffer, NULL);
      return pStatus;
    }
    if (!WRITEv(tBuffer,1,nBytes,CDF->fp)) {
      FreeMemory (tBuffer, NULL);
      return CDF_WRITE_ERROR;
    }
    FreeMemory (tBuffer, NULL);
    return pStatus;
  }
  /****************************************************************************
  * If that failed, encode/write one element at a time.
  ****************************************************************************/
  for (elemN = 0, ptr = buffer; elemN < numElems; elemN++, ptr += nElemBytes) {
     if (!sX(ConvertBuffer(HostEncoding(),CDF->encoding,
			   CDF->negToPosFp0mode,dataType,1L,ptr,
			   &eValue),&pStatus)) return pStatus;
     if (!WRITEv(&eValue,1,nElemBytes,CDF->fp)) return CDF_WRITE_ERROR;
  }
  return pStatus;
}

/******************************************************************************
* NegativeZeroReal4.
*   Checks for -0.0 (on any type computer).  Assumed to be in host encoding.
******************************************************************************/

STATICforIDL Logical NegativeZeroReal4 (value)
float *value;
{
#if defined(FP1cpu) || defined(FP2cpu)
  return (*((uInt32 *) value) == (uInt32) 0x80000000);
#endif
#if defined(FP3cpu) || defined(FP4cpu)
  /****************************************************************************
  * On VAXes and DEC Alphas running OpenVMS/POSIXshell we're only interested
  * in the sign bit and exponent.
  ****************************************************************************/
  return ((*((uInt32 *) value) & (uInt32) 0x0000FF80) == (uInt32) 0x00008000);
#endif
}

/******************************************************************************
* NegativeZeroReal8.
*   Checks for -0.0 (on any type computer).  Assumed to be in host encoding.
******************************************************************************/

STATICforIDL Logical NegativeZeroReal8 (value)
double *value;
{
#if defined(FP1cpu)
  return ((*((uInt32 *) value) == (uInt32) 0x80000000) &&
	  (*((uInt32 *) value+1) == (uInt32) 0x00000000));
#endif
#if defined(FP2cpu)
  return ((*((uInt32 *) value) == (uInt32) 0x00000000) &&
	  (*((uInt32 *) value+1) == (uInt32) 0x80000000));
#endif
#if defined(FP3cpu)
  /****************************************************************************
  * On VAXes and DEC Alphas running OpenVMS/POSIXshell in D_FLOAT mode we're
  * only interested in the sign bit and exponent (which are in the first
  * longword [32-bit]).
  ****************************************************************************/
  return ((*((uInt32 *) value) & (uInt32) 0x0000FF80) == (uInt32) 0x00008000);
#endif
#if defined(FP4cpu)
  /****************************************************************************
  * On DEC Alphas running OpenVMS/POSIXshell in G_FLOAT mode we're only
  * interested in the sign bit and exponent (which are in the first longword
  * [32-bit]).
  ****************************************************************************/
  return ((*((uInt32 *) value) & (uInt32) 0x0000FFF0) == (uInt32) 0x00008000);
#endif
}

/******************************************************************************
* StripTrailingBlanks.
******************************************************************************/

STATICforIDL void StripTrailingBlanks (string)
char *string;
{
  int i;
  for (i = strlen(string) - 1; i >= 0 && string[i] == ' '; i--)
     string[i] = NUL;
  return;
}

/******************************************************************************
* Uppercase.
*   Convert string to uppercase.
******************************************************************************/

STATICforIDL void Uppercase (string)
char *string;
{
  int i;
  for (i = 0; string[i] != NUL; i++) string[i] = ToUpperChr(string[i]);
  return;
}

/******************************************************************************
* Lowercase.
*   Convert string to lowercase.
******************************************************************************/

STATICforIDL void Lowercase (string)
char *string;
{
  int i;
  for (i = 0; string[i] != NUL; i++) string[i] = ToLowerChr(string[i]); 
  return;
}

/******************************************************************************
* SetBit32.
******************************************************************************/

STATICforIDL void SetBit32 (value, bit)
Int32 *value;
int bit;
{
  *value = *value | (1 << bit);
  return;
}

/******************************************************************************
* ClearBit32.
******************************************************************************/

STATICforIDL void ClearBit32 (value, bit)
Int32 *value;
int bit;
{
  *value = *value & ~(1 << bit);
  return;
}

/******************************************************************************
* FindCDF.
*    Tries various extensions on the specified CDF path to see if the CDF
* exists.  The extensions tried are those which should be present on the
* various platforms plus the extensions which might be generated by a CD-ROM
* driver.  Finally, the pathname is tried without an extension being added
* in case the CDF had been renamed with a different extension or no extension.
******************************************************************************/

STATICforIDL CDFstatus FindCDF (path, no_append, upper, version)
char *path;             /* Base pathname. */
Logical *no_append;     /* Should extensions/version numbers be appended? */
Logical *upper;         /* Should extensions be upper case? */
Logical *version;       /* Should a version number of `;1' be appended? */
{
  char pathT[DU_MAX_PATH_LEN+1];

  strcpyX (pathT, path, DU_MAX_PATH_LEN);
  strcatX (pathT, ".cdf", DU_MAX_PATH_LEN);
  if (IsReg(pathT)) {
    *no_append = FALSE;
    *upper = FALSE;
    *version = FALSE;
    return CDF_OK;
  }

  strcpyX (pathT, path, DU_MAX_PATH_LEN);
  strcatX (pathT, ".CDF", DU_MAX_PATH_LEN);
  if (IsReg(pathT)) {
    *no_append = FALSE;
    *upper = TRUE;
    *version = FALSE;
    return CDF_OK;
  }

  strcpyX (pathT, path, DU_MAX_PATH_LEN);
  strcatX (pathT, ".cdf;1", DU_MAX_PATH_LEN);
  if (IsReg(pathT)) {
    *no_append = FALSE;
    *upper = FALSE;
    *version = TRUE;
    return CDF_OK;
  }

  strcpyX (pathT, path, DU_MAX_PATH_LEN);
  strcatX (pathT, ".CDF;1", DU_MAX_PATH_LEN);
  if (IsReg(pathT)) {
    *no_append = FALSE;
    *upper = TRUE;
    *version = TRUE;
    return CDF_OK;
  }

  if (IsReg(path)) {
    *no_append = TRUE;
    *upper = FALSE;
    *version = FALSE;
    return CDF_OK;
  }

  return NO_SUCH_CDF;
}

/******************************************************************************
* BuildFilePath.
******************************************************************************/

STATICforIDL void BuildFilePath (fileType, path, no_append, upper, version,
				 varN, cdfVersion, pathX)
int fileType;           /* Type of file. */
char *path;             /* Base pathname. */
Logical no_append;      /* Should extensions/version numbers be appended? */
Logical upper;          /* Should uppercase extensions be appended? */
Logical version;        /* Should a version number of `;1' be appended? */
long varN;              /* Variable number.  N/a if a `cdf' file. */
int cdfVersion;         /* Version of creating CDF library.  N/a if not a
			   variable file. */
char pathX[DU_MAX_PATH_LEN+1];
			/* The expanded path w/ extensions/version numbers. */
{
  ExpandPath (path, pathX);
  if (!no_append) {
    switch (fileType) {
      case CDFt:
	strcatX (pathX, (upper ? ".CDF" : ".cdf"), DU_MAX_PATH_LEN);
	break;
      case Vt:
	strcatX (pathX, (upper ? ".V" : ".v"), DU_MAX_PATH_LEN);
	sprintf (EofS(pathX), (cdfVersion == VERSION_1 ? "%02ld" : "%ld"),
		 (long) (cdfVersion == VERSION_1 ? varN + 1 : varN));
	break;
      case Zt:
	strcatX (pathX, (upper ? ".Z" : ".z"), DU_MAX_PATH_LEN);
	sprintf (EofS(pathX), "%ld", varN);
	break;
    }
    strcatX (pathX, (version ? ";1" : ""), DU_MAX_PATH_LEN);
  }
  return;
}

/******************************************************************************
* NulPad.
*    Pads with NUL characters to the length specified.  Also NUL-terminates
* the string.
******************************************************************************/

STATICforIDL void NulPad (string, length)
char *string;
int length;
{
  int i;
  for (i = strlen(string); i < length; i++) string[i] = NUL;
  string[length] = NUL;
  return;
}

/******************************************************************************
* UpdateMaxRec.
******************************************************************************/

STATICforIDL void UpdateMaxRec (CDF, Var, recNum)
struct cdfSTRUCT *CDF;          /* In: Pointer to CDF. */
struct varSTRUCT *Var;          /* In: Pointer to variable. */
long recNum;                    /* In: Possible new maximum record number. */
{
  Var->maxRec = MAXIMUM (Var->maxRec, recNum);
  if (!Var->zVar) CDF->rMaxRec = MAXIMUM (CDF->rMaxRec, recNum);
  if (CDF->singleFile) {
    Var->sFile.maxWritten = MAXIMUM (Var->sFile.maxWritten, recNum);
  }
  return;
}

/******************************************************************************
* CalcNumDims.
*    Calculates the number of dimensions depending on the current zMode.
******************************************************************************/

STATICforIDL CDFstatus CalcNumDims (CDF, offset, zVar, numDims)
struct cdfSTRUCT *CDF;          /* In: Pointer to CDF. */
Int32 offset;                   /* In: Offset of VDR. */
Logical zVar;                   /* In: TRUE if a real zVariable; FALSE if a
				   real rVariable. */
long *numDims;                  /* Out: Number of dimensions. */
{
  CDFstatus pStatus = CDF_OK;
  if (zVar) {
    Int32 tNumDims;
    if (!sX(ReadVDR(CDF,offset,zVar,zVDR_zNUMDIMS,
		    &tNumDims,VDR_NULL),&pStatus)) return pStatus;
    *numDims = tNumDims;
  }
  else {
    switch (CDF->zMode) {
      case zMODEoff:
      case zMODEon1:
	*numDims = CDF->rNumDims;
	break;
      case zMODEon2: {
	Int32 tDimVarys[CDF_MAX_DIMS]; int dN;
	if (!sX(ReadVDR(CDF,offset,zVar,VDR_DIMVARYS,
			tDimVarys,VDR_NULL),&pStatus)) return pStatus;
	for (dN = 0, *numDims = 0; dN < CDF->rNumDims; dN++) {
	   if (tDimVarys[dN]) (*numDims)++;
	}
	break;
      }
    }
  }
  return pStatus;
}

/******************************************************************************
* CalcDimVarys.
*    Calculates the dimension variances depending on the current zMode.
******************************************************************************/

STATICforIDL CDFstatus CalcDimVarys (CDF, offset, zVar, dimVarys)
struct cdfSTRUCT *CDF;          /* In: Pointer to CDF. */
Int32 offset;                   /* In: Offset of VDR. */
Logical zVar;                   /* In: TRUE if a real zVariable; FALSE if a
				   real rVariable. */
long dimVarys[];                /* Out: Dimension variances. */
{
  CDFstatus pStatus = CDF_OK;
  Int32 tNumDims, tDimVarys[CDF_MAX_DIMS];
  int dN, dX;
  if (!sX(ReadVDR(CDF,offset,zVar,VDR_DIMVARYS,tDimVarys,VDR_NULL),&pStatus))
    return pStatus;
  if (zVar) {
    if (!sX(ReadVDR(CDF,offset,zVar,zVDR_zNUMDIMS,
		    &tNumDims,VDR_NULL),&pStatus)) return pStatus;
  }
  else
    tNumDims = CDF->rNumDims;
  switch (CDF->zMode) {
    case zMODEoff:
    case zMODEon1:
      for (dN = 0; dN < tNumDims; dN++) dimVarys[dN] = tDimVarys[dN];
      break;
    case zMODEon2:
      if (zVar) {
	for (dN = 0; dN < tNumDims; dN++) dimVarys[dN] = tDimVarys[dN];
      }
      else {
	for (dN = 0, dX = 0; dN < tNumDims; dN++)
	   if (tDimVarys[dN]) dimVarys[dX++] = VARY;
      }
      break;
  }
  return pStatus;
}

/******************************************************************************
* CalcDimSizes.
*    Calculates the dimension sizes depending on the current zMode.
******************************************************************************/

STATICforIDL CDFstatus CalcDimSizes (CDF, offset, zVar, dimSizes)
struct cdfSTRUCT *CDF;          /* In: Pointer to CDF. */
Int32 offset;                   /* In: Offset of VDR. */
Logical zVar;                   /* In: TRUE if a true zVariable; FALSE if a
				   true rVariable. */
long dimSizes[];                /* Out: Dimension sizes. */
{
  CDFstatus pStatus = CDF_OK;
  Int32 tNumDims, tDimSizes[CDF_MAX_DIMS];
  int dN, dX;
  if (zVar) {
    if (!sX(ReadVDR(CDF,offset,zVar,zVDR_zNUMDIMS,&tNumDims,
				    zVDR_zDIMSIZES,tDimSizes,
				    VDR_NULL),&pStatus)) return pStatus;
  }
  else {
    tNumDims = CDF->rNumDims;
    for (dN = 0; dN < CDF->rNumDims; dN++) tDimSizes[dN] = CDF->rDimSizes[dN];
  }
  switch (CDF->zMode) {
    case zMODEoff:
    case zMODEon1:
      for (dN = 0; dN < tNumDims; dN++) dimSizes[dN] = tDimSizes[dN];
      break;
    case zMODEon2:
      if (zVar) {
	for (dN = 0; dN < tNumDims; dN++) dimSizes[dN] = tDimSizes[dN];
      }
      else {
	Int32 tDimVarys[CDF_MAX_DIMS];
	if (!sX(ReadVDR(CDF,offset,zVar,VDR_DIMVARYS,
			tDimVarys,VDR_NULL),&pStatus)) return pStatus;
	for (dN = 0, dX = 0; dN < tNumDims; dN++)
	   if (tDimVarys[dN]) dimSizes[dX++] = tDimSizes[dN];
      }
      break;
  }
  return pStatus;
}

/******************************************************************************
* NULterminateMAX.
*    NUL-terminate a string but only if a NUL is not found before the maximum
* length is reached.
******************************************************************************/

STATICforIDL void NULterminateMAX (string, maxLen)
char *string;
size_t maxLen;
{
  int i;
  for (i = 0; i < maxLen; i++)
     if (string[i] == NUL) return;
  string[maxLen] = NUL;
  return;
}

/******************************************************************************
* ClearBytes.
******************************************************************************/

STATICforIDL void ClearBytes (buffer, firstByte, lastByte)
void *buffer;
int firstByte;
int lastByte;
{
  int i;
  for (i = firstByte; i <= lastByte; i++) ((Byte *)buffer)[i] = 0;
  return;
}

/******************************************************************************
* WasteInternalRecord.
******************************************************************************/

STATICforIDL CDFstatus WasteInternalRecord (CDF, wasteOffset, size)
struct cdfSTRUCT *CDF;
Int32 wasteOffset;
Int32 size;
{
  CDFstatus pStatus = CDF_OK;
  struct UIRstruct newUIR, firstUIR, tUIR, nextUIR;
  Int32 tOffset, nextOffset, UIRhead;
  /****************************************************************************
  * Begin initializing UIR.
  ****************************************************************************/
  newUIR.RecordSize = size;
  newUIR.RecordType = UIR_;
  /****************************************************************************
  * Check that the internal record being wasted is big enough for the `next'
  * and `previous' fields.  If not, mark it as wasted but don't place it in
  * the linked list of UIRs.  Note that there will always be enough room for
  * the `size' and `type' fields.
  ****************************************************************************/
  if (size < UIR_BASE_SIZE) {
    if (!sX(WriteUIR(CDF,wasteOffset,UIR_RECORDSIZE,&(newUIR.RecordSize),
				     UIR_RECORDTYPE,&(newUIR.RecordType),
				     UIR_NULL),&pStatus)) return pStatus;
    return pStatus;
  }
  /****************************************************************************
  * Read offset of first UIR.
  ****************************************************************************/
  if (!sX(ReadGDR(CDF,GDR_UIRHEAD,&UIRhead,GDR_NULL),&pStatus)) return pStatus;
  /****************************************************************************
  * Check if no UIRs exist yet.
  ****************************************************************************/
  if (UIRhead == 0) {
    newUIR.NextUIR = 0;
    newUIR.PrevUIR = 0;
    if (!sX(WriteUIR(CDF,wasteOffset,UIR_RECORD,&newUIR,
				     UIR_NULL),&pStatus)) return pStatus;
    UIRhead = wasteOffset;
    if (!sX(WriteGDR(CDF,GDR_UIRHEAD,&UIRhead,
			 GDR_NULL),&pStatus)) return pStatus;
    return pStatus;
  }
  /****************************************************************************
  * At least one UIR exists, check if the new UIR is before the first UIR.
  ****************************************************************************/
  if (wasteOffset < UIRhead) {
    if (!sX(ReadUIR(CDF,UIRhead,UIR_RECORD,&firstUIR,
				UIR_NULL),&pStatus)) return pStatus;
    newUIR.NextUIR = UIRhead;
    newUIR.PrevUIR = 0;
    if (!sX(WriteUIR(CDF,wasteOffset,UIR_RECORD,&newUIR,
				     UIR_NULL),&pStatus)) return pStatus;
    firstUIR.PrevUIR = wasteOffset;
    if (!sX(WriteUIR(CDF,UIRhead,UIR_RECORD,&firstUIR,
				 UIR_NULL),&pStatus)) return pStatus;
    UIRhead = wasteOffset;
    if (!sX(WriteGDR(CDF,GDR_UIRHEAD,&UIRhead,
			 GDR_NULL),&pStatus)) return pStatus;
    return pStatus;
  }
  /****************************************************************************
  * The new UIR is not before the first UIR.  Scan the UIRs to find the point
  * at which it should be inserted.
  ****************************************************************************/
  tOffset = UIRhead;
  if (!sX(ReadUIR(CDF,tOffset,UIR_RECORD,&tUIR,
			      UIR_NULL),&pStatus)) return pStatus;
  while (tUIR.NextUIR != 0) {
    if (wasteOffset < tUIR.NextUIR) {
      nextOffset = tUIR.NextUIR;
      if (!sX(ReadUIR(CDF,nextOffset,UIR_RECORD,&nextUIR,
				     UIR_NULL),&pStatus)) return pStatus;
      newUIR.NextUIR = tUIR.NextUIR;
      newUIR.PrevUIR = tOffset;
      if (!sX(WriteUIR(CDF,wasteOffset,UIR_RECORD,&newUIR,
				       UIR_NULL),&pStatus)) return pStatus;
      tUIR.NextUIR = wasteOffset;
      if (!sX(WriteUIR(CDF,tOffset,UIR_RECORD,&tUIR,
				   UIR_NULL),&pStatus)) return pStatus;
      nextUIR.PrevUIR = wasteOffset;
      if (!sX(WriteUIR(CDF,nextOffset,UIR_RECORD,&nextUIR,
				      UIR_NULL),&pStatus)) return pStatus;
      return pStatus;
    }
    tOffset = tUIR.NextUIR;
    if (!sX(ReadUIR(CDF,tOffset,UIR_RECORD,&tUIR,
				UIR_NULL),&pStatus)) return pStatus;
  }
  /****************************************************************************
  * The new UIR is going to be the last UIR.
  ****************************************************************************/
  newUIR.NextUIR = 0;
  newUIR.PrevUIR = tOffset;
  if (!sX(WriteUIR(CDF,wasteOffset,UIR_RECORD,&newUIR,
				   UIR_NULL),&pStatus)) return pStatus;
  tUIR.NextUIR = wasteOffset;
  if (!sX(WriteUIR(CDF,tOffset,UIR_RECORD,&tUIR,
			       UIR_NULL),&pStatus)) return pStatus;
  return pStatus;
}

/******************************************************************************
* AllocateInternalRecord.
******************************************************************************/

STATICforIDL CDFstatus AllocateInternalRecord (CDF, size, offset)
struct cdfSTRUCT *CDF;          /* In: Pointer to CDF. */
Int32 size;                     /* In: Size of internal record (bytes). */
Int32 *offset;                  /* Out: Offset of allocated internal record. */
{
  CDFstatus pStatus = CDF_OK;
  Int32 sOffset, eOffset, tSize, UIRhead, eof;
  struct UIRstruct sUIR, eUIR;
  /****************************************************************************
  * Read EOF and offset of first UIR from GDR.
  ****************************************************************************/
  if (!sX(ReadGDR(CDF,GDR_UIRHEAD,&UIRhead,
		      GDR_EOF,&eof,
		      GDR_NULL),&pStatus)) return pStatus;
  /****************************************************************************
  * If UIRs exist, try to use one or more of them (if contiguous) for the new
  * internal record.
  ****************************************************************************/
  if (UIRhead != 0) {
    sOffset = UIRhead;
    if (!sX(ReadUIR(CDF,sOffset,UIR_RECORD,&sUIR,
				UIR_NULL),&pStatus)) return pStatus;
    eOffset = sOffset;
    eUIR = sUIR;
    tSize = sUIR.RecordSize;
    for (;;) {
       /***********************************************************************
       * Check if the starting to ending UIRs are the exact size needed.
       ***********************************************************************/
       if (size == tSize) {
	 if (!sX(RemoveUIRs(CDF,sOffset,eOffset),&pStatus)) return pStatus;
	 *offset = sOffset;
	 return pStatus;
       }
       /***********************************************************************
       * Check if the starting to ending UIRs are big enough for the new
       * internal record and for a new UIR to fill the remaining space.
       ***********************************************************************/
       if (size + UIR_BASE_SIZE <= tSize) {
	 if (!sX(RemoveUIRs(CDF,sOffset,eOffset),&pStatus)) return pStatus;
	 if (!sX(WasteInternalRecord(CDF,sOffset+size,
				     tSize-size),&pStatus)) return pStatus;
	 *offset = sOffset;
	 return pStatus;
       }
       /***********************************************************************
       * Check if the end of the UIRs has been reached.
       ***********************************************************************/
       if (eUIR.NextUIR == 0) {
	 if (eOffset + eUIR.RecordSize == eof) {
	   /*******************************************************************
	   * The ending UIR is the last internal record in the CDF.  Check to
	   * see if after allocating the new internal record less than
	   * UIR_BASE_SIZE bytes will remain before the EOF.  If so, waste an
	   * internal record at the location of those bytes so that a UIR is
	   * at the end.
	   *******************************************************************/
	   if (!sX(RemoveUIRs(CDF,sOffset,eOffset),&pStatus)) return pStatus;
	   if (size < tSize) {
	     if (!sX(WasteInternalRecord(CDF,sOffset+size,
					 UIR_BASE_SIZE),&pStatus)) return
								   pStatus;
	     eof = sOffset + size + UIR_BASE_SIZE;
	   }
	   else
	     eof = sOffset + size;
	   *offset = sOffset;
	   if (!sX(WriteGDR(CDF,GDR_EOF,&eof,GDR_NULL),&pStatus)) return
								  pStatus;
	   return pStatus;
	 }
	 else {
	   /*******************************************************************
	   * Non-UIRs follow the ending UIR.  The new internal record will
	   * have to be allocated at the EOF.
	   *******************************************************************/
	   *offset = eof;
	   eof += size;
	   if (!sX(WriteGDR(CDF,GDR_EOF,&eof,GDR_NULL),&pStatus)) return
								  pStatus;
	   return pStatus;
	 }
       }
       /***********************************************************************
       * If the next UIR is contiguous with the ending UIR, make it the ending
       * UIR.  Otherwise, make the next UIR the starting and ending UIRs.
       ***********************************************************************/
       if (eOffset + eUIR.RecordSize == eUIR.NextUIR) {
	 eOffset = eUIR.NextUIR;
	 if (!sX(ReadUIR(CDF,eOffset,UIR_RECORD,&eUIR,
				     UIR_NULL),&pStatus)) return pStatus;
	 tSize += eUIR.RecordSize;
       }
       else {
	 sOffset = eUIR.NextUIR;
	 if (!sX(ReadUIR(CDF,sOffset,UIR_RECORD,&sUIR,
				     UIR_NULL),&pStatus)) return pStatus;
	 eOffset = sOffset;
	 eUIR = sUIR;
	 tSize = sUIR.RecordSize;
       }
    }
  }
  /****************************************************************************
  * No UIRs exist.  The new internal record will have to be allocated at the
  * EOF.
  ****************************************************************************/
  *offset = eof;
  eof += size;
  if (!sX(WriteGDR(CDF,GDR_EOF,&eof,GDR_NULL),&pStatus)) return pStatus;
  return pStatus;
}

/******************************************************************************
* ResizeInternalRecord.
******************************************************************************/

STATICforIDL CDFstatus ResizeInternalRecord (CDF, curSize, curOffset, newSize,
					     newOffset, move, success)
struct cdfSTRUCT *CDF;
Int32 curSize;          /* In: Current size of internal record. */
Int32 curOffset;        /* In: Current offset of internal record. */
Int32 newSize;          /* In: New size of internal record.  This may be
			   smaller or larger than the current size. */
Int32 *newOffset;       /* Out: New offset of internal record.  This variable
			   is not modified if an error occurs or the internal
			   record cannot be extended (when `move' is FALSE). */
Logical move;           /* In: TRUE if the internal record can be moved if
			   necessary. */
Logical *success;       /* Out: TRUE if the internal record was successfully
			   extended (whether or not it had to be moved). */
{
  CDFstatus pStatus = CDF_OK;
  Int32 eof;
  if (newSize > curSize) {
    /**************************************************************************
    * The internal record is growing.  First check if it is the last one in
    * the CDF.
    **************************************************************************/
    if (!sX(ReadGDR(CDF,GDR_EOF,&eof,GDR_NULL),&pStatus)) return pStatus;
    if (curOffset + curSize == eof) {
      /************************************************************************
      * Last internal record.  Simply extend the CDF.
      ************************************************************************/
      *newOffset = curOffset;
      eof += (newSize - curSize);
      if (!sX(WriteGDR(CDF,GDR_EOF,&eof,GDR_NULL),&pStatus)) return pStatus;
      ASSIGNnotNULL (success, TRUE)
      return pStatus;
    }
    else {
      /************************************************************************
      * Not the last internal record.  If the internal record may be moved,
      * first mark it as unused and then allocate a new internal record.
      * Marking it unused first allows the possibility that if will be used
      * as part of the allocated internal record.  If the internal record can
      * not be moved, check if unused records immediately follow.
      ************************************************************************/
      if (move) {
	if (!sX(WasteInternalRecord(CDF,curOffset,curSize),&pStatus))
	  return pStatus;
	if (!sX(AllocateInternalRecord(CDF,newSize,newOffset),&pStatus))
	  return pStatus;
	ASSIGNnotNULL (success, TRUE)
	return pStatus;
      }
      else {
	Int32 sOffset, eOffset, tSize, UIRhead;
	struct UIRstruct sUIR, eUIR;
	/**********************************************************************
	* First check if there are any UIRs in the CDF.  This is done because
	* CDF V2.5.0* (alpha/beta) created UIRs without the next and previous
	* UIR fields and didn't use the `UIRhead' field in the GDR.  Because
	* we don't want to use UIRs in those CDFs (because they are not the
	* same as the current UIRs), this will keep us from doing so (because
	* the `UIRhead' fields will always contain zero if a V2.5.0* CDF).
	**********************************************************************/
	if (!sX(ReadGDR(CDF,GDR_UIRHEAD,&UIRhead,GDR_NULL),&pStatus)) return
								      pStatus;
	if (UIRhead == 0) {
	  ASSIGNnotNULL (success, FALSE)
	  return pStatus;
	}
	/**********************************************************************
	* Read the internal record which immediately follows the internal
	* record being resized.  If it is a UIR make it the starting UIR.
	* ****************************** DANGER ******************************
	* Don't try to read an entire UIR.  First read only the record type
	* field and check if it is UIR_.  Then read the entire UIR.  This is
	* because the next internal record could be smaller than a UIR (or
	* larger but not entirely written yet [eg. a VVR]).
	**********************************************************************/
	sOffset = curOffset + curSize;
	if (!sX(ReadUIR(CDF,sOffset,UIR_RECORDTYPE,&sUIR.RecordType,
				    UIR_NULL),&pStatus)) return pStatus;
	if (sUIR.RecordType != UIR_) {
	  ASSIGNnotNULL (success, FALSE)
	  return pStatus;
	}
	/* Only now can we safely read the rest of the UIR... */
	if (!sX(ReadUIR(CDF,sOffset,UIR_RECORDSIZE,&sUIR.RecordSize,
				    UIR_NEXTUIR,&sUIR.NextUIR,
				    UIR_PREVUIR,&sUIR.PrevUIR,
				    UIR_NULL),&pStatus)) return pStatus;
	eOffset = sOffset;
	eUIR = sUIR;
	tSize = curSize + sUIR.RecordSize;
	for (;;) {
	   /*******************************************************************
	   * Check if the exact amount of available space has been found.
	   *******************************************************************/
	   if (newSize == tSize) {
	     if (!sX(RemoveUIRs(CDF,sOffset,eOffset),&pStatus)) return pStatus;
	     *newOffset = curOffset;
	     ASSIGNnotNULL (success, TRUE)
	     return pStatus;
	   }
	   /*******************************************************************
	   * Check if enough available space has been found to increase the
	   * internal record and then create a new UIR in the remaining space.
	   *******************************************************************/
	   if (newSize + UIR_BASE_SIZE <= tSize) {
	     if (!sX(RemoveUIRs(CDF,sOffset,eOffset),&pStatus)) return pStatus;
	     if (!sX(WasteInternalRecord(CDF,curOffset+newSize,
					 tSize-newSize),&pStatus)) return
								   pStatus;
	     *newOffset = curOffset;
	     ASSIGNnotNULL (success, TRUE)
	     return pStatus;
	   }
	   /*******************************************************************
	   * Check if the end of the UIRs has been reached.
	   *******************************************************************/
	   if (eUIR.NextUIR == 0) {
	     /*****************************************************************
	     * If the ending UIR is at the EOF, then the internal record can
	     * be extended beyond the EOF or up to it with the creation of a
	     * new UIR at the very end.
	     *****************************************************************/
	     if (eOffset + eUIR.RecordSize == eof) {
	       if (!sX(RemoveUIRs(CDF,sOffset,eOffset),&pStatus)) return
								  pStatus;
	       if (newSize < tSize) {
		 if (!sX(WasteInternalRecord(CDF,curOffset+newSize,
					     UIR_BASE_SIZE),&pStatus)) return
								       pStatus;
		 eof = curOffset + newSize + UIR_BASE_SIZE;
	       }
	       else
		 eof = curOffset + newSize;
	       if (!sX(WriteGDR(CDF,GDR_EOF,&eof,GDR_NULL),&pStatus)) return
								      pStatus;
	       *newOffset = curOffset;
	       ASSIGNnotNULL (success, TRUE)
	       return pStatus;
	     }
	     else {
	       ASSIGNnotNULL (success, FALSE)
	       return pStatus;
	     }
	   }
	   /*******************************************************************
	   * If the next UIR is contiguous with the ending UIR, make it the
	   * ending UIR.
	   *******************************************************************/
	   if (eOffset + eUIR.RecordSize == eUIR.NextUIR) {
	     eOffset = eUIR.NextUIR;
	     if (!sX(ReadUIR(CDF,eOffset,UIR_RECORD,&eUIR,
					 UIR_NULL),&pStatus)) return pStatus;
	     tSize += eUIR.RecordSize;
	   }
	   else {
	     ASSIGNnotNULL (success, FALSE)
	     return pStatus;
	   }
	}
      }
    }
  }
  else {
    /**************************************************************************
    * The internal record is shrinking.  Check if it can be shrunk in place
    * and a UIR created to occupy the extra space.  If not, waste it and then
    * allocate a new internal record (if moving it is allowed).
    **************************************************************************/
    if (newSize <= (curSize - UIR_BASE_SIZE)) {
      if (!sX(WasteInternalRecord(CDF,curOffset+newSize,
				  curSize-newSize),&pStatus)) return pStatus;
      *newOffset = curOffset;
      ASSIGNnotNULL (success, TRUE)
    }
    else {
      if (move) {
	if (!sX(WasteInternalRecord(CDF,curOffset,curSize),&pStatus))
	  return pStatus;
	if (!sX(AllocateInternalRecord(CDF,newSize,newOffset),&pStatus))
	  return pStatus;
	ASSIGNnotNULL (success, TRUE)
      }
      else {
	ASSIGNnotNULL (success, FALSE)
      }      
    }
    return pStatus;
  }
}

/******************************************************************************
* RemoveUIRs.
******************************************************************************/

STATICforIDL CDFstatus RemoveUIRs (CDF, sOffset, eOffset)
struct cdfSTRUCT *CDF;          /* In: Pointer to CDF. */
Int32 sOffset;                  /* In: Offset of starting UIR. */
Int32 eOffset;                  /* In: Offset of ending UIR. */
{
  CDFstatus pStatus = CDF_OK;
  struct UIRstruct sUIR, eUIR;
  Int32 UIRhead;
  if (!sX(ReadGDR(CDF,GDR_UIRHEAD,&UIRhead,
		      GDR_NULL),&pStatus)) return pStatus;
  if (!sX(ReadUIR(CDF,sOffset,UIR_RECORD,&sUIR,
			      UIR_NULL),&pStatus)) return pStatus;
  if (!sX(ReadUIR(CDF,eOffset,UIR_RECORD,&eUIR,
			      UIR_NULL),&pStatus)) return pStatus;
  if (UIRhead == sOffset) {
    UIRhead = eUIR.NextUIR;
    if (!sX(WriteGDR(CDF,GDR_UIRHEAD,&UIRhead,
			 GDR_NULL),&pStatus)) return pStatus;
  }
  else {
    struct UIRstruct prevUIR;
    if (!sX(ReadUIR(CDF,sUIR.PrevUIR,UIR_RECORD,&prevUIR,
				     UIR_NULL),&pStatus)) return pStatus;
    prevUIR.NextUIR = eUIR.NextUIR;
    if (!sX(WriteUIR(CDF,sUIR.PrevUIR,UIR_RECORD,&prevUIR,
				      UIR_NULL),&pStatus)) return pStatus;
  }
  if (eUIR.NextUIR != 0) {
    struct UIRstruct nextUIR;
    if (!sX(ReadUIR(CDF,eUIR.NextUIR,UIR_RECORD,&nextUIR,
				     UIR_NULL),&pStatus)) return pStatus;
    nextUIR.PrevUIR = sUIR.PrevUIR;
    if (!sX(WriteUIR(CDF,eUIR.NextUIR,UIR_RECORD,&nextUIR,
				      UIR_NULL),&pStatus)) return pStatus;
  }
  return pStatus;
}

/******************************************************************************
* PriorTo.
******************************************************************************/

STATICforIDL Logical PriorTo (spec, version, release, increment)
char *spec;
Int32 version;
Int32 release;
Int32 increment;
{
  int ver, rel, incr;
  switch (sscanf(spec,"%d.%d.%d",&ver,&rel,&incr)) {
    case 1:
      if (version < ver) return TRUE;
      break;
    case 2:
      if (version < ver) return TRUE;
      if (version == ver && release < rel) return TRUE;
      break;
    case 3:
      if (version < ver) return TRUE;
      if (version == ver && release < rel) return TRUE;
      if (version == ver && release == rel && increment < incr) return TRUE;
      break;
  }
  return FALSE;
}

/******************************************************************************
* ShortenCDR.
******************************************************************************/

STATICforIDL CDFstatus ShortenCDR (CDF)
struct cdfSTRUCT *CDF;
{
  CDFstatus pStatus = CDF_OK;
  Int32 offset, oldRecordSize, newRecordSize, nBytes;
  if (!sX(ReadCDR(CDF,CDR_RECORDSIZE,&oldRecordSize,CDR_NULL),&pStatus))
    return pStatus;
  newRecordSize = CDR_BASE_SIZE + CDF_COPYRIGHT_LEN;
  if (!sX(WriteCDR(CDF,CDR_RECORDSIZE,
		   &newRecordSize,CDR_NULL),&pStatus)) return pStatus;
  offset = CDF->CDRoffset + newRecordSize;
  nBytes = oldRecordSize - newRecordSize;
  if (!sX(WasteInternalRecord(CDF,offset,nBytes),&pStatus)) return pStatus;
  return pStatus;
}

/******************************************************************************
* CorrectScopes.
*    It is assumed that the last ADR offset has already been fixed.
******************************************************************************/

STATICforIDL CDFstatus CorrectScopes (CDF)
struct cdfSTRUCT *CDF;
{
  Int32 tOffset, attrScope;
  CDFstatus pStatus = CDF_OK;
  /****************************************************************************
  * Read the offset of the first ADR from the GDR.
  ****************************************************************************/
  if (!sX(ReadGDR(CDF,GDR_ADRHEAD,&tOffset,GDR_NULL),&pStatus)) return pStatus;
  /****************************************************************************
  * Read the ADRs correcting each assumed scope.
  ****************************************************************************/
  while (tOffset != 0) {
     if (!sX(ReadADR(CDF,tOffset,ADR_SCOPE,&attrScope,ADR_NULL),&pStatus))
       return pStatus;
     switch (attrScope) {
       case GLOBALscopeASSUMED:
	 attrScope = GLOBAL_SCOPE;
	 if (!sX(WriteADR(CDF,tOffset,ADR_SCOPE,
			  &attrScope,ADR_NULL),&pStatus)) return pStatus;
	 break;
       case VARIABLEscopeASSUMED:
	 attrScope = VARIABLE_SCOPE;
	 if (!sX(WriteADR(CDF,tOffset,ADR_SCOPE,
			  &attrScope,ADR_NULL),&pStatus)) return pStatus;
	 break;
     }
     if (!sX(ReadADR(CDF,tOffset,ADR_ADRNEXT,&tOffset,ADR_NULL),&pStatus))
       return pStatus;
  }
  return pStatus;
}

/******************************************************************************
* ShortenVDRs.
*    It is assumed that the last rVDR offset has already been fixed.
******************************************************************************/

STATICforIDL CDFstatus ShortenVDRs (CDF)
struct cdfSTRUCT *CDF;
{
  Int32 vOffset, nextOffset, recordSize, nTailBytes;
  void *tBuffer;
  long tOffset;
  CDFstatus pStatus = CDF_OK;
  int i;
  for (i = 0; i < 2; i++) {
     Logical zVar = (i == 0);
     /*************************************************************************
     * Read the offset of the first rVDR from the GDR.
     *************************************************************************/
     if (!sX(ReadGDR(CDF,BOO(zVar,GDR_zVDRHEAD,GDR_rVDRHEAD),
		     &vOffset,GDR_NULL),&pStatus)) return pStatus;
     /*************************************************************************
     * Read the rVDRs shortening each.
     *************************************************************************/
     while (vOffset != 0) {
       if (!sX(ReadVDR(CDF,vOffset,zVar,
		       VDR_VDRNEXT,&nextOffset,
		       VDR_RECORDSIZE,&recordSize,
		       VDR_NULL),&pStatus)) return pStatus;
       nTailBytes = recordSize - VDR_WASTED_OFFSET - VDR_WASTED_SIZE;
       recordSize -= VDR_WASTED_SIZE;
       if (!sX(WriteVDR(CDF,vOffset,zVar,VDR_RECORDSIZE,
			&recordSize,VDR_NULL),&pStatus)) return pStatus;
       tBuffer = AllocateMemory ((size_t) nTailBytes, NULL);
       if (tBuffer != NULL) {
	 tOffset = vOffset + VDR_WASTED_OFFSET + VDR_WASTED_SIZE;
	 if (!SEEKv(CDF->fp,tOffset,vSEEK_SET)) return CDF_READ_ERROR;
	 if (!READv(tBuffer,(size_t)nTailBytes,1,CDF->fp)) return
							   CDF_READ_ERROR;
	 tOffset = vOffset + VDR_WASTED_OFFSET;
	 if (!SEEKv(CDF->fp,tOffset,vSEEK_SET)) return CDF_WRITE_ERROR;
	 if (!WRITEv(tBuffer,(size_t)nTailBytes,1,CDF->fp)) return
							    CDF_WRITE_ERROR;
	 FreeMemory (tBuffer, NULL);
       }
       else {
	 long oldOffset = vOffset + VDR_WASTED_OFFSET + VDR_WASTED_SIZE,
	      newOffset = vOffset + VDR_WASTED_OFFSET, byteX;
	 Byte tByte;
	 for (byteX = 0; byteX < nTailBytes; byteX++) {
	    if (!SEEKv(CDF->fp,oldOffset,vSEEK_SET)) return CDF_READ_ERROR;
	    if (!READv(&tByte,1,1,CDF->fp)) return CDF_READ_ERROR;
	    if (!SEEKv(CDF->fp,newOffset,vSEEK_SET)) return CDF_WRITE_ERROR;
	    if (!WRITEv(&tByte,1,1,CDF->fp)) return CDF_WRITE_ERROR;
	    oldOffset++;
	    newOffset++;
	 }
       }
       if (!sX(WasteInternalRecord(CDF,vOffset+recordSize,
				   VDR_WASTED_SIZE),&pStatus)) return pStatus;
       vOffset = nextOffset;
     }
  }
  return pStatus;
}

/******************************************************************************
* CorrectEPOCH.
******************************************************************************/

STATICforIDL CDFstatus CorrectEPOCH (CDF)
struct cdfSTRUCT *CDF;
{
  CDFstatus tStatus, pStatus = CDF_OK;
  Int32 dataType, vNum, vOffset, aOffset, eOffset;
  Logical zVar;
  int i;
  /****************************************************************************
  * Search for EPOCH rVariable.
  ****************************************************************************/
  tStatus = FindVarByName (CDF, "EPOCH", &vOffset, &zVar, NULL);
  switch (tStatus) {
    case CDF_OK:
      if (!sX(ReadVDR(CDF,vOffset,zVar,
		      VDR_NUM,&vNum,
		      VDR_DATATYPE,&dataType,
		      VDR_NULL),&pStatus)) return pStatus;
      if (FLOAT8dataType(dataType)) dataType = CDF_EPOCH;
      if (!sX(WriteVDR(CDF,vOffset,zVar,VDR_DATATYPE,
		       &dataType,VDR_NULL),&pStatus)) return pStatus;
      /************************************************************************
      * Search for associated VALIDMIN/VALIDMAX/SCALEMIN/SCALEMAX rEntries.
      ************************************************************************/
      for (i = 0; i < 4; i++) {
	 char aName[8+1];
	 switch (i) {
	   case 0: strcpy (aName, "VALIDMIN"); break;
	   case 1: strcpy (aName, "VALIDMAX"); break;
	   case 2: strcpy (aName, "SCALEMIN"); break;
	   case 3: strcpy (aName, "SCALEMAX"); break;
	 }
	 tStatus = FindAttrByName (CDF,aName,&aOffset);
	 switch (tStatus) {
	   case CDF_OK:
	     tStatus = FindEntryByNumber (CDF, aOffset, zVar, vNum,
					  &eOffset);    /* We can do this since
							   only rVariables will
							   exist. */
	     switch (tStatus) {
	       case CDF_OK:
		 if (!sX(ReadAEDR(CDF,eOffset,AEDR_DATATYPE,
				  &dataType,AEDR_NULL),&pStatus)) return
								  pStatus;
		 if (FLOAT8dataType(dataType)) dataType = CDF_EPOCH;
		 if (!sX(WriteAEDR(CDF,eOffset,AEDR_DATATYPE,
				   &dataType,AEDR_NULL),&pStatus)) return
								   pStatus;
		 break;
	       case NO_SUCH_ENTRY:
		 break;
	       default:
		 return tStatus;
	     }
	     break;
	   case NO_SUCH_ATTR:
	     break;
	   default:
	     return tStatus;
	 }
      }
      break;
    case NO_SUCH_VAR:
      break;
    default:
      return tStatus;
  }
  return pStatus;
}

/******************************************************************************
* DeleteFile.
******************************************************************************/

STATICforIDL void DeleteFile (path)
char *path;
{
  char tPath[DU_MAX_PATH_LEN+1];
  strcpyX (tPath, path, DU_MAX_PATH_LEN);
#if defined(vms)
  strcatX (tPath, ";0", DU_MAX_PATH_LEN);    /* Only most recent is deleted. */
  delete (tPath);
#endif
#if defined(unix) || defined(dos)
  unlink (tPath);
#endif
#if defined(mac) || defined(posixSHELL)
  remove (tPath);
#endif
  return;
}

/******************************************************************************
* AbortAccess.
******************************************************************************/

STATICforIDL void AbortAccess (CDF, deleteCDF, Cur)
struct cdfSTRUCT *CDF;
Logical deleteCDF;
struct CURstruct *Cur;
{
  if (CDF->status != CDF_CLOSED) CloseCDFfiles (CDF, NULL);
  if (deleteCDF) DeleteCDFfiles (CDF);
  FreeCDFid (CDF);
  Cur->cdf = NULL;
  return;
}

/******************************************************************************
* DeleteCDFfiles.
******************************************************************************/

STATICforIDL void DeleteCDFfiles (CDF)
struct cdfSTRUCT *CDF;
{
  char tmpfile[DU_MAX_PATH_LEN+1];
  /**************************************************************************
  * Delete `.cdf' file.
  **************************************************************************/
  DeleteFile (CDF->pathname);
  /**************************************************************************
  * Delete the variable files (if multi-file).  Both rVariable and zVariable
  * files are deleted.
  **************************************************************************/
  if (!CDF->singleFile) {
    int varN;
    for (varN = 0; varN < CDF->NrVars; varN++) {
       BuildFilePath (Vt, CDF->cdfname, CDF->no_append,
		      CDF->upper_case_ext, CDF->version_numbers,
		      varN, VERSION_2, tmpfile);
       DeleteFile (tmpfile);
    }
    for (varN = 0; varN < CDF->NzVars; varN++) {
       BuildFilePath (Zt, CDF->cdfname, CDF->no_append,
		      CDF->upper_case_ext, CDF->version_numbers,
		      varN, VERSION_2, tmpfile);
       DeleteFile (tmpfile);
    }
  }
  return;
}

/******************************************************************************
* DeleteEntry.
******************************************************************************/

STATICforIDL CDFstatus DeleteEntry (CDF, aOffset, eOffset)
struct cdfSTRUCT *CDF;
Int32 aOffset;
Int32 eOffset;
{
  CDFstatus pStatus = CDF_OK;
  struct ADRstruct ADR;
  struct AEDRstruct AEDR, AEDRt;
  Int32 prevEntryOffset;
  Logical zEntry;
  /****************************************************************************
  * Read the ADR and the AEDR being deleted.
  ****************************************************************************/
  if (!sX(ReadADR(CDF,aOffset,ADR_RECORD,
		  &ADR,ADR_NULL),&pStatus)) return pStatus;
  if (!sX(ReadAEDR(CDF,eOffset,AEDR_RECORD,
		   &AEDR,NULL,AEDR_NULL),&pStatus)) return pStatus;
  zEntry = (AEDR.RecordType == AzEDR_);
  /****************************************************************************
  * Remove the AEDR from the list of entries.
  ****************************************************************************/
  if (!sX(FindPrevEntry(CDF,aOffset,eOffset,
			zEntry,&prevEntryOffset),&pStatus)) return pStatus;
  if (prevEntryOffset == 0) {
    /**************************************************************************
    * The first entry on the linked list is being deleted.  Point the ADR to
    * the entry being pointed to by the entry being deleted.
    **************************************************************************/
    if (zEntry)
      ADR.AzEDRhead = AEDR.AEDRnext;
    else
      ADR.AgrEDRhead = AEDR.AEDRnext;
  }
  else {
    /**************************************************************************
    * The entry being deleted is not the first entry on the linked list.  Point
    * the previous entry to the entry pointed to by the entry being deleted.
    **************************************************************************/
    if (!sX(ReadAEDR(CDF,prevEntryOffset,AEDR_RECORD,&AEDRt,NULL,
		     AEDR_NULL),&pStatus)) return pStatus;
    AEDRt.AEDRnext = AEDR.AEDRnext;
    if (!sX(WriteAEDR(CDF,prevEntryOffset,AEDR_RECORD,&AEDRt,NULL,
		      AEDR_NULL),&pStatus)) return pStatus;
  }
  /****************************************************************************
  * Decrement the number of entries and recalculate the maximum entry (if
  * necessary).
  ****************************************************************************/
  if (zEntry)
    ADR.NzEntries--;
  else
    ADR.NgrEntries--;
  if (BOO(zEntry,ADR.MAXzEntry,ADR.MAXgrEntry) == AEDR.Num) {
    Int32 maxEntry = -1, tOffset = BOO(zEntry,ADR.AzEDRhead,ADR.AgrEDRhead);
    while (tOffset != 0) {
      if (!sX(ReadAEDR(CDF,tOffset,AEDR_RECORD,&AEDRt,NULL,
		       AEDR_NULL),&pStatus)) return pStatus;
      maxEntry = MAXIMUM (maxEntry, AEDRt.Num);
      tOffset = AEDRt.AEDRnext;
    }
    if (zEntry)
      ADR.MAXzEntry = maxEntry;
    else
      ADR.MAXgrEntry = maxEntry;
  }
  /****************************************************************************
  * Rewrite the ADR and waste the AEDR (of the entry being deleted).
  ****************************************************************************/
  if (!sX(WriteADR(CDF,aOffset,ADR_RECORD,&ADR,ADR_NULL),&pStatus)) return
								    pStatus;
  if (!sX(WasteInternalRecord(CDF,eOffset,AEDR.RecordSize),&pStatus)) return
								      pStatus;
  return pStatus;
}

/******************************************************************************
* CtoPstr/PtoCstr.
******************************************************************************/

#if defined(MPW_C)
STATICforIDL unsigned char *CtoPstr (string)
char *string;
{
  size_t length = MINIMUM(strlen(string),255);
  if (length > 0) memmove (&string[1], string, length);
  string[0] = (char) length;
  return ((unsigned char *) string);
}
#endif

#if defined(MPW_C)
STATICforIDL char *PtoCstr (string)
unsigned char *string;
{
  size_t length = (size_t) string[0];
  if (length > 0) memmove (string, &string[1], length);
  string[length] = (unsigned char) NUL;
  return ((char *) string);
}
#endif
