/******************************************************************************
*
*  NSSDC/CDF                                        Write to internal record.
*
*  Version 1.4a, 6-Sep-95, Hughes STX.
*
*  Modification history:
*
*   V1.0   4-Nov-93, J Love     Original version.
*   V1.1  15-Nov-94, J Love     CDF V2.5.
*   V1.2   5-Jan-95, J Love	Encode/decode changes.
*   V1.2a 30-Jan-95, J Love	`Write32s' now checks count.
*   V1.2b 24-Feb-95, J Love	Solaris 2.3 IDL i/f.
*   V1.3  26-May-95, J Love	CDF V2.4 compatibility mode.  What?
*   V1.4  14-Jun-95, J Love	Use `ReadXYZ' routines.
*   V1.4a  6-Sep-95, J Love	CDFexport-related changes.
*
******************************************************************************/

#include "cdflib.h"

/******************************************************************************
* Local macro definitions.
******************************************************************************/

#define CWE CDF_WRITE_ERROR

/******************************************************************************
* Write32.
******************************************************************************/

STATICforIDL Logical Write32 (fp, value)
vFILE *fp;
Int32 *value;
{
#if defined(NETWORKbyteORDERcpu)
  if (!WRITEv(value,4,1,fp)) return FALSE;
#else
  Int32 tValue;
  REVERSE4bIO (value, &tValue)
  if (!WRITEv(&tValue,4,1,fp)) return FALSE;
#endif
  return TRUE;
}

/******************************************************************************
* Write32s.
******************************************************************************/

