%global commit0 abf17cc1e7aadd9f3e4972774a3aba2812c51b75
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global gver .git%{shortcommit0}

%define debug_package %{nil}
%global _build_id_links none


Name: libajantv2
Summary: AJA NTV2 SDK
Version: 16.1
Release: 1%{?dist}
URL: https://github.com/aja-video/ntv2
Group: System Environment/Libraries
Source0:  https://github.com/aja-video/ntv2/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz
License: MIT
BuildRequires: cmake
BuildRequires: gcc-c++
%if 0%{?fedora} >= 36
BuildRequires:	annobin-plugin-gcc
%endif

%description
AJA NTV2 Open Source Static Libs and Headers for building applications that only
wish to statically link against.

%prep
%autosetup -n ntv2-%{commit0}

sed -i 's/Clang|GNU/GNU/g' cmake/CommonFlags.cmake
sed -i 's/Linux|Darwin/Linux/g' cmake/CommonFlags.cmake

%build

mkdir -p build
%cmake -B build -DAJA_BUILD_OPENSOURCE=ON
%make_build -C build
   
   
%install
%make_install -C build

%files
%license LICENSE
%doc README.md
%{_libdir}/libajantv2.a
%{_includedir}/ajalibraries/

%changelog

* Fri Dec 31 2021 Unitedrpms Project <unitedrpms AT protonmail DOT com> 16.1-1
- Initial build
