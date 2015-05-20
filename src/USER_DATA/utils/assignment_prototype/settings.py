#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: salvo
# @Date:   2015-05-18 12:41:44
# @Last Modified by:   salvo
# @Last Modified time: 2015-05-20 13:49:00
from datetime import datetime

ASSIGNMENT_SETTINGS = {
    'COURSE_ID': '1',
    'ASSIGNMENT_NUMBER': '1',  # update existing assignments,
    'ASSIGNMENT_TITLE': 'First semester ending exams',
    'ACTIVATION_DATE': datetime.strptime('01/06/2015', '%d/%m/%Y'),  # or False if you wanna update it in the admin interface,
    'HARD_DATE': datetime.strptime('01/07/2015 10:00', '%d/%m/%Y %H:%M'),  # or False if you wanna update it in the admin interface,
    'DUE_DATE': datetime.strptime('01/07/2015 12:00', '%d/%m/%Y %H:%M'),  # or False if you wanna update it in the admin interface,
    'PENALITY_PERCENT': '50',
}


