#!/usr/bin/env python3
from setuptools import setup, find_packages

import os
import sys
import hitbasic

DESCRIPTION = 'PEG parser transforms Visual Basic-style language into MSX-BASIC'
readme = open('README.md').read()
version = hitbasic.__version__

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    print("You probably want to also tag the version now:")
    print("  git tag -a %s -m 'version %s'" % (version, version))
    print("  git push --tags")
    sys.exit()

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name='hitbasic', 
    version=version,
    author='Pedro de Medeiros',
    author_email='<pedro.medeiros@gmail.com>',
    url='https://github.com/pvmm/hitbasic',
    license='BSD',
    description=DESCRIPTION,
    long_description=readme,
    packages=find_packages(),
    install_requires=['Arpeggio==1.9.2', 'mock==4.0.2'],
    scripts=['bin/hb'],
    keywords=['msx', 'basic', 'visual basic', 'old school', 'retro', '8bit'],
    tests_require=['tox'],
    classifiers= [
        'Development Status :: 3 - Alpha',
        'Programming Language :: Basic',
        'Programming Language :: Visual Basic'
        'Environment :: Console',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: BSD License',
        'Topic :: Software Development :: Code Generators',
    ],
)
