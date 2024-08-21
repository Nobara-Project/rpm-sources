Summary: A set of scripts to run upon first user login
Name: nobara-login
Version: 1.1
Release: 59%{?dist}
License: Public Domain
Group: System Environment/Base
Source0: hwcheck.sh
Source1: nobara-firstrun.sh
Source3: nobara-firstrun.desktop
Source5: 20-starcitizen-max_map_count.conf
Source7: 20-disable-split-lock-detect.conf
Source8: v4l2loopback.conf
Source9: nobara.conf
Source10: 40-hpet-permissions.rules
Source11: 60-ioschedulers.rules
Source12: 20-uplay-mtu-probing.conf
Source13: updatecheck.sh
Source14: 90-corectrl.rules
Source15: 00-handheld-power.conf
Source16: wine_gaming.conf
Source17: nobara-automount.desktop
Source18: nobara-automount
Source19: org.nobaraproject.automount.policy
Source20: nobara-device-quirks
Source21: 99-ntsync.rules
Source22: 70-wooting.rules
Source23: 71-sony-controllers.rules
Source24: 70-drunkdeer.rules

BuildArch: noarch
BuildRequires: filesystem
Requires: system-release
Requires: nobara-login-sysctl
Requires: nobara-welcome
Requires: nobara-nvidia-wizard
Provides: nobara-amdgpu-config > 2.1
Obsoletes: nobara-amdgpu-config <= 2.1

%description
This package contains the Nobara NVIDIA installer, AMD ROCM installer, and Video Codec installer.


%package sysctl

Summary: nobara sysctl game modifications

License: GPLv2+ or LGPLv3+

Requires: nobara-login


%description sysctl

nobara sysctl game modifications


%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}/
install -d $RPM_BUILD_ROOT%{_libexecdir}
install -d $RPM_BUILD_ROOT%{_sysconfdir}/xdg/autostart/
install -d $RPM_BUILD_ROOT%{_sysconfdir}/modprobe.d/
install -d $RPM_BUILD_ROOT%{_sysconfdir}/dnf/protected.d/
install -d $RPM_BUILD_ROOT%{_prefix}/lib/sysctl.d/
install -d $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/
install -d $RPM_BUILD_ROOT%{_sysconfdir}/nobara/automount/
install -d $RPM_BUILD_ROOT%{_sysconfdir}/polkit-1/rules.d/
install -d $RPM_BUILD_ROOT%{_datadir}/polkit-1/actions/
install -d $RPM_BUILD_ROOT%{_sysconfdir}/login.conf.d/
install -d $RPM_BUILD_ROOT%{_datadir}/pipewire/pipewire-pulse.conf.d/
install -m 0755 %{SOURCE0} $RPM_BUILD_ROOT%{_bindir}/hwcheck
install -m 0755 %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}/nobara-firstrun
install -m 0755 %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/xdg/autostart/nobara-firstrun.desktop
install -m 0644 %{SOURCE5} $RPM_BUILD_ROOT%{_prefix}/lib/sysctl.d/20-starcitizen-max_map_count.conf
install -m 0644 %{SOURCE7} $RPM_BUILD_ROOT%{_prefix}/lib/sysctl.d/20-disable-split-lock-detect.conf
install -m 0644 %{SOURCE8} $RPM_BUILD_ROOT%{_sysconfdir}/modprobe.d/v4l2loopback.conf
install -m 0644 %{SOURCE9} $RPM_BUILD_ROOT%{_sysconfdir}/dnf/protected.d/nobara.conf
install -m 0644 %{SOURCE10} $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/40-hpet-permissions.rules
install -m 0644 %{SOURCE11} $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/60-ioschedulers.rules
install -m 0644 %{SOURCE12} $RPM_BUILD_ROOT%{_prefix}/lib/sysctl.d/20-uplay-mtu-probing.conf
install -m 0755 %{SOURCE13} $RPM_BUILD_ROOT%{_bindir}/updatecheck
install -m 0755 %{SOURCE14} $RPM_BUILD_ROOT%{_sysconfdir}/polkit-1/rules.d/90-corectrl.rules
install -m 0755 %{SOURCE15} $RPM_BUILD_ROOT%{_sysconfdir}/login.conf.d/00-handheld-power.conf
install -m 0755 %{SOURCE16} $RPM_BUILD_ROOT%{_datadir}/pipewire/pipewire-pulse.conf.d/wine_gaming.conf
install -m 0755 %{SOURCE17} $RPM_BUILD_ROOT%{_sysconfdir}/xdg/autostart/nobara-automount.desktop
install -m 0755 %{SOURCE18} $RPM_BUILD_ROOT%{_libexecdir}/nobara-automount
install -m 0755 %{SOURCE19} $RPM_BUILD_ROOT%{_datadir}/polkit-1/actions/org.nobaraproject.automount.policy
install -m 0755 %{SOURCE20} $RPM_BUILD_ROOT%{_bindir}/nobara-device-quirks
install -m 0644 %{SOURCE21} $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/99-ntsync.rules
install -m 0644 %{SOURCE22} $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/70-wooting.rules
install -m 0644 %{SOURCE23} $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/71-sony-controllers.rules
install -m 0644 %{SOURCE24} $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/70-drunkdeer.rules

echo '# list of disabled automount partitions' > disabled.conf
install -m 0755 disabled.conf $RPM_BUILD_ROOT%{_sysconfdir}/nobara/automount/disabled.conf
%post sysctl
sysctl -p

%files
%{_bindir}/nobara-firstrun
%{_bindir}/hwcheck
%{_bindir}/updatecheck
%{_bindir}/nobara-device-quirks
%{_libexecdir}/nobara-automount
%{_sysconfdir}/xdg/autostart/nobara-automount.desktop
%{_sysconfdir}/xdg/autostart/nobara-firstrun.desktop
%{_sysconfdir}/modprobe.d/v4l2loopback.conf
%{_sysconfdir}/dnf/protected.d/nobara.conf
%{_sysconfdir}/udev/rules.d/40-hpet-permissions.rules
%{_sysconfdir}/udev/rules.d/60-ioschedulers.rules
%{_sysconfdir}/udev/rules.d/99-ntsync.rules
%{_sysconfdir}/udev/rules.d/70-wooting.rules
%{_sysconfdir}/udev/rules.d/70-drunkdeer.rules
%{_sysconfdir}/udev/rules.d/71-sony-controllers.rules
%{_sysconfdir}/polkit-1/rules.d/90-corectrl.rules
%{_sysconfdir}/login.conf.d/00-handheld-power.conf
%config(noreplace) %{_sysconfdir}/nobara/automount/disabled.conf
%{_datadir}/polkit-1/actions/org.nobaraproject.automount.policy
%{_datadir}/pipewire/pipewire-pulse.conf.d/wine_gaming.conf

%files sysctl
%{_prefix}/lib/sysctl.d/20-starcitizen-max_map_count.conf
%{_prefix}/lib/sysctl.d/20-disable-split-lock-detect.conf
%{_prefix}/lib/sysctl.d/20-uplay-mtu-probing.conf

%changelog
* Thu Nov 25 2021 Thomas Crider <gloriouseggroll@gmail.com> - 1.0.0
- New version v1.0.0
