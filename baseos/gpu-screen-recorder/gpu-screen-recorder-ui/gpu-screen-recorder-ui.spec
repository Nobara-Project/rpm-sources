Name:           gpu-screen-recorder-ui
Version:        1.12.0
Release:        1%{dist}
Summary:        A shadowplay-like screen recorder for Linux. The fastest screen recorder for Linux.
License:        GPL-3.0-or-later
Source:         https://dec05eba.com/snapshot/%{name}.git.%{version}.tar.gz
URL:            https://git.dec05eba.com/%{name}/about

BuildRequires:  desktop-file-utils
BuildRequires:  gcc
BuildRequires:  (gcc-g++ or gcc-c++)
BuildRequires:  meson
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xcomposite)
BuildRequires:  pkgconfig(xrandr)
BuildRequires:  pkgconfig(xfixes)
BuildRequires:  pkgconfig(xi)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(xrender)
BuildRequires:  pkgconfig(libglvnd)
BuildRequires:  pkgconfig(xcursor)
BuildRequires:  pkgconfig(libpulse-simple)
BuildRequires:  pkgconfig(wayland-scanner)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(pango)
BuildRequires:  pkgconfig(pangocairo)
BuildRequires:  kernel-headers
Requires:       gpu-screen-recorder
Requires:       gpu-screen-recorder-notification
Requires:	pango
Requires(post): libcap

%description
A fullscreen overlay UI for GPU Screen Recorder in the style of ShadowPlay.


%prep
%autosetup -c


%build
%meson -Dcapabilities=false
%meson_build

%install
%meson_install

# Say it with me. I will not violate Fedora packaging guidelines.
rm -rf %{_buildroot}%{_datadir}/gsr-ui/fonts

%check
%meson_test

%preun
%systemd_user_preun %{name}.service

%files
%license LICENSE
%doc README.md
%caps(cap_setuid=ep) %{_bindir}/gsr-global-hotkeys
%{_bindir}/gsr*
%{_datadir}/applications/gpu-screen-recorder.desktop
%{_datadir}/icons/hicolor/*/apps/gpu-screen-recorder.png
%{_datadir}/gsr-ui

%changelog
* Tue May 12 2026 LionHeartP <LionHeartP@proton.me> - 1.12.0-1
- Update to 1.12.0

* Sat May 02 2026 LionHeartP <LionHeartP@proton.me> - 1.11.7-1
- Update to 1.11.7

* Thu Apr 23 2026 LionHeartP <LionHeartP@proton.me> - 1.11.5-1
- Update to 1.11.5
- Correctly setcap for global keybinds
- Add temporary %preun macto to get rid of deprecated systemd service 

* Sun Apr 19 2026 LionHeartP <LionHeartP@proton.me> - 1.11.4-1
- Update to 1.11.4

* Sat Apr 18 2026 LionHeartP <LionHeartP@proton.me> - 1.11.2-1
- Update to 1.11.2

* Wed Mar 25 2026 LionHeartP <LionHeartP@proton.me> - 1.10.9-1
- Update to 1.10.9

* Thu Feb 12 2026 LionHeartP <LionHeartP@proton.me> - 1.10.7-1
- Update to 1.10.7

* Wed Jan 28 2026 LionHeartP <LionHeartP@proton.me> - 1.10.6-1
- Update to 1.10.6

* Sat Jan 24 2026 LionHeartP <LionHeartP@proton.me> - 1.10.4-1
- Update to 1.10.4
- Add new dbus dependency

* Wed Jan 21 2026 LionHeartP <LionHeartP@proton.me> - 1.10.2-1
- Update to 1.10.2

* Tue Jan 20 2026 LionHeartP <LionHeartP@proton.me> - 1.10.1-1
- Update to 1.10.1

* Fri Jan 09 2026 LionHeartP <LionHeartP@proton.me> - 1.9.3-1
- Update to 1.9.3
- Add new dependency and files

* Sat Dec 27 2025 LionHeartP <LionHeartP@proton.me> - 1.9.1-1
- Update to 1.9.1

* Thu Dec 25 2025 LionHeartP <LionHeartP@proton.me> - 1.9.0-1
- Update to 1.9.0

* Mon Dec 08 2025 LionHeartP <LionHeartP@proton.me> - 1.8.3-1
- Update to 1.8.3

* Sat Nov 29 2025 LionHeartP <LionHeartP@proton.me> - 1.8.2-1
- Update to 1.8.2

* Fri Nov 21 2025 LionHeartP <LionHeartP@proton.me> - 1.8.1-1
- Update to 1.8.1

* Mon Nov 10 2025 LionHeartP <LionHeartP@proton.me> - 1.8.0-1
- Update to 1.8.0

* Mon Nov 03 2025 LionHeartP <LionHeartP@proton.me> - 1.7.9-1
- Update to 1.7.9

* Sat Oct 04 2025 LionHeartP <LionHeartP@proton.me> - 1.7.8-1
- Update to 1.7.8

* Sun Sep 28 2025 LionHeartP <LionHeartP@proton.me> - 1.7.7-1
- Update to 1.7.7

* Sun Sep 21 2025 LionHeartP <LionHeartP@proton.me> - 1.7.6-1
- Update to 1.7.6

* Sun Sep 07 2025 LionHeartP <LionHeartP@proton.me> - 1.7.5-1
- Update to 1.7.5

* Sat Aug 09 2025 LionHeartP <LionHeartP@proton.me> - 1.7.2-1
- Update to 1.7.2

* Tue Jul 22 2025 LionHeartP <LionHeartP@proton.me> - 1.7.1-1
- Update to 1.7.1

* Mon Jul 21 2025 LionHeartP <LionHeartP@proton.me> - 1.7.0-1
- Update to 1.7.0

* Thu Jul 10 2025 LionHeartP <LionHeartP@proton.me> - 1.6.9-1
- Update to 1.6.9

* Thu Jun 5 2025 LionHeartP <LionHeartP@proton.me> - 1.6.7-1
- Update to 1.6.7
- Switch to versioned source

* Wed Jun 4 2025 LionHeartP <LionHeartP@proton.me> - 1.6.6-1
- Update to 1.6.6
- Remove Epoch in preparation to ship for Nobara

* Fri Dec 13 2024 Brycen G <brycengranville@outlook.com> - r142.4c83972
- Initial package
