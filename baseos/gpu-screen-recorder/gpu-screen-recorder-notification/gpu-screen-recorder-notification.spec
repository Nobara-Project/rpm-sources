Name:           gpu-screen-recorder-notification
Version:        1.3.3
Release:        1%{dist}
Summary:        A shadowplay-like screen recorder for Linux. The fastest screen recorder for Linux.
License:        GPL-3.0-or-later

URL:            https://git.dec05eba.com/%{name}/about

Source:         https://dec05eba.com/snapshot/%{name}.git.%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  (gcc-g++ or gcc-c++)
BuildRequires:  meson
BuildRequires:  pkgconfig(pango)
BuildRequires:  pkgconfig(pangocairo)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(xrandr)
BuildRequires:  pkgconfig(xrender)
BuildRequires:  pkgconfig(libglvnd)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-egl)
BuildRequires:  pkgconfig(wayland-scanner)
Requires:       pango

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
rm -rf %{_buildroot}%{_datadir}/gsr-notify/fonts

%check
%meson_test

%files
%license LICENSE
%doc README.md
%{_bindir}/gsr*
%{_datadir}/gsr-notify

%changelog
* Fri Jul 03 2026 LionHeartP <LionHeartP@proton.me> - 1.3.3-1
- Update to 1.3.3

* Tue Jun 02 2026 LionHeartP <LionHeartP@proton.me> - 1.3.1-1
- Update to 1.3.1

* Tue May 12 2026 LionHeartP <LionHeartP@proton.me> - 1.3.0-1
- Update to 1.3.0

* Sat May 02 2026 LionHeartP <LionHeartP@proton.me> - 1.2.3-1
- Update to 1.2.3

* Sat Apr 18 2026 LionHeartP <LionHeartP@proton.me> - 1.2.1-1
- Update to 1.2.1

* Thu Feb 12 2026 LionHeartP <LionHeartP@proton.me> - 1.1.1-1
- Update to 1.1.1

* Tue Sep 30 2025 LionHeartP <LionHeartP@proton.me> - 1.1.0-1
- Update to 1.1.0

* Sun Sep 28 2025 LionHeartP <LionHeartP@proton.me> - 1.0.9-1
- Update to 1.0.9

* Sat Aug 09 2025 LionHeartP <LionHeartP@proton.me> -  1.0.8-1
- Update to 1.0.8
- Switch to versioned source instead of snapshots

* Wed Jun 4 2025 LionHeartP <LionHeartP@proton.me> -  1.0.7-1
- Update to 1.0.7
- Remove Epoch in preparation to ship for Nobara

* Fri Dec 13 2024 Brycen G <brycengranville@outlook.com> - r43.b03e4cd
- Initial package
