%global sonamebase 0

Name:           libfreeaptx
Version:        %{sonamebase}.1.1
Release:        7%{?dist}
Summary:        Open Source implementation of Audio Processing Technology codec (aptX)

License:        LGPLv2+
URL:            https://github.com/iamthehorker/%{name}
Source0:        %{url}/archive/%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  make

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%package        tools
Summary:        %{name} encoder and decoder utilities
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description
This is Open Source implementation of Audio Processing Technology codec (aptX)
derived from ffmpeg 4.0 project and licensed under LGPLv2.1+. This codec is
mainly used in Bluetooth A2DP profile.

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%description    tools
The %{name}-tools package contains openaptxenc encoder and openaptxdec decoder
command-line utilities.

%prep
%autosetup

%build
# Skip building static binaries
# Environment variable CFLAGS are overridden in makefile so we override that
%make_build STATIC_UTILITIES= LDFLAGS="%{build_ldflags}" CFLAGS="%{optflags}"

%install
# Skip build in install phase
%make_install PREFIX= LIBDIR="%{_libdir}" INCDIR="%{_includedir}" BINDIR="%{_bindir}"

%files
%license COPYING
%{_libdir}/%{name}.so.%{sonamebase}
%{_libdir}/%{name}.so.%{version}

%files devel
%{_libdir}/%{name}.so
%{_includedir}/freeaptx.h
%{_libdir}/pkgconfig/%{name}.pc

%files tools
%{_bindir}/freeaptxenc
%{_bindir}/freeaptxdec

%changelog
* Fri Aug 02 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 0.1.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Feb 03 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 0.1.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Aug 02 2023 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 0.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sun Aug 07 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 0.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild and ffmpeg
  5.1

* Wed Feb 09 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 0.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Sep 22 2021 Gergely Gombos <gombosg@disroot.org> - 0.1.1-2
- Review fixes

* Tue Sep 21 2021 Gergely Gombos <gombosg@disroot.org> - 0.1.1-1
- Initial packaging
