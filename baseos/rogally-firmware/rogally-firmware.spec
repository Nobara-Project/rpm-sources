%global _firmwarepath   /usr/lib/firmware

Summary: ROG Ally/Ally X firmware
Name: rogally-firmware
Version: 1.0
Release: 1%{?dist}
License: Public Domain
Group: System Environment/Base
Source0: https://github.com/ublue-os/bazzite/raw/main/system_files/deck/shared/usr/lib/firmware/ti/tas2781/TAS2XXX1EB3.bin.xz

BuildArch: noarch
BuildRequires: filesystem
Requires:   inputplumber

%description
This package contains ROG Ally/Ally X firmware

%install
install -d %{buildroot}%{_firmwarepath}/ti/tas2781/
install -m 0644 %{SOURCE0} %{buildroot}%{_firmwarepath}/ti/tas2781/TAS2XXX1EB3.bin.xz
unxz %{buildroot}%{_firmwarepath}/ti/tas2781/TAS2XXX1EB3.bin.xz
ln -s %{_firmwarepath}/ti/tas2781/TAS2XXX1EB3.bin %{buildroot}%{_firmwarepath}/TAS2XXX1EB3.bin

%files
%{_firmwarepath}/ti/tas2781/*
%{_firmwarepath}/TAS2XXX1EB3.bin

%changelog
