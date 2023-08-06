from setuptools import setup, find_packages
import sys, os

version = '0.1.2'

setup(name='ngCGH',
      version=version,
      description="Pseudo-cgh of next-generation sequencing data",
      long_description="""
Overview
============
Next-generation sequencing of tumor/normal pairs provides a good opportunity to examine large-scale copy number variation in the tumor relative to the normal sample.  In practice, this concept seems to extend even to exome-capture sequencing of pairs of tumor and normal.  This library consists of a single script, ngCGH, that computes a pseudo-CGH using simple coverage counting on the tumor relative to the normal.

I have chosen to use a fixed number of reads in the normal sample as the "windowing" approach.  This has the advantage of producing copy number estimates that should have similar variance at each location.  The algorithm will adaptively deal with inhomogeneities across the genome such as those associated with exome-capture technologies (to the extent that the capture was similar in both tumor and normal).  The disadvantage is that the pseudo-probes will be at different locations for every "normal control" sample.  

Installation
=============
There are several possible ways to install ngCGH.  

github
-------
If you are a git user, then simply cloning the repository will get you the latest code.

::

  git clone git://github.com/seandavi/ngCGH.git

Alternatively, click the ``Download`` button and get the tarball or zip file.

In either case, change into the resulting directory and::

  cd ngCGH
  python setup.py install

From PyPi
-------------------
If you have easy_install in place, this should suffice for installation:

::

  easy_install ngCGH




Usage
=====
Usage is very simple:

::

    $ ngCGH -h
    usage: ngCGH [-h] [-w WINDOWSIZE] [-o OUTFILE] [-l LOGLEVEL]
               normalbam tumorbam

    positional arguments:
      normalbam             The name of the bamfile for the normal comparison
      tumorbam              The name of the tumor sample bamfile

    optional arguments:
    -h, --help            show this help message and exit
    -w WINDOWSIZE, --windowsize WINDOWSIZE
                        The number of reads captured from the normal sample
                        for calculation of copy number
    -o OUTFILE, --outfile OUTFILE
                        Output filename, default <stdout>
    -l LOGLEVEL, --loglevel LOGLEVEL
                        Logging Level, 1-15 with 1 being minimal logging and
                        15 being everything [10]


Output
======
The output format is also very simple:

::

  chr1    4851    52735   1000    854     -0.025120
  chr1    52736   59251   1000    812     -0.097876
  chr1    59251   119119  1000    876     0.011575
  chr1    119120  707038  1000    1087    0.322924
  chr1    707040  711128  1000    1016    0.225472
  chr1    711128  711375  1000    1059    0.285275
  chr1    711375  735366  1000    919     0.080709
  chr1    735368  798455  1000    972     0.161600

Columns 1-3 describe the chromosome, start, and end for each pseudo-probe.  The fourth column is the number of reads in the normal sample in the window while the fifth column represents the reads *in the same genomic window* from the tumor.  The last column contains the median-centered log2 ratio between tumor and normal.      
""",
      classifiers=["Topic :: Scientific/Engineering :: Bio-Informatics"], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Sean Davis',
      author_email='sdavis2@mail.nih.gov',
      url='http://github.com/seandavi/ngCGH',
      license='GPL-2',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'pysam>=0.3.0'
      ],
      scripts = ['scripts/ngCGH'],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
