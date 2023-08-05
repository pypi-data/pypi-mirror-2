from distutils.core import setup
from distutils.extension import Extension
from distutils.command.build_py import build_py
from Cython.Distutils import build_ext
import subprocess

class build_ficl(build_py):
    subprocess.call("cd ficl; make -f Makefile.linux", shell=True)

setup(
    name = 'pyficl',
    author = 'James Bowman',
    author_email = 'jamesb@excamera.com',
    url = 'http://excamera.com/pyficl/index.html',
    description = "Python interface to FICL",
    long_description = "Python bindings for the Forth-like language FICL",
    version='4.0.31.0',

    cmdclass={'build_ficl': build_ficl, 'build_ext': build_ext},
    ext_modules = [
      Extension("pyficl", ["pyficl.pyx"],
      depends=['defs.pxd'],
      include_dirs=['./ficl'],
      library_dirs=['./ficl'],
      libraries=['ficl'])
    ]
)
