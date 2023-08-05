#!/usr/bin/python
# -*- coding: utf-8 -*-

from distutils.core import setup

setup(name='pylogan',
      version='0.2.1',
      description='Modular Log Analayzer',
      author='Irving Leonard',
      author_email='irvingleonard@gmail.com',
      url='http://don.t.have.one',
      platforms=['POSIX'],
      license='BSD',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'Intended Audience :: System Administrators',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          'Topic :: Communications',
          ],
      provides=['pylogan'],
      requires=['string','re','time','random','pyrrd','xml',],
      packages=['pylogan',],
      scripts=['pylogan_bin.py',],
      data_files=[
	  ('share/pylogan/webroot', ['webroot/pylogan.css',]),
	  ('share/pylogan/', ['README',]),
	  ],
     )