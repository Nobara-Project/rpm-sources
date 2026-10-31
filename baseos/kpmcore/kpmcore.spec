%global kf6min 5.240.0
%global qt6min 6.5.0
%global sover 13

Name:           kpmcore
Version:        26.08.1
Release:        1.nobara%{?dist}
Summary:        Library for managing partitions by KDE programs
License:        GPL-3.0-or-later AND MIT AND CC-BY-4.0 AND CC0-1.0
URL:            https://github.com/KDE/kpmcore
Source:         https://download.kde.org/stable/release-service/%{version}/src/%{name}-%{version}.tar.xz
# Nobara: let Calamares plan logical volumes in a volume group it will create
Patch0:         0001-manual-lvm-planning.patch


BuildRequires:  cmake >= 3.16
BuildRequires:  extra-cmake-modules
BuildRequires:  gettext
BuildRequires:  kf6-rpm-macros

BuildRequires:  cmake(Qt6Core) >= %{qt6min}
BuildRequires:  cmake(Qt6DBus) >= %{qt6min}
BuildRequires:  cmake(Qt6Gui) >= %{qt6min}
BuildRequires:  cmake(Qt6Widgets) >= %{qt6min}

BuildRequires:  cmake(KF6CoreAddons) >= %{kf6min}
BuildRequires:  cmake(KF6I18n) >= %{kf6min}
BuildRequires:  cmake(KF6WidgetsAddons) >= %{kf6min}

BuildRequires:  cmake(PolkitQt6-1)

BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(blkid) >= 2.33.2

Requires:       e2fsprogs
Requires:       kf6-filesystem

Recommends:     dosfstools
Recommends:     exfatprogs
Recommends:     f2fs-tools
Recommends:     fatresize
Recommends:     hfsutils
Recommends:     hfsplus-tools
Recommends:     jfsutils
Recommends:     nilfs-utils
Recommends:     ocfs2-tools
Recommends:     udftools

%description
KPMcore contains common code for managing partitions by KDE Partition Manager 
and other KDE projects


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       cmake(Qt6Core) >= %{qt6min}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}


%prep
%autosetup -p1

%build
%cmake_kf6
%cmake_build


%install
%cmake_install
%find_lang %{name}
%find_lang %{name}._policy_


