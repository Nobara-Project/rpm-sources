Name:           jupiter-hw-support
Version:        0.0.git.1256.484fa801
Release:        26%{?dist}
Summary:        Steam Deck Hardware Support Package
License:        MIT
URL:            https://github.com/nobara-project/steamdeck-edition-packages
Source0:        %{URL}/releases/download/1.0/jupiter-hw-support.tar.gz
Patch0:         fedora.patch
Patch1:         selinux.patch

Requires:       python3
Requires:       python3-evdev
Requires:       python3-crcmod
Requires:       python3-click
Requires:       python3-progressbar2
Requires:       python3-hid
Requires:       hidapi
Requires:       dmidecode
Requires:       jq
Requires:       alsa-utils
Requires:       parted
Requires:       e2fsprogs
Requires:       f3
Requires:       jupiter-fan-control
Requires:       gamescope-htpc-common
Requires:       gamescope-handheld-common

BuildRequires:  systemd-rpm-macros
BuildRequires:  xcursorgen
BuildRequires:  sed

%description
SteamOS 3.0 Steam Deck Hardware Support Package

%package -n gamescope-htpc-common
Summary: SteamOS 3.0 common required files
%description -n gamescope-htpc-common

%package -n gamescope-handheld-common
Summary: SteamOS 3.0 handheld required files
Requires: gamescope-htpc-common
%description -n gamescope-handheld-common

# Disable debug packages
%define debug_package %{nil}

%prep
%autosetup -p1 -n %{name}
cd %{_builddir}
cat << EOF >> %{_builddir}/96-jupiter-hw-support.preset
enable jupiter-biosupdate.service
enable jupiter-controller-update.service
EOF

%build

