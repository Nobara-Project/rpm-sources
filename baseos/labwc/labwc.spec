%global forgeurl https://github.com/labwc/labwc
%global tag %{version}

Name:           labwc
Version:        0.20.2
%forgemeta
Release:        6%{?dist}
Summary:        A Wayland window-stacking compositor

License:        GPL-2.0-only AND MIT
URL:            %{forgeurl}
Source0:        %{forgesource}
Source1:        https://gitlab.freedesktop.org/wlroots/wlroots/-/archive/0.20.2/wlroots-0.20.2.tar.gz
Source2:        wlroots-0.20.2-background-blur.patch
Patch:          0001-add-per-output-hdr-overrides.patch
Patch:          0002-allow-moving-fullscreen-views-between-outputs.patch
Patch:          0003-defer-live-hdr-changes-to-next-frame.patch
Patch:          0004-snap-fullscreen-alt-drags-between-outputs.patch
Patch:          0005-modeset-and-roll-back-live-hdr-changes.patch
Patch:          0006-add-opt-in-background-blur.patch

BuildRequires:  gcc
BuildRequires:  meson >= 0.59.0
BuildRequires:  cmake

BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(libdrm) >= 2.4.129
BuildRequires:  pkgconfig(libinput) >= 1.26
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(librsvg-2.0) >= 2.46
BuildRequires:  pkgconfig(libsfdo-basedir) >= 0.1.3
BuildRequires:  pkgconfig(libsfdo-desktop) >= 0.1.3
BuildRequires:  pkgconfig(libsfdo-icon) >= 0.1.3
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(pangocairo)
BuildRequires:  pkgconfig(pixman-1) >= 0.43.0
BuildRequires:  pkgconfig(scdoc)
BuildRequires:  pkgconfig(systemd)
BuildRequires:  pkgconfig(wayland-protocols) >= 1.47
BuildRequires:  pkgconfig(wayland-server) >= 1.24.0
# Private static wlroots: scene blur needs render hooks unavailable in the ABI.
# Keep the system wlroots package and all its headers/libraries untouched.
BuildRequires:  glslang
BuildRequires:  hwdata-devel
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(glesv2)
BuildRequires:  pkgconfig(vulkan) >= 1.2.182
BuildRequires:  pkgconfig(lcms2)
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(libseat) >= 0.2.0
BuildRequires:  pkgconfig(libdisplay-info) >= 0.2.0
BuildRequires:  pkgconfig(libliftoff) >= 0.4.0
BuildRequires:  pkgconfig(wayland-client) >= 1.24.0
BuildRequires:  pkgconfig(xcb-composite)
BuildRequires:  pkgconfig(xcb-dri3)
BuildRequires:  pkgconfig(xcb-errors)
BuildRequires:  pkgconfig(xcb-present)
BuildRequires:  pkgconfig(xcb-render)
BuildRequires:  pkgconfig(xcb-renderutil)
BuildRequires:  pkgconfig(xcb-res)
BuildRequires:  pkgconfig(xcb-shm)
BuildRequires:  pkgconfig(xcb-xfixes)
BuildRequires:  pkgconfig(xcb-xinput)
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(xcb-ewmh)
BuildRequires:  pkgconfig(xcb-icccm)
BuildRequires:  pkgconfig(xkbcommon) >= 1.8.0
BuildRequires:  pkgconfig(xwayland) >= 21.1.9

Provides:       bundled(wlroots) = 0.20.2

Requires:       mesa-dri-drivers
Requires:       xdg-desktop-portal-wlr

Conflicts:      %{name} < 0.8.2-3
Obsoletes:      %{name} < 0.8.2-3

%description
Labwc stands for Lab Wayland Compositor, where lab can mean any of the
following:

  * lightweight and *box-inspired
  * sense of experimentation and treading new ground
  * inspired by BunsenLabs and ArchLabs
  * your favorite pet

Labwc is a wlroots-based window-stacking compositor for Wayland, inspired by
Openbox.

It is lightweight and independent with a focus on simply stacking windows well
and rendering some window decorations. It takes a no-bling/frills approach and
says no to features such as animations. It relies on clients for panels,
screenshots, wallpapers and so on to create a full desktop environment.

Labwc tries to stay in keeping with wlroots and sway in terms of general
approach and coding style.

Labwc has no reliance on any particular Desktop Environment, Desktop Shell or
session. Nor does it depend on any UI toolkits such as Qt or GTK.

