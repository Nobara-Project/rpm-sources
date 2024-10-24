Summary: A set of scripts to run upon first user login
Name: nobara-controller-config
Version: 1.0
Release: 19%{?dist}
License: Public Domain
Source0: 50-razer-wolverine-v2-pro.rules
Source1: 60-xbox-pads.rules
Source2: 71-sony-controllers.rules
Source3: 50-horipad-steam-controller.rules

BuildArch: noarch
BuildRequires: filesystem
Requires: lpf
Requires: dkms

%description
This package contains the Nobara Xbox Controller configurator.

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/
install -m 0644 %{SOURCE0} $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/50-razer-wolverine-v2-pro.rules
install -m 0644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/60-xbox-pads.rules
install -m 0644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/71-sony-controllers.rules
install -m 0644 %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/50-horipad-steam-controller.rules
install -d $RPM_BUILD_ROOT%{_sysconfdir}/modprobe.d/

%files
%{_sysconfdir}/udev/rules.d/50-razer-wolverine-v2-pro.rules
%{_sysconfdir}/udev/rules.d/60-xbox-pads.rules
%{_sysconfdir}/udev/rules.d/71-sony-controllers.rules
%{_sysconfdir}/udev/rules.d/50-horipad-steam-controller.rules

%changelog
* Thu Nov 25 2021 Thomas Crider <gloriouseggroll@gmail.com> - 1.0.0
- New version v1.0.0
