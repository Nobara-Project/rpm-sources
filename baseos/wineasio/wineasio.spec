%global debug_package    %{nil}
%global _lto_cflags      %{nil}
%global staging_dir	 /opt/wine-staging/lib64

Name:           wineasio
Version:        1.3.0
Release:        %autorelease -b5
Summary:        ASIO to Pipewire's JACK driver for WINE
License:        LGPLv2.1 and GPL-2.0
URL:            https://github.com/wineasio/wineasio
Source0:        %{URL}/releases/download/v%{version}/wineasio-%{version}.tar.gz

Patch: 		fedora.patch

BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  winehq-staging wine-staging-devel

ExcludeArch:    %{ix86}
Requires:       pipewire-jack-audio-connection-kit
Requires:       wine-staging
Requires:       python3-pyqt6
Requires: 	realtime-setup

%description
WineASIO provides an ASIO to JACK driver for WINE. ASIO is the most common
Windows low-latency driver, so is commonly used in audio workstation programs.
You can, for example, use with FLStudio under GNU/Linux systems (together
with JACK).

This version is built against Pipewire's JACK implementation.

%prep
%autosetup -p1 -n wineasio-%{version}

%build
%make_build 64

%install
# create lib dirs
install -d -m0755 %{buildroot}%{_libdir}/wine/x86_64-windows

# install wine-register
install -D -m 0755 wineasio-register %{buildroot}%{_bindir}/wineasio-register

# install libs
install -D -m 0755 build64/wineasio64.dll %{buildroot}%{staging_dir}/wine/x86_64-windows/wineasio64.dll
install -D -m 0755 build64/wineasio64.dll.so %{buildroot}%{staging_dir}/wine/x86_64-unix/wineasio64.dll.so

# install gui
pushd gui
%make_install
popd

