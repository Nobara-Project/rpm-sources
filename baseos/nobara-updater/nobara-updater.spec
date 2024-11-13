Name:          nobara-updater
Version:       1.0.0
Release:       83%{?dist}
License:       GPL-3.0-or-later
Summary:       Nobara System Updater

URL:            https://github.com/nobara-project/nobara-core-packages
Source0:        %{URL}/releases/download/1.0/nobara-updater.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  make

Provides:	nobara-updater

# App Deps
Requires: python
Requires: python3
Requires: python3-gobject
Requires: python3-psutil
Requires: python3-requests
Requires: python3-dnf
Requires: python3-libdnf5
Requires: python3-packaging
Requires: python3-tkinter
Requires: python3-dasbus
Requires: python3-cairo
Requires: python3-pillow
Requires: python3-pillow-tk
Requires: python3-evdev
Requires: python3-vdf

Requires: akmods
Requires: dracut
Requires: flatpak
Requires: glib2
Requires: gtk3
Requires: gtk4
Requires: libadwaita
Requires: rpm
Requires: systemd
Requires: util-linux
Requires: xdg-utils
Requires: xprop

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
%{_bindir}/nobara-tweak-tool
%{_bindir}/nobara-updater-gamescope-gui
%{_bindir}/nobara-browser-select
%{_datadir}/applications/nobara-updater.desktop
%{_datadir}/applications/nobara-tweak-tool.desktop
%{_datadir}/icons/hicolor/64x64/apps/nobara-updater.svg
%{_datadir}/nobara-gamescope/browser-select/*

%clean
rm -rf %{buildroot}

%changelog
* Fri Jun 28 2024 Your Name <you@example.com> - 1.0-1
- Initial package
