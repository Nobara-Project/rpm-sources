# Disable debug packages
%define debug_package %{nil}

Name:           kde-steamdeck-additions
Version:        6.2.2
Release:        1%{?dist}
Summary:        SteamOS Nested Desktop + "Add to Steam" right-click services
License:        GPLv2
URL:            https://github.com/nobara-project/steamdeck-edition-packages
Source0:        %{URL}/releases/download/1.0/kde-steamdeck-additions.tar.gz
BuildArch:      noarch

Requires:       kde-filesystem
Provides:       kde-steamdeck-additions
Provides:       plasma-lookandfeel-nobara-steamdeck-additions
Obsoletes:       plasma-lookandfeel-nobara-steamdeck-additions

Conflicts:      steamdeck-backgrounds
Conflicts:      steameck-gnome-presets

%description
This package includes KDE presets and enhancements from Valve's SteamOS, including the SteamOS Nested Desktop environment and various utilities.

%prep
%setup -T -b 0 -q -n kde-steamdeck-additions

%build
# Nothing to build

%install
# Copying binaries
mkdir -p %{buildroot}%{_bindir}
cp -rv usr/bin/* %{buildroot}%{_bindir}

# Copying udev rules
mkdir -p %{buildroot}%{_prefix}/lib/udev/rules.d
cp -rv usr/lib/udev/rules.d/* %{buildroot}%{_prefix}/lib/udev/rules.d

# Copying application desktop files and assets
mkdir -p %{buildroot}%{_datadir}/applications/steam/steamos-nested-desktop
cp -rv usr/share/applications/steam/steamos-nested-desktop/* %{buildroot}%{_datadir}/applications/steam/steamos-nested-desktop

# Copying additional KDE service menus and configurations
mkdir -p %{buildroot}%{_datadir}/kservices5/ServiceMenus
cp -rv usr/share/kservices5/ServiceMenus/* %{buildroot}%{_datadir}/kservices5/ServiceMenus

mkdir -p %{buildroot}%{_datadir}/plasma/kickeractions
cp -rv usr/share/plasma/kickeractions/* %{buildroot}%{_datadir}/plasma/kickeractions

# Copying X11 configurations
mkdir -p %{buildroot}%{_datadir}/X11/xorg.conf.d
cp -rv usr/share/X11/xorg.conf.d/* %{buildroot}%{_datadir}/X11/xorg.conf.d

%files
%{_bindir}/jupiter-plasma-bootstrap
%{_bindir}/steamos-add-to-steam
%{_bindir}/steamos-nested-desktop
%{_prefix}/lib/udev/rules.d/99-kwin-ignore-tablet-mode.rules
%{_datadir}/applications/steam/steamos-nested-desktop/*
%{_datadir}/kservices5/ServiceMenus/steam.desktop
%{_datadir}/plasma/kickeractions/steam.desktop
%{_datadir}/X11/xorg.conf.d/99-pointer.conf

%changelog
* Sat Dec 9 2023 Matthew Schwartz <njtransit215@gmail.com> - 2.0
- implemented updated nested desktop script that follows native display resolution when creating nested desktop session.tested: rog ally, steam deck, legion go


