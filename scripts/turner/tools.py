# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division

import re
import redis
import threading
import time

from .core import Keys
from .core import Turner


def follow(resources, *args, **kwargs):
    pass


def report_resource(client, resource):
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


def report_general(client):
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


def report(resources, *args, **kwargs):
    client = redis.Redis(**kwargs)
    if resources:
        return report_resource(client=client, resource=resources[0])
    return report_general(client)


def single(resource, sleep, label, *args, **kwargs):
    """ Test a single locking sequence. """
    turner = Turner(**kwargs)
    with turner.lock(resource=resource, label=label, expire=2):
        time.sleep(sleep)
        print(label)


def test(resources, *args, **kwargs):
    if test:
        period = 2
        multiargs = [
            ['resource1', period, 'Task1.1'],
            ['resource1', period, 'Task1.2'],
            ['resource1', period, 'Task1.3'],
            ['resource1', period, 'Task1.4'],
            ['resource2', period, 'Task2.1'],
            ['resource2', period, 'Task2.2'],
            ['resource2', period, 'Task3.3'],
            ['resource3', period, 'Task3.1'],
            ['resource3', period, 'Task3.2'],
            ['resource4', period, 'Task4.1'],
        ]
        threads = []
        for args in multiargs:
            thread = threading.Thread(target=single, args=args, kwargs=kwargs)
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()
        return 0
