#global _with_gen4asm 1
%if 0%{?el7}
%global _without_wayland 1
%endif

%global commit0 d30e01329344858f3c84d0ef9c2b68cbde37bb9a
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global commitdate0 20241027

Name:		libva-intel-driver
Version:	2.4.1^%{commitdate0}git%{shortcommit0}
Release:	1%{?dist}
Summary:	HW video decode support for Intel integrated graphics
License:	MIT and EPL
URL:		https://github.com/intel/intel-vaapi-driver
Source0:	%{url}/archive/%{commit0}/intel-vaapi-driver-%{shortcommit0}.tar.gz
Source1:	intel-vaapi-driver.metainfo.xml
Source9:	parse-intel-vaapi-driver.py
Patch0:		https://github.com/digetx/intel-vaapi-driver/commit/d03fd1f86a9aeee0b33447aee3578aadb3a93f8a.patch
Patch1:		https://github.com/intel/intel-vaapi-driver/pull/548.patch
Patch2:		https://github.com/intel/intel-vaapi-driver/pull/514.patch

ExclusiveArch:	%{ix86} x86_64

BuildRequires:	libtool
BuildRequires:	gcc
BuildRequires:	python3
# AppStream metadata generation
BuildRequires:	libappstream-glib >= 0.6.3

#Renamed when moved to 01.org
Provides:	intel-vaapi-driver = %{version}-%{release}

%{?_with_gen4asm:BuildRequires:	pkgconfig(intel-gen4asm)}
BuildRequires:	systemd
BuildRequires:	glibc-devel%{?_isa}
BuildRequires:	libXext-devel%{?_isa}
BuildRequires:	libXfixes-devel%{?_isa}
BuildRequires:	libdrm-devel%{?_isa}
BuildRequires:	libpciaccess-devel%{?_isa}
BuildRequires:	libva-devel%{?_isa}
BuildRequires:	libGL-devel%{?_isa}
BuildRequires:	libEGL-devel%{?_isa}
%{!?_without_wayland:
BuildRequires:	wayland-devel%{?_isa}
}


%description
HW video decode support for Intel integrated graphics.
https://01.org/intel-media-for-linux


