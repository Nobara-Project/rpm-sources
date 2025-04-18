Name:           svt-hevc
Version:        1.5.1
Release:        8%{?dist}
Summary:        Scalable Video Technology for HEVC Encoder

License:        BSD-2-Clause-Patent
URL:            https://github.com/OpenVisualCloud/SVT-HEVC
Source0:        %url/archive/v%{version}/SVT-HEVC-%{version}.tar.gz
# Correct build flags
Patch0:         cmake.patch

BuildRequires:  gcc
BuildRequires:  cmake
BuildRequires:  yasm
BuildRequires:  meson

Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

ExclusiveArch:  x86_64

%description
The Scalable Video Technology for HEVC Encoder (SVT-HEVC Encoder) is an
HEVC-compliant encoder library core that achieves excellent density-quality
tradeoffs, and is highly optimized for Intel® Xeon™ Scalable Processor and
Xeon™ D processors.

%package        libs
Summary:        Libraries for svt-hevc

%description    libs
Libraries for development svt-hevc.

%package        devel
Summary:        Include files and mandatory libraries for development svt-hevc
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description    devel
Include files and mandatory libraries for development svt-hevc.

%prep
%autosetup -p1 -n SVT-HEVC-%{version}


%build
%cmake -G Ninja

%cmake_build


%install
%cmake_install

%files
%{_bindir}/SvtHevcEncApp

%files libs
%license LICENSE.md
%doc README.md Docs/svt-hevc_encoder_user_guide.md
%{_libdir}/libSvtHevcEnc.so.1*

%files devel
%{_includedir}/%{name}
%{_libdir}/libSvtHevcEnc.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Tue Jan 28 2025 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.5.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Aug 02 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.5.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Feb 04 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.5.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Aug 02 2023 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.5.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Aug 08 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.5.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild and ffmpeg
  5.1

* Wed Feb 09 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Aug 03 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue May 18 2021 Vasiliy Glazov <vascom2@gmail.com> - 1.5.1-1
- Update to 1.5.1

* Sun Feb 07 2021 Vasiliy Glazov <vascom2@gmail.com> - 1.5.0-4
- Fix build for GCC 11
- Remove gstreamer plugin

* Thu Feb 04 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Aug 18 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Aug 04 2020 Vasiliy Glazov <vascom2@gmail.com> - 1.5.0-1
- Update to 1.5.0

* Wed Feb 05 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.4.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Dec 30 2019 Vasiliy Glazov <vascom2@gmail.com> - 1.4.3-1
- Update to 1.4.3

* Tue Sep 17 2019 Vasiliy Glazov <vascom2@gmail.com> - 1.4.1-2
- Correct build gstreamer plugin

* Tue Sep 17 2019 Vasiliy Glazov <vascom2@gmail.com> - 1.4.1-1
- Initial release
