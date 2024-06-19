Name:           obs-studio-plugin-pipewire-audio-capture
Version:        1.1.4
Release:        1%{?dist}
Summary:        Audio device and application capture for OBS Studio using PipeWire

License:        GPL-2.0-or-later
URL:            https://github.com/dimtpap/obs-pipewire-audio-capture
Source0:        https://github.com/dimtpap/obs-pipewire-audio-capture/archive/refs/tags/%{version}.tar.gz
Patch0:         cmake-lib-dir-fixup.patch

BuildRequires:  cmake
BuildRequires:  gcc-c++

BuildRequires:  cmake(libobs)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pipewire-devel

Supplements:    obs-studio%{?_isa}

%description
%{name}.

%prep
%autosetup -n obs-pipewire-audio-capture-%{version} -p1


%build
%cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_FULL_LIBDIR=%{_libdir}
%cmake_build


%install
%cmake_install

%files
%license LICENSE
%{_libdir}/obs-plugins/linux-pipewire-audio*
%{_datadir}/obs/obs-plugins/linux-pipewire-audio*

%changelog
* Wed Jun 05 2024 Tom Crider <gloriouseggroll@gmail.com>
- Initial build 1.1.13
