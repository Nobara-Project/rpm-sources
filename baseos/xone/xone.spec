%global _default_patch_fuzz 2
%global debug_package %{nil}
%global dkms_source_dir %{_usrsrc}/%{name}-%{version}

Name:     xone
Version:  0.5.8
Release:  2%{?dist}
Summary:  Linux kernel driver for Xbox One and Xbox Series X|S accessories
License:  GPLv2
URL:      https://github.com/dlundqvist/xone
Source0:  %{url}/archive/refs/tags/v%{version}.tar.gz

# NOTE: xone_gip_headset is intentionally left out of early module loading because it tries to load snd before snd is available
# It should still load automatically when you plug in the device.
Source1:  modules-load-d-%{name}.conf
Patch1:   0002-fix-wired-usb-reset-race-condition.patch

BuildRequires:  systemd-rpm-macros
BuildRequires:  sed

BuildArch:      noarch

Requires:       dkms
Requires:       bash
Requires:       lpf-xone-firmware
Requires:       gcc, make, kernel-devel

Conflicts:      xow <= 0.5
Obsoletes:      xow <= 0.5
Provides:       %{name}-kmod-common = %{version}-%{release}
Obsoletes:      akmod-xone < %{version}-%{release}

%description
xone is a Linux kernel driver for Xbox One and Xbox Series X|S dongle.

%prep
%autosetup -p1
sed -i 's/#VERSION#/%{version}/' dkms.conf

%build

%install
mkdir -p %{buildroot}%{dkms_source_dir}
cp -fr . %{buildroot}%{dkms_source_dir}
install -D -m 0644 install/modprobe.conf %{buildroot}%{_modprobedir}/60-%{name}.conf
install -D -m 0644 %{SOURCE1} %{buildroot}%{_modulesloaddir}/%{name}.conf

%post
dkms add -m %{name} -v %{version} --rpm_safe_upgrade || :
dkms build -m %{name} -v %{version} || :
dkms install -m %{name} -v %{version} || :

%preun
dkms remove -m %{name} -v %{version} --all --rpm_safe_upgrade || :

%files
%license LICENSE
%doc README.md
%{_usrsrc}/%{name}-%{version}
%{_modprobedir}/60-%{name}.conf
%{_modulesloaddir}/%{name}.conf

%changelog
* Tue Feb 10 2026 LionHeartP <LionHeartP@proton.me> - 0.5.5-1
- Update to 0.5.5
- Convert to dkms

* Wed Dec 17 2025 LionHeartP <LionHeartP@proton.me> - 0.5.0-1
- Update to 0.5.0

* Sat Nov 15 2025 LionHeartP <LionHeartP@proton.me> - 0.4.11-1
- Update to 0.4.11

* Thu Oct 16 2025 LionHeartP <LionHeartP@proton.me> - 0.4.8-1
- Update to 0.4.8

* Sat Aug 23 2025 LionHeartP <LionHeartP@proton.me> - 0.4.3-1
- Update to 0.4.3
- Rebase 0001-convert-to-dongle-only-build.patch
- Remove elite-paddles.patch (upstreamed)

* Sun Jan 28 2024 Jan Drögehoff <sentrycraft123@gmail.com> - 0.3-4
- Force bump release

* Tue Jun 06 2023 Jan Drögehoff <sentrycraft123@gmail.com> - 0.3-3
- Fix Linux 6.3 compilation, add some patches

* Sun Nov 13 2022 Jan Drögehoff <sentrycraft123@gmail.com> - 0.3-2
- correct modules

* Thu Jun 23 2022 Jan Drögehoff <sentrycraft123@gmail.com> - 0.3-1
- Update to 0.3

* Sat Mar 19 2022 Jan Drögehoff <sentrycraft123@gmail.com> - 0.2-2
- Obsolete xow and require firmware

* Sun Feb 27 2022 Jan Drögehoff <sentrycraft123@gmail.com> - 0.2-1
- Update to 0.2

* Fri Jul 02 2021 Jan Drögehoff <sentrycraft123@gmail.com> - 0.1-1
- Initial spec

