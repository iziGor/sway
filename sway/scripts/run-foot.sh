#!/usr/bin/env bash
# vim:autoindent:smartindent:expandtab:smarttab:tabstop=2:softtabstop=2:shiftwidth=2

if ! ( command -v systemctl >/dev/null 2>&1 && systemctl --user list-jobs >/dev/null 2>&1 ); then
  exec foot -s &
else
  exec systemd-run --user --no-block --unit=foot foot --server
fi
