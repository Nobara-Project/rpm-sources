%global godot_version 4.6.1

Name:           opengamepadui
Version:        0.45.0
Release:        8%{?dist}
Summary:        A free and open source game launcher and overlay written using the Godot Game Engine 4 designed with a gamepad native experience in mind

License:        GPL-3.0-only
URL:            https://github.com/ShadowBlip/OpenGamepadUI

%ifarch x86_64
Source0:        https://godot-releases.nbg1.your-objectstorage.com/%{godot_version}-stable/Godot_v%{godot_version}-stable_linux.x86_64.zip
%else
Source0:        https://godot-releases.nbg1.your-objectstorage.com/%{godot_version}-stable/Godot_v%{godot_version}-stable_linux.arm64.zip
%endif

Patch0:         fedora.patch
Patch1:         https://github.com/ShadowBlip/OpenGamepadUI/pull/519.patch
ExclusiveArch: x86_64 aarch64

Requires:       gamescope

BuildRequires:  make
BuildRequires:  cargo
BuildRequires:  git
BuildRequires:  wget
BuildRequires:  systemd-rpm-macros

BuildRequires:  unzip


%description
A free and open source game launcher and overlay written using the Godot Game Engine 4 designed with a gamepad native experience in mind

%define debug_package %{nil}
%define _build_id_links none

%prep
git clone %{URL}
cd OpenGamepadUI
git checkout v%{version}
patch -Np1 < %{PATCH0}
patch -Np1 < %{PATCH1}

%build
cd OpenGamepadUI

# Unpack the bundled Godot binary
rm -rf %{_builddir}/godot-%{godot_version}
mkdir -p %{_builddir}/godot-%{godot_version}
unzip -q %{SOURCE0} -d %{_builddir}/godot-%{godot_version}

# Locate the Godot binary inside the zip (name varies slightly by upstream)
%ifarch x86_64
GODOT_BIN="$(find %{_builddir}/godot-%{godot_version} -type f -name 'Godot_v%{godot_version}*linux.x86_64*' -o -name 'Godot_v%{godot_version}*linux.64*' | head -n 1)"
%else
GODOT_BIN="$(find %{_builddir}/godot-%{godot_version} -type f -name 'Godot_v%{godot_version}*linux.arm64*' -o -name 'Godot_v%{godot_version}*linux.64*' | head -n 1)"
%endif
test -n "$GODOT_BIN"
chmod +x "$GODOT_BIN"

export GODOT="$GODOT_BIN"

# Build/install using the custom Godot
make install PREFIX=%{buildroot}%{_prefix} INSTALL_PREFIX=%{_prefix} ARCH=%{_arch}

%files
%{_bindir}/%{name}
%{_datadir}/%{name}/*.so
%{_datadir}/%{name}/reaper
%{_datadir}/%{name}/scripts/*
%{_datadir}/%{name}/opengamepad-ui.%{_arch}
%{_datadir}/%{name}/opengamepad-ui.pck
%{_datadir}/applications/%{name}.desktop
%{_datadir}/polkit-1/actions/*
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg
%{_userunitdir}/*

%changelog
%autochangelog
