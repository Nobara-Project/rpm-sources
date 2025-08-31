%define _disable_source_fetch 0
%global debug_package %{nil}

Name:           mangojuice
Version:        0.8.7
Release:        1%{?dist}
Summary:        Graphical UI to manage Mangohud settings
Group:          Graphics/Utilities
License:        GPLv3
URL:            https://github.com/radiolamp/mangojuice
Source0:        %{URL}/archive/refs/tags/%{version}.tar.gz

ExcludeArch:    %{ix86}

BuildRequires:  meson
BuildRequires:  cmake
BuildRequires:  pkgconfig(libadwaita-1)
BuildRequires:  pkgconfig(gee-0.8)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(gtk4)
BuildRequires:  pkgconfig(vapigen)

Requires:  mangohud
Requires:  vulkan-tools
Requires:  gtk4

%description
This program will be a convenient alternative to Goverlay for setting up Mangohud.

%prep
%autosetup -n mangojuice-%{version}

%build
%meson 
%meson_build

%install
%meson_install

%files
%{_bindir}/mangojuice
%{_datadir}/applications/io.github.radiolamp.mangojuice.desktop
%{_datadir}/icons/hicolor/scalable/apps/io.github.radiolamp.mangojuice*
%{_datadir}/locale/ru_RU/LC_MESSAGES/mangojuice.mo
%{_datadir}/locale/pt_BR/LC_MESSAGES/mangojuice.mo
%{_datadir}/metainfo/io.github.radiolamp.mangojuice.metainfo.xml

%changelog
* Sun Aug 31 2025 LionHeartP <LionHeartP@proton.me> - 0.8.7-1
- Update to 0.8.7

* Thu Jul 24 2025 LionHeartP <LionHeartP@proton.me> - 0.8.6-1
- Update to 0.8.6

* Tue May 27 2025 LionHeartP <LionHeartP@proton.me> - 0.8.5-1
- Update to 0.8.5
- Add new files for pt_BR
