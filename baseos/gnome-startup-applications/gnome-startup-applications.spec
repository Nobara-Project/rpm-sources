%global tarball_version 1ubuntu1

Name: gnome-startup-applications
Version: 45.0
Release: 1%{?dist}
Summary: GNOME startup applications manager

License: GPLv2+
URL: https://gitlab.gnome.org/GNOME/gnome-session
Source0: http://archive.ubuntu.com/ubuntu/pool/main/g/gnome-session/%{name}_%{version}-%{tarball_version}_amd64.deb


Requires: gnome-session

BuildRequires: tar
BuildRequires: zstd

%description
gnome-startup-applications a tool ported from ubuntu, which allows for a more powerful management of startup applications than the one found in gnome-tweaks.

%prep
mkdir -p "%{name}_%{version}-%{tarball_version}"

ar x --output . %{SOURCE0}
tar -xC "%{name}_%{version}-%{tarball_version}" -f data.tar.zst

%install
mkdir -p %{buildroot}
cp -r "%{name}_%{version}-%{tarball_version}"/* %{buildroot}/
mkdir -p "%{buildroot}/%{_datadir}/licenses/%{name}"
mv "%{buildroot}/usr/share/doc/gnome-startup-applications/copyright" "%{buildroot}/%{_datadir}/licenses/%{name}/LICENSE"
mkdir -p "%{buildroot}/%{_datadir}/doc/%{name}/copyright"
mv "%{buildroot}/usr/share/doc/gnome-startup-applications/changelog.Debian.gz" "%{buildroot}/%{_datadir}/doc/%{name}/changelog"

%files
%{_bindir}/gnome-session-properties
%{_datadir}/applications/gnome-session-properties.desktop
%{_datadir}/doc/gnome-startup-applications/changelog
%{_datadir}/licenses/gnome-startup-applications/LICENSE
%{_datadir}/gnome-session/session-properties.ui
%{_datadir}/icons/hicolor/16x16/session-properties.svg
%{_datadir}/icons/hicolor/22x22/session-properties.svg
%{_datadir}/icons/hicolor/32x32/session-properties.svg
%{_datadir}/icons/hicolor/scalable/apps/session-properties.svg
%{_datadir}/icons/hicolor/symbolic/session-properties-symbolic.svg
%{_datadir}/man/man1/gnome-session-properties.1.gz

