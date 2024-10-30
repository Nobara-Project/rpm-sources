Name:           kde-steamdeck
Version:        6.2.2.git.84.1c1d05a9
Release:        1%{?dist}
Summary:        KDE Presets from Valve's SteamOS 3.0
License:    	GPLv2
URL:            https://github.com/nobara-project/steamdeck-edition-packages
Source0:        %{URL}/releases/download/1.0/kde-steamdeck.tar.gz
BuildArch:      noarch

Requires:		kde-filesystem
Requires:       kde-steamdeck-additions

Conflicts:  	steamdeck-kde-themes
Obsoletes:      steamdeck-kde-presets

%description
KDE Presets from Valve's SteamOS 3.0

%package sddm
Provides:       kde-steamdeck-sddm
Obsoletes:      sddm-sugar-steamOS

Summary: SteamOS 3.0 sddm theme

License: GPLv2+ or LGPLv3+

%description sddm

SteamOS 3.0 sddm theme

# Disable debug packages
%define debug_package %{nil}

%prep
%setup -T -b 0 -q -n kde-steamdeck

%build

%install
mkdir -p %{buildroot}%{_datadir}/
mkdir -p %{buildroot}%{_sysconfdir}/
cp -rv usr/share/* %{buildroot}%{_datadir}
cp -rv etc/* %{buildroot}%{_sysconfdir}

# Do post-installation
%post

# Do before uninstallation
%preun

# Do after uninstallation
%postun

# This lists all the files that are included in the rpm package and that
# are going to be installed into target system where the rpm is installed.
%files
%license LICENSE
%{_datadir}/color-schemes/Vapor.colors
%{_datadir}/color-schemes/VGUI.colors
%{_sysconfdir}/xdg/gtk-2.0/gtkrc
%{_sysconfdir}/xdg/gtk-3.0/settings.ini
%{_sysconfdir}/xdg/kcminputrc
%{_sysconfdir}/xdg/kdeglobals
%{_sysconfdir}/xdg/kscreenlockerrc
%{_sysconfdir}/xdg/kwinrc
%{_sysconfdir}/xdg/kwinrulesrc
%{_sysconfdir}/xdg/plasma-nm
%{_sysconfdir}/xdg/powermanagementprofilesrc
%{_sysconfdir}/xdg/startkderc
%{_datadir}/konsole/Vapor.colorscheme
%{_datadir}/konsole/Vapor.profile
%{_datadir}/plasma/avatars/Portal2/atlas.png
%{_datadir}/plasma/avatars/Portal2/atlas_eye.png
%{_datadir}/plasma/avatars/Portal2/chell.png
%{_datadir}/plasma/avatars/Portal2/companioncube.png
%{_datadir}/plasma/avatars/Portal2/peabody.png
%{_datadir}/plasma/avatars/Portal2/peabody_eye.png
%{_datadir}/plasma/avatars/Portal2/turret.png
%{_datadir}/plasma/avatars/Portal2/wheatley.png
%{_datadir}/plasma/avatars/circles/Cat.png
%{_datadir}/plasma/avatars/circles/Female.png
%{_datadir}/plasma/avatars/circles/Konqui.png
%{_datadir}/plasma/avatars/circles/Male.png
%{_datadir}/plasma/avatars/circles/Penguin.png
%{_datadir}/plasma/avatars/circles/Zebra.png
%{_datadir}/plasma/avatars/tf2/demoman.png
%{_datadir}/plasma/avatars/tf2/engineer.png
%{_datadir}/plasma/avatars/tf2/heavy.png
%{_datadir}/plasma/avatars/tf2/medic.png
%{_datadir}/plasma/avatars/tf2/pyro.png
%{_datadir}/plasma/avatars/tf2/scout.png
%{_datadir}/plasma/avatars/tf2/sniper.png
%{_datadir}/plasma/avatars/tf2/soldier.png
%{_datadir}/plasma/avatars/tf2/spy.png
%{_datadir}/plasma/desktoptheme/Vapor/colors
%{_datadir}/plasma/desktoptheme/Vapor/metadata.desktop
%{_datadir}/plasma/desktoptheme/Vapor/widgets/plasmoidheading.svg
%{_datadir}/plasma/look-and-feel/com.valve.vapor.desktop/contents/defaults
%{_datadir}/plasma/look-and-feel/com.valve.vapor.desktop/contents/icons/deck_icon.png
%{_datadir}/plasma/look-and-feel/com.valve.vapor.desktop/contents/plasmoidsetupscripts/org.kde.plasma.folder.js
%{_datadir}/plasma/look-and-feel/com.valve.vapor.desktop/contents/plasmoidsetupscripts/org.kde.plasma.kickoff.js
%{_datadir}/plasma/look-and-feel/com.valve.vapor.desktop/contents/plasmoidsetupscripts/org.kde.plasma.systemtray.js
%{_datadir}/plasma/look-and-feel/com.valve.vapor.desktop/contents/previews/preview.png
%{_datadir}/plasma/look-and-feel/com.valve.vapor.desktop/contents/splash/Splash.qml
%{_datadir}/plasma/look-and-feel/com.valve.vapor.desktop/contents/splash/images/busywidget.svgz
%{_datadir}/plasma/look-and-feel/com.valve.vapor.desktop/contents/splash/images/deck_logo.svgz
%{_datadir}/plasma/look-and-feel/com.valve.vapor.desktop/metadata.desktop
%{_datadir}/plasma/look-and-feel/com.valve.vapor.desktop/metadata.json
%{_datadir}/plasma/look-and-feel/com.valve.vgui.desktop/contents/defaults
%{_datadir}/plasma/look-and-feel/com.valve.vgui.desktop/contents/icons/deck_icon.png
%{_datadir}/plasma/look-and-feel/com.valve.vgui.desktop/contents/plasmoidsetupscripts/org.kde.plasma.folder.js
%{_datadir}/plasma/look-and-feel/com.valve.vgui.desktop/contents/plasmoidsetupscripts/org.kde.plasma.kickoff.js
%{_datadir}/plasma/look-and-feel/com.valve.vgui.desktop/contents/plasmoidsetupscripts/org.kde.plasma.systemtray.js
%{_datadir}/plasma/look-and-feel/com.valve.vgui.desktop/contents/previews/preview.png
%{_datadir}/plasma/look-and-feel/com.valve.vgui.desktop/contents/splash/Splash.qml
%{_datadir}/plasma/look-and-feel/com.valve.vgui.desktop/contents/splash/images/busywidget.svgz
%{_datadir}/plasma/look-and-feel/com.valve.vgui.desktop/contents/splash/images/deck_logo.svgz
%{_datadir}/plasma/look-and-feel/com.valve.vgui.desktop/metadata.desktop
%{_datadir}/plasma/look-and-feel/com.valve.vgui.desktop/metadata.json
%{_datadir}/themes/Vapor/assets/arrow-down-active.png
%{_datadir}/themes/Vapor/assets/arrow-down-hover.png
%{_datadir}/themes/Vapor/assets/arrow-down-insensitive.png
%{_datadir}/themes/Vapor/assets/arrow-down.png
%{_datadir}/themes/Vapor/assets/arrow-left-active.png
%{_datadir}/themes/Vapor/assets/arrow-left-hover.png
%{_datadir}/themes/Vapor/assets/arrow-left-insensitive.png
%{_datadir}/themes/Vapor/assets/arrow-left.png
%{_datadir}/themes/Vapor/assets/arrow-right-active.png
%{_datadir}/themes/Vapor/assets/arrow-right-hover.png
%{_datadir}/themes/Vapor/assets/arrow-right-insensitive.png
%{_datadir}/themes/Vapor/assets/arrow-right.png
%{_datadir}/themes/Vapor/assets/arrow-small-down-active.png
%{_datadir}/themes/Vapor/assets/arrow-small-down-hover.png
%{_datadir}/themes/Vapor/assets/arrow-small-down-insensitive.png
%{_datadir}/themes/Vapor/assets/arrow-small-down.png
%{_datadir}/themes/Vapor/assets/arrow-small-left-active.png
%{_datadir}/themes/Vapor/assets/arrow-small-left-hover.png
%{_datadir}/themes/Vapor/assets/arrow-small-left-insensitive.png
%{_datadir}/themes/Vapor/assets/arrow-small-left.png
%{_datadir}/themes/Vapor/assets/arrow-small-right-active.png
%{_datadir}/themes/Vapor/assets/arrow-small-right-hover.png
%{_datadir}/themes/Vapor/assets/arrow-small-right-insensitive.png
%{_datadir}/themes/Vapor/assets/arrow-small-right.png
%{_datadir}/themes/Vapor/assets/arrow-small-up-active.png
%{_datadir}/themes/Vapor/assets/arrow-small-up-hover.png
%{_datadir}/themes/Vapor/assets/arrow-small-up-insensitive.png
%{_datadir}/themes/Vapor/assets/arrow-small-up.png
%{_datadir}/themes/Vapor/assets/arrow-up-active.png
%{_datadir}/themes/Vapor/assets/arrow-up-hover.png
%{_datadir}/themes/Vapor/assets/arrow-up-insensitive.png
%{_datadir}/themes/Vapor/assets/arrow-up.png
%{_datadir}/themes/Vapor/assets/button-active.png
%{_datadir}/themes/Vapor/assets/button-hover.png
%{_datadir}/themes/Vapor/assets/button-insensitive.png
%{_datadir}/themes/Vapor/assets/button.png
%{_datadir}/themes/Vapor/assets/check-checked-active.png
%{_datadir}/themes/Vapor/assets/check-checked-active@2.png
%{_datadir}/themes/Vapor/assets/check-checked-backdrop-insensitive.png
%{_datadir}/themes/Vapor/assets/check-checked-backdrop-insensitive@2.png
%{_datadir}/themes/Vapor/assets/check-checked-backdrop.png
%{_datadir}/themes/Vapor/assets/check-checked-backdrop@2.png
%{_datadir}/themes/Vapor/assets/check-checked-hover.png
%{_datadir}/themes/Vapor/assets/check-checked-hover@2.png
%{_datadir}/themes/Vapor/assets/check-checked-insensitive.png
%{_datadir}/themes/Vapor/assets/check-checked-insensitive@2.png
%{_datadir}/themes/Vapor/assets/check-mixed-active.png
%{_datadir}/themes/Vapor/assets/check-mixed-active@2.png
%{_datadir}/themes/Vapor/assets/check-mixed-backdrop-insensitive.png
%{_datadir}/themes/Vapor/assets/check-mixed-backdrop-insensitive@2.png
%{_datadir}/themes/Vapor/assets/check-mixed-backdrop.png
%{_datadir}/themes/Vapor/assets/check-mixed-backdrop@2.png
%{_datadir}/themes/Vapor/assets/check-mixed-hover.png
%{_datadir}/themes/Vapor/assets/check-mixed-hover@2.png
%{_datadir}/themes/Vapor/assets/check-mixed-insensitive.png
%{_datadir}/themes/Vapor/assets/check-mixed-insensitive@2.png
%{_datadir}/themes/Vapor/assets/check-selectionmode-checked-active.png
%{_datadir}/themes/Vapor/assets/check-selectionmode-checked-active@2.png
%{_datadir}/themes/Vapor/assets/check-selectionmode-checked-backdrop-insensitive.png
%{_datadir}/themes/Vapor/assets/check-selectionmode-checked-backdrop-insensitive@2.png
%{_datadir}/themes/Vapor/assets/check-selectionmode-checked-backdrop.png
%{_datadir}/themes/Vapor/assets/check-selectionmode-checked-backdrop@2.png
%{_datadir}/themes/Vapor/assets/check-selectionmode-checked-hover.png
%{_datadir}/themes/Vapor/assets/check-selectionmode-checked-hover@2.png
%{_datadir}/themes/Vapor/assets/check-selectionmode-checked-insensitive.png
%{_datadir}/themes/Vapor/assets/check-selectionmode-checked-insensitive@2.png
%{_datadir}/themes/Vapor/assets/check-selectionmode-unchecked-active.png
%{_datadir}/themes/Vapor/assets/check-selectionmode-unchecked-active@2.png
%{_datadir}/themes/Vapor/assets/check-selectionmode-unchecked-backdrop-insensitive.png
%{_datadir}/themes/Vapor/assets/check-selectionmode-unchecked-backdrop-insensitive@2.png
%{_datadir}/themes/Vapor/assets/check-selectionmode-unchecked-backdrop.png
%{_datadir}/themes/Vapor/assets/check-selectionmode-unchecked-backdrop@2.png
%{_datadir}/themes/Vapor/assets/check-selectionmode-unchecked-hover.png
%{_datadir}/themes/Vapor/assets/check-selectionmode-unchecked-hover@2.png
%{_datadir}/themes/Vapor/assets/check-selectionmode-unchecked-insensitive.png
%{_datadir}/themes/Vapor/assets/check-selectionmode-unchecked-insensitive@2.png
%{_datadir}/themes/Vapor/assets/check-selectionmode-unchecked.png
%{_datadir}/themes/Vapor/assets/check-selectionmode-unchecked@2.png
%{_datadir}/themes/Vapor/assets/check-unchecked-active.png
%{_datadir}/themes/Vapor/assets/check-unchecked-active@2.png
%{_datadir}/themes/Vapor/assets/check-unchecked-backdrop-insensitive.png
%{_datadir}/themes/Vapor/assets/check-unchecked-backdrop-insensitive@2.png
%{_datadir}/themes/Vapor/assets/check-unchecked-backdrop.png
%{_datadir}/themes/Vapor/assets/check-unchecked-backdrop@2.png
%{_datadir}/themes/Vapor/assets/check-unchecked-hover.png
%{_datadir}/themes/Vapor/assets/check-unchecked-hover@2.png
%{_datadir}/themes/Vapor/assets/check-unchecked-insensitive.png
%{_datadir}/themes/Vapor/assets/check-unchecked-insensitive@2.png
%{_datadir}/themes/Vapor/assets/check-unchecked.png
%{_datadir}/themes/Vapor/assets/check-unchecked@2.png
%{_datadir}/themes/Vapor/assets/combo-entry-active.png
%{_datadir}/themes/Vapor/assets/combo-entry-button-active.png
%{_datadir}/themes/Vapor/assets/combo-entry-button-insensitive.png
%{_datadir}/themes/Vapor/assets/combo-entry-button.png
%{_datadir}/themes/Vapor/assets/combo-entry-insensitive.png
%{_datadir}/themes/Vapor/assets/combo-entry.png
%{_datadir}/themes/Vapor/assets/entry-active.png
%{_datadir}/themes/Vapor/assets/entry-insensitive.png
%{_datadir}/themes/Vapor/assets/entry.png
%{_datadir}/themes/Vapor/assets/frame-gap-end.png
%{_datadir}/themes/Vapor/assets/frame-gap-start.png
%{_datadir}/themes/Vapor/assets/frame.png
%{_datadir}/themes/Vapor/assets/handle-h.png
%{_datadir}/themes/Vapor/assets/handle-v.png
%{_datadir}/themes/Vapor/assets/line-h.png
%{_datadir}/themes/Vapor/assets/line-v.png
%{_datadir}/themes/Vapor/assets/menu-arrow-insensitive.png
%{_datadir}/themes/Vapor/assets/menu-arrow-selected.png
%{_datadir}/themes/Vapor/assets/menu-arrow.png
%{_datadir}/themes/Vapor/assets/menubar-button.png
%{_datadir}/themes/Vapor/assets/notebook-frame-bottom.png
%{_datadir}/themes/Vapor/assets/notebook-frame-right.png
%{_datadir}/themes/Vapor/assets/notebook-frame-top.png
%{_datadir}/themes/Vapor/assets/notebook-gap-horizontal.png
%{_datadir}/themes/Vapor/assets/notebook-gap-vertical.png
%{_datadir}/themes/Vapor/assets/null.png
%{_datadir}/themes/Vapor/assets/progressbar-bar.png
%{_datadir}/themes/Vapor/assets/progressbar-trough.png
%{_datadir}/themes/Vapor/assets/radio-checked-active.png
%{_datadir}/themes/Vapor/assets/radio-checked-active@2.png
%{_datadir}/themes/Vapor/assets/radio-checked-backdrop-insensitive.png
%{_datadir}/themes/Vapor/assets/radio-checked-backdrop-insensitive@2.png
%{_datadir}/themes/Vapor/assets/radio-checked-backdrop.png
%{_datadir}/themes/Vapor/assets/radio-checked-backdrop@2.png
%{_datadir}/themes/Vapor/assets/radio-checked-hover.png
%{_datadir}/themes/Vapor/assets/radio-checked-hover@2.png
%{_datadir}/themes/Vapor/assets/radio-checked-insensitive.png
%{_datadir}/themes/Vapor/assets/radio-checked-insensitive@2.png
%{_datadir}/themes/Vapor/assets/radio-mixed-active.png
%{_datadir}/themes/Vapor/assets/radio-mixed-active@2.png
%{_datadir}/themes/Vapor/assets/radio-mixed-backdrop-insensitive.png
%{_datadir}/themes/Vapor/assets/radio-mixed-backdrop-insensitive@2.png
%{_datadir}/themes/Vapor/assets/radio-mixed-backdrop.png
%{_datadir}/themes/Vapor/assets/radio-mixed-backdrop@2.png
%{_datadir}/themes/Vapor/assets/radio-mixed-hover.png
%{_datadir}/themes/Vapor/assets/radio-mixed-hover@2.png
%{_datadir}/themes/Vapor/assets/radio-mixed-insensitive.png
%{_datadir}/themes/Vapor/assets/radio-mixed-insensitive@2.png
%{_datadir}/themes/Vapor/assets/radio-unchecked-active.png
%{_datadir}/themes/Vapor/assets/radio-unchecked-active@2.png
%{_datadir}/themes/Vapor/assets/radio-unchecked-backdrop-insensitive.png
%{_datadir}/themes/Vapor/assets/radio-unchecked-backdrop-insensitive@2.png
%{_datadir}/themes/Vapor/assets/radio-unchecked-backdrop.png
%{_datadir}/themes/Vapor/assets/radio-unchecked-backdrop@2.png
%{_datadir}/themes/Vapor/assets/radio-unchecked-hover.png
%{_datadir}/themes/Vapor/assets/radio-unchecked-hover@2.png
%{_datadir}/themes/Vapor/assets/radio-unchecked-insensitive.png
%{_datadir}/themes/Vapor/assets/radio-unchecked-insensitive@2.png
%{_datadir}/themes/Vapor/assets/radio-unchecked.png
%{_datadir}/themes/Vapor/assets/radio-unchecked@2.png
%{_datadir}/themes/Vapor/assets/scale-slider-active.png
%{_datadir}/themes/Vapor/assets/scale-slider-hover.png
%{_datadir}/themes/Vapor/assets/scale-slider-insensitive.png
%{_datadir}/themes/Vapor/assets/scale-slider.png
%{_datadir}/themes/Vapor/assets/scale-trough-horizontal.png
%{_datadir}/themes/Vapor/assets/scale-trough-vertical.png
%{_datadir}/themes/Vapor/assets/scrollbar-slider-horizontal-active.png
%{_datadir}/themes/Vapor/assets/scrollbar-slider-horizontal-active@2.png
%{_datadir}/themes/Vapor/assets/scrollbar-slider-horizontal-hover.png
%{_datadir}/themes/Vapor/assets/scrollbar-slider-horizontal-hover@2.png
%{_datadir}/themes/Vapor/assets/scrollbar-slider-horizontal.png
%{_datadir}/themes/Vapor/assets/scrollbar-slider-horizontal@2.png
%{_datadir}/themes/Vapor/assets/scrollbar-slider-vertical-active.png
%{_datadir}/themes/Vapor/assets/scrollbar-slider-vertical-active@2.png
%{_datadir}/themes/Vapor/assets/scrollbar-slider-vertical-hover.png
%{_datadir}/themes/Vapor/assets/scrollbar-slider-vertical-hover@2.png
%{_datadir}/themes/Vapor/assets/scrollbar-slider-vertical.png
%{_datadir}/themes/Vapor/assets/scrollbar-slider-vertical@2.png
%{_datadir}/themes/Vapor/assets/scrollbar-trough-horizontal.png
%{_datadir}/themes/Vapor/assets/scrollbar-trough-horizontal@2.png
%{_datadir}/themes/Vapor/assets/scrollbar-trough-vertical.png
%{_datadir}/themes/Vapor/assets/scrollbar-trough-vertical@2.png
%{_datadir}/themes/Vapor/assets/spinbutton-down-insensitive.png
%{_datadir}/themes/Vapor/assets/spinbutton-down-rtl-insensitive.png
%{_datadir}/themes/Vapor/assets/spinbutton-down-rtl.png
%{_datadir}/themes/Vapor/assets/spinbutton-down.png
%{_datadir}/themes/Vapor/assets/spinbutton-up-insensitive.png
%{_datadir}/themes/Vapor/assets/spinbutton-up-rtl-insensitive.png
%{_datadir}/themes/Vapor/assets/spinbutton-up-rtl.png
%{_datadir}/themes/Vapor/assets/spinbutton-up.png
%{_datadir}/themes/Vapor/assets/tab-bottom-active.png
%{_datadir}/themes/Vapor/assets/tab-bottom-inactive.png
%{_datadir}/themes/Vapor/assets/tab-left-active.png
%{_datadir}/themes/Vapor/assets/tab-left-inactive.png
%{_datadir}/themes/Vapor/assets/tab-right-active.png
%{_datadir}/themes/Vapor/assets/tab-right-inactive.png
%{_datadir}/themes/Vapor/assets/tab-top-active.png
%{_datadir}/themes/Vapor/assets/tab-top-inactive.png
%{_datadir}/themes/Vapor/assets/titlebutton-close-active-backdrop.png
%{_datadir}/themes/Vapor/assets/titlebutton-close-active-backdrop@2.png
%{_datadir}/themes/Vapor/assets/titlebutton-close-active.png
%{_datadir}/themes/Vapor/assets/titlebutton-close-active@2.png
%{_datadir}/themes/Vapor/assets/titlebutton-close-backdrop.png
%{_datadir}/themes/Vapor/assets/titlebutton-close-backdrop@2.png
%{_datadir}/themes/Vapor/assets/titlebutton-close-hover-backdrop.png
%{_datadir}/themes/Vapor/assets/titlebutton-close-hover-backdrop@2.png
%{_datadir}/themes/Vapor/assets/titlebutton-close-hover.png
%{_datadir}/themes/Vapor/assets/titlebutton-close-hover@2.png
%{_datadir}/themes/Vapor/assets/titlebutton-close.png
%{_datadir}/themes/Vapor/assets/titlebutton-close@2.png
%{_datadir}/themes/Vapor/assets/titlebutton-maximize-active-backdrop.png
%{_datadir}/themes/Vapor/assets/titlebutton-maximize-active-backdrop@2.png
%{_datadir}/themes/Vapor/assets/titlebutton-maximize-active.png
%{_datadir}/themes/Vapor/assets/titlebutton-maximize-active@2.png
%{_datadir}/themes/Vapor/assets/titlebutton-maximize-backdrop.png
%{_datadir}/themes/Vapor/assets/titlebutton-maximize-backdrop@2.png
%{_datadir}/themes/Vapor/assets/titlebutton-maximize-hover-backdrop.png
%{_datadir}/themes/Vapor/assets/titlebutton-maximize-hover-backdrop@2.png
%{_datadir}/themes/Vapor/assets/titlebutton-maximize-hover.png
%{_datadir}/themes/Vapor/assets/titlebutton-maximize-hover@2.png
%{_datadir}/themes/Vapor/assets/titlebutton-maximize-maximized-active-backdrop.png
%{_datadir}/themes/Vapor/assets/titlebutton-maximize-maximized-active-backdrop@2.png
%{_datadir}/themes/Vapor/assets/titlebutton-maximize-maximized-active.png
%{_datadir}/themes/Vapor/assets/titlebutton-maximize-maximized-active@2.png
%{_datadir}/themes/Vapor/assets/titlebutton-maximize-maximized-backdrop.png
%{_datadir}/themes/Vapor/assets/titlebutton-maximize-maximized-backdrop@2.png
%{_datadir}/themes/Vapor/assets/titlebutton-maximize-maximized-hover-backdrop.png
%{_datadir}/themes/Vapor/assets/titlebutton-maximize-maximized-hover-backdrop@2.png
%{_datadir}/themes/Vapor/assets/titlebutton-maximize-maximized-hover.png
%{_datadir}/themes/Vapor/assets/titlebutton-maximize-maximized-hover@2.png
%{_datadir}/themes/Vapor/assets/titlebutton-maximize-maximized.png
%{_datadir}/themes/Vapor/assets/titlebutton-maximize-maximized@2.png
%{_datadir}/themes/Vapor/assets/titlebutton-maximize.png
%{_datadir}/themes/Vapor/assets/titlebutton-maximize@2.png
%{_datadir}/themes/Vapor/assets/titlebutton-minimize-active-backdrop.png
%{_datadir}/themes/Vapor/assets/titlebutton-minimize-active-backdrop@2.png
%{_datadir}/themes/Vapor/assets/titlebutton-minimize-active.png
%{_datadir}/themes/Vapor/assets/titlebutton-minimize-active@2.png
%{_datadir}/themes/Vapor/assets/titlebutton-minimize-backdrop.png
%{_datadir}/themes/Vapor/assets/titlebutton-minimize-backdrop@2.png
%{_datadir}/themes/Vapor/assets/titlebutton-minimize-hover-backdrop.png
%{_datadir}/themes/Vapor/assets/titlebutton-minimize-hover-backdrop@2.png
%{_datadir}/themes/Vapor/assets/titlebutton-minimize-hover.png
%{_datadir}/themes/Vapor/assets/titlebutton-minimize-hover@2.png
%{_datadir}/themes/Vapor/assets/titlebutton-minimize.png
%{_datadir}/themes/Vapor/assets/titlebutton-minimize@2.png
%{_datadir}/themes/Vapor/assets/togglebutton-active.png
%{_datadir}/themes/Vapor/assets/togglebutton-hover.png
%{_datadir}/themes/Vapor/assets/togglebutton-insensitive.png
%{_datadir}/themes/Vapor/assets/togglebutton.png
%{_datadir}/themes/Vapor/assets/toolbar-background.png
%{_datadir}/themes/Vapor/assets/toolbutton-active.png
%{_datadir}/themes/Vapor/assets/toolbutton-hover.png
%{_datadir}/themes/Vapor/assets/toolbutton-toggled.png
%{_datadir}/themes/Vapor/assets/tree-header.png
%{_datadir}/themes/Vapor/gtk-2.0/gtkrc
%{_datadir}/themes/Vapor/gtk-2.0/widgets/buttons
%{_datadir}/themes/Vapor/gtk-2.0/widgets/default
%{_datadir}/themes/Vapor/gtk-2.0/widgets/entry
%{_datadir}/themes/Vapor/gtk-2.0/widgets/menu
%{_datadir}/themes/Vapor/gtk-2.0/widgets/misc
%{_datadir}/themes/Vapor/gtk-2.0/widgets/notebook
%{_datadir}/themes/Vapor/gtk-2.0/widgets/progressbar
%{_datadir}/themes/Vapor/gtk-2.0/widgets/range
%{_datadir}/themes/Vapor/gtk-2.0/widgets/scrollbar
%{_datadir}/themes/Vapor/gtk-2.0/widgets/styles
%{_datadir}/themes/Vapor/gtk-2.0/widgets/toolbar
%{_datadir}/themes/Vapor/gtk-3.18/gtk.css
%{_datadir}/themes/Vapor/gtk-3.20/gtk.css
"%{_datadir}/wallpapers/Steam Deck Logo 1.jpg"
"%{_datadir}/wallpapers/Steam Deck Logo 10.jpg"
"%{_datadir}/wallpapers/Steam Deck Logo 11.jpg"
"%{_datadir}/wallpapers/Steam Deck Logo 12.jpg"
"%{_datadir}/wallpapers/Steam Deck Logo 13.jpg"
"%{_datadir}/wallpapers/Steam Deck Logo 2.jpg"
"%{_datadir}/wallpapers/Steam Deck Logo 3.jpg"
"%{_datadir}/wallpapers/Steam Deck Logo 4.jpg"
"%{_datadir}/wallpapers/Steam Deck Logo 5.jpg"
"%{_datadir}/wallpapers/Steam Deck Logo 6.jpg"
"%{_datadir}/wallpapers/Steam Deck Logo 7.jpg"
"%{_datadir}/wallpapers/Steam Deck Logo 8.jpg"
"%{_datadir}/wallpapers/Steam Deck Logo 9.jpg"
"%{_datadir}/wallpapers/Steam Deck Logo Default.jpg"
%{_datadir}/wallpapers/Troll.jpg

%files sddm
%license COPYING
%{_datadir}/sddm/themes/sugar-steamOS/*

# Finally, changes from the latest release of your application are generated from
# your project's Git history. It will be empty until you make first annotated Git tag.
%changelog
