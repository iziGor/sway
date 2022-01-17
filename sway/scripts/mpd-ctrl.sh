#!/bin/env bash
# vim: autoindent smartindent expandtab smarttab tabstop=2 softtabstop=2 shiftwidth=2 :

chk_mpd () {
  pgrep mpd >/dev/null
}

#chk_mpd || exit 1

if [[ -z "$@" ]]; then
  mpc current
else
  case "$1" in
    current)
      TITLE="$(mpc | grep -E '\[playing\]|\[paused\]')"
      [[ -z "${TITLE}" ]] && notify-send -i stremio  "mpd stopped" "" \
          || notify-send -i stremio "${TITLE}" "$(mpc $1)"
          #notify-send -i musikcube "Now playing" "$(mpc $1)"
      ;;
    toggle|next|prev)
      mpc $1
      ;;
  esac
fi


