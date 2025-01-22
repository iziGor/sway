#!/bin/env sh
# vim: autoindent smartindent expandtab smarttab tabstop=2 softtabstop=2 shiftwidth=2 :

cleanup () {
  [[ -n $PIDP ]] && kill -TERM $PIDP
}

trap cleanup EXIT INT TERM
python -u -OO ${HOME}/.config/waybar/scripts/tiling-indicator.py 2>>$HOME/logs/sway-waybar-ws.log &
PIDP=$!
wait $PIDP
