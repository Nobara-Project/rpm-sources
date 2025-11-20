%global appstream_version 0.16.4
%global flatpak_version 1.14.1
%global fwupd_version 1.6.2
%global glib2_version 2.76.0
%global gtk4_version 4.16.0
%global json_glib_version 1.6.0
%global libadwaita_version 1.6.0
%global libxmlb_version 0.3.4
%global packagekit_version 1.2.5
%global dnf5_version 5.2.16

# Disable WebApps for RHEL builds
%bcond webapps %[!0%{?rhel}]
# Disable parental control for RHEL builds
%bcond malcontent %[!0%{?rhel}]
# Disable rpm-ostree support for RHEL builds
%bcond rpmostree %[!0%{?rhel}]
# Disable DKMS/akmods support for RHEL builds
%bcond dkms %[!0%{?rhel}]

%bcond packagekit 0
%bcond dnf5 0

# this is not a library version
%define gs_plugin_version 23

%global tarball_version %%(echo %{version} | tr '~' '.')

%global __provides_exclude_from ^%{_libdir}/%{name}/plugins-%{gs_plugin_version}/.*\\.so.*$

Name:      gnome-software
Version:   49.1
Release:   1%{?dist}
Summary:   A software center for GNOME

License:   GPL-2.0-or-later
URL:       https://apps.gnome.org/Software
Source0:   https://download.gnome.org/sources/gnome-software/49/%{name}-%{tarball_version}.tar.xz

%if %{with dnf5}
# to update the patch enter the ./dnf5-plugin/ directory and run from
# it the ./update-patch.sh script
Patch:     0001-dnf5-plugin.patch
%endif

# ostree and flatpak not on i686 for Fedora and RHEL 10
# https://github.com/containers/composefs/pull/229#issuecomment-1838735764
%if 0%{?fedora} || 0%{?rhel} >= 10
ExcludeArch:    %{ix86}
%endif

BuildRequires: docbook-style-xsl
BuildRequires: desktop-file-utils
BuildRequires: gcc
BuildRequires: gettext
BuildRequires: git-core
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
%if %{with packagekit}
BuildRequires: pkgconfig(packagekit-glib2) >= %{packagekit_version}
%endif
BuildRequires: pkgconfig(polkit-gobject-1)
BuildRequires: pkgconfig(rpm)
%if %{with rpmostree}
BuildRequires: pkgconfig(rpm-ostree-1)
%endif
BuildRequires: pkgconfig(sysprof-capture-4)
BuildRequires: pkgconfig(xmlb) >= %{libxmlb_version}
BuildRequires: systemd

Requires: appstream-data
Requires: appstream%{?_isa} >= %{appstream_version}
%if %{with webapps}
Requires: epiphany-runtime%{?_isa}
%endif
%if %{with dnf5}
Requires: dnf5daemon-server%{?_isa} >= %{dnf5_version}
Requires: dnf5daemon-server-polkit
Requires: libdnf5-plugin-appstream%{?_isa}
Requires: rpm-plugin-dbus-announce%{?_isa}
%endif
Requires: flatpak%{?_isa} >= %{flatpak_version}
Requires: flatpak-libs%{?_isa} >= %{flatpak_version}
Requires: fwupd%{?_isa} >= %{fwupd_version}
Requires: glib2%{?_isa} >= %{glib2_version}
%if !0%{?rhel}
Requires: gnome-app-list
%endif
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

%if %{with packagekit}
Recommends: PackageKit%{?_isa} >= %{packagekit_version}
%endif
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
    -Dsnap=false \
%if %{with malcontent}
    -Dmalcontent=true \
%else
    -Dmalcontent=false \
%endif
    -Dgudev=true \
%if %{with packagekit}
    -Dpackagekit=true \
    -Dpackagekit_autoremove=true \
%else
    -Dpackagekit=false \
%endif
%if %{with dnf5}
    -Ddnf5=true \
%endif
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
%if %{with packagekit} || %{with rpmostree} || %{with dnf5}
%{_datadir}/applications/gnome-software-local-file-packagekit.desktop
%endif
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
%if %{with dnf5}
%{_libdir}/gnome-software/plugins-%{gs_plugin_version}/libgs_plugin_dnf5.so
%endif
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
%if %{with packagekit}
%{_libdir}/gnome-software/plugins-%{gs_plugin_version}/libgs_plugin_packagekit.so
%endif
%{_libdir}/gnome-software/plugins-%{gs_plugin_version}/libgs_plugin_provenance-license.so
%{_libdir}/gnome-software/plugins-%{gs_plugin_version}/libgs_plugin_provenance.so
%{_libdir}/gnome-software/plugins-%{gs_plugin_version}/libgs_plugin_repos.so
%if %{with webapps}
%dir %{_datadir}/swcatalog
%dir %{_datadir}/swcatalog/xml
%{_datadir}/swcatalog/xml/gnome-pwa-list-foss.xml
%endif
%if %{with packagekit}
%{_datadir}/dbus-1/services/org.freedesktop.PackageKit.service
%endif
%{_datadir}/dbus-1/services/org.gnome.Software.service
%{_datadir}/gnome-shell/search-providers/org.gnome.Software-search-provider.ini
%{_datadir}/glib-2.0/schemas/org.gnome.software.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.software-fedora.gschema.override
%{_libexecdir}/gnome-software-cmd
%{_libexecdir}/gnome-software-restarter
%{_userunitdir}/gnome-software.service

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
## START: Generated by rpmautospec
* Fri Oct 10 2025 Milan Crha <mcrha@redhat.com> - 49.1-1
- Update to 49.1

* Fri Sep 19 2025 Milan Crha <mcrha@redhat.com> - 49.0-2
- Resolves: #2395811 (Packages not found for "what-provides" searches)

* Fri Sep 12 2025 Milan Crha <mcrha@redhat.com> - 49.0-1
- Update to 49.0

* Fri Sep 05 2025 Milan Crha <mcrha@redhat.com> - 49~rc-3
- Resolves: #2392645 (Use PackageKit plugin instead of dnf5 plugin)

* Mon Sep 01 2025 Milan Crha <mcrha@redhat.com> - 49~rc-2
- Resolves: #2392057 (dnf5-pugin: No update notifications shown)

* Fri Aug 29 2025 Milan Crha <mcrha@redhat.com> - 49~rc-1
- Update to 49.rc

* Tue Aug 26 2025 Milan Crha <mcrha@redhat.com> - 49~beta-6
- dnf5-plugin: Skip historical updates search when no last date is set

* Mon Aug 25 2025 Milan Crha <mcrha@redhat.com> - 49~beta-5
- dnf5-plugin: Auto-accept new RPM keys only when installed from repos
- dnf5-plugin: Download offline updates also by regular users

* Wed Aug 13 2025 Milan Crha <mcrha@redhat.com> - 49~beta-4
- dnf5-plugin: Auto-accept new RPM keys

