/******************************************************************************
*
*  NSSDC/CDF                                            Virtual stream file.
*
*  Version 4.6, 29-Sep-95, Hughes STX.
*
*  Modification history:
*
*   V1.0  22-Jan-91, J Love     Original version (developed for CDF V2.0).
*   V2.0  12-Mar-91, J Love     All fixes to V1.x.  Modified vread and vwrite
*                               to buffer only when necessary.
*   V3.0  14-May-91, J Love     Added caching (for CDF V2.1).
*   V3.1  31-Jul-91, J Love     Added veof.  Added 'memmove' for UNIX.  Added
*                               "deq - default extension quantity" if VMS.
*                               Changed algorithm that looks for bufferN.
*                               Added number of CACHE buffers as a parameter
*                               specified in 'Vopen'.  Renamed functions to
*                               avoid collisions on SGi/IRIX.
*   V3.2  15-Aug-91, J Love     Changed for IBM-PC/MS-DOS port.
*   V4.0  20-May-92, J Love     IBM PC port/CDF V2.2.
*   V4.1  29-Sep-92, J Love     CDF V2.3.  Dealt with EOFs not at 512-byte
*                               boundaries (when FTPed from a UNIX machine).
*   V4.2  21-Dec-93, J Love     CDF V2.4.
*   V4.3  12-Dec-94, J Love     CDF V2.5.
*   V4.3a 19-Jan-95, J Love     IRIX 6.0 (64-bit).
*   V4.3b 24-Feb-95, J Love     Solaris 2.3 IDL i/f.
*   V4.4   7-Jun-95, J Love     Virtual memory under Microsoft C 7.00.
*   V4.5  25-Jul-95, J Love     More virtual memory under Microsoft C 7.00.
*   V4.6  29-Sep-95, J Love     Improved performance...on non-VMS systems don't
*                               extend files a block at a time, don't clear
*                               bytes (anywhere), etc.
*
******************************************************************************/

/******************************************************************************
* Include files.
******************************************************************************/

#include "cdflib.h"

/******************************************************************************
* Local macros/typedef's.
******************************************************************************/

#define CLEAR_BYTES     0

#if defined(vms)
#define EXTEND_FILE     1
#else
#define EXTEND_FILE     0
#endif

#define LASTphyBLOCKn(vFp) BOO(vFp->phyEof == 0, (-1), ((vFp->phyEof - 1)/512))

#if defined(MICROSOFTC_700) && INCLUDEvMEMORY
#define CACHEbufferREADfrom(cache) \
BOO(useVmem,LoadVMemory((MemHandle)cache->ptr,FALSE),cache->ptr)
#define CACHEbufferWRITEto(cache) \
BOO(useVmem,LoadVMemory((MemHandle)cache->ptr,TRUE),cache->ptr)
#else
#define CACHEbufferREADfrom(cache) cache->ptr
#define CACHEbufferWRITEto(cache) cache->ptr
#endif

/******************************************************************************
* Local function prototypes.
******************************************************************************/

static Logical FlushCache PROTOARGs((vFILE *vFp, vCACHE *firstCache));
static Logical FreeCache PROTOARGs((vCACHE *firstCache));
static vCACHE *FindCache PROTOARGs((vFILE *vFp, long blockN));
static Logical vRead PROTOARGs((
  long offset, void *buffer, size_t nBytes, vFILE *vFp
));
static Logical vWrite PROTOARGs((
  long offset, void *buffer, size_t nBytes, vFILE *vFp
));
static vCACHE *AllocateBuffer PROTOARGs((vFILE *vFp));
static vCACHE *PageIn PROTOARGs((vFILE *vFp, long blockN));
static Logical WriteBlockFromCache PROTOARGs((
  vFILE *vFp, vCACHE *cache, size_t Nbytes
));
static Logical WriteBlockFromBuffer PROTOARGs((
  vFILE *vFp, long blockN, void *buffer, size_t Nbytes
));
#if EXTEND_FILE
static Logical ExtendFile PROTOARGs((vFILE *vFp, long toBlockN));
#endif

/******************************************************************************
* FindCache.
******************************************************************************/

static vCACHE *FindCache (vFp, blockN)
vFILE *vFp;
long blockN;
{
  vCACHE *cache = vFp->cacheHead;
  while (cache != NULL) {
    if (cache->blockN == blockN) {
      if (cache != vFp->cacheHead) {
	if (cache == vFp->cacheTail) {
	  cache->prev->next = NULL;
	  vFp->cacheTail = cache->prev;
	}
	else {
	  cache->next->prev = cache->prev;
	  cache->prev->next = cache->next;
	}
	vFp->cacheHead->prev = cache;
	cache->next = vFp->cacheHead;
	vFp->cacheHead = cache;
	cache->prev = NULL;
      }
      return cache;
    }
    cache = cache->next;
  }
  return NULL;
}

