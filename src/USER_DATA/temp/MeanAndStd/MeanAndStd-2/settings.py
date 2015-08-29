#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: salvo
# @Date:   2015-05-18 13:09:12
# @Last Modified by:   Elena Graverini
# @Last Modified time: 2015-08-06 14:30:31
import os

local_folder = os.path.dirname(os.path.abspath(__file__))
user_files_folder = os.path.join(local_folder, 'user_files')
test_files_folder = os.path.join(local_folder, 'test_files')

EX_SETTINGS = {
    'SHORT_DESCRIPTION': 'Calculate mean and standard deviation',
    'ORDINAL_NUMBER': '2',  # required
    'POINTS': '4',
    # Specify file manually if there are supplementary files
    'FILES_TO_COMPLETE': [file for file in os.listdir(user_files_folder) if file.endswith('.py') and not file.startswith('__')],
    'GROUP': 'mean std',
    'FILE_TO_TEST': 'test.py',
    'OUTPUT_PARSER': 'parser.py',
}


