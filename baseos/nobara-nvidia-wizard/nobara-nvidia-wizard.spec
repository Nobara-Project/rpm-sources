BuildArch:              noarch

Name:          nobara-nvidia-wizard
Version:       1.1
Release:       17%{?dist}
License:       GPLv2
Group:         System Environment/Libraries
Summary:       Nobara's Nvidia Installation/Removal Wizard

URL:            https://github.com/nobara-project/nobara-core-packages
Source0:        %{URL}/releases/download/1.0/nobara-nvidia-wizard.tar.gz
Source1:        https://raw.githubusercontent.com/CosmicFusion/cosmo-nvidia-wizard/main/LICENSE.md

BuildRequires:	wget
Requires:      /usr/bin/bash
Requires:	python3
Requires:	python
Requires:	gtk3
Requires: 	glib2


# App Deps
Requires:	python3-gobject
Requires:	nobara-login
Requires:	nobara-login-config
Requires:	papirus-icon-theme
Requires:	nobara-welcome

%install
tar -xf %{SOURCE0}

install -d %{buildroot}%{_bindir}/
install -d %{buildroot}%{_datadir}/applications/
install -d %{buildroot}%{_datadir}/licenses/nobara-nvidia-wizard
install -d %{buildroot}%{_sysconfdir}/nobara/scripts/cosmo-nvidia-wizard
install -m 0644 nobara-nvidia-wizard/etc/nobara/scripts/cosmo-nvidia-wizard/process.ui %{buildroot}%{_sysconfdir}/nobara/scripts/cosmo-nvidia-wizard/
install -m 0644 nobara-nvidia-wizard/etc/nobara/scripts/cosmo-nvidia-wizard/main.ui %{buildroot}%{_sysconfdir}/nobara/scripts/cosmo-nvidia-wizard/
install -m 0755 nobara-nvidia-wizard/etc/nobara/scripts/cosmo-nvidia-wizard/gpu-utils %{buildroot}%{_sysconfdir}/nobara/scripts/cosmo-nvidia-wizard/
install -m 0755 nobara-nvidia-wizard/etc/nobara/scripts/cosmo-nvidia-wizard/end.sh %{buildroot}%{_sysconfdir}/nobara/scripts/cosmo-nvidia-wizard/
install -m 0755 nobara-nvidia-wizard/etc/nobara/scripts/cosmo-nvidia-wizard/install.sh %{buildroot}%{_sysconfdir}/nobara/scripts/cosmo-nvidia-wizard/
install -m 0755 nobara-nvidia-wizard/etc/nobara/scripts/cosmo-nvidia-wizard/remove.sh %{buildroot}%{_sysconfdir}/nobara/scripts/cosmo-nvidia-wizard/
install -m 0755 nobara-nvidia-wizard/etc/nobara/scripts/cosmo-nvidia-wizard/main.py %{buildroot}%{_sysconfdir}/nobara/scripts/cosmo-nvidia-wizard/
install -m 0755 nobara-nvidia-wizard/etc/nobara/scripts/cosmo-nvidia-wizard/process.py %{buildroot}%{_sysconfdir}/nobara/scripts/cosmo-nvidia-wizard/
install -m 0755 nobara-nvidia-wizard/usr/bin/nobara-nvidia-wizard %{buildroot}%{_bindir}/
install -m 0644 nobara-nvidia-wizard/usr/share/applications/nobara-nvidia-wizard.desktop %{buildroot}%{_datadir}/applications/
install -m 0644 %{SOURCE1} %{buildroot}%{_datadir}/licenses/nobara-nvidia-wizard/LICENSE

%description
Nobara's Nvidia Installation/Removal Wizard	
%files
%{_sysconfdir}/nobara/scripts/cosmo-nvidia-wizard/process.ui
%{_sysconfdir}/nobara/scripts/cosmo-nvidia-wizard/main.ui
%{_sysconfdir}/nobara/scripts/cosmo-nvidia-wizard/gpu-utils
%{_sysconfdir}/nobara/scripts/cosmo-nvidia-wizard/end.sh
%{_sysconfdir}/nobara/scripts/cosmo-nvidia-wizard/install.sh
%{_sysconfdir}/nobara/scripts/cosmo-nvidia-wizard/remove.sh
%{_sysconfdir}/nobara/scripts/cosmo-nvidia-wizard/main.py
%{_sysconfdir}/nobara/scripts/cosmo-nvidia-wizard/process.py
%{_bindir}/nobara-nvidia-wizard
%{_datadir}/applications/nobara-nvidia-wizard.desktop
%{_datadir}/licenses/nobara-nvidia-wizard/LICENSE