%package session
Summary:        A Wayland window-stacking compositor - session files
Requires:       %{name} = %{version}-%{release}
Requires:       hicolor-icon-theme
# Upstream recommendations
# https://github.com/labwc/labwc?tab=readme-ov-file#6-integration
# See integration[1] for further details.
# [1]: https://labwc.github.io/integration.html
Recommends:     bemenu                                %dnl # Launchers
Recommends:     swaylock                              %dnl # Screen locker
Suggests:       alacritty                             %dnl # Terminal
Suggests:       fuzzel wofi                           %dnl # Launchers
Suggests:       grim                                  %dnl # Screen-shooter
Suggests:       swaybg                                %dnl # Background image
Suggests:       waybar, yambar, lavalauncher, sfwbar  %dnl # Panel
Suggests:       wf-recorder                           %dnl # Screen recorder
Suggests:       wlopm, kanshi, wlr-randr              %dnl # Output managers
# Downstream useful packages already available in Fedora/Nobara
Suggests:       foot                                  %dnl # Terminal
Suggests:       wdisplays                             %dnl # GUI display configurator

Conflicts:      %{name} < 0.8.2-3
Obsoletes:      %{name} < 0.8.2-3

BuildArch:      noarch

%description session
This package provides the labwc session files to run labwc as a
standalone environment.


%prep
%forgeautosetup -p1
%{__tar} -xf %{SOURCE1} -C subprojects
mv subprojects/wlroots-0.20.2 subprojects/wlroots
%{__patch} -d subprojects/wlroots -p1 < %{SOURCE2}
cp subprojects/wlroots/LICENSE WLROOTS-LICENSE


%build
%meson \
    --wrap-mode=nodownload \
    --force-fallback-for=wlroots-0.20 \
    -Dxwayland=enabled \
    -Dwlroots:default_library=static \
    -Dwlroots:install=false \
    -Dwlroots:examples=false \
    -Dwlroots:background-blur-tests=true \
    -Dwlroots:renderers=gles2,vulkan \
    -Dwlroots:backends=drm,libinput,x11 \
    -Dwlroots:allocators=gbm,udmabuf \
    -Dwlroots:color-management=enabled \
    %{nil}
%meson_build


%check
%meson_test


%install
%meson_install
%find_lang %{name}


%files -f %{name}.lang
%license LICENSE WLROOTS-LICENSE
%doc NEWS.md
%{_bindir}/%{name}
%{_bindir}/lab-sensible-terminal
%{_bindir}/labnag
%{_docdir}/%{name}/*
%{_mandir}/man1/*.1*
%{_mandir}/man5/*.5*
%{_datadir}/xdg-desktop-portal/labwc-portals.conf

%files session
%{_datadir}/wayland-sessions/%{name}.desktop
%{_datadir}/icons/hicolor/*/*/%{name}*.svg
%{_userunitdir}/labwc-session.target

%changelog
* Thu Sep 24 2026 Nobara Project - 0.20.2-6
- Add opt-in live background blur for Wayland surfaces, preserving HDR rendering
- Support standard background-effect regions and independent shell blur strength
- Link a private patched wlroots statically without installing wlroots files
- Verify backdrop clipping, sharp foregrounds, occlusion, damage, and idle rendering

* Tue Sep 01 2026 GloriousEggroll <gloriouseggroll@gmail.com> - 0.20.2-5
- Use modeset-capable atomic commits for dynamic HDR transitions
- Restore the previous output state if an HDR transition is rejected

* Tue Sep 01 2026 GloriousEggroll <gloriouseggroll@gmail.com> - 0.20.2-4
- Defer dynamic HDR changes to frame boundaries to avoid DRM page-flip races
- Snap fullscreen and maximized Alt-drags to the output under the cursor

* Tue Sep 01 2026 GloriousEggroll <gloriouseggroll@gmail.com> - 0.20.2-3
- Allow interactive moves to transfer fullscreen windows between outputs

* Tue Sep 01 2026 GloriousEggroll <gloriouseggroll@gmail.com> - 0.20.2-2
- Add dynamically reloadable per-output HDR overrides

* Mon Aug 31 2026 GloriousEggroll <gloriouseggroll@gmail.com> - 0.20.2-1
- Update to labwc 0.20.2
- Enable upstream HDR10 and Wayland color-management support
