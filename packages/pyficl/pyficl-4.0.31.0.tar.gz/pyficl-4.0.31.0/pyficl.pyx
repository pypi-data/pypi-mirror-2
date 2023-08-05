"""
:mod:`pyficl` --- Python interface to FICL
==========================================
"""

import sys
cimport defs

__version__ = defs.FICL_VERSION

cdef extern from "Python.h":
  cdef void Py_INCREF( object )
  cdef object PyString_FromStringAndSize(char *v, Py_ssize_t len)

class StackIterator:
  def __init__(self, stack):
    self.stack = stack
    self.pos = 0
  def __iter__(self):
    return self
  def next(self):
    if self.pos < self.stack.depth():
      r = self.stack.fetch(self.pos)
      self.pos += 1
      return r
    else:
      raise StopIteration

cdef class Stack:
  """ 
  Stacks get heavy use in Ficl and Forth.
  Each virtual machine (:class:`Vm`) implements two of them:
  one holds parameters (:meth:`Vm.getDataStack`), and the other holds return
  addresses and control flow information for the virtual
  machine (:meth:`Vm.getReturnStack`).
  


  Stack supports the Python iterator protocol, as shown below:

  .. doctest::

    >>> import pyficl
    >>> stk = pyficl.System().createVm().getDataStack()
    >>> stk.push(101)
    >>> stk.push(202)
    >>> stk.push(303)
    >>> print list(stk)
    [303, 202, 101]
    >>> for x in stk:
    ...     print x
    303
    202
    101

  """

  cdef defs.ficlStack* _s
  def depth(self):
    """ returns the depth of the stack, in cells. """
    return defs.ficlStackDepth(self._s)
  def fetch(self, n):
    """
    :param n: stack item, 0 is top of stack
    :type n: int
    
    returns the nth item from the stack.
    """
    return defs.ficlStackFetch(self._s, n).i
  def reset(self):
    """ empty the stack """
    defs.ficlStackReset(self._s)

  def push(self, int i):
    """
    :param i: value
    :type i: int
    
    Push value ``i`` on the stack.
    """
    cdef defs.ficlCell c
    c.i = i
    defs.ficlStackPush(self._s, c)

  def pushFloat(self, float f):
    """
    :param f: value
    :type f: float
    
    Push floating point value ``f`` on the stack.
    """
    cdef defs.ficlCell c
    c.f = f
    defs.ficlStackPush(self._s, c)

  def pushStr(self, s):
    """
    :param s: value
    :type s: str
    
    Push s on the stack as a standard Forth counted string ``( c-addr u )``.

    .. doctest::

      >>> import pyficl
      >>> vm = pyficl.System().createVm()
      >>> stk = vm.getDataStack()
      >>> a = 'Hello world'
      >>> stk.pushStr(a)
      >>> r = vm.evaluate("TYPE CR")
      Hello world

    """
    cdef char* cs = s
    cdef defs.ficlCell c
    c.p = cs
    defs.ficlStackPush(self._s, c)
    self.push(len(s))

  def pushBuffer(self, bo):
    """
    :param str: object that implements the buffer interface
    :type str: str
    
    Push bo on the stack as a standard Forth counted string ``( c-addr u )``.

    .. doctest::

      >>> import pyficl
      >>> vm = pyficl.System().createVm()
      >>> stk = vm.getDataStack()
      >>> a = 'Hello world'
      >>> stk.pushStr(a)
      >>> r = vm.evaluate("TYPE CR")
      Hello world

    """
    cdef defs.ficlCell c
    (address, length) = bo.buffer_info()
    c.i = address
    defs.ficlStackPush(self._s, c)
    self.push(length)

  def pop(self):
    """
    :returns: top value from stack
    :rtype: int

    Removes and returns the top value from the stack as a Python integer
    """

    return defs.ficlStackPop(self._s).i
  
  def popFloat(self):
    """
    :returns: top value from stack
    :rtype: float

    Removes and returns the top value from the stack as a Python float
    """

    return defs.ficlStackPop(self._s).f

  def popStr(self):
    """
    :returns: top value from stack
    :rtype: str

    Removes and returns the top value from the stack as a Python string.  Assumes that the stack is a counted string
    ``( c-addr u )``.
    """

    cdef char *s
    cdef Py_ssize_t l
    l = <Py_ssize_t>(defs.ficlStackPop(self._s).i)
    s = <char*>(defs.ficlStackPop(self._s).p)
    return PyString_FromStringAndSize(s, l)

  def __repr__(self):
    return "[ " + ",".join([str(self.fetch(x)) for x in range(self.depth())]) + " ]"

  def __iter__(self):
    return StackIterator(self)

