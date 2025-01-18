#!/usr/bin/bash

defaultrpm=$(xdg-mime query default application/x-rpm)
if [[ $defaultrpm != "/usr/share/applications/nobara-rpm-installer.desktop"  ]]; then
    xdg-mime default /usr/share/applications/nobara-rpm-installer.desktop application/x-rpm
    echo changed
fi

if [[ $XDG_CURRENT_DESKTOP == "KDE" ]]; then
    defaultsrcrpm=$(xdg-mime query default application/x-src+rpm)
    if [[ $defaultsrcrpm != "/usr/share/applications/org.kde.ark.desktop"  ]]; then
        xdg-mime default /usr/share/applications/org.kde.ark.desktop application/x-src+rpm
        echo changed
    fi
fi

if [[ $XDG_CURRENT_DESKTOP == "GNOME" ]]; then
    defaultsrcrpm=$(xdg-mime query default application/x-src+rpm)
    if [[ $defaultsrcrpm != "/usr/share/applications/org.gnome.FileRoller.desktop"  ]]; then
        xdg-mime default /usr/share/applications/org.gnome.FileRoller.desktop application/x-src+rpm
        echo changed
    fi
fi
