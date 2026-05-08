%if 0%{?rhel}
# Zig depends on a C compiler (gcc) during bootstraping
# older versions of gcc fail to compile the transpiled source so we limit it to x86_64
%global         zig_arches x86_64
%else
# https://ziglang.org/download/VERSION/release-notes.html#Support-Table
%global         zig_arches x86_64 aarch64 riscv64 %{mips64}
%endif
# Signing key from https://ziglang.org/download/
%global         public_key RWSGOq2NVecA2UPNdBUZykf1CCb147pkmdtYxgb3Ti+JO/wCYvhbAb/U

# note here at which Fedora or EL release we need to use compat LLVM packages
%if 0%{?fedora} >= 44 || 0%{?rhel} >= 11
%global         llvm_compat 21
%endif

%global         llvm_version 21.1.8

%bcond bootstrap 0
%bcond docs      %{without bootstrap}
%bcond macro     %{without bootstrap}
%bcond test      1

# GCC < 16.0 miscompiles on RISC-V 
%ifarch riscv64
%if 0%{?fedora} < 44
%bcond toolchain_clang 1
%endif
%endif

%if %{with toolchain_clang}
%global toolchain clang
%endif

%global zig_cache_dir %{_vpath_builddir}/zig-cache

%global zig_build_options %{shrink: \
    --verbose \
    --release=fast \
    --summary all \
    \
    -Dtarget=native \
    -Dcpu=baseline \
    --zig-lib-dir lib \
    --build-id=sha1 \
    \
    --cache-dir "%{zig_cache_dir}" \
    --global-cache-dir "%{zig_cache_dir}" \
    \
    -Dversion-string="%{version}" \
    -Dstatic-llvm=false \
    -Denable-llvm=true \
    -Dno-langref=true \
    -Dstd-docs=false \
    -Dpie \
    -Dconfig_h="%{__cmake_builddir}/config.h" \
}
%global zig_install_options %zig_build_options %{shrink: \
    --prefix "%{_prefix}" \
}

Name:           zig
Version:        0.16.0
Release:        1%{?dist}
Summary:        Programming language for maintaining robust, optimal, and reusable software
# The minisign file references a specific archive name so we store for ease of use
%global         archive_name %{name}-%{version}.tar.xz

License:        MIT AND NCSA AND LGPL-2.1-or-later AND LGPL-2.1-or-later WITH GCC-exception-2.0 AND GPL-2.0-or-later AND GPL-2.0-or-later WITH GCC-exception-2.0 AND BSD-3-Clause AND Inner-Net-2.0 AND ISC AND LicenseRef-Fedora-Public-Domain AND GFDL-1.1-or-later AND ZPL-2.1
URL:            https://ziglang.org
Source0:        %{url}/download/%{version}/%{archive_name}
Source1:        %{url}/download/%{version}/%{archive_name}.minisig
Source2:        macros.%{name}
# Remove native lib directories from rpath
# this is unlikely to be upstreamed in its current state because upstream
# wants to work around the shortcomings of NixOS
Patch0:         0001-remove-native-lib-directories-from-rpath.patch
# LLVM on RHEL/EPEL only provides fewer targets so we patch the required targets down
# Targets come from https://src.fedoraproject.org/rpms/llvm/blob/rawhide/f/llvm.spec
Patch1:         0002-Remove-unsupported-LLVM-targets-for-EPEL.patch

%if %{without toolchain_clang}
BuildRequires:  gcc
BuildRequires:  gcc-c++
%else
BuildRequires:  clang
%endif
BuildRequires:  cmake
BuildRequires:  llvm%{?llvm_compat}-devel
BuildRequires:  clang%{?llvm_compat}-devel
BuildRequires:  lld%{?llvm_compat}-devel
BuildRequires:  zlib-devel
BuildRequires:  libxml2-devel
# for man page generation
BuildRequires:  help2man
# for signature verification
BuildRequires:  minisign

%if %{without bootstrap}
BuildRequires:  (zig >= 0.16 with zig < 0.17)
%endif

