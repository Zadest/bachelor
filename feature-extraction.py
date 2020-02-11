#! /usr/bin/env python3
# -*- coding: utf8 -*-

import numpy as np
import sys

kernel = np.array([
    [-1,1,1],
    [1,-1,1],
    [1,1,-1]
])

def help():
    print('> This is the help-function')
    sys.exit(1)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        if '-h' in sys.argv or '--help' in sys.argv:
            help()
        elif '-d' in sys.argv or '--debug' in sys.argv:
            print(kernel)
        else:
            help()
    else:
        help()