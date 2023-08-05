/******************************************************************************
*
*  NSSDC/CDF                                            Validate CDF things.
*
*  Version 1.8a, 24-Feb-95, Hughes STX.
*
*  Modification history:
*
*   V1.0   3-Jun-91, J Love     Original version (for CDF V2.1).  This is a
*                               combination of validcdfname.c, validvarname.c,
*                               validattrname.c, validdatatype.c,
*                               validattrscope.c, and validencoding.
*   V1.1  10-Jun-91, J Love     Don't allow blanks in VMS CDF names.  Check
*                               all characters in CDF, attr., and var. names.
*   V1.2  28-Jun-91, J Love     Housekeeping.
*   V1.3  15-Sep-91, J Love     Changed for IBM-PC port.
*   V1.4   4-Oct-91, J Love     Changed for IBM-RS6000 port (and IBM-PC).
*   V1.5  23-Mar-92, J Love     HP port/CDF V2.2.
*   V1.6   5-Oct-92, J Love     Added NeXT to `validEncoding' (better late
*                               than never).
*   V1.7  25-Jan-94, J Love     CDF V2.4.
*   V1.7a  4-Feb-94, J Love	DEC Alpha/OpenVMS port.
*   V1.8  13-Dec-94, J Love	CDF V2.5.
*   V1.8a 24-Feb-95, J Love	Solaris 2.3 IDL i/f.
*
******************************************************************************/

#include "cdflib.h"

/******************************************************************************
* Validate CDF name.
******************************************************************************/

STATICforIDL Logical ValidCDFname (name)
char *name;
{
  size_t len = strlen(name);
  int i;
  /****************************************************************************
  * Length must be at least one.
  ****************************************************************************/
  if (len < 1) return FALSE;
  /****************************************************************************
  * All characters must be printable.
  ****************************************************************************/
  for (i = 0; i < len; i++) {
     if (!IsPrintChr(name[i])) return FALSE;
  }
  /****************************************************************************
  * Passed all tests - return TRUE.
  ****************************************************************************/
  return TRUE;
}

/******************************************************************************
* Validate variable name.
******************************************************************************/

STATICforIDL Logical ValidVarName (name)
char *name;
{
  size_t len;     /* length of name */
  size_t i;
  /****************************************************************************
  * Length must be at least one.
  ****************************************************************************/
  len = strlen(name);
  if (len < 1) return FALSE;      /* length must be at least one */
  /****************************************************************************
  * All characters must be printable.
  ****************************************************************************/
  for (i = 0; i < len; i++) {
     if (!IsPrintChr(name[i])) return FALSE;
  }
  /****************************************************************************
  * Passed all tests - return TRUE.
  ****************************************************************************/
  return TRUE;
}

/******************************************************************************
* Validate attribute name.
******************************************************************************/

STATICforIDL Logical ValidAttrName (name)
char *name;
{
  size_t len;     /* length of name */
  size_t i;
  /****************************************************************************
  * Length must be at least one.
  ****************************************************************************/
  len = strlen(name);
  if (len < 1) return FALSE;      /* length must be at least one */
  /****************************************************************************
  * All characters must be printable.
  ****************************************************************************/
  for (i = 0; i < len; i++) {
     if (!IsPrintChr(name[i])) return FALSE;
  }
  /****************************************************************************
  * Passed all tests - return TRUE.
  ****************************************************************************/
  return TRUE;
}

/******************************************************************************
* Validate data type.
******************************************************************************/

STATICforIDL Logical ValidDataType (dataType)
long dataType;
{
  switch (dataType) {
    case CDF_INT1: return TRUE;
    case CDF_INT2: return TRUE;
    case CDF_INT4: return TRUE;
    case CDF_UINT1: return TRUE;
    case CDF_UINT2: return TRUE;
    case CDF_UINT4: return TRUE;
    case CDF_REAL4: return TRUE;
    case CDF_REAL8: return TRUE;
    case CDF_CHAR: return TRUE;
    case CDF_UCHAR: return TRUE;
    case CDF_BYTE: return TRUE;
    case CDF_FLOAT: return TRUE;
    case CDF_DOUBLE: return TRUE;
    case CDF_EPOCH: return TRUE;
  }
  return FALSE;
}

/******************************************************************************
* Validate attribute scope.
******************************************************************************/

STATICforIDL Logical ValidAttrScope (scope)
long scope;
{
  switch (scope) {
    case GLOBAL_SCOPE: return TRUE;
    case VARIABLE_SCOPE: return TRUE;
  }
  return FALSE;
}

/******************************************************************************
* Validate encoding.
******************************************************************************/

STATICforIDL Logical ValidEncoding (encoding, actualEncoding)
long encoding;
long *actualEncoding;
{
  switch (encoding) {
    case HOST_ENCODING:
      *actualEncoding = HostEncoding();
      break;
    case NETWORK_ENCODING:
    case SUN_ENCODING:
    case VAX_ENCODING:
    case DECSTATION_ENCODING:
    case SGi_ENCODING:
    case IBMPC_ENCODING:
    case IBMRS_ENCODING:
    case HP_ENCODING:
    case NeXT_ENCODING:
    case ALPHAOSF1_ENCODING:
    case ALPHAVMSd_ENCODING:
    case ALPHAVMSg_ENCODING:
    case MAC_ENCODING:
      *actualEncoding = encoding;
      break;
    default:
      return FALSE;
  }
  return TRUE;
}

/******************************************************************************
* Validate decoding.
******************************************************************************/

STATICforIDL Logical ValidDecoding (decoding)
long decoding;
{
  switch (decoding) {
    case HOST_DECODING:
    case NETWORK_DECODING:
    case SUN_DECODING:
    case VAX_DECODING:
    case DECSTATION_DECODING:
    case SGi_DECODING:
    case IBMPC_DECODING:
    case IBMRS_DECODING:
    case HP_DECODING:
    case NeXT_DECODING:
    case ALPHAOSF1_DECODING:
    case ALPHAVMSd_DECODING:
    case ALPHAVMSg_DECODING:
	case MAC_DECODING:
      return TRUE;
    default:
      return FALSE;
  }
}
