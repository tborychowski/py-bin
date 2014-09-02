#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import argparse
import json


# http://openweathermap.org/api
def check(town):
    url = ('http://api.openweathermap.org/data/2.5/weather?'
           'appid=afe9ed75c174bff3c0f900fe0c15f994&units=metric&q=' + town)
    resp = requests.get(url)
    json = resp.json()
    print ((json['name'] + ' ' + str(json['main']['temp']) + u'°C (' +
            json['weather'][0]['main'] + ')').encode('utf-8'))


parser = argparse.ArgumentParser(prog='weather', description='Weather CLI', version='1.0')
parser.add_argument('town', help='town to show weather for', nargs='*', default='Dublin')
args = parser.parse_args()
if args.town: check(' '.join(args.town))
