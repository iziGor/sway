#!/bin/bash
# vim:autoindent:smartindent:expandtab:smarttab:tabstop=2:softtabstop=2:shiftwidth=2

if [ -z $@ ]
then
  function gen_workspaces()
  {
    swaymsg -pt get_workspaces | awk -e '/Workspace/{print $2}'
  }

  echo empty
  gen_workspaces
else
  WORKSPACE=$@

  if [ x"empty" = x"${WORKSPACE}" ]
  then
    ${HOME}/.config/sway/scripts/empty_workspace.sh >/dev/null
  elif [ -n "${WORKSPACE}" ]
  then
    swaymsg workspace "${WORKSPACE}" >/dev/null
  fi
fi

