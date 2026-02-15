#!/bin/env bash
# vim: autoindent smartindent expandtab smarttab tabstop=2 softtabstop=2 shiftwidth=2 :

cachedir="$HOME/.cache/misc"
locfile="${0##*/}-location"
loclist="locations.lst"
TMPOUT=""
AGELMT=$(( 29 * 60 ))

if [[ ! -d $cachedir ]]; then
    mkdir -p "$cachedir"
fi

if [[ ! -f $cachedir/$locfile ]]; then
    echo Moscow >"$cachedir/$locfile"
fi

if [[ ! -f $cachedir/$loclist ]]; then
    echo Moscow Москва >"$cachedir/$loclist"
fi

if [[ "${1@L}" == "setloc" ]]; then
  location="$(cat $cachedir/$loclist | rofi -dmenu -p 'Select location:' | awk '{print $1}')"
  if [[ -n $location ]]; then
    echo $location >"$cachedir/$locfile"
  fi
  exit
fi

if [[ -z "$1" ]]; then
  location="$(cat $cachedir/$locfile)"
else
  location="$1"
fi

cachefile="${0##*/}-$location"
cachefile_tt="${0##*/}-tt-$location"

if [[ ! -f $cachedir/$cachefile ]]; then
    touch "$cachedir/$cachefile"
fi

if [[ ! -f $cachedir/$cachefile_tt ]]; then
    touch "$cachedir/$cachefile_tt"
fi

## Save current IFS
#SAVEIFS=$IFS
## Change IFS to new line.
#IFS=$'\n'

_save_tt () {
  # curl --connect-timeout 15 -s -H "Accept-Language: ru" "wttr.in/$location?0q" |
  curl --connect-timeout 15 -s -H "Accept-Language: ru" "wttr.in/$location" |
    ansi2html -pi |
    weather-normal-span.py > "$cachedir"/"$cachefile_tt"
}

cacheage=$(($(date +%s) - $(stat -c '%Y' "$cachedir/$cachefile")))
if [[ $cacheage -gt $AGELMT ]] || [[ ! -s $cachedir/$cachefile ]]; then

  # disabled because 'ping' cannot resolve the name of the resource
  # deskapabligita nam programo 'ping' falias resolvar/obtenar adreso di situo
  # if ping -qc1 wttr.in >/dev/null 2>&1 ; then
    # TMPOUT=$(curl -s "https://wttr.in/$location?format=1")
    TMPOUT=$(curl --connect-timeout 15 -s -H "Accept-Language: ru" "wttr.in/$location?format=1")
    # curl -s "https://wttr.in/$location?format=1" >$cachedir/$cachefile
    if [[ -n "$TMPOUT" ]] ; then
      case "$TMPOUT" in
        *already*|*location*|*Empty*)
          # TMPOUT=""
          ;;
        *)
          echo "$TMPOUT" | tr -s '[:blank:]' >"$cachedir"/"$cachefile"
          # curl -s "https://ru.wttr.in/$location?0qT" |
          # curl --connect-timeout 15 -s -H "Accept-Language: ru" "wttr.in/$location?0q" |
          #   sed 's/\\/\\\\/g' |
          #     sed ':a;N;$!ba;s/\n/\\n/g' |
          #         ansi2html -i |
          #           sed 's/<span style="font-weight: bold">\(.\)<\/span>/<b>\1<\/b>/g' |
          #           sed 's/style="color: \(#......\)"/color=\\"\1\\"/g' |
          #           sed 's/"/\\"/g' > "$cachedir"/"$cachefile_tt"
          #           # sed 's/style="color: /color="/g' > "$cachedir"/"$cachefile_tt"
          _save_tt
          ;;
      esac
    else
      true
    fi
  # fi
fi

cacheage=$(($(date +%s) - $(stat -c '%Y' "$cachedir/$cachefile_tt")))
if [[ $cacheage -gt $AGELMT ]] || [[ ! -s $cachedir/$cachefile_tt ]]; then
  _save_tt
fi

## Restore IFSClear
#IFS=$SAVEIFS

text="$(cat $cachedir/$cachefile)"
tooltip="$(cat $cachedir/$cachefile_tt)"

# echo "{\"text\": \"$text\", \"tooltip\": \"<tt>$tooltip</tt>\", \"class\": \"weather\"}"
echo "{\"text\": \"$text\", \"tooltip\": \"$tooltip\", \"class\": \"weather\"}"

