Name:           opengamepadui
Version:        0.35.7
Release:        1%{?dist}
Summary:        A free and open source game launcher and overlay written using the Godot Game Engine 4 designed with a gamepad native experience in mind
License:        GPL-3.0-only
URL:            https://github.com/ShadowBlip/OpenGamepadUI
BuildArch:      x86_64

Patch0:         fedora.patch

Requires:       gamescope
Requires:       python3

BuildRequires:  make
BuildRequires:  cargo
BuildRequires:  git
BuildRequires:  godot
BuildRequires:  wget
BuildRequires:  systemd-rpm-macros

%description
A free and open source game launcher and overlay written using the Godot Game Engine 4 designed with a gamepad native experience in mind

%define debug_package %{nil}
%define _build_id_links none

%prep
git clone https://github.com/ShadowBlip/OpenGamepadUI
cd OpenGamepadUI
git checkout v%{version}
patch -Np1 < %{PATCH0}

%build
cd OpenGamepadUI
make install PREFIX=%{buildroot}%{_prefix} INSTALL_PREFIX=%{_prefix}

%files
%{_bindir}/opengamepadui
%{_datadir}/opengamepadui/*.so
%{_datadir}/opengamepadui/opengamepad-ui.x86_64
%{_datadir}/opengamepadui/opengamepad-ui.pck
%{_datadir}/opengamepadui/reaper
%{_datadir}/opengamepadui/scripts/make_nice
%{_datadir}/opengamepadui/scripts/manage_input
%{_datadir}/applications/opengamepadui.desktop
%{_datadir}/icons/hicolor/scalable/apps/opengamepadui.svg
%{_datadir}/polkit-1/actions/org.shadowblip.manage_input.policy
%{_datadir}/polkit-1/actions/org.shadowblip.setcap.policy
%{_userunitdir}/systemd-sysext-updater.service
%{_userunitdir}/ogui-overlay-mode.service

%changelog
%autochangelog
