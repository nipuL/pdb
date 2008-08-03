#!/usr/bin/env python
import sys

from crux.pdb import cli

def main():
    cli.PDB().run(sys.argv[1:])

if __name__ == '__main__':
    sys.exit(main())
