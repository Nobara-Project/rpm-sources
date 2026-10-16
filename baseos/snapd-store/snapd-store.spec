Name:           snapd-store
Version:        2.76
Release:        1%{?dist}
Summary:        Installs the Snap Store via Snapd
License:        GPL
URL:            https://www.snapcraft.io/snap-store

Requires:       snapd-service

%description
This package installs the Snap Store using the Snapd service.

%prep
# Nothing to prep for now

%build
# No building is necessary, just the installation of the snap store

%install
# no install steps, everything done in post

%post
# snapd.service is socket-activated: on a new install only snapd.socket is
# running (snapd-service's %post starts it), and snap starts snapd through it.
# A freshly started snapd refuses installs until it has seeded ("too early
# for operation"), which takes about a second.
if systemctl is-active snapd.socket >/dev/null 2>&1; then
    snap wait system seed.loaded
    snap install snap-store
fi
# The store comes from the network and may not be there (offline, chroot), so
# copying its launchers must not fail the transaction.
cp -R /var/lib/snapd/desktop/applications/snap-store*.desktop /usr/share/applications/ 2>/dev/null || :

%files
# No files to be packaged for this simple installer

%changelog
