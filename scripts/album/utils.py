# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division

from scripts.album import config
from scripts.album import meta

import flask
import os


def get_mime(path):
    root, extension = os.path.splitext(path)
    return config.MIME.get(extension.lower(), 'application/octet-stream')


def item(path, directory=False):
    result = dict(
        name=os.path.basename(path),
        path=path,
    )
    if directory:
        result.update(kind='directory')
    else:
        result.update(mime=get_mime(path), meta=meta.load(path))
        result.update(kind=result['mime'].split('/')[0])
    return result


def items_for_path(path):

    dirpath, dirnames, filenames = os.walk(path).next()

    result = [dict(kind='directory', name='..', path=os.path.dirname(path))]

    result += sorted(
        [d for d in [item(os.path.join(dirpath, dirname), directory=True)
         for dirname in dirnames]
         if not d['name'].startswith('.')]

    )
    result += sorted(
        [i for i in [item(os.path.join(dirpath, filename))
                     for filename in filenames]
         if i['mime'] in config.MIME.values()]
    )

    return result


def list_page(path):
    items = items_for_path(path)
    return flask.render_template('list.html', items=items)


def file_page(path):
    return flask.render_template('file.html', item=item(path))
