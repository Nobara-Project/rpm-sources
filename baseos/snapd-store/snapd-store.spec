Name:           snapd-store
Version:        2.72
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
# Ensure that snapd is enabled and running, then install the Snap Store
if systemctl is-active snapd.apparmor.service >/dev/null 2>&1; then
    snap install snap-store
elif systemctl is-active snapd.service >/dev/null 2>&1; then
    snap install snap-store
fi
cp -R /var/lib/snapd/desktop/applications/snap-store*.desktop /usr/share/applications/

%files
# No files to be packaged for this simple installer

%changelog
