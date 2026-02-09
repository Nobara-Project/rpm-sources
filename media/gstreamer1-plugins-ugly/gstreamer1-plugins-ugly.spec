%global src_name gst-plugins-ugly

Summary:        GStreamer 1.0 streaming media framework "ugly" plug-ins
Name:           gstreamer1-plugins-ugly
Epoch:          1
Version:        1.26.10
Release:        1%{?dist}
License:        LGPLv2+
URL:            https://gstreamer.freedesktop.org/
Source0:        %{url}/src/%{src_name}/%{src_name}-%{version}.tar.xz

BuildRequires:  gcc
BuildRequires:  gstreamer1-devel >= %{version}
BuildRequires:  gstreamer1-plugins-base-devel >= %{version}
BuildRequires:  meson
BuildRequires:  orc-devel >= 0.4.5
BuildRequires:  x264-devel >= 0.0.0-0.28

# Provides locale files
# relax dep to >= to make fedora/rpmfusion upgrades easier
Requires:       %{name}-free%{?_isa} >= %{version}

# Subpkg is empty, so no point -- rex
Obsoletes: %{name}-devel-docs < 1.13

%description
GStreamer is a streaming media framework, based on graphs of elements which
operate on media data.

This package contains well-written plug-ins that can't be shipped in
gstreamer-plugins-good because:
- the license is not LGPL
- the license of the library is not LGPL
- there are possible licensing issues with the code.

%prep
%autosetup -p1 -n %{src_name}-%{version}


%build
%meson \
    -D package-name='gst-plugins-ugly 1.0 rpmfusion rpm' \
    -D package-origin='http://rpmfusion.org/' \
    -D asfdemux=disabled \
    -D dvdlpcmdec=disabled \
    -D dvdsub=disabled \
    -D realmedia=disabled \
    -D doc=disabled \
    -D cdio=disabled \
    -D dvdread=disabled \
    -D a52dec=disabled \
    -D sidplay=disabled \
    -D mpeg2dec=disabled \
    -D gpl=enabled \
    -D nls=disabled

%meson_build

%install
%meson_install

%files
%doc AUTHORS NEWS README.md README.static-linking RELEASE REQUIREMENTS
%license COPYING
%{_datadir}/gstreamer-1.0
# Plugins without external dependencies

# Plugins with external dependencies
%{_libdir}/gstreamer-1.0/libgstx264.so


%changelog
* Thu Jan 08 2026 Dominik Mierzejewski <dominik@greysector.net> - 1:1.26.10-1
- Update to 1.26.10

* Thu Dec 04 2025 Dominik Mierzejewski <dominik@greysector.net> - 1:1.26.9-1
- Update to 1.26.9

* Thu Nov 13 2025 Dominik Mierzejewski <dominik@greysector.net> - 1:1.26.8-1
- update to 1.26.8

* Sun Oct 19 2025 Dominik Mierzejewski <dominik@greysector.net> - 1:1.26.7-1
- update to 1.26.7

* Fri Sep 19 2025 Dominik Mierzejewski <dominik@greysector.net> - 1:1.26.6-1
- update to 1.26.6

* Thu Sep 04 2025 Sérgio Basto <sergio@serjux.com> - 1:1.26.5-2
- Rebuild for x264

* Thu Aug 14 2025 Dominik Mierzejewski <dominik@greysector.net> - 1:1.26.5-1
- update to 1.26.5

* Sun Jul 27 2025 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1:1.26.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jun 27 2025 Dominik Mierzejewski <dominik@greysector.net> - 1:1.26.3-1
- update to 1.26.3

* Mon Jun 02 2025 Dominik Mierzejewski <dominik@greysector.net> - 1:1.26.2-1
- update to 1.26.2

* Tue Apr 29 2025 Dominik Mierzejewski <dominik@greysector.net> - 1:1.26.1-1
- update to 1.26.1

* Tue Mar 18 2025 Dominik Mierzejewski <dominik@greysector.net> - 1:1.26.0-1
- update to 1.26.0

