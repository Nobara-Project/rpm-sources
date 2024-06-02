%bcond cloudproviders %{undefined rhel}

%global glib2_version 2.79.0
%global gnome_autoar_version 0.4.4
%global gtk4_version 4.13.6
%global libadwaita_version 1.4~alpha

%global tarball_version %%(echo %{version} | tr '~' '.')

Name:           nautilus
Version:        46.2
Release:        1%{?dist}
Summary:        File manager for GNOME

# Sources are GPL-3.0-or-later and Appdata is CC0-1.0.
License:        GPL-3.0-or-later AND CC0-1.0
URL:            https://apps.gnome.org/Nautilus/
Source0:        https://download.gnome.org/sources/%{name}/46/%{name}-%{tarball_version}.tar.xz
Patch1:		nautilus-restore-typeahead.patch
Patch2:		0001-patch-re-add-breadcrumb-address-bar-toggle.patch

BuildRequires:  desktop-file-utils
BuildRequires:  gcc
BuildRequires:  gettext
BuildRequires:  meson
BuildRequires:  pkgconfig(gexiv2)
BuildRequires:  pkgconfig(gi-docgen)
BuildRequires:  pkgconfig(glib-2.0) >= %{glib2_version}
BuildRequires:  pkgconfig(gnome-autoar-0) >= %{gnome_autoar_version}
BuildRequires:  pkgconfig(gnome-desktop-4)
BuildRequires:  pkgconfig(gobject-introspection-1.0)
BuildRequires:  pkgconfig(gsettings-desktop-schemas)
BuildRequires:  pkgconfig(gstreamer-pbutils-1.0)
BuildRequires:  pkgconfig(gstreamer-tag-1.0)
BuildRequires:  pkgconfig(gtk4) >= %{gtk4_version}
BuildRequires:  pkgconfig(libadwaita-1) >= %{libadwaita_version}
%if %{with cloudproviders}
BuildRequires:  pkgconfig(cloudproviders)
%endif
BuildRequires:  pkgconfig(libportal)
BuildRequires:  pkgconfig(libportal-gtk4)
BuildRequires:  pkgconfig(libseccomp)
BuildRequires:  pkgconfig(libselinux)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(tracker-sparql-3.0)
BuildRequires:  pkgconfig(x11)
BuildRequires:  /usr/bin/appstream-util

Requires:       glib2%{_isa} >= %{glib2_version}
Requires:       gnome-autoar%{_isa} >= %{gnome_autoar_version}
Requires:       gsettings-desktop-schemas%{_isa}
Requires:       gtk4%{_isa} >= %{gtk4_version}
Requires:       gvfs%{_isa}
Requires:       libadwaita%{_isa} >= %{libadwaita_version}
# the main binary links against libnautilus-extension.so
# don't depend on soname, rather on exact version
Requires:       %{name}-extensions%{_isa} = %{version}-%{release}
# For the org.freedesktop.Tracker3.Miner.Files GSettings schema.
Requires:       tracker-miners

Provides:       bundled(libgd)

%description
Nautilus is the file manager and graphical shell for the GNOME desktop
that makes it easy to manage your files and the rest of your system.
It allows to browse directories on local and remote filesystems, preview
files and launch applications associated with them.
It is also responsible for handling the icons on the GNOME desktop.

%package extensions
Summary:        Nautilus extensions library
License:        LGPL-2.1-or-later

%description extensions
This package provides the libraries used by nautilus extensions.

%package devel
Summary:        Support for developing nautilus extensions
License:        LGPL-2.1-or-later
Requires:       %{name}%{_isa} = %{version}-%{release}
Requires:       %{name}-extensions%{_isa} = %{version}-%{release}

%description devel
This package provides libraries and header files needed
for developing nautilus extensions.

%prep
%autosetup -p1 -n %{name}-%{tarball_version}

# Remove -Werror from compiler flags
sed -i '/-Werror/d' meson.build

%build
%meson \
  -Ddocs=true \
  -Dextensions=true \
  -Dintrospection=true \
  -Dselinux=true \
  -Dcloudproviders=%{?with_cloudproviders:true}%{?!with_cloudproviders:false}
  %{nil}
%meson_build

%install
%meson_install

%find_lang %{name}

