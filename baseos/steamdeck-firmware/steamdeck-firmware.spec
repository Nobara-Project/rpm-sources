%global _firmwarepath   /usr/lib/firmware
%define __os_install_post %{nil}

Summary: Steam Deck OLED firmware for wifi and bluetooth
Name: steamdeck-firmware
Version: 1.0
Release: 3%{?dist}
License: Public Domain
Group: System Environment/Base
Source0: https://gitlab.com/evlaV/linux-firmware-neptune/-/archive/jupiter-20231113.1/linux-firmware-neptune-jupiter-20231113.1.tar.gz?path=ath11k/QCA206X#/ath11k.tar.gz
Source1: https://gitlab.com/evlaV/linux-firmware-neptune/-/raw/jupiter-20231113.1/qca/hpbtfw21.tlv
Source2: https://gitlab.com/evlaV/linux-firmware-neptune/-/raw/jupiter-20231113.1/qca/hpnv21.309
Source3: https://gitlab.com/evlaV/linux-firmware-neptune/-/raw/jupiter-20231113.1/qca/hpnv21.bin
Source4: https://gitlab.com/evlaV/linux-firmware-neptune/-/raw/jupiter-20231113.1/qca/hpnv21g.309
Source5: https://gitlab.com/evlaV/linux-firmware-neptune/-/raw/jupiter-20231113.1/qca/hpnv21g.bin

BuildArch: noarch
BuildRequires: filesystem
Requires:   steamdeck-dsp
Requires:   galileo-mura
Obsoletes: steamdeck-oled-firmware

%description
This package contains Steam Deck OLED firmware for wifi and bluetooth

%install
tar --strip-components 1 -xvf %{SOURCE0}
rm -rf %{buildroot}

install -d %{buildroot}%{_firmwarepath}/ath11k/QCA206X/hw2.1/
install -m 0644 ath11k/QCA206X/hw2.1/Data.msc %{buildroot}%{_firmwarepath}/ath11k/QCA206X/hw2.1/Data.msc
install -m 0644 ath11k/QCA206X/hw2.1/amss.bin %{buildroot}%{_firmwarepath}/ath11k/QCA206X/hw2.1/amss.bin
install -m 0644 ath11k/QCA206X/hw2.1/board-2.bin %{buildroot}%{_firmwarepath}/ath11k/QCA206X/hw2.1/board-2.bin
install -m 0644 ath11k/QCA206X/hw2.1/board.bin %{buildroot}%{_firmwarepath}/ath11k/QCA206X/hw2.1/board.bin
install -m 0644 ath11k/QCA206X/hw2.1/boardg.bin %{buildroot}%{_firmwarepath}/ath11k/QCA206X/hw2.1/boardg.bin
install -m 0644 ath11k/QCA206X/hw2.1/m3.bin %{buildroot}%{_firmwarepath}/ath11k/QCA206X/hw2.1/m3.bin
install -m 0644 ath11k/QCA206X/hw2.1/regdb.bin %{buildroot}%{_firmwarepath}/ath11k/QCA206X/hw2.1/regdb.bin

install -d %{buildroot}%{_firmwarepath}/qca/
install -m 0644 %{SOURCE1} %{buildroot}%{_firmwarepath}/qca/hpbtfw21.tlv
install -m 0644 %{SOURCE2} %{buildroot}%{_firmwarepath}/qca/hpnv21.309
install -m 0644 %{SOURCE3} %{buildroot}%{_firmwarepath}/qca/hpnv21.bin
install -m 0644 %{SOURCE4} %{buildroot}%{_firmwarepath}/qca/hpnv21g.309
install -m 0644 %{SOURCE5} %{buildroot}%{_firmwarepath}/qca/hpnv21g.bin

rm -rf %{SOURCE0}


%files
%{_firmwarepath}/qca/*
%{_firmwarepath}/ath11k/*


%changelog
* Thu Nov 25 2021 Thomas Crider <gloriouseggroll@gmail.com> - 1.0.0
- New version v1.0.0

