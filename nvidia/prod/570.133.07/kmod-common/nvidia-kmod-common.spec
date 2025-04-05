%global _dracut_conf_d  %{_prefix}/lib/dracut/dracut.conf.d

# gsp_*.bin: ELF 64-bit LSB executable, UCB RISC-V
%global _binaries_in_noarch_packages_terminate_build 0
%global __brp_strip %{nil}

Name:           nvidia-kmod-common
Version:        570.133.07
Release:        1%{?dist}
Summary:        Common file for NVIDIA's proprietary driver kernel modules
Epoch:          3
License:        NVIDIA License
URL:            http://www.nvidia.com/object/unix.html

BuildArch:      noarch

Source0:        %{name}-%{version}.tar.xz
Source17:       nvidia-boot-update
Source18:       kernel.conf
Source19:       nvidia-modeset.conf
Source20:       nvidia.conf
Source21:       60-nvidia.rules

# UDev rule location (_udevrulesdir) and systemd macros:
BuildRequires:  systemd-rpm-macros

# Owns /usr/lib/firmware:
Requires:       linux-firmware
Requires:       nvidia-modprobe
Requires:       nvidia-kmod = %{?epoch:%{epoch}:}%{version}
Provides:       nvidia-kmod-common = %{?epoch:%{epoch}:}%{version}
Obsoletes:      cuda-nvidia-kmod-common < %{?epoch:%{epoch}:}%{version}

%description
This package provides the common files required by all NVIDIA kernel module
package variants.

%prep
%autosetup

%install
# Script for post/preun tasks
install -p -m 0755 -D %{SOURCE17} %{buildroot}%{_bindir}/nvidia-boot-update

# Choice of kernel module type:
install -p -m 0644 -D %{SOURCE18} %{buildroot}%{_sysconfdir}/nvidia/kernel.conf

# Nvidia modesetting support:
install -p -m 0644 -D %{SOURCE19} %{buildroot}%{_sysconfdir}/modprobe.d/nvidia-modeset.conf

# Load nvidia-uvm, enable complete power management:
install -p -m 0644 -D %{SOURCE20} %{buildroot}%{_modprobedir}/nvidia.conf


# UDev rules
# https://github.com/NVIDIA/nvidia-modprobe/blob/master/modprobe-utils/nvidia-modprobe-utils.h#L33-L46
# https://github.com/negativo17/nvidia-kmod-common/issues/11
# https://github.com/negativo17/nvidia-driver/issues/27
install -p -m 644 -D %{SOURCE21} %{buildroot}%{_udevrulesdir}/60-nvidia.rules

# Firmware files:
mkdir -p %{buildroot}%{_prefix}/lib/firmware/nvidia/%{version}/
install -p -m 644 firmware/* %{buildroot}%{_prefix}/lib/firmware/nvidia/%{version}

%post
%{_bindir}/nvidia-boot-update post

%preun
if [ "$1" -eq "0" ]; then
  %{_bindir}/nvidia-boot-update preun
fi ||:

%files
%{_modprobedir}/nvidia.conf
%{_prefix}/lib/firmware/nvidia/%{version}
%{_bindir}/nvidia-boot-update
%config(noreplace) %{_sysconfdir}/modprobe.d/nvidia-modeset.conf
%config(noreplace) %{_sysconfdir}/nvidia/kernel.conf
%{_udevrulesdir}/60-nvidia.rules

%changelog
* Wed Mar 19 2025 Simone Caronni <negativo17@gmail.com> - 3:570.133.07-1
- Update to 570.133.07.

* Mon Mar 10 2025 Simone Caronni <negativo17@gmail.com> - 3:570.124.04-2
- Move nvidia-boot-update to _bindir.

* Fri Feb 28 2025 Simone Caronni <negativo17@gmail.com> - 3:570.124.04-1
- Update to 570.124.04.

* Wed Feb 12 2025 Simone Caronni <negativo17@gmail.com> - 3:570.86.16-3
- Update nvidia-boot-update script.

* Wed Feb 12 2025 Simone Caronni <negativo17@gmail.com> - 3:570.86.16-2
- Also add a softep on nvidia-uvm, required for some GPUs.

* Fri Jan 31 2025 Simone Caronni <negativo17@gmail.com> - 3:570.86.16-1
- Update to 570.86.16.

* Mon Jan 27 2025 Simone Caronni <negativo17@gmail.com> - 3:570.86.15-1
- Update to 570.86.15.

* Wed Dec 25 2024 Simone Caronni <negativo17@gmail.com> - 3:565.77-2
- Run nvidia-modprobe only on add/bind (thanks os369510).

* Thu Dec 05 2024 Simone Caronni <negativo17@gmail.com> - 3:565.77-1
- Update to 565.77.

* Tue Oct 29 2024 Simone Caronni <negativo17@gmail.com> - 3:565.57.01-2
- Update power management configuration.

* Wed Oct 23 2024 Simone Caronni <negativo17@gmail.com> - 3:565.57.01-1
- Update to 565.57.01.

* Fri Oct 11 2024 Simone Caronni <negativo17@gmail.com> - 3:560.35.03-2
- Fix configuration file replacement (#14).

* Wed Aug 21 2024 Simone Caronni <negativo17@gmail.com> - 3:560.35.03-1
- Update to 560.35.03.

* Tue Aug 06 2024 Simone Caronni <negativo17@gmail.com> - 3:560.31.02-1
- Update to 560.31.02.

* Mon Aug 05 2024 Simone Caronni <negativo17@gmail.com> - 3:560.28.03-1
- Update to 560.28.03.

* Tue Jul 02 2024 Simone Caronni <negativo17@gmail.com> - 3:555.58.02-1
- Update to 555.58.02.

* Thu Jun 27 2024 Simone Caronni <negativo17@gmail.com> - 3:555.58-1
- Update to 555.58.

* Thu Jun 06 2024 Simone Caronni <negativo17@gmail.com> - 3:555.52.04-1
- Update to 555.52.04.

* Fri May 31 2024 Simone Caronni <negativo17@gmail.com> - 3:555.42.02-2
- Fix typo in preun scriptlet.

* Wed May 22 2024 Simone Caronni <negativo17@gmail.com> - 3:555.42.02-1
- Update to 555.42.02.

* Fri Apr 26 2024 Simone Caronni <negativo17@gmail.com> - 3:550.78-1
- Update to 550.78.

* Thu Apr 18 2024 Simone Caronni <negativo17@gmail.com> - 3:550.76-1
- Update to 550.76.

* Sun Mar 24 2024 Simone Caronni <negativo17@gmail.com> - 3:550.67-1
- Update to 550.67.

* Mon Mar 11 2024 Simone Caronni <negativo17@gmail.com> - 3:550.54.14-2
- Add support for installing drivers without a configured bootloader (i.e.
  kickstart case).
- Add support for sdboot.

* Sun Mar 03 2024 Simone Caronni <negativo17@gmail.com> - 3:550.54.14-1
- Update to 550.54.14.

* Tue Feb 06 2024 Simone Caronni <negativo17@gmail.com> - 3:550.40.07-1
- Update to 550.40.07.
