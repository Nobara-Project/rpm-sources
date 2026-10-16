Name:           snapd
Version:        2.76
Release:        1%{?dist}
Summary:        Meta package that installs snapd and the snap store.
License:        GPL
URL:            https://www.snapcraft.io/snap-store

Requires:       snapd-service
Requires:       snapd-store

%description
Meta package that installs snapd and the snap store.

%prep
# Nothing to prep for now

%build
# No building is necessary, just the installation of the snap store

%install
# We don’t need an actual installation step since it's already handled in %post

%post
# Ensure that snapd is enabled and running, then install the Snap Store

%files
# No files to be packaged for this simple installer

%changelog

