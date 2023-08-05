#
# This file is part of RHEVM-API. RHEVM-API is free software that is made
# available under the MIT license. Consult the file "LICENSE" that is
# distributed together with this file for the exact licensing terms.
#
# RHEVM-API is copyright (c) 2010 by the RHEVM-API authors. See the file
# "AUTHORS" for a complete overview.

from rest.api import mapper
from rhevm.api import powershell
from rhevm.collection import RhevmCollection
from rhevm.util import create_filter, create_cmdline


class VmTicketCollection(RhevmCollection):
    """REST API for controlling a VM's state."""

    name = 'ticket'
    contains = 'ticket'
    entity_transform = """
        $!type => $!type
        $ticket => $Ticket
        $valid => $ValidTime
        """

    def create(self, vm, input):
        filter = create_filter(vmid=vm)
        result = powershell.execute('Select-Vm | %s'
                                    ' | Tee-Object -Variable vm' % filter)
        if len(result) != 1:
            return
        cmdline = create_cmdline(**input)
        powershell.execute('Set-VmTicket -VmObject $vm %s' % cmdline)
        url = mapper.url_for(collection='vm', action='show', id=vm)
        return url


def setup_module(app):
    app.add_route('/api/vms/:vm/ticket', method='POST',
                  collection='ticket', action='create')
    app.add_collection(VmTicketCollection())
