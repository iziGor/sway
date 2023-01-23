#!/usr/bin/env bash
# vim: autoindent smartindent expandtab smarttab tabstop=2 softtabstop=2 shiftwidth=2 :

PROGCTL=$( command -v systemctl  2>/dev/null)

if [[ -z $PROGCTL ]]; then
  PROGCTL=$( command -v loginctl  2>/dev/null)
fi

if [[ -z $PROGCTL ]]; then
  echo Programo por guvernar dormo-stato ne prezentesas.
  exit 1
fi

case "${1@L}" in
  susp*) SUSPMODE=suspend
  ;;
  hiber*) SUSPMODE=hibernate
  ;;
  hybri*) SUSPMODE="hybrid-sleep"
  ;;
  *) SUSPMODE=suspend
  ;;
esac
exec sudo $PROGCTL $SUSPMODE
#echo exec sudo $PROGCTL $SUSPMODE
