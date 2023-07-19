#!/usr/bin/env python3
#
# vim: autoindent smartindent expandtab smarttab tabstop=4 softtabstop=4 shiftwidth=4 foldmethod=marker:

from os import environ
from i3ipc import Connection
from logging \
    import ( WARNING
           # , DEBUG
           , INFO
           , basicConfig
           , getLogger )
from scratchpad_tools_sway_i3ipc \
    import ( total_scratchpad_count
           , is_focused_scratchpad
           , in_scratch_count
           , select_from_all_sw
           , select_from_opened_sw )


LOGFILE = environ["HOME"] + "/logs/show_scratchpad.log"
# LOGLEVEL = DEBUG
LOGLEVEL = INFO
# LOGLEVEL = WARNING

basicConfig(filename=LOGFILE, level=LOGLEVEL, format="%(asctime)s %(message)s")
log = getLogger("showsp")
tot_scratchp_count = total_scratchpad_count()
log.info("total_scratchpad_count={}".format(tot_scratchp_count))

conn = Connection()

if  tot_scratchp_count == 0:
    # conn.command("exec xdotool key Super_L+Alt+o")
    conn.command("exec /home/izoom/.config/sway/scripts/run-term-for-scratchpad.sh")

# else:
    # conn.command("scratchpad show")

elif tot_scratchp_count == 1:
    log.info("total_scratchpad_count=1; Launch 'scratchpad show'")
    conn.command("scratchpad show")

else:
    if  is_focused_scratchpad():
        log.info("scratchpad is focused; Launch 'scratchpad show'")
        conn.command("scratchpad show")

    else:
        if  in_scratch_count() == 0:
            log.info("in_scratch_count()=0; Launch 'select_from_opened_sw()'")
            select_from_opened_sw()

        else:
            log.info("in_scratch_count()<>0; Launch 'select_from_all_sw()'")
            select_from_all_sw()

