Name:           nobara-eac
Version:        1.0
Release:        2%{?dist}
Summary:        Easy Anti-Cheat Linux v2 boot entries for Nobara kernels
License:        MIT
URL:            https://onlineservices.epicgames.com/news/introducing-easy-anti-cheat-linux-v2
BuildArch:      noarch

Source0:        95-nobara-eac.install
Source1:        nobara-eac.sysconfig
# Public Nobara Secure Boot CA certificate, enrolled as a MOK so shim boots
# the Nobara-signed GRUB and kernels
# SHA-256 A3:6D:9C:67:6F:ED:15:D6:45:A3:D2:84:5F:CE:8B:73:AB:54:CC:2B:DF:33:BD:A4:37:05:F7:40:68:41:6A:2E
Source2:        nobara-sb-ca.der
# Public Nobara Secure Boot signer certificate, built into the kernels as a
# trusted key so Nobara-signed out-of-tree modules load with enforced signatures
# SHA-256 66:CF:D7:6F:A1:77:FF:22:45:3A:7F:21:44:97:1B:52:5C:A5:12:15:3F:60:2C:8C:36:D2:6A:20:AE:4D:86:B7
Source3:        nobara-sb-signer.crt
Source4:        nobara-eac-enroll
Source5:        nobara-eac.service

BuildRequires:  systemd-rpm-macros

Requires:       %{name}-certs = %{version}-%{release}
Requires:       coreutils
Requires:       gawk
Requires:       grub2-common
Requires:       mokutil
Requires:       sed

%description
Adds a kernel-install plugin that gives every installed kernel a GRUB boot
entry with the kernel command line Easy Anti-Cheat Linux v2 requires
(lockdown integrity mode, enforced module signatures, kexec disabled,
IOMMU without passthrough, BPF LSM) next to an entry without it.
Once Secure Boot is enabled and nobara-eac-enroll has enrolled the Nobara CA
and the local DKMS and akmods module signing keys, the Easy Anti-Cheat entry
is the default.

%package certs
Summary:        Nobara Secure Boot certificates

%description certs
The public Nobara Secure Boot CA and signer certificates. Enroll the CA with
  sudo mokutil --import %{_datadir}/nobara/eac/nobara-sb-ca.der
and confirm the enrollment in MokManager on the next boot. The kernel builds
use the signer certificate as a trusted module signing key.

%prep

%build

%install
install -Dm755 %{SOURCE0} %{buildroot}%{_prefix}/lib/kernel/install.d/95-nobara-eac.install
install -Dm644 %{SOURCE1} %{buildroot}%{_sysconfdir}/sysconfig/nobara-eac
install -Dm644 %{SOURCE2} %{buildroot}%{_datadir}/nobara/eac/nobara-sb-ca.der
install -Dm644 %{SOURCE3} %{buildroot}%{_datadir}/nobara/eac/nobara-sb-signer.crt
install -Dm755 %{SOURCE4} %{buildroot}%{_bindir}/nobara-eac-enroll
install -Dm644 %{SOURCE5} %{buildroot}%{_unitdir}/nobara-eac.service
# Always on, it only rewrites boot entries when Secure Boot or the MOKs changed
mkdir -p %{buildroot}%{_unitdir}/multi-user.target.wants
ln -s ../nobara-eac.service %{buildroot}%{_unitdir}/multi-user.target.wants/nobara-eac.service

%posttrans
%{_prefix}/lib/kernel/install.d/95-nobara-eac.install apply-all || :

%preun
if [ $1 -eq 0 ]; then
    %{_prefix}/lib/kernel/install.d/95-nobara-eac.install remove-all || :
fi

%files
%{_prefix}/lib/kernel/install.d/95-nobara-eac.install
%{_bindir}/nobara-eac-enroll
%{_unitdir}/nobara-eac.service
%{_unitdir}/multi-user.target.wants/nobara-eac.service
%config(noreplace) %{_sysconfdir}/sysconfig/nobara-eac

%files certs
%dir %{_datadir}/nobara/eac
%{_datadir}/nobara/eac/nobara-sb-ca.der
%{_datadir}/nobara/eac/nobara-sb-signer.crt

%changelog
* Fri Oct 30 2026 GloriousEggroll <gloriouseggroll@gmail.com> - 1.0-2
- Add nobara-eac-enroll to enroll the Nobara CA and the local DKMS and akmods
  module signing keys as MOKs
- auto mode: EAC is the default only once those keys are enrolled
- Re-check the boot entries on every boot with nobara-eac.service

* Fri Oct 30 2026 GloriousEggroll <gloriouseggroll@gmail.com> - 1.0-1
- Initial package
