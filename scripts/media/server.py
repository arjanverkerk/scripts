# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division

import flask

import argparse
import logging
import os
import sys

logger = logging.getLogger(__name__)
app = flask.Flask(__name__)

# Content types
MIME = {
    '.jpg': 'image/jpeg',
    '.ogv': 'video/ogg',
}

RANGE_PATTERN = re.compile(
    '^bytes=(?P<start>[0-9]+)-(?P<stop>[0-9]*)'
)

RANGE = 'bytes {start}-{stop}/{size}'

paths = None


def get_parser():
    """ Return argument parser. """
    parser = argparse.ArgumentParser(
        description="A simple webbased media viewer."
    )
    parser.add_argument('file_paths', metavar='FILE', nargs='+')
    return parser


@app.route('/')
def home():
    """ Redirect to first media path. """
    location = paths[0]
    return flask.redirect(flask.url_for('media', path=location))


@app.route('/media/<path:path>')
def media(path):
    """ View path. """
    mime = 'this'

    return flask.render_template(
        'media/media.html',
        path=path,
        mime=mime,
    )


@app.route('/image/<path:path>')
def image(path):
    """ Return image html. """
    src = '/image/{}'.format(paths.index(path))
    return flask.render_template(
        'media/image.html',
        src=src,
    )


@app.route('/video/<path:path>')
def video(path):
    """ Return video html. """
    return flask.render_template(
        'media/video.html',
        path=path,
    )

@app.route('/data/<int:index>')
def data(index):
    """ Return data for a path, supporting partial content. """
        path = paths[index]
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


def command(file_paths):
    """ Do something spectacular. """
    global paths
    paths = file_paths
    app.run(host='0.0.0.0')


def main():
    """ Call command with args from parser. """
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    command(**vars(get_parser().parse_args()))


if __name__ == '__main__':
    exit(main())
