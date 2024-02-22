Name:     hardinfo
Version:  0.6
Release:  1%{?dist}
Summary:  Hardinfo mostra todas as informações de hardware
License:  GPLv2
URL:      https://github.com/lpereira/hardinfo
Source0:  https://github.com/lpereira/hardinfo/archive/refs/heads/master.tar.gz

BuildRequires: cmake
BuildRequires: gcc-c++
BuildRequires: gtk3-devel
BuildRequires: json-glib-devel
BuildRequires: libsoup-devel
BuildRequires: lm_sensors-devel
Requires: lm_sensors
Requires: glx-utils
Requires: hddtemp
Requires: sysbench
Requires: xrandr
Requires: dmidecode

%description
Software para mostrar informações sobre o hardware disponível no sistema.

%prep
%setup -q -n %{name}-master

%build
mkdir build
cd build
cmake -DHARDINFO_GTK3='ON' -DCMAKE_INSTALL_PREFIX=/usr ..
make 

%install
cd build
make install DESTDIR=%{buildroot}

%post
/usr/sbin/sensors-detect > /dev/null

%files
%{_bindir}/hardinfo
%{_libdir}/hardinfo/*
%{_datadir}/applications/hardinfo.desktop
%{_datadir}/%name
%{_datadir}/icons/hicolor/48x48/apps/hardinfo.png
%{_datadir}/locale/*
%{_datadir}/man/man1/hardinfo.1.gz

%changelog
* Sat Feb 25 2023 Fernando Debian <fernandodebian@fedoraproject.org> - 0.6-1
- The issue of requesting to open a module when starting the software and the
- problem of the benchmark session not being available have been fixed. 
- Thanks to the patch by CamberLoid, thank you for the patch, see more at the link:
- https://github.com/lpereira/hardinfo/issues/676.
