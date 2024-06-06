Name:           calamares
Version:        3.3.6
Release:        6%{?dist}
Summary:        Installer from a live CD/DVD/USB to disk

License:        GPL-3.0-or-later
URL:            https://calamares.io/
Source0:        https://github.com/calamares/calamares/releases/download/v%{version}/%{name}-%{version}.tar.gz
Source2:        show.qml
# Run:
# lupdate-qt6 show.qml -ts calamares-auto_fr.ts
# then translate the template in linguist-qt6.
Source3:        calamares-auto_fr.ts
# Run:
# lupdate-qt6 show.qml -ts calamares-auto_de.ts
# then translate the template in linguist-qt6.
Source4:        calamares-auto_de.ts
# Run:
# lupdate-qt6 show.qml -ts calamares-auto_it.ts
# then translate the template in linguist-qt6.
Source5:        calamares-auto_it.ts

# Use a custom install icon for nobara
Source6:        install-icon.svg

# adjust some default settings (default shipped .conf files)
Patch1:         0001-Apply-default-settings-for-Fedora.patch

## use kdesu instead of pkexec (works around #1171779)
Patch1002:       calamares-3.3.3-kdesu.patch


# Calamares is only supported where live images (and GRUB) are. (#1171380)
# This list matches the arches where grub2-efi is used to boot the system
ExclusiveArch:  %{ix86} x86_64 aarch64 riscv64

# Macros
BuildRequires:  git-core
BuildRequires:  kf6-rpm-macros

# Compilation tools
BuildRequires:  cmake >= 3.16
BuildRequires:  extra-cmake-modules >= 5.245
BuildRequires:  gcc-c++ >= 9.0.0
BuildRequires:  pkgconfig
BuildRequires:  make

# Other build-time tools
BuildRequires:  desktop-file-utils
BuildRequires:  gettext

# Qt 6
BuildRequires:  cmake(Qt6Concurrent)
BuildRequires:  cmake(Qt6Core)
BuildRequires:  cmake(Qt6DBus)
BuildRequires:  cmake(Qt6Gui)
BuildRequires:  cmake(Qt6LinguistTools)
BuildRequires:  cmake(Qt6Network)
BuildRequires:  cmake(Qt6Svg)
BuildRequires:  cmake(Qt6Widgets)
BuildRequires:  cmake(Qt6Quick)
BuildRequires:  cmake(Qt6QuickWidgets)

# KF6
BuildRequires:  cmake(KF6CoreAddons)
BuildRequires:  cmake(KF6Config)
BuildRequires:  cmake(KF6Crash)
BuildRequires:  cmake(KF6DBusAddons)
BuildRequires:  cmake(KF6I18n)
BuildRequires:  cmake(KF6Package)
BuildRequires:  cmake(KF6Parts)
BuildRequires:  cmake(KF6Service)
BuildRequires:  cmake(KF6WidgetsAddons)

# Plasma
BuildRequires:  cmake(Plasma)

# KPMcore
BuildRequires:  cmake(KPMcore) >= 4.2.0

# Python 3
BuildRequires:  python3-devel >= 3.3
BuildRequires:  python3-jsonschema
BuildRequires:  python3-pyyaml
BuildRequires:  boost-devel >= 1.55.0
%global __python %{__python3}

# Other libraries
BuildRequires:  cmake(AppStreamQt) >= 1.0.0
BuildRequires:  libpwquality-devel
BuildRequires:  libxcrypt-devel
BuildRequires:  parted-devel
BuildRequires:  yaml-cpp-devel >= 0.5.1

# for automatic branding setup
Requires(post): system-release
Requires(post): system-logos
Requires:       system-logos
Requires:	nobara-logos
Requires:       coreutils
Requires:       util-linux
Requires:       upower
Requires:       NetworkManager
Requires:       dracut
Recommends:       grub2
%ifarch x86_64 aarch64
%ifarch x86_64
# For x86 systems
Recommends:       grub2-efi-x64
Recommends:     grub2-efi-ia32
%else
# For all non-x86 arches
Recommends:       grub2-efi
%endif
Requires:       efibootmgr
%endif
Requires:       console-setup
Requires:       setxkbmap
Requires:       os-prober
Requires:       e2fsprogs
Requires:       dosfstools
Requires:       ntfsprogs
Requires:       gawk
Requires:       systemd
Requires:       rsync
Requires:       shadow-utils
Requires:       dnf
Requires:       kdesu
Requires:       hicolor-icon-theme

Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
# webview module is no longer available
Obsoletes:      %{name}-webview < 3.0.0~


%description
Calamares is a distribution-independent installer framework, designed to install
from a live CD/DVD/USB environment to a hard disk. It includes a graphical
installation program based on Qt 6. This package includes the Calamares
framework and the required configuration files to produce a working replacement
for Anaconda's liveinst.


%package        libs
Summary:        Calamares runtime libraries
Requires:       %{name} = %{version}-%{release}

%description    libs
%{summary}.


%package        interactiveterminal
Summary:        Calamares interactiveterminal module
Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Requires:       konsole-part

%description    interactiveterminal
Optional interactiveterminal module for the Calamares installer, based on the
KonsolePart (from Konsole 6)


