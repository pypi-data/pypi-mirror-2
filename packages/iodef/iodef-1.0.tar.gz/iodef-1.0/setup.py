#!/usr/bin/env python

from distutils.core import setup

setup(name='iodef',
      version='1.0',
      description='Libraries to generate IODEF XML Documents',
      author='Pat Cain and Jose Nazario',
      author_email='pcain@antiphishing.org',
      maintainer='Pat Cain',
      maintainer_email='pcain@antiphishing.org',
      url='https://sourceforge.net/projects/ecrisp-x/files/ecrisp-x/Python-based/iodef-1.0/iodef-1.0.tar.gz/download',
      packages = [ 'iodef',
		   'iodef.phish' ],
      classifiers = [
            'Development Status :: 4 - Beta',
            'Operating System :: OS Independent',
            'Intended Audience :: Developers',
            'License :: Freely Distributable',
            'Programming Language :: Python'
            ]
      )
