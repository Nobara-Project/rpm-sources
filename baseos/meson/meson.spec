## START: Set by rpmautospec
## (rpmautospec version 0.3.5)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 1;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

%global libname mesonbuild

# Don’t run the tests by default, since they are rather flaky.
# I’ll get to getting them running eventually, but free time is sparse.
# — ekulik
%bcond_with check

Name:           meson
Version:        1.3.0
Release:        %autorelease
Summary:        High productivity build system

License:        ASL 2.0
URL:            https://mesonbuild.com/
Source:         https://github.com/mesonbuild/meson/releases/download/%{version_no_tilde .}/meson-%{version_no_tilde %{quote:}}.tar.gz

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
Requires:       python%{python3_version}dist(setuptools)
Requires:       ninja-build

%if %{with check}
BuildRequires:  ninja-build
# Some tests expect the unversioned executable
BuildRequires:  /usr/bin/python
# Various languages
BuildRequires:  gcc
BuildRequires:  libasan
BuildRequires:  gcc-c++
BuildRequires:  gcc-gfortran
BuildRequires:  gcc-objc
BuildRequires:  gcc-objc++
BuildRequires:  java-devel
BuildRequires:  libomp-devel
BuildRequires:  mono-core mono-devel
BuildRequires:  rust
# Since the build is noarch, we can't use %%ifarch
#%%ifarch %%{ldc_arches}
#BuildRequires:  ldc
#%%endif
# Various libs support
BuildRequires:  boost-devel
BuildRequires:  gtest-devel
BuildRequires:  gmock-devel
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtbase-private-devel
BuildRequires:  qt5-linguist
BuildRequires:  vala
BuildRequires:  python3-gobject-base
BuildRequires:  wxGTK3-devel
BuildRequires:  flex
BuildRequires:  bison
BuildRequires:  gettext
BuildRequires:  gnustep-base-devel
BuildRequires:  %{_bindir}/gnustep-config
BuildRequires:  git-core
BuildRequires:  pkgconfig(protobuf)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(glib-sharp-2.0)
BuildRequires:  pkgconfig(gobject-introspection-1.0)
BuildRequires:  gtk-doc
BuildRequires:  itstool
BuildRequires:  pkgconfig(zlib)
BuildRequires:  zlib-static
BuildRequires:  python3dist(cython)
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  %{_bindir}/pcap-config
BuildRequires:  pkgconfig(vulkan)
BuildRequires:  llvm-devel
BuildRequires:  cups-devel
%endif

%description
Meson is a build system designed to optimize programmer
productivity. It aims to do this by providing simple, out-of-the-box
support for modern software development tools and practices, such as
unit tests, coverage reports, Valgrind, CCache and the like.

%prep
%autosetup -p1 -n meson-%{version_no_tilde %{quote:}}
# Macro should not change when we are redefining bindir
sed -i -e "/^%%__meson /s| .*$| %{_bindir}/%{name}|" data/macros.%{name}

%build
%py3_build

%install
%py3_install
install -Dpm0644 -t %{buildroot}%{rpmmacrodir} data/macros.%{name}
install -Dpm0644 -t %{buildroot}%{_datadir}/bash-completion/completions/ data/shell-completions/bash/meson
install -Dpm0644 -t %{buildroot}%{_datadir}/zsh/site-functions/ data/shell-completions/zsh/_meson

%if %{with check}
%check
# Remove Boost tests for now, because it requires Python 2
rm -rf "test cases/frameworks/1 boost"
# Remove MPI tests for now because it is complicated to run
rm -rf "test cases/frameworks/17 mpi"
export MESON_PRINT_TEST_OUTPUT=1
%{__python3} ./run_tests.py
%endif

%files
%license COPYING
%{_bindir}/%{name}
%{python3_sitelib}/%{libname}/
%{python3_sitelib}/%{name}-*.egg-info/
%{_mandir}/man1/%{name}.1*
%{rpmmacrodir}/macros.%{name}
%dir %{_datadir}/polkit-1
%dir %{_datadir}/polkit-1/actions
%{_datadir}/polkit-1/actions/com.mesonbuild.install.policy
%{_datadir}/bash-completion/completions/meson
%{_datadir}/zsh/site-functions/_meson

