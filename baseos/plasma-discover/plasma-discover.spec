%global base_name discover
%global flatpak_version 0.8.0
# enable snap support (or not)
%global snap 0
%global snapd_glib_version 1.66
# enable fwupd support (or not)
%global fwupd 1

Name:    plasma-discover
Summary: KDE and Plasma resources management GUI
Version: 6.2.5
Release: 3%{?dist}

License: BSD-3-Clause AND CC0-1.0 AND GPL-2.0-only AND GPL-2.0-or-later AND GPL-3.0-only AND LGPL-2.0-or-later AND LGPL-2.1-only AND LGPL-3.0-only AND (GPL-2.0-only OR GPL-3.0-only) AND (LGPL-2.1-only OR LGPL-3.0-only)
URL:     https://invent.kde.org/plasma/discover

Source0: https://download.kde.org/%{stable_kf6}/plasma/%{version}/%{base_name}-%{version}.tar.xz

## upstream patches

## downstream patches
# Adjust periodic refresh from 1/24hr to 1/12hr
# This ensures that it is checked at least once during the work day.
# It is double the time that Fedora repos are set to in DNF (6h).
Patch200: discover-pk-refresh-timer.patch

## upstreamable patches

# https://fedoraproject.org/wiki/Changes/EncourageI686LeafRemoval
ExcludeArch: %{ix86}

BuildRequires: appstream-qt-devel >= 1.0.0~
BuildRequires: flatpak-devel >= %{flatpak_version}
BuildRequires: libstemmer-devel
BuildRequires: libyaml-devel
BuildRequires: desktop-file-utils
BuildRequires: gettext
BuildRequires: libxml2-devel
BuildRequires: pkgconfig(libmarkdown)
BuildRequires: cmake(QCoro6)
BuildRequires: cmake(KF6ItemModels)

%if 0%{?fedora}
BuildRequires: rpm-ostree-devel
%endif

%if 0%{?fwupd}
BuildRequires: pkgconfig(fwupd)
%endif

BuildRequires: extra-cmake-modules
BuildRequires: kf6-rpm-macros

BuildRequires: cmake(KF6Config)
BuildRequires: cmake(KF6CoreAddons)
BuildRequires: cmake(KF6DBusAddons)
BuildRequires: cmake(KF6I18n)
BuildRequires: cmake(KF6KIO)
BuildRequires: cmake(KF6KirigamiAddons)
BuildRequires: cmake(KF6Notifications)
BuildRequires: cmake(KF6Purpose)
BuildRequires: cmake(KF6StatusNotifierItem)
BuildRequires: cmake(KF6WidgetsAddons)
BuildRequires: cmake(KF6Attica)
BuildRequires: cmake(KF6Archive)
BuildRequires: cmake(KF6KCMUtils)
BuildRequires: cmake(KF6Crash)
BuildRequires: cmake(KF6Declarative)
BuildRequires: cmake(KF6IconThemes)
BuildRequires: cmake(KF6IdleTime)
BuildRequires: cmake(KF6NewStuff)
BuildRequires: cmake(KF6Kirigami2)
BuildRequires: cmake(KF6UserFeedback)

BuildRequires: pkgconfig(phonon4qt6)


BuildRequires: pkgconfig(Qt6Concurrent)
BuildRequires: pkgconfig(Qt6DBus) >= 5.10.0
BuildRequires: pkgconfig(Qt6Network)
BuildRequires: pkgconfig(Qt6Qml)
BuildRequires: pkgconfig(Qt6QuickWidgets)
BuildRequires: pkgconfig(Qt6Svg)
BuildRequires: pkgconfig(Qt6Test)
%ifarch %{qt6_qtwebengine_arches}
BuildRequires: pkgconfig(Qt6WebView)
%endif
BuildRequires: pkgconfig(Qt6Widgets)
BuildRequires: pkgconfig(Qt6Xml)

Requires: kf6-kirigami2

Requires: %{name}-libs%{?_isa} = %{version}-%{release}

# Enable -flatpak by default
Recommends: %{name}-flatpak = %{version}-%{release}

%if 0%{?fedora} > 35
Recommends: fedora-appstream-metadata
%endif

# Require fedora-third-party on Fedora
%if 0%{?fedora}
Requires: fedora-third-party
%endif

# handle upgrade path
%if ! 0%{?snap}
Obsoletes: plasma-discover-snap < %{version}-%{release}
%endif
Provides: plasma-discover-offline-updates
Obsoletes: plasma-discover-offline-updates
Provides: plasma-discover-packagekit
Obsoletes: plasma-discover-packagekit

%description
KDE and Plasma resources management GUI.


%package libs
Summary: Runtime libraries for %{name}
Requires: qt5-qtquickcontrols2%{?_isa}
%description libs
%{summary}.

