#!/bin/bash
# vim:autoindent:smartindent:expandtab:smarttab:tabstop=2:softtabstop=2:shiftwidth=2

pkill -f 'python-exec.*autoname-workspaces'
#sleep 5
sbg.sh ${HOME}/.config/sway/scripts/autoname-workspaces.py
