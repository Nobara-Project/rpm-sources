%define _disable_source_fetch 0
%define __spec_install_post /usr/lib/rpm/brp-compress || :
%define debug_package %{nil}

Name:       obs-studio-plugin-vertical-canvas
Version:    1.5.2
Release:    1%{?dist}
Summary:    Vertical canvas plugin for OBS

License:    GPL=2.0
URL:        https://github.com/Aitum/obs-vertical-canvas
Source0:    %{URL}/archive/refs/tags/%{version}.tar.gz
Patch0:     0001-cmake-fixup.patch

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  obs-studio-devel
BuildRequires:  libcurl-devel
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qtbase-private-devel
BuildRequires:  qt6-qtsvg-devel
BuildRequires:  qt6-qtwayland-devel
Requires:       obs-studio
Requires:       qt6-qtbase

Provides:   obs-studio-plugin-vertical-canvas
Provides:   obs-vertical-canvas
Obsoletes:  obs-vertical-canvas

%description
Plugin for OBS Studio to add vertical canvas by Aitum

%prep
%autosetup -p1 -n obs-vertical-canvas-%{version}

%build
%cmake \
    -DBUILD_OUT_OF_TREE=On \
    -DCMAKE_BUILD_TYPE=Release
%cmake_build

%install
%cmake_install

%files
%{_datadir}/obs/obs-plugins/vertical-canvas
%{_libdir}/obs-plugins/vertical-canvas.so
