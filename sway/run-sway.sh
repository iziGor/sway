#!/bin/env /bin/bash
# vim: autoindent smartindent expandtab smarttab tabstop=2 softtabstop=2 shiftwidth=2 filetype=sh:

#[ -n $1 ] && [ -f "$1" ] && VIDEO="$(realpath "$1")"

_no_exucutable1 () {
  export MOZ_ENABLE_WAYLAND=1
  export QT_QPA_PLATFORM=wayland-egl
  export CLUTTER_BACKEND=wayland
  export ECORE_EVAS_ENGINE=wayland-egl
  export ELM_ENGINE=wayland_egl
  export SDL_VIDEODRIVER=wayland
  export NO_AT_BRIDGE=1
  export _JAVA_AWT_WM_NONREPARENTING=1
  export QT_AUTO_SCREEN_SCALE_FACTOR=0
  export TDESKTOP_DISABLE_GTK_INTEGRATION=1
}

_no_exucutable2 () {
  # qt env variables
  QT_QPA_PLATFORMTHEME=qt5ct
  QT_QPA_PLATFORM=wayland-egl
  QT_WAYLAND_FORCE_DPI=physical
  QT_WAYLAND_DISABLE_WINDOWDECORATION=1

  # if app support disable csd
  GTK_CSD=0

  # settings for efl
  ELM_DISPLAY=wl
  ECORE_EVAS_ENGINE=wayland_egl
  ELM_ENGINE=wayland_egl
  ELM_ACCEL=opengl

  # sdl wayland
  SDL_VIDEODRIVER=wayland

  # java fix
  _JAVA_AWT_WM_NONREPARENTING=1

  # clutter wayland
  CLUTTER_BACKEND=wayland

  # gtk wayland
  GDK_BACKEND=wayland

  # fix for xwayland
  NO_AT_BRIDGE=1

  # wayland for fucking rust winit
  WINIT_UNIX_BACKEND=wayland

  # wayland support for firefox
  MOZ_ENABLE_WAYLAND=1
  #MOZ_USE_XINPUT2=1

  # configure gpu accel
  __GL_GSYNC_ALLOWED=0
  __GL_VRR_ALLOWED=0
  __GLX_VENDOR_LIBRARY_NAME=nvidia
  LIBVA_DRIVER_NAME=nvidia

  # some prefs for sway
  #GBM_BACKEND=nvidia-drm
  WLR_NO_HARDWARE_CURSORS=1
  WLR_RENDERER=vulkan

  # set desktop sway
  XDG_CURRENT_DESKTOP=sway
  XDG_SESSION_TYPE=wayland

  # wayland for egl
  EGL_PLATFORM=wayland

  # set seatd backend
  LIBSEAT_BACKEND=logind
}

# пробуем, что там насоветовали
export  GTK_CSD=0
export  SDL_VIDEODRIVER=wayland
export  GDK_BACKEND=wayland
export  EGL_PLATFORM=wayland
export  XDG_CURRENT_DESKTOP=sway
export  XDG_SESSION_TYPE=wayland
#export  MOZ_ENABLE_WAYLAND=1

export I3CMDHF=$HOME/tmp/i3-cmd-history
export QT_WAYLAND_DISABLE_WINDOWDECORATION=1
export QT_QPA_PLATFORM=wayland
export QT_QPA_PLATFORMTHEME=qt5ct
#export WLR_DRM_DEVICES="/dev/dri/card1"
#export DRI_PRIME=1
LOGFILE="$HOME/logs/sway.log"
unset XSESSION

export  XCURSOR_PATH=${XCURSOR_PATH}:~/.local/share/icons

# для работы tray в waybar
#export XDG_CURRENT_DESKTOP=Unity

if command -v systemctl >/dev/null 2>&1 && systemctl --user list-jobs >/dev/null 2>&1 ; then
  # we are in systemd environment
  exec sway >>${LOGFILE} 2>&1
else
  # we are in non-systemd environment (openrc?)
  #dbus-run-session sway >>${LOGFILE} 2>&1
  dbus-launch --exit-with-session sway >>${LOGFILE} 2>&1
fi

