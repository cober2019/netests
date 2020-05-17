#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from functions.global_tools import open_file
from functions.global_tools import printline
from functions.verbose_mode import verbose_mode
from const.constants import (
    NOT_SET,
    LEVEL4
)


HEADER = "[netests - select_vars.py] -"


def select_host_vars(hostname: str, groups: list, protocol: str):
    if truth_vars_exists() is False:
        if verbose_mode(
            user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
            needed_value=LEVEL4
        ):
            printline()
            print(f"{HEADER} Truth_vars doesn't exists")
        return {}

    if host_vars_exists(hostname, protocol):
        if verbose_mode(
            user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
            needed_value=LEVEL4
        ):
            printline()
            print(f"{HEADER} Select hosts variables")

        return open_file(
            path=f"truth_vars/hosts/{hostname}/{protocol}.yml"
        )

    if group_vars_exists(groups[0], protocol):
        if verbose_mode(
            user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
            needed_value=LEVEL4
        ):
            printline()
            print(f"{HEADER} Select groups variables")

        return open_file(
            path=f"truth_vars/groups/{groups[0]}/{protocol}.yml"
        )

    if all_vars_exists(protocol):
        if verbose_mode(
            user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
            needed_value=LEVEL4
        ):
            printline()
            print(f"{HEADER} Select all variables")

        return open_file(
            path=f"truth_vars/all/{protocol}.yml"
        )


def truth_vars_exists() -> bool:
    os.path.exists("truth_vars")


def host_vars_exists(hostname: str, protocol: str) -> bool:
    return (
        os.path.exists("truth_vars/hosts") and
        os.path.exists(f"truth_vars/hosts/{hostname}") and
        os.path.exists(f"truth_vars/hosts/{hostname}/{protocol}.yml")
    )


def group_vars_exists(group: str, protocol: str) -> bool:
    return os.path.exists(f"truth_vars/groups/{group}/{protocol}.yml")


def all_vars_exists(protocol: str) -> bool:
    return (
        os.path.exists("truth_vars/all") and
        os.path.exists(f"truth_vars/all/{protocol}.yml")
    )