%files
%defattr(-,root,root)
%license COPYING.LIB COPYING.GUI
%doc README.md
%attr(0755,root,root)        %{_bindir}/wineasio-register
%attr(0755,root,root)        %{_bindir}/wineasio-settings
%attr(0755,root,root)  %dir  %{_datadir}/wineasio
%attr(0644,root,root)        %{_datadir}/wineasio/*.py
%attr(0755,root,root)        %{staging_dir}/wine/x86_64-windows/wineasio64.dll
%attr(0755,root,root)        %{staging_dir}/wine/x86_64-unix/wineasio64.dll.so

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%changelog
* Sat Nov 08 2025 LionHeartP <LionHeartP@proton.me> - 1.3.0-5
- remove Conflicts with itself (oops)

* Fri Nov 07 2025 LionHeartP <LionHeartP@proton.me> - 1.3.0-4
- adjust for wine-staging
- add realtime-setup dep
- rename to wineasio

* Fri Nov 07 2025 LionHeartP <LionHeartP@proton.me> - 1.3.0-3
- add patch for wow64

* Fri Nov 07 2025 LionHeartP <LionHeartP@proton.me> - 1.3.0-2
- adjust spec for Nobara Linux

* Fri Nov 07 2025 Patrick Laimbock <patrick@laimbock.com> - 1.3.0-1
- initial release for F43
- update to version 1.3.0

* Sun Apr 20 2025 Patrick Laimbock <patrick@laimbock.com> - 1.2.1-1
- update to git rev 652964155dcee005078c7cb652656e8a0b995186
- rebuild against wine-9.21 on F42

* Fri Nov 15 2024 Patrick Laimbock <patrick@laimbock.com> - 1.2.0-9
- rebuild against wine-9.4 on F41

* Sat Oct 26 2024 Patrick Laimbock <patrick@laimbock.com> - 1.2.0-8
- rebuild against wine-9.20

* Mon May 06 2024 Patrick Laimbock <patrick@laimbock.com> - 1.2.0-7
- since requiring a specific wine version makes up/downgrading difficult
- let's revert back to requiring 9.4 or later

* Sun May 05 2024 Patrick Laimbock <patrick@laimbock.com> - 1.2.0-6
- build/require wine-9.8 from the wine-tkg-dev copr

* Mon Apr 29 2024 Patrick Laimbock <patrick@laimbock.com> - 1.2.0-5
- rebuild against wine-9.4

* Sat Feb 03 2024 Patrick Laimbock <patrick@laimbock.com> - 1.2.0-4
- rebuild against wine-9.1

* Sat Dec 16 2023 Patrick Laimbock <patrick@laimbock.com> - 1.2.0-3
- rebuild against wine-9.0(-rc2)

* Sun Oct 29 2023 Patrick Laimbock <patrick@laimbock.com> - 1.2.0-2
- test build: require wine >= 8.4 because of an Ableton issue with 8.18

* Sun Oct 29 2023 Patrick Laimbock <patrick@laimbock.com> - 1.2.0-1
- update to version 1.2.0
- include the gui in the main package

* Mon May 29 2023 Patrick Laimbock <patrick@laimbock.com> - 1.1.0-21
- rebuild against wine-8.9.1 from the wine-tkg copr

* Mon May 15 2023 Patrick Laimbock <patrick@laimbock.com> - 1.1.0-20
- rebuild against wine-8.8

* Sat Apr 29 2023 Patrick Laimbock <patrick@laimbock.com> - 1.1.0-19
- rebuild against wine-8.7

* Wed Apr 19 2023 Patrick Laimbock <patrick@laimbock.com> - 1.1.0-18
- rebuild against wine-8.6

* Tue Apr 04 2023 Patrick Laimbock <patrick@laimbock.com> - 1.1.0-17
- rebuild against wine-8.5

* Thu Mar 30 2023 Patrick Laimbock <patrick@laimbock.com> - 1.1.0-16
- rebuild against wine-8.4

* Thu Feb 23 2023 Patrick Laimbock <patrick@laimbock.com> - 1.1.0-15
- rebuild against wine-8.2

* Wed Jan 25 2023 Patrick Laimbock <patrick@laimbock.com> - 1.1.0-14
- rebuild against wine-8.0
- rebuild against latest pipewire

* Sun Jan 22 2023 Patrick Laimbock <patrick@laimbock.com> - 1.1.0-13
- rebuild against wine-8.0rc5

* Thu Jan 12 2023 Patrick Laimbock <patrick@laimbock.com> - 1.1.0-12
- rebuild against wine-8.0rc4
- disable patch

* Thu Jan 12 2023 Patrick Laimbock <patrick@laimbock.com> - 1.1.0-11
- add patch from https://github.com/TobiasKozel/wineasio/commit/c4bcac2a594b2d3ef3bc64c39b20d05b5e4ce87f

* Mon Jan 02 2023 Patrick Laimbock <patrick@laimbock.com> - 1.1.0-10
- build against wine-8.0

* Thu Nov 03 2022 Patrick Laimbock <patrick@laimbock.com> - 1.1.0-9
- build against wine-7.20

* Sat Oct 01 2022 Patrick Laimbock <patrick@laimbock.com> - 1.1.0-8
- build against wine-7.18
=
* Sat Sep 10 2022 Patrick Laimbock <patrick@laimbock.com> - 1.1.0-7
- build against wine-7.17

* Sun Aug 28 2022 Patrick Laimbock <patrick@laimbock.com> - 1.1.0-6
- build against wine-7.16

* Sun Aug 14 2022 Patrick Laimbock <patrick@laimbock.com> - 1.1.0-5
- build against wine-7.15

* Sat Jul 30 2022 Patrick Laimbock <patrick@laimbock.com> - 1.1.0-4
- build against wine-7.14

* Sun Jul 10 2022 Patrick Laimbock <patrick@laimbock.com> - 1.1.0-3
- build against wine-7.13

* Sun Jul 10 2022 Patrick Laimbock <patrick@laimbock.com> - 1.1.0-2
- build against wine-7.12
- disable LTO

* Sun Feb 27 2022 Patrick Laimbock <patrick@laimbock.com> - 1.1.0-1
- update to version 1.1.0
- build against wine-7.3

* Sat Jan 01 2022 Patrick Laimbock <patrick@laimbock.com> - 1.1.0-0.3
- build against wine-7.0rc3

* Sun Dec 05 2021 Patrick Laimbock <patrick@laimbock.com> - 1.1.0-0.2
- build against wine-6.23

* Thu Nov 25 2021 Patrick Laimbock <patrick@laimbock.com> - 1.1.0-0.1
- update to version 1.1.0
- build against wine-6.22

* Thu Oct 07 2021 Patrick Laimbock <patrick@laimbock.com> - 1.0.1-0.9
- build against wine-6.18
- build against pipewire-0.3.38

* Sat Sep 11 2021 Patrick Laimbock <patrick@laimbock.com> - 1.0.1-0.8
- build against wine-6.17
- build against pipewire-0.3.35

* Sat Aug 28 2021 Patrick Laimbock <patrick@laimbock.com> - 1.0.1-0.7
- build against wine-6.16
- build against pipewire-0.3.34

* Sat Aug 14 2021 Patrick Laimbock <patrick@laimbock.com> - 1.0.1-0.6
- build against wine-6.15
- build against pipewire-0.3.33

* Sun Aug 01 2021 Patrick Laimbock <patrick@laimbock.com> - 1.0.1-0.5
- build against wine-6.14

* Mon Jul 26 2021 Patrick Laimbock <patrick@laimbock.com> - 1.0.1-0.4
- enable wineasio-pr-17.patch again as disabling it did not fix anything

* Mon Jul 26 2021 Patrick Laimbock <patrick@laimbock.com> - 1.0.1-0.4
- use the proper wine locations to install the dll.so to

* Mon Jul 26 2021 Patrick Laimbock <patrick@laimbock.com> - 1.0.1-0.3
- disable wineasio-pr-17.patch

* Mon Jul 26 2021 Patrick Laimbock <patrick@laimbock.com> - 1.0.1-0.2
- fix 32bit Requires (remove regular JACK)

* Mon Jul 26 2021 Patrick Laimbock <patrick@laimbock.com> - 1.0.1-0.1
- wineasio built against Pipewire's JACK implementation

