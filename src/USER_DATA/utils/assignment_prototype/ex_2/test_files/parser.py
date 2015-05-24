#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: salvo
# @Date:   2015-05-24 20:27:55
# @Last Modified by:   salvo
# @Last Modified time: 2015-05-24 20:30:59
import sys
import filecmp

if __name__ == '__main__':
    filepath = sys.argv[1]
    res = filecmp.cmp('output.txt', filepath)
    if res:
        print 'Well done.'
        sys.exit(0)
    else:
        print 'Fail'
        sys.exit(1)