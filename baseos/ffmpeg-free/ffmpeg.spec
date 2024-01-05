# For a complete build enable these two
%bcond_with upstream_tarball
%bcond_with all_codecs

# Break dependency cycles by disabling certain optional dependencies.
%bcond_with bootstrap

# If you want to do a build with the upstream source tarball, then set the
# pkg_suffix to %%nil. We can't handle this with a conditional, as srpm
# generation would not take it into account.
%global pkg_suffix -free

# Fails due to asm issue
%ifarch %{ix86} %{arm}
%bcond_with lto
%else
%bcond_without lto
%endif

%ifarch x86_64
%bcond_without vpl
%bcond_without vmaf
%else
%bcond_with vpl
%bcond_with vmaf
%endif

%ifarch s390 s390x
%bcond_with dc1394
%else
%bcond_without dc1394
%endif

%if 0%{?rhel}
# Disable dependencies not offered in RHEL/EPEL
%bcond_with omxil
%else

# Disable some features because RHEL 9 packages are too old
%if 0%{?rhel} && 0%{?rhel} <= 9
%bcond_with flite
%bcond_with lcms2
%bcond_with placebo
%else
%bcond_without flite
%bcond_without lcms2
%bcond_without placebo
%endif

%bcond_without omxil

%endif

# Break chromaprint dependency cycle (Fedora-only):
#   ffmpeg (libavcodec-free) → chromaprint → ffmpeg
%if %{with bootstrap}
%bcond_with chromaprint
%else
%bcond_without chromaprint
%endif


%if %{with all_codecs}
%bcond_without rtmp
%bcond_without x264
%bcond_without x265
%else
%bcond_with rtmp
%bcond_with x264
%bcond_with x265
%endif

%if %{without lto}
%global _lto_cflags %{nil}
%endif

%if "%{__isa_bits}" == "64"
%global lib64_suffix ()(64bit)
%endif
%global openh264_soversion 7

%global av_codec_soversion 60
%global av_device_soversion 60
%global av_filter_soversion 9
%global av_format_soversion 60
%global av_util_soversion 58
%global postproc_soversion 57
%global swresample_soversion 4
%global swscale_soversion 7

Name:           ffmpeg
%global pkg_name %{name}%{?pkg_suffix}

Version:        6.0.1
Release:        2%{?dist}
Summary:        A complete solution to record, convert and stream audio and video
License:        GPL-3.0-or-later
URL:            https://ffmpeg.org/
Source0:        ffmpeg%{?pkg_suffix}-%{version}.tar.xz
Source1:        ffmpeg-dlopen-headers.tar.xz
Source2:        https://ffmpeg.org/releases/ffmpeg-%{version}.tar.xz.asc
# https://ffmpeg.org/ffmpeg-devel.asc
# gpg2 --import --import-options import-export,import-minimal ffmpeg-devel.asc > ./ffmpeg.keyring
Source3:        ffmpeg.keyring
Source4:        ffmpeg_free_sources
Source20:       enable_decoders
Source21:       enable_encoders
# Scripts for generating tarballs
Source90:       ffmpeg_update_free_sources.sh
Source91:       ffmpeg_gen_free_tarball.sh
Source92:       ffmpeg_get_dlopen_headers.sh
Source93:       ffmpeg_find_free_source_headers.sh

# Fixes for reduced codec selection on free build
Patch1:         ffmpeg-codec-choice.patch
# Better error messages for free build
Patch2:         ffmpeg-new-coder-errors.patch
# Allow to build with fdk-aac-free
# See https://bugzilla.redhat.com/show_bug.cgi?id=1501522#c112
Patch3:         ffmpeg-allow-fdk-aac-free.patch
# Backport upstream patches for libplacebo v5.264
Patch4:         0001-avfilter-vf_libplacebo-wrap-deprecated-opts-in-FF_AP.patch
Patch5:         0001-avfilter-vf_libplacebo-remove-deprecated-field.patch

# Backport fix for segfault when passing non-existent filter option
# See: https://bugzilla.rpmfusion.org/show_bug.cgi?id=6773
Patch6:         0001-fftools-ffmpeg_filter-initialize-the-o-to-silence-th.patch

# Backport patches for enhanced rtmp support
# Cf. https://patchwork.ffmpeg.org/project/ffmpeg/list/?series=8926
## From: https://patchwork.ffmpeg.org/series/8926/mbox/
Patch8:         FFmpeg-devel-v10-Support-enhanced-flv-in-FFmpeg.patch

# Backport AV1 VA-API encode support
# Courtesy of GloriousEggroll
## Adapted from: https://patchwork.ffmpeg.org/project/ffmpeg/list/?series=9594
Patch9:         ffmpeg-ge-av1-vaapi-encode-support.patch

# Drop openh264 runtime version checks
# https://patchwork.ffmpeg.org/project/ffmpeg/list/?series=10211
Patch10:        0001-lavc-libopenh264-Drop-openh264-runtime-version-check.patch

# Set up dlopen for openh264
Patch1001:      ffmpeg-dlopen-openh264.patch

# Add first_dts getter to libavformat for Chromium
# See: https://bugzilla.redhat.com/show_bug.cgi?id=2240127
# Reference: https://crbug.com/1306560
Patch1002:      ffmpeg-chromium.patch


