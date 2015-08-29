#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Elena Graverini
# @Date:   2015-08-06 12:11:48
# @Last Modified by:   Elena Graverini
# @Last Modified time: 2015-08-06 14:54:39

import sys
import numpy as np

mean = float(sys.argv[1])  # 12.0
std = float(sys.argv[2])  # 0.1

scale = 10.  # mm in 1 cm
sample = (np.random.normal(mean * scale, std * scale, 30)).tolist()

print( np.mean(sample) * scale - np.std(sample) * scale )
print( np.mean(sample) * scale + np.std(sample) * scale )

with open('measurements.txt', 'wb') as f:
    for s in sample:
        f.write(str(s) + '\n')
