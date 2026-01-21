Name:           gpu-screen-recorder
Version:        5.12.1
Release:        1%{dist}
Summary:        A shadowplay-like screen recorder for Linux. The fastest screen recorder for Linux.

License:        GPL-3.0-or-later

URL:            https://git.dec05eba.com/%{name}/about

Source:         https://dec05eba.com/snapshot/%{name}.git.%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  (gcc-g++ or gcc-c++)
BuildRequires:  pkgconfig(libva)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libva-drm)
BuildRequires:  vulkan-headers
BuildRequires:  pkgconfig(libcap)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-egl)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  (ffmpeg-free-devel or ffmpeg-devel) 
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xdamage)
BuildRequires:  pkgconfig(xcomposite)
BuildRequires:  pkgconfig(xrandr)
BuildRequires:  pkgconfig(xfixes)
BuildRequires:  meson
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(libspa-0.2)
BuildRequires:  pkgconfig(libglvnd)
Requires(post): libcap


%description
Shadowplay like screen recorder for Linux. It is the fastest screen recorder for Linux.


%prep
%autosetup -c

%build
%meson -Dcapabilities=false
%meson_build


%install
%meson_install

%check
%meson_test

%post
setcap cap_sys_admin+ep %{_bindir}/gsr-kms-server

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_bindir}/gsr-kms-server
%{_includedir}/gsr/plugin.h
%{_prefix}/lib/systemd/user/%{name}.service
%{_prefix}/lib/modprobe.d/gsr-nvidia.conf
%{_mandir}/man1/%{name}.1*
%{_mandir}/man1/gsr-kms-server.1*

%changelog
* Wed Jan 21 2026 LionHeartP <LionHeartP@proton.me> - 5.12.1-1
- Update to 5.12.1

* Sun Jan 18 2026 LionHeartP <LionHeartP@proton.me> - 5.12.0-1
- Update to 5.12.0

* Fri Jan 09 2026 LionHeartP <LionHeartP@proton.me> - 5.11.5-1
- Update to 5.11.5

* Sat Dec 27 2025 LionHeartP <LionHeartP@proton.me> - 5.11.2-1
- Update to 5.11.2

* Thu Dec 25 2025 LionHeartP <LionHeartP@proton.me> - 5.11.1-1
- Update to 5.11.1

* Mon Dec 08 2025 LionHeartP <LionHeartP@proton.me> - 5.10.2-1
- Update to 5.10.2

* Fri Dec 05 2025 LionHeartP <LionHeartP@proton.me> - 5.9.4-1
- Update to 5.9.4

* Wed Nov 26 2025 LionHeartP <LionHeartP@proton.me> - 5.9.3-1
- Update to 5.9.3

* Sun Nov 23 2025 LionHeartP <LionHeartP@proton.me> - 5.9.2-1
- Update to 5.9.2

* Fri Nov 21 2025 LionHeartP <LionHeartP@proton.me> - 5.9.1-1
- Update to 5.9.1

* Sat Nov 15 2025 LionHeartP <LionHeartP@proton.me> - 5.8.2-1
- Update to 5.8.2

* Mon Nov 03 2025 LionHeartP <LionHeartP@proton.me> - 5.8.1-1
- Update to 5.8.1

* Mon Oct 06 2025 LionHeartP <LionHeartP@proton.me> - 5.8.0-1
- Update to 5.8.0

* Wed Oct 01 2025 LionHeartP <LionHeartP@proton.me> - 5.7.4-1
- Update to 5.7.4

* Sun Sep 28 2025 LionHeartP <LionHeartP@proton.me> - 5.7.3-1
- Update to 5.7.3

* Wed Sep 24 2025 LionHeartP <LionHeartP@proton.me> - 5.7.2-1
- Update to 5.7.2

* Sun Sep 21 2025 LionHeartP <LionHeartP@proton.me> - 5.7.0-1
- Update to 5.7.0

* Sat Sep 13 2025 LionHeartP <LionHeartP@proton.me> - 5.6.8-1
- Update to 5.6.8

* Sun Sep 07 2025 LionHeartP <LionHeartP@proton.me> - 5.6.7-1
- Update to 5.6.7

* Mon Aug 25 2025 LionHeartP <LionHeartP@proton.me> - 5.6.6-1
- Update to 5.6.6

* Sat Aug 09 2025 LionHeartP <LionHeartP@proton.me> - 5.6.5-1
- Update to 5.6.5

* Fri Aug 01 2025 LionHeartP <LionHeartP@proton.me> - 5.6.4-1
- Update to 5.6.4

* Mon Jul 21 2025 LionHeartP <LionHeartP@proton.me> - 5.6.3-1
- Update to 5.6.3

* Mon Jun 30 2025 LionHeartP <LionHeartP@proton.me> - 5.6.1-1
- Update to 5.6.1

* Sat Jun 28 2025 LionHeartP <LionHeartP@proton.me> - 5.6.0-1
- Update to 5.6.0

* Mon Jun 23 2025 LionHeartP <LionHeartP@proton.me> - 5.5.10-1
- Update to 5.5.10

* Thu Jun 12 2025 LionHeartP <LionHeartP@proton.me> - 5.5.9-1
- Update to 5.5.9

* Tue Jun 10 2025 LionHeartP <LionHeartP@proton.me> - 5.5.8-1
- Update to 5.5.8

* Sat Jun 7 2025 LionHeartP <LionHeartP@proton.me> - 5.5.7-1
- Update to 5.5.7

* Sat Jun 7 2025 LionHeartP <LionHeartP@proton.me> - 5.5.6-1
- Update to 5.5.6
- Switch to versioned source instead of snapshots
- Remove cap_sys_nice as per upstream change

* Wed Jun 4 2025 LionHeartP <LionHeartP@proton.me> - 5.5.5-1
- Update to 5.5.5
- Remove Epoch in preparation to ship for Nobara

* Tue Mar 18 2025 Brycen G <brycengranville@outlook.com> - 5.3.3-1
- Update to 5.3.3

* Thu Sep 05 2024 Brycen G <brycengranville@outlook.com> - 4.3.3-3
- Update to 4.3.3
