#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os

from setuptools import setup

execfile(os.path.join('pycerberus', 'release.py'))

if __name__ == '__main__':
    setup(
          name=name,
          version=version,

          description=description,
          long_description=long_description,
          author=author,
          author_email=email,
          url=url,
          download_url=download_url,
          license=license,
        
          zip_safe=True,
          packages=('pycerberus',),
          classifiers = (
              'Development Status :: 4 - Beta',
              'Intended Audience :: Developers',
              'License :: OSI Approved :: MIT License',
              'Operating System :: OS Independent',
              'Programming Language :: Python',
              'Topic :: Software Development :: Libraries :: Python Modules',
          ),
          test_suite = 'nose.collector',
    )


