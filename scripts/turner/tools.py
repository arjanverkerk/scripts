# -*- coding: utf-8 -*-
"""
This module provides a number of (commandline) tools to manipulate or
question the state of the turner system.
"""

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division

import Queue as queueing
import random
import re
import redis
import time
import threading

from .core import Keys
from .core import Turner

SEPARATOR = 60 * '-'


# common
def find_resources(client):
    """ Detect dispensers and return corresponding resources. """
    wildcard = Keys.DISPENSER.format('*')
    pattern = re.compile(Keys.DISPENSER.format('(.*)'))
    return [pattern.match(d).group(1) for d in client.keys(wildcard)]


# tools
def follow(resources, *args, **kwargs):
    pass


def reset(resources, *args, **kwargs):
    """ Remove dispensers and indicators for a resource. """
    # TODO publish it so that clients can disconnect.
    client = redis.Redis(**kwargs)
    if not resources:
        resources = find_resources(client)
    dispensers = [Keys.DISPENSER.format(r) for r in resources]
    indicators = [Keys.INDICATOR.format(r) for r in resources]
    keys = dispensers + indicators
    client.delete(*keys)


def status(resources, *args, **kwargs):
    """
    Print status report for zero or more resources.
    """
    template = '{:<50}{:>10}'
    client = redis.Redis(**kwargs)

    # resource details
    for loop, resource in enumerate(resources):
        # blank between resources
        if loop:
            print()

        # strings needed
        keys = Keys(resource)
        pattern = re.compile(keys.serial('(.*)'))
        wildcard = keys.serial('*')

        # header
        template = '{:<50}{:>10}'
        indicator = client.get(keys.indicator)
        print(template.format(resource, indicator))
        print(SEPARATOR)

        # body
        serials = sorted([pattern.match(key).group(1)
                          for key in client.keys(wildcard)], key=int)
        for serial in serials:
            label = client.get(keys.serial(serial))
            print(template.format(label, serial))

    if resources:
        return

    # find resources and queue sizes
    resources = find_resources(client)
    if not resources:
        return
    dispensers = (Keys.DISPENSER.format(r) for r in resources)
    indicators = (Keys.INDICATOR.format(r) for r in resources)
    combinations = zip(client.mget(dispensers), client.mget(indicators))
    sizes = (int(dispenser) - int(indicator) + 1
             for dispenser, indicator in combinations)

    # print sorted results
    print(template.format('Resource', 'Size'))
    print(SEPARATOR)
    for resource, size in sorted(zip(sizes, resources), reverse=True):
        print(template.format(resource, size))


def test(resources, *args, **kwargs):
    """
    Indefinitely add jobs to turner.
    """
    # this only works with resources
    if not resources:
        return

    # target for the test threads
    def target(queue, turner):
        """
        Test thread target.
        """
        while True:
            # pick tasks from queue
            try:
                resource, period = queue.get()
            except TypeError:
                break
            label = 'Work for {:.2f} s'.format(period)
            # execue
            with turner.lock(resource=resource, label=label, expire=2):
                time.sleep(period)

    # launch threads
    threads = []
    queue = queueing.Queue(maxsize=1)
    for resource in resources:
        thread = threading.Thread(
            target=target,
            kwargs={'queue': queue, 'turner': Turner(*args, **kwargs)},
        )
        thread.start()
        threads.append(thread)

    try:
        while True:
            queue.put((random.choice(resources),
                       max(0, random.gauss(1, 1))))
    except KeyboardInterrupt:
        pass

    for thread in threads:
        queue.put(None)

    for thread in threads:
        thread.join()
    return 0
