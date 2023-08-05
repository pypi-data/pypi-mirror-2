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
from rhevm.powershell import escape


class VmCollection(RhevmCollection):
    """REST API for managing virtual machines."""

    name = 'vms'
    contains = 'vm'
    entity_transform = """
        $!type <=> $!type
        # Properties required for creation
        $name => $Name * @create
        cluster_id($cluster) => $HostClusterId * @create
        template_object($template) => $TemplateObject * @create
        $type:('server', 'desktop') => $VmType * @create

        # Read-write properties
        $name <=> $Name
        $description <=> $Description
        $memory:int <=> int($MemorySize)
        $domain <=> $Domain
        $os <=> $OperatingSystem
        adjust($display:('vnc', 'spice')) <=> $DisplayType
        $monitors:int <=> int($NumOfMonitors)
        $cpus:int <=> int($NumOfCpus)
        $sockets:int <=> int($NumOfSockets)
        $cores:int <=> int($NumOfCpusPerSocket)
        host_id($defaulthost) <=> host_name($DefaultHost, $HostClusterId)
        $nice:int <=> int($NiceLevel)
        int($failback) <=> boolean($FailBack)
        $boot:('harddisk', 'network', 'cdrom') <=> lower($DefaultBootDevice)
        int($ha) <=> boolean($HighlyAvailable)  # Requires to be set as int

        # Read-only references
        $cluster <= cluster_name($HostClusterId)
        $template <= template_name($TemplateId)
        $host <= host_name($RunningOnHost, $HostClusterId)
        $pool <= pool_name($PoolId) @!rhev21

        # Read-only properties
        $id <= $VmId
        $type <= lower($VmType)
        $created <= $CreationDate
        $status <= lower($Status)
        $session <= $Session
        $ip <= $Ip
        $hostname <= $HostName
        $uptime <= $UpTime
        $login <= $LoginTime
        $username <= $CurrentUserName
        $logout <= $LastLogoutTime
        $time <= int($ElapsedTime)
        $migrating <= host_name($MigratingToHost, $HostClusterId)
        #$applications <= $ApplicationList  # xxx: need to check format
        $port <= int($DisplayPort)

        # Searching
        $query @list
        """

    def show(self, id):
        filter = create_filter(vmid=id)
        result = powershell.execute('Select-Vm | %s' % filter)
        if len(result) != 1:
            return
        return result[0]

    def list(self, **filter):
        query = filter.pop('query', 'vms:')
        filter = create_filter(**filter)
        result = powershell.execute('Select-Vm -SearchText %s | %s'
                                    % (escape(query), filter))
        return result

    def create(self, input):
        props = ('Name', 'TemplateObject', 'HostClusterId', 'VmType')
        args = dict(((prop, input.pop(prop)) for prop in props))
        cmdline = create_cmdline(**args)
        result = powershell.execute('$vm = Add-VM %s' % cmdline)
        updates = create_setattr('vm', **input)
        powershell.execute(updates)
        result = powershell.execute('Update-Vm -VmObject $vm')
        url = mapper.url_for(collection=self.name, action='show',
                             id=result[0]['VmId'])
        return url, result[0]

    def update(self, id, input):
        filter = create_filter(vmid=id)
        result = powershell.execute('Select-Vm | %s'
                                    ' | Tee-Object -Variable vm' % filter)
        if len(result) != 1:
            raise KeyError
        updates = create_setattr('vm', **input)
        powershell.execute(updates)
        result = powershell.execute('Update-Vm -VmObject $vm')
        return result[0]

    def delete(self, id):
        filter = create_filter(vmid=id)
        result = powershell.execute('Select-Vm | %s'
                                    ' | Tee-Object -Variable vm' % filter)
        if len(result) != 1:
            raise KeyError
        powershell.execute('Remove-Vm -VmId $vm.VmId')


def setup_module(app):
    app.add_collection(VmCollection())
