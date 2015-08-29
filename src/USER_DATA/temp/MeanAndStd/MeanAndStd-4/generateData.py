#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Elena Graverini
# @Date:   2015-08-06 12:11:48
# @Last Modified by:   Elena Graverini
# @Last Modified time: 2015-08-06 15:44:41

import sys
import numpy as np

mean = float(sys.argv[1])  # 0.71
std = float(sys.argv[2])  # 0.012

scale = 1440.  # minutes in 1 day
sample = (np.random.normal(mean * scale, std * scale, 30)).tolist()

print( np.mean(sample) / scale - np.std(sample) / scale )
print( np.mean(sample) / scale + np.std(sample) / scale )

with open('measurements.txt', 'wb') as f:
    for s in sample:
        f.write(str(s) + '\n')
