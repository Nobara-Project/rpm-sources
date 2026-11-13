%global debug_package %{nil}
%global modulename linuwu-sense
%global kmodname linuwu_sense
%global commit 4483b6c38b9bb963ac9ada9ca476578e0c63cc08
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global commitdate 20261019

Name:           dkms-%{modulename}
Version:        1.0^%{commitdate}git.%{shortcommit}
Release:        1%{?dist}
Summary:        Acer Predator and Nitro laptop driver, replacing acer-wmi (DKMS)
License:        GPL-2.0-or-later
URL:            https://github.com/0x7375646F/Linuwu-Sense
Source0:        %{url}/archive/%{commit}.tar.gz#/%{modulename}-%{commit}.tar.gz
Source1:        linuwu-sense.conf
Source2:        linuwu-sense-save.service
Source3:        80-linuwu-sense.preset
# Same patch as nobara-signed-kmods: fix the error paths that save the state
# files, which crashed the kernel when a file couldn't be written
Patch0:         linuwu-sense-state-file-errors.patch
BuildRequires:  systemd-rpm-macros
Requires:       dkms
Requires:       gcc, make
Provides:       %{modulename}-kmod = %{version}
BuildArch:      noarch
%{?systemd_requires}

%description
Linuwu-Sense, a fork of the kernel's acer-wmi driver for Acer Predator and
Nitro laptops, built by DKMS for every installed kernel. Besides acer-wmi's
features it controls fan speeds, thermal profiles, the battery charge
limiter and calibration, USB charging, the LCD overdrive, the boot sound and
the RGB keyboard. acer_wmi is blacklisted: both drive the same WMI devices.

Settings are restored when the driver loads. The driver saves them to
/etc/predator_state and /etc/four_zone_kb_state when it is removed, which
linuwu-sense-save.service does at shutdown. The sysfs files stay root-only.

%prep
%autosetup -n Linuwu-Sense-%{commit} -p1

%build

%install
d=%{buildroot}%{_usrsrc}/%{modulename}-%{version}
mkdir -p $d
cp -a src/%{kmodname}.c $d/
echo 'obj-m := %{kmodname}.o' > $d/Kbuild
cat > $d/dkms.conf <<'DKMS'
PACKAGE_NAME="%{modulename}"
PACKAGE_VERSION="%{version}"
MAKE[0]="'make' -C ${kernel_source_dir} M=${dkms_tree}/${PACKAGE_NAME}/${PACKAGE_VERSION}/build modules"
BUILT_MODULE_NAME[0]="%{kmodname}"
DEST_MODULE_LOCATION[0]="/extra"
AUTOINSTALL="yes"
DKMS
# Do not enable weak modules support in Fedora (no kABI)
install -d %{buildroot}%{_sysconfdir}/dkms
echo 'NO_WEAK_MODULES="yes"' > %{buildroot}%{_sysconfdir}/dkms/%{modulename}.conf
install -Dpm644 %{SOURCE1} %{buildroot}%{_prefix}/lib/modprobe.d/%{modulename}.conf
install -Dpm644 %{SOURCE2} %{buildroot}%{_unitdir}/linuwu-sense-save.service
install -Dpm644 %{SOURCE3} %{buildroot}%{_presetdir}/80-linuwu-sense.preset

%post
dkms add -m %{modulename} -v %{version} -q --rpm_safe_upgrade || :
dkms build -m %{modulename} -v %{version} -q || :
dkms install -m %{modulename} -v %{version} -q --force || :
%systemd_post linuwu-sense-save.service

%preun
%systemd_preun linuwu-sense-save.service
dkms remove -m %{modulename} -v %{version} -q --all --rpm_safe_upgrade || :

%postun
%systemd_postun linuwu-sense-save.service

%files
%license LICENSE
%doc README.md
%{_usrsrc}/%{modulename}-%{version}
%config(noreplace) %{_sysconfdir}/dkms/%{modulename}.conf
%{_prefix}/lib/modprobe.d/%{modulename}.conf
%{_unitdir}/linuwu-sense-save.service
%{_presetdir}/80-linuwu-sense.preset

%changelog
* Thu Nov 12 2026 GloriousEggroll <gloriouseggroll@gmail.com> - 1.0^20261019git.4483b6c-1
- Initial package. nobara-signed-kmods builds the signed module for the Easy
  Anti-Cheat kernel from the same source and patch. Unlike upstream's
  install.sh, the sysfs files stay root-only (no linuwu_sense group or
  tmpfiles permissions)
