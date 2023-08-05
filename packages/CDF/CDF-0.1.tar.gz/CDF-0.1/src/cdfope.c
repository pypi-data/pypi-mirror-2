/******************************************************************************
*
*  NSSDC/CDF                                        CDF `open' operations.
*
*  Version 1.3d, 7-Sep-95, Hughes STX.
*
*  Modification history:
*
*   V1.0  20-May-92, J Love     Original version (was part of `cdflib.c').
*   V1.1  29-Sep-92, J Love     CDF V2.3 (shareable/NeXT/zVar).
*   V1.2  25-Jan-94, J Love     CDF V2.4.
*   V1.3  15-Dec-94, J Love     CDF V2.5.
*   V1.3a  9-Jan-95, J Love	Encode/decode changes, etc.
*   V1.3b 24-Feb-95, J Love	Solaris 2.3 IDL i/f.
*   V1.3c  8-May-95, J Love	Only check version/release for FUTURE_CDF.
*   V1.3d  7-Sep-95, J Love	CDFexport-related changes.  Fixed clean up
*				when a CDF is aborted.
*
******************************************************************************/

#include "cdflib.h"
#include "cdfrev.h"

/******************************************************************************
* CDFope.
******************************************************************************/

STATICforIDL CDFstatus CDFope (Va, Cur)
struct VAstruct *Va;
struct CURstruct *Cur;
{
CDFstatus pStatus = CDF_OK;

switch (Va->item) {
  /****************************************************************************
  * CDF_, open an existing CDF.
  ****************************************************************************/
  case CDF_: {
    char *CDFname, cdfname[CDF_PATHNAME_LEN+1], cdfnameX[DU_MAX_PATH_LEN+1];
    vFILE *tmpfp; size_t nBytes; int varN; CDFid *id; struct cdfSTRUCT *CDF;
    Logical upper_case_ext, version_numbers, no_append;
    Int32 file_magic_number, CDRflags, version, release, increment;

    /**************************************************************************
    * Get arguments for this operation/item.
    **************************************************************************/

    CDFname = va_arg (Va->ap, char *);
    id = va_arg (Va->ap, CDFid *);

    *id = (CDFid) NULL;

    /**************************************************************************
    * Validate arguments.
    **************************************************************************/

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

    if (!sX(FindCDF(cdfname,&no_append,
		    &upper_case_ext,
		    &version_numbers),&pStatus)) return pStatus;
				
    /**************************************************************************
    * Open CDF file.
    **************************************************************************/

    BuildFilePath (CDFt, cdfname, no_append, upper_case_ext, version_numbers,
		   0L, 0, cdfnameX);

    tmpfp = V_open (cdfnameX, READ_ONLY_a_mode);
    if (tmpfp == NULL) return CDF_OPEN_ERROR;

    /**************************************************************************
    * Read the magic number to determine what version CDF this is (and if this
    * is actually a CDF).
    **************************************************************************/

    if (!Read32(tmpfp,&file_magic_number)) {
      V_close (tmpfp, NULL);
      return CDF_READ_ERROR;
    }

    switch (file_magic_number) {
      case V1_MAGIC_NUMBER_flip:
	V_close (tmpfp, NULL);
	return ILLEGAL_ON_V1_CDF;
      case V2_MAGIC_NUMBER:
	break;
      default:
	V_close (tmpfp, NULL);
	return NOT_A_CDF;
    }

    /**************************************************************************
    * Allocate and begin initializing CDF structure.
    **************************************************************************/

    CDF = (struct cdfSTRUCT *) AllocateMemory (sizeof(struct cdfSTRUCT), NULL);
    if (CDF == NULL) {
      V_close (tmpfp, NULL);
      return BAD_MALLOC;
    }

    CDF->struct_magic_number = CDFid_MAGIC_NUMBER;
    CDF->file_magic_number = file_magic_number;
    CDF->fp = tmpfp;
    CDF->no_append = no_append;
    CDF->upper_case_ext = upper_case_ext;
    CDF->version_numbers = version_numbers;
    CDF->decoding = HOST_DECODING;
    CDF->readonlyMode = READONLYoff;
    CDF->zMode = zMODEoff;
    CDF->negToPosFp0mode = NEGtoPOSfp0off;
    CDF->status = CDF_READ_ONLY;
    CDF->pseudo_clock = 0;

    strcpyX (CDF->pathname, cdfnameX, CDF_PATHNAME_LEN);
    strcpyX (CDF->cdfname, cdfname, CDF_PATHNAME_LEN);

    CDF->NrVars = 0;	/* These are updated below if the reads are OK... */
    CDF->NzVars = 0;
    CDF->rVars = NULL;
    CDF->zVars = NULL;

    /**************************************************************************
    * Read necessary fields from the CDR and GDR.
    **************************************************************************/

    CDF->CDRoffset = V2_CDR_OFFSET;
    if (!sX(ReadCDR(CDF,CDR_GDROFFSET,&(CDF->GDRoffset),
			CDR_ENCODING,&(CDF->encoding),
			CDR_FLAGS,&CDRflags,
			CDR_VERSION,&version,
			CDR_RELEASE,&release,
			CDR_INCREMENT,&increment,
			CDR_NULL),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }

    if (!sX(ReadGDR(CDF,GDR_NrVARS,&(CDF->NrVars),
			GDR_NzVARS,&(CDF->NzVars),
			GDR_rMAXREC,&(CDF->rMaxRec),
			GDR_rNUMDIMS,&(CDF->rNumDims),
			GDR_rDIMSIZES,CDF->rDimSizes,
			GDR_NULL),&pStatus)) {
      AbortAccess (CDF, FALSE, Cur);
      return pStatus;
    }

    /**************************************************************************
    * Continue initializing CDF structure.
    **************************************************************************/

    CDF->singleFile = SINGLEfileBITset (CDRflags);
    CDF->rowMajor = ROWmajorBITset (CDRflags);
    CDF->fakeEPOCH = PriorTo("2.1.1",version,release,increment);
    CDF->wastedSpace = PriorTo("2.5",version,release,increment);
    CDF->badEOF = PriorTo("2.1",version,release,increment);
    CDF->badTerminatingOffsets = PriorTo("2.1",version,release,increment);
    CDF->assumedScopes = PriorTo("2.5",version,release,increment);

    /**************************************************************************
    * Allocate and initialize variable data structures kept in memory.
    **************************************************************************/

    if (CDF->NrVars > 0) {
      nBytes = (size_t) (CDF->NrVars * sizeof(struct varSTRUCT *));
      CDF->rVars = (struct varSTRUCT **) AllocateMemory (nBytes, NULL);
      if (CDF->rVars == NULL) {
	AbortAccess (CDF, FALSE, Cur);
	return BAD_MALLOC;
      }
      for (varN = 0; varN < CDF->NrVars; varN++) CDF->rVars[varN] = NULL;
      CDF->MAXrVars = (int) CDF->NrVars;
    }
    else {
      CDF->rVars = NULL;
      CDF->MAXrVars = 0;
    }

    if (CDF->NzVars > 0) {
      nBytes = (size_t) (CDF->NzVars * sizeof(struct varSTRUCT *));
      CDF->zVars = (struct varSTRUCT **) AllocateMemory (nBytes, NULL);
      if (CDF->zVars == NULL) {
	AbortAccess (CDF, FALSE, Cur);
	return BAD_MALLOC;
      }
      for (varN = 0; varN < CDF->NzVars; varN++) CDF->zVars[varN] = NULL;
      CDF->MAXzVars = (int) CDF->NzVars;
    }
    else {
      CDF->zVars = NULL;
      CDF->MAXzVars = 0;
    }

    /**************************************************************************
    * If this is a multi-file CDF and a CDF pathname that doesn't require file
    * extensions to be appended was specified (ie. a weird naming convention),
    * close/free the CDF and return an error.  This is because the extensions
    * for the variable files would be known only to the user.  We'd rather not
    * guess.
    **************************************************************************/

    if (!CDF->singleFile && CDF->no_append) {
      AbortAccess (CDF, FALSE, Cur);
      return BAD_CDF_EXTENSION;
    }

    /**************************************************************************
    * Set the cache size for the `.cdf' file.
    **************************************************************************/

    CDF->explicitCache = FALSE;
    CDF->nCacheBuffers = NumberOfCacheBuffers (CDF);

    if (!CACHEv(CDF->fp,CDF->nCacheBuffers)) {
      AbortAccess (CDF, FALSE, Cur);
      return BAD_CACHE_SIZE;
    }

    /**************************************************************************
    * Initialize the current objects/states.
    **************************************************************************/

    InitCURobjectsStates (CDF);

    /**************************************************************************
    * Check if this CDF was created/modified by a CDF distribution in the
    * future.
    **************************************************************************/

    if (version > CDF_LIBRARY_VERSION)
      sX (FUTURE_CDF, &pStatus);
    else
      if (version == CDF_LIBRARY_VERSION && release > CDF_LIBRARY_RELEASE) {
	sX (FUTURE_CDF, &pStatus);
      }

    /**************************************************************************
    * Select the current CDF and pass back the CDF identifier.
    **************************************************************************/

    Cur->cdf = CDF;
    *id = CDF;

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