cdef void cdispatcher(defs.ficlVm* _vm):
  cdef defs.ficlStack *s
  s = defs.ficlVmGetDataStack(_vm)
  cdef object o
  o = <object>(defs.ficlStackPop(s).p)
  
  cdef Vm vm
  vm = Vm()
  vm._vm = _vm

  r = o(vm)

cdef void silent_out(defs.ficlCallback *cb, char *text):
  pass

cdef void myout(defs.ficlCallback *cb, char *text):
  sys.stdout.write(text)

cdef class Dictionary:
  """
  A Dictionary is a linked list of FICL_WORDs. It is also Ficl's
  memory model.  Dictionaries are created when a :class:`System` is created, and accessed by :meth:`System.getDictionary`.
  """
  cdef defs.ficlDictionary* _d

  def appendUnsigned(self, u):
    defs.ficlDictionaryAppendUnsigned(self._d, u)

  def unsmudge(self):
    defs.ficlDictionaryUnsmudge(self._d)

  cdef defs.ficlWord *__appendPrimitive(self, char *name, defs.ficlPrimitive pcode, int flags):
    return defs.ficlDictionaryAppendPrimitive(self._d, name, pcode, flags)

  def setPrimitive(self, name, code):
    """
    :param name: Name of new word
    :type name: str
    :param code: Function for word
    :type code: callable

    Add a new primitive to the FICL Dictionary called name, which when executed calls the Python function code.  The function is passed a single argument, the executing :class:`Vm`.

    .. doctest::

      >>> import pyficl
      >>> s = pyficl.System()
      >>> vm = s.createVm()
      >>> def myfunc(vm):  print "I WAS CALLED"
      >>> s.getDictionary().setPrimitive("myfunc", myfunc)
      >>> r = vm.evaluate("myfunc")
      I WAS CALLED
    """
    Py_INCREF(code)   # lifetime is really lifetime of ficlDictionary,
                      # not sure how to handle this

    cdef defs.ficlWord* dispatcher

    dispatcher = defs.ficlDictionarySetPrimitive(self._d, "dispatcher", cdispatcher, 0)

    self.__appendPrimitive(name, <defs.ficlPrimitive>defs.ficlInstructionColonParen, defs.FICL_WORD_DEFAULT| defs.FICL_WORD_SMUDGED)

    self.appendUnsigned(defs.ficlInstructionLiteralParen)
    cdef defs.ficlCell c
    c.p = <void*>code
    defs.ficlDictionaryAppendCell(self._d, c)

    self.appendUnsigned(<unsigned>dispatcher)
    self.appendUnsigned(defs.ficlInstructionSemiParen)
    self.unsmudge()

cdef class Word:
  """
  A representation of a single Ficl word.
  Obtained by :meth:`System.lookup`, used by :meth:`Vm.executeXT`.

  .. doctest::
    :options: -ELLIPSIS, +NORMALIZE_WHITESPACE

    >>> import pyficl
    >>> s = pyficl.System()
    >>> vm = s.createVm()
    >>> stk = vm.getDataStack()
    >>> dot = s.lookup(".")
    >>> stk.push(787)
    >>> r = vm.executeXT(dot)
    787 

  """
  cdef defs.ficlWord* _w

