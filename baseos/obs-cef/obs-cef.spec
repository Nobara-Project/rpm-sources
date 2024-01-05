## START: Set by rpmautospec
## (rpmautospec version 0.3.5)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 2;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

%define _lto_cflags %{nil}

# set default numjobs for the koji build
%ifarch aarch64
%global numjobs 8
%else
%global numjobs %{_smp_build_ncpus}
%endif

# enable|disable all cpus for the build.
%global use_all_cpus 1

%if %{use_all_cpus}
%global numjobs %{_smp_build_ncpus}
%endif

# official builds have less debugging and go faster... but we have to shut some things off.
%global official_build 1

# Fancy build status, so we at least know, where we are..
# %1 where
# %2 what
%global build_target() \
	export NINJA_STATUS="[%2:%f/%t] " ; \
	ninja -j %{numjobs} -C '%1' -vvv '%2'

# This was faster when it worked, but it didn't always.
# As of chromium 80, it is no longer supported. RIP.
%global use_jumbo 0

%global chromium_pybin %{__python3}

# We'd like to always have this on...
%global use_vaapi 1
# ... but EL9 doesn't ship libva-devel on aarch64?
%if 0%{?rhel} == 9
 %ifarch aarch64
 %global use_vaapi 0
 %endif
%endif

# Seems like we might need this sometimes
# Practically, no. But it's here in case we do.
%global use_gold 0

%ifarch aarch64
%global chromium_arch arm64
%endif
%ifarch x86_64
%global chromium_arch x64
%endif

%global builddir out/Release_GN_%{chromium_arch}

# Debuginfo packages aren't very useful here. If you need to debug
# you should do a proper debug build (not implemented in this spec yet)
%global debug_package %{nil}

%global chromium_path %{_libdir}/obs-cef

# We always filter provides. We only filter Requires when building shared.
%global __provides_exclude_from ^(%{chromium_path}/.*\\.so|%{chromium_path}/.*\\.so.*|%{chromium_path}/lib/.*\\.so|%{chromium_path}/lib/.*\\.so.*)$

# AddressSanitizer mode
# https://www.chromium.org/developers/testing/addresssanitizer
%global asan 0

# Chromium's fork of ICU is now something we can't unbundle.
# This is left here to ease the change if that ever switches.
%global bundleicu 1

%global bundlere2 1

# The libxml_utils code depends on the specific bundled libxml checkout
# which is not compatible with the current code in the Fedora package as of
# 2017-06-08.
%global bundlelibxml 1

# Fedora's Python 2 stack is being removed, we use the bundled Python libraries
# This can be revisited once we upgrade to Python 3
%global bundlepylibs 0

# RHEL 7.9 dropped minizip.
# It exists everywhere else though.
%global bundleminizip 0

# Chromium used to break on wayland, hidpi, and colors with gtk3 enabled.
# Hopefully it does not anymore.
%global gtk3 1

# Chromium really wants to use its bundled harfbuzz. Sigh.
%if 0%{?fedora} > 37
%global bundleharfbuzz 0
%else
%global bundleharfbuzz 1
%endif
%global bundleopus 1
%global bundlelibusbx 0
%global bundlelibwebp 0
%global bundlelibpng 0
%global bundlelibjpeg 0
# Needs FT_ClipBox which was implemented after 2.11.0. Should be able to set this back to 0 later.
%if 0%{?fedora}
%global bundlefreetype 0
%else
%global bundlefreetype 1
%endif
%global bundlelibdrm 0
%global bundlefontconfig 0

%global cef_version 5060
%global majorversion 103
%global chromium_version %{majorversion}.0.5060.134
%global git_date 20231010
%global cef_commit 17f8588498e2be97e667a5ae3ed70cb691a5df52
%global cef_branch 5060-shared-textures
%global cef_commit_number 2594
%global shortcommit %(c=%{cef_commit}; echo ${c:0:7})

Name:	obs-cef
Version: %{cef_version}^cr%{chromium_version}~git%{git_date}.%{shortcommit}
Release: %autorelease
Summary: OBS fork of the Chromium Embedded Framework
Url: https://github.com/obsproject/cef
License: BSD-3-Clause AND LGPL-2.1-or-later AND Apache-2.0 AND IJG AND MIT AND GPL-2.0-or-later AND ISC AND OpenSSL AND (MPL-1.1 OR GPL-2.0-only OR LGPL-2.0-only)

### Chromium Fedora Patches ###
Patch0:		chromium-70.0.3538.67-sandbox-pie.patch
# Use /etc/chromium for initial_prefs
Patch1:		chromium-91.0.4472.77-initial_prefs-etc-path.patch
# Use gn system files
Patch2:		chromium-67.0.3396.62-gn-system.patch
# Do not prefix libpng functions
Patch3:		chromium-60.0.3112.78-no-libpng-prefix.patch
# Do not mangle libjpeg
Patch4:		chromium-60.0.3112.78-jpeg-nomangle.patch
# Do not mangle zlib
Patch5:		chromium-77.0.3865.75-no-zlib-mangle.patch
# Do not use unrar code, it is non-free
Patch6:		chromium-95.0.4638.69-norar.patch
# Use Gentoo's Widevine hack
# https://gitweb.gentoo.org/repo/gentoo.git/tree/www-client/chromium/files/chromium-widevine-r3.patch
Patch7:		chromium-71.0.3578.98-widevine-r3.patch
# Try to load widevine from other places
Patch10:	chromium-100.0.4896.60-widevine-other-locations.patch
# Add "Fedora" to the user agent string
Patch12:	chromium-101.0.4951.41-fedora-user-agent.patch

# Needs to be submitted..
Patch51:	chromium-96.0.4664.45-gcc-remoting-constexpr.patch
# https://gitweb.gentoo.org/repo/gentoo.git/tree/www-client/chromium/files/chromium-unbundle-zlib.patch
Patch52:	chromium-81.0.4044.92-unbundle-zlib.patch
# https://github.com/stha09/chromium-patches/blob/master/chromium-78-protobuf-RepeatedPtrField-export.patch
Patch55:	chromium-78-protobuf-RepeatedPtrField-export.patch
# ../../third_party/perfetto/include/perfetto/base/task_runner.h:48:55: error: 'uint32_t' has not been declared
Patch56:	chromium-96.0.4664.45-missing-cstdint-header.patch
# Missing <cstring> (thanks c++17)
Patch57:	chromium-96.0.4664.45-missing-cstring.patch
# prepare for using system ffmpeg (clean)
# http://svnweb.mageia.org/packages/cauldron/chromium-browser-stable/current/SOURCES/chromium-53-ffmpeg-no-deprecation-errors.patch?view=markup
Patch58:	chromium-53-ffmpeg-no-deprecation-errors.patch
# https://github.com/stha09/chromium-patches/blob/master/chromium-103-VirtualCursor-std-layout.patch
Patch59:	chromium-103-VirtualCursor-std-layout.patch
# https://github.com/stha09/chromium-patches/blob/master/chromium-103-SubstringSetMatcher-packed.patch
Patch60:	chromium-103-SubstringSetMatcher-packed.patch
# https://github.com/stha09/chromium-patches/blob/master/chromium-103-FrameLoadRequest-type.patch
Patch61:	chromium-103-FrameLoadRequest-type.patch

