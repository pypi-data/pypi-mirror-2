# -*- coding: utf-8 -*-

#from distutils.core import setup
from setuptools import setup

setup(name="PyDAQmx", version='1.0.1',
      author=u'Pierre Cladé', author_email="pierre.clade@spectro.jussieu.fr",
      maintainer=u'Pierre Cladé',
      maintainer_email="pierre.clade@spectro.jussieu.fr",
      url='http://packages.python.org/PyDAQmx/',
      license='''\
This software can be used under one of the following two licenses: \
(1) The BSD license. \
(2) Any other license, as long as it is obtained from the original \
author.''',

      description='Interface to the National Instrument PyDAQmx driver',

      long_description=u'''\
Overview
========

This package alows users to use data acquisition hardware from `National 
Instrument`_ with python. It makes an interface between the NIDAQmx driver 
and python. It currently works only with Windows OS.

The package is not an open source driver from NI acquisition hardware. You first need to install the driver provided by NI

Compare to similar package, the PyDAQmx module is a full interface to 
the NIDAQmx ansi C driver. It imports all the functions from the driver 
and also imports all the predefined constants. This provided an almost 
one to one match between C and python code.

A more convenient Object oriented interface is provided, where the mecanism 
of taskHandle in C is replace with a Task object.

**Detailed information** about this package can be found on its `main
website`_.



Installation
============

You need first to install the NI DAQmx driver which is provided with your 
data-acquisition hardware. Please verify that you have install together with 
the driver the C API (which should be the case by default). 

To install PyDAQmx, download the package and run the command 
   python setup.py install

You can also directly **move** the :file:`PyDAQmx` directory to a location
that Python can import from (directory in which scripts 
using :mod:`PyDAQmx` are run, etc.)

Contact
=======

Please send bug reports or feedback to `Pierre Cladé`_.


.. _National Instrument: http://www.ni.com
.. _Pierre Cladé: mailto:pierre.clade@spectro.jussieu.fr
.. _main website: http://packages.python.org/PyDAQmx/
''',  
      keywords=['DAQmx', 'National Instrument', 'Data Acquisition'],
      classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Other Audience',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Physics',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules'], 
     packages=["PyDAQmx"]

)


      
