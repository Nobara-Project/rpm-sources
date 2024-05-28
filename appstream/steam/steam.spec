# Binary package, no debuginfo should be generated
%global debug_package %{nil}

%global appstream_id com.valvesoftware.Steam

Name:           steam
Version:        1.0.0.79
Release:        11%{?dist}
Summary:        Installer for the Steam software distribution service
# Redistribution and repackaging for Linux is allowed, see license file. udev rules are MIT.
License:        Steam License Agreement and MIT
URL:            http://www.steampowered.com/
ExclusiveArch:  i686

Source0:        https://repo.steampowered.com/%{name}/archive/beta/%{name}_%{version}.tar.gz
Source1:        %{name}.sh
Source2:        %{name}.csh
Source5:        README.Fedora

# Ghost touches in Big Picture mode:
# https://github.com/ValveSoftware/steam-for-linux/issues/3384
# https://bugzilla.kernel.org/show_bug.cgi?id=28912
# https://github.com/denilsonsa/udev-joystick-blacklist

# Input devices seen as joysticks:
Source6:        https://raw.githubusercontent.com/denilsonsa/udev-joystick-blacklist/master/after_kernel_4_9/51-these-are-not-joysticks-rm.rules

# Configure limits in systemd
Source7:        01-steam.conf

# Newer udev rules than what is bundled in the tarball
Source8:        https://raw.githubusercontent.com/ValveSoftware/steam-devices/master/60-steam-input.rules
Source9:        https://raw.githubusercontent.com/ValveSoftware/steam-devices/master/60-steam-vr.rules

# Provide alternative icon for Remote Play
Source10:       remote-play.svg

# Steam Restart script
Source11:       steamrestart.sh

# Do not install desktop file in lib/steam, do not install apt sources
Patch0:         %{name}-makefile.patch
# Copy desktop shortcut from /usr/share/applications, not /usr/lib/steam/
Patch1:         %{name}-icon-desktop.patch

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
Requires:       libxcrypt-compat%{?_isa}
Requires:       libpng12%{?_isa}
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

# Required for having a functioning menu on the tray icon
Requires:       libdbusmenu-gtk3%{?_isa} >= 16.04.0

# Required by Feral interactive games
Requires:       libatomic%{?_isa}

# Required by Shank
Requires:       (alsa-plugins-pulseaudio%{?_isa} if pulseaudio)
Requires:       (pipewire-alsa%{?_isa} if pipewire)

# Game performance is increased with gamemode (for games that support it)
Recommends:     gamemode
Recommends:     gamemode%{?_isa}
Recommends:     (gnome-shell-extension-appindicator if gnome-shell)

# Proton uses xdg-desktop-portal to open URLs from inside a container
Requires:       xdg-desktop-portal
Recommends:     (xdg-desktop-portal-gtk if gnome-shell)
Recommends:     (xdg-desktop-portal-kde if kwin)

Requires:       steam-devices = %{?epoch:%{epoch}:}%{version}-%{release}

%description
Steam is a software distribution service with an online store, automated
installation, automatic updates, achievements, SteamCloud synchronized savegame
and screenshot functionality, and many social features.

This package contains the installer for the Steam software distribution service.

%package        devices
Summary:        Permissions required by Steam for gaming devices
# Until the infra can deal with noarch sub-packages from excludearch/exclusivearch
# keep the sub-package arched
#BuildArch:      noarch
Provides:       steam-devices = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      steam-devices < %{?epoch:%{epoch}:}%{version}-%{release}

%description    devices
Steam is a software distribution service with an online store, automated
installation, automatic updates, achievements, SteamCloud synchronized savegame
and screenshot functionality, and many social features.

This package contains the necessary permissions for gaming devices.

%prep
%autosetup -p1 -n %{name}-launcher

cp %{SOURCE5} .

%build
# Nothing to build

%install
%make_install

rm -fr %{buildroot}%{_docdir}/%{name}/ \
    %{buildroot}%{_bindir}/%{name}deps

mkdir -p %{buildroot}%{_udevrulesdir}/
install -m 644 -p %{SOURCE6} %{SOURCE8} %{SOURCE9} \
    %{buildroot}%{_udevrulesdir}/

# Environment files
mkdir -p %{buildroot}%{_sysconfdir}/profile.d
install -pm 644 %{SOURCE1} %{SOURCE2} %{buildroot}%{_sysconfdir}/profile.d

# Raise file descriptor limit
mkdir -p %{buildroot}%{_prefix}/lib/systemd/system.conf.d/
mkdir -p %{buildroot}%{_prefix}/lib/systemd/user.conf.d/
mkdir -p %{buildroot}%{_bindir}/
install -m 644 -p %{SOURCE7} %{buildroot}%{_prefix}/lib/systemd/system.conf.d/
install -m 644 -p %{SOURCE7} %{buildroot}%{_prefix}/lib/systemd/user.conf.d/
install -m 775 -p %{SOURCE11} %{buildroot}%{_bindir}/steamrestart

# Fixes steam open/close loop bug:
# https://github.com/ValveSoftware/steam-for-linux/issues/8179
sed -i 's|PrefersNonDefaultGPU=true|PrefersNonDefaultGPU=false|g' %{buildroot}%{_datadir}/applications/%{name}.desktop

# Use steamdeck interface
sed -i 's|Exec=.*|Exec=/usr/bin/steam %U|g' %{buildroot}%{_datadir}/applications/%{name}.desktop

# Add host remote play shortcut with -pipewire for wayland compatibility
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/
mkdir -p %{buildroot}%{_sysconfdir}/skel/Desktop/
cp %{SOURCE10} %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/
cp %{buildroot}%{_datadir}/applications/%{name}.desktop %{buildroot}%{_sysconfdir}/skel/Desktop/%{name}.desktop

