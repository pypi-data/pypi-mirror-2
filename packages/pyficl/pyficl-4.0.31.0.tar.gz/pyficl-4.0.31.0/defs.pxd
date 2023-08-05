cdef extern from "ficl.h":
  ctypedef struct ficlOutputFunction:
    pass
  cdef struct ficlCallback:
    ficlOutputFunction textOut
    ficlOutputFunction errorOut
  cdef struct ficlSystem:
    pass
  cdef struct ficlVm:
    ficlCallback callback
  cdef struct ficlWord:
    pass
  cdef struct ficlStack:
    pass
  cdef struct ficlDictionary:
    pass
  ctypedef struct ficlPrimitive:
    pass
  ctypedef union ficlCell:
    int i
    void *p
    float f
  ctypedef struct ficlSystemInformation:
    int dictionarySize
    int stackSize
    ficlOutputFunction textOut
    ficlOutputFunction errorOut
  cdef char* FICL_VERSION

  void ficlSystemInformationInitialize(ficlSystemInformation*p)
  ficlSystem* ficlSystemCreate(ficlSystemInformation*p)
  void ficlSystemDestroy(ficlSystem*)
  void ficlSystemCompileExtras(ficlSystem*)
  ficlVm* ficlSystemCreateVm(ficlSystem*)
  ficlDictionary* ficlSystemGetDictionary(ficlSystem*)
  ficlWord *ficlSystemLookup(ficlSystem *system, char *name)

  ficlWord *ficlDictionarySetPrimitive(ficlDictionary*, char*, void (*)(ficlVm*), int)
  void ficlDictionaryAppendUnsigned(ficlDictionary*, unsigned int)
  void ficlDictionaryAppendCell(ficlDictionary*, ficlCell)
  void ficlDictionaryUnsmudge(ficlDictionary*)
  ficlWord *ficlDictionaryAppendPrimitive(ficlDictionary *dictionary, 
                           char *name, 
                           ficlPrimitive pCode, 
                           int flags)

  int ficlVmEvaluate(ficlVm*, char*)
  ficlStack* ficlVmGetDataStack(ficlVm*)
  ficlStack* ficlVmGetReturnStack(ficlVm*)
  ficlStack* ficlVmGetFloatStack(ficlVm*)
  int ficlVmExecuteXT(ficlVm*, ficlWord*)

  int ficlStackDepth(ficlStack*)
  void ficlStackDrop(ficlStack*)
  ficlCell ficlStackFetch(ficlStack*, int)
  void ficlStackPush(ficlStack*, ficlCell)
  ficlCell ficlStackPop(ficlStack *stack)
  void ficlStackReset(ficlStack*)

  int FICL_VM_STATUS_OUT_OF_TEXT
  int FICL_VM_STATUS_ERROR_EXIT
  int FICL_VM_STATUS_USER_EXIT
  int FICL_VM_STATUS_ABORT
  int FICL_DEFAULT_STACK_SIZE
  int FICL_DEFAULT_DICTIONARY_SIZE
  int FICL_DEFAULT_ENVIRONMENT_SIZE
  int FICL_WORD_DEFAULT
  int ficlInstructionColonParen
  int FICL_WORD_DEFAULT
  int FICL_WORD_SMUDGED
  int ficlInstructionLiteralParen
  int ficlInstructionSemiParen