%package notifier
Summary: Plasma Discover Update Notifier
# -notifier replaces plasma-pk-updates for f34+
%if 0%{?fedora} > 33
Obsoletes: plasma-pk-updates < 0.5
%endif
Obsoletes: plasma-discover-updater < 5.6.95
Provides:  plasma-discover-updater = %{version}-%{release}
Requires: %{name} = %{version}-%{release}
%description notifier
%{summary}.

%package flatpak
Summary: Plasma Discover flatpak support
Requires: %{name} = %{version}-%{release}
Requires: %{name}-libs = %{version}-%{release}
Requires: flatpak >= %{flatpak_version}
Requires: flatpak-libs%{?_isa} >= %{flatpak_version}
Requires: (flatpak-kcm if plasma-systemsettings)
Supplements: (%{name} and flatpak)
%if 0%{?fedora}
# Pull in the flathub remote package
Recommends: fedora-flathub-remote
%endif
%description flatpak
%{summary}.

%if 0%{?snap}
%package snap
Summary: Plasma Discover snap support
BuildRequires: cmake(Snapd) >= %{snapd_glib_version}
Requires: %{name} = %{version}-%{release}
Requires: %{name}-libs = %{version}-%{release}
Requires: snapd-qt%{?_isa} >= %{snapd_glib_version}
Requires: snapd
Supplements: (%{name} and snapd)
%description snap
%{summary}.
%endif

%package offline-updates
Summary: Plasma Discover Offline updates enablement
Requires: %{name} = %{version}-%{release}
%description offline-updates
Enable Offline Updates feature by default
in %{name}.

%if 0%{?fedora}
# Only used for Fedora Kinoite
%package rpm-ostree
Summary: Plasma Discover backend for rpm-ostree support
Requires: %{name} = %{version}-%{release}
Supplements: ((%{name} and rpm-ostree) unless dnf)
%description rpm-ostree
Plasma Discover backend for rpm-ostree support in %{name}.
%endif


%prep
%autosetup -n %{base_name}-%{version} -p1


%build
%if 0%{?fedora}
%cmake_kf6 \
  -DBUILD_RpmOstreeBackend:BOOL=ON
%else
%cmake_kf6
%endif

%cmake_build


%install
%cmake_install

## unpackaged files
%if !0%{?snap}
rm -fv %{buildroot}%{_datadir}/applications/org.kde.discover.snap.desktop
%endif

%find_lang libdiscover
%find_lang kcm_updates
%find_lang plasma-discover --with-html
%find_lang plasma-discover-notifier

cat kcm_updates.lang plasma-discover.lang | sort | uniq -u > discover.lang


%check
appstream-util validate-relax --nonet %{buildroot}%{_kf6_metainfodir}/org.kde.discover.appdata.xml ||:
appstream-util validate-relax --nonet %{buildroot}%{_kf6_metainfodir}/org.kde.discover.flatpak.appdata.xml ||:
desktop-file-validate %{buildroot}%{_datadir}/applications/org.kde.discover.desktop


%files -f discover.lang
%{_bindir}/plasma-discover
%{_bindir}/plasma-discover-update
%{_kf6_metainfodir}/org.kde.discover.appdata.xml
%{_datadir}/applications/org.kde.discover.desktop
%{_datadir}/applications/org.kde.discover.urlhandler.desktop
%{_datadir}/icons/hicolor/*/apps/plasmadiscover.*
%{_datadir}/icons/hicolor/*/apps/flatpak-discover.*
%{_datadir}/kxmlgui5/plasmadiscover/
%if 0%{?snap}
%{_libexecdir}/discover/
%endif
%{_kf6_datadir}/applications/kcm_updates.desktop

%files notifier -f plasma-discover-notifier.lang
%{_datadir}/knotifications6/discoverabstractnotifier.notifyrc
%{_sysconfdir}/xdg/autostart/org.kde.discover.notifier.desktop
%{_datadir}/applications/org.kde.discover.notifier.desktop
%{_libexecdir}/DiscoverNotifier

