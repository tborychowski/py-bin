#!/usr/bin/env python

import requests
import re
import json


creds = {'Email': '', 'Passwd': ''}
resp = requests.get('https://www.inoreader.com/accounts/ClientLogin', params=creds).text
token = re.search('Auth=(.*?)$', resp).group(1)

h = {'Authorization': 'GoogleLogin auth=' + token}
resp = requests.post('https://www.inoreader.com/reader/api/0/unread-count', headers=h).json()

print resp['unreadcounts'][0]['count']
