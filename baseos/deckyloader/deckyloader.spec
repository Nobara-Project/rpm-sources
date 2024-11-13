%define _binaries_in_noarch_packages_terminate_build 0

Summary: Decky Loader is a homebrew plugin launcher for the Steam Deck.
Name: deckyloader
Version: 3.0.4
Release: 1%{?dist}
License: Public Domain
Source0: https://github.com/SteamDeckHomebrew/decky-loader/releases/download/v3.0.4/PluginLoader
Source2: gamescope-deckyloader
Source3: org.steamdeckhomebrew.gamescope.deckyloader.start.policy
Source5: nobara-preinstalled-plugins.tar.gz

BuildArch: noarch
BuildRequires: systemd-rpm-macros

%description
Decky Loader is a homebrew plugin launcher for the Steam Deck. It can be used to stylize your menus, change system sounds, adjust your screen saturation, change additional system settings, and more.

%install
tar -xf %{SOURCE5}
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/deckyloader
install -d $RPM_BUILD_ROOT%{_bindir}
install -d $RPM_BUILD_ROOT%{_datadir}/polkit-1/actions/
install -m 0755 %{SOURCE0} $RPM_BUILD_ROOT%{_datadir}/deckyloader/
install -m 0755 %{SOURCE2} $RPM_BUILD_ROOT%{_bindir}/
install -m 0644 %{SOURCE3} $RPM_BUILD_ROOT%{_datadir}/polkit-1/actions/
mv plugins $RPM_BUILD_ROOT%{_datadir}/deckyloader/

%files
%{_datadir}/deckyloader/PluginLoader
%{_datadir}/deckyloader/*
%{_bindir}/gamescope-deckyloader
%{_datadir}/polkit-1/actions/org.steamdeckhomebrew.gamescope.deckyloader.start.policy

%changelog
* Wed Sep 18 2024 Thomas Crider <gloriouseggroll@gmail.com> - 3.0.0
- New version v3.0.0