cdef class Vm:
  """ The virtual machine contains the state for one interpreter.
  Create a Vm using :meth:`System.createVm()`.
  """

  cdef defs.ficlVm* _vm

  def evaluate(self, s):
    """ 
    :param s: input text
    :type s: str
    :returns: status code, see below
    :rtype: int

    Evaluates a block of input text in the context of the
    specified interpreter.

    .. doctest::

      >>> import pyficl
      >>> vm = pyficl.System().createVm()
      >>> stk = vm.getDataStack()
      >>> r = vm.evaluate("1 2 + .")
      3 
      
    status codes:

    FICL_VM_STATUS_OUT_OF_TEXT
      is the normal exit condition
    FICL_VM_STATUS_ERROR_EXIT
      means that the interpreter encountered a syntax error
      and the vm has been reset to recover (some or all
      of the text block got ignored
    FICL_VM_STATUS_USER_EXIT
      means that the user executed the "bye" command
      to shut down the interpreter. This would be a good
      time to delete the vm, etc -- or you can ignore this
      signal.
    FICL_VM_STATUS_ABORT and FICL_VM_STATUS_ABORTQ
      are generated by 'abort' and 'abort"'
      commands.

    """
    return defs.ficlVmEvaluate(self._vm, s)

  def executeXT(self, Word xt):
    """
    :param xt: Word to execute, obtained from :meth:`System.lookup`
    :type xt: :class:`Word`
    :returns: status code, see :meth:`Vm.evaluate`
    :rtype: int

    Executes the given word.
    """
    return defs.ficlVmExecuteXT(self._vm, xt._w)

  def getDataStack(self):
    """
    :returns: the data stack
    :rtype: :class:`Stack`

    Returns the Vm's data stack
    """
    cdef Stack s
    s = Stack()
    s._s = defs.ficlVmGetDataStack(self._vm)
    return s

  def getReturnStack(self):
    """
    :returns: the return stack
    :rtype: :class:`Stack`

    Returns the Vm's return stack
    """
    cdef Stack s
    s = Stack()
    s._s = defs.ficlVmGetReturnStack(self._vm)
    return s

#if (FICL_WANT_FLOAT)
  def getFloatStack(self):
    """
    :returns: the float stack
    :rtype: :class:`Stack`

    Returns the Vm's float stack
    """
    cdef Stack s
    s = Stack()
    s._s = defs.ficlVmGetFloatStack(self._vm)
    return s
#endif

cdef class System:
  """
  The top level data structure of the system - ``System`` ties a list of
  virtual machines to their corresponding dictionaries.
  """
  cdef defs.ficlSystem* _system

  cdef make(self, args):
    cdef defs.ficlSystemInformation si
    defs.ficlSystemInformationInitialize(&si)
    for kw,v in args.items():
      if kw == "dictionarySize":
        si.dictionarySize = v
      else:
        raise "Bad argument"
    si.textOut = <defs.ficlOutputFunction>silent_out
    si.errorOut = <defs.ficlOutputFunction>myout
    self._system = defs.ficlSystemCreate(&si)

  def __init__(self, **kwargs):
    self.make(kwargs)

  def CompileExtras(self):
    defs.ficlSystemCompileExtras(self._system)

  def createVm(self):
    """
    :returns: new virtual machine
    :rtype: :class:`Vm`

    Create a new Vm from the heap, and link it into the system VM list.
    Initializes the VM and binds default sized stacks to it.
    """
    cdef Vm v
    v = Vm()
    v._vm = (defs.ficlSystemCreateVm(self._system))
    v._vm.callback.textOut = <defs.ficlOutputFunction>myout
    return v

  def getDictionary(self):
    """
    :returns: the system's dictionary
    :rtype: :class:`Dictionary`
    """
    cdef Dictionary d
    d = Dictionary()
    d._d = defs.ficlSystemGetDictionary(self._system)
    return d

  def lookup(self, char *name):
    """
    :param name: name of word to look up
    :type name: str
    :returns: word representing name
    :rtype: :class:`Word`

    Returns the :class:`Word` representing str, or None if word is not found.
    """
    cdef Word w
    w = Word()
    w._w = defs.ficlSystemLookup(self._system, name)
    if w._w == NULL:
      return None
    else:
      return w

VM_STATUS_OUT_OF_TEXT = defs.FICL_VM_STATUS_OUT_OF_TEXT
VM_STATUS_ERROR_EXIT = defs.FICL_VM_STATUS_ERROR_EXIT
VM_STATUS_USER_EXIT = defs.FICL_VM_STATUS_USER_EXIT
VM_STATUS_ABORT = defs.FICL_VM_STATUS_ABORT