# https://github.com/v8/v8/commit/2ed27bba6a881a152887f3ab1008e989fce617e3
Patch63:	chromium-102.0.5005.115-v8-aarch64-gcc-cfi-fix.patch
# Extra CXXFLAGS for aarch64
Patch64:	chromium-91.0.4472.77-aarch64-cxxflags-addition.patch
# Fix issue where closure_compiler thinks java is only allowed in android builds
# https://bugs.chromium.org/p/chromium/issues/detail?id=1192875
Patch65:	chromium-91.0.4472.77-java-only-allowed-in-android-builds.patch

# Python3.9 or later no longer support the 'U' mode
Patch66:	chromium-103.0.5060.53-python3-do-not-use-deprecated-mode-U.patch

# Fix missing cstring in remoting code
Patch67:	chromium-98.0.4758.80-remoting-cstring.patch

# Update rjsmin to 1.2.0
Patch69:	chromium-103.0.5060.53-update-rjsmin-to-1.2.0.patch

# Update six to 1.16.0
Patch70:	chromium-103.0.5060.53-python-six-1.16.0.patch

# Do not download proprietary widevine module in the background (thanks Debian)
Patch79:	chromium-99.0.4844.51-widevine-no-download.patch

# Fix crashes with components/cast_*
# Thanks to Gentoo
Patch80:	chromium-98.0.4758.80-EnumTable-crash.patch
# Fix build issues with gcc12
Patch81:	chromium-98.0.4758.102-gcc-12-subzero-fix.patch
# Disable tests on remoting build
Patch82:	chromium-98.0.4758.102-remoting-no-tests.patch


# Add missing cmath header
Patch84:	chromium-94.0.4606.71-remoting-missing-cmath-header.patch

# Clean up clang-format for python3
# thanks to Jon Nettleton
Patch86:	chromium-94.0.4606.81-clang-format.patch

# Markdownsafe 2.0.1 removed soft_unicode (replaced with soft_str)
# This is only in Fedora 37+
Patch87:	chromium-99.0.4844.84-markdownsafe-soft_str.patch

# AddressTracker is broken on non-4k pagesize systems
Patch88:	chromium-103-addresstracker-pagesize.patch

# Fix extra qualification error
Patch97:	chromium-103.0.5060.53-remoting-extra-qualification.patch
# From gentoo
Patch98:	chromium-94.0.4606.71-InkDropHost-crash.patch
# Enable WebRTCPPipeWireCapturer by default
Patch99:	chromium-96.0.4664.110-enable-WebRTCPipeWireCapturer-byDefault.patch
# Add include <utility> for std::exchange
Patch100:	chromium-100.0.4896.60-missing-utility-for-std-exchange.patch

# system ffmpeg
# need for old ffmpeg 5.x on epel9 and fedora 37
Patch114: chromium-107-ffmpeg-5.x-duration.patch
# disable the check
Patch115: chromium-103-proprietary-codecs.patch

# VAAPI
# Upstream turned VAAPI on in Linux in 86
Patch202:	chromium-102.0.5005.61-enable-hardware-accelerated-mjpeg.patch
Patch205:	chromium-86.0.4240.75-fix-vaapi-on-intel.patch

# Apply these patches to work around EPEL8 issues
Patch300:	chromium-99.0.4844.51-rhel8-force-disable-use_gnome_keyring.patch

# And fixes for new compilers
Patch400:       chromium-gcc11.patch

# Thanks Arch Linux for all of these
Patch401:	more-fixes-for-gcc13.patch
Patch402:	iwyu-add-stdint.h-for-various-int-types-in-base.patch
Patch403:	iwyu-add-stdint.h-for-uint64_t-in-EncounteredSurface.patch
Patch404:	iwyu-add-stdint.h-for-uint32_t-in-chrome_pdf.patch
Patch405:	iwyu-add-stdint.h-for-uint32_t-in-cc.patch
Patch406:	iwyu-add-stdint.h-for-int-types-in-gpu_feature_info.patch
Patch407:	iwyu-add-stdint.h-for-integer-types-in-ui.patch
Patch408:	swiftshader-add-cstdint-for-uint64_t.patch
Patch409:	random-fixes-for-gcc13.patch
Patch410:	pdfium-iwyu-add-stdint.h-for-uint32_t.patch
Patch411:	openscreen-iwyu-add-stdint.h.patch
Patch412:	iwyu-add-stdint.h-for-various-int-types-in-comp.patch
Patch413:	iwyu-add-stdint.h-for-various-integer-types-in-net.patch
Patch414:	iwyu-add-cstdint-for-uintptr_t-in-device.patch
Patch415:	iwyu-add-cstdint-for-int-types-in-s2cellid.patch
Patch416:	dawn-tint-add-cstdint.patch
Patch417:	add-missing-includes-causing-build-errors.patch

Patch418:	angle-gcc13.patch
Patch419:	chromium-gcc13.patch

Patch450:	protobuf-py312.patch

# CEF fixes
Patch500:	cef-no-sysroot.patch
Patch501:	cef-gcc13-patch-conflict.patch
# Fixes free() crashes in Skia, probably CEF related?
Patch502:	skia-use-malloc.patch

# Wayland embedded browser fixes
# https://github.com/obsproject/obs-browser/issues/279
# https://github.com/chromiumembedded/cef/issues/2804
# https://bitbucket.org/chromiumembedded/cef/pull-requests/288/wip-add-better-ozone-wayland-x11-support/
#Patch600:	0001.patch
#Patch601:	0002.patch
#Patch602:	0003.patch

# Use chromium-latest.py to generate clean tarball from released build tarballs, found here:
# http://build.chromium.org/buildbot/official/
# For Chromium Fedora use chromium-latest.py --stable --ffmpegclean --ffmpegarm
# If you want to include the ffmpeg arm sources append the --ffmpegarm switch
# https://commondatastorage.googleapis.com/chromium-browser-official/chromium-%%{version}.tar.xz
Source0:	chromium-%{chromium_version}-clean.tar.xz
# Also, only used if you want to reproduce the clean tarball.
Source5:	clean_ffmpeg.sh
Source6:	chromium-latest.py
Source7:	get_free_ffmpeg_source_files.py
# Bring xcb-proto with us (might need more than python on EPEL?)
Source20:	https://www.x.org/releases/individual/proto/xcb-proto-1.14.tar.xz

Source22: https://github.com/obsproject/cef/archive/%{cef_commit}.tar.gz
Source23: mock_git_util.py

# We can assume gcc and binutils.
BuildRequires:	gcc-c++

BuildRequires:	alsa-lib-devel
BuildRequires:	atk-devel
BuildRequires:	bison
BuildRequires:	cups-devel
BuildRequires:	dbus-devel
BuildRequires:	desktop-file-utils
BuildRequires:	expat-devel
BuildRequires:	flex
BuildRequires:	fontconfig-devel
BuildRequires:	glib2-devel
BuildRequires:	glibc-devel
BuildRequires:	gperf
%if 0%{?bundleharfbuzz}
#nothing
%else
BuildRequires:	harfbuzz-devel >= 2.4.0
%endif
BuildRequires:	libatomic
BuildRequires:	libcap-devel
BuildRequires:	libcurl-devel
%if 0%{?bundlelibdrm}
#nothing
%else
BuildRequires:	libdrm-devel
%endif
BuildRequires:	libgcrypt-devel
BuildRequires:	libudev-devel
BuildRequires:	libuuid-devel
%if 0%{?fedora} >= 37
BuildRequires:	libusb-compat-0.1-devel
%else
BuildRequires:	libusb-devel
%endif
BuildRequires:	libutempter-devel
BuildRequires:	libXdamage-devel
BuildRequires:	libXtst-devel
BuildRequires:	xcb-proto
BuildRequires:	mesa-libgbm-devel
BuildRequires:	minizip-compat-devel
BuildRequires:	nodejs

