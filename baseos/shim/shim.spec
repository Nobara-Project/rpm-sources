# this is to make us only expand %%{dist} if we're on a modularity build.
# it's 2 macros make vim's \c not put a brace at the end of the changelog.
%global _dist %{expand:%{?_module_build:%%{?dist}}}
%global dist %{expand:%%{_dist}}

# THIS IS A COMPLETE HACK
# WE USE THE FILES FROM FEDORA'S PRECOMPILED SHIM-UNSIGNED AND SHIM RPMS AND RE-PACKAGE THEM
# WE DO THIS TO RETAIN SECUREBOOT COMPATIBILITY
# WE ALSO USE OLDER VERSION 15.4 DUE TO THIS BUG WHICH PREVENTS SOME OLD SYSTEMS FROM BOOTING:
# https://bugzilla.redhat.com/show_bug.cgi?id=2113005
# THE VERSION 15.6-X IS JUST FOR VERSION DEPENDENCY COMPATIBILITY

Name:		shim-x64
Version:	15.6
Release:	4%{?dist}
Summary:	First-stage UEFI bootloader
License:	BSD
URL:		https://github.com/rhboot/shim/
Source0:	fedora-presigned-15.4.tar.gz

ExclusiveArch:	%{efi}
# but we don't build a .i686 package, just a shim-ia32.x86_64 package
ExcludeArch:	%{ix86}
# but we don't build a .arm package, just a shim-arm.aarch64 package
ExcludeArch:	%{arm}

%global desc \
Initial UEFI bootloader that handles chaining to a trusted full bootloader \
under secure boot environments. This package contains the version signed by \
the UEFI signing service.

%description
%desc

%package -n shim-ia32
Summary:	First-stage UEFI bootloader
Provides:	shim-ia32

%description -n shim-ia32
%desc

%prep
tar -xf %{SOURCE0}

%install
mv boot %{buildroot}/
mv etc %{buildroot}/

