Name:           lact
Version:        0.9.0
Release:        2
Summary:        GPU control utility
SourceLicense:  MIT
License:        Zlib AND (MIT OR Zlib OR Apache-2.0) AND MPL-2.0 AND (MIT OR Apache-2.0 OR LGPL-2.1-or-later) AND BSD-3-Clause AND CC0-1.0 AND CDLA-Permissive-2.0 AND LGPL-3.0-or-later AND (Apache-2.0 WITH LLVM-exception OR Apache-2.0 OR MIT) AND (Apache-2.0 OR MIT) AND (Apache-2.0 OR ISC OR MIT) AND (MIT OR Apache-2.0) AND Unicode-3.0 AND (0BSD OR MIT OR Apache-2.0) AND Apache-2.0 AND ISC AND (Apache-2.0 OR BSL-1.0) AND (Apache-2.0 OR GPL-2.0-only)
URL:            https://github.com/ilya-zlobintsev/LACT
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz

ExcludeArch:    %{ix86}

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  cargo-rpm-macros
BuildRequires:	systemd-rpm-macros
BuildRequires:	clang-devel
BuildRequires:	libadwaita-devel
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(libdrm)
BuildRequires:	pkgconfig(cairo)
BuildRequires:	pkgconfig(cairo-gobject)
BuildRequires:	pkgconfig(graphene-gobject-1.0)
BuildRequires:	pkgconfig(hwdata)
BuildRequires:	pkgconfig(gtk4)
BuildRequires:	pkgconfig(gdk-pixbuf-2.0)
Requires:       gtk4
Requires:       libdrm
Requires:       ocl-icd
Requires:       hwdata
Requires:       vulkan-tools
Requires:       libadwaita

Provides:       LACT

%description
GPU control utility

%prep
%setup -q -n LACT-%{version}

%build
VERGEN_GIT_SHA=454a6e2 make build-release %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install PREFIX=/usr DESTDIR=%{buildroot}

%post
%systemd_post lactd.service

%preun
%systemd_preun lactd.service

%postun
%systemd_postun_with_restart lactd.service

%files
%defattr(-,root,root,-)
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_unitdir}/lactd.service
%{_datadir}/applications/io.github.ilya_zlobintsev.LACT.desktop
%{_iconsdir}/hicolor/scalable/apps/io.github.ilya_zlobintsev.LACT.svg
%{_iconsdir}/hicolor/512x512/apps/io.github.ilya_zlobintsev.LACT.png

# Nobara doesn't support AppStream MetaInfo so there's no reason to include this
%ghost %{_metainfodir}/io.github.ilya_zlobintsev.LACT.metainfo.xml

%changelog
* Fri May 08 2026 Owen Zimmerman <owen@fyralabs.com> - 0.9.0-2
- Use systemd macros, add missing deps, fix ocl-icd dep,
- use pkgconfig, use %%{_iconsidr}, add dep licenses,
- add `Provides:`, bump VERGEN_GIT_SHA, ghost metainfo

* Thu May 07 2026 Owen Zimmerman <owen@fyralabs.com> - 0.9.0-1
- Update to 0.9.0

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