/******************************************************************************
* FlushCache.
*     Write cache buffers to disk from the specified starting buffer to the
* last buffer.
******************************************************************************/

static Logical FlushCache (vFp, firstCache)
vFILE *vFp;             /* Pointer to vFILE structure. */
vCACHE *firstCache;     /* Pointer to the first cache structure to flush. */
{
  vCACHE *cache; long nBytes;
  for (cache = firstCache; cache != NULL; cache = cache->next) {
     if (cache->modified) {
#if defined(vms)
       nBytes = nCACHE_BUFFER_BYTEs;
#else
       nBytes = vFp->eof - (cache->blockN * nCACHE_BUFFER_BYTEs);
       nBytes = MINIMUM (nBytes, nCACHE_BUFFER_BYTEs);
#endif
       if (!WriteBlockFromCache(vFp,cache,(size_t)nBytes)) return FALSE;
       cache->modified = FALSE;
     }
  }
  return TRUE;
}

/******************************************************************************
* FreeCache.
******************************************************************************/

static Logical FreeCache (firstCache)
vCACHE *firstCache;     /* Pointer to the first cache structure to free. */
{
  vCACHE *cache = firstCache;
  while (cache != NULL) {
    vCACHE *nextCache = cache->next;
#if defined(MICROSOFTC_700) && INCLUDEvMEMORY
    if (useVmem)
      FreeVMemory ((MemHandle) cache->ptr);
    else
#endif
      FreeMemory (cache->ptr, NULL);
    FreeMemory (cache, NULL);
    cache = nextCache;
  }
  return TRUE;
}

/******************************************************************************
* AllocateBuffer.
*     Allocate a cache structure to use.  It may be necessary to page out a
* block to the file.  Returns a pointer to the allocated cache structure (or
* NULL if an error occurred).
******************************************************************************/

static vCACHE *AllocateBuffer (vFp)
vFILE *vFp;
{
  vCACHE *cache; long nBytes;
#if !defined(vms)
  long offset;
#endif
  /****************************************************************************
  * Check if a new cache structure can be allocated.  If the allocation(s)
  * fail, process as if the maximum number of cache buffers has already been
  * reached.
  ****************************************************************************/
  if (vFp->vStats.nBuffers < vFp->vStats.maxBuffers) {
    cache = (vCACHE *) AllocateMemory (sizeof(vCACHE), NULL);
    if (cache != NULL) {
#if defined(MICROSOFTC_700) && INCLUDEvMEMORY
      if (useVmem)
	cache->ptr = (void *) AllocateVMemory (nCACHE_BUFFER_BYTEs);
      else
#endif
	cache->ptr = AllocateMemory (nCACHE_BUFFER_BYTEs, NULL);
      if (cache->ptr != NULL) {
	if (vFp->cacheHead == NULL) {
	  vFp->cacheHead = cache;
	  vFp->cacheTail = cache;
	  cache->next = NULL;
	  cache->prev = NULL;
	}
	else {
	  vFp->cacheHead->prev = cache;
	  cache->next = vFp->cacheHead;
	  vFp->cacheHead = cache;
	  cache->prev = NULL;
	}
	(vFp->vStats.nBuffers)++;
	return cache;
      }
      else {
	FreeMemory (cache, NULL);
	if (vFp->vStats.nBuffers == 0) return NULL;
      }
    }
  }
  /****************************************************************************
  * The maximum number of cache buffers have already been created.  Scan the
  * linked list of cache structures searching for the oldest buffer which has
  * not been modified.  If one is found, it is moved to the head of the linked
  * list.
  ****************************************************************************/
  for (cache = vFp->cacheTail; cache != NULL; cache = cache->prev) {
     if (!cache->modified) {
       if (cache != vFp->cacheHead) {
	 if (cache == vFp->cacheTail) {
	   cache->prev->next = NULL;
	   vFp->cacheTail = cache->prev;
	 }
	 else {
	   cache->prev->next = cache->next;
	   cache->next->prev = cache->prev;
	 }
	 vFp->cacheHead->prev = cache;
	 cache->next = vFp->cacheHead;
	 vFp->cacheHead = cache;
	 cache->prev = NULL;
       }
       return cache;
     }
  }
  /****************************************************************************
  * An unmodified buffer was not found.  The last buffer on the linked list
  * will be paged back out to the file and then this cache structure is moved
  * to the head of the linked list.
  ****************************************************************************/
  cache = vFp->cacheTail;
#if defined(vms)
  nBytes = nCACHE_BUFFER_BYTEs;
#else
  offset = nCACHE_BUFFER_BYTEs * cache->blockN;
  nBytes = vFp->eof - offset;
  nBytes = MINIMUM (nBytes, nCACHE_BUFFER_BYTEs);
#endif
  if (!WriteBlockFromCache(vFp,cache,(size_t)nBytes)) return NULL;
  if (cache != vFp->cacheHead) {
    cache->prev->next = NULL;
    vFp->cacheTail = cache->prev;
    vFp->cacheHead->prev = cache;
    cache->next = vFp->cacheHead;
    vFp->cacheHead = cache;
    cache->prev = NULL;
  }
  (vFp->vStats.nPageOuts)++;
  return cache;
}

