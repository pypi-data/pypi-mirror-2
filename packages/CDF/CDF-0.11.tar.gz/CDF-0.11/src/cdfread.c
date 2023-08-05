/******************************************************************************
*
*  NSSDC/CDF                                        Read from internal record.
*
*  Version 1.3a, 4-Aug-95, Hughes STX.
*
*  Modification history:
*
*   V1.0  30-Nov-94, J Love     Original version.
*   V1.1  30-Jan-95, J Love	`Read32s' now checks count.
*   V1.1a 24-Feb-95, J Love	Solaris 2.3 IDL i/f.
*   V1.2  26-May-95, J Love	CDF V2.4 compatibility mode.  What?
*   V1.3  14-Jun-95, J Love	Recursion!
*   V1.3a  4-Aug-95, J Love	More efficient `Read32' and `Read32s'.
*				CDFexport-related changes.
*
******************************************************************************/

#include "cdflib.h"

/******************************************************************************
* Local macro definitions.
******************************************************************************/

#define CRE CDF_READ_ERROR

/******************************************************************************
* Read32.
******************************************************************************/

STATICforIDL Logical Read32 (fp, value)
vFILE *fp;
Int32 *value;
{
#if defined(NETWORKbyteORDERcpu)
  if (!READv(value,4,1,fp)) return FALSE;
#else
  Int32 temp;
  if (!READv(&temp,4,1,fp)) return FALSE;
  REVERSE4bIO (&temp, value)
#endif
  return TRUE;
}

/******************************************************************************
* Read32s.
******************************************************************************/

