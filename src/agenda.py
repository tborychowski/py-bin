#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import re
import requests
from datetime import *
from dateutil import parser as dateParser  # http://labix.org/python-dateutil
from dateutil.relativedelta import *
from tabulate import tabulate


Calendars = [
    'https://www.google.com/calendar/feeds/username%40gmail.com/private-abc123/full'
]


def print_agenda(agenda):
    limit = int((date.today() + relativedelta(days=+5)).strftime('%s'))
    now = int(datetime.now().strftime('%s'))

    table = []
    agenda.sort(key=lambda x: x['unix'])
    for item in agenda:
        if item['unix'] < now or item['unix'] > limit: continue
        table.append([item['dateStr'], item['name']])

    print (tabulate(table, tablefmt='plain'))


def parse_resp(json):
    agenda = []
    for entry in json['feed']['entry']:

        name = entry['title']['$t']
        start = entry['gd$when'][0]['startTime']
        startDate = dateParser.parse(start)
        dateStr = startDate.strftime('%Y-%m-%d')
        if len(start) != 10: dateStr += ' ' + startDate.strftime('%H:%M')

        agenda.append({
            'name': name,
            'content': entry['content']['$t'],
            'date': startDate,
            'unix': int(startDate.strftime('%s')),
            'dateStr': dateStr,
            'row': dateStr + ' ' + name
        })
    return agenda


def get():
    url = '?alt=json&orderby=starttime&singleevents=true&sortorder=ascending&futureevents=true'
    agenda = []
    for cal in Calendars:
        resp = requests.get(cal + url)
        resp.encoding = 'utf-8'
        agenda += parse_resp(resp.json())

    print_agenda(agenda)


parser = argparse.ArgumentParser(prog='agenda', description='GCal agenda', version='1.0')
args = parser.parse_args()
get()
