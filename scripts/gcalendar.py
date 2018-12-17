#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division

import argparse
import csv
import datetime

"""
Example
-------
Subject,Start Date,Start Time,End Date,End Time,All Day
Event,Description,Location,Private
Final Exam,05/12/08,07:10:00 PM,05/12/08,10:00:00 PM,False,Two
essay questions that will cover topics covered throughout the
semester,"Columbia, Schermerhorn 614",True
"""


def get_parser():
    """ Return argument parser. """
    parser = argparse.ArgumentParser(
        description=""
    )
    parser.add_argument('sourcepath', metavar='SOURCE')
    parser.add_argument('targetpath', metavar='TARGET')
    return parser


def command(sourcepath, targetpath):
    """ Do something spectacular. """
    sourcefile = open(sourcepath)
    reader = csv.DictReader(sourcefile)

    targetfile = open(targetpath, 'w')
    writer = csv.DictWriter(targetfile, fieldnames=[
        'Subject',
        'Start Date',
        'Start Time',
        'End Date',
        'End Time',
        'All Day Event',
        'Description',
        'Location',
        'Private',
    ])
    writer.writeheader()

    # Here it all happens
    date = None  # Pyflakes.
    for record in reader:

        # Take date from previous record if this one is empty
        current_record_date = record['datum'].replace('.', '-').strip()
        date = current_record_date if current_record_date else date
        time = record['tijd'].replace('.', ':').strip()
        dt1 = datetime.datetime.strptime(
            ' '.join([date, time]), '%d-%m %H:%M',
        ).replace(year=2019)
        dt2 = dt1 + datetime.timedelta(minutes=90)

        # Base data
        result = {
            'Start Date': dt1.strftime('%d/%m/%Y'),
            'Start Time': dt1.strftime('%I:%M:%S %p'),
            'End Date': dt2.strftime('%d/%m/%Y'),
            'End Time': dt2.strftime('%I:%M:%S %p'),
        }

        # Specific data
        organ = record['organist'].strip()
        if organ:
            result.update({'Subject': 'Orgel {}'.format(organ)})
            writer.writerow(result)

        piano = record['pianist'].strip()
        if piano:
            result.update({'Subject': 'Piano {}'.format(piano)})
            writer.writerow(result)

        team = record['MT'].replace('MT', '').strip()
        if team:
            result.update({'Subject': 'Muziekteam {}'.format(team)})
            writer.writerow(result)

    sourcefile.close()
    targetfile.close()


def main():
    """ Call command with args from parser. """
    command(**vars(get_parser().parse_args()))


if __name__ == '__main__':
    exit(main())
