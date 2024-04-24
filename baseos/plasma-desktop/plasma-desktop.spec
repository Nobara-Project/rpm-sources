%global kf5_version_min 5.98

%global synaptics 1
%global scim 1
%if 0%{?rhel} && 0%{?rhel} > 7
%undefine synaptics
%undefine scim
%endif

Name:    plasma-desktop
Summary: Plasma Desktop shell
Version: 5.27.9
Release: 1%{?dist}

License: GPLv2+ and (GPLv2 or GPLv3)
URL:     https://invent.kde.org/plasma/%{name}

%global verdir %(echo %{version} | cut -d. -f1-3)
%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global majmin_ver %(echo %{version} | cut -d. -f1,2).50
%global stable unstable
%else
%global majmin_ver %(echo %{version} | cut -d. -f1,2)
%global stable stable
%endif
Source0: http://download.kde.org/%{stable}/plasma/%{verdir}/%{name}-%{version}.tar.xz

## upstream patches

## downstream patches
# default kickoff favorites: +konsole +apper
Patch100: plasma-desktop-5.8-default_favorites.patch

## upstreamable patches
# REBASE?  -- rex
#Patch200: https://gitweb.gentoo.org/proj/kde.git/plain/kde-plasma/plasma-desktop/files/plasma-desktop-5.18.4.1-override-include-dirs.patch
Patch202: plasma-desktop-python-shebang.patch

Patch 203: set_dark_default.patch

# use this bundled copy (from f31) if not provided already
Source200: synaptics-properties.h

# filter qmk/plugins provides
%global __provides_exclude_from ^(%{_kf5_qmldir}/.*\\.so|%{_kf5_qtplugindir}/.*\\.so)$

BuildRequires:  pkgconfig(libusb)
BuildRequires:  fontconfig-devel
BuildRequires:  libX11-devel
BuildRequires:  libxkbfile-devel
BuildRequires:  libxcb-devel
BuildRequires:  xcb-util-keysyms-devel
BuildRequires:  xcb-util-image-devel
BuildRequires:  xcb-util-renderutil-devel
BuildRequires:  xcb-util-devel
BuildRequires:  libxkbcommon-devel
BuildRequires:  pkgconfig(xkeyboard-config)

BuildRequires:  qt5-qtbase-devel >= 5.9
BuildRequires:  qt5-qtbase-private-devel
BuildRequires:  qt5-qtx11extras-devel
BuildRequires:  qt5-qtsvg-devel
BuildRequires:  qt5-qtdeclarative-devel
BuildRequires:  qt5-qtwayland-devel
BuildRequires:  phonon-qt5-devel
BuildRequires:  wayland-protocols-devel

BuildRequires:  ibus-devel
%if 0%{?scim}
BuildRequires:  scim-devel
%endif

BuildRequires:  kf5-rpm-macros >= %{kf5_version_min}
BuildRequires:  extra-cmake-modules
BuildRequires:  kf5-plasma-devel >= %{kf5_version_min}
Requires:       kf5-plasma%{?_isa} >= %{_kf5_version}
BuildRequires:  kf5-kdoctools-devel >= %{kf5_version_min}
BuildRequires:  kf5-ki18n-devel >= %{kf5_version_min}
BuildRequires:  kf5-kcmutils-devel >= %{kf5_version_min}
BuildRequires:  kf5-kglobalaccel-devel >= %{kf5_version_min}
BuildRequires:  kf5-knewstuff-devel >= %{kf5_version_min}
BuildRequires:  kf5-kdelibs4support-devel >= %{kf5_version_min}
BuildRequires:  kf5-knotifyconfig-devel >= %{kf5_version_min}
BuildRequires:  kf5-kdesu-devel >= %{kf5_version_min}
BuildRequires:  kf5-attica-devel >= %{kf5_version_min}
BuildRequires:  kf5-kwallet-devel >= %{kf5_version_min}
BuildRequires:  kf5-krunner-devel >= %{kf5_version_min}
BuildRequires:  kf5-baloo-devel >= %{kf5_version_min}
BuildRequires:  kf5-kdeclarative-devel >= %{kf5_version_min}
BuildRequires:  kf5-kpeople-devel >= %{kf5_version_min}
BuildRequires:  kf5-kded-devel >= %{kf5_version_min}

BuildRequires:  libksysguard-devel >= %{majmin_ver}
BuildRequires:  kscreenlocker-devel >= %{majmin_ver}
BuildRequires:  kwin-devel >= %{majmin_ver}
# see %%prep below -- rex
BuildRequires:  plasma-breeze >= %{majmin_ver}
BuildRequires:  plasma-workspace-devel >= %{majmin_ver}

# Optional
%if 0%{?fedora}
BuildRequires:  cmake(AppStreamQt)
%endif
BuildRequires:  cmake(KAccounts) intltool
BuildRequires:  cmake(KUserFeedback)
BuildRequires:  PackageKit-Qt5-devel
BuildRequires:  kf5-kactivities-devel >= %{kf5_version_min}
BuildRequires:  kf5-kactivities-stats-devel >= %{kf5_version_min}
BuildRequires:  libcanberra-devel
BuildRequires:  boost-devel
BuildRequires:  pulseaudio-libs-devel

BuildRequires:  chrpath
BuildRequires:  desktop-file-utils

# xorg-x11 doesn't have hw_server and disable for s390/s390x
%ifnarch s390 s390x
# KCM touchpad has been merged to plasma-desktop in 5.3
Provides:       kcm_touchpad = %{version}-%{release}
Obsoletes:      kcm_touchpad < 5.3.0
# for xserver-properties
BuildRequires:  xorg-x11-server-devel
Requires:       kf5-kded

# for kcm_keyboard
BuildRequires:  pkgconfig(libudev)
Requires:       iso-codes

# for kcm_input, kcm_touchpad
BuildRequires:  pkgconfig(xorg-evdev)
BuildRequires:  pkgconfig(xorg-libinput)
%if 0%{?synaptics}
BuildRequires:  pkgconfig(xorg-synaptics)
%endif
%endif

