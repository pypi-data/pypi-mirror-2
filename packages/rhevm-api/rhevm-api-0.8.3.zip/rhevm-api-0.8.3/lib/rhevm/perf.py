import sys
from httplib import HTTPConnection
import time

username = 'rhevadmin'
password = 'blaataap'
domain = 'RHEVM22'

auth = '%s@%s:%s' % (username, domain, password)
auth = 'Basic %s' % auth.encode('base64').rstrip()
headers = { 'Authorization': auth, 
            'Accept': 'text/yaml',
            'Host': 'localhost:8080' }

client = HTTPConnection('localhost', int(sys.argv[1]))

t1 = time.time()
client.request('GET', '/api/vms', headers=headers)
resp = client.getresponse()
t2 = time.time()

print 'Time taken: %.2f' % (t2 - t1)
