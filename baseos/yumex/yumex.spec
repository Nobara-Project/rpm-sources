%global app_id dk.yumex.Yumex
%global app_build release
%global dnf_backend DNF4
%global app_name yumex
%global gitcommit 0247b7c548e4c5d900204c548a1997492e13a21f
%global shortcommit 0247b7c

Name:     %{app_name}
Version:  5.0.3
Release:  15.git.%{shortcommit}%{?dist}
Summary:  Yum Extender graphical package management tool

Group:    Applications/System
License:  GPLv3+
URL:      http://yumex.dk
Source0:  https://github.com/timlau/yumex-ng/archive/%{gitcommit}.zip#/%{name}-%{shortcommit}.tar.gz
Source1:  nobara.package.manager.svg
Patch0:   rename-desktop-shortcut.patch
Patch1:   0001-add-nobara-update-system-button.patch
Patch2:   0001-add-missing-update_metadata_timestamp-import.-Fixes-.patch
Patch3:   0001-don-t-force-display-and-xauth-envvars-in-user-servic.patch

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
BuildRequires: systemd-rpm-macros

Requires: python3-gobject
Requires: libadwaita
Requires: gtk4
Requires: flatpak-libs
Requires: nobara-welcome
Requires: python3-dbus
Requires: libappindicator-gtk3
Requires: python3-dasbus

# dnf4 requirements
%if "%{dnf_backend}" == "DNF4"
Requires: python3-dnfdaemon
Requires: python3-dnf
%endif

# dnf5 requirements
%if "%{dnf_backend}" == "DNF5"
Requires: python3-libdnf5
Requires: dnf5daemon-server
%endif

Obsoletes: yumex-dnf <= 4.5.1



%description
Graphical package tool for maintain packages on the system


%prep
%autosetup -n %{name}-ng-%{gitcommit} -p1
cp %{SOURCE1} ./data/icons/hicolor/scalable/apps/

# Add nobara-updater as custom_updater option
sed -i 's|""|"/usr/bin/python3 /usr/bin/nobara-updater"|g'  data/dk.yumex.Yumex.gschema.xml.in

%check
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/*.metainfo.xml
desktop-file-validate %{buildroot}/%{_datadir}/applications/%{app_id}.desktop

%build
%meson --buildtype=%{app_build} -Ddnf_backend=%{dnf_backend}
%meson_build

%install
%meson_install

%find_lang %name

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
update-desktop-database %{_datadir}/applications &> /dev/null || :
glib-compile-schemas /usr/share/glib-2.0/schemas/
%systemd_user_post yumex-updater-systray.service

%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache -f %{_datadir}/icons/hicolor &>/dev/null || :
fi
update-desktop-database %{_datadir}/applications &> /dev/null || :

%files -f  %{app_name}.lang
%doc README.md
%license LICENSE
%{_datadir}/%{app_name}
%{_bindir}/%{app_name}
%{python3_sitelib}/%{app_name}/
%{_datadir}/applications/%{app_id}*.desktop
%{_datadir}/icons/hicolor/
%{_metainfodir}/%{app_id}.metainfo.xml
%{_datadir}/glib-2.0/schemas/%{app_id}.gschema.xml
%{_userunitdir}/*.service
%{_prefix}/lib/systemd/user-preset/*.preset
%{_bindir}/yumex_updater_systray

%posttrans
/usr/bin/gtk-update-icon-cache -f %{_datadir}/icons/hicolor &>/dev/null || :
%systemd_user_post yumex-updater-systray.service

%preun
%systemd_user_preun yumex-updater-systray.service

%changelog

* Tue Jun 11 2024 Tim Lauridsen <timlau@fedoraproject.org> 5.0.0-2
- added updater service
- include all .desktop files

* Tue Jun 11 2024 Tim Lauridsen <timlau@fedoraproject.org> 5.0.0-1
- the 5.0.0 release

* Thu Apr 20 2023 Tim Lauridsen <timlau@fedoraproject.org> 4.99.4-1
- the 4.99.4 release

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

