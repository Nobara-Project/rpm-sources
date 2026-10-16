Name:           xdg-desktop-portal-wlr
Version:        0.8.4
Release:        2%{?dist}
Summary:        xdg-desktop-portal backend for wlroots

License:        MIT
URL:            https://github.com/emersion/%{name}
Source0:        %{url}/releases/download/v%{version}/%{name}-%{version}.tar.gz
Source1:        %{url}/releases/download/v%{version}/%{name}-%{version}.tar.gz.sig
Source2:        https://emersion.fr/.well-known/openpgpkey/hu/dj3498u4hyyarh35rkjfnghbjxug6b19#/gpgkey-0FDE7BE0E88F5E48.gpg
# Generic portals.conf(5) for any wlroots-based compositor.
# Can be loaded by setting XDG_CURRENT_DESKTOP=<compositor>:wlroots
Source3:        wlroots-portals.conf

# Preserve the selected monitor's Wayland image description in PipeWire
Patch0:         0001-screencast-publish-Wayland-output-colorimetry.patch

BuildRequires:  gcc
BuildRequires:  gnupg2
BuildRequires:  meson
BuildRequires:  systemd-rpm-macros

BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(inih)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libpipewire-0.3)
BuildRequires:  pkgconfig(libspa-0.2)
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:  pkgconfig(scdoc)
BuildRequires:  pkgconfig(systemd)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-protocols) >= 1.47
BuildRequires:  pkgconfig(wayland-scanner)

Requires:       dbus
# required for Screenshot portal implementation
Requires:       grim
Requires:       xdg-desktop-portal
# required for Screencast output selection.
# xdpw will try to use first available of the 3 utilities
Recommends:     (slurp or wofi or bemenu)
Suggests:       slurp

Enhances:       sway
Supplements:    (sway and (flatpak or snapd))

%description
%{summary}.
This project seeks to add support for the screenshot, screencast, and possibly
remote-desktop xdg-desktop-portal interfaces for wlroots based compositors.


%prep
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%autosetup -p1


%build
%meson \
    -Dsd-bus-provider=libsystemd
%meson_build


%install
%meson_install
install -D -pv -m644 %{SOURCE3} \
    %{buildroot}%{_datadir}/xdg-desktop-portal/wlroots-portals.conf


%post
%systemd_user_post %{name}.service

%preun
%systemd_user_preun %{name}.service


%files
%license LICENSE
%doc README.md contrib/config.sample
%{_libexecdir}/%{name}
%{_mandir}/man5/%{name}.5*
%{_datadir}/xdg-desktop-portal/portals/wlr.portal
%{_datadir}/xdg-desktop-portal/wlroots-portals.conf
%{_datadir}/dbus-1/services/*.service
%{_userunitdir}/%{name}.service


%changelog
* Tue Sep 01 2026 Nobara Project <nobara@protonmail.com> - 0.8.4-2
- Publish Wayland output colorimetry on PipeWire monitor-capture streams

* Sun Aug 02 2026 Aleksei Bavshin <alebastr@fedoraproject.org> - 0.8.4-1
- Update to 0.8.4 (#2490450)

* Fri Jul 17 2026 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_45_Mass_Rebuild

* Sat Apr 18 2026 Aleksei Bavshin <alebastr@fedoraproject.org> - 0.8.2-1
- Update to 0.8.2 (#2459226)

* Thu Mar 26 2026 Aleksei Bavshin <alebastr@fedoraproject.org> - 0.8.1-3
- Apply patches to fix screensharing with pipewire 1.6

* Sat Jan 17 2026 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Thu Dec 04 2025 Tomasz Hołubowicz <mail@alternateved.com> - 0.8.1-1
- Update to 0.8.1

* Tue Oct 21 2025 Tomasz Hołubowicz <mail@alternateved.com> - 0.8.0-1
- Update to 0.8.0

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jan 30 2024 Aleksei Bavshin <alebastr@fedoraproject.org> - 0.7.1-1
- Update to 0.7.1

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Sep 14 2023 Aleksei Bavshin <alebastr@fedoraproject.org> - 0.7.0-3
- Add wlroots-portals.conf for xdg-desktop-portal >= 1.17

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sun Apr 16 2023 Aleksei Bavshin <alebastr@fedoraproject.org> - 0.7.0-1
- Update to 0.7.0

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Dec 13 2022 Aleksei Bavshin <alebastr@fedoraproject.org> - 0.6.0-3
- Recommend only one chooser of 3 supported, prefer slurp.
- Add missing BR: pkgconfig(systemd)
- Add upstream patch for screenshot portal version
- Convert License tag to SPDX

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jun 09 2022 Aleksei Bavshin <alebastr@fedoraproject.org> - 0.6.0-1
- Update to 0.6.0

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Nov 05 2021 Aleksei Bavshin <alebastr@fedoraproject.org> - 0.5.0-1
- Update to 0.5.0

* Wed Nov 03 2021 Aleksei Bavshin <alebastr@fedoraproject.org> - 0.4.0-3
- Apply upstream patch for invalid screencast node_id (#2008645)

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jun 01 2021 Aleksei Bavshin <alebastr@fedoraproject.org> - 0.4.0-1
- Update to 0.4.0

* Sun Apr 18 2021 Aleksei Bavshin <alebastr@fedoraproject.org> - 0.3.0-1
- Update to 0.3.0

* Mon Feb 15 2021 Aleksei Bavshin <alebastr@fedoraproject.org> - 0.2.0-1
- Update to 0.2.0
- Drop versioned pipewire dependency: all supported Fedora releases have required version.

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed May 06 2020 Aleksei Bavshin <alebastr89@gmail.com> - 0.1.0-1
- Initial import (#1831981)
