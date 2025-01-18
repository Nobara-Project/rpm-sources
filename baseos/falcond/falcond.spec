Name:           falcond
Version:        1.0.8
Release:        %autorelease
Summary:        Advanced Linux Gaming Performance Daemon

License:        MIT
URL:            https://git.pika-os.com/general-packages/falcond
Source0:        %{url}/archive/v%{version}.tar.gz

ExclusiveArch:	x86_64

BuildRequires:  zig-nightly
BuildRequires:  systemd-rpm-macros

Recommends:	falcond-profiles
Requires:	falcond-profiles

%description
falcond is a powerful system daemon designed to automatically optimize your Linux gaming experience. It intelligently manages system resources and performance settings on a per-game basis, eliminating the need to manually configure settings for each game.

%prep

%autosetup -n falcond

%build

%install
cd %{name}
mkdir -p %{buildroot}%{_unitdir}/
install -Dm644 debian/falcond.service %{buildroot}%{_unitdir}
DESTDIR="%{buildroot}" \
zig build \
    -Doptimize=ReleaseFast
    
%post
%systemd_post falcond.service

%preun
%systemd_preun falcond.service

%postun
%systemd_postun_with_restart falcond.service
    
%files
%doc README.md
%license LICENSE
%{_bindir}/falcond
%{_unitdir}/falcond.service

%changelog
%autochangelog
