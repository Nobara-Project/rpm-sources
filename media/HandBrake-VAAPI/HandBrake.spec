%global commit0 e0d003d1bb00950f2e4147be30cd5c2afc0751da
%global date 20251219
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
#%%global tag %%{version}

%ifarch %{x86_64}
%global _with_asm 1
%global _with_vpl 1
%endif

%global desktop_id fr.handbrake.ghb
%global appname HandBrake

Name:           HandBrake
Version:        1.10.2
Epoch:		1
Release:        1%{!?tag:.%{date}git%{shortcommit0}}%{?dist}
Summary:        An open-source multiplatform video transcoder
License:        GPLv2+
URL:            https://handbrake.fr/

%if 0%{?tag:1}
Source0:        https://github.com/%{name}/%{name}/releases/download/%{version}/%{name}-%{version}-source.tar.bz2
Source1:        https://github.com/%{name}/%{name}/releases/download/%{version}/%{name}-%{version}-source.tar.bz2.sig
# import from https://handbrake.fr/openpgp.php or https://github.com/HandBrake/HandBrake/wiki/OpenPGP
# gpg2 --export --export-options export-minimal 1629C061B3DDE7EB4AE34B81021DB8B44E4A8645 > gpg-keyring-1629C061B3DDE7EB4AE34B81021DB8B44E4A8645.gpg
Source2:        gpg-keyring-1629C061B3DDE7EB4AE34B81021DB8B44E4A8645.gpg
%else
Source0:        https://github.com/sgothel/%{appname}/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz
%endif

# Don't link with libva unnecessarily
Patch1:         %{appname}-no-libva.patch
# Don't link with fdk_aac unnecessarily
Patch2:         %{appname}-no-fdk_aac.patch
# Fix build on non-x86 (without nasm) and drop libtool requirement
Patch3:         %{appname}-no-libtool-nasm.patch
# Patches from Debian
# https://salsa.debian.org/multimedia-team/handbrake/-/raw/master/debian/patches/0001-Remove-embedded-downloaded-copies-of-various-librari.patch
Patch4:         %{appname}-syslibs-link.patch
# x265 part of
# https://salsa.debian.org/multimedia-team/handbrake/-/raw/master/debian/patches/0003-Remove-ambient-viewing-support.patch
Patch5:         %{appname}-remove-ambient-viewing-support.patch
# https://salsa.debian.org/multimedia-team/handbrake/-/raw/master/debian/patches/0004-Do-not-use-contribs.patch
Patch6:         %{appname}-no-contribs.patch
# https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=1032972#25
# Fix https://github.com/HandBrake/HandBrake/issues/4029 with unpatched FFmpeg
Patch7:         %{appname}-save-pts-of-incomplete-subtitle.patch
# Revert
# https://github.com/HandBrake/HandBrake/commit/fb2397df5d25226493e9ec36671469e4906d8842
# https://github.com/HandBrake/HandBrake/commit/09e99ce641c840686b1b5f860263e89ad7d6651d
# and part of
# https://github.com/HandBrake/HandBrake/commit/6f2cd466ef0e029d9e5a51ac8640c3ab64e212f6
Patch8:         %{appname}-remove-ITU-T.35-support.patch

BuildRequires:  AMF-devel
BuildRequires:  cmake
BuildRequires:  desktop-file-utils
%if 0%{?tag:1}
BuildRequires:  gnupg2
%endif
BuildRequires:  libappstream-glib
# Preview is broken with <7.0 https://github.com/HandBrake/HandBrake/issues/6178
BuildRequires:  ffmpeg-devel >= 7.0
# Should be >= 2.6:
BuildRequires:  freetype-devel >= 2.4.11
# Should be >= 0.19.7:
BuildRequires:  fribidi-devel >= 0.19.4
BuildRequires:  gcc-c++
BuildRequires:  gtk4-devel
BuildRequires:  jansson-devel
BuildRequires:  turbojpeg-devel
# Should be >= 0.13.2:
BuildRequires:  libass-devel >= 0.13.1
BuildRequires:  libbluray-devel >= 0.9.3
BuildRequires:  libdrm-devel
BuildRequires:  libdvdnav-devel >= 5.0.1
BuildRequires:  libdvdread-devel >= 5.0.0
%if 0%{?_with_vpl:1}
BuildRequires:  libvpl-devel
BuildRequires:  libva-devel
%endif
BuildRequires:  libsamplerate-devel
BuildRequires:  libtheora-devel
BuildRequires:  libvorbis-devel
BuildRequires:  make
BuildRequires:  meson
%if 0%{?_with_asm:1}
BuildRequires:  nasm
%endif
BuildRequires:  nv-codec-headers
BuildRequires:  pkgconfig(numa)
BuildRequires:  python3
BuildRequires:  svt-av1-devel
BuildRequires:  x264-devel >= 0.148
BuildRequires:  x265-devel >= 1.9

