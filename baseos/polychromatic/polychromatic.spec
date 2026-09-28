# TODO: Use %elif below once openSUSE stable supports this (15.4 doesn't)

%if 0%{?mageia}
# Mageia doesn't have typelib(AppIndicator3)
%global __requires_exclude typelib\\(AppIndicator3\\)
%endif

#define gitcommit 71244ffd267a30278878adffe0c92bee1af7d1c9

Name: polychromatic
Version: 0.9.8
Release: 1.13
Summary: RGB lighting management front-end application for OpenRazer

License: GPL-3.0
URL: https://github.com/polychromatic/polychromatic

%if 0%{?gitcommit:1}
Source0: https://github.com/polychromatic/polychromatic/archive/%{gitcommit}.tar.gz
%else
Source0: https://github.com/polychromatic/polychromatic/archive/v%{version}.tar.gz
%endif
Patch0: polychromatic-device-support.patch
Source1: naga-v3-pro-with-side-plates.png

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
%autosetup -n polychromatic-%{version} -p1
%endif
install -m 0644 %{SOURCE1} data/devices/naga-v3-pro-with-side-plates.png

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
* Sun Sep 27 2026 Nobara local build - 0.9.8-1.13
- Remove HyperFlux Help, Diagnostics and Advanced buttons and firmware controls.
- Keep receiver status, driver auto-pairing, manual pairing and Refresh.
- Keep failure details in status tooltips without links to removed controls.

* Sun Sep 27 2026 Nobara local build - 0.9.8-1.12
- Replace verbose receiver instructions with compact standard device rows.
- Use the application-themed dialogs with default-No pairing confirmations.
- Move guidance, scan counters and firmware controls into Help/Diagnostics/Advanced.
- Defer page replacement during confirmation and recover inventory after scans.

* Sun Sep 27 2026 Nobara local build - 0.9.8-1.11
- Present sleeping wireless devices with a wake-up message and read-only retry.
- Keep tracebacks in optional details and distinguish busy or stale devices.
- Distinguish automatic discovery from pairing, with separate command counts.

* Sun Sep 27 2026 Nobara local build - 0.9.8-1.10
- Keep HyperFlux receiver and healthy devices visible when a child query fails.
- Show unavailable wireless child entries with explicit retry and error details.

* Sat Sep 26 2026 Nobara local build - 0.9.8-1.9
- Add explicit driver auto-pair enable/disable for mouse and keyboard slots.
- Display kernel policy and progress; keep firmware command separate.
- Handle dynamic HyperFlux keyboard entries using daemon hotplug notifications.

* Sat Sep 26 2026 Nobara local build - 0.9.8-1.8
- Use receiver-slot pairing for all reported mice/keyboards without model gates.
- Display capture coverage as a notice instead of disabling untested models.
- Retain per-receiver inventory controls and support HyperFlux keyboard children.

* Sat Sep 26 2026 Nobara local build - 0.9.8-1.7
- Build receiver pairing controls from the selected pad's live inventory.
- Do not show unpair buttons for absent or unsupported devices.
- Disable pairing actions when live inventory is unavailable.

* Wed Feb 08 2017 Luca Weiss <luca@z3ntu.xyz> 0.3.6.1.git-1
- Initial RPM release
