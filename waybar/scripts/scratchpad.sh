#!/bin/env bash
# vim: autoindent smartindent expandtab smarttab tabstop=2 softtabstop=2 shiftwidth=2 :

scratchpad="$(swaymsg -t get_tree | jq 'recurse(.nodes[]) | first(select(.name=="__i3_scratch")) | .floating_nodes | length')"
#scratchpad="1"
case $scratchpad in
  0) text="" ;;
  *) text=" $scratchpad" ;;
esac
class=$scratchpad
[[ $scratchpad > 7 ]] && class="7"
echo "{\"text\": \"$text\", \"class\": \"$class\"}"