BuildRequires:	gn

BuildRequires: pkgconfig(libavcodec)
BuildRequires: pkgconfig(libavfilter)
BuildRequires: pkgconfig(libavformat)
BuildRequires: pkgconfig(libavutil)
# chromium fail to start for rpmfusion users due to ABI break in ffmpeg-free-6.0.1
# bethween fedora and rpmfusion.
%if 0%{?rhel} == 9 || 0%{?fedora} == 37
Conflicts: libavformat-free%{_isa} < 5.1.4
Conflicts: ffmpeg-libs%{_isa} < 5.1.4
%else
Conflicts: libavformat-free%{_isa} < 6.0.1
Conflicts: ffmpeg-libs%{_isa} < 6.0.1-2
%endif

BuildRequires:	nss-devel >= 3.26
BuildRequires:	pciutils-devel
BuildRequires:	pulseaudio-libs-devel

# For screen sharing on Wayland, currently Fedora only thing - no epel
%if 0%{?fedora}
BuildRequires:	pkgconfig(libpipewire-0.3)
%endif

# for /usr/bin/appstream-util
BuildRequires: libappstream-glib

# Fedora tries to use system libs whenever it can.
BuildRequires:	bzip2-devel
BuildRequires:	dbus-glib-devel
# For eu-strip
BuildRequires:	elfutils
BuildRequires:	elfutils-libelf-devel
BuildRequires:	flac-devel
%if 0%{?bundlefreetype}
# nothing
%else
BuildRequires:	freetype-devel
%endif
# One of the python scripts invokes git to look for a hash. So helpful.
BuildRequires:	/usr/bin/git
BuildRequires:	hwdata
BuildRequires:	kernel-headers
BuildRequires:	libevent-devel
BuildRequires:	libffi-devel
%if 0%{?bundleicu}
# If this is true, we're using the bundled icu.
# We'd like to use the system icu every time, but we cannot always do that.
%else
# Not newer than 54 (at least not right now)
BuildRequires:	libicu-devel = 54.1
%endif
%if 0%{?bundlelibjpeg}
# If this is true, we're using the bundled libjpeg
# which we need to do because the RHEL 7 libjpeg doesn't work for chromium anymore
%else
BuildRequires:	libjpeg-devel
%endif
%if 0%{?bundlelibpng}
# If this is true, we're using the bundled libpng
# which we need to do because the RHEL 7 libpng doesn't work right anymore
%else
BuildRequires:	libpng-devel
%endif
%if 0
# see https://code.google.com/p/chromium/issues/detail?id=501318
BuildRequires:	libsrtp-devel >= 1.4.4
%endif
BuildRequires:	libudev-devel
%if %{bundlelibusbx}
# Do nothing
%else
Requires:	libusbx >= 1.0.21-0.1.git448584a
BuildRequires:	libusbx-devel >= 1.0.21-0.1.git448584a
%endif
%if 0%{use_vaapi}
BuildRequires:	libva-devel
%endif
# We don't use libvpx anymore because Chromium loves to
# use bleeding edge revisions here that break other things
# ... so we just use the bundled libvpx.
%if %{bundlelibwebp}
# Do nothing
%else
BuildRequires:	libwebp-devel
%endif
BuildRequires:	libxslt-devel
BuildRequires:	libxshmfence-devel
# Same here, it seems.
# BuildRequires:	libyuv-devel
BuildRequires:	mesa-libGL-devel
%if %{bundleopus}
# Do nothing
%else
BuildRequires:	opus-devel
%endif
BuildRequires:	perl(Switch)
%if 0%{gtk3}
BuildRequires:	pkgconfig(gtk+-3.0)
%else
BuildRequires:	pkgconfig(gtk+-2.0)
%endif
BuildRequires:	%{chromium_pybin}
BuildRequires:  python3-devel

%if 0%{?bundlepylibs}
# Using bundled bits, do nothing.
%else
BuildRequires:	python3-beautifulsoup4
# BuildRequires:	python2-beautifulsoup
BuildRequires:	python3-html5lib
BuildRequires:	python3-markupsafe
BuildRequires:	python3-ply
BuildRequires:	python3-simplejson
%endif

%if 0%{?bundlere2}
# Using bundled bits, do nothing.
%else
Requires:	re2 >= 20160401
BuildRequires:	re2-devel >= 20160401
%endif
BuildRequires:	speech-dispatcher-devel
BuildRequires:	yasm
BuildRequires:	zlib-devel
# Technically, this logic probably applies to older rhel too... but whatever.
# RHEL 8 and 9 do not have gnome-keyring. Not sure why, but whatever again.
%if 0%{?fedora}
BuildRequires:	pkgconfig(gnome-keyring-1)
%endif
# remote desktop needs this
BuildRequires:	pam-devel
BuildRequires:	systemd
# using the built from source version on aarch64
BuildRequires:	ninja-build
# Yes, java is needed as well..
BuildRequires:	java-1.8.0-openjdk-headless

# There is a hardcoded check for nss 3.26 in the chromium code (crypto/nss_util.cc)
Requires:	nss%{_isa} >= 3.26
Requires:	nss-mdns%{_isa}

# GTK modules it expects to find for some reason.
%if 0%{gtk3}
Requires:	libcanberra-gtk3%{_isa}
%else
Requires:	libcanberra-gtk2%{_isa}
%endif

# Requirements for the CEF wrapper build
BuildRequires:	cmake

ExclusiveArch:	x86_64 aarch64