* Tue Jan 28 2025 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1:1.24.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jan 09 2025 Dominik Mierzejewski <dominik@greysector.net> - 1:1.24.11-1
- update to 1.24.11

* Sun Dec 08 2024 Dominik Mierzejewski <dominik@greysector.net> - 1:1.24.10-1
- update to 1.24.10

* Sat Nov 02 2024 Dominik Mierzejewski <dominik@greysector.net> - 1:1.24.9-1
- Update to 1.24.9

* Thu Oct 03 2024 Sérgio Basto <sergio@serjux.com> - 1:1.24.8-1
- Update gstreamer1-plugins-ugly to 1.24.8

* Mon Aug 26 2024 Dominik Mierzejewski <dominik@greysector.net> - 1:1.24.7-1
- Update to 1.24.7

* Fri Aug 02 2024 Dominik Mierzejewski <dominik@greysector.net> - 1:1.24.6-1
- Update to 1.24.6

* Fri Aug 02 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1:1.24.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jun 06 2024 Dominik Mierzejewski <dominik@greysector.net> - 1:1.24.4-1
- Update to 1.24.4

* Tue Apr 09 2024 Dominik Mierzejewski <dominik@greysector.net> - 1:1.24.0-1
- Update to 1.24.0

* Sat Feb 03 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1:1.22.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jan 31 2024 Dominik Mierzejewski <dominik@greysector.net> - 1:1.22.9-1
- Update to 1.22.9

* Wed Dec 20 2023 Dominik Mierzejewski <dominik@greysector.net> - 1:1.22.8-1
- Update to 1.22.8
- Drop plugins moved to Fedora

* Wed Nov 15 2023 Nicolas Chauvet <kwizart@gmail.com> - 1:1.22.7-1
- Update to 1.22.7

* Thu Nov 02 2023 Leigh Scott <leigh123linux@gmail.com> - 1:1.22.6-1
- Update gstreamer1-plugins-ugly to 1.22.6

* Sat Aug 12 2023 Leigh Scott <leigh123linux@gmail.com> - 1:1.22.5-1
- Update gstreamer1-plugins-ugly to 1.22.5

* Wed Aug 02 2023 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1:1.22.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu May 25 2023 Sérgio Basto <sergio@serjux.com> - 1:1.22.3-1
- Update gstreamer1-plugins-ugly to 1.22.3

* Sun Apr 23 2023 Leigh Scott <leigh123linux@gmail.com> - 1:1.22.2-1
- Updated to version 1.22.2

* Wed Mar 29 2023 Vitaly Zaitsev <vitaly@easycoding.org> - 1:1.22.1-1
- Updated to version 1.22.1.

* Fri Mar 17 2023 Leigh Scott <leigh123linux@gmail.com> - 1:1.22.0-2
- Fix rfbz#6605

* Sun Feb 19 2023 Leigh Scott <leigh123linux@gmail.com> - 1:1.22.0-1
- Update gstreamer1-plugins-ugly to 1.22.0

* Thu Jan 12 2023 Vitaly Zaitsev <vitaly@easycoding.org> - 1:1.20.5-1
- Updated to version 1.20.5.

* Sat Nov 12 2022 Leigh Scott <leigh123linux@gmail.com> - 1:1.20.4-1
- Updated to version 1.20.4

* Sun Aug 07 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1:1.20.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild and ffmpeg
  5.1

* Fri Jul 22 2022 Vitaly Zaitsev <vitaly@easycoding.org> - 1:1.20.3-1
- Updated to version 1.20.3.

* Sun Jun 12 2022 Sérgio Basto <sergio@serjux.com> - 1:1.20.0-2
- Mass rebuild for x264-0.164

* Sun Feb 06 2022 Sérgio Basto <sergio@serjux.com> - 1:1.20.0-1
- Update gstreamer1-plugins-ugly to 1.20.0

