/******************************************************************************
*
*  NSSDC/CDF                                        CDF `create' operations.
*
*  Version 1.4a, 7-Sep-95, Hughes STX.
*
*  Modification history:
*
*   V1.0  20-May-92, J Love     Original version (was part of `cdflib.c').
*   V1.1  29-Sep-92, J Love     CDF V2.3 (shareable/NeXT/zVar).
*   V1.2  24-Jan-94, J Love     CDF V2.4.  Added readonly mode.
*   V1.3  15-Dec-94, J Love     CDF V2.5.
*   V1.3a  9-Jan-95, J Love	Encode/decode changes.  More cache-residency.
*   V1.3b 24-Feb-95, J Love	Solaris 2.3 IDL i/f.
*   V1.4  21-Mar-95, J Love	POSIX.
*   V1.4a  7-Sep-95, J Love	CDFexport-related changes.  Fixed cleanup when
*				a CDF is aborted.
*
******************************************************************************/

#include "cdflib.h"
#include "cdfrev.h"

/******************************************************************************
* CDFcre.
******************************************************************************/

STATICforIDL CDFstatus CDFcre (Va, Cur)
struct VAstruct *Va;
struct CURstruct *Cur;
{
CDFstatus tStatus, pStatus = CDF_OK;

switch (Va->item) {
  /****************************************************************************
  * CDF_, create a new CDF.
  ****************************************************************************/
  case CDF_: {
    long numDims, *dimSizes;
    char cdfname[CDF_PATHNAME_LEN+1], cdfnameX[DU_MAX_PATH_LEN+1], *CDFname;
    char copyRight[CDF_COPYRIGHT_LEN+1];
    CDFid *id;
    struct cdfSTRUCT *CDF;
    struct CDRstruct CDR;
    struct GDRstruct GDR;
    vFILE *tmpfp;
    int dimN;
#if defined(vms) || defined(dos)
    Logical upper_case_ext = TRUE;
#else /* Unix, POSIX, & Macintosh */
    Logical upper_case_ext = FALSE;
#endif
    Logical version_numbers = FALSE;
    Logical no_append = FALSE;

    /**************************************************************************
    * Get arguments for this operation/item.
    **************************************************************************/

    CDFname = va_arg (Va->ap, char *);
    numDims = va_arg (Va->ap, long);
    dimSizes = va_arg (Va->ap, long *);
    id = va_arg (Va->ap, CDFid *);

    *id = (CDFid) NULL;

    /**************************************************************************
    * Validate arguments.
    **************************************************************************/

#if BUILD_READ_ONLY_DISTRIBUTION
    if (!sX(READ_ONLY_DISTRIBUTION,&pStatus)) return pStatus;
#endif

    if (numDims < 0 || numDims > CDF_MAX_DIMS) return BAD_NUM_DIMS;
    for (dimN = 0; dimN < numDims; dimN++) {
       if (dimSizes[dimN] < 1) return BAD_DIM_SIZE;
    }

    if (strlen(CDFname) > (size_t) CDF_PATHNAME_LEN) {
      if (!sX(CDF_NAME_TRUNC,&pStatus)) return pStatus;
    }
    strcpyX (cdfname, CDFname, CDF_PATHNAME_LEN);

#if STRIP_TRAILING_BLANKS_FROM_CDFPATH
    StripTrailingBlanks (cdfname);
#endif

#if defined(vms) || defined(dos)
    Uppercase (cdfname);
#endif

    if (!ValidCDFname(cdfname)) return BAD_CDF_NAME;

    BuildFilePath (CDFt, cdfname, no_append, upper_case_ext, version_numbers,
		   0L, 0, cdfnameX);

    if (IsReg(cdfnameX)) return CDF_EXISTS;

    /**************************************************************************
    * Create CDF file.
    **************************************************************************/

    tmpfp = V_open (cdfnameX, WRITE_PLUS_a_mode);
    if (tmpfp == NULL) return CDF_CREATE_ERROR;

    /**************************************************************************
    * Allocate/initialize CDF structure.
    **************************************************************************/

    CDF = (struct cdfSTRUCT *) AllocateMemory (sizeof(struct cdfSTRUCT), NULL);
    if (CDF == NULL) {
      V_close (tmpfp, NULL);
      DeleteFile (cdfnameX);
      return BAD_MALLOC;
    }

    CDF->struct_magic_number = CDFid_MAGIC_NUMBER;
    CDF->file_magic_number = V2_MAGIC_NUMBER;
    CDF->CDRoffset = V2_CDR_OFFSET;
    CDF->GDRoffset = -1;		/* Reset below when GDR is written. */
    CDF->readonlyMode = READONLYoff;
    CDF->zMode = zMODEoff;
    CDF->decoding = HOST_DECODING;
    CDF->negToPosFp0mode = NEGtoPOSfp0off;
    CDF->status = CDF_READ_WRITE;
    CDF->fp = tmpfp;
    CDF->pseudo_clock = 0;
    CDF->upper_case_ext = upper_case_ext;
    CDF->version_numbers = version_numbers;
    CDF->no_append = no_append;
    CDF->fakeEPOCH = FALSE;
    CDF->wastedSpace = FALSE;
    CDF->badEOF = FALSE;
    CDF->badTerminatingOffsets = FALSE;
    CDF->assumedScopes = FALSE;
    CDF->NrVars = 0;
    CDF->NzVars = 0;
    CDF->MAXrVars = 0;
    CDF->MAXzVars = 0;
    CDF->rVars = NULL;
    CDF->zVars = NULL;
    CDF->encoding = BOO(DEFAULT_TO_HOST_ENCODING,
			HostEncoding(),NETWORK_ENCODING);
    CDF->rowMajor = DEFAULT_TO_ROW_MAJOR;
    CDF->singleFile = DEFAULT_TO_SINGLE_FILE;
    CDF->rMaxRec = -1;
    CDF->rNumDims = numDims;
    for (dimN = 0; dimN < numDims; dimN++) {
       CDF->rDimSizes[dimN] = dimSizes[dimN];
    }
    CDF->explicitCache = FALSE;
    CDF->nCacheBuffers = NumberOfCacheBuffers (CDF);

    strcpyX (CDF->cdfname, cdfname, CDF_PATHNAME_LEN);
    strcpyX (CDF->pathname, cdfnameX, CDF_PATHNAME_LEN);

    InitCURobjectsStates (CDF);

    /**************************************************************************
    * Write magic numbers.  The same magic number is written twice.
    **************************************************************************/

    if (!Write32(CDF->fp,&(CDF->file_magic_number))) {
      AbortAccess (CDF, TRUE, Cur);
      return CDF_WRITE_ERROR;
    }

    if (!Write32(CDF->fp,&(CDF->file_magic_number))) {
      AbortAccess (CDF, TRUE, Cur);
      return CDF_WRITE_ERROR;
    }

    /**************************************************************************
    * Write CDR.
    **************************************************************************/

    CDR.RecordSize = CDR_BASE_SIZE + CDF_COPYRIGHT_LEN;
    CDR.RecordType = CDR_;
    CDR.GDRoffset = CDF->CDRoffset + CDR.RecordSize;
    CDR.Version = CDF_LIBRARY_VERSION;
    CDR.Release = CDF_LIBRARY_RELEASE;
    CDR.Encoding = CDF->encoding;
    CDR.Flags = 0;
    if (CDF->rowMajor) SetBit32 (&(CDR.Flags), CDR_MAJORITY_BIT);
    if (CDF->singleFile) SetBit32 (&(CDR.Flags), CDR_FORMAT_BIT);
    CDR.rfuA = 0;
    CDR.rfuB = 0;
    CDR.Increment = CDF_LIBRARY_INCREMENT;
    CDR.rfuD = -1;
    CDR.rfuE = -1;

    CDFcopyRight (copyRight);
    NulPad (copyRight, CDF_COPYRIGHT_LEN);

    if (!sX(WriteCDR(CDF,CDR_RECORD,&CDR,copyRight,
			 CDR_NULL),&pStatus)) {
      AbortAccess (CDF, TRUE, Cur);
      return pStatus;
    }

    /**************************************************************************
    * Write GDR.
    **************************************************************************/

    CDF->GDRoffset = CDR.GDRoffset;

    GDR.RecordSize = GDR_BASE_SIZE + (numDims * sizeof(Int32));
    GDR.RecordType = GDR_;
    GDR.rVDRhead = 0;
    GDR.zVDRhead = 0;
    GDR.ADRhead = 0;
    GDR.eof = CDR.GDRoffset + GDR.RecordSize;
    GDR.NrVars = CDF->NrVars;
    GDR.NumAttr = 0;
    GDR.rMaxRec = CDF->rMaxRec;
    GDR.rNumDims = CDF->rNumDims;
    GDR.NzVars = CDF->NzVars;
    GDR.UIRhead = 0;
    GDR.rfuC = 0;
    GDR.rfuD = -1;
    GDR.rfuE = -1;
    for (dimN = 0; dimN < CDF->rNumDims; dimN++) {
       GDR.rDimSizes[dimN] = CDF->rDimSizes[dimN];
    }

    if (!sX(WriteGDR(CDF,GDR_RECORD,&GDR,GDR_NULL),&pStatus)) {
      AbortAccess (CDF, TRUE, Cur);
      return pStatus;
    }

    /**************************************************************************
    * Set number of cache buffers based on the CDF's format.
    **************************************************************************/

    if (!CACHEv(CDF->fp,CDF->nCacheBuffers)) {
      AbortAccess (CDF, TRUE, Cur);
      return BAD_CACHE_SIZE;
    }

    /**************************************************************************
    * Select current CDF and pass back CDFid.
    **************************************************************************/

    Cur->cdf = CDF;
    *id = (CDFid) CDF;

    break;
  }

  /****************************************************************************
  * rVAR_/zVAR_, create a new variable.
  ****************************************************************************/

  case rVAR_:
  case zVAR_: {
    Logical zOp = (Va->item == zVAR_);
    long *numOut, dataType, numElements, zNumDims, *zDimSizes, recVariance,
	 *dimVariances, newVarNum, numDims;
    char *name, Tname[CDF_VAR_NAME_LEN+1], pathnameX[DU_MAX_PATH_LEN+1];
    struct cdfSTRUCT *CDF;
    struct VDRstruct VDR;
    struct varSTRUCT ***vars;
    vFILE *fp;
    Int32 offset, ntlOffset, VDRhead, nVars;
    int dimN, *max;

    /**************************************************************************
    * Get arguments for this operation/item.
    **************************************************************************/

    name = va_arg (Va->ap, char *);
    dataType = va_arg (Va->ap, long);
    numElements = va_arg (Va->ap, long);
    if (zOp) {
      zNumDims = va_arg (Va->ap, long);
      zDimSizes = va_arg (Va->ap, long *);
    }
    recVariance = va_arg (Va->ap, long);
    dimVariances = va_arg (Va->ap, long *);
    numOut = va_arg (Va->ap, long *);

    /**************************************************************************
    * Get current CDF.
    **************************************************************************/

    SelectCDF (Cur->cdf, CDF, NO_CDF_SELECTED)

    /**************************************************************************
    * Read GDR fields.
    **************************************************************************/

    if (!sX(ReadGDR(CDF,BOO(zOp,GDR_zVDRHEAD,GDR_rVDRHEAD),&VDRhead,
			BOO(zOp,GDR_NzVARS,GDR_NrVARS),&nVars,
			GDR_NULL),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }

    /**************************************************************************
    * Validate arguments.
    **************************************************************************/

    if (BADzOP(CDF,!zOp)) return ILLEGAL_IN_zMODE;
    if (!ValidDataType(dataType)) return BAD_DATA_TYPE;
    if (numElements < 1) return BAD_NUM_ELEMS;
    if (!STRINGdataType(dataType) && numElements != 1) return BAD_NUM_ELEMS;
    if (zOp) {
      if (zNumDims < 0 || zNumDims > CDF_MAX_DIMS) return BAD_NUM_DIMS;
      for (dimN = 0; dimN < zNumDims; dimN++)
	 if (zDimSizes[dimN] < 1) return BAD_DIM_SIZE;
    }

    if (strlen(name) > (size_t) CDF_VAR_NAME_LEN) {
      if (!sX(VAR_NAME_TRUNC,&pStatus)) return pStatus;
    }
    strcpyX (Tname, name, CDF_VAR_NAME_LEN);

#if LIMITof64K
    if (TOObigIBMpc(CDFelemSize(dataType)*numElements)) return IBM_PC_OVERFLOW;
#endif

    if (!ValidVarName(Tname)) return BAD_VAR_NAME;

    tStatus = FindVarByName (CDF, Tname, NULL, NULL, NULL);
    switch (tStatus) {
      case NO_SUCH_VAR:
	break;
      case CDF_OK:
	return VAR_EXISTS;
      default:
	AbortAccess (CDF, FALSE, Cur);
	return tStatus;
    }

    newVarNum = nVars;
    nVars++;

#if defined(dos)
    if (!CDF->singleFile && newVarNum > 99) return TOO_MANY_VARS;
#endif

    /**************************************************************************
    * Switch to read-write access if necessary.
    **************************************************************************/

    if (CDF->status != CDF_READ_WRITE) {
      if (!WriteAccess(CDF,Cur,&pStatus)) return pStatus;
    }

    /**************************************************************************
    * Allocate initial/additional pointers to variable data structures.
    **************************************************************************/

    max = BOO(zOp,&(CDF->MAXzVars),&(CDF->MAXrVars));
    vars = BOO(zOp,&(CDF->zVars),&(CDF->rVars));

    if (newVarNum >= *max) {
      int newMaxVars = (int) (VARs_INCREMENT * ((newVarNum/VARs_INCREMENT)+1));
      int varN;
      size_t nBytes = newMaxVars * sizeof(struct varSTRUCT *);
      void *ptr;
      if (*max > 0)
	ptr = (struct varSTRUCT **) ReallocateMemory (*vars, nBytes, NULL);
      else
	ptr = (struct varSTRUCT **) AllocateMemory (nBytes, NULL);
      if (ptr == NULL) return BAD_MALLOC;
      *vars = ptr;
      for (varN = *max; varN < newMaxVars; varN++) (*vars)[varN] = NULL;
      *max = newMaxVars;
    }

    /**************************************************************************
    * Create variable file (if multi-file CDF).
    **************************************************************************/

    if (!CDF->singleFile) {
      BuildFilePath (BOO(zOp,Zt,Vt), CDF->cdfname, CDF->no_append,
		     CDF->upper_case_ext, CDF->version_numbers, newVarNum,
		     VERSION_2, pathnameX);
      fp = V_open (pathnameX, WRITE_PLUS_a_mode);
      if (fp == NULL) {
	if (!sX(CloseLRUvar(CDF),&pStatus)) return pStatus;
	fp = V_open (pathnameX, WRITE_PLUS_a_mode);
	if (fp == NULL) return VAR_CREATE_ERROR;
      }
      if (!CLOSEv(fp,NULL)) {
	DeleteFile (pathnameX);
	return VAR_CREATE_ERROR;
      }
    }

    /**************************************************************************
    * Write rVDR/zVDR.
    **************************************************************************/

    VDR.RecordSize = BOO(zOp,zVDR_BASE_SIZE,rVDR_BASE_SIZE) +
		     BOO(zOp,zNumDims,0)*sizeof(Int32) +          /*DimSizes.*/
		     BOO(zOp,zNumDims,
			     CDF->rNumDims)*sizeof(Int32);	  /*DimVarys.*/
    VDR.RecordType = BOO(zOp,zVDR_,rVDR_);
    VDR.VDRnext = 0;
    VDR.DataType = dataType;
    VDR.MaxRec = -1;
    VDR.VXRhead = 0;
    VDR.VXRtail = 0;
    VDR.Flags = 0;
    ClearBit32 (&(VDR.Flags), VDR_PADVALUE_BIT);
    if (recVariance)
      SetBit32 (&(VDR.Flags), VDR_RECVARY_BIT);
    else
      ClearBit32 (&(VDR.Flags), VDR_RECVARY_BIT);
    VDR.rfuA = 0;
    VDR.rfuB = 0;
    VDR.rfuC = -1;
    VDR.rfuF = -1;
    VDR.NumElems = numElements;
    VDR.Num = newVarNum;
    VDR.rfuD = -1;
    VDR.NextendRecs = 0;
    strcpyX (VDR.Name, Tname, CDF_VAR_NAME_LEN);
    NulPad (VDR.Name, CDF_VAR_NAME_LEN);
    if (zOp) {
      VDR.zNumDims = zNumDims;
      for (dimN = 0; dimN < zNumDims; dimN++)
	 VDR.zDimSizes[dimN] = zDimSizes[dimN];
    }
    for (dimN = 0, numDims = BOO(zOp,zNumDims,CDF->rNumDims);
	 dimN < numDims; dimN++) {
       VDR.DimVarys[dimN] = BOO(dimVariances[dimN],VARY,NOVARY);
    }

    if (!sX(AllocateInternalRecord(CDF,VDR.RecordSize,&offset),&pStatus)) {
      DeleteFile (pathnameX);
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }
    if (!sX(WriteVDR(CDF,offset,zOp,VDR_RECORD,&VDR,NULL,VDR_NULL),&pStatus)) {
      DeleteFile (pathnameX);
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }

    /**************************************************************************
    * Point next-to-last rVDR/zVDR (or GDR) to this rVDR/zVDR.
    **************************************************************************/

    if (newVarNum != 0) {
      if (!sX(FindVarByNumber(CDF,newVarNum-1,&ntlOffset,zOp),&pStatus)) {
	AbortAccess (CDF, FALSE, Cur);
	return pStatus;
      }
      if (!sX(WriteVDR(CDF,ntlOffset,zOp,
		       VDR_VDRNEXT,&offset,VDR_NULL),&pStatus)) {
	AbortAccess (CDF, FALSE, Cur);
	return pStatus;
      }
    }
    else
      VDRhead = offset;

    /**************************************************************************
    * Update GDR fields that may have been modified.
    **************************************************************************/

    if (!sX(WriteGDR(CDF,BOO(zOp,GDR_zVDRHEAD,GDR_rVDRHEAD),&VDRhead,
			 BOO(zOp,GDR_NzVARS,GDR_NrVARS),&nVars,
			 GDR_NULL),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }

    /**************************************************************************
    * If a single-file CDF, increase the cache size.
    **************************************************************************/

    if (CDF->singleFile) {
      int nCacheBuffers = NumberOfCacheBuffers (CDF);
      if (!CACHEv(CDF->fp,nCacheBuffers)) {
	AbortAccess (CDF, FALSE, Cur);
	return BAD_CACHE_SIZE;
      }
      CDF->nCacheBuffers = nCacheBuffers;
    }

    /**************************************************************************
    * Update the appropriate variable count held in memory for efficiency.
    **************************************************************************/

    if (zOp)
      CDF->NzVars = nVars;
    else
      CDF->NrVars = nVars;

    /**************************************************************************
    * Select current variable and determine variable number to be passed back
    * (based on zMode).
    **************************************************************************/

    if (zModeON(CDF)) {
      long varN = CDF->NrVars + newVarNum;
      CDF->CURzVarNum = varN;
      *numOut = varN;
    }
    else {
      if (zOp)
	CDF->CURzVarNum = newVarNum;
      else
	CDF->CURrVarNum = newVarNum;
      *numOut = newVarNum;
    }

    break;
  }

  /****************************************************************************
  * ATTR_, 
  ****************************************************************************/

  case ATTR_: {
    long *attrNumOut, scope;
    char *attrName, truncName[CDF_ATTR_NAME_LEN+1];
    struct cdfSTRUCT *CDF;
    struct ADRstruct ADR;
    Int32 offset, numAttr, ADRhead;
    
    /**************************************************************************
    * Get arguments for this operation/item.
    **************************************************************************/

    attrName = va_arg (Va->ap, char *);
    scope = va_arg (Va->ap, long);
    attrNumOut = va_arg (Va->ap, long *);

    /**************************************************************************
    * Select current CDF.
    **************************************************************************/

    SelectCDF (Cur->cdf, CDF, NO_CDF_SELECTED)

    /**************************************************************************
    * Validate arguments.
    **************************************************************************/

    if (!ValidAttrScope(scope)) return BAD_SCOPE;

    if (strlen(attrName) > (size_t) CDF_ATTR_NAME_LEN) {
      if (!sX(ATTR_NAME_TRUNC,&pStatus)) return pStatus;
    }
    strcpyX (truncName, attrName, CDF_ATTR_NAME_LEN);

    if (!ValidAttrName(truncName)) return BAD_ATTR_NAME;

    tStatus = FindAttrByName (CDF, truncName, NULL);
    switch (tStatus) {
      case NO_SUCH_ATTR:
	break;
      case CDF_OK:
	return ATTR_EXISTS;
      default:
	AbortAccess (CDF, FALSE, Cur);
	return tStatus;
    }

    /**************************************************************************
    * Switch to read-write access if necessary.
    **************************************************************************/
    if (CDF->status != CDF_READ_WRITE) {
      if (!WriteAccess(CDF,Cur,&pStatus)) return pStatus;
    }
    /**************************************************************************
    * Read GDR fields.
    **************************************************************************/

    if (!sX(ReadGDR(CDF,GDR_NUMATTR,&numAttr,
			GDR_ADRHEAD,&ADRhead,
			GDR_NULL),&pStatus)) return pStatus;

    /**************************************************************************
    * Write ADR.
    **************************************************************************/

    ADR.RecordSize = ADR_BASE_SIZE;
    ADR.RecordType = ADR_;
    ADR.ADRnext = 0;
    ADR.AgrEDRhead = 0;
    ADR.Scope = scope;
    ADR.Num = numAttr;
    ADR.NgrEntries = 0;
    ADR.MAXgrEntry = -1;
    ADR.rfuA = 0;
    ADR.AzEDRhead = 0;
    ADR.NzEntries = 0;
    ADR.MAXzEntry = -1;
    ADR.rfuE = -1;
    strcpyX (ADR.Name, truncName, CDF_ATTR_NAME_LEN);
    NulPad (ADR.Name, CDF_ATTR_NAME_LEN);

    if (!sX(AllocateInternalRecord(CDF,ADR.RecordSize,&offset),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }

    if (!sX(WriteADR(CDF,offset,ADR_RECORD,&ADR,ADR_NULL),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }

    /**************************************************************************
    * Point last ADR (or GDR) to this ADR.
    **************************************************************************/

    if (numAttr == 0)
      ADRhead = offset;
    else {
      Int32 lastOffset;
      if (!sX(FindLastAttr(CDF,&lastOffset),&pStatus)) {
	AbortAccess (CDF, FALSE, Cur);
	return pStatus;
      }
      if (!sX(WriteADR(CDF,lastOffset,
		       ADR_ADRNEXT,&offset,ADR_NULL),&pStatus)) {
	AbortAccess (CDF, FALSE, Cur);
	return pStatus;
      }
    }

    /**************************************************************************
    * Update GDR fields.
    **************************************************************************/

    numAttr++;

    if (!sX(WriteGDR(CDF,GDR_NUMATTR,&numAttr,
			 GDR_ADRHEAD,&ADRhead,
			 GDR_NULL),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }

    /**************************************************************************
    * Select current attribute and entry offsets and pass back attribute
    * number.
    **************************************************************************/

    CDF->CURattrOffset = offset;
    CDF->CURgrEntryOffset = RESERVED_ENTRYOFFSET;
    CDF->CURzEntryOffset = RESERVED_ENTRYOFFSET;

    *attrNumOut = ADR.Num;
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