# Bundled bits (I'm sure I've missed some)
Provides: bundled(angle) = 2422
Provides: bundled(bintrees) = 1.0.1
# This is a fork of openssl.
Provides: bundled(boringssl)
Provides: bundled(brotli) = 222564a95d9ab58865a096b8d9f7324ea5f2e03e
Provides: bundled(bspatch)
Provides: bundled(cacheinvalidation) = 20150720
Provides: bundled(colorama) = 799604a104
Provides: bundled(crashpad)
Provides: bundled(dmg_fp)
Provides: bundled(expat) = 2.2.0
Provides: bundled(fdmlibm) = 5.3
Provides: bundled(fips181) = 2.2.3
%if 0%{?bundlefontconfig}
Provides: bundled(fontconfig) = 2.12.6
%endif
%if 0%{?bundlefreetype}
Provides: bundled(freetype) = 2.11.0git
%endif
Provides: bundled(gperftools) = svn144
%if 0%{?bundleharfbuzz}
Provides: bundled(harfbuzz) = 2.4.0
%endif
Provides: bundled(hunspell) = 1.6.0
Provides: bundled(iccjpeg)
%if 0%{?bundleicu}
Provides: bundled(icu) = 58.1
%endif
Provides: bundled(kitchensink) = 1
Provides: bundled(leveldb) = 1.20
Provides: bundled(libaddressinput) = 0
%if 0%{?bundlelibdrm}
Provides: bundled(libdrm) = 2.4.85
%endif
Provides: bundled(libevent) = 1.4.15
Provides: bundled(libjingle) = 9564
%if 0%{?bundlelibjpeg}
Provides: bundled(libjpeg-turbo) = 1.4.90
%endif
Provides: bundled(libphonenumber) = a4da30df63a097d67e3c429ead6790ad91d36cf4
%if 0%{?bundlelibpng}
Provides: bundled(libpng) = 1.6.22
%endif
Provides: bundled(libsrtp) = 2cbd85085037dc7bf2eda48d4cf62e2829056e2d
%if %{bundlelibusbx}
Provides: bundled(libusbx) = 1.0.17
%endif
Provides: bundled(libvpx) = 1.6.0
%if %{bundlelibwebp}
Provides: bundled(libwebp) = 0.6.0
%endif
%if %{bundlelibxml}
# Well, it's actually newer than 2.9.4 and has code in it that has been reverted upstream... but eh.
Provides: bundled(libxml) = 2.9.4
%endif
Provides: bundled(libXNVCtrl) = 302.17
Provides: bundled(libyuv) = 1651
Provides: bundled(lzma) = 15.14
Provides: bundled(libudis86) = 1.7.1
Provides: bundled(mesa) = 9.0.3
Provides: bundled(NSBezierPath) = 1.0
Provides: bundled(mozc)
%if %{bundleopus}
Provides: bundled(opus) = 1.1.3
%endif
Provides: bundled(ots) = 8d70cffebbfa58f67a5c3ed0e9bc84dccdbc5bc0
Provides: bundled(protobuf) = 3.0.0.beta.3
Provides: bundled(qcms) = 4
%if 0%{?bundlere2}
Provides: bundled(re2)
%endif
Provides: bundled(sfntly) = 04740d2600193b14aa3ef24cd9fbb3d5996b9f77
Provides: bundled(skia)
Provides: bundled(SMHasher) = 0
Provides: bundled(snappy) = 1.1.4-head
Provides: bundled(speech-dispatcher) = 0.7.1
Provides: bundled(sqlite) = 3.17patched
Provides: bundled(superfasthash) = 0
Provides: bundled(talloc) = 2.0.1
Provides: bundled(usrsctp) = 0
Provides: bundled(v8) = 5.9.211.31
Provides: bundled(webrtc) = 90usrsctp
Provides: bundled(woff2) = 445f541996fe8376f3976d35692fd2b9a6eedf2d
Provides: bundled(xdg-mime)
Provides: bundled(xdg-user-dirs)
# Provides: bundled(zlib) = 1.2.11

Provides: obs-cef(abi) = %{cef_version}

# For selinux scriptlet
Requires(post): /usr/sbin/semanage
Requires(post): /usr/sbin/restorecon

%if 0%{?fedora} >= 30
Requires: minizip-compat%{_isa}
%else
%if %{?rhel} == 9
Requires: minizip1.2%{_isa}
%else
Requires: minizip%{_isa}
%endif
%endif

%description
CEF is an embeddable build of Chromium, powered by WebKit (Blink).
This version is a fork by the OBS project designed to be used as
part of the OBS Browser Source plugin.

%package devel
Summary: Header files for the OBS fork of the Chromium Embedded Framework
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Header files for the OBS fork of the Chromium Embedded Framework.

%prep
%setup -q -T -n cef-%{cef_commit} -b 22
%setup -q -n chromium-%{chromium_version}
mv %{_builddir}/cef-%{cef_commit} ./cef

### Chromium Fedora Patches ###
%patch 0 -p1 -b .sandboxpie
%patch 1 -p1 -b .etc
%patch 2 -p1 -b .gnsystem
%patch 3 -p1 -b .nolibpngprefix
# Upstream accidentally made the same change in 89, but they've already reverted it for 90+ so this patch will return
# %%patch4 -p1 -b .nolibjpegmangle
%patch 5 -p1 -b .nozlibmangle
%patch 6 -p1 -b .nounrar
%patch 7 -p1 -b .widevine-hack
%patch 10 -p1 -b .widevine-other-locations

# Short term fixes (usually gcc and backports)
%patch 51 -p1 -b .gcc-remoting-constexpr
%patch 52 -p1 -b .unbundle-zlib
%patch 55 -p1 -b .protobuf-export
%patch 56 -p1 -b .missing-cstdint
%patch 57 -p1 -b .missing-cstring
%patch 58 -p1 -b .ffmpeg-deprecations
%patch 59 -p1 -b .VirtualCursor-std-layout
%patch 60 -p1 -b .SubstringSetMatcher-packed
%patch 61 -p1 -b .FrameLoadRequest-type

%patch 63 -p1 -b .gcc-cfi-fix
%patch 64 -p1 -b .aarch64-cxxflags-addition
%patch 65 -p1 -b .java-only-allowed
%patch 66 -p1 -b .python3-do-not-use-deprecated-mode-U
%patch 67 -p1 -b .remoting-cstring
%patch 69 -p1 -b .update-rjsmin-to-1.2.0
%patch 70 -p1 -b .update-six-to-1.16.0
%patch 79 -p1 -b .widevine-no-download
%patch 80 -p1 -b .EnumTable-crash
# %%patch81 -p1 -b .gcc12fix
%patch 82 -p1 -b .remoting-no-tests
%patch 84 -p1 -b .remoting-missing-cmath-header
%patch 86 -p1 -b .clang-format-py3
%if 0%{?fedora} >= 37
%patch 87 -p1 -b .markdownsafe-soft_str
%endif
%patch 88 -p1 -b .addresstracker-pagesize
%patch 97 -p1 -b .remoting-extra-qualification
%patch 98 -p1 -b .InkDropHost-crash
%patch 99 -p1 -b .enable-WebRTCPipeWireCapturer-byDefault
%patch 100 -p1 -b .missing-utility-for-std-exchange

# Fedora branded user agent
%if 0%{?fedora}
%patch 12 -p1 -b .fedora-user-agent
%endif

%if 0%{?rhel} == 9 || 0%{?fedora} == 37
%patch 114 -p1 -b .ffmpeg-5.x-duration
%endif
%patch 115 -p1 -b .prop-codecs

# Feature specific patches
%if %{use_vaapi}
%patch 202 -p1 -b .accel-mjpeg
%patch 205 -p1 -b .vaapi-intel-fix
%endif

%if 0%{?rhel} >= 8
%patch 300 -p1 -b .disblegnomekeyring
%endif

%patch 400 -p1 -b .gcc11
%patch 401 -p1 -b .gcc13
%patch 402 -p1 -b .gcc13
%patch 403 -p1 -b .gcc13
%patch 404 -p1 -b .gcc13
%patch 405 -p1 -b .gcc13
%patch 406 -p1 -b .gcc13
%patch 407 -p1 -b .gcc13
%patch 408 -p1 -b .gcc13
%patch 409 -p1 -b .gcc13
%patch 410 -p1 -b .gcc13
%patch 411 -p1 -b .gcc13
%patch 412 -p1 -b .gcc13
%patch 413 -p1 -b .gcc13
%patch 414 -p1 -b .gcc13
%patch 415 -p1 -b .gcc13
%patch 416 -p1 -b .gcc13
%patch 417 -p1 -b .gcc13

%patch 418 -p1 -b .gcc13
%patch 419 -p1 -b .gcc13

%patch 450 -p1 -b .python312

%patch 500 -p1 -b .cef-no-sysroot
%patch 501 -p1 -b .gcc13-patch-conflict
%patch 502 -p1 -b .skia-use-malloc

# Make CEF work with archives instead of Git checkouts
cp -a %{SOURCE23} cef/tools/git_util.py
cat > cef/.git-version <<EOF
COMMIT_HASH=%{cef_commit}
BRANCH_NAME=%{cef_branch}
COMMIT_NUMBER=%{cef_commit_number}
URL=https://github.com/obsproject/cef
EOF
cat > .git-version <<EOF
COMMIT_HASH=refs/tags/%{chromium_version}
URL=https://chromium.googlesource.com/chromium/src.git
EOF

