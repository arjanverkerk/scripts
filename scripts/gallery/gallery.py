# -*- coding: utf-8 -*-
""" Gallery creator. """

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division

import argparse
import collections
import hashlib
import json
import logging
import os
import sys

from PIL import Image

WIDTH = 1024
HEIGHT = 768

logger = logging.getLogger(__name__)


class TemplateLoader(object):
    """ Load templates, if necessary from file. """
    path = os.path.join((os.path.dirname(__file__)), 'templates')
    templates = {}

    @classmethod
    def load(cls, name):
        path = os.path.join(cls.path, '{}.html'.format(name))
        return open(path).read()


class Catalog(object):
    """ Manage album configuration file. """

    CATALOG = 'catalog.json'

    IMAGES = set([
        '.jpeg',
        '.jpg',
        '.png',
    ])

    VIDEOS = set([
        '.avi',
        '.mov',
        '.mp4',
        '.ogv',
        # '.sub',
    ])

    def __init__(self, path):
        """ Initialize the data. """
        self.path = path
        self.load()
        if self.update():
            self.save()

    def load(self):
        """ Loads description, titles and checksums from config file. """
        path = os.path.join(self.path, self.CATALOG)
        try:
            data = json.load(open(path))
            logger.debug('Load existing config.')
        except IOError:
            data = {}
            logger.debug('Start with new config.')
        self.gallery = data.get('gallery', 'Gallery')
        self.description = data.get('description', 'Description')
        self.titles = data.get('titles', {})
        self.checksums = data.get('checksums', {})

    def update(self):
        """ Updates config with new or renamed files. """
        checksums = {self.checksums[name]: name for name in self.checksums}
        names = set(n for n in os.listdir(self.path) if not n.startswith('.'))
        try:
            names.remove(self.CATALOG)
        except KeyError:
            pass

        # handle new files
        create = names.difference(self.titles)
        for new in create:
            logger.debug('Calculate checksum for "{}".'.format(new))
            checksum = hashlib.md5(
                open(os.path.join(self.path, new)).read(),
            ).hexdigest()
            try:
                # change name for existing title
                old = checksums[checksum]
                logger.debug('Rename "{}" to "{}".'.format(old, new))
                self.titles[new] = self.titles[old]
                del self.titles[old]
                del self.checksums[old]
            except KeyError:
                # add new name with dummy title
                logger.debug('Add new file "{}".'.format(new))
                self.titles[new] = new
            finally:
                self.checksums[new] = checksum

        # now use the updated filenames to detect deleted files
        delete = set(self.titles).difference(names)
        for name in delete:
            logger.debug('Remove file "{}".'.format(name))
            del self.titles[name]
            del self.checksums[name]

        return create or delete

    def save(self):
        """ Write current state to config file. """
        data = collections.OrderedDict()
        data['gallery'] = self.gallery
        data['description'] = self.description

        # sorted dicts for titles and checksums
        sorted_dict = lambda d: collections.OrderedDict(sorted(d.items()))

        data['titles'] = sorted_dict(self.titles)
        data['checksums'] = sorted_dict(self.checksums)

        # write indirect
        path = os.path.join(self.path, self.CATALOG)
        tmp_path = '{}.in'.format(path)
        with open(tmp_path, 'w') as tmp_file:
            json.dump(data, tmp_file, indent=2)
        os.rename(tmp_path, path)
        logger.debug('Write config.')

    def objects(self):
        yield HeaderObject(title=self.gallery,
                           description=self.description)
        for name, title in sorted(self.titles.items()):
            path = os.path.join(self.path, name)
            root, ext = os.path.splitext(name)
            if ext.lower() in self.IMAGES:
                yield ImageObject(path=path, title=title)
            if ext.lower() in self.VIDEOS:
                yield VideoObject(path=path, title=title)
        yield FooterObject()


class HeaderObject(object):
    """ Header for gallery index page. """
    TEMPLATE = TemplateLoader.load('header')

    def __init__(self, title, description):
        self.title = title
        self.description = description

    def process(self, gallery):
        return self.TEMPLATE.format(title=self.title,
                                    description=self.description)


class FooterObject(object):
    """ Footer for gallery index page. """
    TEMPLATE = TemplateLoader.load('footer')

    def process(self, gallery):
        return self.TEMPLATE