%if %{with test}
# for testing
BuildRequires:  elfutils-libelf-devel
BuildRequires:  libstdc++-static
%endif

Requires:       %{name}-libs = %{version}

# These packages are bundled as source

# Apache-2.0 WITH LLVM-exception OR NCSA OR MIT
Provides: bundled(compiler-rt) = %{llvm_version}
# LGPL-2.1-or-later AND SunPro AND LGPL-2.1-or-later WITH GCC-exception-2.0 AND BSD-3-Clause AND GPL-2.0-or-later AND LGPL-2.1-or-later WITH GNU-compiler-exception AND GPL-2.0-only AND ISC AND LicenseRef-Fedora-Public-Domain AND HPND AND CMU-Mach AND LGPL-2.0-or-later AND Unicode-3.0 AND GFDL-1.1-or-later AND GPL-1.0-or-later AND FSFUL AND MIT AND Inner-Net-2.0 AND X11 AND GPL-2.0-or-later WITH GCC-exception-2.0 AND GFDL-1.3-only AND GFDL-1.1-only
Provides: bundled(glibc) = 2.43
# Apache-2.0 WITH LLVM-exception OR MIT OR NCSA
Provides: bundled(libcxx) = %{llvm_version}
# Apache-2.0 WITH LLVM-exception OR MIT OR NCSA
Provides: bundled(libcxxabi) = %{llvm_version}
# NCSA
Provides: bundled(libunwind) = %{llvm_version}
# BSD, LGPG, ZPL
Provides: bundled(mingw) = 3839e21b08807479a31d5a9764666f82ae2f0356
# MIT
Provides: bundled(musl) = 1.2.5
# Apache-2.0 WITH LLVM-exception AND Apache-2.0 AND MIT AND BSD-2-Clause
Provides: bundled(wasi-libc) = d03829489904d38c624f6de9983190f1e5e7c9c5

ExclusiveArch: %{zig_arches}

%description
Zig is an open-source programming language designed for robustness, optimality,
and clarity. This package provides the zig compiler and the associated runtime.

# The Zig stdlib only contains uncompiled code
%package libs
Summary:        %{name} Standard Library
BuildArch:      noarch

%description libs
%{name} Standard Library

%if %{with docs}
%package doc
Summary:        Documentation for %{name}
BuildArch:      noarch
Requires:       %{name} = %{version}

%description doc
Documentation for %{name}. For more information, visit %{url}
%endif

%if %{with macro}
%package        rpm-macros
Summary:        Common RPM macros for %{name}
Requires:       rpm
BuildArch:      noarch

%description    rpm-macros
This package contains common RPM macros for %{name}.
%endif

%prep
/usr/bin/minisign -V -m %{SOURCE0} -x %{SOURCE1} -P %{public_key} -Q | grep -F "file:%{archive_name}"

%autosetup -N
%patch 0 -p1
%if 0%{?rhel}
%patch 1 -p1
%endif

%if %{without bootstrap}
# Ensure that the pre-build stage1 binary is not used
rm -f stage1/zig1.wasm
%endif

%build

# Fedora supports using ccache systemwide
# Zig generates a large C file for bootstrapping which does not
# behave well with ccache so we explicitly disable it.
export CCACHE_DISABLE=1

# zig doesn't know how to dynamically link llvm on its own so we need cmake to generate a header ahead of time
# if we provide the header we need to also build zigcpp

# C_FLAGS: wasm2c output generates a lot of noise with -Wunused.
# EXTRA_BUILD_ARGS: explicitly specify a build-id
%cmake \
    -DCMAKE_BUILD_TYPE:STRING=RelWithDebInfo \
    -DCMAKE_C_FLAGS_RELWITHDEBINFO:STRING="-DNDEBUG -Wno-unused" \
    -DCMAKE_CXX_FLAGS_RELWITHDEBINFO:STRING="-DNDEBUG -Wno-unused" \
    \
    -DZIG_EXTRA_BUILD_ARGS:STRING="--verbose;--build-id=sha1" \
    -DZIG_SHARED_LLVM:BOOL=true \
    -DZIG_PIE:BOOL=true \
    \
    -DZIG_TARGET_MCPU:STRING=baseline \
    -DZIG_TARGET_TRIPLE:STRING=native \
    \
    -DZIG_VERSION:STRING="%{version}"

