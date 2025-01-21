%global appstream_version 0.14.0
%global flatpak_version 1.9.1
%global fwupd_version 1.5.6
%global glib2_version 2.70.0
%global gtk4_version 4.14.0
%global json_glib_version 1.6.0
%global libadwaita_version 1.6~alpha
%global libxmlb_version 0.1.7

# Disable WebApps for RHEL builds
%bcond webapps %[!0%{?rhel}]
# Disable parental control for RHEL builds
%bcond malcontent %[!0%{?rhel}]
# Disable rpm-ostree support for RHEL builds
%bcond rpmostree %[!0%{?rhel}]
# Disable DKMS/akmods support for RHEL builds
%bcond dkms %[!0%{?rhel}]

# this is not a library version
%define gs_plugin_version 21

%global tarball_version %%(echo %{version} | tr '~' '.')

%global __provides_exclude_from ^%{_libdir}/%{name}/plugins-%{gs_plugin_version}/.*\\.so.*$

Name:      gnome-software
Version:   47.2
Release:   3%{?dist}
Summary:   A software center for GNOME

License:   GPL-2.0-or-later
URL:       https://apps.gnome.org/Software
Source0:   https://download.gnome.org/sources/gnome-software/47/%{name}-%{tarball_version}.tar.xz

Patch01:   0001-crash-under-gs_appstream_gather_merge_data.patch

# ostree and flatpak not on i686 for Fedora and RHEL 10
# https://github.com/containers/composefs/pull/229#issuecomment-1838735764
%if 0%{?fedora} || 0%{?rhel} >= 10
ExcludeArch:    %{ix86}
%endif

BuildRequires: docbook-style-xsl
BuildRequires: desktop-file-utils
BuildRequires: gcc
BuildRequires: gettext
BuildRequires: gtk-doc
BuildRequires: itstool
BuildRequires: libxslt
BuildRequires: meson
BuildRequires: pkgconfig(appstream) >= %{appstream_version}
BuildRequires: pkgconfig(flatpak) >= %{flatpak_version}
BuildRequires: pkgconfig(fwupd) >= %{fwupd_version}
BuildRequires: pkgconfig(gdk-pixbuf-2.0)
BuildRequires: pkgconfig(gio-unix-2.0) >= %{glib2_version}
BuildRequires: pkgconfig(glib-2.0) >= %{glib2_version}
BuildRequires: pkgconfig(gmodule-2.0) >= %{glib2_version}
BuildRequires: pkgconfig(gsettings-desktop-schemas)
BuildRequires: pkgconfig(gtk4) >= %{gtk4_version}
BuildRequires: pkgconfig(gudev-1.0)
BuildRequires: pkgconfig(json-glib-1.0) >= %{json_glib_version}
BuildRequires: pkgconfig(libadwaita-1) >= %{libadwaita_version}
BuildRequires: pkgconfig(libdnf)
BuildRequires: pkgconfig(libsoup-3.0)
%if %{with malcontent}
BuildRequires: pkgconfig(malcontent-0)
%endif
BuildRequires: pkgconfig(ostree-1)
BuildRequires: pkgconfig(polkit-gobject-1)
BuildRequires: pkgconfig(rpm)
%if %{with rpmostree}
BuildRequires: pkgconfig(rpm-ostree-1)
%endif
BuildRequires: pkgconfig(sysprof-capture-4)
BuildRequires: pkgconfig(xmlb) >= %{libxmlb_version}

Requires: appstream-data
Requires: appstream%{?_isa} >= %{appstream_version}
%if %{with webapps}
Requires: epiphany-runtime%{?_isa}
%endif
Requires: flatpak%{?_isa} >= %{flatpak_version}
Requires: flatpak-libs%{?_isa} >= %{flatpak_version}
Requires: fwupd%{?_isa} >= %{fwupd_version}
Requires: glib2%{?_isa} >= %{glib2_version}
Requires: gnome-app-list
# gnome-menus is needed for app folder .directory entries
Requires: gnome-menus%{?_isa}
Requires: gsettings-desktop-schemas%{?_isa}
Requires: gtk4 >= %{gtk4_version}
Requires: json-glib%{?_isa} >= %{json_glib_version}
Requires: iso-codes
Requires: libadwaita >= %{libadwaita_version}
# librsvg2 is needed for gdk-pixbuf svg loader
Requires: librsvg2%{?_isa}
Requires: libxmlb%{?_isa} >= %{libxmlb_version}

Recommends: %{name}-fedora-langpacks

Obsoletes: gnome-software-snap < 3.33.1
Obsoletes: gnome-software-editor < 3.35.1

%description
gnome-software is an application that makes it easy to add, remove
and update software in the GNOME desktop.

%package devel
Summary: Headers for building external gnome-software plugins
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
These development files are for building gnome-software plugins outside
the source tree. Most users do not need this subpackage installed.

%package fedora-langpacks
Summary: Contains fedora-langpacks plugin
Requires: %{name}%{?_isa} = %{version}-%{release}

%description fedora-langpacks
The fedora-langpacks plugin ensures langpacks packages are installed
for the current locale.

%if %{with rpmostree}
%package rpm-ostree
Summary: rpm-ostree backend for gnome-software
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: rpm-ostree%{?_isa}
Supplements: (gnome-software%{?_isa} and rpm-ostree%{?_isa})

%description rpm-ostree
gnome-software is an application that makes it easy to add, remove
and update software in the GNOME desktop.

This package includes the rpm-ostree backend.
%endif

%prep
%autosetup -p1 -S gendiff -n %{name}-%{tarball_version}

%build
%meson \
    -Dpackagekit=false \
    -Dsnap=false \
%if %{with malcontent}
    -Dmalcontent=true \
%else
    -Dmalcontent=false \
%endif
    -Dgudev=true \
    -Dexternal_appstream=false \
%if %{with rpmostree}
    -Drpm_ostree=true \
%else
    -Drpm_ostree=false \
%endif
%if %{with webapps}
    -Dwebapps=true \
    -Dhardcoded_foss_webapps=true \
    -Dhardcoded_proprietary_webapps=false \
%else
    -Dwebapps=false \
    -Dhardcoded_foss_webapps=false \
    -Dhardcoded_proprietary_webapps=false \
%endif
%if %{with dkms}
    -Ddkms=true \
%else
    -Ddkms=false \
%endif
    -Dtests=false
%meson_build

%install
%meson_install

# remove unneeded dpkg and dummy plugins
rm %{buildroot}%{_libdir}/gnome-software/plugins-%{gs_plugin_version}/libgs_plugin_dpkg.so
rm %{buildroot}%{_libdir}/gnome-software/plugins-%{gs_plugin_version}/libgs_plugin_dummy.so
rm %{buildroot}%{_datadir}/applications/gnome-software-local-file-packagekit.desktop

