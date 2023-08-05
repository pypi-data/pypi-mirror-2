pyficl - a Python interface to FICL
###################################

Introduction
============

The `FICL <http://ficl.sourceforge.net/index.html>`_ package is a Forth implementation with a very comprehensive C interface.

This module implements a Python interface to FICL.  You can use it to call Forth from Python:

.. doctest::
  :options: -ELLIPSIS, +NORMALIZE_WHITESPACE

  >>> import pyficl
  >>> vm = pyficl.System().createVm()
  >>> r = vm.evaluate("1 2 + .")
  3 

and call Python from Forth:

.. doctest::
  :options: -ELLIPSIS, +NORMALIZE_WHITESPACE

  >>> import pyficl
  >>> s = pyficl.System()
  >>> vm = s.createVm()
  >>> def cubed(vm):
  ...   stk = vm.getDataStack()
  ...   stk.push(stk.pop() ** 3)
  ...
  >>> s.getDictionary().setPrimitive("cubed", cubed)
  >>> r = vm.evaluate("3 cubed .")
  27
  >>> r = vm.evaluate(""": demo 10 0 do i . ." cubed is " i cubed . cr loop ; demo""")
  0 cubed is 0 
  1 cubed is 1 
  2 cubed is 8 
  3 cubed is 27 
  4 cubed is 64 
  5 cubed is 125 
  6 cubed is 216 
  7 cubed is 343 
  8 cubed is 512 
  9 cubed is 729 

Building
========

:mod:`pyficl` includes a copy of FICL, so you need to do is download it:

http://excamera.com/files/pyficl-4.0.31.0.tar.gz

extract it and run ``python setup.py install``.  There is a unit test included in the distribution::

  $ python test_ficl.py
  .......
  ----------------------------------------------------------------------
  Ran 7 tests in 0.042s

  OK

Available Types
===============

.. currentmodule:: pyficl


:class:`System` Objects
-----------------------
.. autoclass:: System(dictionarySize = None)

    .. automethod:: createVm()
    .. automethod:: getDictionary()
    .. automethod:: lookup()

:class:`Dictionary` Objects
---------------------------
.. autoclass:: Dictionary

    .. automethod:: setPrimitive(name, code)

:class:`Vm` Objects
-------------------
.. autoclass:: Vm

    .. automethod:: evaluate(s)
    .. automethod:: getDataStack()
    .. automethod:: getReturnStack()
    .. automethod:: getFloatStack()
    .. automethod:: executeXT(xt)

:class:`Word` Objects
---------------------
.. autoclass:: Word

:class:`Stack` Objects
----------------------
.. autoclass:: Stack

    .. automethod:: reset()
    .. automethod:: push(i)
    .. automethod:: pushFloat(f)
    .. automethod:: pushStr(s)
    .. automethod:: pop()
    .. automethod:: popFloat()
    .. automethod:: popStr()
    .. automethod:: depth()
    .. automethod:: fetch(n)

* :ref:`genindex`
* :ref:`search`
