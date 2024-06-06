Name:           kde-nobara
Version:        6.0.5
Release:        2%{?dist}
Summary:        KDE Presets from NobaraProject Official
License:    	GPLv2
URL:            https://github.com/nobara-project/nobara-core-packages
Source0:        %{URL}/releases/download/1.0/kde-nobara.tar.gz
BuildArch:      noarch

Requires:		kde-filesystem
Requires:       papirus-icon-theme
Requires:       kde-rounded-corners
Provides:       kde-nobara
Provides: plasma-lookandfeel-nobara
Requires: kde-nobara-sddm
Recommends: kde-steamdeck-additions
Recommends: kde-nobara-extras-wallpapers
Obsoletes: nobara-kde-presets
Obsoletes: plasma-lookandfeel-nobara
# https://bugzilla.redhat.com/show_bug.cgi?id=1356890
Obsoletes: f22-kde-theme < 22.4
Obsoletes: f23-kde-theme < 23.1
Obsoletes: f24-kde-theme < 24.6
Obsoletes: f24-kde-theme-core < 5.10.5-2
Conflicts: steam-kde-presets

%description
KDE Presets from Nobara Official

%package extras-wallpapers
Provides: kde-nobara-extras-wallpapers
Obsoletes: plasma-lookandfeel-nobara-extras-wallpapers

Summary: Nobara extra wallpapers

License: GPLv2+ or LGPLv3+

%description extras-wallpapers

Nobara extra wallpapers

%package sddm
Provides: kde-nobara-sddm
Obsoletes: plasma-lookandfeel-nobara-sddm

Summary: Nobara sddm theme

License: GPLv2+ or LGPLv3+

%description sddm

Nobara sddm theme

# Disable debug packages
%define debug_package %{nil}

%prep
%setup -T -b 0 -q -n kde-nobara

%build

%install
mkdir -p %{buildroot}%{_bindir}/
mkdir -p %{buildroot}%{_datadir}/
mkdir -p %{buildroot}%{_sysconfdir}/
cp -rv usr/bin/* %{buildroot}%{_bindir}
cp -rv usr/share/* %{buildroot}%{_datadir}
cp -rv etc/* %{buildroot}%{_sysconfdir}

# Do post-installation
%post

# Do before uninstallation
%preun

# Do after uninstallation
%postun

# This lists all the files that are included in the rpm package and that
# are going to be installed into target system where the rpm is installed.
%files
%license LICENSE
%{_bindir}/nobara-gtk
%{_datadir}/color-schemes/Nobara.colors
%{_datadir}/konsole/Nobara.colorscheme
%{_datadir}/konsole/Nobara.profile
%{_datadir}/plasma/desktoptheme/Nobara/*
%{_datadir}/plasma/look-and-feel/org.nobaraproject.desktop/*
%{_datadir}/plasma/layout-templates/*
%{_datadir}/plasma/plasmoids/*
%{_datadir}/wallpapers/nobara-39*
%{_datadir}/wallpapers/nobara-40*
%{_datadir}/themes/Nobara/assets/*
%{_datadir}/themes/Nobara/gtk-2.0/*
%{_datadir}/themes/Nobara/gtk-3.0/*
%{_datadir}/themes/Nobara/gtk-4.0/*
%{_datadir}/themes/Nobara/settings.ini
%{_datadir}/themes/Nobara/window_decorations.css
%{_datadir}/icons/*
%{_datadir}/aurorae/*
%{_sysconfdir}/*

%files extras-wallpapers
%{_datadir}/wallpapers/nobara-mecha-penguins*
%{_datadir}/wallpapers/nobara-weebara*

%files sddm
%{_datadir}/sddm/*

# Finally, changes from the latest release of your application are generated from
# your project's Git history. It will be empty until you make first annotated Git tag.
%changelog
