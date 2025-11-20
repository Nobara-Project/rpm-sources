Name:           adw-gtk3-theme
Version:        6.4
Release:        1%{?dist}
Summary:        The theme from libadwaita ported to GTK-3
License:        GPLv2+
URL:            https://github.com/lassekongo83/adw-gtk3
BuildArch:      noarch
BuildRequires: nodejs-npm
BuildRequires: git
BuildRequires: meson
BuildRequires: ninja-build
Provides: adw-gtk3-theme
Provides: adw-gtk3
Obsoletes: adw-gtk3 <= 6.2

%description
The theme from libadwaita ported to GTK-3


%prep
git clone --recurse-submodules https://github.com/lassekongo83/adw-gtk3.git

%build
cd adw-gtk3
git checkout tags/v6.4
npm config set prefix '~/.npm-global'
export PATH=~/.npm-global/bin:$PATH
npm install -g sass
%meson
%meson_build

%install
cd adw-gtk3
%meson_install

%files
%{_datadir}/themes/adw-gtk3/*
%{_datadir}/themes/adw-gtk3-dark/*
