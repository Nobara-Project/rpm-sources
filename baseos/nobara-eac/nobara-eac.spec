Name:           nobara-eac
Version:        1.2
Release:        2%{?dist}
Summary:        Boot entries and Secure Boot keys for the Nobara Easy Anti-Cheat kernel
License:        MIT
URL:            https://onlineservices.epicgames.com/news/introducing-easy-anti-cheat-linux-v2
BuildArch:      noarch

Source0:        95-nobara-eac.install
Source1:        nobara-eac.sysconfig
# Public Nobara Secure Boot CA certificate, enrolled as a MOK so shim boots
# the normal kernel (kernel)
# SHA-256 A3:6D:9C:67:6F:ED:15:D6:45:A3:D2:84:5F:CE:8B:73:AB:54:CC:2B:DF:33:BD:A4:37:05:F7:40:68:41:6A:2E
Source2:        nobara-sb-ca.der
# Public Nobara Secure Boot signer certificate, issued by that CA: signs the
# normal kernel
# SHA-256 66:CF:D7:6F:A1:77:FF:22:45:3A:7F:21:44:97:1B:52:5C:A5:12:15:3F:60:2C:8C:36:D2:6A:20:AE:4D:86:B7
Source3:        nobara-sb-signer.crt
Source4:        nobara-eac-enroll
Source5:        nobara-eac.service
Source6:        nobara-eac-kmods
# Public Nobara EAC CA certificate, enrolled as a MOK so shim boots GRUB and
# the Easy Anti-Cheat kernel (kernel-eac). A separate hierarchy, so Easy
# Anti-Cheat can tell an EAC boot by the CA shim measures into PCR 7
# SHA-256 97:D9:BA:02:B5:50:05:36:05:8E:C8:F3:4D:4B:60:7C:AB:AF:81:FD:5D:8F:21:32:7E:35:E2:9D:15:86:3B:C2
Source7:        nobara-eac-ca.der
# Public Nobara EAC signer certificate, issued by the EAC CA: signs GRUB,
# kernel-eac and the kmod-*-signed-* modules, and kernel-eac trusts it (only
# it) for out-of-tree module signatures
# SHA-256 85:3E:7C:94:17:8D:20:F0:D2:1E:91:7A:BA:30:3A:AF:31:FF:43:35:75:5D:30:BB:76:81:4B:9E:AE:BD:CB:21
Source8:        nobara-eac-signer.crt
# pkexec nobara-eac-enroll, for the Nobara updater's Secure Boot dialog
Source9:        org.nobaraproject.eac-enroll.policy
# Replace the DKMS and akmods kernel-install plugins with wrappers that skip
# the EAC kernel: it has no development files and loads only Nobara-signed
# modules. Other kernels run the original plugins.
Source10:       nobara-eac-dkms.install
Source11:       nobara-eac-akmods.install

BuildRequires:  systemd-rpm-macros

Requires:       %{name}-certs = %{version}-%{release}
Requires:       coreutils
Requires:       gawk
Requires:       findutils
Requires:       grub2-common
# grub2-editenv, grub2-set-default
Requires:       grub2-tools-minimal
Requires:       rpm
Requires:       kmod
Requires:       mokutil
Requires:       openssl
# Owns the polkit actions directory
Requires:       polkit
Requires:       sed

%description
Boot entries for kernel-eac, the Nobara kernel for Easy Anti-Cheat Linux v2:
a kernel-install plugin gives its GRUB entries the kernel command line Easy
Anti-Cheat requires (lockdown integrity mode, enforced module signatures,
kexec disabled, IOMMU without passthrough, BPF LSM) and an "[EAC]" title
prefix, and makes it the default once it can work: Secure Boot enabled, the
Nobara EAC CA enrolled, and the Nobara-signed builds of the installed
out-of-tree drivers installed for it. nobara-eac-enroll enrolls the Nobara EAC
CA and the Nobara Secure Boot CA, and the DKMS and akmods keys the normal
kernel trusts with Secure Boot on.

%package certs
Summary:        Nobara Secure Boot certificates

%description certs
The public Nobara Secure Boot certificates, from two hierarchies:
  nobara-eac-ca.der      Nobara EAC CA: GRUB and the Easy Anti-Cheat kernel
  nobara-sb-ca.der       Nobara Secure Boot CA: the normal kernel
Enroll both with sudo nobara-eac-enroll (from nobara-eac), and confirm the
enrollment in MokManager on the next boot. kernel-eac uses the EAC signer
certificate as its only trusted out-of-tree module signing key.

%prep

%build

%install
install -Dm755 %{SOURCE0} %{buildroot}%{_prefix}/lib/kernel/install.d/95-nobara-eac.install
install -Dm644 %{SOURCE1} %{buildroot}%{_sysconfdir}/sysconfig/nobara-eac
install -Dm644 %{SOURCE2} %{buildroot}%{_datadir}/nobara/eac/nobara-sb-ca.der
install -Dm644 %{SOURCE3} %{buildroot}%{_datadir}/nobara/eac/nobara-sb-signer.crt
install -Dm644 %{SOURCE7} %{buildroot}%{_datadir}/nobara/eac/nobara-eac-ca.der
install -Dm644 %{SOURCE8} %{buildroot}%{_datadir}/nobara/eac/nobara-eac-signer.crt
install -Dm755 %{SOURCE4} %{buildroot}%{_bindir}/nobara-eac-enroll
install -Dm755 %{SOURCE6} %{buildroot}%{_bindir}/nobara-eac-kmods
install -Dm644 %{SOURCE9} %{buildroot}%{_datadir}/polkit-1/actions/org.nobaraproject.eac-enroll.policy
install -Dm755 %{SOURCE10} %{buildroot}%{_sysconfdir}/kernel/install.d/40-dkms.install
install -Dm755 %{SOURCE11} %{buildroot}%{_sysconfdir}/kernel/install.d/95-akmodsposttrans.install
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
%{_bindir}/nobara-eac-kmods
%{_datadir}/polkit-1/actions/org.nobaraproject.eac-enroll.policy
%{_unitdir}/nobara-eac.service
%{_unitdir}/multi-user.target.wants/nobara-eac.service
%config(noreplace) %{_sysconfdir}/sysconfig/nobara-eac
%config %{_sysconfdir}/kernel/install.d/40-dkms.install
%config %{_sysconfdir}/kernel/install.d/95-akmodsposttrans.install

