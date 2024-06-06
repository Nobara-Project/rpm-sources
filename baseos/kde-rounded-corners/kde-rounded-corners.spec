%global gitcommit 3162c11532e10f7c8b8bd6eb21de85392ad66cad

Name:           kde-rounded-corners
Version:        0.6.5
Release:        7%{?dist}
Summary:        Rounds the corners of your windows in KDE Plasma

License:        GPL-3.0-only
URL:            https://github.com/matinlotfali/KDE-Rounded-Corners
Source0:        https://github.com/matinlotfali/KDE-Rounded-Corners/archive/%{gitcommit}.tar.gz
Patch0:         0001-use-some-sane-default-shadows-and-outlines.patch

BuildRequires:  cmake
BuildRequires:  extra-cmake-modules
BuildRequires:  gcc-c++
BuildRequires:  kf6-rpm-macros
BuildRequires:  wayland-devel

BuildRequires:  cmake(KF6Config)
BuildRequires:  cmake(KF6ConfigWidgets)
BuildRequires:  cmake(KF6CoreAddons)
BuildRequires:  cmake(KF6GlobalAccel)
BuildRequires:  cmake(KF6KCMUtils)
BuildRequires:  cmake(KF6WindowSystem)

BuildRequires:  cmake(Qt6Core)
BuildRequires:  cmake(Qt6DBus)
BuildRequires:  cmake(Qt6Gui)
BuildRequires:  cmake(Qt6Network)
BuildRequires:  cmake(Qt6OpenGL)
BuildRequires:  cmake(Qt6Widgets)
BuildRequires:  cmake(Qt6Xml)
BuildRequires:  qt6-qtbase-private-devel

BuildRequires:  cmake(KWin)
BuildRequires:  cmake(KWinDBusInterface)
BuildRequires:  pkgconfig(epoxy)
BuildRequires:  pkgconfig(xcb)
Obsoletes:  plasma-rounded-corners

%description
%{summary}.

%prep
%autosetup -n KDE-Rounded-Corners-%{gitcommit} -p1

%build
%cmake_kf6 -DQT_MAJOR_VERSION=6
%cmake_build

%install
%cmake_install

%files
%license LICENSE
%doc README.md
%{_kf6_datadir}/kwin/shaders/shapecorners*.frag
%{_qt6_plugindir}/kwin/effects/configs/kwin_shapecorners_config.so
%{_qt6_plugindir}/kwin/effects/plugins/kwin4_effect_shapecorners.so

%changelog
* Thu May 23 2024 Pavel Solovev <daron439@gmail.com> - 0.6.5-2
- rebuilt

* Tue Apr 16 2024 Pavel Solovev <daron439@gmail.com> - 0.6.1-7
- rebuilt

* Wed Mar 27 2024 Pavel Solovev <daron439@gmail.com> - 0.6.1-6
- rebuilt

* Fri Jan 12 2024 Pavel Solovev <daron439@gmail.com>
- Initial build
