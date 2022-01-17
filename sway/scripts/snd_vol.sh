#!/bin/bash
# vim:autoindent:smartindent:expandtab:smarttab:tabstop=2:softtabstop=2:shiftwidth=2

SINK="$(LC_ALL=C pactl info | grep -ie 'default sink:' | awk -F ': ' '{print $2}')"

if [[ -n $SINK ]]; then
  pactl set-sink-volume "$SINK" "$1"
fi
