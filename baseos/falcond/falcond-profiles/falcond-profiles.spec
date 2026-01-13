%global debug_package %{nil}
Name:           falcond-profiles
Version:        1.0
Release:        %autorelease -b11
Summary:        Advanced Linux Gaming Performance Daemon

License:        MIT
URL:            https://github.com/PikaOS-Linux/%{name}/
Source0:        %{url}/archive/refs/heads/main.tar.gz

BuildArch:      noarch

BuildRequires:  tar

Recommends:	falcond
Requires:	falcond

%description
falcond is a powerful system daemon designed to automatically optimize your Linux gaming experience. It intelligently manages system resources and performance settings on a per-game basis, eliminating the need to manually configure settings for each game.

%prep

%autosetup -n %{name}-main

%build

%install
install -Dm644 usr/share/falcond/system.conf -t %{buildroot}%{_datadir}/falcond/
install -Dm644 usr/share/falcond/profiles/*.conf -t %{buildroot}%{_datadir}/falcond/profiles/
install -Dm644 usr/share/falcond/profiles/handheld/* -t %{buildroot}%{_datadir}/falcond/profiles/handheld/
install -Dm644 usr/share/falcond/profiles/htpc/* -t %{buildroot}%{_datadir}/falcond/profiles/htpc/

install -dm2775 %{buildroot}%{_datadir}/falcond/profiles/user

%files
%doc README.md
%license LICENSE
%dir %{_datadir}/falcond
%{_datadir}/falcond/system.conf
%{_datadir}/falcond/profiles/*.conf
%{_datadir}/falcond/profiles/handheld/*.conf
%{_datadir}/falcond/profiles/htpc/*.conf
%attr(2775, root, falcond) %dir %{_datadir}/falcond/profiles/user

%changelog
%autochangelog
