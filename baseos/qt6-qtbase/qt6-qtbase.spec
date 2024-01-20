# See http://bugzilla.redhat.com/223663
%global multilib_archs x86_64 %{ix86} %{?mips} ppc64 ppc s390x s390 sparc64 sparcv9
%global multilib_basearchs x86_64 %{?mips64} ppc64 s390x sparc64

%ifarch s390x ppc64le aarch64 armv7hl
%global no_sse2  1
%endif

%if 0%{?rhel} && 0%{?rhel} < 9
%ifarch %{ix86}
%global no_sse2  1
%endif
%endif

%global platform linux-g++

%if 0%{?use_clang}
%global platform linux-clang
%endif

%global qt_module qtbase

# use external qt_settings pkg
%if 0%{?fedora}
%global qt_settings 1
%endif

%global journald 1
BuildRequires: pkgconfig(libsystemd)

%global examples 1
## skip for now, until we're better at it --rex
#global tests 1

#global unstable 0
%global prerelease rc2

Name:    qt6-qtbase
Summary: Qt6 - QtBase components
Version: 6.6.0
Release: 9%{?dist}

License: LGPL-3.0-only OR GPL-3.0-only WITH Qt-GPL-exception-1.0
Url:     http://qt-project.org/
%global  majmin %(echo %{version} | cut -d. -f1-2)
%global  qt_version %(echo %{version} | cut -d~ -f1)

%if 0%{?unstable}
Source0: https://download.qt.io/development_releases/qt/%{majmin}/%{qt_version}/submodules/%{qt_module}-everywhere-src-%{qt_version}-%{prerelease}.tar.xz
%else
Source0: https://download.qt.io/official_releases/qt/%{majmin}/%{version}/submodules/%{qt_module}-everywhere-src-%{version}.tar.xz
%endif

# https://bugzilla.redhat.com/show_bug.cgi?id=1227295
Source1: qtlogging.ini

# header file to workaround multilib issue
# https://bugzilla.redhat.com/show_bug.cgi?id=1036956
Source5: qconfig-multilib.h

# xinitrc script to check for OpenGL 1 only drivers and automatically set
# QT_XCB_FORCE_SOFTWARE_OPENGL for them
Source6: 10-qt6-check-opengl2.sh

# macros
Source10: macros.qt6-qtbase

Patch1: qtbase-tell-the-truth-about-private-API.patch
Patch2: qtbase-CMake-Install-objects-files-into-ARCHDATADIR.patch

# upstreamable patches
# namespace QT_VERSION_CHECK to workaround major/minor being pre-defined (#1396755)
Patch50: qtbase-version-check.patch

# 1. Workaround moc/multilib issues
# https://bugzilla.redhat.com/show_bug.cgi?id=1290020
# https://bugreports.qt.io/browse/QTBUG-49972
# 2. Workaround sysmacros.h (pre)defining major/minor a breaking stuff
Patch51: qtbase-moc-macros.patch

# drop -O3 and make -O2 by default
Patch54: qtbase-cxxflag.patch

# fix for new mariadb
Patch56: qtbase-mysql.patch

# fix FTBFS against libglvnd-1.3.4+
Patch58: qtbase-libglvnd.patch

# fix FTBS against libxkbcommon 1.6.0
Patch59: qtbase-libxkbcommon-1.6.0.patch

# Bug 1954359 - Many emoji don't show up in Qt apps because qt does not handle 'emoji' font family
# FIXME: this change seems to completely break font rendering for some people
# Patch60: qtbase-cache-emoji-font.patch

%if 0%{?fedora} < 39
# Latest QGnomePlatform needs to be specified to be used
Patch100: qtbase-use-qgnomeplatform-as-default-platform-theme-on-gnome.patch
%endif

## upstream patches
Patch200: qtbase-a11y-fix-race-condition-on-atspi-startup-on-wayland.patch

## upstream patches
Patch201: workaround-kde-429408.patch

# Do not check any files in %%{_qt6_plugindir}/platformthemes/ for requires.
# Those themes are there for platform integration. If the required libraries are
# not there, the platform to integrate with isn't either. Then Qt will just
# silently ignore the plugin that fails to load. Thus, there is no need to let
# RPM drag in gtk3 as a dependency for the GTK+3 dialog support.
%global __requires_exclude_from ^%{_qt6_plugindir}/platformthemes/.*$
# filter plugin provides
%global __provides_exclude_from ^%{_qt6_plugindir}/.*\\.so$

%if 0%{?use_clang}
BuildRequires: clang >= 6.0.0
%else
BuildRequires: gcc-c++
%endif
BuildRequires: cmake
BuildRequires: ninja-build
BuildRequires: cups-devel
BuildRequires: desktop-file-utils
BuildRequires: findutils
BuildRequires: double-conversion-devel
%if 0%{?fedora} || 0%{?epel}
BuildRequires: libb2-devel
%else
Provides:      bundled(libb2)
%endif
BuildRequires: libjpeg-devel
BuildRequires: libmng-devel
BuildRequires: libtiff-devel
BuildRequires: libzstd-devel
BuildRequires: mtdev-devel
%if 0%{?fedora} || 0%{?epel}
BuildRequires: tslib-devel
%endif
BuildRequires: pkgconfig(alsa)
# required for -accessibility
BuildRequires: pkgconfig(atspi-2)
# http://bugzilla.redhat.com/1196359
%global dbus_linked 1
BuildRequires: pkgconfig(dbus-1)
BuildRequires: pkgconfig(libdrm)
BuildRequires: pkgconfig(fontconfig)
BuildRequires: pkgconfig(gl)
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(gtk+-3.0)
BuildRequires: pkgconfig(libproxy-1.0)
BuildRequires: pkgconfig(libsctp)
# xcb-sm
BuildRequires: pkgconfig(ice) pkgconfig(sm)
BuildRequires: pkgconfig(libpng)
BuildRequires: pkgconfig(libudev)
BuildRequires: openssl-devel
BuildRequires: pkgconfig(libpulse) pkgconfig(libpulse-mainloop-glib)
BuildRequires: pkgconfig(libinput)
BuildRequires: pkgconfig(xcb-xkb) >= 1.10
BuildRequires: pkgconfig(xcb-util)
BuildRequires: pkgconfig(xkbcommon) >= 0.4.1
BuildRequires: pkgconfig(xkbcommon-x11) >= 0.4.1
BuildRequires: pkgconfig(xkeyboard-config)
%global vulkan 1
BuildRequires: pkgconfig(vulkan)
%global egl 1
BuildRequires: mesa-libEGL-devel
BuildRequires: pkgconfig(egl)
BuildRequires: pkgconfig(gbm)
BuildRequires: pkgconfig(libglvnd)
BuildRequires: pkgconfig(x11)
# only needed for GLES2 and GLES3 builds
#BuildRequires: pkgconfig(glesv2)