Requires:       libavcodec%{?pkg_suffix}%{_isa} = %{version}-%{release}
Requires:       libavdevice%{?pkg_suffix}%{_isa} = %{version}-%{release}
Requires:       libavfilter%{?pkg_suffix}%{_isa} = %{version}-%{release}
Requires:       libavformat%{?pkg_suffix}%{_isa} = %{version}-%{release}
Requires:       libavutil%{?pkg_suffix}%{_isa} = %{version}-%{release}
Requires:       libpostproc%{?pkg_suffix}%{_isa} = %{version}-%{release}
Requires:       libswresample%{?pkg_suffix}%{_isa} = %{version}-%{release}
Requires:       libswscale%{?pkg_suffix}%{_isa} = %{version}-%{release}

BuildRequires:  AMF-devel
BuildRequires:  fdk-aac-free-devel
%if %{with flite}
BuildRequires:  flite-devel >= 2.2
%endif
BuildRequires:  game-music-emu-devel
BuildRequires:  gcc
BuildRequires:  git-core
BuildRequires:  gnupg2
BuildRequires:  gsm-devel
BuildRequires:  ladspa-devel
BuildRequires:  lame-devel
BuildRequires:  libgcrypt-devel
BuildRequires:  libmysofa-devel
BuildRequires:  libX11-devel
BuildRequires:  libXext-devel
BuildRequires:  libXv-devel
BuildRequires:  make
BuildRequires:  nasm
BuildRequires:  perl(Pod::Man)
BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(aom)
BuildRequires:  pkgconfig(bzip2)
BuildRequires:  pkgconfig(caca)
BuildRequires:  pkgconfig(codec2)
BuildRequires:  pkgconfig(dav1d)
BuildRequires:  pkgconfig(ffnvcodec)
BuildRequires:  pkgconfig(flac)
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(frei0r)
BuildRequires:  pkgconfig(fribidi)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(gnutls)
BuildRequires:  pkgconfig(libilbc)
BuildRequires:  pkgconfig(jack)
%if %{with lcms2}
BuildRequires:  pkgconfig(lcms2) >= 2.13
%endif
BuildRequires:  pkgconfig(libass)
BuildRequires:  pkgconfig(libbluray)
BuildRequires:  pkgconfig(libbs2b)
BuildRequires:  pkgconfig(libcdio)
BuildRequires:  pkgconfig(libcdio_paranoia)
%if %{with chromaprint}
BuildRequires:  pkgconfig(libchromaprint)
%endif
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libjxl) >= 0.7.0
BuildRequires:  pkgconfig(libmodplug)
%if %{with omxil}
BuildRequires:  pkgconfig(libomxil-bellagio)
%endif
BuildRequires:  pkgconfig(libopenjp2)
BuildRequires:  pkgconfig(libopenmpt)
%if %{with placebo}
BuildRequires:  pkgconfig(libplacebo) >= 4.192.0
%endif
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(librabbitmq)
BuildRequires:  pkgconfig(librist)
BuildRequires:  pkgconfig(librsvg-2.0)
BuildRequires:  pkgconfig(libssh)
BuildRequires:  pkgconfig(libv4l2)
BuildRequires:  pkgconfig(libva)
BuildRequires:  pkgconfig(libva-drm)
BuildRequires:  pkgconfig(libva-x11)
BuildRequires:  pkgconfig(libwebp)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(libzmq)
BuildRequires:  pkgconfig(lilv-0)
BuildRequires:  pkgconfig(lv2)
BuildRequires:  pkgconfig(netcdf)
BuildRequires:  pkgconfig(ogg)
BuildRequires:  pkgconfig(openal)
BuildRequires:  pkgconfig(opencore-amrnb)
BuildRequires:  pkgconfig(OpenCL)
BuildRequires:  pkgconfig(opus)
BuildRequires:  pkgconfig(rav1e)
BuildRequires:  pkgconfig(rubberband)
BuildRequires:  pkgconfig(schroedinger-1.0)
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(shaderc) >= 2019.1
BuildRequires:  pkgconfig(smbclient)
BuildRequires:  pkgconfig(snappy)
BuildRequires:  pkgconfig(soxr)
BuildRequires:  pkgconfig(speex)
BuildRequires:  pkgconfig(srt)
BuildRequires:  pkgconfig(SvtAv1Enc) >= 0.9.0
BuildRequires:  pkgconfig(tesseract)
BuildRequires:  pkgconfig(theora)
BuildRequires:  pkgconfig(twolame)
BuildRequires:  pkgconfig(vapoursynth)
BuildRequires:  pkgconfig(vdpau)
BuildRequires:  pkgconfig(vidstab)
BuildRequires:  pkgconfig(vorbis)
BuildRequires:  pkgconfig(vo-amrwbenc)
BuildRequires:  pkgconfig(vpx)
BuildRequires:  pkgconfig(vulkan)
BuildRequires:  pkgconfig(wavpack)
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(xcb-render)
BuildRequires:  pkgconfig(xcb-shape)
BuildRequires:  pkgconfig(xcb-shm)
BuildRequires:  pkgconfig(xcb-xfixes)
BuildRequires:  pkgconfig(zimg)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  pkgconfig(zvbi-0.2)
BuildRequires:  texinfo
BuildRequires:  xvidcore-devel

%if %{with dc1394}
BuildRequires:  pkgconfig(libavc1394)
BuildRequires:  pkgconfig(libdc1394-2)
BuildRequires:  pkgconfig(libiec61883)
%endif
%if %{with rtmp}
BuildRequires:  librtmp-devel
%endif
%if %{with vpl}
BuildRequires:  pkgconfig(vpl) >= 2.6
%endif
%if %{with x264}
BuildRequires:  pkgconfig(x264)
%endif
%if %{with x265}
BuildRequires:  pkgconfig(x265)
%endif
%if %{with vmaf}
BuildRequires:  pkgconfig(libvmaf)
%endif


