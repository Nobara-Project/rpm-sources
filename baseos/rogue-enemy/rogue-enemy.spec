%global _name   rogue-enemy

Name:           rogue-enemy
Version:        1.5.0
Release:        3%{?dist}
Summary:        Convert ROG Ally input to DualShock4 and allows mode switching with a long CC press

License:        GPL3
URL:            https://github.com/NeroReflex/ROGueENEMY

BuildRequires:  cmake
BuildRequires:  libconfig-devel
BuildRequires:  git
BuildRequires:  gcc
BuildRequires:  python-devel
BuildRequires:  libevdev-devel
BuildRequires:  libudev-devel
BuildRequires:  systemd-rpm-macros
BuildRequires:	zlib-devel
Requires:       libevdev libconfig
Recommends:     steam gamescope-session
Provides:       rogue-enemy
Conflicts:      lgcd
Conflicts:      HandyGCCS
Conflicts:      hhd

%description
Convert ROG Ally input to DualShock4 and allows mode switching with a long CC press

# Disable debug packages
%define debug_package %{nil}

%prep
cd %{_builddir}

cat << EOF >> %{_builddir}/99-rogue-enemy.preset
enable rogue-enemy.service
EOF

cat << EOF >> %{_builddir}/rogue-enemy.service
[Unit]
Description=ROGueENEMY Daemon service

[Service]
Type=simple
Nice = -15
Restart=always
RestartSec=5
WorkingDirectory=/usr/bin
ExecStart=/usr/bin/rogue-enemy

[Install]
WantedBy=multi-user.target
EOF

git clone %{url} rogue-enemy
cd rogue-enemy
mkdir -p %{_builddir}/rogue-enemy/build

%build
cd %{_builddir}/rogue-enemy/build
rm -f %{_builddir}/rogue-enemy/Makefile
cmake ..
make

%install
mkdir -p %{buildroot}%{_bindir}/
mkdir -p %{buildroot}%{_unitdir}/
mkdir -p %{buildroot}%{_udevrulesdir}/
mkdir -p %{buildroot}%{_sysconfdir}/rogue-enemy/
mkdir -p %{buildroot}%{_presetdir}/
install -D -m 755 %{_builddir}/rogue-enemy/build/rogue-enemy %{buildroot}%{_bindir}/rogue-enemy
install -m 644 %{_builddir}/99-rogue-enemy.preset %{buildroot}%{_presetdir}/
install -m 644 %{_builddir}/rogue-enemy/80-playstation.rules %{buildroot}%{_udevrulesdir}/
install -m 644 %{_builddir}/rogue-enemy/rogue_enemy.rule %{buildroot}%{_udevrulesdir}/99-rogue-enemy.rules
install -m 644 %{_builddir}/rogue-enemy.service %{buildroot}%{_unitdir}/
install -m 644 %{_builddir}/rogue-enemy/config.cfg.default %{buildroot}%{_sysconfdir}/rogue-enemy/config.cfg

%post
udevadm control --reload-rules
udevadm trigger
%systemd_post rogue-enemy.service

%preun
%systemd_preun rogue-enemy.service

%files
%{_unitdir}/rogue-enemy.service
%{_bindir}/rogue-enemy
%{_udevrulesdir}/*
%{_sysconfdir}/rogue-enemy/config.cfg
%{_presetdir}/99-rogue-enemy.preset

%changelog
* Mon Dec 4 2023 Denis Benato <dbenato.denis96@gmail.com> [1.5.0-1]
- Initial package
