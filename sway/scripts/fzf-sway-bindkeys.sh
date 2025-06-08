#!/bin/zsh
# vim: autoindent smartindent expandtab smarttab tabstop=2 softtabstop=2 shiftwidth=2 :
/home/izoom/.local/bin/fzf-sway-bindkeys.py | fzf --reverse --exact --no-multi --no-sort --preview='echo {}' --preview-window='down,40%:wrap:hidden' --bind 'ctrl-v:toggle-preview'
