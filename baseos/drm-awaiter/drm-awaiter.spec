Name:           drm-awaiter
Version:        1
Release:        1%{?dist}
Summary:        Load GPU drivers from the root filesystem before graphical login
License:        GPL-3.0-or-later
URL:            https://github.com/CachyOS/CachyOS-PKGBUILDS/pull/1695
BuildArch:      noarch
Source0:        drm-module-awaiter-generator
Source1:        90-drm-awaiter.conf
Source2:        README.md
Source3:        COPYING
Source4:        test-generator.py
BuildRequires:  systemd-rpm-macros
BuildRequires:  python3
BuildRequires:  bash
Requires:       bash
Requires:       coreutils
Requires:       kmod
Requires:       systemd
Requires:       dracut
Requires(posttrans): dracut

%description
Adaptation of CachyOS's DRM awaiter for Nobara. A systemd generator orders
graphical login after GPU module insertion on the real root. Vendor GPU
modules and their firmware no longer need to be included in each initramfs.

%prep
%setup -q -T -c
cp %{SOURCE0} %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE4} .

%build

%install
install -Dpm0755 drm-module-awaiter-generator %{buildroot}%{_systemdgeneratordir}/drm-module-awaiter-generator
install -Dpm0644 90-drm-awaiter.conf %{buildroot}%{_prefix}/lib/dracut/dracut.conf.d/90-drm-awaiter.conf

%check
bash -n drm-module-awaiter-generator
python3 test-generator.py

%posttrans
# Migrate existing images after all package payloads and DKMS scriptlets have
# completed. Future images inherit the policy through ordinary kernel-install.
if ! /usr/bin/dracut --regenerate-all --force; then
    echo 'drm-awaiter: initramfs rebuild failed; fix the reported error and rerun dracut --regenerate-all --force.' >&2
fi

%files
%license COPYING
%doc README.md
%{_systemdgeneratordir}/drm-module-awaiter-generator
%{_prefix}/lib/dracut/dracut.conf.d/90-drm-awaiter.conf

%changelog
* Wed Sep 09 2026 Nobara Project <contact@nobaraproject.org> - 1-1
- Adapt CachyOS DRM awaiter for root-filesystem GPU loading with dracut.
