%global dnf_org org.baseurl.Dnf
%global dnf_version 4.2.6

Name:           dnfdaemon
Version:        0.3.22
Release:        0.1.git20221008%{?dist}
Summary:        DBus daemon for dnf package actions

License:        GPLv2+
URL:            https://github.com/manatools/dnfdaemon
Source0:        %{url}/releases/download/%{name}-%{version}/%{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  make

# Ensure systemd macros are available
%if 0%{?mageia}
BuildRequires:  systemd-devel
%else
BuildRequires:  systemd
%endif

# Ensure that correct pygobject module is available
%if 0%{?mageia}
Requires:       python3-gobject3
%else
Requires:       python3-gobject
%endif
Requires:       python3-dbus
Requires:       python3-dnf >= %{dnf_version}

Requires:       polkit

Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description
Dbus daemon for performing package actions with the dnf package manager


%package selinux
Summary:        SELinux integration for dnfdaemon

Requires:       %{name} = %{version}-%{release}

%if 0%{?fedora} >= 23 || 0%{?mageia} >= 6
Requires(post):     policycoreutils-python-utils
Requires(postun):   policycoreutils-python-utils
%else
Requires(post):     policycoreutils-python
Requires(postun):   policycoreutils-python
%endif

# Use boolean weak reverse dependencies
# http://rpm.org/user_doc/dependencies.html#weak-dependencies
# http://rpm.org/user_doc/boolean_dependencies.html
Supplements:    (dnfdaemon and selinux-policy)

%description selinux
Metapackage customizing the SELinux policy to ensure dnfdaemon works with
SELinux enabled in enforcing mode.


%package -n python3-%{name}
Summary:        Python 3 API for communicating with %{name}

BuildRequires:  python3-devel
Requires:       %{name} = %{version}-%{release}
%if 0%{?mageia}
Requires:       python3-gobject3
%else
Requires:       python3-gobject
%endif
%{?python_provide:%python_provide python3-%{name}}

%description -n python3-%{name}
Python 3 API for communicating with %{name}.


%prep
%autosetup

%build
# Nothing to build

%install
make install DESTDIR=%{buildroot} DATADIR=%{_datadir} SYSCONFDIR=%{_sysconfdir}


%files
%doc README.md ChangeLog
%license COPYING
%{_datadir}/dbus-1/system-services/%{dnf_org}*
%{_datadir}/dbus-1/services/%{dnf_org}*
%{_datadir}/%{name}/
%{_unitdir}/%{name}.service
%{_datadir}/polkit-1/actions/%{dnf_org}*
# this should not be edited by the user, so no %%config
%{_sysconfdir}/dbus-1/system.d/%{dnf_org}*
%dir %{python3_sitelib}/%{name}
%{python3_sitelib}/%{name}/__*
%{python3_sitelib}/%{name}/server

%files selinux
# empty metapackage

%files -n  python3-%{name}
%{python3_sitelib}/%{name}/client


%post
%systemd_post %{name}.service

%postun
%systemd_postun %{name}.service

%preun
%systemd_preun %{name}.service

%post selinux
# apply the right selinux file context
# http://fedoraproject.org/wiki/PackagingDrafts/SELinux#File_contexts
semanage fcontext -a -t rpm_exec_t '%{_datadir}/%{name}/%{name}-system' 2>/dev/null || :
restorecon -R %{_datadir}/%{name}/%{name}-system || :

%postun selinux
if [ $1 -eq 0 ] ; then  # final removal
semanage fcontext -d -t rpm_exec_t '%{_datadir}/%{name}/%{name}-system' 2>/dev/null || :
fi


%changelog
* Sat Apr 04 2020 Neal Gompa <ngompa13@gmail.com> 0.3.20-1
- Drop Python 2 support
- Handle removal of dnf.repo._md_expire_cache() in DNF 3.4
- Handle additional DNF transaction callback actions in DNF 3
- check_lock: treat 'locked by other' differently to 'not locked'
- Imported code from "dnf clean metadata" command
- Fix GetRepo crash for Attribute error
- Fix size of number of downloaded bytes to handle huge transactions
- Raise minimum version to DNF 4.2.6

* Sat Jun 23 2018 Daniel Mach <dmach@redhat.com> 0.3.19-1
- Require dnf-3.0.0 due to history and transaction changes.

* Wed May 24 2017 Neal Gompa <ngompa13@gmail.com> 0.3.18-1
- Require dnf-2.5.0 due to API change (rhbz#1454854)
- Remove "filename" updateinfo attribute usage due being
  removed in libdnf (rhbz#1444830)

* Fri Apr 14 2017 Neal Gompa <ngompa13@gmail.com> 0.3.17-1
- Require dnf-2.2.0 due to usage and expectation of new APIs
- Change to have SELinux subpackage weak installed
  based on solution by Kevin Kofler (rhbz#1395531)
- Rework spec file to support Fedora and Mageia

* Wed May 25 2016 Tim Lauridsen <timlau@fedoraproject.org> 0.3.16-1
- bumped release

* Tue May 10 2016 Tim Lauridsen <timlau@fedoraproject.org> 0.3.15-1
- bumped release

* Fri Apr 29 2016 Tim Lauridsen <timlau@fedoraproject.org> 0.3.14-1
- bumped release

* Fri Apr 29 2016 Tim Lauridsen <timlau@fedoraproject.org> 0.3.13-1
- bumped release

* Tue Dec 01 2015 Tim Lauridsen <timlau@fedoraproject.org> 0.3.12-2
- require dnf-1.1.0

* Sat Nov 28 2015 Tim Lauridsen <timlau@fedoraproject.org> 0.3.12-1
- added systemd service

* Wed Nov 18 2015 Tim Lauridsen <timlau@fedoraproject.org> 0.3.11-1
- bumped release

* Wed Sep 30 2015 Tim Lauridsen <timlau@fedoraproject.org> 0.3.10-2
- updated req. policycoreutils-python to policycoreutils-python-utils

* Wed Sep 30 2015 Tim Lauridsen <timlau@fedoraproject.org> 0.3.10-1
- bumped release

* Wed May 27 2015 Tim Lauridsen <timlau@fedoraproject.org> 0.3.9-1
- bumped release

* Wed May 06 2015 Tim Lauridsen <timlau@fedoraproject.org> 0.3.8-1
- bumped release

* Sun Apr 26 2015 Tim Lauridsen <timlau@fedoraproject.org> 0.3.7-1
- bumped release

* Wed Apr 15 2015 Tim Lauridsen <timlau@fedoraproject.org> 0.3.6-1
- bumped release

* Wed Apr 15 2015 Tim Lauridsen <timlau@fedoraproject.org> 0.3.5-1
- bumped release

* Sun Apr 12 2015 Tim Lauridsen <timlau@fedoraproject.org> 0.3.4-1
- bumped release
- require dnf-0.6.3

* Fri Oct 17 2014 Tim Lauridsen <timlau@fedoraproject.org> 0.3.3-1
- bumped release

* Wed Oct 15 2014 Tim Lauridsen <timlau@fedoraproject.org> 0.3.2-3
- removed require python3-dnfdaemon from main package

* Wed Oct 15 2014 Tim Lauridsen <timlau@fedoraproject.org> 0.3.2-2
- include python3-dnfdaemon in the dnfdaemon main package
- renamed python?-dnfdaemon-client to python?-dnfdaemon
- include dir ownerships in the right packages

* Sun Oct 12 2014 Tim Lauridsen <timlau@fedoraproject.org> 0.3.2-1
- bumped release
- fedora review cleanups
- python-dnfdaemon-client should own %%{python_sitelib}/dnfdaemon/client
- group %%files sections
- use uploaded sources on github, not autogenerated ones.

* Sun Sep 21 2014 Tim Lauridsen <timlau@fedoraproject.org> 0.3.1-1
- updated ChangeLog (timlau@fedoraproject.org)

* Sun Sep 21 2014 Tim Lauridsen <timlau@fedoraproject.org> 0.3.0-1
- bumped release

* Mon Sep 01 2014 Tim Lauridsen <timlau@fedoraproject.org> 0.2.5-1
- updated ChangeLog (timlau@fedoraproject.org)
- Hack for GObjects dont blow up (timlau@fedoraproject.org)

* Mon Sep 01 2014 Tim Lauridsen <timlau@fedoraproject.org> 0.2.4-1
- updated ChangeLog (timlau@fedoraproject.org)
- Use GLib mainloop, instead of Gtk, there is crashing in F21
  (timlau@fedoraproject.org)
- use the same cache setup as dnf cli (timlau@fedoraproject.org)
- fix cachedir setup caused by upstream changes (timlau@fedoraproject.org)
- fix: show only latest updates (fixes : timlau/yumex-dnf#2)
  (timlau@fedoraproject.org)
- fix: only get latest upgrades (timlau@fedoraproject.org)

* Sun Jul 13 2014 Tim Lauridsen <timlau@fedoraproject.org> 0.2.3-1
- fix cachedir setup for dnf 0.5.3 bump dnf dnf requirement
  (timlau@fedoraproject.org)

* Thu May 29 2014 Tim Lauridsen <timlau@fedoraproject.org> 0.2.2-1
- build: require dnf 0.5.2 (timlau@fedoraproject.org)
- fix refactor issue (timlau@fedoraproject.org)
- api: merged GetPackages with GetPackageWithAttributes.
  (timlau@fedoraproject.org)
