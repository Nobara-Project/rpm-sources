Name:           gpu-screen-recorder-ui
Version:        1.8.0
Release:        1%{dist}
Summary:        A shadowplay-like screen recorder for Linux. The fastest screen recorder for Linux.
License:        GPL-3.0-or-later
Source:         https://dec05eba.com/snapshot/%{name}.git.%{version}.tar.gz
URL:            https://git.dec05eba.com/%{name}/about

BuildRequires:  gcc
BuildRequires:  (gcc-g++ or gcc-c++)
BuildRequires:  meson
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xcomposite)
BuildRequires:  pkgconfig(xrandr)
BuildRequires:  pkgconfig(xfixes)
BuildRequires:  pkgconfig(xi)
BuildRequires:  pkgconfig(xrender)
BuildRequires:  pkgconfig(libglvnd)
BuildRequires:  pkgconfig(xcursor)
BuildRequires:  pkgconfig(libpulse-simple)
BuildRequires:  pkgconfig(wayland-scanner)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  kernel-headers
Requires:       gpu-screen-recorder
Requires:       gpu-screen-recorder-notification
Requires:       (google-noto-sans-fonts or noto-sans)
Requires(post): libcap

%description
A fullscreen overlay UI for GPU Screen Recorder in the style of ShadowPlay.


%prep
%autosetup -c


%build
%meson
%meson_build

%install
%meson_install

# Say it with me. I will not violate Fedora packaging guidelines.
rm -rf %{_buildroot}%{_datadir}/gsr-ui/fonts

%check
%meson_test

%post
setcap cap_setuid+ep %{_bindir}/gsr-global-hotkeys

%files
%license LICENSE
%doc README.md
%{_bindir}/gsr*
%{_datadir}/gsr-ui
%{_exec_prefix}/lib/systemd/user/%{name}.service

%changelog
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
