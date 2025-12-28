#!/bin/sh

# Quietly bail if xdg-mime isn't available (no stdout)
XDG_MIME=$(command -v xdg-mime) || exit 0
[ -n "$XDG_MIME" ] || exit 0

# application/x-rpm default
defaultrpm=$(xdg-mime query default application/x-rpm)
if [ "$defaultrpm" != "/usr/share/applications/nobara-rpm-installer.desktop" ]; then
    xdg-mime default /usr/share/applications/nobara-rpm-installer.desktop application/x-rpm
fi

# application/x-src+rpm: only set if there is no current default
defaultsrcrpm=$(xdg-mime query default application/x-src+rpm)
if [ -z "$defaultsrcrpm" ]; then
    if [ "$XDG_CURRENT_DESKTOP" = "KDE" ]; then
        xdg-mime default /usr/share/applications/org.kde.ark.desktop application/x-src+rpm
    elif [ "$XDG_CURRENT_DESKTOP" = "GNOME" ]; then
        xdg-mime default /usr/share/applications/org.gnome.FileRoller.desktop application/x-src+rpm
    fi
fi