/******************************************************************************
* ExtendFile.  Extend the file to a specified number of blocks.
******************************************************************************/

#if EXTEND_FILE
static Logical ExtendFile (vFp, toBlockN)
vFILE *vFp;
long toBlockN;
{
  vCACHE *cache; long blockN;
  /****************************************************************************
  * First check to see if the physical end-of-file must be extended out to the
  * next multiple of the cache/block size.
  ****************************************************************************/
  if (vFp->phyEof > 0) {
    long lastPhyBlockN = LASTphyBLOCKn (vFp);
    long nBytes = vFp->phyEof - (nCACHE_BUFFER_BYTEs * lastPhyBlockN);
    if (nBytes < nCACHE_BUFFER_BYTEs) {
      cache = FindCache (vFp, lastPhyBlockN);
      if (cache != NULL) {
	void *buffer = CACHEbufferREADfrom (cache);
	if (buffer == NULL) return FALSE;
	if (!vWrite(nCACHE_BUFFER_BYTEs * lastPhyBlockN,
		    buffer,nCACHE_BUFFER_BYTEs,vFp)) return FALSE;
	cache->modified = FALSE;
      }
      else {
	Byte buffer[nCACHE_BUFFER_BYTEs];
	if (!vRead(nCACHE_BUFFER_BYTEs * lastPhyBlockN,
		   buffer,(size_t)nBytes,vFp)) return FALSE;
#if CLEAR_BYTES
	ClearBytes (buffer, (int) nBytes, nCACHE_BUFFER_BYTEs - 1);
#endif
	if (!vWrite(nCACHE_BUFFER_BYTEs * lastPhyBlockN,
		    buffer,nCACHE_BUFFER_BYTEs,vFp)) return FALSE;
      }
      vFp->phyEof = nCACHE_BUFFER_BYTEs * (lastPhyBlockN + 1);
    }
  }
  /****************************************************************************
  * Then extend the file the remaining blocks.
  ****************************************************************************/
  for (blockN = LASTphyBLOCKn(vFp) + 1; blockN <= toBlockN; blockN++) {
     cache = FindCache (vFp, blockN);
     if (cache != NULL) {
       void *buffer = CACHEbufferREADfrom (cache);
       if (buffer == NULL) return FALSE;
       if (!vWrite(nCACHE_BUFFER_BYTEs * blockN,
		   buffer,nCACHE_BUFFER_BYTEs,vFp)) return FALSE;
       cache->modified = FALSE;
     }
     else {
       Byte buffer[nCACHE_BUFFER_BYTEs];
#if CLEAR_BYTES
       ClearBytes (buffer, 0, nCACHE_BUFFER_BYTEs - 1);
#endif
       if (!vWrite(nCACHE_BUFFER_BYTEs * blockN,
		   buffer,nCACHE_BUFFER_BYTEs,vFp)) return FALSE;
     }
     vFp->phyEof = nCACHE_BUFFER_BYTEs * (blockN + 1);
  }
  return TRUE;
}
#endif

/******************************************************************************
* PageIn.
*    Page in a block from the file.  Returns pointer to cache structure used
* (or NULL if an error occurred).
******************************************************************************/

static vCACHE *PageIn (vFp, blockN)
vFILE *vFp;
long blockN;
{
  long offset, nBytes; vCACHE *cache; void *buffer;
  cache = AllocateBuffer (vFp);
  if (cache == NULL) return NULL;
  offset = blockN * nCACHE_BUFFER_BYTEs;
  nBytes = vFp->phyEof - offset;
  nBytes = MINIMUM (nBytes, nCACHE_BUFFER_BYTEs);
  buffer = CACHEbufferWRITEto (cache);
  if (buffer == NULL) return NULL;
  if (!vRead(offset,buffer,(size_t)nBytes,vFp)) return NULL;
#if CLEAR_BYTES
  ClearBytes (buffer, (int) nBytes, nCACHE_BUFFER_BYTEs - 1);
#endif
  cache->blockN = blockN;
  cache->modified = FALSE;
  (vFp->vStats.nPageIns)++;
  return cache;
}

