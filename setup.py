from __future__ import print_function
from distutils.core import setup


setup(name='w2re',
      version='0.2',
      url='https://bitbucket.org/rlat/w2re',
      author='Radek Lát',
      author_email='radek.lat@gmail.com',
      description='Script for converting a list of words into a compressed regular expression.',
      long_description=open('README.md').read() + '\n' + open('CHANGES.md').read(),
      classifiers=['Development Status :: 5 - Production/Stable',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: Apache Software License',
                   'Topic :: Software Development :: Libraries :: Python Modules',
                   'Programming Language :: Python :: 3.3',
                   ],
      license='Apache License Version 2.0',
      py_modules=['w2re'],
      )
