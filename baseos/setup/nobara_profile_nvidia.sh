#!/usr/bin/sh

# nvidia rendering fixup — fast sysfs check (replaces slow lspci)
if grep -rq "0x10de" /sys/bus/pci/devices/*/vendor 2>/dev/null; then
    export EGL_PLATFORM="$XDG_SESSION_TYPE"
    export GAMESCOPE_WSI_HIDE_PRESENT_EXT=1
fi
