#!/usr/bin/env python

from distutils.core import setup

setup(name='pdb',
      version='0.0a',
      description='CRUX PortDB module',
      author='Lucas Hazel',
      author_email='lucas@die.net.au',
      url='http://git.die.net.au/cgit/crux/tools/pdb',
      packages=['crux.pdb'],
      scripts=['pdb'],
      data_files=[('/usr/man/man1/',['pdb.1'])])