* Mon Aug 11 2025 Milan Crha <mcrha@redhat.com> - 49~beta-3
- dnf5-pugin: Use 'interactive' option, where supported
- dnf5-plugin: Add support to provide update history

* Fri Aug 01 2025 Adam Williamson <awilliam@redhat.com> - 49~beta-2
- Move the user service file to the main package

* Fri Aug 01 2025 Milan Crha <mcrha@redhat.com> - 49~beta-1
- Update to 49.beta

* Fri Jul 25 2025 Milan Crha <mcrha@redhat.com> - 49~alpha-9
- Resolves: #2377094 (Update dnf5 plugin with fixes for rhbz#2377094)

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 49~alpha-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jul 04 2025 Yaakov Selkowitz <yselkowi@redhat.com> - 49~alpha-7
- Fix files list for RHEL builds

* Mon Jun 30 2025 Milan Crha <mcrha@redhat.com> - 49~alpha-6
- dnf5-plugin: Update script to generate patch to not depend on exact
  commit

* Mon Jun 30 2025 Milan Crha <mcrha@redhat.com> - 49~alpha-5
- Add script to update the dnf5-plugin patch

* Mon Jun 30 2025 Milan Crha <mcrha@redhat.com> - 49~alpha-4
- dnf5: Update the dnf5 plugin patch to match the latest upstream main
  branch

* Mon Jun 30 2025 Milan Crha <mcrha@redhat.com> - 49~alpha-3
- dnf5: Install 'gnome-software-local-file-packagekit.desktop' also for
  dnf5 plugin

* Fri Jun 27 2025 Milan Crha <mcrha@redhat.com> - 49~alpha-2
- Bump plugin API version

* Fri Jun 27 2025 Milan Crha <mcrha@redhat.com> - 49~alpha-1
- Update to 49.alpha

* Mon Jun 23 2025 Milan Crha <mcrha@redhat.com> - 48.2-2
- Switch %%autosetup from gendiff to git backups

* Mon Jun 02 2025 Milan Crha <mcrha@redhat.com> - 48.2-1
- Update to 48.2

* Mon Jun 02 2025 Milan Crha <mcrha@redhat.com> - 48.1-3
- Require dnf5daemon-server-polkit for the dnf5 plugin

* Tue Apr 29 2025 Milan Crha <mcrha@redhat.com> - 48.1-2
- Switch from PackageKit to DNF5 plugin

* Fri Apr 11 2025 Milan Crha <mcrha@redhat.com> - 48.1-1
- Update to 48.1

* Fri Mar 14 2025 Milan Crha <mcrha@redhat.com> - 48.0-1
- Update to 48.0

* Mon Mar 03 2025 Milan Crha <mcrha@redhat.com> - 48~rc-1
- Update to 48.rc

* Mon Feb 03 2025 Milan Crha <mcrha@redhat.com> - 48~beta-1
- Update to 48.beta

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 48~alpha3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Jan 14 2025 Milan Crha <mcrha@redhat.com> - 48~alpha3-1
- Update to 48.alpha3

* Tue Jan 07 2025 Milan Crha <mcrha@redhat.com> - 48~alpha2-1
- Update to 48.alpha2

* Mon Dec 09 2024 Milan Crha <mcrha@redhat.com> - 47.2-3
- Resolves: #2272232 (Crash under gs_appstream_gather_merge_data())

* Thu Dec 05 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 47.2-2
- Rebuild for fwupd 2.0

* Mon Nov 25 2024 Milan Crha <mcrha@redhat.com> - 47.2-1
- Update to 47.2

* Thu Oct 10 2024 Milan Crha <mcrha@redhat.com> - 47.1-1
- Update to 47.1

* Fri Oct 04 2024 Richard Hughes <richard@hughsie.com> - 47.0-4
- Rebuild against libfwupd.so.3

* Thu Sep 19 2024 Milan Crha <mcrha@redhat.com> - 47.0-3
- Resolves: #2312882 (dkms: Fix callback user data in a reload() function)

* Tue Sep 17 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 47.0-2
- Fix ELN build

* Fri Sep 13 2024 Milan Crha <mcrha@redhat.com> - 47.0-1
- Update to 47.0

* Fri Aug 30 2024 Milan Crha <mcrha@redhat.com> - 47~rc-1
- Update to 47.rc

* Fri Aug 02 2024 Milan Crha <mcrha@redhat.com> - 47~beta-2
- Build with DKMS/akmods plugin in Fedora

* Fri Aug 02 2024 Milan Crha <mcrha@redhat.com> - 47~beta-1
- Update to 47.beta

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 47~alpha-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 28 2024 Milan Crha <mcrha@redhat.com> - 47~alpha-1
- Update to 47.alpha

* Mon Jun 03 2024 Milan Crha <mcrha@redhat.com> - 46.2-2
- Build fedora-langpacks subpackage only in Fedora

* Fri May 24 2024 Milan Crha <mcrha@redhat.com> - 46.2-1
- Update to 46.2

* Wed May 08 2024 Hristo Marinov <hricky@mail.bg> - 46.1-2
- OSTree not on i686 for Fedora

* Thu Apr 25 2024 Milan Crha <mcrha@redhat.com> - 46.1-1
- Update to 46.1

* Fri Apr 12 2024 Adam Williamson <awilliam@redhat.com> - 46.0-3
- Backport MR #1949 to fix upgrading

* Wed Mar 27 2024 Milan Crha <mcrha@redhat.com> - 46.0-2
- Update URL to point to the new app page

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

* Tue Dec 19 2023 Troy Dawson <tdawson@redhat.com> - 45.2-2
- ostree and flatpak not on i686 for RHEL 10

* Fri Dec 01 2023 Milan Crha <mcrha@redhat.com> - 45.2-1
- Update to 45.2

* Tue Nov 07 2023 Neal Gompa <ngompa@fedoraproject.org> - 45.1-4
- Fix appstream_version macro for prerelease appstream 1.0 package

* Tue Nov 07 2023 Milan Crha <mcrha@redhat.com> - 45.1-3
- Require appstream version 1.0.0

* Tue Nov 07 2023 Milan Crha <mcrha@redhat.com> - 45.1-2
- Add patch to build with appstream 1.0

* Fri Oct 20 2023 Milan Crha <mcrha@redhat.com> - 45.1-1
- Update to 45.1

* Fri Sep 15 2023 Milan Crha <mcrha@redhat.com> - 45.0-1
- Update to 45.0

* Fri Sep 01 2023 Milan Crha <mcrha@redhat.com> - 45~rc-1
- Update to 45.rc

