#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from functions.verbose_mode import verbose_mode
from protocols.vrf import VRF, ListVRF
from const.constants import NOT_SET, LEVEL1, LEVEL4, LEVEL5
from functions.netconf_tools import format_xml_output
from functions.global_tools import printline
from functions.vrf.juniper.vrf_juniper_filters import (
    _juniper_vrf_filter,
    _juniper_vrf_default_mapping
)
import pprint
PP = pprint.PrettyPrinter(indent=4)


def _juniper_vrf_api_converter(
    hostname: str,
    cmd_output: list,
    options={}
) -> ListVRF:
    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL5
    ):
        printline()
        print(type(cmd_output))
        print(cmd_output)

    cmd_output = format_xml_output(cmd_output)

    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL4
    ):
        printline()
        print(type(cmd_output))
        PP.pprint(cmd_output)

    vrf_list = ListVRF(vrf_lst=list())

    for vrf in cmd_output.get('instance-information') \
            .get('instance-core'):
        if _juniper_vrf_filter(vrf.get('instance-name')):
            rd = NOT_SET,
            rt_imp = NOT_SET
            rt_exp = NOT_SET
            imp_targ = NOT_SET
            exp_targ = NOT_SET
            if "instance-vrf" in vrf.keys():
                rd = vrf.get('instance-vrf') \
                        .get('route-distinguisher', NOT_SET)
                rt_imp = vrf.get('instance-vrf') \
                            .get('vrf-import', NOT_SET)
                rt_exp = vrf.get('instance-vrf') \
                            .get('vrf-export', NOT_SET)
                imp_targ = vrf.get('instance-vrf') \
                              .get('vrf-import-target', NOT_SET)
                exp_targ = vrf.get('instance-vrf') \
                              .get('vrf-export-target', NOT_SET)

            vrf_list.vrf_lst.append(
                VRF(
                    vrf_name=_juniper_vrf_default_mapping(
                        vrf.get('instance-name')
                    ),
                    vrf_id=vrf.get('router-id', NOT_SET),
                    vrf_type=vrf.get('instance-type', NOT_SET),
                    l3_vni=NOT_SET,
                    rd=rd,
                    rt_imp=rt_imp,
                    rt_exp=rt_exp,
                    imp_targ=imp_targ,
                    exp_targ=exp_targ,
                    options=options
                )
            )

    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL1
    ):
        printline()
        print(f">>>>> {hostname}")
        PP.pprint(vrf_list.to_json())

    return vrf_list