cp %{buildroot}%{_datadir}/applications/%{name}.desktop %{buildroot}%{_datadir}/applications/RemoteHost.desktop
sed -i 's|Icon=steam|Icon=remote-play|g' %{buildroot}%{_datadir}/applications/RemoteHost.desktop
sed -i 's|Exec=.*|Exec=/usr/bin/steamrestart \&\& /usr/bin/steam -pipewire %U|g' %{buildroot}%{_datadir}/applications/RemoteHost.desktop
sed -i 's|Name=.*|Name=Host Remote Play|g' %{buildroot}%{_datadir}/applications/RemoteHost.desktop
cp %{buildroot}%{_datadir}/applications/RemoteHost.desktop %{buildroot}%{_sysconfdir}/skel/Desktop/RemoteHost.desktop

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{appstream_id}.metainfo.xml

%files
%license COPYING steam_subscriber_agreement.txt
%doc debian/changelog README.Fedora
%{_bindir}/%{name}
%{_bindir}/steamrestart
%{_datadir}/applications/%{name}.desktop
%{_datadir}/applications/RemoteHost.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_datadir}/icons/hicolor/scalable/apps/remote-play.svg
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/pixmaps/%{name}_tray_mono.png
%{_libdir}/%{name}/
%{_sysconfdir}/skel/Desktop/*
%{_mandir}/man6/%{name}.*
%{_metainfodir}/%{appstream_id}.metainfo.xml
%config(noreplace) %{_sysconfdir}/profile.d/%{name}.*sh
%dir %{_prefix}/lib/systemd/system.conf.d/
%{_prefix}/lib/systemd/system.conf.d/01-steam.conf
%dir %{_prefix}/lib/systemd/user.conf.d/
%{_prefix}/lib/systemd/user.conf.d/01-steam.conf

%files devices
%{_udevrulesdir}/*

%changelog
* Sun Feb 18 2024 Simone Caronni <negativo17@gmail.com> - 1.0.0.79-2
- Re-add gnome-shell-extension-appindicator recommendation.

* Sun Feb 18 2024 Simone Caronni <negativo17@gmail.com> - 1.0.0.79-1
- Update to 1.0.0.79.
- Drop gnome-shell-extension-gamemode recommendation (#6853).
- Update udev rules.

* Sun Feb 04 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.0.0.78-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Aug 03 2023 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.0.0.78-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri May 12 2023 Simone Caronni <negativo17@gmail.com> - 1.0.0.78-1
- Update to 1.0.0.78.

* Tue Mar 07 2023 Simone Caronni <negativo17@gmail.com> - 1.0.0.76-1
- Update to 1.0.0.76.
- Separate SPEC file per distribution.
- Trim changelog.

* Mon Aug 08 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.0.0.75-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild and ffmpeg
  5.1

* Fri Jul 22 2022 Simone Caronni <negativo17@gmail.com> - 1.0.0.75-1
- Update to 1.0.0.75.

* Fri Feb 04 2022 Simone Caronni <negativo17@gmail.com> - 1.0.0.74-2
- Add gnome-shell-extension-appindicator if running on Gnome (#6194).
- Require libICE to avoid spamming the console. It's installed by default on a
  Gnome installation but not explicitly required (#6195).

* Fri Dec 10 2021 Simone Caronni <negativo17@gmail.com> - 1.0.0.74-1
- Update to 1.0.0.74.

* Sat Nov 20 2021 Simone Caronni <negativo17@gmail.com> - 1.0.0.73-1
- Update to 1.0.0.73.

* Sat Oct 09 2021 Simone Caronni <negativo17@gmail.com> - 1.0.0.72-1
- Update to 1.0.0.72.

* Fri Aug 27 2021 Simone Caronni <negativo17@gmail.com> - 1.0.0.71-4
- Remove old noruntime provide/obsolete.
- Remove VA-API driver dependencies for RHEL/CentOS 7 and update relevant
  information.
- Remove not really relevant information about controllers from the readme.
- Update steam-devices.

* Wed Aug 25 2021 Nicolas Chauvet <kwizart@gmail.com> - 1.0.0.71-3
- Keep the stream-devices sub-package arched

* Sun Aug 15 2021 Simone Caronni <negativo17@gmail.com> - 1.0.0.71-2
- Steam UDEV subpackage should be noarch.

* Sun Aug 15 2021 Simone Caronni <negativo17@gmail.com> - 1.0.0.71-1
- Update to 1.0.0.71.
- Update README.Fedora with supported controllers.
- Use bundled AppData.

* Wed Aug 04 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.0.0.70-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jun 30 2021 Simone Caronni <negativo17@gmail.com> - 1.0.0.70-4
- Separate udev rules in separate subpackage to be used also by Valve's Flatpak
  Steam client.
- Use upstream's udev rules as those are newer than what is bundled in the
  installer tarball.

* Tue May 04 2021 Leigh Scott <leigh123linux@gmail.com> - 1.0.0.70-3
- Fix appdata screenshots (rfbz#5984)

* Mon Apr 12 2021 Simone Caronni <negativo17@gmail.com> - 1.0.0.70-2
- Remove new desktop entry specification for Fedora 32 and RHEL/CentOS 7/8.

* Mon Apr 12 2021 Simone Caronni <negativo17@gmail.com> - 1.0.0.70-1
- Update to 1.0.0.70.
- Switch to tarball provided steam-devices udev rules.

* Thu Feb 04 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.0.0.68-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild
