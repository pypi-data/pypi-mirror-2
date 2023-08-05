#
# This file is part of RHEVM-API. RHEVM-API is free software that is made
# available under the MIT license. Consult the file "LICENSE" that is
# distributed together with this file for the exact licensing terms.
#
# RHEVM-API is copyright (c) 2010 by the RHEVM-API authors. See the file
# "AUTHORS" for a complete overview.

import random
from urlparse import urlparse
import yaml

from rest import http
from rhevm.test.base import RhevmTest


class TestVm(RhevmTest): 

    def test_crud(self):
        client = self.client
        headers = self.headers
        headers['Content-Type'] = 'text/yaml'
        data = { 'name': 'test-%s' % random.randint(0, 1000000),
                 'template': 'Blank',
                 'cluster': 'Main' }
        body = yaml.dump(data)
        client.request('POST', '/api/vms', body=body, headers=headers)
        response = client.getresponse()
        assert response.status == http.CREATED
        location = response.getheader('Location')
        assert location is not None
        url = urlparse(location)
        client.request('GET', '/api/vms', headers=headers)
        response = client.getresponse()
        assert response.status == http.OK
        assert response.getheader('Content-Type') == 'text/yaml'
        result = yaml.load(response.read())
        for entry in result:
            if entry['name'] == data['name']:
                break
        else:
            raise AssertionError
        del data['template']
        data['memory'] = 512
        data['description'] = 'My new virtual machine'
        body = yaml.dump(data)
        client.request('PUT', url.path, body=body, headers=headers)
        response = client.getresponse()
        assert response.status == http.OK
        client.request('GET', url.path, headers=headers)
        response = client.getresponse()
        assert response.status == http.OK
        assert response.getheader('Content-Type') == 'text/yaml'
        data = yaml.load(response.read())
        assert data['memory'] == 512
        assert data['description'] == 'My new virtual machine'
        client.request('DELETE', url.path, headers=headers)
        response = client.getresponse()
        assert response.status == http.OK
        client.request('DELETE', url.path, headers=headers)
        response = client.getresponse()
        assert response.status == http.NOT_FOUND
