#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Salvatore Zaza
# @Date:   2015-08-02 18:30:48
# @Last Modified by:   Salvatore Zaza
# @Last Modified time: 2015-08-02 18:31:02


import argparse
import requests
import getpass

DEBUG = False


def get_user_and_pass():
    if DEBUG:
        auth_data = {
            'username': 'your_admin_email@whatever.ch',
            'password': 'your_password',
        }
    else:
        auth_data = {
            'username': raw_input("Enter email: "),
            'password': getpass.getpass('Password: '),
        }
    return auth_data

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Upload assignment file to TeaRoom server.')
    parser.add_argument('filename')
    args = parser.parse_args()
    filename = args.filename

    if DEBUG:
        URL = 'http://localhost:8000/upload-assignment/'
        #URL = 'http://marder.physik.uzh.ch/da/upload-assignment/'
    else:
        #URL = 'https://%s/upload-assignment/' % ('SITE_URL')  # to change after the deploy
        URL = 'http://marder.physik.uzh.ch/da/upload-assignment/'

    COOKIE_URL = 'http://marder.physik.uzh.ch/da/'
    s = requests.session()
    r = s.get(COOKIE_URL, verify=False)
    #r = s.get(URL, verify=False)

    files = {'file': open(filename, 'rb')}

    auth_data = get_user_and_pass()

    csrftoken = r.cookies['csrftoken']
    #csrftoken = r.cookies['csrf']
    headers = {'X-CSRFToken': csrftoken, 'Referer': URL}

    r = requests.post(URL, data=auth_data, headers=headers, cookies=r.cookies, files=files)

    # print r.headers
    print r.text
