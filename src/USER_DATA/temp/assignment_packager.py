#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: salvo
# @Date:   2015-05-19 17:02:02
# @Last Modified by:   salvo
# @Last Modified time: 2015-05-24 12:32:19
import argparse
import os
import imp
import sys
import pickle
from os.path import join, basename
import tarfile


def make_tarfile(output_filename, source_dir):
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))


def dump_settings(assignment_folder):
    assignment_settings_file = join(assignment_folder, 'settings.py')
    assignment_settings = imp.load_source('assignment_settings', assignment_settings_file).ASSIGNMENT_SETTINGS
    
    w = os.walk(assignment_folder)
    crap, ex_folder_list, files = w.next()
    
    ex_list = []
    for ex_folder in ex_folder_list:
        ex_full_folder = join(assignment_folder, ex_folder)
        ex_settings_file = join(ex_full_folder, 'settings.py')
        ex_settings = imp.load_source(ex_folder, ex_settings_file).EX_SETTINGS
        ex_settings['RELATIVE_FOLDER'] = basename(ex_full_folder)
        ex_list.append(ex_settings)
    
    SETTINGS = {
        'ASSIGNMENT_SETTINGS': assignment_settings,
        'EX_SETTINGS': ex_list,
    }
    
    config_file = join(assignment_folder, 'settings.pkl')
    
    pickle.dump(SETTINGS, open(config_file, 'wb'))

    # test = pickle.load(open(config_file, 'rb'))
    # print test

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create TeaRoom assignment package from folder.')
    parser.add_argument('folder')
    args = parser.parse_args()
    assignment_folder = os.path.abspath(args.folder)
    assignment_name = os.path.basename(assignment_folder)

    dump_settings(assignment_folder)
    make_tarfile(join(os.path.dirname(assignment_folder), assignment_name + '.tar.gz'), assignment_folder)



