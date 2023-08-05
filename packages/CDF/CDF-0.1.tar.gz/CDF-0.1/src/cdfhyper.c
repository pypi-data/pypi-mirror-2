/******************************************************************************
*
*  NSSDC/CDF                                  CDF library hyper functions.
*
*  Version 1.3b, 24-Feb-95, Hughes STX.
*
*  Modification history:
*
*   V1.0  20-May-92, J Love     Original version.  These functions were taken
*                               out of `cdflib.c'.
*   V1.1  16-Sep-92, J Love     CDF V2.3 (shareable/NeXT/zVar).
*   V1.2  22-Nov-93, J Love     CDF 2.4.  New hyper algorithms.
*   V1.3   7-Dec-94, J Love     CDF V2.5.
*   V1.3a  6-Jan-95, J Love	Encode/decode changes.  More cache-residency.
*   V1.3b 24-Feb-95, J Love	Solaris 2.3 IDL i/f.
*
******************************************************************************/

#include "cdflib.h"

/******************************************************************************
* HyperRead.
******************************************************************************/

STATICforIDL CDFstatus HyperRead (CDF, Var, rd, buffer)
struct cdfSTRUCT *CDF;
struct varSTRUCT *Var;
struct rdSTRUCT *rd;
void *buffer;
{
  long nHypRecValues;
  long nHypRecBytes;
  long nHypDimValues[CDF_MAX_DIMS];
  Logical fullPhyRec;
  Logical fullPhyDim[CDF_MAX_DIMS];
  long firstHypRec, lastHypRec;
  long firstPhyRec, lastPhyRec;
  long nPhyRecs, nBytes, nRecs;
  long phyRecN;
  Int32 offset;
  long i;
  Byte *tBuffer;
  CDFstatus pStatus = CDF_OK;
  int dimN, dimNt;
  int firstDim;                 /* Based on majority, the "highest" dimension
				   (changes the slowest in memory/on disk). */
  int doneDim;                  /* When cycling through the dimensions, the
				   dimension at which to stop (the dimension
				   beyond the last). */
  int dimIncr;                  /* How to cycle through the dimensions.  Incr-
				   ementing (+1) for row-major, decrementing
				   (-1) for column-major. */
  Logical contig;
  /****************************************************************************
  * Determine dimension ordering.
  ****************************************************************************/
  if (Var->numDims > 0) {
    firstDim = (int) (CDF->rowMajor ? 0 : Var->numDims - 1);
    doneDim = (int) (CDF->rowMajor ? Var->numDims : -1);
    dimIncr = (CDF->rowMajor ? 1 : -1);
  }
  /****************************************************************************
  * Determine if full physical dimensions can be read.  In order for this to
  * be so for a particular dimension...
  *   1. If the dimension variance is TRUE, then the entire dimension must be
  *      read (the count equal to the size).  If the dimension variance is
  *      FALSE, the count must be equal to one (only reading the single
  *      physical value).
  *   2. For each `lower' dimension having a TRUE variance, the entire
  *      dimension must be read (the count equal to the size).
  *   3. For each `lower' dimension having a FALSE variance, the count must
  *      be equal to one (only reading the single physical dimension).
  * Also determine if full physical records can be read.  If there are one or
  * more dimensions, this depends on whether or not the first dimension can be
  * read with a single physical read.  If there are zero dimensions, then this
  * is always true.
  ****************************************************************************/
  if (Var->numDims > 0) {
    for (dimN = firstDim; dimN != doneDim; dimN += dimIncr) {
       int dimNt;
       fullPhyDim[dimN] = TRUE;
       for (dimNt = dimN; dimNt != doneDim; dimNt += dimIncr)
	  if ((Var->dimVarys[dimNt] &&
	       rd->dimCounts[dimNt] != Var->dimSizes[dimNt]) ||
	      (!Var->dimVarys[dimNt] && rd->dimCounts[dimNt] > 1)) {
	    fullPhyDim[dimN] = FALSE;
	    break;
	  }
    }
    fullPhyRec = fullPhyDim[firstDim];
  }
  else
    fullPhyRec = TRUE;
  /****************************************************************************
  * Determine if only one read is needed.  In order for this to be so...
  *   1. Full physical records must be being read.
  *   2. If the record variance is TRUE, then...
  *        a. the record interval must be one (or a record count of one) so
  *           that there is no skipping of records
  *        b. at least the first record must exist
  *        c. all of the physical records being read must be contiguous (not
  *           always so if single-file)
  *   3. If the record variance is FALSE, then a physical record must exist.
  ****************************************************************************/
  firstHypRec = rd->recNumber;
  lastHypRec = firstHypRec + (rd->recInterval * (rd->recCount - 1));
  firstPhyRec = (Var->recVary ? firstHypRec : 0);
  lastPhyRec = (Var->recVary ? lastHypRec : 0);

  if (!sX(ContiguousRecords(CDF,Var,firstPhyRec,
			    MINIMUM(lastPhyRec,Var->maxRec),
			    &contig),&pStatus)) {
    return pStatus;
  }

  if (fullPhyRec && 
      ((Var->recVary &&
	(rd->recInterval == 1 || rd->recCount == 1) &&
	firstPhyRec <= Var->maxRec && contig)
		||
       (!Var->recVary && Var->maxRec > -1))) {
    offset = RecordByteOffset (CDF, Var, firstPhyRec);
    if (!SEEKv(Var->fp,(long)offset,vSEEK_SET)) return VAR_READ_ERROR;
    nPhyRecs = MINIMUM(lastPhyRec,Var->maxRec) - firstPhyRec + 1;
    nBytes = nPhyRecs * Var->NphyRecBytes;
    if (!READv(buffer,1,(size_t)nBytes,Var->fp)) return VAR_READ_ERROR;
    if (!sX(DECODE(Var->DecodeFunction,buffer,
		   nPhyRecs * Var->NphyRecElems),&pStatus)) return pStatus;
    if (rd->recCount > nPhyRecs) {
      nRecs = rd->recCount - nPhyRecs;
      for (i = 0,
	   tBuffer = (Byte *) buffer + (size_t) (nPhyRecs * Var->NphyRecBytes);
	   i < nRecs; i++, tBuffer += (size_t) Var->NphyRecBytes) {
	 if (Var->recVary) {
	   if (!sX(PadBuffer(CDF,Var,Var->NphyRecValues,tBuffer),&pStatus))
	     return pStatus;
	 }
	 else
	   memmove (tBuffer, buffer, (size_t) Var->NphyRecBytes);
      }
      if (!sX(VIRTUAL_RECORD_DATA,&pStatus)) return pStatus;
    }
    return pStatus;
  }

  /****************************************************************************
  * A single physical read not possible - read one record at a time.  The case
  * where no physical records exist is also handled here.
  ****************************************************************************/

  if (Var->numDims > 0) {
    for (dimN = firstDim; dimN != doneDim; dimN += dimIncr) {
       nHypDimValues[dimN] = 1;
       for (dimNt = dimN + dimIncr; dimNt != doneDim; dimNt += dimIncr)
	  nHypDimValues[dimN] *= rd->dimCounts[dimNt];
    }
    nHypRecValues = nHypDimValues[firstDim] * rd->dimCounts[firstDim];
  }
  else
    nHypRecValues = 1;

  nHypRecBytes = nHypRecValues * Var->NvalueBytes;

  if (Var->recVary) {
    /**************************************************************************
    * A TRUE record variance.  Read each physical record (or use pad value if
    * record does not exist).
    **************************************************************************/
    for (i = 0, phyRecN = rd->recNumber, tBuffer = buffer;
	 i < rd->recCount;
	 i++, phyRecN += rd->recInterval, tBuffer += (size_t) nHypRecBytes) {
       if (phyRecN <= Var->maxRec) {
	 /*********************************************************************
	 * Physical record exists.
	 *********************************************************************/
	 offset = RecordByteOffset (CDF, Var, phyRecN);
	 if (fullPhyRec) {
	   /*******************************************************************
	   * The full physical record is being read, use one physical read.
	   *******************************************************************/
	   if (!SEEKv(Var->fp,(long)offset,vSEEK_SET)) return VAR_READ_ERROR;
	   if (!READv(tBuffer,1,(size_t)Var->NphyRecBytes,Var->fp))
	     return VAR_READ_ERROR;
	   if (!sX(DECODE(Var->DecodeFunction,tBuffer,
			  Var->NphyRecElems),&pStatus)) return pStatus;
	 }
	 else {
	   /*******************************************************************
	   * Less than the full physical record is to be read.
	   *******************************************************************/
	   if (!sX(HyperReadDim(Var->numDims,Var->dimSizes,
				Var->dimVarys,rd->dimIndices,
				rd->dimCounts,rd->dimIntervals,
				nHypDimValues,Var->nPhyDimValues,
				fullPhyDim,firstDim,dimIncr,offset,
				tBuffer,CDF,Var),&pStatus)) return pStatus;
	   if (!sX(DECODE(Var->DecodeFunction,tBuffer,
			  nHypRecValues * Var->NvalueElems),&pStatus)) return
								       pStatus;
	 }
       }
       else {
	 /*********************************************************************
	 * Beyond the last physical record, use pad values.
	 *********************************************************************/
	 if (!sX(PadBuffer(CDF,Var,nHypRecValues,tBuffer),&pStatus)) return
								     pStatus;
	 if (!sX(VIRTUAL_RECORD_DATA,&pStatus)) return pStatus;
      }
    }
  }
  else {
    /**************************************************************************
    * A FALSE record variance.  At most, one physical record will exist.  Any
    * other records asked for must be propagated from the first record (which
    * was either read or filled with pad values).
    **************************************************************************/
    phyRecN = 0;
    if (phyRecN <= Var->maxRec) {
      /************************************************************************
      * A physical record does exist to be read.
      ************************************************************************/
      offset = RecordByteOffset (CDF, Var, phyRecN);
      if (fullPhyRec) {
	/*******************************************************************
	* The full physical record is being read, use one physical read.
	*******************************************************************/
	if (!SEEKv(Var->fp,(long)offset,vSEEK_SET)) return VAR_READ_ERROR;
	if (!READv(buffer,1,(size_t)Var->NphyRecBytes,Var->fp)) return
							        VAR_READ_ERROR;
	if (!sX(DECODE(Var->DecodeFunction,buffer,
		       Var->NphyRecElems),&pStatus)) return pStatus;
      }
      else {
	/*******************************************************************
	* Less than the full physical record is to be read.
	*******************************************************************/
	if (!sX(HyperReadDim(Var->numDims,Var->dimSizes,Var->dimVarys,
			     rd->dimIndices,rd->dimCounts,
			     rd->dimIntervals,nHypDimValues,
			     Var->nPhyDimValues,fullPhyDim,firstDim,
			     dimIncr,offset,buffer,CDF,Var),&pStatus)) return
								       pStatus;
	if (!sX(DECODE(Var->DecodeFunction,buffer,
		       nHypRecValues * Var->NvalueElems),&pStatus)) return
								    pStatus;
      }
    }
    else {
      /************************************************************************
      * No physical records exist.  Use the pad value.
      ************************************************************************/
      if (!sX(PadBuffer(CDF,Var,nHypRecValues,buffer),&pStatus)) return
								 pStatus;
      if (!sX(VIRTUAL_RECORD_DATA,&pStatus)) return pStatus;
    }
    /**************************************************************************
    * Propagate additional hyper records if necessary.
    **************************************************************************/
    if (rd->recCount > 1) {
      for (i = 1, tBuffer = (Byte *) buffer + (size_t) nHypRecBytes;
	   i < rd->recCount; i++, tBuffer += (size_t) nHypRecBytes)
	 memmove (tBuffer, buffer, (size_t) nHypRecBytes);
    }
  }
  return pStatus;
}

