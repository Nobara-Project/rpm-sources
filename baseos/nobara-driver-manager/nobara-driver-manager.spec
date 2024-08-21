Name:          nobara-driver-manager
Version:       1.1
Release:       3%{?dist}
License:       GPLv2
Group:         System Environment/Libraries
Summary:       Nobara's Driver Manager


URL:            https://github.com/nobara-project/nobara-core-packages
Source0:        %{URL}/releases/download/1.0/nobara-drivers-gtk4.tar.gz

BuildRequires:	wget
BuildRequires:	cargo
BuildRequires:	gdk-pixbuf2-devel
BuildRequires:	gtk4-devel
BuildRequires:	gtk3-devel
BuildRequires:	libadwaita-devel
BuildRequires:	openssl-devel


Requires:      /usr/bin/bash
Requires:	python3
Requires:	python
Requires:	gtk3
Requires:	gtk4
Requires:	libadwaita
Requires: 	glib2

# App Deps
Requires:	python3-gobject
Requires:	nobara-login
Requires:	nobara-login-config
Requires:	nobara-controller-config
Requires:	webapp-manager
Requires:	papirus-icon-theme
Requires: 	gperftools-libs(x86-32)
Requires: 	xterm-resize
Requires: 	colorized-logs
Requires: 	util-linux
Requires: 	nobara-driver-manager
Requires: 	vte291

Provides: nobara-nvidia-wizard
Obsoletes: nobara-nvidia-wizard

# Gnome Deps
Suggests:	gnome-tweaks

# KDE Deps
Suggests:	kde-runtime

%prep
%autosetup -p1 -n nobara-drivers-gtk4

%build
DESTDIR=%{buildroot} make install

%description
Nobara's Python3 & GTK4 built Welcome App

%files
%{_prefix}/lib/nobara/drivers/*
%{_bindir}/*
%{_datadir}/applications/*
%{_datadir}/glib-2.0/schemas/*
%{_datadir}/icons/hicolor/scalable/apps/*.svg

%post
glib-compile-schemas /usr/share/glib-2.0/schemas/

