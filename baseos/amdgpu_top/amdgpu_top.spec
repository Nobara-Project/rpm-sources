Name:           amdgpu_top
Version:        0.11.2
Release:        2%{?dist}
Summary:        Tool that displays AMD GPU utilization
License:        MIT
URL:            https://github.com/Umio-Yasuno/amdgpu_top
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz

ExclusiveArch: x86_64 aarch64

BuildRequires:	anda-srpm-macros
BuildRequires:  cargo-rpm-macros
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
BuildRequires:  libdrm-devel
BuildRequires:  mold
BuildRequires:  rust

Requires:       libdrm

%description
amdgpu_top is tool that displays AMD GPU utilization, like umr or clbr/radeontop or intel_gpu_top.
The tool displays information gathered from performance counters (GRBM, GRBM2), sensors, fdinfo, and AMDGPU driver.

%prep
%autosetup -n %{name}-%{version}
%cargo_prep_online

%build
%cargo_build
%{cargo_license_summary_online}
%{cargo_license_online} > LICENSE.dependencies

%install
%cargo_install
install -Dpm 0644 assets/%{name}.desktop %{buildroot}%{_datadir}/applications/%{name}.desktop
install -Dpm 0644 assets/%{name}-tui.desktop %{buildroot}%{_datadir}/applications/%{name}-tui.desktop
install -Dm644 assets/io.github.umio_yasuno.%{name}.metainfo.xml %{buildroot}%{_datadir}/metainfo/io.github.umio_yasuno.%{name}.metainfo.xml

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}-tui.desktop
appstream-util validate-relax --nonet %{buildroot}%{_datadir}/metainfo/*.metainfo.xml

%files
%doc	 README.md
%license LICENSE
%license LICENSE.dependencies
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/applications/%{name}-tui.desktop
%{_datadir}/metainfo/io.github.umio_yasuno.amdgpu_top.metainfo.xml

%changelog
* Sat Mar 07 2026 Radical <radical@radical.fun> - 0.11.2-2
- Change ExclusiveArch to allow building for aarch64

* Thu Feb 05 2026 LionHeartP <LionHeartP@proton.me> - 0.11.2-1
- Update to 0.11.2

* Sat Jan 24 2026 LionHeartP <LionHeartP@proton.me> - 0.11.0-1
- Initial package
