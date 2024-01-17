## START: Set by rpmautospec
## (rpmautospec version 0.3.5)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 12;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# Build with aom
%bcond_without aom
# Build SVT-AV1
%bcond_without svt
%if (0%{?rhel} && 0%{?rhel} < 9) || 0%{?rhel} >= 10
%bcond_with rav1e
%else
%bcond_without rav1e
%endif
%if 0%{?rhel} >= 10
%bcond_with gtest
%else
%bcond_without gtest
%endif
%bcond_without check

Name:           libavif
Version:        1.0.3
Release:        %autorelease
Summary:        Library for encoding and decoding .avif files

License:        BSD-2-Clause
URL:            https://github.com/AOMediaCodec/libavif
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++
%{?with_check:%{?with_gtest:BuildRequires:  gtest-devel}}
BuildRequires:  nasm
%if %{with aom}
BuildRequires:  pkgconfig(aom)
%endif
BuildRequires:  pkgconfig(dav1d)
BuildRequires:  pkgconfig(libjpeg)
BuildRequires:  pkgconfig(libpng)
%{?with_rav1e:BuildRequires:  pkgconfig(rav1e)}
%{?with_svt:BuildRequires:  pkgconfig(SvtAv1Enc)}
BuildRequires:  pkgconfig(zlib)

%description
This library aims to be a friendly, portable C implementation of the AV1 Image
File Format, as described here:

https://aomediacodec.github.io/av1-avif/

%package devel
Summary:        Development files for libavif
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
This package holds the development files for libavif.

%package tools
Summary:        Tools to encode and decode AVIF files

%description tools
This library aims to be a friendly, portable C implementation of the AV1 Image
File Format, as described here:

https://aomediacodec.github.io/av1-avif/

This package holds the commandline tools to encode and decode AVIF files.

%package     -n avif-pixbuf-loader
Summary:        AVIF image loader for GTK+ applications
BuildRequires:  pkgconfig(gdk-pixbuf-2.0)
Requires:       gdk-pixbuf2%{?_isa}

%description -n avif-pixbuf-loader
Avif-pixbuf-loader contains a plugin to load AVIF images in GTK+ applications.

%prep
%autosetup -p1

%build
%cmake \
    -DCMAKE_BUILD_TYPE=RelWithDebInfo \
    %{?with_aom:-DAVIF_CODEC_AOM=1} \
    -DAVIF_CODEC_DAV1D=1 \
    %{?with_rav1e:-DAVIF_CODEC_RAV1E=1} \
    %{?with_svt:-DAVIF_CODEC_SVT=1} \
    -DAVIF_BUILD_APPS=1 \
    -DAVIF_BUILD_GDK_PIXBUF=1 \
    %{?with_check:-DAVIF_BUILD_TESTS=1 -DAVIF_ENABLE_GTEST=%{with gtest}}
%cmake_build

%install
%cmake_install

%if %{with check}
%check
%ctest
%endif

%files
%license LICENSE
# Do not glob the soname
%{_libdir}/libavif.so*
%{_datadir}/thumbnailers/avif.thumbnailer

%files devel
%{_libdir}/libavif.so
%{_includedir}/avif/
%{_libdir}/cmake/libavif/
%{_libdir}/pkgconfig/libavif.pc

%files tools
%doc CHANGELOG.md README.md
%{_bindir}/avifdec
%{_bindir}/avifenc

