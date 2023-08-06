import sys
major, minor, micro, releaselevel, serial = sys.version_info
if not (major == 2 and minor >= 5):
	print("Python >=2.5 is required to use this module.")
	sys.exit(1)

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import os.path

from test.test_doc import DOCUMENTATION

VERSION = '0.3.3'

setup(
	name='pyfft',
	packages=['pyfft'],
	provides=['pyfft'],
	requires=['mako', 'numpy'],
	package_data={'pyfft': ['*.mako']},
	version=VERSION,
	author='Bogdan Opanchuk',
	author_email='mantihor@gmail.com',
	url='http://github.com/Manticore/pyfft',
	description='FFT library for PyCuda and PyOpenCL',
	long_description=DOCUMENTATION,
	classifiers=[
		'Development Status :: 4 - Beta',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: MIT License',
		'Operating System :: OS Independent',
		'Programming Language :: Python :: 2',
		'Topic :: Scientific/Engineering :: Mathematics'
	]
)