Requires:       hicolor-icon-theme
# needed for reading encrypted DVDs
%{?fedora:Recommends:     libdvdcss%{_isa}}
Obsoletes:      HandBrake-cli < %{version}-%{release}
Provides:       HandBrake-cli = %{version}-%{release}
Provides:       handbrake =  %{version}-%{release}

%description
%{appname} is a general-purpose, free, open-source, cross-platform, multithreaded
video transcoder software application. It can process most common multimedia
files and any DVD or Bluray sources that do not contain any kind of copy
protection.

This package contains the command line version of the program.

%package gui
Summary:        An open-source multiplatform video transcoder (GUI)
Provides:       handbrake-gui = %{version}-%{release}
Requires:       hicolor-icon-theme
# needed for reading encrypted DVDs
%{?fedora:Recommends:     libdvdcss%{_isa}}
# needed for live preview
%{?fedora:Recommends:     gstreamer1-plugins-good%{_isa}}

%description gui
%{appname} is a general-purpose, free, open-source, cross-platform, multithreaded
video transcoder software application. It can process most common multimedia
files and any DVD or Bluray sources that do not contain any kind of copy
protection.

This package contains the main program with a graphical interface.

%prep
%if 0%{?tag:1}
gpgv2 --keyring %{S:2} %{S:1} %{S:0}
%endif
%setup -q %{!?tag:-n %{appname}-%{commit0}}
%if 0%{!?_with_vpl}
%patch -P1 -p1
%endif
%patch -P2 -p1
%patch -P3 -p1
%patch -P4 -p1
%patch -P5 -p1
%patch -P6 -p1
%patch -P7 -p1
%patch -P8 -p1

# Use system libraries in place of bundled ones
for module in fdk-aac ffmpeg libdvdnav libdvdread libbluray %{?_with_vpl:libvpl} nvdec nvenc svt-av1 x265; do
    sed -i -e "/MODULES += contrib\/$module/d" make/include/main.defs
done

%build
echo "HASH=%{commit0}" > version.txt
echo "SHORTHASH=%{shortcommit0}" >> version.txt
echo "DATE=$(date "+%Y-%m-%d %T" -d %{date})" >> version.txt
%if 0%{?tag:1}
echo "TAG=%{tag}" >> version.txt
echo "TAG_HASH=%{commit0}" >> version.txt
%endif

# This makes build stop if any download is attempted
export http_proxy=http://127.0.0.1

# By default the project is built with optimizations for speed and no debug.
# Override configure settings by passing RPM_OPT_FLAGS and disabling preset
# debug options.
echo "GCC.args.O.speed = %{optflags} -I%{_includedir}/vpl -I%{_includedir}/ffmpeg -ldl -lx265 %{?_with_vpl:-lvpl}" > custom.defs
echo "GCC.args.g.none = " >> custom.defs

# Not an autotools configure script.
./configure \
    --build build \
    --prefix=%{_prefix} \
    --debug=std \
    --strip=%{_bindir}/echo \
    --verbose \
    --disable-df-fetch \
    --disable-df-verify \
    %{?_with_asm:--enable-asm} \
    --enable-x265 \
    --enable-nvdec \
    --enable-nvenc \
    --enable-numa \
    --enable-fdk-aac \
    --enable-ffmpeg-aac \
    --enable-gst \
    --enable-vce \
    --force \
    --no-harden \
    %{?_with_vpl:--enable-qsv}

%make_build -C build V=1

%install
%make_install -C build

%find_lang ghb

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{desktop_id}.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{desktop_id}.metainfo.xml

