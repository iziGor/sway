#!/bin/env bash
# vim: autoindent smartindent expandtab smarttab tabstop=2 softtabstop=2 shiftwidth=2 :

text="$(free | awk '/Swap/{printf("%.0f%"), $3/$2*100}')"
tooltip="$(free | awk '/Swap/{printf("Swap used: %.1fMB"), $3/1000}')"
echo "{\"text\": \"$text\", \"tooltip\": \"$tooltip\"}"
