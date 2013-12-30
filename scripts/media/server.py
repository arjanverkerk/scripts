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


def get_parser():
    """ Return argument parser. """
    parser = argparse.ArgumentParser(
        description="A simple webbased media viewer."
    )
    return parser


@app.route('/')
def page():
    return flask.render_template('media/media.html')


def command():
    """ Do something spectacular. """
    paths = [path.strip() for path in sys.stdin]
    app.run(host='0.0.0.0')


def main():
    """ Call command with args from parser. """
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
    command(**vars(get_parser().parse_args()))


if __name__ == '__main__':
    exit(main())
