%global _firmwarepath   /usr/lib/firmware

Summary: ROG Ally/Ally X firmware
Name: rogally-firmware
Version: 1.0
Release: 6%{?dist}
License: Public Domain
Group: System Environment/Base
Source0: https://github.com/ublue-os/bazzite/raw/main/system_files/deck/shared/usr/lib/firmware/ti/tas2781/TAS2XXX1EB3.bin.xz
Source1: ally_mcu_powersave
BuildArch: noarch
BuildRequires: filesystem

%description
This package contains ROG Ally/Ally X firmware

%install
install -d %{buildroot}%{_firmwarepath}/ti/tas2781/
install -d %{buildroot}%{_sysconfdir}/cron.d/
install -m 0644 %{SOURCE0} %{buildroot}%{_firmwarepath}/ti/tas2781/TAS2XXX1EB3.bin.xz
install -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/cron.d/ally_mcu_powersave
unxz %{buildroot}%{_firmwarepath}/ti/tas2781/TAS2XXX1EB3.bin.xz
ln -s %{_firmwarepath}/ti/tas2781/TAS2XXX1EB3.bin %{buildroot}%{_firmwarepath}/TAS2XXX1EB3.bin

%files
%{_firmwarepath}/ti/tas2781/*
%{_firmwarepath}/TAS2XXX1EB3.bin
%{_sysconfdir}/cron.d/ally_mcu_powersave
%changelog