# Change shebang in all relevant files in this directory and all subdirectories
# See `man find` for how the `-exec command {} +` syntax works
find -type f \( -iname "*.py" \) -exec sed -i '1s=^#! */usr/bin/\(python\|env python\)[23]\?=#!%{__python3}=' {} +

%if 0%{?asan}
export CC="clang"
export CXX="clang++"
%else
export CC="gcc"
export CXX="g++"
%endif
export AR="ar"
export RANLIB="ranlib"
export NM="nm"

rm -rf buildtools/third_party/libc++/BUILD.gn

# Core defines are flags that are true for both the browser and headless.
CHROMIUM_CORE_GN_DEFINES=""
CHROMIUM_CORE_GN_DEFINES+=' custom_toolchain="//build/toolchain/linux/unbundle:default"'
CHROMIUM_CORE_GN_DEFINES+=' host_toolchain="//build/toolchain/linux/unbundle:default"'
CHROMIUM_CORE_GN_DEFINES+=' is_debug=false dcheck_always_on=false dcheck_is_configurable=false'
%ifarch x86_64 aarch64
CHROMIUM_CORE_GN_DEFINES+=' system_libdir="lib64"'
%endif
%if %{official_build}
CHROMIUM_CORE_GN_DEFINES+=' is_official_build=true use_thin_lto=false is_cfi=false chrome_pgo_phase=0 use_debug_fission=true'
sed -i 's|OFFICIAL_BUILD|GOOGLE_CHROME_BUILD|g' tools/generate_shim_headers/generate_shim_headers.py
%endif
CHROMIUM_CORE_GN_DEFINES+=' is_clang=false use_sysroot=false disable_fieldtrial_testing_config=true use_lld=false rtc_enable_symbol_export=true'
%if %{use_gold}
CHROMIUM_CORE_GN_DEFINES+=' use_gold=true'
%else
CHROMIUM_CORE_GN_DEFINES+=' use_gold=false'
%endif

CHROMIUM_CORE_GN_DEFINES+=' ffmpeg_branding="Chrome" proprietary_codecs=true is_component_ffmpeg=true enable_ffmpeg_video_decoders=true media_use_ffmpeg=true'
CHROMIUM_CORE_GN_DEFINES+=' treat_warnings_as_errors=false'
CHROMIUM_CORE_GN_DEFINES+=' use_custom_libcxx=false'
CHROMIUM_CORE_GN_DEFINES+=' media_use_openh264=false'
CHROMIUM_CORE_GN_DEFINES+=' rtc_use_h264=false'
CHROMIUM_CORE_GN_DEFINES+=' use_kerberos=true'
%ifarch aarch64
CHROMIUM_CORE_GN_DEFINES+=' target_cpu="%{chromium_arch}"'
%endif
%if %{?use_jumbo}
CHROMIUM_CORE_GN_DEFINES+=' use_jumbo_build=true jumbo_file_merge_limit=8'
%endif
export CHROMIUM_CORE_GN_DEFINES

CHROMIUM_BROWSER_GN_DEFINES=""
CHROMIUM_BROWSER_GN_DEFINES+=' use_gio=true use_pulseaudio=true icu_use_data_file=true'
CHROMIUM_BROWSER_GN_DEFINES+=' enable_nacl=false'
CHROMIUM_BROWSER_GN_DEFINES+=' is_component_build=false'
CHROMIUM_BROWSER_GN_DEFINES+=' blink_symbol_level=0 enable_hangout_services_extension=true'
CHROMIUM_BROWSER_GN_DEFINES+=' use_aura=true'
CHROMIUM_BROWSER_GN_DEFINES+=' enable_widevine=true'
%if %{use_vaapi}
%if 0%{?fedora} >= 28
CHROMIUM_BROWSER_GN_DEFINES+=' use_vaapi=true'
%endif
%else
CHROMIUM_BROWSER_GN_DEFINES+=' use_vaapi=false'
%endif
%if 0%{?fedora}
CHROMIUM_BROWSER_GN_DEFINES+=' rtc_use_pipewire=true rtc_link_pipewire=true'
%endif

# Disable useless things for CEF
# For some reason CEF requires enable_print_preview=true?
CHROMIUM_BROWSER_GN_DEFINES+=' use_cups=false enable_remoting=false use_alsa=false'

export CHROMIUM_BROWSER_GN_DEFINES

CHROMIUM_HEADLESS_GN_DEFINES=""
CHROMIUM_HEADLESS_GN_DEFINES+=' use_ozone=true ozone_auto_platforms=false ozone_platform="headless" ozone_platform_headless=true'
CHROMIUM_HEADLESS_GN_DEFINES+=' headless_use_embedded_resources=false icu_use_data_file=false v8_use_external_startup_data=false'
CHROMIUM_HEADLESS_GN_DEFINES+=' enable_nacl=false enable_print_preview=false enable_remoting=false use_alsa=false'
CHROMIUM_HEADLESS_GN_DEFINES+=' use_cups=false use_dbus=true use_gio=false use_kerberos=false use_libpci=false'
CHROMIUM_HEADLESS_GN_DEFINES+=' use_pulseaudio=false use_udev=false use_gtk=false use_glib=false'
export CHROMIUM_HEADLESS_GN_DEFINES

mkdir -p third_party/node/linux/node-linux-x64/bin
ln -s %{_bindir}/node third_party/node/linux/node-linux-x64/bin/node

