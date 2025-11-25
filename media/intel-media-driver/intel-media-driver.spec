#global pre .pre8

Name:       intel-media-driver
Version:    25.3.4
Release:    1%{?dist}
Summary:    The Intel Media Driver for VAAPI
License:    MIT and BSD
URL:        https://github.com/intel/media-driver
Source0:    %{url}/archive/intel-media-%{version}%{?pre}.tar.gz
Source1:    intel-media-driver.metainfo.xml

# This is an Intel only vaapi backend
ExclusiveArch:  i686 x86_64


BuildRequires:  cmake >= 3.5
BuildRequires:  gcc
BuildRequires:  gcc-c++

# AppStream metadata generation
BuildRequires:  libappstream-glib >= 0.6.3

BuildRequires:  pkgconfig(igdgmm) >= 11.2.0
# cmrt is archived as a separate project - now bundled
# https://github.com/intel/cmrt
#BuildRequires:  pkgconfig(libcmrt)
BuildRequires:  pkgconfig(libva) >= 1.6.0
BuildRequires:  pkgconfig(pciaccess)
BuildRequires:  pkgconfig(x11)

# There is a modified version of libdrm
Provides: bundled(libdrm)
Provides: bundled(libcmrt)

# Compatible instead of conflicting to accomodate fedora multimedia comps
Provides: libva-intel-media-driver = %{version}-%{release}

# See https://src.fedoraproject.org/rpms/libva/pull-request/5
%if 0%{?fedora} >= 40
Conflicts: libva%{__isa} < 1.20.0-5
%endif


%description
The Intel Media Driver for VAAPI is a new VA-API (Video Acceleration API)
user mode driver supporting hardware accelerated decoding, encoding,
and video post processing for GEN based graphics hardware.
https://01.org/intel-media-for-linux


%prep
%autosetup -p1 -n media-driver-intel-media-%{version}%{?pre}
# Fix license perm
chmod -x LICENSE.md README.md CMakeLists.txt

# Remove pre-built (but unused) files
rm -f Tools/MediaDriverTools/UMDPerfProfiler/MediaPerfParser

# Remove all -Werror compile flags
sed -e "/-Werror/d" -i media_driver/cmake/linux/media_compile_flags_linux.cmake
sed -e "/-Werror/d" -i media_driver/media_top_cmake.cmake


%build
%ifarch %{ix86}
export CXXFLAGS="%{optflags} -D_FILE_OFFSET_BITS=64"
%endif
%cmake \
%ifarch %{ix86}
  -DARCH:STRING=32 \
%endif
  -DBUILD_CMRTLIB:BOOL=False \
  -DMEDIA_RUN_TEST_SUITE:BOOL=False \
  -DRUN_TEST_SUITE:BOOL=False

%cmake_build


%install
%cmake_install

# Fix perm on library to be stripped
chmod +x %{buildroot}%{_libdir}/dri/iHD_drv_video.so

# install AppData and add modalias provides
mkdir -p %{buildroot}%{_metainfodir}
install -pm 0644 %{SOURCE1} %{buildroot}%{_metainfodir}

# TODO - have pci based hw detection
%if 0
fn=%{buildroot}%{_metainfodir}/intel-media-driver.metainfo.xml
%{SOURCE9} src/i965_pciids.h | xargs appstream-util add-provide ${fn} modalias
%endif

# Don't provide the headers - Used by anyone else ?
rm -rf %{buildroot}%{_includedir}/igfxcmrt
rm -rf %{buildroot}%{_libdir}/pkgconfig

# Alternate directory for f40+
# See https://src.fedoraproject.org/rpms/libva/pull-request/5
%if 0%{?fedora} >= 40
mv %{buildroot}%{_libdir}/dri{,-nonfree}
%endif


%files
%doc README.md
%license LICENSE.md
%{_libdir}/dri*/iHD_drv_video.so
%{_metainfodir}/intel-media-driver.metainfo.xml


%changelog
* Thu Sep 25 2025 Nicolas Chauvet <kwizart@gmail.com> - 25.3.4-1
- Update to 25.3.4

* Sun Jul 27 2025 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 25.2.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jul 16 2025 Nicolas Chauvet <kwizart@gmail.com> - 25.2.6-1
- Update to 25.2.6

* Sun Mar 23 2025 Nicolas Chauvet <kwizart@gmail.com> - 25.1.4-1
- Update to 25.1.4

