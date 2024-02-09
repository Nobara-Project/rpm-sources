#
# spec file for package asus-nb-ctrl
#
# Copyright (c) 2020-2021 Luke Jones <luke@ljones.dev>
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

%if %{defined fedora}
%global debug_package %{nil}
%endif

# Use hardening ldflags.
%global rustflags -Clink-arg=-Wl,-z,relro,-z,now
Name:           supergfxctl
Version:        5.1.1
Release:        5
Summary:        Super graphics mode controller
License:        MPLv2

Group:          System Environment/Kernel

URL:            https://gitlab.com/asus-linux/supergfxctl
Source:         %URL/-/archive/%version/%{name}-%{version}.tar.gz
Source1:        %URL/uploads/65d12bc0197c6af78df425f545ec6d7d/vendor-%{version}.tar.xz
Source2:	supergfxd-battery-check.sh
Patch0:		0001-Don-t-let-supergfxd-mess-with-nvidia-modprobe-settin.patch
BuildRequires:  cargo

BuildRequires:  systemd-rpm-macros
BuildRequires:  clang-devel
BuildRequires:  rust
BuildRequires:  rust-std-static
BuildRequires:  libudev-devel
BuildRequires:  pkgconfig(dbus-1)

%description
supergfxctl is a super graphics mode controller for laptops with hybrid nvidia.

%prep
%autosetup -p1
%setup -D -T -a 1


mkdir .cargo
cat >.cargo/config <<EOF
[source.crates-io]
replace-with = "vendored-sources"
[source.vendored-sources]
directory = "vendor"
EOF

%build
export RUSTFLAGS="%{rustflags}"
RUST_BACKTRACE=1 cargo build --release --features "daemon cli"

%install
export RUSTFLAGS="%{rustflags}"

mkdir -p "%{buildroot}%{_bindir}"
install -D -m 0755 target/release/supergfxd %{buildroot}%{_bindir}/supergfxd
install -D -m 0755 %{SOURCE2} %{buildroot}%{_bindir}/supergfxd-battery-check.sh
install -D -m 0755 target/release/supergfxctl %{buildroot}%{_bindir}/supergfxctl
install -D -m 0644 data/90-supergfxd-nvidia-pm.rules %{buildroot}%{_udevrulesdir}/90-supergfxd-nvidia-pm.rules
install -D -m 0644 data/org.supergfxctl.Daemon.conf  %{buildroot}%{_sysconfdir}/dbus-1/system.d/org.supergfxctl.Daemon.conf
install -D -m 0644 data/supergfxd.service %{buildroot}%{_unitdir}/supergfxd.service
install -D -m 0644 data/supergfxd.preset %{buildroot}%{_presetdir}/98-supergfxd.preset

sed -i 's|/usr/bin/supergfxd|/usr/bin/supergfxd-battery-check.sh|g' %{buildroot}%{_unitdir}/supergfxd.service

install -D -m 0644 LICENSE %{buildroot}%{_datadir}/licenses/%{name}/LICENSE
install -D -m 0644 README.md %{buildroot}%{_datadir}/doc/%{name}/README.md

%post
%systemd_post supergfxd.service

%preun
%systemd_preun supergfxd.service

%postun
%systemd_postun_with_restart supergfxd.service

%files
%license LICENSE
%{_bindir}/supergfxd
%{_bindir}/supergfxd-battery-check.sh
%{_bindir}/supergfxctl
%{_unitdir}/supergfxd.service
%{_presetdir}/98-supergfxd.preset
%{_udevrulesdir}/90-supergfxd-nvidia-pm.rules
%{_sysconfdir}/dbus-1/system.d/org.supergfxctl.Daemon.conf
%dir %{_datadir}/doc
%dir %{_datadir}/doc/%{name}
%{_datadir}/doc/%{name}/*

%changelog
