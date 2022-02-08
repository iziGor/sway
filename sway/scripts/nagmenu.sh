#!/bin/bash
# vim:autoindent:smartindent:expandtab:smarttab:tabstop=2:softtabstop=2:shiftwidth=2

PADPREF=''

padprefix() {
  for (( i=0; i<$1; i++ )); do
    PADPREF="$PADPREF "
  done
}

DELAY="3"
MSGWIDTH=38
INPMSG="<span color='red'><b>Really exit from sway?</b></span>"
EXPMSG="sway finos sua laboro pos $DELAY sekundi."
LENMSG=$(echo -n $EXPMSG | wc -m)
#echo $LENMSG
LENMSG=$(( $(( $MSGWIDTH - $LENMSG )) / 2 ))
#echo $LENMSG
padprefix $LENMSG
#echo $( echo -n "$PADPREF" | wc -m )
EXPMSG="<span color='red'>${PADPREF}${EXPMSG}</span>"
retv=$( echo 'Yes|No' | rofi -dmenu -sep '|' -p "" -mesg "$INPMSG" -lines 1 -columns 2 -i -width -30 )
if [[ $retv == Yes ]] ; then
  #coproc rofi -e "$EXPMSG" -markup -width $MSGWIDTH
  coproc rofi -e "$EXPMSG" -markup -theme-str "#window { width: ${MSGWIDTH}ch; }"
  sleep $DELAY
  pkill -f 'python-exec.*i3-cycle-focus'
  pkill -u "${USER}" -x pipewire\|wireplumber 1>/dev/null 2>&1
  swaymsg exit
fi
