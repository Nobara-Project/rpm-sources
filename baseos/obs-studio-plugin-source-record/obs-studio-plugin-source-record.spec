# Autofetch sources

%define _disable_source_fetch 0
%define __spec_install_post /usr/lib/rpm/brp-compress || :
%define debug_package %{nil}

# Establish the name and source

Name:       obs-studio-plugin-source-record
Version:    0.4.4
Release:    1%{?dist}
Summary:    Multistream plugin for OBS
License:    GPL=2.0
URL:        https://github.com/exeldro/obs-source-record
Source0:    %{URL}/archive/refs/tags/0.4.4.tar.gz

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
%autosetup -p1 -n obs-source-record-%{version}

# Build phase calls cmake to build our file
%build
%cmake \
    -DBUILD_OUT_OF_TREE=On -DLIB_OUT_DIR=%{_lib}/obs-plugins
%cmake_build

%install
%cmake_install

# remove duplicate/unused
rm -Rf %{buildroot}/usr/obs-plugins
rm -Rf %{buildroot}/usr/data

%files
%{_datadir}/obs/obs-plugins/source-record/
%{_libdir}/obs-plugins/source-record.so
