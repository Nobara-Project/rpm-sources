%global qt5_minver 5.15.0
%global kf5_minver 5.83.0
%global kp5_minver 5.27.5

Name:           xwaylandvideobridge
Version:        0.4.0
Release:        3%{?dist}
Summary:        Utility to allow streaming Wayland windows to X applications

License:        (GPL-2.0-only or GPL-3.0-only) and LGPL-2.0-or-later and BSD-3-Clause
URL:            https://invent.kde.org/system/xwaylandvideobridge
Source0:        https://download.kde.org/stable/%{name}/%{name}-%{version}.tar.xz

BuildRequires:  libappstream-glib
BuildRequires:  desktop-file-utils
BuildRequires:  cmake >= 3.16
BuildRequires:  gcc-c++
BuildRequires:  ninja-build
BuildRequires:  extra-cmake-modules >= %{kf5_minver}
BuildRequires:  cmake(Qt5Quick) >= %{qt5_minver}
BuildRequires:  cmake(Qt5DBus) >= %{qt5_minver}
BuildRequires:  cmake(Qt5X11Extras) >= %{qt5_minver}
BuildRequires:  cmake(KF5CoreAddons) >= %{kf5_minver}
BuildRequires:  cmake(KF5I18n) >= %{kf5_minver}
BuildRequires:  cmake(KF5WindowSystem) >= %{kf5_minver}
BuildRequires:  cmake(KF5Notifications) >= %{kf5_minver}
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(xcb-composite)
BuildRequires:  pkgconfig(xcb-event)
BuildRequires:  pkgconfig(xcb-record)
BuildRequires:  pkgconfig(xcb-xfixes)
BuildRequires:  cmake(KPipeWire) >= %{kp5_minver}

Requires:       hicolor-icon-theme
Requires:       glx-utils

# Requires at least KPipeWire 5.27.5
Requires:       kpipewire%{?_isa} >= %{kp5_minver}

%description
By design, X11 applications can't access window or screen contents
for wayland clients. This is fine in principle, but it breaks screen
sharing in tools like Discord, MS Teams, Skype, etc and more.

This tool allows us to share specific windows to X11 clients,
but within the control of the user at all times.


%prep
%autosetup -n %{name}-%{version} -p1


%build
%cmake_kf5 -GNinja
%cmake_build


%install
%cmake_install

%find_lang %{name} --all-name


%check
appstream-util validate-relax --nonet %{buildroot}%{_kf5_metainfodir}/org.kde.%{name}.appdata.xml
desktop-file-validate %{buildroot}%{_kf5_datadir}/applications/org.kde.%{name}.desktop
mkdir -p %{buildroot}%{_sysconfdir}/xdg/autostart/
cp %{buildroot}%{_kf5_datadir}/applications/org.kde.%{name}.desktop %{buildroot}%{_sysconfdir}/xdg/autostart/


%files -f %{name}.lang
%license LICENSES/*
%doc README.md
%{_kf5_bindir}/%{name}
%{_kf5_datadir}/applications/org.kde.%{name}.desktop
%{_kf5_datadir}/icons/hicolor/*/apps/%{name}.*
%{_kf5_metainfodir}/org.kde.%{name}.appdata.xml
%{_kf5_datadir}/qlogging-categories5/%{name}.categories
%{_sysconfdir}/xdg/autostart/org.kde.%{name}.desktop


%changelog
* Mon Dec 04 2023 Alessandro Astone <ales.astone@gmail.com> - 0.3.0-2
- Do not start in an X11 session
- Opt out of session managment
- Skip the task switcher

* Thu Nov 09 2023 Alessandro Astone <ales.astone@gmail.com> - 0.3.0-1
- Update to 0.3
- Autostart on login

* Fri Oct 27 2023 Alessandro Astone <ales.astone@gmail.com> - 0.2-1
- Update to tagged release 0.2

* Mon Sep 18 2023 Neal Gompa <ngompa@fedoraproject.org> - 0~git20230917.9b27c3f-1
- Bump to new git snapshot

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0~git20230504.3445aff-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon May 15 2023 Neal Gompa <ngompa@fedoraproject.org> - 0~git20230504.3445aff-2
- Add dependency on hicolor-icon-theme

* Wed May 10 2023 Neal Gompa <ngompa@fedoraproject.org> - 0~git20230504.3445aff-1
- Initial package
