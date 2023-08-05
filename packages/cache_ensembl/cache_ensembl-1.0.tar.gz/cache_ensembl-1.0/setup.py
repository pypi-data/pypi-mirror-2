#!/usr/bin/env python
import ez_setup
ez_setup.use_setuptools()

import sys, os
if not sys.version_info[0:2] >= (2,4):
    sys.stderr.write("Requires Python later than 2.4\n")
    sys.exit(1)

# quickly import the latest version of ruffus
sys.path.insert(0, os.path.abspath("."))
import cache_ensembl.cache_ensembl_version
sys.path.pop(0)


if sys.version_info[0:2] >= (2,6):
    module_dependencies = []
else:
    module_dependencies = []


from setuptools import setup, find_packages
setup(
        name='cache_ensembl',
        version=cache_ensembl.cache_ensembl_version.__version__, #major.minor[.patch[.sub]]
        description='Fast Ensembl data cache',
        long_description=\
"""
***************************************
Overview
***************************************
    We want an extremely fast, lightweight way to access in bulk data stored in Ensembl databases


***************************************
A Simple example
***************************************


""",
        author='Leo Goodstadt',
        author_email='cache_ensembl@llew.org.uk',
        url='http://code.google.com/p/gtf-to-genes/',

        install_requires = module_dependencies,
        setup_requires   = module_dependencies,


        classifiers=[
                    'Intended Audience :: End Users/Desktop',
                    'Development Status :: 5 - Production/Stable',
                    'Intended Audience :: Developers',
                    'Intended Audience :: Science/Research',
                    'Intended Audience :: Information Technology',
                    'License :: OSI Approved :: MIT License',
                    'Programming Language :: Python',
                    'Topic :: Scientific/Engineering',
                    'Topic :: Scientific/Engineering :: Bio-Informatics',
                    'Environment :: Console',
                    ],
        license = "MIT",
        keywords = "GTF Ensembl gene transcript parser GFF bioinformatics science",


        packages=['cache_ensembl'],
        package_dir={'cache_ensembl': 'cache_ensembl'},
        include_package_data = True,    # include everything in source control
        #package_data = {
        #    # If any package contains *.txt files, include them:
        #    '': ['*.TXT'],                                \
        #}


     )

#
#  http://pypi.python.org/pypi
#  http://docs.python.org/distutils/packageindex.html
#
#
#
# python setup.py register
# python setup.py sdist --format=gztar upload