%description
FFmpeg is a leading multimedia framework, able to decode, encode, transcode,
mux, demux, stream, filter and play pretty much anything that humans and
machines have created. It supports the most obscure ancient formats up to the
cutting edge. No matter if they were designed by some standards committee, the
community or a corporation.

%if %{without all_codecs}
This build of ffmpeg is limited in the number of codecs supported.
%endif

%if "x%{?pkg_suffix}" != "x"
%package -n     %{pkg_name}
Summary:        A complete solution to record, convert and stream audio and video
Requires:       libavcodec%{?pkg_suffix}%{_isa} = %{version}-%{release}
Requires:       libavdevice%{?pkg_suffix}%{_isa} = %{version}-%{release}
Requires:       libavfilter%{?pkg_suffix}%{_isa} = %{version}-%{release}
Requires:       libavformat%{?pkg_suffix}%{_isa} = %{version}-%{release}
Requires:       libavutil%{?pkg_suffix}%{_isa} = %{version}-%{release}
Requires:       libpostproc%{?pkg_suffix}%{_isa} = %{version}-%{release}
Requires:       libswresample%{?pkg_suffix}%{_isa} = %{version}-%{release}
Requires:       libswscale%{?pkg_suffix}%{_isa} = %{version}-%{release}
Provides:       ffmpeg-free
Provides:       ffmpeg

%description -n %{pkg_name}
FFmpeg is a leading multimedia framework, able to decode, encode, transcode,
mux, demux, stream, filter and play pretty much anything that humans and
machines have created. It supports the most obscure ancient formats up to the
cutting edge. No matter if they were designed by some standards committee, the
community or a corporation.

%if %{without all_codecs}
This build of ffmpeg is limited in the number of codecs supported.
%endif

#/ "x%%{?pkg_suffix}" != "x"
%endif

%package -n     %{pkg_name}-devel
Summary:        Development package for %{name}
Requires:       libavcodec%{?pkg_suffix}-devel = %{version}-%{release}
Requires:       libavdevice%{?pkg_suffix}-devel = %{version}-%{release}
Requires:       libavfilter%{?pkg_suffix}-devel = %{version}-%{release}
Requires:       libavformat%{?pkg_suffix}-devel = %{version}-%{release}
Requires:       libavutil%{?pkg_suffix}-devel = %{version}-%{release}
Requires:       libpostproc%{?pkg_suffix}-devel = %{version}-%{release}
Requires:       libswresample%{?pkg_suffix}-devel = %{version}-%{release}
Requires:       libswscale%{?pkg_suffix}-devel = %{version}-%{release}
Requires:       pkgconfig

%description -n %{pkg_name}-devel
FFmpeg is a leading multimedia framework, able to decode, encode, transcode,
mux, demux, stream, filter and play pretty much anything that humans and
machines have created. It supports the most obscure ancient formats up to the
cutting edge. No matter if they were designed by some standards committee, the
community or a corporation.

%package -n libavcodec%{?pkg_suffix}
Summary:        FFmpeg codec library
Requires:       libavutil%{?pkg_suffix}%{_isa} = %{version}-%{release}
Requires:       libswresample%{?pkg_suffix}%{_isa} = %{version}-%{release}
# We dlopen() openh264, so weak-depend on it...
## Note, we can do this because openh264 is provided in a default-enabled
## third party repository provided by Cisco.
Recommends:     libopenh264.so.%{openh264_soversion}%{?lib64_suffix}
Suggests:       openh264%{_isa}

%description -n libavcodec%{?pkg_suffix}
The libavcodec library provides a generic encoding/decoding framework
and contains multiple decoders and encoders for audio, video and
subtitle streams, and several bitstream filters.

%if %{without all_codecs}
This build of ffmpeg is limited in the number of codecs supported.
%endif

%package -n libavcodec%{?pkg_suffix}-devel
Summary:        Development files for FFmpeg's codec library
Requires:       libavutil%{?pkg_suffix}-devel = %{version}-%{release}
Requires:       libavcodec%{?pkg_suffix}%{_isa} = %{version}-%{release}
Requires:       pkgconfig

%description -n libavcodec%{?pkg_suffix}-devel
The libavcodec library provides a generic encoding/decoding framework
and contains multiple decoders and encoders for audio, video and
subtitle streams, and several bitstream filters.

This subpackage contains the headers for FFmpeg libavcodec.

%package -n libavdevice%{?pkg_suffix}
Summary:        FFmpeg device library
Requires:       libavcodec%{?pkg_suffix}%{_isa} = %{version}-%{release}
Requires:       libavfilter%{?pkg_suffix}%{_isa} = %{version}-%{release}
Requires:       libavformat%{?pkg_suffix}%{_isa} = %{version}-%{release}
Requires:       libavutil%{?pkg_suffix}%{_isa} = %{version}-%{release}

%description -n libavdevice%{?pkg_suffix}
The libavdevice library provides a generic framework for grabbing from
and rendering to many common multimedia input/output devices, and
supports several input and output devices, including Video4Linux2, VfW,
DShow, and ALSA.

