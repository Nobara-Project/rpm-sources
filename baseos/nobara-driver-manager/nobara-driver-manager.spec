Name:          nobara-driver-manager
Epoch:	       2
Version:       0.1.3
Release:       4%{?dist}
License:       MPLv2
Group:         System Environment/Libraries
Summary:       Nobara Driver Manager - Device and Driver control adw gui

URL:            https://github.com/Nobara-Project/nobara-device-manager
Source0:        %{URL}/archive/refs/tags/%{version}.tar.gz
Source1: 	nobara-driver-cli

# https://fedoraproject.org/wiki/Changes/EncourageI686LeafRemoval
ExcludeArch:    %{ix86}

BuildRequires:    cargo
BuildRequires:    clang-devel
BuildRequires:    gdk-pixbuf2-devel
BuildRequires:    gtk4-devel
BuildRequires:    kernel-devel
BuildRequires:    libadwaita-devel
BuildRequires:    llvm-devel
BuildRequires:    openssl-devel
BuildRequires:    pkgconfig(libusb-1.0)
BuildRequires:    pkgconfig(libpci)

Requires:	cfhdb

Provides:	nobara-nvidia-wizard
Obsoletes:	nobara-nvidia-wizard

%prep
%autosetup -p1 -n nobara-device-manager-%{version}
cp %{SOURCE1} .

%build

%install
DESTDIR=%{buildroot} make install
install -Dpm 0755 nobara-driver-cli %{buildroot}%{_bindir}/nobara-driver-cli

%description
Nobara Driver Manager - Device and Driver control adw gui

%files
%{_bindir}/*
%{_datadir}/applications/*
%{_datadir}/glib-2.0/schemas/*
%{_datadir}/icons/hicolor/scalable/apps/*.svg

%post
glib-compile-schemas /usr/share/glib-2.0/schemas/
