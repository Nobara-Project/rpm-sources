%bcond_without compat
%bcond_without sanitizers
%global gitcommit 970d1abed24bc92b056e8b9a4df6f1104a95cc8f
# Be explicit about the soname in order to avoid unintentional changes.
# Before modifying any of the sonames, this must be announced to the Fedora
# community as it may break many other packages.
# A change proposal is needed:
# https://docs.fedoraproject.org/en-US/program_management/changes_policy/
%global soname libz-ng.so.2
%global compat_soname libz.so.1

# Compatible with the following zlib version.
%global zlib_ver 1.3.1
# Obsoletes zlib versions less than.
%global zlib_obsoletes 1.3

# ABI files for ix86 and s390x are not available upstream.
%global supported_abi_test aarch64 ppc64le x86_64

Name:		zlib-ng
Version:	2.1.6
Release:	2.git%{?dist}
Summary:	Zlib replacement with optimizations
License:	Zlib
Url:		https://github.com/zlib-ng/zlib-ng
Source0:	https://github.com/zlib-ng/zlib-ng/archive/%{gitcommit}.tar.gz

Patch0:		far.diff
#https://github.com/zlib-ng/zlib-ng/pull/1713
Patch1:     1713.patch

BuildRequires:	cmake >= 3.1
BuildRequires:	gcc-c++
BuildRequires:	cmake(GTest)
BuildRequires:	libabigail

%description
zlib-ng is a zlib replacement that provides optimizations for "next generation"
systems.

%package	devel
Summary:	Development files for %{name}
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description	devel
The %{name}-devel package contains libraries and header files for developing
application that use %{name}.

%if %{with compat}

%package	compat
Summary:	Zlib implementation provided by %{name}
Provides:	zlib = %{zlib_ver}
Provides:	zlib%{?_isa} = %{zlib_ver}
Conflicts:	zlib%{?_isa}
Obsoletes:	zlib < %{zlib_obsoletes}

%description	compat
zlib-ng is a zlib replacement that provides optimizations for "next generation"
systems.
The %{name}-compat package contains the library that is API and binary
compatible with zlib.

%package	compat-devel
Summary:	Development files for %{name}-compat
Requires:	%{name}-compat%{?_isa} = %{version}-%{release}
Provides:	zlib-devel = %{zlib_ver}
Provides:	zlib-devel%{?_isa} = %{zlib_ver}
Conflicts:	zlib-devel%{?_isa}
Obsoletes:	zlib-devel < %{zlib_obsoletes}

%description	compat-devel
The %{name}-compat-devel package contains libraries and header files for
developing application that use zlib.

%package	compat-static
Summary:	Static libraries for %{name}-compat
Requires:	%{name}-compat-devel%{?_isa} = %{version}-%{release}
Provides:	zlib-static = %{zlib_ver}
Provides:	zlib-static%{?_isa} = %{zlib_ver}
Conflicts:	zlib-static%{?_isa}
Obsoletes:	zlib-static < %{zlib_obsoletes}

%description	compat-static
The %{name}-compat-static package contains static libraries needed for
developing applications that use zlib.

%endif

%prep
%autosetup -p1 -n %{name}-%{gitcommit}

%build
cat <<_EOF_
###########################################################################
#
# Build the default zlib-ng library
#
###########################################################################
_EOF_

# zlib-ng uses a different macro for library directory.
%global cmake_param %{?with_sanitizers:-DWITH_SANITIZER=ON}

# Setting __cmake_builddir is not necessary in this step, but do it anyway for symmetry.
%global __cmake_builddir %{_vpath_builddir}
%cmake %{cmake_param}
%cmake_build

%if %{with compat}
cat <<_EOF_
###########################################################################
#
# Build the compat mode library
#
###########################################################################
_EOF_

%global __cmake_builddir %{_vpath_builddir}-compat
# defining BUILD_SHARED_LIBS disables the static library
%undefine _cmake_shared_libs
# Disable new strategies in order to keep compatibility with zlib.
%cmake %{cmake_param} -DZLIB_COMPAT=ON -DWITH_NEW_STRATEGIES=OFF
%cmake_build
%endif

%check
cat <<_EOF_
###########################################################################
#
# Run the zlib-ng tests
#
###########################################################################
_EOF_

%global __cmake_builddir %{_vpath_builddir}
%ctest

%ifarch ppc64le
# Workaround Copr, that sets _target_cpu to ppc64le.
%global target_cpu powerpc64le
%else
%global target_cpu %{_target_cpu}
%endif

%ifarch x86_64
%global vendor pc
%else
%global vendor unknown
%endif

%ifarch %{supported_abi_test}
CHOST=%{target_cpu}-%{vendor}-linux-gnu sh test/abicheck.sh
%endif