%if %{with bootstrap}
%cmake_build --target stage3
%else
%cmake_build --target zigcpp
zig build %{zig_build_options}

# Zig has no official manpage
# https://github.com/ziglang/zig/issues/715
help2man --no-discard-stderr --no-info "./zig-out/bin/zig" --version-option=version --output=zig.1
%endif


%if %{with docs}
# Use the newly made stage 3 compiler to generate docs 
./zig-out/bin/zig build docs %{zig_build_options}
%endif

%install
%if %{with bootstrap}
%cmake_install
%else
DESTDIR="%{buildroot}" zig build install %{zig_install_options}

install -D -pv -m 0644 -t %{buildroot}%{_mandir}/man1/ zig.1
%endif


%if %{with macro}
install -D -pv -m 0644 %{SOURCE2} %{buildroot}%{_rpmmacrodir}/macros.%{name}
%endif

%if %{with test}
%check
# Run reduced set of tests, based on the Zig CI
"%{buildroot}%{_bindir}/zig" test test/behavior.zig -Itest
%endif

%files
%license LICENSE
%{_bindir}/zig
%if %{without bootstrap}
%{_mandir}/man1/%{name}.1.*
%endif

%files libs
%{_prefix}/lib/%{name}

%if %{with docs}
%files doc
%doc README.md
%doc zig-out/doc/langref.html
%doc zig-out/doc/std
%endif

%if %{with macro}
%files rpm-macros
%{_rpmmacrodir}/macros.%{name}
%endif

%changelog
* Wed Apr 15 2026 Jan200101 <sentrycraft123@gmail.com> - 0.16.0-1
- Update to 0.16.0

* Sat Jan 17 2026 Fedora Release Engineering <releng@fedoraproject.org> - 0.15.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Sun Jan 04 2026 Jan200101 <sentrycraft123@gmail.com> - 0.15.2-2
- Rebuilt for EPEL

* Sun Oct 12 2025 Jan200101 <sentrycraft123@gmail.com> - 0.15.2-1
- Update to 0.15.2

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 09 2025 Jan200101 <sentrycraft123@gmail.com> - 0.14.1-1
- Update to 0.14.1

* Tue May 27 2025 Jan200101 <sentrycraft123@gmail.com> - 0.14.0-4
- add patch to add library directories

* Fri May 09 2025 Jan200101 <sentrycraft123@gmail.com> - 0.14.0-3
- add gcc to runtime dependencies

* Thu Apr 24 2025 Jan200101 <sentrycraft123@gmail.com> - 0.14.0-2
- fix and re-enable documentation

* Thu Mar 06 2025 Jan200101 <sentrycraft123@gmail.com> - 0.14.0-1
- Update to 0.14.0

* Mon Jan 27 2025 Jan200101 <sentrycraft123@gmail.com> - 0.13.0-8
- specify to build against local zig stdlib directory to ensure we are building against the newest stdlib
- use release fast instead of release safe to fix aarch64 builds from running out of memory
- enable position independent executable for the zig build

* Mon Jan 27 2025 Jan200101 <sentrycraft123@gmail.com> - 0.13.0-7
- build stage 3 using zig build system
- add user provided options to the end of the build and install options

* Thu Jan 23 2025 Jan200101 <sentrycraft123@gmail.com> - 0.13.0-6
- rebuild against fixed llvm

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sun Dec 29 2024 Jan200101 <sentrycraft123@gmail.com> - 0.13.0-4
- correct macro variables
- set llvm_compat for F41
- update callaway licenses to follow SPDX

