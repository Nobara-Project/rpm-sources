Name:           lact
Version:        0.9.0
Release:        1
Summary:        GPU control utility
License:        MIT
URL:            https://github.com/ilya-zlobintsev/LACT
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz

ExcludeArch:    %{ix86}

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  rust cargo gtk4-devel gcc libdrm-devel dbus ocl-icd-devel curl make clang git vulkan-tools systemd-rpm-macros
Requires:       gtk4 libdrm ocl-icd-devel hwdata vulkan-tools

%description
GPU control utility

%prep
%setup -q -n LACT-%{version}

%build
VERGEN_GIT_SHA=b65ae69 make build-release %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install PREFIX=/usr DESTDIR=%{buildroot}

%files
%defattr(-,root,root,-)
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_unitdir}/lactd.service
%{_datadir}/applications/io.github.ilya_zlobintsev.LACT.desktop
%{_datadir}/icons/hicolor/scalable/apps/io.github.ilya_zlobintsev.LACT.svg
%{_datadir}/icons/hicolor/512x512/apps/io.github.ilya_zlobintsev.LACT.png
%{_metainfodir}/io.github.ilya_zlobintsev.LACT.metainfo.xml

%changelog
* Sun Jan 25 2026 LionHeartP <LionHeartP@proton.me> - 0.8.4-1
- Update to 0.8.4

* Fri Nov 21 2025 LionHeartP <LionHeartP@proton.me> - 0.8.3-1
- Update to 0.8.3

* Sat Oct 18 2025 LionHeartP <LionHeartP@proton.me> - 0.8.2-1
- Update to 0.8.2

* Fri Aug 08 2025 LionHeartP <LionHeartP@proton.me> - 0.8.1-1
- Update to 0.8.1

* Sat Jun 28 2025 LionHeartP <LionHeartP@proton.me> - 0.8.0-1
- Update to 0.8.0