# Remove most of the bundled libraries. Libraries specified below (taken from
# Gentoo's Chromium ebuild) are the libraries that needs to be preserved.
build/linux/unbundle/remove_bundled_libraries.py \
	'base/third_party/cityhash' \
	'base/third_party/cityhash_v103' \
	'base/third_party/double_conversion' \
	'base/third_party/dynamic_annotations' \
	'base/third_party/icu' \
	'base/third_party/libevent' \
	'base/third_party/nspr' \
	'base/third_party/superfasthash' \
	'base/third_party/symbolize' \
	'base/third_party/valgrind' \
	'base/third_party/xdg_mime' \
	'base/third_party/xdg_user_dirs' \
	'buildtools/third_party/eu-strip' \
	'buildtools/third_party/libc++' \
	'buildtools/third_party/libc++abi' \
	'chrome/third_party/mozilla_security_manager' \
	'courgette/third_party' \
	'net/third_party/mozilla_security_manager' \
	'net/third_party/nss' \
	'net/third_party/quiche' \
	'net/third_party/uri_template' \
	'third_party/abseil-cpp' \
	'third_party/angle' \
	'third_party/angle/src/common/third_party/base' \
	'third_party/angle/src/common/third_party/smhasher' \
	'third_party/angle/src/common/third_party/xxhash' \
	'third_party/angle/src/third_party/libXNVCtrl' \
	'third_party/angle/src/third_party/trace_event' \
	'third_party/angle/src/third_party/volk' \
	'third_party/apple_apsl' \
	'third_party/axe-core' \
	'third_party/blanketjs' \
	'third_party/blink' \
	'third_party/boringssl' \
	'third_party/boringssl/src/third_party/fiat' \
	'third_party/breakpad' \
	'third_party/breakpad/breakpad/src/third_party/curl' \
	'third_party/brotli' \
	'third_party/catapult' \
	'third_party/catapult/common/py_vulcanize/third_party/rcssmin' \
	'third_party/catapult/common/py_vulcanize/third_party/rjsmin' \
	'third_party/catapult/third_party/beautifulsoup4' \
	'third_party/catapult/third_party/beautifulsoup4-4.9.3' \
	'third_party/catapult/third_party/google-endpoints' \
	'third_party/catapult/third_party/html5lib-1.1' \
	'third_party/catapult/third_party/html5lib-python' \
	'third_party/catapult/third_party/polymer' \
	'third_party/catapult/third_party/six' \
	'third_party/catapult/tracing/third_party/d3' \
	'third_party/catapult/tracing/third_party/gl-matrix' \
	'third_party/catapult/tracing/third_party/jpeg-js' \
	'third_party/catapult/tracing/third_party/jszip' \
	'third_party/catapult/tracing/third_party/mannwhitneyu' \
	'third_party/catapult/tracing/third_party/oboe' \
	'third_party/catapult/tracing/third_party/pako' \
        'third_party/ced' \
	'third_party/cld_3' \
	'third_party/closure_compiler' \
	'third_party/cpuinfo' \
	'third_party/crashpad' \
	'third_party/crashpad/crashpad/third_party/lss' \
	'third_party/crashpad/crashpad/third_party/zlib/' \
	'third_party/crc32c' \
	'third_party/cros_system_api' \
	'third_party/dav1d' \
	'third_party/dawn' \
	'third_party/dawn/third_party/gn' \
	'third_party/dawn/third_party/khronos' \
	'third_party/depot_tools' \
	'third_party/devscripts' \
	'third_party/devtools-frontend' \
	'third_party/devtools-frontend/src/third_party/typescript' \
	'third_party/devtools-frontend/src/front_end/third_party' \
	'third_party/devtools-frontend/src/front_end/third_party/acorn' \
	'third_party/devtools-frontend/src/front_end/third_party/axe-core' \
	'third_party/devtools-frontend/src/front_end/third_party/chromium' \
	'third_party/devtools-frontend/src/front_end/third_party/codemirror' \
	'third_party/devtools-frontend/src/front_end/third_party/diff' \
	'third_party/devtools-frontend/src/front_end/third_party/i18n' \
	'third_party/devtools-frontend/src/front_end/third_party/intl-messageformat' \
	'third_party/devtools-frontend/src/front_end/third_party/lighthouse' \
	'third_party/devtools-frontend/src/front_end/third_party/lit-html' \
	'third_party/devtools-frontend/src/front_end/third_party/lodash-isequal' \
	'third_party/devtools-frontend/src/front_end/third_party/marked' \
	'third_party/devtools-frontend/src/front_end/third_party/puppeteer' \
	'third_party/devtools-frontend/src/front_end/third_party/wasmparser' \
	'third_party/devtools-frontend/src/test/unittests/front_end/third_party/i18n' \
	'third_party/devtools-frontend/src/third_party' \
	'third_party/distributed_point_functions' \
	'third_party/dom_distiller_js' \
	'third_party/eigen3' \
	'third_party/emoji-segmenter' \
	'third_party/expat' \
	'third_party/farmhash' \
	'third_party/fdlibm' \
	'third_party/fft2d' \
	'third_party/flac' \
        'third_party/flatbuffers' \
	'third_party/fontconfig' \
	'third_party/fp16' \
	'third_party/freetype' \
	'third_party/fusejs' \
	'third_party/fxdiv' \
	'third_party/gemmlowp' \
	'third_party/google_input_tools' \
	'third_party/google_input_tools/third_party/closure_library' \
	'third_party/google_input_tools/third_party/closure_library/third_party/closure' \
	'third_party/google_trust_services' \
	'third_party/googletest' \
	'third_party/grpc' \
	'third_party/harfbuzz-ng' \
	'third_party/highway' \
	'third_party/hunspell' \
	'third_party/iccjpeg' \
	'third_party/icu' \
	'third_party/inspector_protocol' \
	'third_party/jinja2' \
	'third_party/jsoncpp' \
	'third_party/jstemplate' \
	'third_party/khronos' \
	'third_party/leveldatabase' \
	'third_party/libaddressinput' \
	'third_party/libaom' \
	'third_party/libaom/source/libaom/third_party/fastfeat' \
	'third_party/libaom/source/libaom/third_party/vector' \
	'third_party/libaom/source/libaom/third_party/x86inc' \
	'third_party/libavif' \
	'third_party/libdrm' \
	'third_party/libgav1' \
	'third_party/libgifcodec' \
	'third_party/libjingle' \
	'third_party/libjpeg_turbo' \
	'third_party/libjxl' \
	'third_party/libphonenumber' \
	'third_party/libpng' \
	'third_party/libsecret' \
        'third_party/libsrtp' \
	'third_party/libsync' \
	'third_party/libudev' \
	'third_party/liburlpattern' \
	'third_party/libusb' \
	'third_party/libva_protected_content' \
	'third_party/libvpx' \
	'third_party/libvpx/source/libvpx/third_party/x86inc' \
	'third_party/libwebm' \
	'third_party/libwebp' \
	'third_party/libx11' \
	'third_party/libxcb-keysyms' \
	'third_party/libxml' \
	'third_party/libxml/chromium' \
	'third_party/libxslt' \
	'third_party/libyuv' \
	'third_party/libzip' \
	'third_party/lottie' \
	'third_party/lss' \
	'third_party/lzma_sdk' \
	'third_party/mako' \
	'third_party/maldoca' \
	'third_party/maldoca/src/third_party/tensorflow_protos' \
	'third_party/maldoca/src/third_party/zlibwrapper' \
	'third_party/markupsafe' \
	'third_party/mesa' \
	'third_party/metrics_proto' \
	'third_party/minigbm' \
	'third_party/modp_b64' \
	'third_party/nasm' \
	'third_party/nearby' \
        'third_party/neon_2_sse' \
	'third_party/node' \
	'third_party/node/node_modules/polymer-bundler/lib/third_party/UglifyJS2' \
	'third_party/one_euro_filter' \
	'third_party/openscreen' \
	'third_party/openscreen/src/third_party/mozilla' \
	'third_party/openscreen/src/third_party/tinycbor' \
	'third_party/opus' \
	'third_party/ots' \
	'third_party/pdfium' \
	'third_party/pdfium/third_party/agg23' \
	'third_party/pdfium/third_party/base' \
	'third_party/pdfium/third_party/bigint' \
	'third_party/pdfium/third_party/freetype' \
	'third_party/pdfium/third_party/lcms' \
	'third_party/pdfium/third_party/libopenjpeg20' \
        'third_party/pdfium/third_party/libpng16' \
        'third_party/pdfium/third_party/libtiff' \
	'third_party/pdfium/third_party/skia_shared' \
	'third_party/perfetto' \
	'third_party/perfetto/protos/third_party/chromium' \
	'third_party/pffft' \
        'third_party/ply' \
	'third_party/polymer' \
	'third_party/pthreadpool' \
	'third_party/private-join-and-compute' \
	'third_party/private_membership' \
	'third_party/protobuf' \
	'third_party/protobuf/third_party/six' \
	'third_party/pyjson5' \
	'third_party/qcms' \
	'third_party/qunit' \
%if 0%{?bundlere2}
	'third_party/re2' \
