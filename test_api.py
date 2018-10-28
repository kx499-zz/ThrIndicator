#!bin/python
import requests

res = requests.post('http://localhost:5000/mitigation/get/fw/inbound/ipv4/30')
print 'Indicator Add Results:'
if res.ok:
    print res.json()
else:
    print 'Something bad happened'