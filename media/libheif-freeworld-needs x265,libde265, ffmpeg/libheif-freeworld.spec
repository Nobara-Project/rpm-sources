Name:           libheif-freeworld
Version:        1.21.2
Release:        3%{?dist}
Summary:        HEVC support for HEIF and AVIF file format decoder and encoder

License:        LGPL-3.0-or-later and MIT
URL:            https://github.com/strukturag/libheif
Source0:        %{url}/archive/v%{version}/libheif-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  cmake(vvenc)
BuildRequires:  gcc-c++
BuildRequires:  ninja-build
BuildRequires:  pkgconfig(libavcodec)
BuildRequires:  pkgconfig(libde265)
BuildRequires:  pkgconfig(x265)
BuildRequires:  pkgconfig(aom)
BuildRequires:  pkgconfig(zlib)
Requires:       libheif%{_isa} = %{version}
Supplements:    libheif%{_isa}
Provides:       libheif-hevc = %{version}-%{release}
Obsoletes:      libheif-hevc < %{version}-%{release}

%description
libheif is an ISO/IEC 23008-12:2017 HEIF and AVIF (AV1 Image File Format)
file format decoder and encoder.

This package adds support for HEVC-encoded HEIC files to applications
that use libheif to read HEIF image files.

%prep
%autosetup -p1 -n libheif-%{version}
rm -rf third-party/

%build
%cmake \
 -GNinja \
 -DBUILD_TESTING=ON \
 -DCMAKE_COMPILE_WARNING_AS_ERROR=OFF \
 -DPLUGIN_DIRECTORY=%{_libdir}/libheif \
 -DWITH_EXAMPLES:BOOL=OFF \
 -DWITH_FFMPEG_DECODER=ON \
 -DWITH_FFMPEG_DECODER_PLUGIN=ON \
 -DWITH_LIBDE265_PLUGIN:BOOL=ON \
 -DWITH_UNCOMPRESSED_CODEC=ON \
 -DWITH_VVENC:BOOL=ON \
 -DWITH_VVENC_PLUGIN:BOOL=ON \
 -DWITH_X265_PLUGIN:BOOL=ON \
 -Wno-dev

%cmake_build

%install
%cmake_install
pushd %{buildroot}
rm -rv .%{_includedir}/libheif
rm -rv .%{_libdir}/cmake/libheif
rm -rv .%{_libdir}/libheif.so*
rm  -v .%{_libdir}/pkgconfig/libheif.pc
popd

%check
%ctest

%files
%license COPYING
%doc README.md
%{_libdir}/libheif/libheif-ffmpegdec.so
%{_libdir}/libheif/libheif-libde265.so
%{_libdir}/libheif/libheif-vvenc.so
%{_libdir}/libheif/libheif-x265.so

%changelog
* Thu Mar 19 2026 Leigh Scott <leigh123linux@gmail.com> - 1.21.2-3
- Rebuild for new libde265

* Wed Mar 18 2026 Leigh Scott <leigh123linux@gmail.com> - 1.21.2-2
- Rebuild for new libde265

* Fri Jan 16 2026 Dominik Mierzejewski <dominik@greysector.net> - 1.21.2-1
- update to 1.21.2

* Fri Jan 09 2026 Dominik Mierzejewski <dominik@greysector.net> - 1.21.1-2
- enable vvenc support

* Tue Jan 06 2026 Sérgio Basto <sergio@serjux.com> - 1.21.1-1
- Update libheif-freeworld to 1.21.1

* Wed Nov 05 2025 Leigh Scott <leigh123linux@gmail.com> - 1.20.2-3
- Rebuild for ffmpeg-8.0

* Tue Oct 07 2025 Leigh Scott <leigh123linux@gmail.com> - 1.20.2-2
- Rebuild for svt-av1 soname bump

* Wed Sep 10 2025 Dominik Mierzejewski <dominik@greysector.net> - 1.20.2-1
- update to 1.20.2

* Sun Jul 27 2025 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.20.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jul 06 2025 Dominik Mierzejewski <dominik@greysector.net> - 1.20.1-1
- update to 1.20.1
- fix skipped test when HEVC encoder is built as plugin
- add explicit build dependency on zlib to run more tests

