BuildArch:              noarch

Name:          nobara-welcome
Version:       2.5
Release:       98%{?dist}
License:       GPLv2
Group:         System Environment/Libraries
Summary:       Nobara's Welcome App


URL:            https://github.com/nobara-project/nobara-core-packages
Source0:        %{URL}/releases/download/1.0/nobara-welcome-39.tar.gz

BuildRequires:	wget
Requires:      /usr/bin/bash
Requires:	python3
Requires:	python
Requires:	gtk3
Requires: 	glib2
Provides:	nobara-sync

# App Deps
Requires:	python3-gobject
Requires:	nobara-login
Requires:	nobara-login-config
Requires:	nobara-controller-config
Requires:	webapp-manager
Requires:	papirus-icon-theme
Requires: 	gperftools-libs(x86-32)
Requires: 	xterm-resize
Requires: 	colorized-logs
Requires: 	util-linux
Requires: 	vte291

# Gnome Deps
Suggests:	gnome-tweaks

# KDE Deps
Suggests:	kde-runtime

%install
tar -xf %{SOURCE0}
mv nobara-welcome/usr %{buildroot}/
mv nobara-welcome/etc %{buildroot}/
mkdir -p %{buildroot}%{_sysconfdir}/xdg/autostart/
mv %{buildroot}/usr/share/applications/nobara-autostart.desktop %{buildroot}%{_sysconfdir}/xdg/autostart/
mkdir -p %{buildroot}/usr/share/licenses/nobara-welcome
wget https://raw.githubusercontent.com/CosmicFusion/cosmo-welcome-glade/main/LICENSE.md -O %{buildroot}/usr/share/licenses/nobara-welcome/LICENSE

# for legacy updater to detect changes
ln -s /etc/nobara/scripts/nobara-updater/nobara-sync.sh %{buildroot}%{_sysconfdir}/nobara/scripts/nobara-welcome/updater.sh

%description
Nobara's Python3 & GTK3 built Welcome App
%files
%attr(0755, root, root) /etc/nobara/scripts/nobara-welcome/*
%attr(0755, root, root) /etc/nobara/scripts/nobara-davinci/*
%attr(0755, root, root) /etc/nobara/scripts/nobara-updater/*
%attr(0755, root, root) /etc/nobara/scripts/steam-game-fixups/*
%attr(0755, root, root) /usr/bin/*
%attr(0644, root, root) /usr/share/applications/*
%attr(0644, root, root) /usr/share/glib-2.0/schemas/*
%attr(0644, root, root) /usr/share/icons/hicolor/64x64/apps/*.svg
%attr(0644, root, root) %{_sysconfdir}/xdg/autostart/nobara-autostart.desktop
%attr(0644, root, root) /usr/share/licenses/nobara-welcome/LICENSE

%post
glib-compile-schemas /usr/share/glib-2.0/schemas/

