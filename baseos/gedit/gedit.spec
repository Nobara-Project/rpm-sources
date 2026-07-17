%global amtk_version 5.10
%global glib2_version 2.76
%global gtk3_version 3.24
%global gtksourceview_version 299.7
%global libpeas_version 1.14.1
%global gspell_version 1.0
%global tepl_version 6.14

# Filter provides for plugin .so files
%global __provides_exclude_from ^%{_libdir}/gedit/plugins/

%global api_version %%(ver=%%{version}; echo ${ver%%.*})
%global tarball_version %%(ver=%%{version}; echo ${ver//~/.})
%global libgd_commit 3cccf99234288a6121b3945a25cd4ec3b7445c74

Name:		gedit
Epoch:		2
Version:	50.0
Release:	%autorelease
Summary:	Text editor for the GNOME desktop
License:	GPL-3.0-or-later AND LGPL-3.0-or-later
URL:		https://gedit-text-editor.org/
Source:         https://gitlab.gnome.org/World/gedit/%{name}/-/archive/%{version}/%{name}-%{version}.tar.bz2
# libgd is a git submodule by design, but those are not included in git forge snapshot tarballs
Source:         https://gitlab.gnome.org/GNOME/libgd/-/archive/%{libgd_commit}/libgd-%{libgd_commit}.tar.bz2
Patch0:		change_default_color_scheme_to_more_legible_highlight_default.patch

BuildRequires: pkgconfig(glib-2.0) >= %{glib2_version}
BuildRequires: pkgconfig(gobject-introspection-1.0)
BuildRequires: pkgconfig(gsettings-desktop-schemas)
BuildRequires: pkgconfig(gspell-1) >= %{gspell_version}
BuildRequires: pkgconfig(gtk+-3.0) >= %{gtk3_version}
BuildRequires: pkgconfig(libgedit-amtk-5) >= %{amtk_version}
BuildRequires: pkgconfig(libgedit-gtksourceview-300) >= %{gtksourceview_version}
BuildRequires: pkgconfig(libgedit-tepl-6) >= %{tepl_version}
BuildRequires: pkgconfig(libpeas-gtk-1.0) >= %{libpeas_version}
BuildRequires: desktop-file-utils
BuildRequires: gettext
BuildRequires: gtk-doc
BuildRequires: which
BuildRequires: yelp-tools
BuildRequires: itstool
BuildRequires: meson
BuildRequires: /usr/bin/appstream-util

Provides: bundled(libgd) = %{libgd_commit}

Requires: glib2%{?_isa} >= %{glib2_version}
Requires: gspell%{?_isa} >= %{gspell_version}
Requires: gtk3%{?_isa} >= %{gtk3_version}
Requires: libgedit-gtksourceview%{?_isa} >= %{gtksourceview_version}
Requires: libgedit-tepl%{?_isa} >= %{tepl_version}
Requires: python3-gobject
Requires: gsettings-desktop-schemas

Obsoletes: gedit-collaboration < 3.6.1-6
Obsoletes: gedit-plugin-zeitgeist < 3.35.90
Obsoletes: gedit-plugin-commander < 43.0
Obsoletes: gedit-plugin-findinfiles < 43.0
Obsoletes: gedit-plugin-translate < 43.0
Obsoletes: gedit-plugin-colorschemer < 45.0
Obsoletes: gedit-plugin-synctex < 45.0
Obsoletes: gedit-plugin-git < 48.0
Obsoletes: gedit-plugin-textsize < 48.0
Obsoletes: gedit-color-schemes < 0-18
Obsoletes: gedit-control-your-tabs < 0.5.2
Obsoletes: gedit-latex < 48.0
Obsoletes: gedit-plugin-bracketcompletion < 48.2
Obsoletes: gedit-plugin-charmap < 48.2
Obsoletes: gedit-plugin-codecomment < 48.2
Obsoletes: gedit-plugin-colorpicker < 48.2
Obsoletes: gedit-plugin-joinlines < 48.2
Obsoletes: gedit-plugin-multiedit < 48.2
Obsoletes: gedit-plugin-sessionsaver < 48.2
Obsoletes: gedit-plugin-terminal < 48.2


%description
gedit is a small, but powerful text editor designed specifically for
the GNOME desktop. It has most standard text editor functions and fully
supports international text in Unicode. Advanced features include syntax
highlighting and automatic indentation of source code, printing and editing
of multiple documents in one window.

gedit is extensible through a plugin system, which currently includes
support for spell checking, comparing files, viewing CVS ChangeLogs, and
adjusting indentation levels. Further plugins can be found in the
gedit-plugins package.

%package devel
Summary: Support for developing plugins for the gedit text editor
Requires: %{name}%{?_isa} = %{epoch}:%{version}-%{release}

%description devel
gedit is a small, but powerful text editor for the GNOME desktop.
This package allows you to develop plugins that add new functionality
to gedit.

Install gedit-devel if you want to write plugins for gedit.

%prep
%autosetup -p1 -n %{name}-%{tarball_version}
tar --strip-components=1 -xf %{S:1} -C subprojects/libgd

%build
%meson -Dgtk_doc=true

# parallel make disabled to work around desktop file translations going missing
%define __ninja_common_opts -v
%meson_build

%install
%meson_install

%find_lang %{name} --with-gnome

%check
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/org.gnome.gedit.metainfo.xml
desktop-file-validate %{buildroot}%{_datadir}/applications/org.gnome.gedit.desktop

%files -f %{name}.lang
%doc README.md NEWS
%license COPYING
%{_bindir}/gedit
%{_datadir}/gedit/
%{_datadir}/applications/org.gnome.gedit.desktop
%{_mandir}/man1/gedit.1*
%{_libdir}/gedit/girepository-1.0/
%dir %{_libdir}/gedit
%dir %{_libdir}/gedit/plugins
%{_libdir}/gedit/libgedit-%{api_version}.so
%{_libdir}/gedit/plugins/codecomment.plugin
%{_libdir}/gedit/plugins/libcodecomment.so
%{_libdir}/gedit/plugins/docinfo.plugin
%{_libdir}/gedit/plugins/libdocinfo.so
%{_libdir}/gedit/plugins/filebrowser.plugin
%{_libdir}/gedit/plugins/libfilebrowser.so
%{_libdir}/gedit/plugins/modelines.plugin
%{_libdir}/gedit/plugins/libmodelines.so
%{_libdir}/gedit/plugins/quickhighlight.plugin
%{_libdir}/gedit/plugins/libquickhighlight.so
%{_libdir}/gedit/plugins/sort.plugin
%{_libdir}/gedit/plugins/libsort.so
%{_libdir}/gedit/plugins/spell.plugin
%{_libdir}/gedit/plugins/libspell.so
%{_libdir}/gedit/plugins/textsize.plugin
%{_libdir}/gedit/plugins/libtextsize.so
%{_libdir}/gedit/plugins/time.plugin
%{_libdir}/gedit/plugins/libtime.so
%{_datadir}/glib-2.0/schemas/org.gnome.gedit.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gedit.enums.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gedit.plugins.filebrowser.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gedit.plugins.filebrowser.enums.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gedit.plugins.spell.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gedit.plugins.time.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.gedit.plugins.time.enums.xml
%{_datadir}/dbus-1/services/org.gnome.gedit.service
%{_datadir}/icons/hicolor/*/apps/org.gnome.gedit.png
%{_datadir}/icons/hicolor/symbolic/apps/org.gnome.gedit-symbolic.svg
%{_metainfodir}/org.gnome.gedit.metainfo.xml

%files devel
%{_includedir}/gedit-%{api_version}/
%{_libdir}/pkgconfig/gedit.pc
%{_datadir}/gtk-doc/

%changelog
%autochangelog
