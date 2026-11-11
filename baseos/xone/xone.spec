%global _default_patch_fuzz 2
%global debug_package %{nil}
%global dkms_source_dir %{_usrsrc}/%{name}-%{version}
# Nobara's fork: xone_mtnet runs the new dongle on MediaTek's firmware, with wake on wireless
%global commit ad0d17e74ccd5447e33e37c5952e73ed3ca6bb2d

Name:     xone
# A new version (not just a release) for every source change: DKMS keys builds on
# the version, so the same version over different source is never rebuilt
Version:  0.5.8.2
Release:  1%{?dist}
Summary:  Linux kernel driver for Xbox One and Xbox Series X|S accessories
License:  GPLv2
URL:      https://github.com/GloriousEggroll/xone
Source0:  %{url}/archive/%{commit}/%{name}-%{commit}.tar.gz

# NOTE: xone_gip_headset is intentionally left out of early module loading because it tries to load snd before snd is available
# It should still load automatically when you plug in the device.
Source1:  modules-load-d-%{name}.conf
Patch1:   0002-fix-wired-usb-reset-race-condition.patch

BuildRequires:  systemd-rpm-macros
BuildRequires:  sed

BuildArch:      noarch

Requires:       dkms
Requires:       bash
# Microsoft's firmware is still needed for the old (045e:02e6) and built-in dongles
Requires:       lpf-xone-firmware
Requires:       gcc, make, kernel-devel
Requires:       xpad-noone
# xone-mtnet-setup puts the new dongle's interface into monitor mode with iw
Requires:       iw

Conflicts:      xow <= 0.5
Obsoletes:      xow <= 0.5
Provides:       %{name}-kmod-common = %{version}-%{release}
Obsoletes:      akmod-xone < %{version}-%{release}

%description
xone is a Linux kernel driver for Xbox One and Xbox Series X|S dongle.

%prep
%autosetup -p1 -n %{name}-%{commit}
# Fill the version into dkms.conf and the modules (as upstream's install.sh does):
# with MODULE_VERSION left at "#VERSION#", DKMS sees every build as the same
# version and won't replace installed modules on upgrade
find . -type f \( -name dkms.conf -o -name '*.c' \) -exec sed -i 's/#VERSION#/%{version}/' {} +

%build

%install
mkdir -p %{buildroot}%{dkms_source_dir}
cp -fr . %{buildroot}%{dkms_source_dir}
install -D -m 0644 install/modprobe.conf %{buildroot}%{_modprobedir}/60-%{name}.conf
install -D -m 0644 %{SOURCE1} %{buildroot}%{_modulesloaddir}/%{name}.conf
# The new dongle (045e:02fe) runs on mt76x2u + xone_mtnet: this udev rule puts
# its interface into monitor mode so xone_mtnet attaches.
install -D -m 0644 install/mtnet/70-xone-mtnet.rules %{buildroot}%{_udevrulesdir}/70-xone-mtnet.rules
install -D -m 0755 install/mtnet/xone-mtnet-setup %{buildroot}%{_libexecdir}/xone-mtnet-setup

%post
%udev_rules_update
# Builds before 0.5.8.1 left MODULE_VERSION as "#VERSION#", which DKMS ranks above
# any real version, so it would never replace them. Remove those xone modules from
# every kernel first; DKMS then installs this version for each kernel as usual.
for k in /lib/modules/*; do
    stale=
    for m in "$k"/extra/xone_*.ko*; do
        [ -e "$m" ] || continue
        if [ "$(modinfo -F version "$m" 2>/dev/null)" = "#VERSION#" ]; then
            rm -f "$m"; stale=1
        fi
    done
    [ -n "$stale" ] && depmod -a "${k##*/}" 2>/dev/null || :
done
dkms add -m %{name} -v %{version} --rpm_safe_upgrade || :
dkms build -m %{name} -v %{version} || :
dkms install -m %{name} -v %{version} --force || :

%preun
dkms remove -m %{name} -v %{version} --all --rpm_safe_upgrade || :

%files
%license LICENSE
%doc README.md
%{_usrsrc}/%{name}-%{version}
%{_modprobedir}/60-%{name}.conf
%{_modulesloaddir}/%{name}.conf
%{_udevrulesdir}/70-xone-mtnet.rules
%{_libexecdir}/xone-mtnet-setup

%changelog
* Wed Nov 11 2026 GloriousEggroll <gloriouseggroll@gmail.com> - 0.5.8.2-1
- xone_mtnet: stop enabling wakeup on the USB root hub. It armed wake on
  connect/disconnect for every port on the bus, so another device there
  (a Framework laptop webcam that drops off as the system suspends) woke
  the system at once, controller on or off. The dongle and any external
  hubs above it still get wakeup, which is all the controller wake needs

* Tue Nov 10 2026 GloriousEggroll <gloriouseggroll@gmail.com> - 0.5.8.1-1
- Bump the version so DKMS rebuilds: 0.5.8-4 kept DKMS version 0.5.8, so
  upgrades reported the old build as installed and never built the new
  source (dkms status: "Built modules are missing" for xone_mtnet)
- Fill in MODULE_VERSION (was left as "#VERSION#"). DKMS ranks "#VERSION#"
  above real versions, so %post removes the old xone modules carrying it and
  installs with --force; otherwise upgrades kept the old modules

* Tue Nov 10 2026 GloriousEggroll <gloriouseggroll@gmail.com> - 0.5.8-4
- Build from the GloriousEggroll/xone fork
- Run the new dongle (045e:02fe) on mt76x2u and xone_mtnet with MediaTek's
  firmware instead of xone_dongle and Microsoft's firmware; the old and
  built-in dongles stay on xone_dongle
- Add wake on wireless to xone_mtnet: a controller turning on wakes the host
  from s2idle or S3; the system's sleep mode is left as it is

* Tue Feb 10 2026 LionHeartP <LionHeartP@proton.me> - 0.5.8-3
- Add xpad-noone as a dependency

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

