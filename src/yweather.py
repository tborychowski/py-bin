#!/usr/bin/env python
''' python yweather.py | grep 'temp:' | cut -d':' -f2 '''

import requests
import argparse
from bs4 import BeautifulSoup

__version__ = '1.0'


def check(args):
    url = 'http://weather.yahooapis.com/forecastrss?u=c&w=' + args.id
    # resp = requests.get(url)
    resp = requests.get(url).text.encode('utf-8')
    xml = BeautifulSoup(resp)

    loc = xml.find('yweather:location')
    print('location:' + loc['city'] + ', ' + loc['country'])

    temp = xml.find('yweather:condition')
    print('desc:' + temp['text'])
    print('temp:' + temp['temp'])               # + 'C'
    print('code:' + temp['code'])
    # print('img:' + 'http://l.yimg.com/a/i/us/we/52/' + temp['code'] + '.gif')
    # print('img:' + 'http://s.imwx.com/v.20131006.215409/img/wxicon/100/' + temp['code'] + '.png')

    wind = xml.find('yweather:wind')
    wind_speed = str(int(round(float(wind['speed']))))
    print('feelslike:' + wind['chill'])         # + ' C'
    print('wind:' + wind_speed)                 # + ' km/h'

    athm = xml.find('yweather:atmosphere')
    print('humidity:' + athm['humidity'])       # + '%'
    print('pressure:' + athm['pressure'])       # + 'mBar'

    forecast = xml.find_all('yweather:forecast')
    print('')
    print ('#forecast|co|lw-hi|desc|date')
    for i, f in enumerate(forecast):
        print ('forecast' + str(i) + '|' + f['code'] +
               '|' + f['low'] + '-' + f['high'] +
               '|' + f['text'] +
               '|' + f['day'] + '|' + f['date'])


parser = argparse.ArgumentParser(prog='weather', description='Yahoo Weather CLI')
parser.add_argument('id', help='WOEID to show weather for', nargs='?', default='560743')  # dublin
parser.add_argument('-v', '--version', action='version',
                    version='%(prog)s {version}'.format(version=__version__))
args = parser.parse_args()
if args.id: check(args)
