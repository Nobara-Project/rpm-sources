%global _lto_cflags %{nil}

%global         codecdir %{_libdir}/codecs
%global         pre 20250127svn
%global         svn 1
%global         svnbuild 2025-01-27

Name:           mplayer
Version:        1.5.1
%if 0%{?svn}
Release:        0.17%{?pre:.%{pre}}%{?dist}
%else
Release:        17%{?dist}
%endif
Summary:        Movie player playing most video formats and DVDs

%if 0%{!?_without_amr:1}
License:        GPLv3+
%else
License:        GPLv2+
%endif
URL:            https://www.mplayerhq.hu/
%if 0%{?svn}
# run ./mplayer-snapshot.sh to get this
Source0:        mplayer-export-%{svnbuild}.tar.xz
%else
Source0:        https://www.mplayerhq.hu/MPlayer/releases/MPlayer-%{version}%{?pre}.tar.xz
%endif
Source10:       mplayer-snapshot.sh
# set defaults for Fedora
Patch0:         %{name}-config.patch
# use roff include statements instead of symlinks
Patch1:         %{name}-manlinks.patch
# use system FFmpeg libraries
Patch2:         %{name}-ffmpeg.patch
Patch3:         0204_fix-ftbfs-jack-ffmpeg7.patch

BuildRequires:  SDL-devel
BuildRequires:  a52dec-devel
BuildRequires:  aalib-devel
BuildRequires:  alsa-lib-devel
BuildRequires:  bzip2-devel
BuildRequires:  enca-devel
BuildRequires:  ffmpeg-devel
BuildRequires:  fontconfig-devel
BuildRequires:  freetype-devel >= 2.0.9
BuildRequires:  fribidi-devel
BuildRequires:  gcc-c++
BuildRequires:  giflib-devel
BuildRequires:  gsm-devel
BuildRequires:  jack-audio-connection-kit-devel
BuildRequires:  ladspa-devel
BuildRequires:  lame-devel
BuildRequires:  libGL-devel
BuildRequires:  libXinerama-devel
BuildRequires:  libXScrnSaver-devel
BuildRequires:  libXv-devel
BuildRequires:  libXxf86vm-devel
BuildRequires:  libass-devel >= 0.9.10
BuildRequires:  libbluray-devel
BuildRequires:  libbs2b-devel
BuildRequires:  libcaca-devel
BuildRequires:  libcdio-paranoia-devel
BuildRequires:  libdvdnav-devel >= 4.1.3-1
BuildRequires:  libjpeg-devel
BuildRequires:  librtmp-devel
BuildRequires:  libtheora-devel
BuildRequires:  libvdpau-devel
BuildRequires:  libvorbis-devel
BuildRequires:  lirc-devel
BuildRequires:  lzo-devel >= 2
BuildRequires:  perl-generators
BuildRequires:  pulseaudio-libs-devel
BuildRequires:  speex-devel >= 1.1
BuildRequires:  twolame-devel
BuildRequires:  x264-devel >= 0.0.0-0.28
BuildRequires:  xvidcore-devel >= 0.9.2
BuildRequires:  nasm
%{?_with_a52dec:BuildRequires:  a52dec-devel}
%{?_with_arts:BuildRequires: arts-devel}
%{?_with_dga:BuildRequires: libXxf86dga-devel}
%{?_with_esound:BuildRequires: esound-devel}
%{?_with_faac:BuildRequires:  faac-devel}
%{?_with_faad:BuildRequires:  faad2-devel}
%{?_with_dca:BuildRequires:  libdca-devel}
%{?_with_libmad:BuildRequires:  libmad-devel}
%{?_with_libmpcdec:BuildRequires:  libmpcdec-devel}
%{?_with_libmpeg2:BuildRequires:  libmpeg2-devel}
%{?_with_libmpg123:BuildRequires:  libmpg123-devel}
%{?_with_openal:BuildRequires: openal-soft-devel}
%{?_with_samba:BuildRequires: libsmbclient-devel}
%{?_with_svgalib:BuildRequires: svgalib-devel}
%{?_with_xmms:BuildRequires: xmms-devel}
%if 0%{?svn}
# for XML docs, SVN only
BuildRequires:  docbook-dtds
BuildRequires:  docbook-style-xsl
BuildRequires:  libxml2
BuildRequires:  libxslt
%endif
Requires:       mplayer-common = %{version}-%{release}
Provides:       mplayer-backend
Obsoletes:      mplayer-gui <= %{version}-%{release}

