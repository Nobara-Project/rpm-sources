%global _include_minidebuginfo 0
%global debug_package %{nil}

Name:           falcond
Version:        1.2.2
Release:        %autorelease
Summary:        Advanced Linux Gaming Performance Daemon

License:        MIT
URL:            https://git.pika-os.com/general-packages/%{name}
Source0:        %{url}/archive/v%{version}.tar.gz

ExclusiveArch:	x86_64

BuildRequires:  zig >= 0.14.0
BuildRequires:  systemd-rpm-macros

Recommends:	%{name}-profiles
Recommends:	%{name}-gui
Requires:	%{name}-profiles
Requires:	%{name}-gui
Requires:	scx-scheds

Provides:       group(falcond)

%description
falcond is a powerful system daemon designed to automatically optimize your Linux gaming experience. It intelligently manages system resources and performance settings on a per-game basis, eliminating the need to manually configure settings for each game.

%prep

%autosetup -n %{name}

%build

%install
cd %{name}
mkdir -p %{buildroot}%{_unitdir}/
install -Dm644 debian/%{name}.service %{buildroot}%{_unitdir}
DESTDIR="%{buildroot}" \
zig build \
    -Doptimize=ReleaseFast \
    -Dcpu=x86_64_v2
    
%pre
# Create falcond group if it doesn't exist
getent group 'falcond' >/dev/null || groupadd -f -r 'falcond' || :

# Root must be a member of the group
usermod -aG 'falcond' root || :
    
%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service
    
%files
%doc README.md
%license LICENSE
%{_bindir}/%{name}
%{_unitdir}/%{name}.service

%changelog
* Sat Jan 03 2026 LionHeartP <LionHeartP@proton.me> - 1.2.2-1
- Update to 1.2.2
- Implement falcond group for profile editing

* Thu Jan 01 2026 LionHeartP <LionHeartP@proton.me> - 1.2.1-1
- Update to 1.2.1

* Fri Sep 26 2025 LionHeartP <LionHeartP@proton.me> - 1.1.9-1
- Update to 1.1.9

* Mon Jun 23 2025 LionHeartP <LionHeartP@proton.me> - 1.1.7-1
- Update to 1.1.7
- Change CPU arch to x86_64_v2

* Mon Jun 23 2025 LionHeartP <LionHeartP@proton.me> - 1.1.6-1
- Update to 1.1.6
- Change CPU arch to x86_64_v3