# make the software center load faster
desktop-file-edit %{buildroot}%{_datadir}/applications/org.gnome.Software.desktop \
    --set-key=X-AppInstall-Package --set-value=%{name}

# set up for Fedora
cat >> %{buildroot}%{_datadir}/glib-2.0/schemas/org.gnome.software-fedora.gschema.override << FOE
[org.gnome.software]
%if 0%{?rhel}
official-repos = [ 'rhel-%{?rhel}' ]
%else
official-repos = [ 'anaconda', 'fedora', 'fedora-debuginfo', 'fedora-source', 'koji-override-0', 'koji-override-1', 'rawhide', 'rawhide-debuginfo', 'rawhide-source', 'updates', 'updates-debuginfo', 'updates-source', 'updates-testing', 'updates-testing-debuginfo', 'updates-testing-source', 'fedora-modular', 'fedora-modular-debuginfo', 'fedora-modular-source', 'rawhide-modular', 'rawhide-modular-debuginfo', 'rawhide-modular-source', 'fedora-cisco-openh264', 'fedora-cisco-openh264-debuginfo' ]
required-repos = [ 'fedora', 'updates' ]
packaging-format-preference = [ 'flatpak:fedora-testing', 'flatpak:fedora', 'rpm' ]
%endif
FOE

%find_lang %name --with-gnome

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop

