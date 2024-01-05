%global glibcsrcdir glibc-2.37
%global glibcversion 2.37
%global _default_patch_fuzz 2
# Pre-release tarballs are pulled in from git using a command that is
# effectively:
#
# git archive HEAD --format=tar --prefix=$(git describe --match 'glibc-*')/ \
#	> $(git describe --match 'glibc-*').tar
# gzip -9 $(git describe --match 'glibc-*').tar
#
# glibc_release_url is only defined when we have a release tarball.
# Conversly, glibc_autorequires is set for development snapshots, where
# dependencies based on symbol versions are inaccurate.
%{lua: if string.match(rpm.expand("%glibcsrcdir"), "^glibc%-[0-9.]+$") then
    rpm.define("glibc_release_url https://ftp.gnu.org/gnu/glibc/")
  end
  local major, minor = string.match(rpm.expand("%glibcversion"),
                                    "^([0-9]+)%.([0-9]+)%.9000$")
  if major and minor then
    rpm.define("glibc_autorequires 1")
    -- The minor version in a .9000 development version lags the actual
    -- symbol version by one.
    local symver = "GLIBC_" .. major .. "." .. (minor + 1)
    rpm.define("glibc_autorequires_symver " .. symver)
  else
    rpm.define("glibc_autorequires 0")
  end}
##############################################################################
# We support the following options:
# --with/--without,
# * testsuite - Running the testsuite.
# * benchtests - Running and building benchmark subpackage.
# * bootstrap - Bootstrapping the package.
# * werror - Build with -Werror
# * docs - Build with documentation and the required dependencies.
# * valgrind - Run smoke tests with valgrind to verify dynamic loader.
#
# You must always run the testsuite for production builds.
# Default: Always run the testsuite.
%bcond_without testsuite
# Default: Always build the benchtests.
%bcond_without benchtests
# Default: Not bootstrapping.
%bcond_with bootstrap
# Default: Enable using -Werror
%bcond_without werror
# Default: Always build documentation.
%bcond_without docs

# Default: Always run valgrind tests if there is architecture support.
%ifarch %{valgrind_arches}
%bcond_without valgrind
%else
%bcond_with valgrind
%endif
# Restrict %%{valgrind_arches} further in case there are problems with
# the smoke test.
%if %{with valgrind}
%ifarch ppc64 ppc64p7
# The valgrind smoke test does not work on ppc64, ppc64p7 (bug 1273103).
%undefine with_valgrind
%endif
%endif

%if %{with bootstrap}
# Disable benchtests, -Werror, docs, and valgrind if we're bootstrapping
%undefine with_benchtests
%undefine with_werror
%undefine with_docs
%undefine with_valgrind
%endif

# The annobin annotations cause binutils to produce broken ARM EABI
# unwinding information.  Symptom is a hang/test failure for
# malloc/tst-malloc-stats-cancellation.  See
# <https://bugzilla.redhat.com/show_bug.cgi?id=1951492>.
%ifarch armv7hl
%undefine _annotated_build
%endif

# We do our own build flags management.  In particular, see
# rpm_inherit_flags below.
%undefine _auto_set_build_flags

##############################################################################
# Any architecture/kernel combination that supports running 32-bit and 64-bit
# code in userspace is considered a biarch arch.
%global biarcharches %{ix86} x86_64 s390 s390x

# Avoid generating a glibc-headers package on architectures which are
# not biarch.
%ifarch %{biarcharches}
%global need_headers_package 1
%if 0%{?rhel} > 0
%global headers_package_name glibc-headers
%else
%ifarch %{ix86} x86_64
%global headers_package_name glibc-headers-x86
%endif
%ifarch s390 s390x
%global headers_package_name glibc-headers-s390
%endif
%dnl !rhel
%endif
%else
%global need_headers_package 0
%dnl !biarcharches
%endif

##############################################################################
# Utility functions for pre/post scripts.  Stick them at the beginning of
# any lua %pre, %post, %postun, etc. sections to have them expand into
# those scripts.  It only works in lua sections and not anywhere else.
%global glibc_post_funcs() \
-- We use lua posix.exec because there may be no shell that we can \
-- run during glibc upgrade.  We used to implement much of %%post as a \
-- C program, but from an overall maintenance perspective the lua in \
-- the spec file was simpler and safer given the operations required. \
-- All lua code will be ignored by rpm-ostree; see: \
-- https://github.com/projectatomic/rpm-ostree/pull/1869 \
-- If we add new lua actions to the %%post code we should coordinate \
-- with rpm-ostree and ensure that their glibc install is functional. \
function post_exec (program, ...) \
  local pid = posix.fork () \
  if pid == 0 then \
    posix.exec (program, ...) \
    assert (nil) \
  elseif pid > 0 then \
    posix.wait (pid) \
  end \
end \
\
function update_gconv_modules_cache () \
  local iconv_dir = "%{_libdir}/gconv" \
  local iconv_cache = iconv_dir .. "/gconv-modules.cache" \
  local iconv_modules = iconv_dir .. "/gconv-modules" \
  if (posix.utime (iconv_modules) == 0) then \
    if (posix.utime (iconv_cache) == 0) then \
      post_exec ("%{_prefix}/sbin/iconvconfig", \
		 "-o", iconv_cache, \
		 "--nostdlib", \
		 iconv_dir) \
    else \
      io.stdout:write ("Error: Missing " .. iconv_cache .. " file.\n") \
    end \
  end \
end \
%{nil}

##############################################################################
# %%package glibc - The GNU C Library (glibc) core package.
##############################################################################
Summary: The GNU libc libraries
Name: glibc
Version: %{glibcversion}
Release: 2%{?dist}

# In general, GPLv2+ is used by programs, LGPLv2+ is used for
# libraries.
#
# LGPLv2+ with exceptions is used for things that are linked directly
# into dynamically linked programs and shared libraries (e.g. crt
# files, lib*_nonshared.a).  Historically, this exception also applies
# to parts of libio.
#
# GPLv2+ with exceptions is used for parts of the Arm unwinder.
#
# GFDL is used for the documentation.
#
# Some other licenses are used in various places (BSD, Inner-Net,
# ISC, Public Domain).
#
# HSRL and FSFAP are only used in test cases, which currently do not
# ship in binary RPMs, so they are not listed here.  MIT is used for
# scripts/install-sh, which does not ship, either.
#
# GPLv3+ is used by manual/texinfo.tex, which we do not use.
#
# LGPLv3+ is used by some Hurd code, which we do not build.
#
# LGPLv2 is used in one place (time/timespec_get.c, by mistake), but
# it is not actually compiled, so it does not matter for libraries.
License: LGPLv2+ and LGPLv2+ with exceptions and GPLv2+ and GPLv2+ with exceptions and BSD and Inner-Net and ISC and Public Domain and GFDL

URL: http://www.gnu.org/software/glibc/
Source0: %{?glibc_release_url}%{glibcsrcdir}.tar.xz
Source1: bench.mk
Source2: glibc-bench-compare
Source3: glibc.req.in
Source4: glibc.attr
Source10: wrap-find-debuginfo.sh
Source11: parse-SUPPORTED.py
# Include in the source RPM for reference.
Source12: ChangeLog.old

######################################################################
# Activate the wrapper script for debuginfo generation, by rewriting
# the definition of __debug_install_post.
%{lua:
local wrapper = rpm.expand("%{SOURCE10}")
local ldso = rpm.expand("%{glibc_sysroot}/%{_lib}/ld-%{VERSION}.so")
local original = rpm.expand("%{macrobody:__debug_install_post}")
-- Strip leading newline.  It confuses the macro redefinition.
-- Avoid embedded newlines that confuse the macro definition.
original = original:match("^%s*(.-)%s*$"):gsub("\\\n", "")
rpm.define("__debug_install_post bash " .. wrapper
  .. " " .. ldso .. " " .. original)
}

# The wrapper script relies on the fact that debugedit does not change
# build IDs.
%global _no_recompute_build_ids 1
%undefine _unique_build_ids

##############################################################################
# Patches:
# - See each individual patch file for origin and upstream status.
# - For new patches follow template.patch format.
##############################################################################
Patch4: glibc-fedora-linux-tcsetattr.patch
Patch8: glibc-fedora-manual-dircategory.patch
Patch9: glibc-rh827510.patch
Patch13: glibc-fedora-localedata-rh61908.patch
Patch17: glibc-cs-path.patch
Patch23: glibc-python3.patch
Patch24: glibc-printf-grouping-swbz30068.patch

# Needed for Rogue Company EAC to work
Patch1014: 0001-Revert-elf-Clean-up-GLIBC_PRIVATE-exports-of-interna.patch
Patch1015: 0002-Revert-Install-shared-objects-under-their-ABI-names.patch
Patch1016: 0003-Revert-elf-Generalize-name-based-DSO-recognition-in-.patch
Patch1017: 0004-Revert-Makerules-Remove-lib-version.patch
Patch1018: 0005-Revert-nptl_db-Install-libthread_db-under-a-regular-.patch

# re-enable DT_HASH
Patch1019: 0006-re-enable-DT_HASH.patch

# disable clone3
Patch1020: disable-clone3.patch

##############################################################################
# Continued list of core "glibc" package information:
##############################################################################
Obsoletes: glibc-profile < 2.4
Obsoletes: nscd < 2.35
Provides: ldconfig

# The dynamic linker supports DT_GNU_HASH
Provides: rtld(GNU_HASH)

# We need libgcc for cancellation support in POSIX threads.
Requires: libgcc%{_isa}

Requires: glibc-common = %{version}-%{release}

# Various components (regex, glob) have been imported from gnulib.
Provides: bundled(gnulib)

Requires(pre): basesystem
Requires: basesystem

%ifarch %{ix86}
# Automatically install the 32-bit variant if the 64-bit variant has
# been installed.  This covers the case when glibc.i686 is installed
# after nss_*.x86_64.  (See below for the other ordering.)
Recommends: (nss_db(x86-32) if nss_db(x86-64))
Recommends: (nss_hesiod(x86-32) if nss_hesiod(x86-64))
%endif

# This is for building auxiliary programs like memusage
# For initial glibc bootstraps it can be commented out
%if %{without bootstrap}
BuildRequires: gd-devel libpng-devel zlib-devel
%endif
%if %{with docs}
%endif
%if %{without bootstrap}
BuildRequires: libselinux-devel >= 1.33.4-3
%endif
BuildRequires: audit-libs-devel >= 1.1.3, sed >= 3.95, libcap-devel, gettext
# We need procps-ng (/bin/ps), util-linux (/bin/kill), and gawk (/bin/awk),
# but it is more flexible to require the actual programs and let rpm infer
# the packages. However, until bug 1259054 is widely fixed we avoid the
# following:
# BuildRequires: /bin/ps, /bin/kill, /bin/awk
# And use instead (which should be reverted some time in the future):
BuildRequires: procps-ng, util-linux, gawk
BuildRequires: systemtap-sdt-devel

%if %{with valgrind}
# Require valgrind for smoke testing the dynamic loader to make sure we
# have not broken valgrind.
BuildRequires: valgrind
%endif

# We use python for the microbenchmarks and locale data regeneration
# from unicode sources (carried out manually). We choose python3
# explicitly because it supports both use cases.  On some
# distributions, python3 does not actually install /usr/bin/python3,
# so we also depend on python3-devel.
BuildRequires: python3 python3-devel

# This GCC version is needed for -fstack-clash-protection support.
BuildRequires: gcc >= 7.2.1-6
%global enablekernel 3.2
Conflicts: kernel < %{enablekernel}
%global target %{_target_cpu}-redhat-linux
%ifarch %{arm}
%global target %{_target_cpu}-redhat-linuxeabi
%endif
%ifarch ppc64le
%global target ppc64le-redhat-linux
%endif

# GNU make 4.0 introduced the -O option.
BuildRequires: make >= 4.0

# The intl subsystem generates a parser using bison.
BuildRequires: bison >= 2.7

# binutils 2.30-17 is needed for --generate-missing-build-notes.
BuildRequires: binutils >= 2.30-17

# Earlier releases have broken support for IRELATIVE relocations
Conflicts: prelink < 0.4.2

%if %{without bootstrap}
%if %{with testsuite}
# The testsuite builds static C++ binaries that require a C++ compiler,
# static C++ runtime from libstdc++-static, and lastly static glibc.
BuildRequires: gcc-c++
BuildRequires: libstdc++-static
# A configure check tests for the ability to create static C++ binaries
# before glibc is built and therefore we need a glibc-static for that
# check to pass even if we aren't going to use any of those objects to
# build the tests.
BuildRequires: glibc-static

# libidn2 (but not libidn2-devel) is needed for testing AI_IDN/NI_IDN.
BuildRequires: libidn2

# The testsuite runs mtrace, which is a perl script
BuildRequires: perl-interpreter
%endif
%endif

# Filter out all GLIBC_PRIVATE symbols since they are internal to
# the package and should not be examined by any other tool.
%global __filter_GLIBC_PRIVATE 1
%global __provides_exclude ^libc_malloc_debug\\.so.*$

# For language packs we have glibc require a virtual dependency
# "glibc-langpack" wich gives us at least one installed langpack.
# If no langpack providing 'glibc-langpack' was installed you'd
# get language-neutral support e.g. C, POSIX, and C.UTF-8 locales.
# In the past we used to install the glibc-all-langpacks by default
# but we no longer do this to minimize container and VM sizes.
# Today you must actively use the language packs infrastructure to
# install language support.
Requires: glibc-langpack = %{version}-%{release}
Suggests: glibc-minimal-langpack = %{version}-%{release}

# Suggest extra gconv modules so that they are installed by default but can be
# removed if needed to build a minimal OS image.
Recommends: glibc-gconv-extra%{_isa} = %{version}-%{release}
# Use redhat-rpm-config as a marker for a buildroot configuration, and
# unconditionally pull in glibc-gconv-extra in that case.
Requires: (glibc-gconv-extra%{_isa} = %{version}-%{release} if redhat-rpm-config)

%description
The glibc package contains standard libraries which are used by
multiple programs on the system. In order to save disk space and
memory, as well as to make upgrading easier, common system code is
kept in one place and shared between programs. This particular package
contains the most important sets of shared libraries: the standard C
library and the standard math library. Without these two libraries, a
Linux system will not function.

######################################################################
# libnsl subpackage
######################################################################

%package -n libnsl
Summary: Legacy support library for NIS
Requires: %{name}%{_isa} = %{version}-%{release}

%description -n libnsl
This package provides the legacy version of libnsl library, for
accessing NIS services.

This library is provided for backwards compatibility only;
applications should use libnsl2 instead to gain IPv6 support.

##############################################################################
# glibc "devel" sub-package
##############################################################################
%package devel
Summary: Object files for development using standard C libraries.
Requires: %{name} = %{version}-%{release}
Requires: libxcrypt-devel%{_isa} >= 4.0.0
Requires: kernel-headers >= 3.2
BuildRequires: kernel-headers >= 3.2
%if %{need_headers_package}
Requires: %{headers_package_name} = %{version}-%{release}
%endif
%if !(0%{?rhel} > 0 && %{need_headers_package})
# For backwards compatibility, when the glibc-headers package existed.
Provides: glibc-headers = %{version}-%{release}
Provides: glibc-headers(%{_target_cpu})
Obsoletes: glibc-headers < %{version}-%{release}
%endif

%description devel
The glibc-devel package contains the object files necessary
for developing programs which use the standard C libraries (which are
used by nearly all programs).  If you are developing programs which
will use the standard C libraries, your system needs to have these
standard object files available in order to create the
executables.

Install glibc-devel if you are going to develop programs which will
use the standard C libraries.

##############################################################################
# glibc "doc" sub-package
##############################################################################
%if %{with docs}
%package doc
Summary: Documentation for GNU libc
BuildArch: noarch
Requires: %{name} = %{version}-%{release}

# Removing texinfo will cause check-safety.sh test to fail because it seems to
# trigger documentation generation based on dependencies.  We need to fix this
# upstream in some way that doesn't depend on generating docs to validate the
# texinfo.  I expect it's simply the wrong dependency for that target.
BuildRequires: texinfo >= 5.0

%description doc
The glibc-doc package contains The GNU C Library Reference Manual in info
format.  Additional package documentation is also provided.
%endif

##############################################################################
# glibc "static" sub-package
##############################################################################
%package static
Summary: C library static libraries for -static linking.
Requires: %{name}-devel = %{version}-%{release}
Requires: libxcrypt-static%{?_isa} >= 4.0.0

%description static
The glibc-static package contains the C library static libraries
for -static linking.  You don't need these, unless you link statically,
which is highly discouraged.

##############################################################################
# glibc "headers" sub-package
# - The headers package includes all common headers that are shared amongst
#   the multilib builds. It avoids file conflicts between the architecture-
#   specific glibc-devel variants.
#   Files like gnu/stubs.h which have gnu/stubs-32.h (i686) and gnu/stubs-64.h
#   are included in glibc-headers, but the -32 and -64 files are in their
#   respective i686 and x86_64 devel packages.
##############################################################################
%if %{need_headers_package}
%package -n %{headers_package_name}
Summary: Additional internal header files for glibc-devel.
Requires: %{name} = %{version}-%{release}
%if 0%{?rhel} > 0
Provides: %{name}-headers(%{_target_cpu})
Obsoletes: glibc-headers-x86 < %{version}-%{release}
Obsoletes: glibc-headers-s390 < %{version}-%{release}
%else
BuildArch: noarch
%endif

%description -n %{headers_package_name}
The %{headers_package_name} package contains the architecture-specific
header files which cannot be included in glibc-devel package.
%endif

##############################################################################
# glibc "common" sub-package
##############################################################################
%package common
Summary: Common binaries and locale data for glibc
Requires: %{name} = %{version}-%{release}
Requires: tzdata >= 2003a

%description common
The glibc-common package includes common binaries for the GNU libc
libraries, as well as national language (locale) support.

######################################################################
# File triggers to do ldconfig calls automatically (see rhbz#1380878)
######################################################################

# File triggers for when libraries are added or removed in standard
# paths.
%transfiletriggerin common -P 2000000 -- /lib /usr/lib /lib64 /usr/lib64
/sbin/ldconfig
%end

%transfiletriggerpostun common -P 2000000 -- /lib /usr/lib /lib64 /usr/lib64
/sbin/ldconfig
%end

# We need to run ldconfig manually because __brp_ldconfig assumes that
# glibc itself is always installed in $RPM_BUILD_ROOT, but with sysroots
# we may be installed into a subdirectory of that path.  Therefore we
# unset __brp_ldconfig and run ldconfig by hand with the sysroots path
# passed to -r.
%undefine __brp_ldconfig

######################################################################

%package locale-source
Summary: The sources for the locales
Requires: %{name} = %{version}-%{release}
Requires: %{name}-common = %{version}-%{release}

%description locale-source
The sources for all locales provided in the language packs.
If you are building custom locales you will most likely use
these sources as the basis for your new locale.

# We define a global regular expression to capture all of the locale
# sources. We use it later when constructing the various packages.
%global locale_rx eo syr *_*

