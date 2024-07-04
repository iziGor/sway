#!/bin/env bash
# vim: autoindent smartindent expandtab smarttab tabstop=2 softtabstop=2 shiftwidth=2 :

SFTMP=/tmp/grim-full.png
SCTMP=/tmp/grim-clip.png
grim -l 1 $SFTMP
#imv -f $SFTMP &
nsxiv -f $SFTMP &
IMVPID="$!"
grim -g "$(slurp)" -l 1 $SCTMP
#imv-msg $IMVPID quit
kill $IMVPID
swappy -f $SCTMP
rm -f $SFTMP $SCTMP
