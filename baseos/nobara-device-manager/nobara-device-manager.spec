Name:          nobara-device-manager
Version:       0.1.0
Release:       1%{?dist}
License:       MPLv2
Group:         System Environment/Libraries
Summary:       Nobara Device Manager - Device and Driver control adw gui

URL:            https://github.com/Nobara-Project/nobara-device-manager
Source0:        %{URL}/archive/refs/tags/%{version}.tar.gz

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

Requires:      cfhdb

%prep
%autosetup -p1 -n {version}

%build
DESTDIR=%{buildroot} make install

%description
Nobara Device Manager - Device and Driver control adw gui

%files
%{_bindir}/*
%{_datadir}/applications/*
%{_datadir}/glib-2.0/schemas/*
%{_datadir}/icons/hicolor/scalable/apps/*.svg

%post
glib-compile-schemas /usr/share/glib-2.0/schemas/
