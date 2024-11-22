Name: opentabletdriver
Version: 0.6.4.0
Release: 1%{?dist}
Summary: A cross-platform open-source tablet driver

# This needs to be cloned from git recursively due to submodules
Source0: opentabletdriver-%{version}.tar.gz

License: LGPLv3
URL: https://opentabletdriver.net

BuildRequires: dotnet-sdk-8.0
Requires: dotnet-runtime-8.0
BuildRequires: git
BuildRequires: jq
Requires: gtk3
Requires: udev
Requires(post): grep
Suggests: libX11
Suggests: libXrandr

# libevdev is libevdev2 on SUSE, and libevdev on RHEL/Fedora...
Requires: libevdev.so.2()(64bit)

%description
OpenTabletDriver has the highest number of supported tablets with great
compatibility across multiple platforms, packaged in an easy-to-use graphical
user interface.

OpenTabletDriver has support for multiple tablets from the following (non-exhaustive) OEMs:
 * Wacom
 * Huion
 * XP-Pen
 * XenceLabs
 * Gaomon
 * Veikk

%global __requires_exclude_from ^/usr/lib/opentabletdriver/.*$

# No debug symbols
%global debug_package %{nil}

# No stripping
%global __os_install_post %{nil}

%prep
%autosetup -n OpenTabletDriver-%{version}

%build
./eng/linux/package.sh --output bin

%install
export DONT_STRIP=1
PREFIX="%{_prefix}" ./eng/linux/package.sh --package Generic --build false
mkdir -p "%{buildroot}"
mv ./dist/files/* "%{buildroot}"/
rm -rf ./dist
mkdir -p "%{buildroot}/%{_prefix}/lib/"
cp -r bin "%{buildroot}/%{_prefix}/lib/opentabletdriver"

%post -f eng/linux/Generic/postinst

%postun -f eng/linux/Generic/postrm

%files
%defattr(-,root,root)
%dir %{_prefix}/lib/opentabletdriver
%dir %{_prefix}/share/doc/opentabletdriver
%{_bindir}/otd
%{_bindir}/otd-daemon
%{_bindir}/otd-gui
%{_prefix}/lib/modprobe.d/99-opentabletdriver.conf
%{_prefix}/lib/modules-load.d/opentabletdriver.conf
%{_prefix}/lib/opentabletdriver/*
%{_prefix}/lib/systemd/user/opentabletdriver.service
%{_prefix}/lib/udev/rules.d/70-opentabletdriver.rules
%{_prefix}/share/applications/opentabletdriver.desktop
%{_prefix}/share/man/man8/opentabletdriver.8.gz
%{_prefix}/share/doc/opentabletdriver/LICENSE
%{_prefix}/share/pixmaps/otd.ico
%{_prefix}/share/pixmaps/otd.png

%changelog
