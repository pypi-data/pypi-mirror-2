#
# This file is part of RHEVM-API. RHEVM-API is free software that is made
# available under the MIT license. Consult the file "LICENSE" that is
# distributed together with this file for the exact licensing terms.
#
# RHEVM-API is copyright (c) 2010 by the RHEVM-API authors. See the file
# "AUTHORS" for a complete overview.

from rest.api import mapper
from rhevm.api import powershell
from rhevm.util import *
from rhevm.collection import RhevmCollection


class DataCenterCollection(RhevmCollection):
    """REST API for managing datacenters."""

    name = 'datacenters'
    contains = 'datacenter'
    entity_transform = """
        $!type <=> $!type
        $id <= $DataCenterId
        $name <=> $Name *
        $type <=> $Type *
        $description <=> $Description
        $status <= $Status
    """

    def show(self, id):
        filter = create_filter(datacenterid=id)
        result = powershell.execute('Select-DataCenter | %s' % filter)
        if len(result) != 1:
            return
        return result[0]

    def list(self, **filter):
        filter = create_filter(**filter)
        result = powershell.execute('Select-DataCenter | %s' % filter)
        return result

    def create(self, input):
        cargs = { 'Name': input.pop('Name'),
                  'DataCenterType': input.pop('Type') }
        cmdline = create_cmdline(**cargs)
        # XXX: setting CompatibilityVersion needs improvement
        if powershell.version >= (2, 2):
            powershell.execute('$dc = Select-DataCenter'
                               ' | Select-Object -First 1')
            compat = '-CompatibilityVersion $dc.CompatibilityVersion'
        else:
            compat = ''
        powershell.execute('$dc = Add-DataCenter %s %s' % (compat, cmdline))
        updates = create_setattr('dc', **input)
        powershell.execute(updates)
        result = powershell.execute('Update-DataCenter -DataCenterObject $dc')
        url = mapper.url_for(collection=self.name, action='show',
                             id=result[0]['DataCenterId'])
        return url, result[0]

    def update(self, id, input):
        filter = create_filter(datacenterid=id)
        result = powershell.execute('Select-DataCenter | %s'
                                    ' | Tee-Object -Variable dc' % filter)
        if len(result) != 1:
            raise KeyError
        updates = create_setattr('dc', **input)
        powershell.execute(updates)
        result = powershell.execute('Update-DataCenter -DataCenterObject $dc')
        return result[0]

    def delete(self, id):
        filter = create_filter(datacenterid=id)
        result = powershell.execute('Select-DataCenter | %s'
                                    ' | Tee-Object -Variable dc' % filter)
        if len(result) != 1:
            raise KeyError
        powershell.execute('Remove-DataCenter -DataCenterId $dc.DataCenterId')


def setup_module(app):
    app.add_collection(DataCenterCollection())
