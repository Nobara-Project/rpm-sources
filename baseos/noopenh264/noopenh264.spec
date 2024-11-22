## START: Set by rpmautospec
## (rpmautospec version 0.3.5)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 1;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

%global openh264_version 2.4.1
%global openh264_soversion 7

Name:           noopenh264
# 0.1.0 is the project version from meson.build.
# Additionally, we also include the openh264 version as part of the
# version tag. As "openh264" ends with a digit, _ is used as a separator
# between "openh264" and the openh264 version number.
Version:        0.1.0~openh264_%{openh264_version}
Release:        %autorelease
Summary:        Fake implementation of the OpenH264 library

License:        BSD-2-Clause and LGPL-2.1-or-later
URL:            https://gitlab.com/freedesktop-sdk/noopenh264
%global tag v%{openh264_version}
Source:         %{url}/-/archive/%{tag}/noopenh264-%{tag}.tar.bz2

# https://gitlab.com/freedesktop-sdk/noopenh264/-/merge_requests/6
Patch:          0001-Fix-the-build.patch

BuildRequires:  gcc-c++
BuildRequires:  meson

# Explicitly conflict with openh264 that ships the actual
# non-dummy version of the library.
Provides:      openh264

%description
Fake implementation of the OpenH264 library we can link from
regardless of the actual library being available.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
# Explicitly conflict with openh264-devel that ships the actual
# non-dummy version of the library.
Provides:      openh264-devel

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup -p1 -n noopenh264-%{tag}


%build
%meson
%meson_build


%install
%meson_install

# Remove static library
rm $RPM_BUILD_ROOT%{_libdir}/*.a


%files
%license COPYING*
%doc README
%{_libdir}/libopenh264.so.%{openh264_soversion}
%{_libdir}/libopenh264.so.%{openh264_version}

%files devel
%{_includedir}/wels/
%{_libdir}/libopenh264.so
%{_libdir}/pkgconfig/openh264.pc


%changelog
%autochangelog

