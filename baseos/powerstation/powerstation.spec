%define __spec_install_post %{nil}
%define __os_install_post %{_dbpath}/brp-compress
%define debug_package %{nil}

Name:           powerstation
Version:        0.4.2
Release:        1%{?dist}
Summary:        Daemon for controlling TDP and performance over DBus

License:        GPL-3.0-or-later
URL:            https://github.com/ShadowBlip/PowerStation
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz

ExcludeArch:    %{ix86}

BuildRequires:  rust
BuildRequires:  cargo
BuildRequires:  pciutils-devel
BuildRequires:  systemd-devel
BuildRequires:  clang
BuildRequires:  cmake
Requires:       dbus
Requires:       libgcc
Requires:       glibc
Requires:       pciutils-libs
Requires:       systemd-libs
Requires:       zlib-ng-compat

%description
Powerstation is a daemon for controlling TDP and performance over DBus.
It is designed for use on AMD platforms with access to libryzenadj.

%prep
%autosetup -n PowerStation-%{version}

%build
cargo build --release

%install
# Binary
install -Dm755 target/release/powerstation %{buildroot}/usr/bin/powerstation

# DBus system policy
install -Dm644 rootfs/usr/share/dbus-1/system.d/org.shadowblip.PowerStation.conf \
  %{buildroot}/usr/share/dbus-1/system.d/org.shadowblip.PowerStation.conf

# Systemd service
install -Dm644 rootfs/usr/lib/systemd/system/powerstation.service \
  %{buildroot}/usr/lib/systemd/system/powerstation.service

%files
%license LICENSE
%doc README.md
/usr/bin/powerstation
/usr/share/dbus-1/system.d/org.shadowblip.PowerStation.conf
/usr/lib/systemd/system/powerstation.service

%post
systemctl enable powerstation.service
systemctl start powerstation.service

%changelog
* Fri Apr 18 2025 Your Name <you@example.com> - 0.4.2-1
- Initial RPM release
