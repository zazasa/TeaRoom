#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: salvo
# @Date:   2015-05-18 13:44:07
# @Last Modified by:   Elena Graverini
# @Last Modified time: 2015-08-06 19:09:47

# add external folder to import path
if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

found_import = False
if 'import' in open('compute_mean_std.py', 'rb').read():
    found_import = True

try:
    assert (not found_import)
except:
    print >> sys.stderr, "For this exercise you are asked not to import any external module."
    print >> sys.stderr, "Please write the appropriate functions yourself, and retry submission."
    sys.exit(1)

if not found_import:
    from compute_mean_std import compute_mean, compute_std
    
    from random import random
    rands = []
    for i in xrange(10000):
        rands.append(random())
    
    try:
        assert round(compute_mean(rands), 1) == 0.5
        assert round(compute_std(rands), 1) == 0.3
        print 'Seems to work. Nice Job!'
    except:
        # raise
        print >> sys.stderr, "I'm sorry, your functions do not return the expected results. Please test and check your code."
