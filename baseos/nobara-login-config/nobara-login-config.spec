BuildArch:              noarch

Name:          nobara-login-config
Version:       1.0
Release:       1%{?dist}
License:       GPLv2
Group:         System Environment/Libraries
Summary:       GUI Login Selector


URL:           https://github.com/CosmicFusion/nobara-login-config

Source0:        %{name}-%{version}.tar.gz
Source1:        https://raw.githubusercontent.com/CosmicFusion/nobara-login-config/main/LICENSE.md

BuildRequires:	wget
Requires:      /usr/bin/bash
Requires:	zenity

%install
tar -xf %{SOURCE0}
mv usr %{buildroot}/
mkdir -p %{buildroot}/usr/share/licenses/nobara-login-config
mv %{SOURCE1} %{buildroot}/usr/share/licenses/nobara-login-config/LICENSE

%description
GUI Selector for GDM, SDDM, and LightDM
%files
%attr(0755, root, root) "/usr/bin/nobara-login-config"
%attr(0644, root, root) "/usr/share/licenses/nobara-login-config/LICENSE"