/******************************************************************************
* WriteBlockFromCache.
*     Write a block out to the file from a cache buffer.  Returns TRUE if
* successful, FALSE if an error occurred.
******************************************************************************/

static Logical WriteBlockFromCache (vFp, cache, nBytes)
vFILE *vFp;
vCACHE *cache;
size_t nBytes;
{
  long offset; void *buffer;
  offset = nCACHE_BUFFER_BYTEs * cache->blockN;
#if EXTEND_FILE
  if (offset > vFp->phyEof) {
    if (!ExtendFile(vFp,cache->blockN-1)) return FALSE;
  }
#endif
  buffer = CACHEbufferREADfrom (cache);
  if (buffer == NULL) return FALSE;
  if (!vWrite(offset,buffer,nBytes,vFp)) return FALSE;
  vFp->phyEof = MAXIMUM (vFp->phyEof, (offset + nBytes));
  return TRUE;
}

/******************************************************************************
* WriteBlockFromBuffer.
*     Write a block out to the file from the caller's buffer.  Returns TRUE
* if successful, FALSE if an error occurred.
******************************************************************************/

static Logical WriteBlockFromBuffer (vFp, blockN, buffer, nBytes)
vFILE *vFp;
long blockN;
void *buffer;
size_t nBytes;
{
  long offset = nCACHE_BUFFER_BYTEs * blockN;
#if EXTEND_FILE
  if (offset > vFp->phyEof) {
    if (!ExtendFile(vFp,blockN-1)) return FALSE;
  }
#endif
  if (!vWrite(offset,buffer,nBytes,vFp)) return FALSE;
  vFp->phyEof = MAXIMUM (vFp->phyEof, (offset + nBytes));
  return TRUE;
}

/******************************************************************************
* vRead.
******************************************************************************/

static Logical vRead (offset, buffer, nBytes, vFp)
long offset;
void *buffer;
size_t nBytes;
vFILE *vFp;
{
  int tryN;
  (vFp->vStats.nBlockReads)++;
  for (tryN = 1; tryN <= vMAX_TRYs; tryN++) {
     if (fseek(vFp->fp,offset,vSEEK_SET) == EOF) return FALSE;
     if (fread(buffer,nBytes,1,vFp->fp) == 1) return TRUE;
  }
  return FALSE;
}

/******************************************************************************
* vWrite.
******************************************************************************/

static Logical vWrite(offset,buffer,nBytes,vFp)
long offset;
void *buffer;
size_t nBytes;
vFILE *vFp;
{
  int tryN;
  (vFp->vStats.nBlockWrites)++;
  for (tryN = 1; tryN <= vMAX_TRYs; tryN++) {
     if (fseek(vFp->fp,offset,vSEEK_SET) == EOF) return FALSE;
     if (fwrite(buffer,nBytes,1,vFp->fp) == 1) return TRUE;
  }
  return FALSE;
}

/******************************************************************************
* V_open - open the file and setup V structure.
******************************************************************************/

