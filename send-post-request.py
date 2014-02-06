#! /usr/bin/env python
import sys
import requests

url = sys.argv[1]

#payload = { 'key' : 'value' }
#r = requests.post(url, data=payload)

r = requests.post(url, files=dict(file='test'),)

print r.status_code
print r.text


