#!/usr/bin/env python

import requests
print(requests.get("http://icanhazip.com").text.strip())
