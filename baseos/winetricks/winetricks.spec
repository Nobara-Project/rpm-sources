# Uncomment these, set snapshot to 0.
%global snapshot 1
%global commit0  a06ea8795482d2f49a5461ab5f23e0036e38d12b

Name:           winetricks
Version:        20241017
Release:        1%{?dist}

Summary:        Work around common problems in Wine

License:        LGPLv2+
URL:            https://github.com/Winetricks/%{name}
%if 0%{?snapshot}
Source0:        %{url}/archive/%{commit0}.tar.gz#/%{name}-%{commit0}.tar.gz
%else
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz
%endif

BuildArch:      noarch

# need arch-specific wine, not available everywhere:
# - adopted from wine.spec
ExclusiveArch:  %{ix86} x86_64 %{arm} aarch64
# - explicitly not ppc64* to hopefully not confuse koschei
ExcludeArch:    ppc64 ppc64le

BuildRequires:  make
BuildRequires:  desktop-file-utils

Requires:       winehq-staging
Requires:       cabextract gzip unzip wget which
Requires:       hicolor-icon-theme
Requires:       (kdialog if kdialog else zenity)

%description
Winetricks is an easy way to work around common problems in Wine.

It has a menu of supported games/apps for which it can do all the
workarounds automatically. It also lets you install missing DLLs
or tweak various Wine settings individually.


%prep
%if 0%{?snapshot}
%setup -qn%{name}-%{commit0}
%else
%setup -q
%endif

sed -i -e s:steam:: -e s:flash:: tests/*

%build
# not needed

%install
%make_install
# some tarballs do not install appdata
install -m0644 -D -t %{buildroot}%{_datadir}/metainfo src/%{name}.appdata.xml

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop


%files
%license COPYING debian/copyright
%doc README.md
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/bash-completion/completions/%{name}
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg
%{_datadir}/metainfo/%{name}.appdata.xml


%changelog
* Wed May 18 2022 Frantisek Zatloukal <fzatlouk@redhat.com> - 20220411-1
- Update to 20220411

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 20210825-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Sep 20 2021 Frantisek Zatloukal <fzatlouk@redhat.com> - 20210825-1
- Update to 20210825

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 20210206-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Feb 08 2021 Frantisek Zatloukal <fzatlouk@redhat.com> - 20210206-1
- Update to 20210206
- Drop BR on wine-common

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 20201206-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Nov 04 2020 Frantisek Zatloukal <fzatlouk@redhat.com> - 20201206-1
- Update to 20201206

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 20200412-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat Jun 20 2020 - Ernestas Kulik <ekulik@redhat.com> - 20200412-1
- Update to 20200412

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 20191224-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Jan 13 2020 - Ernestas Kulik <ekulik@redhat.com> - 20191224-1
- Update to 20191224

* Fri Sep 13 2019 - Ernestas Kulik <ekulik@redhat.com> - 20190912-1
- Update to 20190912

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 20190615-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jul 03 2019 - Ernestas Kulik <ekulik@redhat.com> - 20190615-1
- Update to 20190615

* Tue Mar 12 2019 Ernestas Kulik <ekulik@redhat.com> - 20190310-1
- Update to 20190310

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 20181203-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Jan 20 2019 Ernestas Kulik <ekulik@redhat.com> - 20181203-2
- Drop old path appdata exclude
- Add bash completions

* Sun Jan 20 2019 Ernestas Kulik <ekulik@redhat.com> - 20181203-1
- Update to 20181203

* Sun Jan 20 2019 Ernestas Kulik <ekulik@redhat.com> - 20180603-4
- Add dependency on zenity or kdialog for GUI

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 20180603-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jul 01 2018 Raphael Groner <projects.rg@smart.ms> - 20180603-2
- avoid shebang warning of rpmlint for appdata

* Sat Jun 23 2018 Raphael Groner <projects.rg@smart.ms> - 20180603-1
- new version

* Mon Mar 05 2018 Raphael Groner <projects.rg@smart.ms> - 20180217-1
- new version
- drop obsolete scriptlets
- move appdata into mimeinfo

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 20171222-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Jan 22 2018 Ben Rosser <rosser.bjr@gmail.com> - 20171222-1
- Updated to latest upstream release. (#1528622)
- Moved appdata file to new appdata location, /usr/share/metainfo.
- Removed dependency on 'time' package as per #1533795.

* Sun Dec 03 2017 Raphael Groner <projects.rg@smart.ms> - 20171018-1
- new version
- ensure appdata gets installed

* Sun Aug 13 2017 Raphael Groner <projects.rg@smart.ms> - 20170731-1
- new snapshot
- add appdata

* Sun Aug 13 2017 Raphael Groner <projects.rg@smart.ms> - 20170614-1
- new version

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 20170517-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Jun 10 2017 Raphael Groner <projects.rg@smart.ms> - 20170517-1
- new version

* Tue Mar 28 2017 Raphael Groner <projects.rg@smart.ms> - 20170326-1
- new version

* Sat Feb 11 2017 Raphael Groner <projects.rg@smart.ms> - 20170207-1
- new version
- drop additional icon and desktop file in favor of upstream ones

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 20161107-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 05 2016 Builder <projects.rg@smart.ms> - 20161107-2
- add ExcludeArch

* Wed Nov 09 2016 Raphael Groner <projects.rg@smart.ms> - 20161107-1
- new version

* Mon Nov 07 2016 Raphael Groner <projects.rg@smart.ms> - 20161012-1
- new version
- disable architectures without available wine
- don't check explicitly for wine version

* Sun Oct 09 2016 Raphael Groner <projects.rg@smart.ms> - 20161005-2
- use apps subfolder for icon

* Sun Oct 09 2016 Raphael Groner <projects.rg@smart.ms> - 20161005-1
- new version
- add copyright
- add icon

* Fri Jul 29 2016 Raphael Groner <projects.rg@smart.ms> - 20160724-1
- new version

* Mon Jul 11 2016 Raphael Groner <projects.rg@smart.ms> - 20160709-1
- initial