class MediaObject(object):
    """ Base for media objects. """
    THUMBNAILS = 'thumbnails'

    def __init__(self, path, title):
        self.path = path
        self.title = title

    def build(self, gallery, sub, name, ext):
        """ Construct paths and create folder if necessary. """
        try:
            os.mkdir(os.path.join(gallery, sub))
        except OSError:
            pass
        relative = os.path.join(sub, name + ext)
        absolute = os.path.join(gallery, relative)
        return {'relative': relative, 'absolute': absolute}


class ImageObject(MediaObject):
    """ An image. """
    TEMPLATE = TemplateLoader.load('image')
    IMAGES = 'images'

    def prepare(self, gallery):
        """ Set paths on self. """
        name, ext = os.path.splitext(os.path.basename(self.path))
        kwargs = {'gallery': gallery, 'name': name}
        self.image = self.build(sub=self.IMAGES, ext='.jpg', **kwargs)
        self.thumbnail = self.build(sub=self.THUMBNAILS, ext='.jpg', **kwargs)

    def convert(self):
        source = Image.open(self.path)
        width, height = source.size
        resample = Image.ANTIALIAS

        # image
        logger.debug('Create image {}'.format(self.image['absolute']))
        image_ratio = min(WIDTH / width, HEIGHT / height)
        image_size = (int(width * image_ratio),
                      int(height * image_ratio))
        image = source.resize(image_size, resample)
        image.save(self.image['absolute'])

        # thumbnail
        logger.debug('Create thumbnail {}'.format(self.thumbnail['absolute']))
        thumbnail_ratio = image_ratio / 8
        thumbnail_size = (int(width * thumbnail_ratio),
                          int(height * thumbnail_ratio))
        thumbnail = image.resize(thumbnail_size, resample)
        thumbnail.save(self.thumbnail['absolute'])

    def process(self, gallery):
        self.prepare(gallery=gallery)
        self.convert()
        return self.TEMPLATE.format(alt=self.title,
                                    href=self.image['relative'],
                                    title=self.title,
                                    src=self.thumbnail['relative'])


class VideoObject(MediaObject):
    """ A video. """
    TEMPLATE = TemplateLoader.load('image')
    VIDEOS = 'videos'
    POSTERS = 'posters'

    def prepare(self, gallery):
        """ Set paths on self. """
        root, ext = os.path.splitext(os.path.basename(self.path))
        name, ext = os.path.splitext(os.path.basename(self.path))
        kwargs = {'gallery': gallery, 'name': name}
        self.video = self.build(sub=self.VIDEOS, ext='.ogv', **kwargs)
        self.poster = self.build(sub=self.POSTERS, ext='.jpg', **kwargs)
        self.thumbnail = self.build(sub=self.THUMBNAILS, ext='.jpg', **kwargs)

    def convert(self):
        print(self.video['absolute'])
        print(self.poster['absolute'])
        print(self.thumbnail['absolute'])

    def process(self, gallery):
        self.prepare(gallery=gallery)
        self.convert()
        return self.TEMPLATE.format(alt=self.title,
                                    href=self.video['relative'],
                                    title=self.title,
                                    poster=self.poster['relative'],
                                    src=self.thumbnail['relative'])


def gallery(source, gallery):
    # make room for the album
    if not os.path.exists(gallery):
        os.makedirs(gallery)

    # the catalog contains all source information
    catalog = Catalog(source)

    # conversion yields pieces of the index page
    with open(os.path.join(gallery, 'index.html'), 'w') as index:
        for obj in catalog.objects():
            index.write(obj.process(gallery=gallery))
    # create index here pointing to any indexes html found in tree
    return 0


def get_parser():
    """ Return argument parser. """
    parser = argparse.ArgumentParser(
        description=__doc__
    )
    parser.add_argument(
        'source',
        metavar='SOURCE',
    )
    parser.add_argument(
        'gallery',
        metavar='gallery',
    )
    return parser


def main():
    """ Call command with args from parser. """
    kwargs = vars(get_parser().parse_args())

    logging.basicConfig(stream=sys.stderr,
                        level=logging.DEBUG,
                        format='%(message)s')

    try:
        gallery(**kwargs)
        return 0
    except:
        logger.exception('An exception has occurred.')
        return 1
