%global debug_package %{nil}
Name:           falcond-profiles
Version:        1.0
Release:        %autorelease -b3
Summary:        Advanced Linux Gaming Performance Daemon

License:        MIT
URL:            https://github.com/PikaOS-Linux/falcond-profiles/
Source0:        %{url}/archive/refs/heads/main.tar.gz

ExclusiveArch:	x86_64

BuildRequires:  tar

Recommends:	falcond
Requires:	falcond

%description
falcond is a powerful system daemon designed to automatically optimize your Linux gaming experience. It intelligently manages system resources and performance settings on a per-game basis, eliminating the need to manually configure settings for each game.

%prep

%autosetup -n falcond-profiles-main

%build

%install
mkdir -p %{buildroot}%{_datadir}/falcond/
mkdir -p %{buildroot}%{_datadir}/falcond/profiles/
mkdir -p %{buildroot}%{_datadir}/falcond/profiles/handheld/
mkdir -p %{buildroot}%{_datadir}/falcond/profiles/htpc/
cp -a usr/share/falcond/system.conf %{buildroot}%{_datadir}/falcond/
cp -a usr/share/falcond/profiles/* %{buildroot}%{_datadir}/falcond/profiles/
cp -a usr/share/falcond/profiles/handheld/* %{buildroot}%{_datadir}/falcond/profiles/handheld/
cp -a usr/share/falcond/profiles/htpc/* %{buildroot}%{_datadir}/falcond/profiles/htpc/
    
%files
%doc README.md
%license LICENSE
%{_datadir}/falcond/system.conf
%{_datadir}/falcond/profiles/*.conf
%{_datadir}/falcond/profiles/handheld/*.conf
%{_datadir}/falcond/profiles/htpc/*.conf

%changelog
%autochangelog
