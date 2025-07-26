%global 	SHA256SUM0 c1af504fa797be6d127804257874be1850ddafab0d6f0fd06afc0eed68dd8675
%define         appid com.vysp3r.ProtonPlus

Name:           protonplus
Version:        0.5.12
Release:        1%{?dist}
Summary:        Simple and powerful manager for Wine, Proton, DXVK and VKD3D

ExclusiveArch:  x86_64
License:        GPL-3.0-or-later
URL:            https://github.com/vysp3r/ProtonPlus
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  desktop-file-utils
BuildRequires:  fdupes
BuildRequires:  gettext
BuildRequires:  git-core
BuildRequires:  libappstream-glib
BuildRequires:  meson >= 1.0.0
BuildRequires:  ninja-build
BuildRequires:  vala
BuildRequires:  pkgconfig(gee-0.8)
BuildRequires:  pkgconfig(gtk4)
BuildRequires:  pkgconfig(json-glib-1.0)
BuildRequires:  pkgconfig(libadwaita-1) >= 1.5.0
BuildRequires:  pkgconfig(libarchive)
BuildRequires:  pkgconfig(libsoup-3.0)

# Need for TLS support
Requires:       glib-networking

Obsoletes:  	protonup-qt
Obsoletes:	protonplus-next

%description
ProtonPlus is a simple and powerful manager for:
 - Wine
 - Proton
 - DXVK
 - VKD3D
 - Several other runners

Supports Steam, Lutris, Heroic and Bottles.

%prep
echo "%SHA256SUM0 %{SOURCE0}" | sha256sum -c -
%autosetup -n ProtonPlus-%{version}

%build
%meson
%meson_build

%install
%meson_install
%find_lang %{appid}
# create symlinks for icons
# fix rpmlint W: files-duplicate
%fdupes -s %{buildroot}%{_datadir}/icons/hicolor

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{appid}.desktop
appstream-util validate-relax --nonet \
    %{buildroot}%{_datadir}/metainfo/%{appid}.metainfo.xml

%files -f %{appid}.lang
%license LICENSE.md
%doc README.md CONTRIBUTING.md CODE_OF_CONDUCT.md SECURITY.md
%{_bindir}/protonplus
%{_datadir}/metainfo/%{appid}.metainfo.xml
%{_datadir}/applications/%{appid}.desktop
%{_datadir}/glib-2.0/schemas/%{appid}.gschema.xml
%{_datadir}/icons/hicolor/*/apps/%{appid}.*


%changelog
* Sat Jul 26 2025 LionHeartP <LionHeartP@proton.me> - 0.5.12-1
- new upstream version v0.5.12

* Thu Jul 24 2025 LionHeartP <LionHeartP@proton.me> - 0.5.11-1
- new upstream version v0.5.11

* Wed Jul 16 2025 LionHeartP <LionHeartP@proton.me> - 0.5.10-1
- new upstream version v0.5.10

* Fri Jul 04 2025 LionHeartP <LionHeartP@proton.me> - 0.5.8-1
- new upstream version v0.5.8
- rename to protonplus and obsolete protonplus-next to match upstream

* Sat Jun 28 2025 LionHeartP <LionHeartP@proton.me> - 0.5.6-1
- new upstream version v0.5.6

* Wed Jun 11 2025 LionHeartP <LionHeartP@proton.me> - 0.5.2-1
- new upstream version v0.5.2
- refactor .spec file

* Mon Apr 14 2025 LionHeartP <LionHeartP@proton.me> - 0.4.27-1
- new upstream version v0.4.27

* Mon May 27 2024 Wesley Gimenes <wehagy@proton.me> - 0.4.10-1
- new upstream version v0.4.10

* Wed Apr 10 2024 Wesley Gimenes <wehagy@proton.me> - 0.4.9-2
- build: rebuild for fedora 40 release

* Sun Dec 17 2023 Wesley Gimenes <wehagy+github@gmail.com> - 0.4.9-1
- new upstream version v0.4.9

* Sun Dec 17 2023 Wesley Gimenes <wehagy+github@gmail.com> - 0.4.8-1
- new upstream version v0.4.8

* Sun Dec 17 2023 Wesley Gimenes <wehagy+github@gmail.com> - 0.4.7.2-1
- style: fixed indentation
- new upstream version v0.4.7-2

* Sun Dec 17 2023 Wesley Gimenes <wehagy+github@gmail.com> - 0.4.7.1-1
- fix: change upstream version dash to dot
- fix: %%autosetup use upstream versioning
- new upstream version v0.4.7-1

* Sat Dec 16 2023 Wesley Gimenes <wehagy+github@gmail.com> - 0.4.7-1
- tighten dependencies
- removed unused files to accomodate new version
- new upstream version v0.4.7

* Sat Dec 16 2023 Wesley Gimenes <wehagy+github@gmail.com> - 0.4.6-3
- fix: incorrect day of week in changelog

* Thu Nov 09 2023 Wesley Gimenes <wehagy+github@gmail.com> - 0.4.6-3
- rebuild for fedora 39 release
- rename global variable project to owner
- add license to source of the specfile
- add SPDX license header

* Tue Sep 05 2023 Wesley H. Gimenes <wehagy+github@gmail.com> - 0.4.6-2
- rebuild v0.4.6-2 because of the file below
- fix: rename prontonplus-next.rpmlintrc to protonplus.rpmlintrc
- fix: change %%define to %%global
- fix: macros in changelog
- changed legacy license format to SPDX
- fix: W: dangerous-command-in-%%postun rm
- fix: W: dangerous-command-in-%%post ln
- fix: general improvements
- fix: E: standard-dir-owned-by-package
- fix: W: file-not-in-%%lang
- fix: W: no-manual-page-for-binary 
- fix: W: files-duplicate

* Mon Sep 04 2023 Wesley H. Gimenes <wehagy+github@gmail.com> - 0.4.6-2
- fix: use-of-RPM_SOURCE_DIR 

* Mon Sep 04 2023 Wesley H. Gimenes <wehagy+github@gmail.com> - 0.4.6-1
- First Release
