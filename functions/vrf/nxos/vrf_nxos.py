#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from nornir.plugins.tasks.networking import netmiko_send_command
from const.constants import (
    VRF_DATA_KEY,
    NEXUS_GET_VRF
)
from functions.vrf.vrf_converter import (
    _nxos_vrf_converter
)
from exceptions.netests_exceptions import (
    NetestsFunctionNotImplemented
)


def _nxos_get_vrf_api(task):
    raise NetestsFunctionNotImplemented(
        "Cisco Nexus NXOS API functions is not implemented...."
    )


def _nxos_get_vrf_netconf(task):
    raise NetestsFunctionNotImplemented(
        "Cisco Nexus NXOS Netconf functions is not implemented..."
    )


def _nxos_get_vrf_ssh(task):
    if VRF_DATA_KEY not in task.host.keys():
        output = task.run(
            name=f"{NEXUS_GET_VRF}",
            task=netmiko_send_command,
            command_string=f"{NEXUS_GET_VRF}",
        )

        vrf_list = _nxos_vrf_converter(
            hostname=task.host.name,
            cmd_output=json.loads(output.result)
        )

        task.host[VRF_DATA_KEY] = vrf_list
