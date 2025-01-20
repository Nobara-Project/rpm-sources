# https://ziglang.org/download/%{version}/release-notes.html#Support-Table
# 32 bit builds currently run out of memory https://github.com/ziglang/zig/issues/6485
%global         zig_arches x86_64 aarch64 riscv64 %{mips64}
# Signing key from https://ziglang.org/download/
%global         public_key RWSGOq2NVecA2UPNdBUZykf1CCb147pkmdtYxgb3Ti+JO/wCYvhbAb/U

%global         llvm_version 19.0.0


%bcond bootstrap 1
%bcond docs     %{without bootstrap}
%bcond macro    %{without bootstrap}
%bcond test     1

%define prerelease dev.2649+77273103a

Name:           zig-nightly
Version:        0.14.0

%if "%{prerelease}" == "1"
Release:        1%{?dist}
%else
Release:        0%{prerelease}%{?dist}
%endif

Summary:        Programming language for maintaining robust, optimal, and reusable software

License:        MIT and NCSA and LGPLv2+ and LGPLv2+ with exceptions and GPLv2+ and GPLv2+ with exceptions and BSD and Inner-Net and ISC and Public Domain and GFDL and ZPLv2.1
URL:            https://ziglang.org

%if "%{prerelease}" == "1"
Source0:        %{url}/builds/zig-%{version}.tar.xz
Source1:        %{url}/builds/zig-%{version}.tar.xz.minisig
%else
Source0:        %{url}/builds/zig-%{version}-%{prerelease}.tar.xz
Source1:        %{url}/builds/zig-%{version}-%{prerelease}.tar.xz.minisig
%endif

Source2:        macros.zig
# Support clean build of stage3 with temporary bootstrapped package
Patch:          0001-Fedora-bootstrap-and-extra-build-flags-support.patch
# There's no global option for build-id so enable it by default
# instead of patching every project's build.zig
Patch:          0002-Enable-build-id-by-default.patch

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  llvm-devel
BuildRequires:  clang-devel
BuildRequires:  lld-devel
BuildRequires:  zlib-devel
BuildRequires:  libxml2-devel
# for man page generation
BuildRequires:  help2man
# for signature verification
BuildRequires:  minisign

%if %{without bootstrap}
BuildRequires:  %{name} = %{version}
%endif

%if %{with test}
# for testing
BuildRequires:  elfutils-libelf-devel
BuildRequires:  libstdc++-static
%endif

Requires:       %{name}-libs = %{version}
Conflicts:	zig

# These packages are bundled as source

# Apache-2.0 WITH LLVM-exception OR NCSA OR MIT
Provides: bundled(compiler-rt) = %{llvm_version}
# LGPLv2+, LGPLv2+ with exceptions, GPLv2+, GPLv2+ with exceptions, BSD, Inner-Net, ISC, Public Domain and GFDL
Provides: bundled(glibc) = 2.34
# Apache-2.0 WITH LLVM-exception OR MIT OR NCSA
Provides: bundled(libcxx) = %{llvm_version}
# Apache-2.0 WITH LLVM-exception OR MIT OR NCSA
Provides: bundled(libcxxabi) = %{llvm_version}
# NCSA
Provides: bundled(libunwind) = %{llvm_version}
# BSD, LGPG, ZPL
Provides: bundled(mingw) = 10.0.0
# MIT
Provides: bundled(musl) = 1.2.4
# Apache-2.0 WITH LLVM-exception AND Apache-2.0 AND MIT AND BSD-2-Clause
Provides: bundled(wasi-libc) = 3189cd1ceec8771e8f27faab58ad05d4d6c369ef

ExclusiveArch: %{zig_arches}

%description
Zig is an open-source programming language designed for robustness, optimality,
and clarity. This package provides the zig compiler and the associated runtime.

# The Zig stdlib only contains uncompiled code
%package libs
Summary:        zig Standard Library
BuildArch:      noarch

Conflicts:	zig-libs

%description libs
zig Standard Library

%if %{with docs}
%package doc
Summary:        Documentation for zig
BuildArch:      noarch
Requires:       %{name} = %{version}

%description doc
Documentation for zig. For more information, visit %{url}
%endif

%if %{with macro}
%package        rpm-macros
Summary:        Common RPM macros for zig
Requires:       rpm
BuildArch:      noarch

%description    rpm-macros
This package contains common RPM macros for zig.
%endif

%prep
/usr/bin/minisign -V -m %{SOURCE0} -x %{SOURCE1} -P %{public_key}

%if "%{prerelease}" == "1"
%autosetup -p1 -n zig-%{version}
%else
%autosetup -p1 -n zig-%{version}-%{prerelease}
%endif

%if %{without bootstrap}
# Ensure that the pre-build stage1 binary is not used
rm -f stage1/zig1.wasm
%endif

%build
# C_FLAGS: wasm2c output generates a lot of noise with -Wunused.
# EXTRA_BUILD_ARGS: apply --build-id=sha1 even if running unpatched stage2 compiler.
%cmake \
    -DCMAKE_BUILD_TYPE:STRING=RelWithDebInfo \
    -DCMAKE_C_FLAGS_RELWITHDEBINFO:STRING="-DNDEBUG -Wno-unused" \
    -DCMAKE_CXX_FLAGS_RELWITHDEBINFO:STRING="-DNDEBUG -Wno-unused" \
    -DZIG_EXTRA_BUILD_ARGS:STRING="--verbose" \
    -DZIG_SHARED_LLVM:BOOL=true \
    -DZIG_TARGET_MCPU:STRING=baseline \
    -DZIG_TARGET_TRIPLE:STRING=native \
    -DZIG_VERSION:STRING="%{version}" \
    %{!?with_bootstrap:-DZIG_EXECUTABLE:STRING="/usr/bin/zig"}
# Build only stage3 and dependencies. Skips stage1/2 if using /usr/bin/zig
%cmake_build --target stage3

# Zig has no official manpage
# https://github.com/ziglang/zig/issues/715
help2man --no-discard-stderr --no-info "%{__cmake_builddir}/stage3/bin/zig" --version-option=version --output=zig.1

%if %{with docs}
"%{__cmake_builddir}/stage3/bin/zig" build docs --verbose -Dversion-string="%{version}"
%endif

%install
# Ignore standard RPATH for now
export QA_RPATHS=$(( 0x0001 ))

%cmake_install

install -D -pv -m 0644 -t %{buildroot}%{_mandir}/man1/ zig.1

%if %{with macro}
install -D -pv -m 0644 %{SOURCE2} %{buildroot}%{_rpmmacrodir}/macros.zig
%endif

%if %{with test}
%check
# Run reduced set of tests, based on the Zig CI
"%{__cmake_builddir}/stage3/bin/zig" test test/behavior.zig -Itest
%endif

%files
%license LICENSE
%{_bindir}/zig
%{_mandir}/man1/zig.1.*

%files libs
%{_prefix}/lib/zig

%if %{with docs}
%files doc
%doc README.md
%doc zig-out/doc/langref.html
%doc zig-out/doc/std
%endif

%if %{with macro}
%files rpm-macros
%{_rpmmacrodir}/macros.zig
%endif

%changelog
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
