# -*- coding: utf-8 -*-
"""
Any movies in the source should have a poster with the same name as the
video, but having a '.jpg' extension.  Gallery creator. Run from your
www folder where the assets are found.
"""

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
import subprocess
import sys

from PIL import Image

IMAGE_WIDTH = 1920
IMAGE_HEIGHT = 1080

VIDEO_WIDTH = 1280
VIDEO_HEIGHT = 720

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
    ])

    OBJECTS = IMAGES | VIDEOS

    def __init__(self, path):
        """ Initialize the data. """
        self.path = path
        self.load()
        if self.update():
            self.save()

    def inspect(self):
        """
        Return names in path.
        """
        names = os.listdir(self.path)
        roots, exts = zip(*map(os.path.splitext, names))

        videos = [ext.lower() in self.VIDEOS for ext in exts]
        images = [ext.lower() in self.IMAGES for ext in exts]

        videoset = set([root for root, video in zip(roots, videos) if video])

        objects = []
        properties = zip(names, roots, exts, videos, images)
        for name, root, ext, video, image in properties:
            if video:
                objects.append(name)
            elif image:
                if root in videoset and ext.lower() == '.jpg':
                    continue
                objects.append(name)

        return set(objects)

    def load(self):
        """ Loads description, titles and checksums from config file. """
        path = os.path.join(self.path, self.CATALOG)
        try:
            data = json.load(open(path))
            logger.debug('Load existing {}'.format(path))
        except IOError:
            data = {}
            logger.debug('Start with new {}'.format(path))
        self.gallery = data.get('gallery', 'Gallery')
        self.description = data.get('description', 'Description')
        self.titles = data.get('titles', {})
        self.checksums = data.get('checksums', {})

    def update(self):
        """ Updates config with new or renamed files. """
        checksums = {self.checksums[name]: name for name in self.checksums}
        names = self.inspect()

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
    TEMPLATE = TemplateLoader.load('album_header')

    def __init__(self, title, description):
        self.title = title
        self.description = description

    def process(self, gallery):
        return self.TEMPLATE.format(title=self.title,
                                    description=self.description)


class FooterObject(object):
    """ Footer for gallery index page. """
    TEMPLATE = TemplateLoader.load('album_footer')

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

    def resample(self, source_path, graphic_path, thumbnail_path):
        # open
        source = Image.open(source_path)
        width, height = source.size
        resample = Image.ANTIALIAS
        ratio = min(IMAGE_WIDTH / width, IMAGE_HEIGHT / height)

        # graphic
        if os.path.exists(graphic_path):
            logger.debug('Skip {}'.format(graphic_path))
        else:
            logger.debug('Create {}'.format(graphic_path))
            graphic_size = (int(width * ratio),
                            int(height * ratio))
            graphic = source.resize(graphic_size, resample)
            graphic.save(graphic_path)

        # thumbnail
        if os.path.exists(thumbnail_path):
            logger.debug('Skip {}'.format(thumbnail_path))
        else:
            logger.debug('Create {}'.format(thumbnail_path))
            ratio /= 16
            thumbnail_size = (int(width * ratio),
                              int(height * ratio))
            thumbnail = source.resize(thumbnail_size, resample)
            thumbnail.save(thumbnail_path)


class ImageObject(MediaObject):
    """ An image. """
    TEMPLATE = TemplateLoader.load('album_image')
    IMAGES = 'images'

    def prepare(self, gallery):
        """ Set paths on self. """
        name, ext = os.path.splitext(os.path.basename(self.path))
        kwargs = {'gallery': gallery, 'name': name}
        self.image = self.build(sub=self.IMAGES, ext='.jpg', **kwargs)
        self.thumbnail = self.build(sub=self.THUMBNAILS, ext='.jpg', **kwargs)

    def convert(self):
        """ Create necessary files. """
        self.resample(source_path=self.path,
                      graphic_path=self.image['absolute'],
                      thumbnail_path=self.thumbnail['absolute'])

    def process(self, gallery):
        self.prepare(gallery=gallery)
        self.convert()
        return self.TEMPLATE.format(alt=self.title,
                                    href=self.image['relative'],
                                    title=self.title,
                                    src=self.thumbnail['relative'])


