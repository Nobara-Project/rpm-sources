# TODO: Use %elif below once openSUSE stable supports this (15.4 doesn't)

%if 0%{?mageia}
# Mageia doesn't have typelib(AppIndicator3)
%global __requires_exclude typelib\\(AppIndicator3\\)
%endif

#define gitcommit 71244ffd267a30278878adffe0c92bee1af7d1c9

Name: polychromatic
Version: 0.9.8
Release: 1.1
Summary: RGB lighting management front-end application for OpenRazer

License: GPL-3.0
URL: https://github.com/polychromatic/polychromatic

%if 0%{?gitcommit:1}
Source0: https://github.com/polychromatic/polychromatic/archive/%{gitcommit}.tar.gz
%else
Source0: https://github.com/polychromatic/polychromatic/archive/v%{version}.tar.gz
%endif

BuildArch: noarch

Requires: python3
Requires: python3-colorama
Requires: python3-colour
Requires: python3-setproctitle
Requires: python3-requests
Requires: python3-openrazer
%if 0%{?mageia}
Requires: python3-qt6
%else
Requires: python3-PyQt6
%endif
%if 0%{?suse_version}
Requires: libQt6Svg6
%endif # TODO: %elif
%if 0%{?fedora}
Requires: qt6-qtsvg
%endif
%if 0%{?fedora}
Requires: python3-pyqt6-webengine
%endif # TODO: %elif
%if 0%{?mageia}
Requires: python3-qt6-webenginewidgets
%endif # TODO: %elif
%if 0%{?suse_version}
Requires: qt6-webengine
Requires: python3-PyQt6-WebEngine
%endif
%if 0%{?suse_version}
Requires: typelib(AppIndicator3)
%endif # TODO: %elif
%if 0%{?fedora}
Requires: libappindicator-gtk3
%endif
BuildRequires: rsync
BuildRequires: python3-devel
BuildRequires: intltool
BuildRequires: meson

%description
RGB lighting management front-end application for OpenRazer with a
graphical, command line and tray applet interface.

%prep
%if 0%{?gitcommit:1}
%autosetup -n polychromatic-%{gitcommit}
%else
%autosetup -n polychromatic-%{version}
%endif

%build
%meson
%meson_build

%install
%meson_install

%find_lang polychromatic

%clean
rm -rf $RPM_BUILD_ROOT


%files -f polychromatic.lang
%defattr(-,root,root,-)
%{_sysconfdir}/xdg/autostart/polychromatic-autostart.desktop
%{_bindir}/polychromatic-*
%{_datadir}/applications/polychromatic.desktop
%{_datadir}/icons/hicolor/
%{_datadir}/polychromatic/
%{_datadir}/metainfo/
%{python3_sitelib}/polychromatic/
%{_mandir}/man1/polychromatic-*

%changelog
* Wed Feb 08 2017 Luca Weiss <luca@z3ntu.xyz> 0.3.6.1.git-1
- Initial RPM release

