#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from functions.global_tools import printline
from functions.verbose_mode import verbose_mode
from nornir.plugins.tasks.text import template_file
from const.constants import (
    NOT_SET,
    LEVEL1,
    TEMPLATES_PATH,
    JINJA2_PATH,
    JINJA2_PING_PATH,
    JINJA2_PING_RESULT
)


def _generic_generate_ping_cmd(task):

    data = task.run(
        name="Generate CLI command to execute ping.",
        task=template_file,
        template=f"{task.host.platform}_ping.j2",
        path=f"{JINJA2_PING_PATH}/",
    )

    # Create folder templates/
    if not os.path.exists(TEMPLATES_PATH):
        os.makedirs(TEMPLATES_PATH)

    # Create folder templates/jinja2/
    if not os.path.exists(JINJA2_PATH):
        os.makedirs(JINJA2_PATH)

    # Create folder templates/jinja2/ping/
    if not os.path.exists(JINJA2_PING_PATH):
        os.makedirs(JINJA2_PING_PATH)

    # Create folder templates/jinja2/ping/result
    if not os.path.exists(JINJA2_PING_RESULT):
        os.makedirs(JINJA2_PING_RESULT)

    if verbose_mode(
        user_value=os.environ.get("NETESTS_VERBOSE", NOT_SET),
        needed_value=LEVEL1
    ):
        printline()
        print(f">>>>> {task.host.name}")
        print(data.result)

    f = open(f"{JINJA2_PING_RESULT}{task.host.name}_ping_cmd", "w+")
    f.write(data.result)
    f.close()