/******************************************************************************
* HyperReadDim.  DANGER, DANGER, I'm recursive.
******************************************************************************/

STATICforIDL CDFstatus HyperReadDim (numDims, dimSizes, dimVarys, indices,
				     counts, intervals, nHypDimValues,
				     nPhyDimValues, fullPhyDim, firstDim,
				     dimIncr, offset, buffer, CDF, Var)
long numDims;
long *dimSizes;
long *dimVarys;
long *indices;
long *counts;
long *intervals;
long *nHypDimValues;
long *nPhyDimValues;
Logical *fullPhyDim;
int firstDim;
int dimIncr;
Int32 offset;
void *buffer;
struct cdfSTRUCT *CDF;
struct varSTRUCT *Var;
{
  Int32 tOffset;
  long nBytes, i;
  Byte *tBuffer;
  CDFstatus pStatus = CDF_OK;
  /****************************************************************************
  * What to do depends on the number of dimensions.  Note that this function
  * should never be called with zero dimensions.
  ****************************************************************************/
  switch (numDims) {
    case 1: {
      /************************************************************************
      * One dimension - read the values along the dimension.
      ************************************************************************/
      if (dimVarys[0]) {
	/**********************************************************************
	* Dimension variance of TRUE, no virtual values to deal with - read
	* physical values.
	**********************************************************************/
	if (intervals[0] == 1) {
	  /********************************************************************
	  * A contiguous strip of values.
	  ********************************************************************/
	  nBytes = counts[0] * Var->NvalueBytes;
	  tOffset = offset + (indices[0] * Var->NvalueBytes);
	  if (!SEEKv(Var->fp,(long)tOffset,vSEEK_SET)) return VAR_READ_ERROR;
	  if (!READv(buffer,1,(size_t)nBytes,Var->fp)) return VAR_READ_ERROR;
	}
	else {
	  /********************************************************************
	  * Not contiguous, read one value at a time skipping over unwanted
	  * values.
	  ********************************************************************/
	  tOffset = offset + (indices[0] * Var->NvalueBytes);
	  tBuffer = buffer; 
	  for (i = 0; i < counts[0]; i++) {
	     if (!SEEKv(Var->fp,(long)tOffset,vSEEK_SET)) return
							  VAR_READ_ERROR;
	     if (!READv(tBuffer,1,(size_t)Var->NvalueBytes,Var->fp))
	       return VAR_READ_ERROR;
	     tOffset += (intervals[0] * Var->NvalueBytes);
	     tBuffer += (size_t) Var->NvalueBytes;
	  }
	}
      }
      else {
	/**********************************************************************
	* Dimension variance of FALSE, only one physical value exists.  If the
	* count is greater than one, virtual values will have to be generated.
	**********************************************************************/
	if (!SEEKv(Var->fp,(long)offset,vSEEK_SET)) return VAR_READ_ERROR;
	if (!READv(buffer,1,(size_t)Var->NvalueBytes,Var->fp)) return
							       VAR_READ_ERROR;
	if (counts[0] > 1) {
	  for (i = 1, tBuffer = (Byte *) buffer + (size_t) Var->NvalueBytes;
	       i < counts[0]; i++, tBuffer += (size_t) Var->NvalueBytes)
	     memmove (tBuffer, buffer, (size_t) Var->NvalueBytes);
	}
      }
      break;
    }
    default: {
      /************************************************************************
      * Two or more dimensions.
      ************************************************************************/
      long nPhyDimBytes = nPhyDimValues[firstDim] * Var->NvalueBytes;
      long nHypDimBytes = nHypDimValues[firstDim] * Var->NvalueBytes;
      int nextDim = firstDim + dimIncr;
      if (dimVarys[firstDim]) {
	/**********************************************************************
	* The first dimension's variance is TRUE.  If the interval is one and
	* only a single read is necessary for the "lower" dimension, use a
	* single read.  Otherwise, cycle through that dimension physically
	* reading each subarray below it (skipping subarrays if necessary).
	**********************************************************************/
	if (intervals[firstDim] == 1 && fullPhyDim[nextDim]) {
	  tOffset = offset + (indices[firstDim] * nPhyDimBytes);
	  nBytes = counts[firstDim] * nPhyDimBytes;
	  if (!SEEKv(Var->fp,(long)tOffset,vSEEK_SET)) return VAR_READ_ERROR;
	  if (!READv(buffer,1,(size_t)nBytes,Var->fp)) return VAR_READ_ERROR;
	}
	else {
	  tOffset = offset + (indices[firstDim] * nPhyDimBytes);
	  tBuffer = buffer;
	  for (i = 0; i < counts[firstDim]; i++) {
	     if (fullPhyDim[nextDim]) {
	       if (!SEEKv(Var->fp,(long)tOffset,vSEEK_SET))
		 return VAR_READ_ERROR;
	       if (!READv(tBuffer,1,(size_t)nPhyDimBytes,Var->fp))
		 return VAR_READ_ERROR;
	     }
	     else {
	       int numDimsT = (int) (numDims - 1);
	       int firstDimT = (CDF->rowMajor ? 0 : numDimsT - 1);
	       int passDimT = (CDF->rowMajor ? 1 : 0);
	       if (!sX(HyperReadDim(numDimsT,&dimSizes[passDimT],
				    &dimVarys[passDimT],
				    &indices[passDimT],
				    &counts[passDimT],
				    &intervals[passDimT],
				    &nHypDimValues[passDimT],
				    &nPhyDimValues[passDimT],
				    &fullPhyDim[passDimT],firstDimT,
				    dimIncr,tOffset,tBuffer,CDF,Var),
		       &pStatus)) return pStatus;
	     }
	     tOffset += (intervals[firstDim] * nPhyDimBytes);
	     tBuffer += (size_t) nHypDimBytes;
	  }
	}
      }
      else {
	/**********************************************************************
	* The first dimension's variance is FALSE, physically read the only
	* existing subarray and generate virtual subarrays if necessary.
	**********************************************************************/
	if (fullPhyDim[nextDim]) {
	  if (!SEEKv(Var->fp,(long)offset,vSEEK_SET)) return VAR_READ_ERROR;
	  if (!READv(buffer,1,(size_t)nPhyDimBytes,Var->fp)) return
							     VAR_READ_ERROR;
	}
	else {
	  int numDimsT = (int) (numDims - 1);
	  int firstDimT = (CDF->rowMajor ? 0 : numDimsT - 1);
	  int passDimT = (CDF->rowMajor ? 1 : 0);
	  if (!sX(HyperReadDim(numDimsT,&dimSizes[passDimT],
			       &dimVarys[passDimT],&indices[passDimT],
			       &counts[passDimT],&intervals[passDimT],
			       &nHypDimValues[passDimT],
			       &nPhyDimValues[passDimT],
			       &fullPhyDim[passDimT],firstDimT,
			       dimIncr,offset,buffer,CDF,Var),
		  &pStatus)) return pStatus;
	}
	if (counts[firstDim] > 1) {
	  for (i = 1, tBuffer = (Byte *) buffer + (size_t) nHypDimBytes;
	       i < counts[firstDim]; i++, tBuffer += (size_t) nHypDimBytes)
	     memmove (tBuffer, buffer, (size_t) nHypDimBytes);
	}
      }
      break;
    }
  }
  return pStatus;
}

