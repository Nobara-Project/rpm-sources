%global forgeurl https://gitlab.com/CalcProgrammer1/%{upstream_package_name}
%global commit b87c46a273c1bde5ef76bbdabc9069c0991005fe
#%%global tag release_%%{version}
# Workaround for incorrect package suffix name with forge macros
# (.20231017gitrelease.0.9 for example)
#%%global distprefix %%{nil}

# https://fedoraproject.org/wiki/Changes/EncourageI686LeafRemoval
ExcludeArch: %{ix86}

%global upstream_package_name OpenRGB

Name:           openrgb
Version:        0.9
%forgemeta
Release:        %autorelease -b20
Summary:        Open source RGB lighting control

# Entire source code is GPL-2.0-only except some bundled libs:
#   * GPL-3.0-or-later:
#     - hueplusplus-1.0.0
#     - libcmmk
License:        GPL-2.0-only AND GPL-3.0-or-later
URL:            https://openrgb.org
Source0:        %{forgesource}

BuildRequires:  desktop-file-utils
BuildRequires:  gcc-c++
BuildRequires:  libappstream-glib
BuildRequires:  mbedtls-devel
BuildRequires:  systemd-rpm-macros

BuildRequires:  pkgconfig(hidapi-libusb)
BuildRequires:  pkgconfig(libusb)

BuildRequires:  cmake
BuildRequires:  cmake(Qt5)
BuildRequires:  cmake(Qt5LinguistTools)

Requires:       %{name}-udev-rules = %{version}-%{release}
Requires:       hicolor-icon-theme

Provides:       bundled(hueplusplus) = 1.0.0
Provides:       bundled(libcmmk)

%description
Visit our website at https://openrgb.org!

One of the biggest complaints about RGB is the software ecosystem surrounding
it.  Every manufacturer has their own app, their own brand, their own style.
If you want to mix and match devices, you end up with a ton of conflicting,
functionally identical apps competing for your background resources.  On top
of that, these apps are proprietary and Windows-only.  Some even require
online accounts.  What if there was a way to control all of your RGB devices
from a single app, on both Windows and Linux, without any nonsense?  That is
what OpenRGB sets out to achieve.  One app to rule them all.

Features
  * Set colors and select effect modes for a wide variety of RGB hardware
  * Save and load profiles
  * Control lighting from third party software using the OpenRGB SDK
  * Command line interface
  * Connect multiple instances of OpenRGB to synchronize lighting across
    multiple PCs
  * Can operate standalone or in a client/headless server configuration
  * View device information
  * No official/manufacturer software required
  * Graphical view of device LEDs makes creating custom patterns easy


# Separate Udev rules package is useful for Flatpak package and others
%package        udev-rules
Summary:        Udev rules for %{name}
BuildArch:      noarch

Requires:       systemd-udev
Suggests:       %{name} = %{version}-%{release}

%description    udev-rules
Udev rules for %{name}.


%prep
%forgeautosetup -p1

# Remove some bundled libs
pushd dependencies
rm -rf       \
  hidapi     \
  hidapi-win \
  libusb-*   \
  mbedtls-*  \
  %{nil}
popd


%build
%qmake_qt5 \
    .      \
    %{nil}
%make_build


%install
%make_install INSTALL_ROOT=%{buildroot}


%check
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/*.xml
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop


# Need to manually reload udev rules to get working app right after installing
# package
%post -n %{name}-udev-rules
if [ -S /run/udev/control ]; then
    udevadm control --reload
    udevadm trigger
fi


%files
%doc README.md
%{_bindir}/%{name}
%{_datadir}/icons/hicolor/*/apps/*.png
%{_datadir}/applications/*.desktop
%{_metainfodir}/*.metainfo.xml
%{_unitdir}/%{name}.service
%{_tmpfilesdir}/%{name}.conf

%files udev-rules
%license LICENSE
%{_udevrulesdir}/60-%{name}.rules


%changelog
* Sat Apr 18 2026 LionHeartP <LionHeartP@proton.me> - 0.9-20.20260418gitb87c46a
- Update to latest commit

* Sun Nov 16 2025 LionHeartP <LionHeartP@proton.me> - 0.9-19
- Update to latest commit

* Fri Oct 31 2025 LionHeartP <LionHeartP@proton.me> - 0.9-18
- Update to latest commit

* Wed Mar 19 2025 Peter Robinson <pbrobinson@gmail.com> - 0.9-17
- Rebuild for mbedtls 3.6

* Tue Mar 11 2025 Marc Deop i Argemí <marc@marcdeop.com> - 0.9-16
- fix: use patch instead of patch0

* Tue Mar 11 2025 Marc Deop i Argemí <marc@marcdeop.com> - 0.9-15
- feat: simplify spec file, update to latest commit and add patch

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.9-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Sep 03 2024 Morten Stevens <mstevens@fedoraproject.org> - 0.7-3
- Rebuilt for mbedTLS 3.6.1

* Sat Apr 30 2022 Artem Polishchuk <ego.cordatus@gmail.com> - 0.7-2
- build: Trigger udev reload for udev-rules sub-package

* Sun Jan 02 2022 Artem Polishchuk <ego.cordatus@gmail.com> - 0.7-1
- Initial package
