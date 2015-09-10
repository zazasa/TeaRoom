#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: salvo
# @Date:   2015-05-22 14:03:30
# @Last Modified by:   Salvatore Zaza
# @Last Modified time: 2015-08-29 12:01:35

from os.path import join, dirname
from os import remove
import tarfile
import requests
import getpass
import sys

from subprocess import Popen, PIPE, STDOUT

#URL = 'http://localhost:8000/upload-result/'
# URL = 'https://%s/upload-result/' % ('SITE_URL')  # to change after the deploy
URL = 'https://marder.physik.uzh.ch/da/upload-result/'
COOKIE_URL = 'https://marder.physik.uzh.ch/da/'

# FILES_TO_COMPLETE = []
# EXERCISE_ID = 1
# SUBMIT_KEY = 7877143574145281473039462462327

BASEDIR = dirname(__file__)

OUTPUT_FILENAME = 'ex_' + str(EXERCISE_ID) + '.tar.gz'


def get_user_and_pass():
    auth_data = {
        'username': raw_input("Enter email: "),
        'password': getpass.getpass('Password: '),
        'submit_key': SUBMIT_KEY
    }
    return auth_data


def create_package(file_list, out):
    with open('output.txt', 'wb') as f:
        f.write(out)
    file_list.append('output.txt')
    with tarfile.open(OUTPUT_FILENAME, "w:gz") as tar:
        for filename in file_list:
            tar.add(filename)


def upload_package(auth_data, filename):
    s = requests.session()

    # get csrftoken from server
    #r = s.get(URL, verify=False)
    r = s.get(COOKIE_URL, verify=False)
    csrftoken = r.cookies['csrftoken']
    headers = {'X-CSRFToken': csrftoken, 'Referer': URL}

    files = {'file': open(filename, 'rb')}

    data = auth_data
    data['ex_id'] = EXERCISE_ID
    data['type'] = 'upload'

    r = requests.post(URL, data=data, headers=headers, cookies=r.cookies, files=files)

    # print r.headers
    print r.text


def download_and_execute_test(auth_data):
    s = requests.session()
    #r = s.get(URL, verify=False)

    # get csrftoken from server
    r = s.get(COOKIE_URL, verify=False)
    csrftoken = r.cookies['csrftoken']
    headers = {'X-CSRFToken': csrftoken, 'Referer': URL}

    data = auth_data
    data['ex_id'] = EXERCISE_ID
    data['type'] = 'download'  # download tests
    
    # post request to server
    r = requests.post(URL, data=data, headers=headers, cookies=r.cookies)
    # get either compiled python or other info (e.g. auth errors)
    if r.headers['content-type'] == 'application/x-bytecode.python':
        # open a python subprocess with dedicated stdin/out/err
        p = Popen(['python'], stdout=PIPE, stdin=PIPE, stderr=PIPE)
        # put the pyc in the stdin of the subprocess (exec test)
        out, err = p.communicate(r.text)
        if err:
            # Error on the client's side:
            # e.g. exception in the test of a user defined function
            # or syntax errors, etc etc.
            # Print error messages in user's terminal
            print err
            return False
        else:
            print 'Test result: \n %s' % str(out)
            return out
    else:
        print r.text
        return False


if __name__ == '__main__':
    auth_data = get_user_and_pass()
    
    out = download_and_execute_test(auth_data)

    # pack and upload test output
    if out:
        create_package(FILES_TO_COMPLETE, out)
        upload_package(auth_data, OUTPUT_FILENAME)
        # remove test output from user's disk
        remove(OUTPUT_FILENAME)

