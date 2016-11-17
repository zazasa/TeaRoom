#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Salvatore Zaza
# @Date:   2015-09-11 16:23:48
# @Last Modified by:   Salvatore Zaza
# @Last Modified time: 2015-09-14 17:27:20



# BASE_URL = 'https://localhost:8000'

import argparse
import os
import imp
import pickle
from os.path import join, basename
import tarfile
import requests
import getpass
try:
    import keyring
except ImportError:
    keyring = False


def get_ssl_cert():
    r = requests.get(SSL_CERT_URL, verify=False)
    if r.status_code == 200:
        with open("cert.pem", 'wb') as f:
            f.write(r.content)
        return "cert.pem"
    else:
        return False

    
def get_user_and_pass():
    username = raw_input("Please provide a STAFF account email: ")
    password = None
    if keyring:
        password = keyring.get_password("DataAnalysis", username)
    if password is None:
        password = getpass.getpass('Password: ')
    return {'username': username,
            'password': password}


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
    parser = argparse.ArgumentParser(description='Create TeaRoom assignment package from folder, and upload to server.')
    parser.add_argument('folder')
    parser.add_argument("--package", help="Create package but dont upload.")
    args = parser.parse_args()

    # create tarfile
    assignment_folder = os.path.abspath(args.folder)
    assignment_name = os.path.basename(assignment_folder)
    package_filepath = join(os.path.dirname(assignment_folder), assignment_name + '.tar.gz')

    dump_settings(assignment_folder)
    make_tarfile(package_filepath, assignment_folder)

    # upload
    if not args.package:
        verify = get_ssl_cert()

        UPLOAD_URL = BASE_URL + "/upload-assignment/"

        s = requests.session()
        r = s.get(BASE_URL, verify=verify)
    
        files = {'file': open(package_filepath, 'rb')}
    
        auth_data = get_user_and_pass()
    
        csrftoken = r.cookies['csrftoken']
        headers = {'X-CSRFToken': csrftoken, 'Referer': UPLOAD_URL}
    
        r = requests.post(UPLOAD_URL, data=auth_data, headers=headers, cookies=r.cookies, files=files, verify=verify)
    
        # print r.headers
        print r.text
    
    
