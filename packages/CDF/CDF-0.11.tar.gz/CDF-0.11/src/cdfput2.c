/******************************************************************************
*
*  NSSDC/CDF                                    CDF `put' operations, part 2.
*
*  Version 1.3c, 4-Aug-95, Hughes STX.
*
*  Modification history:
*
*   V1.0  20-May-92, J Love     Original version (was part of `cdflib.c').
*   V1.1  16-Sep-92, J Love     CDF V2.3 (shareable/NeXT/zVar).
*   V1.2  24-Jan-94, J Love     CDF V2.4.
*   V1.3   5-Dec-94, J Love     CDF V2.5.
*   V1.3a  6-Jan-95, J Love	Encode/decode changes.  More cache-residency.
*   V1.3b 24-Feb-95, J Love	Solaris 2.3 IDL i/f.
*   V1.3c  4-Aug-95, J Love	CDFexport-related changes.
*
******************************************************************************/

#include "cdflib.h"

/******************************************************************************
* CDFput2.
******************************************************************************/

STATICforIDL CDFstatus CDFput2 (Va, Cur)
struct VAstruct *Va;
struct CURstruct *Cur;
{
CDFstatus tStatus, pStatus = CDF_OK;

switch (Va->item) {
  /****************************************************************************
  * CDF_ENCODING_, 
  *   Can't change if any variables have been written to (including pad
  *   values).  Can't change if any attribute entries have been written.
  ****************************************************************************/

  case CDF_ENCODING_: {
    struct cdfSTRUCT *CDF;
    long actualEncoding;
    long encoding = va_arg (Va->ap, long);
    Logical no;
    SelectCDF (Cur->cdf, CDF, NO_CDF_SELECTED)
    if (!ValidEncoding(encoding,&actualEncoding)) return BAD_ENCODING;
    if (!sX(VerifyNoRecordsWritten(CDF,&no),&pStatus)) return pStatus;
    if (!no) return CANNOT_CHANGE;
    if (!sX(VerifyNoPadsSpecified(CDF,&no),&pStatus)) return pStatus;
    if (!no) return CANNOT_CHANGE;
    if (!sX(VerifyNoEntriesWritten(CDF,&no),&pStatus)) return pStatus;
    if (!no) return CANNOT_CHANGE;
    if (CDF->status != CDF_READ_WRITE) {
      if (!WriteAccess(CDF,Cur,&pStatus)) return pStatus;
    }
    CDF->encoding = actualEncoding;
    /**************************************************************************
    * Update the `encoding' field in the CDR.
    **************************************************************************/
    if (!sX(WriteCDR(CDF,CDR_ENCODING,&(CDF->encoding),CDR_NULL),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    /**************************************************************************
    * Update the initialized variables for the new encoding.
    **************************************************************************/
    if (!sX(UpdateInitializedVars(CDF),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    break;
  }

  /****************************************************************************
  * CDF_MAJORITY_, 
  *   Can't change if any variable values have been written.
  ****************************************************************************/

  case CDF_MAJORITY_: {
    struct cdfSTRUCT *CDF;
    long majority = va_arg (Va->ap,long);
    Logical no; Int32 CDRflags;
    SelectCDF (Cur->cdf, CDF, NO_CDF_SELECTED)
    if (majority != ROW_MAJOR && majority != COL_MAJOR) return BAD_MAJORITY;
    if (!sX(VerifyNoRecordsWritten(CDF,&no),&pStatus)) return pStatus;
    if (!no) return CANNOT_CHANGE;
    if (CDF->status != CDF_READ_WRITE) {
      if (!WriteAccess(CDF,Cur,&pStatus)) return pStatus;
    }
    CDF->rowMajor = ROWmajor(majority);
    /**************************************************************************
    * Update the `flags' field in the CDR.
    **************************************************************************/
    if (!sX(ReadCDR(CDF,CDR_FLAGS,&CDRflags,CDR_NULL),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    if (CDF->rowMajor)
      SetBit32 (&CDRflags, CDR_MAJORITY_BIT);
    else
      ClearBit32 (&CDRflags, CDR_MAJORITY_BIT);
    if (!sX(WriteCDR(CDF,CDR_FLAGS,&CDRflags,CDR_NULL),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    /**************************************************************************
    * Update the initialized variables for the new majority.
    **************************************************************************/
    if (!sX(UpdateInitializedVars(CDF),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    break;
  }

  /****************************************************************************
  * CDF_FORMAT_, 
  *   Can't change if any variables have been created.
  ****************************************************************************/

  case CDF_FORMAT_: {
    struct cdfSTRUCT *CDF;
    long format = va_arg (Va->ap,long);
    int nCacheBuffers; Int32 CDRflags;
    SelectCDF (Cur->cdf, CDF, NO_CDF_SELECTED)
    if (CDF->NrVars > 0) return CANNOT_CHANGE;
    if (CDF->NzVars > 0) return CANNOT_CHANGE;
    if (format != SINGLE_FILE && format != MULTI_FILE) return BAD_FORMAT;
    if (CDF->status != CDF_READ_WRITE) {
      if (!WriteAccess(CDF,Cur,&pStatus)) return pStatus;
    }
    CDF->singleFile = (format == SINGLE_FILE);
    /**************************************************************************
    * Update the `flags' field in the CDR.
    **************************************************************************/
    if (!sX(ReadCDR(CDF,CDR_FLAGS,&CDRflags,CDR_NULL),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    if (CDF->singleFile)
      SetBit32 (&CDRflags, CDR_FORMAT_BIT);
    else
      ClearBit32 (&CDRflags, CDR_FORMAT_BIT);
    if (!sX(WriteCDR(CDF,CDR_FLAGS,&CDRflags,CDR_NULL),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    /**************************************************************************
    * Reset cache size for `.cdf' file.
    **************************************************************************/
    nCacheBuffers = NumberOfCacheBuffers (CDF);
    if (!CACHEv(CDF->fp,nCacheBuffers) == EOF) {
      AbortAccess (CDF, FALSE, Cur);
      return BAD_CACHE_SIZE;
    }
    CDF->nCacheBuffers = nCacheBuffers;
    /**************************************************************************
    * Update the initialized variables for the new format.
    **************************************************************************/
    if (!sX(UpdateInitializedVars(CDF),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    break;
  }

  /****************************************************************************
  * ATTR_NAME_, 
  ****************************************************************************/

  case ATTR_NAME_: {
    struct cdfSTRUCT *CDF;
    char tmpname[CDF_ATTR_NAME_LEN+1];
    char *attrname = va_arg (Va->ap, char *);
    Int32 offsetFound;
    SelectCDF (Cur->cdf, CDF, NO_CDF_SELECTED)
    if (!CURRENTattrSELECTED(CDF)) return NO_ATTR_SELECTED;
    if (strlen(attrname) > (size_t) CDF_ATTR_NAME_LEN) {
      if (!sX(ATTR_NAME_TRUNC,&pStatus)) return pStatus;
    }
    strcpyX (tmpname, attrname, CDF_ATTR_NAME_LEN);
    if (!ValidAttrName(tmpname)) return BAD_ATTR_NAME;
    /**************************************************************************
    * Check that the new attribute name is not already in use.  Don't flag as
    * an error if the new name is the same as the old name (ignoring trailing
    * blanks).  Trailing blanks may be being eliminated.
    **************************************************************************/
    tStatus = FindAttrByName (CDF, tmpname, &offsetFound);
    switch (tStatus) {
      case CDF_OK:
	if (offsetFound != CDF->CURattrOffset) return ATTR_EXISTS;
	break;
      case NO_SUCH_ATTR:
	break;
      default:
	AbortAccess (CDF, FALSE, Cur);
	return tStatus;
    }
    if (CDF->status != CDF_READ_WRITE) {
      if (!WriteAccess(CDF,Cur,&pStatus)) return pStatus;
    }
    NulPad (tmpname, CDF_ATTR_NAME_LEN);
    if (!sX(WriteADR(CDF,CDF->CURattrOffset,
		     ADR_NAME,tmpname,ADR_NULL),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    break;
  }

  /****************************************************************************
  * ATTR_SCOPE_
  ****************************************************************************/

  case ATTR_SCOPE_: {
    struct cdfSTRUCT *CDF;
    Int32 scope = (Int32) va_arg (Va->ap, long);
    SelectCDF (Cur->cdf, CDF, NO_CDF_SELECTED)
    if (!CURRENTattrSELECTED(CDF)) return NO_ATTR_SELECTED;
    if (!ValidAttrScope(scope)) return BAD_SCOPE;
    if (CDF->status != CDF_READ_WRITE) {
      if (!WriteAccess(CDF,Cur,&pStatus)) return pStatus;
    }
    if (!sX(WriteADR(CDF,CDF->CURattrOffset,
		     ADR_SCOPE,&scope,ADR_NULL),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
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
  * gENTRY_DATASPEC_/rENTRY_DATASPEC_/zENTRY_DATASPEC_, change the data
  * specification of an existing entry.  Currently, only the data type can
  * be changed (and must be equivalent).  The number of elements must remain
  * the same.
  ****************************************************************************/

  case rENTRY_DATASPEC_:
  case gENTRY_DATASPEC_:
  case zENTRY_DATASPEC_: {
    int entryType = E3p(Va->item,gENTRY_DATASPEC_,
				 rENTRY_DATASPEC_,
				 zENTRY_DATASPEC_);
    struct cdfSTRUCT *CDF;
    long dataType = va_arg (Va->ap, long);
    long numElems = va_arg (Va->ap, long);
    Int32 dataType32, numElems32, eOffset;
    SelectCDF (Cur->cdf, CDF, NO_CDF_SELECTED)
    if (!CURRENTattrSELECTED(CDF)) return NO_ATTR_SELECTED;
    if (E3(entryType,
	   CDF->CURgrEntryNum,
	   CDF->CURgrEntryNum,
	   CDF->CURzEntryNum) == RESERVED_ENTRYNUM) return NO_ENTRY_SELECTED;
    if (!ValidDataType(dataType)) return BAD_DATA_TYPE;
    if (numElems < 1) return BAD_NUM_ELEMS;
    if (!sX(CheckEntryOp(CDF,entryType,Cur),&pStatus)) return pStatus;
    eOffset = E3(entryType,CDF->CURgrEntryOffset,
			   CDF->CURgrEntryOffset,
			   CDF->CURzEntryOffset);
    if (eOffset == RESERVED_ENTRYOFFSET) return NO_SUCH_ENTRY;
    if (CDF->status != CDF_READ_WRITE) {
      if (!WriteAccess(CDF,Cur,&pStatus)) return pStatus;
    }
    if (!sX(ReadAEDR(CDF,eOffset,AEDR_DATATYPE,&dataType32,
				 AEDR_NUMELEMS,&numElems32,
				 AEDR_NULL),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    if ((!EquivDataTypes(dataType,dataType32)) ||
	 numElems != numElems32) return CANNOT_CHANGE;
    dataType32 = dataType;
    if (!sX(WriteAEDR(CDF,eOffset,AEDR_DATATYPE,
		      &dataType32,AEDR_NULL),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    break;
  }

  /****************************************************************************
  * gENTRY_DATA_/rENTRY_DATA_/zENTRY_DATA_, 
  ****************************************************************************/

  case rENTRY_DATA_:
  case gENTRY_DATA_:
  case zENTRY_DATA_: {
    int entryType = E3p(Va->item,gENTRY_DATA_,rENTRY_DATA_,zENTRY_DATA_);
    struct cdfSTRUCT *CDF;
    struct ADRstruct ADR;
    long entryN;                /* True entry number. */
    Logical zEntry;             /* If true, a AzEDR.  If FALSE, a AgrEDR. */
    int nBytesNew;              /* Size of new entry value. */
    Int32 eOffset;              /* Offset of AEDR. */
    long dataType = va_arg (Va->ap, long);
    long numElems = va_arg (Va->ap, long);
    void *value = va_arg (Va->ap, void *);
    SelectCDF (Cur->cdf, CDF, NO_CDF_SELECTED)
    if (!CURRENTattrSELECTED(CDF)) return NO_ATTR_SELECTED;
    if (E3(entryType,
	   CDF->CURgrEntryNum,
	   CDF->CURgrEntryNum,
	   CDF->CURzEntryNum) == RESERVED_ENTRYNUM) return NO_ENTRY_SELECTED;
    if (!ValidDataType(dataType)) return BAD_DATA_TYPE;
    if (numElems < 1) return BAD_NUM_ELEMS;
    if (!sX(ReadADR(CDF,CDF->CURattrOffset,
		    ADR_RECORD,&ADR,ADR_NULL),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    if (!sX(CheckEntryOp(CDF,entryType,Cur),&pStatus)) return pStatus;
    if (CDF->status != CDF_READ_WRITE) {
      if (!WriteAccess(CDF,Cur,&pStatus)) return pStatus;
    }
    nBytesNew = (int) (CDFelemSize(dataType) * numElems);
    eOffset = E3(entryType,CDF->CURgrEntryOffset,
			   CDF->CURgrEntryOffset,
			   CDF->CURzEntryOffset);
    if (eOffset != RESERVED_ENTRYOFFSET) {
      /************************************************************************
      * The entry already exists.
      ************************************************************************/
      struct AEDRstruct AEDR; int nBytesCur;
      if (!sX(ReadAEDR(CDF,eOffset,AEDR_RECORD,
		       &AEDR,NULL,AEDR_NULL),&pStatus)) {
	AbortAccess (CDF, FALSE, Cur);
	return pStatus;
      }
      nBytesCur = (int) (CDFelemSize(AEDR.DataType) * AEDR.NumElems);
      zEntry = (AEDR.RecordType == AzEDR_);
      if (nBytesNew != nBytesCur) {
	/********************************************************************
	* The size of the new entry value is different than the size of the
	* old entry value.  The AEDR is changing size.
	********************************************************************/
	Int32 prevOffset, newOffset;
	if (!sX(FindPrevEntry(CDF,CDF->CURattrOffset,eOffset,
			      zEntry,&prevOffset),&pStatus)) {
	  AbortAccess (CDF, FALSE, Cur);
	  return pStatus;
	}
	if (!sX(ResizeInternalRecord(CDF,AEDR.RecordSize,eOffset,
				     AEDR_BASE_SIZE+nBytesNew,&newOffset,
				     TRUE,NULL),&pStatus)) {
	  AbortAccess (CDF, FALSE, Cur);
	  return pStatus;
	}
	AEDR.RecordSize = AEDR_BASE_SIZE + nBytesNew;
	AEDR.DataType = dataType;
	AEDR.NumElems = numElems;
	if (!sX(WriteAEDR(CDF,newOffset,AEDR_RECORD,&AEDR,value,
			  AEDR_NULL),&pStatus)) {
	  AbortAccess (CDF, FALSE, Cur);
	  return pStatus;
	}
	switch (entryType) {
	  case gENTRYt:
	  case rENTRYt:
	    CDF->CURgrEntryOffset = newOffset;
	    break;
	  case zENTRYt:
	    CDF->CURzEntryOffset = newOffset;
	    break;
	}
	if (prevOffset == 0) {
	  if (!sX(WriteADR(CDF,CDF->CURattrOffset,
			   BOO(zEntry,ADR_AzEDRHEAD,ADR_AgrEDRHEAD),
			   &newOffset,ADR_NULL),&pStatus)) {
	    AbortAccess (CDF, FALSE, Cur);
	    return pStatus;
	  }
	}
	else {
	  if (!sX(WriteAEDR(CDF,prevOffset,AEDR_AEDRNEXT,
			    &newOffset,AEDR_NULL),&pStatus)) {
	    AbortAccess (CDF, FALSE, Cur);
	    return pStatus;
	  }
	}
      }
      else {
	/********************************************************************
	* The AEDR is not changing size.
	********************************************************************/
	AEDR.DataType = dataType;
	AEDR.NumElems = numElems;
	if (!sX(WriteAEDR(CDF,eOffset,AEDR_RECORD,&AEDR,value,
			  AEDR_NULL),&pStatus)) {
	  AbortAccess (CDF, FALSE, Cur);
	  return pStatus;
	}
      }
    }
    else {
      /************************************************************************
      * The entry does not exist.
      ************************************************************************/
      struct AEDRstruct AEDR;
      Int32 lastOffset;
      zEntry = E3(entryType,FALSE,FALSE,
		  BOO(zModeON(CDF),
		      BOO(CDF->CURzEntryNum < CDF->NrVars,FALSE,TRUE),TRUE));
      entryN = E3(entryType,CDF->CURgrEntryNum,CDF->CURgrEntryNum,
		  BOO(zModeON(CDF),
		      BOO(CDF->CURzEntryNum < CDF->NrVars,
			  CDF->CURzEntryNum,CDF->CURzEntryNum - CDF->NrVars),
		      CDF->CURzEntryNum));
      AEDR.RecordSize = AEDR_BASE_SIZE + nBytesNew;
      AEDR.RecordType = BOO(zEntry,AzEDR_,AgrEDR_);
      AEDR.AEDRnext = 0;
      AEDR.AttrNum = ADR.Num;
      AEDR.DataType = dataType;
      AEDR.Num = entryN;
      AEDR.NumElems = numElems;
      AEDR.rfuA = 0;
      AEDR.rfuB = 0;
      AEDR.rfuC = 0;
      AEDR.rfuD = -1;
      AEDR.rfuE = -1;
      if (!sX(AllocateInternalRecord(CDF,AEDR.RecordSize,&eOffset),&pStatus)) {
	AbortAccess (CDF, FALSE, Cur);
	return pStatus;
      }
      if (!sX(WriteAEDR(CDF,eOffset,AEDR_RECORD,&AEDR,value,
			AEDR_NULL),&pStatus)) {
	AbortAccess (CDF, FALSE, Cur);
	return pStatus;
      }
      switch (entryType) {
	case gENTRYt:
	case rENTRYt:
	  CDF->CURgrEntryOffset = eOffset;
	  break;
	case zENTRYt:
	  CDF->CURzEntryOffset = eOffset;
	  break;
      }
      if (!sX(FindLastEntry(CDF,CDF->CURattrOffset,
			    zEntry,&lastOffset),&pStatus)) {
	AbortAccess (CDF, FALSE, Cur);
	return pStatus;
      }
      if (lastOffset == 0) {
	/********************************************************************
	* This is the first entry (of this type).  The ADR will point to
	* this entry.
	********************************************************************/
	if (zEntry) {
	  ADR.NzEntries = 1;
	  ADR.MAXzEntry = entryN;
	  ADR.AzEDRhead = eOffset;
	}
	else {
	  ADR.NgrEntries = 1;
	  ADR.MAXgrEntry = entryN;
	  ADR.AgrEDRhead = eOffset;
	}
	if (!sX(WriteADR(CDF,CDF->CURattrOffset,
			 ADR_RECORD,&ADR,ADR_NULL),&pStatus)) {
	  AbortAccess (CDF, FALSE, Cur);
	  return pStatus;
	}
      }
      else {
	/********************************************************************
	* Entries already exist (of this type).  The currently last entry
	* will point to this entry.
	********************************************************************/
	if (zEntry) {
	  ADR.NzEntries++;
	  ADR.MAXzEntry = MAXIMUM(ADR.MAXzEntry,entryN);
	}
	else {
	  ADR.NgrEntries++;
	  ADR.MAXgrEntry = MAXIMUM(ADR.MAXgrEntry,entryN);
	}
	if (!sX(WriteADR(CDF,CDF->CURattrOffset,
			 ADR_RECORD,&ADR,ADR_NULL),&pStatus)) {
	  AbortAccess (CDF, FALSE, Cur);
	  return pStatus;
	}
	if (!sX(WriteAEDR(CDF,lastOffset,AEDR_AEDRNEXT,
			  &eOffset,AEDR_NULL),&pStatus)) {
	  AbortAccess (CDF, FALSE, Cur);
	  return pStatus;
	}
      }
    }
    break;
  }
}
return pStatus;
}
