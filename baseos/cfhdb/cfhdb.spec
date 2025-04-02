Name:          cfhdb
Version:       0.1.2
Release:       1%{?dist}
License:       MPLv2
Group:         System Environment/Libraries
Summary:       CosmicFusion Hardware Database - Nobara Edition

URL:            https://github.com/Nobara-Project/cfhdb
Source0:        %{URL}/archive/refs/tags/%{version}.tar.gz

BuildRequires:    cargo
BuildRequires:    clang-devel
BuildRequires:    kernel-devel
BuildRequires:    llvm-devel
BuildRequires:    openssl-devel
BuildRequires:    pkgconfig(libusb-1.0)
BuildRequires:    pkgconfig(libpci)

Requires:      /usr/bin/bash
Requires:      usbutils

%prep
%autosetup -p1 -n {version}

%build
DESTDIR=%{buildroot} make install

%description
CosmicFusion Hardware Database - Nobara Edition

%files
%{_prefix}/lib/cfhdb/*
%{_prefix}/lib/systemd/system/*
%{_datadir}/polkit-1/*
%{_bindir}/*
%{_sysconfdir}/cfhdb/*

%post
mkdir -p /var/cache/cfhdb || true
chmod -R 777 /var/cache/cfhdb
systemctl enable cfhdb-unbind-blacklist.service || true
