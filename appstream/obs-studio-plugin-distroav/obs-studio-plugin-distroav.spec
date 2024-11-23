Name:           obs-studio-plugin-distroav
Version:        6.0.0
Release:        1%{?dist}
Summary:        Network A/V in OBS Studio with NewTek's NDI technology

License:        GPLv2+
URL:            https://github.com/DistroAV/DistroAV
Source0:        %{url}/archive/%{version}/DistroAV-%{version}.tar.gz

# OBS 31+ Compat
# https://github.com/DistroAV/DistroAV/pull/1152
Patch0:         1152.patch

ExclusiveArch:  i686 x86_64 aarch64

BuildRequires:  cmake
BuildRequires:  make
BuildRequires:  gcc-c++
BuildRequires:  cmake(Qt6Core)
BuildRequires:  cmake(Qt6Widgets)
BuildRequires:  libcurl-devel
BuildRequires:  obs-studio-devel
Requires:       obs-studio
# A libndi.so.5 implementation is meant to be dlopen
Requires: libndi-sdk%{?isa}
Requires: ndi-sdk%{?isa}
Provides: obs-ndi
Obsoletes: obs-ndi

%description
* NDI Source : receive NDI video and audio in OBS
* NDI Output : transmit video and audio from OBS to NDI
* NDI Filter (a.k.a NDI Dedicated Output) : transmit a single source or
scene to NDI


%prep
%autosetup -n DistroAV-%{version} -p1

# Where to find the libndi.so.5 library
sed -i -e 's|/usr/lib|%{_libdir}|' src/plugin-main.cpp
sed -i -e 's|/usr/local/lib|/usr/local/%{_lib}|' src/plugin-main.cpp


%build
%cmake \
  -DENABLE_FRONTEND_API=on \
  -DENABLE_QT=on \
  -DLINUX_PORTABLE=off \
  --compile-no-warning-as-error

%cmake_build


%install
%cmake_install


%files
%license LICENSE
%doc README.md
%{_libdir}/obs-plugins/distroav.so
%{_datadir}/obs/obs-plugins/distroav


%changelog
* Sun Feb 04 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 4.13.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Nov 29 2023 Nicolas Chauvet <kwizart@gmail.com> - 4.13.0-1
- Update to 4.13.0

* Wed Nov 29 2023 Nicolas Chauvet <kwizart@gmail.com> - 4.11.1-4
- Add missing deps - rhbz#6800

* Wed Aug 16 2023 Nicolas Chauvet <kwizart@gmail.com> - 4.11.1-3
- Switch to qt6 - rfbz#6747

* Thu Aug 03 2023 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 4.11.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu May 04 2023 Nicolas Chauvet <kwizart@gmail.com> - 4.11.1-1
- Update to 4.11.1

* Mon Aug 08 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 4.9.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild and ffmpeg
  5.1

* Wed Feb 16 2022 Nicolas Chauvet <kwizart@gmail.com> - 4.9.1-5
- rebuilt

* Thu Feb 10 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 4.9.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Aug 04 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 4.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sun Mar 21 2021 Nicolas Chauvet <kwizart@gmail.com> - 4.9.1-2
- Don't enforce c++11

* Wed Feb 24 2021 Nicolas Chauvet <kwizart@gmail.com> - 4.9.1-1
- Initial spec file

