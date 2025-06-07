Name:           gpu-screen-recorder
Version:        5.5.7
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
%{_bindir}/gpu-screen-recorder
%{_bindir}/gsr-kms-server
%{_bindir}/gsr-dbus-server
/usr/lib/systemd/user/%{name}.service
/usr/lib/modprobe.d/gsr-nvidia.conf


%changelog
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
