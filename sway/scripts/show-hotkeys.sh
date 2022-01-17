#!/bin/bash
# vim:autoindent:smartindent:expandtab:smarttab:tabstop=2:softtabstop=2:shiftwidth=2

#MOD=$(grep -vE '^\s*#' ~/.config/sway/config | grep -E 'set\s\$mod' | awk '{print $3}')
#if [[ -z $MOD ]]; then
  #MOD=Mod4
#fi

SCRIPTDIR="~/.config/sway/scripts"
RETV=$( rofi -modi "macro:${SCRIPTDIR}/ls_macro.sh,hotkey:${SCRIPTDIR}/ls_bindsym.sh" -show hotkey -width 1850)
echo $RETV