%files -f %{name}.lang
%doc AUTHORS README.md
%license COPYING
%{_bindir}/gnome-software
%{_datadir}/applications/gnome-software-local-file-flatpak.desktop
%{_datadir}/applications/gnome-software-local-file-fwupd.desktop
%{_datadir}/applications/org.gnome.Software.desktop
%{_datadir}/bash-completion/completions/gnome-software
%{_mandir}/man1/gnome-software.1*
%{_datadir}/icons/hicolor/*/apps/org.gnome.Software.svg
%{_datadir}/icons/hicolor/symbolic/apps/org.gnome.Software-symbolic.svg
%{_datadir}/icons/hicolor/scalable/categories/system-component-addon.svg
%{_datadir}/icons/hicolor/scalable/categories/system-component-application.svg
%{_datadir}/icons/hicolor/scalable/categories/system-component-codecs.svg
%{_datadir}/icons/hicolor/scalable/categories/system-component-driver.svg
%{_datadir}/icons/hicolor/scalable/categories/system-component-firmware.svg
%{_datadir}/icons/hicolor/scalable/categories/system-component-input-sources.svg
%{_datadir}/icons/hicolor/scalable/categories/system-component-language.svg
%{_datadir}/icons/hicolor/scalable/categories/system-component-os-updates.svg
%{_datadir}/icons/hicolor/scalable/categories/system-component-runtime.svg
%{_datadir}/metainfo/org.gnome.Software.metainfo.xml
%if %{with webapps}
%{_datadir}/metainfo/org.gnome.Software.Plugin.Epiphany.metainfo.xml
%endif
%{_datadir}/metainfo/org.gnome.Software.Plugin.Flatpak.metainfo.xml
%{_datadir}/metainfo/org.gnome.Software.Plugin.Fwupd.metainfo.xml
%dir %{_libdir}/gnome-software/plugins-%{gs_plugin_version}
%{_libdir}/gnome-software/libgnomesoftware.so.%{gs_plugin_version}
%{_libdir}/gnome-software/plugins-%{gs_plugin_version}/libgs_plugin_appstream.so
%if %{with webapps}
%{_libdir}/gnome-software/plugins-%{gs_plugin_version}/libgs_plugin_epiphany.so
%endif
%{_libdir}/gnome-software/plugins-%{gs_plugin_version}/libgs_plugin_fedora-pkgdb-collections.so
%{_libdir}/gnome-software/plugins-%{gs_plugin_version}/libgs_plugin_flatpak.so
%{_libdir}/gnome-software/plugins-%{gs_plugin_version}/libgs_plugin_fwupd.so
%{_libdir}/gnome-software/plugins-%{gs_plugin_version}/libgs_plugin_generic-updates.so
%{_libdir}/gnome-software/plugins-%{gs_plugin_version}/libgs_plugin_hardcoded-blocklist.so
%{_libdir}/gnome-software/plugins-%{gs_plugin_version}/libgs_plugin_icons.so
%if %{with malcontent}
%{_libdir}/gnome-software/plugins-%{gs_plugin_version}/libgs_plugin_malcontent.so
%endif
%{_libdir}/gnome-software/plugins-%{gs_plugin_version}/libgs_plugin_modalias.so
%{_libdir}/gnome-software/plugins-%{gs_plugin_version}/libgs_plugin_os-release.so
%{_libdir}/gnome-software/plugins-%{gs_plugin_version}/libgs_plugin_provenance-license.so
%{_libdir}/gnome-software/plugins-%{gs_plugin_version}/libgs_plugin_provenance.so
%{_libdir}/gnome-software/plugins-%{gs_plugin_version}/libgs_plugin_repos.so
%{_sysconfdir}/xdg/autostart/org.gnome.Software.desktop
%dir %{_datadir}/swcatalog
%dir %{_datadir}/swcatalog/xml
%if %{with webapps}
%{_datadir}/swcatalog/xml/gnome-pwa-list-foss.xml
%endif
%{_datadir}/dbus-1/services/org.gnome.Software.service
%{_datadir}/gnome-shell/search-providers/org.gnome.Software-search-provider.ini
%{_datadir}/glib-2.0/schemas/org.gnome.software.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.software-fedora.gschema.override
%{_libexecdir}/gnome-software-cmd
%{_libexecdir}/gnome-software-restarter

%if %{with dkms}
%{_datadir}/polkit-1/actions/org.gnome.software.dkms-helper.policy
%{_libdir}/gnome-software/plugins-%{gs_plugin_version}/libgs_plugin_dkms.so
%{_libexecdir}/gnome-software-dkms-helper
%endif

%files fedora-langpacks
%{_libdir}/gnome-software/plugins-%{gs_plugin_version}/libgs_plugin_fedora-langpacks.so

%if %{with rpmostree}
%files rpm-ostree
%{_libdir}/gnome-software/plugins-%{gs_plugin_version}/libgs_plugin_rpm-ostree.so
%endif

%files devel
%{_libdir}/pkgconfig/gnome-software.pc
%dir %{_includedir}/gnome-software
%{_includedir}/gnome-software/*.h
%{_libdir}/gnome-software/libgnomesoftware.so
%dir %{_datadir}/gtk-doc
%dir %{_datadir}/gtk-doc/html
%{_datadir}/gtk-doc/html/gnome-software/

%changelog
* Mon Dec 09 2024 Milan Crha <mcrha@redhat.com> - 47.2-2
- Resolves: #2272232 (Crash under gs_appstream_gather_merge_data())

* Mon Nov 25 2024 Milan Crha <mcrha@redhat.com> - 47.2-1
- Update to 47.2

* Thu Oct 10 2024 Milan Crha <mcrha@redhat.com> - 47.1-1
- Update to 47.1

* Thu Sep 19 2024 Milan Crha <mcrha@redhat.com> - 47.0-2
- Resolves: #2312882 (dkms: Fix callback user data in a reload() function)

* Fri Sep 13 2024 Milan Crha <mcrha@redhat.com> - 47.0-1
- Update to 47.0

* Fri Aug 30 2024 Milan Crha <mcrha@redhat.com> - 47~rc-1
- Update to 47.rc

* Fri Aug 02 2024 Milan Crha <mcrha@redhat.com> - 47~beta-1
- Update to 47.beta
- Build with DKMS/akmods plugin in Fedora

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 47~alpha-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 28 2024 Milan Crha <mcrha@redhat.com> - 47~alpha-1
- Update to 47.alpha

* Fri May 24 2024 Milan Crha <mcrha@redhat.com> - 46.2-1
- Update to 46.2

* Thu Apr 25 2024 Milan Crha <mcrha@redhat.com> - 46.1-1
- Update to 46.1

* Fri Apr 12 2024 Adam Williamson <awilliam@redhat.com> - 46.0-2
- Backport MR #1949 to fix upgrading

* Mon Mar 18 2024 Milan Crha <mcrha@redhat.com> - 46.0-1
- Update to 46.0

* Fri Mar 01 2024 Milan Crha <mcrha@redhat.com> - 46~rc-1
- Update to 46.rc

* Fri Feb 09 2024 Milan Crha <mcrha@redhat.com> - 46~beta-1
- Update to 46.beta

* Fri Jan 26 2024 Milan Crha <mcrha@redhat.com> - 46~alpha-4
- Resolves: #2260294 (Split fedora-langpacks plugin into a subpackage)

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 46~alpha-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 46~alpha-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 05 2024 Milan Crha <mcrha@redhat.com> - 46~alpha-1
- Update to 46.alpha

* Fri Dec 01 2023 Milan Crha <mcrha@redhat.com> - 45.2-1
- Update to 45.2

* Tue Nov 07 2023 Neal Gompa <ngompa@fedoraproject.org> - 45.1-3
- Fix appstream_version macro for prerelease appstream 1.0 package

* Tue Nov 07 2023 Milan Crha <mcrha@redhat.com> - 45.1-2
- Add patch to build with appstream 1.0

* Fri Oct 20 2023 Milan Crha <mcrha@redhat.com> - 45.1-1
- Update to 45.1

* Fri Sep 15 2023 Milan Crha <mcrha@redhat.com> - 45.0-1
- Update to 45.0

* Fri Sep 01 2023 Milan Crha <mcrha@redhat.com> - 45~rc-1
- Update to 45.rc

* Mon Jul 31 2023 Milan Crha <mcrha@redhat.com> - 45~beta-1
- Update to 45.beta

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 45~alpha-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jun 30 2023 Milan Crha <mcrha@redhat.com> - 45~alpha-1
- Update to 45.alpha

* Thu Jun 22 2023 Tomas Popela <tpopela@redhat.com> - 44.2-2
- Disable parental control (through malcontent) and rpm-ostree support in RHEL

* Fri May 26 2023 Milan Crha <mcrha@redhat.com> - 44.2-1
- Update to 44.2

* Fri May 19 2023 Milan Crha <mcrha@redhat.com> - 44.1-2
- Rebuild for RPM

* Fri Apr 21 2023 Milan Crha <mcrha@redhat.com> - 44.1-1
- Update to 44.1

* Sun Mar 26 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 44.0-3
- Fix libsoup runtime dependency

* Fri Mar 24 2023 Milan Crha <mcrha@redhat.com> - 44.0-2
- Resolves: #2181367 (Prefer Fedora Flatpaks before RPM before other sources for apps)

* Fri Mar 17 2023 Milan Crha <mcrha@redhat.com> - 44.0-1
- Update to 44.0

* Fri Mar 03 2023 Milan Crha <mcrha@redhat.com> - 44~rc-1
- Update to 44.rc

* Thu Feb 23 2023 Adam Williamson <awilliam@redhat.com> - 44~beta-2
- Backport MR #1635 to fix update notifications

* Tue Feb 14 2023 Milan Crha <mcrha@redhat.com> - 44.beta-1
- Update to 44.beta

* Thu Feb 09 2023 Michael Catanzaro <mcatanzaro@redhat.com> - 44~alpha-3
- Switch to libsoup 3

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 44~alpha-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Jan 09 2023 Milan Crha <mcrha@redhat.com> - 44.alpha-1
- Update to 44.alpha

* Fri Dec 02 2022 Milan Crha <mcrha@redhat.com> - 43.2-1
- Update to 43.2

* Tue Nov 08 2022 Milan Crha <mcrha@redhat.com> - 43.1-3
- Also skip gnome-pwa-list-foss.xml when building without WebApps

* Tue Nov 08 2022 Milan Crha <mcrha@redhat.com> - 43.1-2
- Disable WebApps for RHEL builds

* Mon Oct 24 2022 Milan Crha <mcrha@redhat.com> - 43.1-1
- Update to 43.1

* Wed Oct 05 2022 Milan Crha <mcrha@redhat.com> - 43.0-3
- Resolves: #2132292 (rpm-ostree plugin refuses to update)

* Tue Sep 27 2022 Kalev Lember <klember@redhat.com> - 43.0-2
- Rebuild to fix sysprof-capture symbols leaking into libraries consuming it

* Fri Sep 16 2022 Milan Crha <mcrha@redhat.com> - 43.0-1
- Update to 43.0

* Tue Sep 13 2022 Milan Crha <mcrha@redhat.com> - 43.rc-2
- Resolves: #2124869 (Cannot install RPM package file)

* Fri Sep 02 2022 Milan Crha <mcrha@redhat.com> - 43.rc-1
- Update to 43.rc

* Wed Aug 17 2022 Milan Crha <mcrha@redhat.com> - 43.beta-3
- Resolves: #2119089 (No enough apps to show for the "Editor's Choice" section)

* Mon Aug 15 2022 Milan Crha <mcrha@redhat.com> - 43.beta-2
- Add patch for install-queue

* Fri Aug 05 2022 Milan Crha <mcrha@redhat.com> - 43.beta-1
- Update to 43.beta

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 43.alpha-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jul 07 2022 Adam Williamson <awilliam@redhat.com> - 43.alpha-2
- Backport MR #1401 to fix issue #1816 and fedora-workstation #107

* Fri Jul 01 2022 Milan Crha <mcrha@redhat.com> - 43.alpha-1
- Update to 43.alpha

* Fri Jun 17 2022 Richard Hughes <rhughes@redhat.com> - 42.2-4
- Add patch to make fwupd user requests work

* Thu Jun 16 2022 David King <amigadave@amigadave.com> - 42.2-3
- Filter private libraries from Provides
- Use pkgconfig for BuildRequires
- Improve directory onwership

* Mon Jun 13 2022 Milan Crha <mcrha@redhat.com> - 42.2-2
- Add patch for crash under gs_flatpak_refine_app_unlocked()

* Mon May 30 2022 Milan Crha <mcrha@redhat.com> - 42.2-1
- Update to 42.2
- Add patch to correct order of the setup of the GsShell

* Wed Apr 27 2022 Milan Crha <mcrha@redhat.com> - 42.1-1
- Update to 42.1

* Fri Mar 18 2022 Milan Crha <mcrha@redhat.com> - 42.0-1
- Update to 42.0

* Thu Mar 10 2022 Milan Crha <mcrha@redhat.com> - 42.rc-2
- Add upstream patches for gs-download-utils (i#1677 and i#1679)

* Mon Mar 07 2022 Milan Crha <mcrha@redhat.com> - 42.rc-1
- Update to 42.rc

* Mon Feb 21 2022 Milan Crha <mcrha@redhat.com> - 42.beta-3
- Resolves: #2056082 (Enable PackageKit autoremove option)

* Wed Feb 16 2022 Milan Crha <mcrha@redhat.com> - 42.beta-2
- Resolves: #2054939 (Crash on a PackageKit app install)
- Add a temporary workaround for gtk_widget_measure error flood on GsAppRow

* Fri Feb 11 2022 Milan Crha <mcrha@redhat.com> - 42.beta-1
- Update to 42.beta

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 42~alpha-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jan 07 2022 Milan Crha <mcrha@redhat.com> - 42.alpha-1
- Update to 42.alpha

* Fri Dec 03 2021 Milan Crha <mcrha@redhat.com> - 41.2-1
- Update to 41.2

* Fri Oct 29 2021 Milan Crha <mcrha@redhat.com> - 41.1-1
- Update to 41.1

* Tue Oct 19 2021 Milan Crha <mcrha@redhat.com> - 41.0-6
- Resolves: #2012863 (gs-installed-page: Change section on application state change)

* Mon Oct 11 2021 Milan Crha <mcrha@redhat.com> - 41.0-5
- Add patch to mark compulsory only repos, not apps from it

* Fri Oct 08 2021 Milan Crha <mcrha@redhat.com> - 41.0-4
- Resolves: #2011176 (flathub repo can't be added through gnome-software)
- Resolves: #2010660 (gs-repos-dialog: Can show also desktop applications)
- Resolves: #2010353 (Optional repos cannot be disabled)

* Thu Oct 07 2021 Milan Crha <mcrha@redhat.com> - 41.0-3
- Resolves: #2010740 (Refresh on repository setup change)

* Mon Oct 04 2021 Milan Crha <mcrha@redhat.com> - 41.0-2
- Resolves: #2009063 (Correct update notifications)

* Mon Sep 20 2021 Milan Crha <mcrha@redhat.com> - 41.0-1
- Update to 41.0

* Mon Sep 13 2021 Milan Crha <mcrha@redhat.com> - 41~rc-2
- Resolves: #2003365 (packagekit: Ensure PkClient::interactive flag being set)

* Wed Sep 08 2021 Milan Crha <mcrha@redhat.com> - 41~rc-1
- Update to 41.rc

* Wed Sep 01 2021 Milan Crha <mcrha@redhat.com> - 41~beta-3
- Resolves: #1995817 (gs-updates-section: Check also dependencies' download size)

* Tue Aug 24 2021 Kalev Lember <klember@redhat.com> - 41~beta-2
- Enable parental controls support

* Fri Aug 13 2021 Milan Crha <mcrha@redhat.com> - 41~beta-1
- Update to 41.beta

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 41~alpha-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jul 21 2021 Milan Crha <mcrha@redhat.com> - 41~alpha-1
- Update to 41.alpha

* Mon Jul 12 2021 Milan Crha <mcrha@redhat.com> - 40.3-2
- Add rpm-ostree patch to hide packages from the search results
- Add patch to implement what-provides search in the Flatpak plugin

* Mon Jul 12 2021 Milan Crha <mcrha@redhat.com> - 40.3-1
- Update to 40.3

* Wed Jun 23 2021 Milan Crha <mcrha@redhat.com> - 40.2-2
- Add patch to automatically install application updates (i#1248)

* Fri Jun 04 2021 Milan Crha <mcrha@redhat.com> - 40.2-1
- Update to 40.2

* Mon May 03 2021 Milan Crha <mcrha@redhat.com> - 40.1-2
- Add patch for crash under gs_details_page_refresh_all() (i#1227)

* Mon May 03 2021 Milan Crha <mcrha@redhat.com> - 40.1-1
- Update to 40.1

* Fri Mar 26 2021 Kalev Lember <klember@redhat.com> - 40.0-2
- Rebuild to fix sysprof-capture symbols leaking into libraries consuming it

* Mon Mar 22 2021 Kalev Lember <klember@redhat.com> - 40.0-1
- Update to 40.0

* Thu Mar 18 2021 Adam Williamson <awilliam@redhat.com> - 40~rc-2
- Backport a couple of bug fixes from upstream (icon display, crash bug)

* Mon Mar 15 2021 Kalev Lember <klember@redhat.com> - 40~rc-1
- Update to 40.rc

* Wed Mar 10 2021 Adam Williamson <awilliam@redhat.com> - 40~beta-2
- Backport MR #643 to fix update notifications on first run (#1930401)

* Tue Feb 16 2021 Kalev Lember <klember@redhat.com> - 40~beta-1
- Update to 40.beta

* Mon Feb 08 2021 Richard Hughes <richard@hughsie.com> - 3.38.1-1
- New upstream version
- Fix package details not found for some packages
- Ignore harmless warnings when using unusual fwupd versions

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.38.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Sep 14 2020 Kalev Lember <klember@redhat.com> - 3.38.0-2
- Revert an optimization that broke packagekit updates

* Fri Sep 11 2020 Kalev Lember <klember@redhat.com> - 3.38.0-1
- Update to 3.38.0

* Tue Sep 01 2020 Kalev Lember <klember@redhat.com> - 3.37.92-1
- Update to 3.37.92

* Tue Aug 18 2020 Richard Hughes <richard@hughsie.com> - 3.36.1-4
- Rebuild for the libxmlb API bump.

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.36.1-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.36.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri May 22 2020 Richard Hughes <rhughes@redhat.com> - 3.36.1-1
- Update to 3.36.1

* Tue May 12 2020 Kalev Lember <klember@redhat.com> - 3.36.0-2
- Backport various rpm-ostree backend fixes

* Wed Mar 11 2020 Kalev Lember <klember@redhat.com> - 3.36.0-1
- Update to 3.36.0

* Wed Mar 04 2020 Kalev Lember <klember@redhat.com> - 3.35.92-1
- Update to 3.35.92

* Fri Feb 21 2020 Richard Hughes <rhughes@redhat.com> - 3.35.91-2
- Backport a patch to fix a crash when looking at the application details.

* Wed Feb 19 2020 Richard Hughes <rhughes@redhat.com> - 3.35.91-1
- Update to 3.35.91.

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.35.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Nov 25 2019 Richard Hughes <rhughes@redhat.com> - 3.35.2-1
- Update to 3.35.2.

* Fri Oct 18 2019 Kalev Lember <klember@redhat.com> - 3.34.1-6
- Backport patches to fix a crash in gs_flatpak_get_installation (#1762689)

* Mon Oct 14 2019 Kalev Lember <klember@redhat.com> - 3.34.1-5
- Update renamed appstream ids for GNOME 3.34

* Fri Oct 11 2019 Richard Hughes <rhughes@redhat.com> - 3.34.1-4
- Backport a simpler to correct the installed applications
- Resolves #1759193

* Fri Oct 11 2019 Richard Hughes <rhughes@redhat.com> - 3.34.1-3
- Backport a better patch to correct the installed applications
- Resolves #1759193

* Thu Oct 10 2019 Richard Hughes <rhughes@redhat.com> - 3.34.1-2
- Backport a patch to correct the applications shown in the installed list
- Resolves #1759193

* Mon Oct 07 2019 Kalev Lember <klember@redhat.com> - 3.34.1-1
- Update to 3.34.1

* Wed Sep 25 2019 Kalev Lember <klember@redhat.com> - 3.34.0-2
- Fix third party repo enabling not working (#1749566)

* Mon Sep 09 2019 Kalev Lember <klember@redhat.com> - 3.34.0-1
- Update to 3.34.0

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.32.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jul 11 2019 Kalev Lember <klember@redhat.com> - 3.32.4-1
- Update to 3.32.4

* Thu Jul 11 2019 Richard Hughes <rhughes@redhat.com> - 3.32.3-5
- Disable the snap plugin. Canonical upstream are not going to be installing
  gnome-software in the next LTS, prefering instead to ship a "Snap Store"
  rather than GNOME Software.
- Enabling the snap plugin also enables the Snap Store which violated the same
  rules which prevented us installing Flathub by default.
- The existing plugin is barely maintained and I don't want to be the one
  responsible when it breaks.

* Thu Jun 13 2019 Kalev Lember <klember@redhat.com> - 3.32.3-4
- Rebuild for accidental libflatpak ABI break

* Mon Jun 10 22:13:19 CET 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.32.3-3
- Rebuild for RPM 4.15

* Mon Jun 10 15:42:01 CET 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.32.3-2
- Rebuild for RPM 4.15

* Fri May 24 2019 Kalev Lember <klember@redhat.com> - 3.32.3-1
- Update to 3.32.3

* Tue May 07 2019 Kalev Lember <klember@redhat.com> - 3.32.2-1
- Update to 3.32.2

* Fri May 03 2019 Kalev Lember <klember@redhat.com> - 3.32.1-4
- Update a patch to final upstream version

* Tue Apr 30 2019 Kalev Lember <klember@redhat.com> - 3.32.1-3
- Backport a number of rpm-ostree fixes

* Tue Apr 16 2019 Adam Williamson <awilliam@redhat.com> - 3.32.1-2
- Rebuild with Meson fix for #1699099

* Mon Apr 15 2019 Kalev Lember <klember@redhat.com> - 3.32.1-1
- Update to 3.32.1

* Fri Apr 05 2019 Neal Gompa <ngompa13@gmail.com> - 3.32.0-6
- Require snapd instead of the obsolete snapd-login-service for snap subpackage

* Wed Apr 03 2019 Kalev Lember <klember@redhat.com> - 3.32.0-5
- Switch to system libdnf

* Fri Mar 29 2019 Kalev Lember <klember@redhat.com> - 3.32.0-4
- Rebuild for new rpm-ostree

* Fri Mar 15 2019 Kalev Lember <klember@redhat.com> - 3.32.0-3
- Add nm-connection-editor.desktop to Utilities folder (#1686851)

* Tue Mar 12 2019 Kalev Lember <klember@redhat.com> - 3.32.0-2
- Backport a patch to add shadows to app icons

* Mon Mar 11 2019 Kalev Lember <klember@redhat.com> - 3.32.0-1
- Update to 3.32.0

* Tue Mar 05 2019 Kalev Lember <klember@redhat.com> - 3.31.92-1
- Update to 3.31.92

* Thu Feb 28 2019 Kalev Lember <klember@redhat.com> - 3.31.90-4
- Change PackageKit requires to recommends

* Wed Feb 27 2019 Kalev Lember <klember@redhat.com> - 3.31.90-3
- Remove unneeded dpkg plugin

* Mon Feb 25 2019 Kalev Lember <klember@redhat.com> - 3.31.90-2
- Split rpm-ostree backend to its own subpackage

* Sun Feb 24 2019 Kalev Lember <klember@redhat.com> - 3.31.90-1
- Update to 3.31.90
- Add "anaconda" repo to official repos list (#1679693)

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.31.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 16 2019 Kalev Lember <klember@redhat.com> - 3.31.2-1
- Update to 3.31.2

* Fri Dec 14 2018 Kalev Lember <klember@redhat.com> - 3.31.1-2
- Fix offline update notifications to show up (#1659231)

* Tue Oct 09 2018 Kalev Lember <klember@redhat.com> - 3.31.1-1
- Update to 3.31.1

* Fri Oct 05 2018 Kalev Lember <klember@redhat.com> - 3.30.2-1
- Update to 3.30.2

* Wed Sep 26 2018 Kalev Lember <klember@redhat.com> - 3.30.1-2
- Add modular repos to official repos list

* Tue Sep 25 2018 Kalev Lember <klember@redhat.com> - 3.30.1-1
- Update to 3.30.1

* Thu Sep 06 2018 Kalev Lember <klember@redhat.com> - 3.30.0-1
- Update to 3.30.0

* Tue Aug 28 2018 Richard Hughes <rhughes@redhat.com> - 3.29.92-1
- Update to 3.29.92

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.29.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed May 09 2018 Kalev Lember <klember@redhat.com> - 3.29.1-1
- Update to 3.29.1

* Mon Apr 09 2018 Kalev Lember <klember@redhat.com> - 3.28.1-1
- Update to 3.28.1

* Thu Mar 29 2018 Kalev Lember <klember@redhat.com> - 3.28.0-5
- Fix empty OS Updates showing up
- Make rpm-ostree update triggering work

* Thu Mar 15 2018 Kalev Lember <klember@redhat.com> - 3.28.0-4
- Fix opening results from gnome-shell search provider

* Wed Mar 14 2018 Kalev Lember <klember@redhat.com> - 3.28.0-3
- Fix crash on initial run with no network (#1554986)

* Tue Mar 13 2018 Kalev Lember <klember@redhat.com> - 3.28.0-2
- Backport an upstream patch to fix shell extensions app ID

* Mon Mar 12 2018 Kalev Lember <klember@redhat.com> - 3.28.0-1
- Update to 3.28.0

* Sun Mar 11 2018 Kalev Lember <klember@redhat.com> - 3.27.92-3
- Rebuilt for gspell 1.8

* Wed Mar 07 2018 Kalev Lember <klember@redhat.com> - 3.27.92-2
- Move org.gnome.Software.Featured.xml from -editor to main package

* Mon Mar 05 2018 Kalev Lember <klember@redhat.com> - 3.27.92-1
- Update to 3.27.92

* Sun Mar 04 2018 Neal Gompa <ngompa13@gmail.com> - 3.27.90-4
- Drop obsolete snapd-login-service requirement for snap plugin subpackage

* Mon Feb 19 2018 Adam Williamson <awilliam@redhat.com> - 3.27.90-3
- Backport fix for RHBZ #1546893 from upstream git

* Mon Feb 19 2018 Kalev Lember <klember@redhat.com> - 3.27.90-2
- Re-enable rpm-ostree plugin

* Thu Feb 15 2018 Kalev Lember <klember@redhat.com> - 3.27.90-1
- Update to 3.27.90
- Temporarily disable the rpm-ostree plugin

* Tue Feb 13 2018 Björn Esser <besser82@fedoraproject.org> - 3.27.4-4
- Rebuild against newer gnome-desktop3 package

* Thu Feb 08 2018 Kalev Lember <klember@redhat.com> - 3.27.4-3
- Add fedora-workstation-repositories to nonfree-sources schema defaults

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.27.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Jan 08 2018 Kalev Lember <klember@redhat.com> - 3.27.4-1
- Update to 3.27.4
- Drop unused --without packagekit option

* Fri Jan 05 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.27.3-2
- Remove obsolete scriptlets

* Sat Dec 16 2017 Kalev Lember <klember@redhat.com> - 3.27.3-1
- Update to 3.27.3

* Mon Nov 13 2017 Kalev Lember <klember@redhat.com> - 3.27.2-1
- Update to 3.27.2

* Thu Nov 09 2017 Kalev Lember <klember@redhat.com> - 3.26.2-1
- Update to 3.26.2
- Re-enable fwupd support

* Tue Oct 31 2017 Kalev Lember <klember@redhat.com> - 3.26.1-5
- Enable the rpm-ostree plugin

* Wed Oct 25 2017 Kalev Lember <klember@redhat.com> - 3.26.1-4
- Fix "too many results returned" error after distro upgrades (#1496489)

* Tue Oct 10 2017 Kalev Lember <klember@redhat.com> - 3.26.1-3
- Backport a flatpakref installation fix

* Mon Oct 09 2017 Richard Hughes <rhughes@redhat.com> - 3.26.1-2
- Disable fwupd support until we get a 3.27.1 tarball

* Sun Oct 08 2017 Kalev Lember <klember@redhat.com> - 3.26.1-1
- Update to 3.26.1

* Mon Sep 11 2017 Kalev Lember <klember@redhat.com> - 3.26.0-1
- Update to 3.26.0

* Sun Aug 27 2017 Kalev Lember <klember@redhat.com> - 3.25.91-1
- Update to 3.25.91

* Tue Aug 15 2017 Kalev Lember <klember@redhat.com> - 3.25.90-1
- Update to 3.25.90

* Fri Aug 11 2017 Igor Gnatenko <ignatenko@redhat.com> - 3.25.4-6
- Rebuilt after RPM update (№ 3)

* Thu Aug 10 2017 Igor Gnatenko <ignatenko@redhat.com> - 3.25.4-5
- Rebuilt for RPM soname bump

* Thu Aug 10 2017 Igor Gnatenko <ignatenko@redhat.com> - 3.25.4-4
- Rebuilt for RPM soname bump

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.25.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.25.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jul 21 2017 Kalev Lember <klember@redhat.com> - 3.25.4-1
- Update to 3.25.4

* Tue Jul 18 2017 Kalev Lember <klember@redhat.com> - 3.25.3-6
- Drop a meson workaround now that meson is fixed

* Wed Jun 28 2017 Neal Gompa <ngompa13@gmail.com> - 3.25.3-5
- Actually properly enable snap subpackage after removing conditional

* Wed Jun 28 2017 Neal Gompa <ngompa13@gmail.com> - 3.25.3-4
- Remove unnecessary arch-specific conditional for snap subpackage

* Tue Jun 27 2017 Neal Gompa <ngompa13@gmail.com> - 3.25.3-3
- Ensure snap subpackage is installed if snapd is installed

* Fri Jun 23 2017 Richard Hughes <rhughes@redhat.com> - 3.24.3-2
- Enable the snap subpackage

* Fri Jun 23 2017 Kalev Lember <klember@redhat.com> - 3.25.3-1
- Update to 3.25.3
- Switch to the meson build system
- Add an -editor subpackage with new banner editor

* Mon May 15 2017 Richard Hughes <rhughes@redhat.com> - 3.24.3-1
- Update to 3.23.3
- Fix a common crash when installing flatpakrepo files
- Ensure we show the banner when upgrades are available

* Tue May 09 2017 Kalev Lember <klember@redhat.com> - 3.24.2-1
- Update to 3.24.2

* Tue Apr 25 2017 Adam Williamson <awilliam@redhat.com> - 3.24.1-2
- Backport crasher fix from upstream (RHBZ #1444669 / BGO #781217)

* Tue Apr 11 2017 Kalev Lember <klember@redhat.com> - 3.24.1-1
- Update to 3.24.1

* Tue Mar 21 2017 Kalev Lember <klember@redhat.com> - 3.24.0-1
- Update to 3.24.0

* Thu Mar 16 2017 Kalev Lember <klember@redhat.com> - 3.23.92-1
- Update to 3.23.92

* Mon Feb 27 2017 Richard Hughes <rhughes@redhat.com> - 3.23.91-1
- Update to 3.23.91

* Mon Feb 13 2017 Richard Hughes <rhughes@redhat.com> - 3.23.90-1
- Update to 3.23.90

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.23.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Dec 15 2016 Richard Hughes <rhughes@redhat.com> - 3.23.3-1
- Update to 3.23.3

* Wed Nov 23 2016 Kalev Lember <klember@redhat.com> - 3.23.2-1
- Update to 3.23.2

* Tue Nov 08 2016 Kalev Lember <klember@redhat.com> - 3.22.2-1
- Update to 3.22.2

* Wed Oct 12 2016 Kalev Lember <klember@redhat.com> - 3.22.1-1
- Update to 3.22.1

* Mon Sep 19 2016 Kalev Lember <klember@redhat.com> - 3.22.0-1
- Update to 3.22.0

* Wed Sep 14 2016 Kalev Lember <klember@redhat.com> - 3.21.92-1
- Update to 3.21.92
- Don't set group tags

* Thu Sep 01 2016 Kalev Lember <klember@redhat.com> - 3.21.91-1
- Update to 3.21.91

* Wed Aug 17 2016 Kalev Lember <klember@redhat.com> - 3.21.90-2
- Rebuilt for fixed libappstream-glib headers

* Wed Aug 17 2016 Kalev Lember <klember@redhat.com> - 3.21.90-1
- Update to 3.21.90
- Tighten -devel subpackage dependencies

* Thu Jul 28 2016 Richard Hughes <rhughes@redhat.com> - 3.21.4-2
- Allow building without PackageKit for the atomic workstation.

* Mon Jul 18 2016 Richard Hughes <rhughes@redhat.com> - 3.21.4-1
- Update to 3.21.4

* Thu May 26 2016 Kalev Lember <klember@redhat.com> - 3.21.2-2
- Build with flatpak support

* Mon May 23 2016 Richard Hughes <rhughes@redhat.com> - 3.21.2-1
- Update to 3.21.2

* Tue May 10 2016 Kalev Lember <klember@redhat.com> - 3.21.1-2
- Require PackageKit 1.1.1 for system upgrade support

* Mon Apr 25 2016 Richard Hughes <rhughes@redhat.com> - 3.21.1-1
- Update to 3.21.1

* Mon Apr 25 2016 Richard Hughes <rhughes@redhat.com> - 3.20.2-1
- Update to 3.20.1
- Allow popular and featured apps to match any plugin
- Do not make the ODRS plugin depend on xdg-app
- Fix many of the os-upgrade issues and implement the latest mockups
- Make all the plugins more threadsafe
- Return all update descriptions newer than the installed version
- Show some non-fatal error messages if installing fails
- Use a background PackageKit transaction when downloading upgrades

* Wed Apr 13 2016 Kalev Lember <klember@redhat.com> - 3.20.1-1
- Update to 3.20.1

* Fri Apr 01 2016 Richard Hughes <rhughes@redhat.com> - 3.20.1-2
- Set the list of official sources
- Compile with xdg-app support

* Tue Mar 22 2016 Kalev Lember <klember@redhat.com> - 3.20.0-1
- Update to 3.20.0

* Mon Mar 14 2016 Richard Hughes <rhughes@redhat.com> - 3.19.92-1
- Update to 3.19.92

* Thu Mar 03 2016 Kalev Lember <klember@redhat.com> - 3.19.91-2
- Set minimum required json-glib version

* Mon Feb 29 2016 Richard Hughes <rhughes@redhat.com> - 3.19.91-1
- Update to 3.19.91

* Mon Feb 15 2016 Richard Hughes <rhughes@redhat.com> - 3.19.90-1
- Update to 3.19.90

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.19.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan 15 2016 Richard Hughes <rhughes@redhat.com> - 3.19.4-1
- Update to 3.19.4

* Thu Dec 03 2015 Kalev Lember <klember@redhat.com> - 3.18.3-2
- Require librsvg2 for the gdk-pixbuf svg loader

* Thu Nov 05 2015 Richard Hughes <rhughes@redhat.com> - 3.18.3-1
- Update to 3.18.3
- Use the correct user agent string when downloading firmware
- Fix a crash in the limba plugin
- Fix installing web applications

* Mon Oct 26 2015 Kalev Lember <klember@redhat.com> - 3.18.2-2
- Fix apps reappearing as installed a few seconds after removal (#1275163)

* Thu Oct 15 2015 Kalev Lember <klember@redhat.com> - 3.18.2-1
- Update to 3.18.2

* Tue Oct 13 2015 Kalev Lember <klember@redhat.com> - 3.18.1-1
- Update to 3.18.1

* Wed Oct 07 2015 Kalev Lember <klember@redhat.com> - 3.18.0-2
- Backport two crasher fixes from upstream

* Mon Sep 21 2015 Kalev Lember <klember@redhat.com> - 3.18.0-1
- Update to 3.18.0

* Tue Sep 15 2015 Kalev Lember <klember@redhat.com> - 3.17.92-2
- Update dependency versions

* Tue Sep 15 2015 Richard Hughes <rhughes@redhat.com> - 3.17.92-1
- Update to 3.17.92

* Thu Sep 10 2015 Richard Hughes <rhughes@redhat.com> - 3.17.91-2
- Fix firmware updates

* Thu Sep 03 2015 Kalev Lember <klember@redhat.com> - 3.17.91-1
- Update to 3.17.91

* Wed Aug 19 2015 Kalev Lember <klember@redhat.com> - 3.17.90-1
- Update to 3.17.90

* Wed Aug 12 2015 Richard Hughes <rhughes@redhat.com> - 3.17.3-1
- Update to 3.17.3

* Wed Jul 22 2015 David King <amigadave@amigadave.com> - 3.17.2-3
- Bump for new gnome-desktop3

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.17.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Kalev Lember <kalevlember@gmail.com> - 3.17.2-1
- Update to 3.17.2

* Mon May 25 2015 Kalev Lember <kalevlember@gmail.com> - 3.17.1-1
- Update to 3.17.1

* Fri May 15 2015 Kalev Lember <kalevlember@gmail.com> - 3.16.2-2
- Fix a crash under Wayland (#1221968)

* Mon May 11 2015 Kalev Lember <kalevlember@gmail.com> - 3.16.2-1
- Update to 3.16.2

* Tue Apr 14 2015 Kalev Lember <kalevlember@gmail.com> - 3.16.1-1
- Update to 3.16.1

* Mon Mar 23 2015 Kalev Lember <kalevlember@gmail.com> - 3.16.0-1
- Update to 3.16.0

* Mon Mar 16 2015 Kalev Lember <kalevlember@gmail.com> - 3.15.92-1
- Update to 3.15.92
- Use license macro for the COPYING file
- Add a patch to adapt to gnome-terminal desktop file rename

* Mon Mar 02 2015 Kalev Lember <kalevlember@gmail.com> - 3.15.91-1
- Update to 3.15.91

* Sat Feb 21 2015 Kalev Lember <kalevlember@gmail.com> - 3.15.90-3
- Export DisplayName property on the packagekit session service

* Thu Feb 19 2015 Kalev Lember <kalevlember@gmail.com> - 3.15.90-2
- Backport a crash fix

* Tue Feb 17 2015 Richard Hughes <rhughes@redhat.com> - 3.15.90-1
- Update to 3.15.90

* Mon Jan 19 2015 Richard Hughes <rhughes@redhat.com> - 3.15.4-1
- Update to 3.15.4

* Tue Nov 25 2014 Kalev Lember <kalevlember@gmail.com> - 3.15.2-1
- Update to 3.15.2

* Thu Nov 13 2014 Richard Hughes <rhughes@redhat.com> - 3.14.2-3
- Fix non-Fedora build

* Tue Nov 11 2014 Richard Hughes <rhughes@redhat.com> - 3.14.2-2
- Backport a patch to fix compilation

* Mon Nov 10 2014 Kalev Lember <kalevlember@gmail.com> - 3.14.2-1
- Update to 3.14.2

* Sat Nov 08 2014 Kalev Lember <kalevlember@gmail.com> - 3.14.1-3
- Update the list of system apps

* Sat Nov 01 2014 David King <amigadave@amigadave.com> - 3.14.1-2
- Rebuild for new libappstream-glib (#1156494)

* Mon Oct 13 2014 Kalev Lember <kalevlember@gmail.com> - 3.14.1-1
- Update to 3.14.1

* Thu Oct 09 2014 Kalev Lember <kalevlember@gmail.com> - 3.14.0-2
- Depend on gnome-menus for app folder directory entries

* Mon Sep 22 2014 Kalev Lember <kalevlember@gmail.com> - 3.14.0-1
- Update to 3.14.0

* Wed Sep 17 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.92-2
- Set minimum required dependency versions (#1136343)

* Tue Sep 16 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.92-1
- Update to 3.13.92
- Replace gnome-system-log with gnome-logs in the system apps list

* Tue Sep 02 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.91-1
- Update to 3.13.91

* Tue Aug 19 2014 Richard Hughes <rhughes@redhat.com> - 3.13.90-1
- Update to 3.13.90

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.13.5-0.2.git5c89189
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Aug 11 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.5-0.1.git5c89189
- Update to 3.13.5 git snapshot
- Ship HighContrast icons

* Sun Aug 03 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.4-2
- Replace Epiphany with Firefox in the system apps list

* Wed Jul 23 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.4-1
- Update to 3.13.4

* Wed Jun 25 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.3-1
- Update to 3.13.3

* Thu Jun 12 2014 Richard Hughes <rhughes@redhat.com> - 3.13.3-0.2.git7491627
- Depend on the newly-created appstream-data package and stop shipping
  the metadata here.

* Sat Jun 07 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.3-0.1.git7491627
- Update to 3.13.3 git snapshot

* Wed May 28 2014 Richard Hughes <rhughes@redhat.com> - 3.13.2-2
- Rebuild with new metadata.

* Wed May 28 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.2-1
- Update to 3.13.2

* Thu May 15 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.1-4
- Depend on gsettings-desktop-schemas

* Mon May 12 2014 Richard Hughes <rhughes@redhat.com> - 3.13.1-3
- Update the metadata and use appstream-util to install the metadata.

* Wed May 07 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.1-2
- Drop gnome-icon-theme dependency

* Mon Apr 28 2014 Richard Hughes <rhughes@redhat.com> - 3.13.1-1
- Update to 3.13.1

* Fri Apr 11 2014 Kalev Lember <kalevlember@gmail.com> - 3.12.1-2
- Rebuild with new metadata.

* Fri Apr 11 2014 Richard Hughes <rhughes@redhat.com> - 3.12.1-1
- Update to 3.12.1

* Mon Mar 24 2014 Richard Hughes <rhughes@redhat.com> - 3.12.0-1
- Update to 3.12.0

* Thu Mar 20 2014 Richard Hughes <rhughes@redhat.com> - 3.11.92-1
- Update to 3.11.92

* Tue Mar 18 2014 Richard Hughes <rhughes@redhat.com> - 3.11.91-2
- Rebuild with new metadata.

* Sat Mar 08 2014 Richard Hughes <rhughes@redhat.com> - 3.11.91-1
- Update to 3.11.91

* Tue Feb 18 2014 Richard Hughes <rhughes@redhat.com> - 3.11.90-1
- Update to 3.11.90

* Mon Feb 03 2014 Richard Hughes <rhughes@redhat.com> - 3.11.5-2
- Require epiphany-runtime rather than the full application

* Mon Feb 03 2014 Richard Hughes <rhughes@redhat.com> - 3.11.5-1
- Update to 3.11.5

* Thu Jan 30 2014 Richard Hughes <rhughes@redhat.com> - 3.11.4-3
- Rebuild for libpackagekit-glib soname bump

* Wed Jan 22 2014 Richard Hughes <rhughes@redhat.com> - 3.11.4-2
- Rebuild with metadata that has the correct screenshot url.

* Thu Jan 16 2014 Richard Hughes <rhughes@redhat.com> - 3.11.4-1
- Update to 3.11.4

* Tue Dec 17 2013 Richard Hughes <rhughes@redhat.com> - 3.11.3-1
- Update to 3.11.3

* Tue Nov 19 2013 Richard Hughes <rhughes@redhat.com> - 3.11.2-1
- Update to 3.11.2

* Tue Oct 29 2013 Richard Hughes <rhughes@redhat.com> - 3.11.1-1
- Update to 3.11.1
- Add a gnome shell search provider
- Add a module to submit the user rating to the fedora-tagger web service
- Add support for 'missing' codecs that we know exist but we can't install
- Add support for epiphany web applications
- Handle offline installation sensibly
- Save the user rating if the user clicks the rating stars
- Show a modal error message if install or remove actions failed
- Show a star rating on the application details page
- Show font screenshots
- Show more detailed version numbers when required
- Show screenshots to each application

* Wed Sep 25 2013 Richard Hughes <richard@hughsie.com> 3.10.0-1
- New upstream release.
- New metadata for fedora, updates and updates-testing
- Add a plugin to query the PackageKit prepared-update file directly
- Do not clear the offline-update trigger if rebooting succeeded
- Do not load incompatible projects when parsing AppStream data
- Lots of updated translations
- Show the window right away when starting

* Fri Sep 13 2013 Richard Hughes <richard@hughsie.com> 3.9.3-1
- New upstream release.
- Lots of new and fixed UI and updated metadata for Fedora 20

* Tue Sep 03 2013 Richard Hughes <richard@hughsie.com> 3.9.2-1
- New upstream release.
- Allow stock items in the AppStream XML
- Extract the AppStream URL and description from the XML
- Only present the window when the overview is complete
- Return the subcategories sorted by name

* Mon Sep 02 2013 Richard Hughes <richard@hughsie.com> 3.9.1-1
- New upstream release which is a technical preview for the alpha.

* Sun Sep 01 2013 Richard Hughes <richard@hughsie.com> 0.1-3
- Use buildroot not RPM_BUILD_ROOT
- Own all gnome-software directories
- Drop gtk-update-icon-cache requires and the mime database functionality

* Thu Aug 29 2013 Richard Hughes <richard@hughsie.com> 0.1-2
- Add call to desktop-file-validate and fix other review comments.

* Wed Aug 28 2013 Richard Hughes <richard@hughsie.com> 0.1-1
- First release for Fedora package review