* Mon Jul 31 2023 Milan Crha <mcrha@redhat.com> - 45~beta-2
- Remove reference to a dropped plugin (it's builtin now)

* Mon Jul 31 2023 Milan Crha <mcrha@redhat.com> - 45~beta-1
- Update to 45.beta

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 45~alpha-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jun 30 2023 Milan Crha <mcrha@redhat.com> - 45~alpha-1
- Update to 45.alpha

* Thu Jun 22 2023 Tomas Popela <tpopela@redhat.com> - 44.2-3
- Fix a changelog typo

* Thu Jun 22 2023 Tomas Popela <tpopela@redhat.com> - 44.2-2
- Disable parental control (through malcontent) and rpm-ostree support in
  RHEL

* Fri May 26 2023 Milan Crha <mcrha@redhat.com> - 44.2-1
- Update to 44.2

* Fri May 19 2023 Milan Crha <mcrha@redhat.com> - 44.1-2
- Rebuild for RPM

* Fri Apr 21 2023 Milan Crha <mcrha@redhat.com> - 44.1-1
- Update to 44.1

* Mon Mar 27 2023 Milan Crha <mcrha@redhat.com> - 44.0-4
- Added 'flatpak:fedora-testing' into packaging-format-preference

* Sun Mar 26 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 44.0-3
- Fix libsoup runtime dependency

* Fri Mar 24 2023 Milan Crha <mcrha@redhat.com> - 44.0-2
- Resolves: #2181367 (Prefer Fedora Flatpaks before RPM before other
  sources for apps)

* Fri Mar 17 2023 Milan Crha <mcrha@redhat.com> - 44.0-1
- Update to 44.0

* Fri Mar 03 2023 Milan Crha <mcrha@redhat.com> - 44~rc-1
- Update to 44.rc

* Thu Feb 23 2023 Adam Williamson <awilliam@redhat.com> - 44~beta-2
- Backport MR #1635 to fix update notifications

* Tue Feb 14 2023 Milan Crha <mcrha@redhat.com> - 44~beta-1
- Update to 44.beta

* Thu Feb 09 2023 Michael Catanzaro <mcatanzaro@redhat.com> - 44~alpha-3
- Switch to libsoup 3

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 44~alpha-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Jan 09 2023 Milan Crha <mcrha@redhat.com> - 44~alpha-1
- Update to 44.alpha

* Fri Dec 02 2022 Milan Crha <mcrha@redhat.com> - 43.2-1
- Update to 43.2

* Thu Nov 10 2022 Milan Crha <mcrha@redhat.com> - 43.1-4
- Update License tag to SPDX

* Tue Nov 08 2022 Milan Crha <mcrha@redhat.com> - 43.1-3
- Also skip gnome-pwa-list-foss.xml when building without WebApps

* Tue Nov 08 2022 Milan Crha <mcrha@redhat.com> - 43.1-2
- Disable WebApps for RHEL builds

* Mon Oct 24 2022 Milan Crha <mcrha@redhat.com> - 43.1-1
- Update to 43.1

* Wed Oct 05 2022 Milan Crha <mcrha@redhat.com> - 43.0-3
- Resolves: #2132292 (rpm-ostree plugin refuses to update)

* Tue Sep 27 2022 Kalev Lember <klember@redhat.com> - 43.0-2
- Rebuild to fix sysprof-capture symbols leaking into libraries consuming
  it

* Fri Sep 16 2022 Milan Crha <mcrha@redhat.com> - 43.0-1
- Update to 43.0

* Tue Sep 13 2022 Milan Crha <mcrha@redhat.com> - 43.rc-2
- Resolves: #2124869 (Cannot install RPM package file)

* Fri Sep 02 2022 Milan Crha <mcrha@redhat.com> - 43.rc-1
- Update to 43.rc

* Thu Aug 18 2022 Milan Crha <mcrha@redhat.com> - 43.beta-4
- Add rpminspect.yaml (settings for the RUNPATH test)

* Wed Aug 17 2022 Milan Crha <mcrha@redhat.com> - 43.beta-3
- Resolves: #2119089 (No enough apps to show for the "Editor's Choice"
  section)

* Mon Aug 15 2022 Milan Crha <mcrha@redhat.com> - 43.beta-2
- Add patch for install-queue (RH bug #2118265)

* Fri Aug 05 2022 Milan Crha <mcrha@redhat.com> - 43.beta-1
- Update to 43.beta

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 43.alpha-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jul 07 2022 Adam Williamson <awilliam@redhat.com> - 43.alpha-2
- Backport MR #1401 to fix issue #1816 and fedora-workstation #107

* Fri Jul 01 2022 Milan Crha <mcrha@redhat.com> - 43.alpha-1
- Update to 43.alpha

* Fri Jun 17 2022 Richard Hughes <richard@hughsie.com> - 42.2-6
- Add patch to make fwupd user requests work

* Thu Jun 16 2022 David King <amigadave@amigadave.com> - 42.2-5
- Improve directory ownership

* Thu Jun 16 2022 David King <amigadave@amigadave.com> - 42.2-4
- Use pkgconfig for BuildRequires

* Thu Jun 16 2022 David King <amigadave@amigadave.com> - 42.2-3
- Filter private libraries from Provides

* Mon Jun 13 2022 Milan Crha <mcrha@redhat.com> - 42.2-2
- Add patch for crash under gs_flatpak_refine_app_unlocked()

* Mon May 30 2022 Milan Crha <mcrha@redhat.com> - 42.2-1
- Update to 42.2; Add patch to correct order of the setup of the GsShell

* Wed Apr 27 2022 Milan Crha <mcrha@redhat.com> - 42.1-1
- Update to 42.1

* Fri Mar 18 2022 Milan Crha <mcrha@redhat.com> - 42.0-1
- Update to 42.0

* Thu Mar 10 2022 Milan Crha <mcrha@redhat.com> - 42~rc-2
- Add upstream patches for gs-download-utils (i#1677 and i#1679)

* Mon Mar 07 2022 Milan Crha <mcrha@redhat.com> - 42~rc-1
- Update to 42.rc

* Mon Feb 21 2022 Milan Crha <mcrha@redhat.com> - 42~beta-5
- Resolves: #2056082 (Enable PackageKit autoremove option)

* Wed Feb 16 2022 Milan Crha <mcrha@redhat.com> - 42~beta-4
- Add a temporary workaround for gtk_widget_measure error flood on GsAppRow

* Wed Feb 16 2022 Milan Crha <mcrha@redhat.com> - 42~beta-3
- Resolves: #2054939 (Crash on a PackageKit app install)

* Fri Feb 11 2022 Milan Crha <mcrha@redhat.com> - 42~beta-2
- Correct files list for popular plugin removal

* Fri Feb 11 2022 Milan Crha <mcrha@redhat.com> - 42~beta-1
- Update to 42.beta

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 42~alpha-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jan 07 2022 Milan Crha <mcrha@redhat.com> - 42~alpha-1
- Update to 42.alpha

* Fri Dec 03 2021 Milan Crha <mcrha@redhat.com> - 41.2-1
- Update to 41.2

* Fri Oct 29 2021 Milan Crha <mcrha@redhat.com> - 41.1-1
- Update to 41.1

* Tue Oct 19 2021 Milan Crha <mcrha@redhat.com> - 41.0-6
- Resolves: #2012863 (gs-installed-page: Change section on application
  state change)

* Mon Oct 11 2021 Milan Crha <mcrha@redhat.com> - 41.0-5
- Add patch to mark compulsory only repos, not apps from it

* Fri Oct 08 2021 Milan Crha <mcrha@redhat.com> - 41.0-4
- Resolves: #2011176, #2010660, #2010353

* Fri Oct 08 2021 Milan Crha <mcrha@redhat.com> - 41.0-3
- Resolves: #2010740 (Refresh on repository setup change)

* Fri Oct 08 2021 Milan Crha <mcrha@redhat.com> - 41.0-2
- Resolves: #2009063 (Correct update notifications)

* Mon Sep 20 2021 Milan Crha <mcrha@redhat.com> - 41.0-1
- Update to 41.0

* Mon Sep 13 2021 Milan Crha <mcrha@redhat.com> - 41~rc-2
- Resolves: #2003365 (packagekit: Ensure PkClient::interactive flag being
  set)

