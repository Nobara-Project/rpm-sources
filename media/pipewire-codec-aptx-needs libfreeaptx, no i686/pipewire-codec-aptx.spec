%global spaversion   0.2

Name:           pipewire-codec-aptx
Summary:        PipeWire Bluetooth aptX codec plugin
Version:        1.2.6
Release:        1%{?dist}
License:        MIT
URL:            https://pipewire.org/
Source0:        https://gitlab.freedesktop.org/pipewire/pipewire/-/archive/%{version}/pipewire-%{version}.tar.gz

BuildRequires:  meson >= 0.59.0
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(bluez)
BuildRequires:  sbc-devel
BuildRequires:  libfreeaptx-devel

Requires:       pipewire >= %{version}

%description
PipeWire media server Bluetooth aptX codec plugin.

%prep
%autosetup -p1 -n pipewire-%{version}

%build
%meson  --auto-features=disabled -D examples=disabled \
          -D bluez5=enabled -D bluez5-codec-aptx=enabled \
          -D session-managers=[]
%meson_build spa-codec-bluez5-aptx

%install
mkdir -p %{buildroot}%{_libdir}/spa-%{spaversion}/bluez5
install -pm 0755 %{_vpath_builddir}/spa/plugins/bluez5/libspa-codec-bluez5-aptx.so \
   %{buildroot}%{_libdir}/spa-%{spaversion}/bluez5/

%files
%license COPYING
%{_libdir}/spa-%{spaversion}/bluez5/libspa-codec-bluez5-aptx.so

%changelog
* Fri Oct 25 2024 Leigh Scott <leigh123linux@gmail.com> - 1.2.6-1
- Update to 1.2.6

* Sat Sep 28 2024 Leigh Scott <leigh123linux@gmail.com> - 1.2.5-1
- Update to 1.2.5

* Sat Sep 21 2024 Leigh Scott <leigh123linux@gmail.com> - 1.2.4-1
- Update to 1.2.4

* Thu Aug 22 2024 Leigh Scott <leigh123linux@gmail.com> - 1.2.3-1
- Update to 1.2.3

* Fri Aug 02 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jul 12 2024 Leigh Scott <leigh123linux@gmail.com> - 1.2.1-1
- Update to 1.2.1

* Thu Jun 27 2024 Leigh Scott <leigh123linux@gmail.com> - 1.2.0-1
- Update to 1.2.0

* Fri May 24 2024 Leigh Scott <leigh123linux@gmail.com> - 1.1.82-1
- Update to 1.1.82

* Sat May 18 2024 Leigh Scott <leigh123linux@gmail.com> - 1.1.81-1
- Update to 1.1.81

* Fri May 17 2024 Leigh Scott <leigh123linux@gmail.com> - 1.0.6-1
- Update to 1.0.6

* Mon Apr 15 2024 Leigh Scott <leigh123linux@gmail.com> - 1.0.5-1
- Update to 1.0.5

* Sun Mar 17 2024 Leigh Scott <leigh123linux@gmail.com> - 1.0.4-1
- Update to 1.0.4

* Fri Feb 02 2024 Leigh Scott <leigh123linux@gmail.com> - 1.0.3-1
- Update to 1.0.3

* Wed Jan 31 2024 Leigh Scott <leigh123linux@gmail.com> - 1.0.2-1
- Update to 1.0.2

* Thu Jan 11 2024 Leigh Scott <leigh123linux@gmail.com> - 1.0.1-1
- Update to 1.0.1

* Sun Nov 26 2023 Leigh Scott <leigh123linux@gmail.com> - 1.0.0-1
- Update to 1.0.0

* Thu Nov 16 2023 Leigh Scott <leigh123linux@gmail.com> - 0.3.85-1
- Update to 0.3.85

* Thu Nov 02 2023 Leigh Scott <leigh123linux@gmail.com> - 0.3.84-1
- Update to 0.3.84

* Mon Oct 23 2023 Nicolas Chauvet <kwizart@gmail.com> - 0.3.83-1
- Update to 0.3.83

* Fri Oct 13 2023 Nicolas Chauvet <kwizart@gmail.com> - 0.3.82-1
- Update to 0.3.82

