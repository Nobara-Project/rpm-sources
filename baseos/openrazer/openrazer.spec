# This spec file should work on Fedora, openSUSE and Mageia

%define dkms_name openrazer-driver
%define dkms_version 3.12.4

%global _default_patch_fuzz 2

#%%define gitcommit ddea89607b86023e88563b8feabc8fa2d5773cdd

Name: 		openrazer-meta
Version: 	3.12.4
Release: 	15%{?dist}
Summary: 	Open source driver and user-space daemon for managing Razer devices

License: 	GPL-2.0
URL: 		https://github.com/openrazer/openrazer

%if 0%{?gitcommit:1}
Source0: 	https://github.com/crstmkt/openrazer/archive/%{gitcommit}.tar.gz
%else
Source0: 	https://github.com/openrazer/openrazer/releases/download/v%{version}/openrazer-%{version}.tar.xz
%endif
Patch0: 	openrazer-device-support.patch
# HyperFlux reset-resume helper is unavailable on Linux 6.18 LTS.
Patch1:         openrazer-lts-reset-resume.patch

# https://fedoraproject.org/wiki/Changes/EncourageI686LeafRemoval
ExcludeArch:    %{ix86}

BuildArch: 	noarch
BuildRequires: 	make
BuildRequires:  gcc

Requires: 	openrazer-kernel-modules-dkms
Requires: 	openrazer-daemon
Requires: 	python3-openrazer
Requires:   polychromatic

%description
Meta package for installing all required openrazer packages.


%package -n openrazer-kernel-modules-dkms
Summary: 	OpenRazer Driver DKMS package
Group: 		System Environment/Kernel
Obsoletes: 	razer-kernel-modules-dkms
Provides: 	razer-kernel-modules-dkms
Requires: 	dkms
Requires: 	make
Requires: 	udev
# OBS fails without that
%if 0%{?suse_version}
Requires(pre): 	shadow
Requires(post): dkms
%else
Requires(pre): 	shadow-utils
%endif

%description -n openrazer-kernel-modules-dkms
Kernel driver for Razer devices (DKMS-variant)


%package -n openrazer-daemon
Summary: 	OpenRazer Service package
Group: 		System Environment/Daemons
Obsoletes: 	razer-daemon
Provides: 	razer-daemon
BuildRequires: 	python3-devel
BuildRequires: 	python3-setuptools
Requires: 	openrazer-kernel-modules-dkms
Requires: 	python3
%if 0%{?suse_version}
Requires: 	dbus-1-python3
Requires: 	typelib(Gdk) = 3.0
%else
Requires: 	python3-dbus
%endif
%if 0%{?mageia}
Requires: 	python3-gobject3
%else
Requires: 	python3-gobject
%endif
Requires: 	python3-setproctitle
Requires: 	python3-pyudev
Requires: 	python3-daemonize
Requires: 	xautomation

%description -n openrazer-daemon
Userspace daemon that abstracts access to the kernel driver. Provides a DBus service for applications to use.


%package -n python3-openrazer
Summary: 	OpenRazer Python library
Group: 		System Environment/Libraries
Obsoletes: 	python3-razer
Provides: 	python3-razer
BuildRequires: 	python3-devel
BuildRequires: 	python3-setuptools
Requires: 	openrazer-daemon
Requires: 	python3
%if 0%{?suse_version}
Requires: 	dbus-1-python3
%else
Requires: 	python3-dbus
%endif
%if 0%{?mageia}
Requires: 	python3-gobject3
%else
Requires: 	python3-gobject
%endif
Requires: 	python3-numpy

%description -n python3-openrazer
Python library for accessing the daemon from Python.


%prep
%if 0%{?gitcommit:1}
%autosetup -n openrazer-%{gitcommit} -p1
%else
%autosetup -n openrazer-%{version} -p1
%endif

%build
# noop

%check
gcc -Wall -Wextra -Werror -o test-hyperflux scripts/ci/test-hyperflux.c
./test-hyperflux
gcc -Wall -Wextra -Werror -o test-hyperflux-pairing scripts/ci/test-hyperflux-pairing.c
./test-hyperflux-pairing
gcc -Wall -Wextra -Werror -o test-hyperflux-keyboard scripts/ci/test-hyperflux-keyboard.c
./test-hyperflux-keyboard
gcc -Wall -Wextra -Werror -o test-hyperflux-auto scripts/ci/test-hyperflux-auto.c
./test-hyperflux-auto


