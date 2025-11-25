# Binary package, no debuginfo should be generated
%global debug_package %{nil}

%global appstream_id com.valvesoftware.Steam

Name:           steam
Version:        1.0.0.85
Release:        1%{?dist}
Summary:        Installer for the Steam software distribution service
# Redistribution and repackaging for Linux is allowed, see license file. udev rules are MIT.
License:        Steam License Agreement and MIT
URL:            http://www.steampowered.com/
ExclusiveArch:  i686

Source0:        https://repo.steampowered.com/%{name}/archive/beta/%{name}_%{version}.tar.gz
Source1:        %{name}.sh
Source2:        %{name}.csh
Source3:        README.Fedora
# Load ntsync at boot. Might be reverted depending on https://fedoraproject.org/wiki/Changes/NTSYNC
Source4:        ntsync.conf

# Ghost touches in Big Picture mode:
# https://github.com/ValveSoftware/steam-for-linux/issues/3384
# https://bugzilla.kernel.org/show_bug.cgi?id=28912
# https://github.com/denilsonsa/udev-joystick-blacklist
# https://github.com/systemd/systemd/issues/32773

# Configure limits in systemd
Source7:        01-steam.conf

# Do not install desktop file in lib/steam, do not install apt sources
Patch0:         %{name}-makefile.patch

# Nobara changes
Patch2:         nobara-changes.patch


BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
BuildRequires:  make
BuildRequires:  systemd

# Required to run the initial setup
Requires:       tar
Requires:       zenity

# Most games use OpenGL, some games already use Vulkan. Vulkan is also required
# for Steam Play to run Windows games through emulation. i686 version of these
# packages are necessary even on x86_64 systems for running 32bit games. Pull in
# native arch drivers as well, by not specifying _isa macro, native arch
# packages are preferred. This will make sure people have all necessary drivers
# for both i686 and x86_64 games.
Requires:       mesa-dri-drivers%{?_isa}
Requires:       mesa-dri-drivers
Requires:       mesa-vulkan-drivers%{?_isa}
Requires:       mesa-vulkan-drivers
Requires:       vulkan-loader%{?_isa}
Requires:       vulkan-loader

# Minimum requirements for starting the steam client using system libraries
Requires:       alsa-lib%{?_isa}
Requires:       fontconfig%{?_isa}
Requires:       gtk2%{?_isa}
Requires:       libICE%{?_isa}
Requires:       libnsl%{?_isa}
Requires:       libpng%{?_isa}
Requires:       libXext%{?_isa}
Requires:       libXinerama%{?_isa}
Requires:       libXtst%{?_isa}
Requires:       libXScrnSaver%{?_isa}
Requires:       mesa-libGL%{?_isa}
Requires:       mesa-libEGL%{?_isa}
Requires:       NetworkManager-libnm%{?_isa}
Requires:       nss%{?_isa}
Requires:       pulseaudio-libs%{?_isa}

# Required for sending out crash reports to Valve
Requires:       libcurl%{?_isa}

# Workaround for mesa-libGL dependency bug:
# https://bugzilla.redhat.com/show_bug.cgi?id=1168475
Requires:       systemd-libs%{?_isa}

# Required for the firewall rules
# http://fedoraproject.org/wiki/PackagingDrafts/ScriptletSnippets/Firewalld
Requires:       firewalld-filesystem
Requires(post): firewalld-filesystem

# Required for hardware encoding/decoding during Remote Play (intel/radeon/amdgpu/nouveau)
Requires:       libva%{?_isa}
Requires:       libvdpau%{?_isa}

# Required by Feral interactive games
Requires:       libatomic%{?_isa}

# Required by Shank
Requires:       (alsa-plugins-pulseaudio%{?_isa} if pulseaudio)
Requires:       (pipewire-alsa%{?_isa} if pipewire)

# Patched for Wayland
# https://github.com/ValveSoftware/steam-for-linux/issues/8853
# https://github.com/negativo17/steam/issues/9
%if 0%{?fedora}
Requires:       SDL2%{?_isa}
%endif

# Game performance is increased with gamemode (for games that support it)
Recommends:     gamemode
Recommends:     gamemode%{?_isa}
Recommends:     (gnome-shell-extension-appindicator if gnome-shell)

# Proton uses xdg-desktop-portal to open URLs from inside a container
Requires:       xdg-desktop-portal
Recommends:     (xdg-desktop-portal-gtk if gnome-shell)
Recommends:     (xdg-desktop-portal-kde if kwin)

# Prevent log spam when thse are not pulled in as dependencies of full desktops
Recommends:     dbus-x11
Recommends:     xdg-user-dirs

# Allow using Steam Runtime Launch Options
Recommends:     gobject-introspection

Requires:       steam-devices

