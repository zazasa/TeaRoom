#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Elena Graverini
# @Date:   2015-08-06 12:11:48
# @Last Modified by:   Elena Graverini
# @Last Modified time: 2015-08-06 12:26:45

import sys
import numpy as np

mean = float(sys.argv[1])  # 2.7
std = float(sys.argv[2])  # 0.6

scale = 8760.  # hours in 1 year
sample = (np.random.normal(mean / scale, std / scale, 30)).tolist()

print( np.mean(sample) * scale - np.std(sample) * scale )
print( np.mean(sample) * scale + np.std(sample) * scale )

with open('measurements.txt', 'wb') as f:
    for s in sample:
        f.write(str(s) + '\n')