STATICforIDL vFILE *V_open (file_spec, a_mode)
char *file_spec;        /* File specification. */
char *a_mode;           /* Access mode. */
{
  FILE *fp;             /* Temporary file pointer. */
  vFILE *vFp;           /* Pointer to V structure. */
#if defined(vms)
  char mrs[10+1];       /* Maximum record size. */
  char deq[10+1];       /* Default allocation quantity. */
  struct stat st;       /* Status block from `stat'. */
#endif

  /****************************************************************************
  * Open file (in fixed length record mode if VMS).
  ****************************************************************************/

#if defined(vms)
  sprintf (mrs, "mrs=%d", nCACHE_BUFFER_BYTEs);
  sprintf (deq, "deq=%d", VMS_DEFAULT_nALLOCATION_BLOCKS);
  fp = fopen (file_spec, a_mode, "rfm=fix", mrs, deq);
#else
  fp = fopen (file_spec, a_mode);
#endif
 if (fp == NULL) return NULL;
 
#if defined(vms)
  /****************************************************************************
  * If the file is being opened in a mode which may require it to be extended
  * (`r+' [read/write] or `a/a+' [append]), check that the EOF offset in the
  * last block is zero (0).  If not, rewrite the last block out to the end
  * (blocks are 512 bytes long).  `r' is not checked because it is read only.
  * `w/w+' is not checked because a new file (with EOF == 0) will have been
  * created.
  ****************************************************************************/
  if (strstr(a_mode,"r+") || strchr(a_mode,'a')) {
    long eof; size_t EOFoffsetInBlock;
    if (fseek(fp,0,vSEEK_END) == EOF) {
      fclose (fp);
      return NULL;
    }
    eof = ftell (fp);
    if (eof == EOF) {
      fclose (fp);
      return NULL;
    }
    EOFoffsetInBlock = eof % 512;
    if (EOFoffsetInBlock != 0) {
      long offsetToLastBlock; char buffer[512]; size_t numitems; int i;
      offsetToLastBlock = 512 * (eof / 512);
      if (fseek(fp,offsetToLastBlock,vSEEK_SET) == EOF) {
	fclose (fp);
	return NULL;
      }
      for (i = 0; i < 512; i++) buffer[i] = 0;
      if (fread(buffer,EOFoffsetInBlock,1,fp) != 1) {
	fclose (fp);
	return NULL;
      }
      if (fseek(fp,offsetToLastBlock,vSEEK_SET) == EOF) {
	fclose (fp);
	return NULL;
      }
      if (fwrite(buffer,512,1,fp) != 1) {
	fclose (fp);
	return NULL;
      }
      if (fclose(fp) == EOF) {
	fclose (fp);
	return NULL;
      }
      fp = fopen (file_spec, a_mode, "rfm=fix", mrs, deq);
      if (fp == NULL) return NULL;
    }
  }
#endif

  /****************************************************************************
  * Allocate and load vFILE structure.
  ****************************************************************************/

  vFp = (vFILE *) AllocateMemory (sizeof(vFILE), NULL);
  if (vFp == NULL) {
    fclose (fp);
    return NULL;
  }

  vFp->magic_number = VSTREAM_MAGIC_NUMBER;
  vFp->fp = fp;
  vFp->error = FALSE;
  vFp->cacheHead = NULL;
  vFp->cacheTail = NULL;
  vFp->vStats.maxBuffers = DEFAULT_nCACHE_BUFFERs;
  vFp->vStats.nBuffers = 0;
  vFp->vStats.nBlockReads = 0;
  vFp->vStats.nBlockWrites = 0;
  vFp->vStats.nV_reads = 0;
  vFp->vStats.nV_writes = 0;
  vFp->vStats.nPageIns = 0;
  vFp->vStats.nPageOuts = 0;

  /****************************************************************************
  * Determine length of file and set current offset.
  ****************************************************************************/

#if defined(vms)
  /****************************************************************************
  * This method is used on VMS systems in case the file is on a CD-ROM.  Some
  * VMS CD-ROM drivers do not correctly handle the EOF marker of a file.
  ****************************************************************************/
  if (stat(file_spec,&st) != 0) {
    fclose (vFp->fp);
    FreeMemory (vFp, NULL);
    return NULL;
  }
  vFp->eof = st.st_size;
  vFp->phyEof = st.st_size;
#else
  /****************************************************************************
  * This method is used everywhere else.
  ****************************************************************************/
  if (fseek(vFp->fp,0,vSEEK_END) == EOF) {
    fclose (vFp->fp);
    FreeMemory (vFp, NULL);
    return NULL;
  }
  vFp->eof = ftell (vFp->fp);
  if (vFp->eof == EOF) {
    fclose (vFp->fp);
    FreeMemory (vFp, NULL);
    return NULL;
  }
  vFp->phyEof = vFp->eof;
#endif

  if (strchr(a_mode,'a') == NULL)
    vFp->offset = 0;
  else
    vFp->offset = vFp->eof;

  /****************************************************************************
  * Return pointer to V structure.
  ****************************************************************************/

  return vFp;
}

/******************************************************************************
* V_setcache - set number of cache buffers.
*     This can be done at any time after the file is opened.  Note that in
* some cases the new cache size may be the same as the old cache size (do
* nothing).
******************************************************************************/

