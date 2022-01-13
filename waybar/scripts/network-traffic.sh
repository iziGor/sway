#!/bin/env bash
# vim: autoindent smartindent expandtab smarttab tabstop=2 softtabstop=2 shiftwidth=2 :

print_bytes() {
    if [ "$1" -eq 0 ] || [ "$1" -lt 1000 ]; then
        bytes="0 kB/s"
    elif [ "$1" -lt 1000000 ]; then
        bytes="$(echo "scale=0;$1/1000" | bc -l ) kB/s"
    else
        bytes="$(echo "scale=1;$1/1000000" | bc -l ) MB/s"
    fi

    echo "$bytes"
}

print_bit() {
    if [ "$1" -eq 0 ] || [ "$1" -lt 10 ]; then
        bit="0 B"
    elif [ "$1" -lt 100 ]; then
        bit="$(echo "scale=0;$1*8" | bc -l ) B"
    elif [ "$1" -lt 100000 ]; then
        bit="$(echo "scale=0;$1*8/1000" | bc -l ) K"
    else
        bit="$(echo "scale=1;$1*8/1000000" | bc -l ) M"
    fi

    echo "$bit"
}

setifaces() {
  INTERFACES=""
  ICONS=""
  ICON=""
  for e in $( ls -1b /sys/class/net ); do
    if [[ "$e" != "lo" && "${e:0:3}" != "tap" && $( cat /sys/class/net/$e/carrier 2>/dev/null ) = 1 ]]; then
      [[ -z $INTERFACES ]] && INTERFACES="$e" || INTERFACES="$INTERFACES $e"
      case "$e" in
        eth*)
          ICON=""
          ;;
        wlan*)
          ICON=""
          ;;
        tun*)
          ICON=""
          ;;
        *)
          #ICON=""
          DEVDIR="/sys/class/net/$e/device"
          if [[ -d $DEVDIR ]]; then
            if ( ip addr show $e | grep -qie inet ); then
              { grep DEVTYPE $DEVDIR/uevent 2>/dev/null | grep -iqe usb ; } && ICON="" || ICON=""
            else
              #ICON=""
              true
            fi
          fi
          ;;
      esac
      [[ -z "$ICONS" ]] && ICONS="$ICON" || ICONS="$ICONS:$ICON"
    fi
  done
}

INTERVAL=3
#INTERFACES="enp0s20u2 wlan0"
setifaces

declare -A bytes

for interface in $INTERFACES; do
    bytes[past_rx_$interface]="$(cat /sys/class/net/"$interface"/statistics/rx_bytes)"
    bytes[past_tx_$interface]="$(cat /sys/class/net/"$interface"/statistics/tx_bytes)"
done

while true; do
    down=0
    up=0

    setifaces
    for interface in $INTERFACES; do
        bytes[now_rx_$interface]="$(cat /sys/class/net/"$interface"/statistics/rx_bytes)"
        bytes[now_tx_$interface]="$(cat /sys/class/net/"$interface"/statistics/tx_bytes)"

        bytes_down=$(( (${bytes[now_rx_$interface]} - ${bytes[past_rx_$interface]:-0}) / INTERVAL))
        bytes_up=$(( (${bytes[now_tx_$interface]} - ${bytes[past_tx_$interface]:-0}) / INTERVAL))

        down=$(( "$down" + "$bytes_down" ))
        up=$(( "$up" + "$bytes_up" ))

        bytes[past_rx_$interface]=${bytes[now_rx_$interface]}
        bytes[past_tx_$interface]=${bytes[now_tx_$interface]}
    done

    if [[ -z $ICONS ]]; then
      echo "<span color=\"#aaaa00\"></span>"
    else
      echo "<span color=\"#008080\">$ICONS</span><span color=\"#444\">|</span><span color=\"#1aeeea\"> $(print_bytes $down)</span> / <span color=\"#8382eb\"> $(print_bytes $up)</span>"
      # echo "Download: $(print_bit $down) / Upload: $(print_bit $up)"
    fi

    sleep $INTERVAL
done

