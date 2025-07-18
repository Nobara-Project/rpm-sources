%global commit e2971e45063f6b327ccedbf18e168bda6749155c
%if 0%{?rhel} && 0%{?rhel} < 10
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%else
%global shortcommit %{sub %{commit} 1 7}
%endif
%global commitdate 20240522


Name:           steam-devices
Version:        1.0.0.101^git%{commitdate}.%{shortcommit}
Release:        3%{?dist}
License:        MIT
Summary:        Device support for Steam-related hardware
Url:            https://github.com/ValveSoftware/steam-devices/
Source0:        %{url}/archive/%{commit}/%{name}-%{version}.tar.gz
# Input devices seen as joysticks:
Source1:        https://raw.githubusercontent.com/denilsonsa/udev-joystick-blacklist/master/after_kernel_4_9/51-these-are-not-joysticks-rm.rules

BuildArch:      noarch

BuildRequires:  git-core
BuildRequires:  systemd-rpm-macros

# Temporary workaround to obsolete and replace the equivalent i686 package in RPMFusion
# so we don't break current installs. Can be removed after a while.
Obsoletes:      steam-devices < %{version}-%{release}
Provides:       steam-devices = %{version}-%{release}

%description
This package contains the necessary permissions for gaming devices (such as
gamepads, joysticks and VR headsets) that can be used by Wine, Lutris, Heroic,
and other non-Steam games and game launchers.

%prep
%autosetup -n %{name}-%{commit} -S git_am

%install
install -Dpm0644 60-steam-input.rules %{buildroot}%{_udevrulesdir}/60-steam-input.rules
install -Dpm0644 60-steam-vr.rules %{buildroot}%{_udevrulesdir}/60-steam-vr.rules
install -Dpm0644 %{SOURCE1} %{buildroot}%{_udevrulesdir}/51-these-are-not-joysticks-rm.rules

%files
%license LICENSE
%{_udevrulesdir}/60-steam-input.rules
%{_udevrulesdir}/60-steam-vr.rules
%{_udevrulesdir}/51-these-are-not-joysticks-rm.rules

%changelog
* Tue Mar 18 2025 Shawn W. Dunn <sfalken@cloverleaf-linux.org> - 1.0.0.101^git20240522.e2971e4-2
- Added Conditional to fix FTBFS on epel8 and epel9

* Mon Mar 17 2025 Shawn W. Dunn <sfalken@cloverleaf-linux.org> - 1.0.0.101^git20240522.e2971e4-1
- Update to 1.0.0.101^git20240522.e2971e4-1

* Mon Mar 17 2025 Simone Caronni <negativo17@gmail.com> - 1.0.0.100^git20240522.e2971e4-4
- Small cosmetic changes.

* Mon Mar 17 2025 Simone Caronni <negativo17@gmail.com> - 1.0.0.100^git20240522.0.e2971e4-3
- Temporarily provide/obsolete RPMFusion's equivalent i686 package.

* Sat Mar 15 2025 Shawn W. Dunn <sfalken@cloverleaf-linux.org> - 1.0.0.100^git20240522.0.e2971e4-2
- Updated description to remove outdated information

* Fri Mar 7 2025 Shawn W. Dunn <sfalken@cloverleaf-linux.org> 1.0.0.100^git20240522.0.e2971e4-1
- new package

