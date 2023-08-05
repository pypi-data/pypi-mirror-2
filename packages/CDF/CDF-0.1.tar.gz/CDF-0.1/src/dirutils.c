/******************************************************************************
*
*  NSSDC/CDF                                            Directory utilities.
*
*  Version 1.4a, 18-Apr-95, Hughes STX.
*
*  Modification history:
*
*   V1.0  20-Apr-92, J Love     Original version.
*   V1.1  21-Aug-92, J Love     CDF V2.3 (shareable/NeXT).
*   V1.2  26-Jan-94, J Love     CDF V2.4.
*   V1.3  24-Oct-94, J Love     CDF V2.5.
*   V1.3a 23-Jan-95, J Love	IRIX 6.0 (64-bit).
*   V1.3b 24-Feb-95, J Love	Solaris 2.3 IDL i/f.
*   V1.4  21-Mar-95, J Love	POSIX.
*   V1.4a 18-Apr-95, J Love	More POSIX.
*
*****************************************************************************/

#include "cdflib.h"

/*****************************************************************************
* Macro constants.
*****************************************************************************/

#if defined(unix) || defined(posixSHELL)
#define DU_MAX_USERNAME_LEN	100
#define DU_MAX_ENVVAR_LEN	80
#endif

/******************************************************************************
* Local function prototypes.
******************************************************************************/

#if defined(unix) || defined(posixSHELL)
static void DerefEnvVar PROTOARGs((char *shortP,
				   char longP[DU_MAX_PATH_LEN+1]));
static char *NextNonENVchar PROTOARGs((char *ptr));
#endif

/******************************************************************************
* ExpandPath.
******************************************************************************/

STATICforIDL void ExpandPath (shortP, longP)
char *shortP;
char longP[DU_MAX_PATH_LEN+1];
{
#if defined(unix) || defined(posixSHELL)
int len;
char username[DU_MAX_USERNAME_LEN+1];
char tempP[DU_MAX_PATH_LEN+1];
char *tail;
struct passwd *pw;
#endif

#if defined(unix) || defined(posixSHELL)
DerefEnvVar (shortP, tempP);

if (tempP[0] != '~')
  strcpyX (longP, tempP, DU_MAX_PATH_LEN);
else {
  tail = strchr (tempP, '/');
  if (tail != NULL) {
    len = tail - (tempP + 1);
    if (len > 0) {
      strcpyX (username, tempP + 1, MINIMUM(len,DU_MAX_USERNAME_LEN));
      pw = getpwnam (username);
    }
    else
      pw = getpwuid (getuid());
    if (pw != NULL)
      strcpyX (longP, pw->pw_dir, DU_MAX_PATH_LEN);
    else
      strcpyX (longP, "?", DU_MAX_PATH_LEN);

    strcatX (longP, tail, DU_MAX_PATH_LEN);
  }
  else {
    if (tempP[1] != NUL)
      pw = getpwnam (tempP + 1);
    else
      pw = getpwuid (getuid());
    if (pw != NULL)
      strcpyX (longP, pw->pw_dir, DU_MAX_PATH_LEN);
    else
      strcpyX (longP, "?", DU_MAX_PATH_LEN);
  }
}
#endif

#if defined(dos)
  strcpyX (longP, shortP, DU_MAX_PATH_LEN);
#endif

#if defined(vms)
  strcpyX (longP, shortP, DU_MAX_PATH_LEN);
#endif

#if defined(mac)
  /* Macintosh...check for alias? */
  strcpyX (longP, shortP, DU_MAX_PATH_LEN);
#endif

return;
}

/******************************************************************************
* IsReg (regular file).
*    `stat' on VMS and MS-DOS systems will indicate a regular file if ANY
* file can be found matching a wildcard spec.  On UNIX systems, that doesn't
* happen.
******************************************************************************/

