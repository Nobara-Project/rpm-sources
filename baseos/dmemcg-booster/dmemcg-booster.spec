Name:           dmemcg-booster
Version:        0.1.2
Release:        1%{?dist}
Summary:        Userspace utility for controling VRAM utilization
License:        Apache-2.0 OR MIT
URL:            https://gitlab.steamos.cloud/holo/%{name}
Source0:        %{url}/-/archive/%{version}/%{name}-%{version}.tar.gz
Source1:        90-%{name}.system.preset
Source2:        90-%{name}.user.preset
Source3:	%{url}/-/raw/main/LICENSE

BuildRequires:  anda-srpm-macros
BuildRequires:  cargo-rpm-macros
BuildRequires:  dbus-devel
BuildRequires:  libdrm-devel
BuildRequires:  mold
BuildRequires:  systemd-rpm-macros

Requires:       libdrm
Requires:       systemd-libs

%description
%summary.

%prep
%autosetup -n %{name}-%{version}
%cargo_prep_online

%build
%{cargo_license_online -a} > LICENSE.dependencies
cp %{SOURCE3} .

%install
%cargo_install
install -Dpm644 %{name}-system.service %{buildroot}%{_unitdir}/%{name}-system.service
install -Dpm644 %{name}-user.service %{buildroot}%{_userunitdir}/%{name}-user.service
install -Dpm644 %{SOURCE1} %{buildroot}%{_presetdir}/90-%{name}.preset
install -Dpm644 %{SOURCE2} %{buildroot}%{_userpresetdir}/90-%{name}.preset

%post
%systemd_post %{name}-system.service
%systemd_user_post %{name}-user.service

%preun
%systemd_preun %{name}-system.service
%systemd_user_preun %{name}-user.service

%postun
%systemd_postun_with_restart %{name}-system.service
%systemd_user_postun_with_restart %{name}-user.service

%files
%license LICENSE
%license LICENSE.dependencies
%{_bindir}/%{name}
%{_presetdir}/90-dmemcg-booster.preset
%{_userpresetdir}/90-dmemcg-booster.preset
%{_unitdir}/%{name}-system.service
%{_userunitdir}/%{name}-user.service

%changelog
* Fri Apr 17 2026 LionHeartP <LionHeartP@proton.me> - 0.1.2-1
- Initial spec derived from AUR PKGBUILD https://aur.archlinux.org/packages/dmemcg-booster
