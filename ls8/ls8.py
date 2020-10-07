#!/usr/bin/env python3

"""Main."""

import sys
from cpu import CPU

# make sure the correct number of args are passed in
if len(sys.argv) != 2:
    print('Wrong number of arguments.')
    sys.exit(1)

cpu = CPU()

cpu.load(sys.argv[1])
cpu.run()