/******************************************************************************
* HyperWrite.
******************************************************************************/

STATICforIDL CDFstatus HyperWrite (CDF, Var, rd, buffer)
struct cdfSTRUCT *CDF;
struct varSTRUCT *Var;
struct rdSTRUCT *rd;
void *buffer;
{
  long nHypRecValues;
  long nHypRecBytes;
  long nHypDimValues[CDF_MAX_DIMS];
  Logical fullPhyRec;
  Logical fullPhyDim[CDF_MAX_DIMS];
  long firstPhyRec, lastPhyRec;
  long phyRecN, nRecs1st, nRecs2nd;
  Int32 offset;
  long nElems;
  Byte *tBuffer;
  CDFstatus pStatus = CDF_OK;
  int dimN;
  int firstDim;                 /* Based on majority, the "highest" dimension
				   (changes the slowest in memory/on disk). */
  int doneDim;                  /* When cycling through the dimensions, the
				   dimension at which to stop (the dimension
				   beyond the last). */
  int dimIncr;                  /* How to cycle through the dimensions.  Incr-
				   ementing (+1) for row-major, decrementing
				   (-1) for column-major. */
  long i;
  Logical contig;

  /****************************************************************************
  * Determine dimension ordering.
  ****************************************************************************/

  if (Var->numDims > 0) {
    firstDim = (int) (CDF->rowMajor ? 0 : Var->numDims - 1);
    doneDim = (int) (CDF->rowMajor ? Var->numDims : -1);
    dimIncr = (CDF->rowMajor ? 1 : -1);
  }

  /****************************************************************************
  * Determine if full physical dimensions can be written.  In order for this to
  * be so for a particular dimension...
  *   1. If the dimension variance is TRUE, then the entire dimension must be
  *      written (the count equal to the size).  If the dimension variance is
  *      FALSE, the count must be equal to one (only writing the single
  *      physical value).
  *   2. For each `lower' dimension having a TRUE variance, the entire
  *      dimension must be written (the count equal to the size).
  *   3. For each `lower' dimension having a FALSE variance, the count must
  *      be equal to one (only writing the single physical dimension).
  * Also determine if full physical records can be written.  If there are one
  * or more dimensions, this depends on whether or not the first dimension can
  * be written with a single physical write.  If there are zero dimensions,
  * then this is always true.
  ****************************************************************************/

  if (Var->numDims > 0) {
    for (dimN = firstDim; dimN != doneDim; dimN += dimIncr) {
       int dimNt;
       fullPhyDim[dimN] = TRUE;
       for (dimNt = dimN; dimNt != doneDim; dimNt += dimIncr)
	  if ((Var->dimVarys[dimNt] &&
	       rd->dimCounts[dimNt] != Var->dimSizes[dimNt]) ||
	      (!Var->dimVarys[dimNt] && rd->dimCounts[dimNt] > 1)) {
	    fullPhyDim[dimN] = FALSE;
	    break;
	  }
    }
    fullPhyRec = fullPhyDim[firstDim];
  }
  else
    fullPhyRec = TRUE;

  /****************************************************************************
  * Determine if only one write is needed (or maybe two not counting the
  * records being padded).  In order for this to be so...
  *   1. Full physical records must be being written.
  *   2. A record variance of FALSE, or if the record variance is TRUE, then...
  *        a. the record interval must be one (or a record count of one) so
  *           that there is no skipping of records
  *        b. any existing records being overwritten are contiguous (always
  *           true if multi-file, not always true if single-file)
  ****************************************************************************/

  if (fullPhyRec &&
      ((Var->recVary && (rd->recInterval == 1 || rd->recCount == 1)) ||
       (!Var->recVary))) {
    if (Var->recVary) {
      /************************************************************************
      * A record variance of TRUE.
      ************************************************************************/
      firstPhyRec = rd->recNumber;
      lastPhyRec = firstPhyRec + (rd->recInterval * (rd->recCount - 1));
      if (!CDF->singleFile) {
	/**********************************************************************
	* Multi-file CDF.  No need to worry about contiguous records or
	* allocating records.
	**********************************************************************/
	if (firstPhyRec > Var->maxRec + 1) {
	  if (!sX(PadRecords(CDF,Var,Var->maxRec+1,firstPhyRec-1),&pStatus))
	    return pStatus;
	}
	offset = RecordByteOffset (CDF, Var, firstPhyRec);
	if (!SEEKv(Var->fp,(long)offset,vSEEK_SET)) return VAR_WRITE_ERROR;
	nElems = Var->NphyRecElems * rd->recCount;
	if (!sX(WriteVarElems(Var,nElems,buffer),&pStatus)) return pStatus;
	UpdateMaxRec (CDF, Var, lastPhyRec);
	return pStatus;
      }
      else {
	/**********************************************************************
	* Single-file CDF.
	**********************************************************************/
	if (firstPhyRec > Var->sFile.maxAllocated) {
	  /********************************************************************
	  * None of the records to be written are allocated.
	  ********************************************************************/
	  if (!sX(SingleAllocateRecords(CDF,Var,lastPhyRec,FALSE),&pStatus))
	    return pStatus;
	  if (!sX(PadRecords(CDF,Var,Var->sFile.maxWritten+1,
			     firstPhyRec-1),&pStatus)) return pStatus;
	  offset = RecordByteOffset (CDF, Var, firstPhyRec);
	  if (!SEEKv(Var->fp,(long)offset,vSEEK_SET)) return VAR_WRITE_ERROR;
	  nElems = rd->recCount * Var->NphyRecElems;
	  if (!sX(WriteVarElems(Var,nElems,buffer),&pStatus)) return pStatus;
	  UpdateMaxRec (CDF, Var, lastPhyRec);
	  return pStatus;
	}
	else {
	  if (lastPhyRec <= Var->sFile.maxAllocated) {
	    /******************************************************************
	    * All of the records to be written are allocated.
	    ******************************************************************/
	    if (!sX(ContiguousRecords(CDF,Var,firstPhyRec,lastPhyRec,
				      &contig),&pStatus)) return pStatus;
	    if (contig) {
	      offset = RecordByteOffset (CDF, Var, firstPhyRec);
	      if (!SEEKv(Var->fp,(long)offset,vSEEK_SET))
		return VAR_WRITE_ERROR;
	      nElems = rd->recCount * Var->NphyRecElems;
	      if (!sX(WriteVarElems(Var,nElems,buffer),&pStatus)) return
								  pStatus;
	      UpdateMaxRec (CDF, Var, lastPhyRec);
	      return pStatus;
	    }
	  }
	  else {
	    /******************************************************************
	    * Some of the records to be written are allocated.
	    ******************************************************************/
	    if (!sX(ContiguousRecords(CDF,Var,firstPhyRec,
				      Var->sFile.maxAllocated,
				      &contig),&pStatus)) return pStatus;
	    if (contig) {
	      long recNum2nd = Var->sFile.maxAllocated + 1;
	      offset = RecordByteOffset (CDF, Var, firstPhyRec);
	      if (!SEEKv(Var->fp,(long)offset,vSEEK_SET))
		return VAR_WRITE_ERROR;
	      nRecs1st = Var->sFile.maxAllocated - firstPhyRec + 1;
	      nElems = nRecs1st * Var->NphyRecElems;
	      if (!sX(WriteVarElems(Var,nElems,buffer),&pStatus)) return
								  pStatus;
	      if (!sX(SingleAllocateRecords(CDF,Var,lastPhyRec,
					    FALSE),&pStatus)) return pStatus;
	      offset = RecordByteOffset (CDF, Var, recNum2nd);
	      if (!SEEKv(Var->fp,(long)offset,vSEEK_SET))
		return VAR_WRITE_ERROR;
	      nRecs2nd = rd->recCount - nRecs1st;
	      nElems = nRecs2nd * Var->NphyRecElems;
	      tBuffer = (Byte *) buffer +
			(size_t) (nRecs1st * Var->NphyRecBytes);
	      if (!sX(WriteVarElems(Var,nElems,tBuffer),&pStatus)) return
								   pStatus;
	      UpdateMaxRec (CDF, Var, lastPhyRec);
	      return pStatus;
	    }
	  }
	}
      }
    }
    else {
      /************************************************************************
      * A record variance of FALSE.  Only one physical record will ever exist.
      * [Move to last record in buffer in case the record count was greater
      * than one.  This wouldn't make much sense for a variable with a FALSE
      * record variance but one never knows.]
      ************************************************************************/
      phyRecN = 0;
      tBuffer = (Byte *) buffer +
		(size_t) (Var->NphyRecBytes * (rd->recCount - 1));
      if (CDF->singleFile) {
        if (Var->sFile.maxAllocated < phyRecN) {
	  if (!sX(SingleAllocateRecords(CDF,Var,phyRecN,TRUE),&pStatus))
	    return pStatus;
	}
      }
      offset = RecordByteOffset (CDF, Var, phyRecN);
      if (!SEEKv(Var->fp,(long)offset,vSEEK_SET)) return VAR_WRITE_ERROR;
      if (!sX(WriteVarElems(Var,Var->NphyRecElems,tBuffer),&pStatus)) return
								      pStatus;
      UpdateMaxRec (CDF, Var, phyRecN);
      return pStatus;
    }
  }

  /****************************************************************************
  * Only one/two physical writes not possible - will have to write one record
  * at a time.  First calculate size of hyper records.
  ****************************************************************************/

  if (Var->numDims > 0) {
    for (dimN = firstDim; dimN != doneDim; dimN += dimIncr) {
       int dimNt;
       nHypDimValues[dimN] = 1;
       for (dimNt = dimN + dimIncr; dimNt != doneDim; dimNt += dimIncr)
	  nHypDimValues[dimN] *= rd->dimCounts[dimNt];
    }
    nHypRecValues = nHypDimValues[firstDim] * rd->dimCounts[firstDim];
  }
  else
    nHypRecValues = 1;

  nHypRecBytes = nHypRecValues * Var->NvalueBytes;

  /****************************************************************************
  * Make sure that records are allocated at least up to the last record to be
  * written and/or pad records in front of the first record to be written (if
  * necessary).
  ****************************************************************************/

  firstPhyRec = (Var->recVary ? rd->recNumber : 0);
  lastPhyRec = (Var->recVary ?
		rd->recNumber + (rd->recInterval * (rd->recCount - 1)) : 0);

  if (CDF->singleFile) {
    if (lastPhyRec > Var->sFile.maxAllocated) {
      if (!sX(SingleAllocateRecords(CDF,Var,lastPhyRec,
				    (Var->recVary ? FALSE : TRUE)),&pStatus)) {
	return pStatus;
      }
    }
    if (!sX(PadRecords(CDF,Var,Var->sFile.maxWritten+1,
		       firstPhyRec-1),&pStatus)) return pStatus;
    UpdateMaxRec (CDF, Var, firstPhyRec-1);
  }
  else {
    if (firstPhyRec > Var->maxRec + 1) {
      if (!sX(PadRecords(CDF,Var,Var->maxRec+1,firstPhyRec-1),&pStatus))
	return pStatus;
      UpdateMaxRec (CDF, Var, firstPhyRec-1);
    }
  }

  /****************************************************************************
  * Write each physical record (padding in between records if the record
  * interval is greater than one).
  ****************************************************************************/

  if (Var->recVary) {
    /**************************************************************************
    * A TRUE record variance - write each physical record.
    **************************************************************************/
    for (i = 0, phyRecN = firstPhyRec, tBuffer = buffer;
	 i < rd->recCount;
	 i++, phyRecN += rd->recInterval, tBuffer += (size_t) nHypRecBytes) {
       offset = RecordByteOffset (CDF, Var, phyRecN);
       if (fullPhyRec) {
	 /*********************************************************************
	 * The full physical record is being written, use one physical write.
	 *********************************************************************/
	 if (!SEEKv(Var->fp,(long)offset,vSEEK_SET)) return VAR_WRITE_ERROR;
	 if (!sX(WriteVarElems(Var,Var->NphyRecElems,tBuffer),&pStatus))
	   return pStatus;
       }
       else {
	 /*********************************************************************
	 * Less than the full physical record is to be written.  Only pad the
	 * record if it wasn't already written/padded (single-file) or does not
	 * already exist (multi-file).
	 *********************************************************************/
	 if ((CDF->singleFile && phyRecN > Var->sFile.maxWritten) ||
	     (!CDF->singleFile && phyRecN > Var->maxRec)) {
	   if (!sX(PadRecords(CDF,Var,phyRecN,phyRecN),&pStatus)) return
								  pStatus;
	 }
	 if (!sX(HyperWriteDim(Var->numDims,Var->dimSizes,
			       Var->dimVarys,rd->dimIndices,
			       rd->dimCounts,rd->dimIntervals,
			       nHypDimValues,Var->nPhyDimValues,
			       fullPhyDim,firstDim,dimIncr,offset,
			       tBuffer,CDF,Var),&pStatus)) return pStatus;
       }
       UpdateMaxRec (CDF, Var, phyRecN);
       /***********************************************************************
       * Check if records being skipped should be padded.
       ***********************************************************************/
       if (rd->recInterval > 1 && phyRecN != lastPhyRec) {
	 long firstPadRec = phyRecN + 1;
	 long lastPadRec = phyRecN + rd->recInterval - 1;
	 if (CDF->singleFile) {
	   if (lastPadRec > Var->sFile.maxWritten) {
	     if (!sX(PadRecords(CDF,Var,MAXIMUM(firstPadRec,
						Var->sFile.maxWritten+1),
				lastPadRec),&pStatus)) return pStatus;
	     UpdateMaxRec (CDF, Var, lastPadRec);
	   }
	 }
	 else {
	   if (lastPadRec > Var->maxRec) {
	     if (!sX(PadRecords(CDF,Var,MAXIMUM(firstPadRec,Var->maxRec+1),
				lastPadRec),&pStatus)) return pStatus;
	     UpdateMaxRec (CDF, Var, lastPadRec);
	   }
	 }
       }
    }
  }
  else {
    /**************************************************************************
    * A FALSE record variance.  Only one physical record to actually be
    * written.  No need to check if a full physical record can be written
    * since that case would have been handled above (because of the FALSE
    * record variance).  Only pad the record if it does not already exist.
    * If the record count is greater than one, the LAST record in the buffer
    * will be written (as if the records before it had been written but the
    * overwritten by the last one).
    **************************************************************************/
    phyRecN = 0;
    offset = RecordByteOffset (CDF, Var, phyRecN);
    tBuffer = (Byte *) buffer + (size_t) (nHypRecBytes * (rd->recCount - 1));
    if (phyRecN > Var->maxRec) {
      if (!sX(PadRecords(CDF,Var,phyRecN,phyRecN),&pStatus)) return pStatus;
    }
    if (!sX(HyperWriteDim(Var->numDims,Var->dimSizes,Var->dimVarys,
			  rd->dimIndices,rd->dimCounts,
			  rd->dimIntervals,nHypDimValues,
			  Var->nPhyDimValues,fullPhyDim,firstDim,
			  dimIncr,offset,tBuffer,CDF,Var),&pStatus)) return
								     pStatus;
    UpdateMaxRec (CDF, Var, phyRecN);
  }
  return pStatus;
}

