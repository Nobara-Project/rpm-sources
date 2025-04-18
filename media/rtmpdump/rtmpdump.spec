%global commit f1b83c10d8beb43fcc70a6e88cf4325499f25857
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global gitdate 20210219

Name:           rtmpdump
Version:        2.4
Release:        26.%{gitdate}.git%{shortcommit}%{?dist}
Summary:        Toolkit for RTMP streams

# The tools are GPLv2+. The library is LGPLv2+, see below.
License:        GPLv2+
URL:            https://rtmpdump.mplayerhq.hu/
Source0:        https://git.ffmpeg.org/gitweb/rtmpdump.git/snapshot/%{commit}.tar.gz#/rtmpdump-%{shortcommit}.tar.gz
Patch0:         gcc14_buildfix.patch

BuildRequires:  gcc
BuildRequires:  gnutls-devel
BuildRequires:  libgcrypt-devel
BuildRequires:  zlib-devel
BuildRequires:  nettle-devel

# we should force the exact EVR for an ISA - not only the same ABI
Requires: librtmp%{?_isa} = %{version}-%{release}

%description
rtmpdump is a toolkit for RTMP streams. All forms of RTMP are supported,
including rtmp://, rtmpt://, rtmpe://, rtmpte://, and rtmps://.

%package -n librtmp
Summary:        Support library for RTMP streams
License:        LGPLv2+

%description -n librtmp
librtmp is a support library for RTMP streams. All forms of RTMP are supported,
including rtmp://, rtmpt://, rtmpe://, rtmpte://, and rtmps://.

%package -n librtmp-devel
Summary:        Files for librtmp development
License:        LGPLv2+
Requires:       librtmp%{?_isa} = %{version}-%{release}

%description -n librtmp-devel
librtmp is a support library for RTMP streams. The librtmp-devel package
contains include files needed to develop applications using librtmp.

%prep
%autosetup -p1 -n %{name}-%{shortcommit}

%build
# The fact that we have to add -ldl for gnutls is Fedora bug #611318
make SYS=posix CRYPTO=GNUTLS SHARED=yes OPT="%{optflags}" LIB_GNUTLS="-lgnutls -lgcrypt -ldl -lz"

%install
make CRYPTO=GNUTLS SHARED=yes DESTDIR=%{buildroot} prefix=%{_prefix} mandir=%{_mandir} libdir=%{_libdir} sbindir=%{_sbindir} install
rm -f %{buildroot}%{_libdir}/librtmp.a

%ldconfig_scriptlets librtmp

%files
%doc README
%license COPYING
%{_bindir}/rtmpdump
%{_sbindir}/rtmpsrv
%{_sbindir}/rtmpgw
%{_sbindir}/rtmpsuck
%{_mandir}/man1/rtmpdump.1*
%{_mandir}/man8/rtmpgw.8*

%files -n librtmp
%doc ChangeLog
%license librtmp/COPYING
%{_libdir}/librtmp.so.1

%files -n librtmp-devel
%{_includedir}/librtmp/
%{_libdir}/librtmp.so
%{_libdir}/pkgconfig/librtmp.pc
%{_mandir}/man3/librtmp.3*

%changelog
* Tue Jan 28 2025 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 2.4-26.20210219.gitf1b83c1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Aug 02 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 2.4-25.20210219.gitf1b83c1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Feb 04 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 2.4-24.20210219.gitf1b83c1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 28 2023 Nicolas Chauvet <kwizart@gmail.com> - 2.4-23.20210219.gitf1b83c1
- Switch git repo urls

* Sun Aug 07 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 2.4-22.20190330.gitc5f04a5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild and ffmpeg
  5.1

* Wed Feb 09 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 2.4-21.20190330.gitc5f04a5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Aug 03 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.4-20.20190330.gitc5f04a5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Feb 04 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.4-19.20190330.gitc5f04a5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Aug 18 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.4-18.20190330.gitc5f04a5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Mar 12 2020 Leigh Scott <leigh123linux@gmail.com> - 2.4-17.20190330.gitc5f04a5
- Rebuilt for i686

* Wed Feb 05 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.4-16.20190330.gitc5f04a5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Aug 09 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.4-15.20190330.gitc5f04a5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jul 09 2019 Sérgio Basto <sergio@serjux.com> - 2.4-14.20190330.gitc5f04a5
- Add the latest 2 commits, they appear to be security commits.

* Mon Mar 04 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.4-13.20160224.gitfa8646d
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild
- Remove Group tag
- Add BuildRequires:  gcc

* Sun Aug 19 2018 Leigh Scott <leigh123linux@googlemail.com> - 2.4-12.20160224.gitfa8646d
- Rebuilt for Fedora 29 Mass Rebuild binutils issue

* Fri Jul 27 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.4-11.20160224.gitfa8646d
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Mar 01 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 2.4-10.20160224.gitfa8646d
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 2.4-9.20160224.gitfa8646d
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Mar 20 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 2.4-8.20160224.gitfa8646d
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Jul 24 2016 Sérgio Basto <sergio@serjux.com> - 2.4-7.20160224.gitfa8646d
- Force the exact EVR

* Sun Jul 10 2016 Sérgio Basto <sergio@serjux.com> - 2.4-6.20160224.gitfa8646d
- Update last git version (as usual)
- Add license tag.

* Fri Nov 27 2015 Susi Lehtola <jussilehtola@fedoraproject.org> - 2.4-5.20150925.gita107cef
- Fix name of tarball in Sérgio's patch.

* Fri Sep 25 2015 Sérgio Basto <sergio@serjux.com> - 2.4-4.20150925.gita107cef
- Update to git dc76f0a, Jan 14 2015

* Mon Sep 01 2014 Sérgio Basto <sergio@serjux.com> - 2.4-3.20131205.gitdc76f0a
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Apr 26 2014 Nicolas Chauvet <kwizart@gmail.com> - 2.4-2.20131205.gitdc76f0a
- Rebuilt for libgcrypt

* Sun Jan 5 2014 Susi Lehtola <jussilehtola@fedoraproject.org> - 2.4-1.20131205.gitdc76f0a
- Update to newest snapshot.
- Clean up spec file.

* Sun Mar 03 2013 Nicolas Chauvet <kwizart@gmail.com> - 2.4-0.3.20110811gitc58cfb3e
- Mass rebuilt for Fedora 19 Features

* Wed Jan 25 2012 Nicolas Chauvet <kwizart@gmail.com> - 2.4-0.2.20110811gitc58cfb3e
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Aug 29 2011 David Woodhouse <dwmw2@infradead.org> 2.4-0.1.20110811gitc58cfb3e
- Update to almost-2.4 snapshot

* Sun Jul 04 2010 Dominik Mierzejewski <rpm@greysector.net> 2.3-2
- call ldconfig in post(un) scripts for the shared library
- add strict dependency on the library to -devel

* Sun Jul 04 2010 David Woodhouse <dwmw2@infradead.org> 2.3-1
- Update to 2.3; build shared library

* Fri Apr 30 2010 David Woodhouse <dwmw2@infradead.org> 2.2d-1
- Update to 2.2d

* Tue Apr 20 2010 David Woodhouse <dwmw2@infradead.org> 2.2c-2
- Link with libgcrypt explicitly since we call it directly

* Mon Apr 19 2010 David Woodhouse <dwmw2@infradead.org> 2.2c-1
- Initial package
