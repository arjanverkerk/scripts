# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division

import flask

import argparse
import logging
import os
import re
import sys

RANGE_PATTERN = re.compile('^bytes=(?P<start>[0-9]+)-(?P<stop>[0-9]*)')
RANGE_TEMPLATE = 'bytes {start}-{stop}/{size}'

CONTENT_TYPE = dict(
    jpg='image/jpeg',
    ogv='video/ogg',
)

HTML_TEMPLATE = dict(
    image='media/image.html',
    video='media/video.html',
)

app = flask.Flask(__name__)
items = []  # set it from function
logger = logging.getLogger(__name__)


def get_ext(path):
    """ Return lowercase ext without the dot. """
    root, ext = os.path.splitext(path)
    return ext.strip('.').lower()

def get_html_template(ext):
    """ Return template location based on extension. """
    content_type = CONTENT_TYPE[ext]
    return HTML_TEMPLATE[content_type.split('/')[0]]


def get_parser():
    """ Return argument parser. """
    parser = argparse.ArgumentParser(
        description="A simple webbased media viewer."
    )
    parser.add_argument('paths', metavar='FILE', nargs='+')
    return parser


@app.route('/')
def media():
    """ Return home with first media file. """
    return flask.render_template(
        'media/media.html',
        length=len(items),
        index=0, 
    )


@app.route('/html/<int:index>')
def html(index):
    """ Return media html. """
    path, ext = items[index]
    template = get_html_template(ext)
    source = '/data/{}'.format(index)
    name = os.path.basename(path)
    return flask.render_template(template, source=source, name=name)


@app.route('/data/<int:index>')
def data(index):
    """ Return data, supporting partial content. """
    # path, size, mime
    path, ext = items[index]
    size = os.stat(path).st_size
    
    # multipart request
    match = re.match(RANGE_PATTERN,
                     flask.request.headers.get('range', ''))
    if match:
        start = int(match.group('start'))
        try:
            stop = int(match.group('stop'))
        except ValueError:
            stop = size - 1
    
    # ordinary request
    else:
        start = 0
        stop = size - 1

    # response
    content_type = CONTENT_TYPE[ext]
    content_range = RANGE_TEMPLATE.format(
        start=start, stop=size - 1, size=size,
    )
    response_headers = {
        'accept-ranges': 'bytes',
        'content-type': content_type,
        'content-range': content_range,
    }
    status = 200 if start == 0 else 206  # 200:OK or 206:Partial content
    with open(path, 'rb') as f:
        f.seek(start)
        return f.read(start - stop), status, response_headers


def command(paths):
    """ Do something spectacular. """
    global items
    for path in paths:
        ext = get_ext(path)
        if ext in CONTENT_TYPE:
            items.append((path, ext))
    app.run(host='0.0.0.0', debug=True)


def main():
    """ Call command with args from parser. """
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    command(**vars(get_parser().parse_args()))


if __name__ == '__main__':
    exit(main())