* Fri Jan 31 2025 Nicolas Chauvet <kwizart@gmail.com> - 25.1.0-1
- Update to 25.1.0

* Wed Jan 29 2025 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 24.4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild
- Fix build with GCC 15 (Dominik Mierzejewski)

* Tue Dec 24 2024 Nicolas Chauvet <kwizart@gmail.com> - 24.4.4-1
- Update to 24.4.4

* Thu Oct 24 2024 Nicolas Chauvet <kwizart@gmail.com> - 24.3.4-1
- Update to 24.3.4

* Mon Aug 12 2024 Nicolas Chauvet <kwizart@gmail.com> - 24.2.5-1
- Update to 24.2.5

* Fri Aug 02 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 24.1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Mar 20 2024 Nicolas Chauvet <kwizart@gmail.com> - 24.1.5-1
- Update to 24.1.5

* Mon Mar 04 2024 Nicolas Chauvet <kwizart@gmail.com> - 24.1.3-3
- Avoid conflicts on fedora counterpart - rfbz#6861

* Mon Feb 19 2024 Sérgio Basto <sergio@serjux.com> - 24.1.3-2
- With build target multilibs

* Fri Feb 02 2024 Nicolas Chauvet <kwizart@gmail.com> - 24.1.3-1
- Update to 24.1.3

* Fri Feb 02 2024 Nicolas Chauvet <kwizart@gmail.com> - 24.1.2-1
- Update to 24.1.2

* Thu Feb 01 2024 Nicolas Chauvet <kwizart@gmail.com> - 23.4.3-2
- Drop Werror

* Tue Jan 02 2024 Nicolas Chauvet <kwizart@gmail.com> - 23.4.3-1
- Update to 23.4.3

* Fri Oct 20 2023 Nicolas Chauvet <kwizart@gmail.com> - 23.3.5-1
- Update to 23.3.5

* Fri Sep 29 2023 Nicolas Chauvet <nchauvet@linagora.com> - 23.3.4-1
- Update to 23.3.4

* Thu Aug 03 2023 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 23.2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Nicolas Chauvet <kwizart@gmail.com> - 23.2.4-1
- Update to 23.2.4

* Tue Apr 11 2023 Nicolas Chauvet <kwizart@gmail.com> - 23.1.6-1
- Update to 23.1.6

* Wed Mar 22 2023 Nicolas Chauvet <kwizart@gmail.com> - 23.1.4-1
- Update to 23.1.4

* Sun Mar 12 2023 Nicolas Chauvet <kwizart@gmail.com> - 23.1.3-1
- Update to 23.1.3 (pre-release)

* Fri Jan 27 2023 Nicolas Chauvet <kwizart@gmail.com> - 22.6.6-2
- rebuilt

* Fri Jan 13 2023 Michael Cronenworth <mike@cchtml.com> - 22.6.6-1
- Update to 22.6.6
- Include patch to fix Gen 8/9/10 encoding performance

* Thu Dec 29 2022 Nicolas Chauvet <kwizart@gmail.com> - 22.6.4-1
- Update to 22.6.4

* Sun Oct 16 2022 Nicolas Chauvet <kwizart@gmail.com> - 22.5.4-1
- Update to 22.5.4

* Mon Aug 08 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 22.4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild and ffmpeg
  5.1

* Sun Jul 03 2022 Nicolas Chauvet <kwizart@gmail.com> - 22.4.4-1
- Update to 22.4.4

* Fri Apr 01 2022 Nicolas Chauvet <kwizart@gmail.com> - 22.3.1-1
- Update to 22.3.1

* Fri Apr 01 2022 Nicolas Chauvet <kwizart@gmail.com> - 22.1.1-4
- rebuilt

* Mon Mar 28 2022 Leigh Scott <leigh123linux@gmail.com> - 22.1.1-3
- rebuilt

* Thu Feb 10 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 22.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jan 19 2022 Nicolas Chauvet <kwizart@gmail.com> - 22.1.1-1
- Update to 22.1.1

* Sun Dec 19 2021 Nicolas Chauvet <kwizart@gmail.com> - 21.4.3-1
- Update to 21.4.3

* Tue Oct 05 2021 Nicolas Chauvet <kwizart@gmail.com> - 21.3.4-2
- rebuilt

