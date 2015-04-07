# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division

import itertools
import Queue as queue
import random
import re
import redis
import time
import threading

from .core import Keys
from .core import Turner


def follow(resources, *args, **kwargs):
    pass


def status_resource(client, resource):
    """ Print a report about resource. """
    keys = Keys(resource)
    substr = keys.serial('')

    # header
    dispenser = client.get(keys.dispenser)
    indicator = client.get(keys.indicator)
    section = 'dispenser {}  indicator {}'.format(dispenser, indicator)

    print('{:<30}{:>30}'.format(resource, section))
    print(60 * '-')

    # body
    for key in client.keys('{}*'.format(substr)):
        print('{}: {}'.format(key.replace(substr, ''), client.get(key)))


def status_general(client):
    """ Print general report. """
    # find resources
    pattern = Keys.DISPENSER.format('*')
    regex = re.compile(Keys.DISPENSER.format('(.*)'))
    resources = [regex.match(d).group(1) for d in client.keys(pattern)]

    # header
    print('General report')
    print(60 * '-')

    template = '{:<30}{:>15}{:>15}'
    for resource in resources:
        dispenser = int(client.get(Keys.DISPENSER.format(resource)))
        indicator = int(client.get(Keys.INDICATOR.format(resource)))
        print(template.format(resource,
                              dispenser - indicator + 1,
                              '({})'.format(indicator)))


def status(resources, *args, **kwargs):
    client = redis.Redis(**kwargs)
    if resources:
        return status_resource(client=client, resource=resources[0])
    return status_general(client)


def target(turner, periods, resource):
    """ Test target. """
    for serial in itertools.count():
        label = 'task{}'.format(serial)
        period = periods.get()
        if period is None:
            break
        print('{}, {}: Acquiring...'.format(resource, label))
        with turner.lock(resource=resource, label=label, expire=2):
            print('{}, {}: Working {} s'.format(resource, label, period))
            time.sleep(period)
        print('{}, {}: Complete.'.format(resource, label))


def test(resources, *args, **kwargs):
    """ Indefinitely add jobs to turner. """
    # launch threads
    queues, threads = [], []

    for resource in resources:
        turner = Turner(*args, **kwargs)

        periods = queue.Queue()
        queues.append(periods)

        target_kwargs = {'turner': turner,
                         'periods': periods,
                         'resource': resource}
        thread = threading.Thread(target=target, kwargs=target_kwargs)
        thread.start()
        threads.append(thread)

    # queues with periods until ctrl-c
    try:
        while True:
            for periods in queues:
                periods.put(max(0, random.gauss(0.9, 0.5)))
            time.sleep(0.5)
    except KeyboardInterrupt:
        pass

    for periods in queues:
        periods.put(None)

    for thread in threads:
        thread.join()
    return 0