* Mon Nov 15 2021 Sérgio Basto <sergio@serjux.com> - 1:1.19.3-1
- Update gstreamer1-plugins-ugly to 1.19.3

* Sat Oct 09 2021 Sérgio Basto <sergio@serjux.com> - 1:1.19.2-1
- Update gstreamer1-plugins-ugly to 1.19.2

* Mon Aug 02 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1:1.19.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild
- gstreamer1.prov is broken and hangs the build, workarround it


* Sat Jul 10 2021 Sérgio Basto <sergio@serjux.com> - 1:1.19.1-2
- Mass rebuild for x264-0.163

* Tue Jun 08 2021 Leigh Scott <leigh123linux@gmail.com> - 1.19.1-1
- Update

* Wed Mar 17 2021 Leigh Scott <leigh123linux@gmail.com> - 1.18.4-1
- 1.18.4

* Wed Feb 03 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.18.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sun Dec 13 2020 Leigh Scott <leigh123linux@gmail.com> - 1.18.2-1
- 1.18.2

* Fri Nov 27 2020 Sérgio Basto <sergio@serjux.com> - 1.18.1-2
- Mass rebuild for x264-0.161

* Sun Nov  1 2020 Leigh Scott <leigh123linux@gmail.com> - 1.18.1-1
- 1.18.1

* Wed Sep  9 2020 Leigh Scott <leigh123linux@gmail.com> - 1.18.0-1
- 1.18.0

* Sun Aug 23 2020 Leigh Scott <leigh123linux@gmail.com> - 1.17.90-1
- 1.17.90

* Tue Aug 18 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.17.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 08 2020 Leigh Scott <leigh123linux@gmail.com> - 1.17.2-1
- 1.17.2

* Tue Jul 07 2020 Sérgio Basto <sergio@serjux.com> - 1.17.1-2
- Mass rebuild for x264

* Mon Jun 22 2020 Leigh Scott <leigh123linux@gmail.com> - 1.17.1-1
- 1.17.1

* Thu Mar 12 2020 Leigh Scott <leigh123linux@gmail.com> - 1.16.2-3
- Rebuilt for i686

* Tue Feb 04 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.16.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Feb 01 2020 Leigh Scott <leigh123linux@googlemail.com> - 1.16.2-1
- 1.16.2

* Tue Dec 17 2019 Leigh Scott <leigh123linux@gmail.com> - 1.16.1-2
- Mass rebuild for x264

* Wed Sep 25 2019 Leigh Scott <leigh123linux@googlemail.com> - 1.16.1-1
- 1.16.1

* Fri Aug 09 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.16.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 16 2019 Leigh Scott <leigh123linux@gmail.com> - 1.16.0-2
- Disable mpeg2dec, it's been moved to the fedora package

* Wed Apr 24 2019 Leigh Scott <leigh123linux@gmail.com> - 1.16.0-1
- 1.16.0

* Mon Mar 18 2019 Sérgio Basto <sergio@serjux.com> - 1.15.2-1
- Update to 1.15.2

* Tue Mar 12 2019 Sérgio Basto <sergio@serjux.com> - 1.15.1-3
- Mass rebuild for x264

* Mon Mar 04 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.15.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Feb 09 2019 Leigh Scott <leigh123linux@googlemail.com> - 1.15.1-1
- 1.15.1
- clean spec

