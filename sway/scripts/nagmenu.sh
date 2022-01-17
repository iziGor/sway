#!/bin/bash
# vim:autoindent:smartindent:expandtab:smarttab:tabstop=2:softtabstop=2:shiftwidth=2

DELAY="3"
INPMSG="<span color='red'><b>Really exit from sway?</b></span>"
EXPMSG="<span color='red'>sway finos sua laboro pos $DELAY sekundi.</span>"
retv=$( echo 'Yes|No' | rofi -dmenu -sep '|' -p "" -mesg "$INPMSG" -lines 1 -columns 2 -i -width -30 )
if [[ $retv == Yes ]] ; then
  coproc rofi -e "$EXPMSG" -markup -width -36
  sleep $DELAY
  pkill -f 'python-exec.*i3-cycle-focus'
  pkill -u "${USER}" -x pipewire\|wireplumber 1>/dev/null 2>&1
  swaymsg exit
fi
