%global appdatacommit r44.4158bd4

Name:           gpu-screen-recorder-gtk
Version:        5.8.1
Release:        1%{dist}
Summary:        A shadowplay-like screen recorder for Linux. The fastest screen recorder for Linux.

License:        GPL-3.0-or-later

URL:            https://git.dec05eba.com/%{name}/about

Source0:        https://dec05eba.com/snapshot/%{name}.git.%{version}.tar.gz
Source1:        https://dec05eba.com/snapshot/gpu-screen-recorder-appdata.git.%{appdatacommit}.tar.gz

BuildRequires:  gcc
BuildRequires:  (gcc-g++ or gcc-c++)
BuildRequires:  meson
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  (pkgconfig(ayatana-appindicator3-0.1) or libayatana-appindicator-gtk3-devel or libayatana-appindicator3-dev)
BuildRequires:  desktop-file-utils
Requires:       gpu-screen-recorder

%description
Shadowplay like screen recorder for Linux. This package exposes the GTK3 UI.


%prep
%autosetup -c


%build
%meson
%meson_build

%install
install -Dm644 %{SOURCE1} %{buildroot}%{_datadir}/metainfo/com.dec05eba.gpu_screen_recorder.appdata.xml
%meson_install

%check
%meson_test

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_datadir}/applications/com.dec05eba.gpu_screen_recorder.desktop
%{_datadir}/metainfo/com.dec05eba.gpu_screen_recorder.appdata.xml
%{_datadir}/icons/hicolor/

%changelog
* Tue Sep 01 2026 LionHeartP <LionHeartP@proton.me> - 5.8.1-1
- Update to 5.8.1

* Thu Jul 16 2026 LionHeartP <LionHeartP@proton.me> - 5.8.0-1
- Update to 5.8.0

* Tue Dec 23 2025 LionHeartP <LionHeartP@proton.me> - 5.7.9-1
- Update to 5.7.9

* Fri Sep 19 2025 LionHeartP <LionHeartP@proton.me> - 5.7.8-1
- Port to Nobara
- Update to 5.7.8

* Thu Sep 05 2024 Brycen G <brycengranville@outlook.com> - 4.3.3-3
- Update to 4.3.3
