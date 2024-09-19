%define _binaries_in_noarch_packages_terminate_build 0

Summary: Decky Loader is a homebrew plugin launcher for the Steam Deck.
Name: deckyloader
Version: 3.0.1
Release: 6.pre3%{?dist}
License: Public Domain
Source0: https://github.com/SteamDeckHomebrew/decky-loader/releases/download/v%{version}-pre3/PluginLoader
Source1: deckyloader@.service
Source2: gamescope-deckyloader
Source3: org.steamdeckhomebrew.gamesscope.deckyloader.start.policy
Source4: deckyloader-wrapper.sh
Source5: nobara-preinstalled-plugins.tar.gz

BuildArch: noarch
BuildRequires: pnpm
BuildRequires: systemd-rpm-macros

%description
Decky Loader is a homebrew plugin launcher for the Steam Deck. It can be used to stylize your menus, change system sounds, adjust your screen saturation, change additional system settings, and more.

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/deckyloader
install -d $RPM_BUILD_ROOT%{_unitdir}
install -d $RPM_BUILD_ROOT%{_bindir}
install -d $RPM_BUILD_ROOT%{_datadir}/polkit-1/actions/
install -m 0755 %{SOURCE0} $RPM_BUILD_ROOT%{_datadir}/deckyloader/
install -m 0644 %{SOURCE1} $RPM_BUILD_ROOT%{_unitdir}/
install -m 0755 %{SOURCE2} $RPM_BUILD_ROOT%{_bindir}/
install -m 0644 %{SOURCE3} $RPM_BUILD_ROOT%{_datadir}/polkit-1/actions/
install -m 0755 %{SOURCE4} $RPM_BUILD_ROOT%{_bindir}/
install -m 0755 %{SOURCE5} $RPM_BUILD_ROOT%{_datadir}/deckyloader/

%files
%{_datadir}/deckyloader/PluginLoader
%{_datadir}/deckyloader/nobara-preinstalled-plugins.tar.gz
%{_unitdir}/deckyloader@.service
%{_bindir}/gamescope-deckyloader
%{_bindir}/deckyloader-wrapper.sh
%{_datadir}/polkit-1/actions/org.steamdeckhomebrew.gamesscope.deckyloader.start.policy

%changelog
* Wed Sep 18 2024 Thomas Crider <gloriouseggroll@gmail.com> - 3.0.0
- New version v3.0.0
