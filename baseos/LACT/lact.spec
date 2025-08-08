Name:           lact
Version:        0.8.1
Release:        1
Summary:        GPU control utility
License:        MIT
URL:            https://github.com/ilya-zlobintsev/LACT
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz

ExcludeArch:    %{ix86}

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  rust cargo gtk4-devel gcc libdrm-devel dbus ocl-icd-devel curl make clang git vulkan-tools
Requires:       gtk4 libdrm ocl-icd-devel hwdata vulkan-tools

%description
GPU control utility

%prep
%setup -q -n LACT-%{version}

%build
VERGEN_GIT_SHA=044fde0 make build-release %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install PREFIX=/usr DESTDIR=%{buildroot}

%files
%defattr(-,root,root,-)
%license LICENSE
%doc README.md
/usr/bin/lact
/usr/lib/systemd/system/lactd.service
/usr/share/applications/io.github.ilya_zlobintsev.LACT.desktop
/usr/share/icons/hicolor/scalable/apps/io.github.ilya_zlobintsev.LACT.svg
/usr/share/pixmaps/io.github.ilya_zlobintsev.LACT.png
/usr/share/metainfo/io.github.ilya_zlobintsev.LACT.metainfo.xml

%changelog
* Fri Aug 08 2025 LionHeartP <LionHeartP@proton.me> - 0.8.1-1
- Update to 0.8.1

* Sat Jun 28 2025 LionHeartP <LionHeartP@proton.me> - 0.8.0-1
- Update to 0.8.0
