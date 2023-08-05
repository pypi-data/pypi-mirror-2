#!/usr/bin/env python

from distutils.core import setup
import sys

if sys.version_info >= (3, 0):
    try:
        from distutils.command.build_py import build_py_2to3 as build_py
    except ImportError:
        raise ImportError("build_py_2to3 not found in distutils - it is required for Python 3.x")
else:
    from distutils.command.build_py import build_py

ld = """ A "Roman" object is stored in the computer as a binary integer,
but it is displayed in Roman numerals.
(In technical terms, it is a subset of the built-in class int,
with a _str_() method which returns a Roman numeral string.)

Roman objects act very much like the built-in Decimal objects in Python,
they can be added, subtracted, multiplied, or divided and the result will be
another object of the same class.

So a programmer can say:

import romanclass as roman
two = roman.Roman(2)
five = roman.Roman('V')
print (two+five)

and the computer will print:

VII
"""

def setup_package():
    setup(
        cmdclass = {'build_py': build_py},
        name='romanclass',
        version='1.0.1',
        author = "Vernon Cole",
        author_email = "vernondcole@gmail.com",
        description = "Integer subset class using Roman numeral input and output",
        long_description = ld,
        license = "GPL",
        keywords = "roman romanclass emulate int",
        platforms = 'Windows Linux IronPython',
        classifiers = [
            'Development Status :: 5 - Production/Stable',
            'Intended Audience :: Developers',
            'Intended Audience :: Education',
            'License :: OSI Approved :: GNU General Public License (GPL)',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3',
            'Natural Language :: English',
            'Natural Language :: Latin',
            'Operating System :: OS Independent',
            'Topic :: Software Development',
            'Topic :: Software Development :: Libraries :: Python Modules'],
        url = 'https://launchpad.net/romanclass',
        py_modules=["romanclass"]
        )
    
if __name__ == '__main__':
    setup_package()
