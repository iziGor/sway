#!/usr/bin/env bash
# vim:autoindent:smartindent:expandtab:smarttab:tabstop=2:softtabstop=2:shiftwidth=2

SWAYSCRIPTDIR="${XDG_CONFIG_HOME:-$HOME/.config}/sway/scripts"

if ( command -v systemctl >/dev/null 2>&1 && systemctl --user list-jobs >/dev/null 2>&1 ); then
  # nexta du instrucioni dev esar nur ye un lineo nam li dev startesar unu pos altra
  # systemctl --user import-environment {,WAYLAND_}DISPLAY SWAYSOCK; systemctl --user start sway-session.target; systemctl --user start dunst.service
  # # foot-server стартует через `systemd --user enable foot...`
  # swaymsg -t subscribe '["shutdown"]' && systemctl --user stop sway-session.target

  # запускаем сессию, используя инструменты, взятые с https://github.com/alebastr/sway-systemd
  exec ${SWAYSCRIPTDIR}/session.sh
else
  dunst &
  foot -s &
fi