%files libs -f libdiscover.lang
%license LICENSES/*.txt
%{_kf6_datadir}/qlogging-categories6/discover.categories
%dir %{_libdir}/plasma-discover/
%{_libdir}/plasma-discover/libDiscoverNotifiers.so
%{_libdir}/plasma-discover/libDiscoverCommon.so
%dir %{_kf6_qtplugindir}/discover
%dir %{_kf6_qtplugindir}/discover-notifier/
%if 0%{?fwupd}
%{_kf6_qtplugindir}/discover/fwupd-backend.so
%endif
%{_kf6_qtplugindir}/discover/kns-backend.so
%dir %{_datadir}/libdiscover
%dir %{_datadir}/libdiscover/categories
%{_kf6_qtplugindir}/plasma/kcms/systemsettings/kcm_updates.so

%files flatpak
%{_datadir}/applications/org.kde.discover-flatpak.desktop
%{_kf6_metainfodir}/org.kde.discover.flatpak.appdata.xml
%{_kf6_qtplugindir}/discover-notifier/FlatpakNotifier.so
%{_kf6_qtplugindir}/discover/flatpak-backend.so
%{_datadir}/libdiscover/categories/flatpak-backend-categories.xml

%if 0%{?snap}
%files snap
%dir %{_libexecdir}/discover/
%{_libexecdir}/discover/SnapMacaroonDialog
%{_kf6_libexecdir}/kauth/libsnap_helper
%{_kf6_metainfodir}/org.kde.discover.snap.appdata.xml
%{_kf6_qtplugindir}/discover/snap-backend.so
%{_datadir}/dbus-1/system.d/org.kde.discover.libsnapclient.conf
%{_datadir}/dbus-1/system-services/org.kde.discover.libsnapclient.service
%{_datadir}/polkit-1/actions/org.kde.discover.libsnapclient.policy
%{_kf6_datadir}/applications/org.kde.discover.snap.desktop
%endif

%if 0%{?fedora}
%files rpm-ostree
%{_datadir}/libdiscover/categories/rpm-ostree-backend-categories.xml
%{_kf6_qtplugindir}/discover/rpm-ostree-backend.so
%{_kf6_qtplugindir}/discover-notifier/rpm-ostree-notifier.so
%endif


%changelog
* Tue Dec 31 2024 Steve Cossette <farchord@gmail.com> - 6.2.5-1
- 6.2.5

* Tue Nov 26 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.2.4-1
- 6.2.4

* Thu Nov 07 2024 Steve Cossette <farchord@gmail.com> - 6.2.3-2
- Fix for auto-update on kinoite

* Tue Nov 05 2024 Steve Cossette <farchord@gmail.com> - 6.2.3-1
- 6.2.3

* Tue Oct 22 2024 Steve Cossette <farchord@gmail.com> - 6.2.2-1
- 6.2.2

* Tue Oct 15 2024 Steve Cossette <farchord@gmail.com> - 6.2.1-1
- 6.2.1

* Fri Oct 04 2024 Richard Hughes <rhughes@redhat.com> - 6.2.0-2
- Rebuild against fwupd 2.0.0

* Thu Oct 03 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.2.0-1
- 6.2.0

* Fri Sep 27 2024 Alessandro Astone <ales.astone@gmail.com> - 6.1.90-2
- Backport patch to fix showing the system tray icon (rhbz#2314785)

* Thu Sep 12 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.1.90-1
- 6.1.90

* Tue Sep 10 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.1.5-1
- 6.1.5

* Fri Aug 09 2024 Steve Cossette <farchord@gmail.com> - 6.1.4-1
- 6.1.4

* Wed Jul 24 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.1.3-3
- rebuilt

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jul 16 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.1.3-1
- 6.1.3

* Wed Jul 03 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.1.2-1
- 6.1.2

* Tue Jun 25 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.1.1-1
- 6.1.1

* Thu Jun 13 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.1.0-1
- 6.1.0

* Fri May 24 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.0.90-1
- 6.0.90

* Wed May 22 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.0.5-1
- 6.0.5

* Wed May 08 2024 Alessandro Astone <ales.astone@gmail.com> - 6.0.4-2
- Ensure fwupd user agent includes any information that LVFS expects

* Tue Apr 16 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.0.4-1
- 6.0.4

* Tue Mar 26 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.0.3-1
- 6.0.3

* Sat Mar 23 2024 Timothée Ravier <tim@siosm.fr> - 6.0.2-2

- Backport patches to fix rpm-ostree container support

* Tue Mar 12 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.0.2-1
- 6.0.2

* Wed Mar 06 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.0.1-1
- 6.0.1

* Sun Feb 25 2024 Neal Gompa <ngompa@fedoraproject.org> - 6.0.0-3
- Re-enable snap support

* Thu Feb 22 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.0.0-2
- Remove unneeded BuildRequires

* Wed Feb 21 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 6.0.0-1
- 6.0.0

* Wed Jan 31 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 5.93.0-1
- 5.93.0

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.92.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Alessandro Astone <ales.astone@gmail.com> - 5.92.0-3
- Remove patch for disabling rawhide distro upgrade

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.92.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jan 10 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 5.92.0-1
- 5.92.0

* Wed Jan 03 2024 Alessandro Astone <ales.astone@gmail.com> - 5.91.0-3
- Fix notifier (RHBZ#2256650)

* Sun Dec 24 2023 Alessandro Astone <ales.astone@gmail.com> - 5.91.0-2
- Backport patch to fix update button

* Thu Dec 21 2023 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 5.91.0-1
- 5.91.0

* Sun Dec 03 2023 Justin Zobel <justin.zobel@gmail.com> - 5.90.0-1
- Update to 5.90.0

* Sun Nov 26 2023 Alessandro Astone <ales.astone@gmail.com> - 5.27.80-2
- Enable packagekit autoremove

* Sat Nov 18 2023 Alessandro Astone <ales.astone@gmail.com> - 5.27.80-1
- 5.27.80

* Tue Oct 24 2023 Steve Cossette <farchord@gmail.com> - 5.27.9-1
- 5.27.9

* Wed Oct 18 2023 Alessandro Astone <ales.astone@gmail.com> - 5.27.8-2
- Update force refresh patch from upstream

* Tue Sep 12 2023 justin.zobel@gmail.com - 5.27.8-1
- 5.27.8

* Thu Aug 24 2023 Alessandro Astone <ales.astone@gmail.com> - 5.27.7-2
- Backport distro upgrade

* Tue Aug 01 2023 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 5.27.7-1
- 5.27.7

* Mon Jul 24 2023 Timothée Ravier <tim@siosm.fr> - 5.27.6-3
- Enable the rpm-ostree backend only on Fedora (used in Fedora Kinoite).
  Move the "Operating System" category definition to the rpm-ostree backend.

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.27.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sun Jun 25 2023 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 5.27.6-1
- 5.27.6

* Sat May 13 2023 Adam Williamson <awilliam@redhat.com> - 5.27.5-2
- Backport MR #548 to fix error message on start with fwupd 1.9.1

* Wed May 10 2023 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 5.27.5-1
- 5.27.5

* Mon May 01 2023 Neal Gompa <ngompa@fedoraproject.org> - 5.27.4-3
- Add dependencies for fedora-third-party components

* Sun Apr 09 2023 Alessandro Astone <ales.astone@gmail.com> - 5.27.4-2
- Backport patch to fix fwupd updates

* Tue Apr 04 2023 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 5.27.4-1
- 5.27.4

* Wed Mar 22 2023 Alessandro Astone <ales.astone@gmail.com> - 5.27.3-2
- Backport patch to fix updating whithin 5min of login

* Tue Mar 14 2023 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 5.27.3-1
- 5.27.3

* Tue Feb 28 2023 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 5.27.2-1
- 5.27.2

* Thu Feb 23 2023 Adam Williamson <awilliam@redhat.com> - 5.27.1-2
- Backport MR #486 to fix fwupd problem (#2173022)

* Tue Feb 21 2023 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 5.27.1-1
- 5.27.1

* Thu Feb 09 2023 Marc Deop <marcdeop@fedoraproject.org> - 5.27.0-1
- 5.27.0

* Tue Jan 24 2023 Marc Deop <marcdeop@fedoraproject.org> - 5.26.90-3
- -flatpak to install flatpak-kcm if plasma-systemsettings is installed

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.26.90-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jan 19 2023 Marc Deop <marcdeop@fedoraproject.org> - 5.26.90-1
- 5.26.90

* Thu Jan 05 2023 Justin Zobel <justin@1707.io> - 5.26.5-1
- Update to 5.26.5

* Tue Nov 29 2022 Marc Deop <marcdeop@fedoraproject.org> - 5.26.4-1
- 5.26.4

* Wed Nov 09 2022 Marc Deop <marcdeop@fedoraproject.org> - 5.26.3-1
- 5.26.3

* Tue Nov 01 2022 Adam Williamson <awilliam@redhat.com> - 5.26.2-3
- Bump to do F37 build on correct side tag

* Tue Nov 01 2022 Adam Williamson <awilliam@redhat.com> - 5.26.2-2
- Backport MR #404 to fix update notifications (#2139092)

* Wed Oct 26 2022 Marc Deop <marcdeop@fedoraproject.org> - 5.26.2-1
- 5.26.2

* Tue Oct 18 2022 Marc Deop <marcdeop@fedoraproject.org> - 5.26.1-1
- 5.26.1

* Thu Oct 06 2022 Marc Deop <marcdeop@fedoraproject.org> - 5.26.0-1
- 5.26.0

* Wed Sep 21 2022 Marc Deop marcdeop@fedoraproject.org - 5.25.90-2
- Add patch to support systems without a Qt WebView

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

* Fri Jun 24 2022 Timothée Ravier <tim@siosm.fr> - 5.25.1-2
- Recommend fedora-appstream-metadata

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

* Tue Feb 22 2022 Rex Dieter <rdieter@fedoraproject.org> - 5.24.2.1-1
- 5.24.2.1

* Tue Feb 22 2022 Rex Dieter <rdieter@fedoraproject.org> - 5.24.2-1
- 5.24.2

* Tue Feb 15 2022 Marc Deop <marcdeop@fedoraproject.org> - 5.24.1-1
- 5.24.1

* Fri Feb 11 2022 Marc Deop <marcdeop@fedoraproject.org> - 5.24.0-2
- Rebuild due to tarball re-spin

* Thu Feb 03 2022 Marc Deop <marcdeop@fedoraproject.org> - 5.24.0-1
- 5.24.0

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.23.90-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jan 13 2022 Marc Deop <marcdeop@fedoraproject.org> - 5.23.90-1
- 5.23.90

* Tue Jan 04 2022 Marc Deop <marcdeop@fedoraproject.org> - 5.23.5-1
- 5.23.5

* Wed Dec 29 2021 Rex Dieter <rdieter@fedoraproject.org> - 5.23.4-2
- disable do-not-use-system-appstream-cache.patch, no workie with newer appstream-0.15.1+

* Tue Dec 14 2021 Marc Deop <marcdeop@fedoraproject.org> - 5.23.4-1
- 5.23.4

* Mon Nov 29 2021 Timothée Ravier <tim@siosm.fr> - 5.23.3.1-2
- Stronger checks to install rpm-ostree backend only on Kinoite

* Fri Nov 12 2021 Marc Deop <marcdeop@fedoraproject.org> - 5.23.3.1-1
- 5.23.3.1

* Wed Nov 10 2021 Rex Dieter <rdieter@fedoraproject.org> - 5.23.3-1
- 5.23.3

* Tue Oct 26 2021 Rex Dieter <rdieter@fedoraproject.org> - 5.23.2-1
- 5.23.2

* Thu Oct 21 2021 Adam Williamson <awilliam@redhat.com> - 5.23.1-1
- 5.23.1
- Backport a necessary commit upstream missed (to make PK sources checkable)
- Backport MR #192 to make PK sources list less bouncy (#2011774)

* Thu Oct 21 2021 Adam Williamson <awilliam@redhat.com> - 5.23.0-4
- Update some backported patches to final merged versions
- Backport MR #192 to make PackageKit source list less bouncy (#2011774)

* Tue Oct 19 2021 Adam Williamson <awilliam@redhat.com> - 5.23.0-3
- Don't use system appstream cache (#2011322)

* Mon Oct 18 2021 Adam Williamson <awilliam@redhat.com> - 5.23.0-2
- Backport several upstream fixes for various source state issues:
  Flatpak: show correct remote state, fix deleting disabled remotes (#2011291)
  Redraw checkbox correctly when enabling/disabling fwupd remotes (#2011333)

* Thu Oct 07 2021 Rex Dieter <rdieter@fedoraproject.org> - 5.23.0-1
- 5.23.0

* Wed Oct 06 2021 Rex Dieter <rdieter@fedoraproject.org> - 5.22.90-3
- backport fixes from 5.23 branch

* Sat Sep 18 2021 Marc Deop <marcdeop@fedoraproject.org> - 5.22.90-2
- Remove patch as it's applied upstream already (#2000577)

* Fri Sep 17 2021 Marc Deop <marcdeop@fedoraproject.org> - 5.22.90-1
- 5.22.90

* Thu Sep 02 2021 Jonathan Wakely <jwakely@redhat.com> - 5.22.5-2
- Fix typo in restart message (#2000577)

* Tue Aug 31 2021 Jan Grulich <jgrulich@redhat.com> - 5.22.5-1
- 5.22.5

* Fri Aug 27 2021 Timothée Ravier <travier@redhat.com> - 5.22.4-2
- Add rpm-ostree backend

* Wed Jul 28 2021 Jan Grulich <jgrulich@redhat.com> - 5.22.4-1
- 5.22.4

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.22.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jul 12 2021 Jan Grulich <jgrulich@redhat.com> - 5.22.3-1
- 5.22.3

* Tue Jun 22 2021 Jan Grulich <jgrulich@redhat.com> - 5.22.2.1-1
- 5.22.2.1

* Tue Jun 22 2021 Jan Grulich <jgrulich@redhat.com> - 5.22.2-1
- 5.22.2

* Fri Jun 18 2021 Rex Dieter <rdieter@fedoraproject.org> - 5.22.1-2
- -packagekit: add versioned dep on main pkg

* Tue Jun 15 2021 Jan Grulich <jgrulich@redhat.com> - 5.22.1-1
- 5.22.1

* Mon Jun 14 2021 Alessandro Astone <ales.astone@gmail.com> - 5.22.0-2
- Use XDG discoverrc to enable offline updates by default

* Sun Jun 06 2021 Jan Grulich <jgrulich@redhat.com> - 5.22.0-1
- 5.22.0

* Tue May 04 2021 Jan Grulich <jgrulich@redhat.com> - 5.21.5-1
- 5.21.5

* Fri Apr 16 2021 Rex Dieter <rdieter@fedoraproject.org> - 5.21.4-2
- plasma-discover doesnt refresh metadata (#1903294)

* Tue Apr 06 2021 Jan Grulich <jgrulich@redhat.com> - 5.21.4-1
- 5.21.4

* Tue Mar 16 2021 Jan Grulich <jgrulich@redhat.com> - 5.21.3-1
- 5.21.3

* Thu Mar 11 2021 Rex Dieter <rdieter@fedoraproject.org> - 5.21.2-3
- CVE-2021-28117

* Mon Mar 08 2021 Timothée Ravier <travier@redhat.com> - 5.21.2-2
- Have PackageKit backend requires PackageKit for all branches
  Recommend flatpak backend for all branches
  Move PackageKit appdata to sub package

* Tue Mar 02 2021 Jan Grulich <jgrulich@redhat.com> - 5.21.2-1
- 5.21.2

* Fri Feb 26 2021 Timothée Ravier <travier@redhat.com> - 5.21.1-2
- Split PackageKit backend into a sub-package for Fedora Kinoite

* Tue Feb 23 2021 Jan Grulich <jgrulich@redhat.com> - 5.21.1-1
- 5.21.1

* Mon Feb 22 2021 Rex Dieter <rdieter@fedoraproject.org> - 5.21.0-2
- -offline-updates: put env snippet in the right place

* Thu Feb 11 2021 Jan Grulich <jgrulich@redhat.com> - 5.21.0-1
- 5.21.0

* Wed Feb 10 2021 Rex Dieter <rdieter@fedoraproject.org> - 5.20.90-4
- backport upstream fixes

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.20.90-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jan 22 2021 Rex Dieter <rdieter@fedoraproject.org> - 5.20.90-2
- BR: KUserFeedback

* Thu Jan 21 2021 Jan Grulich <jgrulich@redhat.com> - 5.20.90-1
- 5.20.90 (beta)

* Tue Jan  5 16:03:29 CET 2021 Jan Grulich <jgrulich@redhat.com> - 5.20.5-1
- 5.20.5

* Tue Dec  1 09:42:56 CET 2020 Jan Grulich <jgrulich@redhat.com> - 5.20.4-1
- 5.20.4

* Mon Nov 30 2020 Rex Dieter <rdieter@fedoraproject.org> - 5.20.3-3
- Recommends: -flatpak (f34+)

* Mon Nov 30 2020 Rex Dieter <rdieter@fedoraproject.org> - 5.20.3-2
- make env file match name of env variable PK_OFFLINE_UPDATE)

* Wed Nov 11 08:22:38 CET 2020 Jan Grulich <jgrulich@redhat.com> - 5.20.3-1
- 5.20.3

* Thu Nov 05 2020 Rex Dieter <rdieter@fedoraproject.org> - 5.20.2-3
- -notifier: depend on main instead of just -libs
- -notifier: Obsoletes: plasma-pk-updates (f34+)
- Recommands: -offline-updates (f34+)

* Thu Nov 05 2020 Rex Dieter <rdieter@fedoraproject.org> - 5.20.2-2
- .spec cleanup
- update URL
- offline-updates subpkg, to opt-in to the feature

* Tue Oct 27 14:21:58 CET 2020 Jan Grulich <jgrulich@redhat.com> - 5.20.2-1
- 5.20.2

* Tue Oct 20 15:27:56 CEST 2020 Jan Grulich <jgrulich@redhat.com> - 5.20.1-1
- 5.20.1

* Sun Oct 11 19:50:02 CEST 2020 Jan Grulich <jgrulich@redhat.com> - 5.20.0-1
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

* Tue Jun 9 2020 Martin Kyral <martin.kyral@gmail.com> - 5.19.0-1
- 5.19.0

* Fri May 15 2020 Martin Kyral <martin.kyral@gmail.com> - 5.18.90-1
- 5.18.90

* Tue May 05 2020 Jan Grulich <jgrulich@redhat.com> - 5.18.5-1
- 5.18.5

* Sat Apr 04 2020 Rex Dieter <rdieter@fedoraproject.org> - 5.18.4.1-1
- 5.18.4.1

* Tue Mar 31 2020 Jan Grulich <jgrulich@redhat.com> - 5.18.4-1
- 5.18.4

* Tue Mar 10 2020 Jan Grulich <jgrulich@redhat.com> - 5.18.3-1
- 5.18.3

* Tue Feb 25 2020 Jan Grulich <jgrulich@redhat.com> - 5.18.2-1
- 5.18.2

* Tue Feb 18 2020 Rex Dieter <rdieter@fedoraproject.org> - 5.18.1-2
- Recommends: PackageKit

* Tue Feb 18 2020 Jan Grulich <jgrulich@redhat.com> - 5.18.1-1
- 5.18.1
- enable fwupd,markdown support

* Tue Feb 11 2020 Jan Grulich <jgrulich@redhat.com> - 5.18.0-1
- 5.18.0

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.17.90-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jan 16 2020 Jan Grulich <jgrulich@redhat.com> - 5.17.90-1
- 5.17.90

* Wed Jan 08 2020 Jan Grulich <jgrulich@redhat.com> - 5.17.5-1
- 5.17.5

* Thu Dec 05 2019 Jan Grulich <jgrulich@redhat.com> - 5.17.4-1
- 5.17.4

* Wed Nov 13 2019 Martin Kyral <martin.kyral@gmail.com> - 5.17.3-1
- 5.17.3

* Wed Oct 30 2019 Jan Grulich <jgrulich@redhat.com> - 5.17.2-1
- 5.17.2

* Wed Oct 23 2019 Jan Grulich <jgrulich@redhat.com> - 5.17.1-1
- 5.17.1

* Thu Oct 10 2019 Jan Grulich <jgrulich@redhat.com> - 5.17.0-1
- 5.17.0

* Fri Sep 20 2019 Martin Kyral <martin.kyral@gmail.com> - 5.16.90-1
- 5.16.90

* Wed Sep 11 2019 Rex Dieter <rdieter@fedoraproject.org> 5.16.5-2
- handle upgrade path if -snap is not enabled
- re-enable -snap support

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
- temporarily disable snap support on f31+

* Tue Jun 11 2019 Martin Kyral <martin.kyral@gmail.com> - 5.16.0-1
- 5.16.0

* Thu May 16 2019 Martin Kyral <martin.kyral@gmail.com> - 5.15.90-1
- 5.15.90

* Thu May 09 2019 Martin Kyral <martin.kyral@gmail.com> - 5.15.5-1
- 5.15.5

* Wed Apr 03 2019 Rex Dieter <rdieter@fedoraproject.org> - 5.15.4-1
- 5.15.4

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

* Fri Jul 20 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.13.3-4
- use %%_qt5_qmldir

* Wed Jul 11 2018 Martin Kyral <martin.kyral@gmail.com> - 5.13.3-1
- 5.13.3

* Mon Jul 09 2018 Martin Kyral <martin.kyral@gmail.com> - 5.13.2-1
- 5.13.2

* Tue Jun 19 2018 Martin Kyral <martin.kyral@gmail.com> - 5.13.1-1
- 5.13.1

* Mon Jun 18 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.13.0-3
- bump deps
- use Supplements
- %%check: validate apddata consistently

* Tue Jun 12 2018 Neal Gompa <ngompa13@gmail.com> - 5.13.0-2
- Enable snap backend and build as subpackage
- Use rich supplements for flatpak backend subpackage
- Fix file lists to completely separate flatpak and snap backend plugins

* Sat Jun 09 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.13.0-1
- 5.13.0

* Mon May 21 2018 Martin Kyral <martin.kyral@gmail.com> - 5.12.90-1
- 5.12.90

* Sun May 20 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.12.5.1-2
- pull in upstream fix

* Thu May 17 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.12.5.1-1
- 5.12.5.1
- +appdata validation

* Wed May 16 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.12.5-2
- pull in upstream fixes

* Tue May 01 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.12.5-1
- 5.12.5

* Tue May 01 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.12.4-2
- cleanup

* Tue Mar 27 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.12.4-1
- 5.12.4

* Tue Mar 06 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.12.3-1
- 5.12.3

* Wed Feb 21 2018 Jan Grulich <jgrulich@redhat.com> - 5.12.2-1
- 5.12.2

* Tue Feb 13 2018 Jan Grulich <jgrulich@redhat.com> - 5.12.1-1
- 5.12.1

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.12.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Feb 02 2018 Jan Grulich <jgrulich@redhat.com> - 5.12.0-1
- 5.12.0

* Thu Jan 18 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 5.11.95-3
- Remove obsolete scriptlets

* Tue Jan 16 2018 Rex Dieter <rdieter@fedoraproject.org> - 5.11.95-2
- -flatpak subpkg
- drop -muon references (Obsoletes mostly)

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

* Sat Jul 22 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.10.4-1
- 5.10.4

* Fri Jul 07 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.10.3-2
- make kf5-kirigami2 dep versioned
- pull in upstream fixes

* Tue Jun 27 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.10.3-1
- 5.10.3

* Thu Jun 15 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.10.2-1
- 5.10.2

* Thu Jun 15 2017 Jan Grulich <jgrulich@redhat.com> - 5.10.1-2
- Require flatpak to be present for flatpak backend

* Tue Jun 06 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.10.1-1
- 5.10.1

* Wed May 31 2017 Jan Grulich <jgrulich@redhat.com> - 5.10.0-1
- 5.10.0

* Wed Apr 26 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.9.5-1
- 5.9.5

* Thu Mar 23 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.9.4-1
- 5.9.4

* Sat Mar 04 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.9.3-2
- rebuild

* Wed Mar 01 2017 Jan Grulich <jgrulich@redhat.com> - 5.9.3-1
- 5.9.3

* Tue Feb 21 2017 Rex Dieter <rdieter@fedoraproject.org> - 5.8.6-1
- 5.8.6

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.8.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Dec 28 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.8.5-1
- 5.8.5

* Wed Nov 23 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.8.4-2
- pull in upstream fixes

* Tue Nov 22 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.8.4-1
- 5.8.4

* Mon Nov 14 2016 Rex Dieter <rdieter@fedoraproejct.org> - 5.8.3-2
- pull in upstream fixes (appstream FTBFS #1392571)

* Tue Nov 01 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.8.3-1
- 5.8.3

* Tue Oct 18 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.8.2-1
- 5.8.2

* Tue Oct 11 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.8.1-1
- 5.8.1

* Sat Oct 01 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.8.0-2
- bump appstream dep

* Thu Sep 29 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.8.0-1
- 5.8.0

* Fri Sep 23 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.7.95-2
- (Build)Requires: kf5-kirigami

* Thu Sep 22 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.7.95-1
- 5.7.95

* Sat Sep 17 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.7.5-2
- rebuild (appstream)

* Tue Sep 13 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.7.5-1
- 5.7.5

* Tue Aug 23 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.7.4-1
- 5.7.4

* Tue Aug 02 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.7.3-1
- 5.7.3

* Mon Jul 25 2016 Helio Chissini de Castro <helio@kde.org> - 5.7.2-2
- Add missing Requires for qtquick controls

* Tue Jul 19 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.7.2-1
- 5.7.2

* Tue Jul 12 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.7.1-1
- 5.7.1

* Thu Jun 30 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.7.0-1
- 5.7.0

* Sat Jun 25 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6.95-1
- 5.6.95, -updater => -notifier

* Tue Jun 14 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6.5-1
- 5.6.5

* Sat May 14 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6.4-1
- 5.6.4

* Mon Apr 18 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6.2-2
- bindir/muon-discover symlink

* Wed Apr 13 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6.2-1
- 5.6.2

* Sat Apr 09 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6.1-2
- License: GPLv2 or GPLv3 (KDE e.V)
- remove some commented/unused items from .spec
- expand comment why updater applet is disabled by default

* Fri Apr 08 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.6.1-1
- 5.6.1

* Sat Mar 05 2016 Daniel Vrátil <dvratil@fedoraproject.org> - 5.5.95-1
- Plasma 5.5.95

* Tue Mar 01 2016 Daniel Vrátil <dvratil@fedoraproject.org> - 5.5.5-1
- Plasma 5.5.5

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 5.5.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 27 2016 Daniel Vrátil <dvratil@fedoraproject.org> - 5.5.4-1
- Plasma 5.5.4

* Thu Jan 07 2016 Daniel Vrátil <dvratil@fedoraproject.org> - 5.5.3-1
- Plasma 5.5.3

* Thu Dec 31 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.5.2-1
- 5.5.2

* Tue Dec 29 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.5.1-2
- update description, summary, url
- -updater: disable updater plasmoid by default

* Fri Dec 18 2015 Daniel Vrátil <dvratil@fedoraproject.org> - 5.5.1-1
- Plasma 5.5.1

* Sun Dec 13 2015 Rex Dieter <rdieter@fedoraproject.org> 5.5.0-2
- rebuild (appstream)

* Thu Dec 03 2015 Daniel Vrátil <dvratil@fedoraproject.org> - 5.5.0-1
- Plasma 5.5.0

* Wed Nov 25 2015 Daniel Vrátil <dvratil@fedoraproject.org> - 5.4.95-1
- Plasma 5.4.95

* Thu Nov 05 2015 Daniel Vrátil <dvratil@fedoraproject.org> - 5.4.3-1
- Plasma 5.4.3

* Tue Nov 03 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.2-5
- more upstream fixes

* Thu Oct 29 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.2-4
- rebuild (PackageKit-Qt)

* Thu Oct 29 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.2-3
- -libs: (explicitly) Requires: PackageKit

* Wed Oct 28 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.2-2
- backport fix package removal (kde#354415)

* Fri Oct 02 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.4.2-1
- 5.4.2

* Tue Sep 29 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.1-2
- pull in upstream fixes (notably discover .desktop rename)

* Wed Sep 09 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.4.1-1
- 5.4.1

* Sat Jun 27 2015 Rex Dieter <rdieter@fedoraproject.org> 5.3.2-1
- 5.3.2

* Sat Jun 27 2015 Rex Dieter <rdieter@fedoraproject.org> 5.3.1-5
- rebuild (appstream)

* Sat Jun 27 2015 Rex Dieter <rdieter@fedoraproject.org> 5.3.1-4
- rebuild (appstream)

* Wed Jun 17 2015 Rex Dieter <rdieter@fedoraproject.org> 5.3.1-3
- BR: kf5-kiconthemes-devel kf5-kio-devel kf5-kitemviews-devel

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun May 31 2015 Daniel Vrátil <dvratil@redhat.com> 5.3.1-1
- Plasma 5.3.1

* Sun May 03 2015 Rex Dieter <rdieter@fedoraproject.org> 5.3.0-1
- 5.3.0

* Mon Apr 20 2015 Rex Dieter <rdieter@fedoraproject.org> 5.2.2-2
- -discover, -updater, -libs subpkgs (w/ main metapackage)

* Mon Apr 20 2015 Rex Dieter <rdieter@fedoraproject.org> 5.2.2-1
- 5.2.2, %%license COPYING

* Tue Mar 17 2015 Rex Dieter <rdieter@fedoraproject.org> 5.2.1-3
- fix .desktop validation errors

* Mon Mar 16 2015 Rex Dieter <rdieter@fedoraproject.org> 5.2.1-2
- cleanup for review

* Mon Mar 16 2015 Elia Devito <eliadevito@yahoo.it> 5.2.1-1
- Initial SPEC file
