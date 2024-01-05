## START: Set by rpmautospec
## (rpmautospec version 0.3.5)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 4;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

%global _hardened_build 1

%define gtk3_version 2.99.2

%global tarball_version %%(echo %{version} | tr '~' '.')

Name:           gdm
Epoch:          1
Version:        45.0.1
Release:        %autorelease
Summary:        The GNOME Display Manager

License:        GPL-2.0-or-later
URL:            https://wiki.gnome.org/Projects/GDM
Source0:        https://download.gnome.org/sources/gdm/44/gdm-%{tarball_version}.tar.xz
Source1:        org.gnome.login-screen.gschema.override

# moved here from pulseaudio-gdm-hooks-11.1-16
Source5:        default.pa-for-gdm

Source6:        gdm.sysusers

# Downstream patches
Patch:          0001-udev-Stick-with-wayland-on-hybrid-nvidia-with-vendor.patch
Patch:          0001-Honor-initial-setup-being-disabled-by-distro-install.patch
Patch:          0001-data-add-system-dconf-databases-to-gdm-profile.patch

BuildRequires:  dconf
BuildRequires:  desktop-file-utils
BuildRequires:  gettext-devel
BuildRequires:  libXdmcp-devel
BuildRequires:  meson
BuildRequires:  pam-devel
BuildRequires:  pkgconfig(accountsservice) >= 0.6.3
BuildRequires:  pkgconfig(audit)
BuildRequires:  pkgconfig(check)
BuildRequires:  pkgconfig(gobject-introspection-1.0)
BuildRequires:  pkgconfig(gtk+-3.0) >= %{gtk3_version}
BuildRequires:  pkgconfig(gudev-1.0)
BuildRequires:  pkgconfig(iso-codes)
BuildRequires:  pkgconfig(libcanberra-gtk3)
BuildRequires:  pkgconfig(libkeyutils)
BuildRequires:  pkgconfig(libselinux)
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:  pkgconfig(ply-boot-client)
BuildRequires:  pkgconfig(systemd)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xau)
BuildRequires:  pkgconfig(xorg-server)
BuildRequires:  systemd-rpm-macros
BuildRequires:  which
BuildRequires:  xorg-x11-server-Xorg
BuildRequires:  yelp-devel
BuildRequires:  yelp-tools

Provides: service(graphical-login) = %{name}

Requires: accountsservice
Requires: dconf
# since we use it, and pam spams the log if the module is missing
Requires: gnome-keyring-pam
Requires: gnome-session
Requires: gnome-session-wayland-session
Requires: gnome-settings-daemon >= 3.27.90
Requires: gnome-shell
Requires: iso-codes
# We need 1.0.4-5 since it lets us use "localhost" in auth cookies
Requires: libXau >= 1.0.4-4
Requires: pam
Requires: /sbin/nologin
Requires: setxkbmap
Requires: systemd >= 186
Requires: system-logos
Requires: xhost xmodmap xrdb
Requires: xorg-x11-xinit

# Until the greeter gets dynamic user support, it can't
# use a user bus
Requires: /usr/bin/dbus-run-session

%{?sysusers_requires_compat}

Provides: gdm-libs%{?_isa} = %{epoch}:%{version}-%{release}

%description
GDM, the GNOME Display Manager, handles authentication-related backend
functionality for logging in a user and unlocking the user's session after
it's been locked. GDM also provides functionality for initiating user-switching,
so more than one user can be logged in at the same time. It handles
graphical session registration with the system for both local and remote
sessions (in the latter case, via the XDMCP protocol).  In cases where the
session doesn't provide it's own display server, GDM can start the display
server on behalf of the session.

%package devel
Summary: Development files for gdm
Requires: %{name}%{?_isa} = %{epoch}:%{version}-%{release}
Requires: gdm-pam-extensions-devel = %{epoch}:%{version}-%{release}

%description devel
The gdm-devel package contains headers and other
files needed to build custom greeters.

%package pam-extensions-devel
Summary: Macros for developing GDM extensions to PAM
Requires: pam-devel

%description pam-extensions-devel
The gdm-pam-extensions-devel package contains headers and other
files that are helpful to PAM modules wishing to support
GDM specific authentication features.

%prep
%autosetup -p1 -n gdm-%{tarball_version}

%build
%meson -Dpam-prefix=%{_sysconfdir} \
       -Drun-dir=/run/gdm \
       -Dudev-dir=%{_udevrulesdir} \
       -Ddefault-path=/usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin \
       -Dprofiling=true \
       -Dplymouth=enabled \
       -Dselinux=enabled
%meson_build


%install
mkdir -p %{buildroot}%{_sysconfdir}/gdm/Init
mkdir -p %{buildroot}%{_sysconfdir}/gdm/PreSession
mkdir -p %{buildroot}%{_sysconfdir}/gdm/PostSession

%meson_install

install -p -m644 -D %{SOURCE5} %{buildroot}%{_localstatedir}/lib/gdm/.config/pulse/default.pa
install -p -m644 -D %{SOURCE6} %{buildroot}%{_sysusersdir}/%{name}.conf

rm -f %{buildroot}%{_sysconfdir}/pam.d/gdm

# add logo to shell greeter
cp -a %{SOURCE1} %{buildroot}%{_datadir}/glib-2.0/schemas

# docs go elsewhere
rm -rf %{buildroot}/%{_prefix}/doc

# create log dir
mkdir -p %{buildroot}/var/log/gdm

(cd %{buildroot}%{_sysconfdir}/gdm; ln -sf ../X11/xinit/Xsession .)

mkdir -p %{buildroot}%{_datadir}/gdm/autostart/LoginWindow

mkdir -p %{buildroot}/run/gdm

mkdir -p %{buildroot}%{_sysconfdir}/dconf/db/gdm.d/locks

%find_lang gdm --with-gnome

%pre
%sysusers_create_compat %{SOURCE6}

%post
# if the user already has a config file, then migrate it to the new
# location; rpm will ensure that old file will be renamed

custom=/etc/gdm/custom.conf

if [ $1 -ge 2 ] ; then
    if [ -f /usr/share/gdm/config/gdm.conf-custom ]; then
        oldconffile=/usr/share/gdm/config/gdm.conf-custom
    elif [ -f /etc/X11/gdm/gdm.conf ]; then
        oldconffile=/etc/X11/gdm/gdm.conf
    fi

    # Comment out some entries from the custom config file that may
    # have changed locations in the update.  Also move various
    # elements to their new locations.

    [ -n "$oldconffile" ] && sed \
    -e 's@^command=/usr/X11R6/bin/X@#command=/usr/bin/Xorg@' \
    -e 's@^Xnest=/usr/X11R6/bin/Xnest@#Xnest=/usr/X11R6/bin/Xnest@' \
    -e 's@^BaseXsession=/etc/X11/xdm/Xsession@#BaseXsession=/etc/X11/xinit/Xsession@' \
    -e 's@^BaseXsession=/etc/X11/gdm/Xsession@#&@' \
    -e 's@^BaseXsession=/etc/gdm/Xsession@#&@' \
    -e 's@^Greeter=/usr/bin/gdmgreeter@#Greeter=/usr/libexec/gdmgreeter@' \
    -e 's@^RemoteGreeter=/usr/bin/gdmlogin@#RemoteGreeter=/usr/libexec/gdmlogin@' \
    -e 's@^GraphicalTheme=Bluecurve@#&@' \
    -e 's@^BackgroundColor=#20305a@#&@' \
    -e 's@^DefaultPath=/usr/local/bin:/usr/bin:/bin:/usr/X11R6/bin@#&@' \
    -e 's@^RootPath=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin:/usr/X11R6/bin@#&@' \
    -e 's@^HostImageDir=/usr/share/hosts/@#HostImageDir=/usr/share/pixmaps/faces/@' \
    -e 's@^LogDir=/var/log/gdm@#&@' \
    -e 's@^PostLoginScriptDir=/etc/X11/gdm/PostLogin@#&@' \
    -e 's@^PreLoginScriptDir=/etc/X11/gdm/PreLogin@#&@' \
    -e 's@^PreSessionScriptDir=/etc/X11/gdm/PreSession@#&@' \
    -e 's@^PostSessionScriptDir=/etc/X11/gdm/PostSession@#&@' \
    -e 's@^DisplayInitDir=/var/run/gdm.pid@#&@' \
    -e 's@^RebootCommand=/sbin/reboot;/sbin/shutdown -r now;/usr/sbin/shutdown -r now;/usr/bin/reboot@#&@' \
    -e 's@^HaltCommand=/sbin/poweroff;/sbin/shutdown -h now;/usr/sbin/shutdown -h now;/usr/bin/poweroff@#&@' \
    -e 's@^ServAuthDir=/var/gdm@#&@' \
    -e 's@^Greeter=/usr/bin/gdmlogin@Greeter=/usr/libexec/gdmlogin@' \
    -e 's@^RemoteGreeter=/usr/bin/gdmgreeter@RemoteGreeter=/usr/libexec/gdmgreeter@' \
    $oldconffile > $custom
fi

if [ $1 -ge 2 -a -f $custom ] && grep -q /etc/X11/gdm $custom ; then
   sed -i -e 's@/etc/X11/gdm@/etc/gdm@g' $custom
fi

%systemd_post gdm.service

%preun
%systemd_preun gdm.service

%postun
%systemd_postun gdm.service

