#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: salvo
# @Date:   2015-05-18 14:39:30
# @Last Modified by:   salvo
# @Last Modified time: 2015-05-18 14:52:37
import subprocess
try:
    c = subprocess.check_output(["./test.py"], stderr=subprocess.STDOUT)
except subprocess.CalledProcessError, e:
    print e.returncode, e.output.strip()