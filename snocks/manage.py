#!/usr/bin/env python
#coding=utf-8
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "snocks.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)



# 在虚拟坏境py_django下启：动指令 python manage.py runserver
