## START: Set by rpmautospec
## (rpmautospec version 0.6.3)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 1;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

%global glib_version 2.75.1
%global gtk3_version 3.19.8
%global gtk4_version 4.0.0
%global gsettings_desktop_schemas_version 40~alpha
%global json_glib_version 0.12.0
%global libinput_version 1.19.0
%global pipewire_version 0.3.33
%global lcms2_version 2.6
%global colord_version 1.4.5
%global libei_version 1.0.0
%global mutter_api_version 14

%global tarball_version %%(echo %{version} | tr '~' '.')

Name:          mutter
Version:       46.2
Release:       %autorelease
Summary:       Window and compositing manager based on Clutter

License:       GPLv2+
URL:           http://www.gnome.org
Source0:       http://download.gnome.org/sources/%{name}/46/%{name}-%{tarball_version}.tar.xz

# Work-around for OpenJDK's compliance test
Patch0:         0001-window-actor-Special-case-shaped-Java-windows.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=1936991
Patch1:         mutter-42.alpha-disable-tegra.patch

# https://pagure.io/fedora-workstation/issue/79
Patch2:         0001-place-Always-center-initial-setup-fedora-welcome.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=2239128
# https://gitlab.gnome.org/GNOME/mutter/-/issues/3068
# not upstreamed because for upstream we'd really want to find a way
# to fix *both* problems
Patch3:         0001-Revert-x11-Use-input-region-from-frame-window-for-de.patch

# https://gitlab.gnome.org/GNOME/mutter/-/merge_requests/3329
# Modified to add the change from
# https://gitlab.gnome.org/GNOME/mutter/-/merge_requests/3329#note_1874837
# which solves the problems reported with #3329 alone
Patch4: 0001-modified-3329.patch

# enable vrr setting
Patch5:        enable-vrr-setting.patch

# Nobara addons
Patch6:        enable-window-centering.patch
Patch7:	       mutter_increase_check_alive_timeout.patch

# Enable Fractional Scaling
Patch8:	       enable-fractional-scaling.patch

BuildRequires: pkgconfig(gobject-introspection-1.0) >= 1.41.0
BuildRequires: pkgconfig(sm)
BuildRequires: pkgconfig(libwacom)
BuildRequires: pkgconfig(x11)
BuildRequires: pkgconfig(xdamage)
BuildRequires: pkgconfig(xext)
BuildRequires: pkgconfig(xfixes)
BuildRequires: pkgconfig(xi)
BuildRequires: pkgconfig(xrandr)
BuildRequires: pkgconfig(xrender)
BuildRequires: pkgconfig(xcursor)
BuildRequires: pkgconfig(xcomposite)
BuildRequires: pkgconfig(x11-xcb)
BuildRequires: pkgconfig(xkbcommon)
BuildRequires: pkgconfig(xkbcommon-x11)
BuildRequires: pkgconfig(xkbfile)
BuildRequires: pkgconfig(xtst)
BuildRequires: mesa-libEGL-devel
BuildRequires: mesa-libGLES-devel
BuildRequires: mesa-libGL-devel
BuildRequires: mesa-libgbm-devel
BuildRequires: pkgconfig(glesv2)
BuildRequires: pkgconfig(graphene-gobject-1.0)
BuildRequires: pam-devel
BuildRequires: pkgconfig(libdisplay-info)
BuildRequires: pkgconfig(libpipewire-0.3) >= %{pipewire_version}
BuildRequires: pkgconfig(sysprof-capture-4)
BuildRequires: sysprof-devel
BuildRequires: pkgconfig(libsystemd)
BuildRequires: xorg-x11-server-Xorg
BuildRequires: xorg-x11-server-Xvfb
BuildRequires: pkgconfig(xkeyboard-config)
BuildRequires: desktop-file-utils
# Bootstrap requirements
BuildRequires: gettext-devel git-core
BuildRequires: pkgconfig(libcanberra)
BuildRequires: pkgconfig(gsettings-desktop-schemas) >= %{gsettings_desktop_schemas_version}
BuildRequires: pkgconfig(gnome-settings-daemon)
BuildRequires: meson
BuildRequires: pkgconfig(gbm)
BuildRequires: pkgconfig(gnome-desktop-4)
BuildRequires: pkgconfig(gudev-1.0)
BuildRequires: pkgconfig(libdrm)
BuildRequires: pkgconfig(libstartup-notification-1.0)
BuildRequires: pkgconfig(wayland-eglstream)
BuildRequires: pkgconfig(wayland-protocols)
BuildRequires: pkgconfig(wayland-server)
BuildRequires: pkgconfig(lcms2) >= %{lcms2_version}
BuildRequires: pkgconfig(colord) >= %{colord_version}
BuildRequires: pkgconfig(libei-1.0) >= %{libei_version}
BuildRequires: pkgconfig(libeis-1.0) >= %{libei_version}

BuildRequires: pkgconfig(json-glib-1.0) >= %{json_glib_version}
BuildRequires: pkgconfig(libinput) >= %{libinput_version}
BuildRequires: pkgconfig(xwayland)

BuildRequires: python3-dbusmock

Requires: control-center-filesystem
Requires: gsettings-desktop-schemas%{?_isa} >= %{gsettings_desktop_schemas_version}
Requires: gnome-settings-daemon
Requires: gtk4%{?_isa} >= %{gtk4_version}
Requires: json-glib%{?_isa} >= %{json_glib_version}
Requires: libinput%{?_isa} >= %{libinput_version}
Requires: pipewire%{_isa} >= %{pipewire_version}
Requires: startup-notification
Requires: dbus

# Need common
Requires: %{name}-common = %{version}-%{release}

Recommends: mesa-dri-drivers%{?_isa}

Provides: firstboot(windowmanager) = mutter

# Cogl and Clutter were forked at these versions, but have diverged
# significantly since then.
Provides: bundled(cogl) = 1.22.0
Provides: bundled(clutter) = 1.26.0

Conflicts: mutter < 45~beta.1-2

# Make sure dnf updates gnome-shell together with this package; otherwise we
# might end up with broken gnome-shell installations due to mutter ABI changes.
Conflicts: gnome-shell < 45~rc

%description
Mutter is a window and compositing manager that displays and manages
your desktop via OpenGL. Mutter combines a sophisticated display engine
using the Clutter toolkit with solid window-management logic inherited
from the Metacity window manager.

While Mutter can be used stand-alone, it is primarily intended to be
used as the display core of a larger system such as GNOME Shell. For
this reason, Mutter is very extensible via plugins, which are used both
to add fancy visual effects and to rework the window management
behaviors to meet the needs of the environment.

%package common
Summary: Common files used by %{name} and forks of %{name}
BuildArch: noarch
Conflicts: mutter < 45~beta.1-2

%description common
Common files used by Mutter and soft forks of Mutter

%package devel
Summary: Development package for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
# for EGL/eglmesaext.h that's included from public cogl-egl-defines.h header
Requires: mesa-libEGL-devel

%description devel
Header files and libraries for developing Mutter plugins. Also includes
utilities for testing Metacity/Mutter themes.

%package  tests
Summary:  Tests for the %{name} package
Requires: %{name}-devel%{?_isa} = %{version}-%{release}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: gtk3%{?_isa} >= %{gtk3_version}

%description tests
The %{name}-tests package contains tests that can be used to verify
the functionality of the installed %{name} package.

%prep
%autosetup -S git -n %{name}-%{tarball_version}

%build
%meson -Degl_device=true -Dwayland_eglstream=true
%meson_build

%install
%meson_install

%find_lang %{name}

%files -f %{name}.lang
%license COPYING
%doc NEWS
%{_bindir}/mutter
%{_libdir}/lib*.so.*
%{_libdir}/mutter-%{mutter_api_version}/
%{_libexecdir}/mutter-restart-helper
%{_libexecdir}/mutter-x11-frames
%{_mandir}/man1/mutter.1*

%files common
%{_datadir}/GConf/gsettings/mutter-schemas.convert
%{_datadir}/glib-2.0/schemas/org.gnome.mutter.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.mutter.wayland.gschema.xml
%{_datadir}/gnome-control-center/keybindings/50-mutter-*.xml
%{_udevrulesdir}/61-mutter.rules

