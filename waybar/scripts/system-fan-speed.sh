#!/bin/env bash
# vim: autoindent smartindent expandtab smarttab tabstop=2 softtabstop=2 shiftwidth=2 :

#speed=$(sensors 2>/dev/null | grep fan1 | cut -d " " -f 9)
speed="$(sensors 2>/dev/null | grep fan1 | awk -e '{print $2}')"

if [ "$speed" != "" ]; then
  speed_round="$(echo "scale=1;$speed/1000" | bc -l )"
    echo $speed_round
    #echo "%{F#61bbf6}%{F-} $speed_round"
    #echo "%{F#61bbf6}%{F-} $speed_round"
else
  echo 
   #echo "%{F#61bbf6}%{F-}"
   #echo "%{F#61bbf6}%{F-}"
fi

