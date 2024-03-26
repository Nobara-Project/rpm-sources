Name:           lazarus
Summary:        Lazarus Component Library and IDE for Free Pascal

Version:        3.2

%global baserelease 1
Release:        %{baserelease}%{?dist}

# The qt5pas version is taken from lcl/interfaces/qt5/cbindings/Qt5Pas.pro
%global qt5pas_version 2.15
%global qt5pas_release %(relstr="%{version}.%{baserelease}"; relstr=(${relstr//./ }); ((relno=${relstr[0]}*10000 + ${relstr[1]}*100 + ${relstr[2]})); echo "${relno}%{?dist}";)

# The qt6pas version is taken from lcl/interfaces/qt6/cbindings/Qt6Pas.pro
%global qt6pas_version 6.2.7
%global qt6pas_release %{qt5pas_release}

# The IDE itself is licensed under GPLv2+, with minor parts under the modified LGPL.
# The Lazarus Component Library has parts licensed under all the licenses mentioned in the tag.
#
# GNU Classpath style exception, see COPYING.modifiedLGPL
%global license_doc   GPL-2.0-or-later
%global license_tools GPL-2.0-or-later
%global license_ide   GPL-2.0-or-later AND LGPL-2.0 WITH Classpath-exception-2.0
%global license_lcl   GPL-2.0-or-later AND LGPL-2.0 WITH Classpath-exception-2.0 AND MPL-1.1 AND Apache-2.0
License:        %{license_lcl}

URL:            http://www.lazarus-ide.org/
Source0:        https://downloads.sourceforge.net/project/%{name}/Lazarus%20Zip%20_%20GZip/Lazarus%20%{version}/%{name}-%{version}-0.tar.gz

Source100:      lazarus.appdata.xml

# Lazarus wants to put arch-specific stuff in /usr/share - make it go in /usr/lib istead
Patch0:         0000-Makefile_patch.diff

# lazbuild can be too eager to rebuild some Lazarus packages.
# This causes build failures on other Fedora packages, as it tries to overwrite files in /usr/lib.
#
# Taken from Debian:
# https://sources.debian.org/data/main/l/lazarus/3.0%2Bdfsg1-6/debian/patches/Fixed-crash-when-trying-to-recompile-packages.patch
Patch1:         Fixed-crash-when-trying-to-recompile-packages.patch

# -- Build-time dependencies

BuildRequires:  binutils
BuildRequires:  desktop-file-utils
BuildRequires:  fpc
BuildRequires:  fpc-src
BuildRequires:  gcc-c++
BuildRequires:  glibc-devel
BuildRequires:  gtk2-devel
BuildRequires:  libappstream-glib
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtx11extras-devel
BuildRequires:  qt6-qtbase-devel

# -- Run-time dependencies.
# Since "lazarus" is a metapackage, it puts strong requirements on the
# default set of sub-packages. Users not interested in the default set
# can omit the metapackage and install individual sub-packages
# as they see fit.

Requires:	%{name}-ide%{?_isa} = %{version}-%{release}
Requires:	%{name}-lcl%{?_isa} = %{version}-%{release}
Requires:	%{name}-lcl-nogui%{?_isa} = %{version}-%{release}
Requires:	%{name}-lcl-gtk2%{?_isa} = %{version}-%{release}
Requires:	%{name}-tools%{?_isa} = %{version}-%{release}

# For smooth upgrade from F38 or older. Can be removed in F41.
Obsoletes:  lazarus < 2.2.6-2

ExclusiveArch:  %{fpc_arches}

%description
Lazarus is an IDE to create (graphical and console) applications with
Free Pascal, the (L)GPLed Pascal and Object Pascal compiler that runs on
Windows, Linux, Mac OS X, FreeBSD and more.

Lazarus is the missing part of the puzzle that will allow you to develop
programs for all of the above platforms in a Delphi-like environment.
The IDE is a RAD tool that includes a form designer.

Unlike Java's "write once, run anywhere" motto, Lazarus and Free Pascal
strive for "write once, compile anywhere". Since the exact same compiler
is available on all of the above platforms you don't need to do any recoding
to produce identical products for different platforms.

In short, Lazarus is a free RAD tool for Free Pascal using its
Lazarus Component Library (LCL).


%package ide
Summary: Lazarus RAD IDE for Free Pascal
License: %{license_ide}

Requires:	%{name}-lcl%{?_isa} = %{version}-%{release}
Requires:	%{name}-tools%{?_isa} = %{version}-%{release}
Recommends:	%{name}-doc = %{version}-%{release}
Recommends:	%{name}-lcl-nogui%{?_isa} = %{version}-%{release}
Recommends:	%{name}-lcl-gtk2%{?_isa} = %{version}-%{release}

Requires: fpc-src
Requires: gdb
Requires: hicolor-icon-theme
Requires: make

%description ide
Lazarus is a cross-platform IDE and component library for Free Pascal.

This package provides the Lazarus RAD IDE.


%package tools
Summary: Lazarus IDE helper programs
License: %{license_tools}
Requires: binutils
Requires: fpc%{?_isa}
Requires: glibc-devel%{?_isa}
Requires: %{name}-lcl%{?_isa} = %{version}-%{release}

%description tools
Lazarus is a cross-platform IDE and component library for Free Pascal.

This package provides helper programs used for building Lazarus projects.


%package doc
Summary: Lazarus IDE documentation
License: %{license_doc}

# For smooth upgrade from F38 or older. Can be removed in F41.
Obsoletes:  lazarus < 2.2.6-2

%description doc
Lazarus is a cross-platform IDE and component library for Free Pascal.

This package contains documentation and example programs for the Lazarus IDE.


%package lcl
Summary: Lazarus Component Library

%description lcl
Lazarus is a cross-platform IDE and component library for Free Pascal.

This package contains the common parts of the Lazarus Component Library.


%package lcl-nogui
Summary: Lazarus Component Library - non-graphical components
Requires: %{name}-lcl%{?_isa} = %{version}-%{release}

%description lcl-nogui
Lazarus is a cross-platform IDE and component library for Free Pascal.

This package contains LCL components for developing non-graphical applications
and command-line tools.


%package lcl-gtk2
Summary: Lazarus Component Library - GTK2 widgetset support
Requires: %{name}-lcl%{?_isa} = %{version}-%{release}

Requires: gtk2-devel%{?_isa}

%description lcl-gtk2
Lazarus is a cross-platform IDE and component library for Free Pascal.

This package contains LCL components for developing applications
using the GTK2 widgetset.


%package lcl-gtk3
Summary: Lazarus Component Library - GTK2 widgetset support
Requires: %{name}-lcl%{?_isa} = %{version}-%{release}

Requires: gtk3-devel%{?_isa}

%description lcl-gtk3
Lazarus is a cross-platform IDE and component library for Free Pascal.

This package contains LCL components for developing applications
using the GTK3 widgetset.


%package lcl-qt
Summary: Lazarus Component Library - Qt widgetset support
Requires: %{name}-lcl%{?_isa} = %{version}-%{release}

Requires: qt-devel%{?_isa}
Requires: qt4pas-devel%{?_isa}

%description lcl-qt
Lazarus is a cross-platform IDE and component library for Free Pascal.

This package contains LCL components for developing applications
using the Qt widgetset.


%package lcl-qt5
Summary: Lazarus Component Library - Qt5 widgetset support
Requires: %{name}-lcl%{?_isa} = %{version}-%{release}

Requires: qt5pas-devel%{?_isa} = %{qt5pas_version}-%{qt5pas_release}

%description lcl-qt5
Lazarus is a cross-platform IDE and component library for Free Pascal.

This package contains LCL components for developing applications
using the Qt5 widgetset.


%package lcl-qt6
Summary: Lazarus Component Library - Qt6 widgetset support
Requires: %{name}-lcl%{?_isa} = %{version}-%{release}

Requires: qt6pas-devel%{?_isa} = %{qt6pas_version}-%{qt6pas_release}

%description lcl-qt6
Lazarus is a cross-platform IDE and component library for Free Pascal.

This package contains LCL components for developing applications
using the Qt6 widgetset.


# Qt5pas start
%package -n     qt5pas
Version:        %{qt5pas_version}
Release:        %{qt5pas_release}
Summary:        Qt5 bindings for Pascal

%description -n qt5pas
Qt5 bindings for Pascal from Lazarus.

%package -n     qt5pas-devel
Version:        %{qt5pas_version}
Release:        %{qt5pas_release}
Summary:        Development files for qt5pas

Requires:       qt5-qtbase-devel%{?_isa}
Requires:       qt5-qtx11extras-devel%{?_isa}
Requires:       qt5pas%{?_isa} = %{qt5pas_version}-%{qt5pas_release}

%description -n qt5pas-devel
The qt5pas-devel package contains libraries and header files for
developing applications that use qt5pas.

# Qt5pas end, Qt6pas start
%package -n     qt6pas
Version:        %{qt6pas_version}
Release:        %{qt6pas_release}
Summary:        Qt6 bindings for Pascal

%description -n qt6pas
Qt6 bindings for Pascal from Lazarus.

%package -n     qt6pas-devel
Version:        %{qt6pas_version}
Release:        %{qt6pas_release}
Summary:        Development files for qt5pas

Requires:       qt6-qtbase-devel%{?_isa}
Requires:       qt6pas%{?_isa} = %{qt6pas_version}-%{qt6pas_release}

%description -n qt6pas-devel
The qt6pas-devel package contains libraries and header files for
developing applications that use qt6pas.
# Qt6pas end


# Instruct fpmake to build in parallel
%global fpmakeopt %{?_smp_build_ncpus:FPMAKEOPT='-T %{_smp_build_ncpus}'}

# Preferred compilation options - enable GDB debuginfo in DWARF format, plus some optimisations
%global fpcopt -g -gl -gw -O3


%prep
%autosetup -c -p1


%build
cd lazarus

# Remove the files for building other packages
rm -rf debian
pushd tools
find install -depth -type d ! \( -path "install/linux/*" -o -path "install/linux" -o -path "install" \) -exec rm -rf '{}' \;
popd

# Re-create the Makefiles
export FPCDIR=%{_datadir}/fpcsrc/
fpcmake -Tall
pushd components
fpcmake -Tall
popd

# Compile some basic targets required by everything else
make registration %{fpmakeopt} OPT='%{fpcopt}'

# Compile lazbuild - required to build other targets
make lazbuild %{fpmakeopt} OPT='%{fpcopt}'

# Compile LCL base (Lazarus Component Library) for the "nogui" widgetset
make lcl %{fpmakeopt} OPT='%{fpcopt}' LCL_PLATFORM=nogui

# Compile extra tools
make tools %{fpmakeopt} OPT='%{fpcopt}'

# Compile the LCL base + extra components for GUI widgetsets
for WIDGETSET in gtk2 gtk3 qt qt5 qt6; do
	make lcl basecomponents bigidecomponents %{fpmakeopt} OPT='%{fpcopt}' LCL_PLATFORM="${WIDGETSET}"
done

# Compile the IDE itself
# TODO: Could try building the IDE with multiple widgetsets, as well!
make bigide %{fpmakeopt} OPT='%{fpcopt}' LCL_PLATFORM=gtk2

# Build Qt5Pas
pushd lcl/interfaces/qt5/cbindings/
	%{qmake_qt5}
	%make_build
popd

# Build Qt6Pas
pushd lcl/interfaces/qt6/cbindings/
	%{qmake_qt6}
	%make_build
popd


%install
make -C lazarus install INSTALL_PREFIX=%{buildroot}%{_prefix} _LIB=%{_lib}

# Remove man page for an executable that is not actually installed.
rm %{buildroot}%{_mandir}/man1/svn2revisioninc.1* || true

desktop-file-install \
	--dir %{buildroot}%{_datadir}/applications \
	lazarus/install/%{name}.desktop

install -d %{buildroot}%{_sysconfdir}/lazarus
sed 's#__LAZARUSDIR__#%{_libdir}/%{name}#;s#__FPCSRCDIR__#%{_datadir}/fpcsrc#' \
	lazarus/tools/install/linux/environmentoptions.xml \
	> %{buildroot}%{_sysconfdir}/lazarus/environmentoptions.xml

chmod 755 %{buildroot}%{_libdir}/%{name}/components/lazreport/tools/localize.sh

install -m 755 -d %{buildroot}%{_metainfodir}
install -m 644 %{SOURCE100} %{buildroot}%{_metainfodir}/%{name}.appdata.xml

# -- Install Qt5Pas and Qt6Pas

for QTVER in 5 6; do
	pushd "lazarus/lcl/interfaces/qt${QTVER}/cbindings/"
		%make_install INSTALL_ROOT=%{buildroot}
	popd

	# Since we provide Qt?Pas as a standalone package, remove the .so files bundled in Lazarus dir
	# and replace them with symlinks to the standalone .so.
	for FILEPATH in "%{buildroot}%{_libdir}/%{name}/lcl/interfaces/qt${QTVER}/cbindings/libQt${QTVER}Pas.so"* ; do
		FILENAME="$(basename "${FILEPATH}")"
		ln -sf "%{_libdir}/${FILENAME}" "${FILEPATH}"
	done

	# Cannot be done earlier since "make install" expects the tmp/ directory to be present. Sigh.
	rm -rf "%{buildroot}%{_libdir}/%{name}/lcl/interfaces/qt${QTVER}/cbindings/tmp/"
done


%check
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{name}.appdata.xml


%files
# No files, but we want to build the "lazarus" metapackage


%files doc
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/docs
%{_libdir}/%{name}/examples

%license lazarus/COPYING.GPL.txt

# -- IDE files

%files ide
%{_libdir}/%{name}

# Exclude -docs files
%exclude %{_libdir}/%{name}/docs
%exclude %{_libdir}/%{name}/examples

# Exclude -lcl files
%exclude %{_libdir}/%{name}/components
%exclude %{_libdir}/%{name}/lcl

# Exclude -tools files
%exclude %{_libdir}/%{name}/lazbuild
%exclude %{_libdir}/%{name}/packager
%exclude %{_libdir}/%{name}/tools

# Exclude some files that belong in the ide/ directory
# but are actually required by lazbuild to run properly.
%exclude %{_libdir}/%{name}/ide/packages/ideconfig
%exclude %{_libdir}/%{name}/ide/packages/idedebugger

%{_bindir}/lazarus-ide
%{_bindir}/startlazarus
%{_datadir}/pixmaps/lazarus.png
%{_datadir}/applications/*%{name}.desktop
%{_datadir}/mime/packages/lazarus.xml
%{_datadir}/icons/hicolor/48x48/mimetypes/*
%{_metainfodir}/%{name}.appdata.xml

%doc lazarus/README.md
%license lazarus/COPYING.txt
%license lazarus/COPYING.LGPL.txt
%license lazarus/COPYING.modifiedLGPL.txt
%{_mandir}/man1/lazarus-ide.1*
%{_mandir}/man1/startlazarus.1*

# -- Tools files

%files tools
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/lazbuild
%{_libdir}/%{name}/packager/
%{_libdir}/%{name}/tools/

%dir %{_libdir}/%{name}/ide/
%dir %{_libdir}/%{name}/ide/packages/
%{_libdir}/%{name}/ide/packages/ideconfig
%{_libdir}/%{name}/ide/packages/idedebugger

%{_bindir}/lazbuild
%{_bindir}/lazres
%{_bindir}/lrstolfm
%{_bindir}/updatepofiles

%dir %{_sysconfdir}/lazarus
%config(noreplace) %{_sysconfdir}/lazarus/environmentoptions.xml

%license lazarus/COPYING.GPL.txt
%{_mandir}/man1/lazbuild.1*
%{_mandir}/man1/lazres.1*
%{_mandir}/man1/lrstolfm.1*
%{_mandir}/man1/updatepofiles.1*

# -- LCL files

# Helper macro to reduce repetitions (lcl, basecomponents)
%define lcl_base_files(n:) %{expand:
	%{*} %{_libdir}/%{name}/components/*/lib/*-linux/%{-n*}/
	%{*} %{_libdir}/%{name}/components/*/units/*-linux/%{-n*}/
	%{*} %{_libdir}/%{name}/lcl/interfaces/%{-n*}/
	%{*} %{_libdir}/%{name}/lcl/units/*/%{-n*}/
}

# Some files are not present for nogui (bigidecomponents)
%define lcl_extra_files(n:) %{expand:
	%{*} %{_libdir}/%{name}/components/*/design/lib/*-linux/%{-n*}/
	%{*} %{_libdir}/%{name}/components/*/design/units/*-linux/%{-n*}/
	%{*} %{_libdir}/%{name}/components/*/include/%{-n*}/
	%{*} %{_libdir}/%{name}/components/*/include/intf/%{-n*}/
	%{*} %{_libdir}/%{name}/components/*/lib/*-linux-%{-n*}/
	%{*} %{_libdir}/%{name}/components/*/units/%{-n*}/

	%{*} %{_libdir}/%{name}/components/chmhelp/packages/help/lib/*-linux/%{-n*}/
	%{*} %{_libdir}/%{name}/components/chmhelp/packages/idehelp/lib/*-linux/%{-n*}/
	%{*} %{_libdir}/%{name}/components/fpcunit/ide/lib/*-linux/%{-n*}/
	%{*} %{_libdir}/%{name}/components/jcf2/IdePlugin/lazarus/lib/*-linux/%{-n*}/
}

# -- LCL base

%files lcl
%license lazarus/COPYING.txt
%license lazarus/COPYING.LGPL.txt
%license lazarus/COPYING.modifiedLGPL.txt
%license %{_libdir}/%{name}/lcl/interfaces/customdrawn/android/ApacheLicense2.0.txt

%dir %{_libdir}/%{name}
%{_libdir}/%{name}/components/
%{_libdir}/%{name}/lcl/
%lcl_base_files -n nogui %exclude
%lcl_base_files  -n gtk2 %exclude
%lcl_extra_files -n gtk2 %exclude
%lcl_base_files  -n gtk3 %exclude
%lcl_extra_files -n gtk3 %exclude
%lcl_base_files  -n qt %exclude
%lcl_extra_files -n qt %exclude
%lcl_base_files  -n qt5 %exclude
%lcl_extra_files -n qt5 %exclude
%lcl_base_files  -n qt6 %exclude
%lcl_extra_files -n qt6 %exclude

# -- LCL widgetsets

%files lcl-nogui
%lcl_base_files -n nogui

%files lcl-gtk2
%lcl_base_files -n gtk2
%lcl_extra_files -n gtk2

%files lcl-gtk3
%lcl_base_files -n gtk3
%lcl_extra_files -n gtk3

%files lcl-qt
%lcl_base_files -n qt
%lcl_extra_files -n qt

%files lcl-qt5
%lcl_base_files -n qt5
%lcl_extra_files -n qt5

%files lcl-qt6
%lcl_base_files -n qt6
%lcl_extra_files -n qt6

# -- Qt5pas

%files -n qt5pas
%license lazarus/lcl/interfaces/qt5/cbindings/COPYING.TXT
%doc lazarus/lcl/interfaces/qt5/cbindings/README.TXT
%{_libdir}/libQt5Pas.so.*

%files -n qt5pas-devel
%{_libdir}/libQt5Pas.so

# -- Qt6pas

%files -n qt6pas
%license lazarus/lcl/interfaces/qt6/cbindings/COPYING.TXT
%doc lazarus/lcl/interfaces/qt6/cbindings/README.TXT
%{_libdir}/libQt6Pas.so.*

%files -n qt6pas-devel
%{_libdir}/libQt6Pas.so


%changelog
* Sun Mar 17 2024 Artur Frenszek-Iwicki <fedora@svgames.pl> - 3.2-1
- Update to v3.2

* Wed Feb 07 2024 Artur Frenszek-Iwicki <fedora@svgames.pl> - 3.0-1
- Update to v3.0
- Add qt6pas, qt6pas-devel and lazarus-lcl-qt6 packages
- Drop Patch2 (GTK3 fixes - fixed upstream)
- Drop workaround for building Qt on non-x86 platforms (fixed upstream)

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 04 2023 Artur Frenszek-Iwicki <fedora@svgames.pl> - 2.2.6-4
- Add missing dependencies to lcl-qt and lcl-qt5 packages

* Sat Jul 01 2023 Artur Frenszek-Iwicki <fedora@svgames.pl> - 2.2.6-3
- Move /etc/lazarus from lazarus-ide to lazarus-tools (files required by lazbuild)
- Edit dependencies - make the lazarus metapackage strongly require the default set of sub-packages

* Thu Jun 08 2023 Artur Frenszek-Iwicki <fedora@svgames.pl> - 2.2.6-2
- Put the IDE, LCL and documentation in separate packages
- Move lazbuild and other tools to a separate sub-package
- Apart from the default GTK2, build the LCL with GTK3, Qt and Qt5
- Use multiple jobs during the build
- Add Obsoletes: for smooth upgrade from F37/F38

* Wed Mar 08 2023 Artur Frenszek-Iwicki <fedora@svgames.pl> - 2.2.6-1
- Update to v2.2.6
- Add a patch to fix build errors when using the GTK3 widgetset
- Convert License tag to SPDX
- Drop Patch1 (fix components explicitly requesting STABS debuginfo - fixed upstream)

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Sep 27 2022 Artur Frenszek-Iwicki <fedora@svgames.pl> - 2.2.4-1
- Update to v2.2.4

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu May 19 2022 Artur Frenszek-Iwicki <fedora@svgames.pl> - 2.2.2-1
- Update to v2.2.2

* Mon Feb 07 2022 Artur Frenszek-Iwicki <fedora@svgames.pl> - 2.2.0-1
- Update to v2.2.0
- Drop Patch1 - disable PascalScript on ppc64le (compiles successfully now)
- Add Patch1 - use DWARF debuginfo instead of stabs

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jun 03 2021 Artur Frenszek-Iwicki <fedora@svgames.pl> - 2.0.12-2
- Rebuild for FPC 3.2.2

* Fri Apr 30 2021 Artur Frenszek-Iwicki <fedora@svgames.pl> - 2.0.12-1
- Update to 2.0.12
- Use baserelease macro to fix the rpmdev-bumspec issues

* Fri Feb 05 2021 Artur Frenszek-Iwicki <fedora@svgames.pl> - 2.0.10-7
- Fix FailsToInstall due to .1 added to qt5pas release number

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.10-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Jan 16 2021 Artur Frenszek-Iwicki <fedora@svgames.pl> - 2.0.10-5
- Add an appdata file

* Mon Aug 24 2020 Artur Iwicki <fedora@svgames.pl> - 2.0.10-4
- Make the package explicitly require "make"

* Mon Aug 03 2020 Artur Iwicki <fedora@svgames.pl> - 2.0.10-3
- Fix FailsToInstall due to .1 added to qt5pas release number

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat Jul 11 2020 Artur Iwicki <fedora@svgames.pl> - 2.0.10-1
- Update to v2.0.10

* Sun Jun 21 2020 Artur Iwicki <fedora@svgames.pl> - 2.0.8-4
- Rebuilt for FPC 3.2.0

* Wed Jun 03 2020 Artur Iwicki <fedora@svgames.pl> - 2.0.8-3
- Rebuilt for FPC 3.2.0-beta-r45533

* Mon May 04 2020 Artur Iwicki <fedora@svgames.pl> - 2.0.8-2
- Rebuilt for FPC 3.2.0-beta-r45235

* Thu Apr 16 2020 Artur Iwicki <fedora@svgames.pl> - 2.0.8-1
- Update to upstream release v.2.0.8
- Drop Patch2 ("illegal qualifier" compile-time error) - fixed upstream

* Sun Apr 12 2020 Artur Iwicki <fedora@svgames.pl> - 2.0.6-9
- Rebuilt for FPC 3.2.0-beta-r44680

* Sat Mar 28 2020 Artur Iwicki <fedora@svgames.pl> - 2.0.6-8
- Rebuilt for FPC 3.2.0-beta-r44375

* Mon Mar 16 2020 Artur Iwicki <fedora@svgames.pl> - 2.0.6-7
- Rebuilt for FPC 3.2.0-beta-r44301

* Mon Feb 24 2020 Artur Iwicki <fedora@svgames.pl> - 2.0.6-6
- Rebuilt for FPC 3.2.0-beta-r44232

* Wed Feb 12 2020 Artur Iwicki <fedora@svgames.pl> - 2.0.6-5
- Rebuilt for FPC 3.2.0-beta-r44160

* Sat Feb 08 2020 Artur Iwicki <fedora@svgames.pl> - 2.0.6-4
- Fix build failures in Rawhide
- Rebuilt for FPC 3.2.0-beta-r44109

* Wed Jan 29 2020 Artur Iwicki <fedora@svgames.pl> - 2.0.6-3
- Disable PascalScript on ppc64le

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Nov 01 2019 Artur Iwicki <fedora@svgames.pl> - 2.0.6-1
- Update to upstream release v.2.0.6

* Sun Oct 20 2019 Artur Iwicki <fedora@svgames.pl> - 2.0.4-4
- Make Lazarus depend on qt5pas-devel instead of bundling the .so files
- Do not install the tmp/ folder left over after building qt5pas

* Fri Oct 11 2019 Artur Iwicki <fedora@svgames.pl> - 2.0.4-3
- This time really fix the qt5pas and qt5pas-devel nvr mismatch

* Wed Aug 14 2019 Artur Iwicki <fedora@svgames.pl> - 2.0.4-2
- Fix qt5pas and qt5pas-devel nvr mismatch

* Tue Aug 13 2019 Artur Iwicki <fedora@svgames.pl> - 2.0.4-1
- Update to upstream version 2.0.4

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Apr 16 2019 Artur Iwicki <fedora@svgames.pl> - 2.0.2-1
- Update to upstream version 2.0.2
- Drop .1 from qt5pas release numbers

* Fri Feb 08 2019 Artur Iwicki <fedora@svgames.pl> - 2.0.0-1
- Update to upstream version 2.0.0
- Drop the .desktop file patch (issues fixed upstream)
- Drop the "Disable PascalScript on PowerPC64" patch (we no longer ship ppc64 fpc/lazarus)

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Nov 17 2018 Artur Iwicki <fedora@svgames.pl> - 1.8.4-2
- Use Lazarus version number to auto-calculate the qt5pas release number
  This should prevent build failures in koji due to duplicate qt5pas version-release tags.

* Sat Aug 18 2018 Artur Iwicki <fedora@svgames.pl> - 1.8.4-1
- Update to new upstream version

* Tue Aug 07 2018 Artur Iwicki <fedora@svgames.pl> - 1.8.2-3
- Add the Qt5pas package (pull request #3)
- Remove the Group: tag (no longer used in Fedora)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Mar 5 2018 Joost van der Sluis <joost@cnoc.nl> - 1.8.2-1
- Update to upstream version 1.8.2

* Sat Feb 24 2018 Artur Iwicki <fedora@svgames.pl> - 1.8.0-1
- Update to upstream version 1.8.0
- Remove obsolete scriplets (icon cache update)
- Use the %license tag instead of %doc for licence files

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Mar 22 2017 Joost van der Sluis <joost@cnoc.nl> - 1.6.4-1
- Updated to version 1.6.4

* Wed Feb 8 2017 Joost van der Sluis <joost@cnoc.nl> - 1.6.2-3
- Disable PascalScript on Powerpc64

* Sat Feb 04 2017 Björn Esser <besser82@fedoraproject.org> - 1.6.2-2
- Rebuilt for changes in 'ExclusiveArch: %%{fpc_arches}'

* Sun Jan 29 2017 Joost van der Sluis <joost@cnoc.nl> - 1.6.2-1
- Compile exclusively on platforms supported by fpc (rhbz#1247925)

* Thu Jan 26 2017 Joost van der Sluis <joost@cnoc.nl> - 1.6.2-0
- Updated to version 1.6.2

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.6-0.2.RC1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 11 2016 Joost van der Sluis <joost@cnoc.nl> - 1.6-0.1.RC1
- Updated to version 1.6RC1

* Sun Dec 20 2015 Joost van der Sluis <joost@cnoc.nl> - 1.4.4-1
- Updated to version 1.4.4

* Mon Jul 20 2015 Joost van der Sluis <joost@cnoc.nl> - 1.4.2-1
- Updated to version 1.4.2

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Apr 23 2015 Joost van der Sluis <joost@cnoc.nl> - 1.4-1
- Updated to version 1.4

* Mon Mar 9 2015 Joost van der Sluis <joost@cnoc.nl> - 1.4-0.1.RC2
- Updated to version 1.4RC2
- Fixed invalid dates in changelog

* Mon Aug 18 2014 Rex Dieter <rdieter@fedoraproject.org> 1.2-4
- update scriptlets

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Mar 31 2014 Joost van der Sluis <joost@cnoc.nl> - 1.2-1
- Updated to version 1.2

* Fri Mar 28 2014 Joost van der Sluis <joost@cnoc.nl> - 1.0.14-1
- Updated to version 1.0.14

* Mon Aug 12 2013 Joost van der Sluis <joost@cnoc.nl> - 1.0.8-4
- Rebuilt for Free Pascal with arm-support

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 1.0.8-2
- Perl 5.18 rebuild

* Thu Apr 25 2013 Joost van der Sluis <joost@cnoc.nl> - 1.0.8-1
- Updated to version 1.0.8

* Wed Apr 24 2013 Jon Ciesla <limburgher@gmail.com> - 1.0.4-3
- Drop desktop vendor tag.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.30.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Apr 18 2012 Joost van der Sluis <joost@cnoc.nl> - 0.9.30.4-1
- Updated to version 0.9.30.4
- Use default fonts, editoroptions.xml file removed

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.30-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Apr 27 2011 Joost van der Sluis <joost@cnoc.nl> - 0.9.30-1
- Updated to version 0.9.30
- Remove the obsolete .spec BuildRoot tag.
- Do not install manfiles for executables which are not in the path

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.28.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Dec 05 2010 Lubomir Rintel <lkundrak@v3.sk> - 0.9.28.2-2
- Fix LazarusVersion substitution in configuration
- Do not compress manpages in %%build, RPM does this for us

* Wed May 19 2010 Joost van der Sluis <joost@cnoc.nl> - 0.9.28.2-1
- Updated to version 0.9.28.2

* Fri Oct 16 2009 Joost van der Sluis <rel-eng@lists.fedoraproject.org> - 0.9.28-1
- Updated to version 0.9.28

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.26.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jun 18 2009 Dan Horak <dan[at]danny.cz> 0.9.26.2-3
- Exclude s390/s390x architectures, FPC doesn't exist there

* Wed Apr 1 2009 Joost van der Sluis <joost@cnoc.nl> 0.9.26.2-2
 - Adapted Makefile patch for version 0.9.26.2

* Wed Apr 1 2009 Joost van der Sluis <joost@cnoc.nl> 0.9.26.2-1
 - Updated to version 0.9.26.2

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.26-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Dec  4 2008 Michael Schwendt <mschwendt@fedoraproject.org> 0.9.26-3
- Include /etc/lazarus directory.

* Wed Oct 29 2008 Lubomir Rintel <lkundrak@v3.sk> 0.9.26-2
- Fix path to the source tree

* Thu Oct 23 2008 Joost van der Sluis <joost@cnoc.nl> 0.9.26-1
- Updated to version 0.9.26
- Removed scripts which are vulnerable to symlink-attacks (bug 460642)
- Build bigide instead of the standard ide
- Build ideintf and the registration for gtk2
- Install the manfiles
- Install the mime-types
- Install the global .xml configuration files

* Wed Jun 18 2008 Joost van der Sluis <joost@cnoc.nl> 0.9.24-4
- removed the trailing slash from the FPCDIR export in the build section

* Thu Apr 24 2008 Joost van der Sluis <joost@cnoc.nl> 0.9.24-3
- Remove executable-bit in install-section, instead of the files section
- Enabled debug-package on x86_64

* Fri Feb 01 2008 Joost van der Sluis <joost@cnoc.nl> 0.9.24-2
- Changed license-tag according to the official license tags of Fedora
- Removed some more Debian-specific files
- Made two scripts executable
- Improved fedora-lazarus.desktop

* Mon Nov 26 2007 Joost van der Sluis <joost@cnoc.nl> 0.9.24-1
- Removed files specific for debian
- Updated to Lazarus v 0.9.24
- Changed desktop-file categories
- Disabled the debug-package for x86_64 again, see bug 337051
- If the debuginfo-packages is disabled, strip the executables manually
- Require fpc version 2.2.0
- Added -q to setup-macro
- Added OPT='-gl' option in build-section, to make sure that the debuginfo is generated by the compiler
- Removed explicit creation of {buildroot}{_mandir}/man1 and {buildroot}{_datadir}/applications
- Lazarus executable is renamed to lazarus-ide (changed upstream)

* Thu Jan 4 2007 Joost van der Sluis <joost@cnoc.nl> 0.9.20-2
- Added fpc-src as build-dependency to fix problem with fpcmake

* Tue Jan 2 2007 Joost van der Sluis <joost@cnoc.nl> 0.9.20-1
- Version 0.9.20

* Wed Oct 4 2006 Joost van der Sluis <joost@cnoc.nl> 0.9.18-2
- Use the makefile for installing

* Wed Sep 20 2006 Joost van der Sluis <joost@cnoc.nl> 0.9.18-1
- Updated to version 0.9.18.
- Removed obsolete copying of documentation
- Removed double requirements
- Removed part to remove debuginfo package

* Thu Jun 1 2006 Joost van der Sluis <joost@cnoc.nl> 0.9.16-1
- Updated to version 0.9.16.

* Thu May 25 2006 Joost van der Sluis <joost@cnoc.nl> 0.9.14-5
- Added /usr/bin/startlazarus for packaging
- Removed strip in build-section
- added gtk2-devel buildrequirement

* Tue May 23 2006 Joost van der Sluis <joost@cnoc.nl> 0.9.14-4
- Only build the basic IDE, to remove dependencies on things which are buggy in fpc 2.0.2

* Thu May 4 2006 Joost van der Sluis <joost@cnoc.nl> 0.9.14-3
- Added the ability to create gtk2-applications

* Thu May 4 2006 Joost van der Sluis <joost@cnoc.nl> 0.9.14-2
- Updated to version 0.9.14-1.
- Changed the Source0 download url from prdownloads to
  downloads.sourceforge.net

* Mon Apr 10 2006 Joost van der Sluis <joost@cnoc.nl> 0.9.14-1
- Updated to version 0.9.14.

* Tue Mar 28 2006 Joost van der Sluis <joost@cnoc.nl> 0.9.12-1
- Initial build.

