%global commit  274e439dc1f2fcf39186f867a7a863269e236244

Name:           qtgreet
Version:        2.0.1
Release:        2%{?dist}
Summary:        Qt based greeter for greetd

License:        GPL-3.0-or-later
URL:            https://gitlab.com/marcusbritanicus/QtGreet
Source:         %{url}/-/archive/v%{version}/QtGreet-%{version}.tar.gz
Patch0:         0001-Don-t-list-GNOME-s-duplicate-session-entries-also-KD.patch

BuildRequires:  dfl-ipc-devel
BuildRequires:  dfl-applications-devel
BuildRequires:  dfl-login1-devel
BuildRequires:  dfl-utils-devel
BuildRequires:  dfl-wayqt-devel
BuildRequires:  mpv-devel
BuildRequires:  jack-audio-connection-kit-devel
BuildRequires:  meson
BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  ninja-build
BuildRequires:  pkgconfig(json-c)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  wayland-protocols-devel
BuildRequires:  wlroots-devel
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


Requires:  greetd >= 0.6
Requires:  dfl-ipc
Requires:  dfl-applications
Requires:  dfl-login1
Requires:  dfl-utils
Requires:  dfl-wayqt
Requires:  qt5-qtbase
Requires:  qt5-qtwayland

Provides:       greetd-%{name} = %{version}-%{release}

%description
%{summary}.


%prep
%autosetup -p1 -n QtGreet-v%{version}-%{commit}


%build
# QT6
#%%meson -Duse_qt_version=qt6 --buildtype=release
%meson -Duse_qt_version=qt5 --buildtype=release
%meson_build


%install
%meson_install

install -D -m 0644 -pv -t %{buildroot}%{_sysconfdir}/%{name} \
    configs/config.ini configs/wayfire.ini
install -D -m 0644 -pv -t %{buildroot}%{_datadir}/%{name}/backgrounds \
    backgrounds/*


%files
%license LICENSE 
%doc README.md
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/config.ini
%config(noreplace) %{_sysconfdir}/%{name}/wayfire.ini
%config(noreplace) %{_sysconfdir}/%{name}/sway.cfg
%config(noreplace) %{_sysconfdir}/%{name}/users.conf
%{_bindir}/%{name}
%{_bindir}/greetwl
%{_datadir}/%{name}


%changelog
* Tue Aug 30 2022 Aleksei Bavshin <alebastr@fedoraproject.org> - 1.0.0-0.1
- Initial package
