# Autofetch sources

%define _disable_source_fetch 0
%define __spec_install_post /usr/lib/rpm/brp-compress || :
%define debug_package %{nil}

# Establish the name and source

%global commit c48b4bf182f8b354255df7329c9afe3dee4f9820
Name:       obs-studio-plugin-aitum-multistream
Version:    1.0.8
Release:    1%{?dist}
Summary:    Multistream plugin for OBS
License:    GPL=2.0
URL:        https://github.com/Aitum/obs-aitum-multistream
#Source0:    %{URL}/archive/refs/tags/%{version}.tar.gz
Source0:    %{URL}/archive/refs/heads/main.tar.gz

#Patch0:     0001-cmake-fixup.patch
ExcludeArch:%{ix86}


BuildRequires:  cmake
BuildRequires:  obs-studio-devel
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qtbase-private-devel
BuildRequires:  qt6-qtsvg-devel
BuildRequires:  qt6-qtwayland-devel
BuildRequires: cmake(Qt6GuiPrivate)
BuildRequires: libxkbcommon-devel
BuildRequires:  libcurl-devel
Requires:       obs-studio
Requires:       qt6-qtbase

Provides:   obs-studio-plugin-aitum-multistream
Provides:   obs-aitum-multistream
Obsoletes:  obs-aitum-multistream

#A fitting description
%description
A multistreaming plugin for OBS Studio by Aitum

# Here autosetup is a useful macro
%prep
#%%autosetup -p1 -n obs-aitum-multistream-%{version}
%autosetup -p1 -n obs-aitum-multistream-main

# Build phase calls cmake to build our file
%build
%cmake \
    -DBUILD_OUT_OF_TREE=On \
    -DCMAKE_NO_SYSTEM_FROM_IMPORTED=ON \
    -DCMAKE_CXX_FLAGS="-Wno-error=deprecated-declarations"
%cmake_build

%install
%cmake_install

%files
%{_datadir}/obs/obs-plugins/aitum-multistream
%{_libdir}/obs-plugins/aitum-multistream.so
