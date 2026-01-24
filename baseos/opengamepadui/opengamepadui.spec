# Use Custom godot for now. 4.5 is broken and opengamepadui still uses 4.4
%global godot_version 4.5

Name:           opengamepadui
Version:        0.44.1
Release:        8%{?dist}
Summary:        A free and open source game launcher and overlay written using the Godot Game Engine 4 designed with a gamepad native experience in mind

License:        GPL-3.0-only
URL:            https://github.com/ShadowBlip/OpenGamepadUI

# Use Custom godot for now. 4.5 is broken and opengamepadui still uses 4.4
# Upstream URL reference:
# https://downloads.godotengine.org/?version=4.4&flavor=stable&slug=linux.x86_64.zip&platform=linux.64
Source0:        Godot_v%{godot_version}-stable_linux.x86_64.zip

Patch0:         fedora.patch
ExcludeArch:    %{ix86}

Requires:       gamescope

BuildRequires:  make
BuildRequires:  cargo
BuildRequires:  git
BuildRequires:  wget
BuildRequires:  systemd-rpm-macros

# Use Custom godot for now. 4.5 is broken and opengamepadui still uses 4.4
#BuildRequires:  godot
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

%build
cd OpenGamepadUI

# Unpack the bundled Godot 4.4 binary
rm -rf %{_builddir}/godot-%{godot_version}
mkdir -p %{_builddir}/godot-%{godot_version}
unzip -q %{SOURCE0} -d %{_builddir}/godot-%{godot_version}

# Locate the Godot binary inside the zip (name varies slightly by upstream)
GODOT_BIN="$(find %{_builddir}/godot-%{godot_version} -type f -name 'Godot_v%{godot_version}*linux.x86_64*' -o -name 'Godot_v%{godot_version}*linux.64*' | head -n 1)"
test -n "$GODOT_BIN"
chmod +x "$GODOT_BIN"

export GODOT="$GODOT_BIN"

# Build/install using the custom Godot
make install PREFIX=%{buildroot}%{_prefix} INSTALL_PREFIX=%{_prefix}

%files
%{_bindir}/%{name}
%{_datadir}/%{name}/*.so
%{_datadir}/%{name}/reaper
%{_datadir}/%{name}/scripts/*
%{_datadir}/%{name}/opengamepad-ui.x86_64
%{_datadir}/%{name}/opengamepad-ui.pck
%{_datadir}/applications/%{name}.desktop
%{_datadir}/polkit-1/actions/*
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg
%{_userunitdir}/*

%changelog
%autochangelog