STATICforIDL int V_setcache (vFp, maxBuffers)
vFILE *vFp;             /* Pointer to vFILE structure. */
int maxBuffers;         /* New maximum number of cache buffers. */
{
  if (vFp == NULL) return EOF;
  if (vFp->magic_number != VSTREAM_MAGIC_NUMBER) return EOF;
  if (vFp->error) return EOF;
  if (maxBuffers < 1) return EOF;
  if (maxBuffers > vFp->vStats.maxBuffers) {
    /**************************************************************************
    * The number of cache buffers is increasing.
    **************************************************************************/
    vFp->vStats.maxBuffers = maxBuffers;
  }
  else {
    if (maxBuffers < vFp->vStats.maxBuffers) {
      /************************************************************************
      * The number of cache buffers is decreasing - flush to disk and free
      * the buffers which are going away.
      ************************************************************************/
      vCACHE *cache; int count;
      if (vFp->vStats.nBuffers > maxBuffers) {
	for (count = 1, cache = vFp->cacheHead; count < maxBuffers; count++) {
	   cache = cache->next;
	}
	if (!FlushCache(vFp,cache->next)) return EOF;
	FreeCache (cache->next);
	cache->next = NULL;
	vFp->cacheTail = cache;
	vFp->vStats.nBuffers = maxBuffers;
      }
      vFp->vStats.maxBuffers = maxBuffers;
    }
  }
  return 0;
}

/******************************************************************************
* V_seek - seek to a position in the file.
******************************************************************************/

STATICforIDL int V_seek (vFp, offset, direction)
vFILE *vFp;             /* Pointer to vFILE structure. */
long offset;            /* New current file offset. */
int direction;          /* Reference for offset. */
{
  if (vFp == NULL) return EOF;
  if (vFp->magic_number != VSTREAM_MAGIC_NUMBER) return EOF;
  if (vFp->error) return EOF;
  switch (direction) {
    case vSEEK_SET:
      if (offset < 0) return EOF;
      vFp->offset = offset;
      return 0;
    case vSEEK_CUR:
      if (vFp->offset + offset < 0) return EOF;
      vFp->offset += offset;
      return 0;
    case vSEEK_END:
      vFp->offset = vFp->eof;
      return 0;
  }
  return EOF;
}

/******************************************************************************
* V_tell - return current offset (position) in file.
*   This is the byte offset one past the last byte written.
******************************************************************************/

STATICforIDL long V_tell (vFp)
vFILE *vFp;             /* Pointer to vFILE structure. */
{
  if (vFp == NULL) return EOF;
  if (vFp->magic_number != VSTREAM_MAGIC_NUMBER) return EOF;
  if (vFp->error) return EOF;
  return vFp->offset;
}

/******************************************************************************
* V_eof.
* Check if at the end of the file.  If so, return TRUE.  If not, return FALSE.
* This is different than the `feof' function in that a read at the EOF doesn't
* have to occur before `V_eof' will return TRUE.  (Perhaps `feof' has a bug.)
******************************************************************************/

STATICforIDL int V_eof (vFp)
vFILE *vFp;             /* Pointer to vFILE structure. */
{
  if (vFp == NULL) return EOF;
  if (vFp->magic_number != VSTREAM_MAGIC_NUMBER) return FALSE;
  if (vFp->error) return FALSE;
  return BOO(vFp->offset < vFp->eof,FALSE,TRUE);
}

/******************************************************************************
* V_read - read from the file.
******************************************************************************/

