Name:           xapp-symbolic-icons
Version:        1.0.5
Release:        1%{?dist}
Summary:        A set of symbolic icons for GTK applications and projects.
License:        GPL-3.0-only AND LGPL-3.0-only
URL:            https://github.com/xapp-project/xapp-symbolic-icons

Source0:        %{URL}/archive/refs/tags/%{version}.tar.gz

BuildArch:	noarch

BuildRequires:  meson
BuildRequires:  ninja-build
BuildRequires:  pkgconfig(python3)
BuildRequires:  pkgconfig(gtk+-3.0)

Requires:       hicolor-icon-theme

%description
The XApp Symbolic Icons are a set of symbolic icons designed for use in
GTK applications and other projects from the XApp development team
(primarily associated with Linux Mint).

%prep
%autosetup

%build
%meson
%meson_build

%install
%meson_install

%post
/usr/bin/gtk-update-icon-cache -qf /usr/share/icons/hicolor || :

%postun
/usr/bin/gtk-update-icon-cache -qf /usr/share/icons/hicolor || :

%files
%license AUTHORS COPYING
%doc README.md
%{_bindir}/xsi-replace-adwaita-symbolic
%{_datadir}/icons/hicolor/scalable/actions/xsi-*
%{_datadir}/xapp/xsi-adwaita-symbolic.info


%changelog
* Sat Nov 29 2025 LionHeartP <LionHeartP@proton.me> - 1.0.5-1
- Initial package
