Name:           adw-gtk3-theme
Version:        6.5
Release:        2%{?dist}
Summary:        The theme from libadwaita ported to GTK-3
License:        LGPL-2.1-or-later
URL:            https://github.com/lassekongo83/adw-gtk3
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz
BuildArch:      noarch
BuildRequires: nodejs-npm
BuildRequires: git
BuildRequires: meson
BuildRequires: ninja-build
BuildRequires: anda-srpm-macros
Provides: adw-gtk3-theme
Provides: adw-gtk3
Obsoletes: adw-gtk3 <= 6.2

%description
The theme from libadwaita ported to GTK-3

%prep
%autosetup -C

%conf
%__npm config set prefix '~/.npm-global'
export PATH=~/.npm-global/bin:$PATH
%__npm install -g sass
%meson

%build
%meson_build

%install
%meson_install

%files
%{_datadir}/themes/adw-gtk3/*
%{_datadir}/themes/adw-gtk3-dark/*

%changelog
* Thu Sep 17 2026 Owen Zimmerman <owen@fyralabs.com> - 6.5-2
- Switch to tarball source
- Install license and readme
- Correct license identifier
- Use %%conf, clean up spec
- Use npm macros from anda-srpm-macros
