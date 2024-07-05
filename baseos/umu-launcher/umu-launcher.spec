%define commit 86b84b754c0623c9cf76a0387043c2250dc36330
%global shortcommit %(c=%{commit}; echo ${c:0:7})

%global build_timestamp %(date +"%Y%m%d")

%global rel_build RC4.%{build_timestamp}.%{shortcommit}%{?dist}

Name:           umu-launcher
Version:        0.1
Release:        %{rel_build}
Summary:        A tool for launching non-steam games with proton

License:        GPLv3
URL:            https://github.com/Open-Wine-Components/umu-launcher

BuildRequires:  meson >= 0.54.0
BuildRequires:  ninja-build
BuildRequires:  cmake
BuildRequires:  g++
BuildRequires:  gcc-c++
BuildRequires:  scdoc
BuildRequires:  git

Requires: python3-xlib

%description
%{name} A tool for launching non-steam games with proton

%prep
git clone --single-branch --branch main https://github.com/Open-Wine-Components/umu-launcher.git
cd umu-launcher
git checkout %{commit}
git submodule update --init --recursive

%build
cd umu-launcher
./configure.sh --prefix=/usr
make

%install
cd umu-launcher
make DESTDIR=%{buildroot} install

%files
%{_bindir}/umu-run
%{_datadir}/man/*
%{_datadir}/umu/*
%{_datadir}/steam/compatibilitytools.d/umu-launcher/

%changelog