%package        plasmalnf
Summary:        Calamares plasmalnf module
Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Requires:       plasma-desktop

%description    plasmalnf
Optional plasmalnf module for the Calamares installer, based on the KDE Plasma
Desktop Workspace and its KDE Frameworks (KConfig, KPackage, Plasma)


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Requires:       cmake

%description    devel
The %{name}-devel package contains libraries and header files for
developing custom modules for Calamares.


%prep
%autosetup -p1 -n %{name}-%{version}

cp %{SOURCE6} ./data/images/squid.svg
sed -i '/^Icon/ s/calamares/org.fedoraproject.AnacondaInstaller/g' ./calamares.desktop
sed -i '/^Icon\[.*$/d' ./calamares.desktop
sed -i '/^Icon/ s/calamares/org.fedoraproject.AnacondaInstaller/g' ./calamares.desktop.in
sed -i '/^Icon\[.*$/d' ./calamares.desktop.in

%build
%{cmake_kf6} -DCMAKE_BUILD_TYPE:STRING="RelWithDebInfo" \
             -DBUILD_TESTING:BOOL=OFF \
             -DWITH_PYTHONQT:BOOL=OFF \
             -DWITH_QT6:BOOL=ON \
             -DWITH_KPMCORE4API:BOOL=ON \
             -DINSTALL_CONFIG=ON \
             %{nil}
%cmake_build

%install
%cmake_install

