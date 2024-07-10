%global _firmwarepath   /usr/lib/firmware
%define __os_install_post %{nil}
%global _upstreamtag 1
%global valvever 20240605.1

Summary: Steam Deck OLED firmware for wifi and bluetooth
Name: steamdeck-firmware
Version: 1.0
Release: 6.%{valvever}%{?dist}
License: Public Domain
Group: System Environment/Base
Source0: https://steamdeck-packages.steamos.cloud/archlinux-mirror/jupiter-main/os/x86_64/linux-firmware-neptune-jupiter.%{valvever}-%{_upstreamtag}-any.pkg.tar.zst

BuildArch: noarch
BuildRequires: filesystem
Requires:   steamdeck-dsp
Requires:   galileo-mura
Obsoletes: steamdeck-oled-firmware

%description
This package contains Steam Deck OLED firmware for wifi and bluetooth

%pre
# Check if directories exist and remove them before installation
if [ -d "%{_firmwarepath}/ath11k/QCA2066" ]; then
    rm -rf "%{_firmwarepath}/ath11k/QCA206X"
fi

if [ -d "%{_firmwarepath}/ath11k/QCA206X" ]; then
    rm -rf "%{_firmwarepath}/ath11k/QCA2066"
fi

%install
tar --strip-components 1 -xvf %{SOURCE0}
rm -rf %{buildroot}

# Create necessary directories in buildroot
install -d %{buildroot}%{_firmwarepath}/ath11k/QCA2066/hw2.1/
install -m 0644 %{_builddir}/lib/firmware/ath11k/QCA206X/hw2.1/amss.bin.zst %{buildroot}%{_firmwarepath}/ath11k/QCA2066/hw2.1/amss.bin.zst
install -m 0644 %{_builddir}/lib/firmware/ath11k/QCA206X/hw2.1/board-2.bin.zst %{buildroot}%{_firmwarepath}/ath11k/QCA2066/hw2.1/board-2.bin.zst
install -m 0644 %{_builddir}/lib/firmware/ath11k/QCA206X/hw2.1/board.bin.zst %{buildroot}%{_firmwarepath}/ath11k/QCA2066/hw2.1/board.bin.zst
install -m 0644 %{_builddir}/lib/firmware/ath11k/QCA206X/hw2.1/boardg.bin.zst %{buildroot}%{_firmwarepath}/ath11k/QCA2066/hw2.1/boardg.bin.zst
install -m 0644 %{_builddir}/lib/firmware/ath11k/QCA206X/hw2.1/m3.bin.zst %{buildroot}%{_firmwarepath}/ath11k/QCA2066/hw2.1/m3.bin.zst
install -m 0644 %{_builddir}/lib/firmware/ath11k/QCA206X/hw2.1/regdb.bin.zst %{buildroot}%{_firmwarepath}/ath11k/QCA2066/hw2.1/regdb.bin.zst

# for backwards compatibility with pre-6.9 kernels
install -d %{buildroot}%{_firmwarepath}/ath11k/QCA206X/hw2.1/
install -m 0644 %{_builddir}/lib/firmware/ath11k/QCA206X/hw2.1/amss.bin.zst %{buildroot}%{_firmwarepath}/ath11k/QCA206X/hw2.1/amss.bin.zst
install -m 0644 %{_builddir}/lib/firmware/ath11k/QCA206X/hw2.1/board-2.bin.zst %{buildroot}%{_firmwarepath}/ath11k/QCA206X/hw2.1/board-2.bin.zst
install -m 0644 %{_builddir}/lib/firmware/ath11k/QCA206X/hw2.1/board.bin.zst %{buildroot}%{_firmwarepath}/ath11k/QCA206X/hw2.1/board.bin.zst
install -m 0644 %{_builddir}/lib/firmware/ath11k/QCA206X/hw2.1/boardg.bin.zst %{buildroot}%{_firmwarepath}/ath11k/QCA206X/hw2.1/boardg.bin.zst
install -m 0644 %{_builddir}/lib/firmware/ath11k/QCA206X/hw2.1/m3.bin.zst %{buildroot}%{_firmwarepath}/ath11k/QCA206X/hw2.1/m3.bin.zst
install -m 0644 %{_builddir}/lib/firmware/ath11k/QCA206X/hw2.1/regdb.bin.zst %{buildroot}%{_firmwarepath}/ath11k/QCA206X/hw2.1/regdb.bin.zst

install -d %{buildroot}%{_firmwarepath}/qca/
install -m 0644 %{_builddir}/lib/firmware/qca/hpbtfw21.tlv.zst %{buildroot}%{_firmwarepath}/qca/hpbtfw21.tlv.zst
install -m 0644 %{_builddir}/lib/firmware/qca/hpnv21.309.zst %{buildroot}%{_firmwarepath}/qca/hpnv21.309.zst
install -m 0644 %{_builddir}/lib/firmware/qca/hpnv21.bin.zst %{buildroot}%{_firmwarepath}/qca/hpnv21.bin.zst
install -m 0644 %{_builddir}/lib/firmware/qca/hpnv21g.309.zst %{buildroot}%{_firmwarepath}/qca/hpnv21g.309.zst
install -m 0644 %{_builddir}/lib/firmware/qca/hpnv21g.bin.zst %{buildroot}%{_firmwarepath}/qca/hpnv21g.bin.zst

# Decompress each .zst file and remove the compressed archive
find %{buildroot}%{_firmwarepath}/ath11k/QCA2066/hw2.1/ -name '*.zst' -exec zstd -d {} --rm \;
find %{buildroot}%{_firmwarepath}/qca/ -name '*.zst' -exec zstd -d {} --rm \;


%files
%{_firmwarepath}/qca/*
%{_firmwarepath}/ath11k/*


%changelog
* Sat May 25 2024 Matthew Schwartz <njtransit215@gmail.com> - 20240503.1
- New version 20240503.1, switch to upstream Valve package instead of evlaV
* Thu Nov 25 2021 Thomas Crider <gloriouseggroll@gmail.com> - 1.0.0
- New version v1.0.0
