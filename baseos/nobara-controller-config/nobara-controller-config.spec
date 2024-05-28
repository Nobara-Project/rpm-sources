Summary: A set of scripts to run upon first user login
Name: nobara-controller-config
Version: 1.0
Release: 13%{?dist}
License: Public Domain
Source0: controllercheck.sh
Source1: 50-generic-xbox360-controller.rules
Source2: 50-lenovo-legion-controller.rules
BuildArch: noarch
BuildRequires: filesystem
Requires: lpf
Requires: dkms

%description
This package contains the Nobara Xbox Controller configurator.

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}/
install -d $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/
install -m 0755 %{SOURCE0} $RPM_BUILD_ROOT%{_bindir}/nobara-controller-config
install -m 0644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/50-generic-xbox360-controller.rules
install -m 0644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/udev/rules.d/50-lenovo-legion-controller.rules

%files
%{_bindir}/nobara-controller-config
%{_sysconfdir}/udev/rules.d/50-generic-xbox360-controller.rules
%{_sysconfdir}/udev/rules.d/50-lenovo-legion-controller.rules

%changelog
* Thu Nov 25 2021 Thomas Crider <gloriouseggroll@gmail.com> - 1.0.0
- New version v1.0.0