# create the auto branding directory
mkdir -p %{buildroot}%{_datadir}/calamares/branding/auto
touch %{buildroot}%{_datadir}/calamares/branding/auto/branding.desc
install -p -m 644 %{SOURCE2} %{buildroot}%{_datadir}/calamares/branding/auto/show.qml
mkdir -p %{buildroot}%{_datadir}/calamares/branding/auto/lang
lrelease-qt6 %{SOURCE3} -qm %{buildroot}%{_datadir}/calamares/branding/auto/lang/calamares-auto_fr.qm
lrelease-qt6 %{SOURCE4} -qm %{buildroot}%{_datadir}/calamares/branding/auto/lang/calamares-auto_de.qm
lrelease-qt6 %{SOURCE5} -qm %{buildroot}%{_datadir}/calamares/branding/auto/lang/calamares-auto_it.qm
# own the local settings directories
mkdir -p %{buildroot}%{_sysconfdir}/calamares/modules
mkdir -p %{buildroot}%{_sysconfdir}/calamares/branding
# delete dummypythonqt translations, we do not use PythonQt at this time
rm -f %{buildroot}%{_datadir}/locale/*/LC_MESSAGES/calamares-dummypythonqt.mo
%find_lang calamares-python

%check
# validate the .desktop file
desktop-file-validate %{buildroot}%{_datadir}/applications/calamares.desktop

%post
# generate the "auto" branding
. %{_sysconfdir}/os-release

LOGO=%{_datadir}/pixmaps/fedora-logo.png

if [ -e %{_datadir}/pixmaps/fedora-gdm-logo-calamares.png ] ; then
  SPRITE="%{_datadir}/pixmaps/fedora-gdm-logo-calamares.png"
else
  SPRITE="%{_datadir}/calamares/branding/default/squid.png"
fi

if [ -e %{_datadir}/icons/hicolor/48x48/apps/fedora-logo-icon.png ] ; then
  ICON="%{_datadir}/icons/hicolor/48x48/apps/fedora-logo-icon.png"
else
  ICON="$SPRITE"
fi

if [ -n "$HOME_URL" ] ; then
  PRODUCTURL="$HOME_URL"
  HAVE_PRODUCTURL=" "
else
  PRODUCTURL="https://calamares.io/"
  HAVE_PRODUCTURL="#"
fi

if [ -n "$SUPPORT_URL" ] ; then
  SUPPORTURL="$SUPPORT_URL"
  HAVE_SUPPORTURL=" "
elif [ -n "$BUG_REPORT_URL" ] ; then
  SUPPORTURL="$BUG_REPORT_URL"
  HAVE_SUPPORTURL=" "
else
  SUPPORTURL="https://github.com/calamares/calamares/issues"
  HAVE_SUPPORTURL="#"
fi

cat >%{_datadir}/calamares/branding/auto/branding.desc <<EOF
# THIS FILE IS AUTOMATICALLY GENERATED! ANY CHANGES TO THIS FILE WILL BE LOST!
---
componentName:  auto

welcomeStyleCalamares:   false

strings:
    productName:         "$NAME"
    shortProductName:    "$NAME"
    version:             "$VERSION"
    shortVersion:        "$VERSION_ID"
    versionedName:       "$NAME $VERSION_ID"
    shortVersionedName:  "$NAME $VERSION_ID"
    bootloaderEntryName: "$NAME"
$HAVE_PRODUCTURL   productUrl:          "$PRODUCTURL"
$HAVE_SUPPORTURL   supportUrl:          "$SUPPORTURL"
#   knownIssuesUrl:      "http://calamares.io/about/"
#   releaseNotesUrl:     "http://calamares.io/about/"

images:
    productWelcome:      "$LOGO"
    productLogo:         "$SPRITE"
    productIcon:         "$ICON"

slideshow:               "show.qml"

style:
   SidebarBackground:    "#292F34"
   SidebarText:          "#FFFFFF"
   SidebarTextCurrent:    "#292F34"
   SidebarBackgroundCurrent: "#760da6"
EOF

%files -f calamares-python.lang
%doc AUTHORS
%license LICENSES/*
%{_bindir}/calamares
%dir %{_datadir}/calamares/
%{_datadir}/calamares/settings.conf
%dir %{_datadir}/calamares/branding/
%{_datadir}/calamares/branding/default/
%dir %{_datadir}/calamares/branding/auto/
%ghost %{_datadir}/calamares/branding/auto/branding.desc
%{_datadir}/calamares/branding/auto/show.qml
%{_datadir}/calamares/branding/auto/lang/
%{_datadir}/calamares/modules/
%exclude %{_datadir}/calamares/modules/interactiveterminal.conf
%exclude %{_datadir}/calamares/modules/plasmalnf.conf
%{_datadir}/calamares/qml/
%{_datadir}/applications/calamares.desktop
%{_datadir}/icons/hicolor/scalable/apps/calamares-nobara.svg
%{_mandir}/man8/calamares.8*
%{_sysconfdir}/calamares/

%files libs
%{_libdir}/libcalamares.so.*
%{_libdir}/libcalamaresui.so.*
%{_libdir}/calamares/
%exclude %{_libdir}/calamares/modules/interactiveterminal/
%exclude %{_libdir}/calamares/modules/plasmalnf/

%files interactiveterminal
%{_datadir}/calamares/modules/interactiveterminal.conf
%{_libdir}/calamares/modules/interactiveterminal/

%files plasmalnf
%{_datadir}/calamares/modules/plasmalnf.conf
%{_libdir}/calamares/modules/plasmalnf/

%files devel
%{_includedir}/libcalamares/
%{_libdir}/libcalamares.so
%{_libdir}/libcalamaresui.so
%{_libdir}/cmake/Calamares/


%changelog
* Wed Mar 13 2024 Neal Gompa <ngompa@fedoraproject.org> - 3.3.5-1
- Update to 3.3.5

* Mon Feb 26 2024 Neal Gompa <ngompa@fedoraproject.org> - 3.3.4-1
- Update to 3.3.4

* Sat Feb 24 2024 Neal Gompa <ngompa@fedoraproject.org> - 3.3.3-1
- Update to 3.3.3
- Backport fixes for Python module

* Wed Jan 31 2024 Pete Walter <pwalter@fedoraproject.org> - 3.3.1-5
- Rebuild for ICU 74

* Tue Jan 23 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jan 18 2024 Jonathan Wakely <jwakely@redhat.com> - 3.3.1-2
- Rebuilt for Boost 1.83

* Mon Jan 15 2024 Neal Gompa <ngompa@fedoraproject.org> - 3.3.1-1
- Update to 3.3.1

* Sat Dec 30 2023 Neal Gompa <ngompa@fedoraproject.org> - 3.3.0-1
- Update to 3.3.0 final

* Wed Dec 06 2023 Yaakov Selkowitz <yselkowitz@fedoraproject.org> - 3.3.0~alpha6-2
- Rebuilt for KDE Frameworks 5.246.0 and Gear 24.01.80

* Sun Nov 26 2023 Neal Gompa <ngompa@fedoraproject.org> - 3.3.0~alpha6-1
- Rebase to 3.3.0~alpha6 for AppStream 1.0 and Qt 6 compatibility

* Tue Nov 07 2023 Neal Gompa <ngompa@fedoraproject.org> - 3.2.62-5
- Switch to appstream0.16-qt

* Mon Sep 04 2023 Neal Gompa <ngompa@fedoraproject.org> - 3.2.62-4
- Add a patch to fix keyboard layout detection

* Mon Sep 04 2023 Neal Gompa <ngompa@fedoraproject.org> - 3.2.62-3
- Add more patches for Fedora Asahi

* Sat Sep 02 2023 Neal Gompa <ngompa@fedoraproject.org> - 3.2.62-2
- Refresh backported patch stack

* Sat Sep 02 2023 Neal Gompa <ngompa@fedoraproject.org> - 3.2.62-1
- Update to 3.2.62 and backport fixes for Asahi

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.61-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 František Zatloukal <fzatlouk@redhat.com> - 3.2.61-7
- Rebuilt for ICU 73.2

* Thu Jun 15 2023 Python Maint <python-maint@redhat.com> - 3.2.61-6
- Rebuilt for Python 3.12

* Mon Feb 20 2023 Jonathan Wakely <jwakely@redhat.com> - 3.2.61-5
- Rebuilt for Boost 1.81

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.61-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Dec 31 2022 Pete Walter <pwalter@fedoraproject.org> - 3.2.61-3
- Rebuild for ICU 72

* Tue Nov 15 2022 Richard Shaw <hobbes1069@gmail.com> - 3.2.61-2
- Rebuild for yaml-cpp 0.7.0.

* Sat Nov 12 2022 Neal Gompa <ngompa@fedoraproject.org> - 3.2.61-1
- Update to 3.2.61

* Tue Nov 08 2022 Richard Shaw <hobbes1069@gmail.com> - 3.2.41.1-9
- Rebuild for yaml-cpp 0.7.0.

* Mon Aug 01 2022 Frantisek Zatloukal <fzatlouk@redhat.com> - 3.2.41.1-8
- Rebuilt for ICU 71.1

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.41.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jun 24 2022 Jonathan Wakely <jwakely@redhat.com> - 3.2.41.1-6
- Replace obsolete boost-python3-devel build dependency (#2100748)

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 3.2.41.1-5
- Rebuilt for Python 3.11

* Wed May 04 2022 Thomas Rodgers <trodgers@redhat.com> - 3.2.41.1-4
- Rebuilt for Boost 1.78

* Sat Mar 19 2022 Mattia Verga <mattia.verga@protonmail.com> - 3.2.41.1-3
- Rebuilt for kpmcore soname bump to 12

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.41.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sun Aug 22 2021 Neal Gompa <ngompa@fedoraproject.org> - 3.2.41.1-1
- Update to 3.2.41.1
- Enable building for AArch64

* Fri Aug 06 2021 Jonathan Wakely <jwakely@redhat.com> - 3.2.39-6
- Rebuilt for Boost 1.76

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.39-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 3.2.39-4
- Rebuilt for Python 3.10

* Wed May 19 2021 Pete Walter <pwalter@fedoraproject.org> - 3.2.39-3
- Rebuild for ICU 69

* Sun Apr 25 2021 Mattia Verga <mattia.verga@protonmail.com>  - 3.2.39-2
- Rebuilt for kpmcore 21.04.0

* Sat Mar 20 2021 Neal Gompa <ngompa13@gmail.com> - 3.2.39-1
- Update to 3.2.39
- Drop patches included in this release
- Refresh customization patches

* Sun Mar 14 2021 Neal Gompa <ngompa13@gmail.com> - 3.2.38-1
- Update to 3.2.38
- Backport improved Btrfs support
- Set Btrfs by default with the Fedora Btrfs layout

* Sat Mar 06 2021 Neal Gompa <ngompa13@gmail.com> - 3.2.37-1
- Update to 3.2.37
- Drop upstreamed patch to fix shim binary names

* Sat Jan 30 2021 Neal Gompa <ngompa13@gmail.com> - 3.2.35.1-1
- Rebase to 3.2.35.1
- Prepare for support for AArch64
- Add configuration for Fedora GeoIP endpoints
- Add patch to fix shim binary names
- Minor spec cleanups

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.11-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jan 22 2021 Jonathan Wakely <jwakely@redhat.com> - 3.2.11-15
- Rebuilt for Boost 1.75

* Sat Oct 17 2020 Mattia Verga <mattia.verga@protonmail.com>  - 3.2.11-14
- Rebuilt for kpmcore 4.2.0

* Sat Oct 17 2020 Mamoru TASAKA <mtasaka@fedoraproject.org>  - 3.2.11-13
- Workaround for FTBFS
  - Workaround for %%cmake_kf5 forcely undefining %%__cmake_in_source_build
  - Upstream patch for missing header include
  - Kill python bytecompile for now

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.11-12
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Adam Jackson <ajax@redhat.com> - 3.2.11-11
- Require setxkbmap not xorg-x11-xkb-utils

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.11-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jul 24 2020 Jeff Law <law@redhat.com> - 3.2.11-10
- Use __cmake_in_source_build

* Sat May 30 2020 Jonathan Wakely <jwakely@redhat.com> - 3.2.11-9
- Rebuilt for Boost 1.73

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 3.2.11-8
- Rebuilt for Python 3.9

* Mon Feb 10 2020 Mattia Verga <mattia.verga@protonmail.com> - 3.2.11-7
- Rebuilt for kpmcore 4.1.0

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.11-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Oct 18 2019 Richard Shaw <hobbes1069@gmail.com> - 3.2.11-5
- Rebuild for yaml-cpp 0.6.3.

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 3.2.11-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 3.2.11-3
- Rebuilt for Python 3.8

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jul 08 2019 Kevin Kofler <Kevin@tigcc.ticalc.org> - 3.2.11-1
- Update to 3.2.11 (fixes CVE-2019-13178)
- Rebase default-settings and kdesu patches
- default-settings patch: improve default branding (but auto is still better)
- Drop upstreamed shim-grub-cfg patch

* Sun May 12 2019 Kevin Kofler <Kevin@tigcc.ticalc.org> - 3.2.8-3
- bootloader: shim-grub-cfg patch: fix destination path for grub.cfg
- default-settings patch: fix warnings due to missing or unimplemented settings

* Sun May 12 2019 Kevin Kofler <Kevin@tigcc.ticalc.org> - 3.2.8-2
- bootloader: fix sb-shim mode to write grub.cfg into the EFI System Partition

* Fri May 10 2019 Kevin Kofler <Kevin@tigcc.ticalc.org> - 3.2.8-1
- Update to 3.2.8
- Rebase default-settings patch, disable GeoIP that is now enabled by default
- Drop upstreamed boost-python3, unpackfs-dev,
  dont-unmount-dev-mapper-live-base, and mount-selinux patches

* Wed May 08 2019 Kevin Kofler <Kevin@tigcc.ticalc.org> - 3.2.7-10
- mount: copy the SELinux context of the host directory to the mountpoint

* Wed May 08 2019 Kevin Kofler <Kevin@tigcc.ticalc.org> - 3.2.7-9
- Revert the change from "-8", this cannot be done with shellprocess

* Wed May 08 2019 Kevin Kofler <Kevin@tigcc.ticalc.org> - 3.2.7-8
- default-settings patch: enable the shellprocess module to create the mount
  point directories on the / partition with the correct SELinux contexts

* Mon May 06 2019 Kevin Kofler <Kevin@tigcc.ticalc.org> - 3.2.7-7
- default-settings patch: update the log path in umount.conf

* Mon May 06 2019 Kevin Kofler <Kevin@tigcc.ticalc.org> - 3.2.7-6
- Fix branding logos to use the correct form factor for each variant
- partition: do not unmount /dev/mapper/live-* (live-base needed in unpackfs)

* Sun May 05 2019 Kevin Kofler <Kevin@tigcc.ticalc.org> - 3.2.7-5
- Drop the grub2-efi*-modules dependencies, not needed with sb-shim support
- Add Requires: efibootmgr instead, used by the sb-shim support
- default-settings patch: disable the new libpwquality check by default

* Sun May 05 2019 Kevin Kofler <Kevin@tigcc.ticalc.org> - 3.2.7-4
- unpackfs: do not use -o loop if the source is a device (fails on F29+)

* Sun May 05 2019 Kevin Kofler <Kevin@tigcc.ticalc.org> - 3.2.7-3
- Add BuildRequires: parted-devel (used in welcome to check storage requirement)

* Sun May 05 2019 Kevin Kofler <Kevin@tigcc.ticalc.org> - 3.2.7-2
- Fix finding Boost::Python3 on F30+
- Only BuildRequire libatasmart-devel and libblkid-devel on F29-

* Sun May 05 2019 Kevin Kofler <Kevin@tigcc.ticalc.org> - 3.2.7-1
- Update to 3.2.7 and update BuildRequires and Requires
- Add plasmalnf subpackage for the new plasmalnf module requiring plasma-desktop
- Switch webview from QtWebEngine to QtWebKit to work around upstream issue 1051
- Rebase default-settings patch and update some settings:
  - enable INSTALL_CONFIG by default (we patch it in place, so install it)
  - disable plymouthcfg by default (now only needed to change the default theme)
  - bootloader.conf: enable sb-shim (UEFI "Secure Boot" support)
  - plasmalnf.conf (note: module disabled by default): fix default liveuser
  - plasmalnf.conf (note: module disabled by default): default: show all themes
  - tracking.conf (note: module disabled by default): default tracking to none
  - users.conf: default to honoring the default shell from /etc/default/useradd
  - welcome.conf: use https for internetCheckUrl (catches more captive portals)
- Rebase kdesu patch

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.8-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jan 24 2019 Jonathan Wakely <jwakely@redhat.com> - 3.1.8-12
- Rebuilt for Boost 1.69

* Mon Jan 14 2019 Björn Esser <besser82@fedoraproject.org> - 3.1.8-11
- Rebuilt for libcrypt.so.2 (#1666033)

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.8-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 3.1.8-9
- Rebuilt for Python 3.7

* Wed Feb 14 2018 Richard Shaw <hobbes1069@gmail.com> - 3.1.8-8
- Rebuild for yaml-cpp 0.6.0.

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 23 2018 Jonathan Wakely <jwakely@redhat.com> - 3.1.8-6
- Rebuilt for Boost 1.66

* Sat Jan 20 2018 Björn Esser <besser82@fedoraproject.org> - 3.1.8-5
- Rebuilt for switch to libxcrypt

* Sun Jan 07 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.1.8-4
- Remove obsolete scriptlets

* Tue Dec 26 2017 Mattia Verga <mattia.verga@email.it> - 3.1.8-3
- Rebuild for libkpmcore soname bump in rawhide

* Sun Dec 03 2017 Mattia Verga <mattia.verga@email.it> - 3.1.8-2
- Rebuild for libkpmcore soname bump in F27 and F26 branches

* Tue Nov 14 2017 Kevin Kofler <Kevin@tigcc.ticalc.org> - 3.1.8-1
- Update to 3.1.8 (bugfix release)
- Rebase default-settings patch
- Update fallback PRODUCTURL and SUPPORTURL

* Wed Oct 25 2017 Kevin Kofler <Kevin@tigcc.ticalc.org> - 3.1.7-1
- Update to 3.1.7

* Sun Oct 22 2017 Kevin Kofler <Kevin@tigcc.ticalc.org> - 3.1.6-2
- Update grub2-efi* package names for 32-bit UEFI support (F27+) (#1505151)

* Sat Oct 14 2017 Kevin Kofler <Kevin@tigcc.ticalc.org> - 3.1.6-1
- Update to 3.1.6

* Sun Oct 01 2017 Mattia Verga <mattia.verga@email.it> - 3.1.5-2
- Rebuild for libkpmcore soname bump

* Wed Sep 27 2017 Kevin Kofler <Kevin@tigcc.ticalc.org> - 3.1.5-1
- Update to 3.1.5
- Rebase default-settings and kdesu patches
- Drop "-DWITH_CRASHREPORTER:BOOL=OFF", upstream removed the crash reporter
- Install calamares-python.mo, delete unused calamares-dummypythonqt.mo

* Mon Aug 14 2017 Kevin Kofler <Kevin@tigcc.ticalc.org> - 3.1.1-1
- Update to 3.1.1
- Rebase default-settings patch
- Update auto branding to add welcomeStyleCalamares and sidebarTextHighlight
- Update minimum cmake and kpmcore versions
- Add manpage to the file list
- Disable crash reporter for now (as was the default in previous releases)

* Sun Aug 06 2017 Björn Esser <besser82@fedoraproject.org> - 3.1.0-6
- Rebuilt for AutoReq cmake-filesystem

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jul 20 2017 Kalev Lember <klember@redhat.com> - 3.1.0-3
- Rebuilt for Boost 1.64

* Sun Jun 04 2017 Mattia Verga <mattia.verga@tiscali.it> - 3.1.0-2
- Rebuild for libkpmcore soname bump

* Sun Mar 05 2017 Kevin Kofler <Kevin@tigcc.ticalc.org> - 3.1.0-1
- Update to 3.1.0
- Rebase default-settings patch
- default-settings: comment out unneeded and problematic "sudoersGroup: wheel"
- default-settings: change the new internetCheckUrl to the Fedora hotspot.txt

* Thu Feb 09 2017 Mattia Verga <mattia.verga@tiscali.it> - 3.0-2
- Rebuild for libboost_python3 soname bump

* Sat Jan 21 2017 Kevin Kofler <Kevin@tigcc.ticalc.org> - 3.0-1
- Update to 3.0 (stable release, now out of beta)

* Thu Jan 19 2017 Kevin Kofler <Kevin@tigcc.ticalc.org> - 3.0-0.1.beta2
- Update to 3.0-beta2 (upstream renamed 2.5 to 3.0)

* Thu Jan 19 2017 Kevin Kofler <Kevin@tigcc.ticalc.org> - 2.5-0.2.beta1
- Update to 2.5-beta1
- Rebase default-settings patch

* Sun Jan 15 2017 Kevin Kofler <Kevin@tigcc.ticalc.org> - 2.5-0.1.alpha1
- Update to 2.5-alpha1
- Rebase default-settings and kdesu patches

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 2.4.80-0.4.20161119git34516e9477b2f
- Rebuild for Python 3.6

* Sat Nov 19 2016 Kevin Kofler <Kevin@tigcc.ticalc.org> - 2.4.80-0.3.20161119git34516e9477b2f
- New snapshot from git master (34516e9477b2fd5e9b3e5823350d1efc2099573f)

* Sun Nov 13 2016 Peter Robinson <pbrobinson@fedoraproject.org> 2.4.80-0.2.20161113gitd6e0e09bc1472
- Drop PowerPC arches from ExclusiveArch as we don't support them as live arches

* Sun Nov 13 2016 Kevin Kofler <Kevin@tigcc.ticalc.org> - 2.4.80-0.1.20161113gitd6e0e09bc1472
- New snapshot from git master (d6e0e09bc1472009e2bdabd4186979dbf4c2303e)
- Drop upstreamed patches (UEFI fixes, Internet connection check)
- Rebase default-settings and kdesu patches
- BuildRequire kpmcore-devel >= 2.9.90

* Sun Nov 06 2016 Kevin Kofler <Kevin@tigcc.ticalc.org> - 2.4.4-4
- Fix UEFI firmware workaround for 32-bit UEFI (CAL-403, patch by TeHMoroS)
- Disable the Requires: grub2-efi grub2-efi-modules on 32-bit x86 again

* Sat Nov 05 2016 Kevin Kofler <Kevin@tigcc.ticalc.org> - 2.4.4-3
- Fix the check for available Internet connection on startup

* Sat Nov 05 2016 Kevin Kofler <Kevin@tigcc.ticalc.org> - 2.4.4-2
- Fix UEFI installation failure in the bootloader module (bad vfat_correct_case)

* Fri Nov 04 2016 Kevin Kofler <Kevin@tigcc.ticalc.org> - 2.4.4-1
- Update to 2.4.4 (bugfix release, should in particular fix UEFI on Fedora)
- Rebase default-settings patch for packages module changes
- Drop Requires: gdisk (sgdisk), no longer needed
- Enable Requires: grub2-efi also on 32-bit, should work too
- Requires: grub2-efi-modules for UEFI grub2-install until we get shim support

* Fri Oct 28 2016 Kevin Kofler <Kevin@tigcc.ticalc.org> - 2.4.3-1
- Update to 2.4.3 (LUKS FDE support backported upstream, bugfixes)
- Drop grubcfg-quoting, dracut-luks-fde backports, now in upstream 2.4.x (2.4.3)

* Thu Oct 20 2016 Kevin Kofler <Kevin@tigcc.ticalc.org> - 2.4.2-3
- grubcfg module: Fix mismatched quoting and escaping
- Update dracut-luks-fde backport with the grubcfg fixes for hostonly="no" mode

* Tue Oct 18 2016 Kevin Kofler <Kevin@tigcc.ticalc.org> - 2.4.2-2
- Add (backport from master) support for LUKS full disk encryption (with dracut)
- Adjust default-settings patch accordingly

* Fri Oct 14 2016 Kevin Kofler <Kevin@tigcc.ticalc.org> - 2.4.2-1
- Update to 2.4.2 (bugfix release)
- Drop upstreamed users-no-chfn and locale-utf8 patches
- Drop no-luks-fde patch, set enableLuksAutomatedPartitioning: false instead
- Don't write /etc/default/keyboard (set writeEtcDefaultKeyboard: false)

* Sun Oct 02 2016 Kevin Kofler <Kevin@tigcc.ticalc.org> - 2.4.1-3
- BuildRequire Qt >= 5.6, required by the locale and netinstall modules
- Use kdesu instead of pkexec (works around #1171779)
- Hide the LUKS full disk encryption checkbox which does not work on Fedora yet

* Sun Sep 25 2016 Kevin Kofler <Kevin@tigcc.ticalc.org> - 2.4.1-2
- locale module: Fix locale filtering for UTF-8 on Fedora

* Mon Sep 19 2016 Kevin Kofler <Kevin@tigcc.ticalc.org> - 2.4.1-1
- Update to 2.4.1
- Drop support for separate partitionmanager tarball, kpmcore is now an external
  dependency (BuildRequires)
- Update KF5 build requirements
- Update minimum Boost requirement, decreased from 1.55.0 to 1.54.0
- Explicitly BuildRequire gcc-c++ >= 4.9.0
- Drop support for yum (i.e., for Fedora < 22)
- Rebase default-settings patch
- default-settings: Use America/New_York as the default time zone (matches both
                    Anaconda and upstream Calamares, remixes can override it)
- Drop desktop-file patch, use the upstream .desktop file and (now fixed) icon
- Update file list and scriptlets for the icon, add Requires: hicolor-icon-theme
- Use QtWebEngine for the optional webview module by default
- users module: Drop dependency on chfn, which is no longer installed by default
- Add an -interactiveterminal subpackage, new module depending on konsole5-part

* Tue Aug 23 2016 Richard Shaw <hobbes1069@gmail.com> - 1.1.4.2-5
- Rebuild for updated yaml-cpp

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.4.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 18 2016 Jonathan Wakely <jwakely@redhat.com> - 1.1.4.2-3
- Rebuilt for Boost 1.60

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Sat Oct 31 2015 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1.1.4.2-1
- Update to 1.1.4.2
- Update URL tag and the calamares.io link in show.qml to use https

* Sat Sep 26 2015 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1.1.3-1
- Update to 1.1.3
- Add additional changes to calamares-default-settings.patch
- BuildRequires: qt5-qtwebkit-devel >= 5.3 for the webview module
- Add webview subpackage for the webview module (not used by default, extra dep)

* Thu Aug 27 2015 Jonathan Wakely <jwakely@redhat.com> - 1.1.2-2
- Rebuilt for Boost 1.59

* Mon Aug 17 2015 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1.1.2-1
- Update to 1.1.2 (#1246955)
- Add Requires: gdisk (for sgdisk), dmidecode, upower, NetworkManager
- Add slideshow translations (fr, de, it)
- Drop obsolete calamares-1.0.1-fix-version.patch
- Rebase calamares-default-settings.patch

* Wed Aug 05 2015 Jonathan Wakely <jwakely@redhat.com> 1.0.1-6.20150502gita70306e54f505
- Rebuilt for Boost 1.58

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-5.20150502gita70306e54f505
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun May 03 2015 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1.0.1-4.20150502gita70306e54f505
- New snapshot, fixes bugs, improves EFI support, UI and translations
- Drop fix-reboot patch, fixed upstream
- Update default-settings patch
- Update automatic branding generation scriptlet

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 1.0.1-3
- Rebuilt for GCC 5 C++11 ABI change

* Thu Feb 05 2015 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1.0.1-2
- Fix the version number reported in the About dialog (1.0.1, not 1.0.0)
- Apply upstream fix to make "Restart now" in "Finished" page actually reboot
- Make the link in the default show.qml clickable

* Mon Feb 02 2015 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1.0.1-1
- Update to the official release 1.0.1 (adds slideshow support, "Finished" page)
- Install a show.qml with a default, Calamares-branded slideshow
- BuildRequires:  qt5-qtdeclarative-devel >= 5.3 (needed for the new slideshow)

* Mon Jan 19 2015 Kevin Kofler <Kevin@tigcc.ticalc.org> - 0.17.0-8.20150119git5c6a302112cee
- New snapshot, fixes swap fstab entries and yum/dnf package removal

* Sun Jan 11 2015 Kevin Kofler <Kevin@tigcc.ticalc.org> - 0.17.0-7.20150105gitfe44633e0ca52
- Rebuild for new extra-cmake-modules (to verify that it still builds)

* Sat Jan 10 2015 Kevin Kofler <Kevin@tigcc.ticalc.org> - 0.17.0-6.20150105gitfe44633e0ca52
- New snapshot, improves the partitioning interface and updates translations
- Point URL to http://calamares.io/
- default-settings patch: Enable the packages module, make it remove calamares
- desktop-file patch: Remove the NoDisplay=true line, unneeded with the above
- Requires: dnf or yum depending on the Fedora version, for the packages module

* Sun Dec 07 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> - 0.17.0-5.20141206giteb748cca8ebfc
- Bump Release to distinguish official F21 update from Copr build

* Sun Dec 07 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> - 0.17.0-4.20141206giteb748cca8ebfc
- New snapshot, fixes detection and setup of display managers
- default-settings patch: Don't delist non-sddm DMs from displaymanager.conf
- Drop the Requires: sddm, no longer needed (now works with any DM or even none)

* Sat Dec 06 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> - 0.17.0-3.20141206git75adfa03fcba0
- New snapshot, fixes some bugs, adds partial/incomplete grub-efi support
- Add ExclusiveArch matching the livearches from anaconda.spec (#1171380)
- Requires: grub-efi on x86_64
- Rebase default-settings patch, set efiBootloaderId in grub.cfg

* Sat Nov 29 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> - 0.17.0-2.20141128giteee54241d1f58
- New snapshot, sets the machine-id, fixes mounting/unmounting bugs
- Rebase default-settings patch

* Thu Nov 27 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> - 0.17.0-1.20141127git8591dcf731cbf
- New snapshot, adds locale selector, fixes installation with SELinux enabled
- Use the version number from CMakeLists.txt, now at 0.17.0
- Use post-release snapshot numbering, milestone 0.17 was already reached

* Mon Nov 24 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> - 0-0.17.20141123gitc17898a6501fd
- New snapshot, adds "About" dialog and improves partitioning error reporting

* Thu Nov 20 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> - 0-0.16.20141119git01c3244396f35
- Automatically generate the branding to use by default (new "auto" branding)
- Remove README.branding, no longer needed

* Thu Nov 20 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> - 0-0.15.20141119git01c3244396f35
- New snapshot, creates /etc/default/grub if missing (calamares#128)
- README.branding: Mention new bootloaderEntryName setting
- Remove no longer needed workaround that wrote /etc/default/grub in %%post

* Tue Nov 18 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> - 0-0.14.20141117gitdf47842fc7a03
- New snapshot, makes Python modules get branding information from branding.desc
- README.branding: Update with the resulting simplified instructions

* Sat Nov 15 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> - 0-0.13.20141115git6b2ccfb442def
- New snapshot, adds retranslation support to more modules, fixes writing
  /etc/hosts, writes /etc/locale.conf (always LANG=en_US.UTF-8 for now)
- Drop grub2-tools (calamares#123) patch, names made configurable upstream
- Update default-settings patch to set the grub2 names and handle new modules
- Drop workaround recreating calamares/libcalamares.so symlink, fixed upstream
- Move desktop-file-validate call to %%check

* Tue Nov 11 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> - 0-0.12.20141111gitfaa77d7f5e656
- New snapshot, writes keyboard configuration files to the installed system
  (calamares#31), adds a language selector and dynamic retranslation support

* Fri Nov 07 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> - 0-0.11.20141107gitfd5d1935290d9
- New snapshot, fixes the calamares#132 fix again, fixes enabling translations

* Thu Nov 06 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> - 0-0.10.20141106git1df44eddba572
- New snapshot, fixes the calamares#132 fix, calamares#124 (colors in build.log)
- Drop pkexec policy rename from desktop-file patch, fixed upstream

* Wed Nov 05 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> - 0-0.9.20141104gitb9af5b7d544a7
- New snapshot, creates sddm.conf if missing (calamares#132), adds translations
- Use and customize the new upstream .desktop file
- Point URL to the new http://calamares.github.io/ page

* Tue Oct 28 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> - 0-0.8.20141028git10ca85338db00
- New snapshot, fixes FTBFS in Rawhide (Qt 5.4.0 beta) (calamares#125)

* Tue Oct 28 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> - 0-0.7.20141027git6a9c9cbaae0a9
- Add a README.branding documenting how to rebrand Calamares

* Mon Oct 27 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> - 0-0.6.20141027git6a9c9cbaae0a9
- New snapshot, device-source patch (calamares#127) upstreamed

* Thu Oct 23 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> - 0-0.5.20141020git89fe455163c62
- Disable startup notification, does not work properly with pkexec

* Wed Oct 22 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> - 0-0.4.20141020git89fe455163c62
- Add a .desktop file that live kickstarts can use to show a menu entry or icon

* Mon Oct 20 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> - 0-0.3.20141020git89fe455163c62
- New snapshot, fixes escape sequences in g++ diagnostics in the build.log
- Allow using devices as sources for unpackfs, fixes failure to install
- Write /etc/default/grub in %%post if missing, fixes another install failure
- Fix the path to grub.cfg, fixes another install failure
- Own /etc/calamares/branding/

* Mon Oct 20 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> - 0-0.2.20141017git8a623cc1181e9
- Pass -DWITH_PARTITIONMANAGER:BOOL="ON"
- Pass -DCMAKE_BUILD_TYPE:STRING="RelWithDebInfo"
- Remove unnecessary Requires: kf5-filesystem

* Mon Oct 20 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> - 0-0.1.20141017git8a623cc1181e9
- Initial package
