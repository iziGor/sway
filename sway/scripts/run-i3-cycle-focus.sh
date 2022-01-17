#!/bin/bash
# vim:autoindent:smartindent:expandtab:smarttab:tabstop=2:softtabstop=2:shiftwidth=2

pkill -f 'python-exec.*i3-cycle-focus'
#sleep 5
sbg.sh ${HOME}/.config/sway/scripts/i3-cycle-focus.py --delay 1.2 --ignore-floating
