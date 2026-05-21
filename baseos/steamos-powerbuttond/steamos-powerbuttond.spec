Name:           steamos-powerbuttond
Version:        4.2
Release:        %autorelease
Summary:        Steam Deck power button daemon

License:        BSD
URL:            https://gitlab.steamos.cloud/holo/powerbuttond
Source:		%{URL}/-/archive/v%{version}/powerbuttond-v%{version}.tar.gz
BuildRequires:  systemd-rpm-macros
BuildRequires:	systemd-devel
BuildRequires:  libevdev-devel
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  git

Requires:       libevdev

Provides:       steam-powerbuttond
Obsoletes:      steam-powerbuttond < 3.3
Provides:       powerbuttond
Obsoletes:      powerbuttond < 3.3
Obsoletes:      gamescope-session-plus <= 0.2.git.201.5538cd66

%description
Steam Deck power button daemon

# Disable debug packages
%define debug_package %{nil}

%prep
%autosetup -n powerbuttond-v%{version} -p 1

%build
%make_build

%install
%make_install DESTDIR=%{buildroot}
sed -i 's/Requisite=gamescope-session.service//g' %{buildroot}/%{_userunitdir}/%{name}.service
rm -r %{buildroot}/%{_userunitdir}/gamescope-session.service.wants

%post
udevadm control --reload-rules
udevadm trigger
%systemd_user_post %{name}.service

%preun
%systemd_user_preun %{name}.service

%files
%license LICENSE
%dir %{_prefix}/lib/hwsupport
%{_prefix}/lib/hwsupport/%{name}
%{_userunitdir}/%{name}.service
%{_prefix}/lib/udev/rules.d/70-steamos-power-button.rules
%dir %{_prefix}/lib/udev/hwdb.d
%{_prefix}/lib/udev/hwdb.d/70-steamos-power-button.hwdb

%changelog
%autochangelog