* Wed Sep 08 2021 Milan Crha <mcrha@redhat.com> - 41~rc-1
- Update to 41.rc

* Wed Sep 01 2021 Milan Crha <mcrha@redhat.com> - 41~beta-3
- Resolves: #1995817 (gs-updates-section: Check also dependencies' download
  size)

* Tue Aug 24 2021 Kalev Lember <klember@redhat.com> - 41~beta-2
- Enable parental controls support

* Fri Aug 13 2021 Milan Crha <mcrha@redhat.com> - 41~beta-1
- Update to 41.beta

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 41~alpha-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jul 21 2021 Milan Crha <mcrha@redhat.com> - 41~alpha-1
- Update to 41.alpha

* Mon Jul 12 2021 Milan Crha <mcrha@redhat.com> - 40.3-2
- Add rpm-ostree patch to hide packages from the search results; Add patch
  to implement what-provides search in the Flatpak plugin

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
- Rebuild to fix sysprof-capture symbols leaking into libraries consuming
  it

* Mon Mar 22 2021 Kalev Lember <klember@redhat.com> - 40.0-1
- Update to 40.0

* Fri Mar 19 2021 Adam Williamson <awilliam@redhat.com> - 40~rc-2
- Backport a couple of bug fixes from upstream (icon display, crash bug)

* Mon Mar 15 2021 Kalev Lember <klember@redhat.com> - 40~rc-1
- Update to 40.rc

* Wed Mar 10 2021 Adam Williamson <awilliam@redhat.com> - 40~beta-3
- Backport MR #643 to fix update notifications on first run (#1930401)

* Wed Feb 24 2021 Kalev Lember <klember@redhat.com> - 40~beta-2
- BR sysprof-capture-devel rather than sysprof-devel

* Tue Feb 16 2021 Kalev Lember <klember@redhat.com> - 40~beta-1
- Update to 40.beta

* Mon Feb 08 2021 Richard Hughes <richard@hughsie.com> - 3.38.1-1
- New upstream version

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.38.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Sep 14 2020 Kalev Lember <klember@redhat.com> - 3.38.0-2
- Revert an optimization that broke packagekit updates

* Fri Sep 11 2020 Kalev Lember <klember@redhat.com> - 3.38.0-1
- Update to 3.38.0

* Tue Sep 01 2020 Kalev Lember <klember@redhat.com> - 3.37.92-1
- Update to 3.37.92

* Tue Aug 18 2020 Richard Hughes <richard@hughsie.com> - 3.36.1-4
- Rebuild for the libxmlb API bump

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.36.1-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.36.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri May 22 2020 Richard Hughes <richard@hughsie.com> - 3.36.1-1
- Update to 3.36.1

* Tue May 12 2020 Kalev Lember <klember@redhat.com> - 3.36.0-2
- Backport various rpm-ostree backend fixes

* Wed Mar 11 2020 Kalev Lember <klember@redhat.com> - 3.36.0-1
- Update to 3.36.0

* Wed Mar 04 2020 Kalev Lember <klember@redhat.com> - 3.35.92-1
- Update to 3.35.92

* Fri Feb 21 2020 Richard Hughes <richard@hughsie.com> - 3.35.91-5
- Backport a patch to fix a crash when looking at the application details

* Wed Feb 19 2020 Kalev Lember <klember@redhat.com> - 3.35.91-4
- Update source URL

* Wed Feb 19 2020 Kalev Lember <klember@redhat.com> - 3.35.91-3
- Update minimum required dep versions

* Wed Feb 19 2020 Richard Hughes <richard@hughsie.com> - 3.35.91-2
- Actually include souces file

* Wed Feb 19 2020 Richard Hughes <richard@hughsie.com> - 3.35.91-1
- Update to 3.35.91

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.35.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Nov 25 2019 Richard Hughes <richard@hughsie.com> - 3.35.2-1
- Update to 3.35.2

* Fri Oct 18 2019 Kalev Lember <klember@redhat.com> - 3.34.1-6
- Backport patches to fix a crash in gs_flatpak_get_installation

* Mon Oct 14 2019 Kalev Lember <klember@redhat.com> - 3.34.1-5
- Update renamed appstream ids for GNOME 3.34

* Fri Oct 11 2019 Richard Hughes <richard@hughsie.com> - 3.34.1-4
- Simpler patch

* Fri Oct 11 2019 Richard Hughes <richard@hughsie.com> - 3.34.1-3
- Backport a better patch

* Thu Oct 10 2019 Richard Hughes <richard@hughsie.com> - 3.34.1-2
- Backport a patch to correct the applications shown in the installed list

* Mon Oct 07 2019 Kalev Lember <klember@redhat.com> - 3.34.1-1
- Update to 3.34.1

* Wed Sep 25 2019 Kalev Lember <klember@redhat.com> - 3.34.0-4
- Drop unused libsecret-devel BR

* Wed Sep 25 2019 Kalev Lember <klember@redhat.com> - 3.34.0-3
- Remove a no-longer-needed requires filter

* Wed Sep 25 2019 Kalev Lember <klember@redhat.com> - 3.34.0-2
- Fix third party repo enabling not working

* Mon Sep 09 2019 Kalev Lember <klember@redhat.com> - 3.34.0-1
- Update to 3.34.0

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.32.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jul 11 2019 Kalev Lember <klember@redhat.com> - 3.32.4-2
- Bump obsoletes version

* Thu Jul 11 2019 Kalev Lember <klember@redhat.com> - 3.32.4-1
- Update to 3.32.4

* Thu Jul 11 2019 Richard Hughes <richard@hughsie.com> - 3.32.3-5
- Disable the snap plugin