%files -f ghb.lang gui
%license COPYING
%doc AUTHORS.markdown NEWS.markdown README.markdown THANKS.markdown
%{_bindir}/ghb
%{_metainfodir}/%{desktop_id}.metainfo.xml
%{_datadir}/applications/%{desktop_id}.desktop
%{_datadir}/icons/hicolor/scalable/apps/%{desktop_id}.svg

%files
%license COPYING
%doc AUTHORS.markdown NEWS.markdown README.markdown THANKS.markdown
%{_bindir}/HandBrakeCLI

%changelog
* Mon Sep 29 2025 Robert-André Mauchin <zebob.m@gmail.com> - 1.10.2-1
- Update to 1.10.2

* Wed Sep 03 2025 Sérgio Basto <sergio@serjux.com> - 1.9.2-3
- Rebuild for x264

* Sat Jul 26 2025 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.9.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Mar 26 2025 Dominik Mierzejewski <dominik@greysector.net> - 1.9.2-1
- update to 1.9.2
- drop no longer required patches for x265 4.x and FFmpeg 7.1 support
- fix build against upstream FFmpeg by reverting non-upstreamed support
  for ITU T.35 metadata conversion

* Tue Mar 25 2025 Dominik Mierzejewski <dominik@greysector.net> - 1.8.2-7
- drop no longer required patch hunks (amve is supported in FFmpeg 7.0+)
- fix build with FFmpeg 7.1

* Tue Jan 28 2025 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.8.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sun Nov 24 2024 Leigh Scott <leigh123linux@gmail.com> - 1.8.2-5
- Fix x265 buildfix patch

* Sat Nov 23 2024 Leigh Scott <leigh123linux@gmail.com> - 1.8.2-4
- Rebuild for new x265
- Switch build requires from oneVPL to libvpl

* Tue Oct 08 2024 Dominik Mierzejewski <dominik@greysector.net> - 1.8.2-3
- bump to rebuild

* Sun Sep 01 2024 Dominik 'Rathann' Mierzejewski <dominik@greysector.net> - 1.8.2-2
- bump FFmpeg requirement to 7.0
- sync patches from Debian
- fix DVD subtitle PTS handling

* Sun Aug 18 2024 Dominik 'Rathann' Mierzejewski <dominik@greysector.net> - 1.8.2-1
- Update to 1.8.2

* Thu Aug 01 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jul 20 2024 Dominik 'Rathann' Mierzejewski <dominik@greysector.net> - 1.8.1-1
- Update to 1.8.1

* Sat Jun 08 2024 Dominik 'Rathann' Mierzejewski <dominik@greysector.net> - 1.8.0-1
- Update to 1.8.0
- Drop obsolete patch
- Fix linking with system libraries
- Drop unused build dependencies
- Enable nvdec

* Sat Jun 01 2024 Robert-André Mauchin <zebob.m@gmail.com> - 1.7.3-2
- Rebuild for svt-av1 2.1.0

* Wed May 15 2024 Dominik 'Rathann' Mierzejewski <dominik@greysector.net> - 1.7.3-1
- Update to version 1.7.3.
- Drop obsolete patches
- Fix build with system FFmpeg/x265
- Drop unused dependencies
- Fix libxml2 cflags parsing

* Sat Apr 06 2024 Leigh Scott <leigh123linux@gmail.com> - 1.6.1-6
- Rebuild for new x265 version

* Mon Mar 11 2024 Dominik 'Rathann' Mierzejewski <dominik@greysector.net> - 1.6.1-5
- Fix build with GCC14

* Sat Feb 03 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.6.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Nov 12 2023 Leigh Scott <leigh123linux@gmail.com> - 1.6.1-3
- Rebuild for new ffmpeg version

* Wed Aug 02 2023 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sun Apr 09 2023 Leigh Scott <leigh123linux@gmail.com> - 1.6.1-1
- Updated to version 1.6.1.

* Wed Mar 01 2023 Leigh Scott <leigh123linux@gmail.com> - 1.6.0-4
- Rebuild for new ffmpeg

* Mon Jan 23 2023 Dominik 'Rathann' Mierzejewski <dominik@greysector.net> - 1.6.0-3
- enable FDK-AAC "support" (no direct build-time or runtime dependency,
  works if system FFmpeg supports it)