%changelog
* Sat Oct 21 2023 Kalev Lember <klember@redhat.com> - 1.2.3-1
- Update to 1.2.3 (rhbz#2245374)

* Sun Oct 08 2023 Kalev Lember <klember@redhat.com> - 1.2.2-2
- Revert bindgen breakage (rhbz#2241430)

* Fri Sep 29 2023 Kalev Lember <klember@redhat.com> - 1.2.2-1
- Update to 1.2.2

* Wed Aug 09 2023 Kalev Lember <klember@redhat.com> - 1.2.1-1
- Update to 1.2.1 (rhbz#2230235)

* Wed Aug 02 2023 Kalev Lember <klember@redhat.com> - 1.2.0-1
- Update to 1.2.0 (rhbz#2218693)

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 1.1.1-2
- Rebuilt for Python 3.12

* Fri May 26 2023 Kalev Lember <klember@redhat.com> - 1.1.1-1
- Update to 1.1.1 (rhbz#2210176)

* Wed Apr 12 2023 Kalev Lember <klember@redhat.com> - 1.1.0-1
- Update to 1.1.0 (rhbz#2182559)

* Thu Mar 09 2023 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.0.1-1
- Update to 1.0.1 (rhbz#2173210)

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Jan 09 2023 Miro Hrončok <miro@hroncok.cz> - 1.0.0-2
- Fix for meson test crashes with Python 3.12
- Fixes: rhbz#2155463

* Fri Dec 23 2022 Kalev Lember <klember@redhat.com> - 1.0.0-1
- Update to 1.0.0

* Tue Nov 22 2022 Kalev Lember <klember@redhat.com> - 0.64.1-1
- Update to 0.64.1

* Mon Nov 07 2022 Kalev Lember <klember@redhat.com> - 0.64.0-1
- Update to 0.64.0

* Thu Oct 06 2022 Kalev Lember <klember@redhat.com> - 0.63.3-1
- Update to 0.63.3

* Sat Sep 03 2022 Kalev Lember <klember@redhat.com> - 0.63.2-1
- Update to 0.63.2

* Thu Aug 25 2022 Otto Liljalaakso <otto.liljalaakso@iki.fi> - 0.63.1-2
- Apply upstream patch for D build issue
- Fixes rhbz#2121586

* Sat Aug 13 2022 Kalev Lember <klember@redhat.com> - 0.63.1-1
- Update to 0.63.1

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.62.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jun 21 2022 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.62.2-1
- Version 0.62.2

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 0.62.1-3
- Rebuilt for Python 3.11

* Tue Apr 26 2022 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.62.1-1
- Update to 0.62.1

* Tue Mar 15 2022 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.61.3-1
- Update to 0.61.3
- Install zsh & bash completion

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.60.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sun Dec 26 2021 Kalev Lember <klember@redhat.com> - 0.60.3-1
- Update to 0.60.3

* Mon Dec 06 2021 Kalev Lember <klember@redhat.com> - 0.60.2-1
- Update to 0.60.2

* Fri Nov 12 2021 Neal Gompa <ngompa@fedoraproject.org> - 0.60.1-1
- Update to 0.60.1

* Thu Oct 28 2021 Kalev Lember <klember@redhat.com> - 0.59.4-1
- Update to 0.59.4

* Sat Oct 23 2021 Kalev Lember <klember@redhat.com> - 0.59.3-1
- Update to 0.59.3

* Sat Aug 21 2021 Kalev Lember <klember@redhat.com> - 0.59.1-1
- Update to 0.59.1

* Tue Aug 17 2021 Adam Williamson <awilliam@redhat.com> - 0.59.0-2
- Backport PR #9027 to fix a bug that broke some test suites (#1994006)

* Fri Jul 23 2021 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.59.0-1
- new version

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.58.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jun 03 2021 Python Maint <python-maint@redhat.com> - 0.58.0-4
- Rebuilt for Python 3.10

* Tue May 25 2021 Ondrej Holy <oholy@redhat.com> - 0.58.0-3
- Backport upstream patch to fix environment variable regression

* Thu May 20 2021 Kalev Lember <klember@redhat.com> - 0.58.0-2
- Backport upstream patch to fix gtkdoc generation

* Wed May 05 2021 Marc-André Lureau <marcandre.lureau@redhat.com> - 0.58.0-1
- new version

* Sun Apr 11 2021 Kalev Lember <klember@redhat.com> - 0.57.2-1
- Update to 0.57.2

* Fri Mar 05 2021 Igor Raits <ignatenkobrain@fedoraproject.org> - 0.57.1-1
- Update to 0.57.1

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.56.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Jan 21 2021 Kalev Lember <klember@redhat.com> - 0.56.2-1
- Update to 0.56.2

* Tue Nov 10 2020 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.56.0-1
- Update to latest version (#1889242)

* Fri Nov 06 2020 Jeff Law <law@redhat.com> - 0.55.3-2
- Avoid bogus volatile in gnome modules support code caught by gcc-11

* Fri Sep 11 2020 Kalev Lember <klember@redhat.com> - 0.55.3-1
- Update to 0.55.3

* Thu Sep 10 2020 Kalev Lember <klember@redhat.com> - 0.55.2-1
- Update to 0.55.2

* Thu Aug 20 2020 Kalev Lember <klember@redhat.com> - 0.55.1-1
- Update to 0.55.1

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.55.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun Jul 12 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 0.55.0-1
- Update to 0.55.0

* Mon Jul 06 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 0.55.0~rc2-1
- Update to 0.55.0rc2

* Fri Jul 03 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 0.55.0~rc1-1
- Update to 0.55.0rc1

* Thu Jun 18 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 0.54.3-2
- Use verbose mode for meson compile

* Mon Jun 15 2020 Kalev Lember <klember@redhat.com> - 0.54.3-1
- Update to 0.54.3

* Mon Jun 15 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 0.54.2-3
- Switch to meson compile / meson install

* Fri May 22 2020 Miro Hrončok <mhroncok@redhat.com> - 0.54.2-2
- Rebuilt for Python 3.9

* Fri May 15 2020 Kalev Lember <klember@redhat.com> - 0.54.2-1
- Update to 0.54.2

* Thu May 07 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 0.54.1-1
- Update to 0.54.1

* Mon Mar 30 2020 - Ernestas Kulik <ekulik@redhat.com> - 0.54.0-1
- Update to 0.54.0

* Sat Mar 14 2020 - Ernestas Kulik <ekulik@redhat.com> - 0.53.2-1.git88e40c7
- Update to snapshot of 0.53.2 with D fixes

* Fri Feb 07 2020 - Ernestas Kulik <ekulik@redhat.com> - 0.53.1-1
- Update to 0.53.1

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.52.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Dec 26 2019 Björn Esser <besser82@fedoraproject.org> - 0.52.1-1
- Update to 0.52.1

* Wed Oct 09 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.52.0-1
- Update to 0.52.0

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.51.2-2
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 26 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.51.2-1
- Update to 0.51.2

* Thu Aug 15 2019 Miro Hrončok <mhroncok@redhat.com> - 0.51.1-3
- Rebuilt for Python 3.8

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.51.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jul 10 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.51.1-1
- Update to 0.51.1

* Mon Jun 17 10:03:21 CEST 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.51.0-1
- Update to 0.51

* Wed Apr 17 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.50.1-1
- Update to 0.50.1

* Mon Apr 15 2019 Adam Williamson <awilliam@redhat.com> - 0.50.0-4
- Backport patch to revert ld binary method change (#1699099)

* Mon Apr 08 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.50.0-3
- Drop -Db_ndebug=true and just fix it instead

* Mon Mar 25 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.50.0-2
- Set -Db_ndebug=true

* Sun Mar 10 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.50.0-1
- Update to 0.50.0

* Mon Feb 04 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.49.2-1
- Update to 0.49.2

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.49.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 23 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.49.1-1
- Update to 0.49.1

* Sun Dec 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.49.0-1
- Update to 0.49.0

* Sat Nov 17 2018 Kalev Lember <klember@redhat.com> - 0.48.2-1
- Update to 0.48.2

* Sun Oct 21 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.48.1-1
- Update to 0.48.1

* Wed Sep 26 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.48.0-2
- Add missing dependency on setuptools

* Tue Sep 25 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.48.0-1
- Update to 0.48.0

* Sat Aug 25 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.47.2-1
- Update to 0.47.2

* Wed Jul 25 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.47.1-5
- Backport more patches for "feature" option type

* Tue Jul 24 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.47.1-4
- Don't sneak auto-features patch yet

* Tue Jul 24 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.47.1-3
- Macros improvements

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.47.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jul 10 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.47.1-1
- Update to 0.47.1

* Mon Jul 02 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.47.0-1
- Update to 0.47.0

* Thu Jun 28 2018 Miro Hrončok <mhroncok@redhat.com> - 0.46.1-3
- Fix error on Python 3.7 (#1596230)

* Mon Jun 18 2018 Miro Hrončok <mhroncok@redhat.com> - 0.46.1-2
- Rebuilt for Python 3.7

* Thu May 17 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.46.1-1
- Update to 0.46.1

* Fri May 04 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.46.0-2
- Backport upstream fixes

* Tue Apr 24 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.46.0-1
- Update to 0.46.0

* Wed Mar 21 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.45.1-1
- Update to 0.45.1

* Sun Mar 04 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.45.0-1
- Update to 0.45.0

* Tue Feb 20 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.44.1-1
- Update to 0.44.1

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.44.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Dec 10 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.44.0-1
- Update to 0.44.0

* Mon Oct 09 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.43.0-1
- Update to 0.43.0

* Tue Sep 12 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.42.1-1
- Update to 0.42.1

* Fri Aug 18 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.42.0-1
- Update to 0.42.0

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.41.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jul 19 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.41.2-1
- Update to 0.41.2

* Tue Jul 18 2017 Kalev Lember <klember@redhat.com> - 0.41.1-3
- Backport various gtk-doc fixes from upstream

* Thu Jul 13 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.41.1-2
- Strip trailing slash from pkg-config files

* Mon Jun 19 2017 Igor Gnatenko <ignatenko@redhat.com> - 0.41.1-1
- Update to 0.41.1

* Tue Jun 13 2017 Igor Gnatenko <ignatenko@redhat.com> - 0.41.0-1
- Update to 0.41.0

* Wed May 31 2017 Igor Gnatenko <ignatenko@redhat.com> - 0.40.1-2
- Don't run ldc tests

* Fri Apr 28 2017 Igor Gnatenko <ignatenko@redhat.com> - 0.40.1-1
- Update to 0.40.1

* Sun Apr 23 2017 Igor Gnatenko <ignatenko@redhat.com> - 0.40.0-1
- Update to 0.40.0

* Thu Apr 13 2017 Igor Gnatenko <ignatenko@redhat.com> - 0.39.1-2
- Exclude ldc for module builds

* Thu Mar 16 2017 Igor Gnatenko <ignatenko@redhat.com> - 0.39.1-1
- Update to 0.39.1

* Mon Mar 06 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.39.0-1
- Update to 0.39.0

* Tue Feb 07 2017 Igor Gnatenko <ignatenko@redhat.com> - 0.38.1-1
- Update to 0.38.1

* Sun Jan 29 2017 Igor Gnatenko <ignatenko@redhat.com> - 0.38.0-1
- Update to 0.38.0

* Thu Dec 22 2016 Miro Hrončok <mhroncok@redhat.com> - 0.37.1-2
- Rebuild for Python 3.6

* Tue Dec 20 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.37.1-1
- Update to 0.37.1

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.37.0-2
- Rebuild for Python 3.6

* Sun Dec 18 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.37.0-1
- Update to 0.37.0

* Thu Dec 15 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.36.0-4
- Backport more RPM macro fixes (FPC ticket #655)

* Tue Dec 13 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.36.0-3
- Backport fixes to RPM macros

* Sat Dec 03 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.36.0-2
- Print test output during build

* Mon Nov 14 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.36.0-1
- Update to 0.36.0

* Tue Oct 18 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.35.1-1
- Update to 0.35.1 (RHBZ #1385986)

* Tue Oct 11 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.35.0-3
- Backport couple of fixes

* Wed Oct 05 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.35.0-2
- Apply patch to fix FTBFS

* Mon Oct 03 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.35.0-1
- Update to 0.35.0

* Wed Sep 07 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.34.0-2
- Run D test suite

* Wed Sep 07 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.34.0-1
- Update to 0.34.0

* Tue Aug 09 2016 Jon Ciesla <limburgher@gmail.com> - 0.33.0-2
- Obsoletes fix.

* Tue Aug 09 2016 Jon Ciesla <limburgher@gmail.com> - 0.33.0-1
- 0.33.0
- GUI dropped upstream.

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.31.0-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Apr 14 2016 Igor Gnatenko <ignatenko@redhat.com> - 0.31.0-1
- Update to 0.31.0

* Sun Mar 20 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.30.0-1
- Update to 0.30.0

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.29.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Jan 24 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.29.0-1
- Update to 0.29.0

* Fri Jan 15 2016 Jonathan Wakely <jwakely@redhat.com> - 0.28.0-2
- Rebuilt for Boost 1.60

* Mon Dec 28 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.28.0-1
- 0.28.0

* Wed Nov 25 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.27.0-1
- 0.27.0

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.26.0-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Fri Oct 30 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.26.0-2
- Fix rpm macros for using optflags

* Sun Sep 13 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.26.0-1
- 0.26.0

* Thu Aug 27 2015 Jonathan Wakely <jwakely@redhat.com> - 0.25.0-4
- Rebuilt for Boost 1.59

* Wed Jul 29 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.25.0-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/F23Boost159

* Wed Jul 22 2015 David Tardon <dtardon@redhat.com> - 0.25.0-2
- rebuild for Boost 1.58

* Sun Jul 12 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.25.0-1
- 0.25.0

* Sat Jul 11 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.24.0-3
- Update URLs
- drop unneded hacks in install section
- enable print test output for tests

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.24.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon May 25 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.24.0-1
- Update to 0.24.0

* Thu May 21 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.23.0-3.20150328git0ba1d54
- Update to latest git

* Thu May 21 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.23.0-3
- Add patch to accept .S files

* Wed Apr 29 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.23.0-2
- Add python3 to Requires (Thanks to Ilya Kyznetsov)

* Tue Mar 31 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.23.0-1
- 0.23.0

* Sat Mar 28 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.22.0-9.20150328git3b49b71
- Update to latest git

* Mon Mar 23 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.22.0-9.20150325git18550fe
- Update to latest git
- Include mesonintrospect

* Mon Mar 23 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.22.0-9.20150322git78d31ca
- Fix filelists for mesongui (python-bytecode-without-source)

* Sun Mar 22 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.22.0-8.20150322git78d31ca
- Enable C# tests

* Sun Mar 22 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.22.0-7.20150322git78d31ca
- update to latest git
- fix tests on arm

* Sat Mar 21 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.22.0-7.20150321gita084a8e
- update to latest git

* Mon Mar 16 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.22.0-7.20150316gitfa2c659
- update to latest git

* Tue Mar 10 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.22.0-7.20150310gitf9f51b1
- today's git snapshot with support for cool GNOME features
- re-enable wxGTK3 tests, package fixed in rawhide

* Thu Feb 26 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.22.0-6.git7581895
- split gui to subpkg
- update to latest snapshot
- enable tests

* Thu Feb 26 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.22.0-5.gitc6dbf98
- Fix packaging style
- Make package noarch

* Mon Feb 23 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.22.0-4.git.c6dbf98
- Use development version

* Sat Feb 21 2015 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.22.0-3
- Add ninja-build to requires

* Thu Jan 22 2015 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.22.0-2
- fix shebang in python files

* Wed Jan 21 2015 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.22.0-1
- Initial package

