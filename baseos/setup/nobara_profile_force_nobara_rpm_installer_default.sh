#!/bin/sh

# Exit quietly if xdg-mime isn't available
command -v xdg-mime >/dev/null 2>&1 || exit 0

# Run xdg-mime with no output (stdout+stderr)
xdg_mime() { xdg-mime "$@" >/dev/null 2>&1; }

# Query default with no noise; prints nothing except the value we capture
xdg_mime_query_default() {
    xdg-mime query default "$1" 2>/dev/null
}

# application/x-rpm default
defaultrpm="$(xdg_mime_query_default application/x-rpm)"
if [ "$defaultrpm" != "nobara-rpm-installer.desktop" ]; then
    xdg_mime default nobara-rpm-installer.desktop application/x-rpm
fi

# application/x-src+rpm: only set if there's no current default
defaultsrcrpm="$(xdg_mime_query_default application/x-src+rpm)"
if [ -z "$defaultsrcrpm" ]; then
    if [ "$XDG_CURRENT_DESKTOP" = "KDE" ]; then
        xdg_mime default org.kde.ark.desktop application/x-src+rpm
    elif [ "$XDG_CURRENT_DESKTOP" = "GNOME" ]; then
        xdg_mime default org.gnome.FileRoller.desktop application/x-src+rpm
    fi
fi
