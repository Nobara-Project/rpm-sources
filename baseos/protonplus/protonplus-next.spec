# This specfile is licensed under:
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2023 Wesley Gimenes <wehagy+github@gmail.com>
# See %%{name}.spec.license for the full license text.

%global SHA256SUM0      3e52cb76646bf305b365db06e8057ac5956dd1ad8420b8db53c48c5b8d8ac641

%global provider        github
%global provider_tld    com
%global owner           vysp3r
%global repo            ProtonPlus
%global built_tag       v0.4.10
%global built_tag_strip %(b=%{built_tag}; echo ${b:1})
%global gen_version     %(b=%{built_tag_strip}; echo ${b/-/"."})

# com.vysp3r.ProtonPlus
%global flatpak_name    %{provider_tld}.%{owner}.%{repo}

# https://github.com/vysp3r/ProtonPlus
%global provider_prefix %{provider}.%{provider_tld}/%{owner}/%{repo}
%global import_path     %{provider_prefix}
%global git_repo        https://%{import_path}



Name:           protonplus-next
Version:        %{gen_version}
Release:        1%{?dist}
Summary:        Simple and powerful manager for Wine, Proton, DXVK and VKD3D

ExclusiveArch:  x86_64
License:        GPL-3.0-or-later
URL:            %{git_repo}
Source0:        %{url}/archive/%{built_tag}/%{repo}-%{version}.tar.gz
Source1:        %{name}.rpmlintrc
# License of the specfile
Source2:        %{name}.spec.license


# fdupes need to fix file rpmlint W: files-duplicate
# /usr/share/icons/hicolor/symbolic/apps/com.vysp3r.ProtonPlus-symbolic.svg /usr/share/icons/hicolor/scalable/apps/com.vysp3r.ProtonPlus.svg
BuildRequires:  fdupes
BuildRequires:  gettext
BuildRequires:  meson >= 0.62.0
BuildRequires:  vala

BuildRequires:  /usr/bin/appstream-util
BuildRequires:  /usr/bin/desktop-file-validate

BuildRequires:  pkgconfig(gee-0.8)
BuildRequires:  pkgconfig(gtk4)
BuildRequires:  pkgconfig(json-glib-1.0)
BuildRequires:  pkgconfig(libadwaita-1) >= 1.4
BuildRequires:  pkgconfig(libarchive)
BuildRequires:  pkgconfig(libsoup-3.0)



# Need for TLS support
Requires:       glib-networking

Obsoletes:  protonup-qt

%description
%{repo} is a simple and powerful manager for:
 - Wine
 - Proton
 - DXVK
 - VKD3D
 - Several other runners

Supports Steam, Lutris, Heroic and Bottles.



%prep
echo "%SHA256SUM0 %{SOURCE0}" | sha256sum -c -
%autosetup -n %{repo}-%{built_tag_strip}



%build
%meson
%meson_build



%install
%meson_install

%find_lang %{flatpak_name}

# create symlink prontonplus -> com.vysp3r.ProtonPlus
%{__ln_s} %{_bindir}/%{flatpak_name} %{buildroot}%{_bindir}/%{name}

# create symlinks for icons
# fix rpmlint W: files-duplicate
%fdupes -s %{buildroot}%{_datadir}/icons/hicolor



%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{flatpak_name}.desktop

appstream-util validate-relax --nonet \
    %{buildroot}%{_datadir}/appdata/%{flatpak_name}.appdata.xml



%files -f %{flatpak_name}.lang
%license LICENSE.md
%doc README.md CONTRIBUTING.md CODE_OF_CONDUCT.md SECURITY.md
# install symlink prontonplus -> com.vysp3r.ProtonPlus
%{_bindir}/%{name}
%{_bindir}/%{flatpak_name}
%{_datadir}/appdata/%{flatpak_name}.appdata.xml
%{_datadir}/applications/%{flatpak_name}.desktop
%{_datadir}/glib-2.0/schemas/%{flatpak_name}.gschema.xml
%{_datadir}/icons/hicolor/*/apps/%{flatpak_name}.svg



%changelog
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
