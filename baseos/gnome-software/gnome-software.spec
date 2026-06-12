%global appstream_version 0.16.4
%global flatpak_version 1.14.1
%global fwupd_version 1.6.2
%global glib2_version 2.76.0
%global gtk4_version 4.17.5
%global json_glib_version 1.6.0
%global libadwaita_version 1.8.0
%global libxmlb_version 0.3.4
%global packagekit_version 1.2.5
%global dnf5_version 5.4.2

# Disable WebApps for RHEL builds
%bcond webapps %[!0%{?rhel}]
# Disable parental control for RHEL builds
%bcond malcontent %[!0%{?rhel}]
# Disable rpm-ostree support for RHEL builds
%bcond rpmostree %[!0%{?rhel}]
# Disable DKMS/akmods support for RHEL builds
%bcond dkms %[!0%{?rhel}]

%bcond packagekit 0
%bcond dnf5 1

# this is not a library version
%define gs_plugin_version 23

%global tarball_version %%(echo %%{version} | tr '~' '.')
%global major_version %%(echo %%{tarball_version} | cut -d "." -f 1)

%global __provides_exclude_from ^%{_libdir}/%{name}/plugins-%{gs_plugin_version}/.*\\.so.*$

Name:      gnome-software
Version:   50.2
Release:   %autorelease
Summary:   A software center for GNOME

License:   GPL-2.0-or-later
URL:       https://apps.gnome.org/Software
Source0:   https://download.gnome.org/sources/gnome-software/%{major_version}/%{name}-%{tarball_version}.tar.xz

%if %{with dnf5}
# to update the patch enter the ./dnf5-plugin/ directory and run from
# it the ./update-patch.sh script
Patch:     0001-dnf5-plugin.patch
%endif

Patch:     0002-plain-package-update-notification.patch

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
# check for human errors
if [ `echo "%{version}" | grep -cE "\.alpha|\.beta|\.rc"` = "1" ]; then echo "Error: Use tilde in Version field in front of alpha/beta/rc; checked '%{version}'" 1>&2; exit 1; fi

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
%doc AUTHORS NEWS README.md
%license COPYING
%{_bindir}/gnome-software
%{_datadir}/applications/gnome-software-local-file-flatpak.desktop
%{_datadir}/applications/gnome-software-local-file-fwupd.desktop
%{_datadir}/applications/gnome-software-local-file-metainfo.desktop
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
%{_datadir}/dbus-1/services/org.freedesktop.PackageKit.service
%{_datadir}/dbus-1/services/org.gnome.Software.service
%{_datadir}/gnome-shell/search-providers/org.gnome.Software-search-provider.ini
%{_datadir}/glib-2.0/schemas/org.gnome.software.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.software-fedora.gschema.override
%{_libexecdir}/gnome-software-cmd
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
%autochangelog