%files
/boot/efi/EFI/BOOT/*64.*
/boot/efi/EFI/fedora/*64.*
/boot/efi/EFI/fedora/shim.efi
/etc/dnf/protected.d/shim.conf

%files -n shim-ia32
/boot/efi/EFI/BOOT/*32*.*
/boot/efi/EFI/fedora/*32.*
/etc/dnf/protected.d/shim.conf

%changelog
* Thu Jul 07 2022 Robbie Harwood <rharwood@redhat.com> - 15.6-2
- Update aarch64 (only) with relocation fixes
- Resolves: #2101248

* Wed Jun 15 2022 Peter Jones <pjones@redhat.com> - 15.6-1
- Update to shim-15.6
  Resolves: CVE-2022-28737

* Wed May 05 2021 Javier Martinez Canillas <javierm@redhat.com> - 15.4-5
- Bump release to build for F35

* Wed Apr 21 2021 Javier Martinez Canillas <javierm@redhat.com> - 15.4-4
- Fix handling of ignore_db and user_insecure_mode (pjones)
- Fix booting on pre-UEFI Macs (pjones)
- Fix mok variable storage allocation region (glin)
  Resolves: rhbz#1948432
- Fix the package version in the .sbat data (pjones)

* Tue Apr 06 2021 Peter Jones <pjones@redhat.com> - 15.4-3
- Mark signed shim packages as protected in dnf.
  Resolves: rhbz#1874541
- Conflict with older fwupd, but don't require it.
  Resolves: rhbz#1877751

* Tue Apr 06 2021 Peter Jones <pjones@redhat.com> - 15.4-2
- Update to shim 15.4
  - Support for revocations via the ".sbat" section and SBAT EFI variable
  - A new unit test framework and a bunch of unit tests
  - No external gnu-efi dependency
  - Better CI
  Resolves: CVE-2020-14372
  Resolves: CVE-2020-25632
  Resolves: CVE-2020-25647
  Resolves: CVE-2020-27749
  Resolves: CVE-2020-27779
  Resolves: CVE-2021-20225
  Resolves: CVE-2021-20233

* Tue Oct 02 2018 Peter Jones <pjones@redhat.com> - 15-8
- Build a -8 because I can't tag -7 into f30 for pretty meh reasons.

* Tue Oct 02 2018 Peter Jones <pjones@redhat.com> - 15-7
- Rebuild just because I'm dumb.

* Tue Oct 02 2018 Peter Jones <pjones@redhat.com> - 15-6
- Put the legacy shim.efi binary in the right subpackage
  Resolves: rhbz#1631989

* Fri May 04 2018 Peter Jones <pjones@redhat.com> - 15-5
- Rework the .spec to use efi-rpm-macros.

* Fri May 04 2018 Peter Jones <pjones@redhat.com> - 15-4
- Fix directory permissions to be 0700 on FAT filesystems

* Mon Apr 30 2018 Peter Jones <pjones@redhat.com> - 15-3
- Pick a release value that'll be higher than what's in F28.

* Mon Apr 30 2018 Peter Jones <pjones@redhat.com> - 15-1
- Fix BOOT*.CSV and update release to -1

* Tue Apr 24 2018 Peter Jones <pjones@redhat.com> - 15-0.1
- Update to shim 15.
- more reproduceable build
- better checking for bad linker output
- flicker-free console if there's no error output
- improved http boot support
- better protocol re-installation
- dhcp proxy support
- tpm measurement even when verification is disabled
- more reproducable builds
- measurement of everything verified through shim_verify()
- coverity and scan-build checker make targets
- misc cleanups

* Tue Mar 06 2018 Peter Jones <pjones@redhat.com> - 13-5
- Back off to the thing we had in 13-0.8 until I get new signatures.

* Wed Feb 28 2018 Peter Jones <pjones@redhat.com> - 13-4
- Fix an inverted test that crept in in the signing macro.  (Woops.)

* Wed Feb 28 2018 Peter Jones <pjones@redhat.com> - 13-2
- Pivot the shim-signed package to be here.

* Wed Nov 01 2017 Peter Jones <pjones@redhat.com> - 13-1
- Now with the actual signed 64-bit build of shim 13 for x64 as well.
- Make everything under /boot/efi be mode 0700, since that's what FAT will
  show anyway, so that rpm -V is correct.
  Resolves: rhbz#1508516

* Tue Oct 24 2017 Peter Jones <pjones@redhat.com> - 13-0.8
- Now with signed 32-bit x86 build.
  Related: rhbz#1474861

* Wed Oct 04 2017 Peter Jones <pjones@redhat.com> - 13-0.7
- Make /boot/efi/EFI/fedora/shim.efi still exist on aarch64 as well.
  Resolves: rhbz#1497854

* Tue Sep 19 2017 Peter Jones <pjones@redhat.com> - 13-0.6
- Fix binary format issue on Aarch64
  Resolves: rhbz#1489604

* Tue Sep 05 2017 Peter Jones <pjones@redhat.com> - 13-0.5
- Make /boot/efi/EFI/fedora/shim.efi still exist on x86_64, since some
  machines have boot entries that point to it.

* Tue Aug 29 2017 Peter Jones <pjones@redhat.com> - 13-0.4
- Make our provides not get silently ignore by rpmbuild...

* Fri Aug 25 2017 Peter Jones <pjones@redhat.com> - 13-0.3
- x64: use the new fbx64.efi and mm64.efi as fallback.efi and MokManager.efi
- Provide: "shim" in x64 and aa64 builds

* Thu Aug 24 2017 Peter Jones <pjones@redhat.com> - 13-0.2
- Obsolete old shim builds.

* Tue Aug 22 2017 Peter Jones <pjones@redhat.com> - 13-0.1
- Initial (partially unsigned) build for multi-arch support on x64/ia32.

* Thu Mar 23 2017 Petr Šabata <contyk@redhat.com> - 0.8-9
- Re-enable dist tag for module builds

* Tue Feb 17 2015 Peter Jones <pjones@redhat.com> - 0.8-8
- Don't dual-sign shim-%%{efidir}.efi either.
  Resolves: rhbz#1184765

* Tue Feb 17 2015 Peter Jones <pjones@redhat.com> - 0.8-8
- Require dbxtool

* Wed Dec 17 2014 Peter Jones <pjones@redhat.com> - 0.8-7
- Wrong -signed changes got built for aarch64 last time, for dumb reasons.
  Related: rhbz#1170289

* Fri Dec 05 2014 Peter Jones <pjones@redhat.com> - 0.8-6
- Rebuild once more so we can use a different -unsigned version on different
  arches (because we can't tag a newer build into aarch64 without an x86
  update to match.)
  Related: rhbz#1170289

* Wed Dec 03 2014 Peter Jones <pjones@redhat.com> - 0.8-5
- Rebuild for aarch64 path fixes
  Related: rhbz#1170289

* Thu Oct 30 2014 Peter Jones <pjones@redhat.com> - 0.8-2
- Remove the dist tag so people don't complain about what it says.

* Fri Oct 24 2014 Peter Jones <pjones@redhat.com> - 0.8-1
- Update to shim 0.8
  rhbz#1148230
  rhbz#1148231
  rhbz#1148232
- Handle building on aarch64 as well

* Fri Jul 18 2014 Peter Jones <pjones@redhat.com> - 0.7-2
- Don't do multi-signing; too many machines screw up verification.
  Resolves: rhbz#1049749

* Wed Nov 13 2013 Peter Jones <pjones@redhat.com> - 0.7-1
- Update to shim 0.7
  Resolves: rhbz#1023767

* Thu Oct 24 2013 Peter Jones <pjones@redhat.com> - 0.5-1
- Update to shim 0.5

* Thu Jun 20 2013 Peter Jones <pjones@redhat.com> - 0.4-1
- Provide a fallback for uninitialized Boot#### and BootOrder
  Resolves: rhbz#963359
- Move all signing from shim-unsigned to here
- properly compare our generated hash from shim-unsigned with the hash of
  the signed binary (as opposed to doing it manually)

* Fri May 31 2013 Peter Jones <pjones@redhat.com> - 0.2-4.4
- Re-sign to get alignments that match the new specification.
  Resolves: rhbz#963361

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2-4.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jan 02 2013 Peter Jones <pjones@redhat.com> - 0.2-3.3
- Add obsoletes and provides for earlier shim-signed packages, to cover
  the package update cases where previous versions were installed.
  Related: rhbz#888026

* Mon Dec 17 2012 Peter Jones <pjones@redhat.com> - 0.2-3.2
- Make the shim-unsigned dep be on the subpackage.

* Sun Dec 16 2012 Peter Jones <pjones@redhat.com> - 0.2-3.1
- Rebuild to provide "shim" package directly instead of just as a Provides:

* Sat Dec 15 2012 Peter Jones <pjones@redhat.com> - 0.2-3
- Also provide shim-fedora.efi, signed only by the fedora signer.
- Fix the fedora signature on the result to actually be correct.
- Update for shim-unsigned 0.2-3

* Mon Dec 03 2012 Peter Jones <pjones@redhat.com> - 0.2-2
- Initial build