STATICforIDL Logical Read32s (fp, buffer, count)
vFILE *fp;
Int32 *buffer;
int count;
{
#if defined(NETWORKbyteORDERcpu)
  if (count < 1) return TRUE;
  if (!READv(buffer,4,count,fp)) return FALSE;
#else
#define MAX_READ32s CDF_MAX_DIMS	/* This must be the maximum of
					   CDF_MAX_DIMS and NUM_VXR_ENTRIES
					   (and for any other uses of
					   `Read32s'). */
  int i; Int32 temp[MAX_READ32s];
  if (count < 1) return TRUE;
  if (!READv(temp,4,count,fp)) return FALSE;
  for (i = 0; i < count; i++) {
     REVERSE4bIO (&temp[i], &buffer[i])
  }
#endif
  return TRUE;
}

/******************************************************************************
* Read CDR.
*   Note that the length of the CDF copyright was decreased in CDF V2.5 (there
* were way too many characters allowed for).  When reading the copyright, only
* CDF_COPYRIGHT_LEN characters will be read.  This will be less than the
* actual number in CDFs prior to CDF V2.4 but is enough to include all of the
* characters that were used.  (The value of CDF_COPYRIGHT_LEN was decreased
* from CDF V2.4 to CDF V2.5.)
******************************************************************************/

#if defined(STDARG)
STATICforIDL CDFstatus ReadCDR (struct cdfSTRUCT *CDF, ...)
#else
STATICforIDL CDFstatus ReadCDR (va_alist)
va_dcl
#endif
{
  va_list ap;
  CDFstatus pStatus = CDF_OK;
#if defined(STDARG)
  va_start (ap, CDF);
#else
  struct cdfSTRUCT *CDF;
  VA_START (ap);
  CDF = va_arg (ap, struct cdfSTRUCT *);
#endif
  for (;;) {
     int field = va_arg (ap, int);
     switch (field) {
       case CDR_NULL:
	 va_end (ap);
	 return pStatus;
       case CDR_RECORD: {
	 struct CDRstruct *CDR = va_arg (ap, struct CDRstruct *);
	 void *copyRight = va_arg (ap, char *);
	 if (!SEEKv(CDF->fp,(long)CDF->CDRoffset,vSEEK_SET)) return CRE;
	 if (!Read32(CDF->fp,&(CDR->RecordSize))) return CRE;
	 if (!Read32(CDF->fp,&(CDR->RecordType))) return CRE;
	 if (!Read32(CDF->fp,&(CDR->GDRoffset))) return CRE;
	 if (!Read32(CDF->fp,&(CDR->Version))) return CRE;
	 if (!Read32(CDF->fp,&(CDR->Release))) return CRE;
	 if (!Read32(CDF->fp,&(CDR->Encoding))) return CRE;
	 if (!Read32(CDF->fp,&(CDR->Flags))) return CRE;
	 if (!Read32(CDF->fp,&(CDR->rfuA))) return CRE;
	 if (!Read32(CDF->fp,&(CDR->rfuB))) return CRE;
	 if (!Read32(CDF->fp,&(CDR->Increment))) return CRE;
	 if (!Read32(CDF->fp,&(CDR->rfuD))) return CRE;
	 if (!Read32(CDF->fp,&(CDR->rfuE))) return CRE;
	 if (copyRight != NULL) {
	   if (!READv(copyRight,CDF_COPYRIGHT_LEN,1,CDF->fp)) return CRE;
	   NulPad (copyRight, CDF_COPYRIGHT_LEN);
	 }
	 break;
       }
       case CDR_COPYRIGHT: {
	 void *copyRight = va_arg (ap, char *);
	 long tOffset = CDF->CDRoffset + CDR_COPYRIGHT_OFFSET;
	 if (!SEEKv(CDF->fp,tOffset,vSEEK_SET)) return CRE;
	 if (!READv(copyRight,CDF_COPYRIGHT_LEN,1,CDF->fp)) return CRE;
	 NulPad (copyRight, CDF_COPYRIGHT_LEN);
	 break;
       }
       default: {
	 Int32 *buffer = va_arg (ap, Int32 *);
	 long tOffset = CDF->CDRoffset;
	 switch (field) {
	   case CDR_RECORDSIZE: tOffset += CDR_RECORDSIZE_OFFSET; break;
	   case CDR_RECORDTYPE: tOffset += CDR_RECORDTYPE_OFFSET; break;
	   case CDR_GDROFFSET: tOffset += CDR_GDROFFSET_OFFSET; break;
	   case CDR_VERSION: tOffset += CDR_VERSION_OFFSET; break;
	   case CDR_RELEASE: tOffset += CDR_RELEASE_OFFSET; break;
	   case CDR_ENCODING: tOffset += CDR_ENCODING_OFFSET; break;
	   case CDR_FLAGS: tOffset += CDR_FLAGS_OFFSET; break;
	   case CDR_INCREMENT: tOffset += CDR_INCREMENT_OFFSET; break;
	   default: return CDF_INTERNAL_ERROR;
	 }
	 if (!SEEKv(CDF->fp,tOffset,vSEEK_SET)) return CRE;
	 if (!Read32(CDF->fp,buffer)) return CRE;
	 break;
       }
     }
  }
}

/******************************************************************************
* Read GDR.
******************************************************************************/

#if defined(STDARG)
STATICforIDL CDFstatus ReadGDR (struct cdfSTRUCT *CDF, ...)
#else
STATICforIDL CDFstatus ReadGDR (va_alist)
va_dcl
#endif
{
  va_list ap;
  CDFstatus pStatus = CDF_OK;
#if defined(STDARG)
  va_start (ap, CDF);
#else
  struct cdfSTRUCT *CDF;
  VA_START (ap);
  CDF = va_arg (ap, struct cdfSTRUCT *);
#endif
  for (;;) {
     int field = va_arg (ap, int);
     switch (field) {
       case GDR_NULL:
	 va_end (ap);
	 return pStatus;
       case GDR_RECORD: {
	 struct GDRstruct *GDR = va_arg (ap, struct GDRstruct *);
	 if (!SEEKv(CDF->fp,(long)CDF->GDRoffset,vSEEK_SET)) return CRE;
	 if (!Read32(CDF->fp,&(GDR->RecordSize))) return CRE;
	 if (!Read32(CDF->fp,&(GDR->RecordType))) return CRE;
	 if (!Read32(CDF->fp,&(GDR->rVDRhead))) return CRE;
	 if (!Read32(CDF->fp,&(GDR->zVDRhead))) return CRE;
	 if (!Read32(CDF->fp,&(GDR->ADRhead))) return CRE;
	 if (!Read32(CDF->fp,&(GDR->eof))) return CRE;
	 if (!Read32(CDF->fp,&(GDR->NrVars))) return CRE;
	 if (!Read32(CDF->fp,&(GDR->NumAttr))) return CRE;
	 if (!Read32(CDF->fp,&(GDR->rMaxRec))) return CRE;
	 if (!Read32(CDF->fp,&(GDR->rNumDims))) return CRE;
	 if (!Read32(CDF->fp,&(GDR->NzVars))) return CRE;
	 if (!Read32(CDF->fp,&(GDR->UIRhead))) return CRE;
	 if (!Read32(CDF->fp,&(GDR->rfuC))) return CRE;
	 if (!Read32(CDF->fp,&(GDR->rfuD))) return CRE;
	 if (!Read32(CDF->fp,&(GDR->rfuE))) return CRE;
	 if (!Read32s(CDF->fp,GDR->rDimSizes,
		      (int)GDR->rNumDims)) return CRE;
	 break;
       }
       case GDR_rDIMSIZES: {
	 Int32 *rDimSizes = va_arg (ap, Int32 *); Int32 rNumDims; long tOffset;
	 if (!sX(ReadGDR(CDF,GDR_rNUMDIMS,&rNumDims,
			     GDR_NULL),&pStatus)) return pStatus;
	 tOffset = CDF->GDRoffset + GDR_rDIMSIZES_OFFSET;
	 if (!SEEKv(CDF->fp,tOffset,vSEEK_SET)) return CRE;
	 if (!Read32s(CDF->fp,rDimSizes,(int)rNumDims)) return CRE;
	 break;
       }
       default: {
	 Int32 *buffer = va_arg (ap, Int32 *); long tOffset = CDF->GDRoffset;
	 switch (field) {
	   case GDR_RECORDSIZE: tOffset += GDR_RECORDSIZE_OFFSET; break;
	   case GDR_RECORDTYPE: tOffset += GDR_RECORDTYPE_OFFSET; break;
	   case GDR_rVDRHEAD: tOffset += GDR_rVDRHEAD_OFFSET; break;
	   case GDR_zVDRHEAD: tOffset += GDR_zVDRHEAD_OFFSET; break;
	   case GDR_ADRHEAD: tOffset += GDR_ADRHEAD_OFFSET; break;
	   case GDR_EOF: tOffset += GDR_EOF_OFFSET; break;
	   case GDR_NrVARS: tOffset += GDR_NrVARS_OFFSET; break;
	   case GDR_NUMATTR: tOffset += GDR_NUMATTR_OFFSET; break;
	   case GDR_rMAXREC: tOffset += GDR_rMAXREC_OFFSET; break;
	   case GDR_rNUMDIMS: tOffset += GDR_rNUMDIMS_OFFSET; break;
	   case GDR_NzVARS: tOffset += GDR_NzVARS_OFFSET; break;
	   case GDR_UIRHEAD: tOffset += GDR_UIRHEAD_OFFSET; break;
	   default: return CDF_INTERNAL_ERROR;
	 }
	 if (!SEEKv(CDF->fp,tOffset,vSEEK_SET)) return CRE;
	 if (!Read32(CDF->fp,buffer)) return CRE;
	 break;
       }
     }
  }
}

/******************************************************************************
* Read ADR.
******************************************************************************/

#if defined(STDARG)
STATICforIDL CDFstatus ReadADR (struct cdfSTRUCT *CDF, ...)
#else
STATICforIDL CDFstatus ReadADR (va_alist)
va_dcl
#endif
{
  va_list ap; Int32 offset;
  CDFstatus pStatus = CDF_OK;
#if defined(STDARG)
  va_start (ap, CDF);
#else
  struct cdfSTRUCT *CDF;
  VA_START (ap);
  CDF = va_arg (ap, struct cdfSTRUCT *);
#endif
  offset = va_arg (ap, Int32);
  for (;;) {
     int field = va_arg (ap, int);
     switch (field) {
       case ADR_NULL:
	 va_end (ap);
	 return pStatus;
       case ADR_RECORD: {
	 struct ADRstruct *ADR = va_arg (ap, struct ADRstruct *);
	 if (!SEEKv(CDF->fp,(long)offset,vSEEK_SET)) return CRE;
	 if (!Read32(CDF->fp,&(ADR->RecordSize))) return CRE;
	 if (!Read32(CDF->fp,&(ADR->RecordType))) return CRE;
	 if (!Read32(CDF->fp,&(ADR->ADRnext))) return CRE;
	 if (!Read32(CDF->fp,&(ADR->AgrEDRhead))) return CRE;
	 if (!Read32(CDF->fp,&(ADR->Scope))) return CRE;
	 if (!Read32(CDF->fp,&(ADR->Num))) return CRE;
	 if (!Read32(CDF->fp,&(ADR->NgrEntries))) return CRE;
	 if (!Read32(CDF->fp,&(ADR->MAXgrEntry))) return CRE;
	 if (!Read32(CDF->fp,&(ADR->rfuA))) return CRE;
	 if (!Read32(CDF->fp,&(ADR->AzEDRhead))) return CRE;
	 if (!Read32(CDF->fp,&(ADR->NzEntries))) return CRE;
	 if (!Read32(CDF->fp,&(ADR->MAXzEntry))) return CRE;
	 if (!Read32(CDF->fp,&(ADR->rfuE))) return CRE;
	 if (!READv(ADR->Name,CDF_ATTR_NAME_LEN,1,CDF->fp)) return CRE;
	 NulPad (ADR->Name, CDF_ATTR_NAME_LEN);
	 break;
       }
       case ADR_NAME: {
	 char *aName = va_arg (ap, char *);
	 long tOffset = offset + ADR_NAME_OFFSET;
	 if (!SEEKv(CDF->fp,tOffset,vSEEK_SET)) return CRE;
	 if (!READv(aName,CDF_ATTR_NAME_LEN,1,CDF->fp)) return CRE;
	 NulPad (aName, CDF_ATTR_NAME_LEN);
	 break;
       }
       default: {
	 Int32 *buffer = va_arg (ap, Int32 *); long tOffset = offset;
	 switch (field) {
	   case ADR_RECORDSIZE: tOffset += ADR_RECORDSIZE_OFFSET; break;
	   case ADR_RECORDTYPE: tOffset += ADR_RECORDTYPE_OFFSET; break;
	   case ADR_ADRNEXT: tOffset += ADR_ADRNEXT_OFFSET; break;
	   case ADR_AgrEDRHEAD: tOffset += ADR_AgrEDRHEAD_OFFSET; break;
	   case ADR_SCOPE: tOffset += ADR_SCOPE_OFFSET; break;
	   case ADR_NUM: tOffset += ADR_NUM_OFFSET; break;
	   case ADR_NgrENTRIES: tOffset += ADR_NgrENTRIES_OFFSET; break;
	   case ADR_MAXgrENTRY: tOffset += ADR_MAXgrENTRY_OFFSET; break;
	   case ADR_AzEDRHEAD: tOffset += ADR_AzEDRHEAD_OFFSET; break;
	   case ADR_NzENTRIES: tOffset += ADR_NzENTRIES_OFFSET; break;
	   case ADR_MAXzENTRY: tOffset += ADR_MAXzENTRY_OFFSET; break;
	   default: return CDF_INTERNAL_ERROR;
	 }
	 if (!SEEKv(CDF->fp,tOffset,vSEEK_SET)) return CRE;
	 if (!Read32(CDF->fp,buffer)) return CRE;
	 break;
       }
     }
  }
}

/******************************************************************************
* Read AEDR/AzEDR.
*   If the entry value is being read, it is passed back in the encoding of the
* CDF (no decoding is performed).  The caller must decode the value (if that
* is necessary).
******************************************************************************/

#if defined(STDARG)
STATICforIDL CDFstatus ReadAEDR (struct cdfSTRUCT *CDF, ...)
#else
STATICforIDL CDFstatus ReadAEDR (va_alist)
va_dcl
#endif
{
  va_list ap; Int32 offset;
  CDFstatus pStatus = CDF_OK;
#if defined(STDARG)
  va_start (ap, CDF);
#else
  struct cdfSTRUCT *CDF;
  VA_START (ap);
  CDF = va_arg (ap, struct cdfSTRUCT *);
#endif
  offset = va_arg (ap, Int32);
  for (;;) {
     int field = va_arg (ap, int);
     switch (field) {
       case AEDR_NULL:
	 va_end (ap);
	 return pStatus;
       case AEDR_RECORD: {
	 struct AEDRstruct *AEDR = va_arg (ap, struct AEDRstruct *);
	 void *value = va_arg (ap, void *); size_t nBytes;
	 if (!SEEKv(CDF->fp,(long)offset,vSEEK_SET)) return CRE;
	 if (!Read32(CDF->fp,&(AEDR->RecordSize))) return CRE;
	 if (!Read32(CDF->fp,&(AEDR->RecordType))) return CRE;
	 if (!Read32(CDF->fp,&(AEDR->AEDRnext))) return CRE;
	 if (!Read32(CDF->fp,&(AEDR->AttrNum))) return CRE;
	 if (!Read32(CDF->fp,&(AEDR->DataType))) return CRE;
	 if (!Read32(CDF->fp,&(AEDR->Num))) return CRE;
	 if (!Read32(CDF->fp,&(AEDR->NumElems))) return CRE;
	 if (!Read32(CDF->fp,&(AEDR->rfuA))) return CRE;
	 if (!Read32(CDF->fp,&(AEDR->rfuB))) return CRE;
	 if (!Read32(CDF->fp,&(AEDR->rfuC))) return CRE;
	 if (!Read32(CDF->fp,&(AEDR->rfuD))) return CRE;
	 if (!Read32(CDF->fp,&(AEDR->rfuE))) return CRE;
	 if (value != NULL) {
	   nBytes = (size_t) (CDFelemSize(AEDR->DataType) * AEDR->NumElems);
	   if (!READv(value,nBytes,1,CDF->fp)) return CRE;
	 }
	 break;
       }
       case AEDR_VALUE: {
	 void *value = va_arg (ap, void *);
	 size_t nBytes; Int32 dataType, numElems; long tOffset;
	 if (!sX(ReadAEDR(CDF,offset,AEDR_DATATYPE,&dataType,
				     AEDR_NUMELEMS,&numElems,
				     AEDR_NULL),&pStatus)) return pStatus;
	 tOffset = offset + AEDR_VALUE_OFFSET;
	 if (!SEEKv(CDF->fp,tOffset,vSEEK_SET)) return CRE;
	 nBytes = (size_t) (CDFelemSize(dataType) * numElems);
	 if (!READv(value,nBytes,1,CDF->fp)) return CRE;
	 break;
       }
       default: {
	 Int32 *buffer = va_arg (ap, Int32 *); long tOffset = offset;
	 switch (field) {
	   case AEDR_RECORDSIZE: tOffset += AEDR_RECORDSIZE_OFFSET; break;
	   case AEDR_RECORDTYPE: tOffset += AEDR_RECORDTYPE_OFFSET; break;
	   case AEDR_AEDRNEXT: tOffset += AEDR_AEDRNEXT_OFFSET; break;
	   case AEDR_ATTRNUM: tOffset += AEDR_ATTRNUM_OFFSET; break;
	   case AEDR_DATATYPE: tOffset += AEDR_DATATYPE_OFFSET; break;
	   case AEDR_NUM: tOffset += AEDR_NUM_OFFSET; break;
	   case AEDR_NUMELEMS: tOffset += AEDR_NUMELEMS_OFFSET; break;
	   default: return CDF_INTERNAL_ERROR;
	 }
	 if (!SEEKv(CDF->fp,tOffset,vSEEK_SET)) return CRE;
	 if (!Read32(CDF->fp,buffer)) return CRE;
	 break;
       }
     }
  }
}

/******************************************************************************
* Read VDR/zVDR.
*   If the pad value is being read, it is passed back in the encoding of the
* CDF (no decoding is performed).  The caller must decode the value (if that
* is necessary).
*   If this CDF contains wasted space in its VDRs, note that the offset for
* those fields after the wasted space is adjusted.
******************************************************************************/

#if defined(STDARG)
STATICforIDL CDFstatus ReadVDR (struct cdfSTRUCT *CDF, ...)
#else
STATICforIDL CDFstatus ReadVDR (va_alist)
va_dcl
#endif
{
  va_list ap; Int32 offset; Logical zVar;
  CDFstatus pStatus = CDF_OK;
#if defined(STDARG)
  va_start (ap, CDF);
#else
  struct cdfSTRUCT *CDF;
  VA_START (ap);
  CDF = va_arg (ap, struct cdfSTRUCT *);
#endif
  offset = va_arg (ap, Int32);
  zVar = va_arg (ap, Logical);
  for (;;) {
     int field = va_arg (ap, int);
     switch (field) {
       case VDR_NULL:
	 va_end (ap);
	 return pStatus;
       case VDR_RECORD: {
	 struct VDRstruct *VDR = va_arg (ap, struct VDRstruct *);
	 void *padValue = va_arg (ap, void *); Int32 nDims;
	 if (!SEEKv(CDF->fp,(long)offset,vSEEK_SET)) return CRE;
	 if (!Read32(CDF->fp,&(VDR->RecordSize))) return CRE;
	 if (!Read32(CDF->fp,&(VDR->RecordType))) return CRE;
	 if (!Read32(CDF->fp,&(VDR->VDRnext))) return CRE;
	 if (!Read32(CDF->fp,&(VDR->DataType))) return CRE;
	 if (!Read32(CDF->fp,&(VDR->MaxRec))) return CRE;
	 if (!Read32(CDF->fp,&(VDR->VXRhead))) return CRE;
	 if (!Read32(CDF->fp,&(VDR->VXRtail))) return CRE;
	 if (!Read32(CDF->fp,&(VDR->Flags))) return CRE;
	 if (!Read32(CDF->fp,&(VDR->rfuA))) return CRE;
	 if (!Read32(CDF->fp,&(VDR->rfuB))) return CRE;
	 if (!Read32(CDF->fp,&(VDR->rfuC))) return CRE;
	 if (!Read32(CDF->fp,&(VDR->rfuF))) return CRE;
	 if (CDF->wastedSpace) {
	   if (!SEEKv(CDF->fp,(long)VDR_WASTED_SIZE,vSEEK_CUR)) return CRE;
	 }
	 if (!Read32(CDF->fp,&(VDR->NumElems))) return CRE;
	 if (!Read32(CDF->fp,&(VDR->Num))) return CRE;
	 if (!Read32(CDF->fp,&(VDR->rfuD))) return CRE;
	 if (!Read32(CDF->fp,&(VDR->NextendRecs))) return CRE;
	 if (!READv(VDR->Name,CDF_VAR_NAME_LEN,1,CDF->fp)) return CRE;
	 NulPad (VDR->Name, CDF_VAR_NAME_LEN);
	 if (zVar) {
	   if (!Read32(CDF->fp,&(VDR->zNumDims))) return CRE;
	   if (!Read32s(CDF->fp,VDR->zDimSizes,(int)VDR->zNumDims)) return CRE;
	 }
	 if (zVar)
	   nDims = VDR->zNumDims;
	 else {
	   long tOffset = V_tell (CDF->fp);
	   if (!sX(ReadGDR(CDF,GDR_rNUMDIMS,&nDims,
			       GDR_NULL),&pStatus)) return pStatus;
	   if (!SEEKv(CDF->fp,tOffset,vSEEK_SET)) return CRE;
	 }
	 if (!Read32s(CDF->fp,VDR->DimVarys,(int)nDims)) return CRE;
	 if (PADvalueBITset(VDR->Flags) && padValue != NULL) {
	   size_t nBytes = (size_t) (CDFelemSize(VDR->DataType)*VDR->NumElems);
	   if (!READv(padValue,nBytes,1,CDF->fp)) return CRE;
	 }
	 break;
       }
       case VDR_NAME: {
	 char *vName = va_arg (ap, char *);
	 long tOffset = offset + VDR_NAME_OFFSET;
	 if (CDF->wastedSpace) tOffset += VDR_WASTED_SIZE;
	 if (!SEEKv(CDF->fp,tOffset,vSEEK_SET)) return CRE;
	 if (!READv(vName,CDF_VAR_NAME_LEN,1,CDF->fp)) return CRE;
	 NulPad (vName, CDF_VAR_NAME_LEN);
	 break;
       }
       case zVDR_zNUMDIMS: {
	 Int32 *numDims = va_arg (ap, Int32 *);
	 long tOffset = offset + zVDR_zNUMDIMS_OFFSET +
			BOO(CDF->wastedSpace,VDR_WASTED_SIZE,0);
	 if (!zVar) return CDF_INTERNAL_ERROR;
	 if (!SEEKv(CDF->fp,tOffset,vSEEK_SET)) return CRE;
	 if (!Read32(CDF->fp,numDims)) return CRE;
	 break;
       }
       case zVDR_zDIMSIZES: {
	 Int32 *zDimSizes = va_arg (ap, Int32 *);
	 Int32 zNumDims; long tOffset;
	 if (!zVar) return CDF_INTERNAL_ERROR;
	 if (!sX(ReadVDR(CDF,offset,zVar,zVDR_zNUMDIMS,&zNumDims,
					 VDR_NULL),&pStatus)) return pStatus;
	 tOffset = offset + zVDR_zDIMSIZES_OFFSET +
		   BOO(CDF->wastedSpace,VDR_WASTED_SIZE,0);
	 if (!SEEKv(CDF->fp,tOffset,vSEEK_SET)) return CRE;
	 if (!Read32s(CDF->fp,zDimSizes,(int)zNumDims)) return CRE;
	 break;
       }
       case VDR_DIMVARYS: {
	 Int32 *dimVarys = va_arg (ap, Int32 *);
	 Int32 nDims; long tOffset;
	 if (zVar) {
	   if (!sX(ReadVDR(CDF,offset,zVar,zVDR_zNUMDIMS,&nDims,
					   VDR_NULL),&pStatus)) return pStatus;
	   tOffset = offset + zVDR_DIMVARYS_OFFSETb + (nDims*sizeof(Int32)) +
		     BOO(CDF->wastedSpace,VDR_WASTED_SIZE,0);
	 }
	 else {
	   if (!sX(ReadGDR(CDF,GDR_rNUMDIMS,&nDims,
			       GDR_NULL),&pStatus)) return pStatus;
	   tOffset = offset + rVDR_DIMVARYS_OFFSET +
		     BOO(CDF->wastedSpace,VDR_WASTED_SIZE,0);
	 }
	 if (!SEEKv(CDF->fp,tOffset,vSEEK_SET)) return CRE;
	 if (!Read32s(CDF->fp,dimVarys,(int)nDims)) return CRE;
	 break;
       }
       case VDR_PADVALUE: {
	 void *padValue = va_arg (ap, void *);
	 Int32 dataType, numElems; size_t nBytes; long tOffset;
	 if (!sX(ReadVDR(CDF,offset,zVar,VDR_DATATYPE,&dataType,
					 VDR_NUMELEMS,&numElems,
					 VDR_NULL),&pStatus)) return pStatus;
	 if (zVar) {
	   Int32 zNumDims;
	   if (!sX(ReadVDR(CDF,offset,zVar,zVDR_zNUMDIMS,&zNumDims,
					   VDR_NULL),&pStatus)) return pStatus;
	   tOffset = offset + zVDR_PADVALUE_OFFSETb +
		     (zNumDims*sizeof(Int32)) +
		     (zNumDims*sizeof(Int32)) +
		     BOO(CDF->wastedSpace,VDR_WASTED_SIZE,0);
	 }
	 else {
	   Int32 rNumDims;
	   if (!sX(ReadGDR(CDF,GDR_rNUMDIMS,&rNumDims,
			       GDR_NULL),&pStatus)) return pStatus;
	   tOffset = offset + rVDR_PADVALUE_OFFSETb +
		     (rNumDims*sizeof(Int32)) +
		     BOO(CDF->wastedSpace,VDR_WASTED_SIZE,0);
	 }
	 if (!SEEKv(CDF->fp,tOffset,vSEEK_SET)) return CRE;
	 nBytes = (size_t) (CDFelemSize(dataType) * numElems);
	 if (!READv(padValue,nBytes,1,CDF->fp)) return CRE;
	 break;
       }
       default: {
	 Int32 *buffer = va_arg (ap, Int32 *); long tOffset = offset;
	 switch (field) {
	   case VDR_RECORDSIZE: tOffset += VDR_RECORDSIZE_OFFSET; break;
	   case VDR_RECORDTYPE: tOffset += VDR_RECORDTYPE_OFFSET; break;
	   case VDR_VDRNEXT: tOffset += VDR_VDRNEXT_OFFSET; break;
	   case VDR_DATATYPE: tOffset += VDR_DATATYPE_OFFSET; break;
	   case VDR_MAXREC: tOffset += VDR_MAXREC_OFFSET; break;
	   case VDR_VXRHEAD: tOffset += VDR_VXRHEAD_OFFSET; break;
	   case VDR_VXRTAIL: tOffset += VDR_VXRTAIL_OFFSET; break;
	   case VDR_FLAGS: tOffset += VDR_FLAGS_OFFSET; break;
	   case VDR_NUMELEMS:
	     tOffset += (VDR_NUMELEMS_OFFSET +
			 BOO(CDF->wastedSpace,VDR_WASTED_SIZE,0));
	     break;
	   case VDR_NUM:
	     tOffset += (VDR_NUM_OFFSET +
			 BOO(CDF->wastedSpace,VDR_WASTED_SIZE,0));
	     break;
	   case VDR_NEXTENDRECS:
	     tOffset += (VDR_NEXTENDRECS_OFFSET +
			 BOO(CDF->wastedSpace,VDR_WASTED_SIZE,0));
	     break;
	   default: return CDF_INTERNAL_ERROR;
	 }
	 if (!SEEKv(CDF->fp,tOffset,vSEEK_SET)) return CRE;
	 if (!Read32(CDF->fp,buffer)) return CRE;
	 break;
       }
     }
  }
}

/******************************************************************************
* Read VXR.
******************************************************************************/

#if defined(STDARG)
STATICforIDL CDFstatus ReadVXR (struct cdfSTRUCT *CDF, ...)
#else
STATICforIDL CDFstatus ReadVXR (va_alist)
va_dcl
#endif
{
  va_list ap; Int32 offset;
  CDFstatus pStatus = CDF_OK;
#if defined(STDARG)
  va_start (ap, CDF);
#else
  struct cdfSTRUCT *CDF;
  VA_START (ap);
  CDF = va_arg (ap, struct cdfSTRUCT *);
#endif
  offset = va_arg (ap, Int32);
  for (;;) {
     int field = va_arg (ap, int);
     switch (field) {
       case VXR_NULL:
	 va_end (ap);
	 return pStatus;
       case VXR_RECORD: {
	 struct VXRstruct *VXR = va_arg (ap, struct VXRstruct *);
	 if (!SEEKv(CDF->fp,(long)offset,vSEEK_SET)) return CRE;
	 if (!Read32(CDF->fp,&(VXR->RecordSize))) return CRE;
	 if (!Read32(CDF->fp,&(VXR->RecordType))) return CRE;
	 if (!Read32(CDF->fp,&(VXR->VXRnext))) return CRE;
	 if (!Read32(CDF->fp,&(VXR->Nentries))) return CRE;
	 if (!Read32(CDF->fp,&(VXR->NusedEntries))) return CRE;
	 if (!Read32s(CDF->fp,VXR->FirstRec,NUM_VXR_ENTRIES)) return CRE;
	 if (!Read32s(CDF->fp,VXR->LastRec,NUM_VXR_ENTRIES)) return CRE;
	 if (!Read32s(CDF->fp,VXR->VVRoffset,NUM_VXR_ENTRIES)) return CRE;
	 break;
       }
       case VXR_FIRSTREC:
       case VXR_LASTREC:
       case VXR_VVROFFSET: {
	 Int32 *buffer = va_arg (ap, Int32 *); long tOffset = offset;
	 switch (field) {
	   case VXR_FIRSTREC: tOffset += VXR_FIRSTREC_OFFSET; break;
	   case VXR_LASTREC: tOffset += VXR_LASTREC_OFFSET; break;
	   case VXR_VVROFFSET: tOffset += VXR_VVROFFSET_OFFSET; break;
	   default: return CDF_INTERNAL_ERROR;
	 }
	 if (!SEEKv(CDF->fp,tOffset,vSEEK_SET)) return CRE;
	 if (!Read32s(CDF->fp,buffer,NUM_VXR_ENTRIES)) return CRE;
	 break;
       }
       default: {
	 Int32 *buffer = va_arg (ap, Int32 *); long tOffset = offset;
	 switch (field) {
	   case VXR_RECORDSIZE: tOffset += VXR_RECORDSIZE_OFFSET; break;
	   case VXR_RECORDTYPE: tOffset += VXR_RECORDTYPE_OFFSET; break;
	   case VXR_VXRNEXT: tOffset += VXR_VXRNEXT_OFFSET; break;
	   case VXR_NENTRIES: tOffset += VXR_NENTRIES_OFFSET; break;
	   case VXR_NUSEDENTRIES: tOffset += VXR_NUSEDENTRIES_OFFSET; break;
	   default: return CDF_INTERNAL_ERROR;
	 }
	 if (!SEEKv(CDF->fp,tOffset,vSEEK_SET)) return CRE;
	 if (!Read32(CDF->fp,buffer)) return CRE;
	 break;
       }
     }
  }
}

/******************************************************************************
* Read VVR.
******************************************************************************/

#if defined(STDARG)
STATICforIDL CDFstatus ReadVVR (struct cdfSTRUCT *CDF, ...)
#else
STATICforIDL CDFstatus ReadVVR (va_alist)
va_dcl
#endif
{
  va_list ap; Int32 offset;
  CDFstatus pStatus = CDF_OK;
#if defined(STDARG)
  va_start (ap, CDF);
#else
  struct cdfSTRUCT *CDF;
  VA_START (ap);
  CDF = va_arg (ap, struct cdfSTRUCT *);
#endif
  offset = va_arg (ap, Int32);
  for (;;) {
     int field = va_arg (ap, int);
     switch (field) {
       case VVR_NULL:
	 va_end (ap);
	 return pStatus;
       case VVR_RECORD: {
	 return CDF_INTERNAL_ERROR;        /* Unsupported. */
       }
       default: {
	 Int32 *buffer = va_arg (ap, Int32 *); long tOffset = offset;
	 switch (field) {
	   case VVR_RECORDSIZE: tOffset += VVR_RECORDSIZE_OFFSET; break;
	   case VVR_RECORDTYPE: tOffset += VVR_RECORDTYPE_OFFSET; break;
	   case VVR_BUFFER: return CDF_INTERNAL_ERROR;     /* Unsupported. */
	   default: return CDF_INTERNAL_ERROR;
	 }
	 if (!SEEKv(CDF->fp,tOffset,vSEEK_SET)) return CRE;
	 if (!Read32(CDF->fp,buffer)) return CRE;
	 break;
       }
     }
  }
}

/******************************************************************************
* Read UIR.
******************************************************************************/

#if defined(STDARG)
STATICforIDL CDFstatus ReadUIR (struct cdfSTRUCT *CDF, ...)
#else
STATICforIDL CDFstatus ReadUIR (va_alist)
va_dcl
#endif
{
  va_list ap; Int32 offset;
  CDFstatus pStatus = CDF_OK;
#if defined(STDARG)
  va_start (ap, CDF);
#else
  struct cdfSTRUCT *CDF;
  VA_START (ap);
  CDF = va_arg (ap, struct cdfSTRUCT *);
#endif
  offset = va_arg (ap, Int32);
  for (;;) {
     int field = va_arg (ap, int);
     switch (field) {
       case UIR_NULL:
	 va_end (ap);
	 return pStatus;
       case UIR_RECORD: {
	 struct UIRstruct *UIR = va_arg (ap, struct UIRstruct *);
	 if (!SEEKv(CDF->fp,(long)offset,vSEEK_SET)) return CRE;
	 if (!Read32(CDF->fp,&(UIR->RecordSize))) return CRE;
	 if (!Read32(CDF->fp,&(UIR->RecordType))) return CRE;
	 if (!Read32(CDF->fp,&(UIR->NextUIR))) return CRE;
	 if (!Read32(CDF->fp,&(UIR->PrevUIR))) return CRE;
	 break;
       }
       default: {
	 Int32 *buffer = va_arg (ap, Int32 *); long tOffset = offset;
	 switch (field) {
	   case UIR_RECORDSIZE: tOffset += UIR_RECORDSIZE_OFFSET; break;
	   case UIR_RECORDTYPE: tOffset += UIR_RECORDTYPE_OFFSET; break;
	   case UIR_NEXTUIR: tOffset += UIR_NEXTUIR_OFFSET; break;
	   case UIR_PREVUIR: tOffset += UIR_PREVUIR_OFFSET; break;
	   default: return CDF_INTERNAL_ERROR;
	 }
	 if (!SEEKv(CDF->fp,tOffset,vSEEK_SET)) return CRE;
	 if (!Read32(CDF->fp,buffer)) return CRE;
	 break;
       }
     }
  }
}
