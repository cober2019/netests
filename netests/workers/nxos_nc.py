#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from abc import ABC
from ncclient import manager
from netests.workers.device_nc import DeviceNC
from netests.constants import VRF_DATA_KEY
from netests.converters.vrf.nxos.netconf.converter import _nxos_vrf_netconf_converter


class NxosNC(DeviceNC, ABC):

    nc_method: str
    source: str

    def __init__(
        self,
        task,
        commands,
        vrf_loop,
        converter,
        key_store,
        nc_method,
        options={},
        source='running'
    ):
        super().__init__(
            task,
            commands,
            vrf_loop,
            converter,
            key_store,
            options
        )
        if nc_method == 'get' or nc_method == 'get_config':
            self.nc_method = nc_method
        else:
            self.nc_method = 'get'
        self.source = source

    def exec_call(self, task, command):
        if self.nc_method == 'get':
            return self.exec_call_get(task, command)
        elif self.nc_method == 'get_config':
            return self.exec_call_get_config(task, command)

    def exec_call_get(self, task, command):
        pass

    def exec_call_get_config(self, task, command):
        with manager.connect(
            host=task.host.hostname,
            port=task.host.port,
            username=task.host.username,
            password=task.host.password,
            hostkey_verify=False,
            device_params={'name': 'nexus'}
        ) as m:

            vrf_config = m.get_config(
                source=self.source,
                filter=(
                    'subtree',
                    (
                        command
                    )
                )
            ).data_xml
            self.validate_xml(vrf_config)
            return vrf_config


class VRFNxosNC(NxosNC):

    NETCONF_FILTER = """
        <System xmlns="http://cisco.com/ns/yang/cisco-nx-os-device">
            <inst-items/>
        </System>"""

    def __init__(self, task, options={}):
        super().__init__(
            task=task,
            commands={
                "default_vrf": {
                    "no_key": self.NETCONF_FILTER
                }
            },
            vrf_loop=False,
            converter=_nxos_vrf_netconf_converter,
            key_store=VRF_DATA_KEY,
            nc_method='get_config',
            options=options,
            source='running'
        )
