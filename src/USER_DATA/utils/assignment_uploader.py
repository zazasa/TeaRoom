#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: salvo
# @Date:   2015-05-19 11:25:31
# @Last Modified by:   salvo
# @Last Modified time: 2015-05-20 12:53:19
import argparse
import requests
import getpass

DEBUG = True


def get_user_and_pass():
    if DEBUG:
        auth_data = {
            'username': 'salvatore.zaza@gmail.com',
            'password': 'ominozzo2',
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
    else:
        URL = 'http://localhost:8000/upload-assignment/'
        # URL = 'https://%s/upload-assignment/' % ('SITE_URL')  # to change after the deploy

    s = requests.session()
    r = s.get(URL, verify=False)

    files = {'file': open(filename, 'rb')}

    auth_data = get_user_and_pass()

    csrftoken = r.cookies['csrftoken']
    headers = {'X-CSRFToken': csrftoken, 'Referer': URL}

    r = requests.post(URL, data=auth_data, headers=headers, cookies=r.cookies, files=files)

    # print r.headers
    print r.text