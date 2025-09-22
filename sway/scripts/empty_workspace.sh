#!/usr/bin/env bash
# vim:autoindent:smartindent:expandtab:smarttab:tabstop=2:softtabstop=2:shiftwidth=2

MAX_DESKTOPS=20
WORKSPACES=$(seq -s '\n' 1 1 ${MAX_DESKTOPS})
EMPTY_WORKSPACE=$( (swaymsg -pt get_workspaces | awk -e '/Workspace [0-9]+/ {print gensub(/Workspace ([0-9]+).*$/, "\\1", 1)}' ; \
  echo -e "${WORKSPACES}" ) | sort -n | uniq -u | head -n 1)

swaymsg workspace "${EMPTY_WORKSPACE}"
