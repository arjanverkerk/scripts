# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division

from scripts.album import config
from scripts.album import meta
from scripts.album import utils

from scripts.gis import garmin

from flask import views

import flask
import os
import re


class PageView(views.MethodView):
    """
    Generic view for all pages.
    """
    def post(self, relative_path):
        """ Update meta and redirect to this very page """
        path = os.path.join(config.ROOT_DIR, relative_path)
        meta.save(path=path, form=flask.request.form)
        return flask.redirect(
            flask.url_for('pageview', relative_path=relative_path),
        )

    def get(self, relative_path=config.HOME_DIR):
        """ Show a directory listing or a file view. """
        path = os.path.join(config.ROOT_DIR, relative_path)
        # Directories show the list view
        if os.path.isdir(path):
            return utils.list_page(path)
        return utils.file_page(path)


class FileView(views.MethodView):
    """ Acces single files. Support for partial content. """

    def _data(self, path):
        """
        Supports partial content.
        """
        size = os.stat(path).st_size
        match = re.match(config.RANGE_PATTERN,
                         flask.request.headers.get('range', ''))

        if match:
            start = int(match.group('start'))
            try:
                stop = int(match.group('stop'))
            except ValueError:
                stop = size - 1
        else:
            start = 0
            stop = size - 1

        response_headers = {
            'content-type': utils.get_mime(path),
            'content-range': config.RANGE.format(start=start,
                                                 stop=size - 1, size=size),
            'accept-ranges': 'bytes',
        }

        status = 200 if start == 0 else 206  # 200:OK or 206:Partial content

        with open(path, 'rb') as f:
            f.seek(start)
            return f.read(start - stop), status, response_headers

    def get(self, relative_path):
        path = os.path.join(config.ROOT_DIR, relative_path)
        if path.endswith('gar'):
            return garmin.command(path)
        return self._data(path)
