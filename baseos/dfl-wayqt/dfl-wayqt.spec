## Build order:
## dfl-wayqt
%global _gitname wayqt
Name:           dfl-wayqt
Version:        0.2.0
Release:        1%{?dist}
Summary:        A Qt-based wrapper for various wayland protocols

License:        GPL-3.0-or-later
URL:            https://gitlab.com/desktop-frameworks/%{_gitname}
Source:         %{url}/-/archive/v%{version}/%{_gitname}-v%{version}.tar.gz

BuildRequires:  meson
BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  ninja-build
BuildRequires:  pkgconfig(json-c)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  wayland-protocols-devel
BuildRequires:  qt5-qtbase
BuildRequires:  qt5-qtbase-private-devel
BuildRequires:  cmake(Qt5Core)
BuildRequires:  cmake(Qt5Gui)
BuildRequires:  cmake(Qt5WaylandClient)
# workaround for
#   The imported target "Qt5::XkbCommonSupport" references the file
#     "/usr/lib64/libQt5XkbCommonSupport.a"
#  but this file does not exist.
BuildRequires:  qt5-qtbase-static

#QT6
#BuildRequires:  qt6-qtbase
#BuildRequires:  qt6-qtbase-private-devel
#BuildRequires:  cmake(Qt6Core)
#BuildRequires:  cmake(Qt6Gui)
#BuildRequires:  cmake(Qt6WaylandClient)
# workaround for
#   The imported target "Qt5::XkbCommonSupport" references the file
#     "/usr/lib64/libQt5XkbCommonSupport.a"
#  but this file does not exist.
#BuildRequires:  qt6-qtbase-static

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
%meson -Duse_qt_version=qt5 --buildtype=release
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