STATICforIDL size_t V_read (buffer, item_size, n_items, vFp)
void *buffer;           /* Pointer to buffer. */
size_t item_size;       /* Size (in bytes) of each item to read. */
size_t n_items;         /* Number of items to read. */
vFILE *vFp;             /* Pointer to vFILE structure. */
{
  size_t nBytes;        /* Total number of bytes to read. */
  long firstBlockN;     /* First block involved in read. */
  long lastBlockN;      /* Last block involved in read. */
  int bufferOffset;     /* Offset (bytes) into buffer. */
  size_t xBytes;        /* Number of bytes in a transfer. */
  long blockN;          /* Block number in file (from 0). */
  vCACHE *cache;        /* Pointer to cache structure. */
  Byte *cBuffer;        /* Pointer to cache buffer. */
  /****************************************************************************
  * Validate read.
  ****************************************************************************/
  if (vFp == NULL) return 0;
  if (vFp->magic_number != VSTREAM_MAGIC_NUMBER) return 0;
  if (vFp->error) return 0;
  nBytes = item_size * n_items;
  if (nBytes < 1) return 0;
  if (vFp->offset + nBytes > vFp->eof) return 0;
  (vFp->vStats.nV_reads)++;
  /****************************************************************************
  * Read from first block.  This block is brought into the cache.
  ****************************************************************************/
  firstBlockN = vFp->offset / nCACHE_BUFFER_BYTEs;
  bufferOffset = (int) (vFp->offset % nCACHE_BUFFER_BYTEs);
  xBytes = MINIMUM (nBytes, nCACHE_BUFFER_BYTEs - bufferOffset);
  cache = FindCache (vFp, firstBlockN);
  if (cache == NULL) cache = PageIn (vFp, firstBlockN);
  if (cache == NULL) {
    vFp->error = TRUE;
    return 0;
  }
  cBuffer = CACHEbufferREADfrom (cache);
  if (cBuffer == NULL) {
    vFp->error = TRUE;
    return 0;
  }
  memmove (buffer, cBuffer + bufferOffset, xBytes);
  buffer = (char *) buffer + xBytes;
  /****************************************************************************
  * Read from blocks between first and last block.  These blocks are not
  * brought into the cache.
  ****************************************************************************/
  lastBlockN = (vFp->offset + nBytes - 1) / nCACHE_BUFFER_BYTEs;
  for (blockN = firstBlockN + 1; blockN < lastBlockN; blockN++) {
     cache = FindCache (vFp, blockN);
     if (cache != NULL) {
       cBuffer = CACHEbufferREADfrom (cache);
       if (cBuffer == NULL) {
	 vFp->error = TRUE;
	 return 0;
       }
       memmove (buffer, cBuffer, nCACHE_BUFFER_BYTEs);
     }
     else {
       if (!vRead(nCACHE_BUFFER_BYTEs * blockN,
		  buffer,nCACHE_BUFFER_BYTEs,vFp)) {
	 vFp->error = TRUE;
	 return 0;
       }
     }
     buffer = (char *) buffer + nCACHE_BUFFER_BYTEs;
  }
  /****************************************************************************
  * Read from last block.  This block is brought into the cache.
  ****************************************************************************/
  if (lastBlockN != firstBlockN) {
    xBytes = (size_t) (vFp->offset + nBytes -
		       (nCACHE_BUFFER_BYTEs * lastBlockN));
    cache = FindCache (vFp, lastBlockN);
    if (cache == NULL) {
      cache = PageIn (vFp, lastBlockN);
      if (cache == NULL) {
	vFp->error = TRUE;
	return 0;
      }
    }
    cBuffer = CACHEbufferREADfrom (cache);
    if (cBuffer == NULL) {
      vFp->error = TRUE;
      return 0;
    }
    memmove (buffer, cBuffer, xBytes);
  }
  /****************************************************************************
  * Increment current file offset.
  ****************************************************************************/
  vFp->offset += nBytes;
  return n_items;
}

/******************************************************************************
* V_write - write to the file.
******************************************************************************/