%files -f %{name}.lang -f %{name}._policy_.lang
%license LICENSES/*
%doc README.md
%{_kf6_libdir}/libkpmcore.so.%{sover}
%{_kf6_libdir}/libkpmcore.so.%{version}
%{_kf6_qtplugindir}/kpmcore
%{_libexecdir}/kpmcore_externalcommand
%{_datadir}/dbus-1/system.d/org.kde.kpmcore.*.conf
%{_datadir}/dbus-1/system-services/org.kde.kpmcore.*.service
%{_datadir}/polkit-1/actions/org.kde.kpmcore.externalcommand.policy

%files devel
%{_includedir}/%{name}/
%{_kf6_libdir}/cmake/KPMcore
%{_kf6_libdir}/libkpmcore.so


%changelog
* Fri Oct 30 2026 Nobara Project <support@nobaraproject.org> - 26.08.1-1.nobara
- Add an LvmDevice constructor for planned (not yet created) volume groups,
  used by Calamares manual partitioning.
- Fix a division by zero when sizing logical volumes on LVM devices whose
  extents are larger than the partition alignment.

* Wed Sep 09 2026 Steve Cossette <farchord@gmail.com> - 26.08.1-1
- 26.08.1

* Fri Aug 14 2026 Steve Cossette <farchord@gmail.com> - 26.08.0-1
- 26.08.0

* Fri Jul 31 2026 Steve Cossette <farchord@gmail.com> - 26.07.90-1
- 26.07.90

* Wed Jul 29 2026 Steve Cossette <farchord@gmail.com> - 26.07.80-1
- 26.07.80

* Thu Jul 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 26.04.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_45_Mass_Rebuild

* Tue Jun 30 2026 Steve Cossette <farchord@gmail.com> - 26.04.3-1
- 26.04.3

* Wed Jun 03 2026 Steve Cossette <farchord@gmail.com> - 26.04.2-1
- 26.04.2

* Wed May 06 2026 Steve Cossette <farchord@gmail.com> - 26.04.1-1
- 26.04.1

* Sat Apr 11 2026 Steve Cossette <farchord@gmail.com> - 26.04.0-1
- 26.04.0

* Mon Mar 16 2026 Steve Cossette <farchord@gmail.com> - 26.03.80-1
- 26.03.80

* Sun Mar 08 2026 Steve Cossette <farchord@gmail.com> - 25.12.3-1
- 25.12.3

* Thu Feb 12 2026 Steve Cossette <farchord@gmail.com> - 25.12.2-2
- Full Stack Rebuild (kio abi break)

* Wed Feb 04 2026 Steve Cossette <farchord@gmail.com> - 25.12.2-1
- 25.12.2

* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 25.12.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Wed Jan 07 2026 farchord@gmail.com - 25.12.1-1
- 25.12.1

* Sat Dec 06 2025 Steve Cossette <farchord@gmail.com> - 25.12.0-1
- 25.12.0

* Fri Nov 28 2025 Steve Cossette <farchord@gmail.com> - 25.11.90-1
- 25.11.90

* Sat Nov 15 2025 Steve Cossette <farchord@gmail.com> - 25.11.80-1
- 25.11.80

* Tue Nov 04 2025 Steve Cossette <farchord@gmail.com> - 25.08.3-1
- 25.08.3

* Wed Oct 08 2025 Steve Cossette <farchord@gmail.com> - 25.08.2-1
- 25.08.2

* Sun Sep 21 2025 Steve Cossette <farchord@gmail.com> - 25.08.1-1
- 25.08.1

* Sat Aug 16 2025 Neal Gompa <ngompa@fedoraproject.org> - 25.08.0-2
- Undo RPMAutoSpec conversion

* Sat Aug 09 2025 Steve Cossette <farchord@gmail.com> - 25.08.0-1
- 25.08.0

* Sat Jul 26 2025 Steve Cossette <farchord@gmail.com> - 25.07.90-1
- 25.07.90

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 25.07.80-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jul 14 2025 Steve Cossette <farchord@gmail.com> - 25.07.80-1
- 25.07.80

* Thu Jul 03 2025 Steve Cossette <farchord@gmail.com> - 25.04.3-1
- 25.04.3

* Thu Jun 05 2025 Steve Cossette <farchord@gmail.com> - 25.04.2-1
- 25.04.2

* Wed May 14 2025 Steve Cossette <farchord@gmail.com> - 25.04.1-1
- 25.04.1

* Mon Apr 28 2025 Mattia Verga <mattia.verga@proton.me> - 25.04.0-2
- Backport patch to fix reported crashes

* Sat Apr 12 2025 Steve Cossette <farchord@gmail.com> - 25.04.0-1
- 25.04.0

* Sun Mar 23 2025 Steve Cossette <farchord@gmail.com> - 25.03.80-1
- 25.03.80

* Wed Mar 05 2025 Steve Cossette <farchord@gmail.com> - 24.12.3-1
- 24.12.3

* Fri Feb 21 2025 Steve Cossette <farchord@gmail.com> - 24.12.2-2
- Rebuild for ppc64le enablement

* Thu Feb 06 2025 Steve Cossette <farchord@gmail.com> - 24.12.2-1
- 24.12.2

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 24.12.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Jan 07 2025 Steve Cossette <farchord@gmail.com> - 24.12.1-1
- 24.12.1

* Sat Dec 07 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 24.12.0-1
- 24.12.0

* Fri Nov 29 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 24.11.90-1
- 24.11.90

* Wed Nov 20 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 24.11.80-1
- 24.11.80

* Wed Nov 06 2024 Steve Cossette <farchord@gmail.com> - 24.08.3-1
- 24.08.3

* Tue Oct 08 2024 Steve Cossette <farchord@gmail.com> - 24.08.2-1
- 24.08.2

* Thu Sep 26 2024 Alessandro Astone <ales.astone@gmail.com> - 24.08.1-1
- 24.08.1

* Fri Aug 23 2024 Steve Cossette <farchord@gmail.com> - 24.08.0-1
- 24.08.0

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 24.05.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Jul 07 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 24.05.2-1
- 24.05.2

* Sat Jun 15 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 24.05.1-1
- 24.05.1

* Sun May 19 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 24.05.0-1
- 24.05.0

* Sat Apr 13 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 24.02.2-1
- 24.02.2

* Fri Mar 29 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 24.02.1-1
- 24.02.1

* Fri Feb 23 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 24.02.0-1
- 24.02.0

* Thu Feb 01 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 24.01.95-1
- 24.01.95

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 24.01.90-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 24.01.90-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 13 2024 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 24.01.90-1
- 24.01.90

* Sat Dec 23 2023 Alessandro Astone <ales.astone@gmail.com> - 24.01.85-1
- 24.01.85

* Wed Dec 06 2023 Yaakov Selkowitz <yselkowitz@fedoraproject.org> - 24.01.80-1
- 24.01.80

* Sun Oct 15 2023 Mattia Verga <mattia.verga@proton.me> - 23.08.2-2
- Use qt6/kf6 for Fedora >= 40

* Thu Oct 12 2023 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 23.08.2-1
- 23.08.2

* Sat Sep 16 2023 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 23.08.1-1
- 23.08.1

* Sat Aug 26 2023 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 23.08.0-1
- 23.08.0

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 23.04.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jul 08 2023 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 23.04.3-1
- 23.04.3

* Tue Jun 06 2023 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 23.04.2-1
- 23.04.2

* Sun May 14 2023 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 23.04.1-1
- 23.04.1

* Fri Apr 14 2023 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 23.04.0-1
- 23.04.0

* Sat Apr 08 2023 Mattia Verga <mattia.verga@proton.me> - 23.03.90-4
- Update min requirements in specfile and set unstable var

* Sat Apr 08 2023 Mattia Verga <mattia.verga@proton.me> - 23.03.90-3
- Update license tag to SPDX

* Fri Mar 31 2023 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 23.03.90-1
- 23.03.90

* Mon Mar 27 2023 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 23.03.80-1
- 23.03.80

* Thu Mar 02 2023 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 22.12.3-1
- feat: 22.12.3

* Tue Jan 31 2023 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 22.12.2-1
- 22.12.2

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 22.12.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jan 04 2023 Justin Zobel <justin@1707.io> - 22.12.1-1
- Update to 22.12.1 and remove extraneous changelog

* Tue Jan 03 2023 Justin Zobel <justin@1707.io> - 22.12.0-2
- Update to 22.12.1

* Mon Dec 19 2022 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 22.12.0-1
- 22.12.0

* Fri Nov 04 2022 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 22.08.3-1
- 22.08.3

* Sat Oct 15 2022 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 22.08.2-1
- fix: update spec file

* Sat Oct 15 2022 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 22.08.1-2
- 22.08.2

* Thu Sep 08 2022 Marc Deop i Argemí <marcdeop@fedoraproject.org> - 22.08.1-1
- 22.08.1

* Sun Aug 21 2022 Marc Deop <marcdeop@fedoraproject.org> - 22.08.0-1
- 22.08.0

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 22.04.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jul 18 2022 Than Ngo <than@redhat.com> - 22.04.3-1
- 22.04.3

* Sat May 14 2022 Mattia Verga <mattia.verga@protonmail.com> - 22.04.1-1
- Release stable version 22.04.1

* Sat Mar 19 2022 Mattia Verga <mattia.verga@protonmail.com> - 22.03.80-1
- Unstable version 22.03.80

* Thu Mar 03 2022 Marc Deop <marcdeop@fedoraproject.org> - 21.12.3-1
- 21.12.3

* Mon Feb 14 2022 Marc Deop <marcdeop@fedoraproject.org> - 21.12.2-1
- 21.12.2

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 21.12.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jan 06 2022 Mattia Verga <mattia.verga@protonmail.com> - 21.12.1-1
- Release stable version 21.12.1

* Thu Dec 16 2021 Mattia Verga <mattia.verga@protonmail.com> - 21.12.0-1
- Release stable version 21.12.0

* Mon Nov 15 2021 Mattia Verga <mattia.verga@protonmail.com> - 21.11.80-1
- Release development version 21.11.80
- Remove retired reiserfs-utils from Recommends

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 21.04.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sun Apr 25 2021 Mattia Verga <mattia.verga@protonmail.com> - 21.04.0-1
- Release stable version 21.04.0
- Bump soname number to 11
- Initial support for dosfstools

* Sat Mar 06 2021 Mattia Verga <mattia.verga@protonmail.com> - 20.12.3-1
- Release stable version 20.12.3

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 20.12.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sun Dec 13 2020 Mattia Verga <mattia.verga@protonmail.com> - 20.12.0-1
- Release stable version 20.12.0

* Sun Dec 06 2020 Mattia Verga <mattia.verga@protonmail.com> - 20.11.90-1
- Update to unstable release 20.11.90

* Tue Nov 17 2020 Mattia Verga <mattia.verga@protonmail.com> - 20.11.80-2
- Removed Kauth BuildRequires

* Sat Nov 14 2020 Mattia Verga <mattia.verga@protonmail.com> - 20.11.80-1
- Update to unstable release 20.11.80
- Move to KDE release-service versioning

* Sat Oct 17 2020 Mattia Verga <mattia.verga@protonmail.com> - 4.2.0-1
- Update to stable release 4.2.0

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Feb 10 2020 Mattia Verga <mattia.verga@protonmail.com> - 4.1.0-1
- Update to stable release 4.1.0

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Oct 12 2019 Mattia Verga <mattia.verga@protonmail.com> - 4.0.1-1
- Update to stable release 4.0.1

* Mon Aug 05 2019 Mattia Verga <mattia.verga@protonmail.com> - 4.0.0-5
- Fix again %%files section

* Sun Aug 04 2019 Mattia Verga <mattia.verga@protonmail.com> - 4.0.0-4
- Fix %%files section RHBZ#1735969

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat May 11 2019 Mattia Verga <mattia.verga@protonmail.com> - 4.0.0-2
- Backport patch to fix partition restoring RHBZ#1639021

* Sun May 05 2019 Mattia Verga <mattia.verga@protonmail.com> - 4.0.0-1
- Update to stable release 4.0.0

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jun 30 2018 Mattia Verga <mattia.verga@yandex.com> - 3.3.0-3
- Remove ldconfig scriptlets

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Dec 26 2017 Mattia Verga <mattia.verga@tiscali.it> - 3.3.0-1
- Update to stable release 3.3.0
- Soname bump to libkpmcore.so.7

* Wed Nov 01 2017 Mattia Verga <mattia.verga@email.it> - 3.2.1-1
- Update to stable release 3.2.1

* Sun Oct 01 2017 Mattia Verga <mattia.verga@tiscali.it> - 3.2.0-1
- Update to stable release 3.2.0
- Soname bump to libkpmcore.so.6
- Remove kf5-kio-devel dependency
- Add udftools as recommended package

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jul 06 2017 Mattia Verga <mattia.verga@tiscali.it> - 3.1.2-1
- Update to stable release 3.1.2

* Sun Jun 04 2017 Mattia Verga <mattia.verga@tiscali.it> - 3.1.0-1
- Update to stable release 3.1.0
- Soname bump to libkpmcore.so.5

* Thu Feb 09 2017 Mattia Verga <mattia.verga@tiscali.it> - 3.0.3-1
- Update to stable release 3.0.3

* Sun Jan 15 2017 Kevin Kofler <Kevin@tigcc.ticalc.org> - 3.0.2-1
- Update to stable release 3.0.2 (additional bug fixes for Calamares)

* Sun Jan 01 2017 Mattia Verga <mattia.verga@tiscali.it> - 3.0.1-1
- Update to stable release 3.0.1 to fix possible data loss

* Wed Dec 21 2016 Mattia Verga <mattia.verga@tiscali.it> - 3.0.0-1
- Update to stable release 3.0.0

* Fri Nov 25 2016 Mattia Verga <mattia.verga@tiscali.it> - 2.9.90-2
- Backport patch from upstream to fix Calamares bug CAL-416

* Wed Nov 9 2016 Mattia Verga <mattia.verga@tiscali.it> - 2.9.90-1
- Update to unstable 2.9.90
- Soname bump to libkpmcore.so.4
- Add LVM support

* Sun Jul 10 2016 Mattia Verga <mattia.verga@tiscali.it> - 2.2.1-1
- Update to stable 2.2.1
- Switch to hfsplus-tools

* Sun Jun 12 2016 Mattia Verga <mattia.verga@tiscali.it> - 2.2.0-2
- Add weak dependencies to less used filesystem tools

* Sat Jun 11 2016 Mattia Verga <mattia.verga@tiscali.it> - 2.2.0-1
- Update to stable 2.2.0
- Soname bump to libkpmcore.so.3

* Sun May 15 2016 Mattia Verga <mattia.verga@tiscali.it> - 2.1.1-1
- Update to stable 2.1.1

* Sun Mar 13 2016 Mattia Verga <mattia.verga@tiscali.it> - 2.1.0-1
- Update to stable 2.1.0
- Use pkgconfig for libparted

* Sun Feb 28 2016 Mattia Verga <mattia.verga@tiscali.it> - 2.0.1-1
- Update to stable 2.0.1
- Use pkgconfig for libraries
- Alphabetically ordered BR
- Fix Provides and Obsoletes also for -devel package

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Jan 16 2016 Mattia Verga <mattia.verga@tiscali.it> - 2.0.0-2
- Rename from KPMcore to kpmcore

* Thu Jan 14 2016 Mattia Verga <mattia.verga@tiscali.it> - 2.0.0-1
- Update to stable 2.0.0

* Sun Nov 29 2015 Mattia Verga <mattia.verga@tiscali.it> - 1.9.50-5
- Fix package naming

* Sun Nov 29 2015 Mattia Verga <mattia.verga@tiscali.it> - 1.9.50-4
- Replace Obsoletes with Conflicts

* Wed Nov 25 2015 Mattia Verga <mattia.verga@tiscali.it> - 1.9.50-3
- Patch to fix soname versioning

* Mon Nov 23 2015 Mattia Verga <mattia.verga@tiscali.it> - 1.9.50-2
- Make a devel subpackage

* Sun Nov 22 2015 Mattia Verga <mattia.verga@tiscali.it> - 1.9.50-1
- Initial release
