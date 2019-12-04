#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-

"""
Description ...

"""

__author__ = "Dylan Hamel"
__maintainer__ = "Dylan Hamel"
__version__ = "0.1"
__email__ = "dylan.hamel@protonmail.com"
__status__ = "Prototype"
__copyright__ = "Copyright 2019"

########################################################################################################################
#
# HEADERS
#
ERROR_HEADER = "Error import [vrf.py]"

########################################################################################################################
#
# Default value used for exit()
#
try:
    from const.constants import *
except ImportError as importError:
    print(f"{ERROR_HEADER} const.constants")
    print(importError)
    exit(EXIT_FAILURE)

########################################################################################################################
#
# VRF CLASS
#



    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __init__(self, vrf_name=NOT_SET, vrf_id=NOT_SET, vrf_type=NOT_SET, l3_vni=NOT_SET, rd=NOT_SET, rt_imp=NOT_SET,
                 rt_exp=NOT_SET, imp_targ=NOT_SET, exp_targ=NOT_SET):

        self.vrf_name = vrf_name
        self.vrf_id = vrf_id
        self.vrf_type = vrf_type
        self.l3_vni = l3_vni
        self.rd = rd
        self.rt_imp = rt_imp
        self.rt_exp = rt_exp
        self.imp_targ = imp_targ
        self.exp_targ = exp_targ

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __eq__(self, other):
        if not isinstance(other, VRF):
            return NotImplemented

        return ((str(self.vrf_name) == str(other.vrf_name)))

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __repr__(self):
        return f"<VRF vrf_name={self.vrf_name} " \
               f"vrf_id={self.vrf_id} " \
               f"vrf_type={self.vrf_type} " \
               f"l3_vni={self.l3_vni} " \
               f"rd={self.rd} " \
               f"rt_imp={self.rt_imp} " \
               f"rt_exp={self.rt_exp} " \
               f"imp_targ={self.imp_targ} " \
               f"exp_targ={self.exp_targ}>\n"

########################################################################################################################
#
# VRF LIST CLASS
#
class ListVRF:

    vrf_lst: list

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __init__(self, vrf_lst: list()):
        self.vrf_lst = vrf_lst

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __eq__(self, others):
        if not isinstance(others, ListVRF):
            raise NotImplemented

        for vrf in self.vrf_lst:
            if vrf not in others.vrf_lst:
                print(
                    f"[ListVRF - __eq__] - The following VRF is not in the list \n {vrf}")
                print(
                    f"[ListVRF - __eq__] - List: \n {others.vrf_lst}")
                return False

        for vrf in others.vrf_lst:
            if vrf not in self.vrf_lst:
                print(
                    f"[ListVRF - __eq__] - The following VRF is not in the list \n {vrf}")
                print(
                    f"[ListVRF - __eq__] - List: \n {self.vrf_lst}")
                return False

        return True

    # ------------------------------------------------------------------------------------------------------------------
    #
    #
    def __repr__(self):
        result = "<ListVRF \n"
        for vrf in self.vrf_lst:
            result = result + f"{vrf}"
        return result + ">"