%{lua:
-- To make lua-mode happy: '

-- List of supported locales.  This is used to generate the langpack
-- subpackages below.  This table needs adjustments if the set of
-- glibc locales changes.  "code" is the glibc code for the language
-- (before the "_".  "name" is the English translation of the language
-- name (for use in subpackage descriptions).  "regions" is a table of
-- variant specifiers (after the "_", excluding "@" and "."
-- variants/charset specifiers).  The table must be sorted by the code
-- field, and the regions table must be sorted as well.
--
-- English translations of language names can be obtained using (for
-- the "aa" language in this example):
--
-- python3 -c 'import langtable; print(langtable.language_name("aa", languageIdQuery="en"))'

local locales =  {
  { code="aa", name="Afar", regions={ "DJ", "ER", "ET" } },
  { code="af", name="Afrikaans", regions={ "ZA" } },
  { code="agr", name="Aguaruna", regions={ "PE" } },
  { code="ak", name="Akan", regions={ "GH" } },
  { code="am", name="Amharic", regions={ "ET" } },
  { code="an", name="Aragonese", regions={ "ES" } },
  { code="anp", name="Angika", regions={ "IN" } },
  {
    code="ar",
    name="Arabic",
    regions={
      "AE",
      "BH",
      "DZ",
      "EG",
      "IN",
      "IQ",
      "JO",
      "KW",
      "LB",
      "LY",
      "MA",
      "OM",
      "QA",
      "SA",
      "SD",
      "SS",
      "SY",
      "TN",
      "YE" 
    } 
  },
  { code="as", name="Assamese", regions={ "IN" } },
  { code="ast", name="Asturian", regions={ "ES" } },
  { code="ayc", name="Southern Aymara", regions={ "PE" } },
  { code="az", name="Azerbaijani", regions={ "AZ", "IR" } },
  { code="be", name="Belarusian", regions={ "BY" } },
  { code="bem", name="Bemba", regions={ "ZM" } },
  { code="ber", name="Berber", regions={ "DZ", "MA" } },
  { code="bg", name="Bulgarian", regions={ "BG" } },
  { code="bhb", name="Bhili", regions={ "IN" } },
  { code="bho", name="Bhojpuri", regions={ "IN", "NP" } },
  { code="bi", name="Bislama", regions={ "VU" } },
  { code="bn", name="Bangla", regions={ "BD", "IN" } },
  { code="bo", name="Tibetan", regions={ "CN", "IN" } },
  { code="br", name="Breton", regions={ "FR" } },
  { code="brx", name="Bodo", regions={ "IN" } },
  { code="bs", name="Bosnian", regions={ "BA" } },
  { code="byn", name="Blin", regions={ "ER" } },
  { code="ca", name="Catalan", regions={ "AD", "ES", "FR", "IT" } },
  { code="ce", name="Chechen", regions={ "RU" } },
  { code="chr", name="Cherokee", regions={ "US" } },
  { code="ckb", name="Central Kurdish", regions={ "IQ" } },
  { code="cmn", name="Mandarin Chinese", regions={ "TW" } },
  { code="crh", name="Crimean Turkish", regions={ "UA" } },
  { code="cs", name="Czech", regions={ "CZ" } },
  { code="csb", name="Kashubian", regions={ "PL" } },
  { code="cv", name="Chuvash", regions={ "RU" } },
  { code="cy", name="Welsh", regions={ "GB" } },
  { code="da", name="Danish", regions={ "DK" } },
  {
    code="de",
    name="German",
    regions={ "AT", "BE", "CH", "DE", "IT", "LI", "LU" } 
  },
  { code="doi", name="Dogri", regions={ "IN" } },
  { code="dsb", name="Lower Sorbian", regions={ "DE" } },
  { code="dv", name="Divehi", regions={ "MV" } },
  { code="dz", name="Dzongkha", regions={ "BT" } },
  { code="el", name="Greek", regions={ "CY", "GR" } },
  {
    code="en",
    name="English",
    regions={
      "AG",
      "AU",
      "BW",
      "CA",
      "DK",
      "GB",
      "HK",
      "IE",
      "IL",
      "IN",
      "NG",
      "NZ",
      "PH",
      "SC",
      "SG",
      "US",
      "ZA",
      "ZM",
      "ZW" 
    } 
  },
  { code="eo", name="Esperanto", regions={} },
  {
    code="es",
    name="Spanish",
    regions={
      "AR",
      "BO",
      "CL",
      "CO",
      "CR",
      "CU",
      "DO",
      "EC",
      "ES",
      "GT",
      "HN",
      "MX",
      "NI",
      "PA",
      "PE",
      "PR",
      "PY",
      "SV",
      "US",
      "UY",
      "VE" 
    } 
  },
  { code="et", name="Estonian", regions={ "EE" } },
  { code="eu", name="Basque", regions={ "ES" } },
  { code="fa", name="Persian", regions={ "IR" } },
  { code="ff", name="Fulah", regions={ "SN" } },
  { code="fi", name="Finnish", regions={ "FI" } },
  { code="fil", name="Filipino", regions={ "PH" } },
  { code="fo", name="Faroese", regions={ "FO" } },
  { code="fr", name="French", regions={ "BE", "CA", "CH", "FR", "LU" } },
  { code="fur", name="Friulian", regions={ "IT" } },
  { code="fy", name="Western Frisian", regions={ "DE", "NL" } },
  { code="ga", name="Irish", regions={ "IE" } },
  { code="gd", name="Scottish Gaelic", regions={ "GB" } },
  { code="gez", name="Geez", regions={ "ER", "ET" } },
  { code="gl", name="Galician", regions={ "ES" } },
  { code="gu", name="Gujarati", regions={ "IN" } },
  { code="gv", name="Manx", regions={ "GB" } },
  { code="ha", name="Hausa", regions={ "NG" } },
  { code="hak", name="Hakka Chinese", regions={ "TW" } },
  { code="he", name="Hebrew", regions={ "IL" } },
  { code="hi", name="Hindi", regions={ "IN" } },
  { code="hif", name="Fiji Hindi", regions={ "FJ" } },
  { code="hne", name="Chhattisgarhi", regions={ "IN" } },
  { code="hr", name="Croatian", regions={ "HR" } },
  { code="hsb", name="Upper Sorbian", regions={ "DE" } },
  { code="ht", name="Haitian Creole", regions={ "HT" } },
  { code="hu", name="Hungarian", regions={ "HU" } },
  { code="hy", name="Armenian", regions={ "AM" } },
  { code="ia", name="Interlingua", regions={ "FR" } },
  { code="id", name="Indonesian", regions={ "ID" } },
  { code="ig", name="Igbo", regions={ "NG" } },
  { code="ik", name="Inupiaq", regions={ "CA" } },
  { code="is", name="Icelandic", regions={ "IS" } },
  { code="it", name="Italian", regions={ "CH", "IT" } },
  { code="iu", name="Inuktitut", regions={ "CA" } },
  { code="ja", name="Japanese", regions={ "JP" } },
  { code="ka", name="Georgian", regions={ "GE" } },
  { code="kab", name="Kabyle", regions={ "DZ" } },
  { code="kk", name="Kazakh", regions={ "KZ" } },
  { code="kl", name="Kalaallisut", regions={ "GL" } },
  { code="km", name="Khmer", regions={ "KH" } },
  { code="kn", name="Kannada", regions={ "IN" } },
  { code="ko", name="Korean", regions={ "KR" } },
  { code="kok", name="Konkani", regions={ "IN" } },
  { code="ks", name="Kashmiri", regions={ "IN" } },
  { code="ku", name="Kurdish", regions={ "TR" } },
  { code="kw", name="Cornish", regions={ "GB" } },
  { code="ky", name="Kyrgyz", regions={ "KG" } },
  { code="lb", name="Luxembourgish", regions={ "LU" } },
  { code="lg", name="Ganda", regions={ "UG" } },
  { code="li", name="Limburgish", regions={ "BE", "NL" } },
  { code="lij", name="Ligurian", regions={ "IT" } },
  { code="ln", name="Lingala", regions={ "CD" } },
  { code="lo", name="Lao", regions={ "LA" } },
  { code="lt", name="Lithuanian", regions={ "LT" } },
  { code="lv", name="Latvian", regions={ "LV" } },
  { code="lzh", name="Literary Chinese", regions={ "TW" } },
  { code="mag", name="Magahi", regions={ "IN" } },
  { code="mai", name="Maithili", regions={ "IN", "NP" } },
  { code="mfe", name="Morisyen", regions={ "MU" } },
  { code="mg", name="Malagasy", regions={ "MG" } },
  { code="mhr", name="Meadow Mari", regions={ "RU" } },
  { code="mi", name="Maori", regions={ "NZ" } },
  { code="miq", name="Miskito", regions={ "NI" } },
  { code="mjw", name="Karbi", regions={ "IN" } },
  { code="mk", name="Macedonian", regions={ "MK" } },
  { code="ml", name="Malayalam", regions={ "IN" } },
  { code="mn", name="Mongolian", regions={ "MN" } },
  { code="mni", name="Manipuri", regions={ "IN" } },
  { code="mnw", name="Mon", regions={ "MM" } },
  { code="mr", name="Marathi", regions={ "IN" } },
  { code="ms", name="Malay", regions={ "MY" } },
  { code="mt", name="Maltese", regions={ "MT" } },
  { code="my", name="Burmese", regions={ "MM" } },
  { code="nan", name="Min Nan Chinese", regions={ "TW" } },
  { code="nb", name="Norwegian Bokmål", regions={ "NO" } },
  { code="nds", name="Low German", regions={ "DE", "NL" } },
  { code="ne", name="Nepali", regions={ "NP" } },
  { code="nhn", name="Tlaxcala-Puebla Nahuatl", regions={ "MX" } },
  { code="niu", name="Niuean", regions={ "NU", "NZ" } },
  { code="nl", name="Dutch", regions={ "AW", "BE", "NL" } },
  { code="nn", name="Norwegian Nynorsk", regions={ "NO" } },
  { code="nr", name="South Ndebele", regions={ "ZA" } },
  { code="nso", name="Northern Sotho", regions={ "ZA" } },
  { code="oc", name="Occitan", regions={ "FR" } },
  { code="om", name="Oromo", regions={ "ET", "KE" } },
  { code="or", name="Odia", regions={ "IN" } },
  { code="os", name="Ossetic", regions={ "RU" } },
  { code="pa", name="Punjabi", regions={ "IN", "PK" } },
  { code="pap", name="Papiamento", regions={ "AW", "CW" } },
  { code="pl", name="Polish", regions={ "PL" } },
  { code="ps", name="Pashto", regions={ "AF" } },
  { code="pt", name="Portuguese", regions={ "BR", "PT" } },
  { code="quz", name="Cusco Quechua", regions={ "PE" } },
  { code="raj", name="Rajasthani", regions={ "IN" } },
  { code="rif", name="Tarifit", regions={ "MA" } },
  { code="ro", name="Romanian", regions={ "RO" } },
  { code="ru", name="Russian", regions={ "RU", "UA" } },
  { code="rw", name="Kinyarwanda", regions={ "RW" } },
  { code="sa", name="Sanskrit", regions={ "IN" } },
  { code="sah", name="Sakha", regions={ "RU" } },
  { code="sat", name="Santali", regions={ "IN" } },
  { code="sc", name="Sardinian", regions={ "IT" } },
  { code="sd", name="Sindhi", regions={ "IN" } },
  { code="se", name="Northern Sami", regions={ "NO" } },
  { code="sgs", name="Samogitian", regions={ "LT" } },
  { code="shn", name="Shan", regions={ "MM" } },
  { code="shs", name="Shuswap", regions={ "CA" } },
  { code="si", name="Sinhala", regions={ "LK" } },
  { code="sid", name="Sidamo", regions={ "ET" } },
  { code="sk", name="Slovak", regions={ "SK" } },
  { code="sl", name="Slovenian", regions={ "SI" } },
  { code="sm", name="Samoan", regions={ "WS" } },
  { code="so", name="Somali", regions={ "DJ", "ET", "KE", "SO" } },
  { code="sq", name="Albanian", regions={ "AL", "MK" } },
  { code="sr", name="Serbian", regions={ "ME", "RS" } },
  { code="ss", name="Swati", regions={ "ZA" } },
  { code="st", name="Southern Sotho", regions={ "ZA" } },
  { code="sv", name="Swedish", regions={ "FI", "SE" } },
  { code="sw", name="Swahili", regions={ "KE", "TZ" } },
  { code="syr", name="Syriac", regions={} },
  { code="szl", name="Silesian", regions={ "PL" } },
  { code="ta", name="Tamil", regions={ "IN", "LK" } },
  { code="tcy", name="Tulu", regions={ "IN" } },
  { code="te", name="Telugu", regions={ "IN" } },
  { code="tg", name="Tajik", regions={ "TJ" } },
  { code="th", name="Thai", regions={ "TH" } },
  { code="the", name="Chitwania Tharu", regions={ "NP" } },
  { code="ti", name="Tigrinya", regions={ "ER", "ET" } },
  { code="tig", name="Tigre", regions={ "ER" } },
  { code="tk", name="Turkmen", regions={ "TM" } },
  { code="tl", name="Tagalog", regions={ "PH" } },
  { code="tn", name="Tswana", regions={ "ZA" } },
  { code="to", name="Tongan", regions={ "TO" } },
  { code="tpi", name="Tok Pisin", regions={ "PG" } },
  { code="tr", name="Turkish", regions={ "CY", "TR" } },
  { code="ts", name="Tsonga", regions={ "ZA" } },
  { code="tt", name="Tatar", regions={ "RU" } },
  { code="ug", name="Uyghur", regions={ "CN" } },
  { code="uk", name="Ukrainian", regions={ "UA" } },
  { code="unm", name="Unami language", regions={ "US" } },
  { code="ur", name="Urdu", regions={ "IN", "PK" } },
  { code="uz", name="Uzbek", regions={ "UZ" } },
  { code="ve", name="Venda", regions={ "ZA" } },
  { code="vi", name="Vietnamese", regions={ "VN" } },
  { code="wa", name="Walloon", regions={ "BE" } },
  { code="wae", name="Walser", regions={ "CH" } },
  { code="wal", name="Wolaytta", regions={ "ET" } },
  { code="wo", name="Wolof", regions={ "SN" } },
  { code="xh", name="Xhosa", regions={ "ZA" } },
  { code="yi", name="Yiddish", regions={ "US" } },
  { code="yo", name="Yoruba", regions={ "NG" } },
  { code="yue", name="Cantonese", regions={ "HK" } },
  { code="yuw", name="Yau", regions={ "PG" } },
  { code="zh", name="Mandarin Chinese", regions={ "CN", "HK", "SG", "TW" } },
  { code="zu", name="Zulu", regions={ "ZA" } } 
}

-- Prints a list of LANGUAGE "_" REGION pairs.  The output is expected
-- to be identical to parse-SUPPORTED.py.  Called from the %%prep section.
function print_locale_pairs()
   for i = 1, #locales do
      local locale = locales[i]
      if #locale.regions == 0 then
	 print(locale.code .. "\n")
      else
	 for j = 1, #locale.regions do
	    print(locale.code .. "_" .. locale.regions[j] .. "\n")
	 end
      end
   end
end

local function compute_supplements(locale)
   local lang = locale.code
   local regions = locale.regions
   result = "langpacks-core-" .. lang
   for i = 1, #regions do
      result = result .. " or langpacks-core-" .. lang .. "_" .. regions[i]
   end
   return result
end

-- Emit the definition of a language pack package.
local function lang_package(locale)
   local lang = locale.code
   local langname = locale.name
   local suppl = compute_supplements(locale)
   print(rpm.expand([[

%package langpack-]]..lang..[[

Summary: Locale data for ]]..langname..[[

Provides: glibc-langpack = %{version}-%{release}
Requires: %{name} = %{version}-%{release}
Requires: %{name}-common = %{version}-%{release}
Supplements: (glibc and (]]..suppl..[[))
%description langpack-]]..lang..[[

The glibc-langpack-]]..lang..[[ package includes the basic information required
to support the ]]..langname..[[ language in your applications.
%files -f langpack-]]..lang..[[.filelist langpack-]]..lang..[[
]]))
end

for i = 1, #locales do
   lang_package(locales[i])
end
}

# The glibc-all-langpacks provides the virtual glibc-langpack,
# and thus satisfies glibc's requirement for installed locales.
# Users can add one more other langauge packs and then eventually
# uninstall all-langpacks to save space.
%package all-langpacks
Summary: All language packs for %{name}.
Requires: %{name} = %{version}-%{release}
Requires: %{name}-common = %{version}-%{release}
Provides: %{name}-langpack = %{version}-%{release}
%description all-langpacks

# No %files, this is an empty package. The C/POSIX and
# C.UTF-8 files are already installed by glibc. We create
# minimal-langpack because the virtual provide of
# glibc-langpack needs at least one package installed
# to satisfy it. Given that no-locales installed is a valid
# use case we support it here with this package.
%package minimal-langpack
Summary: Minimal language packs for %{name}.
Provides: glibc-langpack = %{version}-%{release}
Requires: %{name} = %{version}-%{release}
Requires: %{name}-common = %{version}-%{release}
%description minimal-langpack
This is a Meta package that is used to install minimal language packs.
This package ensures you can use C, POSIX, or C.UTF-8 locales, but
nothing else. It is designed for assembling a minimal system.
%files minimal-langpack

# Infrequently used iconv converter modules.
%package gconv-extra
Summary: All iconv converter modules for %{name}.
Requires: %{name}%{_isa} = %{version}-%{release}
Requires: %{name}-common = %{version}-%{release}

%description gconv-extra
This package contains all iconv converter modules built in %{name}.

##############################################################################
# Subpackages for NSS modules except nss_files, nss_compat, nss_dns
##############################################################################

# This should remain it's own subpackage or "Provides: nss_db" to allow easy
# migration from old systems that previously had the old nss_db package
# installed. Note that this doesn't make the migration that smooth, the
# databases still need rebuilding because the formats were different.
# The nss_db package was deprecated in F16 and onwards:
# https://lists.fedoraproject.org/pipermail/devel/2011-July/153665.html
# The different database format does cause some issues for users:
# https://lists.fedoraproject.org/pipermail/devel/2011-December/160497.html
%package -n nss_db
Summary: Name Service Switch (NSS) module using hash-indexed files
Requires: %{name}%{_isa} = %{version}-%{release}
%ifarch x86_64
# Automatically install the 32-bit variant if the 64-bit variant has
# been installed.  This covers the case when glibc.i686 is installed
# before nss_db.x86_64.  (See above for the other ordering.)
Recommends: (nss_db(x86-32) if glibc(x86-32))
%endif

%description -n nss_db
The nss_db Name Service Switch module uses hash-indexed files in /var/db
to speed up user, group, service, host name, and other NSS-based lookups.

%package -n nss_hesiod
Summary: Name Service Switch (NSS) module using Hesiod
Requires: %{name}%{_isa} = %{version}-%{release}
%ifarch x86_64
# Automatically install the 32-bit variant if the 64-bit variant has
# been installed.  This covers the case when glibc.i686 is installed
# before nss_hesiod.x86_64.  (See above for the other ordering.)
Recommends: (nss_hesiod(x86-32) if glibc(x86-32))
%endif

%description -n nss_hesiod
The nss_hesiod Name Service Switch module uses the Domain Name System
(DNS) as a source for user, group, and service information, following
the Hesiod convention of Project Athena.

%package nss-devel
Summary: Development files for directly linking NSS service modules
Requires: %{name}%{_isa} = %{version}-%{release}
Requires: nss_db%{_isa} = %{version}-%{release}
Requires: nss_hesiod%{_isa} = %{version}-%{release}

%description nss-devel
The glibc-nss-devel package contains the object files necessary to
compile applications and libraries which directly link against NSS
modules supplied by glibc.

This is a rare and special use case; regular development has to use
the glibc-devel package instead.

##############################################################################
# glibc "utils" sub-package
##############################################################################
%package utils
Summary: Development utilities from GNU C library
Requires: %{name} = %{version}-%{release}

%description utils
The glibc-utils package contains memusage, a memory usage profiler,
mtrace, a memory leak tracer and xtrace, a function call tracer
which can be helpful during program debugging.

If unsure if you need this, don't install this package.

%if %{with benchtests}
%package benchtests
Summary: Benchmarking binaries and scripts for %{name}
%description benchtests
This package provides built benchmark binaries and scripts to run
microbenchmark tests on the system.
%endif

##############################################################################
# compat-libpthread-nonshared
# See: https://sourceware.org/bugzilla/show_bug.cgi?id=23500
##############################################################################
%package -n compat-libpthread-nonshared
Summary: Compatibility support for linking against libpthread_nonshared.a.

%description -n compat-libpthread-nonshared
This package provides compatibility support for applications that expect
libpthread_nonshared.a to exist. The support provided is in the form of
an empty libpthread_nonshared.a that allows dynamic links to succeed.
Such applications should be adjusted to avoid linking against
libpthread_nonshared.a which is no longer used. The static library
libpthread_nonshared.a is an internal implementation detail of the C
runtime and should not be expected to exist.

##############################################################################
# Prepare for the build.
##############################################################################
%prep
%autosetup -n %{glibcsrcdir} -p1

##############################################################################
# %%prep - Additional prep required...
##############################################################################
# Make benchmark scripts executable
chmod +x benchtests/scripts/*.py scripts/pylint

# Remove all files generated from patching.
find . -type f -size 0 -o -name "*.orig" -exec rm -f {} \;

# Ensure timestamps on configure files are current to prevent
# regenerating them.
touch `find . -name configure`

# Ensure *-kw.h files are current to prevent regenerating them.
touch locale/programs/*-kw.h

# Verify that our locales table is compatible with the locales table
# in the spec file.
set +x
echo '%{lua: print_locale_pairs()}' > localedata/SUPPORTED.spec
set -x
python3 %{SOURCE11} localedata/SUPPORTED > localedata/SUPPORTED.glibc
diff -u \
  --label "spec file" localedata/SUPPORTED.spec \
  --label "glibc localedata/SUPPORTED" localedata/SUPPORTED.glibc
rm localedata/SUPPORTED.spec localedata/SUPPORTED.glibc

##############################################################################
# Build glibc...
##############################################################################
%build
# Log osystem information
uname -a
LD_SHOW_AUXV=1 /bin/true
cat /proc/cpuinfo
cat /proc/sysinfo 2>/dev/null || true
cat /proc/meminfo
df

# We build using the native system compilers.
GCC=gcc
GXX=g++

# Part of rpm_inherit_flags.  Is overridden below.
rpm_append_flag ()
{
    BuildFlags="$BuildFlags $*"
}

# Propagates the listed flags to rpm_append_flag if supplied by
# redhat-rpm-config.
BuildFlags="-O2 -g"
rpm_inherit_flags ()
{
	local reference=" $* "
	local flag
	for flag in $RPM_OPT_FLAGS $RPM_LD_FLAGS ; do
		if echo "$reference" | grep -q -F " $flag " ; then
			rpm_append_flag "$flag"
		fi
	done
}

# Propgate select compiler flags from redhat-rpm-config.  These flags
# are target-dependent, so we use only those which are specified in
# redhat-rpm-config.  We keep the -m32/-m32/-m64 flags to support
# multilib builds.
#
# Note: For building alternative run-times, care is required to avoid
# overriding the architecture flags which go into CC/CXX.  The flags
# below are passed in CFLAGS.

rpm_inherit_flags \
	"-Wp,-D_GLIBCXX_ASSERTIONS" \
	"-fasynchronous-unwind-tables" \
	"-fstack-clash-protection" \
	"-fno-omit-frame-pointer" \
	"-funwind-tables" \
	"-m31" \
	"-m32" \
	"-m64" \
	"-march=armv8-a+lse" \
	"-march=armv8.1-a" \
	"-march=haswell" \
	"-march=i686" \
	"-march=x86-64" \
	"-march=x86-64-v2" \
	"-march=x86-64-v3" \
	"-march=x86-64-v4" \
	"-march=z13" \
	"-march=z14" \
	"-march=z15" \
	"-march=zEC12" \
	"-mbranch-protection=standard" \
	"-mcpu=power10" \
	"-mcpu=power8" \
	"-mcpu=power9" \
	"-mfpmath=sse" \
	"-mno-omit-leaf-frame-pointer" \
	"-msse2" \
	"-mstackrealign" \
	"-mtune=generic" \
	"-mtune=power10" \
	"-mtune=power8" \
	"-mtune=power9" \
	"-mtune=z13" \
	"-mtune=z14" \
	"-mtune=z15" \
	"-mtune=zEC12" \
	"-specs=/usr/lib/rpm/redhat/redhat-annobin-cc1" \

%if 0%{?_annotated_build} > 0
# libc_nonshared.a cannot be built with the default hardening flags
# because the glibc build system is incompatible with
# -D_FORTIFY_SOURCE.  The object files need to be marked as to be
# skipped in annobin annotations.  (The -specs= variant of activating
# annobin does not work here because of flag ordering issues.)
# See <https://bugzilla.redhat.com/show_bug.cgi?id=1668822>.
BuildFlagsNonshared="-fplugin=annobin -fplugin-arg-annobin-disable -Wa,--generate-missing-build-notes=yes"
%endif

# Special flag to enable annobin annotations for statically linked
# assembler code.  Needs to be passed to make; not preserved by
# configure.
%global glibc_make_flags_as ASFLAGS="-g -Wa,--generate-missing-build-notes=yes"
%global glibc_make_flags %{glibc_make_flags_as}

##############################################################################
# %%build - Generic options.
##############################################################################
EnableKernel="--enable-kernel=%{enablekernel}"
# Save the used compiler and options into the file "Gcc" for use later
# by %%install.
echo "$GCC" > Gcc

##############################################################################
# build()
#	Build glibc in `build-%{target}$1', passing the rest of the arguments
#	as CFLAGS to the build (not the same as configure CFLAGS). Several
#	global values are used to determine build flags, kernel version,
#	system tap support, etc.
##############################################################################
build()
{
	local builddir=build-%{target}${1:+-$1}
	${1+shift}
	rm -rf $builddir
	mkdir $builddir
	pushd $builddir
	../configure CC="$GCC" CXX="$GXX" CFLAGS="$BuildFlags $*" \
		--prefix=%{_prefix} \
		--with-headers=%{_prefix}/include $EnableKernel \
		--with-nonshared-cflags="$BuildFlagsNonshared" \
		--enable-bind-now \
		--build=%{target} \
		--enable-stack-protector=strong \
		--enable-tunables \
		--enable-systemtap \
		${core_with_options} \
%ifarch x86_64 %{ix86}
	       --enable-cet \
%endif
%ifarch %{ix86}
		--disable-multi-arch \
%endif
%if %{without werror}
		--disable-werror \
%endif
		--disable-profile \
%if %{with bootstrap}
		--without-selinux \
%endif
%ifarch aarch64
		--enable-memory-tagging \
%endif
		--disable-crypt \
	        --disable-build-nscd \
	        --disable-nscd ||
		{ cat config.log; false; }

	%make_build -r %{glibc_make_flags}
	popd
}

# Default set of compiler options.
build

##############################################################################
# Install glibc...
##############################################################################
%install

# The built glibc is installed into a subdirectory of $RPM_BUILD_ROOT.
# For a system glibc that subdirectory is "/" (the root of the filesystem).
# This is called a sysroot (system root) and can be changed if we have a
# distribution that supports multiple installed glibc versions.
%global glibc_sysroot $RPM_BUILD_ROOT

# Remove existing file lists.
find . -type f -name '*.filelist' -exec rm -rf {} \;

# Reload compiler and build options that were used during %%build.
GCC=`cat Gcc`

%ifarch riscv64
# RISC-V ABI wants to install everything in /lib64/lp64d or /usr/lib64/lp64d.
# Make these be symlinks to /lib64 or /usr/lib64 respectively.  See:
# https://lists.fedoraproject.org/archives/list/devel@lists.fedoraproject.org/thread/DRHT5YTPK4WWVGL3GIN5BF2IKX2ODHZ3/
for d in %{glibc_sysroot}%{_libdir} %{glibc_sysroot}/%{_lib}; do
	mkdir -p $d
	(cd $d && ln -sf . lp64d)
done
%endif

# Build and install:
pushd build-%{target}
%make_build install_root=%{glibc_sysroot} install
%make_build install_root=%{glibc_sysroot} \
	install-locale-files -C ../localedata objdir=`pwd`
popd
# Locale creation via install-locale-files does not group identical files
# via hardlinks, so we must group them ourselves.
hardlink -c %{glibc_sysroot}/usr/lib/locale

# install_different:
#	Install all core libraries into DESTDIR/SUBDIR. Either the file is
#	installed as a copy or a symlink to the default install (if it is the
#	same). The path SUBDIR_UP is the prefix used to go from
#	DESTDIR/SUBDIR to the default installed libraries e.g.
#	ln -s SUBDIR_UP/foo.so DESTDIR/SUBDIR/foo.so.
#	When you call this function it is expected that you are in the root
#	of the build directory, and that the default build directory is:
#	"../build-%{target}" (relatively).
#	The primary use of this function is to install alternate runtimes
#	into the build directory and avoid duplicating this code for each
#	runtime.
install_different()
{
	local lib libbase libbaseso dlib
	local destdir="$1"
	local subdir="$2"
	local subdir_up="$3"
	local libdestdir="$destdir/$subdir"
	# All three arguments must be non-zero paths.
	if ! [ "$destdir" \
	       -a "$subdir" \
	       -a "$subdir_up" ]; then
		echo "One of the arguments to install_different was emtpy."
		exit 1
	fi
	# Create the destination directory and the multilib directory.
	mkdir -p "$destdir"
	mkdir -p "$libdestdir"
	# Walk all of the libraries we installed...
	for lib in libc math/libm nptl/libpthread rt/librt nptl_db/libthread_db
	do
		libbase=${lib#*/}
		# Take care that `libbaseso' has a * that needs expanding so
		# take care with quoting.
		libbaseso=$(basename %{glibc_sysroot}/%{_lib}/${libbase}-*.so)
		# Only install if different from default build library.
		if cmp -s ${lib}.so ../build-%{target}/${lib}.so; then
			ln -sf "$subdir_up"/$libbaseso $libdestdir/$libbaseso
		else
			cp -a ${lib}.so $libdestdir/$libbaseso
		fi
		dlib=$libdestdir/$(basename %{glibc_sysroot}/%{_lib}/${libbase}.so.*)
		ln -sf $libbaseso $dlib
	done
}

