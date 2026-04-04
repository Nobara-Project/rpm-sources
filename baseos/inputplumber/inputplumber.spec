%global _name   inputplumber

Name:           inputplumber
Version:        0.75.2
Release:        1%{?dist}
Summary:        InputPlumber is an open source input routing and control daemon for Linux. It can be used to combine any number of input devices (like gamepads, mice, and keyboards) and translate their input to a variety of virtual device formats.

License:        GPLv3+
URL:            https://github.com/ShadowBlip/InputPlumber
Patch0:         icon_workaround.patch
ExcludeArch:    %{ix86}

BuildRequires:  libevdev-devel libiio-devel git make cargo libudev-devel llvm-devel clang-devel
Requires:       libevdev libiio
Recommends:     steam linuxconsoletools
Provides:       inputplumber
%ifarch x86_64
Requires:       opengamepadui
%endif
Conflicts:      hhd

%description
InputPlumber is an open source input routing and control daemon for Linux. It can be used to combine any number of input devices (like gamepads, mice, and keyboards) and translate their input to a variety of virtual device formats.

%prep
rm -rf %{_builddir}/InputPlumber
cd %{_builddir}
git clone --branch v%{version} --depth 1 %{url}

%build
cd %{_builddir}/InputPlumber
patch -Np1 < %{PATCH0}
make build

%install
mkdir -p %{buildroot}/usr/bin
mkdir -p %{buildroot}/usr/share/dbus-1/system.d
mkdir -p %{buildroot}/usr/share/dbus-1/system-services
mkdir -p %{buildroot}/usr/lib/systemd/system
mkdir -p %{buildroot}/usr/lib/udev/hwdb.d
mkdir -p %{buildroot}/usr/lib/udev/rules.d
mkdir -p %{buildroot}/usr/share/inputplumber/capability_maps
mkdir -p %{buildroot}/usr/share/inputplumber/devices
mkdir -p %{buildroot}/usr/share/inputplumber/profiles
mkdir -p %{buildroot}/usr/share/inputplumber/schema
mkdir -p %{buildroot}/usr/share/polkit-1/actions
mkdir -p %{buildroot}/usr/share/polkit-1/rules.d

install -D -m 755 %{_builddir}/InputPlumber/target/%{_arch}-unknown-linux-gnu/release/inputplumber %{buildroot}/usr/bin/inputplumber
install -D -m 644 %{_builddir}/InputPlumber/rootfs/usr/share/dbus-1/system.d/org.shadowblip.InputPlumber.conf %{buildroot}/usr/share/dbus-1/system.d/org.shadowblip.InputPlumber.conf
install -D -m 644 %{_builddir}/InputPlumber/rootfs/usr/share/dbus-1/system-services/* %{buildroot}/usr/share/dbus-1/system-services/
install -D -m 644 %{_builddir}/InputPlumber/rootfs/usr/lib/systemd/system/* %{buildroot}/usr/lib/systemd/system/
install -D -m 644 %{_builddir}/InputPlumber/rootfs/usr/lib/udev/hwdb.d/59-inputplumber.hwdb %{buildroot}/usr/lib/udev/hwdb.d/59-inputplumber.hwdb
install -D -m 644 %{_builddir}/InputPlumber/rootfs/usr/lib/udev/hwdb.d/60-inputplumber-autostart.hwdb %{buildroot}/usr/lib/udev/hwdb.d/60-inputplumber-autostart.hwdb
install -D -m 644 %{_builddir}/InputPlumber/rootfs/usr/lib/udev/rules.d/90-inputplumber-autostart.rules %{buildroot}/usr/lib/udev/rules.d/90-inputplumber-autostart.rules
install -D -m 644 %{_builddir}/InputPlumber/rootfs/usr/share/inputplumber/capability_maps/* %{buildroot}/usr/share/inputplumber/capability_maps/
install -D -m 644 %{_builddir}/InputPlumber/rootfs/usr/share/inputplumber/devices/* %{buildroot}/usr/share/inputplumber/devices/
install -D -m 644 %{_builddir}/InputPlumber/rootfs/usr/share/inputplumber/profiles/* %{buildroot}/usr/share/inputplumber/profiles/
install -D -m 644 %{_builddir}/InputPlumber/rootfs/usr/share/inputplumber/schema/* %{buildroot}/usr/share/inputplumber/schema/
install -D -m 644 %{_builddir}/InputPlumber/rootfs/usr/share/polkit-1/actions/* %{buildroot}/usr/share/polkit-1/actions/
install -D -m 644 %{_builddir}/InputPlumber/rootfs/usr/share/polkit-1/rules.d/* %{buildroot}/usr/share/polkit-1/rules.d/

# Re-assign devices with gyro as deck-uhid devices instead of xb elite
sed -i 's/- xbox-elite/- deck-uhid/g' %{buildroot}/usr/share/inputplumber/devices/50-steam_deck.yaml
sed -i 's/- xbox-elite/- deck-uhid/g' %{buildroot}/usr/share/inputplumber/devices/50-rog_ally.yaml
sed -i 's/- xbox-elite/- deck-uhid/g' %{buildroot}/usr/share/inputplumber/devices/50-rog_ally_x.yaml
sed -i 's/- xbox-elite/- deck-uhid/g' %{buildroot}/usr/share/inputplumber/devices/50-legion_go.yaml
sed -i 's/- xbox-elite/- deck-uhid/g' %{buildroot}/usr/share/inputplumber/devices/50-legion_go_s.yaml
sed -i 's/- xbox-elite/- deck-uhid/g' %{buildroot}/usr/share/inputplumber/devices/50-msi_claw7_a2vm.yaml
sed -i 's/- xbox-elite/- deck-uhid/g' %{buildroot}/usr/share/inputplumber/devices/50-msi_claw8_a2vm.yaml
sed -i 's/- xbox-elite/- deck-uhid/g' %{buildroot}/usr/share/inputplumber/devices/50-msi_claw_a1m.yaml

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
/usr/share/dbus-1/system.d/org.shadowblip.InputPlumber.conf
/usr/share/dbus-1/system-services/
/usr/lib/systemd/system/inputplumber.service
/usr/lib/systemd/system/inputplumber-suspend.service
/usr/lib/udev/hwdb.d/*.hwdb
/usr/lib/udev/rules.d/*.rules
/usr/share/inputplumber/capability_maps/*.yaml
/usr/share/inputplumber/devices/*.yaml
/usr/share/inputplumber/profiles/*.yaml
/usr/share/inputplumber/schema/*.json
/usr/share/polkit-1/actions/*
/usr/share/polkit-1/rules.d/*

%changelog
