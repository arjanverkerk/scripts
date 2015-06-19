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

logger = logging.getLogger(__name__)

"""
Folder structure
----------------
index.html                  # gallery
assets                      # static
path                        # gallery
    index.html              # ...
    to                      # ...
        index.html          # ...
        album               # ...
            index.html      # ...
            media           # ...
            thumbnails      # ...
            posters         # ...
"""


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

    WIDTH = 1024
    HEIGHT = 768

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
        self.description = data.get('description', '')
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

    def objects(self, target_path):
        yield HeaderObject(title=self.description,
                           description=self.description)
        for name, title in sorted(self.titles.items()):
            path = os.path.join(self.path, name)
            if ext.lower() in self.IMAGES:
                yield ImageObject(path=path, title=title)
            if ext.lower() in self.VIDEOS:
                yield VideoObject(path=path, title=title)
        yield FooterObject()


class BaseRouter(object):
    """ Generate paths to media files. """

    THUMBNAILS = 'thumbnails'

    def __init__(self, target_dir):
        self.target = target_dir

    def build(self, sub, root, ext):
        return os.path.join(self.target, sub, '{}{}'.format(root, ext))

    def thumbnail(self, root, ext):
        return self.build(self.THUMBNAILS, root, '.jpg')


class ImageRouter(BaseRouter):
    """ Generate paths to image files. """

    IMAGES = 'images'

    def image(self, root, ext):
        return self.build(self.IMAGES, root, ext)


class VideoRouter(BaseRouter):
    """ Generate paths to video files. """

    VIDEOS = 'videos'
    POSTERS = 'posters'

    def video(self, root, ext):
        return self.build(self.VIDEOS, root, '.ogv')

    def poster(self, root, ext):
        return self.build(self.POSTERS, root, '.jpg')


class GalleryObject(object):
    """ All objects are assigned a target, converted, and rendered. """

    def assign(self, path)
        pass

    def convert(self)
        pass

    def render(self):
        print(self)
        return self.template.format(**self.kwargs)


class HeaderObject(RenderableObject):
    template = TemplateLoader.load('header')

class FooterObject(RenderableObject):
    template = TemplateLoader.load('footer')

class MediaObject(RenderableObject):
    """ Convert media files. """
    def __init__(self, router, title, base, root, ext):
        self.router = router
        self.title = title
        self.base = base
        self.root = root
        self.ext = ext

    def set


class ImageObject(MediaObject):
    template = TemplateLoader.load('image')

    @property
    def kwargs(self):
        return {'href': self.router.
                'title': self.title}

    def prepare(self, target)
        base = self.path
        root, ext = os.path.splitext(name)
        kwargs = {'title': title, 'base': base, 'root': root, 'ext': ext}
        image_router = ImageRouter(base)
        video_router = VideoRouter(base)

    def convert(self):
        """
        Create resized image and thumbnail.
        """
        base, root, ext = self.base, self.root, self.ext
        source_path = os.path.join(base, root + ext)
        image_path = self.router.image(root, ext)
        thumbnail_path = self.router.thumbnail(root, ext)

        source = Image.open(source_path)
        width, height = source.size
        resample = Image.ANTIALIAS

        # image
        logger.debug('Create image {}'.format(image_path))
        image_ratio = min(self.width / width, self.height / height)
        image_size = (int(width * image_ratio),
                      int(height * image_ratio))
        image = source.resize(image_size, resample)
        image.save(image_path)

        # thumbnail
        logger.debug('Create thumbnail {}'.format(thumbnail_path))
        thumbnail_ratio = image_ratio / 8
        thumbnail_size = (int(width * thumbnail_ratio),
                          int(height * thumbnail_ratio))
        thumbnail = image.resize(thumbnail_size, resample)
        thumbnail.save(thumbnail_path)


class VideoObject(MediaObject):
    template = TemplateLoader.load('image')

    def convert(self, base, root, ext):
        video_path = self.router.video(root, ext)
        poster_path = self.router.poster(root, ext)
        thumbnail_path = self.router.thumbnail(root, ext)
        print(video_path)
        print(poster_path)
        print(thumbnail_path)


def gallery(source_dir, target_dir):
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    catalog = Catalog(source_dir)
    # catalog has description for header, so get fill it in template
    with open(os.path.join(target_dir, 'index.html'), 'w') as index:
        index.write(TemplateLoader.load('header'))
        for obj in catalog.objects():
            # call convert on each object.
            index.write(obj.render())
        index.write(TemplateLoader.load('footer'))
    # create index here pointing to any indexes html found in tree
    return 0


def get_parser():
    """ Return argument parser. """
    parser = argparse.ArgumentParser(
        description=__doc__
    )
    parser.add_argument(
        'source_dir',
        metavar='SOURCE',
    )
    parser.add_argument(
        'target_dir',
        metavar='TARGET',
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