* Fri Jan 06 2023 Dominik 'Rathann' Mierzejewski <dominik@greysector.net> - 1.6.0-2
- restore building on non-x86_64 (see https://bugzilla.redhat.com/show_bug.cgi?id=2158920)

* Thu Jan 05 2023 Vitaly Zaitsev <vitaly@easycoding.org> - 1.6.0-1
- Updated to version 1.6.0.
- Switched to intel-mediasdk-devel and oneVPL-devel as required by upstream.
- Install metainfo manifest on EPEL too.
- Removed the legacy scriptlets.
- Added check section.

* Sat Aug 06 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.5.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild and ffmpeg
  5.1

* Thu Jun 23 2022 Robert-André Mauchin <zebob.m@gmail.com> - 1.5.1-3
- Rebuilt for new dav1d

* Sun Jun 12 2022 Sérgio Basto <sergio@serjux.com> - 1.5.1-2
- Mass rebuild for x264-0.164

* Thu Feb 17 2022 Dominik 'Rathann' Mierzejewski <rpm@greysector.net> - 1.5.1-1
- new upstream version (rfbz#6221)
- drop obsolete patch
- keep building with libmfx

* Tue Feb 08 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Nov 10 2021 Leigh Scott <leigh123linux@gmail.com> - 1.4.2-1
- New upstream version

* Wed Nov 10 2021 Leigh Scott <leigh123linux@gmail.com> - 1.3.3-15
- Rebuilt for new ffmpeg snapshot

* Mon Aug 02 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.3.3-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sat Jul 10 2021 Sérgio Basto <sergio@serjux.com> - 1.3.3-13
- Mass rebuild for x264-0.163

* Sun May 30 2021 Dominik 'Rathann' Mierzejewski <rpm@greysector.net> - 1.3.0-12
- fix audio encoders when linking to FFmpeg 4.4 (rfbz#6006)

* Wed Apr 14 2021 Leigh Scott <leigh123linux@gmail.com> - 1.3.3-11
- Rebuild for new x265

* Tue Feb 02 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.3.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jan  1 2021 Leigh Scott <leigh123linux@gmail.com> - 1.3.3-9
- Rebuilt for new ffmpeg snapshot

* Mon Dec 14 2020 Leigh Scott <leigh123linux@gmail.com> - 1.3.3-8
- Actually do the dav1d rebuild

* Mon Dec 14 2020 Robert-André Mauchin <zebob.m@gmail.com> - 1.3.3-7
- Rebuild for dav1d SONAME bump

* Fri Nov 27 2020 Sérgio Basto <sergio@serjux.com> - 1.3.3-6
- Mass rebuild for x264-0.161

* Wed Oct 21 2020 Leigh Scott <leigh123linux@gmail.com> - 1.3.3-5
- Rebuild for new libdvdread

* Mon Aug 17 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.3.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 07 2020 Sérgio Basto <sergio@serjux.com> - 1.3.3-3
- Mass rebuild for x264

* Wed Jul 01 2020 Leigh Scott <leigh123linux@gmail.com> - 1.3.3-2
- Rebuilt

* Sun Jun 14 2020 Leigh Scott <leigh123linux@gmail.com> - 1.3.3-1
- New upstream version

* Sun May 31 2020 Leigh Scott <leigh123linux@gmail.com> - 1.3.2-3
- Rebuild for new x265 version

* Sun May 24 2020 Leigh Scott <leigh123linux@gmail.com> - 1.3.2-2
- Rebuild for dav1d SONAME bump

* Tue May 05 2020 Leigh Scott <leigh123linux@gmail.com> - 1.3.2-1
- New upstream version

* Fri Mar 06 2020 Leigh Scott <leigh123linux@gmail.com> - 1.3.1-1
- New upstream version
- Update source URL
- Run scriptlets on el7 only

* Sun Feb 23 2020 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 1.3.0-7
- Rebuild for x265

* Sat Feb 22 2020 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 1.3.0-6
- Rebuild for ffmpeg-4.3 git

* Tue Feb 04 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.3.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Dec 17 2019 Leigh Scott <leigh123linux@gmail.com> - 1.3.0-4
- Mass rebuild for x264

* Thu Nov 28 2019 Leigh Scott <leigh123linux@googlemail.com> - 1.3.0-3
- Rebuild for new x265

* Wed Nov 27 2019 Dominik 'Rathann' Mierzejewski <rpm@greysector.net> - 1.3.0-2
- update commit hash and date for 1.3.0 release

* Thu Nov 21 2019 FeRD (Frank Dana) <ferdnyc@gmail.com> - 1.3.0-1
- New upstream version (fixes compilation with Pango 1.44+)
- New dependencies: libdav1d, libdrm, libva, numactl
- dropped dependencies: yasm
- fixes rfbz#5426
- fix build on non-x86 (without nasm)

* Fri Nov 15 2019 Dominik 'Rathann' Mierzejewski <rpm@greysector.net> - 1.2.2-7
- rebuild for libdvdread ABI bump

* Wed Aug 07 2019 Leigh Scott <leigh123linux@gmail.com> - 1.2.2-6
- Rebuild for new ffmpeg version

* Tue Jul 02 2019 Nicolas Chauvet <kwizart@gmail.com> - 1.2.2-5
- Rebuilt for x265

* Fri May 03 2019 Leigh Scott <leigh123linux@gmail.com> - 1.2.2-4
- Rebuild for new gstreamer1 version

* Tue Mar 12 2019 Sérgio Basto <sergio@serjux.com> - 1.2.2-3
- Mass rebuild for x264

* Mon Mar 04 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Feb 28 2019 Leigh Scott <leigh123linux@googlemail.com> - 1.2.2-1
- Update to 1.2.2

* Sun Jan 20 2019 Dominik Mierzejewski <rpm@greysector.net> - 1.2.0-1
- Update to 1.2.0
- Drop upstreamed subtitle handling patch
- Make libbluray patch EL-only, all current Fedoras have >1.0.0
- new dependencies: speex, xz
- enable asm parts on x86

* Sun Nov 18 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.1.2-1
- Rebuild for new x265
- Update to 1.1.2

* Thu Oct 04 2018 Sérgio Basto <sergio@serjux.com> - 1.1.0-4
- Mass rebuild for x264 and/or x265
- Add BuildRequires: gcc-c++

* Thu Jul 26 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Jun 17 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.1.0-2
- Rebuild for new libass version

* Mon Apr 09 2018 Dominik Mierzejewski <rpm@greysector.net> - 1.1.0-1
- Update to 1.1.0
- Update source and signature URLs
- Drop obsolete patches
- Bump FFmpeg version requirement to 3.5+ due to AV_PKT_FLAG_DISPOSABLE API use

* Thu Mar 08 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 1.0.7-14
- Rebuilt for new ffmpeg snapshot

* Wed Feb 28 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.0.7-13
- Rebuilt for new x265
- Fix scriptlets

* Sat Jan 27 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.0.7-12
- Rebuilt for new libvpx

* Thu Jan 18 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.0.7-11
- Rebuilt for ffmpeg-3.5 git

* Sun Dec 31 2017 Sérgio Basto <sergio@serjux.com> - 1.0.7-10
- Mass rebuild for x264 and x265

* Fri Dec 29 2017 Dominik Mierzejewski <rpm@greysector.net> - 1.0.7-9
- Fix SubRip subtitle issue when built with FFmpeg

* Fri Dec 01 2017 Dominik Mierzejewski <rpm@greysector.net> - 1.0.7-8
- Rebuild against new libmfx (rhbz#1471768)

* Wed Nov 01 2017 Sérgio Basto <sergio@serjux.com> - 1.0.7-7
- Rebuild for x265 update

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 1.0.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 1.0.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jul 20 2017 Dominik Mierzejewski <rpm@greysector.net> - 1.0.7-4
- update commit id to match 1.0.7 release
- drop redundant Provides/Obsoletes
- switch to a source URL that works with spectool/curl
- add GPG signature and verify it in prep

* Sat Apr 29 2017 Leigh Scott <leigh123linux@googlemail.com> - 1.0.7-3
- Rebuild for ffmpeg and x265 update

* Wed Apr 12 2017 Simone Caronni <negativo17@gmail.com> - 1.0.7-2
- Remove webkitgtk3 build requirement, it's actually used only when the update
  checks are enabled in the gui (not needed in our case and removed in fc27).

* Wed Apr 12 2017 Simone Caronni <negativo17@gmail.com> - 1.0.7-1
- Update to latest 1.0.7.

* Thu Mar 23 2017 Leigh Scott <leigh123linux@googlemail.com> - 1.0.3-4
- Fix ppc64le build

* Sat Mar 18 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 1.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Mar 18 2017 Xavier Bachelot <xavier@bachelot.org> - 1.0.3-2
- Don't apply clip_id patch for releases shipping with libbluray 1.0.0.

* Wed Mar 08 2017 Xavier Bachelot <xavier@bachelot.org> - 1.0.3-1
- Update to 1.0.3.
- Use Recommends: only for Fedora.
- Fix debuginfo sub-package.

* Sat Jan 28 2017 Dominik Mierzejewski <rpm@greysector.net> - 1.0.2-1
- update to 1.0.2
- avoid unnecessary libva dependency

* Fri Jan 20 2017 Dominik Mierzejewski <rpm@greysector.net> - 1.0.1-1
- Update to 1.0.1.
- Use make_build macro.
- Fix BRs and drop redundant ones.
- libva is required to build with QSV.
- Provide lowercase name provides.
- Restore support for building with bundled libav.

* Fri Dec 02 2016 Dominik Mierzejewski <rpm@greysector.net> - 1.0-33.20161201git8a9f21c
- Update to latest sources.
- Soft dependency on gstreamer1-plugins-good for live preview.
- Change hard dependency on libdvdcss to soft.
- libmfx is x86-only.
- Move -cli to the main package.
- Drop support for building with libav.

* Thu Dec 01 2016 Simone Caronni <negativo17@gmail.com> - 1.0-32.20161129gitfac5e0e
- Update to latest snapshot.
- Add patches from Dominik Mierzejewski:
  * Allow use of unpatched libbluray.
  * Use system OpenCL headers.
  * Do not strip binaries.

* Fri Nov 18 2016 Simone Caronni <negativo17@gmail.com> - 1.0-31.20161116gitb9c5daa
- Update to latest snapshot.
- Use Flatpak desktop file, icon and AppStream metadata (more complete).

* Sat Oct 08 2016 Simone Caronni <negativo17@gmail.com> - 1.0-30.20161006git88807bb
- Fix date.
- Rebuild for fdk-aac update.

* Sat Oct 08 2016 Simone Caronni <negativo17@gmail.com> - 1.0-29.20160929git88807bb
- Require x265 hotfix.

* Sun Oct 02 2016 Simone Caronni <negativo17@gmail.com> - 1.0-28.20160929gitd398531
- Rebuild for x265 update.

* Sun Oct 02 2016 Simone Caronni <negativo17@gmail.com> - 1.0-27.20160929gitd398531
- Update to latest snapshot.
- Update package release according to package guidelines.
- Enable Intel Quick Sync Video encoding by default (libmfx package in main
  repositories).
- Add AppData support for Fedora (metadata from upstream).
- Do not run update-desktop-database on Fedora 25+ as per packaging guidelines.

* Fri Aug 05 2016 Simone Caronni <negativo17@gmail.com> - 1.0-26.6b5d91a
- Update to latest sources.

* Thu Jul 14 2016 Simone Caronni <negativo17@gmail.com> - 1.0-25.56c7ee7
- Update to latest snapshot.

* Fri Jul 08 2016 Simone Caronni <negativo17@gmail.com> - 1.0-24.0fc54d0
- Update to latest sources.

* Sun Jul 03 2016 Simone Caronni <negativo17@gmail.com> - 1.0-23.b1a4f0d
- Update to latest sources.

* Sun Jun 19 2016 Simone Caronni <negativo17@gmail.com> - 1.0-22.221bfe7
- Update to latest sources, bump build requirements.

* Tue May 24 2016 Simone Caronni <negativo17@gmail.com> - 1.0-21.879a512
- Update to latest sources.

* Wed Apr 13 2016 Simone Caronni <negativo17@gmail.com> - 1.0-20.8be786a
- Update to latest sources.
- Update build requirements of x264/x265 to match upstream.

* Thu Mar 31 2016 Simone Caronni <negativo17@gmail.com> - 1.0-19.a447656
- Bugfixes.

* Tue Mar 29 2016 Simone Caronni <negativo17@gmail.com> - 1.0-18.113e2a5
- Update to latest snapshot for various fixes.

* Wed Mar 16 2016 Simone Caronni <negativo17@gmail.com> - 1.0-17.12f7be2
- Update to latest sources.

* Fri Feb 12 2016 Simone Caronni <negativo17@gmail.com> - 1.0-16.0da688d
- Update to latest snapshot.

* Sun Jan 31 2016 Simone Caronni <negativo17@gmail.com> - 1.0-15.ba5eb77
- Update to latest snapshot.

* Fri Jan 22 2016 Simone Caronni <negativo17@gmail.com> - 1.0-14.08e7b54
- Update to latest sources, contains normalization fix.
- Make Intel QuickSync encoder suppport conditional at build time.

* Sat Jan 16 2016 Simone Caronni <negativo17@gmail.com> - 1.0-13.ed8c11e
- Update to latest sources.

* Fri Jan 08 2016 Simone Caronni <negativo17@gmail.com> - 1.0-12.ee1167e
- Update to latest sources.

* Wed Dec 23 2015 Simone Caronni <negativo17@gmail.com> - 1.0-11.1e56395
- Update sources. Intel Quick Sync hardware support can be built using the same
  library as FFMpeg. No frontend support yet.

* Mon Dec 21 2015 Simone Caronni <negativo17@gmail.com> - 1.0-10.57a9f48
- Update sources.

* Fri Dec 11 2015 Simone Caronni <negativo17@gmail.com> - 1.0-9.3443f6a
- Update to latest sources.

* Sun Dec 06 2015 Simone Caronni <negativo17@gmail.com> - 1.0-8.ca69335
- Update to latest sources.

* Tue Dec 01 2015 Simone Caronni <negativo17@gmail.com> - 1.0-7.46e641c
- Switch back to bundled libav 11 to fix subtitle detection.
- Make bundling libav conditional.

* Fri Nov 27 2015 Simone Caronni <negativo17@gmail.com> - 1.0-6.46e641c
- Update to latest sources.

* Mon Nov 23 2015 Simone Caronni <negativo17@gmail.com> - 1.0-5.6c731e1
- Update ffmpeg patch.

* Fri Nov 20 2015 Simone Caronni <negativo17@gmail.com> - 1.0-4.6c731e1
- Update to latest upstream.
- Add license macro.

* Sat Nov 14 2015 Simone Caronni <negativo17@gmail.com> - 1.0-3.6d66bd5
- Use system libfdk-aac.

* Tue Nov 10 2015 Simone Caronni <negativo17@gmail.com> - 1.0-2.6d66bd5
- Update snapshot.
- Use packaging guidelines for GitHub snapshots.
- Update fdk-aac bundle.
- Update build requirements.

* Wed Oct 28 2015 Simone Caronni <negativo17@gmail.com> - 1.0-1
- Update to master branch.
- Use system x265.

* Fri Oct 23 2015 Simone Caronni <negativo17@gmail.com> - 0.10.2-3
- Udpate patches from 0.10.x branch.
- Use system ffmpeg libraries in place of bundled libav.

* Mon Sep 28 2015 Simone Caronni <negativo17@gmail.com> - 0.10.2-2
- Update latest patches from the 0.10.x branch.

* Thu Jun 11 2015 Simone Caronni <negativo17@gmail.com> - 0.10.2-1
- Update to 0.10.2.
- Use handbrake.fr URL for source 0.

* Mon Mar 09 2015 Simone Caronni <negativo17@gmail.com> - 0.10.1-1
- Update to 0.10.1.

* Mon Jan 26 2015 Simone Caronni <negativo17@gmail.com> - 0.10.0-12
- Fix huge icons problem.

* Wed Nov 26 2014 Simone Caronni <negativo17@gmail.com> - 0.10.0-11
- Update to 0.10.0 official release.

* Wed Nov 05 2014 Simone Caronni <negativo17@gmail.com> - 0.10-10.svn6507
- Update to SVN revision 6507.

* Mon Nov 03 2014 Simone Caronni <negativo17@gmail.com> - 0.10-9.svn6502
- Update to SVN revision 6502.

* Fri Oct 24 2014 Simone Caronni <negativo17@gmail.com> - 0.10-8.svn6461
- Update to SVN revision 6461.

* Fri Oct 10 2014 Simone Caronni <negativo17@gmail.com> - 0.10-7.svn6439
- Update to SVN revision 6439.

* Fri Oct 03 2014 Simone Caronni <negativo17@gmail.com> - 0.10-6.svn6422
- Update to SVN revision 6430.

* Sun Sep 28 2014 Simone Caronni <negativo17@gmail.com> - 0.10-5.svn6422
- Update to SVN revision 6422.

* Mon Sep 08 2014 Simone Caronni <negativo17@gmail.com> - 0.10-4.svn6404
- Update to SVN revision 6404.
- Update libdvdread and libdvdnav requirements.

* Mon Sep 08 2014 Simone Caronni <negativo17@gmail.com> - 0.10-3.svn6394
- Update to SVN revision 6394.

* Mon Sep 01 2014 Simone Caronni <negativo17@gmail.com> - 0.10-2.svn6386
- Update to svn revision 6386; new x265 presets.
- Update x265 libraries.

* Sat Aug 23 2014 Simone Caronni <negativo17@gmail.com> - 0.9.9-17.svn6304
- Update to svn revision 6351. HandBrake version is now 0.10:
  https://trac.handbrake.fr/milestone/HandBrake%200.10
- Lame and x264 libraries are now linked by default.
- Remove mkv, mpeg2dec and libmkv as they are no longer used.
- LibAV is now enabled by default.
- Add libappindicator-gtk3 build requirement.

* Sun Aug 17 2014 Simone Caronni <negativo17@gmail.com> - 0.9.9-16.svn6304
- Update to 6304 snapshot.

* Wed Aug 06 2014 Simone Caronni <negativo17@gmail.com> - 0.9.9-15.svn6268
- Update to latest snapshot.

* Wed Jul 30 2014 Simone Caronni <negativo17@gmail.com> - 0.9.9-14.svn6244
- Updated to latest snapshot.
- Enable avformat muxer, replaces libmkv and mp4v2 support.
- Requires libdvdnav >= 5.0.0 to fix crashes.
- Remove ExclusiveArch.

* Sat Jul 05 2014 Simone Caronni <negativo17@gmail.com> - 0.9.9-13.svn6227
- Updated to SVN snapshot.
- Remove RHEL 6 conditionals.

* Tue Mar 25 2014 Simone Caronni <negativo17@gmail.com> - 0.9.9-12
- Backport DVD changes from trunk (should fix libdvdnav crashes with specific
  DVD titles).
- Use system ffpmeg 2 libraries in place of bundled libav.

* Mon Mar 17 2014 Simone Caronni <negativo17@gmail.com> - 0.9.9-11
- Fix crash on Fedora.

* Fri Mar 14 2014 Simone Caronni <negativo17@gmail.com> - 0.9.9-10
- Use system libdvdnav/libdvdread.

* Mon Dec 23 2013 Simone Caronni <negativo17@gmail.com> - 0.9.9-9
- Use system libraries for libbluray, lame, mpeg2dec, a52dec (patch), libmkv
  (patch), x264 (faac, fdk-aac, libav, libdvdnav, libdvdread and mp4v2 are still
  bundled).
- Use Fedora compiler options.
- Use GStreamer 1.x on Fedora and RHEL/CentOS 7.
- Add fdk-aac support.

* Mon Dec 23 2013 Simone Caronni <negativo17@gmail.com> - 0.9.9-8
- Scriptlets need to run for gui subpackage and not base package. Thanks to
  Peter Oliver.

* Mon Sep 09 2013 Simone Caronni <negativo17@gmail.com> - 0.9.9-7
- Add requirement on libdvdcss, fix hicolor-icon-theme requirement.

* Fri Jul 26 2013 Simone Caronni <negativo17@gmail.com> - 0.9.9-6
- Enable building CLI only on CentOS/RHEL 6.
- Disable GTK update checks (updates come only packaged).

* Tue Jul 23 2013 Simone Caronni <negativo17@gmail.com> - 0.9.9-5
- Enable command line interface only for CentOS/RHEL 6.

* Thu May 30 2013 Simone Caronni <negativo17@gmail.com> - 0.9.9-4
- Updated x264 to r2282-1db4621 (stable branch) to fix Fedora 19 crash issues.

* Mon May 20 2013 Simone Caronni <negativo17@gmail.com> - 0.9.9-3
- Update to 0.9.9.
- Separate GUI and CLI packages.

* Sat May 11 2013 Simone Caronni <negativo17@gmail.com> - 0.9.9-2.5449svn
- Updated.

* Wed May 01 2013 Simone Caronni <negativo17@gmail.com> - 0.9.9-1.5433svn
- First build.
