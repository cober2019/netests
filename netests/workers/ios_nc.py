#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from abc import ABC
from ncclient import manager
from netests.workers.device_nc import DeviceNC
from netests.converters.bgp.ios.netconf.converter import _ios_bgp_netconf_converter
from netests.converters.cdp.ios.netconf.converter import _ios_cdp_netconf_converter
from netests.converters.facts.ios.netconf.converter import _ios_facts_netconf_converter
from netests.converters.lldp.ios.netconf.converter import _ios_lldp_netconf_converter
from netests.converters.ospf.ios.netconf.converter import _ios_ospf_netconf_converter
from netests.converters.vrf.ios.netconf.converter import _ios_vrf_netconf_converter
from netests.constants import (
    NETCONF_FILTER,
    BGP_SESSIONS_HOST_KEY,
    CDP_DATA_HOST_KEY,
    FACTS_DATA_HOST_KEY,
    LLDP_DATA_HOST_KEY,
    OSPF_SESSIONS_HOST_KEY,
    VRF_DATA_KEY
)


class IosNC(DeviceNC, ABC):

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

    def exec_call(self, task, command, vrf):
        with manager.connect(
            host=task.host.hostname,
            port=task.host.port,
            username=task.host.username,
            password=task.host.password,
            hostkey_verify=False,
            device_params={'name': 'iosxe'}
        ) as m:
            if self.nc_method == 'get':
                config = self.exec_call_get(task, command, m)
            elif self.nc_method == 'get_config':
                config = self.exec_call_get_config(task, command, m)

            self.validate_xml(config)
            return config

    def exec_call_get(self, task, command, m):
            return m.get(
                filter=NETCONF_FILTER.format(command)
            ).data_xml

    def exec_call_get_config(self, task, command, m):
        return m.get_config(
            source=self.source,
            filter=(
                'subtree',
                (
                    command
                )
            )
        ).data_xml
            


class BGPIosNC(IosNC):

    NETCONF_FILTER = """
        <bgp-state-data
            xmlns=\"http://cisco.com/ns/yang/Cisco-IOS-XE-bgp-oper\"
        />"""

    def __init__(self, task, options={}):
        super().__init__(
            task=task,
            commands={
                "default_vrf": {
                    "no_key": self.NETCONF_FILTER
                }
            },
            vrf_loop=False,
            converter=_ios_bgp_netconf_converter,
            key_store=BGP_SESSIONS_HOST_KEY,
            nc_method='get',
            options=options,
            source='running'
        )


class CDPIosNC(IosNC):

    NETCONF_FILTER = """
        <cdp-neighbor-details
            xmlns=\"http://cisco.com/ns/yang/Cisco-IOS-XE-cdp-oper\"
        />"""

    def __init__(self, task, options={}):
        super().__init__(
            task=task,
            commands={
                "default_vrf": {
                    "no_key": self.NETCONF_FILTER
                }
            },
            vrf_loop=False,
            converter=_ios_cdp_netconf_converter,
            key_store=CDP_DATA_HOST_KEY,
            nc_method='get',
            options=options,
            source='running'
        )


class FactsIosNC(IosNC):

    NETCONF_FILTER = """
        <native
            xmlns=\"http://cisco.com/ns/yang/Cisco-IOS-XE-native\"
        />"""

    def __init__(self, task, options={}):
        super().__init__(
            task=task,
            commands={
                "default_vrf": {
                    "no_key": self.NETCONF_FILTER
                }
            },
            vrf_loop=False,
            converter=_ios_facts_netconf_converter,
            key_store=FACTS_DATA_HOST_KEY,
            nc_method='get',
            options=options,
            source='running'
        )


class LLDPIosNC(IosNC):

    NETCONF_FILTER = """
        <lldp-entries
            xmlns=\"http://cisco.com/ns/yang/Cisco-IOS-XE-lldp-oper\"
        />"""

    def __init__(self, task, options={}):
        super().__init__(
            task=task,
            commands={
                "default_vrf": {
                    "no_key": self.NETCONF_FILTER
                }
            },
            vrf_loop=False,
            converter=_ios_lldp_netconf_converter,
            key_store=LLDP_DATA_HOST_KEY,
            nc_method='get',
            options=options,
            source='running'
        )


class OSPFIosNC(IosNC):

    NETCONF_FILTER = """
        <ospf-oper-data
            xmlns=\"http://cisco.com/ns/yang/Cisco-IOS-XE-ospf-oper\"
        />"""

    def __init__(self, task, options={}):
        super().__init__(
            task=task,
            commands={
                "default_vrf": {
                    "no_key": self.NETCONF_FILTER
                }
            },
            vrf_loop=False,
            converter=_ios_ospf_netconf_converter,
            key_store=OSPF_SESSIONS_HOST_KEY,
            nc_method='get',
            options=options,
            source='running'
        )


class VRFIosNC(IosNC):

    NETCONF_FILTER = """
        <native 
            xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native"
        />"""

    def __init__(self, task, options={}):
        super().__init__(
            task=task,
            commands={
                "default_vrf": {
                    "no_key": self.NETCONF_FILTER
                }
            },
            vrf_loop=False,
            converter=_ios_vrf_netconf_converter,
            key_store=VRF_DATA_KEY,
            nc_method='get_config',
            options=options,
            source='running'
        )