* Thu Jun 13 2019 Kalev Lember <klember@redhat.com> - 3.32.3-4
- Rebuild for accidental libflatpak ABI break

* Mon Jun 10 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.32.3-3
- Rebuild for RPM 4.15

* Mon Jun 10 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.32.3-2
- Rebuild for RPM 4.15

* Fri May 24 2019 Kalev Lember <klember@redhat.com> - 3.32.3-1
- Update to 3.32.3

* Wed May 01 2019 Kalev Lember <klember@redhat.com> - 3.32.2-1
- Update to 3.32.2

* Fri May 03 2019 Kalev Lember <klember@redhat.com> - 3.32.1-5
- Update a patch to final upstream version

* Tue Apr 30 2019 Kalev Lember <klember@redhat.com> - 3.32.1-4
- Backport a number of rpm-ostree fixes

* Tue Apr 16 2019 Adam Williamson <awilliam@redhat.com> - 3.32.1-3
- Rebuild with Meson fix for #1699099

* Mon Apr 15 2019 Kalev Lember <klember@redhat.com> - 3.32.1-2
- Set minimum required libxmlb version

* Mon Apr 15 2019 Kalev Lember <klember@redhat.com> - 3.32.1-1
- Update to 3.32.1

* Fri Apr 05 2019 Neal Gompa <ngompa13@gmail.com> - 3.32.0-7
- Require snapd instead of the obsolete snapd-login-service for snap
  subpackage

* Wed Apr 03 2019 Kalev Lember <klember@redhat.com> - 3.32.0-6
- Switch to system libdnf

* Fri Mar 29 2019 Kalev Lember <klember@redhat.com> - 3.32.0-5
- Rebuild for new rpm-ostree

* Fri Mar 15 2019 Kalev Lember <klember@redhat.com> - 3.32.0-4
- Add nm-connection-editor.desktop to Utilities folder

* Wed Mar 13 2019 Kalev Lember <klember@redhat.com> - 3.32.0-3
- Backport one more patch to add shadows to icons in app tiles as well

* Tue Mar 12 2019 Kalev Lember <klember@redhat.com> - 3.32.0-2
- Backport a patch to add shadows to app icons

* Mon Mar 11 2019 Kalev Lember <klember@redhat.com> - 3.32.0-1
- Update to 3.32.0

* Tue Mar 05 2019 Kalev Lember <klember@redhat.com> - 3.31.92-1
- Update to 3.31.92

* Thu Feb 28 2019 Kalev Lember <klember@redhat.com> - 3.31.90-6
- Change PackageKit requires to recommends

* Wed Feb 27 2019 Kalev Lember <klember@redhat.com> - 3.31.90-5
- Remove unneeded dpkg plugin

* Mon Feb 25 2019 Kalev Lember <klember@redhat.com> - 3.31.90-4
- Split rpm-ostree backend to its own subpackage

* Sun Feb 24 2019 Kalev Lember <klember@redhat.com> - 3.31.90-3
- Add "anaconda" repo to official repos list

* Sun Feb 24 2019 Kalev Lember <klember@redhat.com> - 3.31.90-2
- Bundle libdnf to match the exact version that rpm-ostree ships

* Sun Feb 24 2019 Kalev Lember <klember@redhat.com> - 3.31.90-1
- Update to 3.31.90

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.31.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jan 25 2019 Kalev Lember <klember@redhat.com> - 3.31.2-2
- Drop obsolete meson options

* Wed Jan 16 2019 Kalev Lember <klember@redhat.com> - 3.31.2-1
- Update to 3.31.2

* Fri Dec 14 2018 Kalev Lember <klember@redhat.com> - 3.31.1-2
- Fix offline update notifications to show up

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

* Tue Aug 28 2018 Richard Hughes <richard@hughsie.com> - 3.29.92-1
- Update to 3.29.92

* Tue Jul 31 2018 Kalev Lember <klember@redhat.com> - 3.29.1-4
- Disable snap support for RHEL

* Mon Jul 16 2018 Richard Hughes <richard@hughsie.com> - 3.29.1-3
- trivial: Fix BRs

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.29.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed May 09 2018 Kalev Lember <klember@redhat.com> - 3.29.1-1
- Update to 3.29.1

* Mon Apr 09 2018 Kalev Lember <klember@redhat.com> - 3.28.1-1
- Update to 3.28.1

* Thu Mar 29 2018 Kalev Lember <klember@redhat.com> - 3.28.0-6
- Make rpm-ostree update triggering work

* Thu Mar 29 2018 Kalev Lember <klember@redhat.com> - 3.28.0-5
- Fix empty OS Updates showing up

* Thu Mar 15 2018 Kalev Lember <klember@redhat.com> - 3.28.0-4
- Fix opening results from gnome-shell search provider

* Wed Mar 14 2018 Kalev Lember <klember@redhat.com> - 3.28.0-3
- Fix crash on initial run with no network

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

* Mon Mar 05 2018 Neal Gompa <ngompa13@gmail.com> - 3.27.90-6
- Drop obsolete snapd-login-service requirement for snap plugin subpackage

* Tue Feb 20 2018 Adam Williamson <awilliam@redhat.com> - 3.27.90-5
- Backport fix for RHBZ #1546893 from upstream git

* Mon Feb 19 2018 Kalev Lember <klember@redhat.com> - 3.27.90-4
- Re-enable rpm-ostree plugin

* Thu Feb 15 2018 Kalev Lember <klember@redhat.com> - 3.27.90-3
- Update BRs for the switch to gspell

* Thu Feb 15 2018 Kalev Lember <klember@redhat.com> - 3.27.90-2
- Temporarily disable the rpm-ostree plugin

* Thu Feb 15 2018 Kalev Lember <klember@redhat.com> - 3.27.90-1
- Update to 3.27.90 and adjust the gsettings schema overrides for upstream
  changes in this release.

* Tue Feb 13 2018 Björn Esser <besser82@fedoraproject.org> - 3.27.4-5
- Rebuild against newer gnome-desktop3 package

* Thu Feb 08 2018 Kalev Lember <klember@redhat.com> - 3.27.4-4
- Add fedora-workstation-repositories to nonfree-sources schema defaults

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.27.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Jan 08 2018 Kalev Lember <klember@redhat.com> - 3.27.4-2
- Drop unused --without packagekit option

* Mon Jan 08 2018 Kalev Lember <klember@redhat.com> - 3.27.4-1
- Update to 3.27.4

* Fri Jan 05 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.27.3-2
- Remove obsolete scriptlets

* Sat Dec 16 2017 Kalev Lember <klember@redhat.com> - 3.27.3-1
- Update to 3.27.3

* Mon Nov 13 2017 Kalev Lember <klember@redhat.com> - 3.27.2-2
- Explicitly disable ubuntuone support

* Mon Nov 13 2017 Kalev Lember <klember@redhat.com> - 3.27.2-1
- Update to 3.27.2

