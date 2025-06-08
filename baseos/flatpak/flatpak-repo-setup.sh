#!/bin/sh

# First we ensure the fedora flatpak repos are deleted if they exist and ignore errors if they don't exist
/usr/bin/flatpak remote-delete --force --system fedora &> /dev/null || true
/usr/bin/flatpak remote-delete --force --system fedora-testing &> /dev/null || true

# Next enable flathub for system/admin installs (add/delete/add to fix gpg error):
/usr/bin/flatpak remote-add --system --if-not-exists --title "Flatpak Official Flathub" flathub /etc/flatpak/remotes.d/flathub.flatpakrepo
/usr/bin/flatpak remote-delete --force --system flathub
/usr/bin/flatpak remote-add --system --if-not-exists --title "Flatpak Official Flathub" flathub /etc/flatpak/remotes.d/flathub.flatpakrepo

# Perform an appstream update to populate metadata
/usr/bin/flatpak update --system --appstream &> /dev/null

# Now we get a list of all users and enable flathub for them, also perform an appstream update to populate metadata
for user in $(getent passwd | awk -F: -v min_uid=1000 -v max_uid=60000 \
        '$3 >= min_uid && $3 <= max_uid && $NF !~ /(\/sbin\/nologin|\/bin\/false)$/ {print $1}')
do
    sudo -H -u $user bash -c '
        /usr/bin/flatpak remote-add --user --if-not-exists --title "Flatpak Official Flathub" flathub /etc/flatpak/remotes.d/flathub.flatpakrepo && \
        /usr/bin/flatpak update --user --appstream &> /dev/null
    '
done