%package -n libavdevice%{?pkg_suffix}-devel
Summary:        Development files for FFmpeg's device library
Requires:       libavcodec%{?pkg_suffix}-devel = %{version}-%{release}
Requires:       libavfilter%{?pkg_suffix}-devel = %{version}-%{release}
Requires:       libavformat%{?pkg_suffix}-devel = %{version}-%{release}
Requires:       libavutil%{?pkg_suffix}-devel = %{version}-%{release}
Requires:       libpostproc%{?pkg_suffix}-devel = %{version}-%{release}
Requires:       libswresample%{?pkg_suffix}-devel = %{version}-%{release}
Requires:       libswscale%{?pkg_suffix}-devel = %{version}-%{release}
Requires:       libavdevice%{?pkg_suffix}%{_isa} = %{version}-%{release}
Requires:       pkgconfig

%description -n libavdevice%{?pkg_suffix}-devel
The libavdevice library provides a generic framework for grabbing from
and rendering to many common multimedia input/output devices, and
supports several input and output devices, including Video4Linux2, VfW,
DShow, and ALSA.

This subpackage contains the headers for FFmpeg libavdevice.

%package -n libavfilter%{?pkg_suffix}
Summary:        FFmpeg audio and video filtering library
Requires:       libavcodec%{?pkg_suffix}%{_isa} = %{version}-%{release}
Requires:       libavformat%{?pkg_suffix}%{_isa} = %{version}-%{release}
Requires:       libavutil%{?pkg_suffix}%{_isa} = %{version}-%{release}
Requires:       libpostproc%{?pkg_suffix}%{_isa} = %{version}-%{release}
Requires:       libswresample%{?pkg_suffix}%{_isa} = %{version}-%{release}
Requires:       libswscale%{?pkg_suffix}%{_isa} = %{version}-%{release}

%description -n libavfilter%{?pkg_suffix}
The libavfilter library provides a generic audio/video filtering
framework containing several filters, sources and sinks.

%package -n libavfilter%{?pkg_suffix}-devel
Summary:        Development files for FFmpeg's audio/video filter library
Requires:       libavcodec%{?pkg_suffix}-devel = %{version}-%{release}
Requires:       libavformat%{?pkg_suffix}-devel = %{version}-%{release}
Requires:       libavutil%{?pkg_suffix}-devel = %{version}-%{release}
Requires:       libpostproc%{?pkg_suffix}-devel = %{version}-%{release}
Requires:       libswresample%{?pkg_suffix}-devel = %{version}-%{release}
Requires:       libswscale%{?pkg_suffix}-devel = %{version}-%{release}
Requires:       libavfilter%{?pkg_suffix} = %{version}-%{release}
Requires:       pkgconfig

%description -n libavfilter%{?pkg_suffix}-devel
The libavfilter library provides a generic audio/video filtering
framework containing several filters, sources and sinks.

This subpackage contains the headers for FFmpeg libavfilter.

%package -n libavformat%{?pkg_suffix}
Summary:        FFmpeg's stream format library
Requires:       libavcodec%{?pkg_suffix}%{_isa} = %{version}-%{release}
Requires:       libavutil%{?pkg_suffix}%{_isa} = %{version}-%{release}

%description -n libavformat%{?pkg_suffix}
The libavformat library provides a generic framework for multiplexing
and demultiplexing (muxing and demuxing) audio, video and subtitle
streams. It encompasses multiple muxers and demuxers for multimedia
container formats.

%if %{without all_codecs}
This build of ffmpeg is limited in the number of codecs supported.
%endif

%package -n libavformat%{?pkg_suffix}-devel
Summary:        Development files for FFmpeg's stream format library
Requires:       libavcodec%{?pkg_suffix}-devel = %{version}-%{release}
Requires:       libavutil%{?pkg_suffix}-devel = %{version}-%{release}
Requires:       libswresample%{?pkg_suffix}-devel = %{version}-%{release}
Requires:       libavformat%{?pkg_suffix}%{_isa} = %{version}-%{release}
Requires:       pkgconfig

%description -n libavformat%{?pkg_suffix}-devel
The libavformat library provides a generic framework for multiplexing
and demultiplexing (muxing and demuxing) audio, video and subtitle
streams. It encompasses multiple muxers and demuxers for multimedia
container formats.

This subpackage contains the headers for FFmpeg libavformat.

%package -n libavutil%{?pkg_suffix}
Summary:        FFmpeg's utility library
Group:          System/Libraries

%description -n libavutil%{?pkg_suffix}
The libavutil library is a utility library to aid portable multimedia
programming. It contains safe portable string functions, random
number generators, data structures, additional mathematics functions,
cryptography and multimedia related functionality (like enumerations
for pixel and sample formats).

%package -n libavutil%{?pkg_suffix}-devel
Summary:        Development files for FFmpeg's utility library
Requires:       libavutil%{?pkg_suffix}%{_isa} = %{version}-%{release}
Requires:       pkgconfig

%description -n libavutil%{?pkg_suffix}-devel
The libavutil library is a utility library to aid portable multimedia
programming. It contains safe portable string functions, random
number generators, data structures, additional mathematics functions,
cryptography and multimedia related functionality (like enumerations
for pixel and sample formats).

This subpackage contains the headers for FFmpeg libavutil.

%package -n libpostproc%{?pkg_suffix}
Summary:        FFmpeg post-processing library
Requires:       libavutil%{?pkg_suffix}%{_isa} = %{version}-%{release}

%description -n libpostproc%{?pkg_suffix}
A library with video postprocessing filters, such as deblocking and
deringing filters, noise reduction, automatic contrast and brightness
correction, linear/cubic interpolating deinterlacing.

