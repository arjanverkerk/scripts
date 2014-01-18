# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division

import flask

import argparse
import logging
import sys

logger = logging.getLogger(__name__)
app = flask.Flask(__name__)

# Content types
MIME = {
    '.jpg': 'image/jpeg',
    '.ogv': 'video/ogg',
}

files = None


def get_parser():
    """ Return argument parser. """
    parser = argparse.ArgumentParser(
        description="A simple webbased media viewer."
    )
    parser.add_argument('file_paths', metavar='FILE', nargs='+')
    return parser


@app.route('/')
def home():
    """ View first path. """
    location = files[0]
    return flask.redirect(location)


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
    return flask.render_template(
        'media/image.html',
        path=path,
    )


@app.route('/video/<path:path>')
def video(path):
    """ Return video html. """
    return flask.render_template(
        'media/video.html',
        path=path,
    )


def command(file_paths):
    """ Do something spectacular. """
    global files
    files = file_paths
    app.run(host='0.0.0.0')


def main():
    """ Call command with args from parser. """
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    command(**vars(get_parser().parse_args()))


if __name__ == '__main__':
    exit(main())
