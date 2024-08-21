%global commit0 649c079a461cbb08604ecb2d4acc04ce07283692
%global date 20240412
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
#global tag %{version}

Name:           egl-gbm
Epoch:          2
Version:        1.1.1
Release:        6%{!?tag:.%{date}git%{shortcommit0}}%{?dist}
Summary:        Nvidia egl gbm libary
License:        MIT
URL:            https://github.com/NVIDIA/%{name}

%if 0%{?tag:1}
Source0:        %url/archive/%{version}/%{name}-%{version}.tar.gz
%else
Source0:        %url/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz
%endif

BuildRequires:  gcc
BuildRequires:  meson
BuildRequires:  eglexternalplatform-devel
BuildRequires:  libdrm-devel
BuildRequires:  libglvnd-devel
BuildRequires:  mesa-libgbm-devel

%description
The GBM EGL external platform library.

%prep
%if 0%{?tag:1}
%autosetup -p1
%else
%autosetup -p1 -n %{name}-%{commit0}
%endif

%build
%meson
%meson_build

%install
%meson_install
# Delete unversioned .so
rm %{buildroot}%{_libdir}/libnvidia-egl-gbm.so

%files
%license COPYING
%{_libdir}/libnvidia-egl-gbm.so.1*

%changelog
* Wed Aug 07 2024 Simone Caronni <negativo17@gmail.com> - 2:1.1.1-6.20240412git649c079
- Update to latest snapshot with required commits for driver 560+.

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2:1.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Feb 28 2024 Leigh Scott <leigh123linux@gmail.com> - 2:1.1.1-4
- Add an epoch as some fool addded an epoch to their thirdparty repo!

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jan 03 2024 Leigh Scott <leigh123linux@gmail.com> - 1.1.1-1
- Update to 1.1.1

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Dec 22 2021 Leigh Scott <leigh123linux@gmail.com> - 1.1.0-1
- Initial build