%global sqlite 1
BuildRequires: pkgconfig(sqlite3) >= 3.7
BuildRequires: pkgconfig(harfbuzz) >= 0.9.42
BuildRequires: pkgconfig(icu-i18n)
BuildRequires: pkgconfig(libpcre2-16) >= 10.20
%global pcre 1
BuildRequires: pkgconfig(xcb-xkb)
BuildRequires: pkgconfig(xcb) pkgconfig(xcb-glx) pkgconfig(xcb-icccm) pkgconfig(xcb-image) pkgconfig(xcb-keysyms) pkgconfig(xcb-renderutil) pkgconfig(xcb-cursor)
BuildRequires: pkgconfig(zlib)
BuildRequires: perl
BuildRequires: perl-generators
# see patch68
BuildRequires: python3
BuildRequires: qt6-rpm-macros

%if 0%{?tests}
BuildRequires: dbus-x11
BuildRequires: mesa-dri-drivers
BuildRequires: time
BuildRequires: xorg-x11-server-Xvfb
%endif

Requires: %{name}-common = %{version}-%{release}

## Sql drivers
%if 0%{?fedora} || 0%{?epel}
%global ibase 1
%endif
	

%description
Qt is a software toolkit for developing applications.

This package contains base tools, like string, xml, and network
handling.

%package common
Summary: Common files for Qt6
Requires: %{name} = %{version}-%{release}
BuildArch: noarch
%description common
%{summary}.

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: %{name}-gui%{?_isa}
%if 0%{?egl}
Requires: libEGL-devel
%endif
Requires: pkgconfig(gl)
%if 0%{?vulkan}
Requires: pkgconfig(vulkan)
%endif
Requires: qt6-rpm-macros
%if 0%{?use_clang}
Requires: clang >= 3.7.0
%endif
%if 0%{?ibase}
Requires: %{name}-ibase%{?_isa} = %{version}-%{release}
%endif
Requires: %{name}-mysql%{?_isa} = %{version}-%{release}
Requires: %{name}-odbc%{?_isa} = %{version}-%{release}
Requires: %{name}-postgresql%{?_isa} = %{version}-%{release}
%description devel
%{summary}.

%package private-devel
Summary: Development files for %{name} private APIs
Requires: %{name}-devel%{?_isa} = %{version}-%{release}
# QtPrintSupport/private requires cups/ppd.h
Requires: cups-devel
%description private-devel
%{summary}.

%package examples
Summary: Programming examples for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}

%description examples
%{summary}.

%package static
Summary: Static library files for %{name}
Requires: %{name}-devel%{?_isa} = %{version}-%{release}
Requires: pkgconfig(fontconfig)
Requires: pkgconfig(glib-2.0)
Requires: pkgconfig(libinput)
Requires: pkgconfig(xkbcommon)
Requires: pkgconfig(zlib)

%description static
%{summary}.

%if 0%{?ibase}
%package ibase
Summary: IBase driver for Qt6's SQL classes
BuildRequires: firebird-devel
Requires: %{name}%{?_isa} = %{version}-%{release}
%description ibase
%{summary}.
%endif

%package mysql
Summary: MySQL driver for Qt6's SQL classes
%if 0%{?fedora} > 27 || 0%{?rhel} > 8
BuildRequires: mariadb-connector-c-devel
%else
BuildRequires: mysql-devel
%endif
Requires: %{name}%{?_isa} = %{version}-%{release}
%description mysql
%{summary}.

%package odbc
Summary: ODBC driver for Qt6's SQL classes
BuildRequires: unixODBC-devel
Requires: %{name}%{?_isa} = %{version}-%{release}
%description odbc
%{summary}.

%package postgresql
Summary: PostgreSQL driver for Qt6's SQL classes
BuildRequires: libpq-devel
Requires: %{name}%{?_isa} = %{version}-%{release}
%description postgresql
%{summary}.

# debating whether to do 1 subpkg per library or not -- rex
%package gui
Summary: Qt6 GUI-related libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
Recommends: mesa-dri-drivers%{?_isa}
Recommends: qt6-qtwayland%{?_isa}
# for Source6: 10-qt6-check-opengl2.sh:
# glxinfo
Requires: glx-utils
%description gui
Qt6 libraries used for drawing widgets and OpenGL items.


%prep
%autosetup -n %{qt_module}-everywhere-src-%{qt_version}%{?unstable:-%{prerelease}} -p1

# move some bundled libs to ensure they're not accidentally used
pushd src/3rdparty
mkdir UNUSED
mv harfbuzz-ng freetype libjpeg libpng sqlite zlib UNUSED/
popd

# builds failing mysteriously on f20
# ./configure: Permission denied
# check to ensure that can't happen -- rex
test -x configure || chmod +x configure


%build
# QT is known not to work properly with LTO at this point.  Some of the issues
# are being worked on upstream and disabling LTO should be re-evaluated as
# we update this change.  Until such time...
# Disable LTO
# https://bugzilla.redhat.com/1900527
%define _lto_cflags %{nil}