# kcm_users
Requires:       accountsservice

# Desktop
Requires:       plasma-workspace >= %{majmin_ver}

# Qt Integration (brings in Breeze)
Requires:       plasma-integration >= %{majmin_ver}

# Install systemsettings, full set of KIO slaves and write() notifications
Requires:       plasma-systemsettings >= %{majmin_ver}
Requires:       kio-extras
Requires:       kwrited >= %{majmin_ver}

# Install KWin
Requires:       kwin >= %{majmin_ver}

# kickoff -> edit applications (#1229393)
Requires:       kmenuedit >= %{majmin_ver}

Requires:	plasma-discover

BuildRequires:  kf5-kirigami2
Requires:       kf5-kirigami2%{?_isa}
BuildRequires:  qqc2-desktop-style
Requires:       qqc2-desktop-style%{?_isa}

# for kimpanel-ibus-panel and kimpanel-ibus-panel-launcher
Recommends: ibus

# Virtual provides for plasma-workspace
Provides:       plasmashell(desktop) = %{version}-%{release}
Provides:       plasmashell = %{version}-%{release}

Obsoletes:      kde-workspace < 5.0.0-1

Obsoletes:      kactivities-workspace < 5.6.0
Provides:       kactivities-workspace = %{version}-%{release}

Obsoletes:      plasma-user-manager < 5.19.50
Provides:       plasma-user-manager = %{version}-%{release}

# kimpanel moved here from kdeplasma-addons-5.5.x
Conflicts:      kdeplasma-addons < 5.6.0

# kcm_activities.mo moved here (#1325724)
Conflicts:      kde-l10n < 15.12.3-4

# needed for python os.system calls
Requires:	kde-runtime

%description
%{summary}.

%package        kimpanel-scim
Summary:        SCIM backend for kimpanel
Requires:       %{name} = %{version}-%{release}
%description    kimpanel-scim
A backend for the kimpanel panel icon for input methods using the SCIM input
method framework.

%package        doc
Summary:        Documentation and user manuals for %{name}
# when conflicting HTML docs were removed
Conflicts:      kcm_colors < 1:4.11.16-10
# when conflicting HTML docs were removed
Conflicts:      kde-runtime-docs < 17.08.3-6
# when made noarch
Obsoletes: plasma-desktop-doc < 5.3.1-2
BuildArch: noarch
%description    doc
%{summary}.


%prep
%setup -q

## upstream patches

## upstreamable patches
#patch200 -p1
%patch202 -p1

%patch203 -p1


%if ! 0%{?synaptics}
install -pD %{SOURCE200} 3rdparty/xorg/synaptics-properties.h
%endif

## downstream patches
%patch100 -p1

# relax plasma-breeze/plasma-workspace deps
sed -i.breeze_ver \
  -e "s|find_package(Breeze \${PROJECT_VERSION} |find_package(Breeze %{majmin_ver} |g" \
  -e "s|find_package(LibKWorkspace \${PROJECT_VERSION} |find_package(LibKWorkspace %{majmin_ver} |g" \
  -e "s|find_package(LibColorCorrect \${PROJECT_VERSION} |find_package(LibColorCorrect %{majmin_ver} |g" \
  -e "s|find_package(LibNotificationManager \${PROJECT_VERSION} |find_package(LibNotificationManager %{majmin_ver} |g" \
  -e "s|find_package(LibTaskManager \${PROJECT_VERSION} |find_package(LibTaskManager %{majmin_ver} |g" \
  CMakeLists.txt


%build
%ifarch s390 %{arm}
# Decrease debuginfo verbosity to reduce memory consumption even more
%global optflags %(echo %{optflags} | sed 's/-g /-g1 /')
%endif

%{cmake_kf5} \
  %{?!synaptics:-DSynaptics_INCLUDE_DIRS:PATH="$(pwd)/../3rdparty/xorg"}
%cmake_build


%install
%cmake_install

%find_lang %{name} --with-html --all-name

grep "%{_kf5_docdir}" %{name}.lang > %{name}-doc.lang
cat  %{name}.lang %{name}-doc.lang | sort | uniq -u > plasmadesktop5.lang

# No -devel
rm -fv %{buildroot}%{_libdir}/libkfontinst{,ui}.so