##############################################################################
# Remove the files we don't want to distribute
##############################################################################

# Remove the libNoVersion files.
# XXX: This looks like a bug in glibc that accidentally installed these
#      wrong files. We probably don't need this today.
rm -f %{glibc_sysroot}/%{_libdir}/libNoVersion*
rm -f %{glibc_sysroot}/%{_lib}/libNoVersion*

# Remove the old nss modules.
rm -f %{glibc_sysroot}/%{_lib}/libnss1-*
rm -f %{glibc_sysroot}/%{_lib}/libnss-*.so.1

# This statically linked binary is no longer necessary in a world where
# the default Fedora install uses an initramfs, and further we have rpm-ostree
# which captures the whole userspace FS tree.
# Further, see https://github.com/projectatomic/rpm-ostree/pull/1173#issuecomment-355014583
rm -f %{glibc_sysroot}/{usr/,}sbin/sln

######################################################################
# Run ldconfig to create all the symbolic links we need
######################################################################

# Note: This has to happen before creating /etc/ld.so.conf.

mkdir -p %{glibc_sysroot}/var/cache/ldconfig
truncate -s 0 %{glibc_sysroot}/var/cache/ldconfig/aux-cache

# ldconfig is statically linked, so we can use the new version.
%{glibc_sysroot}/sbin/ldconfig -N -r %{glibc_sysroot}

##############################################################################
# Install info files
##############################################################################

%if %{with docs}
# Move the info files if glibc installed them into the wrong location.
if [ -d %{glibc_sysroot}%{_prefix}/info -a "%{_infodir}" != "%{_prefix}/info" ]; then
  mkdir -p %{glibc_sysroot}%{_infodir}
  mv -f %{glibc_sysroot}%{_prefix}/info/* %{glibc_sysroot}%{_infodir}
  rm -rf %{glibc_sysroot}%{_prefix}/info
fi

# Compress all of the info files.
gzip -9nvf %{glibc_sysroot}%{_infodir}/libc*

# Copy the debugger interface documentation over to the right location
mkdir -p %{glibc_sysroot}%{_docdir}/glibc
cp elf/rtld-debugger-interface.txt %{glibc_sysroot}%{_docdir}/glibc
%else
rm -f %{glibc_sysroot}%{_infodir}/dir
rm -f %{glibc_sysroot}%{_infodir}/libc.info*
%endif

##############################################################################
# Create locale sub-package file lists
##############################################################################

olddir=`pwd`
pushd %{glibc_sysroot}%{_prefix}/lib/locale
rm -f locale-archive
$olddir/build-%{target}/elf/ld.so \
        --library-path $olddir/build-%{target}/ \
        $olddir/build-%{target}/locale/localedef \
	--alias-file=$olddir/intl/locale.alias \
        --prefix %{glibc_sysroot} --add-to-archive \
        %locale_rx
# Historically, glibc-all-langpacks deleted the file on updates (sic),
# so we need to restore it in the posttrans scriptlet (like the old
# glibc-all-langpacks versions)
ln locale-archive locale-archive.real

# Almost half the LC_CTYPE files in langpacks are identical to the C.utf8
# variant which is installed by default.  When we keep them as hardlinks,
# each langpack ends up retaining a copy.  If we convert these to symbolic
# links instead, we save ~350K each when they get installed that way.
#
# LC_MEASUREMENT and LC_PAPER also have several duplicates but we don't
# bother with these because they are only ~30 bytes each.
pushd %{glibc_sysroot}/usr/lib/locale
for f in $(find %locale_rx -samefile C.utf8/LC_CTYPE); do
  rm $f && ln -s '../C.utf8/LC_CTYPE' $f
done
popd

# Create the file lists for the language specific sub-packages:
for i in %locale_rx 
do
    lang=${i%%_*}
    if [ ! -e langpack-${lang}.filelist ]; then
        echo "%dir %{_prefix}/lib/locale" >> langpack-${lang}.filelist
    fi
    echo "%dir  %{_prefix}/lib/locale/$i" >> langpack-${lang}.filelist
    echo "%{_prefix}/lib/locale/$i/*" >> langpack-${lang}.filelist
done
popd
pushd %{glibc_sysroot}%{_prefix}/share/locale
for i in */LC_MESSAGES/libc.mo
do
    locale=${i%%%%/*}
    lang=${locale%%%%_*}
    echo "%lang($lang) %{_prefix}/share/locale/${i}" \
         >> %{glibc_sysroot}%{_prefix}/lib/locale/langpack-${lang}.filelist
done
popd
mv  %{glibc_sysroot}%{_prefix}/lib/locale/*.filelist .

##############################################################################
# Install configuration files for services
##############################################################################

# Include ld.so.conf
echo 'include ld.so.conf.d/*.conf' > %{glibc_sysroot}/etc/ld.so.conf
truncate -s 0 %{glibc_sysroot}/etc/ld.so.cache
chmod 644 %{glibc_sysroot}/etc/ld.so.conf
mkdir -p %{glibc_sysroot}/etc/ld.so.conf.d
truncate -s 0 %{glibc_sysroot}/etc/gai.conf

# Include %{_libdir}/gconv/gconv-modules.cache
truncate -s 0 %{glibc_sysroot}%{_libdir}/gconv/gconv-modules.cache
chmod 644 %{glibc_sysroot}%{_libdir}/gconv/gconv-modules.cache

# Remove any zoneinfo files; they are maintained by tzdata.
rm -rf %{glibc_sysroot}%{_prefix}/share/zoneinfo

# Make sure %config files have the same timestamp across multilib packages.
#
# XXX: Ideally ld.so.conf should have the timestamp of the spec file, but there
# doesn't seem to be any macro to give us that.  So we do the next best thing,
# which is to at least keep the timestamp consistent. The choice of using
# SOURCE0 is arbitrary.
touch -r %{SOURCE0} %{glibc_sysroot}/etc/ld.so.conf
touch -r inet/etc.rpc %{glibc_sysroot}/etc/rpc

%if %{with benchtests}
# Build benchmark binaries.  Ignore the output of the benchmark runs.
pushd build-%{target}
make BENCH_DURATION=1 bench-build
popd

# Copy over benchmark binaries.
mkdir -p %{glibc_sysroot}%{_prefix}/libexec/glibc-benchtests
cp $(find build-%{target}/benchtests -type f -executable) %{glibc_sysroot}%{_prefix}/libexec/glibc-benchtests/
# ... and the makefile.
for b in %{SOURCE1} %{SOURCE2}; do
	cp $b %{glibc_sysroot}%{_prefix}/libexec/glibc-benchtests/
done
# .. and finally, the comparison scripts.
cp benchtests/scripts/benchout.schema.json %{glibc_sysroot}%{_prefix}/libexec/glibc-benchtests/
cp benchtests/scripts/compare_bench.py %{glibc_sysroot}%{_prefix}/libexec/glibc-benchtests/
cp benchtests/scripts/import_bench.py %{glibc_sysroot}%{_prefix}/libexec/glibc-benchtests/
cp benchtests/scripts/validate_benchout.py %{glibc_sysroot}%{_prefix}/libexec/glibc-benchtests/
%endif

# The #line directives gperf generates do not give the proper
# file name relative to the build directory.
pushd locale
ln -s programs/*.gperf .
popd
pushd iconv
ln -s ../locale/programs/charmap-kw.gperf .
popd

%if %{with docs}
# Remove the `dir' info-heirarchy file which will be maintained
# by the system as it adds info files to the install.
rm -f %{glibc_sysroot}%{_infodir}/dir
%endif

# Move libpcprofile.so and libmemusage.so into the proper library directory.
# They can be moved without any real consequences because users would not use
# them directly.
mkdir -p %{glibc_sysroot}%{_libdir}
mv -f %{glibc_sysroot}/%{_lib}/lib{pcprofile,memusage}.so \
	%{glibc_sysroot}%{_libdir}

# Disallow linking against libc_malloc_debug.
rm %{glibc_sysroot}%{_libdir}/libc_malloc_debug.so

# Strip all of the installed object files.
strip -g %{glibc_sysroot}%{_libdir}/*.o

# The xtrace and memusage scripts have hard-coded paths that need to be
# translated to a correct set of paths using the $LIB token which is
# dynamically translated by ld.so as the default lib directory.
for i in %{glibc_sysroot}%{_prefix}/bin/{xtrace,memusage}; do
%if %{with bootstrap}
  test -w $i || continue
%endif
  sed -e 's~=/%{_lib}/libpcprofile.so~=%{_libdir}/libpcprofile.so~' \
      -e 's~=/%{_lib}/libmemusage.so~=%{_libdir}/libmemusage.so~' \
      -e 's~='\''/\\\$LIB/libpcprofile.so~='\''%{_prefix}/\\$LIB/libpcprofile.so~' \
      -e 's~='\''/\\\$LIB/libmemusage.so~='\''%{_prefix}/\\$LIB/libmemusage.so~' \
      -i $i
done

##############################################################################
# Build an empty libpthread_nonshared.a for compatiliby with applications
# that have old linker scripts that reference this file. We ship this only
# in compat-libpthread-nonshared sub-package.
##############################################################################
ar cr %{glibc_sysroot}%{_prefix}/%{_lib}/libpthread_nonshared.a

##############################################################################
# Beyond this point in the install process we no longer modify the set of
# installed files.
##############################################################################

##############################################################################
# Build the file lists used for describing the package and subpackages.
##############################################################################
# There are several main file lists (and many more for
# the langpack sub-packages (langpack-${lang}.filelist)):
# * master.filelist
#	- Master file list from which all other lists are built.
# * glibc.filelist
#	- Files for the glibc packages.
# * common.filelist
#	- Flies for the common subpackage.
# * utils.filelist
#	- Files for the utils subpackage.
# * devel.filelist
#	- Files for the devel subpackage.
# * doc.filelist
#	- Files for the documentation subpackage.
# * headers.filelist
#	- Files for the headers subpackage.
# * static.filelist
#	- Files for the static subpackage.
# * libnsl.filelist
#       - Files for the libnsl subpackage
# * nss_db.filelist
# * nss_hesiod.filelist
#       - File lists for nss_* NSS module subpackages.
# * nss-devel.filelist
#       - File list with the .so symbolic links for NSS packages.
# * compat-libpthread-nonshared.filelist.
#	- File list for compat-libpthread-nonshared subpackage.

# Create the main file lists. This way we can append to any one of them later
# wihtout having to create it. Note these are removed at the start of the
# install phase.
touch master.filelist
touch glibc.filelist
touch common.filelist
touch utils.filelist
touch gconv.filelist
touch devel.filelist
touch doc.filelist
touch headers.filelist
touch static.filelist
touch libnsl.filelist
touch nss_db.filelist
touch nss_hesiod.filelist
touch nss-devel.filelist
touch compat-libpthread-nonshared.filelist

###############################################################################
# Master file list, excluding a few things.
###############################################################################
{
  # List all files or links that we have created during install.
  # Files with 'etc' are configuration files, likewise 'gconv-modules'
  # and 'gconv-modules.cache' are caches, and we exclude them.
  find %{glibc_sysroot} \( -type f -o -type l \) \
       \( \
	 -name etc -printf "%%%%config " -o \
	 -name gconv-modules.cache \
	 -printf "%%%%verify(not md5 size mtime) " -o \
	 -name gconv-modules* \
	 -printf "%%%%verify(not md5 size mtime) %%%%config(noreplace) " \
	 , \
	 ! -path "*/lib/debug/*" -printf "/%%P\n" \)
  # List all directories with a %%dir prefix.  We omit the info directory and
  # all directories in (and including) /usr/share/locale.
  find %{glibc_sysroot} -type d \
       \( -path '*%{_prefix}/share/locale' -prune -o \
       \( -path '*%{_prefix}/share/*' \
%if %{with docs}
	! -path '*%{_infodir}' -o \
%endif
	  -path "*%{_prefix}/include/*" \
       \) -printf "%%%%dir /%%P\n" \)
} | {
  # Also remove the *.mo entries.  We will add them to the
  # language specific sub-packages.
  # libnss_ files go into subpackages related to NSS modules.
  # and .*/share/i18n/charmaps/.*), they go into the sub-package
  # "locale-source":
  sed -e '\,.*/share/locale/\([^/_]\+\).*/LC_MESSAGES/.*\.mo,d' \
      -e '\,.*/share/i18n/locales/.*,d' \
      -e '\,.*/share/i18n/charmaps/.*,d' \
      -e '\,.*/etc/\(localtime\|nsswitch.conf\|ld\.so\.conf\|ld\.so\.cache\|default\|rpc\|gai\.conf\),d' \
      -e '\,.*/%{_libdir}/lib\(pcprofile\|memusage\)\.so,d' \
      -e '\,.*/bin/\(memusage\|mtrace\|xtrace\|pcprofiledump\),d'
} | sort > master.filelist

# The master file list is now used by each subpackage to list their own
# files. We go through each package and subpackage now and create their lists.
# Each subpackage picks the files from the master list that they need.
# The order of the subpackage list generation does not matter.

# Make the master file list read-only after this point to avoid accidental
# modification.
chmod 0444 master.filelist

###############################################################################
# glibc
###############################################################################

# Add all files with the following exceptions:
# - The info files '%{_infodir}/dir'
# - The partial (lib*_p.a) static libraries, include files.
# - The static files, objects, and unversioned DSOs.
# - The bin, locale, some sbin, and share.
#   - We want iconvconfig in the main package and we do this by using
#     a double negation of -v and [^i] so it removes all files in
#     sbin *but* iconvconfig.
# - All the libnss files (we add back the ones we want later).
# - All bench test binaries.
# - The aux-cache, since it's handled specially in the files section.
# - Extra gconv modules.  We add the required modules later.
cat master.filelist \
	| grep -v \
	-e '%{_infodir}' \
	-e '%{_libdir}/lib.*_p.a' \
	-e '%{_prefix}/include' \
	-e '%{_libdir}/lib.*\.a' \
        -e '%{_libdir}/.*\.o' \
	-e '%{_libdir}/lib.*\.so' \
	-e '%{_libdir}/gconv/.*\.so$' \
	-e '%{_libdir}/gconv/gconv-modules.d/gconv-modules-extra\.conf$' \
	-e '%{_prefix}/bin' \
	-e '%{_prefix}/lib/locale' \
	-e '%{_prefix}/sbin/[^i]' \
	-e '%{_prefix}/share' \
	-e '/var/db/Makefile' \
	-e '/libnss_.*\.so[0-9.]*$' \
	-e '/libnsl' \
	-e 'glibc-benchtests' \
	-e 'aux-cache' \
	> glibc.filelist

# Add specific files:
# - The nss_files, nss_compat, and nss_db files.
# - The libmemusage.so and libpcprofile.so used by utils.
for module in compat files dns; do
    cat master.filelist \
	| grep -E \
	-e "/libnss_$module(\.so\.[0-9.]+|-[0-9.]+\.so)$" \
	>> glibc.filelist
done
grep -e "libmemusage.so" -e "libpcprofile.so" master.filelist >> glibc.filelist

###############################################################################
# glibc-gconv-extra
###############################################################################

grep -e "gconv-modules-extra.conf" master.filelist > gconv.filelist

# Put the essential gconv modules into the main package.
GconvBaseModules="ANSI_X3.110 ISO8859-15 ISO8859-1 CP1252"
GconvBaseModules="$GconvBaseModules UNICODE UTF-16 UTF-32 UTF-7"
%ifarch s390 s390x
GconvBaseModules="$GconvBaseModules ISO-8859-1_CP037_Z900 UTF8_UTF16_Z9"
GconvBaseModules="$GconvBaseModules UTF16_UTF32_Z9 UTF8_UTF32_Z9"
%endif
GconvAllModules=$(cat master.filelist |
                 sed -n 's|%{_libdir}/gconv/\(.*\)\.so|\1|p')

# Put the base modules into glibc and the rest into glibc-gconv-extra
for conv in $GconvAllModules; do
    if echo $GconvBaseModules | grep -q $conv; then
	grep -E -e "%{_libdir}/gconv/$conv.so$" \
	    master.filelist >> glibc.filelist
    else
	grep -E -e "%{_libdir}/gconv/$conv.so$" \
	    master.filelist >> gconv.filelist
    fi
done

###############################################################################
# glibc-devel
###############################################################################

# Static libraries that land in glibc-devel, not glibc-static.
devel_static_library_pattern='/lib\(\(c\|nldbl\|mvec\)_nonshared\|g\|ieee\|mcheck\|pthread\|dl\|rt\|util\|anl\)\.a$'
# Static libraries neither in glibc-devel nor in glibc-static.
other_static_library_pattern='/libpthread_nonshared\.a'

grep '%{_libdir}/lib.*\.a' master.filelist \
  | grep "$devel_static_library_pattern" \
  | grep -v "$other_static_library_pattern" \
  > devel.filelist

# Put all of the object files and *.so (not the versioned ones) into the
# devel package.
grep '%{_libdir}/.*\.o' < master.filelist >> devel.filelist
grep '%{_libdir}/lib.*\.so' < master.filelist >> devel.filelist
# The exceptions are:
# - libmemusage.so and libpcprofile.so in glibc used by utils.
# - libnss_*.so which are in nss-devel.
sed -i -e '\,libmemusage.so,d' \
	-e '\,libpcprofile.so,d' \
	-e '\,/libnss_[a-z]*\.so$,d' \
	devel.filelist

%if %{glibc_autorequires}
mkdir -p %{glibc_sysroot}/%{_rpmconfigdir} %{glibc_sysroot}/%{_fileattrsdir}
sed < %{SOURCE3} \
    -e s/@VERSION@/%{version}/ \
    -e s/@RELEASE@/%{release}/ \
    -e s/@SYMVER@/%{glibc_autorequires_symver}/ \
    > %{glibc_sysroot}/%{_rpmconfigdir}/glibc.req
cp %{SOURCE4} %{glibc_sysroot}/%{_fileattrsdir}/glibc.attr
%endif

###############################################################################
# glibc-doc
###############################################################################

%if %{with docs}
# Put the info files into the doc file list, but exclude the generated dir.
grep '%{_infodir}' master.filelist | grep -v '%{_infodir}/dir' > doc.filelist
grep '%{_docdir}' master.filelist >> doc.filelist
%endif

###############################################################################
# glibc-headers
###############################################################################

%if %{need_headers_package}
# The glibc-headers package includes only common files which are identical
# across all multilib packages. We must keep gnu/stubs.h and gnu/lib-names.h
# in the glibc-headers package, but the -32, -64, -64-v1, and -64-v2 versions
# go into glibc-devel.
grep '%{_prefix}/include/gnu/stubs-.*\.h$' < master.filelist >> devel.filelist || :
grep '%{_prefix}/include/gnu/lib-names-.*\.h$' < master.filelist >> devel.filelist || :
# Put the include files into headers file list.
grep '%{_prefix}/include' < master.filelist \
  | egrep -v '%{_prefix}/include/gnu/stubs-.*\.h$' \
  | egrep -v '%{_prefix}/include/gnu/lib-names-.*\.h$' \
  > headers.filelist
%else
# If there is no glibc-headers package, all header files go into the
# glibc-devel package.
grep '%{_prefix}/include' < master.filelist >> devel.filelist
%endif

###############################################################################
# glibc-static
###############################################################################

# Put the rest of the static files into the static package.
grep '%{_libdir}/lib.*\.a' < master.filelist \
  | grep -v "$devel_static_library_pattern" \
  | grep -v "$other_static_library_pattern" \
  > static.filelist

###############################################################################
# glibc-common
###############################################################################

# All of the bin and certain sbin files go into the common package except
# iconvconfig which needs to go in glibc.  The iconvconfig binary is kept in
# the main glibc package because we use it in the post-install scriptlet to
# rebuild the gconv-modules.cache.  The makedb binary is in nss_db.
grep '%{_prefix}/bin' master.filelist \
	| grep -v '%{_prefix}/bin/makedb' \
	>> common.filelist
grep '%{_prefix}/sbin' master.filelist \
	| grep -v '%{_prefix}/sbin/iconvconfig' >> common.filelist
# All of the files under share go into the common package since they should be
# multilib-independent.
# Exceptions:
# - The actual share directory, not owned by us.
# - The info files which go into doc, and the info directory.
# - All documentation files, which go into doc.
grep '%{_prefix}/share' master.filelist \
	| grep -v \
	-e '%{_prefix}/share/info/libc.info.*' \
	-e '%%dir %{prefix}/share/info' \
	-e '%%dir %{prefix}/share' \
	-e '%{_docdir}' \
	>> common.filelist

###############################################################################
# glibc-utils
###############################################################################

# Add the utils scripts and programs to the utils subpackage.
cat > utils.filelist <<EOF
%if %{without bootstrap}
%{_prefix}/bin/memusage
%{_prefix}/bin/memusagestat
%endif
%{_prefix}/bin/mtrace
%{_prefix}/bin/pcprofiledump
%{_prefix}/bin/xtrace
EOF

###############################################################################
# nss_db, nss_hesiod
###############################################################################

# Move the NSS-related files to the NSS subpackages.  Be careful not
# to pick up .debug files, and the -devel symbolic links.
for module in db hesiod; do
  grep -E "/libnss_$module(\.so\.[0-9.]+|-[0-9.]+\.so)$" \
    master.filelist > nss_$module.filelist
done
grep -E "%{_prefix}/bin/makedb$" master.filelist >> nss_db.filelist

###############################################################################
# nss-devel
###############################################################################

# Symlinks go into the nss-devel package (instead of the main devel
# package).
grep '/libnss_[a-z]*\.so$' master.filelist > nss-devel.filelist

###############################################################################
# libnsl
###############################################################################

# Prepare the libnsl-related file lists.
grep '/libnsl-[0-9.]*.so$' master.filelist > libnsl.filelist
test $(wc -l < libnsl.filelist) -eq 1

%if %{with benchtests}
###############################################################################
# glibc-benchtests
###############################################################################

# List of benchmarks.
find build-%{target}/benchtests -type f -executable | while read b; do
	echo "%{_prefix}/libexec/glibc-benchtests/$(basename $b)"
done >> benchtests.filelist
# ... and the makefile.
for b in %{SOURCE1} %{SOURCE2}; do
	echo "%{_prefix}/libexec/glibc-benchtests/$(basename $b)" >> benchtests.filelist
done
# ... and finally, the comparison scripts.
echo "%{_prefix}/libexec/glibc-benchtests/benchout.schema.json" >> benchtests.filelist
echo "%{_prefix}/libexec/glibc-benchtests/compare_bench.py*" >> benchtests.filelist
echo "%{_prefix}/libexec/glibc-benchtests/import_bench.py*" >> benchtests.filelist
echo "%{_prefix}/libexec/glibc-benchtests/validate_benchout.py*" >> benchtests.filelist
%endif

###############################################################################
# compat-libpthread-nonshared
###############################################################################
echo "%{_libdir}/libpthread_nonshared.a" >> compat-libpthread-nonshared.filelist

##############################################################################
# Run the glibc testsuite
##############################################################################
%check
%if %{with testsuite}

