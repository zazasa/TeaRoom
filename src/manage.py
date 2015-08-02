#!/bin/sh
"""":
exec /usr/bin/env python -W ignore::DeprecationWarning $0 $@
"""

import os
import sys

import warnings
warnings.simplefilter("ignore", DeprecationWarning)

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TeaRoom.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)

