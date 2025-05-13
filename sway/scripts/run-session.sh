#!/usr/bin/env bash
# vim:autoindent:smartindent:expandtab:smarttab:tabstop=2:softtabstop=2:shiftwidth=2

SWAYSCRIPTDIR="${XDG_CONFIG_HOME:-$HOME/.config}/sway/scripts"

if ( command -v systemctl >/dev/null 2>&1 && systemctl --user list-jobs >/dev/null 2>&1 ); then
  # nexta du instrucioni dev esar nur ye un lineo nam li dev startesar unu pos altra
  # systemctl --user import-environment {,WAYLAND_}DISPLAY SWAYSOCK; systemctl --user start sway-session.target; systemctl --user start dunst.service
  # # foot-server стартует через `systemctl --user enable foot...`
  # или через systemd-run
  # systemd-run --user --no-block --unit=foot foot --server
  # swaymsg -t subscribe '["shutdown"]' && systemctl --user stop sway-session.target

  # запускаем сессию, используя инструменты, взятые с https://github.com/alebastr/sway-systemd
  exec ${SWAYSCRIPTDIR}/session.sh --add-env=GTK_CSD --add-env=SDL_VIDEODRIVER --add-env=GDK_BACKEND --add-env=EGL_PLATFORM --add-env=QT_WAYLAND_DISABLE_WINDOWDECORATION --add-env=XCURSOR_PATH --add-env=YDOTOOL_SOCKET --add-env=LIBVA_DRIVER_NAME
else
  dunst &
  foot -s &
fi