* Wed Sep 04 2024 Miroslav Suchý <msuchy@redhat.com> - 0.13.0-3
- convert license to SPDX

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jun 11 2024 Jan200101 <sentrycraft123@gmail.com> - 0.13.0-1
- Update to 0.13.0

* Sat Jun 08 2024 Jan200101 <sentrycraft123@gmail.com> - 0.12.1-1
- Update to 0.12.1

* Sat May 25 2024 Jan200101 <sentrycraft123@gmail.com> - 0.12.0-1
- Update to 0.12.0

* Wed Feb 21 2024 Jan Drögehoff <sentrycraft123@gmail.com> - 0.11.0-2
- Rebuilt for bootstrapping

* Sat Jan 27 2024 Aleksei Bavshin <alebastr@fedoraproject.org> - 0.11.0-1
- Update to 0.11.0

* Sat Jan 27 2024 Aleksei Bavshin <alebastr@fedoraproject.org> - 0.9.1-6
- Fix build with `--without macro`
- Skip %%check and test dependencies when tests are disabled
- Drop %%_zig_version macro

* Sat Jan 27 2024 Benson Muite <benson_muite@emailplus.org> - 0.9.1-6
- Verify source signature

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Feb 18 2022 Jan Drögehoff <sentrycraft123@gmail.com> - 0.9.1-1
- Update to 0.9.1

* Thu Jan 27 2022 Jan Drögehoff <sentrycraft123@gmail.com> - 0.9.0-3
- Jan: add rpath patch
- Aleksei Bavshin: rpm macros: set default build flags

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Dec 20 2021 Jan Drögehoff <sentrycraft123@gmail.com> - 0.9.0-1
- Update to 0.9.0

* Wed Nov 17 2021 Jan Drögehoff <sentrycraft123@gmail.com> - 0.8.1-5
- Enable documentation on Fedora 35

* Tue Nov 09 2021 Tom Stellard <tstellar@redhat.com> - 0.8.1-4
- Rebuild for llvm-13.0.0

* Sat Oct 30 2021 Jan Drögehoff <sentrycraft123@gmail.com> - 0.8.1-3
- Update LLVM13 Patch

* Thu Oct 07 2021 Tom Stellard <tstellar@redhat.com> - 0.8.1-2
- Rebuild for llvm-13.0.0

* Sun Sep 12 2021 Jan Drögehoff <sentrycraft123@gmail.com> - 0.8.1-1
- Update to Zig 0.8.1, add LLVM 13 patch

* Wed Aug 18 2021 Jan Drögehoff <sentrycraft123@gmail.com> - 0.8.0-8
- Rebuilt for lld soname bump

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jul 19 2021 Jan Drögehoff <sentrycraft123@gmail.com> - 0.8.0-6
- add native libc detection patch

* Sun Jul 04 2021 Jan Drögehoff <sentrycraft123@gmail.com> - 0.8.0-5
- correct newline in macro that caused DESTDIR to be ignored

* Mon Jun 28 2021 Jan Drögehoff <sentrycraft123@gmail.com> - 0.8.0-4
- correct macro once again to allow for proper packaging

* Thu Jun 24 2021 Jan Drögehoff <sentrycraft123@gmail.com> - 0.8.0-3
- improve macro for using the zig binary

* Thu Jun 24 2021 Jan Drögehoff <sentrycraft123@gmail.com> - 0.8.0-2
- Update patches, correct rpm macro

* Sat Jun 05 2021 Jan Drögehoff <sentrycraft123@gmail.com> - 0.8.0-1
- Update to Zig 0.8.0

* Sun Dec 13 23:18:24 CET 2020 Jan Drögehoff <sentrycraft123@gmail.com> - 0.7.1-1
- Update to Zig 0.7.1

* Wed Nov 11 17:18:27 CET 2020 Jan Drögehoff <sentrycraft123@gmail.com> - 0.7.0-1
- Update to Zig 0.7.0

* Tue Aug 18 2020 Jan Drögehoff <sentrycraft123@gmail.com> - 0.6.0-1
- Initial zig spec
