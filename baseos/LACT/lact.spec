Name:           lact
Version:        0.7.1
Release:        1
Summary:        AMDGPU control utility
License:        MIT
URL:            https://github.com/ilya-zlobintsev/LACT
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz

# https://fedoraproject.org/wiki/Changes/EncourageI686LeafRemoval
ExcludeArch:    %{ix86}

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  rust cargo gtk4-devel gcc libdrm-devel blueprint-compiler dbus curl make clang git
Requires:       gtk4 libdrm hwdata

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
/usr/bin/lact
/usr/lib/systemd/system/lactd.service
/usr/share/applications/io.github.lact-linux.desktop
/usr/share/icons/hicolor/scalable/apps/io.github.lact-linux.svg
/usr/share/pixmaps/io.github.lact-linux.png

%changelog
%autochangelog