STATICforIDL Logical IsReg (path)
char *path;
{
  char pathX[DU_MAX_PATH_LEN+1];
#if defined(mac)
  struct FInfo fndrInfo;
#else
  struct stat st;
#endif
  ExpandPath (path, pathX);
#if defined(mac)
  if (GetFInfo(CtoPstr(pathX),0,&fndrInfo) == noErr)
    return TRUE;
  else
    return FALSE;
#else
#if defined(vms)
  if (strchr(pathX,'*') != NULL) return FALSE; 
  if (strchr(pathX,'%') != NULL) return FALSE;
#endif
#if defined(dos)
  if (strchr(pathX,'*') != NULL) return FALSE; 
  if (strchr(pathX,'?') != NULL) return FALSE;
#endif
  if (stat(pathX, &st) == 0) {
#if defined(SALFORDC)		/* Salford's `stat' is broken. */
    return (st.st_size > 0);
#else
#if defined(S_ISREG)
    return S_ISREG(st.st_mode);
#else
    return (st.st_mode & S_IFREG);
#endif
#endif
  }
  else {
#if defined(vms)
    /**************************************************************************
    * If this is a VMS system and the file is on DECnet (`::' is in the
    * pathname following the DECnet nodename), `stat' may produce an error.
    * In that case, try to open the file before giving up.
    **************************************************************************/
    if (strstr(pathX,"::") != NULL) {
      FILE *fp = fopen (pathX, READ_ONLY_a_mode);
      if (fp != NULL) {
        fclose (fp);
        return TRUE;
      }
    }
#endif
    return FALSE;
  }
#endif
}

/******************************************************************************
* DerefEnvVar. (Only used on UNIX/POSIXshell systems).
******************************************************************************/

#if defined(unix) || defined(posixSHELL)
static void DerefEnvVar (shortP, longP)
char *shortP;			/* Short path (with environment variables). */
char longP[DU_MAX_PATH_LEN+1];	/* Long path (with environment variables
				   dereferenced). */
{
  char *Sptr = shortP;    /* Current position in "short" path. */
  char *Lptr = longP;     /* End position in "long" path. */
  char *DOLLARptr;        /* Pointer to '$' in "short" path. */
  char *ENVptr;           /* Pointer to environment variable in "short" path.*/
  char *DEREFptr;         /* Pointer to dereferenced environment variable
			     "value". */
  size_t len;
  char *ptr;
  char ENVvar[DU_MAX_ENVVAR_LEN + 1];     /* Environment variable. */
  for (*Lptr = NUL;;) {
     DOLLARptr = strchr (Sptr, '$');
     if (DOLLARptr != NULL) {
       len = DOLLARptr - Sptr;
       if (len > 0) {
         strcpyX (Lptr, Sptr, MINIMUM(len,DU_MAX_PATH_LEN));
         Lptr += len;
       }
       if (*(DOLLARptr + 1) == '{') {
         ENVptr = DOLLARptr + 2;
         ptr = strchr (ENVptr, '}');
         if (ptr != NULL) {
	   len = ptr - ENVptr;
	   Sptr = ptr + 1;
         }
         else {
	   len = strlen (ENVptr);
	   Sptr = ENVptr + len;
         }
       }
       else {
         ENVptr = DOLLARptr + 1;
         ptr = NextNonENVchar (ENVptr + 1);
         if (ptr != NULL) {
	   len = ptr - ENVptr;
	   Sptr = ptr;
         }
         else {
	   len = strlen (ENVptr);
	   Sptr = ENVptr + len;
         }
       }
       strcpyX (ENVvar, ENVptr, MINIMUM(len,DU_MAX_ENVVAR_LEN));
       DEREFptr = getenv (ENVvar);
       if (DEREFptr != NULL) {
         len = strlen (DEREFptr);
         strcpyX (Lptr, DEREFptr, MINIMUM(len,DU_MAX_PATH_LEN));
         Lptr += len;
       }
     }
     else {
       strcatX (Lptr, Sptr, DU_MAX_PATH_LEN);
       return;
     }
  }
}
#endif

