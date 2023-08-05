#!/usr/bin/env python

from distutils.core import setup

setup(name='Adamanteus',
      version='0.2',
      description='Database Backups with Version Control',
      author='Josh Ourisman',
      author_email='josh@joshourisman.com',
      license='BSD',
      url='http://www.bitbucket.org/Josh/adamanteus/',
      download_url=("http://bitbucket.org/Josh/adamanteus/get/v0.1.tar.bz2"),
      classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Database',
        'Topic :: System',
        'Topic :: System :: Archiving',
        'Topic :: System :: Archiving :: Backup',
        'Topic :: Utilities',
        ],
      platforms=['any',],
      requires=['mercurial',],
      scripts=['adamanteus.py',],)