* Thu Nov 09 2017 Kalev Lember <klember@redhat.com> - 3.26.2-2
- Re-enable fwupd support

* Thu Nov 09 2017 Kalev Lember <klember@redhat.com> - 3.26.2-1
- Update to 3.26.2

* Tue Oct 31 2017 Kalev Lember <klember@redhat.com> - 3.26.1-5
- Enable the rpm-ostree plugin

* Wed Oct 25 2017 Kalev Lember <klember@redhat.com> - 3.26.1-4
- Fix "too many results returned" error after distro upgrades

* Tue Oct 10 2017 Kalev Lember <klember@redhat.com> - 3.26.1-3
- Backport a flatpakref installation fix

* Mon Oct 09 2017 Richard Hughes <richard@hughsie.com> - 3.26.1-2
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
- Rebuilt for
  https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.25.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jul 21 2017 Kalev Lember <klember@redhat.com> - 3.25.4-1
- Update to 3.25.4

* Tue Jul 18 2017 Kalev Lember <klember@redhat.com> - 3.25.3-8
- Drop a meson workaround now that meson is fixed

* Wed Jun 28 2017 Neal Gompa <ngompa13@gmail.com> - 3.25.3-7
- Actually properly enable snap subpackage after removing conditional

* Wed Jun 28 2017 Neal Gompa <ngompa13@gmail.com> - 3.25.3-6
- Remove unnecessary arch-specific conditional for snap subpackage

* Tue Jun 27 2017 Neal Gompa <ngompa13@gmail.com> - 3.25.3-5
- Ensure snap subpackage is installed if snapd is installed

* Sat Jun 24 2017 Richard Hughes <richard@hughsie.com> - 3.25.3-4
- Enable the snap subpackage

* Fri Jun 23 2017 Kalev Lember <klember@redhat.com> - 3.25.3-3
- Add missing build dep

* Fri Jun 23 2017 Kalev Lember <klember@redhat.com> - 3.25.3-2
- Add temporary workaround for meson 0.41.1 breakage

* Fri Jun 23 2017 Kalev Lember <klember@redhat.com> - 3.25.3-1
- Update to 3.25.3
- Switch to the meson build system
- Add an -editor subpackage with new banner editor

* Mon May 15 2017 Richard Hughes <richard@hughsie.com> - 3.24.3-1
- Update to 3.23.3

* Tue May 09 2017 Kalev Lember <klember@redhat.com> - 3.24.2-1
- Update to 3.24.2

