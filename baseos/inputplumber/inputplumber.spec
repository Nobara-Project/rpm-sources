%global _name   inputplumber

Name:           inputplumber
Version:        0.55.0
Release:        1%{?dist}
Summary:        InputPlumber is an open source input routing and control daemon for Linux. It can be used to combine any number of input devices (like gamepads, mice, and keyboards) and translate their input to a variety of virtual device formats.

License:        GPLv3+
URL:            https://github.com/ShadowBlip/InputPlumber

BuildRequires:  libevdev-devel libiio-devel git make cargo libudev-devel llvm-devel clang-devel
Requires:       libevdev libiio
Recommends:     steam gamescope-session linuxconsoletools
Provides:       inputplumber
Requires:       opengamepadui
Conflicts:      hhd

%description
InputPlumber is an open source input routing and control daemon for Linux. It can be used to combine any number of input devices (like gamepads, mice, and keyboards) and translate their input to a variety of virtual device formats.

%prep
rm -rf %{_builddir}/InputPlumber
cd %{_builddir}
git clone %{url}
cd InputPlumber
git checkout v%{version}
cd ..


%build
cd %{_builddir}/InputPlumber
make build

%install
mkdir -p %{buildroot}/usr/bin
mkdir -p %{buildroot}/usr/share/dbus-1/system.d
mkdir -p %{buildroot}/usr/lib/systemd/system
mkdir -p %{buildroot}/usr/lib/udev/hwdb.d
mkdir -p %{buildroot}/usr/share/inputplumber/capability_maps
mkdir -p %{buildroot}/usr/share/inputplumber/devices
mkdir -p %{buildroot}/usr/share/inputplumber/profiles
mkdir -p %{buildroot}/usr/share/inputplumber/schema

install -D -m 755 %{_builddir}/InputPlumber/target/release/inputplumber %{buildroot}/usr/bin/inputplumber
install -D -m 644 %{_builddir}/InputPlumber/rootfs/usr/share/dbus-1/system.d/org.shadowblip.InputPlumber.conf %{buildroot}/usr/share/dbus-1/system.d/org.shadowblip.InputPlumber.conf
install -D -m 644 %{_builddir}/InputPlumber/rootfs/usr/lib/systemd/system/* %{buildroot}/usr/lib/systemd/system/
install -D -m 644 %{_builddir}/InputPlumber/rootfs/usr/lib/udev/hwdb.d/59-inputplumber.hwdb %{buildroot}/usr/lib/udev/hwdb.d/59-inputplumber.hwdb
install -D -m 644 %{_builddir}/InputPlumber/rootfs/usr/share/inputplumber/capability_maps/* %{buildroot}/usr/share/inputplumber/capability_maps/
install -D -m 644 %{_builddir}/InputPlumber/rootfs/usr/share/inputplumber/devices/* %{buildroot}/usr/share/inputplumber/devices/
install -D -m 644 %{_builddir}/InputPlumber/rootfs/usr/share/inputplumber/profiles/* %{buildroot}/usr/share/inputplumber/profiles/
install -D -m 644 %{_builddir}/InputPlumber/rootfs/usr/share/inputplumber/schema/* %{buildroot}/usr/share/inputplumber/schema/

# Re-assign devices with gyro as ds-edge devices instead of xb elite
sed -i 's/- xbox-elite/- ds5-edge/g' %{buildroot}/usr/share/inputplumber/devices/50-rog_ally.yaml
sed -i 's/- xbox-elite/- ds5-edge/g' %{buildroot}/usr/share/inputplumber/devices/50-rog_ally_x.yaml
sed -i 's/- xbox-elite/- ds5-edge/g' %{buildroot}/usr/share/inputplumber/devices/50-legion_go.yaml
sed -i 's/- xbox-elite/- ds5-edge/g' %{buildroot}/usr/share/inputplumber/devices/50-legion_go_s.yaml
sed -i 's/- xbox-elite/- ds5-edge/g' %{buildroot}/usr/share/inputplumber/devices/50-msi_claw7_a2vm.yaml
sed -i 's/- xbox-elite/- ds5-edge/g' %{buildroot}/usr/share/inputplumber/devices/50-msi_claw8_a2vm.yaml
sed -i 's/- xbox-elite/- ds5-edge/g' %{buildroot}/usr/share/inputplumber/devices/50-msi_claw_a1m.yaml

# Fixup for elite v2 not being detected
sed -i 's/02e3,0b00/02e3,0b00,0b22,0b05/g' %{buildroot}/usr/share/inputplumber/devices/60-xbox_one_elite_gamepad.yaml


%post
udevadm control --reload-rules
udevadm trigger
systemctl daemon-reload
systemctl enable inputplumber.service
systemctl start inputplumber.service

%preun
systemctl stop inputplumber.service
systemctl disable inputplumber.service
%systemd_preun inputplumber.service

%files
/usr/bin/inputplumber
/usr/share/dbus-1/system.d/*
/usr/lib/systemd/system/*
/usr/lib/udev/*
/usr/share/inputplumber/capability_maps/*
/usr/share/inputplumber/devices/*
/usr/share/inputplumber/profiles/*
/usr/share/inputplumber/schema/*

%changelog
* Tue Aug 6 2024 William Edwards [0.33.1-0]
- Initial spec file for Fedora based testing and distribution (please refer to https://github.com/ShadowBlip/InputPlumber)
