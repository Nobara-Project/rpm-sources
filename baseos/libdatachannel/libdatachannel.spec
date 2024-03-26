%define soversion() %(echo "%1" | awk -F. '{print $1"."$2}')

Name:           libdatachannel
Version:        0.20.1
Release:        1%{?dist}
Summary:        WebRTC network library featuring Data Channels, Media Transport, and WebSockets

License:        MPL-2.0
URL:            https://libdatachannel.org/
Source0:        https://github.com/paullouisageneau/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gawk
BuildRequires:  gcc-c++
BuildRequires:  make
# Not yet needed and not packaged in Fedora yet
#BuildRequires:  cmake(LibJuice)
BuildRequires:  cmake(nlohmann_json)
BuildRequires:  cmake(plog)
BuildRequires:  pkgconfig(gio-unix-2.0)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(nice)
BuildRequires:  libsrtp-devel
BuildRequires:  usrsctp-devel

%description
libdatachannel is a standalone implementation of WebRTC Data Channels,
WebRTC Media Transport, and WebSockets in C++17 with C bindings for POSIX platforms
(including GNU/Linux, Android, FreeBSD, Apple macOS and iOS) and Microsoft Windows.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup


%build
%cmake -DPREFER_SYSTEM_LIB=ON -DUSE_GNUTLS=ON -DUSE_NICE=ON
%cmake_build


%install
%cmake_install


%files
%license LICENSE
%{_libdir}/%{name}.so.%{soversion %{version}}{,.*}

%files devel
%doc README.md DOC.md
%{_includedir}/rtc/
%{_libdir}/cmake/LibDataChannel/
%{_libdir}/%{name}.so


%changelog
* Mon Nov 13 2023 Neal Gompa <ngompa@fedoraproject.org> - 0.19.3-1
- Update to 0.19.3

* Fri Sep 15 2023 Neal Gompa <ngompa@fedoraproject.org> - 0.19.1-2
- Add patch to fix library soversion

* Sun Sep 10 2023 Neal Gompa <ngompa@fedoraproject.org> - 0.19.1-1
- Initial package
