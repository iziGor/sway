#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# vim: autoindent smartindent expandtab smarttab tabstop=4 softtabstop=4 shiftwidth=4 foldmethod=marker:
'''
Toggle touchpads scroll_method "two_finger"<->"edge"
'''
from i3ipc import Connection

methods = {"two_finger": "edge", "edge": "two_finger"}
conn = Connection()
inputs = conn.get_inputs()

for e in inputs:
    if  e.type == "touchpad":
        conn.command(
                "input type:touchpad scroll_method {}".format(
                    methods.get(e.libinput.get("scroll_method"), "two_finger")))
        break