%description
Steam is a software distribution service with an online store, automated
installation, automatic updates, achievements, SteamCloud synchronized savegame
and screenshot functionality, and many social features.

This package contains the installer for the Steam software distribution service.

%prep
%autosetup -p1 -n %{name}-launcher

cp %{SOURCE3} .

%build
# Nothing to build

%install
%make_install

rm -fr %{buildroot}%{_docdir}/%{name}/ \
    %{buildroot}%{_bindir}/%{name}deps

# Environment files
mkdir -p %{buildroot}%{_sysconfdir}/profile.d
install -pm 644 %{SOURCE1} %{SOURCE2} %{buildroot}%{_sysconfdir}/profile.d

# Raise file descriptor limit
mkdir -p %{buildroot}%{_prefix}/lib/systemd/system.conf.d/
mkdir -p %{buildroot}%{_prefix}/lib/systemd/user.conf.d/
install -m 644 -p %{SOURCE7} %{buildroot}%{_prefix}/lib/systemd/system.conf.d/
install -m 644 -p %{SOURCE7} %{buildroot}%{_prefix}/lib/systemd/user.conf.d/

# Fixes steam open/close loop bug:
# https://github.com/ValveSoftware/steam-for-linux/issues/8179
sed -i 's|PrefersNonDefaultGPU=true|PrefersNonDefaultGPU=false|g' %{buildroot}%{_datadir}/applications/%{name}.desktop

%if 0%{?fedora}
mkdir -p %{buildroot}%{_modulesloaddir}
install -m 644 -p %{SOURCE4} %{buildroot}%{_modulesloaddir}/
%endif

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{appstream_id}.metainfo.xml

%files
%license COPYING steam_subscriber_agreement.txt
%doc debian/changelog README.Fedora
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/pixmaps/%{name}_tray_mono.png
%{_libdir}/%{name}/
%{_mandir}/man6/%{name}.*
%{_metainfodir}/%{appstream_id}.metainfo.xml
%config(noreplace) %{_sysconfdir}/profile.d/%{name}.*sh
%dir %{_prefix}/lib/systemd/system.conf.d/
%{_prefix}/lib/systemd/system.conf.d/01-steam.conf
%dir %{_prefix}/lib/systemd/user.conf.d/
%{_prefix}/lib/systemd/user.conf.d/01-steam.conf
%if 0%{?fedora}
%{_modulesloaddir}/ntsync.conf
%endif

%changelog
* Fri Oct 17 2025 Simone Caronni <negativo17@gmail.com> - 1.0.0.85-1
- Update to 1.0.0.85.

* Sat Sep 06 2025 Simone Caronni <negativo17@gmail.com> - 1.0.0.83-3
- Load ntsync module.

* Mon Jul 28 2025 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.0.0.83-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun May 11 2025 Simone Caronni <negativo17@gmail.com> - 1.0.0.83-1
- Update to 1.0.0.83.

* Wed Apr 09 2025 Simone Caronni <negativo17@gmail.com> - 1.0.0.82-4
- Drop steam-devices subpackage.

* Wed Mar 19 2025 Simone Caronni <negativo17@gmail.com> - 1.0.0.82-3
- Relax requirement on steam-devices.
- Trim changelog.
- Update README.

* Wed Jan 29 2025 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.0.0.82-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sun Nov 10 2024 Simone Caronni <negativo17@gmail.com> - 1.0.0.82-1
- Update to 1.0.0.82.

* Sun Sep 01 2024 Simone Caronni <negativo17@gmail.com> - 1.0.0.81-1
- Update to 1.0.0.81.

* Mon Aug 05 2024 Simone Caronni <negativo17@gmail.com> - 1.0.0.79-7
- Fix for Wayland on Fedora 40.

* Sat Aug 03 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.0.0.79-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jun 24 2024 Simone Caronni <negativo17@gmail.com> - 1.0.0.79-5
- Update udev rules.
- Convert udev rule for blocking wrong joystick devices to a systemd hwdb file:
  https://github.com/denilsonsa/udev-joystick-blacklist/issues/58

* Tue May 28 2024 Simone Caronni <negativo17@gmail.com> - 1.0.0.79-4
- Add dependencies when full desktop is not installed.
- Add dependencies for using steam-runtime-launch-options.

* Tue Mar 19 2024 Simone Caronni <negativo17@gmail.com> - 1.0.0.79-3
- Adjust dependencies.

* Sun Feb 18 2024 Simone Caronni <negativo17@gmail.com> - 1.0.0.79-2
- Re-add gnome-shell-extension-appindicator recommendation.

* Sun Feb 18 2024 Simone Caronni <negativo17@gmail.com> - 1.0.0.79-1
- Update to 1.0.0.79.
- Drop gnome-shell-extension-gamemode recommendation (#6853).
- Update udev rules.

* Sun Feb 04 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.0.0.78-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild
