#!/bin/sh

# First we enable the fedora flatpak repos if they dont exist, then we delete them. This ensures deletion without exit code 1 in case they dont exist to begin with (new installs). If they do exist (old installs) it wont create them due to the --if-not-exists option, but it will delete them as expected.
/usr/bin/flatpak remote-add --system --if-not-exists --title "Fedora Flatpaks" fedora oci+https://registry.fedoraproject.org
/usr/bin/flatpak remote-add --system --if-not-exists --disable --title "Fedora Flatpaks (testing)" fedora-testing oci+https://registry.fedoraproject.org#testing
/usr/bin/flatpak remote-delete --force --system fedora
/usr/bin/flatpak remote-delete --force --system fedora-testing

# Next enable flathub for system/admin installs (add/delete/add to fix gpg error):
/usr/bin/flatpak remote-add --system --if-not-exists --title "Flatpak Official Flathub" flathub /etc/flatpak/remotes.d/flathub.flatpakrepo
/usr/bin/flatpak remote-delete --force --system flathub
/usr/bin/flatpak remote-add --system --if-not-exists --title "Flatpak Official Flathub" flathub /etc/flatpak/remotes.d/flathub.flatpakrepo

# Next enable flathub beta for system/admin installs (add/delete/add to fix gpg error):
/usr/bin/flatpak remote-add --system --if-not-exists --title "Flatpak Official Flathub (Beta)" flathub-beta /etc/flatpak/remotes.d/flathub-beta.flatpakrepo
/usr/bin/flatpak remote-delete --force --system flathub-beta
/usr/bin/flatpak remote-add --system --if-not-exists --title "Flatpak Official Flathub (Beta)" flathub-beta /etc/flatpak/remotes.d/flathub-beta.flatpakrepo

# Perform a search to populate metadata
/usr/bin/flatpak search --system chromium &> /dev/null

# Now we get a list of all users and enable flathub for them, also perform a search to populate metadata
for user in $(getent passwd {1000..60000} | cut -d: -f1)
do
	sudo -H -u $user bash -c '/usr/bin/flatpak remote-add --user --if-not-exists --title "Flatpak Official Flathub" flathub /etc/flatpak/remotes.d/flathub.flatpakrepo'
	sudo -H -u $user bash -c '/usr/bin/flatpak remote-add --user --if-not-exists --title "Flatpak Official Flathub (Beta)" flathub-beta /etc/flatpak/remotes.d/flathub-beta.flatpakrepo'
	sudo -H -u $user bash -c '/usr/bin/flatpak search --user chromium &> /dev/null'
done
