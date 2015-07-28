#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: salvo
# @Date:   2015-05-18 13:44:07
# @Last Modified by:   salvo
# @Last Modified time: 2015-05-24 20:23:32

# add external folder to import path
if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from user_files.compute_mean_std import compute_mean, compute_std

from random import random
rands = []
for i in xrange(10000):
    rands.append(random())

try:
    assert round(compute_mean(rands), 1) == 0.5
    assert round(compute_std(rands), 1) == 0.3
    print 'Seems to work. Nice Job!'
except:
    print "I'm sorry, your functions do not return the expected results. Please check your code."
