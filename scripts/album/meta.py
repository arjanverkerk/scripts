# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division

import json
import os


def json_path(path):
    root, ext = os.path.splitext(path)
    return root + '.json'


def save(path, form):
    with open(json_path(path), 'w') as json_file:
        json.dump(form, json_file)


def load(path):
    try:
        with open(json_path(path)) as json_file:
            return json.load(json_file)
    except IOError:
        return {}