%description
MPlayer is a movie player that plays most MPEG, VOB, AVI, OGG/OGM,
VIVO, ASF/WMA/WMV, QT/MOV/MP4, FLI, RM, NuppelVideo, yuv4mpeg, FILM,
RoQ, and PVA files. You can also use it to watch VCDs, SVCDs, DVDs,
3ivx, RealMedia, and DivX movies.
It supports a wide range of output drivers including X11, XVideo, DGA,
OpenGL, SVGAlib, fbdev, AAlib etc. There are also nice
antialiased shaded subtitles and OSD.
The following on-default rpmbuild options are available:
--with samba:   Enable Samba (smb://) support
--with xmms:    Enable XMMS input plugin support
--with a52dec:  Enable a52dec support
--without amr:  Disable AMR support
--with dca:     Enable libdca support
--with faac:    Enable FAAC support
--with faad:    Enable FAAD support
--with dv:      Enable libdv support
--with libmad:  Enable libmad support
--with libmpeg2:Enable libmpeg2 support
--with libmpg123:Enable libmpg123 support
--with openal:  Enable OpenAL support
--with arts:    Enable aRts support
--with esound:  Enable EsounD support
--with dga:     Enable DGA support
--with svgalib: Enable SVGAlib support

%package        common
Summary:        MPlayer common files

%description    common
This package contains common files for MPlayer packages.

%package     -n mencoder
Summary:        MPlayer movie encoder
Requires:       mplayer-common = %{version}-%{release}

%description -n mencoder
This package contains the MPlayer movie encoder. 

%package        doc
Summary:        MPlayer documentation in various languages

%description    doc
MPlayer documentation in various languages.

%package        tools
Summary:        Useful scripts for MPlayer
Requires:       mencoder%{?_isa} = %{version}-%{release}
Requires:       mplayer%{?_isa} = %{version}-%{release}

%description    tools
This package contains various scripts from MPlayer TOOLS directory.

%define mp_configure \
./configure \\\
    --prefix=%{_prefix} \\\
    --bindir=%{_bindir} \\\
    --datadir=%{_datadir}/mplayer \\\
    --mandir=%{_mandir} \\\
    --confdir=%{_sysconfdir}/mplayer \\\
    --libdir=%{_libdir} \\\
    --codecsdir=%{codecdir} \\\
    \\\
    --extra-cflags="$RPM_OPT_FLAGS" \\\
    --language=all \\\
    \\\
    --enable-joystick \\\
    --enable-lirc \\\
    --enable-menu \\\
    --enable-radio \\\
    --enable-radio-capture \\\
%ifarch %{ix86} x86_64 %{power64} \
    --enable-runtime-cpudetection \\\
%endif \
    --enable-unrarexec \\\
    \\\
    %{!?_with_samba:--disable-smb} \\\
    \\\
    --disable-ffmpeg_a \\\
    \\\
    %{!?_with_a52dec:--disable-liba52} \\\
    %{?_without_amr:--disable-libopencore_amrnb --disable-libopencore_amrwb} \\\
    %{!?_with_faac:--disable-faac} \\\
    %{!?_with_faad:--disable-faad} \\\
    %{!?_with_dca:--disable-libdca} \\\
    %{!?_with_dv:--disable-libdv} \\\
    %{!?_with_libmad:--disable-mad} \\\
    %{?_with_libmpcdec:--enable-musepack} \\\
    --disable-libmpeg2-internal \\\
    %{!?_with_libmpeg2:--disable-libmpeg2} \\\
    %{!?_with_libmpg123:--disable-mpg123} \\\
    %{?_with_xmms:--enable-xmms} \\\
    %{?_with_xmms:--with-xmmslibdir=%{_libdir}} \\\
    \\\
    --disable-bitmap-font \\\
    %{!?_with_dga:--disable-dga1 --disable-dga2} \\\
    %{!?_with_svgalib:--disable-svga} \\\
    --disable-termcap \\\
    \\\
    %{!?_with_arts:--disable-arts} \\\
    %{!?_with_esound:--disable-esd} \\\
    %{!?_with_openal:--disable-openal} \\\
    --disable-live \\\


%prep
%if 0%{?svn}
%setup -q -n mplayer-export-%{svnbuild}
%else
%setup -q -n MPlayer-%{version}%{?pre}
rm -rf ffmpeg
%endif
%patch -P 0 -p1 -b .config
%patch -P 1 -p1 -b .manlinks
%patch -P 2 -p1 -b .ffmpeg
%patch -P 3 -p1 -b .ffmpeg7

sed -i '1s=^#! */usr/bin/\(python\|env python\)[23]\?=#!%{__python3}=' TOOLS/{mphelp_check,vobshift}.py

%build
export CC=gcc
export CXX=g++
%{mp_configure}

%make_build V=1

%if 0%{?svn}
# build HTML documentation from XML files 
%make_build V=1 html-chunked
%endif

%install
rm -rf $RPM_BUILD_ROOT doc

%make_install INSTALLSTRIP=
for file in aconvert.sh divx2svcd.sh mencvcd.sh midentify.sh mpconsole.sh qepdvcd.sh subsearch.sh ; do
install -pm 755 TOOLS/$file $RPM_BUILD_ROOT%{_bindir}/`basename $file .sh`
done

for file in calcbpp.pl countquant.pl dvd2divxscript.pl ; do
install -pm 755 TOOLS/$file $RPM_BUILD_ROOT%{_bindir}/`basename $file .pl`
done

for file in vobshift.py ; do
install -pm 755 TOOLS/$file $RPM_BUILD_ROOT%{_bindir}/`basename $file .py`
done

mkdir -p $RPM_BUILD_ROOT%{_datadir}/mplayer
install -pm 644 TOOLS/*.fp $RPM_BUILD_ROOT%{_datadir}/mplayer/

# Clean up documentation
mkdir doc
cp -pR DOCS/* doc/
rm -r doc/man doc/xml doc/README
mv doc/HTML/* doc/
rm -rf doc/HTML

# Default config files
install -Dpm 644 etc/example.conf \
    $RPM_BUILD_ROOT%{_sysconfdir}/mplayer/mplayer.conf

install -pm 644 etc/{input,menu}.conf $RPM_BUILD_ROOT%{_sysconfdir}/mplayer/

# Codec dir
install -dm 755 $RPM_BUILD_ROOT%{codecdir}
sed -i '1s:#!/usr/bin/env python:#!/usr/bin/env python2:' %{buildroot}%{_bindir}/vobshift

%find_lang %{name} --with-man
%find_lang mencoder --with-man

%files
%{_bindir}/mplayer

%files common -f mplayer.lang
%license LICENSE
%doc AUTHORS Changelog Copyright README
%dir %{_sysconfdir}/mplayer
%config(noreplace) %{_sysconfdir}/mplayer/mplayer.conf
%config(noreplace) %{_sysconfdir}/mplayer/input.conf
%config(noreplace) %{_sysconfdir}/mplayer/menu.conf
%dir %{codecdir}/
%dir %{_datadir}/mplayer/
%{_mandir}/man1/mplayer.1*

%files -n mencoder -f mencoder.lang
%{_bindir}/mencoder
%{_mandir}/man1/mencoder.1*

%files doc
%doc doc/en/ doc/tech/
%lang(cs) %doc doc/cs/
%lang(de) %doc doc/de/
%lang(es) %doc doc/es/
%lang(fr) %doc doc/fr/
%lang(hu) %doc doc/hu/
%lang(pl) %doc doc/pl/
%lang(ru) %doc doc/ru/
%lang(zh_CN) %doc doc/zh_CN/

%files tools
%{_bindir}/aconvert
%{_bindir}/calcbpp
%{_bindir}/countquant
%{_bindir}/divx2svcd
%{_bindir}/dvd2divxscript
%{_bindir}/mencvcd
%{_bindir}/midentify
%{_bindir}/mpconsole
%{_bindir}/qepdvcd
%{_bindir}/subsearch
%{_bindir}/vobshift
%{_datadir}/mplayer/*.fp

%changelog
* Mon Jan 27 2025 Leigh Scott <leigh123linux@gmail.com> - 1.5.1-0.17.20250127svn
- Update snapshot

* Tue Oct 08 2024 Nicolas Chauvet <kwizart@gmail.com> - 1.5.1-0.16.20241008svn
- Update snapshot

* Fri Aug 02 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.5.1-0.15.20240415svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Apr 15 2024 Leigh Scott <leigh123linux@gmail.com> - 1.5.1-0.14.20240415svn
- Update snapshot to fix AVChannelLayout issue (rfbz#6911)

* Tue Apr 09 2024 Leigh Scott <leigh123linux@gmail.com> - 1.5.1-0.13.20240409svn
- Update snapshot to fix AVChannelLayout issue (rfbz#6911)

* Mon Mar 18 2024 Leigh Scott <leigh123linux@gmail.com> - 1.5.1-0.12.20240317svn
- Drop GUI

* Sun Mar 17 2024 Leigh Scott <leigh123linux@gmail.com> - 1.5.1-0.11.20240317svn
- Update snapshot
- Readd GUI

* Sun Feb 04 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.5.1-0.10.20230811svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Jan 09 2024 Leigh Scott <leigh123linux@gmail.com> - 1.5.1-0.9.20230811svn
- Use compat-ffmpeg5

* Fri Aug 11 2023 Leigh Scott <leigh123linux@gmail.com> - 1.5.1-0.8.20230811svn
- Update snapshot
- Drop GUI

* Wed Aug 02 2023 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.5.1-0.7.20230530svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue May 30 2023 Leigh Scott <leigh123linux@gmail.com> - 1.5.1-0.6.20230530svn
- Drop requires ffmpeg-libs

* Tue May 30 2023 Leigh Scott <leigh123linux@gmail.com> - 1.5.1-0.5.20230530svn
- Use compat-ffmpeg4 as mplayer doesn't support ffmpeg-6.0 (rfbz#6692)

* Tue Feb 28 2023 Leigh Scott <leigh123linux@gmail.com> - 1.5.1-0.4.20230228svn
- Rebuild for new ffmpeg

* Tue Nov 22 2022 Leigh Scott <leigh123linux@gmail.com> - 1.5.1-0.3.20220726svn
- Fix rfbz#6500

* Sun Sep 04 2022 Leigh Scott <leigh123linux@gmail.com> - 1.5.1-0.2.20220726svn
- Add requires ffmpeg-libs

* Sat Aug 06 2022 Leigh Scott <leigh123linux@gmail.com> - 1.5.1-0.1.20220726svn
- Update to latest svn

* Sun Jun 12 2022 Sérgio Basto <sergio@serjux.com> - 1.5-2
- Mass rebuild for x264-0.164

* Mon Feb 28 2022 Leigh Scott <leigh123linux@gmail.com> - 1.5-1
- Update to 1.5 release

* Wed Feb 09 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.4.1-0.6.20211109svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Nov 09 2021 Leigh Scott <leigh123linux@gmail.com> - 1.4.1-0.5.20211109svn
- Update to latest svn

* Tue Nov 09 2021 Leigh Scott <leigh123linux@gmail.com> - 1.4.1-0.4.20210313svn
- Rebuilt for new ffmpeg snapshot

* Tue Aug 03 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.4.1-0.3.20210313svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sun Jul 11 2021 Sérgio Basto <sergio@serjux.com> - 1.4.1-0.2.20210313svn
- Mass rebuild for x264-0.163

* Sat Mar 13 2021 Leigh Scott <leigh123linux@gmail.com> - 1.4.1-0.1.20210313svn
- Update to latest svn

* Wed Feb 03 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.4-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Dec 31 2020 Leigh Scott <leigh123linux@gmail.com> - 1.4-14
- Rebuilt for new ffmpeg snapshot

* Fri Nov 27 2020 Sérgio Basto <sergio@serjux.com> - 1.4-13
- Mass rebuild for x264-0.161

* Wed Oct 21 2020 Leigh Scott <leigh123linux@gmail.com> - 1.4-12
- Rebuild for new libdvdread

* Tue Aug 18 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.4-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 07 2020 Sérgio Basto <sergio@serjux.com> - 1.4-10
- Mass rebuild for x264

* Fri Apr 17 2020 Leigh Scott <leigh123linux@gmail.com> - 1.4-9
- Add AV1 support

* Fri Apr 10 2020 Leigh Scott <leigh123linux@gmail.com> - 1.4-8
- Rebuild for new libcdio version

* Sat Feb 22 2020 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 1.4-7
- Rebuild for ffmpeg-4.3 git

* Wed Feb 05 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Dec 17 2019 Leigh Scott <leigh123linux@gmail.com> - 1.4-5
- Mass rebuild for x264

* Fri Nov 15 2019 Dominik 'Rathann' Mierzejewski <rpm@greysector.net> - 1.4-4
- rebuild for libdvdread ABI bump

* Wed Aug 21 2019 Leigh Scott <leigh123linux@gmail.com> - 1.4-3
- Drop XvMC support (rfbz #5328)

* Tue Aug 06 2019 Leigh Scott <leigh123linux@gmail.com> - 1.4-2
- Rebuild for new ffmpeg version

* Fri Apr 19 2019 Leigh Scott <leigh123linux@googlemail.com> - 1.4-1
- Update to 1.4 release

* Tue Apr 16 2019 Leigh Scott <leigh123linux@googlemail.com> - 1.3.0-29.20190416svn
- Update to latest svn

* Tue Mar 12 2019 Sérgio Basto <sergio@serjux.com> - 1.3.0-28.20180620svn.2
- Mass rebuild for x264

* Mon Mar 04 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.3.0-28.20180620svn.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 23 2019 Dominik Mierzejewski <rpm@greysector.net> - 1.3.0-28.20180620svn
- Use HTTPS for URLs
- Drop obsolete stuff
- Make dependencies which duplicate existing FFmpeg features optional by default
- Generate manpage translation list automatically
- Use license macro
- Enable JACK support by default (rfbz #4556)

* Mon Nov 12 2018 Antonio Trande <sagitter@fedoraproject.org> - 1.3.0-27.20180620svn
- Rebuild for ffmpeg-3.4.5 on el7
- Rebuild for x264-0.148 on el7
- Add icon-cache scriptlets for epel only

* Thu Oct 04 2018 Sérgio Basto <sergio@serjux.com> - 1.3.0-26.20180620svn
- Mass rebuild for x264 and/or x265
- Fix sources
- Add BuildRequires: gcc-c++
- Fix ambiguous python shebang

* Fri Jul 27 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.3.0-25.20180620svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 20 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.3.0-24.20180620svn
- Update to latest svn
- Enable runtime cpu detection for i686 again

* Sun Jun 17 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.3.0-23.20180424svn
- Rebuild for new libass version

* Tue Apr 24 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.3.0-22.20180424svn
- Update to latest svn

* Tue Apr 24 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.3.0-21.20180119svn
- Rebuild for ffmpeg-4.0 release

* Thu Mar 08 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 1.3.0-20.20180119svn
- Rebuilt for new ffmpeg snapshot

* Mon Mar 05 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.3.0-19.20180119svn
- Disable runtime cpu detection for i686
- Remove scriptlets

* Thu Mar 01 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 1.3.0-18.20180119svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Jan 28 2018 Nicolas Chauvet <kwizart@gmail.com> - 1.3.0-17.20180119svn
- Rebuilt for libcdio

* Fri Jan 19 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.3.0-16.20180119svn
- Update to latest svn

* Thu Jan 18 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.3.0-15
- Rebuilt for ffmpeg-3.5 git

* Sun Dec 31 2017 Sérgio Basto <sergio@serjux.com> - 1.3.0-14
- Mass rebuild for x264 and x265

* Mon Oct 23 2017 Leigh Scott <leigh123linux@googlemail.com> - 1.3.0-13
- Exclude ix86 (rfbz #4687)

* Tue Oct 17 2017 Leigh Scott <leigh123linux@googlemail.com> - 1.3.0-12
- Rebuild for ffmpeg update
- Add build upstream build fix for newer ffmpeg

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 1.3.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Jul 15 2017 Paul Howarth <paul@city-fan.org> - 1.3.0-10
- Perl 5.26 rebuild

* Sat Apr 29 2017 Leigh Scott <leigh123linux@googlemail.com> - 1.3.0-9
- Rebuild for ffmpeg update

* Mon Mar 20 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 1.3.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Mar 03 2017 Leigh Scott <leigh123linux@googlemail.com> - 1.3.0-7
- Fix vo_png with recent ffmpeg (rfbz#4470)

* Mon Feb 06 2017 Leigh Scott <leigh123linux@googlemail.com> - 1.3.0-6
- Fix screenshot crash (rfbz#4391)

* Thu Nov 17 2016 Adrian Reber <adrian@lisas.de> - 1.3.0-5
- Rebuilt for libcdio-0.94

* Sat Nov 05 2016 Leigh Scott <leigh123linux@googlemail.com> - 1.3.0-4
- Add provides mplayer-backend (rfbz#4284)
- Rebuilt for new ffmpeg

* Tue Oct 25 2016 Paul Howarth <paul@city-fan.org> - 1.3.0-3
- BR: perl-generators for proper dependency generation
  (https://fedoraproject.org/wiki/Changes/Build_Root_Without_Perl)

* Sat Jul 30 2016 Julian Sikorski <belegdol@fedoraproject.org> - 1.3.0-2
- Rebuilt for ffmpeg-3.1.1

* Wed May 18 2016 Julian Sikorski <belegdol@fedoraproject.org> - 1.3.0-1
- Updated to 1.3.0

* Sat Apr 02 2016 Julian Sikorski <belegdol@fedoraproject.org> - 1.2.1-2
- Fixed BuildRequires so that audio CD support actually works

* Thu Jan 28 2016 Julian Sikorski <belegdol@fedoraproject.org> - 1.2.1-1
- Updated to 1.2.1
- Removed asm.h from mplayer-ffmpeg.patch

* Thu Oct 29 2015 Julian Sikorski <belegdol@fedoraproject.org> - 1.2-1
- Updated to 1.2
- Updated Blue skin to 1.11

* Thu May 07 2015 Julian Sikorski <belegdol@fedoraproject.org> - 1.1-33.20150505svn
- 20150505 snapshot
- Updated ffmpeg patch

* Sat Jan 31 2015 Julian Sikorski <belegdol@fedoraproject.org> - 1.1-32.20150123svn
- 20150123 snapshot
- Internal libdvd* are no more, cleaned up the spec accordingly

* Tue Oct 21 2014 Julian Sikorski <belegdol@fedoraproject.org> - 1.1-31.20141020svn
- 20141020 snapshot

* Mon Oct 20 2014 Sérgio Basto <sergio@serjux.com> - 1.1-30.20140919svn
- Rebuilt for FFmpeg 2.4.3

* Wed Oct 01 2014 Sérgio Basto <sergio@serjux.com> - 1.1-29.20140919svn
- Rebuilt again for FFmpeg 2.3.x (with FFmpeg 2.3.x in buildroot)

* Sat Sep 27 2014 kwizart <kwizart@gmail.com> - 1.1-28.20140919svn
- Rebuilt for FFmpeg 2.3x

* Thu Sep 25 2014 Julian Sikorski <belegdol@fedoraproject.org> - 1.1-27.20140919svn
- 20140919 snapshot

* Wed Aug 06 2014 Julian Sikorski <belegdol@fedoraproject.org> - 1.1-26.20140806svn
- 20140806 snapshot

* Sat Jul 12 2014 Julian Sikorski <belegdol@fedoraproject.org> - 1.1-25.20140711svn
- 20140711 snapshot

* Thu Mar 27 2014 Julian Sikorski <belegdol@fedoraproject.org> - 1.1-24.20140327svn
- 20140327 snapshot

* Fri Mar 21 2014 Julian Sikorski <belegdol@fedoraproject.org> - 1.1-23.20140301svn
- Rebuilt for libass-0.10.2

* Tue Mar 18 2014 Julian Sikorski <belegdol@fedoraproject.org> - 1.1-22.20140301svn
- Rebuilt for x264

* Thu Mar 06 2014 Nicolas Chauvet <kwizart@gmail.com> - 1.1-21.20140301svn
- Rebuilt for x264

* Sat Mar 01 2014 Julian Sikorski <belegdol@fedoraproject.org> - 1.1-20.20140301svn
- 20140301 snapshot

* Tue Feb 11 2014 Julian Sikorski <belegdol@fedoraproject.org> - 1.1-19.20140211svn
- 20140211 snapshot

* Sun Jan 12 2014 Julian Sikorski <belegdol@fedoraproject.org> - 1.1-18.20140111svn
- 20140111 snapshot

* Tue Jan 07 2014 Nicolas Chauvet <kwizart@gmail.com> - 1.1-17.20131125svn
- Rebuilt for librtmp

* Thu Nov 28 2013 Julian Sikorski <belegdol@fedoraproject.org> - 1.1-16.20131125svn
- 20131125 snapshot

* Sat Nov 02 2013 Julian Sikorski <belegdol@fedoraproject.org> - 1.1-15.20131102svn
- 20131102 snapshot

* Tue Oct 22 2013 Nicolas Chauvet <kwizart@gmail.com> - 1.1-14.20130811svn
- Rebuilt for x264

* Tue Aug 13 2013 Julian Sikorski <belegdol@fedoraproject.org> - 1.1-13.20130811svn
- 20130811 snapshot

* Thu Aug 01 2013 Julian Sikorski <belegdol@fedoraproject.org> - 1.1-12.20130801svn
- 20130801 snapshot
- Updated the ffmpeg patch
- Re-numbered the patches

* Sat Jul 20 2013 Nicolas Chauvet <kwizart@gmail.com> - 1.1-11.20130416svn
- Rebuilt for x264

* Fri Jun 07 2013 Julian Sikorski <belegdol@fedoraproject.org> - 1.1-10.20130416svn
- Fixed cpu detection (mplayer #2141)

* Wed May 08 2013 Julian Sikorski <belegdol@fedoraproject.org> - 1.1-9.20130416svn
- Fixed dangerous playlist parsing

* Mon May 06 2013 Julian Sikorski <belegdol@fedoraproject.org> - 1.1-8.20130416svn
- Rebuilt for x264-0.130

* Sun Apr 21 2013 Julian Sikorski <belegdol@fedoraproject.org> - 1.1-7.20130416svn
- 20130416 snapshot

* Thu Mar 28 2013 Julian Sikorski <belegdol@fedoraproject.org> - 1.1-6.20130329svn
- 20130329 snapshot
- Updated the nodvdcss patch
- Updated the ffmpeg patch
- Dropped em8300-devel BR since the package was retired in Fedora

* Sun Feb 03 2013 Julian Sikorski <belegdol@fedoraproject.org> - 1.1-5.20130123svn
- 20130123 snapshot
- Updated the nodvdcss patch
- Updated the ffmpeg patch

* Fri Nov 23 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.1-4.20121008svn
- Rebuilt for x264

* Sat Oct 20 2012 Julian Sikorski <belegdol@fedoraproject.org> - 1.1-3.20121008svn
- 20121008 snapshot
- Internal tremor copy is no more
- Dropped the included gmplayer subtitles patch 

* Wed Sep 05 2012 Nicolas Chauvet <kwizart@gmail.com>
- Rebuilt for x264 ABI 125
- Use --cpu-runtime-detection only on supported arches - rfbz#2467

* Sun Jun 24 2012 Julian Sikorski <belegdol@fedoraproject.org> - 1.1-1
- Updated to 1.1
- Made %%pre, %%svn and %%svnbuild defines optional
- Switched to .xz sources
- Updated the ffmpeg patch

* Wed Jun 13 2012 Julian Sikorski <belegdol@fedoraproject.org> - 1.0-0.139.20120205svn
- Restored the ability to disable subtitles in gmplayer (RPM Fusion bug #2373)
- Rebuilt for ffmpeg-0.10.4
- Fix BR to pulseaudio-libs-devel

* Mon May 07 2012 Julian Sikorski <belegdol@fedoraproject.org> - 1.0-0.138.20120205svn
- Rebuilt for ffmpeg-0.10.3

* Fri May 04 2012 Nicolas Chauvet <kwizart@gmail.com>  - 1.0-0.137.20120205svn
- Disable live (broken) - See libnemesi as an alternative

* Sun Mar 18 2012 Julian Sikorski <belegdol@fedoraproject.org> - 1.0-0.135.20120205svn
- Rebuilt for ffmpeg-0.10.2

* Tue Mar 13 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.0-0.134.20120205svn
- Rebuilt for x264 ABI 0.120

* Sun Mar 11 2012 Dominik Mierzejewski <rpm@greysector.net> - 1.0-0.133.20120205svn
- drop libvpx build requirement (unused due to shared FFmpeg)
- trim patch for shared FFmpeg support to minimum
- replace cdparanoia with libcdio for better CD-Audio support
- add conditional to enable libmpcdec (disabled upstream by default)

* Wed Feb 29 2012 Julian Sikorski <belegdol@fedoraproject.org> - 1.0-0.132.20120205svn
- 20120205 snapshot

* Mon Feb 27 2012 Julian Sikorski <belegdol@fedoraproject.org> - 1.0-0.131.20120204svn
- Added libbs2b-devel to BuildRequires (RPM Fusion bug #2157)
- Fixed --with directfb (RPM Fusion bug #2141)
- Don't mangle the manpages (RPM Fusion bug #1994)
- Fixed man links (RPM Fusion bug #1625)

* Mon Feb 27 2012 Julian Sikorski <belegdol@fedoraproject.org> - 1.0-0.130.20120204svn
- 20120204 snapshot
- Dropped obsolete Group, Buildroot, %%clean and %%defattr
- Updated the ffmpeg patch
- Updated Blue skin to 1.8
- Building documentation is now done from the top-level Makefile
- Icons now come in different sizes

* Fri Jan 27 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.0-0.129.20110816svn
- Rebuilt for live555

* Tue Jan 10 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.0-0.128.20110816svn
- Rebuild for FFmpeg

* Mon Jan 02 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.0-0.127.20110816svn
- Rebuild for new ffmpeg

* Fri Sep 23 2011 Dominik Mierzejewski <rpm at greysector.net> - 1.0-0.126.20110816svn
- 20110816 snapshot
- drop obsolete pause crash patch
- re-enable mp3lib decoder
- enable libmpg123 decoder

* Fri Jul 15 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.0-0.125.20110412svn
- Rebuilt for x264 ABI 115

* Thu Jun 16 2011 Ricky Zhou <ricky@rzhou.org> - 1.0-0.124.20110412svn
- Add upstream patch for pause crash.

* Tue Apr 12 2011 Dominik Mierzejewski <rpm at greysector.net> - 1.0-0.123.20110412svn
- 20110412 snapshot
- drop obsolete libvorbis patch
- add explanatory comments to all patches
- temporarily disable mp3lib decoder (workaround for bug #1680)

* Sun Mar 27 2011 Dominik Mierzejewski <rpm at greysector.net> - 1.0-0.122.20110227svn
- 20110227 snapshot
- rebuilt for new ffmpeg and x264

* Sun Mar 27 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.0-0.121.20110110svn
- Rebuild for x264

* Mon Jan 10 2011 Dominik Mierzejewski <rpm at greysector.net> - 1.0-0.120.20110110svn
- 20110110 snapshot
- enabled BluRay, bzip2, libgsm, rtmp support
- DGA support is now a build-time option
- build against system FFmpeg (experimental!)
  (drop direct opencore-amr and schroedinger linking)

* Sat Jul 03 2010 Dominik Mierzejewski <rpm at greysector.net> - 1.0-0.119.20100703svn
- rebuild against latest x264

* Sat Jul 03 2010 Dominik Mierzejewski <rpm at greysector.net> - 1.0-0.118.20100703svn
- 20100703 snapshot
- dropped obsolete libgif patch
- enabled libvpx support
- enabled external libmpeg2 (internal copy is scheduled to be dropped by upstream)

* Thu May 06 2010 Nicolas Chauvet <kwizart@fedoraproject.org> - 1.0-0.117.20100429svn
- Rebuilt for live555

* Thu Apr 29 2010 Dominik Mierzejewski <rpm at greysector.net> - 1.0-0.116.20100429svn
- 20100429 snapshot
- drop unnecessary patches

* Sat Apr 24 2010 Dominik Mierzejewski <rpm at greysector.net> - 1.0-0.115.20100424svn
- 20100424 snapshot
- patch to build against older x264

* Sat Mar 27 2010 Dominik Mierzejewski <rpm at greysector.net> - 1.0-0.114.20100327svn
- 20100327 snapshot
- drop unused patch
- fix build on F-13+ by linking against libgif instead of libungif

* Thu Jan 28 2010 Nicolas Chauvet <kwizart@fedoraproject.org> - 1.0-0.113.20100116svn
- Rebuild for live555

* Sat Jan 16 2010 Dominik Mierzejewski <rpm at greysector.net> - 1.0-0.112.20100116svn
- 20100116 snapshot
- rebuild against current x264
- fix licence tag when compiled with OpenCore AMR
- fix build --with faac (bug #997)
- enable radio support (bug #634)
- openal-devel is now openal-soft-devel (bug #935)
- move some files to -common subpackage, adjust dependencies (bug #1037)
- introduce -tools subpackage, move scripts there (bugs #544, #1037)

* Thu Oct 29 2009 Dominik Mierzejewski <rpm at greysector.net> - 1.0-0.111.20091029svn
- 20091029 snapshot
- rebuild against current x264
- fix debuginfo generation (bug #101)
- move aconvert to mencoder package (bug #544)
- fix snapshot script not to mangle version string (bug #577)
- disable screensaver by default (bug #672)
- restore and rebase some of the dropped patches
- build against external liba52
- enable dirac decoding via libschroedinger

* Wed Oct 21 2009 kwizart < kwizart at gmail.com > - 1.0-0.110.20091021svn
- Update to snapshot 20091021
  mplayer svn rev: 29776
  ffmpeg : HEAD
  dvdnav : HEAD
- Move from amrnb amrwb to opencore-amr
- Conditionalize faac (moved to nonfree).

* Sun Mar 29 2009 Dominik Mierzejewski <rpm at greysector.net> - 1.0-0.109.20090329svn
- 20090329 snapshot from 1.0rc3 branch
- fix RPM_OPT_FLAGS usage
- drop obsolete patch

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 1.0-0.108.20090319svn
- rebuild for new F11 features

* Thu Mar 19 2009 Dominik Mierzejewski <rpm at greysector.net> - 1.0-0.107.20091319svn
- 20090319 snapshot
- fix HTML docs generation

* Wed Feb 04 2009 Dominik Mierzejewski <rpm at greysector.net> - 1.0-0.106.20090204svn
- 20090204 snapshot
- dropped obsolete patch
- dropped obsolete BR
- dropped redundant altivec CFLAGS on ppc
- fixed build on ppc

* Wed Jan 07 2009 Dominik Mierzejewski <rpm at greysector.net> - 1.0-0.105.20090107svn
- 20090107 snapshot
- dropped .sh extension from shell scripts in %%{_bindir}
- BR: yasm for more asm-optimized routines
- rebased patches

* Thu Dec 18 2008 Dominik Mierzejewski <rpm at greysector.net> - 1.0-0.104.20081218svn
- 20081218 snapshot
- dropped obsolete/upstreamed patches

* Sun Nov 23 2008 Dominik Mierzejewski <rpm at greysector.net> - 1.0-0.103.20080903svn
- fix broken terminal after using dvb input (bug #117)
- disable backing store (fixes tearing on Xorg Xserver 1.5.x)
- disable samba support by default, too much dependency bloat (bug #147)
- add missing Requires for hicolor icon dirs to -gui
- drop provides and obsoletes for mplayer-mencoder (last seen for FC4)

* Tue Oct 28 2008 Dominik Mierzejewski <rpm at greysector.net> - 1.0-0.102.20080903svn
- rework the build system
- rebuild for new libcaca

* Thu Oct 16 2008 Dominik Mierzejewski <rpm at greysector.net> - 1.0-0.101.20080903svn
- remove libdvdcss copy from the source tarball

* Sun Oct 12 2008 Dominik Mierzejewski <rpm at greysector.net> - 1.0-0.100.20080903svn
- backport the fix for CVE-2008-3827

* Tue Sep 09 2008 Dominik Mierzejewski <rpm at greysector.net> - 1.0-0.99.20080903svn
- updated to 20080903 SVN snapshot
- added snapshot creation script
- dropped version sed-patching (happens in the snapshot script now)
- enabled samba support by default

* Tue Aug 19 2008 Dominik Mierzejewski <rpm at greysector.net> - 1.0-0.98.20080818svn
- moved config settings to config patch
- rebased patches against current snapshot

* Mon Aug 18 2008 Dominik Mierzejewski <rpm at greysector.net> - 1.0-0.97.20080818svn
- updated to latest SVN snapshot
- dropped obsolete patches
- installed aconvert.sh to bindir
- fixed zh_CN manpage installation

* Sun Aug 17 2008 Dominik Mierzejewski <rpm at greysector.net> - 1.0-0.96.20080613svn
- live-devel is now live555-devel
- added missing libXScrnSaver-devel BR
- fixed audio in some rtsp streams (backport from SVN)

* Sat Aug 09 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 1.0-0.95.20080613svn
- rebuild

* Sat Jun 14 2008 Dominik Mierzejewski <rpm at greysector.net> - 1.0-0.94.20080613svn
- updated to latest SVN snapshot (bugs #1812, #1910, #1895)
- fixed building with svgalib support
- use pulseaudio output by default
- BR latest libdvdnav
- bring back live (bug #1950), make libnemesi optional
- drop obsolete patches
- fix building against fribidi (bug #1887)
- BR latest x264
- re-enable parallel make

* Sat Mar 15 2008 Thorsten Leemhuis <fedora at leemhuis.info> - 1.0-0.93.20080211svn
- rebuild for new x264

* Mon Feb 11 2008 Dominik Mierzejewski <rpm at greysector.net> - 1.0-0.92.20080211svn
- updated to latest SVN snapshot
- fixed opening files with spaces in their names (bug #1674)
- libnemesi doesn't conflict with live anymore
- fixed samba BR (bug #1809)
- enabled libnemesi by default
- made live optional
- security fixes: CVE-2008-0485, CVE-2008-0486, CVE-2008-0629, CVE-2008-0630
  (bug #1852)

* Mon Dec 03 2007 Dominik Mierzejewski <rpm at greysector.net> - 1.0-0.91.20071201svn
- use correct chanmap patch
- obsolete mplayer-fonts
- require our faad2 2.6.1

* Sat Dec 01 2007 Dominik Mierzejewski <rpm at greysector.net> - 1.0-0.90.20071201svn
- updated to latest SVN snapshot
- reverted a change which requires newer libdvdnav snapshot
- fixed license tag
- use man-links instead of real filesystem symlinks for mencoder.1
- fixed desktop file

* Sun Nov 11 2007 Dominik Mierzejewski <rpm at greysector.net> - 1.0-0.89.rc2
- rebuild against faad2-2.6.1
- drop obsolete patch

* Tue Nov 06 2007 Dominik Mierzejewski <rpm at greysector.net> - 1.0-0.88.rc2
- fixed crash in vorbis decoder (bug #1516)
- added pulseaudio support
- better libnemesi support
- fixed libdca support

* Tue Nov 06 2007 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 1.0-87
- rebuild

* Sat Oct 13 2007 Dominik Mierzejewski <rpm at greysector.net> - 1.0-0.86.rc2
- work around Fedora bug 330031

* Thu Oct 11 2007 Dominik Mierzejewski <rpm at greysector.net> - 1.0-0.85.rc2
- 1.0rc2
- drop obsolete/useless patches
- add experimental audio channel reordering patch
- optional libnemesi support (mutually exclusive with LIVE555)
- revert to internal faad2 (linking with 2.5 makes MPlayer non-distributable)
  but leave a build-time option
- don't rebuild HTML docs for releases
- include Copyright file

* Thu Sep 27 2007 Dominik Mierzejewski <rpm at greysector.net> - 1.0-0.84.20070923svn
- really fix it this time

* Wed Sep 26 2007 Dominik Mierzejewski <rpm at greysector.net> - 1.0-0.83.20070923svn
- fix build on x86_32

* Wed Sep 26 2007 Dominik Mierzejewski <rpm at greysector.net> - 1.0-0.82.20070923svn
- disable parallel make (fails on vidix)
- re-enable external faad2 (fixed in 2.5-4)

* Sun Sep 23 2007 Dominik Mierzejewski <rpm at greysector.net> - 1.0-0.81.20070923svn
- latest snapshot
- update Blue skin
- fix seeking with -demux lavf
- dropped obsolete patches
- Czech manpage is already utf8 (bug #1626)
- fixes CVE-2007-4938 (bug #1645)
- disable external faad, seems broken

* Sat Jul 21 2007 Dominik Mierzejewski <rpm at greysector.net> - 1.0-0.80.20070715svn
- fix build on i386
- another libdca patch update
- fix parallel builds

* Fri Jul 20 2007 Dominik Mierzejewski <rpm at greysector.net> - 1.0-0.79.20070715svn
- fix a crash in subtitle selection code
- updated libdca patch

* Sun Jul 15 2007 Dominik Mierzejewski <rpm at greysector.net> - 1.0-0.78.20070715svn
- latest snapshot
- use external libfaad again
- restore libdca support
- make ad_faad detect the correct sample rate on 64-bit systems
  (based on a patch by Rasmus Rohde)

* Tue Jun 12 2007 Dominik Mierzejewski <rpm at greysector.net> - 1.0-0.77.20070612svn
- latest snapshot
- dropped one obsolete patch
- fixed CVE-2007-2948 (#1525)
- backported compilation fix from r23546
- dropped redundant BR: libpng-devel (brought in by gtk2-devel)

* Tue May 15 2007 Dominik Mierzejewski <rpm at greysector.net> - 1.0-0.75.20070513svn
- BuildRequire the new libdvdnav

* Sun May 13 2007 Dominik Mierzejewski <rpm at greysector.net> - 1.0-0.74.20070513svn
- 20070513 snapshot
- libdha is now static

* Sun Mar 25 2007 Dominik Mierzejewski <rpm at greysector.net> - 1.0-0.72.20070325svn
- 20070325 snapshot
- built with internal libav{codec,format,util}
- dropped obsolete patches

* Sun Mar 18 2007 Dominik Mierzejewski <rpm at greysector.net> - 1.0-0.71.rc1
- fix buffer overflow in DS_VideoDecoder.c (bug #1443)

* Sat Mar 10 2007 Dominik Mierzejewski <rpm at greysector.net> - 1.0-0.70.rc1
- fix buffer overflow in DMO_VideoDecoder.c

* Wed Jan 03 2007 Dominik Mierzejewski <rpm at greysector.net> - 1.0-0.69.rc1                                          
- fix buffer overflow in asmrp.c 

* Thu Dec 28 2006 Dominik Mierzejewski <rpm at greysector.net> - 1.0-0.68.rc1
- don't depend on urw-fonts, use generic Sans font instead

* Tue Dec 26 2006 Dominik Mierzejewski <rpm at greysector.net> - 1.0-0.67.rc1
- disable bitmap fonts
- add libdca support
- add twolame support
- prevent linking mplayer with GUI libs
- make libmad support optional

* Sun Nov  5 2006 Ville Skyttä <ville.skytta at iki.fi> - 1.0-0.66.rc1
- Apply upstream mp3lib workaround instead of disabling 3DNow altogether in it,
  thanks to Dominik 'Rathann' Mierzejewski.

* Tue Oct 31 2006 Ville Skyttä <ville.skytta at iki.fi> - 1.0-0.65.rc1
- 1.0rc1, ffmpeg WMV3 patch applied upstream.
- Include libdvdnav and x264 support.

* Fri Oct 06 2006 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> 1.0-64
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Tue Sep 26 2006 Ville Skyttä <ville.skytta at iki.fi> - 1.0-0.63.pre8
- Rebuild.

* Fri Aug 18 2006 Ville Skyttä <ville.skytta at iki.fi> - 1.0-0.62.pre8
- Enable ffmpeg WMV3 decoder.
- Work around hang when dumping to wav on ix86 (#1127).
- Disable internal tremor due to above workaround making it crashy.
- Disable FriBidi (#612) and joystick (#983) in default config file.
- Specfile/build dependency cleanups.
- Update default Blue skin to 1.6.

* Thu Jul 27 2006 Ville Skyttä <ville.skytta at iki.fi> - 1.0-0.61.pre8
- Move codecs dir to %%{_libdir}/codecs to follow upstream, old location
  in %%{_libdir}/win32 still appears to work as a fallback.
- Ship codecs dir on all architectures again.

* Thu Jul 27 2006 Ville Skyttä <ville.skytta at iki.fi> - 1.0-0.60.pre8
- Make DirectFB support optional, disabled by default (#1102).
- Adapt to lzo2, require it.
- Include midentify (#1105).

* Mon Jun 26 2006 Ville Skyttä <ville.skytta at iki.fi> - 1.0-0.44.pre8
- System wide skins dir has changed to /usr/share/mplayer/skins (#1070).

* Thu Jun 22 2006 Ville Skyttä <ville.skytta at iki.fi> - 1.0-0.42.pre8
- Make arts and esound support optional, disabled by default (#1067).
- Specfile and legacy dependency cleanups.

* Fri Jun 16 2006 Ville Skyttä <ville.skytta at iki.fi> - 1.0-0.40.pre8
- 1.0pre8.
- Drop runtime CPU detection message removal patch.
- Disable XMMS and OpenAL support by default.
- Add support for building with JACK support, disabled by default.
- Don't include the %%{_libdir}/win32 dir on non-x86.
- Fix %%lang tags in -doc.

* Sat May 13 2006 Ville Skyttä <ville.skytta at iki.fi> - 1.0-0.39.20060513
- 2006-05-13 CVS snapshot.
- Make audio output default to ALSA in default config (#970).
- Trim pre-2005 %%changelog entries.

* Sat May 06 2006 Noa Resare <noa@resare.com>
- Move doc to a separate package (#960).

* Sun Apr 16 2006 Ville Skyttä <ville.skytta at iki.fi> - 1.0-0.39.20060412
- Enable Musepack support.

* Thu Apr 13 2006 Ville Skyttä <ville.skytta at iki.fi> - 1.0-0.38.20060412
- 2006-04-12 CVS snapshot.
- Fix 3dnow disabling patch, some parts were erroneously omitted in the
  previous revision (Thomas Jansen).

* Sat Apr  8 2006 Ville Skyttä <ville.skytta at iki.fi> - 1.0-0.38.20060407
- 2006-04-07 CVS snapshot using shared ffmpeg, GTK2, FAAC, OpenAL, and XvMC.
- XMMS input plugin support can be disabled by rebuilding with "--without xmms"
- GUI changes: use upstream desktop entry file, update GTK icon cache and
  desktop database at post(un)install time, install icon to %%{_datadir}/icons.
- Drop lots of obsolete patches.

* Fri Mar 24 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
1.0-0.37.pre7try2
- fix #836
- fix #835,#834 by disabling detection of 3dnowext for now (Thomas Jansen)
  this should work around the garbage sound output

* Sat Mar 18 2006 Ville Skyttä <ville.skytta at iki.fi> - 1.0-0.36.pre7try2
- Add RLO identifier to version string per upstream recommendation.
- Use configure flags instead of patch for enabling v4l*.
- Make DVB and DirectFB support unconditional.
- Drop libXvMC-devel build dependency until xvmc is actually built (#731).
- Backport get_time_pos slave mode command from CVS to fix progress bar
  with mplayerplug-in >= 3.15.
- Drop vdr-mplayer slave mode patch.
- Rename mplayer-mencoder to mencoder.

* Fri Mar 17 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
1.0-0.35.pre7try2
- fix x86_64 asm issues (maybe?!)
- fix file section for ppc

* Thu Mar 09 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- switch to new release field

* Tue Feb 28 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- add dist

* Thu Feb 23 2006 Ville Skyttä <ville.skytta at iki.fi> - 1.0-0.lvn.0.34.pre7try2
- Apply upstream demuxer.h heap overflow fix (CVE-2006-0579).
- Fix build time X11 detection on lib64 archs.
- Update Blue skin to 1.5.

* Mon Jan 16 2006 Adrian Reber <adrian@lisas.de> - 1.0-0.lvn.0.32.pre7try2
- re-enabled the aalib-devel BR

* Thu Dec 22 2005 Ville Skyttä <ville.skytta at iki.fi> - 1.0-0.lvn.0.31.pre7try2
- Apply fix for CVE-2005-4048 from ffmpeg CVS.

* Sun Dec 11 2005 Adrian Reber <adrian@lisas.de> - 1.0-0.lvn.0.30.pre7try2
- changed BR for modular X
- temporary removal of aalib-devel BR

* Fri Nov 25 2005 Ville Skyttä <ville.skytta at iki.fi> - 1.0-0.lvn.0.29.pre7try2
- More pre-FC3 cleanups.
- Make "Blue" the default skin by symlinking, fixes fallback (#571).
- Build against new DirectFB.

* Thu Sep 29 2005 Ville Skyttä <ville.skytta at iki.fi> - 1.0-0.lvn.0.28.pre7try2
- Clean up obsolete pre-FC3 stuff (LIRC, CACA, DXR3, and Enca support now
  unconditional).
- Drop zero Epochs.

* Thu Sep 15 2005 Ville Skyttä <ville.skytta at iki.fi> - 0:1.0-0.lvn.0.27.pre7try2
- Enable Enca by default, build with it for FC3+.

* Tue Sep  6 2005 Ville Skyttä <ville.skytta at iki.fi> - 0:1.0-0.lvn.0.26.pre7try2
- 1.0pre7try2.
- Enable v4l2 interface (#576).
- Enable DVB support only with recent enough glibc-kernheaders.

* Mon Jul  4 2005 Thorsten Leemhuis <fedora at leemhuis.info> - 0:1.0-0.lvn.0.26.pre7
- Add a patch to allow compiling for x86_64-FC4; thx to Ryo Dairiki:
  https://www.redhat.com/archives/fedora-extras-list/2005-July/msg00997.html

* Mon Jul  4 2005 Ville Skyttä <ville.skytta at iki.fi> - 0:1.0-0.lvn.0.25.pre7
- Enable DirectFB by default, rebuild with "--without directfb" to disable.
- Clean up obsolete pre-FC2 support.

* Thu Jun 30 2005 Dams <anvil[AT]livna.org> - 0:1.0-0.lvn.0.24.pre7
- Added patch to fix ppc/altivec builds (#494)

* Mon Jun 20 2005 Ville Skyttä <ville.skytta at iki.fi> - 0:1.0-0.lvn.0.23.pre7
- Completely disable parallel make for now.

* Mon Jun  6 2005 Thorsten Leemhuis <fedora at leemhuis.info> - 0:1.0-0.lvn.0.22.pre7
- add gcc4 patch from thias/gentoo/myself

* Mon May  9 2005 Ville Skyttä <ville.skytta at iki.fi> - 0:1.0-0.lvn.0.21.pre7
- Use em8300-devel for DXR3 support, and make it optional, default enabled.

* Tue May 03 2005 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 0:1.0-0.lvn.0.20.pre7
- fix build issues on x86_64:
 - move target= to a ix86 section -- on x86_64 it passes the option x86-64 
   and not x86_64
 - use explicit --with-xmmslibdir
 - {_libdir}/libdha.so.* and {_libdir}/mplayer are missing on x86_64

* Tue Apr 19 2005 Dams <anvil[AT]livna.org> - 0:1.0-0.lvn.0.19.pre7
- Updated installstrip patch
- Updated ldconfig patch
- Updated to 1.0pre7

* Sun Feb 27 2005 Ville Skyttä <ville.skytta at iki.fi> 0:1.0-0.lvn.0.18.pre6a
- Fix PPC build (David Woodhouse, bug 376).
- Add libcaca support (rebuild "--without caca" to disable).
- Rebuild with LIRC support.

* Thu Jan  6 2005 Ville Skyttä <ville.skytta at iki.fi> 0:1.0-0.lvn.0.17.pre6a
- Update to 1.0pre6a (== 1.0pre6 + included HTML docs).