%files certs
%dir %{_datadir}/nobara/eac
%{_datadir}/nobara/eac/nobara-sb-ca.der
%{_datadir}/nobara/eac/nobara-sb-signer.crt
%{_datadir}/nobara/eac/nobara-eac-ca.der
%{_datadir}/nobara/eac/nobara-eac-signer.crt

%changelog
* Wed Nov 04 2026 GloriousEggroll <gloriouseggroll@gmail.com> - 1.2-2
- Skip DKMS and akmods for the EAC kernel when it is installed: it has no
  development files, so DKMS printed "Your kernel headers ... cannot be found"
  and akmods@ failed. Wrappers in /etc/kernel/install.d replace the DKMS and
  akmods kernel-install plugins and run them unchanged for the other kernels

* Wed Nov 04 2026 GloriousEggroll <gloriouseggroll@gmail.com> - 1.2-1
- A separate key hierarchy for Easy Anti-Cheat: the Nobara EAC CA signs GRUB,
  kernel-eac and the signed modules, the Nobara Secure Boot CA only the normal
  kernel. Easy Anti-Cheat tells the kernels apart by the CA shim measures
- certs: add the Nobara EAC CA and signer certificates
- nobara-eac-enroll enrolls the Nobara EAC CA too; --check checks it
- nobara-eac-enroll --password-stdin enrolls without prompting, with the
  one-time password from stdin, for the Nobara updater's Secure Boot dialog;
  add a polkit action for it
- The EAC kernel's modules must be signed by the Nobara EAC signer
- Add zfs (the LTS EAC kernel only) to the signed drivers

* Mon Nov 02 2026 GloriousEggroll <gloriouseggroll@gmail.com> - 1.1-5
- Fix the EAC kernel not becoming the default after an update with the Nobara
  updater: it keeps state.json with its final status, so only wait while an
  update is unconfirmed, not whenever state.json exists

* Mon Nov 02 2026 GloriousEggroll <gloriouseggroll@gmail.com> - 1.1-4
- The EAC kernel also waits for the Nobara-signed nct6687d build, when
  nct6687d is installed

* Mon Nov 02 2026 GloriousEggroll <gloriouseggroll@gmail.com> - 1.1-3
- Add nobara-eac-kmods: installs the signed builds missing for the installed
  EAC kernels, after a driver is installed or switched (nobara-driver-manager
  runs it for NVIDIA)

* Mon Nov 02 2026 GloriousEggroll <gloriouseggroll@gmail.com> - 1.1-2
- The EAC kernel also waits for the Nobara-signed builds of hid-tmff2,
  hid-fanatecff, new-lg4ff, DisplayLink (evdi) and r8125, when those drivers
  are installed

* Mon Nov 02 2026 GloriousEggroll <gloriouseggroll@gmail.com> - 1.1-1
- Easy Anti-Cheat now has its own kernel, kernel-eac, which requires this
  package. Its entries get the EAC command line and the "[EAC]" prefix; the
  normal kernel's entries stay plain. The ~eac and ~noeac entries, and the EAC
  options and marks 1.0 added to normal kernels, are removed
- auto mode: the newest EAC kernel is the default once Secure Boot is on, the
  Nobara CA is enrolled and the Nobara-signed builds of the installed NVIDIA,
  xone, xpad-noone and OpenRazer drivers are installed for it, and none of its
  out-of-tree modules is unsigned. The default is chosen when a kernel is
  installed and on every boot, after the Nobara updater confirmed its update
- nobara-eac-enroll: --check only needs the Nobara CA, the DKMS and akmods
  keys are for the normal kernel; add --list
- Drop EAC_ENTRIES: remove kernel-eac instead

* Sun Nov 01 2026 GloriousEggroll <gloriouseggroll@gmail.com> - 1.0-4
- Add EAC_ENTRIES to /etc/sysconfig/nobara-eac. EAC_ENTRIES=no keeps only
  the normal boot entry for every kernel; EAC_DEFAULT=no still adds the
  EAC entry and only keeps it from being the default

* Fri Oct 30 2026 GloriousEggroll <gloriouseggroll@gmail.com> - 1.0-3
- nobara-eac-enroll: don't ask for an immediate restart, so the keys are
  confirmed on the restart that installs the system update
- Fix the Secure Boot check in auto mode, which read the wrong EFI variable
  and never made the EAC entry the default
- Mark EAC entries with "[EAC] " at the start of the title, where long
  release names can't hide it
- Write the boot entries with mode 0644, like 20-grub.install
- Only add EAC entries for kernels built for EAC (linux.nobara SBAT entry);
  older kernels are not signed and keep their plain entry

* Fri Oct 30 2026 GloriousEggroll <gloriouseggroll@gmail.com> - 1.0-2
- Add nobara-eac-enroll to enroll the Nobara CA and the local DKMS and akmods
  module signing keys as MOKs
- auto mode: EAC is the default only once those keys are enrolled
- Re-check the boot entries on every boot with nobara-eac.service

* Fri Oct 30 2026 GloriousEggroll <gloriouseggroll@gmail.com> - 1.0-1
- Initial package
