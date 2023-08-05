'''
Created on Mar 31, 2010

@author: sean
'''

from setuptools import setup,Extension
from glob import glob


ext_modules = [Extension("c_signal_lab", ["components/api/src/c_signal_lab.c"])]

setup( 
name = "signal_lab",
    version = "0.1",
    package_dir = {'': 'components/api/src'},
    py_modules = ['signal_lab','signal_lab_mpi'],
    scripts = glob('user/signal_lab/sl*'),
    ext_modules = ext_modules,
    description = "Alternate Python API to Madagascar software package",
    author = "Sean Ross-Ross",
    author_email="srossross@geospin.ca",
    license="LGPL",

    
    
)