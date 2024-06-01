%global dnf_org org.baseurl.Dnf
%global dnf_version 4.2.6

Name:           dnfdaemon
Version:        0.3.22
Release:        1%{?dist}
Summary:        DBus daemon for dnf package actions

License:        GPLv2+
URL:            https://github.com/manatools/%{name}
Source0:        %{url}/releases/download/%{name}-%{version}/%{name}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  systemd

Requires:       python3-gobject
Requires:       python3-dbus
Requires:       python3-dnf >= %{dnf_version}
Requires:       polkit

%{?systemd_requires}

%description
Dbus daemon for performing package actions with the dnf package manager


%package selinux
Summary:        SELinux integration for the dnf-daemon

Requires:       %{name} = %{version}-%{release}

Requires(post):   policycoreutils-python-utils
Requires(postun): policycoreutils-python-utils

# http://rpm.org/user_doc/boolean_dependencies.html#cautionary-tale-about-if
Supplements:    (dnfdaemon and selinux-policy)

%description selinux
Metapackage customizing the SELinux policy to make the dnf-daemon work with
SELinux enabled in enforcing mode.


%package -n python3-%{name}
Summary:        Python 3 api for communicating with the dnf-daemon DBus service

BuildRequires:  python3-devel
BuildRequires: make

Requires:       %{name} = %{version}-%{release}
Requires:       python3-gobject

%{?python_provide:%python_provide python3-%{name}}

%description -n python3-%{name}
Python 3 api for communicating with the dnf-daemon DBus service


%prep
%autosetup -p1


%build
# Nothing to build


%install
%make_install DATADIR=%{_datadir} SYSCONFDIR=%{_datadir}


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


%files
%license COPYING
%doc README.md ChangeLog
%{_datadir}/dbus-1/system-services/%{dnf_org}*
%{_datadir}/dbus-1/services/%{dnf_org}*
%{_datadir}/%{name}/
%{_unitdir}/%{name}.service
%{_datadir}/polkit-1/actions/%{dnf_org}*
%{_datadir}/dbus-1/system.d/%{dnf_org}*
%dir %{python3_sitelib}/%{name}
%{python3_sitelib}/%{name}/__*
%{python3_sitelib}/%{name}/server


%files selinux
# empty metapackage


%files -n  python3-%{name}
%{python3_sitelib}/%{name}/client


%changelog
* Thu Feb 01 2024 Jonathan Wright <jonathan@almalinux.org> - 0.3.22-1
- Update to 0.3.22 rhbz#2132423

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.20-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.20-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.20-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 0.3.20-12
- Rebuilt for Python 3.12

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.20-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.20-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 0.3.20-9
- Rebuilt for Python 3.11

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.20-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.20-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jun 10 2021 Carl George <carl@george.computer> - 0.3.20-6
- Add patch to fix Python 3.10 build

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.3.20-5
- Rebuilt for Python 3.10

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.20-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.20-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.3.20-2
- Rebuilt for Python 3.9

* Sat Apr 04 2020 Neal Gompa <ngompa13@gmail.com> - 0.3.20-1
- New version 0.3.20 (#1820953)

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.19-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.3.19-9
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.3.19-8
- Rebuilt for Python 3.8

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.19-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.19-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 14 2019 Miro Hrončok <mhroncok@redhat.com> - 0.3.19-5
- Subpackage python2-dnfdaemon has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Mon Sep 17 2018 Adam Williamson <awilliam@redhat.com> - 0.3.19-4
- Backport fixes for DNF 3 crashers (rhbz#1629378) (rhbz#1624652)

* Sun Jul 22 2018 Neal Gompa <ngompa13@gmail.com> - 0.3.19-3
- Backport patch from upstream to fix build for F29+ (rhbz#1603807)

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 27 2018 Neal Gompa <ngompa13@gmail.com> - 0.3.19-1
- New version 0.3.19
- Bump requires DNF >= 3.0.0

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.3.18-8
- Rebuilt for Python 3.7

* Tue Feb 20 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.3.18-7
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.18-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Dec 29 2017 Björn Esser <besser82@fedoraproject.org> - 0.3.18-5
- Add upstream patch for undo operation

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.18-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 14 2017 Björn Esser <besser82@fedoraproject.org> - 0.3.18-3
- Bump Requires DNF >= 2.5.1
- Remove patch to revert API-break in DNF

* Thu May 25 2017 Björn Esser <besser82@fedoraproject.org> - 0.3.18-2
- Revert API-break in DNF

* Wed May 24 2017 Björn Esser <besser82@fedoraproject.org> - 0.3.18-1
- New upstream release

* Wed May 24 2017 Björn Esser <besser82@fedoraproject.org> - 0.3.17-3
- Add patch, fixing new keyword for progress.start (rhbz#1454854)
- Requires dnf >= 2.5.0

* Mon May 01 2017 Björn Esser <besser82@fedoraproject.org> - 0.3.17-2
- Add patch, fixing deprecated API in hawkey (rhbz#1444830)

* Sat Apr 15 2017 Björn Esser <besser82@fedoraproject.org> - 0.3.17-1
- New upstream release

* Thu Mar 30 2017 Björn Esser <besser82@fedoraproject.org> - 0.3.16-11
- Add -selinux subpackage and drag it in through boolean Supplements
  Thanks to Kevin Kofler (rhbz#1395531)

* Thu Mar 30 2017 Björn Esser <besser82@fedoraproject.org> - 0.3.16-10
- Updated spec-file to latest guidelines
- Removed obsolete bits
- Moved dbus-config to non-user config-dir
- Require dnf >= 2.2.0

* Thu Mar 30 2017 Björn Esser <besser82@fedoraproject.org> - 0.3.16-9
- Updated Patch fixing new dbus-signal with dnf >= 2.2.0

* Thu Mar 23 2017 Björn Esser <besser82@fedoraproject.org> - 0.3.16-8
- Update URL to reflect new upstream
- Merge all patches
- More support for dnf >= 2.0.0

* Mon Feb 20 2017 Björn Esser <besser82@fedoraproject.org> - 0.3.16-7
- Add Patch3 for more support for dnf >= 2.0.0

* Tue Feb 07 2017 Björn Esser <besser82@fedoraproject.org> - 0.3.16-6
- Add Patch2 for more support for dnf >= 2.0.0

* Fri Feb 03 2017 Björn Esser <besser82@fedoraproject.org> - 0.3.16-5
- Rebuilt with hard requirement for dnf >= 2.0.0

* Fri Feb 03 2017 Björn Esser <besser82@fedoraproject.org> - 0.3.16-4
- Add Patch1 for supporting dnf-2.0

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.3.16-3
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.16-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

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