%package -n libpostproc%{?pkg_suffix}-devel
Summary:        Development files for the FFmpeg post-processing library
Requires:       libavutil%{?pkg_suffix}-devel = %{version}-%{release}
Requires:       libpostproc%{?pkg_suffix}%{_isa} = %{version}-%{release}
Requires:       pkgconfig

%description -n libpostproc%{?pkg_suffix}-devel
A library with video postprocessing filters, such as deblocking and
deringing filters, noise reduction, automatic contrast and brightness
correction, linear/cubic interpolating deinterlacing.

This subpackage contains the headers for FFmpeg libpostproc.

%package -n libswresample%{?pkg_suffix}
Summary:        FFmpeg software resampling library
Requires:       libavutil%{?pkg_suffix}%{_isa} = %{version}-%{release}

%description -n libswresample%{?pkg_suffix}
The libswresample library performs audio conversion between different
sample rates, channel layout and channel formats.

%package -n libswresample%{?pkg_suffix}-devel
Summary:        Development files for the FFmpeg software resampling library
Requires:       libavutil%{?pkg_suffix}-devel = %{version}-%{release}
Requires:       libswresample%{?pkg_suffix}%{_isa} = %{version}-%{release}

%description -n libswresample%{?pkg_suffix}-devel
The libswresample library performs audio conversion between different
sample rates, channel layout and channel formats.

This subpackage contains the headers for FFmpeg libswresample.

%package -n libswscale%{?pkg_suffix}
Summary:        FFmpeg image scaling and colorspace/pixel conversion library
Requires:       libavutil%{?pkg_suffix}%{_isa} = %{version}-%{release}

%description -n libswscale%{?pkg_suffix}
The libswscale library performs image scaling and colorspace and
pixel format conversion operations.

%package -n libswscale%{?pkg_suffix}-devel
Summary:        Development files for FFmpeg's image scaling and colorspace library
Provides:       libswscale%{?pkg_suffix}-devel = %{version}-%{release}
Conflicts:      libswscale%{?pkg_suffix}-devel < %{version}-%{release}
Requires:       libavutil%{?pkg_suffix}-devel = %{version}-%{release}
Requires:       libswscale%{?pkg_suffix}%{_isa} = %{version}-%{release}

%description -n libswscale%{?pkg_suffix}-devel
The libswscale library performs image scaling and colorspace and
pixel format conversion operations.

This subpackage contains the headers for FFmpeg libswscale.

%prep
%if %{with upstream_tarball}
%{gpgverify} --keyring='%{SOURCE3}' --signature='%{SOURCE2}' --data='%{SOURCE0}'
%endif

%autosetup -a1 -S git_am
install -m 0644 %{SOURCE20} enable_decoders
install -m 0644 %{SOURCE21} enable_encoders
# fix -O3 -g in host_cflags
sed -i "s|check_host_cflags -O3|check_host_cflags %{optflags}|" configure
install -m0755 -d _doc/examples
cp -a doc/examples/{*.c,Makefile,README} _doc/examples/

%build
%set_build_flags

# This is not a normal configure script, don't use %%configure
./configure \
    --prefix=%{_prefix} \
    --bindir=%{_bindir} \
    --datadir=%{_datadir}/%{name} \
    --docdir=%{_docdir}/%{name} \
    --incdir=%{_includedir}/%{name} \
    --libdir=%{_libdir} \
    --mandir=%{_mandir} \
    --arch=%{_target_cpu} \
    --optflags="%{build_cflags}" \
    --extra-ldflags="%{build_ldflags}" \
    --disable-htmlpages \
    --enable-pic \
    --disable-stripping \
    --enable-shared \
    --disable-static \
    --enable-gpl \
    --enable-version3 \
    --enable-libsmbclient \
    --disable-openssl \
    --enable-bzlib \
    --enable-frei0r \
%if %{with chromaprint}
    --enable-chromaprint \
%else
    --disable-chromaprint \
%endif
    --enable-gcrypt \
    --enable-gnutls \
    --enable-ladspa \
%if %{with lcms2}
    --enable-lcms2 \
%endif
    --enable-libshaderc \
    --enable-vulkan \
    --disable-cuda-sdk \
    --enable-libaom \
    --enable-libass \
    --enable-libbluray \
    --enable-libbs2b \
    --enable-libcaca \
    --enable-libcdio \
    --enable-libcodec2 \
    --enable-libdav1d \
%if %{with dc1394}
    --enable-libdc1394 \
%endif
    --enable-libdrm \
    --enable-libfdk-aac \
%if %{with flite}
    --enable-libflite \
%endif
    --enable-libfontconfig \
    --enable-libfreetype \
    --enable-libfribidi \
    --enable-libgme \
    --enable-libgsm \
%if %{with dc1394}
    --enable-libiec61883 \
%endif
    --enable-libilbc \
    --enable-libjack \
    --enable-libjxl \
    --enable-libmodplug \
    --enable-libmp3lame \
    --enable-libmysofa \
    --enable-libopenh264-dlopen \
    --enable-libopenjpeg \
    --enable-libopenmpt \
    --enable-libopus \
%if %{with placebo}
    --enable-libplacebo \
%endif
    --enable-libpulse \
    --enable-librabbitmq \
    --enable-librav1e \
    --enable-librist \
    --enable-librsvg \
    --enable-librubberband \
    --enable-libsnappy \
    --enable-libsvtav1 \
    --enable-libsoxr \
    --enable-libspeex \
    --enable-libssh \
    --enable-libsrt \
    --enable-libtesseract \
    --enable-libtheora \
    --enable-libtwolame \
    --enable-libvidstab \
