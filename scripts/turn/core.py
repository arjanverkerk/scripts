# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division

import contextlib
import hashlib
import re
import select
import threading

import redis

PATIENCE = 60000   # time in milliseconds in queue before bumping
PREFIX = 'turn'  # prefix for all redis keys


class Keys(object):
    """ Key generation for redis. """
    # values
    DISPENSER = '{}:{{}}:dispenser'.format(PREFIX)
    INDICATOR = '{}:{{}}:indicator'.format(PREFIX)
    NUMBER = '{}:{{}}:serial:{{}}'.format(PREFIX)  # used as message, too

    # channels
    INTERNAL = '{}:{{}}:internal'.format(PREFIX)
    EXTERNAL = '{}:{{}}:external'.format(PREFIX)

    def __init__(self, resource):
        self.resource = resource
        self.internal = self.INTERNAL.format(resource)
        self.external = self.EXTERNAL.format(resource)
        self.dispenser = self.DISPENSER.format(resource)
        self.indicator = self.INDICATOR.format(resource)

        self.pattern = re.compile(self.NUMBER.format(self.resource, '(.*)'))

    def key(self, number):
        """ Return key for a number. """
        return self.NUMBER.format(self.resource, number)

    def number(self, key):
        """ Return number for a key. """
        return int(self.pattern.match(key).group(1))


class Subscription(object):
    def __init__(self, client, *channels):
        """ Subscribe and receive subscription message. """
        self.pubsub = client.pubsub()
        self.pubsub.subscribe(*channels)
        self.pubsub.get_message()

    def listen(self, timeout=None):
        """
        redis-py master branch supports timeout in pubsub.get_message()
        but until it gets released select.poll is used.
        """
        socket = self.pubsub.connection._sock
        poll = select.poll()
        poll.register(socket, select.POLLIN)
        events = poll.poll(timeout)
        if not events:
            return None
        return self.pubsub.get_message()

    def close(self):
        self.pubsub.close()


class Keeper(object):
    """ Keeps key-value pair alive in redis. """
    def __init__(self, **kwargs):
        self.thread = threading.Thread(target=self.target, kwargs=kwargs)
        self.leave = threading.Event()
        self.thread.start()

    def target(self, client, key, label, expire):
        # set key signaling this number is active
        client.set(key, label, ex=expire)

        # keep key alive
        while not self.leave.wait(timeout=expire - 1):
            client.expire(key, time=expire)

        # revoke presence
        client.delete(key)

    def close(self):
        """ Start and return thread. """
        self.leave.set()
        self.thread.join()


class Queue(object):
    """ Server initialized for specific resource. """
    def __init__(self, client, resource):
        self.client = client
        self.resource = resource
        self.keys = Keys(resource)
        self.subscription = Subscription(client, self.keys.internal)

    @contextlib.contextmanager
    def draw(self, label, expire):
        """
        Return a Serial number for this resource queue, after bootstrapping.
        """
        # get next number
        with self.client.pipeline() as pipe:
            pipe.msetnx({self.keys.dispenser: 0, self.keys.indicator: 1})
            pipe.incr(self.keys.dispenser)
            number = pipe.execute()[-1]

        # publish for humans
        self.message('{} drawn by "{}"'.format(number, label))

        # launch keeper
        kwargs = {'client': self.client, 'key': self.keys.key(number)}
        keeper = Keeper(label=label, expire=expire, **kwargs)

        # yield number
        yield number

        # close keeper
        keeper.close()

        # publish for humans
        self.message('{} completed by "{}"'.format(number, label))

        # set and announce next number
        number += 1
        self.client.set(self.keys.indicator, number)
        self.announce(number)

    def wait(self, number):
        """ Waits and resets if necessary. """
        # inspect indicator for our number
        waiting = int(self.client.get(self.keys.indicator)) != number

        # wait until someone announces our number
        while waiting:
            message = self.subscription.listen(PATIENCE)
            if message is None:
                # timeout beyond patience, bump and try again
                self.message('{} bumps'.format(number))
                self.bump()
                continue
            if message['type'] != 'message':
                continue  # a subscribe message

            waiting = self.keys.number(message['data']) != number

        # our turn now
        self.message('{} starts'.format(number))

    def message(self, text):
        """ Public message. """
        self.client.publish(self.keys.external,
                            '{}: {}'.format(self.resource, text))

    def announce(self, number):
        """ Announce an indicator change on both channels. """
        self.client.publish(self.keys.internal, self.keys.key(number))
        self.message('{} can start now'.format(number))

    def bump(self):
        """ Fix indicator in case of unnanounced departments. """
        # read client
        indicator, dispenser = map(int,
                                   self.client.mget(self.keys.indicator,
                                                    self.keys.dispenser))

        # determine active users
        numbers = xrange(indicator, dispenser + 1)
        keys = map(self.keys.key, numbers)
        pairs = zip(keys, self.client.mget(*keys))

        # determine number of first active user
        number = next(self.keys.number(key)
                      for key, value in pairs if value is not None)

        # set indicator to it if necessary
        if number != indicator:
            self.client.set(self.keys.indicator, number)

        # announce it anyway
        self.announce(number)


class Server(object):
    """ Wraps a redis server. """
    cache = {}

    def __init__(self, *args, **kwargs):
        """ The args and kwargs are passed to Redis instance. """
        key = hashlib.md5(str(list(args) +
                              sorted(kwargs.items()))).hexdigest()

        if key not in self.cache:
            self.cache[key] = redis.Redis(*args, **kwargs)

        self.client = self.cache[key]

    @contextlib.contextmanager
    def lock(self, resource, label='', expire=60):
        """
        Lock a resource.

        :param resource: String corresponding to resource type
        :param label: String label to attach
        :param expire: int seconds
        """
        queue = Queue(client=self.client, resource=resource)
        with queue.draw(label=label, expire=expire) as number:
            queue.wait(number)
            yield