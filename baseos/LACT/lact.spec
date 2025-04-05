Name:           lact
Version:        0.7.3
Release:        1
Summary:        AMDGPU control utility
License:        MIT
URL:            https://github.com/ilya-zlobintsev/LACT
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz

# https://fedoraproject.org/wiki/Changes/EncourageI686LeafRemoval
ExcludeArch:    %{ix86}

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  rust cargo gtk4-devel gcc libdrm-devel dbus curl make clang git vulkan-tools
Requires:       gtk4 libdrm hwdata vulkan-tools

%description
AMDGPU control utility

%prep
%setup -q -n LACT-%{version}

%build
make build-release %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install PREFIX=/usr DESTDIR=%{buildroot}

%files
%defattr(-,root,root,-)
%license LICENSE
%doc README.md
%{_bindir}/lact
%{_prefix}/lib/systemd/system/lactd.service
%{_datadir}/applications/io.github.ilya_zlobintsev.LACT.desktop
%{_datadir}/icons/hicolor/scalable/apps/io.github.ilya_zlobintsev.LACT.svg
%{_datadir}/metainfo/io.github.ilya_zlobintsev.LACT.metainfo.xml
%{_datadir}/pixmaps/io.github.ilya_zlobintsev.LACT.png

%changelog
%autochangelog