## FIXME/TODO:
# * for %%ix86, add sse2 enabled builds for Qt6Gui, Qt6Core, QtNetwork, see also:
#   http://anonscm.debian.org/cgit/pkg-kde/qt/qtbase.git/tree/debian/rules (234-249)

## adjust $RPM_OPT_FLAGS
# remove -fexceptions
RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed 's|-fexceptions||g'`
RPM_OPT_FLAGS="$RPM_OPT_FLAGS %{?qt6_arm_flag} %{?qt6_deprecated_flag} %{?qt6_null_flag}"

%if 0%{?use_clang}
RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed 's|-fno-delete-null-pointer-checks||g'`
%endif

export CFLAGS="$CFLAGS $RPM_OPT_FLAGS"
export CXXFLAGS="$CXXFLAGS $RPM_OPT_FLAGS"
export LDFLAGS="$LDFLAGS $RPM_LD_FLAGS"
export MAKEFLAGS="%{?_smp_mflags}"

%cmake_qt6 \
 -DQT_FEATURE_accessibility=ON \
 -DQT_FEATURE_fontconfig=ON \
 -DQT_FEATURE_glib=ON \
 -DQT_FEATURE_sse2=%{?no_sse2:OFF}%{!?no_sse2:ON} \
 -DQT_FEATURE_icu=ON \
 -DQT_FEATURE_enable_new_dtags=ON \
 -DQT_FEATURE_journald=%{?journald:ON}%{!?journald:OFF} \
 -DQT_FEATURE_openssl_linked=ON \
 -DQT_FEATURE_openssl_hash=ON \
 -DQT_FEATURE_libproxy=ON \
 -DQT_FEATURE_sctp=ON \
 -DQT_FEATURE_separate_debug_info=OFF \
 -DQT_FEATURE_reduce_relocations=OFF \
 -DQT_FEATURE_relocatable=OFF \
 -DQT_FEATURE_system_jpeg=ON \
 -DQT_FEATURE_system_png=ON \
 -DQT_FEATURE_system_zlib=ON \
 %{?ibase:-DQT_FEATURE_sql_ibase=ON} \
 -DQT_FEATURE_sql_odbc=ON \
 -DQT_FEATURE_sql_mysql=ON \
 -DQT_FEATURE_sql_psql=ON \
 -DQT_FEATURE_sql_sqlite=ON \
 -DQT_FEATURE_rpath=OFF \
 -DQT_FEATURE_zstd=ON \
 %{?dbus_linked:-DQT_FEATURE_dbus_linked=ON} \
 %{?pcre:-DQT_FEATURE_system_pcre2=ON} \
 %{?sqlite:-DQT_FEATURE_system_sqlite=ON} \
 -DBUILD_SHARED_LIBS=ON \
 -DQT_BUILD_EXAMPLES=%{?examples:ON}%{!?examples:OFF} \
 -DQT_BUILD_TESTS=%{?tests:ON}%{!?tests:OFF} \
 -DQT_QMAKE_TARGET_MKSPEC=%{platform}

# FIXME
#  -DQT_FEATURE_directfb=ON \

%cmake_build


%install
%cmake_install

install -m644 -p -D %{SOURCE1} %{buildroot}%{_qt6_datadir}/qtlogging.ini

# Qt6.pc
mkdir -p %{buildroot}%{_libdir}/pkgconfig
cat << EOF > %{buildroot}%{_libdir}/pkgconfig/Qt6.pc
prefix=%{_qt6_prefix}
archdatadir=%{_qt6_archdatadir}
bindir=%{_qt6_bindir}
datadir=%{_qt6_datadir}

docdir=%{_qt6_docdir}
examplesdir=%{_qt6_examplesdir}
headerdir=%{_qt6_headerdir}
importdir=%{_qt6_importdir}
libdir=%{_qt6_libdir}
libexecdir=%{_qt6_libexecdir}
moc=%{_qt6_libexecdir}/moc
plugindir=%{_qt6_plugindir}
qmake=%{_qt6_bindir}/qmake
settingsdir=%{_qt6_settingsdir}
sysconfdir=%{_qt6_sysconfdir}
translationdir=%{_qt6_translationdir}

Name: Qt6
Description: Qt6 Configuration
Version: 6.6.0
EOF

# rpm macros
install -p -m644 -D %{SOURCE10} \
  %{buildroot}%{_rpmmacrodir}/macros.qt6-qtbase
sed -i \
  -e "s|@@NAME@@|%{name}|g" \
  -e "s|@@EPOCH@@|%{?epoch}%{!?epoch:0}|g" \
  -e "s|@@VERSION@@|%{version}|g" \
  -e "s|@@EVR@@|%{?epoch:%{epoch:}}%{version}-%{release}|g" \
  %{buildroot}%{_rpmmacrodir}/macros.qt6-qtbase

# create/own dirs
mkdir -p %{buildroot}{%{_qt6_archdatadir}/mkspecs/modules,%{_qt6_importdir},%{_qt6_libexecdir},%{_qt6_plugindir}/{designer,iconengines,script,styles},%{_qt6_translationdir}}
mkdir -p %{buildroot}%{_sysconfdir}/xdg/QtProject

# hardlink files to {_bindir}, add -qt6 postfix to not conflict
mkdir %{buildroot}%{_bindir}
pushd %{buildroot}%{_qt6_bindir}
for i in * ; do
  case "${i}" in
    qdbuscpp2xml|qdbusxml2cpp|qtpaths)
      ln -v  ${i} %{buildroot}%{_bindir}/${i}-qt6
      ;;
    *)
      ln -v  ${i} %{buildroot}%{_bindir}/${i}
      ;;
  esac
done
popd


%ifarch %{multilib_archs}
# multilib: qconfig.h
  mv %{buildroot}%{_qt6_headerdir}/QtCore/qconfig.h %{buildroot}%{_qt6_headerdir}/QtCore/qconfig-%{__isa_bits}.h
  install -p -m644 -D %{SOURCE5} %{buildroot}%{_qt6_headerdir}/QtCore/qconfig.h
%endif


