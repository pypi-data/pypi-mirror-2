#!/usr/bin/env python
'''
No global docstrings.
'''
import os
from distutils.core import setup, Extension
DSCR = 'cSlurp is an optimized PEG parser.'
exts = [Extension('cslurp', ['src/slurp.c', 'src/cslurp.c'], include_dirs=['src'])]

setup(name="cslurp", 
      version="0.0.2", 
      description=DSCR, 
      author="Mike 'Fuzzy' Partin", 
      author_email="fuzzy.wombat.iii@gmail.com", 
      url="", 
      license = "BSD",
      keywords = "parser text processing markup peg regex",
      classifiers=['Development Status :: 4 - Beta',
                   'Intended Audience :: Developers',
                   'Operating System :: POSIX',
                   'License :: OSI Approved :: BSD License',
                   'Programming Language :: C',
                   'Programming Language :: Python',
                   'Topic :: Software Development',
                   'Topic :: Software Development :: Libraries :: Python Modules',
                   'Topic :: Text Processing',
                   ],
      ext_modules=exts)

