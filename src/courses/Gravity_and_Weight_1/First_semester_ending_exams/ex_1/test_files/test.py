#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: salvo
# @Date:   2015-05-18 13:44:07
# @Last Modified by:   salvo
# @Last Modified time: 2015-05-18 14:38:29

# add external folder to import path
if __name__ == '__main__' and __package__ is None:
    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from user_files.calculate_g import g_values

try:
    assert round(g_values[0], 2) == 6.67
    assert round(g_values[1], 1) == 0.2
except:
    sys.exit('Wrong values, try again.')