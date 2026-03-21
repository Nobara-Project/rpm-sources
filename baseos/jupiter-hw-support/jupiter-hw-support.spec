Name:           jupiter-hw-support
Version:        0.0.git.1256.484fa801
Release:        43%{?dist}
Summary:        Steam Deck Hardware Support Package
License:        MIT
URL:            https://github.com/nobara-project/steamdeck-edition-packages
Source0:        %{URL}/releases/download/1.0/jupiter-hw-support.tar.gz

ExcludeArch:    %{ix86}

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
Requires:       gamescope-session-common
Requires:       gamescope-htpc-common
Requires:       gamescope-handheld-common

BuildRequires:  systemd-rpm-macros
BuildRequires:  xcursorgen
BuildRequires:  sed

%description
SteamOS 3.0 Steam Deck Hardware Support Package

%package -n gamescope-session-common
Requires:       gamescope-session-steam
Summary: Gamescope Session required files
%description -n gamescope-session-common

%package -n gamescope-htpc-common
Requires: gamescope-session-common
Summary: SteamOS HTPC experience required files
%description -n gamescope-htpc-common

%package -n gamescope-handheld-common
Summary: SteamOS Handheld experience required files
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
mkdir -p %{buildroot}%{_prefix}/lib/jupiter-dock-updater/
mkdir -p %{buildroot}%{_sysconfdir}/xdg/autostart/
install -m 644 %{_builddir}/96-jupiter-hw-support.preset %{buildroot}%{_presetdir}/
cp -rv usr/share/* %{buildroot}%{_datadir}
cp -rv usr/lib/systemd/system/* %{buildroot}%{_unitdir}/
cp -rv usr/lib/hwsupport/* %{buildroot}%{_libexecdir}/
cp usr/lib/jupiter-dock-updater/* %{buildroot}%{_prefix}/lib/jupiter-dock-updater/
cp -rv usr/lib/udev %{buildroot}%{_prefix}/lib/udev
cp -rv usr/bin/* %{buildroot}%{_bindir}
cp -rv usr/lib/systemd/system/* %{buildroot}%{_unitdir}
cp -rv etc/* %{buildroot}%{_sysconfdir}
chmod +x %{buildroot}%{_sysconfdir}/xdg/autostart/steam.desktop
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

# This lists all the files that are included in the rpm package and that
# are going to be installed into target system where the rpm is installed.
%files
%{_sysconfdir}/systemd/system/alsa-restore.service
%{_bindir}/amd_system_info
%{_bindir}/foxnet-biosupdate
%{_bindir}/jupiter*
%{_bindir}/thumbstick_cal
%{_bindir}/thumbstick_fine_cal
%{_bindir}/trigger_cal
%{_prefix}/lib/systemd/system/jupiter-biosupdate.service
%{_prefix}/lib/systemd/system/jupiter-controller-update.service
%{_prefix}/lib/systemd/system/multi-user.target.wants/jupiter-biosupdate.service
%{_prefix}/lib/systemd/system/multi-user.target.wants/jupiter-controller-update.service
%{_datadir}/jupiter_bios
%{_datadir}/jupiter_bios_updater
%{_datadir}/jupiter_controller_fw_updater
%{_presetdir}/96-jupiter-hw-support.preset
%{_prefix}/lib/udev/rules.d/80-rtl-wobt.rules

%files -n gamescope-session-common
%{_bindir}/steamos-polkit-helpers/*
%{_prefix}/lib/udev/rules.d/80-gpu-reset.rules

%{_datadir}/icons
%{_datadir}/steamos
%{_datadir}/polkit-1/rules.d/*
%{_datadir}/polkit-1/actions/*

%files -n gamescope-htpc-common
%{_datadir}/plymouth
%{_sysconfdir}/xdg/autostart/steam.desktop
%{_prefix}/lib/udev/rules.d/99-sdcard-rescan.rules

%files -n gamescope-handheld-common
%{_libexecdir}/*
%{_prefix}/lib/udev/rules.d/99-steamos-automount.rules
%{_prefix}/lib/udev/rules.d/99-power-button.rules
%{_sysconfdir}/systemd/system/steamos-automount@.service

%{_prefix}/lib/jupiter-dock-updater/

# Finally, changes from the latest release of your application are generated from
# your project's Git history. It will be empty until you make first annotated Git tag.
%changelog
