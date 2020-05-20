#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from abc import ABC
from netests.workers.device_api import DeviceAPI
from netests.converters.bgp.cumulus.api.converter import _cumulus_bgp_api_converter
from netests.converters.ospf.cumulus.api.converter import _cumulus_ospf_api_converter
from netests.converters.vrf.cumulus.api.converter import _cumulus_vrf_api_converter
from netests.constants import (
    BGP_SESSIONS_HOST_KEY,
    OSPF_SESSIONS_HOST_KEY,
    VRF_DATA_KEY,
    CUMULUS_API_GET_BGP,
    CUMULUS_API_GET_BGP_VRF,
    CUMULUS_API_GET_OSPF,
    CUMULUS_API_GET_OSPF_RID,
    CUMULUS_API_GET_OSPF_VRF,
    CUMULUS_API_GET_OSPF_RID_VRF,
    CUMULUS_API_GET_VRF,
    VRF_DEFAULT_RT_LST
)

class CumulusAPI(DeviceAPI, ABC):

    def __init__(
        self,
        task,
        commands,
        vrf_loop,
        converter,
        key_store,
        options={},
    ):
        super().__init__(
            task,
            commands,
            vrf_loop,
            converter,
            key_store,
            options
        )
        
    def create_payload(self, command):
        return self.payload_to_json(
            {
               "cmd": f"{command}"
            }
        )

    def exec_call(self, task, command):
        p = self.use_https(task.host.get('secure_api', True))

        res = requests.post(
            url=f"{p}://{task.host.hostname}:{task.host.port}/nclu/v1/rpc",
            data=self.create_payload(command),
            headers={'content-type': 'application/json'},
            auth=requests.auth.HTTPBasicAuth(
                f"{task.host.username}",
                f"{task.host.password}"
            ),
            verify=False
        )
        self.check_status_code(res.status_code)
        return res.content


class BGPCumulusAPI(CumulusAPI):

    def __init__(self, task, options={}):
        super().__init__(
            task=task,
            commands={
                "default_vrf": {
                    "no_key": CUMULUS_API_GET_BGP
                },
                "vrf": {
                    "no_key": CUMULUS_API_GET_BGP_VRF
                }
            },
            vrf_loop=False,
            converter=_cumulus_vrf_api_converter,
            key_store=VRF_DATA_KEY,
            options=options
        )


class OSPFCumulusAPI(CumulusAPI):

    def __init__(self, task, options={}):
        super().__init__(
            task=task,
            commands={
                "default_vrf": {
                    "rid": CUMULUS_API_GET_OSPF_RID,
                    "data": CUMULUS_API_GET_OSPF
                },
                "vrf": {
                    "rid": CUMULUS_API_GET_OSPF_RID_VRF,
                    "data": CUMULUS_API_GET_OSPF_VRF
                }
            },
            vrf_loop=True,
            converter=_cumulus_ospf_api_converter,
            key_store=OSPF_SESSIONS_HOST_KEY,
            options=options
        )

class VRFCumulusAPI(CumulusAPI):

    def __init__(self, task, options={}):
        super().__init__(
            task=task,
            commands={
                "default_vrf": {
                    "no_key": CUMULUS_API_GET_VRF
                }
            },
            vrf_loop=False,
            converter=_cumulus_vrf_api_converter,
            key_store=VRF_DATA_KEY,
            options=options
        )
