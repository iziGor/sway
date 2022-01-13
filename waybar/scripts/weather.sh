#!/bin/env bash
# vim: autoindent smartindent expandtab smarttab tabstop=2 softtabstop=2 shiftwidth=2 :

cachedir=~/.cache/misc
locfile=${0##*/}-location

if [ ! -d $cachedir ]; then
    mkdir -p $cachedir
fi

if [ ! -f $cachedir/$locfile ]; then
    touch $cachedir/$locfile
fi

if [[ -z "$1" ]]; then
  location="$(cat $cachedir/$locfile)"
else
  location="$1"
fi

cachefile=${0##*/}-$location
cachefile_tt=${0##*/}-tt-$location

if [ ! -f $cachedir/$cachefile ]; then
    touch $cachedir/$cachefile
fi

if [ ! -f $cachedir/$cachefile_tt ]; then
    touch $cachedir/$cachefile_tt
fi

## Save current IFS
#SAVEIFS=$IFS
## Change IFS to new line.
#IFS=$'\n'

cacheage=$(($(date +%s) - $(stat -c '%Y' "$cachedir/$cachefile")))
if [ $cacheage -gt 1740 ] || [ ! -s $cachedir/$cachefile ]; then

  if ping -qc1 wttr.in >/dev/null 2>&1 ; then
    curl -s "https://wttr.in/$location?format=1" >$cachedir/$cachefile
    curl -s "https://ru.wttr.in/$location?0qT" |
      sed 's/\\/\\\\/g' |
        sed ':a;N;$!ba;s/\n/\\n/g' |
          sed 's/"/\\"/g' > $cachedir/$cachefile_tt
  fi
fi

## Restore IFSClear
#IFS=$SAVEIFS

text="$(cat $cachedir/$cachefile)"
tooltip="$(cat $cachedir/$cachefile_tt)"

#echo "{\"text\": \"$text\", \"tooltip\": \"<tt>$tooltip</tt>\", \"class\": \"weather\"}"
echo "{\"text\": \"$text\", \"tooltip\": \"$tooltip\", \"class\": \"weather\"}"

