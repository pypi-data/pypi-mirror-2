/******************************************************************************
*
*  NSSDC/CDF                                            Memory Functions.
*
*  Version 1.1b, 22-Sep-95, Hughes STX.
*
*  Modification history:
*
*   V1.0  17-May-95, J Love     Original version.
*                    J Williams
*   V1.1  25-Jul-95, J Love     Simple virtual memory function.
*   V1.1a  6-Sep-95, J Love     Added `nBytes' to MEMLOG_.
*   V1.1b 22-Sep-95, J Love     Fixed call to `FreeVMemory'.
*
******************************************************************************/

#include "cdflib.h"

#define MEMLOG_ 0

/******************************************************************************
* Local structures.
******************************************************************************/

typedef struct memSTRUCT {
  void *ptr;
  struct memSTRUCT *next;
  size_t nBytes;
} MEM;

/******************************************************************************
* Local function prototypes.
******************************************************************************/

#if defined(MICROSOFTC_700) && INCLUDEvMEMORY
static Logical InitVMemory PROTOARGs((void));
static void TermVMemory PROTOARGs((void));
#endif

/******************************************************************************
* Global variables (local to this source file).
******************************************************************************/

static MEM *memHead = NULL;

/******************************************************************************
* AllocateMemory.
******************************************************************************/

STATICforIDL void *AllocateMemory (nBytes, fatalFnc)
size_t nBytes;
void (*fatalFnc) PROTOARGs((char *msg));
{
  MEM *mem;
  if (nBytes < 1) return NULL;
  mem = (MEM *) malloc (sizeof(MEM));
  if (mem == NULL) {
    if (fatalFnc != NULL) (*fatalFnc)("Unable to allocate memory buffer.");
    return NULL;
  }
  mem->ptr = (void *) malloc (nBytes);
  if (mem->ptr == NULL) {
    free (mem);
    if (fatalFnc != NULL) (*fatalFnc)("Unable to allocate memory buffer.");
    return NULL;
  }
  mem->nBytes = nBytes;
  mem->next = memHead;
  memHead = mem;
#if MEMLOG_
  {FILE *fp = fopen("mem.log","a");
   fprintf (fp, "Allocated: %d bytes at %p\n", mem->nBytes, mem->ptr);
   fclose (fp);}
#endif
  return mem->ptr;
}

/******************************************************************************
* ReallocateMemory.
******************************************************************************/

STATICforIDL void *ReallocateMemory (ptr, nBytes, fatalFnc)
void *ptr;
size_t nBytes;
void (*fatalFnc) PROTOARGs((char *msg));
{
  MEM *mem = memHead;
  while (mem != NULL) {
    if (mem->ptr == ptr) {
      void *newPtr = (void *) realloc (ptr, nBytes);
      if (newPtr == NULL) {
	if (fatalFnc != NULL) {
	  (*fatalFnc)("Unable to reallocate memory buffer.");
	}
	return NULL;
      }
      mem->ptr = newPtr;
      mem->nBytes = nBytes;
#if MEMLOG_
      {FILE *fp = fopen("mem.log","a");
       fprintf (fp, "Reallocated: %d bytes at %p\n", mem->nBytes, mem->ptr);
       fclose (fp);}
#endif
      return newPtr;
    }
    mem = mem->next;
  }
  if (fatalFnc != NULL) (*fatalFnc)("Unable to reallocate memory buffer.");
  return NULL;
}

/******************************************************************************
* FreeMemory.
*    If NULL is passed as the pointer to free, then free the entire list of
* allocated memory blocks.
******************************************************************************/

STATICforIDL int FreeMemory (ptr, fatalFnc)
void *ptr;
void (*fatalFnc) PROTOARGs((char *msg));
{
  if (ptr == NULL) {
    int count = 0;
    MEM *mem = memHead;
    while (mem != NULL) {
      MEM *memX = mem;
      mem = mem->next;
#if MEMLOG_
      {FILE *fp = fopen("mem.log","a");
       fprintf (fp, "Freeing (NULL): %p, %d bytes\n", memX->ptr, memX->nBytes);
       fclose (fp);}
#endif
      free (memX->ptr);
      free (memX);
      count++;
    }
    memHead = NULL;
    return count;
  }
  else {
    MEM *mem = memHead, *memPrev = NULL;
    while (mem != NULL) {
      if (mem->ptr == ptr) {
	MEM *memX = mem;
	if (memPrev == NULL)
	  memHead = mem->next;
	else
	  memPrev->next = mem->next;
#if MEMLOG_
	{FILE *fp = fopen("mem.log","a");
	 fprintf (fp, "Freed: %p, %d bytes\n", memX->ptr, memX->nBytes);
	 fclose (fp);}
#endif
	free (memX->ptr);
	free (memX);
	return 1;
      }
      memPrev = mem;
      mem = mem->next;
    }
    if (fatalFnc != NULL) (*fatalFnc)("Unable to free memory buffer.");
    return 0;
  }
}

/******************************************************************************
* CallocateMemory.
******************************************************************************/

STATICforIDL void *CallocateMemory (nObjects, objSize, fatalFnc)
size_t nObjects;
size_t objSize;
void (*fatalFnc) PROTOARGs((char *msg));
{
  size_t nBytes = nObjects * objSize, i;
  void *ptr = AllocateMemory (nBytes, fatalFnc);
  if (ptr != NULL) for (i = 0; i < nBytes; i++) ((Byte *) ptr)[i] = 0;
  return ptr;
}

/******************************************************************************
* InitVMemory.
*   NOTE: It is a mystery as to why values of `maxParagraphs' other than 128
* (or near 128) cause allocation/loading failures (as well as other nasty
* things).  Be a hero, solve the mystery...
******************************************************************************/

#if defined(MICROSOFTC_700) && INCLUDEvMEMORY
static Logical InitVMemory () {
  unsigned int maxParagraphs = (unsigned int) (vMemSize / 16);
  if (!_vheapinit(0U,maxParagraphs,vMemMask)) return FALSE;
  return TRUE;
}
#endif

/******************************************************************************
* TermVMemory.
******************************************************************************/

#if defined(MICROSOFTC_700) && INCLUDEvMEMORY
static void TermVMemory () {
  _vheapterm();
}
#endif

/******************************************************************************
* AllocateVMemory.
******************************************************************************/

#if defined(MICROSOFTC_700) && INCLUDEvMEMORY
STATICforIDL MemHandle AllocateVMemory (nBytes)
size_t nBytes;
{
  MemHandle handle;
  static int first = TRUE;
  if (first) {
    first = FALSE;
    if (!InitVMemory()) return NULL;
    _fatexit (TermVMemory);
  }
  if ((handle = _vmalloc(nBytes)) == _VM_NULL) return NULL;
  return handle;
}
#endif

/******************************************************************************
* LoadVMemory.
******************************************************************************/

#if defined(MICROSOFTC_700) && INCLUDEvMEMORY
STATICforIDL void *LoadVMemory (handle, writeFlag)
MemHandle handle;
Logical writeFlag;      /* TRUE if virtual memory will be written to. */
{
  void *buffer = _vload(handle,BOO(writeFlag,_VM_DIRTY,_VM_CLEAN));
  if (buffer == NULL) {
    FreeVMemory (handle);
    return NULL;
  }
  return buffer;
}
#endif

/******************************************************************************
* FreeVMemory.
******************************************************************************/

#if defined(MICROSOFTC_700) && INCLUDEvMEMORY
STATICforIDL int FreeVMemory (handle)
MemHandle handle;
{
  _vfree (handle);
  return 1;
}
#endif
