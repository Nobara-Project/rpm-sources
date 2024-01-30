%global _name   lgcd

Name:           lgcd
Version:        1.5.0
Release:        4%{?dist}
Summary:        Convert Lenovo Legion GO input to DualShock4 and allows mode switching with a long CC press

License:        GPL3
# This is a fork of rogue enemy modified for the lenovo legion go
URL:            https://github.com/corando98/ROGueENEMY
Source0:        0001-convert-from-rogue-enemy-to-lgcd.patch
Source1:        0001-reverse-legion-button-swap-logic-so-it-matches-whats.patch

BuildRequires:  cmake
BuildRequires:  libconfig-devel
BuildRequires:  git
BuildRequires:  gcc
BuildRequires:  python-devel
BuildRequires:  libevdev-devel
BuildRequires:  systemd-rpm-macros
Requires:       libevdev libconfig
Recommends:     steam gamescope-session
Provides:       lgcd
Conflicts:      rogue-enemy
Conflicts:      HandyGCCS
Conflicts:      hhd

%description
Convert Lenovo Legion GO input to DualShock4 and allows mode switching with a long CC press

# Disable debug packages
%define debug_package %{nil}

%prep
cd %{_builddir}

cat << EOF >> %{_builddir}/99-lgcd.preset
enable lgcd.service
EOF

git clone %{url} lgcd
cd lgcd
patch -Np1 < %{SOURCE0}
patch -Np1 < %{SOURCE1}
mkdir -p %{_builddir}/lgcd/build

%build
cd %{_builddir}/lgcd/build
rm -f %{_builddir}/lgcd/Makefile
cmake ..
make

%install
mkdir -p %{buildroot}%{_bindir}/
mkdir -p %{buildroot}%{_unitdir}/
mkdir -p %{buildroot}%{_udevrulesdir}/
mkdir -p %{buildroot}%{_sysconfdir}/lgcd/
mkdir -p %{buildroot}%{_presetdir}/
install -D -m 755 %{_builddir}/lgcd/build/lgcd %{buildroot}%{_bindir}/lgcd
install -m 644 %{_builddir}/99-lgcd.preset %{buildroot}%{_presetdir}/
install -m 644 %{_builddir}/lgcd/99-disable-sonypad.rules %{buildroot}%{_udevrulesdir}/
install -m 644 %{_builddir}/lgcd/99-lgcd.rules %{buildroot}%{_udevrulesdir}/
install -m 644 %{_builddir}/lgcd/lgcd.service %{buildroot}%{_unitdir}/
install -m 644 %{_builddir}/lgcd/config.cfg.default %{buildroot}%{_sysconfdir}/lgcd/config.cfg

%post
udevadm control --reload-rules
udevadm trigger
%systemd_post lgcd.service

%preun
%systemd_preun lgcd.service

%files
%{_unitdir}/lgcd.service
%{_bindir}/lgcd
%{_udevrulesdir}/*
%{_sysconfdir}/lgcd/config.cfg
%{_presetdir}/99-lgcd.preset

%changelog
* Mon Dec 4 2023 Denis Benato <dbenato.denis96@gmail.com> [1.5.0-1]
- Initial package