* Fri Oct 06 2023 Nicolas Chauvet <nchauvet@linagora.com> - 0.3.81-1
- Update to 0.3.81

* Thu Sep 14 2023 Nicolas Chauvet <kwizart@gmail.com> - 0.3.80-1
- Update to 0.3.80

* Thu Aug 31 2023 Nicolas Chauvet <kwizart@gmail.com> - 0.3.79-1
- Update to 0.3.79

* Tue Aug 22 2023 Nicolas Chauvet <kwizart@gmail.com> - 0.3.78-1
- Update to 0.3.78

* Fri Aug 04 2023 Nicolas Chauvet <kwizart@gmail.com> - 0.3.77-1
- Update to 0.3.77

* Thu Aug 03 2023 Nicolas Chauvet <kwizart@gmail.com> - 0.3.76-2
- Relax version requirement

* Sat Jul 29 2023 Nicolas Chauvet <kwizart@gmail.com> - 0.3.76-1
- Update to 0.3.76

* Mon Jul 24 2023 Nicolas Chauvet <kwizart@gmail.com> - 0.3.75-1
- Update to 0.3.75

* Thu Jul 13 2023 Nicolas Chauvet <kwizart@gmail.com> - 0.3.74-1
- Update to 0.3.74

* Tue Jul 11 2023 Sérgio Basto <sergio@serjux.com> - 0.3.73-1
- Update pipewire-codec-aptx to 0.3.73

* Sun Jul 02 2023 Leigh Scott <leigh123linux@gmail.com> - 0.3.72-1
- Update to 0.3.72

* Tue May 23 2023 Leigh Scott <leigh123linux@gmail.com> - 0.3.71-1
- Update to 0.3.71

* Sun Apr 23 2023 Leigh Scott <leigh123linux@gmail.com> - 0.3.70-1
- Update to 0.3.70

* Thu Apr 13 2023 Nicolas Chauvet <kwizart@gmail.com> - 0.3.69-1
- Update to 0.3.69

* Sun Apr 09 2023 Leigh Scott <leigh123linux@gmail.com> - 0.3.68-1
- Bump Pipewire version

* Thu Mar 09 2023 Leigh Scott <leigh123linux@gmail.com> - 0.3.67-1
- Bump Pipewire version

* Sat Feb 11 2023 Leigh Scott <leigh123linux@gmail.com> - 0.3.65-1
- Bump Pipewire version

* Sat Dec 17 2022 Leigh Scott <leigh123linux@gmail.com> - 0.3.63-1
- Bump Pipewire version

* Sat Nov 12 2022 Leigh Scott <leigh123linux@gmail.com> - 0.3.60-1
- Bump Pipewire version

* Wed Oct 05 2022 Leigh Scott <leigh123linux@gmail.com> - 0.3.59-1
- Bump Pipewire version

* Sat Sep 17 2022 Leigh Scott <leigh123linux@gmail.com> - 0.3.58-1
- Bump Pipewire version

* Sun Aug 07 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 0.3.56-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild and ffmpeg
  5.1

* Thu Aug 04 2022 Leigh Scott <leigh123linux@gmail.com> - 0.3.56-1
- Bump Pipewire version

* Mon Jul 04 2022 Leigh Scott <leigh123linux@gmail.com> - 0.3.53-1
- Bump Pipewire version

* Tue Apr 05 2022 Leigh Scott <leigh123linux@gmail.com> - 0.3.49-1
- Bump Pipewire version

* Wed Feb 09 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 0.3.42-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Dec 28 2021 Gergely Gombos <gombosg@disroot.org> - 0.3.42-1
- Bump Pipewire version

* Tue Dec 28 2021 Gergely Gombos <gombosg@disroot.org> - 0.3.40-1
- Bump Pipewire version

* Wed Sep 22 2021 Gergely Gombos <gombosg@disroot.org> - 0.3.36-3
- Review fixes

* Tue Sep 21 2021 Gergely Gombos <gombosg@disroot.org> - 0.3.36-2
- Initial packaging

* Thu Sep 16 2021 Pauli Virtanen <pav@iki.fi> - 0.3.36-1
- Initial version (kudos!)