# Run the glibc tests. If any tests fail to build we exit %check with
# an error, otherwise we print the test failure list and the failed
# test output and continue.  Write to standard error to avoid
# synchronization issues with make and shell tracing output if
# standard output and standard error are different pipes.
run_tests () {
  # This hides a test suite build failure, which should be fatal.  We
  # check "Summary of test results:" below to verify that all tests
  # were built and run.
  %make_build check |& tee rpmbuild.check.log >&2
  test -n tests.sum
  if ! grep -q '^Summary of test results:$' rpmbuild.check.log ; then
    echo "FAIL: test suite build of target: $(basename "$(pwd)")" >& 2
    exit 1
  fi
  set +x
  grep -v ^PASS: tests.sum > rpmbuild.tests.sum.not-passing || true
  if test -n rpmbuild.tests.sum.not-passing ; then
    echo ===================FAILED TESTS===================== >&2
    echo "Target: $(basename "$(pwd)")" >& 2
    cat rpmbuild.tests.sum.not-passing >&2
    while read failed_code failed_test ; do
      for suffix in out test-result ; do
        if test -e "$failed_test.$suffix"; then
	  echo >&2
          echo "=====$failed_code $failed_test.$suffix=====" >&2
          cat -- "$failed_test.$suffix" >&2
	  echo >&2
        fi
      done
    done <rpmbuild.tests.sum.not-passing
  fi

  # Unconditonally dump differences in the system call list.
  echo "* System call consistency checks:" >&2
  cat misc/tst-syscall-list.out >&2
  set -x
}

# Increase timeouts
export TIMEOUTFACTOR=16
parent=$$
echo ====================TESTING=========================

# Default libraries.
pushd build-%{target}
run_tests
popd

echo ====================TESTING END=====================
PLTCMD='/^Relocation section .*\(\.rela\?\.plt\|\.rela\.IA_64\.pltoff\)/,/^$/p'
echo ====================PLT RELOCS LD.SO================
readelf -Wr %{glibc_sysroot}/%{_lib}/ld-*.so | sed -n -e "$PLTCMD"
echo ====================PLT RELOCS LIBC.SO==============
readelf -Wr %{glibc_sysroot}/%{_lib}/libc-*.so | sed -n -e "$PLTCMD"
echo ====================PLT RELOCS END==================

# Obtain a way to run the dynamic loader.  Avoid matching the symbolic
# link and then pick the first loader (although there should be only
# one).  See wrap-find-debuginfo.sh.
run_ldso="$(find %{glibc_sysroot}/%{_lib}/ld-*.so -type f | LC_ALL=C sort | head -n1) --library-path %{glibc_sysroot}/%{_lib}"

# Show the auxiliary vector as seen by the new library
# (even if we do not perform the valgrind test).
LD_SHOW_AUXV=1 $run_ldso /bin/true

%if 0%{?_enable_debug_packages}
# Finally, check if valgrind runs with the new glibc.
# We want to fail building if valgrind is not able to run with this glibc so
# that we can then coordinate with valgrind to get it fixed before we update
# glibc.
%if %{with valgrind}
$run_ldso /usr/bin/valgrind --error-exitcode=1 \
	$run_ldso /usr/bin/true
# true --help performs some memory allocations.
$run_ldso /usr/bin/valgrind --error-exitcode=1 \
	$run_ldso /usr/bin/true --help >/dev/null
%endif
%endif

%endif


%pre -p <lua>
-- Check that the running kernel is new enough
required = '%{enablekernel}'
rel = posix.uname("%r")
if rpm.vercmp(rel, required) < 0 then
  error("FATAL: kernel too old", 0)
end

%post -p <lua>
%glibc_post_funcs
-- (1) Remove multilib libraries from previous installs.
-- In order to support in-place upgrades, we must immediately remove
-- obsolete platform directories after installing a new glibc
-- version.  RPM only deletes files removed by updates near the end
-- of the transaction.  If we did not remove the obsolete platform
-- directories here, they may be preferred by the dynamic linker
-- during the execution of subsequent RPM scriptlets, likely
-- resulting in process startup failures.

-- Full set of libraries glibc may install.
install_libs = { "anl", "BrokenLocale", "c", "dl", "m", "mvec",
		 "nss_compat", "nss_db", "nss_dns", "nss_files",
		 "nss_hesiod", "pthread", "resolv", "rt", "SegFault",
		 "thread_db", "util" }

-- We are going to remove these libraries. Generally speaking we remove
-- all core libraries in the multilib directory.
-- For the versioned install names, the version are [2.0,9.9*], so we
-- match "libc-2.0.so" and so on up to "libc-9.9*".
-- For the unversioned install names, we match the library plus ".so."
-- followed by digests.
remove_regexps = {}
for i = 1, #install_libs do
  remove_regexps[#remove_regexps + 1] = ("lib" .. install_libs[i]
                                         .. "%%-[2-9]%%.[0-9]+%%.so$")
end