%if %{with compat}
cat <<_EOF_
###########################################################################
#
# Run the compat mode tests
#
###########################################################################
_EOF_

%global __cmake_builddir %{_vpath_builddir}-compat
%ctest
%ifarch %{supported_abi_test}
CHOST=%{target_cpu}-%{vendor}-linux-gnu sh test/abicheck.sh --zlib-compat
%endif
%endif


%install
%global __cmake_builddir %{_vpath_builddir}
%cmake_install

%if %{with compat}
%global __cmake_builddir %{_vpath_builddir}-compat
%cmake_install
%endif

%files
%license LICENSE.md
%doc README.md
%{_libdir}/libz-ng.so.%{version}
%{_libdir}/%{soname}

%files devel
%{_includedir}/zconf-ng.h
%{_includedir}/zlib-ng.h
%{_includedir}/zlib_name_mangling-ng.h
%{_libdir}/libz-ng.so
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/cmake/zlib-ng/*

%if %{with compat}

%files compat
%{_libdir}/%{compat_soname}
%{_libdir}/libz.so.%{zlib_ver}.zlib-ng

%files compat-devel
%{_includedir}/zconf.h
%{_includedir}/zlib.h
%{_includedir}/zlib_name_mangling.h
%{_libdir}/libz*.so*
%{_libdir}/pkgconfig/zlib.pc
%{_libdir}/cmake/ZLIB/*

%files compat-static
%{_libdir}/libz.a


%endif


%changelog
* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jan 11 2024 Lukas Javorsky <ljavorsk@redhat.com> - 2.1.6-1
- Rebase to version 2.1.6

* Tue Jan 09 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 2.1.5-2
- Add zlib-ng-compat-static to replace zlib-static

* Wed Dec 20 2023 Tulio Magno Quites Machado Filho <tuliom@redhat.com> - 2.1.5-1
- Update to zlib-ng 2.1.5

* Wed Oct 18 2023 Tulio Magno Quites Machado Filho <tuliom@redhat.com> - 2.1.3-7
- Improve the patch that defines the FAR macro

* Wed Sep 27 2023 Tulio Magno Quites Machado Filho <tuliom@redhat.com> - 2.1.3-6
- Add a patch that defines the FAR macro

* Wed Sep 20 2023 Tulio Magno Quites Machado Filho <tuliom@redhat.com> - 2.1.3-5
- Fix WITH_SANITIZER

* Tue Sep 19 2023 Tulio Magno Quites Machado Filho <tuliom@redhat.com> - 2.1.3-4
- Disable WITH_NEW_STRATEGIES in compat mode

* Thu Aug 24 2023 Tulio Magno Quites Machado Filho <tuliom@redhat.com> - 2.1.3-3
- Enable zlib compat build

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Ali Erdinc Koroglu <aekoroglu@fedoraproject.org> - 2.1.3-1
- Update to 2.1.3

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Apr 14 2022 Ali Erdinc Koroglu <aekoroglu@fedoraproject.org> - 2.0.6-1
- New upstream release 2.0.6

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.5-2.20210625gitc69f78bc5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sat Aug 07 2021 Tulio Magno Quites Machado Filho <tuliom@ascii.art.br> - 2.0.2-5.20210625gitc69f78bc5e
- Update to v2.0.5.

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-2.20210323git5fe25907e
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sun Apr 18 2021 Tulio Magno Quites Machado Filho <tuliom@ascii.art.br> - 2.0.2-1.20210323gite5fe25907e
- Update to v2.0.2.
- Remove the manpage that got removed from upstream.

* Thu Jan 28 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.9-0.4.20200912gite58738845
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sun Sep 13 2020 Tulio Magno Quites Machado Filho <tuliom@ascii.art.br> - 1.9.9-0.3.20200912gite58738845
- Update to a newer commit.

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.9-0.3.20200609gitfe69810c2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jul 09 2020 Tulio Magno Quites Machado Filho <tuliom@ascii.art.br> - 1.9.9-0.2.20200609gitfe69810c2
- Replace cmake commands with new cmake macros

* Mon Jul 06 2020 Tulio Magno Quites Machado Filho <tuliom@ascii.art.br> - 1.9.9-0.1.20200609gitfe69810c2
- Improve the archive name.
- Starte release at 0.1 as required for prerelease.
- Make the devel package require an arch-dependent runtime subpackage.
- Remove %%ldconfig_scriptlets.
- Glob the man page extension.
- Move unversioned shared library to the devel subpackage

* Wed Jul 01 2020 Tulio Magno Quites Machado Filho <tuliom@ascii.art.br> - 1.9.9-0.20200609gitfe69810c2
- Initial commit
