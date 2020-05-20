#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from netests.getters.base_get import GetterBase
from netests.constants import FACTS_DATA_HOST_KEY
from netests.workers.arista_api import FactsAristaAPI

HEADER = "[netests - get_facts]"


class GetterFacts(GetterBase):

    def __init__(
        self,
        nr,
        options,
        from_cli,
        num_workers,
        verbose,
        print_task_output
    ):
        super().__init__(
            nr,
            options,
            from_cli,
            num_workers,
            verbose,
            print_task_output
        )
        self.init_mapping_function()

    def run(self):
        self.devices.run(
            task=self.generic_get,
            on_failed=True,
            num_workers=self.num_workers
        )
        self.print_result()

    def print_result(self):
        self.print_protocols_result(FACTS_DATA_HOST_KEY, "Facts")

    def init_mapping_function(self):
        self.MAPPING_FUNCTION = {
            self.ARISTA_PLATEFORM_NAME: {
                self.API_CONNECTION: FactsAristaAPI,
                self.SSH_CONNECTION: "pass",
                self.NETCONF_CONNECTION: "pass",
                self.NAPALM_CONNECTION: self.device_not_compatible_with_napalm
            },
            self.CUMULUS_PLATEFORM_NAME: {
                self.API_CONNECTION: "pass",
                self.SSH_CONNECTION: "pass",
                self.NETCONF_CONNECTION: "pass",
                self.NAPALM_CONNECTION: self.device_not_compatible_with_napalm
            }
        }
