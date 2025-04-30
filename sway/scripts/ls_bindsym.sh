#!/bin/bash
# vim:autoindent:smartindent:expandtab:smarttab:tabstop=2:softtabstop=2:shiftwidth=2

if [[ -z "$@" ]]
then
  grep -vE '^\s*#' ~/.config/sway/config | grep -E 'bind(sy|co|sw|ge)' | sed -Ee 's/bind(sy|co|sw|ge)[^[:blank:]]+\s/b\1 /'
else
  true
fi