%files -f gdm.lang
%doc AUTHORS NEWS README.md
%license COPYING
%dir %{_sysconfdir}/gdm
%config(noreplace) %{_sysconfdir}/gdm/custom.conf
%config %{_sysconfdir}/gdm/Init/*
%config %{_sysconfdir}/gdm/PostLogin/*
%config %{_sysconfdir}/gdm/PreSession/*
%config %{_sysconfdir}/gdm/PostSession/*
%config %{_sysconfdir}/pam.d/gdm-autologin
%config %{_sysconfdir}/pam.d/gdm-password
# not config files
%{_sysconfdir}/gdm/Xsession
%{_datadir}/gdm/gdm.schemas
%{_sysconfdir}/dbus-1/system.d/gdm.conf
%dir %{_sysconfdir}/gdm/Init
%dir %{_sysconfdir}/gdm/PreSession
%dir %{_sysconfdir}/gdm/PostSession
%dir %{_sysconfdir}/gdm/PostLogin
%dir %{_sysconfdir}/dconf/db/gdm.d
%dir %{_sysconfdir}/dconf/db/gdm.d/locks
%{_datadir}/glib-2.0/schemas/org.gnome.login-screen.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.login-screen.gschema.override
%{_libexecdir}/gdm-host-chooser
%{_libexecdir}/gdm-runtime-config
%{_libexecdir}/gdm-session-worker
%{_libexecdir}/gdm-simple-chooser
%{_libexecdir}/gdm-wayland-session
%{_libexecdir}/gdm-x-session
%{_sbindir}/gdm
%{_bindir}/gdmflexiserver
%{_bindir}/gdm-screenshot
%dir %{_datadir}/dconf
%dir %{_datadir}/dconf/profile
%{_datadir}/dconf/profile/gdm
%dir %{_datadir}/gdm/greeter
%dir %{_datadir}/gdm/greeter/applications
%{_datadir}/gdm/greeter/applications/*
%dir %{_datadir}/gdm/greeter/autostart
%{_datadir}/gdm/greeter/autostart/*
%{_datadir}/gdm/greeter-dconf-defaults
%{_datadir}/gdm/locale.alias
%{_datadir}/gdm/gdb-cmd
%{_datadir}/gnome-session/sessions/gnome-login.session
%{_libdir}/girepository-1.0/Gdm-1.0.typelib
%{_libdir}/security/pam_gdm.so
%{_libdir}/libgdm*.so*
%attr(0711, root, gdm) %dir %{_localstatedir}/log/gdm
%attr(1770, gdm, gdm) %dir %{_localstatedir}/lib/gdm
%attr(0700, gdm, gdm) %dir %{_localstatedir}/lib/gdm/.config
%attr(0700, gdm, gdm) %dir %{_localstatedir}/lib/gdm/.config/pulse
%attr(0600, gdm, gdm) %{_localstatedir}/lib/gdm/.config/pulse/default.pa
%attr(0711, root, gdm) %dir /run/gdm
%config %{_sysconfdir}/pam.d/gdm-smartcard
%config %{_sysconfdir}/pam.d/gdm-fingerprint
%{_sysconfdir}/pam.d/gdm-launch-environment
%{_udevrulesdir}/61-gdm.rules
%{_unitdir}/gdm.service
%dir %{_userunitdir}/gnome-session@gnome-login.target.d/
%{_userunitdir}/gnome-session@gnome-login.target.d/session.conf
%{_sysusersdir}/%{name}.conf

%files devel
%dir %{_includedir}/gdm
%{_includedir}/gdm/*.h
%exclude %{_includedir}/gdm/gdm-pam-extensions.h
%dir %{_datadir}/gir-1.0
%{_datadir}/gir-1.0/Gdm-1.0.gir
%{_libdir}/pkgconfig/gdm.pc

%files pam-extensions-devel
%{_includedir}/gdm/gdm-pam-extensions.h
%{_libdir}/pkgconfig/gdm-pam-extensions.pc

%changelog
* Mon Sep 25 2023 Sandro Bonazzola <sbonazzo@redhat.com> - 1:45.0.1-4
- Synchronize permission and group ownership for log dir between rpm file
  manifest and daemon expectations.

* Tue Sep 19 2023 Kalev Lember <klember@redhat.com> - 1:45.0.1-3
- Drop some old versioned dependencies

* Tue Sep 19 2023 Kalev Lember <klember@redhat.com> - 1:45.0.1-2
- Use standard whitespace

* Tue Sep 19 2023 Kalev Lember <klember@redhat.com> - 1:45.0.1-1
- Update to 45.0.1

* Tue Aug 29 2023 Ray Strode <rstrode@redhat.com> - 1:45~beta-1
- Update to 45.beta

* Tue Aug 29 2023 Ray Strode <rstrode@redhat.com> - 1:44.1-4
- Add crash fix, initial-setup fix, and simpledrm fix (other half)

* Tue Aug 29 2023 Ray Strode <rstrode@redhat.com> - 1:44.1-3
- Add crash fix, initial-setup fix, and simpledrm fix

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:44.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue May 09 2023 David King <amigadave@amigadave.com> - 1:44.1-1
- Update to 44.1

* Fri Mar 31 2023 David King <amigadave@amigadave.com> - 1:44.0-1
- Update to 44.0

* Thu Mar 02 2023 Adam Williamson <awilliam@redhat.com> - 1:43.0-8
- Backport a follow-up to the EFI patch

* Thu Mar 02 2023 Ray Strode <rstrode@redhat.com> - 1:43.0-7
- Fix wayland on virt efi setups

* Thu Feb 09 2023 Iker Pedrosa <ipedrosa@redhat.com> - 1:43.0-6
- pam-redhat: Remove pam_console from service files

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:43.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Sep 27 2022 Ray Strode <rstrode@redhat.com> - 1:43.0-4
- Keep F36 behavior for hybrid machines with vendor nvidia driver...

* Tue Sep 27 2022 Ray Strode <rstrode@redhat.com> - 1:43.0-3
- Keep F36 behavior for hybrid machines with vendor nvidia driver...

* Tue Sep 27 2022 Ray Strode <rstrode@redhat.com> - 1:43.0-2
- Vendor nvidia wayland hybrid graphics udev change

* Tue Sep 20 2022 Kalev Lember <klember@redhat.com> - 1:43.0-1
- Update to 43.0

* Mon Aug 22 2022 Debarshi Ray <debarshir@gnome.org> - 1:42.0-3
- Use %%sysusers_requires_compat to match %%sysusers_create_compat

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:42.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Mar 22 2022 David King <amigadave@amigadave.com> - 1:42.0-1
- Update to 42.0

* Fri Jan 21 2022 Olivier Fourdan <ofourdan@redhat.com> - 1:41.3-4
- Bump release

* Thu Jan 20 2022 Olivier Fourdan <ofourdan@redhat.com> - 1:41.3-3
- Enable Wayland by default with NVIDIA version 510 and above

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:41.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jan 12 2022 David King <amigadave@amigadave.com> - 1:41.3-1
- Update to 41.3

* Thu Nov 18 2021 Kevin Fenzi <kevin@scrye.com> - 1:41.0-5
- Typo fix from Timothée Ravier

* Wed Nov 17 2021 Timothée Ravier <tim@siosm.fr> - 1:41.0-4
- Fix %%sysusers_create_compat macro call

* Tue Nov 16 2021 Ray Strode <rstrode@redhat.com> - 1:41.0-3
- Fix Xorg selection when SessionType is unspecified in accountsservice but
  session is specified

* Fri Oct 15 2021 Timothée Ravier <tim@siosm.fr> - 1:41.0-2
- Use systemd sysusers config to create user and group

* Tue Sep 21 2021 Kalev Lember <klember@redhat.com> - 1:41.0-1
- Update to 41.0

* Wed Sep 08 2021 Kalev Lember <klember@redhat.com> - 1:41~rc-1
- Update to 41.rc

* Wed Aug 04 2021 Kalev Lember <klember@redhat.com> - 1:41~alpha-3
- Avoid systemd_requires as per updated packaging guidelines

* Wed Aug 04 2021 Kalev Lember <klember@redhat.com> - 1:41~alpha-2
- BuildRequire systemd-rpm-macros rather than systemd

* Wed Jul 28 2021 Ray Strode <rstrode@redhat.com> - 1:41~alpha-1
- Update to 41.alpha

* Tue Jul 27 2021 Ray Strode <rstrode@redhat.com> - 1:40.0-10
- Correct logic error leading to wrong display server preference getting
  chosen

* Tue Jul 27 2021 Ray Strode <rstrode@redhat.com> - 1:40.0-9
- Correct logic error leading to wrong display server preference getting
  chosen

* Thu Jul 22 2021 Ray Strode <rstrode@redhat.com> - 1:40.0-8
- Allow vendor nvidia driver users the ability to pick wayland sessions
  without editing udev

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:40.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jun 16 2021 Christian Stadelmann <a.fp.o@genodeftest.de> - 1:40.0-6
- default.pa: Remove deprecated module-rescue-stream

* Tue Jun 15 2021 Ray Strode <rstrode@redhat.com> - 1:40.0-5
- make sure dconf dirs are created

* Tue Jun 15 2021 Ray Strode <rstrode@redhat.com> - 1:40.0-4
- drop unused patches

* Tue Jun 15 2021 Ray Strode <rstrode@redhat.com> - 1:40.0-3
- Provide gdm specific dconf source

* Tue Mar 30 2021 Kalev Lember <klember@redhat.com> - 1:40.0-2
- Remove old obsoletes and provides

* Tue Mar 30 2021 Kalev Lember <klember@redhat.com> - 1:40.0-1
- Update to 40.0

* Tue Mar 16 2021 Kalev Lember <klember@redhat.com> - 1:40~rc-1
- Update to 40.rc

* Wed Mar 10 2021 Benjamin Berg <bberg@redhat.com> - 1:40~beta-3
- Add patch to fix issues with the first login after boot

* Fri Feb 26 2021 Kalev Lember <klember@redhat.com> - 1:40~beta-2
- Drop changelog trimtime as it's set by the build system now

* Fri Feb 26 2021 Kalev Lember <klember@redhat.com> - 1:40~beta-1
- Update to 40.beta

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.38.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Dec 19 2020 Kalev Lember <klember@redhat.com> - 1:3.38.2.1-1
- Update to 3.38.2.1

* Wed Nov 04 2020 Kalev Lember <klember@redhat.com> - 1:3.38.2-1
- Update to 3.38.2

* Tue Oct 13 2020 Ray Strode <rstrode@redhat.com> - 1:3.38.1-2
- Update sources

* Tue Oct 13 2020 Ray Strode <rstrode@redhat.com> - 1:3.38.1-1
- Update to 3.38.1

* Sat Sep 12 2020 Kalev Lember <klember@redhat.com> - 1:3.38.0-1
- Update to 3.38.0

* Tue Sep 08 2020 Debarshi Ray <debarshir@gnome.org> - 1:3.37.90-3
- Fix Source0

* Tue Sep 08 2020 Dan Horák <dan@danny.cz> - 1:3.37.90-2
- Remove stale and unnecessary architecture-specific exceptions

* Mon Aug 17 2020 Kalev Lember <klember@redhat.com> - 1:3.37.90-1
- Update to 3.37.90

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.37.3-4
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Adam Jackson <ajax@redhat.com> - 1:3.37.3-3
- Requires xhost xmodmap xrdb, not xorg-x11-server-utils

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.37.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 20 2020 Ray Strode <rstrode@redhat.com> - 1:3.37.3-1
- Update to 3.37.3

* Tue May 05 2020 Ray Strode <rstrode@redhat.com> - 1:3.37.1-4
- Make sure users have dbus-run-session installed since the greeter depends
  on it

* Mon May 04 2020 Ray Strode <rstrode@redhat.com> - 1:3.37.1-3
- gdm: update build requires

* Mon May 04 2020 Ray Strode <rstrode@redhat.com> - 1:3.37.1-2
- Upload sources

* Mon May 04 2020 Ray Strode <rstrode@redhat.com> - 1:3.37.1-1
- Update to 3.37.1

* Mon May 04 2020 Ray Strode <rstrode@redhat.com> - 1:3.35.1-1
- gdm: port to meson

* Tue Apr 07 2020 Ray Strode <rstrode@redhat.com> - 1:3.34.1-3
- Fix autologin when gdm is started from VT other than VT 1

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.34.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Oct 07 2019 Kalev Lember <klember@redhat.com> - 1:3.34.1-1
- Update to 3.34.1

* Wed Sep 25 2019 Benjamin Berg <bberg@redhat.com> - 1:3.34.0-2
- Add patch to fix fast user switching

* Wed Sep 11 2019 Kalev Lember <klember@redhat.com> - 1:3.34.0-1
- Update to 3.34.0

* Wed Sep 04 2019 Kalev Lember <klember@redhat.com> - 1:3.33.92-1
- Update to 3.33.92

* Wed Sep 04 2019 Benjamin Berg <bberg@redhat.com> - 1:3.33.90-4
- Add patch to fix environment setup

* Mon Aug 26 2019 Adam Williamson <awilliam@redhat.com> - 1:3.33.90-3
- Drop patch from -2, better fix was applied to systemd

* Thu Aug 22 2019 Adam Williamson <awilliam@redhat.com> - 1:3.33.90-2
- Revert upstream commit that gives sbin priority in non-root $PATH

* Tue Aug 20 2019 Kalev Lember <klember@redhat.com> - 1:3.33.90-1
- Update to 3.33.90

* Mon Aug 12 2019 Kalev Lember <klember@redhat.com> - 1:3.33.4-1
- Update to 3.33.4

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.32.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Apr 15 2019 Ray Strode <rstrode@redhat.com> - 1:3.32.0-3
- avoid wayland if nomodeset is on kernel command line

* Mon Apr 15 2019 Ray Strode <rstrode@redhat.com> - 1:3.32.0-2
- Drop CanGraphical patch for now

* Wed Mar 13 2019 Kalev Lember <klember@redhat.com> - 1:3.32.0-1
- Update to 3.32.0

* Wed Feb 27 2019 Ray Strode <rstrode@redhat.com> - 1:3.31.91-1
- Update to 3.31.91

* Tue Feb 26 2019 Kalev Lember <klember@redhat.com> - 1:3.30.3-1
- Update to 3.30.3

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.30.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 28 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1:3.30.2-2
- Remove obsolete Group tag

* Wed Dec 19 2018 Kalev Lember <klember@redhat.com> - 1:3.30.2-1
- Update to 3.30.2

* Sat Oct 06 2018 Ray Strode <rstrode@redhat.com> - 1:3.30.1-3
- Fix login screen for machines that boot to fast
- Fix autologin crash

* Sat Sep 29 2018 Kalev Lember <klember@redhat.com> - 1:3.30.1-2
- Drop ldconfig scriptlets

* Sat Sep 29 2018 Kalev Lember <klember@redhat.com> - 1:3.30.1-1
- Update to 3.30.1

* Fri Sep 07 2018 Kalev Lember <klember@redhat.com> - 1:3.30.0-5
- Rebuilt against fixed atk (#1626575)

* Fri Sep 07 2018 Ray Strode <rstrode@redhat.com> - 1:3.30.0-4
- More initial setup fixes

* Tue Sep 04 2018 Ray Strode <rstrode@redhat.com> - 1:3.30.0-3
- fix up some upstream udev confusion

* Tue Sep 04 2018 Ray Strode <rstrode@redhat.com> - 1:3.30.0-2
- Drop upstreamed patch

* Tue Sep 04 2018 Ray Strode <rstrode@redhat.com> - 1:3.30.0-1
- Update to 3.30.0
- Fixes initial setup Resolves: #1624534

* Fri Aug 24 2018 Ray Strode <rstrode@redhat.com> - 1:3.29.91-1
- Update to 3.29.91

* Mon Aug 13 2018 Kalev Lember <klember@redhat.com> - 1:3.29.90-2
- Add missing build dep

* Mon Aug 13 2018 Kalev Lember <klember@redhat.com> - 1:3.29.90-1
- Update to 3.29.90

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.28.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu May 17 2018 Kalev Lember <klember@redhat.com> - 1:3.28.2-2
- Drop an unused patch

* Thu May 17 2018 Kalev Lember <klember@redhat.com> - 1:3.28.2-1
- Update to 3.28.2

* Tue May 08 2018 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 1:3.28.1-2
- Update gdm.spec

* Tue Apr 10 2018 Kalev Lember <klember@redhat.com> - 1:3.28.1-1
- Update to 3.28.1

* Thu Mar 22 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1:3.28.0-182
- Fixup ldconfig in postun

* Wed Mar 21 2018 Kevin Fenzi <kevin@scrye.com> - 1:3.28.0-181
- Fix my ldconfig fix to be actually correct.

* Wed Mar 21 2018 Kevin Fenzi <kevin@scrye.com> - 1:3.28.0-180
- Fix post/postun calls to ldconfig scriptlet.

* Tue Mar 20 2018 Ray Strode <rstrode@redhat.com> - 1:3.28.0-179
- err fix the patch

* Tue Mar 20 2018 Ray Strode <rstrode@redhat.com> - 1:3.28.0-178
- Drop /etc/dconf/db/gdm.d from list of dconf sources

* Tue Mar 20 2018 Rex Dieter <rdieter@gmail.com> - 1:3.28.0-177
- move pulseaudio-gdm-hooks content here use %%ldconfig %%make_build
  %%make_install %%systemd_requires

* Tue Mar 13 2018 Kalev Lember <klember@redhat.com>
- Update to 3.28.0

* Sun Mar 11 2018 Kalev Lember <klember@redhat.com>
- Update to 3.27.92

* Fri Mar 02 2018 Kalev Lember <klember@redhat.com>
- Update to 3.27.91

* Mon Feb 19 2018 Ray Strode <rstrode@redhat.com>
- Make sure GDM checks systemd dconf databases

* Fri Feb 09 2018 Bastien Nocera <hadess@hadess.net>
- + gdm-3.27.4-4 Update for gnome-settings-daemon changes

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 09 2018 Ray Strode <rstrode@redhat.com>
- Update to 3.27.4

* Sat Jan 06 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org>
- Remove obsolete scriptlets

* Thu Nov 30 2017 Ray Strode <rstrode@redhat.com>
- drop stale workaround from spec file

* Thu Nov 30 2017 Ray Strode <rstrode@redhat.com>
- Add buildrequires for X server

* Wed Nov 15 2017 Ray Strode <rstrode@redhat.com>
- Split PAM macros off into a new subpackage

* Wed Nov 08 2017 Ray Strode <rstrode@redhat.com>
- update spec file description

* Wed Nov 08 2017 Matej Habrnal <mhabrnal@redhat.com>
- preserve files permissions while copying them

* Wed Nov 08 2017 Matej Habrnal <mhabrnal@redhat.com>
- Use colon instead of dot in chown

* Wed Nov 08 2017 Matej Habrnal <mhabrnal@redhat.com>
- Replace deprecated macro for buildroot

* Wed Nov 01 2017 Kalev Lember <klember@redhat.com>
- Update to 3.26.2.1

* Tue Oct 24 2017 Ray Strode <rstrode@redhat.com>
- oops fix release name

* Mon Oct 23 2017 Ray Strode <rstrode@redhat.com>
- make sure initial-setup starts when wayland fails

* Sun Oct 08 2017 Kalev Lember <klember@redhat.com>
- Update to 3.26.1

* Wed Sep 13 2017 Kalev Lember <klember@redhat.com>
- Update to 3.26.0

* Fri Sep 08 2017 Kalev Lember <klember@redhat.com>
- Update to 3.25.92

* Tue Aug 15 2017 Kalev Lember <klember@redhat.com>
- Update to 3.25.90.1

* Mon Aug 14 2017 Ville Skyttä <ville.skytta@iki.fi>
- Own %%{_datadir}/{dconf,gdm/greeter,gir-1.0} dirs

* Mon Jul 31 2017 Kalev Lember <klember@redhat.com>
- Update to 3.25.4.1

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 25 2017 Kalev Lember <klember@redhat.com>
- Update to 3.25.3

* Wed May 10 2017 Kalev Lember <klember@redhat.com>
- Update to 3.24.2

* Wed Apr 12 2017 Kalev Lember <klember@redhat.com>
- Update to 3.24.1

* Sat Mar 25 2017 Ray Strode <rstrode@redhat.com>
- Fix fallback to X logic

* Tue Mar 21 2017 Kalev Lember <klember@redhat.com>
- Update to 3.24.0

* Fri Mar 17 2017 Kalev Lember <klember@redhat.com>
- Update to 3.23.92

* Mon Mar 06 2017 Kalev Lember <klember@redhat.com>
- Update to 3.23.91.1

* Mon Feb 13 2017 Richard Hughes <richard@hughsie.com>
- Update to 3.23.4

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jan 31 2017 Rui Matos <tiagomatos@gmail.com>
- Honor anaconda's firstboot being disabled

* Wed Oct 12 2016 Kalev Lember <klember@redhat.com>
- Use standard tag order in spec file

* Wed Oct 12 2016 Kalev Lember <klember@redhat.com>
- Don't set group tags

* Wed Oct 12 2016 Kalev Lember <klember@redhat.com>
- Update to 3.22.1

* Wed Sep 21 2016 Ray Strode <rstrode@redhat.com>
- Fix log in after log out

* Tue Sep 20 2016 Kalev Lember <klember@redhat.com>
- Update to 3.22.0

* Thu Sep 01 2016 Ray Strode <rstrode@redhat.com>
- Add buildrequire on kernel keyring development headers

* Thu Sep 01 2016 Ray Strode <rstrode@redhat.com>
- Update to 3.21.91

* Tue Aug 30 2016 Ray Strode <rstrode@redhat.com>
- Fix autologin

* Tue Aug 23 2016 Kalev Lember <klember@redhat.com>
- Update to 3.21.90

* Tue Jul 26 2016 Kalev Lember <klember@redhat.com>
- Update to 3.21.4

* Wed Jun 22 2016 Richard Hughes <richard@hughsie.com>
- Fix BRs

* Wed Jun 22 2016 Richard Hughes <richard@hughsie.com>
- Update to 3.21.3

* Thu Apr 21 2016 Kalev Lember <klember@redhat.com>
- Update to 3.20.1

* Tue Mar 22 2016 Kalev Lember <klember@redhat.com>
- Update to 3.20.0

* Tue Mar 15 2016 Kalev Lember <klember@redhat.com>
- Update to 3.19.92

* Fri Mar 04 2016 Kalev Lember <klember@redhat.com>
- Update to 3.19.91

* Thu Feb 18 2016 Richard Hughes <richard@hughsie.com>
- Update to 3.19.90

* Tue Feb 09 2016 Ray Strode <rstrode@redhat.com>
- More fixes need to get get gnome-terminal, gedit, etc working

* Thu Feb 04 2016 Ray Strode <rstrode@redhat.com>
- Fix gnome-terminal launched in an X session (and gedit etc)

* Wed Feb 03 2016 Dennis Gilmore <dennis@ausil.us>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 25 2016 Ray Strode <rstrode@redhat.com>
- Update to 3.19.4.1

* Thu Jan 21 2016 Kalev Lember <klember@redhat.com>
- Update to 3.19.4

* Thu Dec 17 2015 Kalev Lember <klember@redhat.com>
- Update to 3.19.2

* Tue Nov 10 2015 Ray Strode <rstrode@redhat.com>
- Update to git snapshot

* Mon Sep 21 2015 Kalev Lember <klember@redhat.com>
- Update to 3.18.0

* Wed Sep 16 2015 Kalev Lember <klember@redhat.com>
- Update to 3.17.92

* Mon Aug 24 2015 Ray Strode <rstrode@redhat.com>
- Update to 3.17.90
- Fixes sporadic failure to login and corruption of GDM_LANG environment
  variable

* Thu Aug 06 2015 Ray Strode <rstrode@redhat.com>
- drop /bin and /sbin from default path

* Tue Jul 28 2015 Kalev Lember <klember@redhat.com>
- Drop unused fontconfig build dep

* Tue Jul 28 2015 Kalev Lember <klember@redhat.com>
- Update to 3.17.4

* Tue Jun 23 2015 Ray Strode <rstrode@redhat.com>
- Update to 3.17.3.1

* Wed Jun 17 2015 Dennis Gilmore <dennis@ausil.us>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Ray Strode <rstrode@redhat.com>
- Update to 3.17.2

* Thu Apr 16 2015 Ray Strode <rstrode@redhat.com>
- Update to 3.16.1.1

* Thu Apr 16 2015 Kalev Lember <kalevlember@gmail.com>
- Update to 3.16.1

* Tue Apr 07 2015 Ray Strode <rstrode@redhat.com>
- Fix permissions on /var/lib/gdm/.local/share

* Fri Mar 27 2015 Ray Strode <rstrode@redhat.com>
- set XORG_RUN_AS_USER_OK in environment

* Tue Mar 24 2015 Kalev Lember <kalevlember@gmail.com>
- Update to 3.16.0.1

* Tue Mar 24 2015 Ray Strode <rstrode@redhat.com>
- actually quit plymouth at startup

* Mon Mar 23 2015 Kalev Lember <kalevlember@gmail.com>
- Update to 3.16.0

* Fri Mar 20 2015 Kalev Lember <kalevlember@gmail.com>
- Drop unused 90-grant-audio-devices-to-gdm.fdi

* Fri Mar 20 2015 Kalev Lember <kalevlember@gmail.com>
- Update to 3.15.92

* Tue Mar 03 2015 Ray Strode <rstrode@redhat.com>
- fix typo in changelog entry

* Tue Mar 03 2015 Ray Strode <rstrode@redhat.com>
- update sources

* Tue Mar 03 2015 Ray Strode <rstrode@redhat.com>
- Update to 3.15.92.1
- fixes "black screen on logout" of wayland sessions

* Tue Mar 03 2015 Ray Strode <rstrode@redhat.com>
- Update to 3.15.91.1
- fixes deadlock on VT switch in some cases

* Fri Feb 27 2015 Ray Strode <rstrode@redhat.com>
- Update for 3.15.91
- Reduces flicker
- Fixes hang for autologin Resolves: #1197224
- Fixes users that disable root running X in /etc/X11/Xwrapper.conf
- Fixes intermittent crash at login

* Wed Feb 25 2015 Ray Strode <rstrode@redhat.com>
- Update to 3.15.90.5
- gnome-initial-setup should work again Resolves: #1194948
- X will work better when configured to not need root (still not perfect
  though)

* Sun Feb 22 2015 Ray Strode <rstrode@redhat.com>
- Update to 3.15.90.4

* Sun Feb 22 2015 Ray Strode <rstrode@redhat.com>
- Update to 3.15.90.3

* Sat Feb 21 2015 Ray Strode <rstrode@redhat.com>
- add sources

* Fri Feb 20 2015 Ray Strode <rstrode@redhat.com>
- Update to 3.15.90.2

* Fri Feb 20 2015 Ray Strode <rstrode@redhat.com>
- Require gnome-session-wayland-session since we default to wayland now

* Fri Feb 20 2015 David King <amigadave@amigadave.com>
- Update URL

* Fri Feb 20 2015 David King <amigadave@amigadave.com>
- Use pkgconfig for BuildRequires

* Fri Feb 20 2015 David King <amigadave@amigadave.com>
- Use license macro for COPYING

* Fri Feb 20 2015 David King <amigadave@amigadave.com>
- Update to 3.15.90.1

* Thu Feb 19 2015 Richard Hughes <richard@hughsie.com>
- Fix filelists

* Thu Feb 19 2015 Richard Hughes <richard@hughsie.com>
- Update to 3.15.90

* Fri Jan 23 2015 Ray Strode <rstrode@redhat.com>
- Another user switching fix

* Thu Jan 22 2015 Ray Strode <rstrode@redhat.com>
- Fix user switching

* Fri Jan 16 2015 Ray Strode <rstrode@redhat.com>
- Fix pam_ecryptfs. unfortunately adds back gross last login messages.

* Fri Dec 19 2014 Richard Hughes <richard@hughsie.com>
- Update to 3.15.3.1

* Fri Dec 19 2014 Richard Hughes <richard@hughsie.com>
- Update to 3.15.3

* Tue Nov 25 2014 Kalev Lember <kalevlember@gmail.com>
- Update to 3.15.2

* Tue Oct 14 2014 Kalev Lember <kalevlember@gmail.com>
- Update to 3.14.1

* Mon Sep 22 2014 Kalev Lember <kalevlember@gmail.com>
- Update to 3.14.0

* Wed Sep 17 2014 Kalev Lember <kalevlember@gmail.com>
- Update to 3.13.92

* Wed Sep 03 2014 Kalev Lember <kalevlember@gmail.com>
- Remove duplicate -devel subpackage %%description

* Wed Sep 03 2014 Kalev Lember <kalevlember@gmail.com>
- Drop last GConf remnants

* Wed Sep 03 2014 Kalev Lember <kalevlember@gmail.com>
- Update to 3.13.91

* Sat Aug 16 2014 Peter Robinson <pbrobinson@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com>
- Rebuilt for gobject-introspection 1.41.4

* Sat Jun 07 2014 Dennis Gilmore <dennis@ausil.us>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 16 2014 Kalev Lember <kalevlember@gmail.com>
- Update to 3.12.2

* Thu May 08 2014 Ray Strode <rstrode@redhat.com>
- Fix PATH

* Wed May 07 2014 Kalev Lember <kalevlember@gmail.com>
- Drop gnome-icon-theme-symbolic dependency

* Tue Apr 15 2014 Kalev Lember <kalevlember@gmail.com>
- Update to 3.12.1

* Sat Apr 05 2014 Kalev Lember <kalevlember@gmail.com>
- Fold -libs into the main gdm package

* Sat Apr 05 2014 Kalev Lember <kalevlember@gmail.com>
- Tighten subpackage deps

* Sat Apr 05 2014 Kalev Lember <kalevlember@gmail.com>
- Move all requires together

* Tue Mar 25 2014 Richard Hughes <richard@hughsie.com>
- Update to 3.12.0

* Thu Mar 20 2014 Richard Hughes <richard@hughsie.com>
- Fix filelists

* Thu Mar 20 2014 Richard Hughes <richard@hughsie.com>
- Update to 3.11.92.1

* Sat Feb 22 2014 Kalev Lember <kalevlember@gmail.com>
- Fix the build

* Fri Feb 21 2014 Richard Hughes <richard@hughsie.com>
- Fix BRs

* Fri Feb 21 2014 Richard Hughes <richard@hughsie.com>
- Update to 3.11.90

* Wed Jan 15 2014 Richard Hughes <richard@hughsie.com>
- Update to 3.11.4

* Sun Dec 22 2013 Ville Skyttä <ville.skytta@iki.fi>
- Drop empty TODO from docs, trivial rpmlint fixes.

* Tue Dec 17 2013 Richard Hughes <richard@hughsie.com>
- Update to 3.11.3

* Tue Nov 19 2013 Richard Hughes <richard@hughsie.com>
- Update to 3.11.2

* Mon Oct 28 2013 Richard Hughes <richard@hughsie.com>
- Update to 3.10.0.1

* Tue Sep 24 2013 Kalev Lember <kalevlember@gmail.com>
- Update to 3.10.0

* Thu Aug 22 2013 Kalev Lember <kalevlember@gmail.com>
- Update to 3.9.90

* Sat Aug 10 2013 Kalev Lember <kalevlember@gmail.com>
- Update to 3.9.5

* Thu Jul 25 2013 Ray Strode <rstrode@redhat.com>
- Fix build

* Tue Jul 16 2013 Richard Hughes <richard@hughsie.com>
- Update to 3.8.3.1

* Sat Jun 22 2013 Matthias Clasen <mclasen@redhat.com>
- Trimp changelog

* Fri Jun 14 2013 Ray Strode <rstrode@redhat.com>
- Update to 3.8.3

* Tue May 21 2013 Matthias Clasen <mclasen@redhat.com>
- Don't include fallback greeter

* Mon May 20 2013 Ray Strode <rstrode@redhat.com>
- Fix permissions on /run/gdm

* Mon May 20 2013 Ray Strode <rstrode@redhat.com>
- Require gnome-shell

* Fri May 17 2013 Ray Strode <rstrode@redhat.com>
- Build with -fpie

* Thu May 16 2013 Florian Müllner <fmuellner@gnome.org>
- Update branding

* Wed Apr 17 2013 Richard Hughes <richard@hughsie.com>
- Update to 3.8.1.1

* Mon Apr 15 2013 Kalev Lember <kalevlember@gmail.com>
- Update to 3.8.1

* Mon Apr 01 2013 Kalev Lember <kalevlember@gmail.com>
- Drop the metacity dep now that the fallback greeter is gone

* Tue Mar 26 2013 Kalev Lember <kalevlember@gmail.com>
- Update to 3.8.0

* Wed Mar 20 2013 Kalev Lember <kalevlember@gmail.com>
- Drop the polkit-gnome dep now that the fallback greeter is gone

* Wed Mar 20 2013 Richard Hughes <richard@hughsie.com>
- Update to 3.7.92

* Wed Mar 06 2013 Matthias Clasen <mclasen@redhat.com>
- 3.7.91

* Wed Feb 27 2013 Ray Strode <rstrode@redhat.com>
- add changelog entry

* Wed Feb 27 2013 Ray Strode <rstrode@redhat.com>
- fix run dir for real this time

* Tue Feb 26 2013 Ray Strode <rstrode@redhat.com>
- change mkdir to new run dir

* Tue Feb 26 2013 Ray Strode <rstrode@redhat.com>
- Fix up runtime dir path

* Fri Feb 22 2013 Kalev Lember <kalevlember@gmail.com>
- Update to 3.7.90

* Tue Feb 05 2013 Kalev Lember <kalevlember@gmail.com>
- Update to 3.7.5

* Wed Jan 09 2013 Richard Hughes <richard@hughsie.com>
- Update to 3.7.3.1

* Tue Nov 20 2012 Richard Hughes <richard@hughsie.com>
- Update to 3.7.2

* Tue Nov 20 2012 Matthias Clasen <mclasen@redhat.com>
- remove patch fuzz of 999

* Wed Nov 14 2012 Kalev Lember <kalevlember@gmail.com>
- Update to 3.6.2

* Wed Nov 14 2012 Kalev Lember <kalevlember@gmail.com>
- Minor spec file cleanup

* Wed Nov 14 2012 Ray Strode <rstrode@redhat.com>
- Fix GDM auth cookie problem

* Mon Oct 29 2012 Matthias Clasen <mclasen@redhat.com>
- Add ppc to %%ExcludeArch

* Thu Oct 18 2012 Matthias Clasen <mclasen@redhat.com>
- Require gnome-icon-theme-symbolic

* Tue Oct 16 2012 Kalev Lember <kalevlember@gmail.com>
- 3.6.1

* Wed Sep 26 2012 Matthias Clasen <mclasen@redhat.com>
- fix file lists

* Tue Sep 25 2012 Richard Hughes <richard@hughsie.com>
- Update to 3.6.0

* Wed Sep 19 2012 Kalev Lember <kalevlember@gmail.com>
- Drop upstreamed patches

* Wed Sep 19 2012 Matthias Clasen <mclasen@redhat.com>
- 3.5.92.1

* Fri Sep 07 2012 Ray Strode <rstrode@redhat.com>
- fix selinux context after forking session

* Fri Sep 07 2012 Ray Strode <rstrode@redhat.com>
- rev release

* Fri Sep 07 2012 Ray Strode <rstrode@redhat.com>
- Fix autologin

* Thu Sep 06 2012 Richard Hughes <richard@hughsie.com>
- Call intltoolize to work around a tarball buglet

* Thu Sep 06 2012 Richard Hughes <richard@hughsie.com>
- Update to 3.5.91

* Wed Aug 22 2012 Richard Hughes <richard@hughsie.com>
- Fix file lists

* Tue Aug 21 2012 Richard Hughes <richard@hughsie.com>
- Update to 3.5.90

* Tue Aug 07 2012 Lennart Poettering <lennart@poettering.net>
- https://fedoraproject.org/wiki/Features/DisplayManagerRework

* Tue Aug 07 2012 Richard Hughes <richard@hughsie.com> - 1:3.5.5-3
- Fix filelists

* Tue Aug 07 2012 Richard Hughes <richard@hughsie.com> - 1:3.5.5-2
- Fix filelists

* Tue Aug 07 2012 Richard Hughes <richard@hughsie.com> - 1:3.5.5-1
- Update to 3.5.5

* Fri Jul 27 2012 Dennis Gilmore <dennis@ausil.us> - 1:3.5.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jul 19 2012 Ray Strode <rstrode@redhat.com> - 1:3.5.4.2-1
- Update to 3.5.4.2 - Fixes non-autologin

* Thu Jul 19 2012 Ray Strode <rstrode@redhat.com> - 1:3.5.4.1-2
- drop upstreamed patches

* Thu Jul 19 2012 Ray Strode <rstrode@redhat.com> - 1:3.5.4.1-1
- Update to 3.5.4.1
- Fixes autologin
- Fixes logind integration
- Fixes dconf incompatibility

* Thu Jul 19 2012 Matthias Clasen <mclasen@redhat.com> - 1:3.5.4-5
- fix dconf profile syntax

* Thu Jul 19 2012 Kalev Lember <kalevlember@gmail.com> - 1:3.5.4-4
- Require systemd >= 186 for libsystemd-login

* Wed Jul 18 2012 Ray Strode <rstrode@redhat.com> - 1:3.5.4-3
- Update filelist

* Tue Jul 17 2012 Richard Hughes <richard@hughsie.com> - 1:3.5.4-2
- Fix file list

* Tue Jul 17 2012 Richard Hughes <richard@hughsie.com> - 1:3.5.4-1
- Update to 3.5.4

* Thu Jun 28 2012 Ray Strode <rstrode@redhat.com> - 1:3.5.2-4
- Build with plymouth support (woops).

* Wed Jun 13 2012 Ray Strode <rstrode@redhat.com> - 1:3.5.2-3
- Drop unused spool dir

* Sat Jun 09 2012 Matthias Clasen <mclasen@redhat.com> - 1:3.5.2-2
- Fix gnome-shell detection

* Thu Jun 07 2012 Richard Hughes <richard@hughsie.com> - 1:3.5.2-1
- Update to 3.5.2

* Sat May 19 2012 Matthias Clasen <mclasen@redhat.com> - 1:3.4.1-2
- fix source url

* Mon Apr 16 2012 Matthias Clasen <mclasen@redhat.com> - 1:3.4.1-1
- 3.4.1

* Mon Apr 16 2012 Ray Strode <rstrode@redhat.com> - 1:3.4.0.1-8
- one more try at fixing live image crash

* Mon Apr 16 2012 Ray Strode <rstrode@redhat.com> - 1:3.4.0.1-7
- fix crash in liveimage

* Mon Apr 16 2012 Matthias Clasen <mclasen@redhat.com> - 1:3.4.0.1-6
- really drop gdm.pam

* Mon Apr 16 2012 Matthias Clasen <mclasen@redhat.com> - 1:3.4.0.1-5
- fix session unlock

* Mon Apr 16 2012 Ray Strode <rstrode@redhat.com> - 1:3.4.0.1-4
- drop /etc/pam.d/gdm

* Mon Apr 16 2012 Ray Strode <rstrode@redhat.com> - 1:3.4.0.1-3
- rev release

* Mon Apr 16 2012 Ray Strode <rstrode@redhat.com> - 1:3.4.0.1-2
- move pam gnome keyring after XDG_RUNTIME_DIR is setup

* Thu Mar 29 2012 Ray Strode <rstrode@redhat.com> - 1:3.4.0.1-1
- Update to 3.4.0.1

* Thu Mar 29 2012 Richard Hughes <richard@hughsie.com> - 1:3.4.0-1
- Update to 3.4.0

* Thu Mar 29 2012 Ray Strode <rstrode@redhat.com> - 1:3.3.92.1-3
- More consolekit registration fixes

* Tue Mar 20 2012 Ray Strode <rstrode@redhat.com> - 1:3.3.92.1-2
- update tarball

* Tue Mar 20 2012 Ray Strode <rstrode@redhat.com> - 1:3.3.92.1-1
- Update to latest version

* Mon Feb 13 2012 Ray Strode <rstrode@redhat.com> - 1:3.2.1.1-12
- rev release

* Mon Feb 13 2012 Ray Strode <rstrode@redhat.com> - 1:3.2.1.1-11
- Restore ConsoleKit registration if ConsoleKit is installed

* Thu Feb 09 2012 Ray Strode <rstrode@redhat.com> - 1:3.2.1.1-10
- Fix crasher bug

* Tue Feb 07 2012 Ray Strode <rstrode@redhat.com> - 1:3.2.1.1-9
- Add build requires and mind plymouth patch changes

* Tue Feb 07 2012 Ray Strode <rstrode@redhat.com> - 1:3.2.1.1-8
- Rebase plymouth patch

* Tue Feb 07 2012 Lennart Poettering <lennart@poettering.net> - 1:3.2.1.1-7
- multi-seat patch

* Thu Jan 26 2012 Ray Strode <rstrode@redhat.com> - 1:3.2.1.1-6
- Drop system-icon-theme requirement

* Fri Jan 13 2012 Dennis Gilmore <dennis@ausil.us> - 1:3.2.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Nov 10 2011 Adam Williamson <awilliam@redhat.com> - 1:3.2.1.1-4
- update the plymouth patch

* Thu Nov 10 2011 Adam Williamson <awilliam@redhat.com> - 1:3.2.1.1-3
- add the patch file, improve RPM changelog to list all synced fixes

* Thu Nov 10 2011 Adam Williamson <awilliam@redhat.com> - 1:3.2.1.1-2
- update the source

* Thu Nov 10 2011 Adam Williamson <awilliam@redhat.com> - 1:3.2.1.1-1
- re-sync with f16 (manually, since it all seems too confused for git
  merge)

* Fri Nov 04 2011 Bill Nottingham <notting@redhat.com> - 1:3.2.1-5
- Fix logo in fallback mode.

* Thu Nov 03 2011 Ray Strode <rstrode@redhat.com> - 1:3.2.1-4
- Drop fprintd-pam dependency

* Wed Oct 26 2011 Dennis Gilmore <dennis@ausil.us> - 1:3.2.1-3
- Rebuilt for glibc bug#747377

* Wed Oct 19 2011 Ray Strode <rstrode@redhat.com> - 1:3.2.1-2
- merge in changes from f16 spec file

* Wed Oct 19 2011 Ray Strode <rstrode@redhat.com> - 1:3.2.1-1
- Update to 3.2.1

* Wed Oct 05 2011 Adam Williamson <awilliam@redhat.com> - 1:3.2.0-2
- re-add check for gnome-shell before using it to handle login

* Thu Sep 29 2011 Ray Strode <rstrode@redhat.com> - 1:3.2.0-1
- Update to 3.2.0

* Tue Jun 28 2011 Ray Strode <rstrode@redhat.com> - 1:3.1.2-4
- disable fatal-critical stuff

* Tue Jun 21 2011 Michael Schwendt <mschwendt@fedoraproject.org> - 1:3.1.2-3
- Fix /dev/ull typo in scriptlets (#693046).

* Thu Jun 16 2011 Ray Strode <rstrode@redhat.com> - 1:3.1.2-2
- fix build

* Thu Jun 16 2011 Ray Strode <rstrode@redhat.com> - 1:3.1.2-1
- update to gdm 3.1.2

* Mon Jun 06 2011 Ray Strode <rstrode@redhat.com> - 1:3.0.4-1
- Update to gdm 3.0.4 to fix CVE-2011-1709

* Fri Apr 15 2011 Matthias Clasen <mclasen@redhat.com> - 1:3.0.0-8
- one more time

* Fri Apr 15 2011 Matthias Clasen <mclasen@redhat.com> - 1:3.0.0-7
- More BRs...

* Fri Apr 15 2011 Matthias Clasen <mclasen@redhat.com> - 1:3.0.0-6
- still collecting BRs...

* Fri Apr 15 2011 Matthias Clasen <mclasen@redhat.com> - 1:3.0.0-5
- fix BRs

* Fri Apr 15 2011 Matthias Clasen <mclasen@redhat.com> - 1:3.0.0-4
- Fix BRs

* Fri Apr 15 2011 Matthias Clasen <mclasen@redhat.com> - 1:3.0.0-3
- Yay, fedora

* Fri Apr 15 2011 Matthias Clasen <mclasen@redhat.com> - 1:3.0.0-2
- Yay, fedora

* Mon Apr 04 2011 Matthias Clasen <mclasen@redhat.com> - 1:3.0.0-1
- 3.0.0

* Tue Mar 22 2011 Ray Strode <rstrode@redhat.com> - 1:2.91.94-1
- Update to latest release

* Wed Mar 09 2011 Ray Strode <rstrode@redhat.com> - 1:2.91.93-3
- Fix autologin crash

* Tue Mar 08 2011 Ray Strode <rstrode@redhat.com> - 1:2.91.93-2
- Update sources

* Tue Mar 08 2011 Ray Strode <rstrode@redhat.com> - 1:2.91.93-1
- Update to 2.91.93

* Tue Mar 08 2011 Ray Strode <rstrode@redhat.com> - 1:2.91.92-3
- Add missing build requires

* Tue Mar 08 2011 Ray Strode <rstrode@redhat.com> - 1:2.91.92-2
- Update sources for release

* Mon Mar 07 2011 Ray Strode <rstrode@redhat.com> - 1:2.91.92-1
- Update to 2.91.92

* Mon Feb 28 2011 Matthias Clasen <mclasen@redhat.com> - 1:2.91.91-3
- Drop gnome-panel dep, not used anymore

* Sun Feb 27 2011 Matthias Clasen <mclasen@redhat.com> - 1:2.91.91-2
- Clean up BRs

* Wed Feb 23 2011 Ray Strode <rstrode@redhat.com> - 1:2.91.91-1
- Update to 2.91.91

* Tue Feb 22 2011 Ray Strode <rstrode@redhat.com> - 1:2.91.6-17
- s/user-list/userlist/

* Tue Feb 22 2011 Ray Strode <rstrode@redhat.com> - 1:2.91.6-16
- Fix empty user list.

* Fri Feb 18 2011 Ray Strode <rstrode@redhat.com> - 1:2.91.6-15
- Fix user list async bugs by dropping async code and moving to accounts
  service library Resolves: #678236 - Add requires for accounts service to
  spec since it isn't optional (and hasn't been for a while)

* Thu Feb 17 2011 Ray Strode <rstrode@redhat.com> - 1:2.91.6-14
- add forgotton patch

* Thu Feb 17 2011 Ray Strode <rstrode@redhat.com> - 1:2.91.6-13
- rev release

* Thu Feb 17 2011 Ray Strode <rstrode@redhat.com> - 1:2.91.6-12
- Add back session chooser

* Mon Feb 14 2011 Ray Strode <rstrode@redhat.com> - 1:2.91.6-11
- Build pam changes

* Mon Feb 14 2011 Paolo Bonzini <pbonzini@redhat.com> - 1:2.91.6-10
- Add support for postlogin stack

* Mon Feb 14 2011 Ray Strode <rstrode@redhat.com> - 1:2.91.6-9
- Fix crasher do to size calculation bugs

* Fri Feb 11 2011 Matthias Clasen <mclasen@redhat.com> - 1:2.91.6-8
- rebuild

* Thu Feb 10 2011 Christopher Aillon <caillon@redhat.com> - 1:2.91.6-7
- Drop the requires on plymouth-gdm-hooks since it no longer exists

* Tue Feb 08 2011 Dennis Gilmore <dennis@ausil.us> - 1:2.91.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Feb 07 2011 Bastien Nocera <hadess@hadess.net> - 1:2.91.6-5
- Really disable gnome-settings-daemon plugins in the greeter

* Fri Feb 04 2011 Ray Strode <rstrode@redhat.com> - 1:2.91.6-4
- don't call render_frame if there's no frame

* Thu Feb 03 2011 Ray Strode <rstrode@redhat.com> - 1:2.91.6-3
- Add accountsservice dep

* Thu Feb 03 2011 Ray Strode <rstrode@redhat.com> - 1:2.91.6-2
- add sources

* Thu Feb 03 2011 Ray Strode <rstrode@redhat.com> - 1:2.91.6-1
- Update to 2.91.6

* Sat Jan 29 2011 Ville Skyttä <ville.skytta@iki.fi> - 1:2.91.4-6
- Dir ownership fixes.

* Thu Jan 20 2011 Ray Strode <rstrode@redhat.com> - 1:2.91.4-5
- Fix swapped LHS and RHS in more-aggressive-about-loading-icons patch

* Wed Jan 19 2011 Ray Strode <rstrode@redhat.com> - 1:2.91.4-4
- Update previous patch to handle NULL better

* Wed Jan 19 2011 Ray Strode <rstrode@redhat.com> - 1:2.91.4-3
- user-chooser-widget: fix ref counting issue on user pixbuf

* Wed Jan 19 2011 Ray Strode <rstrode@redhat.com> - 1:2.91.4-2
- user-chooser: try to find fallback icon more aggressively

* Fri Dec 17 2010 Ray Strode <rstrode@redhat.com> - 1:2.91.4-1
- Update to 2.91.4

* Wed Dec 15 2010 Christopher Aillon <caillon@redhat.com> - 1:2.32.0-5
- Add maybe-set-is-loaded.patch to ensure we end up with a loaded user

* Wed Dec 01 2010 Peter Hutterer <peter.hutterer@who-t.net> - 1:2.32.0-4
- plymouth.patch: xserver 1.10 takes "-background none" root argument
  instead of the fedora-specific "-nr". - Add missing BuildRequires for
  dbus-glib-devel

* Tue Nov 16 2010 Dan Williams <dcbw@redhat.com> - 1:2.32.0-3
- Fix upower build requirement

* Wed Sep 29 2010 Ray Strode <rstrode@redhat.com> - 1:2.32.0-2
- More post update spec file tweaks

* Wed Sep 29 2010 Ray Strode <rstrode@redhat.com> - 1:2.32.0-1
- Update to 2.32.0

* Wed Aug 18 2010 Ray Strode <rstrode@redhat.com> - 1:2.31.90-2
- Update sources file

* Tue Aug 17 2010 Ray Strode <rstrode@redhat.com> - 1:2.31.90-1
- Update to 2.31.90

* Wed Jul 28 2010 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:2.30.2-4
- dist-git conversion

* Thu Jun 17 2010 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.30.2-3
- kill explicit library deps

* Tue Apr 27 2010 Ray Strode <rstrode@fedoraproject.org> - 1:2.30.2-2
- Update multistack patch - Add accounts service patch - Update plymouth
  patch

* Tue Apr 27 2010 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.30.2-1
- 2.30.2

* Tue Apr 06 2010 Ray Strode <rstrode@fedoraproject.org> - 1:2.30.0-2
- Update plymouth patch to work with 0.8.1

* Mon Mar 29 2010 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.30.0-1
- 2.30.0

* Wed Mar 24 2010 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.29.92-2
- update patch

* Wed Mar 24 2010 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.29.92-1
- 2.29.92

* Wed Mar 24 2010 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.29.6-4
- drop hal dep

* Fri Feb 12 2010 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.29.6-3
- Make ld happy

* Fri Feb 12 2010 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.29.6-2
- drop obsolete patches

* Thu Feb 11 2010 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.29.6-1
- 2.29.6

* Thu Jan 28 2010 Ray Strode <rstrode@fedoraproject.org> - 1:2.29.5-4
- name graphical-login vprovides (bug 559268)

* Wed Jan 27 2010 Ray Strode <rstrode@fedoraproject.org> - 1:2.29.5-3
- add missing patch

* Wed Jan 27 2010 Ray Strode <rstrode@fedoraproject.org> - 1:2.29.5-2
- update sources

* Wed Jan 27 2010 Ray Strode <rstrode@fedoraproject.org> - 1:2.29.5-1
- Update to 2.29.5

* Sun Jan 17 2010 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.29.4-4
- Rebuild

* Thu Jan 14 2010 Ray Strode <rstrode@fedoraproject.org> - 1:2.29.4-3
- hard code path

* Thu Jan 14 2010 Ray Strode <rstrode@fedoraproject.org> - 1:2.29.4-2
- Fix boot

* Tue Dec 22 2009 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.29.4-1
- 2.29.4

* Wed Dec 09 2009 Ray Strode <rstrode@fedoraproject.org> - 1:2.29.1-4
- Update to work better with latest plymouth

* Tue Dec 08 2009 Ray Strode <rstrode@fedoraproject.org> - 1:2.29.1-3
- Add xdmcp build req

* Thu Dec 03 2009 Ray Strode <rstrode@fedoraproject.org> - 1:2.29.1-2
- Drop upstreamed patches - rebase multi-stack patch

* Tue Dec 01 2009 Bastien Nocera <hadess@fedoraproject.org> - 1:2.29.1-1
- Update to 2.29.1

* Wed Nov 25 2009 Bill Nottingham <notting@fedoraproject.org> - 1:2.28.1-2
- Fix typo that causes a failure to update the common directory. (releng
  #2781)

* Mon Nov 02 2009 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.28.1-1
- Copy F12 work over

* Wed Oct 07 2009 Ray Strode <rstrode@fedoraproject.org> - 1:2.28.0-6
- Fix xguest

* Mon Sep 28 2009 Ray Strode <rstrode@fedoraproject.org> - 1:2.28.0-5
- Add cache dir to package manifest

* Mon Sep 28 2009 Richard Hughes <rhughes@fedoraproject.org> - 1:2.28.0-4
- Add a patch to use DeviceKit-power rather than the removed methods in
  gnome-power-manager.

* Fri Sep 25 2009 Ray Strode <rstrode@fedoraproject.org> - 1:2.28.0-3
- Fix autologin

* Wed Sep 23 2009 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.28.0-2
- fix patch

* Wed Sep 23 2009 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.28.0-1
- 2.28.0

* Sat Aug 29 2009 Caolan McNamara <caolanm@fedoraproject.org> - 1:2.27.90-3
- rebuild with new audit

* Mon Aug 24 2009 Ray Strode <rstrode@fedoraproject.org> - 1:2.27.90-2
- add buildrequires

* Mon Aug 24 2009 Ray Strode <rstrode@fedoraproject.org> - 1:2.27.90-1
- update to 2.27.90

* Fri Aug 21 2009 Tomáš Mráz <tmraz@fedoraproject.org> - 1:2.27.4-8
- rebuilt with new audit

* Wed Aug 19 2009 Lennart Poettering <lennart@fedoraproject.org> - 1:2.27.4-7
- Add pulseaudio-gdm-hooks to dependencies

* Thu Aug 06 2009 Ray Strode <rstrode@fedoraproject.org> - 1:2.27.4-6
- rebuild

* Sun Aug 02 2009 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.27.4-5
- drop unneded direct deps

* Fri Jul 24 2009 Ray Strode <rstrode@fedoraproject.org> - 1:2.27.4-4
- Fix delay during login

* Mon Jul 20 2009 Ray Strode <rstrode@fedoraproject.org> - 1:2.27.4-3
- Use correct multi-stack patch

* Mon Jul 20 2009 Ray Strode <rstrode@fedoraproject.org> - 1:2.27.4-2
- adding missing file

* Mon Jul 20 2009 Ray Strode <rstrode@fedoraproject.org> - 1:2.27.4-1
- Update to 2.27.4

* Thu Jul 02 2009 Adam Jackson <ajax@fedoraproject.org> - 1:2.26.1-14
- Requires: xorg-x11-xkb-utils -> Requires: setxkbmap

* Wed Jul 01 2009 Ray Strode <rstrode@fedoraproject.org> - 1:2.26.1-13
- Drop defunct arch conditional buildrequires

* Wed Jul 01 2009 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.26.1-12
- fix for xklavier api changes

* Tue Jun 30 2009 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.26.1-11
- Rebuild

* Fri Jun 12 2009 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.26.1-10
- Bump rev

* Tue Jun 09 2009 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.26.1-9
- fix spec

* Tue Jun 09 2009 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.26.1-8
- Port to PolicyKit 1

* Thu Jun 04 2009 Ray Strode <rstrode@fedoraproject.org> - 1:2.26.1-7
- drop erroneous bullets that snuck in during copy and paste

* Thu Jun 04 2009 Ray Strode <rstrode@fedoraproject.org> - 1:2.26.1-6
- Fix language parsing code (bug 502778)

* Mon Apr 27 2009 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.26.1-5
- don't drop schemas translations

* Fri Apr 24 2009 Ray Strode <rstrode@fedoraproject.org> - 1:2.26.1-4
- Add Requires for pam modules in plugins

* Tue Apr 21 2009 Ray Strode <rstrode@fedoraproject.org> - 1:2.26.1-3
- Stop inactive pam conversations when one succeeds. Should fix bug 496234

* Tue Apr 14 2009 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.26.1-2
- new sources

* Tue Apr 14 2009 Ray Strode <rstrode@fedoraproject.org> - 1:2.26.1-1
- Update to 2.26.1

* Mon Apr 13 2009 Ray Strode <rstrode@fedoraproject.org> - 1:2.26.0-9
- Ease up on patch fuzz requirements

* Mon Apr 13 2009 Ray Strode <rstrode@fedoraproject.org> - 1:2.26.0-8
- Add less boring multistack patch for testing

* Mon Mar 23 2009 Ray Strode <rstrode@fedoraproject.org> - 1:2.26.0-7
- Load session and language settings when username is read on Other user

* Fri Mar 20 2009 Ray Strode <rstrode@fedoraproject.org> - 1:2.26.0-6
- Fix problem in keyboard layout selector (483195)

* Thu Mar 19 2009 Ray Strode <rstrode@fedoraproject.org> - 1:2.26.0-5
- Use gethostname() _properly_ instead of g_get_host_name() when writing
  out xauth files, because the hostname may change out from under us and
  glib caches it.

* Thu Mar 19 2009 Ray Strode <rstrode@fedoraproject.org> - 1:2.26.0-4
- Use gethostname() instead of g_get_host_name() when writing out xauth
  files, because the hostname may change out from under us and glib caches
  it.

* Wed Mar 18 2009 Ray Strode <rstrode@fedoraproject.org> - 1:2.26.0-3
- emit "user-selected" signal for non-user items in the list as well.

* Tue Mar 17 2009 Ray Strode <rstrode@fedoraproject.org> - 1:2.26.0-2
- Clean up empty auth dirs so they don't hang around forever (bug 485974)

* Mon Mar 16 2009 Ray Strode <rstrode@fedoraproject.org> - 1:2.26.0-1
- Update to 2.26.0 - Drop gcc workaround. it might not be needed now.

* Sun Mar 15 2009 Ray Strode <rstrode@fedoraproject.org> - 1:2.25.2-21
- Drop the use localhost patch because it broke things. Instead add
  authorization that doesn't depend on a hostname

* Thu Mar 12 2009 Ray Strode <rstrode@fedoraproject.org> - 1:2.25.2-20
- Add a lame patch in the off chance it might work around a gcc bug on ppc:
  unable to find register to spill in class 'LINK_OR_CTR_REGS' Probably
  won't work.

* Thu Mar 12 2009 Ray Strode <rstrode@fedoraproject.org> - 1:2.25.2-19
- Actually add patch

* Thu Mar 12 2009 Ray Strode <rstrode@fedoraproject.org> - 1:2.25.2-18
- Add Requires: libXau >= 1.0.4-4 to use localhost in xauth cookies - Use
  localhost instead of g_get_host_name ()

* Thu Mar 12 2009 Ray Strode <rstrode@fedoraproject.org> - 1:2.25.2-17
- Don't force X server on active vt more than once

* Mon Mar 09 2009 Ray Strode <rstrode@fedoraproject.org> - 1:2.25.2-16
- Don't race with PAM modules that ask questions during pam_open_session
  (and don't subsequently go bonkers when losing the race).

* Fri Mar 06 2009 Ray Strode <rstrode@fedoraproject.org> - 1:2.25.2-15
- Reset "start session when ready" state to FALSE when starting new greeter
  from existing slave. May fix problem Chris Ball is seeing with language
  selection in autologin the second time after boot up.

* Thu Mar 05 2009 Ray Strode <rstrode@fedoraproject.org> - 1:2.25.2-14
- 2.25.2-10 fixes were actually only for timed login. Add same fix for auto
  login

* Thu Mar 05 2009 Ray Strode <rstrode@fedoraproject.org> - 1:2.25.2-13
- Create settings object early to prevent assertion failures when one pam
  conversation completes before another starts.

* Thu Mar 05 2009 Ray Strode <rstrode@fedoraproject.org> - 1:2.25.2-12
- Bring back language/session/layout selector for autologin

* Thu Mar 05 2009 Ray Strode <rstrode@fedoraproject.org> - 1:2.25.2-11
- Add some fixes for autologin

* Tue Mar 03 2009 Ray Strode <rstrode@fedoraproject.org> - 1:2.25.2-10
- Regen patch to get rid of fuzz

* Tue Mar 03 2009 Ray Strode <rstrode@fedoraproject.org> - 1:2.25.2-9
- Add limited 'one-stack-only' version of multistack patch (See
  https://fedoraproject.org/wiki/Features/MultiplePAMStacksInGDM) - Drop 10
  second delay in start up because of broken autostart file

* Fri Feb 27 2009 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.25.2-8
- Require PolicyKit-authentication-agent

* Wed Feb 25 2009 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.25.2-7
- refine hal patch

* Tue Feb 24 2009 Jesse Keating <jkeating@fedoraproject.org> - 1:2.25.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Feb 21 2009 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.25.2-5
- Improve handling of default keyboard layout

* Fri Feb 20 2009 Ray Strode <rstrode@fedoraproject.org> - 1:2.25.2-4
- add Provides: service(graphical-login) to help anaconda

* Thu Jan 22 2009 Ray Strode <rstrode@fedoraproject.org> - 1:2.25.2-3
- Open log files for append to make selinux lock down easier

* Thu Dec 18 2008 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.25.2-2
- drop xkb group workaround

* Wed Dec 17 2008 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.25.2-1
- 2.25.2

* Thu Dec 04 2008 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.25.1-2
- libtool fun

* Thu Dec 04 2008 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.25.1-1
- 2.25.1

* Mon Oct 20 2008 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.24.0-13
- respect system keyboard setting

* Wed Oct 15 2008 Ray Strode <rstrode@fedoraproject.org> - 1:2.24.0-12
- Rework "force X on vt1" code to work after the user logs out

* Wed Oct 15 2008 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.24.0-11
- save space

* Fri Oct 03 2008 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.24.0-10
- hide nonfunctional help menuitems

* Wed Oct 01 2008 Ray Strode <rstrode@fedoraproject.org> - 1:2.24.0-9
- add upstream bug reference

* Wed Oct 01 2008 Ray Strode <rstrode@fedoraproject.org> - 1:2.24.0-8
- Make panel slide in initially like the gnome panel

* Tue Sep 30 2008 Ray Strode <rstrode@fedoraproject.org> - 1:2.24.0-7
- pull patch from upstream to scale face icons with fontsize

* Tue Sep 30 2008 Ray Strode <rstrode@fedoraproject.org> - 1:2.24.0-6
- drop background priority change. Choppyiness in -3 ended up being a bug
  in gnome-settings-daemon.

* Thu Sep 25 2008 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.24.0-5
- require gnome-session

* Tue Sep 23 2008 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.24.0-4
- fix sound on the login screen

* Tue Sep 23 2008 Ray Strode <rstrode@fedoraproject.org> - 1:2.24.0-3
- Load background after everything else, so the crossfade isn't choppy.

* Mon Sep 22 2008 Ray Strode <rstrode@fedoraproject.org> - 1:2.24.0-2
- Fix permssions on spool dir

* Mon Sep 22 2008 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.24.0-1
- 2.24.0

* Mon Sep 22 2008 Ray Strode <rstrode@fedoraproject.org> - 1:2.23.92-11
- Flush X event queue after setting _XROOTPMAP_ID so there's no race with
  settings daemon reading the property

* Fri Sep 19 2008 Ray Strode <rstrode@fedoraproject.org> - 1:2.23.92-10
- Fix crash from language dialog

* Wed Sep 17 2008 Ray Strode <rstrode@fedoraproject.org> - 1:2.23.92-9
- canonicalize codeset to match output of locale -m - filter duplicates
  from language list

* Wed Sep 17 2008 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.23.92-8
- plug a few memory leaks

* Tue Sep 16 2008 Ray Strode <rstrode@fedoraproject.org> - 1:2.23.92-7
- Use _XROOTPMAP_ID instead of _XSETROOT_ID

* Tue Sep 16 2008 Ray Strode <rstrode@fedoraproject.org> - 1:2.23.92-6
- Save root window in XSETROOTID property for transition

* Fri Sep 12 2008 Ray Strode <rstrode@fedoraproject.org> - 1:2.23.92-5
- fix whitespace issue introduced from editing patch in place

* Fri Sep 12 2008 Ray Strode <rstrode@fedoraproject.org> - 1:2.23.92-4
- Fix bug in last patch

* Thu Sep 11 2008 Ray Strode <rstrode@fedoraproject.org> - 1:2.23.92-3
- Add hook to allow for plymouth transition

* Tue Sep 09 2008 William Jon McCann <mccann@fedoraproject.org> - 1:2.23.92-2
- Disallow root login

* Tue Sep 09 2008 William Jon McCann <mccann@fedoraproject.org> - 1:2.23.92-1
- Update to 2.23.92-1

* Thu Aug 28 2008 William Jon McCann <mccann@fedoraproject.org> - 1:2.23.91-2
- Update to non-broken snapshot

* Thu Aug 28 2008 William Jon McCann <mccann@fedoraproject.org> - 1:2.23.91-1
- Update to snapshot

* Tue Aug 26 2008 William Jon McCann <mccann@fedoraproject.org> - 1:2.23.90-2
- Add desktop file for metacity

* Mon Aug 25 2008 William Jon McCann <mccann@fedoraproject.org> - 1:2.23.90-1
- Update to 2.23.90

* Thu Aug 14 2008 Behdad Esfahbod <behdad@fedoraproject.org> - 1:2.23.2-4
- Add upstreamed patch gdm-2.23.2-unknown-lang.patch

* Wed Aug 13 2008 Ray Strode <rstrode@fedoraproject.org> - 1:2.23.2-3
- get rid of <<<< cvs spew

* Wed Aug 13 2008 Ray Strode <rstrode@fedoraproject.org> - 1:2.23.2-2
- Require plymouth-gdm-hooks so plymouth-log-viewer gets pulled in on
  upgrades

* Thu Jul 31 2008 William Jon McCann <mccann@fedoraproject.org> - 1:2.23.2-1
- Update to 2.23.2

* Mon Jul 28 2008 William Jon McCann <mccann@fedoraproject.org> - 1:2.23.1-4
- Update to newer snapshot

* Tue Jul 22 2008 William Jon McCann <mccann@fedoraproject.org> - 1:2.23.1-3
- Update to newer snapshot

* Mon Jul 21 2008 William Jon McCann <mccann@fedoraproject.org> - 1:2.23.1-2
- Update to new snapshot

* Mon Jul 21 2008 William Jon McCann <mccann@fedoraproject.org> - 1:2.23.1-1
- Update to snapshot

* Sat Jul 12 2008 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.22.0-16
- apply patch

* Thu Jul 10 2008 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.22.0-15
- fix some broken icons

* Thu Jul 10 2008 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.22.0-14
- improve rendering of languages

* Thu Jul 03 2008 William Jon McCann <mccann@fedoraproject.org> - 1:2.22.0-13
- Check for a null filesystem type

* Wed Jun 25 2008 Ray Strode <rstrode@fedoraproject.org> - 1:2.22.0-12
- After discussion with X team, turn tcp connections off by default, but
  add back option to toggle on (bug 446672)

* Wed Jun 25 2008 Ray Strode <rstrode@fedoraproject.org> - 1:2.22.0-11
- Add patch from last commit

* Wed Jun 25 2008 Ray Strode <rstrode@fedoraproject.org> - 1:2.22.0-10
- enable tcp connections by default

* Wed Jun 25 2008 Ray Strode <rstrode@fedoraproject.org> - 1:2.22.0-9
- Remove blank line at top of file

* Thu May 08 2008 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.22.0-8
- Add a GConf key to disable the user list

* Mon May 05 2008 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.22.0-7
- fix BRs

* Mon May 05 2008 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.22.0-6
- bump rev

* Mon May 05 2008 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.22.0-5
- autoreconf

* Mon May 05 2008 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.22.0-4
- add keyboard chooser

* Mon May 05 2008 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.22.0-3
- fix source url

* Fri May 02 2008 William Jon McCann <mccann@fedoraproject.org> - 1:2.22.0-2
- Retry tagging

* Fri May 02 2008 William Jon McCann <mccann@fedoraproject.org> - 1:2.22.0-1
- Update to 2.22.0 - Fix restarting when bus goes away

* Thu May 01 2008 Ray Strode <rstrode@fedoraproject.org> - 1:2.21.10-35
- ConsoleKit fixes - Don't show session selector if only one session
  installed - automatically pop up language/session selectors when using
  mnemonics

* Wed Apr 30 2008 William Jon McCann <mccann@fedoraproject.org> - 1:2.21.10-34
- Fix debugging - Fix resetting slave after session migration - Desensitize
  power buttons briefly after page switch - Remove Users: label from
  greeter

* Tue Apr 29 2008 William Jon McCann <mccann@fedoraproject.org> - 1:2.21.10-33
- make transient greeter less transient to workaround spurious vt switch

* Mon Apr 28 2008 Ray Strode <rstrode@fedoraproject.org> - 1:2.21.10-32
- a11y improvements - make "Suspend" desensitize properly when not-
  available - make resize animation faster - user switcher fixes

* Fri Apr 18 2008 Ray Strode <rstrode@fedoraproject.org> - 1:2.21.10-31
- Get Chinese back in language list

* Fri Apr 18 2008 Ray Strode <rstrode@fedoraproject.org> - 1:2.21.10-30
- start orca without main window - add missing priorities for plugins - add
  more failsafe lockdown

* Wed Apr 16 2008 Ray Strode <rstrode@fedoraproject.org> - 1:2.21.10-29
- add bug reference

* Wed Apr 16 2008 Ray Strode <rstrode@fedoraproject.org> - 1:2.21.10-28
- Disable typeahead when asking for password so password can't get shown in
  clear text

* Wed Apr 16 2008 Ray Strode <rstrode@fedoraproject.org> - 1:2.21.10-27
- Use start-here instead of fedora-logo-icon to aid generic-logos

* Sat Apr 12 2008 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.21.10-26
- Fix the XKB fix

* Fri Apr 11 2008 Ray Strode <rstrode@fedoraproject.org> - 1:2.21.10-25
- add missing "- "

* Fri Apr 11 2008 Ray Strode <rstrode@fedoraproject.org> - 1:2.21.10-24
- Fix security issue in last commit

* Fri Apr 11 2008 Ray Strode <rstrode@fedoraproject.org> - 1:2.21.10-23
- Fix focus handling when tabbing from user-chooser to buttons - don't set
  real uid to user before setcred - fix permissions on /var/run/gdm ...
  again

* Thu Apr 10 2008 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.21.10-22
- Work around a XKB problem

* Wed Apr 09 2008 Ray Strode <rstrode@fedoraproject.org> - 1:2.21.10-21
- Language list was incomplete (bug 441613)

* Tue Apr 08 2008 Ray Strode <rstrode@fedoraproject.org> - 1:2.21.10-20
- Fix permissions on /var/run/gdm

* Tue Apr 08 2008 Ray Strode <rstrode@fedoraproject.org> - 1:2.21.10-19
- Install X auth cookies in /var/run/gdm instead of /tmp

* Tue Apr 08 2008 Ray Strode <rstrode@fedoraproject.org> - 1:2.21.10-18
- Disable image for automatic login and other user - Act more sanely if
  gnome isn't installed

* Mon Apr 07 2008 Ray Strode <rstrode@fedoraproject.org> - 1:2.21.10-17
- Allow double-click to select language from list

* Mon Apr 07 2008 Ray Strode <rstrode@fedoraproject.org> - 1:2.21.10-16
- Make automatic login timer fade in - No more checkboxes in user-switch
  applet

* Mon Apr 07 2008 Ray Strode <rstrode@fedoraproject.org> - 1:2.21.10-15
- Focus face browser after failed login attempt - disable debug messages
  until 2.22.0 is released

* Sun Apr 06 2008 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.21.10-14
- Improve handling of CK error messages

* Sun Apr 06 2008 Ray Strode <rstrode@fedoraproject.org> - 1:2.21.10-13
- Fix jump in animation for autologin - Fix crash if LANG="somethingbogus"

* Sat Apr 05 2008 Ray Strode <rstrode@fedoraproject.org> - 1:2.21.10-12
- Fix crash when canceling autologin

* Sat Apr 05 2008 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.21.10-11
- fix handling of gconf schemas

* Thu Apr 03 2008 Ray Strode <rstrode@fedoraproject.org> - 1:2.21.10-10
- Update to snapshot - Improves shrink/grow animation of login window

* Thu Apr 03 2008 William Jon McCann <mccann@fedoraproject.org> - 1:2.21.10-9
- Update to snapshot

* Mon Mar 31 2008 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.21.10-8
- Fix a directory ownership oversight

* Wed Mar 26 2008 William Jon McCann <mccann@fedoraproject.org> - 1:2.21.10-7
- Fix build due to #436349

* Wed Mar 26 2008 William Jon McCann <mccann@fedoraproject.org> - 1:2.21.10-6
- Update to newer snapshot that includes more lockdown

* Wed Mar 26 2008 Ray Strode <rstrode@fedoraproject.org> - 1:2.21.10-5
- add unpackaged filed

* Wed Mar 26 2008 Ray Strode <rstrode@fedoraproject.org> - 1:2.21.10-4
- Update to snapshot - Turn on profiling

* Sat Mar 22 2008 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.21.10-3
- Drop dependency on theme package we don;t use

* Wed Mar 19 2008 Ray Strode <rstrode@fedoraproject.org> - 1:2.21.10-2
- Fix default path (bug 430187)

* Tue Mar 18 2008 William Jon McCann <mccann@fedoraproject.org> - 1:2.21.10-1
- Update to snapshot

* Mon Mar 17 2008 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.21.9-11
- implement tooltips in the language selection dialog

* Mon Mar 17 2008 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.21.9-10
- no fuse in the sandbox

* Tue Mar 11 2008 Ray Strode <rstrode@fedoraproject.org> - 1:2.21.9-9
- remove duplication signal definition from bad patch merge which led to
  crash for "Other" user

* Tue Mar 11 2008 William Jon McCann <mccann@fedoraproject.org> - 1:2.21.9-8
- Fix case where we can't lookup a user.

* Tue Mar 11 2008 William Jon McCann <mccann@fedoraproject.org> - 1:2.21.9-7
- Update to 2.21.9

* Mon Mar 10 2008 Ray Strode <rstrode@fedoraproject.org> - 1:2.21.9-6
- Prevent some spurious wake ups caused by the timed login timer animation

* Mon Mar 10 2008 Ray Strode <rstrode@fedoraproject.org> - 1:2.21.9-5
- add unpackaged files

* Mon Mar 10 2008 Ray Strode <rstrode@fedoraproject.org> - 1:2.21.9-4
- Update to latest snapshot

* Fri Mar 07 2008 David Woodhouse <dwmw2@fedoraproject.org> - 1:2.21.9-3
- fix endianness breakage

* Tue Mar 04 2008 Ray Strode <rstrode@fedoraproject.org> - 1:2.21.9-2
- Be more explicit in file list; use less globs - Don't package user-
  switcher in both packages!

* Fri Feb 29 2008 Ray Strode <rstrode@fedoraproject.org> - 1:2.21.9-1
- Update to snapshot - Split user-switcher out

* Tue Feb 26 2008 William Jon McCann <mccann@fedoraproject.org> - 1:2.21.8-1
- Update to 2.21.8

* Wed Feb 13 2008 William Jon McCann <mccann@fedoraproject.org> - 1:2.21.7-4
- Update to 2.21.7

* Sat Feb 09 2008 Ray Strode <rstrode@fedoraproject.org> - 1:2.21.7-3
- add a RPM_BUILD_ROOT where needed

* Sat Feb 09 2008 Ray Strode <rstrode@fedoraproject.org> - 1:2.21.7-2
- Add BuildRequires Fix changelog entry

* Sat Feb 09 2008 Ray Strode <rstrode@fedoraproject.org> - 1:2.21.7-1
- Update to snapshot

* Thu Jan 31 2008 William Jon McCann <mccann@fedoraproject.org> - 1:2.21.6-1
- Update to 2.21.6

* Thu Jan 24 2008 Ray Strode <rstrode@fedoraproject.org> - 1:2.21.5-2
- add BuildRequires for iso-codes-devel

* Fri Jan 18 2008 William Jon McCann <mccann@fedoraproject.org> - 1:2.21.5-1
- Update to 2.21.5

* Thu Jan 17 2008 William Jon McCann <mccann@fedoraproject.org> - 1:2.21.2-27
- Rebuild

* Mon Jan 14 2008 Daniel J Walsh <dwalsh@fedoraproject.org> - 1:2.21.2-26
- Fix gdm.pam file so that session include system-auth happens after other
  session setup

* Mon Jan 07 2008 Ray Strode <rstrode@fedoraproject.org> - 1:2.21.2-25
- hide guest account since it doesn't work

* Fri Dec 21 2007 Ray Strode <rstrode@fedoraproject.org> - 1:2.21.2-24
- Fix background (and other settings)

* Wed Dec 19 2007 Ray Strode <rstrode@fedoraproject.org> - 1:2.21.2-23
- Improve animation to be less jumpy

* Wed Dec 19 2007 Ray Strode <rstrode@fedoraproject.org> - 1:2.21.2-22
- drop unused patches

* Fri Dec 14 2007 Ray Strode <rstrode@fedoraproject.org> - 1:2.21.2-21
- one more time...

* Fri Dec 14 2007 Ray Strode <rstrode@fedoraproject.org> - 1:2.21.2-20
- fix typo from editing patch in place

* Fri Dec 14 2007 Ray Strode <rstrode@fedoraproject.org> - 1:2.21.2-19
- Fix an uninitialized variable that makes the session list stop growing
  before its finished sometimes

* Thu Dec 13 2007 Ray Strode <rstrode@fedoraproject.org> - 1:2.21.2-18
- add session chooser to login screen - add hoaky animations

* Fri Nov 30 2007 Ray Strode <rstrode@fedoraproject.org> - 1:2.21.2-17
- add missing patch

* Fri Nov 30 2007 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.21.2-16
- Make keyring unlocking work

* Wed Nov 21 2007 Ray Strode <rstrode@fedoraproject.org> - 1:2.21.2-15
- use metacity for now

* Tue Nov 20 2007 Ray Strode <rstrode@fedoraproject.org> - 1:2.21.2-14
- Drop dont run profile patch since dwalsh changed /usr/sbin/gdm label

* Tue Nov 20 2007 Ray Strode <rstrode@fedoraproject.org> - 1:2.21.2-13
- Update to today's snapshot

* Mon Nov 19 2007 Ray Strode <rstrode@fedoraproject.org> - 1:2.21.2-12
- fix permissions on homedir

* Mon Nov 19 2007 Ray Strode <rstrode@fedoraproject.org> - 1:2.21.2-11
- move homedir to /var/lib/gdm

* Mon Nov 19 2007 Ray Strode <rstrode@fedoraproject.org> - 1:2.21.2-10
- more file list fixups

* Mon Nov 19 2007 Ray Strode <rstrode@fedoraproject.org> - 1:2.21.2-9
- add other patch

* Mon Nov 19 2007 Ray Strode <rstrode@fedoraproject.org> - 1:2.21.2-8
- add dropped patch

* Mon Nov 19 2007 Ray Strode <rstrode@fedoraproject.org> - 1:2.21.2-7
- update filelist

* Mon Nov 19 2007 Ray Strode <rstrode@fedoraproject.org> - 1:2.21.2-6
- Update to today's snapshot

* Thu Nov 15 2007 Ray Strode <rstrode@fedoraproject.org> - 1:2.21.2-5
- don't source /etc/profile at startup

* Wed Nov 14 2007 Ray Strode <rstrode@fedoraproject.org> - 1:2.21.2-4
- Update to today's snapshot

* Fri Nov 09 2007 Ray Strode <rstrode@fedoraproject.org> - 1:2.21.2-3
- one more time...

* Fri Nov 09 2007 Ray Strode <rstrode@fedoraproject.org> - 1:2.21.2-2
- s/config/data/

* Fri Nov 09 2007 Ray Strode <rstrode@fedoraproject.org> - 1:2.21.2-1
- Update to today's snapshot

* Tue Oct 30 2007 Ray Strode <rstrode@fedoraproject.org> - 1:2.21.1-5
- Update to today's snapshot

* Tue Oct 30 2007 Ray Strode <rstrode@fedoraproject.org> - 1:2.21.1-4
- Update to today's snapshot

* Wed Oct 24 2007 Ray Strode <rstrode@fedoraproject.org> - 1:2.21.1-3
- Update to today's snapshot

* Mon Oct 22 2007 Ray Strode <rstrode@fedoraproject.org> - 1:2.21.1-2
- remove some upstreamed patches

* Mon Oct 22 2007 Ray Strode <rstrode@fedoraproject.org> - 1:2.21.1-1
- Add a snapshot gdm trunk, totally different unfinished ui...

* Wed Oct 17 2007 Daniel J Walsh <dwalsh@fedoraproject.org> - 1:2.99.0-4
- keyinit has to happen after selinux open

* Mon Oct 15 2007 Bill Nottingham <notting@fedoraproject.org> - 1:2.99.0-3
- makefile update to properly grab makefile.common

* Sun Oct 14 2007 Ray Strode <rstrode@fedoraproject.org> - 1:2.99.0-2
- update patches

* Sun Oct 14 2007 Ray Strode <rstrode@fedoraproject.org> - 1:2.99.0-1
- Add a snapshot from the mccann-gobject branch, totally different
  unfinished ui...

* Fri Oct 05 2007 Daniel J Walsh <dwalsh@fedoraproject.org> - 1:2.20.0-18
- Update spec for pam changes

* Fri Oct 05 2007 Daniel J Walsh <dwalsh@fedoraproject.org> - 1:2.20.0-17
- add pam_selinux_permit and pam_namespace so xguest autologin will work
  and pam_namespace will work

* Wed Oct 03 2007 Alexander Larsson <alexl@fedoraproject.org> - 1:2.20.0-16
- Fix up pam keyring integration to be what the latest version of the docs
  says

* Tue Oct 02 2007 Ray Strode <rstrode@fedoraproject.org> - 1:2.20.0-15
- Actually add said escape == cancel behavior back

* Tue Oct 02 2007 Ray Strode <rstrode@fedoraproject.org> - 1:2.20.0-14
- Add escape == cancel behavior back

* Mon Oct 01 2007 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.20.0-13
- fix a reference handling issue

* Mon Oct 01 2007 Ray Strode <rstrode@fedoraproject.org> - 1:2.20.0-12
- apply upstream patch from Brady Anderson <brady.anderson@gmail.com> to
  fix writing out .dmrc file when setting default language (upstream bug
  453916)

* Fri Sep 28 2007 Ray Strode <rstrode@fedoraproject.org> - 1:2.20.0-11
- drop redhat-artwork dep, add fedorainfinity-gdm-theme dep

* Fri Sep 28 2007 Ray Strode <rstrode@fedoraproject.org> - 1:2.20.0-10
- update bug link

* Fri Sep 28 2007 Ray Strode <rstrode@fedoraproject.org> - 1:2.20.0-9
- Another crack at 240853

* Fri Sep 28 2007 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.20.0-8
- fix the stupid bullets

* Thu Sep 27 2007 Ray Strode <rstrode@fedoraproject.org> - 1:2.20.0-7
- The previously mentioned typo didn't matter before because the compiled
  in default matched what the config file was supposed to say. This commit
  restores matched default behavior (bug 301031)

* Thu Sep 27 2007 Ray Strode <rstrode@fedoraproject.org> - 1:2.20.0-6
- Fix an apparent typo in the securitytokens.conf config file (bug 301031)

* Thu Sep 20 2007 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.20.0-5
- reenable root login

* Wed Sep 19 2007 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.20.0-4
- FedoraInfinity

* Wed Sep 19 2007 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.20.0-3
- fix a hang

* Tue Sep 18 2007 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.20.0-2
- re-add faces to sources

* Tue Sep 18 2007 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.20.0-1
- 2.20.0

* Wed Sep 12 2007 Ray Strode <rstrode@fedoraproject.org> - 1:2.19.8-7
- Change default password character back to circle instead of asterisk (bug
  287951)

* Fri Sep 07 2007 Ray Strode <rstrode@fedoraproject.org> - 1:2.19.8-6
- add buildrequires for libselinux-devel

* Fri Sep 07 2007 Ray Strode <rstrode@fedoraproject.org> - 1:2.19.8-5
- rev release

* Fri Sep 07 2007 Ray Strode <rstrode@fedoraproject.org> - 1:2.19.8-4
- rebuild --with-selinux

* Fri Sep 07 2007 Ray Strode <rstrode@fedoraproject.org> - 1:2.19.8-3
- rev release

* Fri Sep 07 2007 Ray Strode <rstrode@fedoraproject.org> - 1:2.19.8-2
- make things work better for xguest users (bug 254164)

* Fri Sep 07 2007 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.19.8-1
- 2.19.8

* Tue Sep 04 2007 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.19.7-1
- 2.19.7

* Fri Aug 24 2007 Ray Strode <rstrode@fedoraproject.org> - 1:2.19.6-9
- use pam_selinux instead of home grown selinux code (bug 254164)

* Wed Aug 22 2007 Kristian Høgsberg <krh@fedoraproject.org> - 1:2.19.6-8
- Pass -br to the default X server too.

* Sat Aug 18 2007 Ray Strode <rstrode@fedoraproject.org> - 1:2.19.6-7
- update previous changelog entry to actually make sense

* Sat Aug 18 2007 Ray Strode <rstrode@fedoraproject.org> - 1:2.19.6-6
- le sigh

* Sat Aug 18 2007 Ray Strode <rstrode@fedoraproject.org> - 1:2.19.6-5
- disable root password (see "low-hanging fruit" discussion on fedora-
  desktop-list)

* Thu Aug 16 2007 Ray Strode <rstrode@fedoraproject.org> - 1:2.19.6-4
- disable type ahead in user list (bug 252991)

* Thu Aug 16 2007 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.19.6-3
- use find_lang for help files

* Thu Aug 16 2007 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.19.6-2
- re-add faces to sources

* Thu Aug 16 2007 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.19.6-1
- 2.19.6

* Mon Aug 13 2007 Adam Jackson <ajax@fedoraproject.org> - 1:2.19.5-11
- Remove the filereq on /etc/pam.d/system-auth, pam alone is sufficient. -
  Bump the pam requirement to 0.99, 0.75 is ancient.

* Sun Aug 12 2007 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.19.5-10
- fix the previous fix

* Sun Aug 12 2007 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.19.5-9
- make gdmsetup work with consolehelper and pam, again

* Mon Aug 06 2007 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.19.5-8
- remove a conflict marker

* Mon Aug 06 2007 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.19.5-7
- require gnome-keyring-pam

* Mon Aug 06 2007 Ray Strode <rstrode@fedoraproject.org> - 1:2.19.5-6
- change previous patch to drop even more code

* Mon Aug 06 2007 Ray Strode <rstrode@fedoraproject.org> - 1:2.19.5-5
- turn off dwellmouselistener if devices don't send core events. don't warp
  pointer to stylus ever (upstream bug 457998)

* Fri Aug 03 2007 Ray Strode <rstrode@fedoraproject.org> - 1:2.19.5-4
- remove dwellmouselistener module from default configuration. It's pretty
  broken (bug 248752)

* Fri Aug 03 2007 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.19.5-3
- update license field

* Tue Jul 31 2007 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.19.5-2
- update sources

* Tue Jul 31 2007 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.19.5-1
- 2.19.5

* Mon Jul 30 2007 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.19.4-3
- add optional gnome-keyring support to the gdm pam stack

* Wed Jul 11 2007 Ray Strode <rstrode@fedoraproject.org> - 1:2.19.4-2
- update sources file

* Wed Jul 11 2007 Ray Strode <rstrode@fedoraproject.org> - 1:2.19.4-1
- Update to 2.19.4

* Thu Jun 28 2007 Ray Strode <rstrode@fedoraproject.org> - 1:2.19.3-4
- set Browser=true by default

* Wed Jun 27 2007 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.19.3-3
- drop unneeded requires

* Mon Jun 18 2007 Ray Strode <rstrode@fedoraproject.org> - 1:2.19.3-2
- add sources file

* Mon Jun 18 2007 Ray Strode <rstrode@fedoraproject.org> - 1:2.19.3-1
- Update to 2.19.3

* Tue Jun 05 2007 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.19.2-3
- Fix file list

* Tue Jun 05 2007 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.19.2-2
- Fix up file lists

* Tue Jun 05 2007 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.19.2-1
- 2.19.2

* Tue May 22 2007 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.19.1-10
- remove wrong bug ref

* Mon May 21 2007 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.19.1-9
- move patch fixes

* Mon May 21 2007 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.19.1-8
- grr, syslog missing

* Mon May 21 2007 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.19.1-7
- another try

* Mon May 21 2007 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.19.1-6
- fix another patch

* Mon May 21 2007 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.19.1-5
- more display list fixing

* Mon May 21 2007 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.19.1-4
- fix patch

* Mon May 21 2007 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.19.1-3
- fix patch

* Mon May 21 2007 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.19.1-2
- fix sources

* Mon May 21 2007 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.19.1-1
- Update tons of patches

* Tue May 15 2007 Ray Strode <rstrode@fedoraproject.org> - 1:2.18.0-22
- remove erroneous patch line

* Tue May 15 2007 Ray Strode <rstrode@fedoraproject.org> - 1:2.18.0-21
- hide users from userlist that have disabled shells (bug 240148)

* Fri May 11 2007 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.18.0-20
- Follow packaging guidelines for scrollkeeper dependencies

* Mon May 07 2007 Ray Strode <rstrode@fedoraproject.org> - 1:2.18.0-19
- reenable utmp logging (bug 209537)

* Thu May 03 2007 Ray Strode <rstrode@fedoraproject.org> - 1:2.18.0-18
- i'm going to say "spandex" now, so I hope no one is reading

* Tue Apr 17 2007 Ray Strode <rstrode@fedoraproject.org> - 1:2.18.0-17
- Be more verbose to help isolate the problem in bug 234567

* Thu Apr 12 2007 Ray Strode <rstrode@fedoraproject.org> - 1:2.18.0-16
- add "Default" session back to the sessions menu (bug 234218)

* Thu Apr 05 2007 Ray Strode <rstrode@fedoraproject.org> - 1:2.18.0-15
- grr fix typo in patch

* Thu Apr 05 2007 Ray Strode <rstrode@fedoraproject.org> - 1:2.18.0-14
- add upstream bug reference for "hide uninstalled languages" patch

* Thu Apr 05 2007 Ray Strode <rstrode@fedoraproject.org> - 1:2.18.0-13
- don't expect utf-8 usernames for plain greeter face browser either.

* Thu Apr 05 2007 Ray Strode <rstrode@fedoraproject.org> - 1:2.18.0-12
- don't expect utf8 in plain greeter either

* Thu Apr 05 2007 Ray Strode <rstrode@fedoraproject.org> - 1:2.18.0-11
- don't expect utf-8 usernames for face browser (bug 235351).

* Thu Mar 29 2007 Ray Strode <rstrode@fedoraproject.org> - 1:2.18.0-10
- don't strcpy overlapping strings (bug 208181).

* Tue Mar 27 2007 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.18.0-9
- Hide gdmphotosetup

* Tue Mar 20 2007 Ray Strode <rstrode@fedoraproject.org> - 1:2.18.0-8
- add bugzilla reference

* Tue Mar 20 2007 Ray Strode <rstrode@fedoraproject.org> - 1:2.18.0-7
- add fix to allow themes to cope with low resolution modes better (bug
  232672)

* Tue Mar 20 2007 Ray Strode <rstrode@fedoraproject.org> - 1:2.18.0-6
- uncomment securitytoken conf file from file list

* Tue Mar 20 2007 Ray Strode <rstrode@fedoraproject.org> - 1:2.18.0-5
- update and reenable security token patch

* Tue Mar 20 2007 David Zeuthen <davidz@fedoraproject.org> - 1:2.18.0-4
- Also pass AT's to the session from the plain greeter (#232518) - New
  faces including new subpackage gdm-extra-faces

* Tue Mar 13 2007 David Zeuthen <davidz@fedoraproject.org> - 1:2.18.0-3
- bump

* Tue Mar 13 2007 David Zeuthen <davidz@fedoraproject.org> - 1:2.18.0-2
- Update to upstream release 2.18.0 - Switch default theme to
  FedoraFlyingHigh and show /etc/passwd users - Fix accessibility in the
  themed greeter (GNOME #412576) - Enable accessible login, make sure gdm
  can access devices and pass activated AT's to the login session (#229912)
  - Disable smart card login for now as patch doesn't apply anymore

* Tue Mar 13 2007 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.18.0-1
- 2.18.0

* Fri Mar 09 2007 Ray Strode <rstrode@fedoraproject.org> - 1:2.17.8-4
- fix a typo in patch

* Fri Mar 09 2007 Ray Strode <rstrode@fedoraproject.org> - 1:2.17.8-3
- hide langauges that aren't displayable from the list (bug 206048)

* Tue Mar 06 2007 Ray Strode <rstrode@fedoraproject.org> - 1:2.17.8-2
- turn off pam sanity check because it conflicts with audit

* Wed Feb 28 2007 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.17.8-1
- 2.17.8

* Sat Feb 24 2007 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.17.7-6
- fix keynav in the face browser

* Sat Feb 24 2007 David Zeuthen <davidz@fedoraproject.org> - 1:2.17.7-5
- Add some enhancements to the greeter (bgo #411427)

* Sat Feb 24 2007 Ray Strode <rstrode@fedoraproject.org> - 1:2.17.7-4
- readd audit patch

* Sat Feb 24 2007 Ray Strode <rstrode@fedoraproject.org> - 1:2.17.7-3
- drop the dot

* Sat Feb 24 2007 Ray Strode <rstrode@fedoraproject.org>
- Update to 2.17.7

* Fri Feb 23 2007 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.17.7-1
- small fixes

* Mon Feb 12 2007 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.17.6-4
- more fast user switching fixups

* Sat Feb 10 2007 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.17.6-3
- fix a consolekit problem

* Wed Feb 07 2007 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.17.6-2
- improve fast user switching experience

* Tue Jan 23 2007 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.17.6-1
- 2.17.6

* Sat Jan 13 2007 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.17.5-2
- Enable ConsoleKit

* Thu Jan 11 2007 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.17.5-1
- 2.17.5

* Fri Dec 15 2006 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.17.4-2
- fix spec

* Fri Dec 15 2006 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.17.4-1
- 2.17.4

* Tue Dec 05 2006 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.17.3-2
- 2.17.3

* Tue Dec 05 2006 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.17.3-1
- 2.17.3

* Tue Nov 07 2006 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.17.2-1
- 2.17.2

* Sun Nov 05 2006 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.17.1-1
- 2.17.1

* Thu Oct 26 2006 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.17.0-2
- fix a gdm crash

* Mon Oct 23 2006 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.17.0-1
- 2.17.0

* Tue Oct 17 2006 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.16.0-17
- fix a nonworking help button

* Mon Oct 16 2006 Ray Strode <rstrode@fedoraproject.org> - 1:2.16.0-16
- don't log canceled pam conversations as failed login attempts

* Sun Oct 15 2006 Ray Strode <rstrode@fedoraproject.org> - 1:2.16.0-15
- Prefer modules in secmod db over hardcoded coolkey path

* Sun Oct 15 2006 Ray Strode <rstrode@fedoraproject.org> - 1:2.16.0-14
- have security token monitor helper process kill itself when the
  communication pipe to the main process goes away (bug 210677).

* Fri Oct 13 2006 Ray Strode <rstrode@fedoraproject.org> - 1:2.16.0-13
- desensitize entry fields until pam asks for input, so if pam doesn't
  initially ask for input (like in smart card required mode) the user can't
  type something and confuse gdm (bug 201344)

* Fri Oct 06 2006 Ray Strode <rstrode@fedoraproject.org> - 1:2.16.0-12
- invoke standard X server with -br option to ensure we get a black root on
  startup

* Fri Oct 06 2006 Ray Strode <rstrode@fedoraproject.org> - 1:2.16.0-11
- make monitoring code more reliable (bug 208018)

* Wed Sep 27 2006 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.16.0-10
- Fix a small gdmsetup bug

* Wed Sep 27 2006 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.16.0-9
- fix a markup problem

* Tue Sep 19 2006 Ray Strode <rstrode@fedoraproject.org> - 1:2.16.0-8
- Add as_IN, si_LK to language list (bug 203917)

* Mon Sep 18 2006 Ray Strode <rstrode@fedoraproject.org> - 1:2.16.0-7
- fix a problem recently introduced in the smart card forking code

* Mon Sep 18 2006 Ray Strode <rstrode@fedoraproject.org> - 1:2.16.0-6
- fix a problem recently introduced in the smart card driver loading code
  (bug 206882)

* Fri Sep 15 2006 Ray Strode <rstrode@fedoraproject.org> - 1:2.16.0-5
- don't leak pipe fds (bug 206709)

* Thu Sep 14 2006 Ray Strode <rstrode@fedoraproject.org> - 1:2.16.0-4
- update security token patch to not poll

* Sat Sep 09 2006 Jesse Keating <jkeating@fedoraproject.org> - 1:2.16.0-3
- use correct defaults patch

* Thu Sep 07 2006 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.16.0-2
- Use new default theme

* Tue Sep 05 2006 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.16.0-1
- 2.16.0

* Sat Aug 26 2006 Karsten Hopp <karsten@fedoraproject.org> - 1:2.15.10-3
- buildrequire inttools as this isn't a requirement of scrollkeeper anymore
  and thus missing from the buildroot

* Mon Aug 21 2006 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.15.10-2
- drop patch

* Mon Aug 21 2006 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.15.10-1
- 2.15.10

* Mon Aug 14 2006 Ray Strode <rstrode@fedoraproject.org> - 1:2.15.9-1
- update to 2.15.9

* Fri Aug 04 2006 Ray Strode <rstrode@fedoraproject.org> - 1:2.15.7-4
- update gdmsetup pam file to use config-util stacks

* Thu Aug 03 2006 Ray Strode <rstrode@fedoraproject.org> - 1:2.15.7-3
- add new source tarball

* Thu Aug 03 2006 Ray Strode <rstrode@fedoraproject.org> - 1:2.15.7-2
- update to 2.15.7 - drop selinux patch that I don't think was ever
  finished

* Thu Aug 03 2006 Ray Strode <rstrode@fedoraproject.org> - 1:2.15.7-1
- update to 2.15.7

* Thu Aug 03 2006 Ray Strode <rstrode@fedoraproject.org> - 1:2.15.6-15
- fix face browser (http://bugzilla.gnome.org/show_bug.cgi?id=349640) - fix
  error message reporting
  (http://bugzilla.gnome.org/show_bug.cgi?id=349758)

* Sat Jul 22 2006 Ray Strode <rstrode@fedoraproject.org> - 1:2.15.6-14
- simplify all the security token code by only using one pam stack - drop
  lame kill on token removal feature

* Fri Jul 21 2006 Ray Strode <rstrode@fedoraproject.org> - 1:2.15.6-13
- move authcookies out of home directories to prevent problems on nfs/afs
  mounted home directories (bug 178233).

* Fri Jul 21 2006 Ray Strode <rstrode@fedoraproject.org> - 1:2.15.6-12
- really fix annoying dialog problem mentioned in 2.15.6-6

* Wed Jul 19 2006 Ray Strode <rstrode@fedoraproject.org> - 1:2.15.6-11
- center cursor on xinerama head (bug 180085)

* Wed Jul 19 2006 Ray Strode <rstrode@fedoraproject.org> - 1:2.15.6-10
- add "kill all sessions on token removal" feature

* Tue Jul 18 2006 Ray Strode <rstrode@fedoraproject.org> - 1:2.15.6-9
- rev release

* Tue Jul 18 2006 Ray Strode <rstrode@fedoraproject.org> - 1:2.15.6-8
- reenable session keyring support in pam module (bug 198629)

* Tue Jul 18 2006 Ray Strode <rstrode@fedoraproject.org> - 1:2.15.6-7
- add /etc/gdm/securitytoken.conf to file list

* Tue Jul 18 2006 Ray Strode <rstrode@fedoraproject.org> - 1:2.15.6-6
- make security token support use its own config file in preparation for
  modularizing it.

* Mon Jul 17 2006 Ray Strode <rstrode@fedoraproject.org> - 1:2.15.6-5
- fix off-by-one in the process-all-ops patch that was causing an anoying
  dialog to pop up on each login

* Mon Jul 17 2006 Ray Strode <rstrode@fedoraproject.org> - 1:2.15.6-4
- add initial wtmp and btmp logging support 2.15.6-4 - fix bug in security
  token support

* Fri Jul 14 2006 Ray Strode <rstrode@fedoraproject.org> - 1:2.15.6-3
- fix hang in gdmsetup

* Fri Jul 14 2006 Ray Strode <rstrode@fedoraproject.org> - 1:2.15.6-2
- put new pam module at top of stack (bug 198629)

* Wed Jul 12 2006 Ray Strode <rstrode@fedoraproject.org> - 1:2.15.6-1
- Update to 2.15.6

* Wed Jul 12 2006 Ray Strode <rstrode@fedoraproject.org> - 1:2.15.5-9
- add new pam module to pam files to support kernel session keyring

* Wed Jul 12 2006 Jesse Keating <jkeating@fedoraproject.org> - 1:2.15.5-8
- bumped for rebuild

* Wed Jul 12 2006 Ray Strode <rstrode@fedoraproject.org> - 1:2.15.5-7
- add missing buildrequires

* Wed Jul 12 2006 Ray Strode <rstrode@fedoraproject.org> - 1:2.15.5-6
- add initial support for smart card security tokens

* Fri Jul 07 2006 Ray Strode <rstrode@fedoraproject.org> - 1:2.15.5-5
- rev release

* Fri Jul 07 2006 Ray Strode <rstrode@fedoraproject.org> - 1:2.15.5-4
- add patch to process all operations when more than one comes in really
  quickly - move default "Please enter your username" message to the
  greeter instead of the slave so that it doesn't get stacked if a pam
  module has a non default message - add new message for reseting the
  current login operation (like the cancel button does, but accessible via
  the gdm fifo)

* Tue Jun 13 2006 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.15.5-3
- drop more patches

* Tue Jun 13 2006 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.15.5-2
- drop upstreamed patches

* Tue Jun 13 2006 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.15.5-1
- 2.15.5

* Tue Jun 13 2006 Bill Nottingham <notting@fedoraproject.org> - 1:2.15.3-13
- we call automake-1.9, don't buildreq automake14

* Thu Jun 08 2006 Ray Strode <rstrode@fedoraproject.org> - 1:2.15.3-12
- fix CVE-2006-2452

* Wed Jun 07 2006 Jeremy Katz <katzj@fedoraproject.org> - 1:2.15.3-11
- no xserver on ppc64 yet

* Wed Jun 07 2006 Jeremy Katz <katzj@fedoraproject.org> - 1:2.15.3-10
- fix s390 build

* Wed Jun 07 2006 Jeremy Katz <katzj@fedoraproject.org> - 1:2.15.3-9
- buildrequire the server so that we get the path right in the config file

* Tue Jun 06 2006 Karsten Hopp <karsten@fedoraproject.org> - 1:2.15.3-8
- gdm looses DMX support when built in mock/brew without buildrequiring
  libdmx-devel

* Mon Jun 05 2006 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.15.3-7
- fix requires

* Tue May 23 2006 Ray Strode <rstrode@fedoraproject.org> - 1:2.15.3-6
- Support xdm -nodaemon option (bug 192461)

* Mon May 22 2006 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.15.3-5
- fix build reqs

* Mon May 22 2006 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.15.3-4
- fix build reqs

* Thu May 18 2006 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.15.3-3
- make it build`

* Wed May 17 2006 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.15.3-2
- remove obsolete patch

* Wed May 17 2006 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.15.3-1
- 2.15.3

* Wed May 10 2006 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.15.0-2
- make it compile

* Wed May 10 2006 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.15.0-1
- 2.15.0

* Wed Apr 26 2006 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.14.4-1
- 2.14.4

* Wed Apr 12 2006 Ray Strode <rstrode@fedoraproject.org> - 1:2.14.1-4
- fix libexecdir substitution problem in configuration file

* Tue Apr 11 2006 Ray Strode <rstrode@fedoraproject.org> - 1:2.14.1-3
- Add gdmthemetester.in to the mix (upstream bug 338079)

* Tue Apr 11 2006 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.14.1-2
- 2.14.1

* Tue Apr 11 2006 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.14.1-1
- 2.14.1

* Mon Mar 13 2006 Ray Strode <rstrode@fedoraproject.org> - 1:2.14.0-1
- Update to 2.14.0

* Tue Mar 07 2006 Ray Strode <rstrode@fedoraproject.org> - 1:2.13.0.9-4
- Follow Solaris's lead and default to AlwaysRestartServer=True (may work
  around bug 182957)

* Tue Mar 07 2006 Ray Strode <rstrode@fedoraproject.org> - 1:2.13.0.9-3
- migrate users with baseXsession=/etc/X11/gdm/Xsession to
  /etc/X11/xinit/Xsession

* Mon Mar 06 2006 Ray Strode <rstrode@fedoraproject.org> - 1:2.13.0.9-2
- disable sounds completely when disabled in configuration file (upstream
  bug 333435)

* Tue Feb 28 2006 Ray Strode <rstrode@fedoraproject.org> - 1:2.13.0.9-1
- Update to 2.13.0.9 - Use new %%%%post section, written by Michal
  Jaegermann <michal@harddata.com> (bug 183082)

* Sun Feb 26 2006 Ray Strode <rstrode@fedoraproject.org> - 1:2.13.0.8-8
- Use new %%%%post section, written by Michal Jaegermann
  <michal@harddata.com> (bug 183082)

* Sat Feb 25 2006 Ray Strode <rstrode@fedoraproject.org> - 1:2.13.0.8-7
- fix a broken link

* Fri Feb 24 2006 Ray Strode <rstrode@fedoraproject.org> - 1:2.13.0.8-6
- change some /etc/X11 bits in the spec file to /etc

* Fri Feb 24 2006 Ray Strode <rstrode@fedoraproject.org> - 1:2.13.0.8-5
- change some /etc/X11 bits in the spec file to /etc

* Sun Feb 19 2006 Ray Strode <rstrode@fedoraproject.org> - 1:2.13.0.8-4
- add server entry for accel-indirect branch of xorg

* Wed Feb 15 2006 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.13.0.8-3
- fix a double free crash

* Mon Feb 13 2006 Ray Strode <rstrode@fedoraproject.org> - 1:2.13.0.8-2
- s/bz2/gz/

* Mon Feb 13 2006 Ray Strode <rstrode@fedoraproject.org> - 1:2.13.0.8-1
- update to 2.13.0.8

* Mon Feb 13 2006 Ray Strode <rstrode@fedoraproject.org> - 1:2.13.0.7.0.2006.02.12-2
- migrate custom.conf settings with /etc/X11/gdm to /etc/gdm

* Sun Feb 12 2006 Ray Strode <rstrode@fedoraproject.org> - 1:2.13.0.7.0.2006.02.12-1
- update to cvs snapshot - move gdm to /etc instead of /etc/X11 - move
  custom gdm.conf to sysconfdir instead of symlinking from datadir (bug
  180364)

* Sat Feb 11 2006 Jesse Keating <jkeating@fedoraproject.org> - 1:2.13.0.7-5
- bump for bug in double-long on ppc(64)

* Thu Feb 09 2006 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.13.0.7-4
- misc fixes

* Thu Feb 09 2006 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.13.0.7-3
- misc fixes

* Tue Feb 07 2006 Jesse Keating <jkeating@fedoraproject.org> - 1:2.13.0.7-2
- bump for new gcc/glibc

* Tue Jan 31 2006 Ray Strode <rstrode@fedoraproject.org> - 1:2.13.0.7-1
- update to 2.13.0.7

* Mon Jan 30 2006 Bill Nottingham <notting@fedoraproject.org> - 1:2.13.0.5-7
- be quiet! :)

* Thu Jan 19 2006 Ray Strode <rstrode@fedoraproject.org> - 1:2.13.0.5-6
- sed -ie isn't the same as sed -i -e (we want the latter)

* Thu Jan 19 2006 Ray Strode <rstrode@fedoraproject.org> - 1:2.13.0.5-5
- sed -ie isn't the same as sed -i -e (we want the latter)

* Thu Jan 19 2006 Christopher Aillon <caillon@fedoraproject.org> - 1:2.13.0.5-4
- Add patch to fix clock to default to 24h in locales that expect it
  (175453)

* Wed Jan 18 2006 Bill Nottingham <notting@fedoraproject.org> - 1:2.13.0.5-3
- UTF8!

* Tue Jan 17 2006 Ray Strode <rstrode@fedoraproject.org> - 1:2.13.0.5-2
- remove selinux patch

* Tue Jan 17 2006 Ray Strode <rstrode@fedoraproject.org> - 1:2.13.0.5-1
- update to 2.13.0.5 (bug 178099)

* Tue Jan 17 2006 Ray Strode <rstrode@fedoraproject.org> - 1:2.13.0.4-9
- add new theme by Diana Fong, Máirín Duffy, and me

* Mon Jan 16 2006 Ray Strode <rstrode@fedoraproject.org> - 1:2.13.0.4-8
- improve migration snippet (bug 177443).

* Mon Jan 16 2006 Ray Strode <rstrode@fedoraproject.org> - 1:2.13.0.4-7
- add patch3 back

* Mon Jan 16 2006 Ray Strode <rstrode@fedoraproject.org> - 1:2.13.0.4-6
- migrate to new greeter location (bug 177443).

* Fri Jan 13 2006 Ray Strode <rstrode@fedoraproject.org> - 1:2.13.0.4-5
- migrate X server configuration for pre-modular X configurations. Problems
  reported by Dennis Gregorovic <dgregor@redhat.com>

* Mon Jan 09 2006 Ray Strode <rstrode@fedoraproject.org> - 1:2.13.0.4-4
- use xinit Xsession again.

* Mon Jan 09 2006 Ray Strode <rstrode@fedoraproject.org> - 1:2.13.0.4-3
- update sources

* Mon Jan 09 2006 Ray Strode <rstrode@fedoraproject.org> - 1:2.13.0.4-2
- fix changelog entry year to be right

* Mon Jan 09 2006 Ray Strode <rstrode@fedoraproject.org> - 1:2.13.0.4-1
- update to 2.13.0.4

* Fri Dec 09 2005 Jesse Keating <jkeating@fedoraproject.org> - 1:2.8.0.4-17
- gcc update bump

* Wed Nov 16 2005 Ray Strode <rstrode@fedoraproject.org> - 1:2.8.0.4-16
- Don't fallback to xsm, try gnome-session instead - Require xorg-x11-xinit

* Mon Nov 14 2005 Ray Strode <rstrode@fedoraproject.org> - 1:2.8.0.4-15
- Make sure that dbus-launch gets called if available

* Mon Nov 14 2005 Ray Strode <rstrode@fedoraproject.org> - 1:2.8.0.4-14
- add /etc/X11/gdm/Xsession to file list

* Mon Nov 14 2005 Ray Strode <rstrode@fedoraproject.org> - 1:2.8.0.4-13
- Don't use X session / setup files anymore. - Don't install early login
  init scripts - remove xsri dependency - don't prune language lists
  anymore

* Mon Nov 14 2005 Jeremy Katz <katzj@fedoraproject.org> - 1:2.8.0.4-12
- also fix default xsession for where its moved in modular X

* Sun Nov 13 2005 Jeremy Katz <katzj@fedoraproject.org> - 1:2.8.0.4-11
- change requirements for modular X - patch to find x server with modular X

* Thu Oct 20 2005 Ray Strode <rstrode@fedoraproject.org> - 1:2.8.0.4-10
- redhat-artwork was busted, require new version

* Tue Oct 18 2005 Ray Strode <rstrode@fedoraproject.org> - 1:2.8.0.4-9
- zero-initialize message buffer, bug fixed by Josh Parson
  (jbparsons@usdavis.edu) (bug 160603) - fix typo in redhat-artwork
  requires line

* Mon Oct 17 2005 Steve Grubb <sgrubb@fedoraproject.org> - 1:2.8.0.4-8
- add login audit patch (bug 170569)

* Mon Oct 17 2005 Ray Strode <rstrode@fedoraproject.org> - 1:2.8.0.4-7
- bump redhat-artwork requirement to get rid of the boot throbber for now,
  since it seems to have reappeared mysteriously (bug 171025)

* Fri Oct 14 2005 Daniel J Walsh <dwalsh@fedoraproject.org> - 1:2.8.0.4-6
- Change to use getseuserbyname

* Wed Sep 28 2005 Daniel J Walsh <dwalsh@fedoraproject.org> - 1:2.8.0.4-5
- Fix selinux not to fail when in permissive mode

* Tue Sep 27 2005 Ray Strode <rstrode@fedoraproject.org> - 1:2.8.0.4-4
- remove flexiserver from menus

* Thu Sep 08 2005 Ray Strode <rstrode@fedoraproject.org> - 1:2.8.0.4-3
- gdmphotosetup.desktop moved

* Thu Sep 08 2005 Ray Strode <rstrode@fedoraproject.org> - 1:2.8.0.4-2
- actually update source tarball

* Thu Sep 08 2005 Ray Strode <rstrode@fedoraproject.org> - 1:2.8.0.4-1
- update to 2.8.0.4

* Tue Sep 06 2005 Ray Strode <rstrode@fedoraproject.org> - 1:2.8.0.2-4
- Apply clean up patch from Steve Grubb (gnome bug 315388).

* Tue Aug 30 2005 Ray Strode <rstrode@fedoraproject.org> - 1:2.8.0.2-3
- Prune language list of installed languages - Make config file noreplace
  again (bug 167087).

* Mon Aug 22 2005 Ray Strode <rstrode@fedoraproject.org> - 1:2.8.0.2-2
- hide throbber

* Fri Aug 19 2005 Ray Strode <rstrode@fedoraproject.org> - 1:2.8.0.2-1
- update to 2.8.0.2 - disable early login stuff temporarily

* Thu Aug 18 2005 Ray Strode <rstrode@fedoraproject.org> - 1:2.6.0.8-26
- add patch i forgot about to cvs - disable patch in spec file

* Thu Aug 18 2005 Ray Strode <rstrode@fedoraproject.org> - 1:2.6.0.8-25
- rebuild

* Mon May 23 2005 Ray Strode <rstrode@fedoraproject.org> - 1:2.6.0.8-24
- Make sure username/password incorrect message gets displayed (bug
  158127). - reread system locale before starting gdm in early login mode
  (bug 158376).

* Thu May 19 2005 Ray Strode <rstrode@fedoraproject.org> - 1:2.6.0.8-23
- Take out some syslog spew (bug 157711).

* Mon May 16 2005 Ray Strode <rstrode@fedoraproject.org> - 1:2.6.0.8-22
- workaround some cvs funkiness

* Mon May 16 2005 Ray Strode <rstrode@fedoraproject.org> - 1:2.6.0.8-21
- Fix processing of new-line characters that got broken in 2.6.0.8-11 (bug
  157442).

* Tue May 03 2005 Ray Strode <rstrode@fedoraproject.org> - 1:2.6.0.8-20
- rev release

* Tue May 03 2005 Ray Strode <rstrode@fedoraproject.org> - 1:2.6.0.8-19
- Fix processing of non-ascii characters that got broken in 2.6.0.8-11,
  found by Miloslav Trmac <mitr@redhat.com>, (bug 156590).

* Thu Apr 28 2005 Ray Strode <rstrode@fedoraproject.org> - 1:2.6.0.8-18
- Fix halt command (bug 156299) - Process all messages sent to the greeter
  in a read, not just the first

* Wed Apr 27 2005 Jeremy Katz <katzj@fedoraproject.org> - 1:2.6.0.8-17
- silence %%postun

* Tue Apr 26 2005 Ray Strode <rstrode@fedoraproject.org> - 1:2.6.0.8-16
- Change default standard greeter theme to clearlooks and default graphical
  greeter theme to Bluecurve specifically. - Change default path values
  (bug 154280)

* Mon Apr 25 2005 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.6.0.8-15
- Delay XDMCP initialization with early-login

* Mon Apr 25 2005 Ray Strode <rstrode@fedoraproject.org> - 1:2.6.0.8-14
- add patch

* Mon Apr 25 2005 Ray Strode <rstrode@fedoraproject.org> - 1:2.6.0.8-13
- rev release

* Mon Apr 25 2005 Ray Strode <rstrode@fedoraproject.org> - 1:2.6.0.8-12
- calling gdm_debug and g_strdup_printf from signal handlers are bad news
  (Spotted by Mark McLoughlin <markmc@redhat.com>).

* Wed Apr 20 2005 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.6.0.8-11
- Make it build

* Wed Apr 20 2005 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.6.0.8-10
- Boot throbber

* Mon Apr 18 2005 Ray Strode <rstrode@fedoraproject.org> - 1:2.6.0.8-9
- Don't install gnome.desktop to /usr/share/xsessions (bug 145791)

* Fri Apr 15 2005 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.6.0.8-8
- Bump revision

* Fri Apr 15 2005 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.6.0.8-7
- Work on early-login

* Thu Apr 14 2005 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.6.0.8-6
- Make early-login work with firstboot

* Thu Apr 14 2005 Ray Strode <rstrode@fedoraproject.org> - 1:2.6.0.8-5
- Fix invalid bug reference

* Wed Apr 13 2005 Ray Strode <rstrode@fedoraproject.org> - 1:2.6.0.8-4
- Don't hard code dpi setting to 96.0, but instead look at Xft.dpi

* Wed Apr 13 2005 Ray Strode <rstrode@fedoraproject.org> - 1:2.6.0.8-3
- touch /var/lock/subsys/gdm-early-login so gdm gets killed on runlevel
  changes (bug 113107) - don't try to use system dpi settings for canvas
  text (bug 127532) - merge resource database from displays other than :0

* Sat Apr 02 2005 Ray Strode <rstrode@fedoraproject.org> - 1:2.6.0.8-2
- update sources file for new source tarball

* Sat Apr 02 2005 Ray Strode <rstrode@fedoraproject.org> - 1:2.6.0.8-1
- update to 2.6.0.8 - add new init scripts to support early-login mode

* Tue Mar 29 2005 Ray Strode <rstrode@fedoraproject.org> - 1:2.6.0.7-11
- Update patch to hopefully build on x86_64

* Tue Mar 29 2005 Ray Strode <rstrode@fedoraproject.org> - 1:2.6.0.7-10
- Add a --wait-for-bootup cmdline option.

* Mon Mar 28 2005 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.6.0.7-9
- Add a --wait-for-system-started cmdline option

* Mon Mar 28 2005 Christopher Aillon <caillon@fedoraproject.org> - 1:2.6.0.7-8
- Fix if check in specfiles.

* Fri Mar 25 2005 Christopher Aillon <caillon@fedoraproject.org> - 1:2.6.0.7-7
- Update the GTK+ theme icon cache on (un)install

* Fri Mar 11 2005 aoliva <aoliva@fedoraproject.org> - 1:2.6.0.7-6
- fix patch for bug 149899 (fixes bug 150745)

* Wed Mar 09 2005 Than Ngo <than@fedoraproject.org> - 1:2.6.0.7-5
- OnlyShowIn=GNOME;

* Mon Feb 28 2005 Ray Strode <rstrode@fedoraproject.org> - 1:2.6.0.7-4
- seteuid/egid as user before testing for presence of user's home directory
  (fixes bug 149899)

* Thu Feb 10 2005 Ray Strode <rstrode@fedoraproject.org> - 1:2.6.0.7-3
- Turn off "switchdesk" mode by default which accidentally got turned on by
  default in 2.6.0.5-4

* Wed Feb 02 2005 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.6.0.7-2
- Upload new source

* Wed Feb 02 2005 Matthias Clasen <mclasen@fedoraproject.org> - 1:2.6.0.7-1
- Update to 2.6.0.7

* Tue Jan 25 2005 Ray Strode <rstrode@fedoraproject.org> - 1:2.6.0.5-12
- Fix date in changelog entry. I'm a year behind the times aparently.

* Tue Jan 25 2005 Ray Strode <rstrode@fedoraproject.org> - 1:2.6.0.5-11
- Fix bug in greeter sort-session-list patch where selecting a session did
  nothing (bug 145626)

* Thu Dec 09 2004 Daniel J Walsh <dwalsh@fedoraproject.org> - 1:2.6.0.5-10
- Remove pam_selinux from gdmsetup pam file

* Wed Dec 01 2004 Ray Strode <rstrode@fedoraproject.org> - 1:2.6.0.5-9
- Look up and use username instead of assuming that user entered login is
  cannonical. Patch from Mike Patnode <mike.patnode@centrify.com> (fixes
  bug 141380).

* Fri Nov 12 2004 Ray Strode <rstrode@fedoraproject.org> - 1:2.6.0.5-8
- Sort session list so that default session comes out on top (fixes bug
  107324)

* Thu Nov 11 2004 Ray Strode <rstrode@fedoraproject.org> - 1:2.6.0.5-7
- Make desktop file symlink instead of absolute (bug 104390) - Add
  flexiserver back to menus

* Wed Oct 20 2004 Ray Strode <rstrode@fedoraproject.org> - 1:2.6.0.5-6
- Clean up xses if the session was successfullly completed. (fixes bug
  #136382)

* Tue Oct 19 2004 Ray Strode <rstrode@fedoraproject.org> - 1:2.6.0.5-5
- Prefer nb_NO over no_NO for Norwegian (fixes bug #136033)

* Thu Oct 07 2004 Alexander Larsson <alexl@fedoraproject.org> - 1:2.6.0.5-4
- Change default greeter theme to "Default", require redhat-artwork with
  Default symlink.

* Wed Sep 29 2004 Ray Strode <rstrode@fedoraproject.org> - 1:2.6.0.5-3
- Check if there is a selected node before using iterator. (fixes bug
  #133329).

* Fri Sep 24 2004 Ray Strode <rstrode@fedoraproject.org> - 1:2.6.0.5-2
- Don't mess with gdmphotosetup categories. Upstream categories are fine.

* Mon Sep 20 2004 Ray Strode <rstrode@fedoraproject.org> - 1:2.6.0.5-1
- update to 2.6.0.5

* Thu Sep 09 2004 cvsdist <cvsdist@fedoraproject.org> - 1:2.6.0.3-5
- auto-import gdm-2.6.0.3-5 from gdm-2.6.0.3-5.src.rpm

* Thu Sep 09 2004 cvsdist <cvsdist@fedoraproject.org> - 1:2.6.0.3-4
- auto-import changelog data from gdm-2.6.0.3-4.src.rpm 2.6.0.3-4 - rebuilt

* Thu Sep 09 2004 cvsdist <cvsdist@fedoraproject.org> - 1:2.6.0.3-3
- auto-import changelog data from gdm-2.6.0.3-3.src.rpm 2.6.0.3-3 - rebuilt

* Thu Sep 09 2004 cvsdist <cvsdist@fedoraproject.org> - 1:2.6.0.3-2
- auto-import changelog data from gdm-2.6.0.3-2.src.rpm 2.6.0.3-2 - fix
  theme (#128599)

* Thu Sep 09 2004 cvsdist <cvsdist@fedoraproject.org> - 1:2.6.0.3-1
- auto-import changelog data from gdm-2.6.0.3-1.src.rpm 2.6.0.3-1 - update
  to 2.6.0.3 (fixes bug #117677)

* Thu Sep 09 2004 cvsdist <cvsdist@fedoraproject.org> - 1:2.6.0.0-4
- auto-import changelog data from gdm-2.6.0.0-6.src.rpm Tue Jun 15 2004
  Elliot Lee <sopwith@redhat.com> - rebuilt

* Thu Sep 09 2004 cvsdist <cvsdist@fedoraproject.org> - 1:2.6.0.0-3
- auto-import changelog data from gdm-2.6.0.0-5.src.rpm 2.6.0.0-5 - rebuild

* Thu Sep 09 2004 cvsdist <cvsdist@fedoraproject.org> - 1:2.6.0.0-2
- auto-import changelog data from gdm-2.6.0.0-4.src.rpm 2.6.0.0-4 - add
  patch to build gdm-binary with PIE

* Thu Sep 09 2004 cvsdist <cvsdist@fedoraproject.org> - 1:2.6.0.0-1
- auto-import changelog data from gdm-2.6.0.0-3.src.rpm 2.6.0.0-3 - Update
  the "use switchdesk" message to only be display when switchdesk-gui is
  installed and to not reference a non existant menu item (bug #121460)
  2.6.0.0-2 - Always put session errors in /tmp, in preparation for
  completely preventing gdm from writing to /home/ 2.6.0.0-1 - update to
  2.6.0.0

* Thu Sep 09 2004 cvsdist <cvsdist@fedoraproject.org> - 1:2.5.90.2-1
- auto-import changelog data from gdm-2.5.90.2-3.src.rpm 2.5.90.3-1 - Use
  selinux patch again 2.5.90.3-1 - Stop using selinux patch and use
  pam_selinux instead. 2.5.90.2-1 - update to 2.5.90.2 Tue Mar 02 2004
  Elliot Lee <sopwith@redhat.com> - rebuilt 2.5.90.1-1 - update to 2.5.90.1
  Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com> - rebuilt

* Thu Sep 09 2004 cvsdist <cvsdist@fedoraproject.org> - 1:2.4.4.5-3
- auto-import gdm-2.4.4.5-7 from gdm-2.4.4.5-7.src.rpm

* Thu Sep 09 2004 cvsdist <cvsdist@fedoraproject.org> - 1:2.4.4.5-2
- auto-import changelog data from gdm-2.4.4.5-1.2.src.rpm 2.4.4.5-1.2 -
  renamed for FC1 update 2.4.4.5-9 - add two lines to match upstream CVS to
  xdmcp_sessions.patch Fully resolves #110315 and #113154 2.4.4.5-8 -
  patch30 xdmcp_session counter fix from gdm-2.5.90.0 #110315 - automake14
  really needed, not automake - BR libcroco-devel, libcroco-devel, libattr-
  devel, gettext - conditionally BR libselinux-devel - explicit epoch in
  all deps - make the ja.po time format change with a sed expression rather
  than overwriting the whole file (Petersen #113995) 2.4.4.5-7 - fix build
  with current auto* 2.4.4.5-5 - try a simple rebuild for libcroco abi
  change 2.4.4.5-4 - Fix call to is_selinux_enabled 2.4.4.5-3 - Use
  /sbin/reboot and /sbin/poweroff instead of consolehelper version
  2.4.4.5-2.sel - turn on SELinux 2.4.4.5-1 - get rid of the teal

* Thu Sep 09 2004 cvsdist <cvsdist@fedoraproject.org> - 1:2.4.4.5-1
- auto-import changelog data from gdm-2.4.4.5-1.src.rpm 2.4.4.5-1 - new
  version 2.4.4.3-6.sel - new patch from George to fix #106189 - change bg
  color in rhdefaults patch - turn off SELinux 2.4.4.3-6.sel - turn on
  SELinux 2.4.4.3-5 - Fix greeter line-breaking crash (rest of #106189)
  2.4.4.3-4 - Set the BaseXSession properly in the config. - This fixes
  parts of bug #106189 2.4.4.3-3 - change DefaultSession=Default.desktop to
  DefaultSession=default.desktop - SELinux off again 2.4.4.3-2.sel - turn
  on SELinux 2.4.4.3-1 - 2.4.4.3 - --without-selinux for now, since
  libselinux not in the buildroot 2.4.4.0-4 - turn off SELinux
  2.4.4.0-3.sel - turn on SELinux 2.4.4.0-2 - Use the right default session
  (#103546) 2.4.4.0-1 - update to 2.4.4.0 - update to georges new selinux
  patch 2.4.2.102-2 - Remove scrollkeeper files 2.4.2.102-1 - updated to
  2.4.2.102 - removed outdated patches - Use Xsetup_0 only for :0 since
  that's the way it works for xdm - remove the gnome.desktop file, its
  going into gnome-session 2.4.1.6-1 - update to latest bugfix version on
  george's advice - remove setlocale patch that's upstream - remove console
  setup patches that are upstream

* Thu Sep 09 2004 cvsdist <cvsdist@fedoraproject.org> - 1:2.4.1.3-2
- auto-import gdm-2.4.1.3-5.1 from gdm-2.4.1.3-5.1.src.rpm

* Thu Sep 09 2004 cvsdist <cvsdist@fedoraproject.org> - 1:2.4.1.3-1
- auto-import gdm-2.4.1.3-5 from gdm-2.4.1.3-5.src.rpm

* Thu Sep 09 2004 cvsdist <cvsdist@fedoraproject.org> - 1:2.4.0.7-12
- auto-import gdm-2.4.0.7-14 from gdm-2.4.0.7-14.src.rpm

* Thu Sep 09 2004 cvsdist <cvsdist@fedoraproject.org> - 1:2.4.0.7-11
- auto-import gdm-2.4.0.7-13 from gdm-2.4.0.7-13.src.rpm

* Thu Sep 09 2004 cvsdist <cvsdist@fedoraproject.org> - 1:2.4.0.7-10
- auto-import gdm-2.4.0.7-12 from gdm-2.4.0.7-12.src.rpm

* Thu Sep 09 2004 cvsdist <cvsdist@fedoraproject.org> - 1:2.4.0.7-9
- auto-import gdm-2.4.0.7-11 from gdm-2.4.0.7-11.src.rpm

* Thu Sep 09 2004 cvsdist <cvsdist@fedoraproject.org> - 1:2.4.0.7-8
- auto-import gdm-2.4.0.7-10 from gdm-2.4.0.7-10.src.rpm

* Thu Sep 09 2004 cvsdist <cvsdist@fedoraproject.org> - 1:2.4.0.7-7
- auto-import gdm-2.4.0.7-9 from gdm-2.4.0.7-9.src.rpm

* Thu Sep 09 2004 cvsdist <cvsdist@fedoraproject.org> - 1:2.4.0.7-6
- auto-import gdm-2.4.0.7-8 from gdm-2.4.0.7-8.src.rpm

* Thu Sep 09 2004 cvsdist <cvsdist@fedoraproject.org> - 1:2.4.0.7-5
- auto-import gdm-2.4.0.7-7 from gdm-2.4.0.7-7.src.rpm

* Thu Sep 09 2004 cvsdist <cvsdist@fedoraproject.org> - 1:2.4.0.7-4
- auto-import gdm-2.4.0.7-6 from gdm-2.4.0.7-6.src.rpm

* Thu Sep 09 2004 cvsdist <cvsdist@fedoraproject.org> - 1:2.4.0.7-3
- auto-import gdm-2.4.0.7-5 from gdm-2.4.0.7-5.src.rpm

* Thu Sep 09 2004 cvsdist <cvsdist@fedoraproject.org> - 1:2.4.0.7-2
- auto-import gdm-2.4.0.7-4 from gdm-2.4.0.7-4.src.rpm

* Thu Sep 09 2004 cvsdist <cvsdist@fedoraproject.org> - 1:2.4.0.7-1
- auto-import gdm-2.4.0.7-3 from gdm-2.4.0.7-3.src.rpm

* Thu Sep 09 2004 cvsdist <cvsdist@fedoraproject.org> - 1:2.4.0.0-1
- auto-import gdm-2.4.0.0-1 from gdm-2.4.0.0-1.src.rpm

* Thu Sep 09 2004 cvsdist <cvsdist@fedoraproject.org> - 1:2.2.3.1-12
- auto-import gdm-2.2.3.1-23 from gdm-2.2.3.1-23.src.rpm

* Thu Sep 09 2004 cvsdist <cvsdist@fedoraproject.org> - 1:2.2.3.1-11
- auto-import gdm-2.2.3.1-22 from gdm-2.2.3.1-22.src.rpm

* Thu Sep 09 2004 cvsdist <cvsdist@fedoraproject.org> - 1:2.2.3.1-10
- auto-import gdm-2.2.3.1-21 from gdm-2.2.3.1-21.src.rpm

* Thu Sep 09 2004 cvsdist <cvsdist@fedoraproject.org> - 1:2.2.3.1-9
- auto-import gdm-2.2.3.1-20 from gdm-2.2.3.1-20.src.rpm

* Thu Sep 09 2004 cvsdist <cvsdist@fedoraproject.org> - 1:2.2.3.1-8
- auto-import gdm-2.2.3.1-18 from gdm-2.2.3.1-18.src.rpm

* Thu Sep 09 2004 cvsdist <cvsdist@fedoraproject.org> - 1:2.2.3.1-7
- auto-import gdm-2.2.3.1-17 from gdm-2.2.3.1-17.src.rpm

* Thu Sep 09 2004 cvsdist <cvsdist@fedoraproject.org> - 1:2.2.3.1-6
- auto-import gdm-2.2.3.1-16 from gdm-2.2.3.1-16.src.rpm

* Thu Sep 09 2004 cvsdist <cvsdist@fedoraproject.org>
- auto-import changelog data from gdm-2.0beta2-46.src.rpm Wed Aug 13 2003
  Havoc Pennington <hp@redhat.com> - fix a security issue CAN-2003-0547
  bugzilla #102275

* Thu Sep 09 2004 cvsdist <cvsdist@fedoraproject.org>
- auto-import changelog data from gdm-2.0beta2-45.src.rpm Fri Mar 23 2001
  Nalin Dahyabhai <nalin@redhat.com> - reinitialize pam credentials after
  calling initgroups() -- the credentials may be group memberships Tue Mar
  20 2001 Owen Taylor <otaylor@redhat.com> - Fix colors patch Fri Mar 16
  2001 Havoc Pennington <hp@redhat.com> - translations Tue Mar 06 2001
  Preston Brown <pbrown@redhat.com> - don't screw up color map on 8 bit
  displays Sat Feb 24 2001 Trond Eivind Glomsr�d <teg@redhat.com> - langify
  - Don't define and use "ver" and "nam" at the top of the spec file - use
  %%{_tmppath} Wed Feb 14 2001 Tim Powers <timp@redhat.com> - don't allow
  gdm to show some system accounts in the browser bugzilla Sat Jan 20 2001
  Akira TAGOH <tagoh@redhat.com> - Updated Japanese translation.

* Thu Sep 09 2004 cvsdist <cvsdist@fedoraproject.org>
- auto-import changelog data from gdm-2.0beta2-37tc1.src.rpm Sun Jan 07
  2001 Jason Wilson <jwilson@redhat.com> - added Traditional Chinese
  translations - added Chinese and Korean to locale list

* Thu Sep 09 2004 cvsdist <cvsdist@fedoraproject.org>
- auto-import changelog data from gdm-2.0beta2-37j1.src.rpm Tue Sep 12 2000
  Matt Wilson <msw@redhat.com> - updated Japanese translation from Nakai-
  san

* Thu Sep 09 2004 cvsdist <cvsdist@fedoraproject.org>
- auto-import changelog data from gdm-2.0beta2-37.src.rpm Sun Aug 13 2000
  Owen Taylor <otaylor@redhat.com> - Return to toplevel main loop and start
  Xdcmp if enabled (Bug #16106) Fri Aug 11 2000 Jonathan Blandford
  <jrb@redhat.com> - Up Epoch and release Wed Aug 02 2000 Havoc Pennington
  <hp@redhat.com> - Requires Xsession script Wed Jul 19 2000 Owen Taylor
  <otaylor@redhat.com> - Italian is better as it_IT than it_CH (bugzilla
  12425) Mon Jul 17 2000 Jonathan Blandford <jrb@redhat.com> - Don't
  instally gdmconfig as it doesn't work. Fri Jul 14 2000 Havoc Pennington
  <hp@redhat.com> - Rearrange code to avoid calling innumerable system
  calls in a signal handler Fri Jul 14 2000 Havoc Pennington
  <hp@redhat.com> - Verbose debug spew for infinite loop stuff Fri Jul 14
  2000 Havoc Pennington <hp@redhat.com> - Try to fix infinite loops on X
  server failure Thu Jul 13 2000 Prospector <bugzilla@redhat.com> -
  automatic rebuild Thu Jun 29 2000 Havoc Pennington <hp@redhat.com> -
  Remove Docdir Mon Jun 19 2000 Havoc Pennington <hp@redhat.com> - Fix file
  descriptor leak (Bugzilla 12301) Mon Jun 19 2000 Havoc Pennington
  <hp@redhat.com> - Apply security errata patch we released for 6.2 - Add
  Gnome.session back, don't know when it disappeared or why Thu Jun 01 2000
  Nalin Dahyabhai <nalin@redhat.com> - modify PAM setup to use system-auth
  Fri May 19 2000 Havoc Pennington <hp@redhat.com> - rebuild for the
  Winston tree Fri Feb 04 2000 Havoc Pennington <hp@redhat.com> - Modify
  Default.session and Failsafe.session not to add -login option to bash -
  exec the session scripts with the user's shell with a hyphen prepended -
  doesn't seem to actually work yet with tcsh, but it doesn't seem to break
  anything. needs a look to see why it doesn't work Fri Feb 04 2000 Havoc
  Pennington <hp@redhat.com> - Link PreSession/Default to xdm/GiveConsole -
  Link PostSession/Default to xdm/TakeConsole Fri Feb 04 2000 Havoc
  Pennington <hp@redhat.com> - Fix the fix to the fix (8877) - remove
  docs/gdm-manual.txt which doesn't seem to exist from %%doc Fri Feb 04
  2000 Havoc Pennington <hp@redhat.com> - Enhance 8877 fix by not deleting
  the "Please login" message Fri Feb 04 2000 Havoc Pennington
  <hp@redhat.com> - Try to fix bug 8877 by clearing the message below the
  entry box when the prompt changes. may turn out to be a bad idea. Mon Jan
  17 2000 Elliot Lee <sopwith@redhat.com> - Fix bug #7666: exec Xsession
  instead of just running it Mon Oct 25 1999 Jakub Jelinek
  <jakub@redhat.com> - Work around so that russian works (uses koi8-r
  instead of the default iso8859-5) Tue Oct 12 1999 Owen Taylor
  <otaylor@redhat.com> - Try again Tue Oct 12 1999 Owen Taylor
  <otaylor@redhat.com> - More fixes for i18n Tue Oct 12 1999 Owen Taylor
  <otaylor@redhat.com> - Fixes for i18n Sun Sep 26 1999 Elliot Lee
  <sopwith@redhat.com> - Fixed pipewrite bug (found by mkj & ewt). Fri Sep
  17 1999 Michael Fulbright <drmike@redhat.com> - added requires for pam >=
  0.68 Fri Sep 10 1999 Elliot Lee <sopwith@redhat.com> - I just update this
  package every five minutes, so any recent changes are my fault. Thu Sep
  02 1999 Michael K. Johnson <johnsonm@redhat.com> - built gdm-2.0beta2 Mon
  Aug 30 1999 Michael K. Johnson <johnsonm@redhat.com> - built gdm-2.0beta1
  Tue Aug 17 1999 Michael Fulbright <drmike@redhat.com> - included
  rmeier@liberate.com patch for tcp socket X connections Mon Apr 19 1999
  Michael Fulbright <drmike@redhat.com> - fix to handling ancient gdm
  config files with non-standard language specs - dont close display
  connection for xdmcp connections, else we die if remote end dies. Fri Apr
  16 1999 Michael Fulbright <drmike@redhat.com> - fix language handling to
  set GDM_LANG variable so gnome-session can pick it up Wed Apr 14 1999
  Michael Fulbright <drmike@redhat.com> - fix so certain dialog boxes dont
  overwrite background images Wed Apr 14 1999 Michael K. Johnson
  <johnsonm@redhat.com> - do not specify -r 42 to useradd -- it doesn't
  know how to fall back if id 42 is already taken Fri Apr 09 1999 Michael
  Fulbright <drmike@redhat.com> - removed suspend feature Mon Apr 05 1999
  Jonathan Blandford <jrb@redhat.com> - added patch from otaylor to not
  call gtk funcs from a signal. - added patch to tab when username not
  added. - added patch to center About box (and bring up only one) and
  ignore "~" and ".rpm" files. Fri Mar 26 1999 Michael Fulbright
  <drmike@redhat.com> - fixed handling of default session, merged all
  gdmgreeter patches into one Tue Mar 23 1999 Michael Fulbright
  <drmike@redhat.com> - remove GNOME/KDE/AnotherLevel session scripts,
  these have been moved to the appropriate packages instead. - added patch
  to make option menus always active (security problem otherwise) - added
  jrb's patch to disable stars in passwd entry field Fri Mar 19 1999
  Michael Fulbright <drmike@redhat.com> - made sure /usr/bin isnt in
  default path twice - strip binaries Wed Mar 17 1999 Michael Fulbright
  <drmike@redhat.com> - fixed to use proper system path when root logs in
  Tue Mar 16 1999 Michael Fulbright <drmike@redhat.com> - linked
  Init/Default to Red Hat default init script for xdm - removed logo from
  login dialog box Mon Mar 15 1999 Michael Johnson <johnsonm@redhat.com> -
  pam_console integration Tue Mar 09 1999 Michael Fulbright
  <drmike@redhat.com> - added session files for
  GNOME/KDE/AnotherLevel/Default/Failsafe - patched gdmgreeter to not
  complete usernames - patched gdmgreeter to not safe selected session
  permanently - patched gdmgreeter to center dialog boxes Mon Mar 08 1999
  Michael Fulbright <drmike@redhat.com> - removed comments from gdm.conf
  file, these are not parsed correctly Sun Mar 07 1999 Michael Fulbright
  <drmike@redhat.com> - updated source line for accuracy Fri Feb 26 1999
  Owen Taylor <otaylor@redhat.com> - Updated patches for 1.0.0 - Fixed some
  problems in 1.0.0 with installation directories - moved /usr/var/gdm
  /var/gdm Thu Feb 25 1999 Michael Fulbright <drmike@redhat.com> - moved
  files from /usr/etc to /etc Tue Feb 16 1999 Michael Johnson
  <johnsonm@redhat.com> - removed commented-out #1 definition -- put back
  after testing gnome-libs comment patch Sat Feb 06 1999 Michael Johnson
  <johnsonm@redhat.com> - initial packaging