STATICforIDL Logical Write32s (fp, buffer, count)
vFILE *fp;
Int32 *buffer;
int count;
{
#if defined(NETWORKbyteORDERcpu)
  if (count < 1) return TRUE;
  if (!WRITEv(buffer,4,count,fp)) return FALSE;
#else
#define MAX_tBUFFER_SIZE 10             /* This must be set to the maximum
					   value that `count' may ever be.
					   Currently, that is either the
					   maximum number of dimensions or
					   the number of entries in a VXR. */
  Int32 tBuffer[MAX_tBUFFER_SIZE]; int i;
  if (count < 1) return TRUE;
  for (i = 0; i < count; i++) {
     REVERSE4bIO (&buffer[i], &tBuffer[i])
  }
  if (!WRITEv(tBuffer,4,count,fp)) return FALSE;
#endif
  return TRUE;
}

/******************************************************************************
* Write CDR.
******************************************************************************/

#if defined(STDARG)
STATICforIDL CDFstatus WriteCDR (struct cdfSTRUCT *CDF, ...)
#else
STATICforIDL CDFstatus WriteCDR (va_alist)
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
	 char *copyRight = va_arg (ap, char *);
	 if (!SEEKv(CDF->fp,(long)CDF->CDRoffset,vSEEK_SET)) return CWE;
	 if (!Write32(CDF->fp,&(CDR->RecordSize))) return CWE;
	 if (!Write32(CDF->fp,&(CDR->RecordType))) return CWE;
	 if (!Write32(CDF->fp,&(CDR->GDRoffset))) return CWE;
	 if (!Write32(CDF->fp,&(CDR->Version))) return CWE;
	 if (!Write32(CDF->fp,&(CDR->Release))) return CWE;
	 if (!Write32(CDF->fp,&(CDR->Encoding))) return CWE;
	 if (!Write32(CDF->fp,&(CDR->Flags))) return CWE;
	 if (!Write32(CDF->fp,&(CDR->rfuA))) return CWE;
	 if (!Write32(CDF->fp,&(CDR->rfuB))) return CWE;
	 if (!Write32(CDF->fp,&(CDR->Increment))) return CWE;
	 if (!Write32(CDF->fp,&(CDR->rfuD))) return CWE;
	 if (!Write32(CDF->fp,&(CDR->rfuE))) return CWE;
	 if (copyRight != NULL) {
	   if (!WRITEv(copyRight,CDF_COPYRIGHT_LEN,1,CDF->fp)) return CWE;
	 }
	 break;
       }
       case CDR_COPYRIGHT: {
	 char *copyRight = va_arg (ap, char *);
	 long tOffset = CDF->CDRoffset + CDR_COPYRIGHT_OFFSET;
	 if (!SEEKv(CDF->fp,tOffset,vSEEK_SET)) return CWE;
	 if (!WRITEv(copyRight,CDF_COPYRIGHT_LEN,1,CDF->fp)) return CWE;
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
	 if (!SEEKv(CDF->fp,tOffset,vSEEK_SET)) return CWE;
	 if (!Write32(CDF->fp,buffer)) return CWE;
	 break;
       }
     }
  }
}

/******************************************************************************
* Write GDR.
******************************************************************************/

#if defined(STDARG)
STATICforIDL CDFstatus WriteGDR (struct cdfSTRUCT *CDF, ...)
#else
STATICforIDL CDFstatus WriteGDR (va_alist)
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
	 if (!SEEKv(CDF->fp,(long)CDF->GDRoffset,vSEEK_SET)) return CWE;
	 if (!Write32(CDF->fp,&(GDR->RecordSize))) return CWE;
	 if (!Write32(CDF->fp,&(GDR->RecordType))) return CWE;
	 if (!Write32(CDF->fp,&(GDR->rVDRhead))) return CWE;
	 if (!Write32(CDF->fp,&(GDR->zVDRhead))) return CWE;
	 if (!Write32(CDF->fp,&(GDR->ADRhead))) return CWE;
	 if (!Write32(CDF->fp,&(GDR->eof))) return CWE;
	 if (!Write32(CDF->fp,&(GDR->NrVars))) return CWE;
	 if (!Write32(CDF->fp,&(GDR->NumAttr))) return CWE;
	 if (!Write32(CDF->fp,&(GDR->rMaxRec))) return CWE;
	 if (!Write32(CDF->fp,&(GDR->rNumDims))) return CWE;
	 if (!Write32(CDF->fp,&(GDR->NzVars))) return CWE;
	 if (!Write32(CDF->fp,&(GDR->UIRhead))) return CWE;
	 if (!Write32(CDF->fp,&(GDR->rfuC))) return CWE;
	 if (!Write32(CDF->fp,&(GDR->rfuD))) return CWE;
	 if (!Write32(CDF->fp,&(GDR->rfuE))) return CWE;
	 if (!Write32s(CDF->fp,GDR->rDimSizes,(int)GDR->rNumDims)) return CWE;
	 break;
       }
       case GDR_rDIMSIZES: {
	 Int32 *rDimSizes = va_arg (ap, Int32 *), rNumDims; long tOffset;
	 if (!sX(ReadGDR(CDF,GDR_rNUMDIMS,&rNumDims,
			     GDR_NULL),&pStatus)) return pStatus;
	 tOffset = CDF->GDRoffset + GDR_rDIMSIZES_OFFSET;
	 if (!SEEKv(CDF->fp,tOffset,vSEEK_SET)) return CWE;
	 if (!Write32s(CDF->fp,rDimSizes,(int)rNumDims)) return CWE;
	 break;
       }
       default: {
	 Int32 *buffer = va_arg (ap, Int32 *);
	 Int32 tOffset = CDF->GDRoffset;
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
	 if (!SEEKv(CDF->fp,tOffset,vSEEK_SET)) return CWE;
	 if (!Write32(CDF->fp,buffer)) return CWE;
	 break;
       }
     }
  }
}

/******************************************************************************
* Write ADR.
******************************************************************************/

#if defined(STDARG)
STATICforIDL CDFstatus WriteADR (struct cdfSTRUCT *CDF, ...)
#else
STATICforIDL CDFstatus WriteADR (va_alist)
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
	 if (!SEEKv(CDF->fp,(long)offset,vSEEK_SET)) return CWE;
	 if (!Write32(CDF->fp,&(ADR->RecordSize))) return CWE;
	 if (!Write32(CDF->fp,&(ADR->RecordType))) return CWE;
	 if (!Write32(CDF->fp,&(ADR->ADRnext))) return CWE;
	 if (!Write32(CDF->fp,&(ADR->AgrEDRhead))) return CWE;
	 if (!Write32(CDF->fp,&(ADR->Scope))) return CWE;
	 if (!Write32(CDF->fp,&(ADR->Num))) return CWE;
	 if (!Write32(CDF->fp,&(ADR->NgrEntries))) return CWE;
	 if (!Write32(CDF->fp,&(ADR->MAXgrEntry))) return CWE;
	 if (!Write32(CDF->fp,&(ADR->rfuA))) return CWE;
	 if (!Write32(CDF->fp,&(ADR->AzEDRhead))) return CWE;
	 if (!Write32(CDF->fp,&(ADR->NzEntries))) return CWE;
	 if (!Write32(CDF->fp,&(ADR->MAXzEntry))) return CWE;
	 if (!Write32(CDF->fp,&(ADR->rfuE))) return CWE;
	 if (!WRITEv(ADR->Name,CDF_ATTR_NAME_LEN,1,CDF->fp)) return CWE;
	 break;
       }
       case ADR_NAME: {
	 char *aName = va_arg (ap, char *);
	 long tOffset = offset + ADR_NAME_OFFSET;
	 if (!SEEKv(CDF->fp,tOffset,vSEEK_SET)) return CWE;
	 if (!WRITEv(aName,CDF_ATTR_NAME_LEN,1,CDF->fp)) return CWE;
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
	 if (!SEEKv(CDF->fp,tOffset,vSEEK_SET)) return CWE;
	 if (!Write32(CDF->fp,buffer)) return CWE;
	 break;
       }
     }
  }
}

/******************************************************************************
* Write AgrEDR/AzEDR.
*    If the entry value is being written, it is assumed that the value passed
* in is in the host machine's encoding.
******************************************************************************/

#if defined(STDARG)
STATICforIDL CDFstatus WriteAEDR (struct cdfSTRUCT *CDF, ...)
#else
STATICforIDL CDFstatus WriteAEDR (va_alist)
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
	 void *value = va_arg (ap, void *);
	 if (!SEEKv(CDF->fp,(long)offset,vSEEK_SET)) return CWE;
	 if (!Write32(CDF->fp,&(AEDR->RecordSize))) return CWE;
	 if (!Write32(CDF->fp,&(AEDR->RecordType))) return CWE;
	 if (!Write32(CDF->fp,&(AEDR->AEDRnext))) return CWE;
	 if (!Write32(CDF->fp,&(AEDR->AttrNum))) return CWE;
	 if (!Write32(CDF->fp,&(AEDR->DataType))) return CWE;
	 if (!Write32(CDF->fp,&(AEDR->Num))) return CWE;
	 if (!Write32(CDF->fp,&(AEDR->NumElems))) return CWE;
	 if (!Write32(CDF->fp,&(AEDR->rfuA))) return CWE;
	 if (!Write32(CDF->fp,&(AEDR->rfuB))) return CWE;
	 if (!Write32(CDF->fp,&(AEDR->rfuC))) return CWE;
	 if (!Write32(CDF->fp,&(AEDR->rfuD))) return CWE;
	 if (!Write32(CDF->fp,&(AEDR->rfuE))) return CWE;
	 if (value != NULL) {
	   if (!sX(WriteBuffer(CDF,(long)AEDR->DataType,
			       (long)AEDR->NumElems,
			       value),&pStatus)) return pStatus;
	 }
	 break;
       }
       case AEDR_VALUE: {
	 void *value = va_arg (ap, void *);
	 Int32 dataType, numElems; long tOffset;
	 if (!sX(ReadAEDR(CDF,offset,AEDR_DATATYPE,&dataType,
				     AEDR_NUMELEMS,&numElems,
				     AEDR_NULL),&pStatus)) return pStatus;
	 tOffset = offset + AEDR_VALUE_OFFSET;
	 if (!SEEKv(CDF->fp,tOffset,vSEEK_SET)) return CWE;
	 if (!sX(WriteBuffer(CDF,(long)dataType,
			     (long)numElems,value),&pStatus)) return pStatus;
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
	 if (!SEEKv(CDF->fp,tOffset,vSEEK_SET)) return CWE;
	 if (!Write32(CDF->fp,buffer)) return CWE;
	 break;
       }
     }
  }
}

/******************************************************************************
* Write rVDR/zVDR.
*    If the pad value is being written, it is assumed that the value passed
* in is in the host machine's encoding.
******************************************************************************/

#if defined(STDARG)
STATICforIDL CDFstatus WriteVDR (struct cdfSTRUCT *CDF, ...)
#else
STATICforIDL CDFstatus WriteVDR (va_alist)
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
	 if (!SEEKv(CDF->fp,(long)offset,vSEEK_SET)) return CWE;
	 if (!Write32(CDF->fp,&(VDR->RecordSize))) return CWE;
	 if (!Write32(CDF->fp,&(VDR->RecordType))) return CWE;
	 if (!Write32(CDF->fp,&(VDR->VDRnext))) return CWE;
	 if (!Write32(CDF->fp,&(VDR->DataType))) return CWE;
	 if (!Write32(CDF->fp,&(VDR->MaxRec))) return CWE;
	 if (!Write32(CDF->fp,&(VDR->VXRhead))) return CWE;
	 if (!Write32(CDF->fp,&(VDR->VXRtail))) return CWE;
	 if (!Write32(CDF->fp,&(VDR->Flags))) return CWE;
	 if (!Write32(CDF->fp,&(VDR->rfuA))) return CWE;
	 if (!Write32(CDF->fp,&(VDR->rfuB))) return CWE;
	 if (!Write32(CDF->fp,&(VDR->rfuC))) return CWE;
	 if (!Write32(CDF->fp,&(VDR->rfuF))) return CWE;
	 if (!Write32(CDF->fp,&(VDR->NumElems))) return CWE;
	 if (!Write32(CDF->fp,&(VDR->Num))) return CWE;
	 if (!Write32(CDF->fp,&(VDR->rfuD))) return CWE;
	 if (!Write32(CDF->fp,&(VDR->NextendRecs))) return CWE;
	 if (!WRITEv(VDR->Name,CDF_VAR_NAME_LEN,1,CDF->fp)) return CWE;
	 if (zVar) {
	   if (!Write32(CDF->fp,&(VDR->zNumDims))) return CWE;
	   if (!Write32s(CDF->fp,VDR->zDimSizes,
			 (int)VDR->zNumDims)) return CWE;
	 }
	 if (zVar)
	   nDims = VDR->zNumDims;
	 else {
	   long tOffset = V_tell (CDF->fp);
	   if (!sX(ReadGDR(CDF,GDR_rNUMDIMS,&nDims,
			       GDR_NULL),&pStatus)) return pStatus;
	   if (!SEEKv(CDF->fp,tOffset,vSEEK_SET)) return CWE;
	 }
	 if (!Write32s(CDF->fp,VDR->DimVarys,(int)nDims)) return CWE;
	 if (PADvalueBITset(VDR->Flags) && padValue != NULL) {
	   if (!sX(WriteBuffer(CDF,(long)VDR->DataType,
			       (long)VDR->NumElems,
			       padValue),&pStatus)) return pStatus;
	 }
	 break;
       }
       case VDR_NAME: {
	 char *vName = va_arg (ap, char *);
	 long tOffset = offset + VDR_NAME_OFFSET;
	 if (!SEEKv(CDF->fp,tOffset,vSEEK_SET)) return CWE;
	 if (!WRITEv(vName,CDF_VAR_NAME_LEN,1,CDF->fp)) return CWE;
	 break;
       }
       case zVDR_zNUMDIMS: {
	 Int32 *numDims = va_arg (ap, Int32 *);
	 long tOffset = offset + zVDR_zNUMDIMS_OFFSET;
	 if (!zVar) return CDF_INTERNAL_ERROR;
	 if (!SEEKv(CDF->fp,tOffset,vSEEK_SET)) return CWE;
	 if (!Write32(CDF->fp,numDims)) return CWE;
	 break;
       }
       case zVDR_zDIMSIZES: {
	 Int32 *zDimSizes = va_arg (ap, Int32 *), zNumDims;
	 int dimN; long tOffset;
	 if (!zVar) return CDF_INTERNAL_ERROR;
	 if (!sX(ReadVDR(CDF,offset,zVar,zVDR_zNUMDIMS,&zNumDims,
					 VDR_NULL),&pStatus)) return pStatus;
	 tOffset = offset + zVDR_zDIMSIZES_OFFSET;
	 if (!SEEKv(CDF->fp,tOffset,vSEEK_SET)) return CWE;
	 for (dimN = 0; dimN < zNumDims; dimN++) {
	    if (!Write32(CDF->fp,&(zDimSizes[dimN]))) return CWE;
	 }
	 break;
       }
       case VDR_DIMVARYS: {
	 Int32 *dimVarys = va_arg (ap, Int32 *), nDims; long tOffset;
	 if (zVar) {
	   if (!sX(ReadVDR(CDF,offset,zVar,zVDR_zNUMDIMS,&nDims,
					   VDR_NULL),&pStatus)) return pStatus;
	   tOffset = offset + zVDR_DIMVARYS_OFFSETb + (nDims * sizeof(Int32));
	 }
	 else {
	   if (!sX(ReadGDR(CDF,GDR_rNUMDIMS,&nDims,GDR_NULL),&pStatus))
	     return pStatus;
	   tOffset = offset + rVDR_DIMVARYS_OFFSET;
	 }
	 if (!SEEKv(CDF->fp,tOffset,vSEEK_SET)) return CWE;
	 if (!Write32s(CDF->fp,dimVarys,(int)nDims)) return CWE;
	 break;
       }
       case VDR_PADVALUE: {
	 void *padValue = va_arg (ap, void *);
	 Int32 dataType, numElems; long tOffset;
	 if (!sX(ReadVDR(CDF,offset,zVar,VDR_DATATYPE,&dataType,
					 VDR_NUMELEMS,&numElems,
					 VDR_NULL),&pStatus)) return pStatus;
	 if (zVar) {
	   Int32 zNumDims;
	   if (!sX(ReadVDR(CDF,offset,zVar,zVDR_zNUMDIMS,&zNumDims,
					   VDR_NULL),&pStatus)) return pStatus;
	   tOffset = offset + zVDR_PADVALUE_OFFSETb +
		     (zNumDims * sizeof(Int32)) + (zNumDims * sizeof(Int32));
	 }
	 else {
	   Int32 rNumDims;
	   if (!sX(ReadGDR(CDF,GDR_rNUMDIMS,&rNumDims,
			       GDR_NULL),&pStatus)) return pStatus;
	   tOffset = offset + rVDR_PADVALUE_OFFSETb + (rNumDims*sizeof(Int32));
	 }
	 if (!SEEKv(CDF->fp,tOffset,vSEEK_SET)) return CWE;
	 if (!sX(WriteBuffer(CDF,(long)dataType,
			     (long)numElems,padValue),&pStatus)) return
								 pStatus;
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
	   case VDR_NUMELEMS: tOffset += VDR_NUMELEMS_OFFSET; break;
	   case VDR_NUM: tOffset += VDR_NUM_OFFSET; break;
	   case VDR_NEXTENDRECS: tOffset += VDR_NEXTENDRECS_OFFSET; break;
	   default: return CDF_INTERNAL_ERROR;
	 }
	 if (!SEEKv(CDF->fp,tOffset,vSEEK_SET)) return CWE;
	 if (!Write32(CDF->fp,buffer)) return CWE;
	 break;
       }
     }
  }
}

/******************************************************************************
* Write VXR.
******************************************************************************/

#if defined(STDARG)
STATICforIDL CDFstatus WriteVXR (struct cdfSTRUCT *CDF, ...)
#else
STATICforIDL CDFstatus WriteVXR (va_alist)
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
	 if (!SEEKv(CDF->fp,(long)offset,vSEEK_SET)) return CWE;
	 if (!Write32(CDF->fp,&(VXR->RecordSize))) return CWE;
	 if (!Write32(CDF->fp,&(VXR->RecordType))) return CWE;
	 if (!Write32(CDF->fp,&(VXR->VXRnext))) return CWE;
	 if (!Write32(CDF->fp,&(VXR->Nentries))) return CWE;
	 if (!Write32(CDF->fp,&(VXR->NusedEntries))) return CWE;
	 if (!Write32s(CDF->fp,VXR->FirstRec,NUM_VXR_ENTRIES)) return CWE;
	 if (!Write32s(CDF->fp,VXR->LastRec,NUM_VXR_ENTRIES)) return CWE;
	 if (!Write32s(CDF->fp,VXR->VVRoffset,NUM_VXR_ENTRIES)) return CWE;
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
	 if (!SEEKv(CDF->fp,tOffset,vSEEK_SET)) return CWE;
	 if (!Write32s(CDF->fp,buffer,NUM_VXR_ENTRIES)) return CWE;
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
	 if (!SEEKv(CDF->fp,tOffset,vSEEK_SET)) return CWE;
	 if (!Write32(CDF->fp,buffer)) return CWE;
	 break;
       }
     }
  }
}

/******************************************************************************
* Write VVR.
******************************************************************************/

#if defined(STDARG)
STATICforIDL CDFstatus WriteVVR (struct cdfSTRUCT *CDF, ...)
#else
STATICforIDL CDFstatus WriteVVR (va_alist)
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
	 if (!SEEKv(CDF->fp,tOffset,vSEEK_SET)) return CWE;
	 if (!Write32(CDF->fp,buffer)) return CWE;
	 break;
       }
     }
  }
}

/******************************************************************************
* Write UIR.
******************************************************************************/

#if defined(STDARG)
STATICforIDL CDFstatus WriteUIR (struct cdfSTRUCT *CDF, ...)
#else
STATICforIDL CDFstatus WriteUIR (va_alist)
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
	 if (!SEEKv(CDF->fp,(long)offset,vSEEK_SET)) return CWE;
	 if (!Write32(CDF->fp,&(UIR->RecordSize))) return CWE;
	 if (!Write32(CDF->fp,&(UIR->RecordType))) return CWE;
	 if (!Write32(CDF->fp,&(UIR->NextUIR))) return CWE;
	 if (!Write32(CDF->fp,&(UIR->PrevUIR))) return CWE;
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
	 if (!SEEKv(CDF->fp,tOffset,vSEEK_SET)) return CWE;
	 if (!Write32(CDF->fp,buffer)) return CWE;
	 break;
       }
     }
  }
}
