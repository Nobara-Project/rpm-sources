%global _include_minidebuginfo 0
%global debug_package %{nil}

Name:           falcond
Version:        2.0.12
Release:        %autorelease
Summary:        Advanced Linux Gaming Performance Daemon

License:        MIT
URL:            https://git.pika-os.com/general-packages/%{name}
Source0:        %{url}/archive/v%{version}.tar.gz
Source1:	falcond-vendor.tar.gz

ExclusiveArch:	x86_64 aarch64

BuildRequires:  zig >= 0.16
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
mkdir -p .zig-cache-local
tar -xzf %{SOURCE1} -C %{name}/

%build

%install
cd %{name}
mkdir -p %{buildroot}%{_unitdir}/
install -Dm644 debian/%{name}.service %{buildroot}%{_unitdir}
DESTDIR="%{buildroot}" \
%ifarch x86_64
zig build \
    -Doptimize=ReleaseFast \
    -Dcpu=x86_64_v2
%else
zig build \
    -Doptimize=ReleaseFast
%endif
    
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
* Thu Jul 09 2026 LionHeartP <LionHeartP@proton.me> - 2.0.12-1
- Update to 2.0.12

* Tue Jul 07 2026 LionHeartP <LionHeartP@proton.me> - 2.0.11-1
- Update to 2.0.11

* Thu Jul 02 2026 LionHeartP <LionHeartP@proton.me> - 2.0.10-1
- Update to 2.0.10

* Thu Jun 25 2026 LionHeartP <LionHeartP@proton.me> - 2.0.9-1
- Update to 2.0.9

* Fri May 22 2026 LionHeartP <LionHeartP@proton.me> - 2.0.8-1
- Update to 2.0.8

* Fri May 15 2026 LionHeartP <LionHeartP@proton.me> - 2.0.6-1
- Update to 2.0.6

* Wed Apr 22 2026 LionHeartP <LionHeartP@proton.me> - 2.0.5-1
- Update to 2.0.5

* Sun Apr 19 2026 LionHeartP <LionHeartP@proton.me> - 2.0.4-1
- Update to 2.0.4

* Sun Apr 05 2026 LionHeartP <LionHeartP@proton.me> - 2.0.2-1
- Update to 2.0.2

* Sat Mar 14 2026 LionHeartP <LionHeartP@proton.me> - 2.0.1-1
- Update to 2.0.1

* Sat Mar 07 2026 Radical <radical@radical.fun> - 1.2.3-1
- Update specfile to allow aarch64 build

* Tue Jan 06 2026 LionHeartP <LionHeartP@proton.me> - 1.2.3-1
- Update to 1.2.3

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