/******************************************************************************
* NextNonENVchar.  (Only used on UNIX/POSIXshell systems).
******************************************************************************/

#if defined(unix) || defined(posixSHELL)
static char *NextNonENVchar (ptr)
char *ptr;
{
  Uchar *p;
  for (p = (Uchar *) ptr; *p != NUL; p++) {
    if (*p <= '/') return ((char *) p);
    if (':' <= *p && *p <= '@') return ((char *) p);
    if ('[' <= *p && *p <= '^') return ((char *) p);
    if (*p == '`') return ((char *) p);
    if ('{' <= *p) return ((char *) p);
  }
  return NULL;
}
#endif

/******************************************************************************
* MacDirSpecified.  (Only used on Macintosh systems).
* WARNING - Using `PBHGetVol' caused some really weird things to happen.  Use
* `HGetVol' instead.
******************************************************************************/

#if defined(mac)
STATICforIDL Logical MacDirSpecified (path, vRefNum, dirID)
char *path;		/* In: Pathname to be checked. */
short *vRefNum;		/* Out: Volume reference number. */
long *dirID;		/* Out: Directory identifier. */
{
  char pathX[DU_MAX_PATH_LEN+1];
  OSErr rCode;
  short tVRefNum;
  long tDirID;
  ExpandPath (path, pathX);
  /****************************************************************************
  * Check for no directory specified (which implies the current working
  * directory) or just `:' (which also implies the current working directory).
  ****************************************************************************/
  if (NULstring(pathX) || !strcmp(pathX,":")) {
    rCode = HGetVol (NULL, &tVRefNum, &tDirID);
    if (rCode != noErr) return FALSE;
  }
  else {
    /**************************************************************************
    * Some sort of pathname has been specified (full or partial).
    **************************************************************************/
    HParamBlockRec hParms;
    CInfoPBRec cParms;
    long topDirID;		/* Top directory ID of partial pathname. */
    Str255 tempS;
    if (pathX[0] == ':') {
      /*****************************************************************
      * Partial pathname.
      *****************************************************************/
      rCode = HGetVol (NULL, &tVRefNum, &topDirID);
      if (rCode != noErr) return FALSE;
    }
    else {
      /*****************************************************************
      * Full pathname.
      *****************************************************************/
      hParms.volumeParam.ioNamePtr = tempS;
      strcpyX ((char *) hParms.volumeParam.ioNamePtr, pathX, 255);
      CtoPstr ((char *) hParms.volumeParam.ioNamePtr);
      hParms.volumeParam.ioVRefNum = 0;
      hParms.volumeParam.ioVolIndex = -1;
      rCode = PBHGetVInfo (&hParms, FALSE);
      if (rCode == noErr)
        tVRefNum = hParms.volumeParam.ioVRefNum;
      else
        return FALSE;
      topDirID = 0;
    }
    cParms.hFileInfo.ioNamePtr = tempS;
    strcpyX ((char *) cParms.hFileInfo.ioNamePtr, pathX, 255);
    CtoPstr ((char *) cParms.hFileInfo.ioNamePtr);
    cParms.hFileInfo.ioVRefNum = tVRefNum;
    cParms.hFileInfo.ioFDirIndex = 0;
    cParms.hFileInfo.ioDirID = topDirID;
    rCode = PBGetCatInfo (&cParms, FALSE);
    if (rCode == noErr)
      tDirID = cParms.hFileInfo.ioDirID;
    else
      return FALSE;
    if (BITCLR(cParms.hFileInfo.ioFlAttrib,4)) return FALSE;	/* `Dir' bit */
  }
  /****************************************************************************
  * Pass back volume reference number and directory identifier.
  ****************************************************************************/
  ASSIGNnotNULL (vRefNum, tVRefNum)
  ASSIGNnotNULL (dirID, tDirID)
  return TRUE;
}
#endif