%prep
%autosetup -p1 -n intel-vaapi-driver-%{commit0}
%{?_with_gen4asm:
#Move pre-built (binary) asm code
for f in src/shaders/vme/*.g?b ; do
  mv ${f} ${f}.prebuilt
done
for f in src/shaders/h264/mc/*.g?b* ; do
  mv ${f} ${f}.prebuilt
done
}


%build
autoreconf -vif
%configure --disable-static \
  --enable-hybrid-codec

%make_build

%install
%make_install
find %{buildroot} -regex ".*\.la$" | xargs rm -f --

%{?_with_gen4asm:
#Display a diff between prebuit ASM and our generation
gendiff . .prebuilt
}

# install AppData and add modalias provides
mkdir -p %{buildroot}%{_datadir}/appdata/
install -pm 0644 %{SOURCE1} %{buildroot}%{_datadir}/appdata/
fn=%{buildroot}%{_datadir}/appdata/intel-vaapi-driver.metainfo.xml
%{SOURCE9} src/i965_pciids.h | xargs appstream-util add-provide ${fn} modalias


%files
%doc AUTHORS NEWS README
%license COPYING
%{_libdir}/dri/i965_drv_video.so
%{_datadir}/appdata/intel-vaapi-driver.metainfo.xml


%changelog
* Sat Feb 01 2025 Dominik Mierzejewski <dominik@greysector.net> - 2.4.1^20241027gitd30e013-1
- update to upstream commit d30e013
- drop redundant patch

* Tue Jan 28 2025 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 2.4.1^20221130gitab755cb-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Oct 01 2024 Dominik Mierzejewski <dominik@greysector.net> - 2.4.1^20221130gitab755cb-1
- switched to modern post-release versioning scheme
- use tabs consistently
- drop unnecessary Obsoletes
- Add pull requests 514, fixing glitches, and 566, making the deprecated wl_drm
  Wayland protocol optional. (rmader)

* Fri Aug 02 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 2.4.1-15.20221130gitab755cb
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Feb 03 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 2.4.1-14.20221130gitab755cb
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Aug 02 2023 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 2.4.1-13.20221130gitab755cb
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Mar 22 2023 Nicolas Chauvet <kwizart@gmail.com> - 2.4.1-12.20221130gitab755cb
- rebuilt

* Mon Mar 13 2023 Nicolas Chauvet <kwizart@gmail.com> - 2.4.1-11.20221130gitab755cb
- Update to 20221130

* Mon Mar 13 2023 Nicolas Chauvet <kwizart@gmail.com> - 2.4.1-10
- Add missing pciids

* Sun Aug 07 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 2.4.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild and ffmpeg
  5.1

* Wed Mar 30 2022 Nicolas Chauvet <kwizart@gmail.com> - 2.4.1-8
- Rebuilt

* Wed Feb 09 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 2.4.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Aug 03 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.4.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Mar 23 2021 Nicolas Chauvet <kwizart@gmail.com> - 2.4.1-5
- Add patch from !530

* Wed Feb 03 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.4.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Aug 18 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 30 2020 Nicolas Chauvet <kwizart@gmail.com> - 2.4.1-2
- Bump

* Mon Jun 08 2020 Nicolas Chauvet <kwizart@gmail.com> - 2.4.1-1
- Update to 2.4.1

* Tue Mar 10 2020 Nicolas Chauvet <kwizart@gmail.com> - 2.4.0-3
- Define _legacy_common_support

* Tue Feb 04 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Dec 06 2019 Nicolas Chauvet <kwizart@gmail.com> - 2.4.0-1
- Update to 2.4.0

* Mon Sep 23 2019 Nicolas Chauvet <kwizart@gmail.com> - 2.3.0-5
- Adapt for el8

* Fri Aug 09 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Mar 04 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Feb 13 2019 Nicolas Chauvet <kwizart@gmail.com> - 2.3.0-2
- Fix https://github.com/intel/intel-vaapi-driver/issues/419
  Backport a patch to fix compatibility with mesa 18.3 in F29
  Sent by Pete Walter <pwalter@fedoraproject.org>

* Sat Jan 26 2019 Nicolas Chauvet <kwizart@gmail.com> - 2.3.0-1
- Update to 2.3.0

* Thu Oct 11 2018 Nicolas Chauvet <kwizart@gmail.com> - 2.2.0-3
- Rebuilt for libva update

* Thu Jul 26 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jul 13 2018 Nicolas Chauvet <kwizart@gmail.com> - 2.2.0-1
- Update to 2.2.0

* Fri Mar 23 2018 Nicolas Chauvet <kwizart@gmail.com> - 2.1.0-2
- Add appstream support

* Mon Feb 12 2018 Nicolas Chauvet <kwizart@gmail.com> - 2.1.0-1
- Update to 2.1.0

* Mon Jan 15 2018 Nicolas Chauvet <kwizart@gmail.com> - 2.0.0-1
- Update to 2.0.0

* Tue Aug 22 2017 Nicolas Chauvet <kwizart@gmail.com> - 1.8.3-2
- Enable hybrid codec - rhbz#1475962

* Wed Jul 12 2017 Nicolas Chauvet <kwizart@gmail.com> - 1.8.3-1
- Update to 1.8.3

* Tue May 23 2017 Nicolas Chauvet <kwizart@gmail.com> - 1.8.2-1
- Update to 1.8.2

* Tue Apr 18 2017 Nicolas Chauvet <kwizart@gmail.com> - 1.8.1-1
- Update to 1.8.1

* Fri Apr 07 2017 Nicolas Chauvet <kwizart@gmail.com> - 1.8.0-1
- Update to 1.8.0
- Move to 01.org
- Add Virtual Provides as the project change it's name
- Drop Group

* Sun Mar 19 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 1.7.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 15 2017 Hans de Goede <j.w.r.degoede@gmail.com> - 1.7.3-2
- Fix libva not working when using with libglvnd + wayland (rhbz#1422151)

* Thu Nov 10 2016 Nicolas Chauvet <kwizart@gmail.com> - 1.7.3-1
- Update to 1.7.3

* Tue Sep 06 2016 Nicolas Chauvet <kwizart@gmail.com> - 1.7.2-1
- Update to 1.7.2

* Fri Jul 01 2016 Nicolas Chauvet <kwizart@gmail.com> - 1.7.1-1
- Update to 1.7.1

* Sun May 15 2016 Nicolas Chauvet <kwizart@gmail.com> - 1.7.0-1
- Update to 1.7.0

* Thu Dec 17 2015 Nicolas Chauvet <kwizart@gmail.com> - 1.6.2-1
- Update to 1.6.2

* Sat Oct 24 2015 Nicolas Chauvet <kwizart@gmail.com> - 1.6.1-1
- Update to 1.6.1

* Tue May 05 2015 Nicolas Chauvet <kwizart@gmail.com> - 1.5.1-1
- Update to 1.5.1

* Tue Oct 28 2014 Nicolas Chauvet <kwizart@gmail.com> - 1.4.1-1
- Update to 1.4.1

* Mon Sep 01 2014 Sérgio Basto <sergio@serjux.com> - 1.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Jun 02 2014 Nicolas Chauvet <kwizart@gmail.com> - 1.3.1-1
- Update to 1.3.1

* Sat Apr 12 2014 Nicolas Chauvet <kwizart@gmail.com> - 1.3.0-2
- Add missing wayland-scanner BR

* Sat Apr 12 2014 Nicolas Chauvet <kwizart@gmail.com> - 1.3.0-1
- Update to 1.3.0

* Tue Mar 04 2014 Nicolas Chauvet <kwizart@gmail.com> - 1.2.2-2
- Backport patch - rhbz#3193

* Mon Feb 17 2014 Nicolas Chauvet <kwizart@gmail.com> - 1.2.2-1
- Update to 1.2.2

* Tue Oct 01 2013 Nicolas Chauvet <kwizart@gmail.com> - 1.2.1-1
- Update to 1.2.1

* Wed Jun 26 2013 Nicolas Chauvet <kwizart@gmail.com> - 1.2.0-1
- Update to 1.2.0

* Wed Mar 20 2013 Nicolas Chauvet <kwizart@gmail.com> - 1.0.20-1
- Update to 1.0.20
- Spec file clean-up

* Fri Nov 09 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.0.19-1
- Update to 1.0.19

* Fri Aug 03 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.0.18-4
- Update to final 1.0.18

* Wed Jul 11 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.0.18-3
- Switch to pkgconfig(libudev)

* Mon Jun 04 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.0.18-1
- Update to 1.0.18

* Sat May 26 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.0.15-4
- Introduce --with gen4asm

* Tue Jan 03 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.0.15-3
- Add BR intel-gen4asm
- Move pre-built asm code
- Adjust license with EPL

* Mon Jan 02 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.0.15-2
- Spec cleanup

* Thu Nov 03 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.0.15-1
- Rename the package to libva-intel-driver

* Sun Aug 07 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.0.14-1
- Update to 1.0.14

* Sat Jun 11 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.0.13-2
- Fix typo when building --with full
- Requires at least the same libva version.

* Wed Jun 08 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.0.13-1
- Update to 1.0.13

* Sun Apr 10 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.0.12-1
- Update to 1.0.12

* Thu Mar 10 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.0.10-1
- Switch to additional package using the freedesktop version
- Add git rev from today as patch

* Mon Feb 21 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.0.10-1
- Update to 1.0.10

* Tue Jan 25 2011 Adam Williamson <awilliam@redhat.com> - 1.0.8-1
- bump to new version
- fix modded tarball to actually not have i965 dir
- merge with the other spec I seem to have lying around somewhere

* Wed Nov 24 2010 Adam Williamson <awilliam@redhat.com> - 1.0.6-1
- switch to upstream from sds branch (sds now isn't carrying any very
  interesting changes according to gwenole)
- pull in the dont-install-test-programs patch from sds
- split out libva-utils again for multilib purposes
- drop -devel package obsolete/provides itself too

* Tue Nov 23 2010 Adam Williamson <awilliam@redhat.com> - 0.31.1-3.sds4
- drop obsoletes and provides of itself (hangover from freeworld)

* Tue Nov 23 2010 Adam Williamson <awilliam@redhat.com> - 0.31.1-2.sds4
- fix the tarball to actually remove the i965 code (duh)

* Thu Oct 7 2010 Adam Williamson <awilliam@redhat.com> - 0.31.1-1.sds4
- initial package (based on package from elsewhere by myself and Nic
  Chauvet with i965 driver removed)
