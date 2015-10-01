#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: salvo
# @Date:   2015-05-22 14:03:30
# @Last Modified by:   Salvatore Zaza
# @Last Modified time: 2015-09-26 18:51:13

from os.path import join, dirname
from os import remove
import tarfile
import requests
import getpass
import sys
from subprocess import Popen, PIPE, STDOUT

# SSL_CERT_URL="http://localhost:8000/static/CAServerRoot.pem"
# BASE_URL = 'https://localhost:8000'
# FILES_TO_COMPLETE = []
# EXERCISE_ID = 1
# SUBMIT_KEY = 7877143574145281473039462462327

UPLOAD_URL = BASE_URL + "/upload-result/"

BASEDIR = dirname(__file__)

OUTPUT_FILENAME = 'ex_' + str(EXERCISE_ID) + '.tar.gz'


def get_ssl_cert():
    r = requests.get(SSL_CERT_URL, verify=False)
    if r.status_code == 200:
        with open("cert.pem", 'wb') as f:
            f.write(r.content)
        return "cert.pem"
    else:
        return False


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


def upload_package(auth_data, filename, verify, different_user):
    s = requests.session()

    # get csrftoken from server
    r = s.get(BASE_URL, verify=verify)
    csrftoken = r.cookies['csrftoken']
    headers = {'X-CSRFToken': csrftoken, 'Referer': UPLOAD_URL}

    files = {'file': open(filename, 'rb').read()}

    data = auth_data
    data['ex_id'] = str(EXERCISE_ID)
    data['type'] = 'upload'
    if different_user:
        data['different_user'] = different_user

    r = requests.post(UPLOAD_URL, data=data, headers=headers, cookies=r.cookies, files=files, verify=verify)

    # print r.headers
    print r.text


def download_and_execute_test(auth_data, verify):
    s = requests.session()
    #r = s.get(URL, verify=False)

    # get csrftoken from server
    r = s.get(BASE_URL, verify=verify)
    csrftoken = r.cookies['csrftoken']
    headers = {'X-CSRFToken': csrftoken, 'Referer': UPLOAD_URL}

    data = auth_data
    data['ex_id'] = str(EXERCISE_ID)
    data['type'] = 'download'  # download tests
    
    # post request to server
    r = requests.post(UPLOAD_URL, data=data, headers=headers, cookies=r.cookies, verify=verify)
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

    if '--admin' in sys.argv:
        different_user = raw_input("Please provide a student account email: ")
    else:
        different_user = False

    verify = get_ssl_cert()
    
    out = download_and_execute_test(auth_data, verify)

    # pack and upload test output
    if out:
        print '\n\n\t Now please WAIT until your result is uploaded to the server...'
        print '\t Do NOT exit the program until you read \"info - Exercise result: Submission successful\".'
        create_package(FILES_TO_COMPLETE, out)
        upload_package(auth_data, OUTPUT_FILENAME, verify, different_user)
        # remove test output from user's disk
        remove(OUTPUT_FILENAME)
