FILES_TO_COMPLETE = [u'escape_velocity.py'] 
EXERCISE_ID = 5 
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: salvo
# @Date:   2015-05-22 14:03:30
# @Last Modified by:   salvo
# @Last Modified time: 2015-05-22 19:38:41

from os.path import join, dirname
from os import remove
import tarfile
import requests
import getpass

URL = 'http://localhost:8000/upload-result/'
# URL = 'https://%s/upload-result/' % ('SITE_URL')  # to change after the deploy

# FILES_TO_COMPLETE = []
# EXERCISE_ID = 1

BASEDIR = dirname(__file__)

OUTPUT_FILENAME = 'ex_' + str(EXERCISE_ID) + '.tar.gz'


def get_user_and_pass():
    auth_data = {
        'username': raw_input("Enter email: "),
        'password': getpass.getpass('Password: '),
    }
    return auth_data


def create_package(file_list):
    with tarfile.open(OUTPUT_FILENAME, "w:gz") as tar:
        for filename in file_list:
            tar.add(filename)


def upload_package(filename):
    s = requests.session()
    r = s.get(URL, verify=False)

    files = {'file': open(filename, 'rb')}

    data = get_user_and_pass()
    data['ex_id'] = EXERCISE_ID

    csrftoken = r.cookies['csrftoken']
    headers = {'X-CSRFToken': csrftoken, 'Referer': URL}

    r = requests.post(URL, data=data, headers=headers, cookies=r.cookies, files=files)

    # print r.headers
    print r.text

if __name__ == '__main__':
    create_package(FILES_TO_COMPLETE)
    upload_package(OUTPUT_FILENAME)
    remove(OUTPUT_FILENAME)
