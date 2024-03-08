## Build order:
## dfl-utils
%global _gitname utils

Name:           dfl-utils
Version:        0.2.0
Release:        1%{?dist}
Summary:        Some utilities for DFL

License:        GPL-3.0-or-later
URL:            https://gitlab.com/desktop-frameworks/%{_gitname}
Source:         %{url}/-/archive/v%{version}/%{_gitname}-v%{version}.tar.gz

BuildRequires:  meson
BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  qt5-qtbase
BuildRequires:  cmake(Qt5Core)

#QT6
#BuildRequires:  qt6-qtbase
#BuildRequires:  cmake(Qt6Core)

%description
%{summary}.

%package devel
Summary: Development package for %{name}
Requires: %{name}

%description devel
Header files and libraries for developing dfl applications.

%prep
%autosetup -n %{_gitname}-v%{version}


%build
# QT6
#%%meson -Duse_qt_version=qt6 --buildtype=release
%meson --buildtype=release
%meson_build


%install
%meson_install

%files
%license LICENSE 
%doc README.md
%{_libdir}/lib*.so.*
%{_libdir}/pkgconfig/*

%files devel
%{_includedir}/DFL/*
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*

%changelog
* Tue Aug 30 2022 Aleksei Bavshin <alebastr@fedoraproject.org> - 1.0.0-0.1
- Initial package