%endif
	'third_party/rnnoise' \
	'third_party/ruy' \
	'third_party/s2cellid' \
	'third_party/securemessage' \
	'third_party/shell-encryption' \
	'third_party/simplejson' \
	'third_party/sinonjs' \
	'third_party/six' \
	'third_party/skia' \
	'third_party/skia/include/third_party/skcms' \
	'third_party/skia/include/third_party/vulkan' \
	'third_party/skia/third_party/skcms' \
	'third_party/skia/third_party/vulkan' \
	'third_party/smhasher' \
	'third_party/snappy' \
	'third_party/speech-dispatcher' \
	'third_party/sqlite' \
	'third_party/swiftshader' \
	'third_party/swiftshader/third_party/astc-encoder' \
	'third_party/swiftshader/third_party/llvm-subzero' \
	'third_party/swiftshader/third_party/llvm-10.0' \
	'third_party/swiftshader/third_party/marl' \
	'third_party/swiftshader/third_party/subzero' \
	'third_party/swiftshader/third_party/SPIRV-Headers' \
	'third_party/swiftshader/third_party/SPIRV-Tools' \
	'third_party/tensorflow-text' \
	'third_party/tflite' \
	'third_party/tflite/src/third_party/eigen3' \
	'third_party/tflite/src/third_party/fft2d' \
	'third_party/ukey2' \
        'third_party/usb_ids' \
	'third_party/utf' \
	'third_party/vulkan' \
	'third_party/wayland' \
	'third_party/web-animations-js' \
	'third_party/webdriver' \
	'third_party/webgpu-cts' \
	'third_party/webrtc' \
	'third_party/webrtc/common_audio/third_party/ooura' \
	'third_party/webrtc/common_audio/third_party/spl_sqrt_floor' \
	'third_party/webrtc/modules/third_party/fft' \
	'third_party/webrtc/modules/third_party/g711' \
	'third_party/webrtc/modules/third_party/g722' \
	'third_party/webrtc/rtc_base/third_party/base64' \
	'third_party/webrtc/rtc_base/third_party/sigslot' \
	'third_party/widevine' \
        'third_party/woff2' \
	'third_party/wuffs' \
	'third_party/x11proto' \
	'third_party/xcbproto' \
        'third_party/xdg-utils' \
	'third_party/xnnpack' \
	'third_party/zxcvbn-cpp' \
        'third_party/zlib' \
	'third_party/zlib/google' \
	'tools/gn/src/base/third_party/icu' \
	'url/third_party/mozilla' \
	'v8/src/third_party/siphash' \
	'v8/src/third_party/utf8-decoder' \
	'v8/src/third_party/valgrind' \
	'v8/third_party/v8' \
	'v8/third_party/inspector_protocol' \
	--do-remove

DEPOT_TOOLS=%{_builddir}/chromium-%{chromium_version}/third_party/depot_tools

# Use system ninja, remove the wrapper which only supports x86_64
rm ${DEPOT_TOOLS}/ninja

export PATH=$PATH:$DEPOT_TOOLS

build/linux/unbundle/replace_gn_files.py --system-libraries \
%if 0%{?bundlefontconfig}
%else
	fontconfig \
%endif
%if 0%{?bundlefreetype}
%else
	freetype \
%endif
%if 0%{?bundleharfbuzz}
%else
	harfbuzz-ng \
%endif
%if 0%{?bundleicu}
%else
	icu \
%endif
%if %{bundlelibdrm}
%else
	libdrm \
%endif
%if %{bundlelibjpeg}
%else
	libjpeg \
%endif
%if %{bundlelibpng}
%else
	libpng \
%endif
%if %{bundlelibusbx}
%else
	libusb \
%endif
%if %{bundlelibwebp}
%else
	libwebp \
%endif
%if %{bundlelibxml}
%else
	libxml \
%endif
	libxslt \
%if %{bundleopus}
%else
	opus \
%endif
%if 0%{?bundlere2}
%else
	re2 \
%endif
%if 0%{?bundleminizip}
%else
	zlib \
%endif
	flac \
	ffmpeg

# fix arm gcc
sed -i 's|arm-linux-gnueabihf-|arm-linux-gnu-|g' build/toolchain/linux/BUILD.gn

%ifarch aarch64
# We don't need to cross compile while building on an aarch64 system.
sed -i 's|aarch64-linux-gnu-||g' build/toolchain/linux/BUILD.gn
%endif

# Get rid of the pre-built eu-strip binary, it is x86_64 and of mysterious origin
rm -rf buildtools/third_party/eu-strip/bin/eu-strip
# Replace it with a symlink to the Fedora copy
ln -s %{_bindir}/eu-strip buildtools/third_party/eu-strip/bin/eu-strip

# Check that there is no system 'google' module, shadowing bundled ones:
if python3 -c 'import google ; print google.__path__' 2> /dev/null ; then \
    echo "Python 3 'google' module is defined, this will shadow modules of this build"; \
    exit 1 ; \
fi

mkdir -p %{builddir} && cp -a %{_bindir}/gn %{builddir}/

PYTHONPATH=%{builddir}/depot_tools
GN_DEFINES="$CHROMIUM_CORE_GN_DEFINES $CHROMIUM_BROWSER_GN_DEFINES" \
GN_ARGUMENTS="--script-executable=%{chromium_pybin}" \
%{chromium_pybin} cef/tools/gclient_hook.py

%if %{bundlelibusbx}
# no hackity hack hack
%else
# hackity hack hack
rm -rf third_party/libusb/src/libusb/libusb.h
# we _shouldn't need to do this, but it looks like we do.
cp -a %{_includedir}/libusb-1.0/libusb.h third_party/libusb/src/libusb/libusb.h
%endif

# Hard code extra version
FILE=chrome/common/channel_info_posix.cc
sed -i.orig -e 's/getenv("CHROME_VERSION_EXTRA")/"Fedora Project"/' $FILE

# Remove useless imports that no longer exist in Python 3.12
sed -i '/import imp/d' \
	mojo/public/tools/mojom/mojom/fileutil.py \
	mojo/public/tools/mojom/mojom/parse/lexer.py

%build

# Turning the buildsystem up to 11.
ulimit -n 4096

# unpack a local copy of the xcb-proto bits
tar xf %{SOURCE20}

# Decrease the debuginfo verbosity, so it compiles in koji
%ifarch %{ix86}
%global optflags %(echo %{optflags} | sed 's/-g /-g1 /')
%endif

export PYTHONPATH="../../third_party/pyjson5/src:../../xcb-proto-1.14:../../third_party/catapult/third_party/html5lib-1.1"

echo

%build_target %{builddir} cefclient
%build_target %{builddir} chrome_sandbox

# bug #827861, vk_swiftshader_icd.json not getting properly installed in out/Release
sed -e 's|${ICD_LIBRARY_PATH}|./libvk_swiftshader.so|g' third_party/swiftshader/src/Vulkan/vk_swiftshader_icd.json.tmpl > %{builddir}/vk_swiftshader_icd.json

# Build the CEF binary "distribution"
python3 cef/tools/make_distrib.py --distrib-subdir=distrib --output-dir=.. --ninja-build --%{chromium_arch}-build --minimal --no-docs --no-archive

# And compile libcef_dll_wrapper.a
cd ../
mkdir -p distrib-build
cd distrib-build
cmake ../distrib_minimal -GNinja -DPROJECT_ARCH="%{chromium_arch}"
ninja -j %{numjobs}

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{chromium_path}

pushd ../distrib_minimal/Resources
	cp -a *.pak locales icudtl.dat %{buildroot}%{chromium_path}
popd

