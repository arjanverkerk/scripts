# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division

import contextlib
import hashlib
import select
import threading

import redis

PATIENCE = 1      # time in queue before bumping
PREFIX = 'turno'  # prefix for all redis keys


class Keys(object):
    # values
    DISPENSER = '{}:{{}}:dispenser'.format(PREFIX)
    INDICATOR = '{}:{{}}:indicator'.format(PREFIX)
    SERIAL = '{}:{{}}:serial:{{}}'.format(PREFIX)

    # channels
    CHANNEL1 = '{}:{{}}:channel1'.format(PREFIX)
    CHANNEL2 = '{}:{{}}:channel2'.format(PREFIX)

    # messages
    CHANGE = '{}:{{}}:change:{{}}'.format(PREFIX)

    def __init__(self, resource):
        self.resource = resource
        self.channel1 = self.CHANNEL1.format(resource)
        self.channel2 = self.CHANNEL2.format(resource)
        self.dispenser = self.DISPENSER.format(resource)
        self.indicator = self.INDICATOR.format(resource)

    def serial(self, serial):
        return self.SERIAL.format(self.resource, serial)

    def change(self, serial):
        return self.CHANGE.format(self.resource, serial + 1)


class Channel(object):
    def __init__(self, client, channel):
        """ Subscribe and receive subscription message. """
        self.pubsub = client.pubsub()
        self.pubsub.subscribe(channel)
        self.pubsub.get_message()

    def listen(self, timeout):
        """
        redis-py master branch supports timeout in pubsub.get_message()
        but until it gets released select.select is used
        """
        socket = self.pubsub.connection._sock
        rlist, wlist, xlist = select.select([socket], [], [], PATIENCE)
        if not rlist:
            return None
        return self.pubsub.get_message()

    def close(self):
        self.pubsub.close()


class Keeper(object):
    def __init__(self, **kwargs):
        self.thread = threading.Thread(target=self.target, kwargs=kwargs)
        self.leave = threading.Event()
        self.thread.start()

    def target(self, client, key, value, expire):
        # set key signaling this number is active
        client.set(key, value, ex=expire)

        # keep key alive
        while not self.leave.wait(timeout=expire - 1):
            client.expire(key, time=expire)

        # revoke presence
        client.delete(key)

    def close(self):
        """ Start and return thread. """
        self.leave.set()
        self.thread.join()


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

    def bump(self, keys):
        """
        Resolve a possible lockup by appropriately bumping indicator.

        :param keys: Keys

        This should only be used in case of anomalies.
        """
        # read redis
        client = self.client
        indicator = int(client.get(keys.indicator))
        dispenser = int(client.get(keys.dispenser))

        # determine active users
        func = lambda n: client.get(keys.serial(n))
        numbers = xrange(indicator, dispenser + 1)
        active = filter(func, numbers)
        first = active[0]

        # leave if things look ok
        if first == indicator:
            return

        # set indicator and announce change
        client.set(keys.indicator, first)
        change = keys.change(first)
        client.publish(keys.channel1, change)

    def channel(self, channel):
        """ Return a pubsub channel. """
        return Channel(client=self.client, channel=channel)

    def keeper(self, key, value, expire):
        """ Maintain a value for given resource and number. """
        return Keeper(client=self.client, key=key, value=value, expire=expire)


class Turner(object):

    def __init__(self, *args, **kwargs):
        self.server = Server(*args, **kwargs)

    @contextlib.contextmanager
    def lock(self, resource, label='', expire=60):
        """
        Lock a resource.

        :param resource: String corresponding to resource type
        :param label: String label to attach
        :param expire: int seconds
        """
        # bootstrap the indicator if necessary
        keys = Keys(resource)
        server = self.server
        client = server.client
        client.setnx(keys.indicator, 1)

        # draw a number
        serial = client.incr(keys.dispenser)

        # keeper to keep value alive in server
        key = keys.serial(serial)
        keeper = server.keeper(key=key, value=label, expire=expire)

        # subscribe to the channel corresponding to resource
        channel = server.channel(keys.channel1)

        while True:
            # read indicator
            indicator = int(client.get(keys.indicator))

            # it's our turn now
            if serial == indicator:
                break

            message = channel.listen(timeout=PATIENCE)
            if not message:
                server.bump(keys)

        try:
            yield  # caller may now use resource
        except Exception as exception:
            raise exception
        finally:
            # advance and announce indicator value
            serial = client.incr(keys.indicator)
            change = keys.change(serial)
            client.publish(keys.channel1, change)

            # close things
            keeper.close()
            channel.close()
