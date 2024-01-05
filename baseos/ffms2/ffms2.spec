Name:           ffms2
Version:        2.40
Release:        10%{?dist}
License:        MIT
Summary:        Wrapper library around libffmpeg
URL:            https://github.com/FFMS/ffms2
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz
Patch0:         %{url}/commit/96cbf38ea9381829a1314f432a2c60495dcefaad.patch
Patch1:         %{url}/commit/586d87de3f896d0c4ff01b21f572375e11f9c3f1.patch
Patch2:         %{url}/commit/45673149e9a2f5586855ad472e3059084eaa36b1.patch

BuildRequires:  gcc
BuildRequires:  gcc-c++
%{?el7:BuildRequires: epel-rpm-macros}
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  pkgconfig(libavformat)
BuildRequires:  pkgconfig(libavcodec)
BuildRequires:  pkgconfig(libswscale)
BuildRequires:  pkgconfig(libavutil)
BuildRequires:  zlib-devel
BuildRequires:  ffmpeg-free
BuildRequires:  ffmpeg-free-devel

Provides: bundled(vapoursynth) = 35

%description
FFmpegSource (usually known as FFMS or FFMS2) is a cross-platform wrapper
library around libffmpeg, plus some additional components to deal with file
formats libavformat has (or used to have) problems with.

%package devel
Summary:        Development package for %{name}
Requires:       %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description devel
FFmpegSource (usually known as FFMS or FFMS2) is a cross-platform wrapper
library around libffmpeg, plus some additional components to deal with file
formats libavformat has (or used to have) problems with.

%prep
%setup -q
%if 0%{?fedora} >= 36
%patch0 -p1 -b ffmpeg45-0
%patch1 -p1 -b ffmpeg45-1
%patch2 -p1 -b ffmpeg45-2
%endif
sed -i 's/\r$//' COPYING
mkdir -p src/config
autoreconf -vfi

%build
%configure --disable-static --disable-silent-rules
%make_build

%install
%make_install
rm %{buildroot}%{_libdir}/lib%{name}.la
rm -rf %{buildroot}%{_docdir}

%ldconfig_scriptlets

%files
%license COPYING
%doc README.md
%{_bindir}/ffmsindex
%{_libdir}/lib%{name}.so.4*

%files devel
%doc doc/*
%{_libdir}/lib%{name}.so
%{_includedir}/ffms*
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Wed Aug 02 2023 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 2.40-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Mar 01 2023 Leigh Scott <leigh123linux@gmail.com> - 2.40-9
- Rebuild for new ffmpeg

* Sun Aug 07 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 2.40-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild and ffmpeg
  5.1

* Wed Feb 09 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 2.40-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Nov 11 2021 Leigh Scott <leigh123linux@gmail.com> - 2.40-6
- Rebuilt for new ffmpeg snapshot

* Mon Aug 02 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.40-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sat Apr 24 2021 Leigh Scott <leigh123linux@gmail.com> - 2.40-4
- Rebuilt for removed libstdc++ symbol (#1937698)

* Wed Feb 03 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.40-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Dec 31 2020 Leigh Scott <leigh123linux@gmail.com> - 2.40-2
- Rebuilt for new ffmpeg snapshot

* Sun Nov  1 2020 Leigh Scott <leigh123linux@gmail.com> - 2.40-1
- Update to 2.40

* Mon Aug 17 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.23-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu May 28 2020 Leigh Scott <leigh123linux@gmail.com> - 2.23-16
- Remove libavresample dependency (rfbz#5349)

* Sat Feb 22 2020 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 2.23-15
- Rebuild for ffmpeg-4.3 git

* Tue Feb 04 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.23-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Aug 07 2019 Leigh Scott <leigh123linux@gmail.com> - 2.23-13
- Rebuild for new ffmpeg version

* Mon Mar 04 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.23-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Nov 13 2018 Antonio Trande <sagitter@fedoraproject.org> - 2.23-11
- Rebuild for ffmpeg-3.4.5 on el7
- Use ldconfig_scriptlets macros

* Thu Jul 26 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 2.23-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Mar 08 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 2.23-9
- Rebuilt for new ffmpeg snapshot

* Thu Mar 01 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 2.23-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 18 2018 Leigh Scott <leigh123linux@googlemail.com> - 2.23-7
- Rebuilt for ffmpeg-3.5 git

* Thu Jan 18 2018 Leigh Scott <leigh123linux@googlemail.com> - 2.23-6
- Rebuilt for ffmpeg-3.5 git

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 2.23-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 2.23-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Apr 29 2017 Leigh Scott <leigh123linux@googlemail.com> - 2.23-3
- Rebuild for ffmpeg update

* Sun Mar 19 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 2.23-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 05 2017 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.23-1
- Update to 2.23

* Tue Aug 30 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.22-3
- Couple of trivial fixes

* Tue Jun 14 2016 Arkady L. Shane <ashejn@russianfedora.pro> - 2.2-2
- rebuilt against new ffmpeg

* Wed Nov 04 2015 Vasiliy N. Glazov <vascom2@gmail.com> 2.22-1
- Update to 2.22

* Sun Jun 28 2015 Ivan Epifanov <isage.dna@gmail.com> - 2.21-1
- Update to 2.21

* Mon Jan  5 2015 Ivan Epifanov <isage.dna@gmail.com> - 2.20-1
- Update to 2.20

* Fri Mar 28 2014 Ivan Epifanov <isage.dna@gmail.com> - 2.19-1
- Initial spec for Fedora
