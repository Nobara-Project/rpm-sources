%global debug_package %{nil}
%global __strip /bin/true

Name:           ndi-sdk
Version:        5.6.0
Release:        3%{?dist}
Summary:        NewTek NDI SDK

License:        Proprietary
URL:            https://ndi.tv/sdk
Source0:        https://downloads.ndi.tv/SDK/NDI_SDK_Linux/Install_NDI_SDK_v5_Linux.tar.gz
Source1:        ndi.pc.in

ExclusiveArch: i686 x86_64 armv7hl aarch64

Requires:       libndi-sdk%{?_isa} = %{version}-%{release}


%description
NewTek NDI SDK.

%package -n libndi-sdk
Summary:        Libraries files for %{name}


%description -n libndi-sdk
The libndi-sdk package contains libraries for %{name}.


%package devel
Summary:        Libraries/include files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}


%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package documentation
Summary:        Documentation for %{name}

%description documentation
The %{name}-documentation documentations for %{name}.



%prep
%autosetup -c

# Uncompress installer
ARCHIVE=$(awk '/^__NDI_ARCHIVE_BEGIN__/ { print NR+1; exit 0; }' Install_NDI_SDK_v5_Linux.sh)
tail -n+$ARCHIVE Install_NDI_SDK_v5_Linux.sh | tar -xz
mv 'NDI SDK for Linux'/* .


%build
# Nothing to build


%install
_arch=$(uname -m)

case ${_arch} in
  aarch64)
    _ndi_arch="aarch64-rpi4-linux-gnueabi"
    ;;
  armv7l)
    _ndi_arch="arm-rpi3-linux-gnueabihf"
    ;;
  i386)
    _ndi_arch=i686-linux-gnu
    ;;
  i686|x86_64)
    _ndi_arch=${_arch}-linux-gnu
    ;;
  *)
    echo "Architecture not included"
    exit 2
    ;;
esac

# Install lib/bin as appropriate
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_libdir}
install -pm 0755 bin/${_ndi_arch}/ndi* %{buildroot}%{_bindir}
install -pm 0755 lib/${_ndi_arch}/libndi.so* %{buildroot}%{_libdir}
ldconfig -n %{buildroot}%{_libdir}

# Install headers
mkdir -p %{buildroot}%{_includedir}/%{name}
install -pm 0644 include/*.h %{buildroot}%{_includedir}/%{name}

# Install pc file
mkdir -p %{buildroot}%{_libdir}/pkgconfig
install -pm 0644 %{SOURCE1} %{buildroot}%{_libdir}/pkgconfig/ndi.pc
sed -i -e 's|@LIBDIR@|%{_libdir}|' \
  -e 's|@PREFIX@|%{_prefix}|' \
  -e 's|@VERSION@|%{version}|' \
  %{buildroot}%{_libdir}/pkgconfig/ndi.pc



%files
%{_bindir}/ndi-*

%files -n libndi-sdk
%license "NDI SDK License Agreement.pdf"  "NDI SDK License Agreement.txt" Version.txt licenses/libndi_licenses.txt
%{_libdir}/libndi.so.5*

%files devel
%doc examples
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/*.h
%{_libdir}/pkgconfig/ndi.pc

%files documentation
%doc documentation


%changelog
* Sat Aug 03 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 5.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Feb 04 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 5.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Nov 29 2023 Nicolas Chauvet <kwizart@gmail.com> - 5.6.0-1
- Update to 5.6.0
- Add aarch64 support

* Thu Aug 03 2023 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 5.5.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu May 04 2023 Nicolas Chauvet <kwizart@gmail.com> - 5.5.4-1
- Update to 5.5.4

* Mon Aug 08 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 4.6.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild and ffmpeg
  5.1

* Thu Feb 10 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 4.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Aug 04 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 4.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Feb 24 2021 Nicolas Chauvet <kwizart@gmail.com> - 4.6.1-1
- Initial spec file
