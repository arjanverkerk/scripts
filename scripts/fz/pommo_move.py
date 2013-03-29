# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division


def main():
    pass

import datetime
import shutil
import os

HOME = os.getenv('HOME')

SOURCE_NAME = 'poMMo_Subscribers.csv'
SOURCE_PATH = os.path.join(HOME, 'Downloads')
DESTINATION_PATH = os.path.join(HOME, 'Dropbox/usr/fz/mail')

datetime_now = datetime.datetime.now()
dst_fmt = os.path.join(
    DESTINATION_PATH,
    '%Y-%m-%d-' + SOURCE_NAME
)
DESTINATION_FILE = datetime_now.strftime(dst_fmt)

src = os.path.join(SOURCE_PATH, SOURCE_NAME)
dst = os.path.join(DESTINATION_PATH, DESTINATION_FILE)

shutil.move(src, dst)
