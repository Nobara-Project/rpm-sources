%{?!vlc_plugindir:%global vlc_plugindir %{_libdir}/vlc/plugins}

Name:		vlc-plugins-freeworld
Version:	3.0.21
Release:	2%{?dist}
Summary:	AAC, H.264, and HEVC codec plugins for VLC media player
License:	GPL-2.0-or-later AND LGPL-2.1-or-later AND BSD-2-Clause AND BSD-3-Clause
URL:		https://www.videolan.org
Source:		https://download.videolan.org/pub/videolan/vlc/%{version}/vlc-%{version}.tar.xz

%global __provides_exclude_from ^%{vlc_plugindir}/.*$

BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	gettext-devel
BuildRequires:	libtool
BuildRequires:	gcc-c++

# libvlccore dependencies, for consistency with vlc-libs
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(libidn)

BuildRequires:	faad2-devel
BuildRequires:	pkgconfig(x264) >= 0.153
BuildRequires:	pkgconfig(x265)

BuildRequires:	vlc-devel

Requires:	vlc-libs%{?_isa} >= 1:%{version}
Supplements:	vlc-plugins-base%{?_isa} >= 1:%{version}

%description
%{summary}


%prep
%autosetup -n vlc-%{version} -p1
rm -f aclocal.m4 m4/lib*.m4 m4/lt*.m4

%build
./bootstrap
touch src/revision.txt

%configure				\
    --disable-silent-rules		\
    --disable-dependency-tracking	\
    --with-binary-version=%{version}	\
    --disable-static			\
    --with-pic				\
    --disable-rpath			\
    --enable-dbus			\
    --disable-optimizations		\
    --disable-lua			\
    --enable-faad			\
    --enable-x264			\
    --enable-x26410b			\
    --enable-x265			\
    --disable-archive			\
    --disable-live555			\
    --disable-dc1394			\
    --disable-dv1394			\
    --disable-linsys			\
    --disable-dvdread			\
    --disable-dvdnav			\
    --disable-bluray			\
    --disable-opencv			\
    --disable-smbclient			\
    --disable-dsm			\
    --disable-sftp			\
    --disable-nfs			\
    --disable-smb2			\
    --disable-v4l2			\
    --disable-decklink			\
    --disable-vcd			\
    --disable-libcddb			\
    --disable-screen			\
    --disable-vnc			\
    --disable-freerdp			\
    --disable-realrtsp			\
    --disable-asdcp			\
    --disable-dvbpsi			\
    --disable-gme			\
    --disable-sid			\
    --disable-ogg			\
    --disable-shout			\
    --disable-matroska			\
    --disable-mod			\
    --disable-mpc			\
    --disable-shine			\
    --disable-omxil			\
    --disable-crystalhd			\
    --disable-mad			\
    --disable-mpg123			\
    --disable-gst-decode		\
    --disable-avcodec			\
    --disable-libva			\
    --disable-avformat			\
    --disable-swscale			\
    --disable-postproc			\
    --disable-aom			\
    --disable-dav1d			\
    --disable-vpx			\
    --disable-twolame			\
    --disable-fdkaac			\
    --disable-a52			\
    --disable-dca			\
    --disable-flac			\
    --disable-libmpeg2			\
    --disable-vorbis			\
    --disable-tremor			\
    --disable-speex			\
    --disable-opus			\
    --disable-spatialaudio		\
    --disable-theora			\
    --disable-oggspots			\
    --disable-daala			\
    --disable-schroedinger		\
    --disable-png			\
    --disable-jpeg			\
    --disable-bpg			\
    --disable-x262			\
    --disable-mfx			\
    --disable-fluidsynth		\
    --disable-fluidlite			\
    --disable-zvbi			\
    --disable-telx			\
    --disable-libass			\
    --disable-aribsub			\
    --disable-aribb25			\
    --disable-kate			\
    --disable-tiger			\
    --disable-css			\
    --disable-gles2			\
    --disable-xcb			\
    --disable-xvideo			\
    --disable-vdpau			\
    --disable-wayland			\
    --disable-sdl-image			\
    --disable-freetype			\
    --disable-fribidi			\
    --disable-harfbuzz			\
    --disable-fontconfig		\
    --disable-svg			\
    --disable-svgdec			\
    --disable-aa			\
    --disable-caca			\
    --disable-mmal			\
    --disable-evas			\
    --disable-pulse			\
    --disable-alsa			\
    --disable-jack			\
    --disable-samplerate		\
    --disable-soxr			\
    --disable-chromaprint		\
    --disable-chromecast		\
    --disable-qt			\
    --disable-skins2			\
    --disable-libtar			\
    --disable-lirc			\
    --disable-srt			\
    --disable-goom			\
    --disable-projectm			\
    --disable-vsxu			\
    --disable-avahi			\
    --disable-udev			\
    --disable-mtp			\
    --disable-upnp			\
    --disable-microdns			\
    --disable-libxml2			\
    --disable-libgcrypt			\
    --disable-gnutls			\
    --disable-taglib			\
    --disable-secret			\
    --disable-kwallet			\
    --disable-update-check		\
    --disable-notify			\
    --disable-libplacebo		\
    --without-kde-solid			\
    --without-vlc			\
    %{nil}

