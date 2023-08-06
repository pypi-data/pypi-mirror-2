#! /usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

version = '0.4'

def read(name):
    return open(name).read()

long_description=(
        read('README.txt')
        + '\n' +
        read('CHANGES.txt')
    )

setup(name="xupdate-processor",
      version=version,
      description="XUpdate Processor",
      long_description=long_description,
      author="Nicolas DELABY",
      author_email="nicolas@nexedi.com",
      url="http://nexedi.com",
      license="GPL",
      packages=find_packages('src'),
      package_dir={'': 'src'},
      scripts=["xuproc"],
      install_requires=['PyXML', 'lxml', 'erp5diff >= 0.7'],
      classifiers=['License :: OSI Approved :: GNU General Public License (GPL)',
                  'Operating System :: OS Independent',
                  'Topic :: Text Processing :: Markup :: XML',
                  'Topic :: Utilities'],
      include_package_data=True,
      zip_safe=False,
      test_suite='xupdate_processor',
     )
