Name:           steamtinkerlaunch
Version:        12.12
Release:        1%{?dist}
Summary:        Wrapper tool for use with the Steam client for custom launch options

License:        GPLv3
URL:            https://github.com/frostworx/steamtinkerlaunch
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz
Patch0:         steamtinkerlaunch-build.patch

BuildArch:      noarch

BuildRequires:  make

Requires:       gawk bash git procps-ng unzip wget xdotool xprop xrandr vim-common xwininfo 
Requires:       yad >= 7.2
Recommends:     strace gamemode mangohud winetricks vkBasalt net-toolsa scummvm gameconqueror
Recommends:     gamescope innoextract usbutils jq ImageMagick rsync p7zip


%description
Steam Tinker Launch is a Linux wrapper tool for use with the Steam client which
allows customizing and start tools and options for games quickly on the fly


%prep
%autosetup


%build


%install
rm -rf $RPM_BUILD_ROOT
%{__make} install PREFIX=%{_prefix} BUILDROOT=%{buildroot}


%files
%license LICENSE
%doc README.md
%{_bindir}/steamtinkerlaunch
%{_datadir}/steamtinkerlaunch
%{_datadir}/applications/steamtinkerlaunch.desktop
%{_datadir}/icons/hicolor/scalable/apps/steamtinkerlaunch.svg


%changelog
* Sat Mar 5 2022 João Capucho <jcapucho7@gmail.com> - 9.2-1
- Update to version 9.2

* Sat Jan 15 2022 João Capucho <jcapucho7@gmail.com> - 9.0.1-1
- Update to version 9.0.1

* Wed Dec 08 2021 João Capucho <jcapucho7@gmail.com> - 8.0-1
- First steamtinkerlauncher package
