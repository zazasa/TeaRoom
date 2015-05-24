#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: salvo
# @Date:   2015-05-18 17:33:58
# @Last Modified by:   salvo
# @Last Modified time: 2015-05-24 13:20:57
import os

local_folder = os.path.dirname(os.path.abspath(__file__))
user_files_folder = os.path.join(local_folder, 'user_files')
test_files_folder = os.path.join(local_folder, 'test_files')

EX_SETTINGS = {
    'NAME': os.path.basename(os.path.dirname(os.path.abspath(__file__))),
    'SHORT_DESCRIPTION': 'Calculate escape velocity',
    'ORDINAL_NUMBER': '2',
    'POINTS': '30',
    
    # Specify file manually if there are supplemental py files
    'FILES_TO_COMPLETE': [file for file in os.listdir(user_files_folder) if file.endswith('.py') and not file.startswith('__')],
    
    # Specify file manually if there are supplemental py files
    'FILE_TO_TEST': 'test.py',
}