* Wed Nov 07 2018 Rex Dieter <rdieter@fedoraproject.org> - 1.14.4-2
- rebuild for x264 (rf#5071)

* Tue Oct 09 2018 Rex Dieter <rdieter@fedoraproject.org> - 1.14.4-1
- 1.14.4

* Thu Oct 04 2018 Sérgio Basto <sergio@serjux.com> - 1.14.3-2
- Mass rebuild for x264 and/or x265

* Tue Sep 18 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.14.3-1
- 1.14.3

* Sat Aug 18 2018 Rex Dieter <rdieter@fedoraproject.org> - 1.14.2-1
- 1.14.2

* Thu Jul 26 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.14.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu May 31 2018 Rex Dieter <rdieter@fedoraproject.org> - 1.14.1-2
- BR: s/mpeg2dec-devel/libmpeg2-devel/

* Thu May 31 2018 Rex Dieter <rdieter@fedoraproject.org> - 1.14.1-1
- 1.14.1

* Fri Mar 23 2018 Rex Dieter <rdieter@fedoraproject.org> - 1.14.0-1
- 1.14.0

* Wed Feb 28 2018 Rex Dieter <rdieter@fedoraproject.org> - 1.13.1-1
- 1.13.1

* Wed Jan 17 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.12.4-3
- remove twolame (rfbz#4766)

* Sat Dec 30 2017 Sérgio Basto <sergio@serjux.com> - 1.12.4-2
- Mass rebuild for x264 and x265

* Mon Dec 11 2017 Leigh Scott <leigh123linux@googlemail.com> - 1.12.4-1
- Update to 1.12.4

* Thu Sep 21 2017 Leigh Scott <leigh123linux@googlemail.com> - 1.12.3-1
- Update to 1.12.3

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 1.12.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jul 18 2017 Leigh Scott <leigh123linux@googlemail.com> - 1.12.2-1
- Update to 1.12.2

* Sun Jul 09 2017 Leigh Scott <leigh123linux@googlemail.com> - 1.12.1-3
- A better fix, add requires gstreamer1-plugins-ugly-free-devel (rfbz #4589)

* Sun Jul 09 2017 Leigh Scott <leigh123linux@googlemail.com> - 1.12.1-2
- Remove conflicting file in devel-docs (rfbz #4589)

* Fri Jun 23 2017 Leigh Scott <leigh123linux@googlemail.com> - 1.12.1-1
- Update to 1.12.1

* Fri May 12 2017 Leigh Scott <leigh123linux@googlemail.com> - 1.12.0-2
- Remove lame plugin

* Thu May 11 2017 Leigh Scott <leigh123linux@googlemail.com> - 1.12.0-1
- Update to 1.12.0
- Add requires gstreamer1-plugins-ugly-free
- remove a52dec, cdio, dvdread and xingmux plugins,
  moved to gstreamer1-plugins-ugly-free package.
- Remove locale files

* Tue Apr 18 2017 Leigh Scott <leigh123linux@googlemail.com> - 1.11.90-1
- Update to 1.11.90
- Upstream renamed libgstrmdemux.so to libgstrealmedia.so

* Sun Mar 19 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 1.11.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Feb 27 2017 Leigh Scott <leigh123linux@googlemail.com> - 1.11.2-1
- Update to 1.11.2
- Add upstream gcc-7 commit

* Mon Jan 16 2017 Leigh Scott <leigh123linux@googlemail.com> - 1.11.1-1
- Update to 1.11.1
- Remove libmad bits as mad is no longer included in the source

* Wed Nov 30 2016 leigh scott <leigh123linux@googlemail.com> - 1.10.2-1
- Update to 1.10.2

* Fri Nov 18 2016 Adrian Reber <adrian@lisas.de> - 1.10.0-3
- Rebuilt for libcdio-0.94

* Sun Nov 13 2016 Hans de Goede <j.w.r.degoede@gmail.com> - 1.10.0-2
- Drop mpg123 plugin, it is in Fedora proper now

* Fri Nov 11 2016 Hans de Goede <j.w.r.degoede@gmail.com> - 1.10.0-1
- Rebase to new upstream release 1.10.0

* Sun Jun 12 2016 Hans de Goede <j.w.r.degoede@gmail.com> - 1.8.2-1
- Rebase to new upstream release 1.8.2

* Wed May 18 2016 Hans de Goede <j.w.r.degoede@gmail.com> - 1.8.1-1
- Rebase to new upstream release 1.8.1

* Sat Jan 23 2016 Hans de Goede <j.w.r.degoede@gmail.com> - 1.6.3-1
- Rebase to new upstream release 1.6.3

* Thu Dec 24 2015 Hans de Goede <j.w.r.degoede@gmail.com> - 1.6.2-1
- Rebase to new upstream release 1.6.2

* Sat Oct 31 2015 Hans de Goede <j.w.r.degoede@gmail.com> - 1.6.1-1
- Rebase to new upstream release 1.6.1

* Sat May 16 2015 Hans de Goede <j.w.r.degoede@gmail.com> - 1.4.5-1
- Rebase to new upstream release 1.4.5

* Wed Oct  1 2014 Hans de Goede <j.w.r.degoede@gmail.com> - 1.4.3-1
- Rebase to new upstream release 1.4.3

* Fri Aug 29 2014 Hans de Goede <j.w.r.degoede@gmail.com> - 1.4.1-1
- Rebase to new upstream release 1.4.1 (rf#3343)

* Sun Jun 15 2014 Hans de Goede <j.w.r.degoede@gmail.com> - 1.2.4-1
- Rebase to new upstream release 1.2.4

* Sat Mar 22 2014 Sérgio Basto <sergio@serjux.com> - 1.2.3-3
- Rebuilt for x264

* Thu Mar 06 2014 Nicolas Chauvet <kwizart@gmail.com> - 1.2.3-2
- Rebuilt for x264

* Sun Feb 23 2014 Hans de Goede <j.w.r.degoede@gmail.com> - 1.2.3-1
- Rebase to new upstream release 1.2.3

* Fri Feb 21 2014 Nicolas Chauvet <kwizart@gmail.com> - 1.2.1-2
- Rebuilt

* Sat Nov 16 2013 Hans de Goede <j.w.r.degoede@gmail.com> - 1.2.1-1
- Rebase to new upstream release 1.2.1

* Tue Nov 05 2013 Nicolas Chauvet <kwizart@gmail.com> - 1.2.0-3
- Rebuilt for x264/FFmpeg

* Tue Oct 22 2013 Nicolas Chauvet <kwizart@gmail.com> - 1.2.0-2
- Rebuilt for x264

* Sun Oct 13 2013 Hans de Goede <j.w.r.degoede@gmail.com> - 1.2.0-1
- Rebase to new upstream release 1.2.0

* Thu Aug 08 2013 Hans de Goede <j.w.r.degoede@gmail.com> - 1.1.3-1
- Rebase to new upstream release 1.1.3

* Wed Aug 07 2013 Hans de Goede <j.w.r.degoede@gmail.com> - 1.0.9-1
- New upstream release 1.0.9

* Tue May 07 2013 Nicolas Chauvet <kwizart@gmail.com> - 1.0.6-2
- Rebuilt for x264

* Mon Mar 25 2013 Hans de Goede <j.w.r.degoede@gmail.com> - 1.0.6-1
- New upstream release 1.0.6

* Sat Mar  2 2013 Hans de Goede <j.w.r.degoede@gmail.com> - 1.0.5-1
- New upstream release 1.0.5
- Drop no longer needed PyXML BuildRequires (rf#2572)

* Sun Jan 20 2013 Nicolas Chauvet <kwizart@gmail.com> - 1.0.2-3
- Rebuilt for FFmpeg/x264

* Fri Nov 23 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.0.2-2
- Rebuilt for x264

* Sun Oct 28 2012 Hans de Goede <j.w.r.degoede@gmail.com> - 1.0.2-1
- New upstream release 1.0.2

* Sun Sep 23 2012 Hans de Goede <j.w.r.degoede@gmail.com> - 0.11.99-1
- New upstream release 0.11.99

* Sun Sep 16 2012 Hans de Goede <j.w.r.degoede@gmail.com> - 0.11.93-2
- Fix gtk-doc dir ownership (rf#2474)

* Sun Sep  9 2012 Hans de Goede <j.w.r.degoede@gmail.com> - 0.11.93-1
- First version of gstreamer1-plugins-ugly for rpmfusion