%if %{with vmaf}
    --enable-libvmaf \
%endif
    --enable-libvorbis \
    --enable-libv4l2 \
    --enable-libvpx \
    --enable-libwebp \
    --enable-libxml2 \
    --enable-libzimg \
    --enable-libzmq \
    --enable-libzvbi \
%if %{with lto}
  --enable-lto \
%endif
%if %{with vpl}
    --enable-libvpl \
%endif
    --enable-lv2 \
    --enable-vaapi \
    --enable-vdpau \
    --enable-libopencore-amrnb \
    --enable-libopencore-amrwb \
    --enable-libvo-amrwbenc \
%if %{with x264}
    --enable-libx264 \
%endif
%if %{with x265}
    --enable-libx265 \
%endif
%if %{with librtmp}
    --enable-librtmp \
%endif
    --enable-libxvid \
    --enable-openal \
    --enable-opencl \
    --enable-opengl \
    --enable-pthreads \
    --enable-vapoursynth \
%if %{without all_codecs}
    --enable-muxers \
    --enable-demuxers \
    --enable-hwaccels \
    --disable-encoders \
    --disable-decoders \
    --disable-decoder="h264,hevc,vc1" \
    --enable-encoder="$(perl -pe 's{^(\w*).*}{$1,}gs' <enable_encoders)" \
    --enable-decoder="$(perl -pe 's{^(\w*).*}{$1,}gs' <enable_decoders)" \
%endif
%ifarch %{power64}
%ifarch ppc64
    --cpu=g5 \
%endif
%ifarch ppc64p7
    --cpu=power7 \
%endif
%ifarch ppc64le
    --cpu=power8 \
%endif
    --enable-pic \
%endif
%ifarch %{arm}
    --disable-runtime-cpudetect --arch=arm \
%ifarch armv6hl
    --cpu=armv6 \
%endif
%ifarch armv7hl armv7hnl
    --cpu=armv7-a \
    --enable-vfpv3 \
    --enable-thumb \
%endif
%ifarch armv7hl
    --disable-neon \
%endif
%ifarch armv7hnl
    --enable-neon \
%endif
%endif
    || cat ffbuild/config.log

cat config.h
cat config_components.h

# Paranoia check
%if %{without all_codecs}
# DECODER
for i in H264 HEVC HEVC_RKMPP VC1; do
    grep -q "#define CONFIG_${i}_DECODER 0" config_components.h
done

# ENCODER
for i in LIBX264 LIBX264RGB LIBX265; do
    grep -q "#define CONFIG_${i}_ENCODER 0" config_components.h
done
for i in H264 HEVC; do
    for j in MF VIDEOTOOLBOX; do
        grep -q "#define CONFIG_${i}_${j}_ENCODER 0" config_components.h
    done
done
%endif

%make_build V=1
%make_build documentation V=1
%make_build alltools V=1

%install
%make_install V=1

# We will package is as %%doc in the devel package
rm -rf %{buildroot}%{_datadir}/%{name}/examples

%ldconfig_scriptlets -n libavcodec%{?pkg_suffix}
%ldconfig_scriptlets -n libavdevice%{?pkg_suffix}
%ldconfig_scriptlets -n libavfilter%{?pkg_suffix}
%ldconfig_scriptlets -n libavformat%{?pkg_suffix}
%ldconfig_scriptlets -n libavutil%{?pkg_suffix}
%ldconfig_scriptlets -n libpostproc%{?pkg_suffix}
%ldconfig_scriptlets -n libswresample%{?pkg_suffix}
%ldconfig_scriptlets -n libswscle%{?pkg_suffix}

%files -n %{pkg_name}
%doc CREDITS README.md
%{_bindir}/ffmpeg
%{_bindir}/ffplay
%{_bindir}/ffprobe
%{_mandir}/man1/ff*.1*
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/ffprobe.xsd
%{_datadir}/%{name}/libvpx-*.ffpreset