%files devel
%{_includedir}/*
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*

%files tests
%{_libexecdir}/installed-tests/mutter-%{mutter_api_version}
%{_datadir}/installed-tests/mutter-%{mutter_api_version}
%{_datadir}/mutter-%{mutter_api_version}/tests

%changelog
## START: Generated by rpmautospec
* Sun Apr 21 2024 Florian Müllner <fmuellner@redhat.com> - 46.1-2
- Update downstream patch

* Sun Apr 21 2024 Florian Müllner <fmuellner@redhat.com> - 46.1-1
- Update to 46.1

* Sat Mar 16 2024 Florian Müllner <fmuellner@redhat.com> - 46.0-1
- Update to 46.0

* Sat Mar 16 2024 Florian Müllner <fmuellner@redhat.com> - 46~rc-4
- Use libdisplay-info

* Sat Mar 16 2024 Florian Müllner <fmuellner@redhat.com> - 46~rc-3
- Add missing build require

* Tue Mar 12 2024 Adam Williamson <awilliam@redhat.com> - 46~rc-2
- Backport MR #3642 to fix mouse wheel scrolling

* Sun Mar 03 2024 Florian Müllner <fmuellner@redhat.com> - 46~rc-1
- Update to 46.rc

* Fri Feb 16 2024 Michael Catanzaro <mcatanzaro@redhat.com> - 46~beta-3
- Defer fractional scaling feature to F41

* Fri Feb 16 2024 Florian Müllner <fmuellner@gnome.org> - 46~beta-2
- Rebuild for side-tag

* Sun Feb 11 2024 Florian Müllner <fmuellner@gnome.org> - 46~beta-1
- Update to 46.beta

* Thu Feb 08 2024 Adam Williamson <awilliam@redhat.com> - 46~alpha-5
- Backport MR #3539 to fix RHBZ #2261842

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 46~alpha-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 46~alpha-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 08 2024 Florian Müllner <fmuellner@gnome.org> - 46~alpha-2
- Fix i686 build

* Sun Jan 07 2024 Florian Müllner <fmuellner@gnome.org> - 46~alpha-1
- Update to 46.alpha

* Sat Dec 02 2023 Florian Müllner <fmuellner@gnome.org> - 45.2-1
- Update to 45.2

* Wed Nov 01 2023 Florian Müllner <fmuellner@gnome.org> - 45.1-1
- Update to 45.1

* Mon Oct 30 2023 Adam Williamson <awilliam@redhat.com> - 45.0-15
- Backport MRs #3311 and #3326 to fix screencast issues (#2247033)

* Tue Oct 24 2023 Adam Williamson <awilliam@redhat.com> - 45.0-14
- Update the #3329 backport with jadahl's proposed fix

* Fri Oct 20 2023 Kalev Lember <klember@redhat.com> - 45.0-13
- Backport upstream MR3329 to fix black screen in the installer (#2241632)

* Wed Oct 11 2023 Ray Strode <rstrode@redhat.com> - 45.0-12
- Update realtime-disabling patch to latest upstream revision

* Tue Oct 10 2023 Ray Strode <rstrode@redhat.com> - 45.0-11
- Drop real-time debugging patch

* Tue Oct 10 2023 Ray Strode <rstrode@redhat.com> - 45.0-10
- Disable realtime scheduling during modesets (#2240457)

* Fri Oct 06 2023 Adam Williamson <awilliam@redhat.com> - 45.0-9
- Revert a change to fix installer window interaction

* Fri Oct 06 2023 Adam Williamson <awilliam@redhat.com> - 45.0-8
- Don't number patches, it's no longer necessary and it's a lot simpler not
  to.

* Wed Oct 04 2023 Kalev Lember <klember@redhat.com> - 45.0-7
- Backport upstream MR3306 to fix issues with caps lock and accented
  letters

* Wed Oct 04 2023 Kalev Lember <klember@redhat.com> - 45.0-6
- Backport upstream MR3299 to fix disabling scale-monitor-framebuffer

* Sat Sep 30 2023 Ray Strode <rstrode@redhat.com> - 45.0-5
- Fix meson goo to install polkit rules in right place

* Sat Sep 30 2023 Ray Strode <rstrode@redhat.com> - 45.0-4
- Add polkit-gobject-1 dependency to fix build

* Sat Sep 30 2023 Ray Strode <rstrode@redhat.com> - 45.0-3
- Update files manifest to fix build

* Fri Sep 29 2023 Ray Strode <rstrode@redhat.com> - 45.0-2
- Add debugging patch from
  https://gitlab.gnome.org/GNOME/mutter/-/merge_requests/3293

* Sat Sep 16 2023 Florian Müllner <fmuellner@gnome.org> - 45.0-1
- Update to 45.0

* Wed Sep 06 2023 Kalev Lember <klember@redhat.com> - 45~rc-3
- Add conflicts with older gnome-shell versions

* Wed Sep 06 2023 Adam Williamson <awilliam@redhat.com> - 45~rc-2
- Rebuild on side tag to create combined update with gnome-shell

* Wed Sep 06 2023 Florian Müllner <fmuellner@gnome.org> - 45~rc-1
- Update to 45.rc

* Tue Sep 05 2023 Jonas Ådahl <jadahl@gmail.com> - 45~beta.1-5
- Enable fractional scaling by default

* Sat Sep 02 2023 Michael Catanzaro <mcatanzaro@redhat.com> - 45~beta.1-4
- Revert "Stop crashing on idle"

* Fri Sep 01 2023 Michael Catanzaro <mcatanzaro@redhat.com> - 45~beta.1-3
- Stop crashing on idle

* Tue Aug 15 2023 Joshua Strobl <me@joshuastrobl.com> - 45~beta.1-2
- Split common mutter files into subpackage for consumption by soft-forks
  without creating conflicts

* Fri Aug 11 2023 Florian Müllner <fmuellner@gnome.org> - 45~beta.1-1
- Update to 45.beta.1

* Thu Aug 10 2023 Adam Williamson <awilliam@redhat.com> - 45~beta-7
- Backport MR #3163 to help fix broken alt-tab behavior

* Wed Aug 09 2023 Kalev Lember <klember@redhat.com> - 45~beta-6
- Backport #3168 to fix mouse clicks sometimes going missing

* Tue Aug 08 2023 Kalev Lember <klember@redhat.com> - 45~beta-5
- Revert "compositor: Do not repick after effects finish"

* Tue Aug 08 2023 Adam Williamson <awilliam@redhat.com> - 45~beta-4
- Backport #3162 to fix super key not triggering overview

* Tue Aug 08 2023 Adam Williamson <awilliam@redhat.com> - 45~beta-3
- Revert "Revert "compositor: Do not repick after effects finish""

* Tue Aug 08 2023 Kalev Lember <klember@redhat.com> - 45~beta-2
- Revert "compositor: Do not repick after effects finish"

* Tue Aug 08 2023 Florian Müllner <fmuellner@gnome.org> - 45~beta-1
- Update to 45.beta

* Mon Aug 07 2023 Sandro Bonazzola <sbonazzo@redhat.com> - 45~alpha-7
- address rpmdeps test suggestions

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 45~alpha-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jul 12 2023 Sandro Bonazzola <sbonazzo@redhat.com> - 45~alpha-5
- Drop confusing comment from previous commit

* Wed Jul 12 2023 Sandro Bonazzola <sbonazzo@redhat.com> - 45~alpha-4
- Drop build requirement on zenity

* Wed Jul 12 2023 Sandro Bonazzola <sbonazzo@redhat.com> - 45~alpha-3
- Drop gtk-doc dependency

* Wed Jul 12 2023 Sandro Bonazzola <sbonazzo@redhat.com> - 45~alpha-2
- move gtk3 only to tests sub-package

* Thu Jul 06 2023 Florian Müllner <fmuellner@gnome.org> - 45~alpha-1
- Update to 45.alpha

* Thu Jun 08 2023 Florian Müllner <fmuellner@gnome.org> - 44.2-2
- Drop upstreamed patch

* Sat Jun 03 2023 Florian Müllner <fmuellner@gnome.org> - 44.2-1
- Update to 44.2

* Wed May 24 2023 David King <amigadave@amigadave.com> - 44.1-2
- Drop merged patch

* Tue Apr 25 2023 Florian Müllner <fmuellner@gnome.org> - 44.1-1
- Update to 44.1

* Tue Apr 18 2023 Adam Williamson <awilliam@redhat.com> - 44.0-2
- Backport MR #2954 to fix X.org click-to-raise (#2187831)

* Sun Mar 19 2023 Florian Müllner <fmuellner@redhat.com> - 44.0-1
- Update to 44.0

* Thu Mar 16 2023 Adam Williamson <awilliam@redhat.com> - 44~rc-5
- Backport MR #2901 to fix crash when reverting Display settings
- Backport MR #2912 to fix crash when using win+P shortcut

* Fri Mar 10 2023 Florian Müllner <fmuellner@redhat.com> - 44~rc-4
- Fix typo in centering patch
- Also check for possible future fedora-welcome ID

* Thu Mar 09 2023 Adam Williamson <awilliam@redhat.com> - 44~rc-3
- From Florian: adjust centering patch to not crash on null values
- Backport MR #2906 to fix g-i-s startup problems (#2176700)

* Mon Mar 06 2023 Florian Müllner <fmuellner@redhat.com> - 44~rc-1
- Update to 44.rc

* Sat Mar 04 2023 Ray Strode <rstrode@redhat.com> - 44~beta-3
- Add some backports of Carlos's focus fixes
  Related: #2173985

* Mon Feb 20 2023 Adam Williamson <awilliam@redhat.com> - 44~beta-2
- Rebuild without changes for Bodhi reasons

* Tue Feb 14 2023 Florian Müllner <fmuellner@redhat.com> - 44~beta-1
- Update to 44.beta

* Fri Feb 10 2023 Jonas Ådahl <jadahl@redhat.com> - 43.2-2
- Backport patches on the gnome-43 branch

* Fri Feb 10 2023 Adam Williamson <awilliam@redhat.com> - 43.2-1
- Update to 43.2

* Fri Feb 10 2023 Adam Williamson <awilliam@redhat.com> - 43.1-6
- Drop zenity requirement (upstream dropped it in 43-alpha)

* Sun Jan 29 2023 Stefan Bluhm <stefan.bluhm@clacee.eu> - 43.1-5
- Fixed broken Fedora condition.

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 43.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Jan 17 2023 Olivier Fourdan <ofourdan@redhat.com> - 43.1-3
- Add Xwayland byte-swapped clients support on Fedora 38 and above (#2159489)

* Thu Nov 17 2022 Jonas Ådahl <jadahl@redhat.com> - 43.1-2
- Backport regression fixes

* Fri Nov 04 2022 Florian Müllner <fmuellner@redhat.com> - 43.1-1
- Update to 43.1

* Tue Sep 27 2022 Kalev Lember <klember@redhat.com> - 43.0-3
- Rebuild to fix sysprof-capture symbols leaking into libraries consuming it

* Thu Sep 22 2022 Kalev Lember <klember@redhat.com> - 43.0-2
- Backport upstream MR2623 to fix night light controls
- Backport upstream MR2624 to fix maximized windows appearing on all
  screens (#2128660)

* Sat Sep 17 2022 Florian Müllner <fmuellner@redhat.com> - 43.0-1
- Update to 43.0

* Sun Sep 04 2022 Florian Müllner <fmuellner@redhat.com> - 43~rc-1
- Update to 43.rc

* Thu Aug 25 2022 Kalev Lember <klember@redhat.com> - 43~beta-4
- wayland: Unlink surface listener when freeing token

* Thu Aug 25 2022 Kalev Lember <klember@redhat.com> - 43~beta-3
- wayland: Ensure to unlink destroy listeners after destruction

* Wed Aug 24 2022 Kalev Lember <klember@redhat.com> - 43~beta-2
- Backport upstream patch to fix a compositor crash (#2120470)

* Wed Aug 10 2022 Florian Müllner <fmuellner@redhat.com> - 43~beta-1
- Update to 43.beta

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 43~alpha-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sun Jul 10 2022 Florian Müllner <fmuellner@redhat.com> - 43~alpha-1
 - Update to 43.alpha

* Sun May 29 2022 Florian Müllner <fmuellner@redhat.com> - 42.2-1
- Update to 42.2

* Fri May 06 2022 Florian Müllner <fmuellner@redhat.com> - 42.1-1
- Update to 42.1

* Mon May 02 2022 Adam Williamson <awilliam@redhat.com> - 42.0-6
- Backport MR #2359 to fix GNOME on legacy Radeon (#2081070)

* Tue Apr 19 2022 Adam Williamson <awilliam@redhat.com> - 42.0-5
- Backport MR #2366 to fix stuck modifier key issues (#2076390)
- Backport MR #2321 to fix top bar hover issues

* Mon Apr 18 2022 Adam Williamson <awilliam@redhat.com> - 42.0-4
- Backport MR #2333 to fix partial lock on interrupted dimming (#2073206)

* Thu Mar 31 2022 Adam Williamson <awilliam@redhat.com> - 42.0-3
- Backport MR #2353 to fix overview search with input methods (#2062660)

* Mon Mar 14 2022 Adam Williamson <awilliam@redhat.com> - 42.0-2
- Backport MR #2299 to avoid a commonly-encountered crash (#2063381)

* Sun Mar 13 2022 Florian Müllner <fmuellner@redhat.com> - 42.0-1
- Update to 42.0

* Thu Mar 10 2022 Adam Williamson <awilliam@redhat.com> - 42~rc-4
- Update MR #2331 backport again

* Wed Mar 09 2022 Adam Williamson <awilliam@redhat.com> - 42~rc-3
- Update MR #2331 backport

* Tue Mar 08 2022 Adam Williamson <awilliam@redhat.com> - 42~rc-2
- Backport MR #2331 for input device capabilities (#2017043)

* Mon Mar 07 2022 Florian Müllner <fmuellner@redhat.com> - 42~rc-1
- Update to 42.rc

* Mon Feb 14 2022 Florian Müllner <fmuellner@redhat.com> - 42~beta-1
- Update to 42.beta

* Thu Jan 27 2022 Adam Williamson <awilliam@redhat.com> - 42~alpha-3
- Drop a test setup to fix build with latest glibc (catchsegv removed)
- Backport MR #2257 to fix clicks on burger menus failing in openQA

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 42~alpha-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jan 14 2022 David King <amigadave@amigadave.com> - 42~alpha-1
- Update to 42~alpha
- Use pkgconfig for BuildRequires

* Mon Dec 13 2021 Peter Hutterer <peter.hutterer@redhat.com> - 41.0-5
- Rebuild for libwacom soname bump

* Mon Oct 25 2021 Adam Williamson <awilliam@redhat.com> - 41.0-4
- Backport MR #2059 to fix cursor jumping around in text editors (#2017192)

* Tue Oct 05 2021 Adam Williamson <awilliam@redhat.com> - 41.0-3
- Backport MR #2040 to fix cursor offset in VMs (#2009304)

* Mon Sep 20 2021 Kalev Lember <klember@redhat.com> - 41.0-2
- Add missing mesa-libEGL-devel dep to mutter-devel (#2002441)

* Sun Sep 19 2021 Florian Müllner <fmuellner@redhat.com> - 41.0-1
- Update to 41.0

* Sun Sep 05 2021 Florian Müllner <fmuellner@redhat.com> - 41~rc
- Update to 41.rc

* Wed Aug 18 2021 Florian Müllner <fmuellner@redhat.com> - 41~beta
- Update to 41.beta

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 40.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jul 12 2021 Florian Müllner <fmuellner@redhat.com> - 40.3-1
- Update to 40.3

* Mon Jun 14 2021 Florian Müllner <fmuellner@redhat.com> - 40.2.1-1
- Update to 40.2.1

* Thu Jun 10 2021 Florian Müllner <fmuellner@redhat.com> - 40.2-1
- Update to 40.2

* Thu May 13 2021 Florian Müllner <fmuellner@redhat.com> - 40.1-1
- Update to 40.1

* Tue Apr 13 2021 Kalev Lember <klember@redhat.com> - 40.0-6
- Recommend mesa-dri-drivers

* Wed Apr 07 2021 Jonas Ådahl <jadahl@redhat.com> - 40.0-5
- Fix crash on resume fix regression (rhbz#1946652)

* Tue Mar 30 2021 Kalev Lember <klember@redhat.com> - 40.0-4
- Fix enter, space, backspace keys not working with input methods (#1942294)
- Drop old obsoletes and conflicts

* Mon Mar 29 2021 Jonas Ådahl <jadahl@redhat.com> - 40.0-3
- Fix crash on resume (rhbz#1941971)

* Fri Mar 26 2021 Kalev Lember <klember@redhat.com> - 40.0-2
- Rebuild to fix sysprof-capture symbols leaking into libraries consuming it

* Sat Mar 20 2021 Florian Müllner <fmuellner@redhat.com> - 40.0-1
- Update to 40.0

* Mon Mar 15 2021 Florian Müllner <fmuellner@redhat.com> - 40.0~rc-1
- Update to 40.rc

* Fri Mar 12 2021 Benjamin Berg <bberg@redhat.com> - 40.0~beta-3
- Pull in Xwayland autostart fix for non-systemd startup
  Resolves: #1924908

* Tue Mar 09 2021 Adam Williamson <awilliam@redhat.com> - 40.0~beta-2
- Add a workaround for RHBZ#1936991 (disable atomic KMS on tegra)

* Mon Feb 22 2021 Florian Müllner <fmuellner@redhat.com> - 40.0~beta-1
- Update to 40.beta

* Tue Feb 02 2021 Florian Müllner <fmuellner@redhat.com> - 40.0~alpha.1.1-4.20210202gita9d9aee6c
- Build snapshot of current upstream

* Mon Feb  1 2021 Olivier Fourdan <ofourdan@redhat.com> - 40.0~alpha.1.1-3
- Add build dependency on Xwayland-devel package (from Xwayland standalone)
- Do not explicitly disable initfd support.

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 40.0~alpha.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Jan 14 2021 Florian Müllner <fmuellner@redhat.com> - 40.0~alpha.1.1-1
- Update to 40.alpha.1.1 to adjust for GSettings schema changes in g-s-d

* Thu Jan 14 2021 Florian Müllner <fmuellner@redhat.com> - 40.0~alpha.1-1
- Update to 40.alpha.1

* Wed Dec 02 2020 Florian Müllner <fmuellner@redhat.com> - 40.alpha-1
- Update to 40.alpha

* Mon Oct 05 2020 Florian Müllner <fmuellner@redhat.com> - 3.38.1-1
- Update to 3.38.1

* Mon Sep 28 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 3.38.0-2
- Upstream fix for NVidia Jetson devices

* Mon Sep 14 2020 Florian Müllner <fmuellner@redhat.com> - 3.38.0-1
- Update to 3.38.0

* Sat Sep 05 2020 Florian Müllner <fmuellner@redhat.com> - 3.37.92-1
- Update to 3.37.92

* Mon Aug 24 2020 Florian Müllner <fmuellner@redhat.com> - 3.37.91-1
- Update to 3.37.91

* Tue Aug 11 2020 Florian Müllner <fmuellner@redhat.com> - 3.37.90-1
- Update to 3.37.90

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.37.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 07 2020 Florian Müllner <fmuellner@redhat.com> - 3.37.3-1
- Update to 3.37.3

* Wed Jun 03 2020 Florian Müllner <fmuellner@redhat.com> - 3.37.2-1
- Update to 3.37.2

* Thu Apr 30 2020 Florian Müllner <fmuellner@redhat.com> - 3.37.1-1
- Update to 3.37.1

* Mon Mar 30 2020 Florian Müllner <fmuellner@redhat.com> - 3.36.1-1
- Update to 3.36.1

* Tue Mar 24 2020 Adam Williamson <awilliam@redhat.com> - 3.36.0-3
- Backport all patches to git master for various fixes inc (#1809717)

* Mon Mar 23 2020 Adam Williamson <awilliam@redhat.com> - 3.36.0-2
- Backport fix for preedit cursor position bug (#1812449)

* Sat Mar 07 2020 Florian Müllner <fmuellner@redhat.com> - 3.36.0-1
- Update to 3.36.0

* Fri Mar 06 2020 Adam Williamson <awilliam@redhat.com> - 3.35.92-3
- Backport fix for pop-up menus on secondary heads (Gitlab #1098)

* Tue Mar 03 2020 Bastien Nocera <bnocera@redhat.com> - 3.35.92-2
+ mutter-3.35.92-2
- Fix wayland session not starting up, see https://gitlab.gnome.org/GNOME/mutter/-/merge_requests/1103

* Sun Mar 01 2020 Florian Müllner <fmuellner@redhat.com> - 3.35.92-1
- Update to 3.35.92

* Mon Feb 17 2020 Florian Müllner <fmuellner@redhat.com> - 3.35.91-1
- Update to 3.35.91

* Thu Feb 06 2020 Florian Müllner <fmuellner@redhat.com> - 3.35.90-1
- Update to 3.35.90

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.35.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jan 16 2020 Kalev Lember <klember@redhat.com> - 3.35.3-2
- Rebuilt for libgnome-desktop soname bump

* Sun Jan 05 2020 Florian Müllner <fmuellner@redhat.com> - 3.35.3-1
- Update to 3.35.3

* Wed Dec 11 2019 Florian Müllner <fmuellner@redhat.com> - 3.35.2-1
- Update to 3.35.2

* Tue Oct 29 2019 Florian Müllner <fmuellner@redhat.com> - 3.35.1-3
- Enable sysprof support
  The required dependency was missing from rawhide when the feature
  landed, but there's no reason for keeping it disabled nowadays

* Mon Oct 14 2019 Adam Williamson <awilliam@redhat.com> - 3.35.1-2
- Update MR #832 backport to fully fix cursor zoom bug (#1749433)

* Sat Oct 12 2019 Florian Müllner <fmuellner@redhat.com> - 3.35.1-1
- Update to 3.35.1

* Sat Oct 12 2019 Adam Williamson <awilliam@redhat.com> - 3.34.1-2
- Backport multiple fixes for F31 FE/blocker bugs:
  MR #832 for #1749433 (also needs change in gnome-shell)
  MR #840 for #1760254
  MR #848 for #1751646 and #1759644
  MR #842 for #1758873

* Wed Oct 09 2019 Florian Müllner <fmuellner@redhat.com> - 3.34.1-1
- Update to 3.34.1

* Sat Sep 28 2019 Kenneth Topp <toppk@bllue.org> - 3.34.0-5
- Backport fix for dual special modifier keys bug (#1754867)
- Backport fix that enables core dumps (#1748145)

* Fri Sep 27 2019 Kenneth Topp <toppk@bllue.org> - 3.34.0-4
- Backport a patch to prevent crash during animations
- See upstream issue https://gitlab.gnome.org/GNOME/mutter/issues/815

* Thu Sep 12 2019 Kalev Lember <klember@redhat.com> - 3.34.0-3
- Update previous patch to final upstream version

* Wed Sep 11 2019 Kalev Lember <klember@redhat.com> - 3.34.0-2
- Backport a patch to fix xsettings/ibus-x11 initialization (#1750512)

* Mon Sep 09 2019 Florian Müllner <fmuellner@redhat.com> - 3.34.0-1
- Update to 3.34.0

* Wed Sep 04 2019 Florian Müllner <fmuellner@redhat.com> - 3.33.92-1
- Update to 3.33.92

* Tue Sep 03 2019 Ray Strode <rstrode@redhat.com> - 3.33.91-2
- Fix crash dealing with powersaving
  Resolves: #1747845

* Wed Aug 21 2019 Florian Müllner <fmuellner@redhat.com> - 3.33.91-1
- Update to 3.33.91

* Sat Aug 10 2019 Florian Müllner <fmuellner@redhat.com> - 3.33.90-1
- Update to 3.33.90

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.33.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jul 21 2019 Kalev Lember <klember@redhat.com> - 3.33.4-2
- Rebuilt for libgnome-desktop soname bump

* Sat Jul 20 2019 Florian Müllner <fmuellner@redhat.com> - 3.33.4-1
- Update to 3.33.4

* Mon Jun 24 2019 Florian Müllner <fmuellner@redhat.com> - 3.33.3-1
- Update to 3.33.3

* Wed May 22 2019 Florian Müllner <fmuellner@redhat.com> - 3.33.2-1
- Update to 3.33.2

* Tue May 14 2019 Florian Müllner <fmuellner@redhat.com> - 3.33.1-1
- Update to 3.33.1

* Wed Apr 17 2019 Florian Müllner <fmuellner@redhat.com> - 3.32.1-1
- Update to 3.32.1

* Wed Apr 17 2019 Adam Williamson <awilliam@redhat.com> - 3.32.0-4
- Backport MR #498 for spinner bug, plus two crasher fixes
  Resolves: #1692135

* Tue Apr 16 2019 Adam Williamson <awilliam@redhat.com> - 3.32.0-3
- Rebuild with Meson fix for #1699099

* Mon Mar 25 2019 Adam Williamson <awilliam@redhat.com> - 3.32.0-2
- Backport work-around for hangul text input bug (rhbz#1632981)

* Tue Mar 12 2019 Florian Müllner <fmuellner@redhat.com> - 3.32.0-1
- Update to 3.32.0

* Fri Mar 08 2019 Kalev Lember <klember@redhat.com> - 3.31.92-3
- Backport more inverted colour fixes (#1686649)

* Wed Mar 06 2019 Kalev Lember <klember@redhat.com> - 3.31.92-2
- Backport a patch to fix inverted colours

* Tue Mar 05 2019 Florian Müllner <fmuellner@redhat.com> - 3.31.92-1
- Update to 3.31.92

* Thu Feb 21 2019 Florian Müllner <fmuellner@redhat.com> - 3.31.91-1
- Update to 3.31.91

* Thu Feb 07 2019 Florian Müllner <fmuellner@redhat.com> - 3.31.90-1
- Update to 3.31.90

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.31.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jan 10 2019 Florian Müllner <fmuellner@redhat.com> - 3.31.4-1
- Update to 3.31.4

* Sat Nov 17 2018 Kalev Lember <klember@redhat.com> - 3.31.2-2
- Remove libtool .la files from private libs (#1622944)

* Wed Nov 14 2018 Florian Müllner <fmuellner@redhat.com> - 3.31.2-1
- Update to 3.31.2

* Mon Oct 22 2018 Jonas Ådahl <jadahl@redhat.com> - 3.30.1-5
- Backport work-around for hangul text input bug (rhbz#1632981)

* Sat Oct 20 2018 Jonas Ådahl <jadahl@redhat.com> - 3.30.1-4
- Backport a couple of memory leak fixes (rhbz#1641254)

* Thu Oct 11 2018 Jonas Ådahl <jadahl@redhat.com> - 3.30.1-3
- Fix disabled monitor when laptop lid is closed (rhbz#1638444)

* Thu Oct 11 2018 David Herrmann <dh.herrmann@gmail.com> - 3.30.1-2
- Reduce 'dbus-x11' dependency to 'dbus'. The xinit script are no longer the
  canonical way to start dbus, but the 'dbus' package is nowadays required to
  provide a user and system bus to its dependents.

* Mon Oct 08 2018 Florian Müllner <fmuellner@redhat.com> - 3.30.1-1
- Update to 3.30.1

* Wed Oct 03 2018 Adam Williamson <awilliam@redhat.com> - 3.30.0-3
- Backport fix for #1630943 from upstream master

* Thu Sep 06 2018 Mateusz Mikuła <mati865@gmail.com> - 3.30.0-2
- Enable EGLDevice support

* Tue Sep 04 2018 Florian Müllner <fmuellner@redhat.com> - 3.30.0-1
- Update to 3.30.0

* Wed Aug 29 2018 Florian Müllner <fmuellner@redhat.com> - 3.29.92-1
- Update to 3.29.92

* Mon Aug 20 2018 Florian Müllner <fmuellner@redhat.com> - 3.29.91-1
- Update to 3.29.91

* Wed Aug 01 2018 Jan Grulich <jgrulich@redhat.com> - 3.29.90-2
- Update libpipewire requirements

* Wed Aug 01 2018 Florian Müllner <fmuellner@redhat.com> - 3.29.90-1
- Update to 3.29.90

* Tue Jul 24 2018 Adam Williamson <awilliam@redhat.com> - 3.29.4-2
- Backport MR#175 to fix 90/270 degree screen rotation

* Wed Jul 18 2018 Florian Müllner <fmuellner@redhat.com> - 3.29.4-1
- Update to 3.29.4

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.29.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 01 2018 Adam Williamson <awilliam@redhat.com> - 3.29.2-2
- Backport crasher fix from upstream master (#1585360)

* Thu May 24 2018 Florian Müllner <fmuellner@redhat.com> - 3.29.2-1
- Update to 3.29.2

* Wed Apr 25 2018 Florian Müllner <fmuellner@redhat.com> - 3.29.1-1
- Update to 3.29.1

* Fri Apr 13 2018 Florian Müllner <fmuellner@redhat.com> - 3.28.1-1
- Update to 3.28.1

* Mon Mar 12 2018 Florian Müllner <fmuellner@redhat.com> - 3.28.0-1
- Update to 3.28.0

* Mon Mar 05 2018 Florian Müllner <fmuellner@redhat.com> - 3.27.92-1
- Update to 3.27.92

* Wed Feb 28 2018 Adam Williamson <awilliam@redhat.com> - 3.27.91-2
- Backport MR#36 to fix RHBZ #1547691 (GGO #2), mouse issues

* Wed Feb 21 2018 Florian Müllner <fmuellner@redhat.com> - 3.27.91-1
- Update to 3.27.91

* Tue Feb 13 2018 Björn Esser <besser82@fedoraproject.org> - 3.27.1-4
- Rebuild against newer gnome-desktop3 package
- Add patch for adjustments to pipewire 0.1.8 API

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.27.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Jan 06 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.27.1-2
- Remove obsolete scriptlets

* Mon Oct 30 2017 Florian Müllner <fmuellner@redhat.com> - 3.27.1-1
- Include 32-bit build fixes

* Tue Oct 17 2017 Florian Müllner <fmuellner@redhat.com> - 3.27.1-1
- Update to 3.27.1

* Fri Oct 06 2017 Florian Müllner <fmuellner@redhat.com> - 3.26.1-2
- Fix screencasts

* Wed Oct 04 2017 Florian Müllner <fmuellner@redhat.com> - 3.26.1-1
- Update to 3.26.1

* Thu Sep 21 2017 Florian Müllner <fmuellner@redhat.com> - 3.26.0-5
- Adjust to pipewire API break

* Wed Sep 20 2017 Florian Müllner <fmuellner@redhat.com> - 3.26.0-5
- Enable tablet support

* Tue Sep 12 2017 Adam Williamson <awilliam@redhat.com> - 3.26.0-4
- Also backport BGO #787570 fix from upstream

* Tue Sep 12 2017 Adam Williamson <awilliam@redhat.com> - 3.26.0-3
- Backport upstream fixes for crasher bug BGO #787568

* Tue Sep 12 2017 Florian Müllner <fmuellner@redhat.com> - 3.26.0-2
- Enable remote desktop support

* Tue Sep 12 2017 Florian Müllner <fmuellner@redhat.com> - 3.26.0-1
- Update to 3.26.0

* Thu Sep 07 2017 Florian Müllner <fmuellner@redhat.com> - 3.25.92-1
- Update to 3.25.92

* Thu Aug 24 2017 Bastien Nocera <bnocera@redhat.com> - 3.25.91-2
+ mutter-3.25.91-2
- Fix inverted red and blue channels with newer Mesa

* Tue Aug 22 2017 Florian Müllner <fmuellner@redhat.com> - 3.25.91-1
- Update to 3.25.91

* Thu Aug 10 2017 Florian Müllner <fmuellner@redhat.com> - 3.25.90-1
- Update to 3.25.90

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.25.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.25.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jul 19 2017 Florian Müllner <fmuellner@redhat.con> - 3.25.4-1
- Update to 3.25.4

* Wed Jun 21 2017 Florian Müllner <fmuellner@redhat.com> - 3.25.3-1
- Update to 3.25.3

* Wed May 24 2017 Florian Müllner <fmuellner@redhat.com> - 3.25.2-1
- Update to 3.25.2

* Thu May 18 2017 Florian Müllner <fmuellner@redhat.com> - 3.25.1-2
- Fix copy+paste of UTF8 strings between X11 and wayland

* Thu Apr 27 2017 Florian Müllner <fmuellner@redhat.com> - 3.25.1-1
- Update to 3.25.1

* Tue Apr 11 2017 Florian Müllner <fmuellner@redhat.com> - 3.24.1-1
- Update to 3.24.1

* Mon Mar 20 2017 Florian Müllner <fmuellner@redhat.com> - 3.24.0-1
- Update to 3.24.0

* Tue Mar 14 2017 Florian Müllner <fmuellner@redhat.com> - 3.23.92-1
- Update to 3.23.92

* Fri Mar 10 2017 Florian Müllner <fmuellner@redhat.com> - 3.23.91-4
- Apply startup-notification hack again

* Tue Mar 07 2017 Adam Williamson <awilliam@redhat.com> - 3.23.91-3
- Backport more color fixes, should really fix BGO #779234, RHBZ #1428559

* Thu Mar 02 2017 Adam Williamson <awilliam@redhat.com> - 3.23.91-2
- Backport fix for a color issue in 3.23.91 (BGO #779234, RHBZ #1428559)

* Wed Mar 01 2017 Florian Müllner <fmuellner@redhat.com> - 3.23.91-1
- Update to 3.23.91

* Thu Feb 16 2017 Florian Müllner <fmuellner@redhat.com> - 3.23.90-1
- Update to 3.23.90

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.23.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Dec 15 2016 Florian Müllner <fmuellner@redhat.com> - 3.23.3-1
- Update to 3.23.3

* Fri Dec 02 2016 Florian Müllner <fmuellner@redhat.com> - 3.23.2-2
- Fix build error on 32-bit platforms

* Thu Nov 24 2016 Kevin Fenzi <kevin@scrye.com> - 3.23.2-2
- Some fixes to get building. Still needs patch1 rebased.

* Wed Nov 23 2016 Florian Müllner <fmuellner@redhat.com> - 3.23.2-1
- Update to 3.23.2

* Tue Nov  8 2016 Matthias Clasen <mclasen@redhat.com> - 3.23.1-2
- Fix 1376471

* Sun Oct 30 2016 Florian Müllner <fmuellner@redhat.com> - 3.23.1-1
- Update to 3.23.1

* Tue Oct 18 2016 Kalev Lember <klember@redhat.com> - 3.22.1-3
- Backport a fix to make gnome-screenshot --area work

* Tue Oct 11 2016 Adam Jackson <ajax@redhat.com> - 3.22.1-2
- Prefer eglGetPlatformDisplay() to eglGetDisplay()

* Tue Oct 11 2016 Florian Müllner <fmuellner@redhat.com> - 3.22.1-1
- Update to 3.22.1

* Wed Sep 28 2016 Florian Müllner <fmuellner@redhat.com> - 3.22.0-2
- Include fix for crash on VT switch

* Mon Sep 19 2016 Florian Müllner <fmuellner@redhat.com> - 3.22.0-1
- Update to 3.22.0

* Tue Sep 13 2016 Florian Müllner <fmuellner@redhat.com> - 3.21.92-1
- Update to 3.21.92

* Thu Sep 08 2016 Kalev Lember <klember@redhat.com> - 3.21.91-2
- wayland/cursor-role: Increase buffer use count on construction (#1373372)

* Tue Aug 30 2016 Florian Müllner <fmuellner@redhat.com> - 3.21.91-1
- Update to 3.21.91

* Mon Aug 29 2016 Kalev Lember <klember@redhat.com> - 3.21.90-3
- clutter/evdev: Fix absolute pointer motion events (#1369492)

* Sat Aug 20 2016 Kalev Lember <klember@redhat.com> - 3.21.90-2
- Update minimum dep versions

* Fri Aug 19 2016 Florian Müllner <fmuellner@redhat.com> - 3.21.90-1
- Update to 3.21.90

* Wed Jul 20 2016 Florian Müllner <fmuellner@redhat.com> - 3.21.4-1
- Update to 3.21.4
- Drop downstream patch
- Fix build error on 32-bit

* Tue Jun 21 2016 Florian Müllner <fmuellner@redhat.com> - 3.21.3-1
- Update to 3.21.3

* Fri May 27 2016 Florian Müllner <fmuellner@redhat.com> - 3.21.2-1
- Update to 3.21.2

* Fri Apr 29 2016 Florian Müllner <fmuellner@redhat.com> - 3.21.1-1
- Update to 3.21.1

* Wed Apr 13 2016 Florian Müllner <fmuellner@redhat.com> - 3.20.1-1
- Update to 3.20.1

* Tue Mar 22 2016 Florian Müllner <fmuellner@redhat.com> - 3.20.0-1
- Update to 3.20.0

* Wed Mar 16 2016 Florian Müllner <fmuellner@redhat.com> - 3.19.92-1
- Update to 3.19.92

* Thu Mar 03 2016 Florian Müllner <fmuellner@redhat.com> - 3.19.91-2
- Include fix for invalid cursor wl_buffer access

* Thu Mar 03 2016 Florian Müllner <fmuellner@redhat.com> - 3.19.91-1
- Update to 3.19.91

* Fri Feb 19 2016 Florian Müllner <fmuellner@redhat.com> - 3.19.90-1
- Update to 3.19.90

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.19.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jan 21 2016 Florian Müllner <fmuellner@redhat.com> - 3.19.4-1
- Update to 3.19.4

* Thu Dec 17 2015 Florian Müllner <fmuellner@redhat.com> - 3.19.3-1
- Update to 3.19.3

* Wed Nov 25 2015 Florian Müllner <fmuellner@redhat.com> - 3.19.2-1
- Update to 3.19.2

* Tue Nov 10 2015 Ray Strode <rstrode@redhat.com> 3.19.1-5.20151110git049f1556d
- Update to git snapshot

* Thu Oct 29 2015 Florian Müllner <fmuellner@redhat.com> - 3.19.1-1
- Update to 3.19.1

* Wed Oct 21 2015 Ray Strode <rstrode@redhat.com> 3.18.1-4
- Force the cursor visible on vt switches after setting
  the crtc to workaround that qxl bug from before in a
  different situation
  Related: #1273247

* Wed Oct 21 2015 Kalev Lember <klember@redhat.com> - 3.18.1-3
- Backport a fix for a common Wayland crash (#1266486)

* Thu Oct 15 2015 Kalev Lember <klember@redhat.com> - 3.18.1-2
- Bump gnome-shell conflicts version

* Thu Oct 15 2015 Florian Müllner <fmuellner@redhat.com> - 3.18.1-1
- Update to 3.18.1

* Mon Sep 21 2015 Florian Müllner <fmuellner@redhat.com> - 3.18.0-1
- Update to 3.18.0

* Wed Sep 16 2015 Florian Müllner <fmuellner@redhat.com> - 3.17.92-1
- Update to 3.17.92

* Thu Sep 03 2015 Florian Müllner <fmuellner@redhat.com> - 3.17.91-1
- Update to 3.17.91

* Thu Sep 03 2015 Ray Strode <rstrode@redhat.com> 3.17.90-2
- Add workaround for qxl cursor visibility wonkiness that we
  did for f22
  Related: #1200901

* Thu Aug 20 2015 Florian Müllner <fmuellner@redhat.com> - 3.17.90-1
- Update to 3.17.90

* Thu Jul 23 2015 Florian Müllner <fmuellner@redhat.com> - 3.17.4-1
- Update to 3.17.4

* Wed Jul 22 2015 David King <amigadave@amigadave.com> - 3.17.3-2
- Bump for new gnome-desktop3

* Thu Jul 02 2015 Florian Müllner <fmuellner@redhat.com> - 3.17.3-1
- Update to 3.17.3

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.17.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed May 27 2015 Florian Müllner <fmuellner@redhat.com> - 3.17.2-1
- Update to 3.17.2

* Thu Apr 30 2015 Florian Müllner <fmuellner@redhat.com> - 3.17.1-1
- Update to 3.17.1

* Thu Apr 16 2015 Kalev Lember <kalevlember@gmail.com> - 3.16.1.1-2
- Bump gnome-shell conflicts version

* Wed Apr 15 2015 Rui Matos <rmatos@redhat.com> - 3.16.1.1-1
- Update to 3.16.1.1

* Tue Apr 14 2015 Florian Müllner <fmuellner@redhat.com> - 3.16.1-1
- Update to 3.16.1

* Mon Mar 23 2015 Florian Müllner <fmuellner@redhat.com> - 3.16.0-1
- Update to 3.16.0

* Tue Mar 17 2015 Kalev Lember <kalevlember@gmail.com> - 3.15.92-2
- Update minimum dep versions
- Use license macro for the COPYING file

* Tue Mar 17 2015 Florian Müllner <fmuellner@redhat.com> - 3.15.92-1
- Update to 3.15.92

* Tue Mar 10 2015 Peter Hutterer <peter.hutterer@redhat.com> - 3.15.91-2
- Rebuild for libinput soname bump

* Wed Mar 04 2015 Florian Müllner <fmuellner@redhat.com> - 3.15.91-1
- Update to 3.15.91

* Fri Feb 20 2015 Florian Müllner <fmuellner@redhat.com> - 3.15.90-1
- Update to 3.15.90

* Mon Feb 02 2015 Adam Williamson <awilliam@redhat.com> - 3.15.4-2
- backport ad90b7dd to fix BGO #743412 / RHBZ #1185811

* Wed Jan 21 2015 Florian Müllner <fmuellner@redhat.com> - 3.15.4-1
- Update to 3.15.4

* Mon Jan 19 2015 Peter Hutterer <peter.hutterer@redhat.com> 3.15.3-3
- Rebuild for libinput soname bump

* Mon Jan 12 2015 Ray Strode <rstrode@redhat.com> 3.15.3-2
- Add specific BuildRequires for wayland bits, so we don't
  get wayland support by happenstance.
- Add BuildRequires for autogoo since ./autogen.sh is run as part of
  the build process

* Fri Dec 19 2014 Florian Müllner <fmuellner@redhat.com> - 3.15.3-1
- Revert unsatisfiable wayland requirement

* Fri Dec 19 2014 Florian Müllner <fmuellner@redhat.com> - 3.15.3-1
- Update to 3.15.3

* Thu Nov 27 2014 Florian Müllner <fmuellner@redhat.com> - 3.15.2-1
- Update to 3.15.2

* Wed Nov 12 2014 Vadim Rutkovsky <vrutkovs@redhat.com> - 3.15.1-2
- Build installed tests

* Thu Oct 30 2014 Florian Müllner <fmuellner@redhat.com> - 3.15.1-1
- Update to 3.15.1

* Tue Oct 21 2014 Florian Müllner <fmuellner@redhat.com> - 3.14.1-2
- Fix regression in handling raise-on-click option (rhbz#1151918)

* Tue Oct 14 2014 Florian Müllner <fmuellner@redhat.com> - 3.14.1-1
- Update to 3.14.1

* Fri Oct 03 2014 Adam Williamson <awilliam@redhat.com> - 3.14.0-3
- backport fix for BGO #737233 / RHBZ #1145952 (desktop right click broken)

* Mon Sep 22 2014 Kalev Lember <kalevlember@gmail.com> - 3.14.0-2
- Bump gnome-shell conflicts version

* Mon Sep 22 2014 Florian Müllner <fmuellner@redhat.com> - 3.14.0-1
- Update to 3.14.0

* Wed Sep 17 2014 Florian Müllner <fmuellner@redhat.com> - 3.13.92-1
- Update to 3.13.92

* Fri Sep 12 2014 Peter Hutterer <peter.hutterer@redhat.com> - 3.13.91-2
- Rebuild for libinput soname bump

* Wed Sep 03 2014 Florian Müllner <fmuellner@redhat.com> - 3.31.91-1
- Update to 3.13.91, drop downstream patches

* Tue Aug 26 2014 Adel Gadllah <adel.gadllah@gmail.com> - 3.13.90-4
- Apply fix for RH #1133166

* Mon Aug 25 2014 Hans de Goede <hdegoede@redhat.com> - 3.13.90-3
- Add a patch from upstream fixing gnome-shell crashing non stop on
  multi monitor setups (rhbz#1103221)

* Fri Aug 22 2014 Kevin Fenzi <kevin@scrye.com> 3.13.90-2
- Rebuild for new wayland

* Wed Aug 20 2014 Florian Müllner <fmuellner@redhat.com> - 3.13.90-1
- Update to 3.13.90

* Mon Aug 18 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.4-3
- Rebuilt for upower 0.99.1 soname bump

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.13.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Jul 23 2014 Florian Müllner <fmuellner@redhat.com> - 3.13.4-1
- Update to 3.13.4

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.3-2
- Rebuilt for gobject-introspection 1.41.4

* Fri Jun 27 2014 Florian Müllner <fmuellner@redhat.com> - 3.13.3-1
- New gobject-introspection has been built, drop the last patch again

* Wed Jun 25 2014 Florian Müllner <fmuellner@redhat.com> - 3.13.3-1
- Revert annotation updates until we get a new gobject-introspection build

* Wed Jun 25 2014 Florian Müllner <fmuellner@redhat.com> - 3.13.3-1
- Update to 3.13.1

* Wed Jun 11 2014 Florian Müllner <fmuellner@redhat.com> - 3.13.2-2
- Backport fix for legacy fullscreen check

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.13.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 27 2014 Florian Müllner <fmuellner@redhat.com> - 3.13.2-1
- Update to 3.13.2, drop upstreamed patches

* Thu May  8 2014 Matthias Clasen <mclasen@redhat.com> - 3.13.1-5
- Fix shrinking terminals

* Wed May 07 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.1-4
- Backport an upstream fix for a Wayland session crash

* Wed May 07 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.1-3
- Install mutter-launch as setuid root

* Thu May 01 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.1-2
- Obsolete mutter-wayland

* Wed Apr 30 2014 Florian Müllner <fmuellner@redhat.com> - 3.13.1-1
- Update to 3.13.1

* Tue Apr 15 2014 Florian Müllner <fmuellner@redhat.com> - 3.12.1-1
- Update to 3.12.1

* Sat Apr 05 2014 Kalev Lember <kalevlember@gmail.com> - 3.12.0-2
- Update dep versions

* Tue Mar 25 2014 Florian Müllner <fmuellner@redhat.com> - 3.12.0-1
- Update to 3.12.0

* Wed Mar 19 2014 Florian Müllner <fmuellner@redhat.com> - 3.11.92-1
- Update to 3.11.92

* Thu Mar 06 2014 Florian Müllner <fmuellner@redhat.com> - 3.11.91-1
- Update to 3.11.91

* Thu Feb 20 2014 Kalev Lember <kalevlember@gmail.com> - 3.11.90-2
- Rebuilt for cogl soname bump

* Wed Feb 19 2014 Florian Müllner <fmuellner@redhat.com> - 3.11.90-1
- Update to 3.11.90

* Wed Feb 19 2014 Richard Hughes <rhughes@redhat.com> - 3.11.5-4
- Rebuilt for gnome-desktop soname bump

* Mon Feb 10 2014 Peter Hutterer <peter.hutterer@redhat.com> - 3.11.5-3
- Rebuild for libevdev soname bump

* Wed Feb 05 2014 Richard Hughes <rhughes@redhat.com> - 3.11.5-2
- Rebuilt for cogl soname bump

* Wed Feb 05 2014 Florian Müllner <fmuellner@redhat.com> - 3.11.5-1
- Update to 3.11.5

* Wed Jan 15 2014 Florian Müllner <fmuellner@redhat.com> - 3.11.4-1
- Update to 3.11.4

* Fri Dec 20 2013 Florian Müllner <fmuellner@redhat.com> - 3.11.3-1
- Update to 3.11.3

* Wed Nov 13 2013 Florian Müllner <fmuellner@redhat.com> - 3.11.2-1
- Update to 3.11.2

* Wed Oct 30 2013 Florian Müllner <fmuellner@redhat.com> - 3.11.1-1
- Update to 3.11.1

* Tue Oct 15 2013 Florian Müllner <fmuellner@redhat.com> - 3.10.1.1-1
- Update to 3.10.1.1

* Mon Oct 14 2013 Florian Müllner <fmuellner@redhat.com> - 3.10.1-1
- Update to 3.10.1

* Wed Sep 25 2013 Florian Müllner <fmuellner@redhat.com> - 3.10.0.1-1
- Update to 3.10.0.1

* Mon Sep 23 2013 Florian Müllner <fmuellner@redhat.com> - 3.10.0-1
- Update to 3.10.0

* Tue Sep 17 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.92-2
- Update the description and URL
- Tighten -devel subpackage deps with _isa
- Use the make_install macro

* Mon Sep 16 2013 Florian Müllner <fmuellner@redhat.com> - 3.9.92-1
- Update to 3.9.92

* Tue Sep 03 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.91-2
- Rebuilt for libgnome-desktop soname bump

* Tue Sep 03 2013 Florian Müllner <fmuellner@redhat.com> - 3.9.91-1
- Update to 3.9.91

* Thu Aug 22 2013 Florian Müllner <fmuellner@redhat.com> - 3.9.90-1
- Update to 3.9.90

* Fri Aug 09 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.5-2
- Rebuilt for cogl 1.15.4 soname bump

* Tue Jul 30 2013 Florian Müllner <fmuellner@redhat.com> - 3.9.5-1
- Update to 3.9.5

* Wed Jul 10 2013 Florian Müllner <fmuellner@redhat.com> - 3.9.4-1
- Update to 3.9.4

* Tue Jun 18 2013 Florian Müllner <fmuellner@redhat.com> - 3.9.3-1
- Update to 3.9.3

* Tue May 28 2013 Florian Müllner <fmuellner@redhat.com> - 3.9.2-1
- Update to 3.9.2

* Wed May 01 2013 Florian Müllner <fmuellner@redhat.com> - 3.9.1-1
- Update to 3.9.1

* Tue Apr 23 2013 Florian Müllner <fmuellner@redhat.com> - 3.8.1-1
- Update to 3.8.1

* Tue Mar 26 2013 Florian Müllner <fmuellner@redhat.com> - 3.8.0-1
- Update to 3.8.0

* Tue Mar 19 2013 Florian Müllner <fmuellner@redhat.com> - 3.7.92-1
- Update to 3.7.92

* Mon Mar 04 2013 Florian Müllner <fmuellner@redhat.com> - 3.7.91-1
- Update to 3.7.91

* Wed Feb 20 2013 Florian Müllner <fmuellner@redhat.com> - 3.7.90-1
- Update to 3.7.90

* Tue Feb 05 2013 Florian Müllner <fmuellner@redhat.com> - 3.7.5-1
- Update to 3.7.5

* Fri Jan 25 2013 Peter Robinson <pbrobinson@fedoraproject.org> 3.7.4-2
- Rebuild for new cogl

* Tue Jan 15 2013 Florian Müllner <fmuellner@redhat.com> - 3.7.4-1
- Update to 3.7.4

* Tue Dec 18 2012 Florian Müllner <fmuellner@redhat.com> - 3.7.3-1
- Update to 3.7.3

* Mon Nov 19 2012 Florian Müllner <fmuellner@redhat.com> - 3.7.2-1
- Update to 3.7.2

* Fri Nov 09 2012 Kalev Lember <kalevlember@gmail.com> - 3.7.1-1
- Update to 3.7.1

* Mon Oct 15 2012 Florian Müllner <fmuellner@redhat.com> - 3.6.1-1
- Update to 3.6.1

* Tue Sep 25 2012 Florian Müllner <fmuellner@redhat.com> - 3.6.0-1
- Update to 3.6.0

* Wed Sep 19 2012 Florian Müllner <fmuellner@redhat.com> - 3.5.92-1
- Update to 3.5.92

* Tue Sep 04 2012 Debarshi Ray <rishi@fedoraproject.org> - 3.5.91-2
- Rebuild against new cogl

* Tue Sep 04 2012 Debarshi Ray <rishi@fedoraproject.org> - 3.5.91-1
- Update to 3.5.91

* Tue Aug 28 2012 Matthias Clasen <mclasen@redhat.com> - 3.5.90-2
- Rebuild against new cogl/clutter

* Tue Aug 21 2012 Richard Hughes <hughsient@gmail.com> - 3.5.90-1
- Update to 3.5.90

* Tue Aug 07 2012 Richard Hughes <hughsient@gmail.com> - 3.5.5-1
- Update to 3.5.5

* Fri Jul 27 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 17 2012 Richard Hughes <hughsient@gmail.com> - 3.5.4-1
- Update to 3.5.4

* Tue Jun 26 2012 Matthias Clasen <mclasen@redhat.com> - 3.5.3-1
- Update to 3.5.3

* Fri Jun  8 2012 Matthias Clasen <mclasen@redhat.com> - 3.5.2-3
- Make resize grip area larger

* Thu Jun 07 2012 Matthias Clasen <mclasen@redhat.com> - 3.5.2-2
- Don't check for Xinerama anymore - it is now mandatory

* Thu Jun 07 2012 Richard Hughes <hughsient@gmail.com> - 3.5.2-1
- Update to 3.5.2
- Remove upstreamed patches

* Wed May 09 2012 Adam Jackson <ajax@redhat.com> 3.4.1-3
- mutter-never-slice-shape-mask.patch, mutter-use-cogl-texrect-api.patch:
  Fix window texturing on hardware without ARB_texture_non_power_of_two
  (#813648)

* Wed Apr 18 2012 Kalev Lember <kalevlember@gmail.com> - 3.4.1-2
- Silence glib-compile-schemas scriplets

* Wed Apr 18 2012 Kalev Lember <kalevlember@gmail.com> - 3.4.1-1
- Update to 3.4.1
- Conflict with gnome-shell versions older than 3.4.1

* Tue Mar 27 2012 Richard Hughes <hughsient@gmail.com> - 3.4.0-1
- Update to 3.4.0

* Wed Mar 21 2012 Kalev Lember <kalevlember@gmail.com> - 3.3.92-1
- Update to 3.3.92

* Sat Mar 10 2012 Matthias Clasen <mclasen@redhat.com> - 3.3.90-2
- Rebuild against new cogl

* Sat Feb 25 2012 Matthias Clasen <mclasen@redhat.com> - 3.3.90-1
- Update to 3.3.90

* Tue Feb  7 2012 Matthias Clasen <mclasen@redhat.com> - 3.3.5-1
- Update to 3.3.5

* Fri Jan 20 2012 Matthias Clasen <mclasen@redhat.com> - 3.3.4-1
- Update to 3.3.4

* Thu Jan 19 2012 Matthias Clasen <mclasen@redhat.com> - 3.3.3-2
- Rebuild against new cogl

* Thu Jan  5 2012 Matthias Clasen <mclasen@redhat.com> - 3.3.3-1
- Update to 3.3.3

* Wed Nov 23 2011 Matthias Clasen <mclasen@redhat.com> - 3.3.2-2
- Rebuild against new clutter

* Tue Nov 22 2011 Matthias Clasen <mclasen@redhat.com> - 3.3.2-1
- Update to 3.3.2

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.1-2
- Rebuilt for glibc bug#747377

* Wed Oct 19 2011 Matthias Clasen <mclasen@redhat.com> - 3.2.1-1
- Update to 3.2.1

* Mon Sep 26 2011 Owen Taylor <otaylor@redhat.com> - 3.2.0-1
- Update to 3.2.0

* Tue Sep 20 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.92-1
- Update to 3.1.92

* Wed Sep 14 2011 Owen Taylor <otaylor@redhat.com> - 3.1.91.1-1
- Update to 3.1.91.1

* Wed Aug 31 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.90.1-1
- Update to 3.1.90.1

* Wed Jul 27 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.4-1
- Update to 3.1.4

* Wed Jul 27 2011 Matthias Clasen <mclasen@redhat.com> - 3.1.3.1-3
- Rebuild

* Mon Jul  4 2011 Peter Robinson <pbrobinson@gmail.com> - 3.1.3.1-2
- rebuild against new clutter/cogl

* Mon Jul 04 2011 Adam Williamson <awilliam@redhat.com> - 3.1.3.1-1
- Update to 3.1.3.1

* Thu Jun 30 2011 Owen Taylor <otaylor@redhat.com> - 3.1.3-1
- Update to 3.1.3

* Wed May 25 2011 Owen Taylor <otaylor@redhat.com> - 3.0.2.1-1
- Update to 3.0.2.1

* Fri Apr 29 2011 Matthias Clasen <mclasen@redhat.com> - 3.0.1-3
- Actually apply the patch for #700276

* Thu Apr 28 2011 Matthias Clasen <mclasen@redhat.com> - 3.0.1-2
- Make session saving of gnome-shell work

* Mon Apr 25 2011 Owen Taylor <otaylor@redhat.com> - 3.0.1-1
- Update to 3.0.1

* Mon Apr  4 2011 Owen Taylor <otaylor@redhat.com> - 3.0.0-1
- Update to 3.0.0

* Mon Mar 28 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.93-1
- Update to 2.91.93

* Wed Mar 23 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.92-1
- Update to 2.91.92

* Mon Mar  7 2011 Owen Taylor <otaylor@redhat.com> - 2.91.91-1
- Update to 2.91.91

* Tue Mar  1 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.90-2
- Build against libcanberra, to enable AccessX feedback features

* Tue Feb 22 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.90-1
- Update to 2.91.90

* Thu Feb 10 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.6-4
- Rebuild against newer gtk

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.91.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb  2 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.6-2
- Rebuild against newer gtk

* Tue Feb  1 2011 Owen Taylor <otaylor@redhat.com> - 2.91.6-1
- Update to 2.91.6

* Tue Jan 11 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.5-1
- Update to 2.91.5

* Fri Jan  7 2011 Matthias Clasen <mclasen@redhat.com> - 2.91.4-1
- Update to 2.91.4

* Fri Dec  3 2010 Matthias Clasen <mclasen@redhat.com> - 2.91.3-2
- Rebuild against new gtk
- Drop no longer needed %%clean etc

* Mon Nov 29 2010 Owen Taylor <otaylor@redhat.com> - 2.91.3-1
- Update to 2.91.3

* Tue Nov  9 2010 Owen Taylor <otaylor@redhat.com> - 2.91.2-1
- Update to 2.91.2

* Tue Nov  2 2010 Matthias Clasen <mclasen@redhat.com> - 2.91.1-2
- Rebuild against newer gtk3

* Fri Oct 29 2010 Owen Taylor <otaylor@redhat.com> - 2.91.1-1
- Update to 2.91.1

* Mon Oct  4 2010 Owen Taylor <otaylor@redhat.com> - 2.91.0-1
- Update to 2.91.0

* Wed Sep 22 2010 Matthias Clasen <mclasen@redhat.com> - 2.31.5-4
- Rebuild against newer gobject-introspection

* Wed Jul 14 2010 Colin Walters <walters@verbum.org> - 2.31.5-3
- Rebuild for new gobject-introspection

* Tue Jul 13 2010 Adel Gadllah <adel.gadllah@gmail.com> - 2.31.5-2
- Build against gtk3

* Mon Jul 12 2010 Colin Walters <walters@pocket> - 2.31.5-1
- New upstream version

* Mon Jul 12 2010 Colin Walters <walters@verbum.org> - 2.31.2-5
- Rebuild against new gobject-introspection

* Tue Jul  6 2010 Colin Walters <walters@verbum.org> - 2.31.2-4
- Changes to support snapshot builds

* Fri Jun 25 2010 Colin Walters <walters@megatron> - 2.31.2-3
- drop gir-repository-devel dep

* Wed May 26 2010 Adam Miller <maxamillion@fedoraproject.org> - 2.31.2-2
- removed "--with-clutter" as configure is claiming it to be an unknown option

* Wed May 26 2010 Adam Miller <maxamillion@fedoraproject.org> - 2.31.2-1
- New upstream 2.31.2 release

* Thu Mar 25 2010 Peter Robinson <pbrobinson@gmail.com> 2.29.1-1
- New upstream 2.29.1 release

* Wed Mar 17 2010 Peter Robinson <pbrobinson@gmail.com> 2.29.0-1
- New upstream 2.29.0 release

* Tue Feb 16 2010 Adam Jackson <ajax@redhat.com> 2.28.1-0.2
- mutter-2.28.1-add-needed.patch: Fix FTBFS from --no-add-needed

* Thu Feb  4 2010 Peter Robinson <pbrobinson@gmail.com> 2.28.1-0.1
- Move to git snapshot

* Wed Oct  7 2009 Owen Taylor <otaylor@redhat.com> - 2.28.0-1
- Update to 2.28.0

* Tue Sep 15 2009 Owen Taylor <otaylor@redhat.com> - 2.27.5-1
- Update to 2.27.5

* Fri Sep  4 2009 Owen Taylor <otaylor@redhat.com> - 2.27.4-1
- Remove workaround for #520209
- Update to 2.27.4

* Sat Aug 29 2009 Owen Taylor <otaylor@redhat.com> - 2.27.3-3
- Fix %%preun GConf script to properly be for package removal

* Fri Aug 28 2009 Owen Taylor <otaylor@redhat.com> - 2.27.3-2
- Add a workaround for Red Hat bug #520209

* Fri Aug 28 2009 Owen Taylor <otaylor@redhat.com> - 2.27.3-1
- Update to 2.27.3, remove mutter-metawindow.patch

* Fri Aug 21 2009 Peter Robinson <pbrobinson@gmail.com> 2.27.2-2
- Add upstream patch needed by latest mutter-moblin

* Tue Aug 11 2009 Peter Robinson <pbrobinson@gmail.com> 2.27.2-1
- New upstream 2.27.2 release. Drop upstreamed patches.

* Wed Jul 29 2009 Peter Robinson <pbrobinson@gmail.com> 2.27.1-5
- Add upstream patches for clutter 1.0

* Wed Jul 29 2009 Peter Robinson <pbrobinson@gmail.com> 2.27.1-4
- Add patch to fix mutter --replace

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.27.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Jul 18 2009 Peter Robinson <pbrobinson@gmail.com> 2.27.1-2
- Updates from review request

* Fri Jul 17 2009 Peter Robinson <pbrobinson@gmail.com> 2.27.1-1
- Update to official 2.27.1 and review updates

* Thu Jun 18 2009 Peter Robinson <pbrobinson@gmail.com> 2.27.0-0.2
- Updates from initial reviews

* Thu Jun 18 2009 Peter Robinson <pbrobinson@gmail.com> 2.27.0-0.1
- Initial packaging


## END: Generated by rpmautospec