pushd ../distrib_minimal/Release
	cp -a libvk_swiftshader.so* %{buildroot}%{chromium_path}
	strip %{buildroot}%{chromium_path}/libvk_swiftshader.so
	cp -a libvulkan.so* %{buildroot}%{chromium_path}
	strip %{buildroot}%{chromium_path}/libvulkan.so.1
	cp -a vk_swiftshader_icd.json %{buildroot}%{chromium_path}

	cp -a libcef.so %{buildroot}%{chromium_path}
	strip %{buildroot}%{chromium_path}/libcef.so
	cp -a chrome-sandbox %{buildroot}%{chromium_path}/chrome-sandbox
	strip %{buildroot}%{chromium_path}/chrome-sandbox

	# V8 initial snapshots
	# https://code.google.com/p/chromium/issues/detail?id=421063
	cp -a snapshot_blob.bin %{buildroot}%{chromium_path}
	cp -a v8_context_snapshot.bin %{buildroot}%{chromium_path}
	# This is ANGLE, not to be confused with the similarly named files under swiftshader/
	cp -a libEGL.so* libGLESv2.so* %{buildroot}%{chromium_path}
	strip %{buildroot}%{chromium_path}/libEGL.so
	strip %{buildroot}%{chromium_path}/libGLESv2.so
popd

pushd ../distrib_minimal/include
	mkdir -p %{buildroot}%{_includedir}/obs-cef
	cp -a * %{buildroot}%{_includedir}/obs-cef
	find %{buildroot}%{_includedir}/obs-cef -type f \( -iname "*.h" \) -exec sed -i 's,"include/,"obs-cef/,g' {} +
popd

pushd ../distrib-build/libcef_dll_wrapper
	cp -a libcef_dll_wrapper.a %{buildroot}%{chromium_path}
popd

mkdir -p .fedora-rpm/docs/
cp AUTHORS .fedora-rpm/docs/AUTHORS-CHROMIUM
cp cef/AUTHORS.txt .fedora-rpm/docs/AUTHORS-CEF

mkdir -p .fedora-rpm/license/
cp LICENSE .fedora-rpm/license/LICENSE-CHROMIUM
cp cef/LICENSE.txt .fedora-rpm/license/LICENSE-CEF

%post
# Set SELinux labels - semanage itself will adjust the lib directory naming
# But only do it when selinux is enabled, otherwise, it gets noisy.
if selinuxenabled; then
	semanage fcontext -a -t bin_t %{chromium_path} &>/dev/null || :
	semanage fcontext -a -t chrome_sandbox_exec_t %{chromium_path}/chrome-sandbox &>/dev/null || :
	restorecon -R -v %{chromium_path} &>/dev/null || :
fi

%files devel
%{chromium_path}/libcef_dll_wrapper.a
%{_includedir}/obs-cef/

%files
%doc .fedora-rpm/docs/AUTHORS*
%license .fedora-rpm/license/LICENSE*
%dir %{chromium_path}/
%{chromium_path}/chrome_*.pak
%{chromium_path}/resources.pak
%{chromium_path}/icudtl.dat
%{chromium_path}/libEGL.so*
%{chromium_path}/libGLESv2.so*
%attr(4755, root, root) %{chromium_path}/chrome-sandbox
%{chromium_path}/libvk_swiftshader.so*
%{chromium_path}/libvulkan.so*
%{chromium_path}/libcef.so
%{chromium_path}/vk_swiftshader_icd.json
%{chromium_path}/*.bin
%dir %{chromium_path}/locales/
%lang(af) %{chromium_path}/locales/af.pak*
%lang(am) %{chromium_path}/locales/am.pak*
%lang(ar) %{chromium_path}/locales/ar.pak*
%lang(bg) %{chromium_path}/locales/bg.pak*
%lang(bn) %{chromium_path}/locales/bn.pak*
%lang(ca) %{chromium_path}/locales/ca.pak*
%lang(cs) %{chromium_path}/locales/cs.pak*
%lang(da) %{chromium_path}/locales/da.pak*
%lang(de) %{chromium_path}/locales/de.pak*
%lang(el) %{chromium_path}/locales/el.pak*
%lang(en_GB) %{chromium_path}/locales/en-GB.pak*
# Chromium _ALWAYS_ needs en-US.pak as a fallback
# This means we cannot apply the lang code here.
# Otherwise, it is filtered out on install.
%{chromium_path}/locales/en-US.pak*
%lang(es) %{chromium_path}/locales/es.pak*
%lang(es) %{chromium_path}/locales/es-419.pak*
%lang(et) %{chromium_path}/locales/et.pak*
%lang(fa) %{chromium_path}/locales/fa.pak*
%lang(fi) %{chromium_path}/locales/fi.pak*
%lang(fil) %{chromium_path}/locales/fil.pak*
%lang(fr) %{chromium_path}/locales/fr.pak*
%lang(gu) %{chromium_path}/locales/gu.pak*
%lang(he) %{chromium_path}/locales/he.pak*
%lang(hi) %{chromium_path}/locales/hi.pak*
%lang(hr) %{chromium_path}/locales/hr.pak*
%lang(hu) %{chromium_path}/locales/hu.pak*
%lang(id) %{chromium_path}/locales/id.pak*
%lang(it) %{chromium_path}/locales/it.pak*
%lang(ja) %{chromium_path}/locales/ja.pak*
%lang(kn) %{chromium_path}/locales/kn.pak*
%lang(ko) %{chromium_path}/locales/ko.pak*
%lang(lt) %{chromium_path}/locales/lt.pak*
%lang(lv) %{chromium_path}/locales/lv.pak*
%lang(ml) %{chromium_path}/locales/ml.pak*
%lang(mr) %{chromium_path}/locales/mr.pak*
%lang(ms) %{chromium_path}/locales/ms.pak*
%lang(nb) %{chromium_path}/locales/nb.pak*
%lang(nl) %{chromium_path}/locales/nl.pak*
%lang(pl) %{chromium_path}/locales/pl.pak*
%lang(pt_BR) %{chromium_path}/locales/pt-BR.pak*
%lang(pt_PT) %{chromium_path}/locales/pt-PT.pak*
%lang(ro) %{chromium_path}/locales/ro.pak*
%lang(ru) %{chromium_path}/locales/ru.pak*
%lang(sk) %{chromium_path}/locales/sk.pak*
%lang(sl) %{chromium_path}/locales/sl.pak*
%lang(sr) %{chromium_path}/locales/sr.pak*
%lang(sv) %{chromium_path}/locales/sv.pak*
%lang(sw) %{chromium_path}/locales/sw.pak*
%lang(ta) %{chromium_path}/locales/ta.pak*
%lang(te) %{chromium_path}/locales/te.pak*
%lang(th) %{chromium_path}/locales/th.pak*
%lang(tr) %{chromium_path}/locales/tr.pak*
%lang(uk) %{chromium_path}/locales/uk.pak*
%lang(ur) %{chromium_path}/locales/ur.pak*
%lang(vi) %{chromium_path}/locales/vi.pak*
%lang(zh_CN) %{chromium_path}/locales/zh-CN.pak*
%lang(zh_TW) %{chromium_path}/locales/zh-TW.pak*
# These are psuedolocales, not real ones.
# They only get generated when is_official_build=false
%if ! %{official_build}
%{chromium_path}/locales/ar-XB.pak*
%{chromium_path}/locales/en-XA.pak*
%endif

%changelog
* Sun Dec 10 2023 Asahi Lina <lina@asahilina.net> - 5060^cr103.0.5060.134~git20231010.17f8588-2
- Fix segfaults due to allocator mixup in Skia

* Sun Dec 10 2023 Asahi Lina <lina@asahilina.net> - 5060^cr103.0.5060.134~git20231010.17f8588-1
- Initial package for Fedora
