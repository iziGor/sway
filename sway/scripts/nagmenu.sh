#!/bin/bash
# vim:autoindent:smartindent:expandtab:smarttab:tabstop=2:softtabstop=2:shiftwidth=2

#PADPREF=''

#padprefix() {
  #for (( i=0; i<$1; i++ )); do
    #PADPREF="$PADPREF "
  #done
#}

DELAY="3"
#MSGWIDTH=52
INPMSG="<span color='red'><b>Really exit from sway?</b></span>"
EXPMSG="sway finos sua laboro pos $DELAY sekundi."
#LENMSG=$(echo -n $EXPMSG | wc -m)
#exit
#padprefix $(( $(( $MSGWIDTH - $LENMSG )) / 2 - 1 ))
#echo $( echo -n "$PADPREF" | wc -m )
#EXPMSG="<span color='red'>${PADPREF}${EXPMSG}</span>"
#EXPMSG="<span color='yellow'>${PADPREF}${EXPMSG}</span>"
EXPMSG="<span color='yellow'>${EXPMSG}</span>"
#retv=$( echo 'Yes|No' | rofi -dmenu -sep '|' -p "" -mesg "$INPMSG" -lines 1 -columns 2 -i -width -30 )
retv=$( echo 'Yes|No' | rofi -dmenu -sep '|' -p "" -mesg "$INPMSG" -theme-str "listview { lines: 2; }" -i )
if [[ $retv == Yes ]] ; then
  #coproc rofi -e "$EXPMSG" -markup -width $MSGWIDTH
  coproc rofi -e "$EXPMSG" -markup -theme-str "textbox { horizontal-align: 0.5; }"
  sleep $DELAY
  pkill -f 'python-exec.*i3-cycle-focus'
  pkill -u "${USER}" -x pipewire\|wireplumber 1>/dev/null 2>&1
  swaymsg exit
fi
