#!/bin/env bash
# vim: autoindent smartindent expandtab smarttab tabstop=2 softtabstop=2 shiftwidth=2 :

#export LC_MESSAGES=C

light $*
sleep .2
notify-send -i mx-alerts "Current level" "$(light -G)"