%check
appstream-util validate-relax --nonet $RPM_BUILD_ROOT%{_metainfodir}/org.gnome.Nautilus.metainfo.xml
desktop-file-validate $RPM_BUILD_ROOT%{_datadir}/applications/*.desktop

%files  -f %{name}.lang
%doc NEWS README.md
%license LICENSE
%{_datadir}/applications/*
%{_bindir}/*
%{_datadir}/dbus-1/services/org.freedesktop.FileManager1.service
%{_datadir}/dbus-1/services/org.gnome.Nautilus.service
%{_datadir}/dbus-1/services/org.gnome.Nautilus.Tracker3.Miner.Extract.service
%{_datadir}/dbus-1/services/org.gnome.Nautilus.Tracker3.Miner.Files.service
%dir %{_datadir}/gnome-shell
%dir %{_datadir}/gnome-shell/search-providers
%{_datadir}/gnome-shell/search-providers/org.gnome.Nautilus.search-provider.ini
%{_datadir}/icons/hicolor/scalable/apps/org.gnome.Nautilus.svg
%{_datadir}/icons/hicolor/symbolic/apps/org.gnome.Nautilus-symbolic.svg
%{_mandir}/man1/nautilus.1*
%{_mandir}/man1/nautilus-autorun-software.1*
%{_datadir}/glib-2.0/schemas/org.gnome.nautilus.gschema.xml
%{_datadir}/nautilus/
%{_datadir}/tracker3/domain-ontologies/org.gnome.Nautilus.domain.rule
%{_libdir}/nautilus/extensions-4/libnautilus-image-properties.so
%{_libdir}/nautilus/extensions-4/libtotem-properties-page.so
%{_metainfodir}/org.gnome.Nautilus.metainfo.xml

%files extensions
%license libnautilus-extension/LICENSE
%{_libdir}/libnautilus-extension.so.4*
%{_libdir}/girepository-1.0/Nautilus-4.0.typelib
%dir %{_libdir}/nautilus
%dir %{_libdir}/nautilus/extensions-4

%files devel
%{_includedir}/nautilus
%{_libdir}/pkgconfig/libnautilus-extension-4.pc
%{_libdir}/libnautilus-extension.so
%{_datadir}/gir-1.0/Nautilus-4.0.gir
%doc %{_datadir}/doc/nautilus/

%changelog
* Tue May 28 2024 David King <amigadave@amigadave.com> - 46.2-1
- Update to 46.2

* Sun Apr 21 2024 David King <amigadave@amigadave.com> - 46.1-1
- Update to 46.1

* Sun Apr 14 2024 Adam Williamson <awilliam@redhat.com> - 46.0-2
- Backport MR #1488 to fix crash when compressing files and folders

* Tue Mar 19 2024 David King <amigadave@amigadave.com> - 46.0-1
- Update to 46.0

* Fri Mar 08 2024 David King <amigadave@amigadave.com> - 46~rc-1
- Update to 46.rc

* Wed Feb 14 2024 David King <amigadave@amigadave.com> - 46~beta-1
- Update to 46.beta

* Mon Jan 29 2024 David King <amigadave@amigadave.com> - 46~alpha.1-1
- Update to 46.alpha.1

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 46~alpha.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 David King <amigadave@amigadave.com> - 46~alpha.0-1
- Update to 46.alpha.0

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 45.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Dec 06 2023 Kalev Lember <klember@redhat.com> - 45.2.1-1
- Update to 45.2.1

* Sun Oct 22 2023 Kalev Lember <klember@redhat.com> - 45.1-1
- Update to 45.1

* Wed Sep 20 2023 Kalev Lember <klember@redhat.com> - 45.0-1
- Update to 45.0

* Tue Sep 05 2023 Kalev Lember <klember@redhat.com> - 45~rc-1
- Update to 45.rc

* Sat Aug 26 2023 Kalev Lember <klember@redhat.com> - 45~beta2-1
- Update to 45.beta2

* Fri Aug 11 2023 Kalev Lember <klember@redhat.com> - 45~beta-1
- Update to 45.beta

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 45~alpha-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jul 03 2023 Kalev Lember <klember@redhat.com> - 45~alpha-1
- Update to 45.alpha

* Mon Jun 26 2023 Ondrej Holy <oholy@redhat.com> - 44.2.1-2
- Disable cloudproviders in RHEL

* Mon Jun 05 2023 Kalev Lember <klember@redhat.com> - 44.2.1-1
- Update to 44.2.1

* Wed May 31 2023 Kalev Lember <klember@redhat.com> - 44.2-1
- Update to 44.2

* Tue Apr 25 2023 David King <amigadave@amigadave.com> - 44.1-2
- Raise requirement on gtk4

* Mon Apr 24 2023 David King <amigadave@amigadave.com> - 44.1-1
- Update to 44.1

* Fri Mar 17 2023 David King <amigadave@amigadave.com> - 44.0-1
- Update to 44.0 (#2159040)

* Thu Mar 16 2023 Adam Williamson <awilliam@redhat.com> - 44~rc-2
- Backport MR #1151 to fix drag-and-drop (#2176766)

* Sun Mar 05 2023 David King <amigadave@amigadave.com> - 44~rc-1
- Update to 44.rc

* Wed Feb 15 2023 David King <amigadave@amigadave.com> - 44~beta-1
- Update to 44.beta

* Fri Feb 10 2023 David King <amigadave@amigadave.com> - 44~alpha-2
- Update tracker-miners dependency

* Mon Feb 06 2023 David King <amigadave@amigadave.com> - 44~alpha-1
- Update to 44.alpha

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 43.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sun Jan 08 2023 David King <amigadave@amigadave.com> - 43.2-1
- Update to 43.2

* Tue Dec 06 2022 David King <amigadave@amigadave.com> - 43.1-1
- Update to 43.1

* Fri Sep 30 2022 Adam Williamson <awilliam@redhat.com> - 43.0-2
- Backport MR #977 to revert broken high-res thumbnails (#2127618)

* Tue Sep 20 2022 Kalev Lember <klember@redhat.com> - 43.0-1
- Update to 43.0

* Tue Sep 06 2022 Kalev Lember <klember@redhat.com> - 43~rc-1
- Update to 43.rc

* Wed Aug 17 2022 Kalev Lember <klember@redhat.com> - 43~beta.1-2
- Drop temporary libnautilus-extension ABI compat

* Tue Aug 09 2022 Kalev Lember <klember@redhat.com> - 43~beta.1-1
- Update to 43.beta.1

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 43~alpha-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jul 18 2022 Kalev Lember <klember@redhat.com> - 43~alpha-3
- Rebuild

* Mon Jul 18 2022 Kalev Lember <klember@redhat.com> - 43~alpha-2
- Install previous libnautilus-extension soname for temporary ABI compat

* Mon Jul 18 2022 Kalev Lember <klember@redhat.com> - 43~alpha-1
- Update to 43.alpha
- Always build with libportal support
- Switch to gtk4

* Sun May 29 2022 David King <amigadave@amigadave.com> - 42.2-1
- Update to 42.2

* Sun Apr 24 2022 David King <amigadave@amigadave.com> - 42.1-1
- Update to 42.1.1

* Sat Mar 19 2022 David King <amigadave@amigadave.com> - 42.0-1
- Update to 42.0

* Mon Mar 07 2022 David King <amigadave@amigadave.com> - 42~rc-1
- Update to 42.rc

* Mon Feb 28 2022 David King <amigadave@amigadave.com> - 42~beta-2
- Fix thumbnail drop shadow refresh bug

* Sun Feb 13 2022 David King <amigadave@amigadave.com> - 42~beta-1
- Update to 42.beta

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 42~alpha-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jan 12 2022 David King <amigadave@amigadave.com> - 42~alpha-2
- Rebuild against gnome-desktop4

* Sun Jan 09 2022 David King <amigadave@amigadave.com> - 42~alpha-1
- Update to 42.alpha

* Tue Dec 07 2021 Ondrej Holy <oholy@redhat.com> - 41.1-2
- Fix cropped popover for compress formats on X11

* Mon Nov 01 2021 Kalev Lember <klember@redhat.com> - 41.1-1
- Update to 41.1

* Fri Sep 17 2021 Kalev Lember <klember@redhat.com> - 41.0-1
- Update to 41.0

* Wed Sep 08 2021 Kalev Lember <klember@redhat.com> - 41~rc-1
- Update to 41.rc

* Mon Aug 16 2021 Kalev Lember <klember@redhat.com> - 41~beta-1
- Update to 41.beta

* Tue Aug 03 2021 Kalev Lember <klember@redhat.com> - 41~alpha-1
- Update to 41.alpha

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 40.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu May 20 2021 Ondrej Holy <oholy@redhat.com> - 40.1-3
- Add missing bundled(libgd) provides statement

* Thu May 06 2021 Kalev Lember <klember@redhat.com> - 40.1-2
- Backport upstream fix to keep working directory when executing programs

* Wed May 05 2021 Kalev Lember <klember@redhat.com> - 40.1-1
- Update to 40.1

* Mon Mar 22 2021 Kalev Lember <klember@redhat.com> - 40.0-1
- Update to 40.0

* Mon Mar 15 2021 Kalev Lember <klember@redhat.com> - 40~rc-1
- Update to 40.rc

* Thu Feb 18 2021 Kalev Lember <klember@redhat.com> - 40~beta-2
- Only require libportal for Flatpak builds

* Thu Feb 18 2021 Kalev Lember <klember@redhat.com> - 40~beta-1
- Update to 40.beta

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.38.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Nov 25 2020 Kalev Lember <klember@redhat.com> - 3.38.2-1
- Update to 3.38.2

* Mon Oct  5 2020 Kalev Lember <klember@redhat.com> - 3.38.1-1
- Update to 3.38.1

* Fri Sep 11 2020 Kalev Lember <klember@redhat.com> - 3.38.0-1
- Update to 3.38.0

* Tue Sep 08 2020 Kalev Lember <klember@redhat.com> - 3.37.92-1
- Update to 3.37.92
- Switch to tracker3
- Tighten nautilus-extensions soname glob
- Fix directory ownership for /usr/lib/nautilus/extensions-3.0 directory

* Fri Aug 21 2020 Kalev Lember <klember@redhat.com> - 3.37.91-1
- Update to 3.37.91

* Tue Aug 18 2020 Kalev Lember <klember@redhat.com> - 3.37.90-1
- Update to 3.37.90

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.37.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Mar 27 2020 Kalev Lember <klember@redhat.com> - 3.37.1-1
- Update to 3.37.1

* Fri Mar 06 2020 Kalev Lember <klember@redhat.com> - 3.36.0-1
- Update to 3.36.0

* Mon Mar 02 2020 Kalev Lember <klember@redhat.com> - 3.35.92-1
- Update to 3.35.92

* Mon Feb 17 2020 Kalev Lember <klember@redhat.com> - 3.35.91.1-1
- Update to 3.35.91.1

* Thu Feb 06 2020 Bastien Nocera <bnocera@redhat.com> - 3.35.90-2
+ nautilus-3.35.90-2
- Fix launching multiple files at once

* Sun Feb 02 2020 Kalev Lember <klember@redhat.com> - 3.35.90-1
- Update to 3.35.90

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.35.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jan 16 2020 Kalev Lember <klember@redhat.com> - 3.35.2-2
- Rebuilt for libgnome-desktop soname bump

* Mon Dec 02 2019 Kalev Lember <klember@redhat.com> - 3.35.2-1
- Update to 3.35.2

* Wed Nov 27 2019 Kalev Lember <klember@redhat.com> - 3.34.2-1
- Update to 3.34.2

* Mon Oct 07 2019 Kalev Lember <klember@redhat.com> - 3.34.1-1
- Update to 3.34.1

* Tue Sep 10 2019 Kalev Lember <klember@redhat.com> - 3.34.0-1
- Update to 3.34.0

* Tue Aug 20 2019 Kalev Lember <klember@redhat.com> - 3.33.90-1
- Update to 3.33.90

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.32.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun May 12 2019 Ernestas Kulik <ekulik@redhat.com> - 3.32.1-2
- Add tracker-miners dependency (rhbz#1695400)

* Mon May 06 2019 Kalev Lember <klember@redhat.com> - 3.32.1-1
- Update to 3.32.1

* Wed Mar 13 2019 Kalev Lember <klember@redhat.com> - 3.32.0-1
- Update to 3.32.0
- Move libtotem-properties-page.so extension here from totem-nautilus

* Wed Feb 06 2019 Kalev Lember <klember@redhat.com> - 3.31.90-1
- Update to 3.31.90

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.30.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Dec 16 2018 Phil Wyett <philwyett@kathenas.org> - 3.30.5-1
- Update to 3.30.5

* Wed Nov 21 2018 Kalev Lember <klember@redhat.com> - 3.30.4-1
- Update to 3.30.4

* Wed Oct 31 2018 Kalev Lember <klember@redhat.com> - 3.30.3-1
- Update to 3.30.3

* Fri Oct 12 2018 Kalev Lember <klember@redhat.com> - 3.30.2-1
- Update to 3.30.2

* Wed Oct 03 2018 Kalev Lember <klember@redhat.com> - 3.30.1-1
- Update to 3.30.1

* Fri Sep 07 2018 Kalev Lember <klember@redhat.com> - 3.30.0-2
- Rebuilt against fixed atk (#1626575)

* Thu Sep 06 2018 Kalev Lember <klember@redhat.com> - 3.30.0-1
- Update to 3.30.0

* Mon Aug 13 2018 Kalev Lember <klember@redhat.com> - 3.29.90.1-1
- Update to 3.29.90.1

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.28.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Apr 09 2018 Kalev Lember <klember@redhat.com> - 3.28.1-1
- Update to 3.28.1
- Fix /usr/share/gnome-shell directory ownership

* Sat Mar 31 2018 Michael Catanzaro <mcatanzaro@gnome.org> - 3.28.0.1-2
- Build with -Dselinux=true to turn it on explicitly, and remove downstream screenshots

* Thu Mar 15 2018 Kalev Lember <klember@redhat.com> - 3.28.0.1-1
- Update to 3.28.0.1

* Tue Mar 13 2018 Kalev Lember <klember@redhat.com> - 3.28.0-1
- Update to 3.28.0

* Mon Mar 05 2018 Kalev Lember <klember@redhat.com> - 3.27.92.1-1
- Update to 3.27.92.1
- Remove -Werror from compiler flags

* Tue Feb 13 2018 Björn Esser <besser82@fedoraproject.org> - 3.26.2-4
- Rebuild against newer gnome-desktop3 package

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.26.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.26.2-2
- Switch to %%ldconfig_scriptlets

* Tue Nov 21 2017 Kalev Lember <klember@redhat.com> - 3.26.2-1
- Update to 3.26.2

* Wed Nov 08 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.26.0-2
- Remove obsolete scriptlets
- Add BuildRequires: gcc

* Wed Sep 13 2017 Kalev Lember <klember@redhat.com> - 3.26.0-1
- Update to 3.26.0

* Tue Sep 05 2017 Kalev Lember <klember@redhat.com> - 3.25.92-1
- Update to 3.25.92

* Tue Aug 15 2017 Kalev Lember <klember@redhat.com> - 3.25.90-1
- Update to 3.25.90

* Tue Aug 01 2017 Kalev Lember <klember@redhat.com> - 3.25.1-1
- Update to 3.25.1
- Switch to the meson build system
- Reflect upstream license change to GPLv3+

* Thu Jul 27 2017 Debarshi Ray <rishi@fedoraproject.org> - 3.24.2.1-3
- Rebuild against tracker-2.0

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.24.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jul 18 2017 Kalev Lember <klember@redhat.com> - 3.24.2.1-1
- Update to 3.24.2.1

* Tue May 09 2017 Kalev Lember <klember@redhat.com> - 3.24.1-1
- Update to 3.24.1

* Tue Mar 21 2017 Kalev Lember <klember@redhat.com> - 3.24.0-1
- Update to 3.24.0

* Fri Mar 17 2017 Kalev Lember <klember@redhat.com> - 3.23.92-1
- Update to 3.23.92

* Mon Mar 06 2017 Kalev Lember <klember@redhat.com> - 3.23.91-1
- Update to 3.23.91

* Wed Feb 15 2017 Richard Hughes <rhughes@redhat.com> - 3.23.90-1
- Update to 3.23.90

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.22.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 12 2016 David King <amigadave@amigadave.com> - 3.22.2-1
- Update to 3.22.2

* Fri Oct 14 2016 Kalev Lember <klember@redhat.com> - 3.22.1-1
- Update to 3.22.1

* Wed Sep 21 2016 Kalev Lember <klember@redhat.com> - 3.22.0-1
- Update to 3.22.0

* Fri Sep 16 2016 Kalev Lember <klember@redhat.com> - 3.21.92-1
- Update to 3.21.92

* Sat Sep 03 2016 Kalev Lember <klember@redhat.com> - 3.21.91.1-1
- Update to 3.21.91.1
- Filter private libgd from provides and requires
- Use upstream defaults for OnlyShowIn

* Tue Aug 30 2016 Kalev Lember <klember@redhat.com> - 3.20.3-1
- Update to 3.20.3
- Don't set group tags

* Mon Aug 01 2016 Kalev Lember <klember@redhat.com> - 3.20.2-1
- Update to 3.20.2

* Thu Jun 02 2016 Kalev Lember <klember@redhat.com> - 3.20.1-1
- Update to 3.20.1

* Wed Mar 23 2016 Kalev Lember <klember@redhat.com> - 3.20.0-1
- Update to 3.20.0

* Fri Mar 18 2016 Kalev Lember <klember@redhat.com> - 3.19.93-1
- Update to 3.19.93

* Mon Mar 14 2016 Richard Hughes <rhughes@redhat.com> - 3.19.91-1
- Update to 3.19.91

* Mon Feb 29 2016 Richard Hughes <rhughes@redhat.com> - 3.19.90-1
- Update to 3.19.90

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.19.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Dec 14 2015 Kalev Lember <klember@redhat.com> - 3.19.2-1
- Update to 3.19.2

* Wed Nov 18 2015 Kalev Lember <klember@redhat.com> - 3.18.2-2
- Bump gtk3 dep to 3.18.5 (#1283246)

* Fri Nov 13 2015 Kalev Lember <klember@redhat.com> - 3.18.2-1
- Update to 3.18.2

* Thu Oct 15 2015 Kalev Lember <klember@redhat.com> - 3.18.1-1
- Update to 3.18.1

* Tue Sep 22 2015 Kalev Lember <klember@redhat.com> - 3.18.0-1
- Update to 3.18.0
- Don't pull in all of nautilus for the -extensions subpackage
- Tighten a dep with the _isa macro
- Drop ancient obsoletes

* Fri Sep 04 2015 Kalev Lember <klember@redhat.com> - 3.17.91-1
- Update to 3.17.91

* Fri Aug 21 2015 Kalev Lember <klember@redhat.com> - 3.17.90-1
- Update to 3.17.90
- Use make_install macro

* Mon Jul 27 2015 David King <amigadave@amigadave.com> - 3.17.3-1
- Update to 3.17.3

* Tue Jul 21 2015 David King <amigadave@amigadave.com> - 3.17.2-3
- Bump for new gnome-desktop3

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.17.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri May 29 2015 David King <amigadave@amigadave.com> - 3.17.2-1
- Update to 3.17.2

* Wed May 13 2015 Kalev Lember <kalevlember@gmail.com> - 3.16.2-1
- Update to 3.16.2

* Mon May 04 2015 David King <amigadave@amigadave.com> - 3.16.1-2
- Add patch to fix misplaced style element

* Wed Apr 15 2015 Kalev Lember <kalevlember@gmail.com> - 3.16.1-1
- Update to 3.16.1

* Mon Mar 30 2015 Richard Hughes <rhughes@redhat.com> - 3.16.0-2
- Use better AppData screenshots

* Tue Mar 24 2015 Kalev Lember <kalevlember@gmail.com> - 3.16.0-1
- Update to 3.16.0

* Tue Mar 17 2015 Kalev Lember <kalevlember@gmail.com> - 3.15.92-1
- Update to 3.15.92

* Thu Mar 12 2015 David King <amigadave@amigadave.com> - 3.15.91-1
- Update to 3.15.91
- Validate AppData in check

* Tue Feb 17 2015 Richard Hughes <rhughes@redhat.com> - 3.15.90-1
- Update to 3.15.90

* Sun Jan 25 2015 David King <amigadave@amigadave.com> - 3.15.4-1
- Update to 3.15.4
- Use pkgconfig for BuildRequires
- Update man page globs in files section
- Use license macro for license texts

* Tue Nov 25 2014 Kalev Lember <kalevlember@gmail.com> - 3.14.2-1
- Update to 3.14.2

* Thu Nov 13 2014 Kalev Lember <kalevlember@gmail.com> - 3.14.1-1
- Update to 3.14.1

* Tue Sep 23 2014 Kalev Lember <kalevlember@gmail.com> - 3.14.0-2
- Drop redhat-menus dependency

* Tue Sep 23 2014 Kalev Lember <kalevlember@gmail.com> - 3.14.0-1
- Update to 3.14.0

* Tue Sep 16 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.92-1
- Update to 3.13.92

* Wed Sep 03 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.91-1
- Update to 3.13.91

* Thu Aug 21 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.90-1
- Update to 3.13.90

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.13.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Aug 12 2014 Rex Dieter <rdieter@fedoraproject.org> 3.13.2-6
- update mime scriptlet

* Sat Aug 02 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.2-5
- Fix appdata file name

* Mon Jul 28 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.2-4
- Rebuilt once more for tracker

* Mon Jul 28 2014 Peter Robinson <pbrobinson@fedoraproject.org> 3.13.2-3
- rebuild (tracker)

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.2-2
- Rebuilt for gobject-introspection 1.41.4

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.2-1
- Update to 3.13.2

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.13.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 01 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.1-1
- Update to 3.13.1

* Sat Apr 05 2014 Kalev Lember <kalevlember@gmail.com> - 3.12.0-2
- Update dep versions

* Tue Mar 25 2014 Kalev Lember <kalevlember@gmail.com> - 3.12.0-1
- Update to 3.12.0

* Tue Mar 18 2014 Richard Hughes <rhughes@redhat.com> - 3.11.92-1
- Update to 3.11.92

* Wed Feb 19 2014 Richard Hughes <rhughes@redhat.com> - 3.11.90-2
- Rebuilt for gnome-desktop soname bump

* Tue Feb 18 2014 Richard Hughes <rhughes@redhat.com> - 3.11.90-1
- Update to 3.11.90

* Thu Dec 19 2013 Debarshi Ray <rishi@fedoraproject.org> - 3.11.3-1
- Update to 3.11.3

* Tue Nov 19 2013 Richard Hughes <rhughes@redhat.com> - 3.11.2-1
- Update to 3.11.2

* Mon Nov 04 2013 Kalev Lember <kalevlember@gmail.com> - 3.10.1-1
- Update to 3.10.1

* Wed Sep 25 2013 Kalev Lember <kalevlember@gmail.com> - 3.10.0-1
- Update to 3.10.0

* Wed Sep 18 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.92-1
- Update to 3.9.92

* Wed Sep 04 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.91-1
- Update to 3.9.91

* Thu Aug 22 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.90-1
- Update to 3.9.90

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.9.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun 21 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.3-1
- Update to 3.9.3
- Use arch-specific deps

* Sun Jun 16 2013 Matthias Clasen <mclasen@redhat.com> - 3.8.2-1
- Update to 3.8.2

* Tue Apr 16 2013 Kalev Lember <kalevlember@gmail.com> - 3.8.1-1
- Update to 3.8.1

* Tue Mar 26 2013 Kalev Lember <kalevlember@gmail.com> - 3.8.0-1
- Update to 3.8.0

* Wed Mar 20 2013 Richard Hughes <rhughes@redhat.com> - 3.7.92-1
- Update to 3.7.92

* Thu Mar  7 2013 Matthias Clasen <mclasen@redhat.com> - 3.7.91-1
- Update to 3.7.91

* Wed Feb 20 2013 Kalev Lember <kalevlember@gmail.com> - 3.7.90-2
- Rebuilt for libgnome-desktop soname bump

* Tue Feb 19 2013 Richard Hughes <rhughes@redhat.com> - 3.7.90-1
- Update to 3.7.90

* Fri Feb  8 2013 Tomas Bzatek <tbzatek@redhat.com> - 3.7.5-2
- Disable smp build to fix intltool issues

* Thu Feb 07 2013 Richard Hughes <rhughes@redhat.com> - 3.7.5-1
- Update to 3.7.5

* Sun Jan 27 2013 Kalev Lember <kalevlember@gmail.com> - 3.7.4-2
- Rebuilt for tracker 0.16 ABI

* Wed Jan 16 2013 Richard Hughes <hughsient@gmail.com> - 3.7.4-1
- Update to 3.7.4

* Fri Dec 21 2012 Kalev Lember <kalevlember@gmail.com> - 3.7.3-1
- Update to 3.7.3

* Thu Dec  6 2012 Tomas Bzatek <tbzatek@redhat.com> - 3.7.2-2
- nautilus-devel should require nautilus-extensions

* Tue Nov 20 2012 Richard Hughes <hughsient@gmail.com> - 3.7.2-1
- Update to 3.7.2

* Fri Nov 09 2012 Kalev Lember <kalevlember@gmail.com> - 3.7.1-1
- Update to 3.7.1
- Own the gtk-doc directories

* Mon Oct 15 2012 Cosimo Cecchi <cosimoc@redhat.com> - 3.6.1-1
- Update to 3.6.1

* Tue Sep 25 2012 Cosimo Cecchi <cosimoc@redhat.com> - 3.6.0-1
- Update to 3.6.0

* Tue Sep 18 2012 Cosimo Cecchi <cosimoc@redhat.com> - 3.5.92-1
- Update to 3.5.92

* Tue Sep 04 2012 Cosimo Cecchi <cosimoc@redhat.com> - 3.5.91-1
- Update to 3.5.91

* Tue Aug 21 2012 Cosimo Cecchi <cosimoc@redhat.com> - 3.5.90-1
- Update to 3.5.90

* Fri Aug 10 2012 Cosimo Cecchi <cosimoc@redhat.com> - 3.5.5-1
- Update to 3.5.5

* Fri Jul 27 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 17 2012 Cosimo Cecchi <cosimoc@redhat.com> - 3.5.4-2
- Enable tracker support

* Tue Jul 17 2012 Richard Hughes <hughsient@gmail.com> - 3.5.4-1
- Update to 3.5.4

* Sat Jul 14 2012 Ville Skyttä <ville.skytta@iki.fi> - 3.5.3-2
- Move ldconfig calls from main package to -extensions.

* Tue Jun 26 2012 Richard Hughes <hughsient@gmail.com> - 3.5.3-1
- Update to 3.5.3

* Thu Jun 07 2012 Richard Hughes <hughsient@gmail.com> - 3.5.2-1
- Update to 3.5.2

* Sat May 05 2012 Kalev Lember <kalevlember@gmail.com> - 3.5.1-1
- Update to 3.5.1

* Tue Apr 24 2012 Kalev Lember <kalevlember@gmail.com> - 3.4.1-2
- Silence rpm scriptlet output

* Mon Apr 16 2012 Richard Hughes <hughsient@gmail.com> - 3.4.1-1
- Update to 3.4.1

* Mon Mar 26 2012 Cosimo Cecchi <cosimoc@redhat.com> - 3.4.0-1
- Update to 3.4.0

* Tue Mar 20 2012 Cosimo Cecchi <cosimoc@redhat.com> - 3.3.92-1
- Update to 3.3.92

* Tue Mar 06 2012 Cosimo Cecchi <cosimoc@redhat.com> - 3.3.91-1
- Update to 3.3.91

* Sun Feb 26 2012 Matthias Clasen <mclasen@redhat.com> - 3.3.90-1
- Update to 3.3.90

* Tue Feb  7 2012 Cosimo Cecchi <cosimoc@redhat.com> - 3.3.5-1
- Update to 3.3.5

* Tue Jan 17 2012 Matthias Clasen <mclasen@redhat.com> - 3.3.4-1
- Update to 3.3.4

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 20 2011 Matthias Clasen <mclasen@redhat.com> - 3.3.3-1
- Update to 3.3.3

* Wed Nov  2 2011 Matthias Clasen <mclasen@redhat.com> - 3.3.1.1-1
- Update to 3.3.1.1

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.1-2
- Rebuilt for glibc bug#747377

* Tue Oct 18 2011 Cosimo Cecchi <cosimoc@redhat.com> - 3.2.1-1
- Update to 3.2.1

* Tue Sep 27 2011 Cosimo Cecchi <cosimoc@redhat.com> - 3.2.0-1
- Update to 3.2.0

* Mon Sep 19 2011 Cosimo Cecchi <cosimoc@redhat.com> - 3.1.92-1
- Update to 3.1.92

* Wed Aug 31 2011 Matthias Clasen <mclasen@redhat.com> 3.1.90-1
- Update to 3.1.90

* Mon Jul 25 2011 Matthias Clasen <mclasen@redhat.com> 3.1.4-1
- Update to 3.1.4

* Mon Jul 04 2011 Bastien Nocera <bnocera@redhat.com> 3.1.3-1
- Update to 3.1.3

* Tue Jun 14 2011 Cosimo Cecchi <cosimoc@redhat.com> - 3.1.2-1
- Update to 3.1.2

* Wed May 11 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.1-1
- Update to 3.1.1

* Mon Apr 25 2011 Matthias Clasen <mclasen@redhat.com> - 3.0.1-1
- Update to 3.0.1

* Mon Apr 04 2011 Cosimo Cecchi <cosimoc@redhat.com> - 3.0.0-1
- Update to 3.0.0

* Wed Mar 30 2011 Cosimo Cecchi <cosimoc@redhat.com> - 2.91.94-1
- Update to 2.91.94

* Sun Mar 27 2011 Colin Walters <walters@verbum.org> - 2.91.93-2
- Drop --vendor from nautilus.desktop
  Vendor prefixes are pointless, and in this case breaks upstream
  components trying to reference each other via .desktop file, such
  as GNOME Shell having nautilus.desktop in its default favorite
  list.

* Fri Mar 25 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.93-1
- Update to 2.91.93

* Mon Mar 21 2011 Cosimo Cecchi <cosimoc@redhat.com> - 2.91.92-1
- Update to 2.91.92

* Mon Mar 07 2011 Cosimo Cecchi <cosimoc@redhat.com> 2.91.91-1
- Update to 2.91.91

* Tue Feb 22 2011 Cosimo Cecchi <cosimoc@redhat.com> 2.91.90.1-1
- Update to 2.91.90.1

* Mon Feb 21 2011 Cosimo Cecchi <cosimoc@redhat.com> 2.91.90-1
- Update to 2.91.90

* Thu Feb 10 2011 Matthias Clasen <mclasne@redhat.com> 2.91.9-4
- Rebuild against newer gtk

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.91.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Feb  7 2011 Cosimo Cecchi <cosimoc@redhat.com> - 2.91.9-2
- Add a patch from upstream for missing bookmark names

* Fri Feb  4 2011 Cosimo Cecchi <cosimoc@redhat.com> - 2.91.9-1
- Update to 2.91.9

* Wed Feb  2 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.8-4
- Rebuild against new gtk

* Tue Feb  1 2011 Tomas Bzatek <tbzatek@redhat.com> - 2.91.8-3
- Remove last traces of gconf (#674359)

* Mon Jan 31 2011 Cosimo Cecchi <cosimoc@redhat.com> - 2.91.8-2
- Update selinux patch

* Mon Jan 31 2011 Cosimo Cecchi <cosimoc@redhat.com> - 2.91.8-1
- Update to 2.91.8

* Wed Jan 12 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.7-2
- Drop explicit gnome-desktop dependency
- Drop some no-longer-required tweaks

* Tue Jan 11 2011 Cosimo Cecchi <cosimoc@redhat.com> - 2.91.7-1
- Update to 2.91.7

* Fri Jan  7 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.6-1
- Update to 2.91.6

* Fri Dec  3 2010 Matthias Clasen <mclasen@redhat.com> - 2.91.3-2
- Rebuild against new gtk

* Mon Nov 29 2010 Cosimo Cecchi <cosimoc@redhat.com> - 2.91.3-1
- Update to 2.91.3
- Drop unnecessary patches

* Wed Nov 10 2010 Tomas Bzatek <tbzatek@redhat.com> - 2.91.2-1
- Update to 2.91.2

* Mon Nov  1 2010 Matthias Clasen <mclasen@redhat.com> - 2.91.1-1
- Update to 2.91.1

* Wed Oct  6 2010 Matthias Clasen <mclasen@redhat.com> - 2.91.0-1
- Update to 2.91.0

* Wed Sep 29 2010 jkeating - 2.90.1-6.gitf3bbee7
- Rebuilt for gcc bug 634757

* Sat Sep 25 2010 Owen Taylor <otaylor@redhat.com> - 2.90.1-5.gitf3bbee7
- Bump and rebuild for gtk3 ABI changes

* Tue Sep 21 2010 Matthias Clasen <mclasen@redhat.com> - 2.90.1-4.gitf3bbee7
- git snapshot
- Rebuild against newer gobject-introspection

* Mon Aug 30 2010 Tomas Bzatek <tbzatek@redhat.com> - 2.90.1-2
- Require gsettings-desktop-schemas (#628273)

* Tue Aug 24 2010 Matthias Clasen <mclasen@redhat.com> - 2.90.1-1
- Update to 2.31.91

* Wed Aug 18 2010 Tomas Bzatek <tbzatek@redhat.com> - 2.31.90-1
- Update to 2.31.90

* Thu Aug 12 2010 Tomas Bzatek <tbzatek@redhat.com> - 2.31.6-1
- Update to 2.31.6

* Fri Aug  6 2010 Tomas Bzatek <tbzatek@redhat.com> - 2.31.5-3.really.2.30.1
- Revert back (temporarily) to 2.30.1 and mask it as 2.31.5 due to recent gnome3 changes

* Thu Jul 15 2010 Colin Walters <walters@verbum.org> - 2.31.5-2
- Rebuild with new gobject-introspection

* Mon Jul 12 2010 Matthias Clasen <mclasen@redhat.com> 2.31.5-1
- Update to 2.31.5

* Mon Jun 28 2010 Matthias Clasen <mclasen@redhat.com> 2.31.4-1
- Update to 2.31.4

* Wed Jun 23 2010 Bastien Nocera <bnocera@redhat.com> 2.31.3-4.20100618git
- Fix libnautilus-extensions pkg-config files

* Wed Jun 23 2010 Matthias Clasen <mclasen@redhat.com> - 2.31.3-3.20100618git
- Rebuild to get rid of mixed gtk deps

* Fri Jun 18 2010 Matthias Clasen <mclasen@redhat.com> - 2.31.3-2.20100618git
- git snapshot that builds against GLib 2.25.9 and GTK+ 2.90.3

* Tue Jun  8 2010 Matthias Clasen <mclasen@redhat.com> - 2.31.3-1
- Update to 2.31.3

* Mon May 24 2010 Tomas Bzatek <tbzatek@redhat.com> - 2.31.2-1
- Update to 2.31.2

* Tue May  4 2010 Tomas Bzatek <tbzatek@redhat.com> - 2.31.1-1
- Update to 2.31.1

* Tue May  4 2010 Tomas Bzatek <tbzatek@redhat.com> - 2.30.1-3
- Remove .desktop entry in applications > system tools (#583790)

* Mon Apr 26 2010 Tomas Bzatek <tbzatek@redhat.com> - 2.30.1-2
- Do not show Unmount when showing Eject/Safe removal

* Mon Apr 26 2010 Tomas Bzatek <tbzatek@redhat.com> - 2.30.1-1
- Update to 2.30.1

* Sat Apr 24 2010 Matthias Clasen <mclasen@redhat.com> - 2.30.0-3
- Also obsolete eel2-devel (#583722)

* Tue Apr 13 2010 Seth Vidal <skvidal at fedoraproject.org> - 2.30.0-2
- fix obsoletes/provides for eel2 to not include pkg name in ver/rel 

* Mon Mar 29 2010 Tomas Bzatek <tbzatek@redhat.com> - 2.30.0-1
- Update to 2.30.0

* Mon Mar 15 2010 Tomas Bzatek <tbzatek@redhat.com> - 2.29.92.1-1
- Update to 2.29.92.1
- Fix eel2 obsoletion

* Mon Mar  8 2010 Tomas Bzatek <tbzatek@redhat.com> - 2.29.92-1
- Update to 2.29.92

* Mon Feb 22 2010 Matthias Clasen <mclasen@redhat.com> - 2.29.91-1
- Update to 2.29.91

* Wed Feb 17 2010 Tomas Bzatek <tbzatek@redhat.com> - 2.29.90-2
- Explicitly require exact nautilus-extensions package (#565802)

* Tue Feb  9 2010 Tomas Bzatek <tbzatek@redhat.com> - 2.29.90-1
- Update to 2.29.90

* Thu Jan 28 2010 Jesse Keating <jkeating@redhat.com> - 2.29.2-2
- Add a requires to keep nautilus-extensions updated if nautilus gets updated

* Mon Jan 25 2010 Tomas Bzatek <tbzatek@redhat.com> - 2.29.2-1
- Update to 2.29.2

* Sun Jan 17 2010 Matthias Clasen <mclasen@redhat.com> - 2.29.1-2
- Rebuild

* Fri Dec 18 2009 Tomas Bzatek <tbzatek@redhat.com> - 2.29.1-1
- Update to 2.29.1

* Thu Dec 10 2009 Jon McCann <jmccann@redhat.com> - 2.28.2-3
- Update the monitor changes patch (gnome #147808)

* Tue Dec  8 2009 Tomas Bzatek <tbzatek@redhat.com> - 2.28.2-2
- Fix some memory leaks

* Mon Nov 30 2009 Alexander Larsson <alexl@redhat.com> - 2.28.2-1
- Update to 2.28.2

* Wed Nov 18 2009 Tomas Bzatek <tbzatek@redhat.com> - 2.28.1-4
- Proper fix for crash in the infopanel (#531826)

* Mon Nov  9 2009 Matthias Clasen <mclasen@redhat.com> - 2.28.1-3
- Handle monitor changes when drawing the background (gnome #147808)

* Mon Nov  2 2009 Tomas Bzatek <tbzatek@redhat.com> - 2.28.1-2
- Don't crash in infopanel on invalid selection (#531826)

* Wed Oct 21 2009 Tomas Bzatek <tbzatek@redhat.com> - 2.28.1-1
- Update to 2.28.1

* Thu Sep 24 2009 Matthias Clasen <mclasen@redhat.com> - 2.28.0-3
- Avoid lingering menuitems (#518570)

* Wed Sep 23 2009 Ray Strode <rstrode@redhat.com> 2.28.0-2
- Fix crossfade

* Mon Sep 21 2009 Tomas Bzatek <tbzatek@redhat.com> - 2.28.0-1
- Update to 2.28.0

* Wed Sep  9 2009 Matthias Clasen <mclasen@redhat.com> - 2.27.92-2
- Fix desktop files to be valid

* Mon Sep  7 2009 Tomas Bzatek <tbzatek@redhat.com> - 2.27.92-1
- Update to 2.27.92

* Sun Sep  6 2009 Matthias Clasen <mclasen@redhat.com> - 2.27.91-3
- Fix uninhibiting when long-running operations are over

* Wed Aug 26 2009 Matthias Clasen <mclasen@redhat.com> - 2.27.91-2
- Make nautilus-file-management-properties not crash on start

* Mon Aug 24 2009 Matthias Clasen <mclasen@redhat.com> - 2.27.91-1
- Update to 2.27.91

* Wed Aug 12 2009 Matthias Clasen <mclasen@redhat.com> - 2.27.4-5
- Turn off autorun for x-content/software

* Mon Aug  3 2009 Matthias Clasen <mclasen@redhat.com> - 2.27.4-4
- Show icons for bookmarks and similar in menus

* Sun Aug  2 2009 Matthias Clasen <mclasen@redhat.com> - 2.27.4-3
- Drop desktop-backgrounds-basic dep that we've carried for 9 years
  without ever making use of it

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.27.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul 14 2009 Matthias Clasen <mclasen@redhat.com> - 2.27.4-1
- Update to 2.27.4

* Mon Jun 15 2009 Tomas Bzatek <tbzatek@redhat.com> - 2.27.2-1
- Update to 2.27.2

* Tue May  5 2009 Tomas Bzatek <tbzatek@redhat.com> - 2.27.1-1
- Update to 2.27.1

* Mon Apr 27 2009 Matthias Clasen <mclasen@redhat.com> - 2.26.2-3
- Don't drop schemas translations from po files anymore

* Thu Apr 16 2009 Alexander Larsson <alexl@redhat.com> - 2.26.2-2
- Fix whitespace on the right in icon view when zooming

* Mon Apr 13 2009 Alexander Larsson <alexl@redhat.com> - 2.26.2-1
- Update to 2.26.2

* Mon Apr  6 2009 Tomas Bzatek <tbzatek@redhat.com> - 2.26.1-2
- Fix dragging files via NFS moves instead of copy (#456515)

* Thu Apr  2 2009 Tomas Bzatek <tbzatek@redhat.com> - 2.26.1-1
- Update to 2.26.1

* Mon Mar 16 2009 Tomas Bzatek <tbzatek@redhat.com> - 2.26.0-1
- Update to 2.26.0

* Thu Mar 12 2009 Matthias Clasen <mclasen@redhat.com> - 2.25.93-2
- Avoid respawning in a loop when not showing the desktop (#485375)

* Wed Mar 11 2009 Tomas Bzatek <tbzatek@redhat.com> - 2.25.93-1
- Update to 2.25.93

* Mon Mar  2 2009 Tomas Bzatek <tbzatek@redhat.com> - 2.25.92-1
- Update to 2.25.92

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.25.91-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 19 2009 Tomas Bzatek <tbzatek@redhat.com> - 2.25.91-2
- Workaround for broken gcc optimization (#486088)

* Mon Feb 16 2009 Tomas Bzatek <tbzatek@redhat.com> - 2.25.91-1
- Update to 2.25.91

* Mon Feb  2 2009 Tomas Bzatek <tbzatek@redhat.com> - 2.25.4-1
- Update to 2.25.4

* Tue Jan 20 2009 Matthias Clasen <mclasen@redhat.com>- 2.25.3-2
- Reenable the translation size reduction

* Tue Jan 20 2009 Tomas Bzatek <tbzatek@redhat.com> - 2.25.3-1
- Update to 2.25.3

* Mon Jan 19 2009 Ray Strode <rstrode@redhat.com> - 2.25.2-7
- Update fade patch to work with updated gnome-desktop api
- Fix fade start pixmap

* Wed Jan  7 2009 Ray Strode <rstrode@redhat.com> - 2.25.2-6
- Don't crash when closing spatial window very quickly after
  opening it (gnome bug 552859)

* Thu Dec 18 2008 Matthias Clasen <mclasen@redhat.com> - 2.25.2-5
- Fix spec

* Thu Dec 18 2008 - Ray Strode <rstrode@redhat.com> - 2.25.2-4
- Add eel crossfade patch

* Wed Dec 17 2008 - Bastien Nocera <bnocera@redhat.com> - 2.25.2-3
- Rebuild for new libgnome-desktop

* Tue Dec 16 2008 Matthias Clasen <mclasen@redhat.com> - 2.25.2-2
- Drop the eel2 Obsoletes temporarily to give people some time
  to port away

* Tue Dec 16 2008 Matthias Clasen <mclasen@redhat.com> - 2.25.2-1
- Update to 2.25.2
- Clean up Requires
- Obsolete eel2
- Drop hard dependency on gvfs backends. 
  These are pulled in by comps, anyway

* Fri Dec  5 2008 Matthias Clasen <mclasen@redhat.com> - 2.25.1-5
- Obsolete gnome-volume-manager

* Fri Dec  5 2008 Tomas Bzatek <tbzatek@redhat.com> - 2.25.1-4
- Properly open new windows after long mount operation
- Fix callback connection to the GtkMountOperation dialog

* Thu Dec  4 2008 Tomas Bzatek <tbzatek@redhat.com> - 2.25.1-3
- Fix BuildRequires

* Thu Dec  4 2008 Tomas Bzatek <tbzatek@redhat.com> - 2.25.1-2
- Rediff the XDS patch

* Tue Dec  2 2008 Tomas Bzatek <tbzatek@redhat.com> - 2.25.1-1
- Update to 2.25.1

* Wed Nov 26 2008 Tomas Bzatek <tbzatek@redhat.com> - 2.24.2-1
- Update to 2.24.2

* Fri Nov 21 2008 Matthias Clasen  <mclasen@redhat.com> - 2.24.1-5
- Better URL
- Tweak %%description

* Thu Nov 13 2008 Matthias Clasen  <mclasen@redhat.com> - 2.24.1-4
- Rebuild

* Mon Oct 27 2008 Tomas Bzatek <tbzatek@redhat.com> - 2.24.1-3
- Updated XDS support in tree view patch (sync with gnomebz #171655)

* Fri Oct 24 2008 Alexander Larsson <alexl@redhat.com> - 2.24.1-2
- Manually check for fallback file icon since we're not
  always returning that from gio anymore (from upstream)

* Mon Oct 20 2008 Tomas Bzatek <tbzatek@redhat.com> - 2.24.1-1
- Update to 2.24.1

* Tue Oct 14 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.0-3
- Remove debug flags

* Thu Sep 25 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.0-2
- Save some space

* Sun Sep 21 2008 Matthias Clasen <mclasen@redhat.com> - 2.24.0-1
- Update to 2.24.0

* Sat Sep 20 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.92-3
- Plug some memory leaks

* Fri Sep 19 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.92-2
- Plug some memory leaks

* Mon Sep  8 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.92-1
- Update to 2.23.92

* Tue Sep 02 2008 Tomas Bzatek <tbzatek@redhat.com> - 2.23.91-1
- Update to 2.23.91

* Sat Aug 30 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.90-4
- Plug a few small memory leaks

* Thu Aug 28 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.90-3
- Pull in split-off gvfs backends

* Wed Aug 27 2008 - Bastien Nocera <bnocera@redhat.com> - 2.23.90-2
- Fix typo in the schemas file

* Sat Aug 23 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.90-1
- Update to 2.23.90

* Mon Aug  4 2008 Tomas Bzatek <tbzatek@redhat.com> - 2.23.6.1-1
- Update to 2.23.6.1
- Dropped upstreamed patches

* Mon Aug  4 2008 Tomas Bzatek <tbzatek@redhat.com> - 2.23.6-1
- Update to 2.23.6

* Sun Jul 27 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.5-3
- More icon name fixes

* Sun Jul 27 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.5-2
- Use standard icon names

* Tue Jul 22 2008 Tomas Bzatek <tbzatek@redhat.com> - 2.23.5.1-1
- Update to 2.23.5.1

* Tue Jul 22 2008 Matthias Clasen <mclasen@redhat.com> - 2.23.5-1
- Update to 2.23.5

* Tue Jun 17 2008 Tomas Bzatek <tbzatek@redhat.com> - 2.23.4-1
- Update to 2.23.4

* Thu Jun 12 2008 Tomas Bzatek <tbzatek@redhat.com> - 2.23.3-2
- Fix DnD segfaults (#450416, #450449)

* Wed Jun  4 2008 Tomas Bzatek <tbzatek@redhat.com> - 2.23.3-1
- Update to 2.23.3

* Fri May 30 2008 Tomas Bzatek <tbzatek@redhat.com> - 2.23.2-3
- Add DnD support to drop files onto archive files with help 
  of file-roller (gnomebz #377157)
- Add fix preventing crash on bad GFileInfos (gnomebz #519743)

* Fri May 16 2008 Tomas Bzatek <tbzatek@redhat.com> - 2.23.2-2
- Add treeview XDS drag&drop support (#446760)

* Tue May 13 2008 Tomas Bzatek <tbzatek@redhat.com> - 2.23.2-1
- Update to 2.23.2

* Fri May  2 2008 David Zeuthen <davidz@redhat.com> - 2.23.1-4
- Default to "Ask what to do" for all actions (#444639)

* Fri May  2 2008 Tomas Bzatek <tbzatek@redhat.com> - 2.23.1-3
- Mask file moving to nautilus-cd-burner window as copy operation (#443944)
- Don't allow recursive move/copy into itself (gnomebz #530720)

* Thu Apr 24 2008 Tomas Bzatek <tbzatek@redhat.com> - 2.23.1-2
- Add SELinux patch (gnomebz #529694)

* Wed Apr 23 2008 Tomas Bzatek <tbzatek@redhat.com> - 2.23.1-1
- Update to 2.23.1

* Thu Apr 17 2008 Matthias Clasen <mclasen@redhat.com> - 2.22.2-5
- Make "Open Folder" work as expected for media handling

* Thu Apr 17 2008 David Zeuthen <davidz@redhat.com> - 2.22.2-4
- Put X-Gnome-Vfs-System=gio into desktop files (See #442835)

* Wed Apr 16 2008 David Zeuthen <davidz@redhat.com> - 2.22.2-3
- Revert Fedora livecd mount (fix is in latest gvfs packages) and
  add a patch to avoid trying to autorun mounts that are mounted
  from outside Nautilus (#442189)

* Fri Apr 11 2008 Tomas Bzatek <tbzatek@redhat.com> - 2.22.2-2
- Hide Fedora livecd mount (#439166)

* Mon Apr  7 2008 Matthias Clasen <mclasen@redhat.com> - 2.22.2-1
- Update to 2.22.2

* Sun Apr  6 2008 Matthias Clasen <mclasen@redhat.com> - 2.22.1-6
- Backport a patch from upstream svn thats needed for file-roller

* Fri Apr  4 2008 Matthias Clasen <mclasen@redhat.com> - 2.22.1-5
- Fix beagle support some more

* Thu Apr  3 2008 Tomas Bzatek <tbzatek@redhat.com> - 2.22.1-4
- Fix SELinux attributes display issue (#439686)

* Wed Apr  2 2008 Matthias Clasen <mclasen@redhat.com> - 2.22.1-3
- Fix the build to include tracker and beagle support again

* Mon Mar 31 2008 Ray Strode <rstrode@redhat.com> - 2.22.1-2
- Over the releases we've accumulated default.png, default-wide.png default-5_4.png
  and default.jpg.  We haven't been able to drop them because it would leave some
  users with white backgrounds on upgrade.  This patch just falls back to the
  default image if the user's background doesn't exist.


* Fri Mar 28 2008 Tomas Bzatek <tbzatek@redhat.com> - 2.22.1-1
- Update to 2.22.1

* Thu Mar 13 2008 Tomas Bzatek <tbzatek@redhat.com> - 2.22.0-2
- Don't create application/x-ext-<extension> types for known mimetypes (patch from head)
- Fix a crash in the Properties dialog while changing owner (patch from head)

* Mon Mar 10 2008 Matthias Clasen <mclasen@redhat.com> - 2.22.0-1
- Update to 2.22.0

* Tue Feb 26 2008 Tomas Bzatek <tbzatek@redhat.com> - 2.21.92-2
- Change libbeagle .so name for libbeagle-0.3.0 in nautilus-2.21.1-dynamic-search-r2.patch (#434722)

* Tue Feb 26 2008 Tomas Bzatek <tbzatek@redhat.com> - 2.21.92-1
- Update to 2.21.92

* Tue Feb 12 2008 Matthias Clasen <mclasen@redhat.com> - 2.21.91-1
- Update to 2.21.91

* Tue Jan 29 2008 Matthias Clasen <mclasen@redhat.com> - 2.21.90-1
- Update to 2.21.90

* Mon Jan 21 2008 Matthias Clasen <mclasen@redhat.com> - 2.21.6-1
- Update to 2.21.6

* Mon Jan 14 2008 Matthias Clasen <mclasen@redhat.com> - 2.21.5-1
- Update to 2.21.5

* Tue Jan  8 2008 Matthias Clasen <mclasen@redhat.com> - 2.21.2-1
- Update to 2.21.2

* Sun Dec 23 2007 Matthias Clasen <mclasen@redhat.com> - 2.21.1-2
- Fix extensiondir

* Fri Dec 21 2007 Matthias Clasen <mclasen@redhat.com> - 2.21.1-1
- Upodate to 2.21.1

* Wed Dec 19 2007 - Bastien Nocera <bnocera@redhat.com> - 2.20.0-7
- Update audio preview patch to check for aliases (#381401)

* Tue Oct 30 2007 - Bastien Nocera <bnocera@redhat.com> - 2.20.0-6
- Fix audio preview command-line to use decodebin so playbin doesn't
  pop up a window for videos detected as audio

* Tue Oct 16 2007 - Bastien Nocera <bnocera@redhat.com> - 2.20.0-5
- Add patch from upstream to get audio preview working again
  (#332251)

* Wed Oct  3 2007 Matthias Clasen <mclasen@redhat.com> - 2.20.0-4
- Move /usr/lib/nautilus/extensions-1.0 to the extensions package

* Tue Oct  2 2007 Matthias Clasen <mclasen@redhat.com> - 2.20.0-3
- Fix a crash with small fonts (#242350)

* Tue Oct  2 2007 Alexander Larsson <alexl@redhat.com> - 2.20.0-1
- Backport fixes for async thumbnail loading from svn

* Fri Sep 28 2007 Ray Strode <rstrode@redhat.com> - 2.20.0-2
- drop redhat-artwork dep. Alex says we don't need it anymore 

* Tue Sep 18 2007 Matthias Clasen <mclasen@redhat.com> - 2.20.0-1
- Update to 2.20.0

* Mon Sep  3 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.91-1
- Update to 2.19.91

* Mon Aug 13 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.90-1
- Update to 2.19.90

* Fri Aug 10 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.6-3
- Bump gnome-vfs requirement (#251306)

* Fri Aug  3 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.6-2
- Update license field

* Mon Jul 30 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.6-1
- Update to 2.19.6

* Wed Jul 25 2007 Jesse Keating <jkeating@redhat.com> - 2.19.5-3
- Rebuild for RH #249435

* Mon Jul 23 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.5-2
- Port to new GTK+ tooltips API

* Tue Jul 10 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.5-1
- Update to 2.19.5

* Fri Jul  6 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.4-2
- Fix directory ownership issues

* Mon Jun 18 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.4-1
- Update to 2.19.4

* Tue Jun  5 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.3-1
- Update to 2.19.3

* Sat May 19 2007 Matthias Clasen <mclasen@redhat.com> - 2.19.2-1
- Update to 2.19.2

* Wed Apr 11 2007 Alexander Larsson <alexl@redhat.com> - 2.18.1-2
- Fix memleak (#235696)

* Wed Apr 11 2007 Alexander Larsson <alexl@redhat.com> - 2.18.1-1
- Update to 2.18.1

* Mon Mar 26 2007 Matthias Clasen <mclasen@redhat.com> - 2.18.0.1-2
- Update icon caches (#234020)

* Mon Mar 12 2007 Alexander Larsson <alexl@redhat.com> - 2.18.0.1-1
- Update to 2.18.0.1

* Tue Mar  6 2007 Alexander Larsson <alexl@redhat.com> - 2.17.92-3
- Update xdg-user-dirs patch, now handle renaming desktop dir

* Thu Mar  1 2007 Alexander Larsson <alexl@redhat.com> - 2.17.92-2
- Add xdg-user-dirs patch

* Tue Feb 27 2007 Matthias Clasen <mclasen@redhat.com> - 2.17.92-1
- Update to 2.17.92

* Tue Feb 13 2007 Matthias Clasen <mclasen@redhat.com> - 2.17.91-1
- Update to 2.17.91

* Wed Feb  7 2007 Matthias Clasen <mclasen@redhat.com> - 2.17.90-4
- Add DesktopSettings category to nautilus-file-management-properties.desktop

* Tue Feb  6 2007 Alexander Larsson <alexl@redhat.com> - 2.17.90-3
- update tracker dynamic search patch to new .so name

* Tue Jan 23 2007 Alexander Larsson <alexl@redhat.com> - 2.17.90-2
- Fix gnome bug #362302 in selinux patch

* Mon Jan 22 2007 Matthias Clasen <mclasen@redhat.com> - 2.17.90-1
- Update to 2.17.90

* Tue Dec 19 2006 Matthias Clasen <mclasen@redhat.com> - 2.17.1-1
- Update to 2.17.1

* Wed Nov 22 2006 Alexander Larsson <alexl@redhat.com> - 2.16.2-7
- Look for beagle before tracker, because tracker autostarts
  This lets us support having both installed at the same time.
- Remove buildreqs for beagle, as they are not necessary with
  the dynamic work.

* Tue Nov 14 2006 Matthias Clasen <mclasen@redhat.com> - 2.16.2-6
- Detect tracker dynamically, too

* Mon Nov 13 2006 Alexander Larsson <alexl@redhat.com> - 2.16.2-5.fc7
- Fix commonly reported NautilusDirectory crash

* Wed Nov  8 2006 Alexander Larsson <alexl@redhat.com> - 2.16.2-4.fc7
- Revert upstream icon placement patch as it seems broken

* Tue Nov  7 2006 Alexander Larsson <alexl@redhat.com> - 2.16.2-2.fc7
- Update to 2.16.2

* Sat Oct 21 2006 Matthias Clasen <mclasen@redhat.com> - 2.16.1-1 
- Update to 2.16.1

* Wed Oct 18 2006 Matthias Clasen <mclasen@redhat.com> - 2.16.0-6
- Fix scripts according to the packaging guidelines
- Require GConf2 for the scripts
- Require pkgconfig for the -devel package

* Sun Oct 01 2006 Jesse Keating <jkeating@redhat.com> - 2.16.0-5
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Tue Sep 19 2006 Alexander Larsson <alexl@redhat.com> - 2.16.0-4
- Support changing selinux contexts (#204030)

* Thu Sep 14 2006 Alexander Larsson <alexl@redhat.com> - 2.16.0-3
- Fix crash when opening custom icon dialog (#205352)

* Tue Sep  5 2006 Matthias Clasen <mclasen@redhat.com> - 2.16.0-2
- Add a %%preun script (#205260)

* Mon Sep  4 2006 Alexander Larsson <alexl@redhat.com> - 2.16.0-1
- Update to 2.16.0

* Fri Aug 25 2006 Alexander Larsson <alexl@redhat.com> - 2.15.92.1-2
- Omit self check code in build

* Tue Aug 22 2006 Alexander Larsson <alexl@redhat.com> - 2.15.92.1-1
- update to 2.15.92.1

* Mon Aug 21 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.92-1.fc6
- Update to 2.15.92

* Sat Aug 12 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.91-2.fc6
- Don't Provide/Obsolete nautilus-devel from the main package (#202322)

* Thu Aug 10 2006 Alexander Larsson <alexl@redhat.com> - 2.15.91-1.fc6
- Update to 2.15.91
- Split package into devel and extensions (#201967)

* Thu Aug  3 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.90-1.fc6
- Update to 2.15.90

* Tue Jul 18 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.4-3
- Spec file cleanups

* Wed Jul 12 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.4-2
- Don't require nautilus-cd-burner, to avoid a 
  BuildRequires-Requires loop

* Wed Jul 12 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.4-1
- Update to 2.15.4

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.15.2-1.1
- rebuild

* Tue Jun 13 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.2-1
- Update to 2.15.1

* Sun May 21 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.1-2
- Add missing BuildRequires (#129184)

* Wed May 17 2006 Matthias Clasen <mclasen@redhat.com> - 2.15.1-1
- Update to 2.15.1

* Fri May 12 2006 Matthias Clasen <mclasen@redhat.com> - 2.14.1-3
- Close the about dialog

* Tue Apr 11 2006 Matthias Clasen <mclasen@redhat.com> - 2.14.1-2
- Update to 2.14.1

* Mon Mar 13 2006 Matthias Clasen <mclasen@redhat.com> - 2.14.0-1
- Update to 2.14.0

* Mon Mar  6 2006 Matthias Clasen <mclasen@redhat.com> - 2.13.92-2
- Reinstate the format patch which was accidentally dropped

* Mon Feb 27 2006 Matthias Clasen <mclasen@redhat.com> - 2.13.92-1
- Update to 2.13.92

* Mon Feb 13 2006 Matthias Clasen <mclasen@redhat.com> - 2.13.91-1
- Update to 2.13.91

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.13.90-2.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.13.90-2.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Feb  6 2006 Matthias Clasen <mclasen@redhat.com> - 2.13.90-2
- Avoid delays in rendering the background

* Tue Jan 31 2006 Matthias Clasen <mclasen@redhat.com> - 2.13.90-1
- Update to 2.13.90

* Tue Jan 17 2006 Matthias Clasen <mclasen@redhat.com> - 2.13.4-1
- Update to 2.13.4

* Mon Jan  9 2006 Alexander Larsson <alexl@redhat.com> - 2.13.3-2
- Buildrequire libbeagle

* Tue Dec 13 2005 Alexander Larsson <alexl@redhat.com> 2.13.3-1
- Update to 2.13.3

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Dec  2 2005 Matthias Clasen <mclasen@redhat.com> 2.13.2-1
- Update to 2.13.2
- Update patches

* Tue Nov  1 2005 Alexander Larsson <alexl@redhat.com> - 2.12.1-6
- Switch XFree86-devel buildrequirement to libX11-devel

* Fri Oct 28 2005 Matthias Clasen <mclasen@redhat.com> 2.12.1-5
- Implement icon stretching keynav
- Support formatting non-floppy devices

* Sat Oct 22 2005 Matthias Clasen <mclasen@redhat.com> 2.12.1-4
- Improve icon stretching ui

* Fri Oct 21 2005 Matthias Clasen <mclasen@redhat.com> 2.12.1-3
- Only show the "Format menu item if gfloppy is present

* Fri Oct 21 2005 Matthias Clasen <mclasen@redhat.com> 2.12.1-2
- Add a "Format" context menu item to the floppy in "Computer"

* Thu Oct  6 2005 Matthias Clasen <mclasen@redhat.com> 2.12.1-1
- Update to 2.12.1

* Wed Sep  7 2005 Matthias Clasen <mclasen@redhat.com> 2.12.0-1
- Update to 2.12.0

* Tue Aug 16 2005 Matthias Clasen <mclasen@redhat.com> 
- New upstream release

* Wed Aug  3 2005 Matthias Clasen <mclasen@redhat.com> 2.11.90-1
- New upstream release

* Mon Jul 11 2005 Matthias Clasen <mclasen@redhat.com> 2.11.3-1
- Update to 2.11.3

* Wed May 11 2005 David Zeuthen <davidz@redhat.com> 2.10.0-4
- Fix default font for zh_TW (#154185)

* Sun Apr  3 2005 David Zeuthen <davidz@redhat.com> 2.10.0-3
- Include patches for desktop background memory saving (GNOME bug #169347)
- Obsoletes: nautilus-media (#153223)

* Mon Mar 28 2005 Matthias Clasen <mclasen@redhat.com> 2.10.0-2
- Rebuild against newer libexif

* Mon Mar 21 2005 David Zeuthen <davidz@redhat.com> 2.10.0-1
- Update to latest upstream version; tweak requires

* Thu Mar  3 2005 Alex Larsson <alexl@redhat.com> 2.9.91-2
- Rebuild

* Fri Feb 11 2005 Matthias Clasen <mclasen@redhat.com> - 2.9.91-1
- Update to 2.9.91

* Tue Nov  9 2004 Marco Pesenti Gritti <mpg@redhat.com> - 2.8.1-5
- Remove eog dependency. The bonobo component is no more used.

* Mon Oct 18 2004 Marco Pesenti Gritti <mpg@redhat.com> - 2.8.1-4
- #135824 Fix throbber position

* Fri Oct 15 2004 Alexander Larsson <alexl@redhat.com> - 2.8.1-3
- Slightly less bad error dialog when there is no handler for a file.
  Not ideal, but this change doesn't change any strings.

* Tue Oct 12 2004 Alexander Larsson <alexl@redhat.com> - 2.8.1-2
- Fix open with menu on mime mismatch
- Create desktop links ending with .desktop (#125104)
- Remove old cruft from specfile

* Mon Oct 11 2004 Alexander Larsson <alexl@redhat.com> - 2.8.1-1
- update to 2.8.1

* Fri Oct  8 2004 Alexander Larsson <alexl@redhat.com> - 2.8.0-3
- Backport more fixes from cvs

* Mon Oct  4 2004 Alexander Larsson <alexl@redhat.com> - 2.8.0-2
- Backport various bugfixes from HEAD

* Mon Sep 13 2004 Alexander Larsson <alexl@redhat.com> - 2.8.0-1
- Update to 2.8.0

* Fri Sep 10 2004 Alexander Larsson <alexl@redhat.com> - 2.7.92-3
- Don't require eject on s390(x), since there is none (#132228)

* Tue Sep  7 2004 Alexander Larsson <alexl@redhat.com> - 2.7.92-2
- Add patch to fix desktop keynav (#131894)

* Tue Aug 31 2004 Alex Larsson <alexl@redhat.com> 2.7.92-1
- update to 2.7.92

* Thu Aug 26 2004 Alexander Larsson <alexl@redhat.com> - 2.7.4-3
- Added requires eject
- Depend on gnome-vfs2-smb instead of -extras

* Tue Aug 24 2004 Alexander Larsson <alexl@redhat.com> - 2.7.4-2
- backport cvs fixes, including default view fix

* Thu Aug 19 2004 Alex Larsson <alexl@redhat.com> 2.7.4-1
- update to 2.7.4

* Fri Aug  6 2004 Ray Strode <rstrode@redhat.com> 2.7.2-1
- update to 2.7.2

* Tue Aug 3 2004 Matthias Clasen <mclasen@redhat.com> 2.6.0-7
- rebuilt

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri May 21 2004 Matthias Clasen <mclasen@redhat.com> 2.6.0-5
- rebuild

* Wed Apr 14 2004 Alexander Larsson <alexl@redhat.com> 2.6.0-4
- update cvs backport, now handles kde trash dir better

* Wed Apr 14 2004 Alexander Larsson <alexl@redhat.com> 2.6.0-3
- add cvs backport

* Wed Apr  7 2004 Alex Larsson <alexl@redhat.com> 2.6.0-2
- Make network servers go to network:// again

* Thu Apr  1 2004 Alex Larsson <alexl@redhat.com> 2.6.0-1
- update to 2.6.0

* Tue Mar 16 2004 Mike A. Harrisn <mharris@redhat.com> 2.5.91-2
- Changed BuildRequires: XFree86-libs >= 4.2.99 to BuildRequires: XFree86-devel
- Fixed BuildRoot to use _tmppath instead of /var/tmp

* Mon Mar 15 2004 Alex Larsson <alexl@redhat.com> 2.5.91-1
- update to 2.5.91

* Mon Mar  8 2004 Alexander Larsson <alexl@redhat.com> 2.5.90-1
- update to 2.5.90

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Feb 25 2004 Alexander Larsson <alexl@redhat.com>
- update libgnomeui required version to 2.5.3 (#116229)

* Tue Feb 24 2004 Alexander Larsson <alexl@redhat.com> 2.5.8-1
- update to 2.5.8

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Alexander Larsson <alexl@redhat.com> 2.5.7-1
- update to 2.5.7

* Fri Jan 30 2004 Alexander Larsson <alexl@redhat.com> 2.5.6-1
- update to 2.5.6

* Tue Jan 27 2004 Alexander Larsson <alexl@redhat.com> 2.5.5-1
- update to 2.5.5

* Tue Oct 28 2003 Than Ngo <than@redhat.com> 2.4.0-7
- fix start-here desktop file

* Mon Oct 27 2003 Than Ngo <than@redhat.com> 2.4.0-6
- rebuild against new librsvg2

* Fri Oct  3 2003 Alexander Larsson <alexl@redhat.com> 2.4.0-5
- Update cvs backport, now have the better desktop icon layout

* Mon Sep 29 2003 Alexander Larsson <alexl@redhat.com> 2.4.0-4
- Update cvs backport, fixes #105869

* Fri Sep 19 2003 Alexander Larsson <alexl@redhat.com> 2.4.0-3
- Backport bugfixes from the gnome-2-4 branch

* Tue Sep 16 2003 Alexander Larsson <alexl@redhat.com> 2.4.0-2
- Add patch that fixes crash when deleting in listview

* Tue Sep  9 2003 Alexander Larsson <alexl@redhat.com> 2.4.0-1
- 2.4.0

* Thu Sep  4 2003 Alexander Larsson <alexl@redhat.com> 2.3.90-2
- Add desktop icons patch

* Tue Sep  2 2003 Alexander Larsson <alexl@redhat.com> 2.3.90-1
- update to 2.3.90

* Tue Aug 26 2003 Alexander Larsson <alexl@redhat.com> 2.3.9-1
- update
- Add patch to ignore kde desktop links
- Re-enable kdesktop detection hack.
  kde doesn't seem to support the manager selection yet

* Wed Aug 20 2003 Alexander Larsson <alexl@redhat.com> 2.3.8-2
- don't require fontilus

* Mon Aug 18 2003 Alexander Larsson <alexl@redhat.com> 2.3.8-1
- update to gnome 2.3

* Wed Aug  6 2003 Elliot Lee <sopwith@redhat.com> 2.2.4-5
- Fix libtool

* Tue Jul  8 2003 Alexander Larsson <alexl@redhat.com> 2.2.4-4.E
- Rebuild

* Tue Jul  8 2003 Alexander Larsson <alexl@redhat.com> 2.2.4-4
- Backport fixes from cvs
- Change some default configurations

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue May 27 2003 Alexander Larsson <alexl@redhat.com> 2.2.4-2
- Add performance increase backport
- Add desktop manager selection backport

* Mon May 19 2003 Alexander Larsson <alexl@redhat.com> 2.2.4-1
- update to 2.2.4

* Tue May  6 2003 Alexander Larsson <alexl@redhat.com> 2.2.3-2
- Fix scrollkeeper pre-requires

* Mon Mar 31 2003 Alexander Larsson <alexl@redhat.com> 2.2.3-1
- Update to 2.2.3

* Tue Feb 25 2003 Alexander Larsson <alexl@redhat.com> 2.2.1-5
- Change the default new window size to fit in 800x600 (#85037)

* Thu Feb 20 2003 Alexander Larsson <alexl@redhat.com>
- Require gnome-vfs2-extras, since network menu item uses it (#84145)

* Tue Feb 18 2003 Alexander Larsson <alexl@redhat.com>
- Update to the latest bugfixes from cvs.
- Fixes #84291 for nautilus, context menu duplication and some other small bugs.

* Thu Feb 13 2003 Alexander Larsson <alexl@redhat.com> 2.2.1-2
- Add a patch to fix the forkbomb-under-kde bug (#81520)
- Add a patch to fix thumbnail memory leak
- require libXft.so.2 instead of Xft, since that changed in the XFree86 package

* Tue Feb 11 2003 Alexander Larsson <alexl@redhat.com> 2.2.1-1
- 2.2.1, lots of bugfixes

* Fri Jan 31 2003 Alexander Larsson <alexl@redhat.com> 2.2.0.2-2
- remove nautilus-server-connect since it broke without editable vfolders

* Fri Jan 31 2003 Alexander Larsson <alexl@redhat.com> 2.2.0.2-1
- Update to 2.2.0.2, fixes bg crasher
- parallelize build
- Added patch from cvs that fixes password hang w/ smb

* Thu Jan 23 2003 Alexander Larsson <alexl@redhat.com> 2.2.0.1-1
- Update to 2.2.0.1

* Wed Jan 22 2003 Tim Powers <timp@redhat.com> 2.2.0-2
- rebuilt

* Tue Jan 21 2003 Alexander Larsson <alexl@redhat.com> 2.2.0-1
- update to 2.2.0

* Fri Jan 17 2003 Alexander Larsson <alexl@redhat.com> 2.1.91-8
- Add requirement on fontilus and nautilus-cd-burner to get them
  on an upgrade.

* Fri Jan 17 2003 Alexander Larsson <alexl@redhat.com> 2.1.91-7
- Added patch to enable the look for kde desktop hack
- Removed patches that were fixed upstream

* Fri Jan 17 2003 Alexander Larsson <alexl@redhat.com> 2.1.91-6
- Removed the requirement of nautilus-cd-burner, since
  that is now on by default in comps

* Thu Jan 16 2003 Alexander Larsson <alexl@redhat.com> 2.1.91-5
- Require(post,postun) scrollkeeper (#67340)
- Add dot to end of summary

* Tue Jan 14 2003 Havoc Pennington <hp@redhat.com> 2.1.91-4
- use system-group.png not network-server.png for "Network Servers"

* Tue Jan 14 2003 Alexander Larsson <alexl@redhat.com> 2.1.91-3
- Correct filename in last change

* Tue Jan 14 2003 Alexander Larsson <alexl@redhat.com> 2.1.91-2
- change the network menu item to go to smb:

* Tue Jan 14 2003 Alexander Larsson <alexl@redhat.com> 2.1.91-1
- Update to 2.1.91
- Updated URL

* Tue Jan 14 2003 Havoc Pennington <hp@redhat.com>
- perl-munge the icon names in a couple desktop files
  to find redhat-network-server.png and redhat-file-manager.png.
  Upstream icon names here were weird and seem broken. 

* Thu Jan  9 2003 Alexander Larsson <alexl@redhat.com>
- 2.1.6
- Removed mp3 stripping script. Thats gone upstream now.

* Wed Dec 18 2002 Alexander Larsson <alexl@redhat.com> 2.1.5-2
- Add cdburn patch.
- Remove nautilus-1.1.19-starthere-hang-hackaround.patch
- Require nautilus-cd-burner

* Mon Dec 16 2002 Alexander Larsson <alexl@redhat.com> 2.1.5-1
- Update to 2.1.5. Require gnome-icon-theme >= 0.1.5, gnome-vfs >= 2.1.5

* Tue Dec  3 2002 Havoc Pennington <hp@redhat.com>
- add explicit startup-notification dependency because build system is
  dumb 
- 2.1.3

* Wed Nov 13 2002 Havoc Pennington <hp@redhat.com>
- 2.1.2

* Thu Oct 10 2002 Havoc Pennington <hp@redhat.com>
- 2.0.7
- remove patches that are upstream

* Tue Sep  3 2002 Alexander Larsson <alexl@redhat.com>  2.0.6-6
- Add badhack to make weblinks on desktop work

* Mon Sep  2 2002 Havoc Pennington <hp@redhat.com>
- fix #70667 assertion failures
- fix triple click patch

* Mon Sep  2 2002 Jonathan Blandford <jrb@redhat.com>
- don't activate on double click

* Sat Aug 31 2002 Havoc Pennington <hp@redhat.com>
- put button press mask in triple-click patch, maybe it will work
- remove html-hack patch as it does nothing useful

* Sat Aug 31 2002 Havoc Pennington <hp@redhat.com>
- require newer redhat-artwork, -menus, eel2, gnome-vfs2 to avoid
  bogus bug reports
- add hack for HTML mime type handling in a web browser, not 
  nautilus

* Thu Aug 29 2002 Alexander Larsson <alexl@redhat.com>
- Updated to 2.0.6. Removed the patches I put upstream.
- Added patch that fixes #72410

* Wed Aug 28 2002 Owen Taylor <otaylor@redhat.com>
- Add a simple patch so that redhat-config-packages can disable 
  the new window behavior for mounted CDs behavior.

* Wed Aug 28 2002 Alexander Larsson <alexl@redhat.com> 2.0.5-4
- Add patch to fix bug #70667

* Sun Aug 25 2002 Havoc Pennington <hp@redhat.com>
- remove mp3

* Fri Aug 23 2002 Havoc Pennington <hp@redhat.com>
- ignore the "add_to_session" preference as it only broke stuff
- pad the left margin a bit to cope with poor word wrapping

* Fri Aug 23 2002 Alexander Larsson <alexl@redhat.com> 2.0.5-1
- Update to 2.0.5, remove topleft icon patch

* Thu Aug 15 2002 Alexander Larsson <alexl@redhat.com> 2.0.4-2
- Add patch to fix the bug where desktop icons get
  stuck in the top left corner on startup

* Wed Aug 14 2002 Alexander Larsson <alexl@redhat.com> 2.0.4-1
- 2.0.4

* Tue Aug 13 2002 Havoc Pennington <hp@redhat.com>
- obsolete nautilus-mozilla < 2.0 #69839

* Mon Aug 12 2002 Havoc Pennington <hp@redhat.com>
- add rhconfig patch to Bluecurve theme and disable sidebar by default

* Wed Aug  7 2002 Havoc Pennington <hp@redhat.com>
- drop start here files, require redhat-menus that has them

* Tue Aug  6 2002 Havoc Pennington <hp@redhat.com>
- 2.0.3

* Sat Jul 27 2002 Havoc Pennington <hp@redhat.com>
- build for new eel2, gail

* Wed Jul 24 2002 Havoc Pennington <hp@redhat.com>
- and add the libexec components, mumble

* Wed Jul 24 2002 Havoc Pennington <hp@redhat.com>
- put the components in the file list, were moved upstream

* Tue Jul 23 2002 Havoc Pennington <hp@redhat.com>
- 2.0.1

* Thu Jun 27 2002 Owen Taylor <otaylor@redhat.com>
- Relibtoolize to fix relink problems for solib components
- Add LANG=en_US to %%makeinstall as well
- Back out previous change, force locale to en_US to prevent UTF-8 problems
- Add workaround for intltool-merge bug on ia64

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sun Jun 16 2002 Havoc Pennington <hp@redhat.com>
- 2.0.0
- use desktop-file-install
- require desktop-backgrounds-basic

* Wed Jun 12 2002 Havoc Pennington <hp@redhat.com>
- add wacky hack in hopes of fixing the hang-on-login thing

* Sat Jun  8 2002 Havoc Pennington <hp@redhat.com>
- add build requires on new gail
- rebuild to try to lose broken libgailutil.so.13 dependency

* Sat Jun 08 2002 Havoc Pennington <hp@redhat.com>
- rebuild in different environment

* Wed Jun  5 2002 Havoc Pennington <hp@redhat.com>
- 1.1.19

* Fri May 31 2002 Havoc Pennington <hp@redhat.com>
- rebuild in different environment

* Thu May 30 2002 Havoc Pennington <hp@redhat.com>
- really remove nautilus-devel if we are going to obsolete it
- don't require hwbrowser

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue May 21 2002 Havoc Pennington <hp@redhat.com>
- rebuild in different environment

* Tue May 21 2002 Havoc Pennington <hp@redhat.com>
- 1.1.17

* Fri May  3 2002 Havoc Pennington <hp@redhat.com>
- 1.1.14

* Thu Apr 25 2002 Havoc Pennington <hp@redhat.com>
- require eog
- obsolete nautilus-devel
- fix name of schemas file in post

* Mon Apr 22 2002 Alex Larsson <alexl@redhat.com>
- Update to 1.1.13

* Fri Apr 19 2002 Havoc Pennington <hp@redhat.com>
- put tree view in file list

* Thu Apr 18 2002 Havoc Pennington <hp@redhat.com>
- nautilus for gnome 2
- clean up the spec file and file list a bit

* Mon Apr 15 2002 Havoc Pennington <hp@redhat.com>
- merge translations

* Thu Apr  4 2002 Alex Larsson <alexl@redhat.com>
- Add patch to fix trash crash

* Mon Apr  1 2002 Havoc Pennington <hp@redhat.com>
- fix for metadata tmp race
- backport thumbnail speed fix and thumbnail inf. loop fix

* Mon Mar 25 2002 Havoc Pennington <hp@redhat.com>
- add some fixes from CVS version, including one for #61819 and a couple segfaults

* Wed Mar 20 2002 Havoc Pennington <hp@redhat.com>
- fix thumbnails for files with future timestamp, #56862

* Mon Mar 11 2002 Havoc Pennington <hp@redhat.com>
- buildrequires intltool #60633
- apply Alex's pixbuf cache patch to save a few megs #60581

* Wed Feb 27 2002 Havoc Pennington <hp@redhat.com>
- drop Milan-specific features, including png10 and ac25 patches
- copy in 1.0.5 help component to avoid large risky patch
- remove .la files
- drop mozilla from ia64 again
- remove oaf file from nautilus-mozilla that was also in the base 
  package

* Mon Jan 28 2002 Bill Nottingham <notting@redhat.com>
- enable mozilla support on ia64

* Fri Dec 28 2001 Christopher Blizzard <blizzard@redhat.com>
- require Mozilla 0.9.7
- Add patch that puts mozilla profile startup before embedding is initialized

* Tue Nov 20 2001 Havoc Pennington <hp@redhat.com>
- 1.0.6, require Mozilla 0.9.6

* Tue Oct 23 2001 Alex Larsson <alexl@redhat.com>
- Update to 1.0.5

* Thu Sep  6 2001 Owen Taylor <otaylor@redhat.com>
- Fix handling of GnomeVFSFileInfo structure (#53315)

* Wed Sep  5 2001 Owen Taylor <otaylor@redhat.com>
- Change handling of names on unmount to fix #52325

* Tue Sep  4 2001 Havoc Pennington <hp@redhat.com>
- put nautilus-help.desktop in file list; #53109

* Fri Aug 31 2001 Havoc Pennington <hp@redhat.com>
- Add po files from sources.redhat.com

* Mon Aug 27 2001 Havoc Pennington <hp@redhat.com>
- Add po files from sources.redhat.com

* Thu Aug 23 2001 Alex Larsson <alexl@redhat.com> 1.0.4-38
- Added patch to fix the .directory issuer

* Thu Aug 23 2001 Havoc Pennington <hp@redhat.com>
- I screwed up the build yesterday, so it didn't actually contain the
  fixes mentioned. This build should contain them.

* Wed Aug 22 2001 Havoc Pennington <hp@redhat.com>
- fix bug causing 32000 stats or so in large directories, 
  should speed things up somewhat
- fix #52104 via gruesome kdesktop-detection hack and setting
  window type hint on our desktop window
- fix so Start Here icon displays in sidebar
- don't load non-local .desktop files

* Mon Aug 20 2001 Havoc Pennington <hp@redhat.com>
- make Programs icon into a link, to match the other .desktop files
- own various directories #51164
- web page titles in Japanese, #51709
- tree defaults to only directories #51850

* Wed Aug 15 2001 Havoc Pennington <hp@redhat.com>
- make start here icon work again
- kill some warning spew, #51661
- cache getpwnam() results to speed things up a bit

* Tue Aug 14 2001 Owen Taylor <otaylor@redhat.com>
- Fix problem with missing desktop starthere.desktop file
- New snapshot from our branch, fixes:
  - On upgrade, icons migrated from GNOME desktop are not properly lined up
    (#51436)
  - icons dropped on the desktop don't end up where dropped. (#51441)
  - Nautilus shouldn't have fam monitor read-only windows. This
    keeps CDROMS from being unmounted until you close all

    nautilus windows pointing to them. (#51442)
  - Warnings about 'cannot statfs...' when moving items to trash.
- Use separate start-here.desktop for panel, since the one used
  for the root window only works from Nautilus.

* Fri Aug 10 2001 Alexander Larsson <alexl@redhat.com>
- Changed starthere .desktop files to be links instead
- of spawning a new nautilus. This makes start-here:
- much faster.

* Thu Aug  9 2001 Alexander Larsson <alexl@redhat.com>
- Added hwbrowser dependency
- New snapshot, fixes the mozilla-view submit form problem

* Wed Aug  8 2001 Jonathan Blandford <jrb@redhat.com>
- Rebuild with new xml-i18n-tools
- fix crash in creating new desktop files

* Tue Aug  7 2001 Jonathan Blandford <jrb@redhat.com>
- Fix up DnD code some more

* Thu Aug 02 2001 Havoc Pennington <hp@redhat.com>
- Sync our CVS version; fixes some MUSTFIX
  (the one about drawing background on startup, 
   properly translate desktop files, etc.)

* Wed Aug  1 2001 Alexander Larsson <alexl@redhat.com> 1.0.4-24
- Fix 64bit cleanness issue
- Fix NULL mimetype crash
- Disable additional_text for .desktop files

* Tue Jul 31 2001 Alexander Larsson <alexl@redhat.com> 1.0.4-23
- Fix unmounting devices.

* Tue Jul 31 2001 Alexander Larsson <alexl@redhat.com> 1.0.4-22
- Make it depend on gnome-vfs-1.0.1-13. Needed for .desktop
- mimetype sniffing.

* Mon Jul 30 2001 Alexander Larsson <alexl@redhat.com> 1.0.4-21
- Remove the "don't run as root" warning.
- Remove eazel from bookmarks
- langified (again? did someone change it?)

* Fri Jul 27 2001 Alexander Larsson <alexl@redhat.com>
- Apply a patch that makes nautilus dnd reset work with the latest
- eel release.

* Thu Jul 26 2001 Alexander Larsson <alexl@redhat.com>
- Build on ia64 without the mozilla component.

* Wed Jul 25 2001 Havoc Pennington <hp@redhat.com>
- Fix crash-on-startup showstopper
- Fix can't-find-images bug (this one was only showing up
  when built with debug symbols, since it was an uninitialized memory
  read)

* Tue Jul 24 2001 Havoc Pennington <hp@redhat.com>
- sync new tarball from our CVS branch, 
  fixes some drag-and-drop, changes URI scheme names,
  etc.

* Tue Jul 24 2001 Owen Taylor <otaylor@redhat.com>
- Add BuildRequires (#49539, 49537)
- Fix %%post, %%postun (#49720)
- Background efficiency improvements and hacks

* Fri Jul 13 2001 Alexander Larsson <alexl@redhat.com>
- Don't launch esd on each mouseover.

* Wed Jul 11 2001 Havoc Pennington <hp@redhat.com>
- move first time druid patch into my "CVS outstanding" patch
- try to really remove Help/Feedback
- try to really fix Help/Community Support
- try again to get Start Here in the Go menu
- try again to get Start Here on the desktop
- don't show file sizes for .desktop files

* Tue Jul 10 2001 Havoc Pennington <hp@redhat.com>
- add newline to ends of .desktop files that were missing them

* Tue Jul 10 2001 Havoc Pennington <hp@redhat.com>
- update to my latest 'cvs diff -u' (adds default 
  Start Here link, displays .directory name in sidebar)
- include /etc/X11/* links (starthere, sysconfig, serverconfig)

* Tue Jul 10 2001 Jonathan Blandford <jrb@redhat.com>
- Patch to remove firsttime druid and flash

* Mon Jul 09 2001 Havoc Pennington <hp@redhat.com>
- add hacks for displaying desktop files
- add hack to turn off the "unwriteable" emblem

* Sun Jul  8 2001 Tim Powers <timp@redhat.com>
- added defattr to the files lists to be (-,root,root)
- languified

* Sat Jul  7 2001 Alexander Larsson <alexl@redhat.com>
- Need to run autoheader too.

* Fri Jul  6 2001 Alexander Larsson <alexl@redhat.com>
- Make the fam dependency a real runtime dependency
- by linking to libfam (nautilus-1.0.4-fam-lib.patch)
- Cleaned up specfile.

* Fri Jul  6 2001 Alexander Larsson <alexl@redhat.com>
- Change default background and rubberband color.
- Use the sidebar tabs from the default theme
- BuildDepend on fam-devel, depend on fam
- Disable the eazel update pages in the first-time druid.
- Remove the eazel logo from the first-time druid

* Thu Jul 05 2001 Havoc Pennington <hp@redhat.com>
- 1.0.4, removes eazel services icon and wizard page
- Eazel logo is still in startup wizard for now, needs fixing

* Tue Jul 03 2001 Havoc Pennington <hp@redhat.com>
- fix group (s/Desktop/Desktops/) #47134
- remove ammonite dependency

* Wed Jun 27 2001 Havoc Pennington <hp@redhat.com>
- add a different default theme
- clean up file list overspecificity a bit

* Tue Jun 26 2001 Havoc Pennington <hp@redhat.com>
- move to a CVS snapshot of nautilus for now
  (Darin is my hero for having distcheck work out of CVS)

* Thu May 10 2001 Jonathan Blandford <jrb@redhat.com>
- clean up defaults a bit

* Wed May  9 2001 Jonathan Blandford <jrb@redhat.com>
- New version

* Tue Apr 17 2001 Gregory Leblanc <gleblanc@grego1.cu-portland.edu>
- Added BuildRequires lines
- Changed Source to point to ftp.gnome.org instead of just the tarball name
- Moved %%description sections closer to their %%package sections
- Moved %%changelog to the end, where so that it's not in the way
- Changed configure and make install options to allow moving of
  libraries, includes, binaries more easily
- Removed hard-coded paths (don't define %%prefix or %%docdir)
- replace %%{prefix}/bin with %%{_bindir}
- replace %%{prefix}/share with %%{_datadir}
- replace %%{prefix}/lib with %%{_libdir}
- replace %%{prefix}/include with %%{_includedir}

* Tue Oct 10 2000 Robin Slomkowski <rslomkow@eazel.com>
- removed obsoletes from sub packages and added mozilla and trilobite
subpackages

* Wed Apr 26 2000 Ramiro Estrugo <ramiro@eazel.com>
- created this thing
