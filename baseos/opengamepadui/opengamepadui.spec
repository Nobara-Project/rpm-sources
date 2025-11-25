Name:           opengamepadui
Version:        0.42.1
Release:        1%{?dist}
Summary:        A free and open source game launcher and overlay written using the Godot Game Engine 4 designed with a gamepad native experience in mind

License:        GPL-3.0-only
URL:            https://github.com/ShadowBlip/OpenGamepadUI

Source:         %{URL}/releases/download/v%{version}/%{name}.tar.gz

ExcludeArch:    %{ix86}

Requires:       gamescope

BuildRequires:  make
BuildRequires:  systemd-rpm-macros

%description
A free and open source game launcher and overlay written using the Godot Game Engine 4 designed with a gamepad native experience in mind

%define debug_package %{nil}
%define _build_id_links none
%define __os_install_post %{nil}

%prep
%autosetup -p1 -n opengamepadui

%install
make install PREFIX=%{buildroot}%{_prefix} INSTALL_PREFIX=%{_prefix}

%files
%{_bindir}/%{name}
%{_datadir}/%{name}/*.so
%{_datadir}/%{name}/reaper
%{_datadir}/%{name}/scripts/*
%{_datadir}/%{name}/opengamepad-ui.x86_64
%{_datadir}/%{name}/opengamepad-ui.pck
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg
%{_datadir}/polkit-1/actions/*
/usr/lib/systemd/user/*

%changelog
%autochangelog