/******************************************************************************
* HyperWriteDim.  DANGER, DANGER, I'm recursive.  It is assumed that the
*                 record has already been allocated and padded.
******************************************************************************/

STATICforIDL CDFstatus HyperWriteDim (numDims, dimSizes, dimVarys, indices,
				      counts, intervals, nHypDimValues,
				      nPhyDimValues, fullPhyDim, firstDim,
				      dimIncr, offset, buffer, CDF, Var)
long numDims;
long *dimSizes;
long *dimVarys;
long *indices;
long *counts;
long *intervals;
long *nHypDimValues;
long *nPhyDimValues;
Logical *fullPhyDim;
int firstDim;
int dimIncr;
Int32 offset;
void *buffer;
struct cdfSTRUCT *CDF;
struct varSTRUCT *Var;
{
  Int32 tOffset;
  long i, nElems;
  Byte *tBuffer;
  CDFstatus pStatus = CDF_OK;
  /****************************************************************************
  * What to do depends on the number of dimensions.  Note that this function
  * should never be called with zero dimensions.
  ****************************************************************************/
  switch (numDims) {
    case 1: {
      /************************************************************************
      * One dimension - write the values along the dimension.
      ************************************************************************/
      if (dimVarys[0]) {
	/**********************************************************************
	* Dimension variance of TRUE, there are no virtual values to deal
	* with (skip) - read physical values.
	**********************************************************************/
	if (intervals[0] == 1) {
	  /********************************************************************
	  * A contiguous strip of values.
	  ********************************************************************/
	  nElems = counts[0] * Var->NvalueElems;
	  tOffset = offset + (indices[0] * Var->NvalueBytes);
	  if (!SEEKv(Var->fp,(long)tOffset,vSEEK_SET)) return VAR_WRITE_ERROR;
	  if (!sX(WriteVarElems(Var,nElems,buffer),&pStatus)) return pStatus;
	}
	else {
	  /********************************************************************
	  * Not contiguous, write one value at a time skipping over physical
	  * values not being written.
	  ********************************************************************/
	  tOffset = offset + (indices[0] * Var->NvalueBytes);
	  tBuffer = buffer; 
	  for (i = 0; i < counts[0]; i++) {
	     if (!SEEKv(Var->fp,(long)tOffset,vSEEK_SET))
	       return VAR_WRITE_ERROR;
	     if (!sX(WriteVarElems(Var,Var->NvalueElems,tBuffer),&pStatus))
	       return pStatus;
	     tOffset += (intervals[0] * Var->NvalueBytes);
	     tBuffer += (size_t) Var->NvalueBytes;
	  }
	}
      }
      else {
	/**********************************************************************
	* Dimension variance of FALSE, only one physical value to be written.
	* If the count is greater than one, skip to the last value in the
	* buffer (this is an unlikely situation).
	**********************************************************************/
	tBuffer = (Byte *) buffer +
		  (size_t) (Var->NvalueBytes * (counts[0] - 1));
	if (!SEEKv(Var->fp,(long)offset,vSEEK_SET)) return VAR_WRITE_ERROR;
	if (!sX(WriteVarElems(Var,Var->NvalueElems,tBuffer),&pStatus)) return
								       pStatus;

      }
      break;
    }
    default: {
      /************************************************************************
      * Two or more dimensions.
      ************************************************************************/
      long nPhyDimElems = nPhyDimValues[firstDim] * Var->NvalueElems;
      long nPhyDimBytes = nPhyDimValues[firstDim] * Var->NvalueBytes;
      long nHypDimBytes = nHypDimValues[firstDim] * Var->NvalueBytes;
      int nextDim = firstDim + dimIncr;
      if (dimVarys[firstDim]) {
	/**********************************************************************
	* The first dimension's variance is TRUE.  If the interval is one and
	* only a single write is necessary for the "lower" dimension, use a
	* single write.  Otherwise, cycle through that dimension physically
	* writing each subarray below it (skipping subarrays if necessary).
	**********************************************************************/
	if (intervals[firstDim] == 1 && fullPhyDim[nextDim]) {
	  tOffset = offset + (indices[firstDim] * nPhyDimBytes);
	  nElems = counts[firstDim] * nPhyDimElems;
	  if (!SEEKv(Var->fp,(long)tOffset,vSEEK_SET)) return VAR_WRITE_ERROR;
	  if (!sX(WriteVarElems(Var,nElems,buffer),&pStatus)) return pStatus;
	}
	else {
	  tOffset = offset + (indices[firstDim] * nPhyDimBytes);
	  tBuffer = buffer;
	  for (i = 0; i < counts[firstDim]; i++) {
	     if (fullPhyDim[nextDim]) {
	       if (!SEEKv(Var->fp,(long)tOffset,vSEEK_SET))
		 return VAR_WRITE_ERROR;
	       if (!sX(WriteVarElems(Var,nPhyDimElems,tBuffer),&pStatus))
		 return pStatus;
	     }
	     else {
	       int numDimsT = (int) (numDims - 1);
	       int firstDimT = (CDF->rowMajor ? 0 : numDimsT - 1);
	       int passDimT = (CDF->rowMajor ? 1 : 0);
	       if (!sX(HyperWriteDim(numDimsT,&dimSizes[passDimT],
				     &dimVarys[passDimT],
				     &indices[passDimT],
				     &counts[passDimT],
				     &intervals[passDimT],
				     &nHypDimValues[passDimT],
				     &nPhyDimValues[passDimT],
				     &fullPhyDim[passDimT],
				     firstDimT,dimIncr,tOffset,
				     tBuffer,CDF,Var),&pStatus)) return
								 pStatus;
	     }
	     tOffset += (intervals[firstDim] * nPhyDimBytes);
	     tBuffer += (size_t) nHypDimBytes;
	  }
	}
      }
      else {
	/**********************************************************************
	* The first dimension's variance is FALSE, skip to the last subarray
	* and write the single physical subarray.
	**********************************************************************/
	tBuffer = (Byte *) buffer +
		  (size_t) (nHypDimBytes * (counts[firstDim] - 1));
	if (fullPhyDim[nextDim]) {
	  if (!SEEKv(Var->fp,(long)offset,vSEEK_SET)) return VAR_WRITE_ERROR;
	  if (!sX(WriteVarElems(Var,nPhyDimElems,tBuffer),&pStatus)) return
								     pStatus;
	}
	else {
	  int numDimsT = (int) (numDims - 1);
	  int firstDimT = (CDF->rowMajor ? 0 : numDimsT - 1);
	  int passDimT = (CDF->rowMajor ? 1 : 0);
	  if (!sX(HyperWriteDim(numDimsT,&dimSizes[passDimT],
				&dimVarys[passDimT],
				&indices[passDimT],
				&counts[passDimT],
				&intervals[passDimT],
				&nHypDimValues[passDimT],
				&nPhyDimValues[passDimT],
				&fullPhyDim[passDimT],firstDimT,
				dimIncr,offset,tBuffer,CDF,Var),&pStatus))
								return pStatus;
	}
      }
      break;
    }
  }

  return pStatus;
}