# clean unused-direct-shlib-dependencies
sed -i -e 's! -shared ! -Wl,--as-needed\0!g' libtool

%make_build -C compat
%make_build -C modules LTLIBVLCCORE=-lvlccore \
    codec_LTLIBRARIES="libfaad_plugin.la libx264_plugin.la libx26410b_plugin.la libx265_plugin.la" \
    access_LTLIBRARIES= access_out_LTLIBRARIES= aout_LTLIBRARIES= \
    audio_filter_LTLIBRARIES= audio_mixer_LTLIBRARIES= check_LTLIBRARIES= \
    chroma_LTLIBRARIES= control_LTLIBRARIES= demux_LTLIBRARIES= gui_LTLIBRARIES= \
    keystore_LTLIBRARIES= logger_LTLIBRARIES= lua_LTLIBRARIES= meta_LTLIBRARIES= \
    misc_LTLIBRARIES= mmal_LTLIBRARIES= mux_LTLIBRARIES= notify_LTLIBRARIES= \
    packetizer_LTLIBRARIES= pkglib_LTLIBRARIES= sd_LTLIBRARIES= sout_LTLIBRARIES= \
    splitter_LTLIBRARIES= spu_LTLIBRARIES= stream_extractor_LTLIBRARIES= \
    stream_filter_LTLIBRARIES= text_LTLIBRARIES= vaapi_LTLIBRARIES= \
    vdpau_LTLIBRARIES= video_filter_LTLIBRARIES= visu_LTLIBRARIES= \
    vout_LTLIBRARIES= noinst_LTLIBRARIES=


%install
%make_install -C modules CPPROG="cp -p" LTLIBVLCCORE=-lvlccore \
    codec_LTLIBRARIES="libfaad_plugin.la libx264_plugin.la libx26410b_plugin.la libx265_plugin.la" \
    access_LTLIBRARIES= access_out_LTLIBRARIES= aout_LTLIBRARIES= \
    audio_filter_LTLIBRARIES= audio_mixer_LTLIBRARIES= check_LTLIBRARIES= \
    chroma_LTLIBRARIES= control_LTLIBRARIES= demux_LTLIBRARIES= gui_LTLIBRARIES= \
    keystore_LTLIBRARIES= logger_LTLIBRARIES= lua_LTLIBRARIES= meta_LTLIBRARIES= \
    misc_LTLIBRARIES= mmal_LTLIBRARIES= mux_LTLIBRARIES= notify_LTLIBRARIES= \
    packetizer_LTLIBRARIES= pkglib_LTLIBRARIES= sd_LTLIBRARIES= sout_LTLIBRARIES= \
    splitter_LTLIBRARIES= spu_LTLIBRARIES= stream_extractor_LTLIBRARIES= \
    stream_filter_LTLIBRARIES= text_LTLIBRARIES= vaapi_LTLIBRARIES= \
    vdpau_LTLIBRARIES= video_filter_LTLIBRARIES= visu_LTLIBRARIES= \
    vout_LTLIBRARIES= noinst_LTLIBRARIES=

# Remove libtool libraries (for RHEL 9 and older)
find %{buildroot}%{_libdir} -name '*.la' -delete


%files
%doc AUTHORS NEWS README THANKS
%license COPYING COPYING.LIB
%{vlc_plugindir}/codec/libfaad_plugin.so
%{vlc_plugindir}/codec/libx264_plugin.so
%{vlc_plugindir}/codec/libx26410b_plugin.so
%{vlc_plugindir}/codec/libx265_plugin.so


%changelog
* Fri Aug 02 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 3.0.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jun 06 2024 Sérgio Basto <sergio@serjux.com> - 3.0.21-1
- Update vlc-plugins-freeworld to 3.0.21

* Sat Apr 06 2024 Leigh Scott <leigh123linux@gmail.com> - 3.0.20-3
- Rebuild for new x265 version

* Sun Feb 04 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 3.0.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Dec 15 2023 Dominik Mierzejewski <dominik@greysector.net> - 3.0.20-1
- Initial import
