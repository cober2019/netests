#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from netests.getters.routing_get import GetterRouting
from netests.constants import BGP_SESSIONS_HOST_KEY
from netests.workers.arista_api import BGPAristaAPI
from netests.workers.arista_nc import BGPAristaNC
from netests.workers.arista_ssh import BGPAristaSSH
from netests.workers.cumulus_api import BGPCumulusAPI
from netests.workers.cumulus_nc import CumulusNC
from netests.workers.cumulus_ssh import BGPCumulusSSH
from netests.workers.extreme_vsp_api import BGPExtremeVSPAPI
from netests.workers.extreme_vsp_nc import ExtremeVSPNC
from netests.workers.extreme_vsp_ssh import BGPExtremeVSPSSH
from netests.workers.ios_api import BGPIosAPI
from netests.workers.ios_nc import BGPIosNC
from netests.workers.ios_ssh import BGPIosSSH
from netests.workers.iosxr_api import IosxrAPI
from netests.workers.iosxr_nc import BGPIosxrNC
from netests.workers.iosxr_ssh import BGPIosxrSSH
from netests.workers.juniper_api import BGPJuniperAPI
from netests.workers.juniper_nc import BGPJuniperNC
from netests.workers.juniper_ssh import BGPJuniperSSH
from netests.workers.nxos_api import BGPNxosAPI
from netests.workers.nxos_nc import BGPNxosNC
from netests.workers.nxos_ssh import BGPNxosSSH



HEADER = "[netests - get_bgp]"


class GetterBGP(GetterRouting):

    def __init__(
        self,
        nr,
        options,
        from_cli,
        num_workers,
        verbose,
        print_task_output,
        compare
    ):
        super().__init__(
            nr,
            options,
            from_cli,
            num_workers,
            verbose,
            print_task_output,
            compare
        )
        self.init_mapping_function()

    def run(self):
        self.get_vrf()
        self.devices.run(
            task=self.generic_get,
            on_failed=True,
            num_workers=self.num_workers
        )
        self.print_result()

    def print_result(self):
        self.print_protocols_result(BGP_SESSIONS_HOST_KEY, "BGP")

    def init_mapping_function(self):
        self.MAPPING_FUNCTION = {
            self.ARISTA_PLATEFORM_NAME: {
                self.API_CONNECTION: BGPAristaAPI,
                self.NETCONF_CONNECTION: BGPAristaNC,
                self.SSH_CONNECTION: BGPAristaSSH,
                self.NAPALM_CONNECTION: self.device_not_compatible_with_napalm
            },
            self.CUMULUS_PLATEFORM_NAME: {
                self.API_CONNECTION: BGPCumulusAPI,
                self.NETCONF_CONNECTION: CumulusNC,
                self.SSH_CONNECTION: BGPCumulusSSH,
                self.NAPALM_CONNECTION: self.device_not_compatible_with_napalm
            },
            self.EXTREME_PLATEFORM_NAME: {
                self.API_CONNECTION: BGPExtremeVSPAPI,
                self.NETCONF_CONNECTION: ExtremeVSPNC,
                self.SSH_CONNECTION: BGPExtremeVSPSSH,
                self.NAPALM_CONNECTION: self.device_not_compatible_with_napalm
            },
            self.CISCO_IOS_PLATEFORM_NAME: {
                self.API_CONNECTION: BGPIosAPI,
                self.NETCONF_CONNECTION: BGPIosNC,
                self.SSH_CONNECTION: BGPIosSSH,
                self.NAPALM_CONNECTION: "pass"
            },
            self.CISCO_IOSXR_PLATEFORM_NAME: {
                self.API_CONNECTION: IosxrAPI,
                self.NETCONF_CONNECTION: BGPIosxrNC,
                self.SSH_CONNECTION: BGPIosxrSSH,
                self.NAPALM_CONNECTION: "pass"
            },
            self.JUNOS_PLATEFORM_NAME: {
                self.API_CONNECTION: BGPJuniperAPI,
                self.NETCONF_CONNECTION: BGPJuniperNC,
                self.SSH_CONNECTION: BGPJuniperSSH,
                self.NAPALM_CONNECTION: "pass"
            },
            self.NEXUS_PLATEFORM_NAME: {
                self.API_CONNECTION: BGPNxosAPI,
                self.NETCONF_CONNECTION: BGPNxosNC,
                self.SSH_CONNECTION: BGPNxosSSH,
                self.NAPALM_CONNECTION: "pass"
            }
        }