%files -n %{pkg_name}-devel
%doc MAINTAINERS doc/APIchanges doc/*.txt
%doc _doc/examples

%files -n libavcodec%{?pkg_suffix}
%license COPYING.GPLv2 LICENSE.md
%{_libdir}/libavcodec.so.%{av_codec_soversion}{,.*}

%files -n libavcodec%{?pkg_suffix}-devel
%{_includedir}/%{name}/libavcodec
%{_libdir}/pkgconfig/libavcodec.pc
%{_libdir}/libavcodec.so
%{_mandir}/man3/libavcodec.3*

%files -n libavdevice%{?pkg_suffix}
%license COPYING.GPLv2 LICENSE.md
%{_libdir}/libavdevice.so.%{av_device_soversion}{,.*}

%files -n libavdevice%{?pkg_suffix}-devel
%{_includedir}/%{name}/libavdevice
%{_libdir}/pkgconfig/libavdevice.pc
%{_libdir}/libavdevice.so
%{_mandir}/man3/libavdevice.3*

%files -n libavfilter%{?pkg_suffix}
%license COPYING.GPLv2 LICENSE.md
%{_libdir}/libavfilter.so.%{av_filter_soversion}{,.*}

%files -n libavfilter%{?pkg_suffix}-devel
%{_includedir}/%{name}/libavfilter
%{_libdir}/pkgconfig/libavfilter.pc
%{_libdir}/libavfilter.so
%{_mandir}/man3/libavfilter.3*

%files -n libavformat%{?pkg_suffix}
%license COPYING.GPLv2 LICENSE.md
%{_libdir}/libavformat.so.%{av_format_soversion}{,.*}

%files -n libavformat%{?pkg_suffix}-devel
%{_includedir}/%{name}/libavformat
%{_libdir}/pkgconfig/libavformat.pc
%{_libdir}/libavformat.so
%{_mandir}/man3/libavformat.3*

%files -n libavutil%{?pkg_suffix}
%license COPYING.GPLv2 LICENSE.md
%{_libdir}/libavutil.so.%{av_util_soversion}{,.*}

%files -n libavutil%{?pkg_suffix}-devel
%{_includedir}/%{name}/libavutil
%{_libdir}/pkgconfig/libavutil.pc
%{_libdir}/libavutil.so
%{_mandir}/man3/libavutil.3*

%files -n libpostproc%{?pkg_suffix}
%license COPYING.GPLv2 LICENSE.md
%{_libdir}/libpostproc.so.%{postproc_soversion}{,.*}

%files -n libpostproc%{?pkg_suffix}-devel
%{_includedir}/%{name}/libpostproc
%{_libdir}/pkgconfig/libpostproc.pc
%{_libdir}/libpostproc.so

%files -n libswresample%{?pkg_suffix}
%license COPYING.GPLv2 LICENSE.md
%{_libdir}/libswresample.so.%{swresample_soversion}{,.*}

%files -n libswresample%{?pkg_suffix}-devel
%{_includedir}/%{name}/libswresample
%{_libdir}/pkgconfig/libswresample.pc
%{_libdir}/libswresample.so
%{_mandir}/man3/libswresample.3*

%files -n libswscale%{?pkg_suffix}
%license COPYING.GPLv2 LICENSE.md
%{_libdir}/libswscale.so.%{swscale_soversion}{,.*}

%files -n libswscale%{?pkg_suffix}-devel
%{_includedir}/%{name}/libswscale
%{_libdir}/pkgconfig/libswscale.pc
%{_libdir}/libswscale.so
%{_mandir}/man3/libswscale.3*

%changelog
* Wed Dec 06 2023 Kalev Lember <klember@redhat.com> - 6.0.1-2
- Prefer openh264 over noopenh264
- Backport upstream patch to drop openh264 runtime version checks

* Sat Nov 11 2023 Neal Gompa <ngompa@fedoraproject.org> - 6.0.1-1
- Update to 6.0.1
- Add ffmpeg chromium support patch (#2240127)
- Use git to apply patches

* Fri Nov 10 2023 Neal Gompa <ngompa@fedoraproject.org> - 6.0-13
- Add patches to support enhanced RTMP and AV1 encoding through VA-API
- Force AAC decoding through fdk-aac-free

* Sun Oct 08 2023 Dominik Mierzejewski <dominik@greysector.net> - 6.0-12
- Backport upstream patch to fix segfault when passing non-existent filter
  option (rfbz#6773)

* Sat Aug 05 2023 Richard Shaw <hobbes1069@gmail.com> - 6.0-11
- Rebuild for codec2.

* Fri Jul 28 2023 Dominik Mierzejewski <dominik@greysector.net> - 6.0-10
- Rebuild for libplacebo

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 6.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jul 14 2023 Sandro Mani <manisandro@gmail.com> - 6.0-8
- Rebuild (tesseract)

* Sun Jun 18 2023 Sérgio Basto <sergio@serjux.com> - 6.0-7
- Mass rebuild for jpegxl-0.8.1

* Mon Jun 12 2023 Dominik Mierzejewski <dominik@greysector.net> - 6.0-6
- Rebuild for libdc1394

* Thu Apr 06 2023 Adam Williamson <awilliam@redhat.com> - 6.0-5
- Rebuild (tesseract) again

* Mon Apr 03 2023 Neal Gompa <ngompa@fedoraproject.org> - 6.0-4
- Include RISC-V support sources in the tarball

* Mon Apr 03 2023 Sandro Mani <manisandro@gmail.com> - 6.0-3
- Rebuild (tesseract)

* Wed Mar 22 2023 Nicolas Chauvet <kwizart@gmail.com> - 6.0-2
- Backport upstream patches for libplacebo support

* Sun Mar 12 2023 Neal Gompa <ngompa@fedoraproject.org> - 6.0-1
- Rebase to version 6.0
- Enable SVT-AV1 on all architectures
- Use oneVPL for QSV
- Switch to SPDX license identifiers

* Wed Feb 15 2023 Neal Gompa <ngompa@fedoraproject.org> - 5.1.2-12
- Enable support for the RIST protocol through librist

* Wed Feb 15 2023 Tom Callaway <spot@fedoraproject.org> - 5.1.2-11
- bootstrap off

* Wed Feb 15 2023 Tom Callaway <spot@fedoraproject.org> - 5.1.2-10
- rebuild for libvpx (bootstrap)

* Mon Feb 13 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 5.1.2-9
- Enable lcms2, lv2, placebo, rabbitmq, xv

* Mon Feb 13 2023 Neal Gompa <ngompa@fedoraproject.org> - 5.1.2-8
- Disable flite for RHEL 9 as flite is too old

* Fri Feb 03 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 5.1.2-7
- Properly enable caca, flite, gme, iec61883

* Mon Jan 30 2023 Neal Gompa <ngompa@fedoraproject.org> - 5.1.2-6
- Enable more approved codecs

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sun Jan 15 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 5.1.2-4
- Properly enable libzvbi_teletext decoder

* Fri Dec 23 2022 Sandro Mani <manisandro@gmail.com> - 5.1.2-3
- Rebuild (tesseract)

* Wed Nov 09 2022 Neal Gompa <ngompa@fedoraproject.org> - 5.1.2-2
- Unconditionally enable Vulkan

* Wed Oct 12 2022 Neal Gompa <ngompa@fedoraproject.org> - 5.1.2-1
- Update to version 5.1.2
- Refresh dlopen headers and patch for OpenH264 2.3.1

* Sun Sep 04 2022 Neal Gompa <ngompa@fedoraproject.org> - 5.1.1-1
- Update to version 5.1.1
- Refresh dlopen headers for OpenH264 2.3.0
- Disable omxil and crystalhd for RHEL

* Wed Aug 24 2022 Neal Gompa <ngompa@fedoraproject.org> - 5.1-1
- Rebase to version 5.1

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.1-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jul 09 2022 Richard Shaw <hobbes1069@gmail.com> - 5.0.1-15
- Rebuild for codec2 1.0.4.

* Fri Jul 08 2022 Sandro Mani <manisandro@gmail.com> - 5.0.1-14
- Rebuild (tesseract)

* Wed Jun 22 2022 Robert-André Mauchin <zebob.m@gmail.com> - 5.0.1-13
- Rebuilt for new aom, dav1d, rav1e and svt-av1

* Fri Jun 17 2022 Mamoru TASAKA <mtasaka@tbz.t-com.ne.jp> - 5.0.1-12
- Rebuild for new srt

* Thu Jun 09 2022 Neal Gompa <ngompa@fedoraproject.org> - 5.0.1-11
- Ensure libavdevice-devel is pulled in with devel metapackage

* Sun Jun 05 2022 Neal Gompa <ngompa@fedoraproject.org> - 5.0.1-10
- Update for OpenH264 2.2.0

* Tue May 31 2022 Neal Gompa <ngompa@fedoraproject.org> - 5.0.1-9
- Rebuild for ilbc-3.0.4

* Thu May 26 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 5.0.1-9
- Rebuild for ilbc-3.0.4 (bootstrap)

* Sat May 21 2022 Sandro Mani <manisandro@gmail.com> - 5.0.1-8
- Rebuild for gdal-3.5.0 and/or openjpeg-2.5.0

* Fri May 20 2022 Sandro Mani <manisandro@gmail.com> - 5.0.1-7
- Rebuild for gdal-3.5.0 and/or openjpeg-2.5.0

* Sun Apr 24 2022 Neal Gompa <ngompa@fedoraproject.org> - 5.0.1-6
- Add VAAPI encoders for mjpeg, mpeg2, vp8, and vp9
- Ensure hwaccels for enabled codecs are turned on

* Tue Apr 19 2022 Neal Gompa <ngompa@fedoraproject.org> - 5.0.1-5
- Drop unused enca build dependency

* Tue Apr 19 2022 Neal Gompa <ngompa@fedoraproject.org> - 5.0.1-4
- Use shaderc for Vulkan support

* Mon Apr 18 2022 Neal Gompa <ngompa@fedoraproject.org> - 5.0.1-3
- Fix codec2 support enablement

* Mon Apr 18 2022 Dominik Mierzejewski <dominik@greysector.net> - 5.0.1-2
- Properly enable decoding and encoding ilbc

* Tue Apr 12 2022 Neal Gompa <ngompa@fedoraproject.org> - 5.0.1-1
- Update to 5.0.1 to fix crashes with muxing MP4 video (#2073980)

* Tue Apr 05 2022 Dominik Mierzejewski <dominik@greysector.net> - 5.0-11
- Enable OpenCL acceleration
- be explicit about enabled external features in configure
- enable gcrypt
- drop duplicate CFLAGS and use Fedora LDFLAGS

* Thu Mar 10 2022 Sandro Mani <manisandro@gmail.com> - 5.0-10
- Rebuild for tesseract 5.1.0

* Tue Mar 08 2022 Neal Gompa <ngompa@fedoraproject.org> - 5.0-9
- Drop ffmpeg chromium support patch (#2061392)

* Fri Feb 18 2022 Neal Gompa <ngompa@fedoraproject.org> - 5.0-8
- Add patch to return correct AVERROR with bad OpenH264 versions

* Fri Feb 18 2022 Neal Gompa <ngompa@fedoraproject.org> - 5.0-7
- Update OpenH264 dlopen patch to split dlopen code into c and h files

* Thu Feb 17 2022 Neal Gompa <ngompa@fedoraproject.org> - 5.0-6
- Update OpenH264 dlopen patch to use AVERROR return codes correctly

* Tue Feb 15 2022 Neal Gompa <ngompa@fedoraproject.org> - 5.0-5
- Disable hardware decoders due to broken failure modes

* Tue Feb 15 2022 Neal Gompa <ngompa@fedoraproject.org> - 5.0-4
- Add support for dlopening OpenH264
- Add tarball scripts as sources

* Sun Feb 13 2022 Neal Gompa <ngompa@fedoraproject.org> - 5.0-3
- Enable more QSV and V4L2M2M codecs

* Sun Feb 13 2022 Neal Gompa <ngompa@fedoraproject.org> - 5.0-2
- Enable support for more hardware codecs

* Fri Feb 11 2022 Andreas Schneider <asn@redhat.com> - 5.0-1
- Initial import (fedora#2051008)