## .prl/.la file love
# nuke .prl reference(s) to %%buildroot, excessive (.la-like) libs
pushd %{buildroot}%{_qt6_libdir}
for prl_file in libQt6*.prl ; do
  sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" ${prl_file}
  if [ -f "$(basename ${prl_file} .prl).so" ]; then
    rm -fv "$(basename ${prl_file} .prl).la"
    sed -i -e "/^QMAKE_PRL_LIBS/d" ${prl_file}
  fi
done
popd

install -p -m755 -D %{SOURCE6} %{buildroot}%{_sysconfdir}/X11/xinit/xinitrc.d/10-qt6-check-opengl2.sh

# install privat headers for qtxcb
mkdir -p %{buildroot}%{_qt6_headerdir}/QtXcb
install -m 644 src/plugins/platforms/xcb/*.h %{buildroot}%{_qt6_headerdir}/QtXcb/

rm %{buildroot}/%{_qt6_libexecdir}/qt-cmake-private-install.cmake

# Use better location for some new scripts in qtbase-6.0.1
mv %{buildroot}/%{_qt6_libexecdir}/ensure_pro_file.cmake %{buildroot}/%{_qt6_libdir}/cmake/Qt6/ensure_pro_file.cmake

%check
# verify Qt6.pc
export PKG_CONFIG_PATH=%{buildroot}%{_libdir}/pkgconfig
test "$(pkg-config --modversion Qt6)" = "%{qt_version}"
%if 0%{?tests}
## see tests/README for expected environment (running a plasma session essentially)
## we are not quite there yet
export CTEST_OUTPUT_ON_FAILURE=1
export PATH=%{buildroot}%{_qt6_bindir}:$PATH
export LD_LIBRARY_PATH=%{buildroot}%{_qt6_libdir}
# dbus tests error out when building if session bus is not available
dbus-launch --exit-with-session \
%make_build sub-tests  -k ||:
xvfb-run -a --server-args="-screen 0 1280x1024x32" \
dbus-launch --exit-with-session \
time \
make check -k ||:
%endif

%ldconfig_scriptlets

%files
%license LICENSES/GPL*
%license LICENSES/LGPL*
%dir %{_sysconfdir}/xdg/QtProject/
%{_qt6_libdir}/libQt6Concurrent.so.6*
%{_qt6_libdir}/libQt6Core.so.6*
%{_qt6_libdir}/libQt6DBus.so.6*
%{_qt6_libdir}/libQt6Network.so.6*
%{_qt6_libdir}/libQt6Sql.so.6*
%{_qt6_libdir}/libQt6Test.so.6*
%{_qt6_libdir}/libQt6Xml.so.6*
%dir %{_qt6_docdir}/
%{_qt6_docdir}/global/
%{_qt6_docdir}/config/
%{_qt6_importdir}/
%{_qt6_translationdir}/
%if "%{_qt6_prefix}" != "%{_prefix}"
%dir %{_qt6_prefix}/
%endif
%dir %{_qt6_archdatadir}/
%dir %{_qt6_datadir}/
%{_qt6_datadir}/qtlogging.ini
%dir %{_qt6_libexecdir}/
%dir %{_qt6_plugindir}/
%dir %{_qt6_plugindir}/designer/
%dir %{_qt6_plugindir}/generic/
%dir %{_qt6_plugindir}/iconengines/
%dir %{_qt6_plugindir}/imageformats/
%dir %{_qt6_plugindir}/platforminputcontexts/
%dir %{_qt6_plugindir}/platforms/
%dir %{_qt6_plugindir}/platformthemes/
%dir %{_qt6_plugindir}/printsupport/
%dir %{_qt6_plugindir}/script/
%dir %{_qt6_plugindir}/sqldrivers/
%dir %{_qt6_plugindir}/styles/
%{_qt6_plugindir}/networkinformation/libqglib.so
%{_qt6_plugindir}/networkinformation/libqnetworkmanager.so
%{_qt6_plugindir}/sqldrivers/libqsqlite.so
%{_qt6_plugindir}/tls/libqcertonlybackend.so
%{_qt6_plugindir}/tls/libqopensslbackend.so

%files common
# mostly empty for now, consider: filesystem/dir ownership, licenses
%{_rpmmacrodir}/macros.qt6-qtbase

%files devel
%dir %{_qt6_libdir}/qt6/modules
%dir %{_qt6_libdir}/qt6/metatypes
%dir %{_qt6_libdir}/cmake/Qt6
%dir %{_qt6_libdir}/cmake/Qt6/platforms
%dir %{_qt6_libdir}/cmake/Qt6/platforms/Platform
%dir %{_qt6_libdir}/cmake/Qt6/config.tests
%dir %{_qt6_libdir}/cmake/Qt6/3rdparty/extra-cmake-modules
%dir %{_qt6_libdir}/cmake/Qt6/3rdparty/kwin
%dir %{_qt6_libdir}/cmake/Qt6BuildInternals
%dir %{_qt6_libdir}/cmake/Qt6BuildInternals/StandaloneTests
%dir %{_qt6_libdir}/cmake/Qt6Concurrent
%dir %{_qt6_libdir}/cmake/Qt6Core
%dir %{_qt6_libdir}/cmake/Qt6CoreTools
%dir %{_qt6_libdir}/cmake/Qt6DBus
%dir %{_qt6_libdir}/cmake/Qt6DBusTools
%dir %{_qt6_libdir}/cmake/Qt6DeviceDiscoverySupportPrivate
%dir %{_qt6_libdir}/cmake/Qt6EglFSDeviceIntegrationPrivate
%dir %{_qt6_libdir}/cmake/Qt6EglFsKmsGbmSupportPrivate
%dir %{_qt6_libdir}/cmake/Qt6EglFsKmsSupportPrivate
%dir %{_qt6_libdir}/cmake/Qt6ExampleIconsPrivate
%dir %{_qt6_libdir}/cmake/Qt6FbSupportPrivate
%dir %{_qt6_libdir}/cmake/Qt6Gui
%dir %{_qt6_libdir}/cmake/Qt6GuiTools
%dir %{_qt6_libdir}/cmake/Qt6HostInfo
%dir %{_qt6_libdir}/cmake/Qt6KmsSupportPrivate
%dir %{_qt6_libdir}/cmake/Qt6Network
%dir %{_qt6_libdir}/cmake/Qt6OpenGL
%dir %{_qt6_libdir}/cmake/Qt6OpenGLWidgets
%dir %{_qt6_libdir}/cmake/Qt6PrintSupport
%dir %{_qt6_libdir}/cmake/Qt6Sql
%dir %{_qt6_libdir}/cmake/Qt6Test
%dir %{_qt6_libdir}/cmake/Qt6Widgets
%dir %{_qt6_libdir}/cmake/Qt6WidgetsTools
%dir %{_qt6_libdir}/cmake/Qt6Xml
%if "%{_qt6_bindir}" != "%{_bindir}"
%dir %{_qt6_bindir}
%endif
%{_bindir}/androiddeployqt
%{_bindir}/androiddeployqt6
%{_bindir}/androidtestrunner
%{_bindir}/qdbuscpp2xml*
%{_bindir}/qdbusxml2cpp*
%{_bindir}/qmake*
%{_bindir}/qtpaths*
%{_bindir}/qt-cmake
%{_bindir}/qt-cmake-create
%{_bindir}/qt-configure-module
%{_libdir}/qt6/bin/qmake6
%{_qt6_bindir}/androiddeployqt
%{_qt6_bindir}/androiddeployqt6
%{_qt6_bindir}/androidtestrunner
%{_qt6_bindir}/qdbuscpp2xml
%{_qt6_bindir}/qdbusxml2cpp
%{_qt6_bindir}/qmake
%{_qt6_bindir}/qtpaths*
%{_qt6_bindir}/qt-cmake
%{_qt6_bindir}/qt-cmake-create
%{_qt6_bindir}/qt-configure-module
%{_qt6_libexecdir}/qt-cmake-private
%{_qt6_libexecdir}/qt-cmake-standalone-test
%{_qt6_libexecdir}/cmake_automoc_parser
%{_qt6_libexecdir}/qt-internal-configure-tests
%{_qt6_libexecdir}/sanitizer-testrunner.py
%{_qt6_libexecdir}/syncqt
%{_qt6_libexecdir}/android_emulator_launcher.sh
%{_qt6_libexecdir}/moc
%{_qt6_libexecdir}/tracegen
%{_qt6_libexecdir}/tracepointgen
%{_qt6_libexecdir}/qlalr
%{_qt6_libexecdir}/qvkgen
%{_qt6_libexecdir}/rcc
%{_qt6_libexecdir}/uic
%{_qt6_libexecdir}/qt-testrunner.py
%{_qt6_libdir}/qt6/modules/*.json
%if "%{_qt6_headerdir}" != "%{_includedir}"
%dir %{_qt6_headerdir}
%endif
%{_qt6_headerdir}/QtConcurrent/
%{_qt6_headerdir}/QtCore/
%{_qt6_headerdir}/QtDBus/
%{_qt6_headerdir}/QtInputSupport
%{_qt6_headerdir}/QtExampleIcons
%{_qt6_headerdir}/QtGui/
%{_qt6_headerdir}/QtNetwork/
%{_qt6_headerdir}/QtOpenGL/
%{_qt6_headerdir}/QtOpenGLWidgets
%{_qt6_headerdir}/QtPrintSupport/
%{_qt6_headerdir}/QtSql/
%{_qt6_headerdir}/QtTest/
%{_qt6_headerdir}/QtWidgets/
%{_qt6_headerdir}/QtXcb/
%{_qt6_headerdir}/QtXml/
%{_qt6_headerdir}/QtEglFSDeviceIntegration
%{_qt6_headerdir}/QtEglFsKmsGbmSupport
%{_qt6_headerdir}/QtEglFsKmsSupport
%{_qt6_mkspecsdir}/
%{_qt6_libdir}/libQt6Concurrent.prl
%{_qt6_libdir}/libQt6Concurrent.so
%{_qt6_libdir}/libQt6Core.prl
%{_qt6_libdir}/libQt6Core.so
%{_qt6_libdir}/libQt6DBus.prl
%{_qt6_libdir}/libQt6DBus.so
%{_qt6_libdir}/libQt6Gui.prl
%{_qt6_libdir}/libQt6Gui.so
%{_qt6_libdir}/libQt6Network.prl
%{_qt6_libdir}/libQt6Network.so
%{_qt6_libdir}/libQt6OpenGL.prl
%{_qt6_libdir}/libQt6OpenGL.so
%{_qt6_libdir}/libQt6OpenGLWidgets.prl
%{_qt6_libdir}/libQt6OpenGLWidgets.so
%{_qt6_libdir}/libQt6PrintSupport.prl
%{_qt6_libdir}/libQt6PrintSupport.so
%{_qt6_libdir}/libQt6Sql.prl
%{_qt6_libdir}/libQt6Sql.so
%{_qt6_libdir}/libQt6Test.prl
%{_qt6_libdir}/libQt6Test.so
%{_qt6_libdir}/libQt6Widgets.prl
%{_qt6_libdir}/libQt6Widgets.so
%{_qt6_libdir}/libQt6XcbQpa.prl
%{_qt6_libdir}/libQt6XcbQpa.so 
%{_qt6_libdir}/libQt6Xml.prl
%{_qt6_libdir}/libQt6Xml.so
%{_qt6_libdir}/libQt6EglFSDeviceIntegration.prl
%{_qt6_libdir}/libQt6EglFSDeviceIntegration.so
%{_qt6_libdir}/libQt6EglFsKmsGbmSupport.prl
%{_qt6_libdir}/libQt6EglFsKmsGbmSupport.so
%{_qt6_libdir}/cmake/Qt6/*.h.in
%{_qt6_libdir}/cmake/Qt6/*.cmake
%{_qt6_libdir}/cmake/Qt6/*.cmake.in
%{_qt6_libdir}/cmake/Qt6/PkgConfigLibrary.pc.in
%{_qt6_libdir}/cmake/Qt6/config.tests/*
%{_qt6_libdir}/cmake/Qt6/libexec/*
%{_qt6_libdir}/cmake/Qt6/platforms/*.cmake
%{_qt6_libdir}/cmake/Qt6/platforms/Platform/*.cmake
%{_qt6_libdir}/cmake/Qt6/qbatchedtestrunner.in.cpp
%{_qt6_libdir}/cmake/Qt6/ModuleDescription.json.in
%{_qt6_libdir}/cmake/Qt6/QtFileConfigure.txt.in
%{_qt6_libdir}/cmake/Qt6/QtConfigureTimeExecutableCMakeLists.txt.in
%{_qt6_libdir}/cmake/Qt6/QtSeparateDebugInfo.Info.plist.in
%{_qt6_libdir}/cmake/Qt6/3rdparty/extra-cmake-modules/COPYING-CMAKE-SCRIPTS
%{_qt6_libdir}/cmake/Qt6/3rdparty/extra-cmake-modules/find-modules/*.cmake
%{_qt6_libdir}/cmake/Qt6/3rdparty/extra-cmake-modules/modules/*.cmake
%{_qt6_libdir}/cmake/Qt6/3rdparty/extra-cmake-modules/qt_attribution.json
%{_qt6_libdir}/cmake/Qt6/3rdparty/kwin/COPYING-CMAKE-SCRIPTS
%{_qt6_libdir}/cmake/Qt6/3rdparty/kwin/*.cmake
%{_qt6_libdir}/cmake/Qt6/3rdparty/kwin/qt_attribution.json
%{_qt6_libdir}/cmake/Qt6BuildInternals/*.cmake
%{_qt6_libdir}/cmake/Qt6BuildInternals/QtStandaloneTestTemplateProject/CMakeLists.txt
%{_qt6_libdir}/cmake/Qt6BuildInternals/StandaloneTests/QtBaseTestsConfig.cmake
%{_qt6_libdir}/cmake/Qt6BuildInternals/QtStandaloneTestTemplateProject/Main.cmake
%{_qt6_libdir}/cmake/Qt6Concurrent/*.cmake
%{_qt6_libdir}/cmake/Qt6Core/*.cmake
%{_qt6_libdir}/cmake/Qt6Core/Qt6CoreConfigureFileTemplate.in
%{_qt6_libdir}/cmake/Qt6CoreTools/*.cmake
%{_qt6_libdir}/cmake/Qt6DBus/*.cmake
%{_qt6_libdir}/cmake/Qt6DBusTools/*.cmake
%{_qt6_libdir}/cmake/Qt6DeviceDiscoverySupportPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6EglFSDeviceIntegrationPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6EglFsKmsGbmSupportPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6EglFsKmsSupportPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6ExampleIconsPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6FbSupportPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6Gui/*.cmake
%{_qt6_libdir}/cmake/Qt6GuiTools/*.cmake
%{_qt6_libdir}/cmake/Qt6HostInfo/*.cmake
%{_qt6_libdir}/cmake/Qt6InputSupportPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6KmsSupportPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6Network/*.cmake
%{_qt6_libdir}/cmake/Qt6OpenGL/*.cmake
%{_qt6_libdir}/cmake/Qt6OpenGLWidgets/*.cmake
%{_qt6_libdir}/cmake/Qt6PrintSupport/*.cmake
%{_qt6_libdir}/cmake/Qt6Sql/Qt6Sql*.cmake
%{_qt6_libdir}/cmake/Qt6Sql/Qt6QSQLiteDriverPlugin*.cmake
%{_qt6_libdir}/cmake/Qt6Test/*.cmake
%{_qt6_libdir}/cmake/Qt6Widgets/*.cmake
%{_qt6_libdir}/cmake/Qt6WidgetsTools/*.cmake
%{_qt6_libdir}/cmake/Qt6XcbQpaPrivate/*.cmake
%{_qt6_libdir}/cmake/Qt6Xml/*.cmake
%{_qt6_libdir}/qt6/metatypes/*.json
%{_qt6_libdir}/qt6/objects-RelWithDebInfo/ExampleIconsPrivate_resources_1/.rcc/qrc_example_icons.cpp.o
%{_qt6_libdir}/pkgconfig/*.pc

%if 0%{?egl}
%{_qt6_libdir}/libQt6EglFsKmsSupport.prl
%{_qt6_libdir}/libQt6EglFsKmsSupport.so
%endif
## private-devel globs
%exclude %{_qt6_headerdir}/*/%{qt_version}/