## unpackaged files
rm -rfv %{buildroot}%{_datadir}/kdm/pics/users/
# odd locale stuff?
rm -rfv %{buildroot}%{_datadir}/locale/*/LC_SCRIPTS/kfontinst/


%check
desktop-file-validate %{buildroot}/%{_datadir}/applications/org.kde.knetattach.desktop


%ldconfig_scriptlets

%files -f plasmadesktop5.lang
%license LICENSES
%{_bindir}/kaccess
%{_bindir}/knetattach
%{_bindir}/solid-action-desktop-gen
%{_bindir}/plasma-emojier
%{_bindir}/tastenbrett
%{_bindir}/krunner-plugininstaller
%{_kf5_libexecdir}/kauth/kcmdatetimehelper
%{_libexecdir}/kimpanel-ibus-panel
%{_libexecdir}/kimpanel-ibus-panel-launcher
%{_kf5_qmldir}/org/kde/plasma/private
# TODO: -libs subpkg -- rex
%{_kf5_qtplugindir}/*.so
%{_kf5_qtplugindir}/plasma/kcms/desktop/kcm_krunnersettings.so
%{_kf5_qtplugindir}/plasma/kcms/systemsettings/*.so
%{_kf5_qtplugindir}/plasma/kcms/systemsettings_qwidgets/*.so
%{_kf5_plugindir}/kded/*.so
%{_kf5_plugindir}/krunner/krunner*.so
%{_kf5_qmldir}/org/kde/plasma/activityswitcher
%{_kf5_qmldir}/org/kde/plasma/emoji/
%{_kf5_qmldir}/org/kde/private/desktopcontainment/*
%{_kf5_qmldir}/org/kde/activities/settings/
%{_kf5_datadir}/plasma/*
%ifnarch s390 s390x
# touchpad
%{_bindir}/kcm-touchpad-list-devices
%{_kf5_qtplugindir}/plasma/dataengine/plasma_engine_touchpad.so
%{_kf5_qtplugindir}/plasma/kcminit/kcm_touchpad_init.so
%{_datadir}/dbus-1/interfaces/org.kde.touchpad.xml
# kcminput
%{_kf5_bindir}/kapplymousetheme
%{_kf5_datadir}/kcmmouse/
%{_kf5_qtplugindir}/plasma/kcminit/kcm_mouse_init.so
%endif
%{_datadir}/config.kcfg/*.kcfg
%{_datadir}/kglobalaccel/org.kde.plasma.emojier.desktop
%{_datadir}/qlogging-categories5/*.categories
%{_kf5_datadir}/kconf_update/*
%{_kf5_datadir}/kcmkeys
%{_kf5_datadir}/kpackage/kcms/*
%{_kf5_datadir}/knsrcfiles/
%{_kf5_datadir}/kf5/kactivitymanagerd/workspace/
%{_kf5_datadir}/kf5/kcm_recentFiles/workspace/settings/qml/recentFiles/BlacklistApplicationView.qml
%{_kf5_datadir}/kcmsolidactions/
%{_kf5_datadir}/solid/devices/*.desktop
%{_kf5_datadir}/dbus-1/system.d/*.conf
%{_kf5_datadir}/kservicetypes5/*.desktop
%{_kf5_datadir}/knotifications5/*.notifyrc
%ifnarch s390 s390x
%{_datadir}/icons/hicolor/*/*/*
%endif
%{_kf5_metainfodir}/*.xml
%{_datadir}/applications/*.desktop
%{_datadir}/dbus-1/system-services/*.service
%{_datadir}/polkit-1/actions/org.kde.kcontrol.kcmclock.policy
%{_sysconfdir}/xdg/autostart/*.desktop
%{_kf5_datadir}/accounts/providers/kde/
%{_kf5_datadir}/accounts/services/kde/

%if 0%{?scim}
%files kimpanel-scim
%{_libexecdir}/kimpanel-scim-panel
%endif

%files doc -f %{name}-doc.lang


%changelog
* Tue Oct 24 2023 Steve Cossette <farchord@gmail.com> - 5.27.9-1
- 5.27.9

* Tue Sep 12 2023 justin.zobel@gmail.com - 5.27.8-1
- 5.27.8

* Tue Aug 01 2023 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 5.27.7-1
- 5.27.7

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.27.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sun Jun 25 2023 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 5.27.6-1
- 5.27.6

* Wed May 10 2023 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 5.27.5-1
- 5.27.5

* Tue Apr 04 2023 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 5.27.4-1
- 5.27.4

* Tue Mar 14 2023 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 5.27.3-1
- 5.27.3

* Tue Feb 28 2023 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 5.27.2-1
- 5.27.2

* Tue Feb 21 2023 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 5.27.1-1
- 5.27.1

* Tue Feb 14 2023 Marc Deop <marcdeop@fedoraproject.org> - 5.27.0-2
- Rebuild against new sources

* Thu Feb 09 2023 Marc Deop <marcdeop@fedoraproject.org> - 5.27.0-1
- 5.27.0

* Thu Jan 19 2023 Marc Deop <marcdeop@fedoraproject.org> - 5.26.90-1
- 5.26.90

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.26.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jan 05 2023 Justin Zobel <justin@1707.io> - 5.26.5-1
- Update to 5.26.5

* Tue Nov 29 2022 Marc Deop <marcdeop@fedoraproject.org> - 5.26.4-1
- 5.26.4

* Wed Nov 09 2022 Marc Deop <marcdeop@fedoraproject.org> - 5.26.3-1
- 5.26.3

* Wed Oct 26 2022 Marc Deop <marcdeop@fedoraproject.org> - 5.26.2-1
- 5.26.2

* Tue Oct 18 2022 Marc Deop <marcdeop@fedoraproject.org> - 5.26.1-1
- 5.26.1

* Thu Oct 06 2022 Marc Deop <marcdeop@fedoraproject.org> - 5.26.0-1
- 5.26.0

* Sat Sep 17 2022 Marc Deop <marcdeop@fedoraproject.org> - 5.25.90-1
- 5.25.90

* Wed Sep 07 2022 Marc Deop <marcdeop@fedoraproject.org> - 5.25.5-1
- 5.25.5

* Wed Aug 03 2022 Justin Zobel <justin@1707.io> - 5.25.4-1
- Update to 5.25.4

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.25.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jul 12 2022 Marc Deop <marcdeop@fedoraproject.org> - 5.25.3-1
- 5.25.3

* Tue Jun 28 2022 Marc Deop <marcdeop@fedoraproject.org> - 5.25.2-1
- 5.25.2

* Tue Jun 21 2022 Marc Deop <marcdeop@fedoraproject.org> - 5.25.1-1
- 5.25.1

* Thu Jun 09 2022 Marc Deop <marcdeop@fedoraproject.org> - 5.25.0-1
- 5.25.0

* Fri May 20 2022 Marc Deop <marcdeop@fedoraproject.org> - 5.24.90-1
- 5.24.90

* Tue May 03 2022 Marc Deop <marcdeop@fedoraproject.org> - 5.24.5-1
- 5.24.5

* Thu Mar 31 2022 Justin Zobel <justin@1707.io> - 5.24.4-1
- Update to 5.24.4

* Tue Mar 08 2022 Marc Deop <marcdeop@fedoraproject.org> - 5.24.3-1
- 5.24.3

* Tue Feb 22 2022 Rex Dieter <rdieter@fedoraproject.org> - 5.24.2-1
- 5.24.2

* Tue Feb 15 2022 Marc Deop <marcdeop@fedoraproject.org> - 5.24.1-1
- 5.24.1

* Thu Feb 03 2022 Marc Deop <marcdeop@fedoraproject.org> - 5.24.0-1
- 5.24.0

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.23.90-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jan 13 2022 Marc Deop <marcdeop@fedoraproject.org> - 5.23.90-1
- 5.23.90

* Tue Jan 04 2022 Marc Deop <marcdeop@fedoraproject.org> - 5.23.5-1
- 5.23.5

* Tue Dec 14 2021 Marc Deop <marcdeop@fedoraproject.org> - 5.23.4-1
- 5.23.4

* Wed Nov 10 2021 Rex Dieter <rdieter@fedoraproject.org> - 5.23.3-1
- 5.23.3

* Wed Oct 27 2021 Rex Dieter <rdieter@fedoraproject.org> - 5.23.2.1-1
- 5.23.2.1

* Tue Oct 26 2021 Rex Dieter <rdieter@fedoraproject.org> - 5.23.2-1
- 5.23.2

* Sat Oct 23 2021 Marc Deop <marcdeop@fedoraproject.org> - 5.23.1-1
- 5.23.1

* Fri Oct 08 2021 Marc Deop <marcdeop@fedoraproject.org> - 5.23.0-1
- 5.23.0

* Mon Sep 20 2021 Marc Deop <marcdeop@fedoraproject.org> - 5.22.90-2
- Adjust license
- Adjust files section

* Fri Sep 17 2021 Marc Deop <marcdeop@fedoraproject.org> - 5.22.90-1
- 5.22.90

* Tue Aug 31 2021 Jan Grulich <jgrulich@redhat.com> - 5.22.5-1
- 5.22.5

* Tue Jul 27 2021 Jan Grulich <jgrulich@redhat.com> - 5.22.4-1
- 5.22.4

* Tue Jul 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.22.3-2
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jul 12 2021 Jan Grulich <jgrulich@redhat.com> - 5.22.3-1
- 5.22.3

* Tue Jun 22 2021 Jan Grulich <jgrulich@redhat.com> - 5.22.2.1-1
- 5.22.2.1

* Tue Jun 22 2021 Jan Grulich <jgrulich@redhat.com> - 5.22.2-1
- 5.22.2

* Tue Jun 15 2021 Jan Grulich <jgrulich@redhat.com> - 5.22.1-1
- 5.22.1

* Sun Jun 06 2021 Jan Grulich <jgrulich@redhat.com> - 5.22.0-1
- 5.22.0

* Thu May 20 2021 Rex Dieter <rdieter@fedoraproject.org> - 5.21.90-3
- pull in some upstream fixes

* Sun May 16 2021 Rex Dieter <rdieter@fedoraproject.org> - 5.21.90-2
- s/kf5-ksysguard/libksysguard/

* Fri May 14 2021 Rex Dieter <rdieter@fedoraproject.org> - 5.21.90-1
- 5.21.90

* Tue May 04 2021 Jan Grulich <jgrulich@redhat.com> - 5.21.5-1
- 5.21.5

* Tue Apr 06 2021 Jan Grulich <jgrulich@redhat.com> - 5.21.4-1
- 5.21.4

* Tue Mar 16 2021 Jan Grulich <jgrulich@redhat.com> - 5.21.3-1
- 5.21.3

* Tue Mar 02 2021 Jan Grulich <jgrulich@redhat.com> - 5.21.2-1
- 5.21.2

* Tue Feb 23 2021 Jan Grulich <jgrulich@redhat.com> - 5.21.1-1
- 5.21.1

* Mon Feb 15 2021 Jan Grulich <jgrulich@redhat.com> - 5.21.0-2
- Tarball respin

* Thu Feb 11 2021 Jan Grulich <jgrulich@redhat.com> - 5.21.0-1
- 5.21.0

* Thu Jan 28 2021 Rex Dieter <rdieter@fedoraproject.org> - 5.20.90-3
- ibus-ui-emojier-plasma: +Recommends: ibus

* Tue Jan 26 2021 Rex Dieter <rdieter@fedoraproject.org> - 5.20.90-2
- for ibus-ui-emojier-plasma: +Recommends: ibus-uniemoji
- fix URL

* Thu Jan 21 2021 Jan Grulich <jgrulich@redhat.com> - 5.20.90-1
- 5.20.90 (beta)

* Tue Jan  5 16:03:32 CET 2021 Jan Grulich <jgrulich@redhat.com> - 5.20.5-1
- 5.20.5

* Thu Dec 31 2020 Rex Dieter <rdieter@fedoraproject.org> - 5.20.4-2
- Requires: accountsservice (kde#430916)

* Tue Dec  1 09:42:59 CET 2020 Jan Grulich <jgrulich@redhat.com> - 5.20.4-1
- 5.20.4

* Wed Nov 11 08:22:41 CET 2020 Jan Grulich <jgrulich@redhat.com> - 5.20.3-1
- 5.20.3

* Tue Oct 27 14:23:44 CET 2020 Jan Grulich <jgrulich@redhat.com> - 5.20.2-1
- 5.20.2

* Tue Oct 20 15:29:34 CEST 2020 Jan Grulich <jgrulich@redhat.com> - 5.20.1-1
- 5.20.1

* Sun Oct 11 19:50:04 CEST 2020 Jan Grulich <jgrulich@redhat.com> - 5.20.0-1
- 5.20.0

* Fri Sep 18 2020 Jan Grulich <jgrulich@redhat.com> - 5.19.90-1
- 5.19.90

* Tue Sep 01 2020 Jan Grulich <jgrulich@redhat.com> - 5.19.5-1
- 5.19.5

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.19.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Jan Grulich <jgrulich@redhat.com> - 5.19.4-1
- 5.19.4

* Tue Jul 07 2020 Jan Grulich <jgrulich@redhat.com> - 5.19.3-1
- 5.19.3

* Tue Jun 23 2020 Jan Grulich <jgrulich@redhat.com> - 5.19.2-1
- 5.19.2

* Wed Jun 17 2020 Martin Kyral <martin.kyral@gmail.com> - 5.19.1-1
- 5.19.1

* Wed Jun 10 2020 Rex Dieter <rdieter@fedoraproject.org> - 5.19.0-2
- adjust synaptics hacks (for rhel8), bump kf5 dep

* Tue Jun 9 2020 Martin Kyral <martin.kyral@gmail.com> - 5.19.0-1
- 5.19.0

* Fri May 15 2020 Martin Kyral <martin.kyral@gmail.com> - 5.18.90-1
- 5.18.90

* Tue May 05 2020 Jan Grulich <jgrulich@redhat.com> - 5.18.5-1
- 5.18.5

* Sat May 02 2020 Rex Dieter <rdieter@fedoraproject.org> - 5.18.4.1-2
- use bundled synaptics header, if needed
- fix feature macro logic (defined as 1 on, undefined off)
- minor cleanups

* Sat Apr 04 2020 Rex Dieter <rdieter@fedoraproject.org> - 5.18.4.1-1
- 5.18.4.1

* Tue Mar 31 2020 Jan Grulich <jgrulich@redhat.com> - 5.18.4-1
- 5.18.4

* Tue Mar 10 2020 Jan Grulich <jgrulich@redhat.com> - 5.18.3-1
- 5.18.3

* Tue Feb 25 2020 Jan Grulich <jgrulich@redhat.com> - 5.18.2-1
- 5.18.2

* Tue Feb 18 2020 Jan Grulich <jgrulich@redhat.com> - 5.18.1-1
- 5.18.1

* Mon Feb 17 2020 Rex Dieter <rdieter@fedoraproject.org> - 5.18.0-2
- pull in upstream kcm_fonts fix

* Tue Feb 11 2020 Jan Grulich <jgrulich@redhat.com> - 5.18.0-1
- 5.18.0

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.17.90-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jan 16 2020 Jan Grulich <jgrulich@redhat.com> - 5.17.90-1
- 5.17.90

* Wed Jan 08 2020 Jan Grulich <jgrulich@redhat.com> - 5.17.5-1
- 5.17.5

* Fri Dec 27 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.17.4-2
- pull in upstream pager fix

* Thu Dec 05 2019 Jan Grulich <jgrulich@redhat.com> - 5.17.4-1
- 5.17.4

* Wed Nov 13 2019 Martin Kyral <martin.kyral@gmail.com> - 5.17.3-1
- 5.17.3

* Wed Oct 30 2019 Jan Grulich <jgrulich@redhat.com> - 5.17.2-1
- 5.17.2

* Wed Oct 23 2019 Jan Grulich <jgrulich@redhat.com> - 5.17.1-1
- 5.17.1

* Wed Oct 16 2019 Jan Grulich <jgrulich@redhat.com> - 5.17.0-2
- Updated tarball

* Thu Oct 10 2019 Jan Grulich <jgrulich@redhat.com> - 5.17.0-1
- 5.17.0

* Fri Sep 20 2019 Martin Kyral <martin.kyral@gmail.com> - 5.16.90-1
- 5.16.90

* Fri Sep 06 2019 Martin Kyral <martin.kyral@gmail.com> - 5.16.5-1
- 5.16.5

* Tue Jul 30 2019 Martin Kyral <martin.kyral@gmail.com> - 5.16.4-1
- 5.16.4

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.16.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jul 10 2019 Martin Kyral <martin.kyral@gmail.com> - 5.16.3-1
- 5.16.3

* Wed Jun 26 2019 Martin Kyral <martin.kyral@gmail.com> - 5.16.2-1
- 5.16.2

* Tue Jun 18 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.16.1-1
- 5.16.1

* Tue Jun 11 2019 Martin Kyral <martin.kyral@gmail.com> - 5.16.0-1
- 5.16.0

* Mon May 20 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.15.90.1-1
- 5.15.90.1

* Thu May 16 2019 Martin Kyral <martin.kyral@gmail.com> - 5.15.90-1
- 5.15.90

* Thu May 09 2019 Martin Kyral <martin.kyral@gmail.com> - 5.15.5-1
- 5.15.5

* Wed Apr 03 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.15.4-1
- 5.15.4

* Wed Mar 13 2019 Martin Kyral <martin.kyral@gmail.com> - 5.15.3.2-1
- 5.15.3.2
- tarball respun to remove docs causing build issues with KDocTools < 5.57

* Tue Mar 12 2019 Martin Kyral <martin.kyral@gmail.com> - 5.15.3-1
- 5.15.3

* Tue Feb 26 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.15.2-1
- 5.15.2

* Tue Feb 19 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.15.1-1
- 5.15.1

* Wed Feb 13 2019 Martin Kyral <martin.kyral@gmail.com> - 5.15.0-1
- 5.15.0

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.14.90-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Jan 20 2019 Martin Kyral <martin.kyral@gmail.com> - 5.14.90-1
- 5.14.90

* Wed Nov 28 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.14.4-2
- pull in upstream taskmanager fix

* Tue Nov 27 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.14.4-1
- 5.14.4

* Thu Nov 08 2018 Martin Kyral <martin.kyral@gmail.com> - 5.14.3-1
- 5.14.3

* Wed Oct 24 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.14.2-1
- 5.14.2

* Tue Oct 16 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.14.1-1
- 5.14.1

* Fri Oct 05 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.14.0-1
- 5.14.0

* Fri Sep 14 2018 Martin Kyral <martin.kyral@gmail.com> - 5.13.90-1
- 5.13.90

* Tue Sep 04 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.13.5-1
- 5.13.5

* Thu Aug 02 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.13.4-1
- 5.13.4

* Thu Jul 26 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.13.3-4
- Requires: qqc2-desktop-style

* Fri Jul 20 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.13.3-3
- use %%_kf5_qmldir (more)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.13.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jul 11 2018 Martin Kyral <martin.kyral@gmail.com> - 5.13.3-1
- 5.13.3

* Mon Jul 09 2018 Martin Kyral <martin.kyral@gmail.com> - 5.13.2-1
- 5.13.2

* Wed Jun 20 2018 Martin Kyral <martin.kyral@gmail.com> - 5.13.1.1-1
- 5.13.1.1

* Tue Jun 19 2018 Martin Kyral <martin.kyral@gmail.com> - 5.13.1-1
- 5.13.1

* Sat Jun 09 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.13.0-1
- 5.13.0

* Thu May 31 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.12.90.1-1
- 5.12.90.1
- kickoff crashes when click on categories (#1584515)

* Fri May 18 2018 Martin Kyral <martin.kyral@gmail.com> - 5.12.90-1
- 5.12.90

* Tue May 01 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.12.5-1
- 5.12.5

* Tue Mar 27 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.12.4-1
- 5.12.4

* Fri Mar 09 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.12.3-2
- BR: AppStreamQt libudev xorg-input

* Tue Mar 06 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.12.3-1
- 5.12.3

* Fri Mar 02 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.12.2-2
- -doc: drop Obsoletes: kde-runtime-docs (#1550857,#1199720)
- bump min qt5/kf5 dep
- use %%make_build %%ldconfig_scriptlets
- drop konq4 support (last used f25)

* Wed Feb 21 2018 Jan Grulich <jgrulich@redhat.com> - 5.12.2-1
- 5.12.2

* Tue Feb 13 2018 Jan Grulich <jgrulich@redhat.com> - 5.12.1-1
- 5.12.1

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.12.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Feb 02 2018 Jan Grulich <jgrulich@redhat.com> - 5.12.0-1
- 5.12.0

* Thu Jan 18 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 5.11.95-2
- Remove obsolete scriptlets

* Mon Jan 15 2018 Jan Grulich <jgrulich@redhat.com> - 5.11.95-1
- 5.11.95

* Tue Jan 02 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.11.5-1
- 5.11.5

* Thu Nov 30 2017 Martin Kyral <martin.kyral@gmail.com> - 5.11.4-1
- 5.11.4

* Wed Nov 08 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.11.3-1
- 5.11.3

* Wed Oct 25 2017 Martin Kyral <martin.kyral@gmail.com> - 5.11.2-1
- 5.11.2

* Tue Oct 17 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.11.1-1
- 5.11.1

* Wed Oct 11 2017 Martin Kyral <martin.kyral@gmail.com> - 5.11.0-1
- 5.11.0

* Thu Aug 24 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.10.5-1
- 5.10.5

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.10.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.10.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jul 21 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.10.4-1
- 5.10.4

* Tue Jun 27 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.10.3-1
- 5.10.3

* Thu Jun 15 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.10.2-1
- 5.10.2

* Tue Jun 06 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.10.1-1
- 5.10.1

* Wed May 31 2017 Jan Grulich <jgrulich@redhat.com> - 5.10.0-1
- 5.10.0

* Wed Apr 26 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.9.5-1
- 5.9.5, cleanup, BR: plasma-breeze, use %%find_lang more

* Fri Apr 14 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.9.4-2
- pull in upstream fixes, update URL

* Thu Mar 23 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.9.4-1
- 5.9.4

* Sat Mar 04 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.9.3-2
- rebuild

* Wed Mar 01 2017 Jan Grulich <jgrulich@redhat.com> - 5.9.3-1
- 5.9.3

* Sat Feb 25 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.8.6-2
- Requires: kf5-plasma >= %%_kf5_version

* Tue Feb 21 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.8.6-1
- 5.8.6

* Mon Feb 13 2017 Than Ngo <than@redhat.com> - 5.8.5-4
- backport upstream to security issue
  honor the setting for prompting when executing executable files on the desktop
- fixed error: placeholders is not a namespace-name with gcc7

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.8.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan 02 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.8.5-2
- filter qml/plugin provides, drop unused PK patch/support

* Wed Dec 28 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.8.5-1
- 5.8.5

* Tue Nov 22 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.8.4-1
- 5.8.4

* Thu Nov 10 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.8.3-2
- adjust default_favorites.patch for namespaced apper

* Tue Nov 01 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.8.3-1
- 5.8.3

* Tue Oct 18 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.8.2-1
- 5.8.2

* Tue Oct 11 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.8.1-1
- 5.8.1

* Fri Oct 07 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.8.0-4
- default_favorites.patch: use preferred://browser again

* Fri Oct 07 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.8.0-3
- drop re-enabling kicker PackageKit integration, it's racy (#1382360)

* Wed Oct 05 2016 Kevin Kofler <Kevin@tigcc.ticalc.org> - 5.8.0-2
- move kimpanel-scim-panel to a -kimpanel-scim subpackage (#1381420)

* Thu Sep 29 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.8.0-1
- 5.8.0

* Thu Sep 22 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.7.95-1
- 5.7.95

* Tue Sep 13 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.7.5-1
- 5.7.5

* Tue Aug 23 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.7.4-1
- 5.7.4

* Tue Aug 02 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.7.3-1
- 5.7.3, drop f22 support

* Tue Jul 19 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.7.2-1
- 5.7.2

* Tue Jul 12 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.7.1-1
- 5.7.1

* Thu Jun 30 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.7.0-1
- 5.7.0

* Sat Jun 25 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6.95-1
- 5.6.95

* Tue Jun 14 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6.5-1
- 5.6.5

* Thu May 26 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6.4-2
- fix kickoff kcm_useraccount => user_manager (kde#363528)
- backport 5.6 branch fixes

* Sat May 14 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6.4-1
- 5.6.4

* Sat Apr 23 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6.3-2
- kickoff applet still use KF5::ActivitiesExperimentalStats (kde#361952)

* Tue Apr 19 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6.3-1
- 5.6.3

* Mon Apr 18 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6.2-3
- muon-discover => plasma-discover (f24+)

* Mon Apr 11 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6.2-2
- Conflicts: kde-l10n < 15.12.3-4 (#1325724)

* Sat Apr 09 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6.2-1
- 5.6.2

* Fri Apr 08 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6.1-2
- BR: ibus-devel scim-devel

* Fri Apr 08 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6.1-1
- 5.6.1

* Mon Mar 28 2016 Rex Dieter <rdieter@fedoraproject.org> 5.5.5-5
- upstream fixes for: No 'favorites' in F24 KDE menu (#1320395,kde#357029)

* Fri Mar 25 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.5.5-4
- favorites: cleanup, no backups, f22+ fix firefox/konsole/discover, f22 fix konq/konsole/discover

* Wed Mar 23 2016 Rex Dieter <rdieter@fedoraproject.org> 5.5.5-3
- No 'favorites' in F24 KDE menu (#1320395,kde#357029)

* Fri Mar 11 2016 Rex Dieter <rdieter@fedoraproject.org> 5.5.5-2
- drop Requires: kde-style-breeze (f23+)

* Tue Mar 01 2016 Daniel Vrátil <dvratil@fedoraproject.org> - 5.5.5-1
- Plasma 5.5.5

* Mon Feb 29 2016 Rex Dieter <rdieter@fedoraproject.org> 5.5.4-4
- (backport) wrong breeze icons used ... in taskmanager (#359387)

* Fri Feb 26 2016 Rex Dieter <rdieter@fedoraproject.org> 5.5.4-3
- fix kickoff "right click => remove app" packagekit integration (#359837)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 5.5.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 27 2016 Daniel Vrátil <dvratil@fedoraproject.org> - 5.5.4-1
- Plasma 5.5.4

* Sat Jan 09 2016 Rex Dieter <rdieter@fedoraproject.org> 5.5.3-3
- pull in some upstream patches, simplify/consolidate s390 blocks

* Sat Jan 09 2016 Rex Dieter <rdieter@fedoraproject.org> 5.5.3-2
- Fix font preview (#1208229, kde#336089)

* Thu Jan 07 2016 Daniel Vrátil <dvratil@fedoraproject.org> - 5.5.3-1
- Plasma 5.5.3

* Thu Dec 31 2015 Rex Dieter <rdieter@fedoraproject.org> 5.5.2-2
- update URL, old sources

* Thu Dec 31 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.5.2-1
- 5.5.2

* Fri Dec 18 2015 Daniel Vrátil <dvratil@fedoraproject.org> - 5.5.1-1
- Plasma 5.5.1

* Wed Dec 16 2015 Than Ngo <than@redhat.com> - 5.5.0-6
- add workaround for "virtual memory exhausted: Cannot allocate memory" on s390
- exclude touchpad for s390/s390x

* Tue Dec 15 2015 Than Ngo <than@redhat.com> - 5.5.0-5
- fix build failure on s390/s390x

* Wed Dec 09 2015 Rex Dieter <rdieter@fedoraproject.org> 5.5.0-4
- omit env hack, rename plasma update script instead

* Tue Dec 08 2015 Rex Dieter <rdieter@fedoraproject.org> 5.5.0-3
- force plasma's obsolete_kickoffrc.js to run again

* Tue Dec 08 2015 Rex Dieter <rdieter@fedoraproject.org> 5.5.0-2
- backport favorites migration fix (#1289709)

* Thu Dec 03 2015 Daniel Vrátil <dvratil@fedoraproject.org> - 5.5.0-1
- Plasma 5.5.0

* Wed Nov 25 2015 Daniel Vrátil <dvratil@fedoraproject.org> - 5.4.95-1
- Plasma 5.4.95

* Thu Nov 05 2015 Daniel Vrátil <dvratil@fedoraproject.org> - 5.4.3-1
- Plasma 5.4.3

* Thu Oct 29 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.2-5
- Recommends: muon-discover (#1224421)

* Mon Oct 26 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.2-4
- revert default_favorites.patch back to apper

* Fri Oct 16 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.2-3
- default_favorites.patch: -apper, +muon-discover

* Sun Oct 04 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.4.2-2
- Recommends: muon-discover
- consistently use %%{majmin_ver} macro for plasma5-related dependencies

* Fri Oct 02 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.4.2-1
- 5.4.2, use %%license, .spec cosmetics

* Thu Oct 01 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.1-7
- relax some deps %%{version} => %%{majmin_ver} to ease bootstrapping

* Mon Sep 28 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.1-6
- re-fix font management, kauth_helper paths (#1208229, kde#353215)

* Mon Sep 21 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.1-5
- restore f22 default favorites

* Fri Sep 18 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.1-4
- conditionally apply C.UTF-8 workaround only for < f24 (#1250238)

* Sat Sep 12 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.1-3
- tighten build deps (simimlar to plasma-workspace)

* Fri Sep 11 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.1-2
- make kio-extras unversioned (it's in kde-apps releases now)

* Wed Sep 09 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.4.1-1
- 5.4.1

* Wed Sep 09 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-4
- Wrong C.UTF-8 locale (#1250238)

* Fri Sep 04 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.0-3
- make plasma-related runtime deps versioned

* Tue Sep 01 2015 Daniel Vrátil <dvratil@redhat.com> - 5.4.0-2
- Try rebuild against new Baloo

* Fri Aug 21 2015 Daniel Vrátil <dvratil@redhat.com> - 5.4.0-1
- Plasma 5.4.0

* Thu Aug 13 2015 Daniel Vrátil <dvratil@redhat.com> - 5.3.95-1
- Plasma 5.3.95

* Wed Jul 29 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.2-6
- Rebuilt for https://fedoraproject.org/wiki/Changes/F23Boost159

* Wed Jul 22 2015 David Tardon <dtardon@redhat.com> - 5.3.2-5
- rebuild for Boost 1.58

* Tue Jul 07 2015 Rex Dieter <rdieter@fedoraproject.org> 5.3.2-4
- BR: pkgconfig(xkeyboard-config)

* Mon Jul 06 2015 Rex Dieter <rdieter@fedoraproject.org> 5.3.2-3
- Switch to Next Keyboard Layout shortcut restores after OS restarting (#1234082)

* Sat Jun 27 2015 Rex Dieter <rdieter@fedoraproject.org> 5.3.2-2
- pull in upstream fix for kcm_touchpad: No touchpad found (#1199825)

* Thu Jun 25 2015 Daniel Vrátil <dvratil@redhat.com> - 5.3.2-1
- Plasma 5.3.2

* Tue Jun 23 2015 Rex Dieter <rdieter@fedoraproject.org> 5.3.1-7
- kcm_touchpad: No touchpad found (#1199825)

* Wed Jun 17 2015 Rex Dieter <rdieter@fedoraproject.org> 5.3.1-6
- kcm_phonon does not display all HDMI audio ports (#1232903)

* Tue Jun 16 2015 Rex Dieter <rdieter@fedoraproject.org> 5.3.1-5
- backport trashcan applet fix (#1231972,kde#349207)

* Mon Jun 15 2015 Rex Dieter <rdieter@fedoraproject.org> 5.3.1-4
- backport "Fix-dropping-files-onto-the-desktop-containment"
- BR: kf5-kglobalaccel-devel

* Mon Jun 08 2015 Rex Dieter <rdieter@fedoraproject.org> 5.3.1-3
- Requires: kmenuedit, instead of Recommends which doesn't seem to work reliably yet (#1229393)

* Tue Jun 02 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.3.1-2
- use %%{kf5_kinit_requires}
- -doc: noarch, %%lang'ify
- Provides: plasmashell

* Tue May 26 2015 Daniel Vrátil <dvratil@redhat.com> - 5.3.1-1
- Plasma 5.3.1

* Thu May 21 2015 Rex Dieter <rdieter@fedoraproject.org> 5.3.0-6
- default to folder containment (#1220862)

* Fri May 08 2015 Rex Dieter <rdieter@fedoraproject.org> 5.3.0-5
- Recommends: kmenuedit

* Sun May 03 2015 Rex Dieter <rdieter@fedoraproject.org> 5.3.0-4
- (re)fix fontinst service paths (#1208229)

* Wed Apr 29 2015 Daniel Vrátil <dvratil@redhat.com> - 5.3.0-3
- Provides plasmashell(desktop) (#1215691)

* Tue Apr 28 2015 Daniel Vrátil <dvratil@redhat.com> - 5.3.0-2
- Provides/Obsoletes kcm_touchpad (#1216897)

* Mon Apr 27 2015 Daniel Vrátil <dvratil@redhat.com> - 5.3.0-1
- Plasma 5.3.0

* Thu Apr 23 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.95-1
- Plasma 5.2.95

* Thu Apr 23 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.2.2-5
- fix fontinst service paths harder (#1208229)
- Konqueror "favorite" opens as a file manager (#1209169)

* Thu Apr 02 2015 Daniel Vrátil <dvratil@redhat.com> 5.2.2-4
- fix fontinst service paths (rhbz#1208229)

* Mon Mar 30 2015 Rex Dieter <rdieter@fedoraproject.org> 5.2.2-3
- own /usr/share/plasma/shells/org.kde.plasma.desktop/updates

* Fri Mar 20 2015 Rex Dieter <rdieter@fedoraproject.org> 5.2.2-2
- -doc: Conflicts: kcm_colors < 1:4.11.16-10 (drop conflicts in main pkg)

* Fri Mar 20 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.2-1
- Plasma 5.2.2

* Wed Mar 11 2015 Rex Dieter <rdieter@fedoraproject.org> 5.2.1-6
- adjust default kickoff favorites: +konsole +apper

* Mon Mar 09 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.2.1-5
- .spec cleanup
- pull in upstream fixes, particularly...
- Top level "tabs" disappears in Kickoff (kde#343524)

* Sat Mar 07 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.2.1-4
- -doc: Obsoletes: kde-runtime-docs (#1199720)
- %%find_lang: drop --with-kde, we want handbooks in -doc instead

* Fri Mar 06 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.1-3
- Does not obsolete kcm_colors anymore (KDE 4 version is co-installable now)

* Fri Feb 27 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.1-2
- Rebuild (GCC 5)

* Tue Feb 24 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.1-1
- Plasma 5.2.1

* Mon Feb 09 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.0-5
- Requires: iso-codes (for kcm_keyboard)

* Mon Feb 09 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.0-4
- Copy konqsidebartng to /usr/share/kde4/apps so that KDE4 Konqueror can find it

* Tue Jan 27 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.0-3
- Workaround broken DBus service file generated by CMake

* Tue Jan 27 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.0-2
- Requires: breeze, systemsettings, kwin (for full Plasma experience)

* Mon Jan 26 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.0-1
- Plasma 5.2.0

* Wed Jan 14 2015 Daniel Vrátil <dvratil@redhat.com> - 5.1.95-2.beta
- Obsoletes/Provides kcm_colors

* Wed Jan 14 2015 Daniel Vrátil <dvratil@redhat.com> - 5.1.95-1.beta
- Plasma 5.1.95 Beta

* Wed Jan 07 2015 Jan Grulich <jgrulich@redhat.com> - 5.1.2-3
- Omit "5" from pkg summary
  Add icon cache scriptlets
  Validate application .desktop files
  Fixed license

* Wed Dec 17 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.2-2
- Plasma 5.1.2

* Fri Nov 07 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.1-1
- Plasma 5.1.1

* Tue Oct 14 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.0.1-1
- Plasma 5.1.0.1

* Thu Oct 09 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.0-1
- Plasma 5.1.0

* Tue Sep 16 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.2-1
- Plasma 5.0.2

* Sun Aug 10 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.1-1
- Plasma 5.0.1

* Thu Jul 17 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.0-1
- Plasma 5.0.0

* Thu May 15 2014 Daniel Vrátil <dvratil@redhat.com> - 4.96.0-1.20140515git532fc47
- Initial version of kde5-plasma-desktop