* Tue Apr 29 2025 Dominik Mierzejewski <dominik@greysector.net> - 1.19.8-1
- update to 1.19.8

* Tue Mar 18 2025 Dominik Mierzejewski <dominik@greysector.net> - 1.19.7-1
- update to 1.19.7 (resolves rhbz#2349315)

* Tue Jan 28 2025 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.19.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sun Nov 24 2024 Sérgio Basto <sergio@serjux.com> - 1.19.5-1
- Update libheif-freeworld to 1.19.5

* Sat Nov 23 2024 Leigh Scott <leigh123linux@gmail.com> - 1.19.3-2
- Rebuild for new x265

* Tue Nov 12 2024 Dominik Mierzejewski <dominik@greysector.net> - 1.19.3-1
- update to 1.19.3 (resolves rhbz#2295525)
- drop obsolete patches
- run tests unconditionally, they no longer require special build options

* Tue Oct 08 2024 Nicolas Chauvet <kwizart@gmail.com> - 1.17.6-4
- Rebuilt

* Mon Sep 30 2024 Leigh Scott <leigh123linux@gmail.com> - 1.17.6-3
- Rebuild for x265

* Fri Aug 02 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.17.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun May 26 2024 Robert-André Mauchin <zebob.m@gmail.com> - 1.17.6-1
- Update to 1.17.6
- Fix CVE-2024-25269

* Sat Apr 06 2024 Leigh Scott <leigh123linux@gmail.com> - 1.17.5-3
- Rebuild for new x265 version

* Sat Feb 03 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.17.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Dec 15 2023 Dominik Mierzejewski <dominik@greysector.net> - 1.17.5-2
- Update to 1.17.5 (rhbz#2244583)
- Backport fixes for: CVE-2023-49460 (rhbz#2253575, rhbz#2253576)
                      CVE-2023-49462 (rhbz#2253567, rhbz#2253568)
                      CVE-2023-49463 (rhbz#2253565, rhbz#2253566)
                      CVE-2023-49464 (rhbz#2253562, rhbz#2253563)
- Enable HEVC decoding via libavcodec

* Fri Sep 08 2023 Dominik Mierzejewski <dominik@greysector.net> - 1.16.2-2
- Enable uncompressed codec (rhbz#2237849)
- Run tests conditionally (requires making all symbols visible)

* Mon Sep 04 2023 Dominik Mierzejewski <dominik@greysector.net> - 1.16.2-1
- update to 1.16.2

* Wed Aug 02 2023 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.16.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sun May 07 2023 Sérgio Basto <sergio@serjux.com> - 1.16.1-1
- Update libheif-freeworld to 1.16.1

* Sun Apr 30 2023 Dominik Mierzejewski <dominik@greysector.net> - 1.15.2-2
- backport fix for issue#590

* Fri Apr 21 2023 Dominik Mierzejewski <dominik@greysector.net> - 1.15.2-1
- update to 1.15.2
- drop obsolete patch

* Sun Apr 16 2023 Sérgio Basto <sergio@serjux.com> - 1.15.1-5
- Obsolete libheif-hevc to prevent conflict

* Tue Apr 11 2023 Sérgio Basto <sergio@serjux.com> - 1.15.1-4
- add supplements:libheif

* Sat Apr 08 2023 Dominik Mierzejewski <dominik@greysector.net> - 1.15.3-1
- rename main package to libheif-freeworld to avoid conflict in koji

* Wed Mar 22 2023 Dominik Mierzejewski <dominik@greysector.net> - 1.15.1-2.1
- drop explicit dependency on main package from -hevc subpackage

* Fri Mar 17 2023 Neal Gompa <ngompa@fedoraproject.org> - 1.15.1-2
- Adapt for Fedora

* Fri Feb 17 2023 Leigh Scott <leigh123linux@gmail.com> - 1.15.1-1
- Update to 1.15.1

* Sat Jan 07 2023 Leigh Scott <leigh123linux@gmail.com> - 1.14.2-1
- Update to 1.14.2
- Switch back to autotools to build due to cmake issues (rfbz#6550}

* Thu Jan 05 2023 Leigh Scott <leigh123linux@gmail.com> - 1.14.1-1
- Update to 1.14.1

* Mon Dec 19 2022 Leigh Scott <leigh123linux@gmail.com> - 1.14.0-4
- Don't build rav1e and SVT-AV1 as plugins (rfbz#6532)

* Mon Dec 05 2022 Nicolas Chauvet <kwizart@gmail.com> - 1.14.0-3
- Fix for SvtAv1Enc in devel - rfbz#6521

* Wed Nov 23 2022 Nicolas Chauvet <kwizart@gmail.com> - 1.14.0-2
- Enable svt-av1 on el9

* Tue Nov 15 2022 Leigh Scott <leigh123linux@gmail.com> - 1.14.0-1
- Update to 1.14.0

* Fri Sep 02 2022 Leigh Scott <leigh123linux@gmail.com> - 1.13.0-1
- Update to 1.13.0

* Sun Aug 07 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.12.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild and ffmpeg
  5.1

* Thu Jun 23 2022 Robert-André Mauchin <zebob.m@gmail.com> - 1.12.0-5
- Rebuilt for new dav1d, rav1e and jpegxl

* Wed Feb 09 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.12.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Nov 25 2021 Nicolas Chauvet <kwizart@gmail.com> - 1.12.0-3
- Rebuilt

* Tue Aug 03 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.12.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jun 14 2021 Leigh Scott <leigh123linux@gmail.com> - 1.12.0-1
- Update to 1.12.0

* Sun Jun 13 2021 Robert-André Mauchin <zebob.m@gmail.com> - 1.11.0-3
- Rebuild for new aom

* Wed Apr 14 2021 Leigh Scott <leigh123linux@gmail.com> - 1.11.0-2
- Rebuild for new x265

* Sat Feb 20 2021 Leigh Scott <leigh123linux@gmail.com> - 1.11.0-1
- Update to 1.11.0

* Wed Feb 03 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Dec 19 2020 Leigh Scott <leigh123linux@gmail.com> - 1.10.0-1
- Update to 1.10.0

* Mon Dec 14 2020 Leigh Scott <leigh123linux@gmail.com> - 1.9.1-3
- Actually do the dav1d rebuild

* Mon Dec 14 2020 Robert-André Mauchin <zebob.m@gmail.com> - 1.9.1-2
- Rebuild for dav1d SONAME bump

* Tue Oct 27 2020 Leigh Scott <leigh123linux@gmail.com> - 1.9.1-1
- Update to 1.9.1

* Fri Aug 28 2020 Leigh Scott <leigh123linux@gmail.com> - 1.8.0-1
- Update to 1.8.0

* Tue Aug 18 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.7.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 08 2020 Leigh Scott <leigh123linux@gmail.com> - 1.7.0-2
- Rebuilt

* Thu Jun 04 2020 Leigh Scott <leigh123linux@gmail.com> - 1.7.0-1
- Update to 1.7.0

* Sun May 31 2020 Leigh Scott <leigh123linux@gmail.com> - 1.6.2-3
- Rebuild for new x265 version

* Sun Feb 23 2020 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 1.6.2-2
- Rebuild for x265

* Mon Feb 10 2020 Leigh Scott <leigh123linux@gmail.com> - 1.6.2-1
- Update to 1.6.2

* Tue Feb 04 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Nov 28 2019 Leigh Scott <leigh123linux@googlemail.com> - 1.6.0-1
- Update to 1.6.0
- Rebuilt for x265

* Sun Nov 03 2019 Leigh Scott <leigh123linux@googlemail.com> - 1.5.1-1
- Update to 1.5.1

* Fri Aug 09 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jul 02 2019 Nicolas Chauvet <kwizart@gmail.com> - 1.4.0-3
- Rebuilt for x265

* Mon Mar 04 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Feb 28 2019 Leigh Scott <leigh123linux@googlemail.com> - 1.4.0-1
- Update to 1.4.0

* Thu Jan 03 2019 Leigh Scott <leigh123linux@googlemail.com> - 1.3.2-2
- Rebuild for new x265 for el7

* Thu Nov 29 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.3.2-1
- First build