* Wed Apr 26 2017 Adam Williamson <awilliam@redhat.com> - 3.24.1-2
- Backport crasher fix from upstream (RHBZ #1444669 / BGO #781217)

* Tue Apr 11 2017 Kalev Lember <klember@redhat.com> - 3.24.1-1
- Update to 3.24.1

* Tue Mar 21 2017 Kalev Lember <klember@redhat.com> - 3.24.0-1
- Update to 3.24.0

* Thu Mar 16 2017 Kalev Lember <klember@redhat.com> - 3.23.92-1
- Update to 3.23.92

* Mon Feb 27 2017 Richard Hughes <richard@hughsie.com> - 3.23.91-1
- Update to 3.23.91

* Mon Feb 13 2017 Richard Hughes <richard@hughsie.com> - 3.23.90-1
- Update to 3.23.90

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.23.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Dec 17 2016 Kalev Lember <klember@redhat.com> - 3.23.3-2
- Update required gtk3 version

* Thu Dec 15 2016 Richard Hughes <richard@hughsie.com> - 3.23.3-1
- Update to 3.23.3

* Wed Nov 23 2016 Kalev Lember <klember@redhat.com> - 3.23.2-1
- Update to 3.23.2

* Tue Nov 08 2016 Kalev Lember <klember@redhat.com> - 3.22.2-1
- Update to 3.22.2

* Wed Oct 12 2016 Kalev Lember <klember@redhat.com> - 3.22.1-1
- Update to 3.22.1

* Mon Sep 19 2016 Kalev Lember <klember@redhat.com> - 3.22.0-1
- Update to 3.22.0

* Wed Sep 14 2016 Kalev Lember <klember@redhat.com> - 3.21.92-4
- Use https download URL

* Wed Sep 14 2016 Kalev Lember <klember@redhat.com> - 3.21.92-3
- Don't set group tags

* Wed Sep 14 2016 Kalev Lember <klember@redhat.com> - 3.21.92-2
- Use standard tag order in spec file

* Wed Sep 14 2016 Kalev Lember <klember@redhat.com> - 3.21.92-1
- Update to 3.21.92

* Tue Sep 13 2016 Richard Hughes <richard@hughsie.com> - 3.21.91-2
- Update the BRs and filelists for the next release

* Thu Sep 01 2016 Kalev Lember <klember@redhat.com> - 3.21.91-1
- Update to 3.21.91

* Wed Aug 17 2016 Kalev Lember <klember@redhat.com> - 3.21.90-4
- Rebuilt for fixed libappstream-glib headers

* Wed Aug 17 2016 Kalev Lember <klember@redhat.com> - 3.21.90-3
- Tighten -devel subpackage dependencies

* Wed Aug 17 2016 Kalev Lember <klember@redhat.com> - 3.21.90-2
- Make sure we have new enough flatpak and flatpak-libs versions

* Wed Aug 17 2016 Kalev Lember <klember@redhat.com> - 3.21.90-1
- Update to 3.21.90

* Thu Jul 28 2016 Richard Hughes <richard@hughsie.com> - 3.21.4-4
- Fix BRs

* Thu Jul 28 2016 Richard Hughes <richard@hughsie.com> - 3.21.4-3
- Allow building without PackageKit for the atomic workstation

* Mon Jul 18 2016 Richard Hughes <richard@hughsie.com> - 3.21.4-2
- Fix BRs and filelists

* Mon Jul 18 2016 Richard Hughes <richard@hughsie.com> - 3.21.4-1
- Update to 3.21.4

* Fri Jul 01 2016 Kalev Lember <klember@redhat.com> - 3.21.2-4
- Set minimum fwupd version

* Fri Jul 01 2016 Kalev Lember <klember@redhat.com> - 3.21.2-3
- trivial: Move Requires below BuildRequires

* Thu May 26 2016 Kalev Lember <klember@redhat.com> - 3.21.2-2
- Build with flatpak support

* Mon May 23 2016 Richard Hughes <richard@hughsie.com> - 3.21.2-1
- Update to 3.21.2

* Tue May 10 2016 Kalev Lember <klember@redhat.com> - 3.21.1-3
- Require PackageKit 1.1.1 for system upgrade support

* Tue May 03 2016 Kalev Lember <klember@redhat.com> - 3.21.1-2
- Update required libappstream-glib version

* Mon Apr 25 2016 Richard Hughes <richard@hughsie.com> - 3.21.1-1
- Update to 3.21.1

* Mon Apr 25 2016 Richard Hughes <richard@hughsie.com> - 3.20.2-1
- Update to 3.20.1

* Wed Apr 13 2016 Kalev Lember <klember@redhat.com> - 3.20.1-1
- Update to 3.20.1

* Fri Apr 01 2016 Richard Hughes <richard@hughsie.com> - 3.20.0-4
- Compile with xdg-app support

* Fri Apr 01 2016 Richard Hughes <richard@hughsie.com> - 3.20.0-3
- Set the list of official sources

* Fri Apr 01 2016 Richard Hughes <richard@hughsie.com> - 3.20.0-2
- Fix up the Source

* Tue Mar 22 2016 Kalev Lember <klember@redhat.com> - 3.20.0-1
- Update to 3.20.0

* Mon Mar 14 2016 Richard Hughes <richard@hughsie.com> - 3.19.92-2
- Fix filelists

* Mon Mar 14 2016 Richard Hughes <richard@hughsie.com> - 3.19.92-1
- Update to 3.19.92

* Thu Mar 03 2016 Kalev Lember <klember@redhat.com> - 3.19.91-3
- Set minimum required json-glib version to make sure that F23 gnome-
  software update pulls in the updated json-glib as well.

* Wed Mar 02 2016 Richard Hughes <richard@hughsie.com> - 3.19.91-2
- Update BRs

* Mon Feb 29 2016 Richard Hughes <richard@hughsie.com> - 3.19.91-1
- Update to 3.19.91

* Mon Feb 15 2016 Richard Hughes <richard@hughsie.com> - 3.19.90-2
- Update BRs

* Mon Feb 15 2016 Richard Hughes <richard@hughsie.com> - 3.19.90-1
- Update to 3.19.90

* Mon Feb 15 2016 Richard Hughes <richard@hughsie.com> - 3.19.4-4
- trivial: Update for mclazy

* Wed Feb 03 2016 Dennis Gilmore <dennis@ausil.us> - 3.19.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan 15 2016 Richard Hughes <richard@hughsie.com> - 3.19.4-2
- Fix BRs

* Fri Jan 15 2016 Richard Hughes <richard@hughsie.com> - 3.19.4-1
- Update to 3.19.4

* Thu Dec 03 2015 Kalev Lember <klember@redhat.com> - 3.18.3-2
- Require librsvg2 for the gdk-pixbuf svg loader

* Fri Nov 06 2015 Richard Hughes <richard@hughsie.com> - 3.18.3-1
- Update to 3.18.3

* Mon Oct 26 2015 Kalev Lember <klember@redhat.com> - 3.18.2-2
- Fix apps reappearing as installed a few seconds after removal

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

* Tue Sep 15 2015 Richard Hughes <richard@hughsie.com> - 3.17.92-1
- Update to 3.17.92

* Thu Sep 10 2015 Richard Hughes <richard@hughsie.com> - 3.17.91-3
- Fix firmware updates

* Thu Sep 03 2015 Kalev Lember <klember@redhat.com> - 3.17.91-2
- Remove unnecessary macro use

* Thu Sep 03 2015 Kalev Lember <klember@redhat.com> - 3.17.91-1
- Update to 3.17.91

* Wed Aug 19 2015 Kalev Lember <klember@redhat.com> - 3.17.90-1
- Update to 3.17.90

* Wed Aug 12 2015 Richard Hughes <richard@hughsie.com> - 3.17.3-2
- fix BRs

* Wed Aug 12 2015 Richard Hughes <richard@hughsie.com> - 3.17.3-1
- Update to 3.17.3

* Wed Jul 22 2015 David King <amigadave@amigadave.com> - 3.17.2-3
- Bump for new gnome-desktop3

* Wed Jun 17 2015 Dennis Gilmore <dennis@ausil.us> - 3.17.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Kalev Lember <kalevlember@gmail.com> - 3.17.2-1
- Update to 3.17.2

* Mon May 25 2015 Kalev Lember <kalevlember@gmail.com> - 3.17.1-1
- Update to 3.17.1

* Fri May 15 2015 Kalev Lember <kalevlember@gmail.com> - 3.16.2-2
- Fix a crash under Wayland

* Mon May 11 2015 Kalev Lember <kalevlember@gmail.com> - 3.16.2-1
- Update to 3.16.2

* Tue Apr 14 2015 Kalev Lember <kalevlember@gmail.com> - 3.16.1-1
- Update to 3.16.1

* Mon Mar 23 2015 Kalev Lember <kalevlember@gmail.com> - 3.16.0-1
- Update to 3.16.0

* Mon Mar 16 2015 Kalev Lember <kalevlember@gmail.com> - 3.15.92-3
- Add a patch to adapt to gnome-terminal desktop file rename

* Mon Mar 16 2015 Kalev Lember <kalevlember@gmail.com> - 3.15.92-2
- Use license macro for the COPYING file

* Mon Mar 16 2015 Kalev Lember <kalevlember@gmail.com> - 3.15.92-1
- Update to 3.15.92

* Mon Mar 02 2015 Kalev Lember <kalevlember@gmail.com> - 3.15.91-1
- Update to 3.15.91

* Sat Feb 21 2015 Kalev Lember <kalevlember@gmail.com> - 3.15.90-3
- Export DisplayName property on the packagekit session service

* Thu Feb 19 2015 Kalev Lember <kalevlember@gmail.com> - 3.15.90-2
- Backport a crash fix

* Tue Feb 17 2015 Richard Hughes <richard@hughsie.com> - 3.15.90-1
- Update to 3.15.90

* Mon Jan 19 2015 Richard Hughes <richard@hughsie.com> - 3.15.4-1
- Update to 3.15.4

* Tue Nov 25 2014 Kalev Lember <kalevlember@gmail.com> - 3.15.2-1
- Update to 3.15.2

* Tue Nov 25 2014 Richard Hughes <richard@hughsie.com> - 3.14.2-3
- Fix non-Fedora build

* Tue Nov 11 2014 Richard Hughes <richard@hughsie.com> - 3.14.2-2
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

* Wed Sep 17 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.92-4
- Set minimum required dependency versions

* Tue Sep 16 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.92-3
- Replace gnome-system-log with gnome-logs in the system apps list

* Tue Sep 16 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.92-2
- Drop unused libnotify-devel build dep

* Tue Sep 16 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.92-1
- Update to 3.13.92

* Tue Sep 02 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.91-1
- Update to 3.13.91

* Tue Aug 19 2014 Richard Hughes <richard@hughsie.com> - 3.13.90-1
- Update to 3.13.90

* Sat Aug 16 2014 Peter Robinson <pbrobinson@fedoraproject.org> - 3.13.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Aug 11 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.5-1
- Update to 3.13.5 git snapshot

* Sun Aug 03 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.4-4
- Actually apply the patch

* Sun Aug 03 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.4-3
- Replace Epiphany with Firefox in the system apps list

* Wed Jul 23 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.4-2
- Drop an unused define

* Wed Jul 23 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.4-1
- Update to 3.13.4

* Wed Jun 25 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.3-3
- Update to 3.13.3

* Thu Jun 12 2014 Richard Hughes <richard@hughsie.com> - 3.13.3-2
- Depend on appstream-data for the AppStream metadata

* Sat Jun 07 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.3-1
- Update to 3.13.3 git snapshot so that I could more easily get feedback
  for latest changes.

* Wed May 28 2014 Richard Hughes <richard@hughsie.com> - 3.13.2-2
- Rebuild with new metadata

* Wed May 28 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.2-1
- Update to 3.13.2

* Thu May 15 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.1-10
- Depend on gsettings-desktop-schemas

* Mon May 12 2014 Richard Hughes <richard@hughsie.com> - 3.13.1-9
- Bump revision for build

* Mon May 12 2014 Richard Hughes <richard@hughsie.com> - 3.13.1-8
- Use appstream-util to install the AppStream files

* Mon May 12 2014 Richard Hughes <richard@hughsie.com> - 3.13.1-7
- Update metadata

* Wed May 07 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.1-6
- Drop gnome-icon-theme dependency

* Mon Apr 28 2014 Richard Hughes <richard@hughsie.com> - 3.13.1-5
- Backport a patch to fix compile with the new anal GCC

* Mon Apr 28 2014 Richard Hughes <richard@hughsie.com> - 3.13.1-4
- Fix URL

* Mon Apr 28 2014 Richard Hughes <richard@hughsie.com> - 3.13.1-3
- Fix BRs

* Mon Apr 28 2014 Richard Hughes <richard@hughsie.com> - 3.13.1-2
- Rebuild with new metadata

* Mon Apr 28 2014 Richard Hughes <richard@hughsie.com> - 3.13.1-1
- Update to 3.13.1

* Fri Apr 11 2014 Kalev Lember <kalevlember@gmail.com> - 3.12.1-4
- Rebuild with new metadata

* Fri Apr 11 2014 Richard Hughes <richard@hughsie.com> - 3.12.1-3
- New metadata

* Fri Apr 11 2014 Kalev Lember <kalevlember@gmail.com> - 3.12.1-2
- Add back accidentally removed appdata files

* Fri Apr 11 2014 Richard Hughes <richard@hughsie.com> - 3.12.1-1
- Update to 3.12.1

* Mon Mar 24 2014 Richard Hughes <richard@hughsie.com> - 3.12.0-2
- New metadata

* Mon Mar 24 2014 Richard Hughes <richard@hughsie.com> - 3.12.0-1
- Update to 3.12.0

* Thu Mar 20 2014 Richard Hughes <richard@hughsie.com> - 3.11.92-3
- Fix BRs

* Thu Mar 20 2014 Richard Hughes <richard@hughsie.com> - 3.11.92-2
- trivial: Reinstate the metadata

* Thu Mar 20 2014 Richard Hughes <richard@hughsie.com> - 3.11.92-1
- Update to 3.11.92

* Tue Mar 18 2014 Richard Hughes <richard@hughsie.com> - 3.11.91-3
- Rebuild with new metadata

* Fri Mar 14 2014 Kalev Lember <kalevlember@gmail.com> - 3.11.91-2
- Add back accidentally removed appdata files

* Sat Mar 08 2014 Richard Hughes <richard@hughsie.com> - 3.11.91-1
- Update to 3.11.91

* Wed Feb 19 2014 Richard Hughes <richard@hughsie.com> - 3.11.90-3
- Fix filelists

* Wed Feb 19 2014 Richard Hughes <richard@hughsie.com> - 3.11.90-2
- Use new metadata

* Tue Feb 18 2014 Richard Hughes <richard@hughsie.com> - 3.11.90-1
- Update to 3.11.90

* Mon Feb 03 2014 Richard Hughes <richard@hughsie.com> - 3.11.5-2
- Require epiphany-runtime rather than the full application

* Mon Feb 03 2014 Richard Hughes <richard@hughsie.com> - 3.11.5-1
- Update to 3.11.5

* Thu Jan 30 2014 Richard Hughes <richard@hughsie.com> - 3.11.4-4
- Rebuild for libpackagekit-glib soname bump

* Wed Jan 22 2014 Richard Hughes <richard@hughsie.com> - 3.11.4-3
- Rebuild with metadata that has the correct screenshot url

* Fri Jan 17 2014 Richard Hughes <richard@hughsie.com> - 3.11.4-2
- Update metadata

* Thu Jan 16 2014 Richard Hughes <richard@hughsie.com> - 3.11.4-1
- Update to 3.11.4

* Tue Dec 17 2013 Richard Hughes <richard@hughsie.com> - 3.11.3-2
- Upload latest metadata

* Tue Dec 17 2013 Richard Hughes <richard@hughsie.com> - 3.11.3-1
- Update to 3.11.3

* Tue Nov 19 2013 Richard Hughes <richard@hughsie.com> - 3.11.2-3
- Update BRs

* Tue Nov 19 2013 Richard Hughes <richard@hughsie.com> - 3.11.2-2
- Regenerate the metadata

* Tue Nov 19 2013 Richard Hughes <richard@hughsie.com> - 3.11.2-1
- Update to 3.11.2

* Tue Nov 19 2013 Richard Hughes <richard@hughsie.com> - 3.11.1-3
- Update filelists and BRs

* Tue Oct 29 2013 Richard Hughes <richard@hughsie.com> - 3.11.1-2
- Upload the new metdata for 3.11.1

* Tue Oct 29 2013 Richard Hughes <richard@hughsie.com> - 3.11.1-1
- Update to 3.11.1

* Wed Sep 25 2013 Richard Hughes <richard@hughsie.com> - 3.10.0-1
- New upstream release

* Fri Sep 13 2013 Richard Hughes <richard@hughsie.com> - 3.9.3-4
- Update BRs

* Fri Sep 13 2013 Richard Hughes <richard@hughsie.com> - 3.9.3-3
- Ahhhh... set all three files as sources

* Fri Sep 13 2013 Richard Hughes <richard@hughsie.com> - 3.9.3-2
- Actually upload sources

* Fri Sep 13 2013 Richard Hughes <richard@hughsie.com> - 3.9.3-1
- New upstream release

* Tue Sep 03 2013 Richard Hughes <richard@hughsie.com> - 3.9.2-1
- New upstream release

* Mon Sep 02 2013 Richard Hughes <richard@hughsie.com> - 3.9.1-2
- Fix BRs

* Mon Sep 02 2013 Richard Hughes <richard@hughsie.com> - 3.9.1-1
- New upstream release

* Mon Sep 02 2013 Richard Hughes <richard@hughsie.com> - 0.1-1
- Initial package
## END: Generated by rpmautospec