STATICforIDL size_t V_write (buffer, item_size, n_items, vFp)
void *buffer;           /* Pointer to buffer. */
size_t item_size;       /* Size (in bytes) of each item to write. */
size_t n_items;         /* Number of items to write. */
vFILE *vFp;             /* Pointer to vFILE structure. */
{
  size_t nBytes;        /* Total number of bytes in write. */
  long firstBlockN;     /* First block involved in write. */
  long lastBlockN;      /* Last block involved in write. */
  int bufferOffset;     /* Offset (bytes) into buffer. */
  long blockN;          /* Block number in file (from 0). */
  size_t xBytes;        /* Number of bytes in a transfer. */
  vCACHE *cache;        /* Pointer to cache structure. */
  Byte *cBuffer;        /* Pointer to cache buffer. */
  /****************************************************************************
  * Validate read.
  ****************************************************************************/
  if (vFp == NULL) return 0;
  if (vFp->magic_number != VSTREAM_MAGIC_NUMBER) return 0;
  if (vFp->error) return 0;
  nBytes = item_size * n_items;
  if (nBytes < 1) return 0;
  (vFp->vStats.nV_writes)++;
  /****************************************************************************
  * Write to first block.  This block is brought into the cache.
  ****************************************************************************/
  firstBlockN = vFp->offset / nCACHE_BUFFER_BYTEs;
  bufferOffset = (int) (vFp->offset % nCACHE_BUFFER_BYTEs);
  xBytes = MINIMUM (nBytes, nCACHE_BUFFER_BYTEs - bufferOffset);
  cache = FindCache (vFp, firstBlockN);
  if (cache == NULL) {
    if (firstBlockN <= LASTphyBLOCKn(vFp)) {
      cache = PageIn (vFp, firstBlockN);
      if (cache == NULL) {
	vFp->error = TRUE;
	return 0;
      }
    }
    else {
      cache = AllocateBuffer (vFp);
      if (cache == NULL) {
	vFp->error = TRUE;
	return 0;
      }
      cache->blockN = firstBlockN;
#if CLEAR_BYTES
      cBuffer = CACHEbufferWRITEto (cache);
      if (cBuffer == NULL) {
	vFp->error = TRUE;
	return 0;
      }
      ClearBytes (cBuffer, 0, bufferOffset - 1);
#endif
    }
  }
  cBuffer = CACHEbufferWRITEto (cache);
  if (cBuffer == NULL) {
    vFp->error = TRUE;
    return 0;
  }
  memmove (cBuffer + bufferOffset, buffer, xBytes);
  cache->modified = TRUE;
  vFp->eof = MAXIMUM (vFp->eof, vFp->offset + xBytes);
  buffer = (char *) buffer + xBytes;
  /****************************************************************************
  * Write to blocks between first and last block.  These blocks are not
  * brought into the cache (but they might already be there).
  ****************************************************************************/
  lastBlockN = (vFp->offset + nBytes - 1) / nCACHE_BUFFER_BYTEs;
  for (blockN = firstBlockN + 1; blockN < lastBlockN; blockN++) {
     cache = FindCache (vFp, blockN);
     if (cache != NULL) {
       cBuffer = CACHEbufferWRITEto (cache);
       if (cBuffer == NULL) {
	 vFp->error = TRUE;
	 return 0;
       }
       memmove (cBuffer, buffer, nCACHE_BUFFER_BYTEs);
       cache->modified = TRUE;
     }
     else {
       if (!WriteBlockFromBuffer(vFp,blockN,buffer,nCACHE_BUFFER_BYTEs)) {
	 vFp->error = TRUE;
	 return 0;
       }
     }
     vFp->eof = MAXIMUM (vFp->eof,(nCACHE_BUFFER_BYTEs * (blockN+1)));
     buffer = (char *) buffer + nCACHE_BUFFER_BYTEs;
  }
  /****************************************************************************
  * Write to last block.  This block is brought into the cache.
  ****************************************************************************/
  if (lastBlockN != firstBlockN) {
    xBytes = (size_t) (vFp->offset + nBytes -
		       (nCACHE_BUFFER_BYTEs * lastBlockN));
    cache = FindCache (vFp, lastBlockN);
    if (cache == NULL) {
      if (lastBlockN <= LASTphyBLOCKn(vFp)) {
	cache = PageIn (vFp, lastBlockN);
	if (cache == NULL) {
	  vFp->error = TRUE;
	  return 0;
	}
      }
      else {
	cache = AllocateBuffer (vFp);
	if (cache == NULL) {
	  vFp->error = TRUE;
	  return 0;
	}
	cache->blockN = lastBlockN;
#if CLEAR_BYTES
	cBuffer = CACHEbufferWRITEto (cache);
	if (cBuffer == NULL) {
	  vFp->error = TRUE;
	  return 0;
	}
	ClearBytes (cBuffer, (int) xBytes, nCACHE_BUFFER_BYTEs - 1);
#endif
      }
    }
    cBuffer = CACHEbufferWRITEto (cache);
    if (cBuffer == NULL) {
      vFp->error = TRUE;
      return 0;
    }
    memmove (cBuffer, buffer, xBytes);
    cache->modified = TRUE;
    vFp->eof = MAXIMUM (vFp->eof, (nCACHE_BUFFER_BYTEs * lastBlockN) + xBytes);
  }
  /****************************************************************************
  * Increment current file offset.
  ****************************************************************************/
  vFp->offset += nBytes;
  return n_items;
}

/******************************************************************************
* V_close - close the file.
******************************************************************************/

STATICforIDL int V_close (vFp, vStats)
vFILE *vFp;             /* Pointer to V structure. */
vSTATS *vStats;         /* Pointer to statistics structure. */
{
  Logical error = FALSE;        /* Has an error occurred? */
  /****************************************************************************
  * Check if a valid pointer to a vFILE structure.
  ****************************************************************************/
  if (vFp == NULL) return EOF;
  if (vFp->magic_number != VSTREAM_MAGIC_NUMBER) return EOF;
  /****************************************************************************
  * Write cache buffers (if no previous errors).
  ****************************************************************************/
  if (!FlushCache(vFp,vFp->cacheHead)) error = TRUE;
  /****************************************************************************
  * Close the file.
  ****************************************************************************/
  if (fclose(vFp->fp) == EOF) error = TRUE;
  /****************************************************************************
  * Pass back statistics (if requested).
  ****************************************************************************/
  if (vStats != NULL) memmove (vStats, &(vFp->vStats), sizeof(vSTATS));
  /****************************************************************************
  * Deallocate cache and vFILE structure.
  ****************************************************************************/
  FreeCache (vFp->cacheHead);
  FreeMemory (vFp, NULL);
  /****************************************************************************
  * Return status of fclose call.
  ****************************************************************************/
  return BOO(error,EOF,0);
}