-- Two exceptions:
remove_regexps[#install_libs + 1] = "libthread_db%%-1%%.0%%.so"
remove_regexps[#install_libs + 2] = "libSegFault%%.so"

-- We are going to search these directories.
local remove_dirs = { "%{_libdir}/i686",
		      "%{_libdir}/i686/nosegneg",
		      "%{_libdir}/power6",
		      "%{_libdir}/power7",
		      "%{_libdir}/power8",
		      "%{_libdir}/power9",
		    }

-- Add all the subdirectories of the glibc-hwcaps subdirectory.
repeat
  local iter = posix.files("%{_libdir}/glibc-hwcaps")
  if iter ~= nil then
    for entry in iter do
      if entry ~= "." and entry ~= ".." then
        local path = "%{_libdir}/glibc-hwcaps/" .. entry
        if posix.access(path .. "/.", "x") then
          remove_dirs[#remove_dirs + 1] = path
        end
      end
    end
  end
until true

-- Walk all the directories with files we need to remove...
for _, rdir in ipairs (remove_dirs) do
  if posix.access (rdir) then
    -- If the directory exists we look at all the files...
    local remove_files = posix.files (rdir)
    for rfile in remove_files do
      for _, rregexp in ipairs (remove_regexps) do
	-- Does it match the regexp?
	local dso = string.match (rfile, rregexp)
        if (dso ~= nil) then
	  -- Removing file...
	  os.remove (rdir .. '/' .. rfile)
	end
      end
    end
  end
end

-- (2) Update /etc/ld.so.conf
-- Next we update /etc/ld.so.conf to ensure that it starts with
-- a literal "include ld.so.conf.d/*.conf".

local ldsoconf = "/etc/ld.so.conf"
local ldsoconf_tmp = "/etc/glibc_post_upgrade.ld.so.conf"

if posix.access (ldsoconf) then

  -- We must have a "include ld.so.conf.d/*.conf" line.
  local have_include = false
  for line in io.lines (ldsoconf) do
    -- This must match, and we don't ignore whitespace.
    if string.match (line, "^include ld.so.conf.d/%%*%%.conf$") ~= nil then
      have_include = true
    end
  end

  if not have_include then
    -- Insert "include ld.so.conf.d/*.conf" line at the start of the
    -- file. We only support one of these post upgrades running at
    -- a time (temporary file name is fixed).
    local tmp_fd = io.open (ldsoconf_tmp, "w")
    if tmp_fd ~= nil then
      tmp_fd:write ("include ld.so.conf.d/*.conf\n")
      for line in io.lines (ldsoconf) do
        tmp_fd:write (line .. "\n")
      end
      tmp_fd:close ()
      local res = os.rename (ldsoconf_tmp, ldsoconf)
      if res == nil then
        io.stdout:write ("Error: Unable to update configuration file (rename).\n")
      end
    else
      io.stdout:write ("Error: Unable to update configuration file (open).\n")
    end
  end
end

-- (3) Rebuild ld.so.cache early.
-- If the format of the cache changes then we need to rebuild
-- the cache early to avoid any problems running binaries with
-- the new glibc.

-- Note: We use _prefix because Fedora's UsrMove says so.
post_exec ("%{_prefix}/sbin/ldconfig")

-- (4) Update gconv modules cache.
-- If the /usr/lib/gconv/gconv-modules.cache exists, then update it
-- with the latest set of modules that were just installed.
-- We assume that the cache is in _libdir/gconv and called
-- "gconv-modules.cache".

update_gconv_modules_cache()

-- (5) On upgrades, restart systemd if installed.  "systemctl -q" does
-- not suppress the error message (which is common in chroots), so
-- open-code post_exec with standard error suppressed.
if tonumber(arg[2]) >= 2
   and posix.access("%{_prefix}/bin/systemctl", "x")
then
  local pid = posix.fork()
  if pid == 0 then
    posix.redirect2null(2)
    assert(posix.exec("%{_prefix}/bin/systemctl", "daemon-reexec"))
  elseif pid > 0 then
    posix.wait(pid)
  end
end

%posttrans all-langpacks -e -p <lua>
-- The old glibc-all-langpacks postun scriptlet deleted the locale-archive
-- file, so we may have to resurrect it on upgrades.
local archive_path = "%{_prefix}/lib/locale/locale-archive"
local real_path = "%{_prefix}/lib/locale/locale-archive.real"
local stat_archive = posix.stat(archive_path)
local stat_real = posix.stat(real_path)
-- If the hard link was removed, restore it.
if stat_archive ~= nil and stat_real ~= nil
    and (stat_archive.ino ~= stat_real.ino
         or stat_archive.dev ~= stat_real.dev) then
  posix.unlink(archive_path)
  stat_archive = nil
end
-- If the file is gone, restore it.
if stat_archive == nil then
  posix.link(real_path, archive_path)
end
-- Remove .rpmsave file potentially created due to config file change.
local save_path = archive_path .. ".rpmsave"
if posix.access(save_path) then
  posix.unlink(save_path)
end

%post gconv-extra -p <lua>
%glibc_post_funcs
update_gconv_modules_cache ()

%postun gconv-extra -p <lua>
%glibc_post_funcs
update_gconv_modules_cache ()

%files -f glibc.filelist
%dir %{_prefix}/%{_lib}/audit
%verify(not md5 size mtime) %config(noreplace) /etc/ld.so.conf
%verify(not md5 size mtime) %config(noreplace) /etc/rpc
%dir /etc/ld.so.conf.d
%dir %{_prefix}/libexec/getconf
%dir %{_libdir}/gconv
%dir %{_libdir}/gconv/gconv-modules.d
%dir %attr(0700,root,root) /var/cache/ldconfig
%attr(0600,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /var/cache/ldconfig/aux-cache
%attr(0644,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /etc/ld.so.cache
%attr(0644,root,root) %verify(not md5 size mtime) %ghost %config(missingok,noreplace) /etc/gai.conf
# If rpm doesn't support %license, then use %doc instead.
%{!?_licensedir:%global license %%doc}
%license COPYING COPYING.LIB LICENSES

%files -f common.filelist common
%dir %{_prefix}/lib/locale
%dir %{_prefix}/lib/locale/C.utf8
%{_prefix}/lib/locale/C.utf8/*

%files all-langpacks
%{_prefix}/lib/locale/locale-archive
%{_prefix}/lib/locale/locale-archive.real
%{_prefix}/share/locale/*/LC_MESSAGES/libc.mo

%files locale-source
%dir %{_prefix}/share/i18n/locales
%{_prefix}/share/i18n/locales/*
%dir %{_prefix}/share/i18n/charmaps
%{_prefix}/share/i18n/charmaps/*

%files -f devel.filelist devel
%if %{glibc_autorequires}
%attr(0755,root,root) %{_rpmconfigdir}/glibc.req
%{_fileattrsdir}/glibc.attr
%endif

%if %{with docs}
%files -f doc.filelist doc
%endif

%files -f static.filelist static

%if  %{need_headers_package}
%files -f headers.filelist -n %{headers_package_name}
%endif

%files -f utils.filelist utils

%files -f gconv.filelist gconv-extra

%files -f nss_db.filelist -n nss_db
/var/db/Makefile
%files -f nss_hesiod.filelist -n nss_hesiod
%doc hesiod/README.hesiod
%files -f nss-devel.filelist nss-devel

%files -f libnsl.filelist -n libnsl
/%{_lib}/libnsl.so.1

%if %{with benchtests}
%files benchtests -f benchtests.filelist
%endif

%files -f compat-libpthread-nonshared.filelist -n compat-libpthread-nonshared

%changelog
* Sat Feb 04 2023 Carlos O'Donell <carlos@redhat.com> - 2.37-1
- Drop already included glibc-dprintf-length.patch patch.
- Apply glibc-printf-grouping-swbz30068.patch to fix swbz#30068.
- Auto-sync with upstream branch release/2.37/master,
  commit a704fd9a133bfb10510e18702f48a6a9c88dbbd5:
- Create ChangeLog.old/ChangeLog.26. (tag: glibc-2.37)
- Prepare for glibc 2.37 release.
- x86: Fix strncat-avx2.S reading past length [BZ #30065]
- Update install.texi, and regenerate INSTALL.
- Update manual/contrib.texi.
- Update NEWS file with bug fixes.
- Regenerate configure.
- Update all PO files in preparation for release.
- doc: correct _FORTIFY_SOURCE doc in features.h
- libio: Update number of written bytes in dprintf implementation

* Tue Jan 31 2023 Florian Weimer <fweimer@redhat.com> - 2.36.9000-25
- Apply glibc-dprintf-length.patch to fix dprintf return value regression.
- Auto-sync with upstream branch master,
  commit 2f39e44a8417b4186a7f15bfeac5d0b557e63e03:
- Account for octal marker in %#o format (rhbz#2165869)
- Use binutils 2.40 branch in build-many-glibcs.py
- Use MPFR 4.2.0, MPC 1.3.1 in build-many-glibcs.py

* Wed Jan 25 2023 Florian Weimer <fweimer@redhat.com> - 2.36.9000-24
- Auto-sync with upstream branch master,
  commit 0d50f477f47ba637b54fb03ac48d769ec4543e8d:
- stdio-common: Handle -1 buffer size in __sprintf_chk & co (bug 30039)
- Document '%F' format specifier
- sparc (64bit): Regenerate ulps
- ia64: Regenerate ulps
- Update libc.pot for 2.37 release.
- x86: Cache computation for AMD architecture.
- manual: Fix typo
- Add STATX_DIOALIGN from Linux 6.1 to bits/statx-generic.h
- Add IPPROTO_L2TP from Linux 6.1 to netinet/in.h
- AArch64: Improve strrchr
- AArch64: Optimize strnlen
- AArch64: Optimize strlen
- AArch64: Optimize strcpy
- AArch64: Improve strchrnul
- AArch64: Optimize strchr
- AArch64: Improve strlen_asimd
- AArch64: Optimize memrchr
- AArch64: Optimize memchr

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.36.9000-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Jan 17 2023 Florian Weimer <fweimer@redhat.com> - 2.36.9000-22
- Auto-sync with upstream branch master,
  commit 569cfcc6bf35c28112ca8d7112e9eb4a22bed5b8:
- hurd: Fix _NOFLSH value
- elf: Fix GL(dl_phdr) and GL(dl_phnum) for static builds [BZ #29864]
- string: Suppress -Wmaybe-unitialized for wordcopy [BZ #19444]
- scripts/build-many-glibcs.py: Remove unused RANLIB and STRIP option
- configure: Move nm, objdump, and readelf to LIBC_PROG_BINUTILS

* Wed Jan 11 2023 Patsy Griffin <patsy@redhat.com> - 2.36.9000-21
- Auto-sync with upstream branch master,
  commit 2d2d7e1a8f2e62b442ae8978f0a6c17f385575c4.
- configure: Allow user override LD, AR, OBJCOPY, and GPROF
- math: Suppress -O0 warnings for soft-fp fsqrt [BZ #19444]
- sunrpc: Suppress GCC -O1 warning on user2netname [BZ #19444]
- locale: Use correct buffer size for utf8_sequence_error [BZ #19444]
- Add HWCAP2_SVE_EBF16 from Linux 6.1 to AArch64 bits/hwcap.h
- Add _FORTIFY_SOURCE implementation documentation [BZ #28998]
- Update copyright dates not handled by scripts/update-copyrights
- Update copyright dates with scripts/update-copyrights
- Remove trailing whitespace in gmp.h
- Remove trailing whitespace
- C2x semantics for <tgmath.h>
- time: Set daylight to 1 for matching DST/offset change (bug 29951)
- Fix ldbl-128 built-in function use
- x86: Check minimum/maximum of non_temporal_threshold [BZ #29953]
- i686: Regenerate ulps

* Mon Jan 02 2023 Arjun Shankar <arjun@redhat.com> - 2.36.9000-20
- Drop glibc-rh2155825.patch; fix applied upstream, and
- Auto-sync with upstream branch master,
  commit 5f55b22f4b3ea14c777a60f239d25dc4555eb804:
- hurd getcwd: Fix memory leak on error
- hurd fcntl: Make LOCKED macro more robust
- hurd: Make dl-sysdep __sbrk check __vm_allocate call
- htl: Drop duplicate check in __pthread_stack_alloc
- hurd hurdstartup: Initialize remaining fields of hurd_startup_data
- hurd _S_msg_add_auth: Initialize new arrays to 0
- htl: Check error returned by __getrlimit
- getdelim: ensure error indicator is set on error (bug 29917)
- htl: Fix sem_wait race between read and gsync_wait
- Avoid use of atoi in malloc
- Linux: Pass size argument of epoll_create to the kernel
- Simplify scripts/cross-test-ssh.sh configuration.
- Define MADV_COLLAPSE from Linux 6.1
- powerpc64: Increase SIGSTKSZ and MINSIGSTKSZ
- Update all PO files in preparation for release.
- Update kernel version to 6.1 in header constant tests
- Update syscall lists for Linux 6.1
- libio: Convert __vswprintf_internal to buffers (bug 27857)
- libio: Convert __obstack_vprintf_internal to buffers (bug 27124)
- libio: Convert __vdprintf_internal to buffers
- libio: Convert __vasprintf_internal to buffers
- libio: Convert __vsprintf_internal to buffers
- stdio-common: Add lock optimization to vfprintf and vfwprintf
- stdio-common: Convert vfprintf and related functions to buffers
- stdio-common: Add __translated_number_width
- stdio-common: Add __printf_function_invoke
- stdio-common: Introduce buffers for implementing printf
- locale: Implement struct grouping_iterator
- Use Linux 6.1 in build-many-glibcs.py
- Avoid use of atoi in some places in libc

* Thu Dec 22 2022 Florian Weimer <fweimer@redhat.com> - 2.36.9000-19
- Fix epoll_create regression (#2155825)

* Mon Dec 19 2022 Florian Weimer <fweimer@redhat.com> - 2.36.9000-18
- Auto-sync with upstream branch master,
  commit c1c0dea38833751f36a145c322ce53c9a08332e1:
- Linux: Remove epoll_create, inotify_init from syscalls.list (#2154747)
- Linux: Reflow and sort some Makefile variables
- mach: Drop remnants of old_CFLAGS
- mach: Fix passing -ffreestanding when checking for gnumach headers
- Force use of -ffreestanding when checking for gnumach headers
- elf: Fix tst-relro-symbols.py argument passing
- x86: Prevent SIGSEGV in memcmp-sse2 when data is concurrently modified [BZ #29863]
- Allow _Qp_fgt in sparc64 localplt.data

* Mon Dec 12 2022 DJ Delorie <dj@redhat.com> - 2.36.9000-17
- Auto-sync with upstream branch master,
  commit 5dcd2d0ad02ff12c76355ef4f40947c1857ac482.
- stdlib: Move _IO_cleanup to call_function_static_weak
- elf: Do not assume symbol order on tst-audit25{a,b}
- time: Use 64 bit time on tzfile
- nscd: Use 64 bit time_t on libc nscd routines (BZ# 29402)
- nis: Build libnsl with 64 bit time_t
- realloc: Return unchanged if request is within usable size
- Linux: Consolidate typesizes.h
- Linux: Make generic fcntl.h the default one
- Linux: make generic xstatver.h the default one
- Linux: Remove generic sysdep
- Linux: Assume and consolidate shutdown wire-up syscall
- Linux: Assume and consolidate listen wire-up syscall
- Linux: Assume and consolidate socketpair wire-up syscall
- Linux: Assume and consolidate socket wire-up syscall
- Linux: Assume and consolidate bind wire-up syscall
- Linux: consolidate ____longjmp_chk
- Linux: consolidate sendfile implementation
- Linux: consolidate unlink implementation
- Linux: consolidate symlink implementation
- Linux: consolidate rmdir implementation
- Linux: consolidate readlink implementation
- Linux: consolidate mkdir implementation
- Linux: consolidate link implementation
- Linux: consolidate lchown implementation
- Linux: consolidate inotify_init implementation
- Lninux: consolidate epoll_create implementation
- Linux: consolidate dup2 implementation
- Linux: consolidate chown implementation
- Linux: consolidate chmod implementation
- linux: Consolidate dl-origin.c
- linux: Use long int for syscall return value
- LoongArch: Use medium cmodel build libc_nonshared.a.
- x86_64: State assembler is being tested on sysdeps/x86/configure
- configure: Remove AS check
- configure: Remove check if ld is GNU
- configure: Remove check if as is GNU
- configure: Move locale tools early

* Mon Dec 05 2022 Arjun Shankar <arjun@redhat.com> - 2.36.9000-16
- Auto-sync with upstream branch master,
  commit 8fb923ddc38dd5f4bfac4869d70fd80483fdb87a:
- hurd: Make getrandom cache the server port
- powerpc64: Remove old strncmp optimization
- x86-64 strncpy: Properly handle the length parameter [BZ# 29839]
- x86-64 strncat: Properly handle the length parameter [BZ# 24097]
- ARC: update definitions in elf/elf.h
- scripts: Add "|" operator support to glibcpp's parsing
- Apply asm redirections in syslog.h before first use [BZ #27087]
- LoongArch: Add support for ilogb[f]
- LoongArch: Add support for scalb[f]
- LoongArch: Add support for scalbn[f]
- LoongArch: Use __builtin_logb{,f} with GCC >= 13
- Use GCC builtins for logb functions if desired.
- LoongArch: Use __builtin_llrint{,f} with GCC >= 13
- Use GCC builtins for llrint functions if desired.
- LoongArch: Use __builtin_lrint{,f} with GCC >= 13
- Use GCC builtins for lrint functions if desired.
- LoongArch: Use __builtin_rint{,f} with GCC >= 13

* Mon Nov 28 2022 Florian Weimer <fweimer@redhat.com> - 2.36.9000-15
- Auto-sync with upstream branch master,
  commit f704192911c6c7b65a54beab3ab369fca7609a5d:
- x86/fpu: Factor out shared avx2/avx512 code in svml_{s|d}_wrapper_impl.h
- x86/fpu: Cleanup code in svml_{s|d}_wrapper_impl.h
- x86/fpu: Reformat svml_{s|d}_wrapper_impl.h
- x86/fpu: Fix misspelled evex512 section in variety of svml files
- x86/fpu: Add missing ISA sections to variety of svml files
- stdio-common: Add missing dependencies (bug 29780)
- i386: Avoid rely on linker optimization to avoid relocation
- elf: Fix rtld-audit trampoline for aarch64
- Define in_int32_t_range to check if the 64 bit time_t syscall should be used

* Mon Nov 14 2022 Arjun Shankar <arjun@redhat.com> - 2.36.9000-14
- Auto-sync with upstream branch master,
  commit 94628de77888c3292fc103840731ff85f283368e:
- elf/tst-tlsopt-powerpc fails when compiled with -mcpu=power10 (BZ# 29776)
- LoongArch: Hard Float Support for fmaximum_mag_num{f/ }, fminimum_mag_num{f/ }.
- LoongArch: Hard Float Support for fmaximum_mag{f/ }, fminimum_mag{f/ }.
- LoongArch: Hard Float Support for fmaxmag{f/ }, fminmag{f/ }.
- LoongArch: Hard Float Support for fmaximum_num{f/ }, fminimum_num{f/ }.
- LoongArch: Hard Float Support for fmaximum{f/ }, fminimum{f/ }.
- LoongArch: Hard Float Support for float-point classification functions.
- LoongArch: Use __builtin_{fma, fmaf} to implement function {fma, fmaf}.

* Thu Nov 10 2022 Florian Weimer <fweimer@redhat.com> - 2.36.9000-13
- Auto-sync with upstream branch master,
  commit 22a46dee24351fd5f4f188ad80554cad79c82524:
- Linux: Support __IPC_64 in sysvctl *ctl command arguments (bug 29771)
- mktime: improve heuristic for ca-1986 Indiana DST
- Makerules: fix MAKEFLAGS assignment for upcoming make-4.4 [BZ# 29564]
- LoongArch: Fix ABI related macros in elf.h to keep consistent with binutils[1].
- linux: Fix fstatat on MIPSn64 (BZ #29730)
- longlong.h: update from GCC for LoongArch clz/ctz support
- elf: Reinstate on DL_DEBUG_BINDINGS _dl_lookup_symbol_x
- linux: Fix generic struct_stat for 64 bit time (BZ# 29657)
- Avoid undefined behaviour in ibm128 implementation of llroundl (BZ #29488)
- Fix BZ #29463 in the ibm128 implementation of y1l too
- elf: Do not completely clear reused namespace in dlmopen (bug 29600)
- nss: Use shared prefix in IPv4 address in tst-reload1
- nss: Fix tst-nss-files-hosts-long on single-stack hosts (bug 24816)
- nss: Implement --no-addrconfig option for getent
- Ensure calculations happen with desired rounding mode in y1lf128

* Mon Oct 17 2022 Carlos O'Donell <carlos@redhat.com> - 2.36-7
- Enable ELF DT_HASH for shared objects and the dynamic loader (#2129358)

* Fri Oct 07 2022 Arjun Shankar <arjun@redhat.com> - 2.36-6
- Auto-sync with upstream branch release/2.36/master,
  commit 2bd815d8347851212b9a91dbdca8053f4dbdac87:
- nscd: Drop local address tuple variable [BZ #29607]
- x86-64: Require BMI1/BMI2 for AVX2 strrchr and wcsrchr implementations
- x86-64: Require BMI2 and LZCNT for AVX2 memrchr implementation
- x86-64: Require BMI2 for AVX2 (raw|w)memchr implementations
- x86-64: Require BMI2 for AVX2 wcs(n)cmp implementations
- x86-64: Require BMI2 for AVX2 strncmp implementation
- x86-64: Require BMI2 for AVX2 strcmp implementation
- x86-64: Require BMI2 for AVX2 str(n)casecmp implementations
- x86: include BMI1 and BMI2 in x86-64-v3 level
- hppa: undef __ASSUME_SET_ROBUST_LIST
- hppa: Fix initialization of dp register [BZ 29635]
- stdlib: Fix __getrandom_nocancel type and arc4random usage (BZ #29638)
- get_nscd_addresses: Fix subscript typos [BZ #29605]
- m68k: Enforce 4-byte alignment on internal locks (BZ #29537)
- gconv: Use 64-bit interfaces in gconv_parseconfdir (bug 29583)
- elf: Implement force_first handling in _dl_sort_maps_dfs (bug 28937)
- elf: Rename _dl_sort_maps parameter from skip to force_first
- scripts/dso-ordering-test.py: Generate program run-time dependencies
- elf: Fix hwcaps string size overestimation

* Fri Sep 23 2022 Florian Weimer <fweimer@redhat.com> - 2.36-5
- Remove .annobin* symbols from ld.so (#2126477)

* Wed Sep 14 2022 Florian Weimer <fweimer@redhat.com> - 2.36-4
- Auto-sync with upstream branch release/2.36/master,
  commit df51334828f2af214105aad82042140ee3a6de0a:
- elf: Run tst-audit-tlsdesc, tst-audit-tlsdesc-dlopen everywhere
- NEWS: Note bug 12154 and bug 29305 as fixed
- resolv: Fix building tst-resolv-invalid-cname for earlier C standards
- nss_dns: Rewrite _nss_dns_gethostbyname4_r using current interfaces
- resolv: Add new tst-resolv-invalid-cname
- nss_dns: In gaih_getanswer_slice, skip strange aliases (bug 12154)
- nss_dns: Rewrite getanswer_r to match getanswer_ptr (bug 12154, bug 29305)
- nss_dns: Remove remnants of IPv6 address mapping
- nss_dns: Rewrite _nss_dns_gethostbyaddr2_r and getanswer_ptr
- nss_dns: Split getanswer_ptr from getanswer_r
- resolv: Add DNS packet parsing helpers geared towards wire format
- resolv: Add internal __ns_name_length_uncompressed function
- resolv: Add the __ns_samebinaryname function
- resolv: Add internal __res_binary_hnok function
- resolv: Add tst-resolv-aliases
- resolv: Add tst-resolv-byaddr for testing reverse lookup
- nscd: Fix netlink cache invalidation if epoll is used [BZ #29415]
- Add NEWS entry for CVE-2022-39046
- syslog: Remove extra whitespace between timestamp and message (BZ#29544)
- elf: Restore how vDSO dependency is printed with LD_TRACE_LOADED_OBJECTS (BZ #29539)
- Apply asm redirections in wchar.h before first use (rhbz#2115752)
- elf: Call __libc_early_init for reused namespaces (bug 29528)
- syslog: Fix large messages (BZ#29536)
- Linux: Fix enum fsconfig_command detection in <sys/mount.h> (rhbz#2126522)
- linux: Fix sys/mount.h usage with kernel headers (rhbz#2126522)
- linux: Use compile_c_snippet to check linux/mount.h availability
- linux: Mimic kernel defition for BLOCK_SIZE
- linux: Use compile_c_snippet to check linux/pidfd.h availability
- glibcextract.py: Add compile_c_snippet

* Tue Sep 06 2022 Arjun Shankar <arjun@redhat.com> - 2.36-3
- Co-Authored-By: Benjamin Herrenschmidt <benh@amazon.com>
- Retain .gnu_debuglink section in libc.so.6 (#2090744)
- Remove redundant ld.so debuginfo file (#2090744)

* Tue Aug 23 2022 Arjun Shankar <arjun@redhat.com> - 2.36-2
- Auto-sync with upstream branch release/2.36/master,
  commit 5c62874f423af93e97b51bc9a57af228a546156f:
- NEWS: Add entry for bug 28846
- socket: Check lengths before advancing pointer in CMSG_NXTHDR
- alpha: Fix generic brk system call emulation in __brk_call (bug 29490)
- Linux: Terminate subprocess on late failure in tst-pidfd (bug 29485)
- elf: Replace `strcpy` call with `memcpy` [BZ #29454]
- Update syscall lists for Linux 5.19
- dlfcn: Pass caller pointer to static dlopen implementation (bug 29446)

* Wed Aug 03 2022 Carlos O'Donell <carlos@redhat.com> - 2.36-1
- Auto-sync with upstream branch release/2.36/master,
  commit 33f1b4c1452b33991e670f636ebe98b90a405e10:
- wcsmbs: Add missing test-c8rtomb/test-mbrtoc8 dependency
- stdlib: Suppress gcc diagnostic that char8_t is a keyword in C++20 in uchar.h.
- Create ChangeLog.old/ChangeLog.25. (tag: glibc-2.36)
- Prepare for glibc 2.36 release.
- Update install.texi, and regenerate INSTALL.
- Update NEWS bug list.
- Update libc.pot for 2.36 release.
- tst-pidfd.c: UNSUPPORTED if we get EPERM on valid pidfd_getfd call
- stdlib: Tuned down tst-arc4random-thread internal parameters
- LoongArch: Add greg_t and gregset_t.
- LoongArch: Fix VDSO_HASH and VDSO_NAME.
- riscv: Update rv64 libm test ulps
- riscv: Update nofpu libm test ulps

* Wed Jul 27 2022 Arjun Shankar <arjun@redhat.com> - 2.35.9000-32
- Auto-sync with upstream branch master,
  commit eaad4f9e8f07fc43618f6c8635a7e82831a423dd:
- arc4random: simplify design for better safety
- LoongArch: Update NEWS and README for the LoongArch port.
- LoongArch: Update build-many-glibcs.py for the LoongArch Port.
- LoongArch: Hard Float Support
- LoongArch: Build Infrastructure
- LoongArch: Add ABI Lists
- LoongArch: Linux ABI
- LoongArch: Linux Syscall Interface
- LoongArch: Atomic and Locking Routines
- LoongArch: Generic <math.h> and soft-fp Routines
- LoongArch: Thread-Local Storage Support
- LoongArch: ABI Implementation
- LoongArch: Add relocations and ELF flags to elf.h and scripts/glibcelf.py
- LoongArch: Add LoongArch entries to config.h.in
- struct stat is not posix conformant on microblaze with __USE_FILE_OFFSET64
- Linux: dirent/tst-readdir64-compat needs to use TEST_COMPAT (bug 27654)
- manual: Add documentation for arc4random functions
- s390x: Add optimized chacha20
- powerpc64: Add optimized chacha20
- x86: Add AVX2 optimized chacha20
- x86: Add SSE2 optimized chacha20
- aarch64: Add optimized chacha20
- benchtests: Add arc4random benchtest
- stdlib: Add arc4random tests
- stdlib: Add arc4random, arc4random_buf, and arc4random_uniform (BZ #4417)
- locale: Optimize tst-localedef-path-norm
- malloc: Simplify implementation of __malloc_assert
- Update scripts/config.* files from upstream GNU config version
- linux: return UNSUPPORTED from tst-mount if entering mount namespace fails

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.35.9000-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sun Jul 17 2022 Patsy Griffin <patsy@redhat.com> - 2.35.9000-30
- Auto-sync with upstream branch master,
  commit 49889fb256a7f9b894b2d16fea23de1ac25b65e2.
- x86: Add support to build st{p|r}{n}{cpy|cat} with explicit ISA level
- x86: Add support to build wcscpy with explicit ISA level
- x86: Add support to build strcmp/strlen/strchr with explicit ISA level
- elf: Fix wrong fscanf usage on tst-pldd
- Apply asm redirections in stdio.h before first use [BZ #27087]
- S390: Define SINGLE_THREAD_BY_GLOBAL only on s390x
- x86: Add missing rtm tests for strcmp family
- x86: Remove unneeded rtld-wmemcmp
- x86: Move wcslen SSE2 implementation to multiarch/wcslen-sse2.S
- x86: Move wcschr SSE2 implementation to multiarch/wcschr-sse2.S
- x86: Move strcat SSE2 implementation to multiarch/strcat-sse2.S
- x86: Move strchr SSE2 implementation to multiarch/strchr-sse2.S
- x86: Move strrchr SSE2 implementation to multiarch/strrchr-sse2.S
- x86: Move memrchr SSE2 implementation to multiarch/memrchr-sse2.S
- x86: Move strcpy SSE2 implementation to multiarch/strcpy-sse2.S
- x86: Move strlen SSE2 implementation to multiarch/strlen-sse2.S
- x86: Move strcmp SSE42 implementation to multiarch/strcmp-sse4_2.S
- x86: Move wcscmp SSE2 implementation to multiarch/wcscmp-sse2.S
- x86: Move strcmp SSE2 implementation to multiarch/strcmp-sse2.S
- x86: Rename STRCASECMP_NONASCII macro to STRCASECMP_L_NONASCII
- nptl: Fix ___pthread_unregister_cancel_restore asynchronous restore
- x86: Remove __mmask intrinsics in strstr-avx512.c
- x86: Remove generic strncat, strncpy, and stpncpy implementations
- i386: Remove -Wa,-mtune=i686
- x86-64: Remove redundant strcspn-generic/strpbrk-generic/strspn-generic
- elf: Rename tst-audit26 to tst-audit28
- x86-64: Don't mark symbols as hidden in strcmp-XXX.S
- stdlib: Tests for mbrtoc8, c8rtomb, and the char8_t typedef.
- stdlib: Implement mbrtoc8, c8rtomb, and the char8_t typedef.
- gconv: Correct Big5-HKSCS conversion to preserve all state bits. [BZ #25744]
- aarch64: Optimize string functions with shrn instruction
- test-container: return UNSUPPORTED for ENOSPC on clone()
- x86: Add support for building {w}memcmp{eq} with explicit ISA level
- x86: Add support for building {w}memset{_chk} with explicit ISA level
- x86: Add support for building {w}memmove{_chk} with explicit ISA level
- x86: Add support for building str{c|p}{brk|spn} with explicit ISA level
- x86: Add comment explaining no Slow_SSE4_2 check in ifunc-sse4_2
- Replace __libc_multiple_threads with __libc_single_threaded
- linux: Add mount_setattr
- linux: Add tst-mount to check for Linux new mount API
- linux: Add open_tree
- linux: Add fspick
- linux: Add fsconfig
- AArch64: Reset HWCAP2_AFP bits in FPCR for default fenv
- elf: Fix direction of NODELETE log messages during symbol lookup

* Fri Jul  8 2022 Stephen Gallagher <sgallagh@redhat.com> - 2.35.9000-29
- Modify glibc autorequires to exclude %%dist

* Tue Jul  5 2022 Florian Weimer <fweimer@redhat.com> - 2.35.9000-28
- ppc64le: Increase Clang compatibility of float128 redirects (#2100546)

* Tue Jul 05 2022 Florian Weimer <fweimer@redhat.com> - 2.35.9000-27
- Auto-sync with upstream branch master,
  commit 7519dee356a0ab21c8990e59ed05dd48a4e573a0:
- malloc: Simplify checked_request2size interface
- stdlib: Simplify buffer management in canonicalize
- localedef: Support building for older C standards
- de_DE: Convert to UTF-8
- locale: localdef input files are now encoded in UTF-8
- locale: Introduce translate_unicode_codepoint into linereader.c
- locale: Fix signed char bug in lr_getc
- locale: Turn ADDC and ADDS into functions in linereader.c
- libc-symbols.h: remove unused macros

* Mon Jul 04 2022 Carlos O'Donell <carlos@redhat.com> - 2.35.9000-26
- Auto-sync with upstream branch master,
  commit 8ee2c043cfb35c48b45c7c5aed4022a8a7352bdc.
- Fix hurd namespace issues for internal signal functions
- argp: Remove old includes in !_LIBC case
- Use GCC 12 branch in build-many-glibcs.py
- Refactor internal-signals.h
- riscv: Use memcpy to handle unaligned access when fixing R_RISCV_RELATIVE
- AArch64: Add asymmetric faulting mode for tag violations in mem.tagging tunable
- linux: Fix mq_timereceive check for 32 bit fallback code (BZ 29304)
- x86: Add missing IS_IN (libc) check to strncmp-sse4_2.S
- x86: Add missing IS_IN (libc) check to strcspn-sse4.c
- x86: Add missing IS_IN (libc) check to memmove-ssse3.S
- x86-64: Properly indent X86_IFUNC_IMPL_ADD_VN arguments
- x86-64: Small improvements to dl-trampoline.S
- x86: Move mem{p}{mov|cpy}_{chk_}erms to its own file
- x86: Move and slightly improve memset_erms
- x86: Add definition for __wmemset_chk AVX2 RTM in ifunc impl list
- linux: Remove unnecessary nice.c and signal.c
- nptl: Remove unused members from struct pthread
- Linux: Forward declaration of struct iovec for process_madvise
- x86: Add more feature definitions to isa-level.h

* Wed Jun 29 2022 DJ Delorie <dj@redhat.com> - 2.35.9000-25
- Rebuild for fixed CI test for bz699724

* Tue Jun 28 2022 DJ Delorie <dj@redhat.com> - 2.35.9000-24
- Auto-sync with upstream branch master,
  commit a3563f3f369878467dd74aeb360448119a7a4b41.
- elf: Fix -DNDEBUG warning in _dl_start_args_adjust
- elf: Fix compile error with -Werror and -DNDEBUG
- x86-64: Only define used SSE/AVX/AVX512 run-time resolvers
- x86: Move CPU_FEATURE{S}_{USABLE|ARCH}_P to isa-level.h
- x86: Fix backwards Prefer_No_VZEROUPPER check in ifunc-evex.h
- x86: Rename strstr_sse2 to strstr_generic as it uses string/strstr.c
- x86: Remove unused file wmemcmp-sse4
- x86: Put wcs{n}len-sse4.1 in the sse4.1 text section
- x86: Align entry for memrchr to 64-bytes.
- Makerules: Remove no-op -Wl,-d when linking libc_pic.os
- m68k: optimize RTLD_START
- misc: Optimize internal usage of __libc_single_threaded
- linux: Add move_mount
- linux: Add fsmount
- linux: Add fsopen
- resolv/tst-resolv-noaaaa: Support building for older C standards
- resolv: Implement no-aaaa stub resolver option
- support: Change non-address output format of support_format_dns_packet
- riscv: Use elf_machine_rela_relative to handle R_RISCV_RELATIVE
- x86: Remove faulty sanity tests for RTLD build with no multiarch
- stdlib: Fixup mbstowcs NULL __dst handling. [BZ #29279]
- x86: Replace all sse instructions with vex equivilent in avx+ files
- x86: Add support for compiling {raw|w}memchr with high ISA level
- x86: Add defines / utilities for making ISA specific x86 builds
- stdlib: Remove attr_write from mbstows if dst is NULL [BZ: 29265]
- stdlib: Remove trailing whitespace from Makefile
- debug: make __read_chk a cancellation point (bug 29274)
- s390: use LC_ALL=C for readelf call
- s390: use $READELF

* Mon Jun 20 2022 Arjun Shankar <arjun@redhat.com> - 2.35.9000-23
- Auto-sync with upstream branch master,
  commit e5446dfea11e969212939197b606424a718d9b65:
- i386: Fix include paths for strspn, strcspn, and strpbrk
- elf: Silence GCC 11/12 false positive warning
- x86: Rename generic functions with unique postfix for clarity
- x86: Add BMI1/BMI2 checks for ISA_V3 check
- x86-64: Handle fewer relocation types for RTLD_BOOTSTRAP
- aarch64: Handle fewer relocations for RTLD_BOOTSTRAP
- riscv: Change the relocations handled for RTLD_BOOTSTRAP
- x86: Cleanup bounds checking in large memcpy case
- x86: Add bounds `x86_non_temporal_threshold`
- Remove remnant reference to ELF_RTYPE_CLASS_EXTERN_PROTECTED_DATA
- elf: Remove ELF_RTYPE_CLASS_EXTERN_PROTECTED_DATA
- x86: Add sse42 implementation to strcmp's ifunc
- x86: Fix misordered logic for setting `rep_movsb_stop_threshold`
- elf: Refine direct extern access diagnostics to protected symbol
- Avoid -Wstringop-overflow= warning in iconv module.
- Add bounds check to __libc_ifunc_impl_list
- libio: Avoid RMW of flags2 outside lock (BZ #27842)
- x86: Optimize svml_s_tanhf4_core_sse4.S
- x86: Optimize svml_s_tanhf8_core_avx2.S
- x86: Add data file that can be shared by tanhf-avx2 and tanhf-sse4
- x86: Optimize svml_s_tanhf16_core_avx512.S
- x86: Improve svml_s_atanhf4_core_sse4.S
- x86: Improve svml_s_atanhf8_core_avx2.S
- x86: Improve svml_s_atanhf16_core_avx512.S
- x86: Align varshift table to 32-bytes
- x86: Add copyright to strpbrk-c.c

* Thu Jun 09 2022 Florian Weimer <fweimer@redhat.com> - 2.35.9000-22
- Auto-sync with upstream branch master,
  commit ace9e3edbca62d978b1e8f392d8a5d78500272d9:
- nss: handle stat failure in check_reload_and_get (BZ #28752)
- nss: add assert to DB_LOOKUP_FCT (BZ #28752)
- x86: Fix page cross case in rawmemchr-avx2 [BZ #29234]
- nptl_db: disable DT_RELR on libthread_db.so
- elf: add missing newlines in lateglobal test
- nptl: Fix __libc_cleanup_pop_restore asynchronous restore (BZ#29214)
- x86: ZERO_UPPER_VEC_REGISTERS_RETURN_XTEST expect no transactions
- x86: Shrink code size of memchr-evex.S
- x86: Shrink code size of memchr-avx2.S
- x86: Optimize memrchr-avx2.S
- x86: Optimize memrchr-evex.S
- x86: Optimize memrchr-sse2.S
- Benchtests: Improve memrchr benchmarks
- x86: Add COND_VZEROUPPER that can replace vzeroupper if no `ret`
- x86: Create header for VEC classes in x86 strings library
- powerpc: Fix VSX register number on __strncpy_power9 [BZ #29197]
- AArch64: Sort makefile entries
- AArch64: Add SVE memcpy
- x86_64: Add strstr function with 512-bit EVEX
- scripts/glibcelf.py: Add PT_AARCH64_MEMTAG_MTE constant

* Mon Jun 06 2022 Carlos O'Donell <carlos@redhat.com> - 2.35.9000-21
- Auto-sync with upstream branch master,
  commit 999835533bc60fbd0b0b65d2412a6742e5a54b9d:
- socket: Fix mistyped define statement in socket/sys/socket.h (BZ #29225)
- Declare timegm for ISO C2X
- Add PT_AARCH64_MEMTAG_MTE from Linux 5.18 to elf.h
- grep: egrep -> grep -E, fgrep -> grep -F
- string.h: Fix boolean spelling in comments
- elf: Add #include <errno.h> for use of E* constants.
- elf: Add #include <sys/param.h> for MAX usage.
- linux: Add process_mrelease
- linux: Add process_madvise
- linux: Set tst-pidfd-consts unsupported for kernels headers older than 5.10
- testrun.sh: Support passing strace and valgrind arguments
- Linux: Adjust struct rseq definition to current kernel version
- iconv: Use 64 bit stat for gconv_parseconfdir (BZ# 29213)
- catgets: Use 64 bit stat for __open_catalog (BZ# 29211)
- inet: Use 64 bit stat for ruserpass (BZ# 29210)
- socket: Use 64 bit stat for isfdtype (BZ# 29209)
- posix: Use 64 bit stat for fpathconf (_PC_ASYNC_IO) (BZ# 29208)
- posix: Use 64 bit stat for posix_fallocate fallback (BZ# 29207)
- misc: Use 64 bit stat for getusershell (BZ# 29203)
- misc: Use 64 bit stat for daemon (BZ# 29203)
- linux: use statx for fstat if neither newfstatat nor fstatat64 is present
- Add MADV_DONTNEED_LOCKED from Linux 5.18 to bits/mman-linux.h
- Add HWCAP2_MTE3 from Linux 5.18 to AArch64 bits/hwcap.h
- i686: Use generic sincosf implementation for SSE2 version
- benchtests: Add workload name for sincosf
- i686: Use generic sinf implementation for SSE2 version
- i686: Use generic cosf implementation for SSE2 version
- benchtests: Add workload name for cosf
- x86_64: Optimize sincos where sin/cos is optimized (bug 29193)
- manual: fix reference to source file
- Add SOL_SMC from Linux 5.18 to bits/socket.h
- elf: Remove _dl_skip_args
- x86_64: Remove _dl_skip_args usage
- sparc: Remove _dl_skip_args usage
- sh: Remove _dl_skip_args usage
- s390: Remove _dl_skip_args usage
- riscv: Remove _dl_skip_args usage
- nios2: Remove _dl_skip_args usage (BZ# 29187)
- mips: Remove _dl_skip_args usage
- microblaze: Remove _dl_skip_args usage
- m68k: Remove _dl_skip_args usage
- ia64: Remove _dl_skip_args usage
- i686: Remove _dl_skip_args usage
- hppa: Remove _dl_skip_args usage (BZ# 29165)
- csky: Remove _dl_skip_args usage
- arc: Remove _dl_skip_args usage
- arm: Remove _dl_skip_args usage
- alpha: Remove _dl_skip_args usage
- benchtests: Improve benchtests for strstr, memmem, and memchr
- dlsym: Make RTLD_NEXT prefer default version definition [BZ #14932]
- x86-64: Ignore r_addend for R_X86_64_GLOB_DAT/R_X86_64_JUMP_SLOT
- x86_64: Implement evex512 version of strlen, strnlen, wcslen and wcsnlen
- Update kernel version to 5.18 in header constant tests
- String: Improve overflow test coverage for strnlen

* Thu May 26 2022 Arjun Shankar <arjun@redhat.com> - 2.35.9000-20
- Auto-sync with upstream branch master,
  commit 3d9926663cba19f40d26d8a8ab3b2a7cc09ffb13:
- Update syscall-names.list for Linux 5.18
- Fix deadlock when pthread_atfork handler calls pthread_atfork or dlclose
- Use Linux 5.18 in build-many-glibcs.py
- stdio-common: Simplify printf_unknown interface in vfprintf-internal.c
- stdio-common: Move union printf_arg int <printf.h>
- stdio-common: Add printf specifier registry to <printf.h>
- elf/dl-reloc.c: Copyright The GNU Toolchain Authors
- benchtests: Improve bench-strnlen.c
- math: Add math-use-builtins-fabs (BZ#29027)
- linux: Add CLONE_NEWTIME from Linux 5.6 to bits/sched.h
- Revert "[ARM][BZ #17711] Fix extern protected data handling"
- Revert "[AArch64][BZ #17711] Fix extern protected data handling"
- elf: Rewrite long RESOLVE_MAP macro to an always_inline static function

* Mon May 23 2022 DJ Delorie <dj@redhat.com> - 2.35.9000-19
- Auto-sync with upstream branch master,
  commit 748df8126ac69e68e0b94e236ea3c2e11b1176cb.
- dlfcn: Move RTLD_DEFAULT/RTLD_NEXT outside __USE_GNU
- elf: Optimize _dl_new_hash in dl-new-hash.h
- nss: Optimize nss_hash in nss_hash.c
- benchtests: Add benchtests for dl_elf_hash, dl_new_hash and nss_hash
- nss: Add tests for the nss_hash in nss_hash.h
- elf: Add tests for the dl hash funcs (_dl_new_hash and _dl_elf_hash)
- elf: Refactor dl_new_hash so it can be tested / benchmarked
- locale: Add more cached data to LC_CTYPE
- locale: Remove private union from struct __locale_data
- locale: Remove cleanup function pointer from struct __localedata
- locale: Call _nl_unload_locale from _nl_archive_subfreeres
- stdio-common: Add tst-memstream-string for open_memstream overflow
- __printf_fphex always uses LC_NUMERIC
- vfprintf: Consolidate some multibyte/wide character processing
- vfprintf: Move argument processing into vfprintf-process-arg.c
- stdio-common: Add tst-vfprintf-width-i18n to cover numeric field width
- string.h: fix __fortified_attr_access macro call [BZ #29162]
- Enable DT_RELR in glibc shared libraries and PIEs automatically
- S390: Enable static PIE
- linux: Add tst-pidfd.c
- linux: Add P_PIDFD
- linux: Add pidfd_send_signal
- linux: Add pidfd_getfd
- linux: Add pidfd_open
- aarch64: Move ld.so _start to separate file and drop _dl_skip_args
- linux: Add a getauxval test [BZ #23293]
- rtld: Remove DL_ARGV_NOT_RELRO and make _dl_skip_args const
- rtld: Use generic argv adjustment in ld.so [BZ #23293]
- scripts/glibcelf.py: Add *T_RISCV_* constants
- Remove dl-librecon.h header.
- elf: Remove ldconfig kernel version check
- Remove kernel version check
- linux: Use /sys/devices/system/cpu on __get_nprocs_conf (BZ#28991)
- csu: Implement and use _dl_early_allocate during static startup
- Linux: Introduce __brk_call for invoking the brk system call
- sys/cdefs.h: Do not require C++ compilers to define __STDC__
- fortify: Ensure that __glibc_fortify condition is a constant [BZ #29141]
- Update RISC-V specific ELF definitions

* Mon May 16 2022 Arjun Shankar <arjun@redhat.com> - 2.35.9000-18
- Auto-sync with upstream branch master,
  commit 9403b71ae97e3f1a91c796ddcbb4e6f044434734:
- x86_64: Remove bzero optimization
- RISC-V: Use an autoconf template to produce `preconfigure'
- MIPS: Use an autoconf template to produce `preconfigure'
- m68k: Use an autoconf template to produce `preconfigure'
- C-SKY: Use an autoconf template to produce `preconfigure'
- Remove configure fno_unit_at_a_time
- stdio: Remove the usage of $(fno-unit-at-a-time) for siglist.c
- stdio: Remove the usage of $(fno-unit-at-a-time) for errlist.c
- Add declare_object_symbol_alias for assembly codes (BZ #28128)
- wcrtomb: Make behavior POSIX compliant

* Tue May 10 2022 Patsy Griffin <patsy@redhat.com> - 2.35.9000-17
- Auto-sync with upstream branch master,
  commit 8162147872491bb5b48e91543b19c49a29ae6b6d.
- nptl: Add backoff mechanism to spinlock loop
- Linux: Implement a useful version of _startup_fatal
- ia64: Always define IA64_USE_NEW_STUB as a flag macro
- linux: Fix posix_spawn return code if clone fails (BZ#29109)
- benchtests: Add wcrtomb microbenchmark
- clock_settime/clock_gettime: Use __nonnull to avoid null pointer
- clock_adjtime: Use __nonnull to avoid null pointer
- ntp_xxxtimex: Use __nonnull to avoid null pointer
- adjtimex/adjtimex64: Use __nonnull to avoid null pointer
- hurd spawni: Fix reauthenticating closed fds
- Linux: Define MMAP_CALL_INTERNAL
- i386: Honor I386_USE_SYSENTER for 6-argument Linux system calls
- i386: Remove OPTIMIZE_FOR_GCC_5 from Linux libc-do-syscall.S
- manual: Clarify that abbreviations of long options are allowed

* Tue May 03 2022 Florian Weimer <fweimer@redhat.com> - 2.35.9000-16
- Auto-sync with upstream branch master,
  commit 8e28aa3a51bf0ef3683f2aed4b5b448744897b66:
- elf: Remove fallback to the start of DT_STRTAB for dladdr
- powerpc32: Remove unused HAVE_PPC_SECURE_PLT
- dlfcn: Implement the RTLD_DI_PHDR request type for dlinfo
- manual: Document the dlinfo function
- Do not use --hash-style=both for building glibc shared objects
- benchtests: Better libmvec integration
- benchtests: Add UNSUPPORTED benchmark status
- linux: Fix fchmodat with AT_SYMLINK_NOFOLLOW for 64 bit time_t (BZ#29097)
- Use __ehdr_start rather than _begin in _dl_start_final
- sysdeps: Add 'get_fast_jitter' interace in fast-jitter.h
- posix/glob.c: update from gnulib
- benchtests: Add pthread-mutex-locks bench
- linux: Fix missing internal 64 bit time_t stat usage
- elf: Fix DFS sorting algorithm for LD_TRACE_LOADED_OBJECTS with missing libraries (BZ #28868)
- posix: Remove unused definition on _Fork
- NEWS: Mention DT_RELR support
- elf: Add more DT_RELR tests
- elf: Properly handle zero DT_RELA/DT_REL values
- elf: Support DT_RELR relative relocation format [BZ #27924]
- Add GLIBC_ABI_DT_RELR for DT_RELR support
- elf: Define DT_RELR related macros and types
- elf: Replace PI_STATIC_AND_HIDDEN with opposite HIDDEN_VAR_NEEDS_DYNAMIC_RELOC
- i386: Regenerate ulps
- dlfcn: Do not use rtld_active () to determine ld.so state (bug 29078)
- INSTALL: Rephrase -with-default-link documentation

* Mon Apr 25 2022 Carlos O'Donell <carlos@redhat.com> - 2.35.9000-15
- Auto-sync with upstream branch master,
  commit 1305edd42c44fee6f8660734d2dfa4911ec755d6:
- elf: Move post-relocation code of _dl_start into _dl_start_final
- misc: Fix rare fortify crash on wchar funcs. [BZ 29030]
- elf: Remove unused enum allowmask
- scripts/glibcelf.py: Mark as UNSUPPORTED on Python 3.5 and earlier
- x86: Optimize {str|wcs}rchr-evex
- x86: Optimize {str|wcs}rchr-avx2
- x86: Optimize {str|wcs}rchr-sse2
- benchtests: Improve bench-strrchr
- x86-64: Fix SSE2 memcmp and SSSE3 memmove for x32
- Default to --with-default-link=no (bug 25812)
- scripts: Add glibcelf.py module
- Add locale for syr_SY
- elf: Move elf_dynamic_do_Rel RTLD_BOOTSTRAP branches outside
- m68k: Handle fewer relocations for RTLD_BOOTSTRAP (#BZ29071)
- nptl: Fix pthread_cancel cancelhandling atomic operations
- x86: Fix missing __wmemcmp def for disable-multiarch build
- elf: Remove __libc_init_secure

* Tue Apr 19 2022 DJ Delorie <dj@redhat.com> - 2.35.9000-14
- Auto-sync with upstream branch master,
  commit 78fb88827362fbd2cc8aa32892ae5b015106e25c.
- mips: Fix mips64n32 64 bit time_t stat support (BZ#29069)
- x86: Cleanup page cross code in memcmp-avx2-movbe.S
- x86: Remove memcmp-sse4.S
- x86: Optimize memcmp SSE2 in memcmp.S
- misc: Use 64 bit time_t interfaces on syslog
- misc: syslog: Move SYSLOG_NAME to USE_MISC (BZ #16355)
- misc: syslog: Use fixed-sized buffer and remove memstream
- misc: syslog: Simplify implementation
- misc: syslog: Fix indentation and style
- misc: Add syslog test
- support: Add xmkfifo
- stdio: Split __get_errname definition from errlist.c
- x86: Reduce code size of mem{move|pcpy|cpy}-ssse3
- x86: Remove mem{move|cpy}-ssse3-back
- x86: Remove str{p}{n}cpy-ssse3
- x86: Remove str{n}cat-ssse3
- x86: Remove str{n}{case}cmp-ssse3
- x86: Remove {w}memcmp-ssse3
- nptl: Handle spurious EINTR when thread cancellation is disabled (BZ#29029)
- S390: Add new s390 platform z16.
- Replace {u}int_fast{16|32} with {u}int32_t
- stdlib: Reflow and sort most variable assignments
- elf: Fix memory leak in _dl_find_object_update (bug 29062)
- hurd: Define ELIBEXEC
- hurd: Fix arbitrary error code
- NEWS: Move PLT tracking slowdown to glibc 2.35.
- Remove _dl_skip_args_internal declaration
- test-container: Fix "unused code" warnings on HURD
- Add .clang-format style file
- manual: Avoid name collision in libm ULP table [BZ #28956]

* Tue Apr 12 2022 Arjun Shankar <arjun@redhat.com> - 2.35.9000-13
- Add entry for Tarifit language locale for Morocco, and
- Auto-sync with upstream branch master,
  commit 1a85970f41ea1e5abe6da2298a5e8fedcea26b70:
- powerpc: Relocate stinfo->main
- powerpc64: Set up thread register for _dl_relocate_static_pie
- powerpc64: Use medium model toc accesses throughout
- linux: Constify rfv variable in dl_vdso_vsym
- string: Replace outdated comments in strlen().
- S390: Fix elf/tst-audit25[ab]
- sparc64: Remove fcopysign{f} implementation
- alpha: Remove fcopysign{f} implementation
- math: Use builtin for ldbl-96 copysign
- ia64: Remove fcopysign{f} implementation
- x86: Remove fcopysign{f} implementation
- powerpc: Remove fcopysign{f} implementation
- Add rif_MA locale [BZ #27781]
- tests/string: Drop simple/stupid/builtin tests
- test-memcpy: Actually reverse source and destination
- benchtests: Only build libmvec benchmarks iff $(build-mathvec) is set

* Tue Apr 05 2022 Florian Weimer <fweimer@redhat.com> - 2.35.9000-12
- Auto-sync with upstream branch master,
  commit 053fe273434056f551ed8f81daf750db9dab5931:
- linux: Fix __closefrom_fallback iterates until max int (BZ#28993)
- Remove -z combreloc and HAVE_Z_COMBRELOC
- sparc: Remove s_abs implementations
- ia64: Remove fabs implementations
- x86: Remove fabs{f} implementation
- alpha: Remove s_abs implementations
- Allow for unpriviledged nested containers
- Increase the test timeout of some string tests
- realpath: Bring back GNU extension on ENOENT and EACCES [BZ #28996]
- stdlib: Fix tst-getrandom memcmp call
- stdlib: Fix tst-rand48.c printf types
- elf: Remove unused functions from tst-audit25(a,b)
- nptl: Use libc-diag.h with tst-thread-setspecific
- crypt: Remove unused variable on cert test
- elf: Remove unused variables in tests
- elf: Fix wrong fscanf usage on tst-pldd
- posix: Remove unused variable on tst-_Fork.c
- resolv: Initialize loop variable on tst-resolv-trailing
- locale: Remove set but unused variable on ld-collate.c
- localedate: Fix printf type on tst_mbrtowc
- localedata: Remove unused variables in tests
- x86: Small improvements for wcslen
- x86: Small improvements for wcscpy-ssse3
- debug: Improve fdelt_chk error message
- Add HWCAP2_AFP, HWCAP2_RPRES from Linux 5.17 to AArch64 bits/hwcap.h
- x86: Remove AVX str{n}casecmp
- x86: Add EVEX optimized str{n}casecmp
- x86: Add AVX2 optimized str{n}casecmp
- string: Expand page cross test cases in test-strncmp.c
- string: Expand page cross test cases in test-strcmp.c
- x86: Optimize str{n}casecmp TOLOWER logic in strcmp-sse42.S
- x86: Optimize str{n}casecmp TOLOWER logic in strcmp.S
- string: Expand page cross tests in test-strncasecmp.c
- string: Expand page cross tests in test-strcasecmp.c
- benchtests: Use json-lib in bench-strncasecmp.c
- benchtests: Use json-lib in bench-strcasecmp.c
- x86: Fix fallback for wcsncmp_avx2 in strcmp-avx2.S [BZ #28896]
- x86: Remove strspn-sse2.S and use the generic implementation
- x86: Remove strpbrk-sse2.S and use the generic implementation
- x86: Remove strcspn-sse2.S and use the generic implementation
- x86: Optimize strspn in strspn-c.c
- x86: Optimize strcspn and strpbrk in strcspn-c.c
- benchtests: Use json-lib in bench-strspn.c
- benchtests: Use json-lib in bench-strpbrk.c
- x86: Code cleanup in strchr-evex and comment justifying branch
- x86: Code cleanup in strchr-avx2 and comment justifying branch
- benchtests: Add random benchmark in bench-strchr.c
- benchtests: Use json-lib in bench-strchr.c
- Update kernel version to 5.17 in tst-mman-consts.py
- iconvdata: Fix enum type on UTF-7
- nscd: Remove unused variable
- support: Fix support_process_state_wait path size calculation
- support: Remove unused extract_8 function
- locale: Remove ununsed wctype_table_get function
- gmon: Remove unused sprofil.c functions
- Update syscall lists for Linux 5.17
- Fix ununsed fstatat64_time64_statx
- malloc: Fix duplicate inline for do_set_mxfast
- elf: Remove inline _dl_dprintf
- configure.ac: fix bashisms in configure.ac
- getaddrinfo: Refactor code for readability
- Use Linux 5.17 in build-many-glibcs.py
- resolv: Fix unaligned accesses to fields in HEADER struct
- gai_init: Avoid jumping from if condition to its else counterpart
- gaiconf_init: Refactor some bits for readability
- gethosts: Return EAI_MEMORY on allocation failure
- gaih_inet: Split result generation into its own function
- gaih_inet: split loopback lookup into its own function
- gaih_inet: make gethosts into a function
- gaih_inet: separate nss lookup loop into its own function
- gaih_inet: Split nscd lookup code into its own function.
- gaih_inet: Split simple gethostbyname into its own function
- gaih_inet: make numeric lookup a separate routine
- gaih_inet: Simplify service resolution
- getaddrinfo: Fix leak with AI_ALL [BZ #28852]
- gaih_inet: Simplify canon name resolution
- Simplify allocations and fix merge and continue actions [BZ #28931]
- iconv: Add UTF-7-IMAP variant in utf-7.c
- iconv: make utf-7.c able to use variants
- iconv: Better mapping to RFC for UTF-7
- iconv: Always encode "optional direct" UTF-7 characters
- stdio-common: Add wide stream coverage to tst-vfprintf-user-type
- libio: Flush-only _IO_str_overflow must not return EOF (bug 28949)
- libio: Convert tst_swprintf to the test framework
- scripts/dso-ordering-test.py: Fix C&P error in * callrefs processing
- stdio-common: Generate ja_JP.EUC-JP locale
- stdio-common: Re-flow and sort Makefile variables
- nss: Sort tests and tests-container and put one test per line
- benchtests: Use "=" instead of ":=" [BZ #28970]
- hppa: Use END instead of PSEUDO_END in swapcontext.S

* Tue Mar 15 2022 DJ Delorie <dj@redhat.com> - 2.35.9000-11
- Auto-sync with upstream branch master,
  commit d05e6dc8d1032e1732542a48e0fb895432008b6e.
- hppa: Implement swapcontext in assembler (bug 28960)
- associate a deallocator for iconv_open
- associate a deallocation for opendir
- Add access function attributes to epoll_wait
- Add access function attributes to grp and shadow headers
- Define ISO 639-3 "tok" [BZ #28950]
- nss: Protect against errno changes in function lookup (bug 28953)
- nss: Do not mention NSS test modules in <gnu/lib-names.h>
- malloc: Exit early on test failure in tst-realloc
- Add some missing access function attributes
- libio: Ensure output buffer for wchars (bug #28828)
- inet: Return EAI_MEMORY when nrl_domainname() fails to allocate memory
- inet: Remove strdupa from nrl_domainname()
- inet: Fix getnameinfo (NI_NOFQDN) race condition (BZ#28566)
- benchtests: make compare_strings.py accept string as attribute value

* Wed Mar 09 2022 Arjun Shankar <arjun@redhat.com> - 2.35.9000-10
- Drop glibc-rh1070416.patch; nscd related, thus no longer relevant.

* Tue Mar 08 2022 Arjun Shankar <arjun@redhat.com> - 2.35.9000-9
- Auto-sync with upstream branch master,
  commit 6de743a4e31a94e3d022e64a90c9082290a5a573:
- x86_64: Fix code formatting of vectorized math functions
- pthread: Do not overwrite tests-time64
- x86_64: Fix svml_s_acosf16_core_avx512.S code formatting
- i386: Remove libc-do-syscall from sysdep-dl-routines [BZ #28936]
- linux/i386: remove dead assignment of sysdep-dl-routines

* Tue Mar 08 2022 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.35.9000-8
- Fix version check to accommodate gettext snapshot builds in rawhide.

* Tue Mar 01 2022 Carlos O'Donell <carlos@redhat.com> - 2.35.9000-7
- Auto-sync with upstream branch master,
  commit 2bbc694df279020a6620096d31c1e05c93966f9b:
- nptl: Fix cleanups for stack grows up [BZ# 28899]
- manual: SA_ONSTACK is ignored without alternate stack
- io: Add fsync call in tst-stat
- Linux: Consolidate auxiliary vector parsing (redo)

* Fri Feb 25 2022 Arjun Shankar <arjun@redhat.com> - 2.35.9000-6
- Auto-sync with upstream branch master,
  commit 1fe00d3eb602a0754873b536dc92fb6226759ee4:
- build: Properly generate .d dependency files [BZ #28922]
- benchtests: Generate .d dependency files [BZ #28922]
- benchtests: Remove duplicated loop in bench-bzero-walk.c
- localedata: Do not generate output if warnings were present.
- localedef: Update LC_MONETARY handling (Bug 28845)
- localedef: Handle symbolic links when generating locale-archive
- benchtests: Add small sizes (<= 64) to bench-bzero-walk.c
- math: Add more input to atanh accuracy tests
- resolv: Fix tst-resolv tests for 2.35 ABIs and later
- x86_64: Disable libmvec tests if multiarch not enabled [BZ# 28869]
- benchtests: Add benches for memset with 0 value
- i686: Remove bzero optimizations
- s390: Remove bzero optimizations
- powerpc: Remove powerpc64 bzero optimizations
- powerpc: Remove powerpc32 bzero optimizations
- sparc: Remove bzero optimization
- ia64: Remove bzero optimization
- alpha: Remove bzero optimization
- x86_64: Remove bcopy optimizations
- i386: Remove bcopy optimizations
- powerpc: Remove bcopy optimizations
- ia64: Remove bcopy
- hppa: Fix warnings from _dl_lookup_address
- hppa: Revise gettext trampoline design

* Wed Feb 23 2022 Carlos O'Donell <carlos@redhat.com> - 2.35.9000-5
- Fix locale-archive generation (#2057697)

* Tue Feb 22 2022 Carlos O'Donell <carlos@redhat.com> - 2.35.9000-4
- Auto-sync with upstream branch master,
  commit fdc1ae67fef27eea1445bab4bdfe2f0fb3bc7aa1:
- Add SOL_MPTCP, SOL_MCTP from Linux 5.16 to bits/socket.h
- elf: Check invalid hole in PT_LOAD segments [BZ #28838]
- realpath: Do not copy result on failure (BZ #28815)
- x86: Fix TEST_NAME to make it a string in tst-strncmp-rtm.c
- x86: Test wcscmp RTM in the wcsncmp overflow case [BZ #28896]
- hppa: Fix swapcontext
- x86: Fallback {str|wcs}cmp RTM in the ncmp overflow case [BZ #28896]
- string: Add a testcase for wcsncmp with SIZE_MAX [BZ #28755]
- microblaze: Use the correct select syscall (BZ #28883)
- Update kernel version to 5.16 in tst-mman-consts.py
- pthread: Use 64 bit time_t stat internally for sem_open (BZ #28880)
- x86: Fix bug in strncmp-evex and strncmp-avx2 [BZ #28895]
- String: Strength memset tests in test-memset.c
- x86-64: Define __memcmpeq in ld.so
- htl: Destroy thread-specific data before releasing joins
- htl: Fix initializing the key lock
- mach: Fix LLL_SHARED value
- htl: Make pthread_[gs]etspecific not check for key validity
- x86-64: Remove bzero weak alias in SS2 memset
- hppa: Fix typo
- linux: Use socket-constants-time64.h on tst-socket-timestamp-compat
- x86/configure.ac: Define PI_STATIC_AND_HIDDEN/SUPPORT_STATIC_PIE
- Fix elf/tst-audit2 on hppa
- x86: Use CHECK_FEATURE_PRESENT on PCONFIG
- x86: Don't check PTWRITE in tst-cpu-features-cpuinfo.c
- x86: Set .text section in memset-vec-unaligned-erms
- Linux: Include <dl-auxv.h> in dl-sysdep.c only for SHARED
- Revert "Linux: Consolidate auxiliary vector parsing"
- String: Ensure 'MIN_PAGE_SIZE' is multiple of 'getpagesize'
- Use binutils 2.38 branch in build-many-glibcs.py
- elf: Remove LD_USE_LOAD_BIAS
- malloc: Remove LD_TRACE_PRELINKING usage from mtrace
- elf: Remove prelink support
- Linux: Consolidate auxiliary vector parsing
- Linux: Assume that NEED_DL_SYSINFO_DSO is always defined
- Linux: Remove DL_FIND_ARG_COMPONENTS
- Linux: Remove HAVE_AUX_SECURE, HAVE_AUX_XID, HAVE_AUX_PAGESIZE
- elf: Merge dl-sysdep.c into the Linux version
- hppa: Fix bind-now audit (BZ #28857)

* Tue Feb 15 2022 Arjun Shankar <arjun@redhat.com> - 2.35.9000-3
- Reduce installed size of some langpacks by de-duplicating LC_CTYPE

* Thu Feb 10 2022 Arjun Shankar <arjun@redhat.com> - 2.35.9000-2
- Drop glibc-fedora-localedef.patch and adjust locale installation
  accordingly so that installed content remains unchanged.

* Wed Feb 09 2022 Florian Weimer <fweimer@redhat.com> - 2.35.9000-1
- Auto-sync with upstream branch master,
  commit 3d9f171bfb5325bd5f427e9fc386453358c6e840:
- x86-64: Optimize bzero
- benchtests: Add benches for bzero
- linux: fix accuracy of get_nprocs and get_nprocs_conf [BZ #28865]
- x86: Remove SSSE3 instruction for broadcast in memset.S (SSE2 Only)
- benchtests: Sort benches in Makefile
- Benchtests: Add length zero benchmark for memset in bench-memset.c
- x86: Improve vec generation in memset-vec-unaligned-erms.S
- x86-64: Add vector tan/tanf to libmvec microbenchmark
- x86-64: Add vector erfc/erfcf to libmvec microbenchmark
- x86-64: Add vector asinh/asinhf to libmvec microbenchmark
- x86-64: Add vector tanh/tanhf to libmvec microbenchmark
- x86-64: Add vector erf/erff to libmvec microbenchmark
- x86-64: Add vector acosh/acoshf to libmvec microbenchmark
- x86-64: Add vector atanh/atanhf to libmvec microbenchmark
- x86-64: Add vector log1p/log1pf to libmvec microbenchmark
- x86-64: Add vector log2/log2f to libmvec microbenchmark
- x86-64: Add vector log10/log10f to libmvec microbenchmark
- x86-64: Add vector atan2/atan2f to libmvec microbenchmark
- x86-64: Add vector cbrt/cbrtf to libmvec microbenchmark
- x86-64: Add vector sinh/sinhf to libmvec microbenchmark
- x86-64: Add vector expm1/expm1f to libmvec microbenchmark
- x86-64: Add vector cosh/coshf to libmvec microbenchmark
- x86-64: Add vector exp10/exp10f to libmvec microbenchmark
- x86-64: Add vector exp2/exp2f to libmvec microbenchmark
- x86-64: Add vector hypot/hypotf to libmvec microbenchmark
- x86-64: Add vector asin/asinf to libmvec microbenchmark
- x86-64: Add vector atan/atanf to libmvec microbenchmark
- elf: Replace tst-audit24bmod2.so with tst-audit24bmod2
- x86_64/multiarch: Sort sysdep_routines and put one entry per line
- string: Sort headers, routines, tests and tests-translation
- x86: Improve L to support L(XXX_SYMBOL (YYY, ZZZ))
- Benchtests: move 'alloc_bufs' from loop in bench-memset.c
- x86-64: Fix strcmp-evex.S
- x86-64: Fix strcmp-avx2.S
- x86-64: Add vector acos/acosf to libmvec microbenchmark
- benchtests: Add more coverage for strcmp and strncmp benchmarks
- x86: Optimize strcmp-evex.S
- x86: Optimize strcmp-avx2.S
- string: Improve coverage in test-strcmp.c and test-strncmp.c
- string/test-str*cmp: remove stupid_[strcmp, strncmp, wcscmp, wcsncmp].
- Open master branch for glibc 2.36 development

* Tue Feb 08 2022 Florian Weimer <fweimer@redhat.com> - 2.35-2
- Auto-sync with upstream branch release/2.35/master,
  commit 24962427071fa532c3c48c918e9d64d719cc8a6c:
- Add BZ#28860 reference on NEWS
- linux: Fix missing __convert_scm_timestamps (BZ #28860)

* Thu Feb 03 2022 Florian Weimer <fweimer@redhat.com> - 2.35-1
- glibc 2.35 upstream release
- Auto-sync with upstream branch release/2.35/master,
  commit a2f1675634b3513c09c38e55e6766e8c05768b1f:
- linux: __get_nprocs_sched: do not feed CPU_COUNT_S with garbage [BZ #28850]
- posix: Fix tst-spawn6 terminal handling (BZ #28853)
- Regenerate configure
- Create ChangeLog.old/ChangeLog.24.
- Prepare for glibc 2.35 release.
- Regenerate configure.
- Update install.texi, and regenerate INSTALL.
- Update NEWS bug list.
- Update NEWS.
- Update translations.
- Linux: Use ptrdiff_t for __rseq_offset
- Fix elf/tst-audit25a with default bind now toolchains
- posix: Replace posix_spawnattr_tc{get,set}pgrp_np with posix_spawn_file_actions_addtcsetpgrp_np
- or1k: Define PI_STATIC_AND_HIDDEN
- SET_RELHOOK: merge i386 and x86_64, and move to sysdeps/mach/hurd/x86
- elf: Fix runtime linker auditing on aarch64 (BZ #26643)
- elf: Issue la_symbind for bind-now (BZ #23734)
- elf: Fix initial-exec TLS access on audit modules (BZ #28096)
- elf: Add la_activity during application exit
- localedata: Adjust C.UTF-8 to align with C/POSIX.
- localedef: Fix handling of empty mon_decimal_point (Bug 28847)
- malloc: Fix tst-mallocalign1 macro spacing.

* Tue Feb 01 2022 Florian Weimer <fweimer@redhat.com> - 2.34.9000-39
- Drop glibc-temp-Wno-use-after-free.patch, fixed upstream.
- Auto-sync with upstream branch master,
  commit 3fb18fd80c5900cc82748f3320b30516c57d24da:
- elf: Add <dl-r_debug.h>
- Mention _FORTIFY_SOURCE=3 for gcc12 in NEWS
- malloc: Fix -Wuse-after-free warning in tst-mallocalign1 [BZ #26779]
- Update libc.pot for 2.35 release.
- tst-socket-timestamp-compat.c: Check __TIMESIZE [BZ #28837]
- Add prelink removal plan on NEWS
- Linux: Only generate 64 bit timestamps for 64 bit time_t recvmsg/recvmmsg
- linux: Fix ancillary 64-bit time timestamp conversion (BZ #28349, BZ#28350)
- support: Add support_socket_so_timestamp_time64
- Fix elf/loadfail test build dependencies
- Fix glibc 2.34 ABI omission (missing GLIBC_2.34 in dynamic loader)
- x86: Use CHECK_FEATURE_PRESENT to check HLE [BZ #27398]
- Guard tst-valgrind-smoke.out with run-built-tests
- hurd: Add posix_spawnattr_tc{get,set}pgrp_np on libc.abilist
- Avoid -Wuse-after-free in tests [BZ #26779].
- elf: Replace tst-p_alignmod1-editX with a python script
- stdlib: Avoid -Wuse-after-free in __add_to_environ [BZ #26779]
- io: Fix use-after-free in ftw [BZ #26779]
- intl: Avoid -Wuse-after-free [BZ #26779]
- elf: Fix use-after-free in ldconfig [BZ #26779]
- posix: Add terminal control setting support for posix_spawn

* Mon Jan 24 2022 DJ Delorie <dj@redhat.com> - 2.34.9000-38
- Auto-sync with upstream branch master,
  commit 5b8e7980c5dabd9aaefeba4f0208baa8cf7653ee.
- Linux: Detect user namespace support in io/tst-getcwd-smallbuff
- Fix handling of unterminated bracket expressions in fnmatch (bug 28792)
- realpath: Avoid overwriting preexisting error (CVE-2021-3998)
- elf: Add a test for PT_LOAD segments with invalid p_align [BZ #28688]
- elf: Add a test for PT_LOAD segments with p_align == 1 [BZ #28688]
- elf: Add a test for PT_LOAD segments with mixed p_align [BZ #28676]
- Add and use link-test-modules-rpath-link [BZ #28455]
- tst-realpath-toolong: Fix hurd build
- getcwd: Set errno to ERANGE for size == 1 (CVE-2021-3999)
- Add valgrind smoke test
- htl: Fix cleaning the reply port
- elf: Properly align all PT_LOAD segments [BZ #28676]
- realpath: Set errno to ENAMETOOLONG for result larger than PATH_MAX [BZ #28770]
- support: Add helpers to create paths longer than PATH_MAX
- nptl: Effectively skip CAS in spinlock loop
- mips: Move DT_MIPS into <ldsodefs.h>
- x86_64: Document libmvec vector functions accuracy [BZ #28766]
- x86: Black list more Intel CPUs for TSX [BZ #27398]
- elf: Fix tst-align3
- elf: Move _dl_setup_hash to its own file
- htl: Fix build error in annexc
- elf: Reinstate tst-audit17
- x86: use default cache size if it cannot be determined [BZ #28784]
- rt/tst-mqueue*: Return UNSUPPORTED when mq_open fails with ENOSYS
- Linux: Add epoll_pwait2 (BZ #27359)
- Properly handle --disable-default-pie [BZ #28780]
- elf: Fix 64 time_t support for installed statically binaries
- Revert "elf: Fix 64 time_t support for installed statically binaries"
- CVE-2022-23218: Buffer overflow in sunrpc svcunix_create (bug 28768)
- sunrpc: Test case for clnt_create "unix" buffer overflow (bug 22542)
- CVE-2022-23219: Buffer overflow in sunrpc clnt_create for "unix" (bug 22542)
- socket: Add the __sockaddr_un_set function
- elf/tst-dl_find_object: Disable subtests for non-contiguous maps (bug 28732)
- elf: Set l_contiguous to 1 for the main map in more cases
- elf: Introduce rtld_setup_main_map
- hurd: Make RPC input array parameters const
- hurd: optimize exec cleanup
- hurd: Add __rtld_execve
- hurd: Fix exec() leak on proc_task2proc failure
- htl: Hide __pthread_attr's __schedparam type [BZ #23088]
- htl: Clear kernel_thread field before releasing the thread structure
- hurd: drop SA_SIGINFO availability xfail
- hurd: Fix timer/clock_getres crash on NULL res parameter
- hurd: Fix pthread_kill on exiting/ted thread
- [hurd] Drop spurious #ifdef SHARED
- [hurd] Call _dl_sort_maps_init in _dl_sysdep_start
- elf tst-dl_find_object: Fix typo
- s390x: Use <gcc-macros.h> in early HWCAP check
- x86: Add x86-64-vN check to early startup
- powerpc64le: Use <gcc-macros.h> in early HWCAP check
- Add --with-rtld-early-cflags configure option
- elf: Split dl-printf.c from dl-misc.c
- elf/Makefile: Reflow and sort most variable assignments
- Generate gcc-macros.h
- x86: HAVE_X86_LAHF_SAHF, HAVE_X86_MOVBE and -march=x86-64-vN (bug 28782)
- math: Add more inputs to atan2 accuracy tests [BZ #28765]
- Disable debuginfod in printer tests [BZ #28757]
- Update syscall lists for Linux 5.16
- i386: Remove broken CAN_USE_REGISTER_ASM_EBP (bug 28771)
- stdlib: Fix formatting of tests list in Makefile
- stdlib: Sort tests in Makefile
- x86_64: Fix SSE4.2 libmvec atan2 function accuracy [BZ #28765]
- debug: Synchronize feature guards in fortified functions [BZ #28746]
- debug: Autogenerate _FORTIFY_SOURCE tests
- Do not build libresolv module with 64 bit time_t flags
- Revert "linux: Fix ancillary 64-bit time timestamp conversion (BZ #28349, BZ #28350)"
- Revert "support: Add support_socket_so_timestamp_time64"
- timezone: Fix tst-bz28707 Makefile rule
- linux: Fix ancillary 64-bit time timestamp conversion (BZ #28349, BZ #28350)
- support: Add support_socket_so_timestamp_time64
- elf: Fix 64 time_t support for installed statically binaries
- Enable _FORTIFY_SOURCE=3 for gcc 12 and above
- manual: Drop obsolete @refill
- aarch64: Add HWCAP2_ECV from Linux 5.16
- Use Linux 5.16 in build-many-glibcs.py
- x86: Fix __wcsncmp_evex in strcmp-evex.S [BZ# 28755]
- x86: Fix __wcsncmp_avx2 in strcmp-avx2.S [BZ# 28755]
- math: Fix float conversion regressions with gcc-12 [BZ #28713]
- elf: Simplify software TM implementation in _dl_find_object
- Restore ENTRY_POINT definition on hppa, ia64 (bug 28749)
- elf: Fix fences in _dl_find_object_update (bug 28745)
- ttydefaults.h: Fix CSTATUS to control-t
- AArch64: Check for SVE in ifuncs [BZ #28744]
- debug: Remove catchsegv and libSegfault (BZ #14913)
- Documentation for OpenRISC port
- build-many-glibcs.py: add OpenRISC support
- or1k: Build Infrastructure
- or1k: ABI lists
- or1k: Linux ABI
- or1k: Linux Syscall Interface
- or1k: math soft float support
- or1k: Atomics and Locking primitives
- or1k: Thread Local Storage support
- or1k: startup and dynamic linking code
- or1k: ABI Implementation
- linux/syscalls: Add or1k_atomic syscall for OpenRISC
- elf: Add reloc for OpenRISC
- elf: Add a comment after trailing backslashes
- elf: Also try DT_RUNPATH for LD_AUDIT dlopen [BZ #28455]
- elf: Fix tst-linkall-static link when pthread is not in libc

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.34.9000-37
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Jan 04 2022 Florian Weimer <fweimer@redhat.com> - 2.34.9000-36
- Auto-sync with upstream branch master,
  commit 28713c06129f8f64f88c423266e6ff2880216509:
- elf: Sort tests and modules-names
- hurd: nuke all unknown ports on exec
- hurd: Fix auth port leak
- Remove stale reference to libanl.a
- elf: Add <dl-debug.h>
- Properly check linker option in LIBC_LINKER_FEATURE [BZ #28738]
- hurd: Implement _S_msg_get_dtable
- Update automatically-generated copyright dates
- Sync move-if-change from Gnulib, updating copyright
- Update copyright dates not handled by scripts/update-copyrights.
- Update copyright dates with scripts/update-copyrights
- hurd: Use __trivfs_server_name instead of trivfs_server_name
- hurd: Bump BRK_START to 0x20000000
- hurd: Avoid overzealous shared objects constraints
- time: Refactor timesize.h for some ABIs
- hurd: Make getrandom a stub inside the random translator
- open64: Force O_LARGEFILE on all architectures
- x86-64: Add vector tan/tanf implementation to libmvec
- x86-64: Add vector erfc/erfcf implementation to libmvec
- resolv: Do not install libanl.so symbolic link
- resolv: Do not build libanl.so for ABIs starting at 2.35
- timezone: test-case for BZ #28707
- timezone: handle truncated timezones from tzcode-2021d and later (BZ #28707)
- x86-64: Add vector asinh/asinhf implementation to libmvec
- x86-64: Add vector tanh/tanhf implementation to libmvec
- x86-64: Add vector erf/erff implementation to libmvec
- x86-64: Add vector acosh/acoshf implementation to libmvec
- x86-64: Add vector atanh/atanhf implementation to libmvec
- x86-64: Add vector log1p/log1pf implementation to libmvec
- x86-64: Add vector log2/log2f implementation to libmvec
- x86-64: Add vector log10/log10f implementation to libmvec
- x86-64: Add vector atan2/atan2f implementation to libmvec
- x86-64: Add vector cbrt/cbrtf implementation to libmvec
- x86-64: Add vector sinh/sinhf implementation to libmvec
- x86-64: Add vector expm1/expm1f implementation to libmvec
- x86-64: Add vector cosh/coshf implementation to libmvec
- x86-64: Add vector exp10/exp10f implementation to libmvec
- x86-64: Add vector exp2/exp2f implementation to libmvec
- x86-64: Add vector hypot/hypotf implementation to libmvec
- x86-64: Add vector asin/asinf implementation to libmvec
- x86-64: Add vector atan/atanf implementation to libmvec

* Wed Dec 29 2021 Florian Weimer <fweimer@redhat.com> - 2.34.9000-35
- Auto-sync with upstream branch master,
  commit 5d28a8962dcb6ec056b81d730e3c6fb57185a210:
- elf: Add _dl_find_object function
- malloc: Remove memusage.h
- malloc: Use hp-timing on libmemusage
- Remove atomic-machine.h atomic typedefs
- malloc: Remove atomic_* usage
- microblaze: Add missing implementation when !__ASSUME_TIME64_SYSCALLS
- elf: Do not fail for failed dlmopen on audit modules (BZ #28061)
- elf: Issue audit la_objopen for vDSO
- elf: Add audit tests for modules with TLSDESC
- elf: Avoid unnecessary slowdown from profiling with audit (BZ#15533)
- elf: Add _dl_audit_pltexit
- elf: Add _dl_audit_pltenter
- elf: Add _dl_audit_preinit
- elf: Add _dl_audit_symbind_alt and _dl_audit_symbind
- elf: Add _dl_audit_objclose
- elf: Add _dl_audit_objsearch
- elf: Add _dl_audit_activity_map and _dl_audit_activity_nsid
- elf: Add _dl_audit_objopen
- hurd: Fix static-PIE startup
- hurd: let csu initialize tls
- hurd: Fix XFAIL-ing mallocfork2 tests
- hurd: XFAIL more tests that require setpshared support
- malloc: Add missing shared thread library flags
- stdio-common: Fix %m sprintf test output for GNU/Hurd
- x86: Optimize L(less_vec) case in memcmpeq-evex.S
- x86: Optimize L(less_vec) case in memcmp-evex-movbe.S
- elf: Remove AArch64 from comment for AT_MINSIGSTKSZ
- math: Properly cast X_TLOSS to float [BZ #28713]
- Set default __TIMESIZE default to 64
- stdio: Implement %#m for vfprintf and related functions
- elf: Remove unused NEED_DL_BASE_ADDR and _dl_base_addr
- x86-64: Add vector acos/acosf implementation to libmvec
- intl/plural.y: Avoid conflicting declarations of yyerror and yylex
- elf: Remove excessive p_align check on PT_LOAD segments [BZ #28688]
- s_sincosf.h: Change pio4 type to float [BZ #28713]
- Linux: Fix 32-bit vDSO for clock_gettime on powerpc32
- Regenerate ulps on x86_64 with GCC 12
- Add ARPHRD_CAN, ARPHRD_MCTP to net/if_arp.h
- Remove ununsed tcb-offset
- riscv: align stack before calling _dl_init [BZ #28703]
- riscv: align stack in clone [BZ #28702]
- elf: Fix tst-cpu-features-cpuinfo for KVM guests on some AMD systems [BZ #28704]
- powerpc64[le]: Allocate extra stack frame on syscall.S
- Update copyright header in recently merged ab_GE locale
- fortify: Fix spurious warning with realpath

* Tue Dec 28 2021 Florian Weimer <fweimer@redhat.com> - 2.34.9000-34
- armhfp, i686: Revert 64-bit time_t/off_t for internal use (#2034715)

* Fri Dec 17 2021 Florian Weimer <fweimer@redhat.com> - 2.34.9000-33
- Auto-sync with upstream branch master,
  commit b99b0f93ee8762fe53ff65802deb6f00700b9924:
- nss: Use "files dns" as the default for the hosts database (#2033020)
- arm: Guard ucontext _rtld_global_ro access by SHARED, not PIC macro
- Fix The GNU ToolChain Authors copyright notice
- Remove upper limit on tunable MALLOC_MMAP_THRESHOLD
- localedata: add new locale ab_GE
- Fix __minimal_malloc segfaults in __mmap due to stack-protector
- __glibc_unsafe_len: Fix comment
- malloc: Enable huge page support on main arena
- malloc: Move MORECORE fallback mmap to sysmalloc_mmap_fallback
- malloc: Add Huge Page support to arenas
- malloc: Add Huge Page support for mmap
- malloc: Move mmap logic to its own function
- malloc: Add THP/madvise support for sbrk
- malloc: Add madvise support for Transparent Huge Pages
- powerpc: Use global register variable in <thread_pointer.h>
- Use LFS and 64 bit time for installed programs (swbz#15333)

* Wed Dec 15 2021 Arjun Shankar <arjun@redhat.com> - 2.34.9000-32
- Do not use --enable-static-pie configure flag since it is now ignored

* Wed Dec 15 2021 Florian Weimer <fweimer@redhat.com> - 2.34.9000-31
- Drop glibc-fedora-revert-PT_LOAD-segment-align.patch; fix applied upstream
- Auto-sync with upstream branch master,
  commit 4435c29892c43ae9908a42e591747be63102689b:
- Support target specific ALIGN for variable alignment test [BZ #28676]
- NEWS: Document LD_PREFER_MAP_32BIT_EXEC as x86-64 only
- elf: Align argument of __munmap to page size [BZ #28676]

* Tue Dec 14 2021 Arjun Shankar <arjun@redhat.com> - 2.34.9000-30
- Add glibc-fedora-revert-PT_LOAD-segment-align.patch to revert upstream
  commits 718fdd87b1b9 and fc2334ab32e0.
- Auto-sync with upstream branch master,
  commit 0884724a95b60452ad483dbe086d237d02ba624d:
- intl: Emit no lines in bison generated files
- hurd: Do not set PIE_UNSUPPORTED
- NEWS: Move LD_PREFER_MAP_32BIT_EXEC
- mach: Fix spurious inclusion of stack_chk_fail_local in libmachuser.a
- Disable DT_RUNPATH on NSS tests [BZ #28455]
- sysdeps: Simplify sin Taylor Series calculation
- math: Remove the error handling wrapper from hypot and hypotf
- math: Use fmin/fmax on hypot
- aarch64: Add math-use-builtins-f{max,min}.h
- math: Add math-use-builtinds-fmin.h
- math: Add math-use-builtinds-fmax.h
- math: Remove powerpc e_hypot
- i386: Move hypot implementation to C
- math: Use an improved algorithm for hypotl (ldbl-128)
- math: Use an improved algorithm for hypotl (ldbl-96)
- math: Improve hypot performance with FMA
- math: Use an improved algorithm for hypot (dbl-64)
- math: Simplify hypotf implementation
- Cleanup encoding in comments
- Replace --enable-static-pie with --disable-default-pie
- hurd: Add rules for static PIE build
- hurd: Fix gmon-static
- x86-64: Remove LD_PREFER_MAP_32BIT_EXEC support [BZ #28656]
- elf: Use errcode instead of (unset) errno in rtld_chain_load
- Add a testcase to check alignment of PT_LOAD segment [BZ #28676]
- elf: Properly align PT_LOAD segments [BZ #28676]
- elf: Install a symbolic link to ld.so as /usr/bin/ld.so
- nptl: Add one more barrier to nptl/tst-create1
- Remove TLS_TCB_ALIGN and TLS_INIT_TCB_ALIGN
- nptl: rseq failure after registration on main thread is fatal
- nptl: Add public rseq symbols and <sys/rseq.h>
- nptl: Add glibc.pthread.rseq tunable to control rseq registration
- Linux: Use rseq to accelerate sched_getcpu
- nptl: Add rseq registration
- nptl: Introduce THREAD_GETMEM_VOLATILE
- nptl: Introduce <tcb-access.h> for THREAD_* accessors
- nptl: Add <thread_pointer.h> for defining __thread_pointer
- String: test-memcpy used unaligned types for buffers [BZ 28572]
- localedef: check magic value on archive load [BZ #28650]
- x86: Don't set Prefer_No_AVX512 for processors with AVX512 and AVX-VNNI
- linux: Add generic ioctl implementation
- linux: Add generic syscall implementation
- misc, nptl: Remove stray references to __condvar_load_64_relaxed
- csu: Always use __executable_start in gmon-start.c
- elf: execve statically linked programs instead of crashing [BZ #28648]
- Add --with-timeoutfactor=NUM to specify TIMEOUTFACTOR

* Mon Dec 13 2021 Arjun Shankar <arjun@redhat.com> - 2.34.9000-29
- Remove nscd (#1905142)
  https://fedoraproject.org/wiki/Changes/RemoveNSCD

* Fri Dec 10 2021 Pavel Březina <pbrezina@redhat.com> - 2.34.9000-28
- /etc/nsswitch.conf is now owned by authselect (rhbz#2023741)

* Thu Dec 09 2021 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.34.9000-27
- Set BuildFlagsNonshared only if _annotated_build is set.

* Sat Dec 04 2021 Florian Weimer <fweimer@redhat.com> - 2.34.9000-26
- Drop glibc-rh2026399.patch, not needed anymore due to upstream fix.
- Auto-sync with upstream branch master,
  commit 4df1fa6ddc8925a75f3da644d5da3bb16eb33f02:
- x86-64: Use notl in EVEX strcmp (#2026399)
- nptl: Increase default TCB alignment to 32
- elf: add definition for ELF_NOTE_FDO and NT_FDO_PACKAGING_METADATA note
- AArch64: Improve A64FX memcpy
- AArch64: Optimize memcmp
- powerpc64[le]: Fix CFI and LR save address for asm syscalls [BZ #28532]
- linux: Implement pipe in terms of __NR_pipe2
- linux: Implement mremap in C
- linux: Add prlimit64 C implementation
- elf: Include <stdbool.h> in tst-tls20.c
- elf: Include <stdint.h> in tst-tls20.c
- hurd: Let report-wait use a weak reference to _hurd_itimer_thread

* Sat Dec  4 2021 Florian Weimer <fweimer@redhat.com> - 2.34.9000-25
- x86_64: Disable additional EVEX string functions (#2026399)

* Fri Dec  3 2021 Florian Weimer <fweimer@redhat.com> - 2.34.9000-24
- x86_64: Disable EVEX *cmp* string functions (#2026399)

* Thu Dec  2 2021 Florian Weimer <fweimer@redhat.com> - 2.34.9000-23
- Drop glibc-sdt-headers.patch; the official systemtap headers work again.

* Thu Nov 25 2021 Carlos O'Donell <carlos@redhat.com> - 2.34.9000-22
- Auto-sync with upstream branch master,
  commit 137ed5ac440a4d3cf4178ce97f349b349a9c2c66:
- linux: Use /proc/stat fallback for __get_nprocs_conf (BZ #28624)
- linux: Add fanotify_mark C implementation
- linux: Only build fstatat fallback if required
- regex: fix buffer read overrun in search [BZ#28470]
- x86-64: Add vector sin/sinf to libmvec microbenchmark
- x86-64: Add vector pow/powf to libmvec microbenchmark
- x86-64: Add vector log/logf to libmvec microbenchmark
- x86-64: Add vector exp/expf to libmvec microbenchmark
- x86-64: Add vector cos/cosf to libmvec microbenchmark
- io: Refactor close_range and closefrom
- nptl: Do not set signal mask on second setjmp return [BZ #28607]
- powerpc: Define USE_PPC64_NOTOC iff compiler supports it
- setjmp: Replace jmp_buf-macros.h with jmp_buf-macros.sym
- Update kernel version to 5.15 in tst-mman-consts.py
- socket: Do not use AF_NETLINK in __opensock
- elf: Move la_activity (LA_ACT_ADD) after _dl_add_to_namespace_list() (BZ #28062)
- Add PF_MCTP, AF_MCTP from Linux 5.15 to bits/socket.h
- malloc: Fix malloc debug for 2.35 onwards
- elf: Introduce GLRO (dl_libc_freeres), called from __libc_freeres
- nptl: Extract <bits/atomic_wide_counter.h> from pthread_cond_common.c

* Wed Nov 17 2021 Florian Weimer <fweimer@redhat.com> - 2.34.9000-21
- Temporary patch glibc-sdt-headers.patch, to fix s390x build failure.
- Temporary patch glibc-dso-sort-makefile-fail.patch, to fix x86_64 build.
- Auto-sync with upstream branch master,
  commit a43c0b5483da4c5e3796af309864cb44256c02db:
- x86-64: Create microbenchmark infrastructure for libmvec
- elf: hidden visibility for __minimal_malloc functions
- elf: Use a temporary file to generate Makefile fragments [BZ #28550]
- dso-ordering-test.py: Put all sources in one directory [BZ #28550]
- elf: Move LAV_CURRENT to link_lavcurrent.h
- Move assignment out of the CAS condition
- Add a comment for --enable-initfini-array [BZ #27945]
- tst-tzset: output reason when creating 4GiB file fails
- Add LLL_MUTEX_READ_LOCK [BZ #28537]
- Avoid extra load with CAS in __pthread_mutex_clocklock_common [BZ #28537]
- Avoid extra load with CAS in __pthread_mutex_lock_full [BZ #28537]
- String: Split memcpy tests so that parallel build is faster
- x86: Shrink memcmp-sse4.S code size
- Support C2X printf %b, %B
- Update syscall lists for Linux 5.15
- s390: Use long branches across object boundaries (jgh instead of jh)

* Tue Nov 16 2021 Arjun Shankar <arjun@redhat.com> - 2.34.9000-20
- Create /{bin,lib,lib64,sbin} as symbolic links in test-container

* Wed Nov 10 2021 Arjun Shankar <arjun@redhat.com> - 2.34.9000-19
- Auto-sync with upstream branch master,
  commit 0bd356df1afb0591470499813d4ebae9bcedd6a6:
- Remove the unused +mkdep/+make-deps/s-proto.S/s-proto-cancel.S
- Fix build a chec failures after b05fae4d8e34
- elf: Use the minimal malloc on tunables_strdup

* Mon Nov 08 2021 Arjun Shankar <arjun@redhat.com> - 2.34.9000-18
- Auto-sync with upstream branch master,
  commit db6c4935fae6005d46af413b32aa92f4f6059dce:
- Fix memmove call in vfprintf-internal.c:group_number
- locale: Fix localedata/sort-test undefined behavior
- test-memcpy.c: Double TIMEOUT to (8 * 60)
- hurd: Remove unused __libc_close_range
- hurd: Implement close_range and closefrom
- x86: Double size of ERMS rep_movsb_threshold in dl-cacheinfo.h
- x86: Optimize memmove-vec-unaligned-erms.S
- benchtests: Add partial overlap case in bench-memmove-walk.c
- benchtests: Add additional cases to bench-memcpy.c and bench-memmove.c
- string: Make tests birdirectional test-memcpy.c
- Remove the last trace of generate-md5 [BZ #28554]
- Revert "benchtests: Add acosf function to bench-math"
- Configure GCC with --enable-initfini-array [BZ #27945]
- elf: Earlier missing dynamic segment check in _dl_map_object_from_fd
- gconv: Do not emit spurious NUL character in ISO-2022-JP-3 (bug 28524)
- [powerpc] Tighten contraints for asm constant parameters

* Wed Nov 03 2021 Patsy Griffin <patsy@redhat.com> - 2.34.9000-17
- Auto-sync with upstream branch master,
  commit d3bf2f5927d51258a51ac7fde04f4805f8ee294a.
- elf: Do not run DSO sorting if tunables is not enabled
- riscv: Build with -mno-relax if linker does not support R_RISCV_ALIGN
- x86-64: Replace movzx with movzbl
- regex: Unnest nested functions in regcomp.c
- Use Linux 5.15 in build-many-glibcs.py
- elf: Assume disjointed .rela.dyn and .rela.plt for loader
- i386: Explain why __HAVE_64B_ATOMICS has to be 0
- benchtests: Add hypotf
- benchtests: Make hypot input random
- arm: Use have-mtls-dialect-gnu2 to check for ARM TLS descriptors support
- arm: Use internal symbol for _dl_argv on _dl_start_user
- x86-64: Remove Prefer_AVX2_STRCMP
- x86-64: Improve EVEX strcmp with masked load

* Fri Oct 29 2021 DJ Delorie <dj@redhat.com> - 2.34.9000-16
- Auto-sync with upstream branch master,
  commit 79d0fc65395716c1d95931064c7bf37852203c66.
- benchtests: Add acosf function to bench-math
- benchtests: Improve bench-memcpy-random
- Disable -Waggressive-loop-optimizations warnings in tst-dynarray.c
- Fix compiler issue with mmap_internal
- Check if linker also support -mtls-dialect=gnu2
- Fix LIBC_PROG_BINUTILS for -fuse-ld=lld
- elf: Disable ifuncmain{1,5,5pic,5pie} when using LLD
- Handle NULL input to malloc_usable_size [BZ #28506]
- x86_64: Add memcmpeq.S to fix disable-multi-arch build
- login: Add back libutil as an empty library
- riscv: Fix incorrect jal with HIDDEN_JUMPTARGET
- x86_64: Add evex optimized __memcmpeq in memcmpeq-evex.S
- x86_64: Add avx2 optimized __memcmpeq in memcmpeq-avx2.S
- x86_64: Add sse2 optimized __memcmpeq in memcmp-sse2.S
- x86_64: Add support for __memcmpeq using sse2, avx2, and evex
- Benchtests: Add benchtests for __memcmpeq
- String: Add __memcmpeq as build target
- NEWS: Add item for __memcmpeq
- String: Add tests for __memcmpeq
- String: Add hidden defs for __memcmpeq() to enable internal usage
- String: Add support for __memcmpeq() ABI on all targets
- configure: Don't check LD -v --help for LIBC_LINKER_FEATURE
- elf: Make global.out depend on reldepmod4.so [BZ #28457]
- x86: Replace sse2 instructions with avx in memcmp-evex-movbe.S
- bench-math: Sort and put each bench per line
- x86_64: Add missing libmvec ABI tests
- elf: Fix e6fd79f379 build with --enable-tunables=no
- elf: Fix slow DSO sorting behavior in dynamic loader (BZ #17645)
- elf: Testing infrastructure for ld.so DSO sorting (BZ #17645)
- iconv: Use TIMEOUTFACTOR for iconv test timeout
- posix: Remove alloca usage for internal fnmatch implementation
- Add alloc_align attribute to memalign et al
- linux: Fix a possibly non-constant expression in _Static_assert
- x86-64: Add sysdeps/x86_64/fpu/Makeconfig

* Wed Oct 20 2021 Carlos O'Donell <carlos@redhat.com> - 2.34.9000-15
- Remove glibc-ld-readonly-revert.patch.
- Auto-sync with upstream branch master,
  commit e037274c8ec86ca9d491331984b34f30701b23cf:
- stdlib: Fix tst-canon-bz26341 when the glibc build current working
  directory is itself using symlinks.
- powerpc: Remove backtrace implementation
- Correct access attribute on memfrob (bug 28475)
- debug: Add tests for _FORTIFY_SOURCE=3
- Make sure that the fortified function conditionals are constant
- Don't add access size hints to fortifiable functions
- glibcextract.py: Place un-assemblable @@@ in a comment
- nss: Unnest nested function add_key
- ld.so: Initialize bootstrap_map.l_ld_readonly [BZ #28340]
- timex: Use 64-bit fields on 32-bit TIMESIZE=64 systems (BZ #28469)
- manual: Update _TIME_BITS to clarify it's user defined
- nptl: Fix tst-cancel7 and tst-cancelx7 pidfile race
- elf: Fix elf_get_dynamic_info() for bootstrap
- hurd if_index: Explicitly use AF_INET for if index discovery
- hurd: Fix intr-msg parameter/stack kludge
- x86-64: Add test-vector-abi.h/test-vector-abi-sincos.h
- elf: Fix dynamic-link.h usage on rtld.c

* Thu Oct 14 2021 Arjun Shankar <arjun@redhat.com> - 2.34.9000-14
- Adjust glibc-ld-readonly-revert.patch.
- Auto-sync with upstream branch master,
  commit e59ced238482fd71f3e493717f14f6507346741e:
- x86: Optimize memset-vec-unaligned-erms.S
- x86: Optimize memcmp-evex-movbe.S for frontend behavior and size
- libio: Update tst-wfile-sync to not depend on stdin
- elf: Update audit tests to not depend on stdout
- elf: Fix elf_get_dynamic_info definition
- Add TEST_COMPARE_STRING_WIDE to support/check.h
- Fix nios2 localplt failure
- elf: Remove Intel MPX support (lazy PLT, ld.so profile, and LD_AUDIT)
- resolv: Avoid GCC 12 false positive warning [BZ #28439].
- benchtests: Add medium cases and increase iters in bench-memset.c
- x86: Modify ENTRY in sysdep.h so that p2align can be specified
- resolv: make res_randomid use random_bits()
- Linux: implement getloadavg(3) using sysinfo(2)
- Remove unreliable parts of rt/tst-cpuclock2
- elf: Avoid nested functions in the loader [BZ #27220]
- Add run-time check for indirect external access
- Initial support for GNU_PROPERTY_1_NEEDED
- io: Fix ftw internal realloc buffer (BZ #28126)
- Fix subscript error with odd TZif file [BZ #28338]

* Thu Oct 07 2021 Carlos O'Donell <carlos@redhat.com> - 2.34.9000-13
- Auto-sync with upstream branch master,
  commit f2e06656d04a9fcb0603802a4f8ce7aa3a1f055e:
- S390: Add PCI_MIO and SIE HWCAPs
- support: Also return fd when it is 0
- ld.so: Don't fill the DT_DEBUG entry in ld.so [BZ #28129]
- S390: update libm test ulps
- powerpc: update libm test ulps
- math: Also xfail the new j0f tests for ibm128-libgcc
- y2038: Use a common definition for stat for sparc32
- Fix stdlib/tst-setcontext.c for GCC 12 -Warray-compare
- aarch64: update libm test ulps
- Fixed inaccuracy of j0f (BZ #28185)
- Fix stdio-common tests for GCC 12 -Waddress
- benchtests: Building benchmarks as static executables
- elf: Avoid deadlock between pthread_create and ctors [BZ #28357]
- time: Ignore interval nanoseconds on tst-itimer
- io: Do not skip timestamps tests for 32-bit time_t
- Update to Unicode 14.0.0 [BZ #28390]

* Fri Oct 01 2021 Florian Weimer <fweimer@redhat.com> - 2.34.9000-12
- Auto-sync with upstream branch master,
  commit eae81d70574e923ce3c59078b8df857ae192efa6:
- nptl: pthread_kill must send signals to a specific thread [BZ #28407]
- support: Add check for TID zero in support_wait_for_thread_exit
- nptl: Add CLOCK_MONOTONIC support for PI mutexes
- support: Add support_mutex_pi_monotonic
- nptl: Use FUTEX_LOCK_PI2 when available
- Linux: Add FUTEX_LOCK_PI2
- Add C2X _PRINTF_NAN_LEN_MAX
- Add exp10 macro to <tgmath.h> (bug 26108)
- elf: Replace nsid with args.nsid [BZ #27609]
- Add missing braces to bsearch inline implementation [BZ #28400]
- Update alpha libm-test-ulps
- Suppress -Wcast-qual warnings in bsearch
- elf: Copy l_addr/l_ld when adding ld.so to a new namespace
- powerpc: Fix unrecognized instruction errors with recent binutils

* Wed Sep 29 2021 Florian Weimer <fweimer@redhat.com> - 2.34.9000-11
- Drop glibc-rh1992702-*.patch, applied upstream.
- Auto-sync with upstream branch master,
  commit 9bd9978639c2f75dbea5c25226264b1ac11fdf05:
- Do not declare fmax, fmin _FloatN, _FloatNx versions for C2X
- Do not define tgmath.h fmaxmag, fminmag macros for C2X (bug 28397)
- Add fmaximum, fminimum functions
- Linux: Simplify __opensock and fix race condition [BZ #28353]
- pthread/tst-cancel28: Fix barrier re-init race condition
- powerpc: Delete unneeded ELF_MACHINE_BEFORE_RTLD_RELOC
- posix: Remove spawni.c
- Disable symbol hack in libc_nonshared.a
- linux: Revert the use of sched_getaffinity on get_nproc (BZ #28310)
- linux: Simplify get_nprocs
- misc: Add __get_nprocs_sched
- htl: Fix sigset of main thread
- htl: make pthread_sigstate read/write set/oset outside sigstate section
- Avoid warning: overriding recipe for .../tst-ro-dynamic-mod.so
- benchtests: Improve reliability of memcmp benchmarks
- Define __STDC_IEC_60559_BFP__ and __STDC_IEC_60559_COMPLEX__
- build-many-glibcs.py: add powerpc64le glibc variant without multiarch
- Fix sysdeps/x86/fpu/s_ffma.c for 32-bit FMA processor case
- Linux: Avoid closing -1 on failure in __closefrom_fallback
- i386: Port elf_machine_{load_address,dynamic} from x86-64
- aarch64: Disable A64FX memcpy/memmove BTI unconditionally
- xsysconf: Only fail on error results and errno set
- powerpc64le: Avoid conflicting types for f64xfmaf128 when IFUNC is not used
- Fix ffma use of round-to-odd on x86
- vfprintf: Unify argument handling in process_arg
- vfprintf: Handle floating-point cases outside of process_arg macro

* Thu Sep 23 2021 Florian Weimer <fweimer@redhat.com> - 2.34.9000-10
- Fix ppc64le build failure by reverting DL_RO_DYN_SECTION removal

* Thu Sep 23 2021 Florian Weimer <fweimer@redhat.com> - 2.34.9000-9
- Auto-sync with upstream branch master,
  commit 2849e2f53311b66853cb5159b64cba2bddbfb854:
- nptl: Avoid setxid deadlock with blocked signals in thread exit [BZ #28361]
- Add narrowing fma functions
- ld.so: Replace DL_RO_DYN_SECTION with dl_relocate_ld [BZ #28340]
- Adjust new narrowing div/mul tests for IBM long double, update powerpc ULPs
- Mention today's regex merge in SHARED-FILES
- Fix f64xdivf128, f64xmulf128 spurious underflows (bug 28358)
- regex: copy back from Gnulib
- nptl: Fix type of pthread_mutexattr_getrobust_np,
  pthread_mutexattr_setrobust_np (bug 28036)
- powerpc: Fix unrecognized instruction errors with recent GCC
- elf: Include <sysdep.h> in elf/dl-debug-symbols.S
- nptl: pthread_kill needs to return ESRCH for old programs (bug 19193)
- Extend struct r_debug to support multiple namespaces [BZ #15971]
- Use $(pie-default) with conformtest
- Run conform/ tests using newly built libc
- posix: Fix attribute access mode on getcwd [BZ #27476]
- Fix build-many-glibcs.py --strip for installed library renaming
- benchtests: Fix validate_benchout.py exceptions
- elf: Remove THREAD_GSCOPE_IN_TCB
- htl: Reimplement GSCOPE
- htl: Move thread table to ld.so
- Redirect fma calls to __fma in libm
- time: Fix compile error in itimer test affecting hurd

* Wed Sep 15 2021 Florian Weimer <fweimer@redhat.com> - 2.34.9000-8
- Use system CPU count for sysconf(_SC_NPROCESSORS_*) (#1992702)

* Wed Sep 15 2021 Florian Weimer <fweimer@redhat.com> - 2.34.9000-7
- Auto-sync with upstream branch master,
  commit 2444ce5421c6036a503842d8dd8d93c27aad59ee:
- mach lll_lock/unlock: Explicitly request private locking
- elf: Replace most uses of THREAD_GSCOPE_IN_TCB
- Add MADV_POPULATE_READ and MADV_POPULATE_WRITE from Linux 5.14 to
  bits/mman-linux.h
- Update kernel version to 5.14 in tst-mman-consts.py
- configure: Fix check for INSERT in linker script
- iconvconfig: Fix behaviour with --prefix [BZ #28199]
- nptl: Fix race between pthread_kill and thread exit (bug 12889)
- nptl: pthread_kill, pthread_cancel should not fail after exit (bug 19193)
- benchtests: Remove redundant assert.h
- benchtests: Enable scripts/plot_strings.py to read stdin
- Add narrowing square root functions
- _Static_assert needs two arguments for compatibility with GCC before 9
- testrun.sh: Add support for --tool=rpctrace

* Thu Sep 09 2021 Patsy Griffin <patsy@redhat.com> - 2.34.9000-6
- Auto-sync with upstream branch master,
  commit 89dc0372a9055e7ef86fe19be6201fa0b16b2f0e.
- Update syscall lists for Linux 5.14
- Fix failing nss/tst-nss-files-hosts-long with local resolver
- MIPS: Setup errno for {f,l,}xstat
- Use Linux 5.14 in build-many-glibcs.py
- locale: Add missing second argument to _Static_assert in C-collate-seq.c
- Update hppa libm-test-ulps
- Add generic C.UTF-8 locale (Bug 17318)
- Add 'codepoint_collation' support for LC_COLLATE.
- AArch64: Update A64FX memset not to degrade at 16KB
- Revert "AArch64: Update A64FX memset not to degrade at 16KB"
- Remove "Contributed by" lines
- Port shared code information from the wiki
- AArch64: Update A64FX memset not to degrade at 16KB
- posix: remove some iso-8859-encoded characters
- configure: Allow LD to be LLD 13.0.0 or above [BZ #26558]
- hurd msync: Drop bogus test
- hurd: Fix typo in msync

* Tue Aug 31 2021 Florian Weimer <fweimer@redhat.com> - 2.34.9000-5
- Auto-sync with upstream branch master,
  commit 3c8b9879cab6d41787bc5b14c1748f62fd6d0e5f:
- x86-64: Use testl to check __x86_string_control
- i686: Don't include multiarch memove in libc.a
- support: Add support_wait_for_thread_exit
- Allow #pragma GCC in headers in conformtest
- nptl: Fix tst-cancel7 and tst-cancelx7 race condition (BZ #14232)
- Use support_open_dev_null_range io/tst-closefrom,
  misc/tst-close_range, and posix/tst-spawn5 (BZ #28260)
- support: Add support_open_dev_null_range
- llio.texi: Wording fixes in description of closefrom()
- Fix error message in memmove test to display correct src pointer

* Wed Aug 25 2021 Arjun Shankar <arjun@redhat.com> - 2.34.9000-4
- Auto-sync with upstream branch master,
  commit 9926f6e2eeb374cf729d4bb3f092dd4b36a8f861:
- elf: Skip tst-auditlogmod-* if the linker doesn't support --depaudit [BZ #28151]
- powerpc: Use --no-tls-get-addr-optimize in test only if the linker supports it
- x86-64: Remove assembler AVX512DQ check
- x86-64: Remove compiler -mavx512f check
- Use __executable_start as the lowest address for profiling [BZ #28153]
- hurd: Fix errlist error mapping
- hurd: Remove old test-err_np.c file
- Fix iconv build with GCC mainline
- rtld: copy terminating null in tunables_strdup (bug 28256)
- mtrace: Fix output with PIE and ASLR [BZ #22716]
- x86-64: Optimize load of all bits set into ZMM register [BZ #28252]
- Update string/test-memmove.c to cover 16KB copy
- elf: Fix missing colon in LD_SHOW_AUXV output [BZ #28253]
- x86: fix Autoconf caching of instruction support checks [BZ #27991]
- arm: Simplify elf_machine_{load_address,dynamic}
- riscv: Drop reliance on _GLOBAL_OFFSET_TABLE_[0]
- Remove sysdeps/*/tls-macros.h

* Tue Aug 24 2021 Siddhesh Poyarekar <siddhesh@redhat.com> - 2.34.9000-3
- Disable dependencies and linking for libc_malloc_debug.so (#1985048).

* Tue Aug 17 2021 DJ Delorie <dj@redhat.com> - 2.34.9000-2
- Auto-sync with upstream branch master,
  commit b37b75d269883a2c553bb7019a813094eb4e2dd1.
- x86_64: Simplify elf_machine_{load_address,dynamic}
- elf: Drop elf/tls-macros.h in favor of __thread and tls_model attributes [BZ #28152] [BZ #28205]
- hurd: Drop fmh kludge
- time: Fix overflow itimer tests on 32-bit systems
- mips: increase stack alignment in clone to match the ABI
- mips: align stack in clone [BZ #28223]


* Thu Aug 12 2021 Arjun Shankar <arjun@redhat.com> - 2.34.9000-1
- Auto-sync with upstream branch master,
  commit 4cc79c217744743077bf7a0ec5e0a4318f1e6641:
- librt: add test (bug 28213)
- mtrace: Use a static buffer for printing [BZ #25947]
- hurd mmap: Reduce the requested max vmprot
- hurd mmap: Factorize MAP_SHARED flag check
- aarch64: Make elf_machine_{load_address,dynamic} robust [BZ #28203]
- elf: Unconditionally use __ehdr_start
- hurd: Add support for AT_NO_AUTOMOUNT
- [5/5] AArch64: Improve A64FX memset medium loops
- [4/5] AArch64: Improve A64FX memset by removing unroll32
- [3/5] AArch64: Improve A64FX memset for remaining bytes
- [2/5] AArch64: Improve A64FX memset for large sizes
- [1/5] AArch64: Improve A64FX memset for small sizes
- Use binutils 2.37 branch in build-many-glibcs.py
- Add PTRACE_GET_RSEQ_CONFIGURATION from Linux 5.13 to sys/ptrace.h
- librt: fix NULL pointer dereference (bug 28213)
- powerpc64: Add checks for Altivec and VSX in ifunc selection
- powerpc64: Check cacheline size before using optimised memset routines
- powerpc64: Replace some PPC_FEATURE_HAS_VSX with PPC_FEATURE_ARCH_2_06
- Linux: Fix fcntl, ioctl, prctl redirects for _TIME_BITS=64 (bug 28182)
- Add INADDR_DUMMY from Linux 5.13 to netinet/in.h
- tst-mxfast: Don't run with mcheck
- rt: Set the correct message queue for tst-mqueue10
- Update sparc libm-test-ulps
- linux: Add sparck brk implementation
- test-dlclose-exit-race: avoid hang on pthread_create error
- gethosts: Remove unused argument _type
- hurd: Avoid spurious warning
- gaiconf_init: Avoid double-free in label and precedence lists
- copy_and_spawn_sgid: Avoid double calls to close()
- iconv_charmap: Close output file when done
- gconv_parseconfdir: Fix memory leak
- ldconfig: avoid leak on empty paths in config file
- Fix build of nptl/tst-thread_local1.cc with GCC 12
- nis: Fix leak on realloc failure in nis_getnames [BZ #28150]
- Remove obsolete comments/name from several benchtest input files.
- Remove obsolete comments/name from acos-inputs, since slow path was removed.
- Open master branch for glibc 2.35 development

* Mon Aug  2 2021 Florian Weimer <fweimer@redhat.com> - 2.34-1
- Switch to glibc 2.34 release tarball:
- Update ChangeLog.old/ChangeLog.23.
- Prepare for glibc 2.34 release.
- po/nl.po: Update Dutch translation.
- Update install.texi, and regenerate INSTALL.
- Update translations.
- Update NEWS.
- NEWS: Fix typos, grammar, and missing words
- elf: Fix audit regression
