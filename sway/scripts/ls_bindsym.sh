#!/bin/bash
# vim:autoindent:smartindent:expandtab:smarttab:tabstop=2:softtabstop=2:shiftwidth=2

if [[ -z "$@" ]]
then
  grep -vE '^\s*#' ~/.config/sway/config | grep bindsym | sed -e 's/bindsym\s//'
else
  true
fi