class VideoObject(MediaObject):
    """ A video. """
    TEMPLATE = TemplateLoader.load('album_video')
    VIDEOS = 'videos'
    POSTERS = 'posters'

    def prepare(self, gallery):
        """ Set paths on self. """
        root, ext = os.path.splitext(os.path.basename(self.path))
        name, ext = os.path.splitext(os.path.basename(self.path))
        kwargs = {'gallery': gallery, 'name': name}
        self.video = self.build(sub=self.VIDEOS, ext='.mp4', **kwargs)
        self.poster = self.build(sub=self.POSTERS, ext='.jpg', **kwargs)
        self.thumbnail = self.build(sub=self.THUMBNAILS, ext='.jpg', **kwargs)

    def convert(self):
        """ Create necessary files. """
        # poster and thumbnail
        self.resample(graphic_path=self.poster['absolute'],
                      thumbnail_path=self.thumbnail['absolute'],
                      source_path=os.path.splitext(self.path)[0] + '.jpg')

        # video
        path = self.video['absolute']
        if os.path.exists(path):
            logger.debug('Skip {}'.format(path))
        else:
            logger.debug('Create {}'.format(path))

            # determine size
            command = ['ffmpeg2theora', '--info', self.path]
            devnull = open(os.devnull, 'w')
            output = subprocess.check_output(command, stderr=devnull)
            info = json.loads(output)['video'][0]
            width, height = info['width'], info['height']
            video_ratio = min(VIDEO_WIDTH / width, VIDEO_HEIGHT / height)
            if video_ratio < 1:
                width = int(width * video_ratio)
                height = int(height * video_ratio)

            # convert
            command = ['HandBrakeCLI',
                       '-i', self.path,
                       '-o', path,
                       '-e', 'x264',
                       '-q', '22.0',
                       '-r', '30',
                       '--pfr',
                       '-a', '1'
                       '-E', 'faac',
                       '-B', '128',
                       '-6', 'dpl2',
                       '-R', 'Auto',
                       '-D', '0.0',
                       '--audio-copy-mask', 'aac,ac3,dtshd,dts,mp3'
                       '--audio-fallback', 'ffac3',
                       '-f', 'mp4',
                       # '-X', '1280',
                       # '-Y', '720',
                       '-X', str(width),
                       '-Y', str(height),
                       '--loose-anamorphic',
                       '--modulus', '2',
                       '--x264-preset', 'medium',
                       '--h264-profile', 'main',
                       '--h264-level', '3.1']
            subprocess.call(command, stdout=devnull, stderr=devnull)
            # subprocess.call(command)

    def process(self, gallery):
        self.prepare(gallery=gallery)
        self.convert()
        return self.TEMPLATE.format(alt=self.title,
                                    href=self.video['relative'],
                                    title=self.title,
                                    poster=self.poster['relative'],
                                    src=self.thumbnail['relative'])


def rebuild():
    """ Rewrite global index. """
    # load templates
    header = TemplateLoader.load('index_header')
    footer = TemplateLoader.load('index_footer')
    sub = '      <h2>{group}</h2>\n'
    link = '        <li><a href="{gallery}">{name}</a></li>\n'

    # write while walking
    assets = {'js', 'css', 'img', 'fonts', 'index.html'}
    with open('index.html', 'w') as index:
        index.write(header)
        for group in os.listdir('.'):
            if group in assets:
                continue
            index.write(sub.format(group=group))
            index.write('      <ul>\n')
            for name in os.listdir(group):
                gallery = os.path.join(group, name)
                index.write(link.format(name=name, gallery=gallery))
            index.write('      </ul>\n')
        index.write(footer)


def gallery(source, gallery):
    # make room for the album
    if not os.path.exists(gallery):
        os.makedirs(gallery)

    # the catalog contains all source information
    catalog = Catalog(source)

    # conversion yields pieces of the index page
    path = os.path.join(gallery, 'index.html')
    logger.debug('Write {}'.format(path))
    with open(path, 'w') as index:
        for obj in catalog.objects():
            index.write(obj.process(gallery=gallery))

    # rebuild index here
    path = os.path.join('index.html')
    logger.debug('Write {}'.format(path))
    rebuild()
    return 0


def get_parser():
    """ Return argument parser. """
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument('source', metavar='SOURCE')
    parser.add_argument('gallery', metavar='GALLERY')
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
