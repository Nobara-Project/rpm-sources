Name:          nobara-updater
Version:       1.0.0
Release:       31%{?dist}
License:       GPL-3.0-or-later
Summary:       Nobara System Updater

URL:            https://github.com/nobara-project/nobara-core-packages
Source0:        %{URL}/releases/download/1.0/nobara-updater.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  make

Requires:	python3
Requires:	python
Requires:	gtk3
Requires:	gtk4
Requires:	libadwaita
Requires: 	glib2
Provides:	nobara-updater

# App Deps
Requires: python3
Requires: python3-gobject
Requires: python3-psutil
Requires: python3-requests
Requires: python3-dnf
Requires: python3-libdnf5
Requires: python3-packaging
Requires: flatpak
Requires: gtk3
Requires: python3-dasbus

Requires: akmods
Requires: dracut
Requires: rpm
Requires: systemd
Requires: xdg-utils
Requires: util-linux

Provides: nobara-sync
Obsoletes: nobara-sync

Requires:	nobara-welcome > 5.0.1
Requires:	nobara-driver-manager > 1.0
Requires:	yumex > 5.0.2

%description
Nobara System Updater.

%prep
%autosetup -p1 -n nobara-updater

%build
make all DESTDIR=%{buildroot}

%files
%license %{_datadir}/licenses/nobara-updater/LICENSE
%{python3_sitelib}/nobara_updater/
%{_bindir}/nobara-sync
%{_bindir}/nobara-updater
%{_datadir}/applications/nobara-updater.desktop
%{_datadir}/icons/hicolor/64x64/apps/nobara-updater.svg

%clean
rm -rf %{buildroot}

%changelog
* Fri Jun 28 2024 Your Name <you@example.com> - 1.0-1
- Initial package
