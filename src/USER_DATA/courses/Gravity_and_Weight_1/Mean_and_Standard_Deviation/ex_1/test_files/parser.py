#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: salvo
# @Date:   2015-05-24 20:27:55
# @Last Modified by:   Elena Graverini
# @Last Modified time: 2015-08-06 18:37:37
import sys
import filecmp

if __name__ == '__main__':
    filepath = sys.argv[1]
    #res = filecmp.cmp('output.txt', filepath)
    #if res:
    if 'Seems to work. Nice Job!' in open(filepath).read():
        print 'Submission successful.'
        sys.exit(0)
    else:
        print 'Submission failed.'
        sys.exit(1)