%install
export QA_RPATHS=0x0003
mkdir -p %{buildroot}%{_datadir}/
mkdir -p %{buildroot}%{_unitdir}/
mkdir -p %{buildroot}%{_presetdir}/
mkdir -p %{buildroot}%{_bindir}/
mkdir -p %{buildroot}%{_libexecdir}/
mkdir -p %{buildroot}%{_sysconfdir}/
mkdir -p %{buildroot}%{_prefix}/lib/hwsupport/
install -m 644 %{_builddir}/96-jupiter-hw-support.preset %{buildroot}%{_presetdir}/
cp -rv usr/share/* %{buildroot}%{_datadir}
cp -rv usr/lib/systemd/system/* %{buildroot}%{_unitdir}/
cp usr/lib/hwsupport/power-button-handler.py %{buildroot}%{_prefix}/lib/hwsupport/power-button-handler.py
cp usr/lib/hwsupport/format-device.sh %{buildroot}%{_libexecdir}/format-device
cp usr/lib/hwsupport/format-sdcard.sh %{buildroot}%{_libexecdir}/format-sdcard
cp usr/lib/hwsupport/steamos-automount.sh %{buildroot}%{_libexecdir}/steamos-automount
cp usr/lib/hwsupport/trim-devices.sh %{buildroot}%{_libexecdir}/trim-devices
cp -rv usr/lib/udev %{buildroot}%{_prefix}/lib/udev
cp -rv usr/bin/* %{buildroot}%{_bindir}
cp -rv usr/lib/systemd/system/* %{buildroot}%{_unitdir}
cp -rv etc/* %{buildroot}%{_sysconfdir}
sed -i 's@steamos-cursor.png@usr/share/steamos/steamos-cursor.png@g' usr/share/steamos/steamos-cursor-config
xcursorgen usr/share/steamos/steamos-cursor-config %{buildroot}%{_datadir}/icons/steam/cursors/default

# Do pre-installation
%pre
# Check if the file exists and remove it
if [ -f /usr/bin/steamos-polkit-helpers/steamos-retrigger-automounts ]; then
    rm -f /usr/bin/steamos-polkit-helpers/steamos-retrigger-automounts
fi

# Do post-installation
%post
%systemd_post jupiter-biosupdate.service
%systemd_post jupiter-controller-update.service

# Do before uninstallation
%preun
%systemd_preun jupiter-biosupdate.service
%systemd_preun jupiter-controller-update.service

# Do after uninstallation
%postun
%systemd_postun_with_restart jupiter-biosupdate.service
%systemd_postun_with_restart jupiter-controller-update.service

# Do post-installation
%post -n gamescope-handheld-common
grubby --update-kernel=ALL --args="amdgpu.gttsize=8128 spi_amd.speed_dev=1 audit=0 fbcon=vc:2-6 iomem=relaxed amdgpu.ppfeaturemask=0xffffffff"
grub2-mkconfig -o /boot/grub2/grub.cfg

# Do after uninstallation
%postun -n gamescope-handheld-common
grubby --update-kernel=ALL --remove-args="amdgpu.gttsize=8128 spi_amd.speed_dev=1 audit=0 fbcon=vc:2-6 iomem=relaxed amdgpu.ppfeaturemask=0xffffffff"
grub2-mkconfig -o /boot/grub2/grub.cfg

# This lists all the files that are included in the rpm package and that
# are going to be installed into target system where the rpm is installed.
%files
%{_sysconfdir}/systemd/system/alsa-restore.service
%{_bindir}/amd_system_info
%{_bindir}/foxnet-biosupdate
%{_bindir}/jupiter-biosupdate
%{_bindir}/jupiter-check-support
%{_bindir}/jupiter-controller-update
%{_bindir}/jupiter-initial-firmware-update
%{_bindir}/thumbstick_cal
%{_bindir}/thumbstick_fine_cal
%{_bindir}/trigger_cal
%{_bindir}/steamos-polkit-helpers/jupiter-amp-control
%{_bindir}/steamos-polkit-helpers/jupiter-biosupdate
%{_bindir}/steamos-polkit-helpers/jupiter-check-support
%{_bindir}/steamos-polkit-helpers/jupiter-dock-updater
%{_bindir}/steamos-polkit-helpers/jupiter-fan-control
%{_bindir}/steamos-polkit-helpers/jupiter-get-als-gain
%{_prefix}/lib/systemd/system/jupiter-biosupdate.service
%{_prefix}/lib/systemd/system/jupiter-controller-update.service
%{_datadir}/jupiter_bios
%{_datadir}/jupiter_bios_updater
%{_datadir}/jupiter_controller_fw_updater
%{_presetdir}/96-jupiter-hw-support.preset

%files -n gamescope-htpc-common
%{_bindir}/steamos-polkit-helpers/steamos-devkit-mode
%{_bindir}/steamos-polkit-helpers/steamos-disable-wireless-power-management
%{_bindir}/steamos-polkit-helpers/steamos-enable-sshd
%{_bindir}/steamos-polkit-helpers/steamos-factory-reset-config
%{_bindir}/steamos-polkit-helpers/steamos-format-device
%{_bindir}/steamos-polkit-helpers/steamos-trim-devices
%{_bindir}/steamos-polkit-helpers/steamos-poweroff-now
%{_bindir}/steamos-polkit-helpers/steamos-priv-write
%{_bindir}/steamos-polkit-helpers/steamos-reboot-now
%{_bindir}/steamos-polkit-helpers/steamos-reboot-other
%{_bindir}/steamos-polkit-helpers/steamos-restart-sddm
%{_bindir}/steamos-polkit-helpers/steamos-select-branch
%{_bindir}/steamos-polkit-helpers/steamos-set-hostname
%{_bindir}/steamos-polkit-helpers/steamos-set-timezone
%{_bindir}/steamos-polkit-helpers/steamos-update
%{_prefix}/lib/hwsupport/power-button-handler.py
%{_prefix}/lib/udev/rules.d/80-gpu-reset.rules
%{_prefix}/lib/udev/rules.d/99-power-button.rules
%{_libexecdir}/format-device
%{_libexecdir}/trim-devices
%{_datadir}/icons
%{_datadir}/plymouth
%{_datadir}/steamos
%{_datadir}/polkit-1/rules.d/*
%{_datadir}/polkit-1/actions/*

%files -n gamescope-handheld-common
%{_sysconfdir}/systemd/system/steamos-automount@.service
%{_bindir}/steamos-polkit-helpers/steamos-format-sdcard
%{_libexecdir}/steamos-automount
%{_libexecdir}/format-sdcard
%{_prefix}/lib/udev/rules.d/99-steamos-automount.rules

# Finally, changes from the latest release of your application are generated from
# your project's Git history. It will be empty until you make first annotated Git tag.
%changelog
