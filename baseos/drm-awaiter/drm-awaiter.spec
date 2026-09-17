Name:           drm-awaiter
Version:        1
Release:        2%{?dist}
Summary:        Load GPU drivers from the root filesystem before graphical login
License:        GPL-3.0-or-later
URL:            https://github.com/CachyOS/CachyOS-PKGBUILDS/pull/1695
BuildArch:      noarch
Source0:        drm-module-awaiter-generator
Source1:        90-drm-awaiter.conf
Source2:        README.md
Source3:        COPYING
Source4:        test-generator.py
Source5:        drm-awaiter-initramfs
BuildRequires:  systemd-rpm-macros
BuildRequires:  python3
BuildRequires:  bash
Requires:       bash
Requires:       coreutils
Requires:       kmod
Requires:       systemd
Requires:       dracut
Requires:       util-linux-core
Requires(post): bash coreutils util-linux-core

%description
Adaptation of CachyOS's DRM awaiter for Nobara. A systemd generator orders
graphical login after GPU module insertion on the real root. Vendor GPU
modules and their firmware no longer need to be included in each initramfs.

%prep
%setup -q -T -c
cp %{SOURCE0} %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE4} %{SOURCE5} .

%build

%install
install -Dpm0755 drm-module-awaiter-generator %{buildroot}%{_systemdgeneratordir}/drm-module-awaiter-generator
install -Dpm0644 90-drm-awaiter.conf %{buildroot}%{_prefix}/lib/dracut/dracut.conf.d/90-drm-awaiter.conf
install -Dpm0755 drm-awaiter-initramfs %{buildroot}%{_libexecdir}/drm-awaiter-initramfs

%check
bash -n drm-module-awaiter-generator
python3 test-generator.py

%post
%{_libexecdir}/drm-awaiter-initramfs request

# Both trigger types may run during an upgrade. The shared pending request is
# consumed only once, after all DKMS scriptlets and kernel posttrans work.
%transfiletriggerin -P 100 -- %{_usrsrc}/nvidia- %{_prefix}/lib/dracut/dracut.conf.d/90-drm-awaiter.conf
%{_libexecdir}/drm-awaiter-initramfs flush

%transfiletriggerpostun -P 100 -- %{_usrsrc}/nvidia-
%{_libexecdir}/drm-awaiter-initramfs flush

%files
%license COPYING
%doc README.md
%{_systemdgeneratordir}/drm-module-awaiter-generator
%{_prefix}/lib/dracut/dracut.conf.d/90-drm-awaiter.conf
%{_libexecdir}/drm-awaiter-initramfs

%changelog
* Wed Sep 09 2026 Nobara Project <contact@nobaraproject.org> - 1-1
- Adapt CachyOS DRM awaiter for root-filesystem GPU loading with dracut.
