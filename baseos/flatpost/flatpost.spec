%global tag 1.0.9

# Manual commit is auto-inserted by workflow
%global commit 12454b8e6494b691dc7476a3d30366ce06f55790

%global shortcommit %(c=%{commit}; echo ${c:0:7})

%global build_timestamp %(date +"%Y%m%d")

%global rel_build 1.%{build_timestamp}.%{shortcommit}%{?dist}

Name:          flatpost
Version:       %{tag}
Release:       %{rel_build}
License:       BSD 2-Clause
Summary:       Desktop environment agnostic Flathub software center.

URL:            https://github.com/gloriouseggroll/flatpost
Source0:        %{url}/archive/refs/tags/%{tag}.tar.gz#/%{name}-%{tag}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  make
BuildRequires:  desktop-file-utils

Provides:	nobara-updater

# App Deps
Requires: python
Requires: python3
Requires: python3-gobject
Requires: python3-requests
Requires: python3-pillow
Requires: python3-svgwrite
Requires: python3-fonttools
Requires: python3-numpy

Requires: adw-gtk3-theme
Requires: adwaita-icon-theme
Requires: flatpak
Requires: glib2
Requires: gtk3
Requires: gtk4
Requires: xdg-utils

Requires(post):      shared-mime-info
Requires(postun):    shared-mime-info
Requires(posttrans): shared-mime-info

Provides: flatpost

%description
Desktop environment agnostic Flathub software center. Allows for browsing,
installation, removal, updating, and permission management of flatpak packages and repositories.

%prep
%autosetup -p 1

%build
make all DESTDIR=%{buildroot}

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/com.flatpost.flatpostapp.desktop

%post
xdg-icon-resource forceupdate --theme hicolor &>/dev/null
update-mime-database usr/share/mime &>/dev/null
update-desktop-database -q

%postun
xdg-icon-resource forceupdate --theme hicolor &>/dev/null
update-mime-database usr/share/mime &>/dev/null
update-desktop-database -q

%posttrans
xdg-icon-resource forceupdate --theme hicolor &>/dev/null
update-mime-database usr/share/mime &>/dev/null
update-desktop-database -q

%files
%{python3_sitelib}/flatpost/
%{_bindir}/flatpost
%{_datadir}/applications/com.flatpost.flatpostapp.desktop
%{_datadir}/flatpost/collections_data.json
%{_datadir}/icons/hicolor/1024x1024/apps/com.flatpost.flatpostapp.png
%{_datadir}/icons/hicolor/64x64/apps/com.flatpost.flatpostapp.png
%{_datadir}/mime/packages/flatpost.xml
%license %{_datadir}/licenses/flatpost/LICENSE

%clean
rm -rf %{buildroot}

%changelog
* Fri Jun 28 2024 Your Name <you@example.com> - 1.0-1
- Initial package
