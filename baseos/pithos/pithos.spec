# brp-python-bytecompile is ran with python2 by default
%global __python %{__python3}
%global appid io.github.Pithos

Name:           pithos
Version:        1.6.1
Release:        1%{?dist}
Summary:        A Pandora client for the GNOME Desktop

License:        GPLv3
URL:            https://pithos.github.io/
Source0:        https://github.com/pithos/pithos/releases/download/%{version}/pithos-master.tar.gz


BuildArch:      noarch

BuildRequires:  desktop-file-utils
BuildRequires:  python3-devel >= 3.4
BuildRequires:  meson >= 0.40.0
BuildRequires:  glib2-devel
BuildRequires:  gdk-pixbuf2-devel
BuildRequires:  libappstream-glib
BuildRequires:  gettext

Requires:       gtk3
Requires:       libsecret
Requires:       python3-gobject-base
Requires:       python3-cairo
Requires:       hicolor-icon-theme
# HTTP support
Requires:       gstreamer1-plugins-good
# MP3
Requires:       gstreamer1-plugin-mpg123
# AACPlus (faad)
Requires:       gstreamer1-plugins-bad-free
Requires:       gstreamer1-plugins-bad-free-extras
# Last.fm plugin
Recommends:     python3-pylast
# Keybinder plugin on DEs other than Gnome/Mate
Recommends:     keybinder3
# Notification Icon plugin on some DEs
Suggests:       libappindicator-gtk

%description
Pithos is a easy to use native Pandora Radio client that is more lightweight
than the pandora.com web client and integrates with the desktop.
It supports most functionality of pandora.com such as rating songs,
creating/managing stations, quickmix, etc. On top of that it has features such
as last.fm scrobbling, media keys, notifications, proxies, and mpris support.

%prep
%autosetup -n pithos-master -p1

%build
%meson
%meson_build

%install
%meson_install

# Remove Unity specific icons
rm -rf %{buildroot}%{_datadir}/icons/ubuntu*

%check
appstream-util validate-relax --nonet %{buildroot}/%{_metainfodir}/%{appid}.appdata.xml
desktop-file-validate %{buildroot}/%{_datadir}/applications/%{appid}.desktop

%files
%doc README.md
%license license
%{_bindir}/%{name}
%{_datadir}/%{name}/
%{_datadir}/applications/%{appid}.desktop
%{_metainfodir}/%{appid}.appdata.xml
%{_datadir}/dbus-1/services/%{appid}.service
%{_datadir}/glib-2.0/schemas/%{appid}.gschema.xml
%{_datadir}/icons/hicolor/*/apps/%{appid}*.png
%{_datadir}/icons/hicolor/*/apps/%{appid}*.svg
%{_mandir}/man1/%{name}.1.*

%changelog
* Tue Oct 04 2022 Leigh Scott <leigh123linux@gmail.com> - 1.6.0-1
- Bump version to 1.6.0
- Fix byte compile

* Sun Aug 07 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.5.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild and ffmpeg
  5.1

* Wed Feb 09 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Aug 03 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Feb 03 2021 Leigh Scott <leigh123linux@gmail.com> - 1.5.1-1
- Bump version to 1.5.1

* Wed Feb 03 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.4.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Aug 18 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.4.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Feb 05 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.4.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Aug 09 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.4.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Mar 04 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.4.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Aug 19 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.4.1-6
- Rebuilt for Fedora 29 Mass Rebuild binutils issue

* Fri Jul 27 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.4.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jul 10 2018 Miro Hrončok <mhroncok@redhat.com> - 1.4.1-4
- Rebuilt for Python 3.7

* Tue Apr 24 2018 Leigh Scott <leigh123linux@googlemail.com> - 1.4.1-3
- Fix missing requires (rfbz#4854)
- Remove obsolete scriptlets
- Cleanup spec file

* Thu Mar 01 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 1.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Nov 26 2017 Patrick Griffis <tingping@tingping.se> - 1.4.1-1
- Bump version to 1.4.1

* Sun Oct 15 2017 Patrick Griffis <tingping@tingping.se> - 1.4.0-1
- Bump version to 1.4.0

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 1.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Apr 21 2017 Patrick Griffis <tingping@tingping.se> - 1.3.1-1
- Bump version to 1.3.1

* Thu Apr 13 2017 Patrick Griffis <tingping@tingping.se> - 1.3.0-1
- Bump version to 1.3.0
- Fix directory ownership

* Mon Mar 20 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Jul 31 2016 Patrick Griffis <tingping@tingping.se> - 1.2.1-1
- Bump version to 1.2.1

* Wed Jul 27 2016 Patrick Griffis <tingping@tingping.se> - 1.2.0-1
- Bump version to 1.2.0

* Mon Nov 23 2015 TingPing <tingping@tingping.se> - 1.1.2-1
- Bump version to 1.1.2

* Mon May 18 2015 TingPing <tingping@tingping.se> - 1.1.1-1
- Bump version to 1.1.1

* Sun May 10 2015 TingPing <tingping@tingping.se> - 1.1.0-1
- Bump version to 1.1.0

* Mon Jan 5 2015 TingPing <tingping@tingping.se> - 1.0.1-2
- Fix importing pylast

* Sun Sep 21 2014 TingPing <tingping@tingping.se> - 1.0.1-1
- Bump version to 1.0.1

* Fri Jul 18 2014 TingPing <tingping@tingping.se> - 1.0.0-3
- Fix python2 sitelib macro

* Sat Jun 21 2014 TingPing <tingping@tingping.se> - 1.0.0-2
- Fix python2 sitelib macro

* Sat Jun 7 2014 TingPing <tingping@tingping.se> - 1.0.0-1
- Bump version to 1.0.0

* Fri Apr 18 2014 TingPing <tingping@tingping.se> - 0.3.18-2
- Fix dependency issue

* Thu Mar 27 2014 TingPing <tingping@tingping.se> - 0.3.18-1
- Initial package
