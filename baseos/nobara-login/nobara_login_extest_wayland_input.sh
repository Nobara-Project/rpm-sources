#!/bin/sh

if [ "$(id -u)" -ne 0 ]; then
    if command -v flatpak >/tmp/flatpak_path.$$ 2>/dev/null && read -r _ </tmp/flatpak_path.$$; then
        flatpak permission-set kde-authorized remote-desktop "" yes
        rm -f /tmp/flatpak_path.$$
    else
        rm -f /tmp/flatpak_path.$$
    fi
fi