%files -n avif-pixbuf-loader
%{_libdir}/gdk-pixbuf-2.0/*/loaders/libpixbufloader-avif.so

%changelog
* Fri Jan 12 2024 Fabio Valentini <decathorpe@gmail.com> - 0.11.1-12
- Rebuild for dav1d 1.3.0

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 21 2023 Jiri Kucera <jkucera@redhat.com> - 0.11.1-10
- Drop gtest on RHEL

* Fri Mar 17 2023 Dominik 'Rathann' Mierzejewski <dominik@greysector.net> - 0.11.1-9
- ensure gdk-pixbuf2 dependency matches avif-pixbuf-loader arch

* Fri Mar 17 2023 Dominik 'Rathann' Mierzejewski <dominik@greysector.net> - 0.11.1-8
- enable tests

* Fri Mar 17 2023 Dominik 'Rathann' Mierzejewski <dominik@greysector.net> - 0.11.1-7
- enable svt-av1 support on all arches (resolves rhbz#2162675)

* Thu Feb 23 2023 Andreas Schneider <asn@cryptomilk.org> - 0.11.1-6
- Update License to SPDX expressions

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Dec 01 2022 Kalev Lember <klember@redhat.com> - 0.11.1-4
- Enable rav1e support for EPEL 9

* Wed Nov 30 2022 Kalev Lember <klember@redhat.com> - 0.11.1-3
- Fix rav1e conditional for non-RHEL

* Thu Nov 03 2022 Kalev Lember <klember@redhat.com> - 0.11.1-2
- Fix typo in devel package summary

* Sun Oct 23 2022 Robert-André Mauchin <zebob.m@gmail.com> - 0.11.1-1
- Update to 0.11.1

* Sun Oct 23 2022 Robert-André Mauchin <zebob.m@gmail.com> - 0.10.1-4
- Add condition for rav1e for EPEL integration - Close: rhbz#2071940

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jun 24 2022 Stephen Gallagher <sgallagh@redhat.com> - 0.10.1-2
- Rebuild for libdav1d soname bump in ELN

* Mon Jun 20 2022 Robert-André Mauchin <zebob.m@gmail.com> - 0.10.1-1
- Update to 0.10.1 Close: rhbz#2073138

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Dec 28 2021 Robert-André Mauchin <zebob.m@gmail.com> - 0.9.3-2
- Rebuild

* Mon Nov 29 2021 Robert-André Mauchin <zebob.m@gmail.com> - 0.9.3-1
- Update to 0.9.3 Close: rhbz#2016224

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sun Jun 13 13:40:21 CEST 2021 Robert-André Mauchin <zebob.m@gmail.com> - 0.9.1-2
- Rebuilt for aom v3.1.1

* Sun May 23 19:44:09 CEST 2021 Robert-André Mauchin <zebob.m@gmail.com> - 0.9.1-1
- Update to 0.9.1
- Close: rhbz#1937556

* Mon Mar 15 2021 Andreas Schneider <asn@redhat.com> - 0.9.0-1
- Update to version 0.9.0

* Wed Mar 10 2021 Leigh Scott <leigh123linux@gmail.com> - 0.8.4-5
- Build with aom

* Wed Mar 10 2021 Leigh Scott <leigh123linux@gmail.com> - 0.8.4-4
- Build without aom for new vmaf version

* Sat Feb 20 2021 Andreas Schneider <asn@redhat.com> - 0.8.4-4
- Build release with debug info

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Dec 14 2020 Robert-André Mauchin <zebob.m@gmail.com> - 0.8.4-2
- Rebuild for dav1d SONAME bump

* Wed Dec 09 05:52:07 CET 2020 Robert-André Mauchin <zebob.m@gmail.com> - 0.8.4-1
- Update to version 0.8.4

* Mon Oct 19 2020 Andreas Schneider <asn@redhat.com> - 0.8.2-1
- Update to version 0.8.2
  https://github.com/AOMediaCodec/libavif/blob/master/CHANGELOG.md

* Thu Aug 06 22:14:02 CEST 2020 Robert-André Mauchin <zebob.m@gmail.com> - 0.8.1-1
- Update to 0.8.1

* Wed Aug 05 21:17:23 CEST 2020 Robert-André Mauchin <zebob.m@gmail.com> - 0.8.0-1
- Update to 0.8.0

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.3-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri May 22 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 0.7.3-1
- Update to 0.7.3

* Wed Apr 29 2020 Andreas Schneider <asn@redhat.com> - 0.7.2-1
- Update to version 0.7.2
  * https://github.com/AOMediaCodec/libavif/blob/master/CHANGELOG.md

* Wed Apr 29 2020 Andreas Schneider <asn@redhat.com> - 0.7.1-1
- Update to version 0.7.1

* Wed Mar 04 2020 Andreas Schneider <asn@redhat.com> - 0.5.7-1
- Update to version 0.5.7

* Wed Mar 04 2020 Andreas Schneider <asn@redhat.com> - 0.5.3-2
- Fix License

* Sun Feb 16 2020 Andreas Schneider <asn@redhat.com> - 0.5.3-1
- Initial version

