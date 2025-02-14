# Autofetch sources

%define _disable_source_fetch 0
%define __spec_install_post /usr/lib/rpm/brp-compress || :
%define debug_package %{nil}

# Establish the name and source

Name:       obs-aitum-multistream
Version:    1.0.7
Release:    1%{?dist}
Summary:    Multistream plugin for OBS
License:    GPL=2.0
URL:        https://github.com/Aitum/obs-aitum-multistream
Source0:    %{URL}/archive/refs/tags/%{version}.tar.gz
Patch0:     0001-cmake-fixup.patch

BuildRequires:  cmake
BuildRequires:  obs-studio-devel
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qtbase-private-devel
BuildRequires:  qt6-qtsvg-devel
BuildRequires:  qt6-qtwayland-devel
BuildRequires:  libcurl-devel
Requires:       obs-studio
Requires:       qt6-qtbase

#A fitting description
%description
A multistreaming plugin for OBS Studio by Aitum

# Here autosetup is a useful macro
%prep
%autosetup -p1

# Build phase calls cmake to build our file
%build
%cmake \
    -DBUILD_OUT_OF_TREE=On
%cmake_build

%install
%cmake_install

%files
%{_datadir}/obs/obs-plugins/aitum-multistream
%{_libdir}/obs-plugins/aitum-multistream.so
