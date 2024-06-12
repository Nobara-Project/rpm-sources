%define commit 3d143a70b36e56ba0c3143718a12bcf695dcb570
%define shortcommit 3d143a7
%global appid net.lutris.Lutris
%define debug_package %{nil}

Name:           lutris
Version:        0.5.17
Release:        4.git.%{shortcommit}%{?dist}
Summary:        Video game preservation platform

License:        GPL-3.0+
Group:          Amusements/Games/Other
URL:            http://lutris.net
Source0:        https://github.com/lutris/lutris/archive/%{commit}.tar.gz#/lutris-%{commit}.tar.gz

BuildRequires:  desktop-file-utils
BuildRequires:  python3-devel
Requires:       cabextract
Requires:       gtk3, psmisc, xorg-x11-server-Xephyr, xrandr
Requires:       hicolor-icon-theme
Requires:       gnome-desktop3
Requires:       python3-distro
Requires:       python3-cairo

# Tests
BuildRequires:  python3dist(pytest)
BuildRequires:  gtk3-devel
BuildRequires:  webkit2gtk4.1-devel
BuildRequires:  python3-cairo-devel


%ifarch x86_64
Requires:       mesa-dri-drivers(x86-32)
Requires:       mesa-vulkan-drivers(x86-32)
Requires:       vulkan-loader(x86-32)
Requires:       mesa-libGL(x86-32)
Recommends:     pipewire(x86-32)
Recommends:     libFAudio(x86-32)
Recommends:     wine-pulseaudio(x86-32)
Recommends:     wine-core(x86-32)
%endif

Requires:       mesa-vulkan-drivers
Requires:       mesa-dri-drivers
Requires:       vulkan-loader
Requires:       mesa-libGL
Requires:       glx-utils
Requires:       gvfs
Requires:       webkit2gtk4.1
Recommends: 	p7zip, curl
Recommends:	fluid-soundfont-gs
Recommends:     wine-core
Recommends:	p7zip-plugins
Recommends:	gamemode
Recommends:     libFAudio
Recommends:     gamescope
BuildRequires:  fdupes
BuildRequires:  libappstream-glib
BuildRequires:  meson, gettext

%description
Lutris is a gaming platform for GNU/Linux. Its goal is to make
gaming on Linux as easy as possible by taking care of installing
and setting up the game for the user. The only thing you have to
do is play the game. It aims to support every game that is playable
on Linux.

%prep
%autosetup -n %{name}-%{commit} -p1

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel
%meson
%meson_build

%install
%pyproject_install
%pyproject_save_files lutris
%meson_install
appstream-util validate-relax --nonet %{buildroot}/%{_datadir}/metainfo/net.%{name}.Lutris.metainfo.xml
%fdupes %{buildroot}%{python3_sitelib}
desktop-file-install --dir=%{buildroot}%{_datadir}/applications share/applications/net.%{name}.Lutris.desktop

%check
# Python tests: Disabled because either they are querying hardware (Don't work in mock) or they're
# trying to spawn processes, which is also blocked.
%pytest --ignore=tests/test_dialogs.py --ignore=tests/test_installer.py --ignore=tests/test_api.py -k "not GetNvidiaDriverInfo and not GetNvidiaGpuInfo and not import_module and not options"

%files -f %{pyproject_files}
%{_bindir}/%{name}
%{_datadir}/%{name}/
%{_datadir}/applications/net.%{name}.Lutris.desktop
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg
%{_datadir}/icons/hicolor/16x16/apps/%{name}.png
%{_datadir}/icons/hicolor/22x22/apps/%{name}.png
%{_datadir}/icons/hicolor/24x24/apps/%{name}.png
%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
%{_datadir}/icons/hicolor/48x48/apps/%{name}.png
%{_datadir}/icons/hicolor/64x64/apps/%{name}.png
%{_datadir}/icons/hicolor/128x128/apps/%{name}.png
%{_datadir}/man/man1/%{name}.1.gz
# Some files being missed by the Python macros
%{python3_sitelib}/%{name}/__pycache__/optional_settings.*.pyc
%{python3_sitelib}/%{name}/optional_settings.py
# ---
%{_datadir}/metainfo/
%{_datadir}/locale/

%changelog
%autochangelog
