/******************************************************************************
*
*  NSSDC/CDF			CDF C interface (for non-macro'ed functions.
*
*  Version 2.3, 9-Nov-94, Hughes STX.
*
*  Modification history:
*
*   V1.0   1-Jun-91, J Love	Original version (for CDF V2.1).  This is a
*				combination of cdf.c, cdfattr.c and cdfvar.c.
*				Most of these functions can be replaced by
*				the macros in 'cdf.h'.
*   V1.1  30-Jul-91, J Love	Use 'CDFlib'.
*   V2.0  10-Feb-92, J Love	IBM PC port.
*   V2.1  21-Aug-92, J Love	CDF V2.3 (shareable/NeXT/zVar).
*   V2.2  18-Oct-93, J Love	CDF V2.4.
*   V2.3   9-Nov-94, J Love	CDF V2.5.
*
******************************************************************************/

#include "cdflib.h"

/******************************************************************************
* CDFattrInquire.
*   Can't implement with macro because the attribute's scope determines which
* item(s) to use.
******************************************************************************/

CDFstatus CDFattrInquire (id, attrNum, attrName, attrScope, maxEntry)
CDFid	id;		/* In -- CDF id. */
long	attrNum;	/* In -- Attribute number. */
char	*attrName;	/* Out -- Attribute name. */
long	*attrScope;	/* Out -- Attribute scope. */
long	*maxEntry;	/* Out -- Maximum gEntry/rEntry number used. */
{
  CDFstatus pStatus = CDF_OK;
  if (!sX(CDFlib(SELECT_, CDF_, id,
			  ATTR_, attrNum,
		 GET_, ATTR_SCOPE_, attrScope,
		 NULL_), &pStatus)) return pStatus;
  if (!sX(CDFlib(SELECT_, CDF_, id,
		 GET_, ATTR_NAME_, attrName,
		       BOO(GLOBALscope(*attrScope),ATTR_MAXgENTRY_,
						   ATTR_MAXrENTRY_), maxEntry,
		 NULL_), &pStatus)) return pStatus;
  return pStatus;
}

/******************************************************************************
* CDFattrEntryInquire.
*   Can't implement with macro because the attribute's scope determines which
* item(s) to use.
******************************************************************************/

CDFstatus CDFattrEntryInquire (id, attrNum, entryNum, dataType, numElems)
CDFid	id;		/* In -- CDF id. */
long	attrNum;	/* In -- Attribute number. */
long	entryNum;	/* In -- gEntry/rEntry number. */
long	*dataType;	/* Out -- gEntry/rEntry data type. */
long	*numElems;	/* Out -- gEntry/rEntry number of elements. */
{
  long scope;
  CDFstatus pStatus = CDF_OK;
  if (!sX(CDFlib(SELECT_, CDF_, id,
			  ATTR_, attrNum,
		 GET_, ATTR_SCOPE_, &scope,
		 NULL_), &pStatus)) return pStatus;
  if (!sX(CDFlib(SELECT_, CDF_, id,
			  BOO(GLOBALscope(scope),gENTRY_,rENTRY_), entryNum,
		 GET_, BOO(GLOBALscope(scope),gENTRY_DATATYPE_,
					      rENTRY_DATATYPE_), dataType,
		       BOO(GLOBALscope(scope),gENTRY_NUMELEMS_,
					      rENTRY_NUMELEMS_), numElems,
		 NULL_), &pStatus)) return pStatus;
  return pStatus;
}

/******************************************************************************
* CDFattrPut.
*   Can't implement with macro because the attribute's scope determines which
* item(s) to use.
******************************************************************************/

CDFstatus CDFattrPut (id, attrNum, entryNum, dataType, numElems, value)
CDFid	id;		/* In -- CDF id. */
long	attrNum;	/* In -- Attribute number. */
long	entryNum;	/* In -- gEntry/rEntry number. */
long	dataType;	/* In -- gEntry/rEntry data type. */
long	numElems;	/* In -- gEntry/rEntry number of elements. */
void	*value;		/* In -- Value. */
{
  long scope;
  CDFstatus pStatus = CDF_OK;
  if (!sX(CDFlib(SELECT_, CDF_, id,
			  ATTR_, attrNum,
		 GET_, ATTR_SCOPE_, &scope,
		 NULL_), &pStatus)) return pStatus;
  if (!sX(CDFlib(SELECT_, CDF_, id,
			  BOO(GLOBALscope(scope),gENTRY_,rENTRY_), entryNum,
		 PUT_, BOO(GLOBALscope(scope),gENTRY_DATA_,rENTRY_DATA_),
						  dataType, numElems, value,
		 NULL_), &pStatus)) return pStatus;
  return pStatus;
}

/******************************************************************************
* CDFattrGet.
*   Can't implement with macro because the attribute's scope determines which
* item(s) to use.
******************************************************************************/

CDFstatus CDFattrGet (id, attrNum, entryNum, value)
CDFid	id;		/* In -- CDF id. */
long	attrNum;	/* In -- Attribute number. */
long	entryNum;	/* In -- gEntry/rEntry number. */
void	*value;		/* In -- Value. */
{
  long scope;
  CDFstatus pStatus = CDF_OK;
  if (!sX(CDFlib(SELECT_, CDF_, id,
			  ATTR_, attrNum,
		 GET_, ATTR_SCOPE_, &scope,
		 NULL_), &pStatus)) return pStatus;
  if (!sX(CDFlib(SELECT_, CDF_, id,
			  BOO(GLOBALscope(scope),gENTRY_,rENTRY_), entryNum,
		 GET_, BOO(GLOBALscope(scope),gENTRY_DATA_,
					      rENTRY_DATA_), value,
		 NULL_), &pStatus)) return pStatus;
  return pStatus;
}

/******************************************************************************
* CDFattrNum.
*   Can't implement with macro since it is the attribute number which is to be
* returned (unless an error).
******************************************************************************/

long CDFattrNum(id,attrName)
CDFid	id;		/* In -- CDF id. */
char	*attrName;	/* In -- attribute name. */
{
  CDFstatus status;
  long attrNum;
  status = CDFlib (SELECT_, CDF_, id,
		   GET_, ATTR_NUMBER_, attrName, &attrNum,
		   NULL_);
  if (StatusOK(status))
    return attrNum;
  else
    return status;
}

/******************************************************************************
* CDFvarNum.
*   Can't implement with macro since it is the variable number which is to be
* returned (unless an error).
******************************************************************************/

long CDFvarNum(id,varName)
CDFid	id;		/* In -- CDF id. */
char	*varName;	/* In -- variable name. */
{
  CDFstatus status;
  long varNum;
  status = CDFlib (SELECT_, CDF_, id,
		   GET_, rVAR_NUMBER_, varName, &varNum,
		   NULL_);
  if (StatusOK(status))
    return varNum;
  else
    return status;
}