* Sun Oct 03 2021 Nicolas Chauvet <kwizart@gmail.com> - 21.3.4-1
- Update to 21.3.4

* Wed Aug 04 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 21.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jun 30 2021 Nicolas Chauvet <kwizart@gmail.com> - 21.2.3-1
- Update to 21.2.3

* Sat Apr 03 2021 Nicolas Chauvet <kwizart@gmail.com> - 21.1.3-1
- Update to 21.1.3

* Wed Mar 24 2021 Nicolas Chauvet <kwizart@gmail.com> - 20.4.5-3
- Bump spec

* Wed Mar 24 2021 Nicolas Chauvet <kwizart@gmail.com> - 20.4.5-2
- Backport patch

* Thu Feb 25 2021 Nicolas Chauvet <kwizart@gmail.com> - 20.4.5-1
- Update to 20.4.5

* Thu Feb 04 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 20.4.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Dec 31 2020 Nicolas Chauvet <kwizart@gmail.com> - 20.4.5-1
- Update to 20.4.5

* Thu Nov 05 2020 Nicolas Chauvet <kwizart@gmail.com> - 20.4.0-1
- Update to 20.4.0

* Wed Sep 30 2020 Nicolas Chauvet <kwizart@gmail.com> - 20.3.0-1
- Update to 20.3.0

* Tue Sep 29 2020 Nicolas Chauvet <kwizart@gmail.com> - 20.3-0.2.pre8
- Update to pre8

* Wed Sep 02 2020 Nicolas Chauvet <kwizart@gmail.com> - 20.3-0.1.pre3
- Update to 20.3.pre3

* Wed Aug 19 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 20.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Aug 03 2020 Nicolas Chauvet <kwizart@gmail.com> - 20.2.0-3
- Rebuilt

* Fri Jul 10 2020 Nicolas Chauvet <kwizart@gmail.com> - 20.2.0-2
- Rebuilt

* Fri Jul 10 2020 Nicolas Chauvet <kwizart@gmail.com> - 20.2.0-1
- Update to 20.2.0

* Fri Apr 10 2020 Nicolas Chauvet <kwizart@gmail.com> - 20.1.1-1
- Update to 20.1.1

* Mon Mar 09 2020 Nicolas Chauvet <kwizart@gmail.com> - 19.4.0-4
- Enable i686 build

* Wed Feb 05 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 19.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jan 09 2020 Nicolas Chauvet <kwizart@gmail.com> - 19.4.0-2
- Rebuilt for to gmmlib

* Fri Dec 20 2019 Vasiliy N. Glazov <vascom2@gmail.com> - 19.4.0-1
- Update to 19.4.0

* Wed Oct 30 2019 Vasiliy N. Glazov <vascom2@gmail.com> - 19.3.1-1
- Update to 19.3.1

* Wed Oct 09 2019 Vasiliy N. Glazov <vascom2@gmail.com> - 19.3.0-1
- Update to 19.3.0

* Fri Sep 20 2019 Vasiliy N. Glazov <vascom2@gmail.com> - 19.2.1-3
- Rebuild for new intel-gmmlib

* Sat Aug 10 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 19.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Aug 01 2019 Nicolas Chauvet <kwizart@gmail.com> - 19.2.1-1
- Update to 19.2.1

* Fri Jul 05 2019 Nicolas Chauvet <kwizart@gmail.com> - 19.2-1
- Update to Final 19.2

* Fri May 10 2019 Nicolas Chauvet <kwizart@gmail.com> - 19.1-2
- Update to Final 19.1

* Sat Apr 06 2019 Nicolas Chauvet <kwizart@gmail.com> - 19.1-1
- Update to 19.1 pre3

* Tue Mar 05 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 18.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Feb 20 2019 Nicolas Chauvet <kwizart@gmail.com> - 18.4.1-2
- Unbundle cmrt

* Thu Feb 14 2019 Nicolas Chauvet <kwizart@gmail.com> - 18.4.1-1
- Update to 18.4.1

* Wed Oct 10 2018 Nicolas Chauvet <kwizart@gmail.com> - 18.3.0-2
- Use metainfodir
- Enable AppStream support (no hardware detection yet)
- Add missing BR
- Remove pre-built tools

* Mon Oct 08 2018 Nicolas Chauvet <kwizart@gmail.com> - 18.3.0-1
- Initial spec file
