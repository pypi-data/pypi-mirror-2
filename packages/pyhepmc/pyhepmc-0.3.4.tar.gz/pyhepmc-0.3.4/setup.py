#! /usr/bin/env python

from distutils.core import setup, Extension

longdesc = """This is a simple SWIG wrapper on the main classes of the HepMC event
simulation representation, making it possible to create, read and manipulate HepMC
events from Python code.
"""

import os
wrapsrc = './hepmc_wrap.cc'
ext = Extension('_hepmc',
                [wrapsrc],
                define_macros = [("SWIG_TYPE_TABLE", "hepmccompat")],
                include_dirs=['/home/andy/heplocal/include'],
                library_dirs=['/home/andy/heplocal/lib'],
                libraries=['HepMC'])

## Setup definition
setup(name = 'pyhepmc',
      version = '0.3.4',
      ext_modules = [ext],
      py_modules = ['hepmc'],
      author = ['Andy Buckley'],
      author_email = 'andy@insectnation.org',
      description = 'A Python interface to the HepMC high-energy physics event record API',
      long_description = longdesc,
      keywords = 'generator montecarlo simulation data hep physics particle',
      license = 'GPL',
      )