%install
rm -rf $RPM_BUILD_ROOT
# setup_dkms & udev_install -> razer-kernel-modules-dkms
# daemon_install -> razer_daemon
# python_library_install -> python3-razer
make DESTDIR=$RPM_BUILD_ROOT setup_dkms udev_install daemon_install python_library_install


%clean
rm -rf $RPM_BUILD_ROOT


%pre -n openrazer-kernel-modules-dkms
#!/bin/sh
set -e

getent group plugdev >/dev/null || groupadd -r plugdev


%if 0%{?mageia}

%posttrans -n openrazer-kernel-modules-dkms
dkms add -m %{dkms_name} -v %{dkms_version} --rpm_safe_upgrade
dkms build -m %{dkms_name} -v %{dkms_version} --rpm_safe_upgrade
dkms install -m %{dkms_name} -v %{dkms_version} --rpm_safe_upgrade

echo -e "\e[31m********************************************"
echo -e "\e[31m* To complete installation, please run:    *"
echo -e "\e[31m* # sudo gpasswd -a <yourUsername> plugdev *"
echo -e "\e[31m********************************************"
echo -e -n "\e[39m"

%preun -n openrazer-kernel-modules-dkms
dkms remove -m %{dkms_name} -v %{dkms_version} --rpm_safe_upgrade --all

%else

%posttrans -n openrazer-kernel-modules-dkms
#!/bin/sh
set -e

dkms install %{dkms_name}/%{dkms_version}

echo -e "\e[31m********************************************"
echo -e "\e[31m* To complete installation, please run:    *"
echo -e "\e[31m* # sudo gpasswd -a <yourUsername> plugdev *"
echo -e "\e[31m********************************************"
echo -e -n "\e[39m"

%preun -n openrazer-kernel-modules-dkms
#!/bin/sh

if [ "$(dkms status -m %{dkms_name} -v %{dkms_version})" ]; then
  dkms remove -m %{dkms_name} -v %{dkms_version} --all
fi

%endif


%files
# meta package is empty


%files -n openrazer-kernel-modules-dkms
%defattr(-,root,root,-)
# A bit hacky but it works
/usr/lib/udev/rules.d/../razer_mount
/usr/lib/udev/rules.d/99-razer.rules
%{_usrsrc}/%{dkms_name}-%{dkms_version}/

%files -n openrazer-daemon
%{_bindir}/openrazer-daemon
%{python3_sitelib}/openrazer_daemon/
%{python3_sitelib}/openrazer_daemon-*.egg-info/
%{_datadir}/openrazer/
%{_datadir}/dbus-1/services/org.razer.service
%{_prefix}/lib/systemd/user/openrazer-daemon.service
%{_mandir}/man5/razer.conf.5*
%{_mandir}/man8/openrazer-daemon.8*

%files -n python3-openrazer
%{python3_sitelib}/openrazer/
%{python3_sitelib}/openrazer-*.egg-info/

%changelog
* Fri Oct 02 2026 Nobara Project <support@nobaraproject.org> - 3.12.4-14
- Build HyperFlux support on Linux 6.18 LTS without the newer HID resume helper.
- Preserve HID input reset-resume handling on Linux 6.19 and newer.

* Sun Sep 27 2026 Nobara local build - 3.12.4-13
- Create and remove HyperFlux mouse controls dynamically on pairing changes.
- Support pairing after empty-slot boot and switching Naga models without replug.
- Keep PID-specific control paths, stable daemon identities and unchanged HID input.
- Retry registration after transient udev permission races without settings writes.

* Sun Sep 27 2026 Nobara local build - 3.12.4-12
- Publish confirmed mouse membership and remove unpaired logical devices.
- Preserve sleeping children and existing entries on failed inventory reads.
- Expose discovery versus pairing counters and require completed discovery.

* Sun Sep 27 2026 Nobara local build - 3.12.4-11
- Defer client firmware reads so a sleeping child cannot abort DeviceManager.
- Cache successful firmware queries only, preserving explicit errors and retries.
- Isolate suspend/resume I/O failures and restore flags so shutdown completes.
- Exercise the full client enumeration path with an isolated real D-Bus service.

* Sun Sep 27 2026 Nobara local build - 3.12.4-10
- Register HyperFlux mouse children without startup feature reads or settings writes.
- Use stable per-receiver/model mouse identity and preserve input mode.
- Keep battery notification threads alive on busy/asleep wireless read failures.

* Sat Sep 26 2026 Nobara local build - 3.12.4-9
- Add opt-in kernel-managed auto-pairing for independent mouse/keyboard slots.
- Refresh keyboard sysfs/daemon children on wireless membership changes.
- Preserve input, slot/token checks, bounded operations and disconnect teardown.