%files private-devel
%{_qt6_headerdir}/*/%{qt_version}/

%files static
%{_qt6_headerdir}/QtDeviceDiscoverySupport
%{_qt6_libdir}/libQt6DeviceDiscoverySupport.*a
%{_qt6_libdir}/libQt6DeviceDiscoverySupport.prl
%{_qt6_libdir}/libQt6ExampleIcons.a
%{_qt6_libdir}/libQt6ExampleIcons.prl
%{_qt6_headerdir}/QtFbSupport
%{_qt6_libdir}/libQt6FbSupport.*a
%{_qt6_libdir}/libQt6FbSupport.prl
%{_qt6_libdir}/libQt6InputSupport.*a
%{_qt6_libdir}/libQt6InputSupport.prl
%{_qt6_headerdir}/QtKmsSupport
%{_qt6_libdir}/libQt6KmsSupport.*a
%{_qt6_libdir}/libQt6KmsSupport.prl
%if 0%{?examples}
%files examples
%{_qt6_examplesdir}/
%endif

%if 0%{?ibase}
%files ibase
%{_qt6_plugindir}/sqldrivers/libqsqlibase.so
%{_qt6_libdir}/cmake/Qt6Sql/Qt6QIBaseDriverPlugin*.cmake
%endif

%files mysql
%{_qt6_plugindir}/sqldrivers/libqsqlmysql.so
%{_qt6_libdir}/cmake/Qt6Sql/Qt6QMYSQLDriverPlugin*.cmake

%files odbc
%{_qt6_plugindir}/sqldrivers/libqsqlodbc.so
%{_qt6_libdir}/cmake/Qt6Sql/Qt6QODBCDriverPlugin*.cmake

%files postgresql
%{_qt6_plugindir}/sqldrivers/libqsqlpsql.so
%{_qt6_libdir}/cmake/Qt6Sql/Qt6QPSQLDriverPlugin*.cmake

%ldconfig_scriptlets gui

%files gui
%dir %{_sysconfdir}/X11/xinit
%dir %{_sysconfdir}/X11/xinit/xinitrc.d/
%{_sysconfdir}/X11/xinit/xinitrc.d/10-qt6-check-opengl2.sh
%{_qt6_libdir}/libQt6Gui.so.6*
%{_qt6_libdir}/libQt6OpenGL.so.6*
%{_qt6_libdir}/libQt6OpenGLWidgets.so.6*
%{_qt6_libdir}/libQt6PrintSupport.so.6*
%{_qt6_libdir}/libQt6Widgets.so.6*
%{_qt6_libdir}/libQt6XcbQpa.so.6*
# Generic
%{_qt6_plugindir}/generic/libqevdevkeyboardplugin.so
%{_qt6_plugindir}/generic/libqevdevmouseplugin.so
%{_qt6_plugindir}/generic/libqevdevtabletplugin.so
%{_qt6_plugindir}/generic/libqevdevtouchplugin.so
%{_qt6_plugindir}/generic/libqlibinputplugin.so
%if 0%{?fedora} || 0%{?epel}
%{_qt6_plugindir}/generic/libqtslibplugin.so
%endif
%{_qt6_plugindir}/generic/libqtuiotouchplugin.so
# Imageformats
%{_qt6_plugindir}/imageformats/libqico.so
%{_qt6_plugindir}/imageformats/libqjpeg.so
%{_qt6_plugindir}/imageformats/libqgif.so
# Platforminputcontexts
%{_qt6_plugindir}/platforminputcontexts/libcomposeplatforminputcontextplugin.so
%{_qt6_plugindir}/platforminputcontexts/libibusplatforminputcontextplugin.so
# EGL
%if 0%{?egl}
%{_qt6_libdir}/libQt6EglFSDeviceIntegration.so.6*
%{_qt6_libdir}/libQt6EglFsKmsSupport.so.6*
%{_qt6_libdir}/libQt6EglFsKmsGbmSupport.so.6*
%{_qt6_plugindir}/platforms/libqeglfs.so
%{_qt6_plugindir}/platforms/libqminimalegl.so
%dir %{_qt6_plugindir}/egldeviceintegrations/
%{_qt6_plugindir}/egldeviceintegrations/libqeglfs-kms-integration.so
%{_qt6_plugindir}/egldeviceintegrations/libqeglfs-x11-integration.so
%{_qt6_plugindir}/egldeviceintegrations/libqeglfs-kms-egldevice-integration.so
%{_qt6_plugindir}/egldeviceintegrations/libqeglfs-emu-integration.so
%{_qt6_plugindir}/xcbglintegrations/libqxcb-egl-integration.so
%endif
# Platforms
%{_qt6_plugindir}/platforms/libqlinuxfb.so
%{_qt6_plugindir}/platforms/libqminimal.so
%{_qt6_plugindir}/platforms/libqoffscreen.so
%{_qt6_plugindir}/platforms/libqxcb.so
%{_qt6_plugindir}/platforms/libqvnc.so
%{_qt6_plugindir}/platforms/libqvkkhrdisplay.so
%{_qt6_plugindir}/xcbglintegrations/libqxcb-glx-integration.so
# Platformthemes
%{_qt6_plugindir}/platformthemes/libqxdgdesktopportal.so
%{_qt6_plugindir}/platformthemes/libqgtk3.so
%{_qt6_plugindir}/printsupport/libcupsprintersupport.so


%changelog
* Thu Nov 09 2023 Jan Grulich <jgrulich@redhat.com> - 6.6.0-6
- Revert: Fix Qt not showing up emoji by handling emoji font family

* Tue Nov 07 2023 Jan Grulich <jgrulich@redhat.com> - 6.6.0-5
- Fix Qt not showing up emoji by handling emoji font family

* Mon Nov 06 2023 Jan Grulich <jgrulich@redhat.com> - 6.6.0-4
- Upstream backports
  - a11y - fix race condition on atspi startup on Wayland

* Mon Oct 23 2023 Jan Grulich <jgrulich@redhat.com> - 6.6.0-3
- Do not use tslib on RHEL builds

* Sun Oct 15 2023 Neal Gompa <ngompa@fedoraproject.org> - 6.6.0-2
- Add qtwayland weak dep to -gui subpackage and use arched weak deps

* Tue Oct 10 2023 Jan Grulich <jgrulich@redhat.com> - 6.6.0-1
- 6.6.0

* Sun Oct 01 2023 Justin Zobel <justin.zobel@gmail.com> - 6.5.3-1
- new version

* Sun Sep 03 2023 LuK1337 <priv.luk@gmail.com> - 6.5.2-5
- Unbreak CMake Qt6::ExampleIconsPrivate package

* Mon Aug 28 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 6.5.2-4
- Use bundled libb2 in RHEL builds

* Fri Aug 11 2023 Jan Grulich <jgrulich@redhat.com> - 6.5.2-3
- Don't use QGnomePlatform by default on F39+

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 6.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jul 21 2023 Jan Grulich <jgrulich@redhat.com> - 6.5.2-1
- 6.5.2

* Wed Jul 12 2023 František Zatloukal <fzatlouk@redhat.com> - 6.5.1-4
- Rebuilt for ICU 73.2

* Wed Jul 12 2023 Jan Grulich <jgrulich@redhat.com> - 6.5.1-3
- Bump build for private API version change

* Tue Jul 11 2023 František Zatloukal <fzatlouk@redhat.com> - 6.5.1-2
- Rebuilt for ICU 73.2

* Mon May 22 2023 Jan Grulich <jgrulich@redhat.com> - 6.5.1-1
- 6.5.1

* Fri Apr 7 2023 Marie Loise Nolden <loise@kde.org> - 6.5.0-2
- fix xcb plugin with new dependency xcb-cursor instead of Xcursor
  introduction with qt 6.5, add firebird sql plugin cleanly, clean up spec file
  
* Mon Apr 03 2023 Jan Grulich <jgrulich@redhat.com> - 6.5.0-1
- 6.5.0

* Mon Apr 03 2023 Jan Grulich <jgrulich@redhat.com> - 6.4.3-2
- Enable zstd support

* Thu Mar 23 2023 Jan Grulich <jgrulich@redhat.com> - 6.4.3-1
- 6.4.3

* Sun Mar 05 2023 Jan grulich <jgrulich@redhat.com> - 6.4.2-5
- Use QGnomePlatform as default platform theme on GNOME
  Resolves: bz#2174905

* Wed Feb 08 2023 Jan Grulich <jgrulich@redhat.com> - 6.4.2-4
- Fix possible DOS involving the Qt SQL ODBC driver plugin
  CVE-2023-24607

* Tue Jan 31 2023 Jan Grulich <jgrulich@redhat.com> - 6.4.2-3
- migrated to SPDX license

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 6.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Jan 16 2023 Jan Grulich <jgrulich@redhat.com> - 6.4.2-1
- 6.4.2

* Mon Jan 02 2023 Jan Grulich <jgrulich@redhat.com> - 6.4.1-4
- Make -devel package to require database plugins

* Sat Dec 31 2022 Pete Walter <pwalter@fedoraproject.org> - 6.4.1-3
- Rebuild for ICU 72

* Wed Nov 30 2022 Pavel Raiskup <praiskup@redhat.com> - 6.4.1-2
- rebuild for the new PostgreSQL 15

* Wed Nov 23 2022 Jan Grulich <jgrulich@redhat.com> - 6.4.1-1
- 6.4.1

* Mon Oct 31 2022 Jan Grulich <jgrulich@redhat.com> - 6.4.0-1
- 6.4.0

* Mon Aug 01 2022 Frantisek Zatloukal <fzatlouk@redhat.com> - 6.3.1-4
- Rebuilt for ICU 71.1

* Fri Jul 29 2022 Jan Grulich <jgrulich@redhat.com> - 6.3.1-3
- Fix moc location in pkgconfig file
  Resolves: bz#2112029

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 6.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jul 13 2022 Jan Grulich <jgrulich@redhat.com> - 6.3.1-1
- 6.3.1

* Wed Apr 13 2022 Jan Grulich <jgrulich@redhat.com> - 6.3.0-1
- 6.3.0

* Fri Feb 25 2022 Jan Grulich <jgrulich@redhat.com> - 6.2.3-2
- Enable s390x builds

* Mon Jan 31 2022 Jan Grulich <jgrulich@redhat.com> - 6.2.3-1
- 6.2.3

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 6.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jan 06 2022 Filip Januš <fjanus@redhat.com> - 6.2.2-2
- Rebuild for Postgresql 14

* Tue Dec 14 2021 Jan Grulich <jgrulich@redhat.com> - 6.2.2-1
- 6.2.2

* Fri Oct 29 2021 Jan Grulich <jgrulich@redhat.com> - 6.2.1-1
- 6.2.1

* Thu Sep 30 2021 Jan Grulich <jgrulich@redhat.com> - 6.2.0-1
- 6.2.0

* Mon Sep 27 2021 Jan Grulich <jgrulich@redhat.com> - 6.2.0~rc2-1
- 6.2.0 - rc2

* Sat Sep 18 2021 Jan Grulich <jgrulich@redhat.com> - 6.2.0~rc-1
- 6.2.0 - rc

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 6.2.0~beta4-3
- Rebuilt with OpenSSL 3.0.0

* Mon Sep 13 2021 Jan Grulich <jgrulich@redhat.com> - 6.2.0~beta4-2
- Skip s390x for qtdeclarative issue

* Fri Sep 10 2021 Jan Grulich <jgrulich@redhat.com> - 6.2.0~beta4-1
- 6.2.0 - beta4

* Wed Sep 08 2021 Rex Dieter <rdieter@fedoraproject.org> - 6.2.0~beta3-4
- rebuild

* Tue Sep 07 2021 Jan Grulich <jgrulich@redhat.com> - 6.2.0~beta3-3
- Disable rpath
  Resolves: bz#1982699

* Tue Aug 31 2021 Jan Grulich <jgrulich@redhat.com> - 6.2.0~beta3-2
- Fix file conflict with qt5-qttools
- Rebuild against older libglvnd

* Mon Aug 30 2021 Jan Grulich <jgrulich@redhat.com> - 6.2.0~beta3-1
- 6.2.0 - beta3

* Thu Aug 12 2021 Jan Grulich <jgrulich@redhat.com> - 6.1.2-1
- 6.1.2

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 6.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jun 07 2021 Jan Grulich <jgrulich@redhat.com> - 6.1.1-1
- 6.1.1

* Mon May 24 2021 Jan Grulich <jgrulich@redhat.com> - 6.1.0-3
- Rebuild with correct libexecdir path

* Thu May 20 2021 Pete Walter <pwalter@fedoraproject.org> - 6.1.0-2
- Rebuild for ICU 69

* Thu May 06 2021 Jan Grulich <jgrulich@redhat.com> - 6.1.0-1
- 6.1.0

* Mon Apr 05 2021 Jan Grulich <jgrulich@redhat.com> - 6.0.3-1
- 6.0.3

* Thu Feb 04 2021 Jan Grulich <jgrulich@redhat.com> - 6.0.1-1
- 6.0.1

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jan 06 2021 Jan Grulich <jgrulich@redhat.com> - 6.0.0-1
- 6.0.0
