Name:          nobara-welcome
Version:       5.0.1
Release:       6%{?dist}
License:       GPLv2
Group:         System Environment/Libraries
Summary:       Nobara's Welcome App


URL:            https://github.com/nobara-project/nobara-core-packages
Source0:        %{URL}/releases/download/1.0/nobara-welcome-gtk4.tar.gz

BuildRequires:	wget
BuildRequires:	cargo
BuildRequires:	gdk-pixbuf2-devel
BuildRequires:	gtk4-devel
BuildRequires:	gtk3-devel
BuildRequires:	libadwaita-devel
BuildRequires:	systemd-rpm-macros

Requires:      /usr/bin/bash
Requires:	python3
Requires:	python
Requires:	gtk3
Requires:	gtk4
Requires:	libadwaita
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
Requires: 	nobara-driver-manager
Requires: 	vte291
Requires: 	rt
Requires: 	libappindicator-gtk3
Requires: 	python-cairosvg
Requires: 	python-pillow
Requires: 	python3-dbus

# Gnome Deps
Suggests:	gnome-tweaks

# KDE Deps
Suggests:	kde-runtime

%prep
%autosetup -p1 -n nobara-welcome-gtk4

%build
DESTDIR=%{buildroot} make install

# for legacy updater to detect changes
mkdir -p %{buildroot}%{_sysconfdir}/nobara/scripts/nobara-welcome/
mkdir -p %{buildroot}%{_sysconfdir}/nobara/scripts/nobara-updater/
ln -s /usr/lib/nobara/nobara-welcome/scripts/updater/nobara-sync.sh %{buildroot}%{_sysconfdir}/nobara/scripts/nobara-welcome/updater.sh
ln -s /usr/lib/nobara/nobara-welcome/scripts/updater/nobara-sync.sh %{buildroot}%{_sysconfdir}/nobara/scripts/nobara-updater/nobara-sync.sh


%description
Nobara's Python3 & GTK3 built Welcome App
%files
%{_prefix}/lib/nobara/nobara-welcome/scripts/updater/*
%{_prefix}/lib/nobara/nobara-welcome/scripts/*
%{_bindir}/*
%{_datadir}/applications/*
%{_datadir}/glib-2.0/schemas/*
%{_datadir}/icons/hicolor/64x64/apps/*.svg
%{_datadir}/icons/hicolor/scalable/apps/*.svg
%{_datadir}/nobara/*
%{_sysconfdir}/xdg/autostart/*.desktop
%{_sysconfdir}/nobara/scripts/nobara-welcome/updater.sh
%{_sysconfdir}/nobara/scripts/nobara-updater/nobara-sync.sh

%post
glib-compile-schemas /usr/share/glib-2.0/schemas/
%systemd_user_post nobara-updater-systray.service

%posttrans
# Debug statement to verify %posttrans execution
echo "Running %posttrans scriptlet"

# Iterate over all user sessions
for session in $(loginctl list-sessions --no-legend | awk '{print $1}'); do
    uid=$(loginctl show-session $session -p User --value)
    user=$(getent passwd $uid | cut -d: -f1)

    # Debug statement to verify user and UID
    echo "Restarting service for user $user with UID $uid"

    # Set environment variables for the user session
    XDG_RUNTIME_DIR="/run/user/$uid"
    DBUS_SESSION_BUS_ADDRESS="unix:path=$XDG_RUNTIME_DIR/bus"

    # Restart the user service for each user session
    su - $user -c "XDG_RUNTIME_DIR=$XDG_RUNTIME_DIR DBUS_SESSION_BUS_ADDRESS=$DBUS_SESSION_BUS_ADDRESS systemctl --user daemon-reload" || echo "Failed to perform daemon-reload for user $user"
    su - $user -c "XDG_RUNTIME_DIR=$XDG_RUNTIME_DIR DBUS_SESSION_BUS_ADDRESS=$DBUS_SESSION_BUS_ADDRESS systemctl --user stop nobara-updater-systray.service" || echo "Failed to restart service for user $user"
done

%preun
%systemd_user_preun nobara-updater-systray.service
