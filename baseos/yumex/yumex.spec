%global app_id dk.yumex.Yumex
%global app_build debug
%global dnf_backend DNF4
%global gitcommit 645173b12efdf77027b14c1d845107118e58da42
%global shortcommit 645173b

Name:     yumex
Version:  4.99.4
Release:  0.16.git.%{shortcommit}%{?dist}
Summary:  Yum Extender graphical package management tool

Group:    Applications/System
License:  GPLv3+
URL:      http://yumex.dk
Source0:  https://github.com/timlau/yumex-ng/archive/%{gitcommit}.zip#/%{name}-%{shortcommit}.tar.gz
Source1:  rename-desktop-shortcut.patch
Source2:  0001-add-nobara-update-system-button.patch

BuildArch: noarch
BuildRequires: python3-devel
BuildRequires: meson
BuildRequires: blueprint-compiler >= 0.4.0
BuildRequires: gettext
BuildRequires: desktop-file-utils
BuildRequires: libappstream-glib
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(gtk4)
BuildRequires: pkgconfig(libadwaita-1)
BuildRequires: pkgconfig(pygobject-3.0)


Requires: python3-dnfdaemon
Requires: python3-gobject
Requires: python3-dnf
Requires: libadwaita
Requires: gtk4
Requires: flatpak-libs
Requires: nobara-welcome

# support for dnf5 backend
%if "%{dnf_backend}" == "DNF5"
Requires: python3-libdnf5
%endif

Obsoletes: yumex-dnf <= 4.5.1



%description
Graphical package tool for maintain packages on the system


%prep
%setup -q -n %{name}-ng-%{gitcommit}
patch -Np1 < %{SOURCE1}
patch -Np1 < %{SOURCE2}

%check
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/*.metainfo.xml
desktop-file-validate %{buildroot}/%{_datadir}/applications/%{app_id}.desktop
# hack so we don't have to recompile gnome and kde packages for default taskbar applications
mv %{buildroot}/%{_datadir}/applications/%{app_id}.desktop %{buildroot}/%{_datadir}/applications/yumex-dnf.desktop


%build
%meson --buildtype=%{app_build} -Ddnf_backend=%{dnf_backend}
%meson_build

%install
%meson_install

%find_lang %name

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
update-desktop-database %{_datadir}/applications &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache -f %{_datadir}/icons/hicolor &>/dev/null || :
fi
update-desktop-database %{_datadir}/applications &> /dev/null || :

%posttrans
/usr/bin/gtk-update-icon-cache -f %{_datadir}/icons/hicolor &>/dev/null || :

%files -f  %{name}.lang
%doc README.md
%license LICENSE
%{_datadir}/%{name}
%{_bindir}/%{name}
%{python3_sitelib}/%{name}/
%{_datadir}/applications/yumex-dnf.desktop
%{_datadir}/icons/hicolor/
%{_metainfodir}/%{app_id}.metainfo.xml
%{_datadir}/glib-2.0/schemas/%{app_id}.gschema.xml

%changelog

* Sat Jan 21 2023 Tim Lauridsen <timlau@fedoraproject.org> 4.99.3-1
- the 4.99.3 release

* Wed Jan 4 2023 Tim Lauridsen <timlau@fedoraproject.org> 4.99.2-1
- add support for building with dnf5 backend

* Wed Jan 4 2023 Tim Lauridsen <timlau@fedoraproject.org> 4.99.2-1
- the 4.99.2 release

* Tue Dec 20 2022 Tim Lauridsen <timlau@fedoraproject.org> 4.99.1-1
- the 4.99.1 release

* Tue Dec 20 2022 Tim Lauridsen <timlau@fedoraproject.org> 4.99.0-1
- initial release (dev)

