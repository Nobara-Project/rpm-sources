%global _description %{expand:
pbcli is a command line client which allows to upload and download pastes from privatebin directly from the command line.}

Name:           pbcli
Version:        2.9.0
Release:        1%?dist
Summary:        A PrivateBin commandline upload and download utility
SourceLicense:  Unlicense OR MIT
License:        ((Apache-2.0 OR MIT) AND BSD-3-Clause) AND (0BSD OR MIT OR Apache-2.0) AND (Apache-2.0 AND ISC) AND (Apache-2.0 OR BSL-1.0) AND (Apache-2.0 OR ISC OR MIT) AND (Apache-2.0 OR MIT) AND (Apache-2.0 WITH LLVM-exception OR Apache-2.0 OR MIT) AND Apache-2.0 AND (BSD-2-Clause OR Apache-2.0 OR MIT) AND BSD-3-Clause AND ISC AND (MIT OR Apache-2.0 OR Zlib) AND (MIT OR Apache-2.0) AND (MIT OR Zlib OR Apache-2.0) AND MIT AND MPL-2.0 AND (Unlicense OR MIT) AND (Zlib OR Apache-2.0 OR MIT)
URL:            https://github.com/Mydayyy/%{name}
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz
Source1:	config
Patch0:     0001-add-url-shortener-support.patch
ExclusiveArch:	x86_64 aarch64

BuildRequires:  cargo-rpm-macros >= 24
BuildRequires:  mold
BuildRequires:  openssl-libs
BuildRequires:  perl-ExtUtils-MM-Utils
BuildRequires:  perl-FindBin
BuildRequires:  perl-File-Compare
BuildRequires:  perl-File-Copy
BuildRequires:  perl-IPC-Cmd
BuildRequires:  perl-lib
Packager:       Gilver E. <rockgrub@disroot.org>

%description 	%_description

%package	nobara
Summary:	paste.nobaraproject.org config file
Requires:	%{name}

%description	nobara
%summary.

%package        devel
Summary:        Development libraries for %{name}
Requires:       %{name}

%description    devel
This package contains the development files for %{name}.

%prep
%autosetup -n pbcli-%version -p1
set -eu
%{__mkdir} -p .cargo
cat > .cargo/config << EOF
[profile.rpm]
inherits = "release"
opt-level = 3
codegen-units = 1
debug = 2
strip = "none"


[build]
rustc = "%{__rustc}"
rustdoc = "%{__rustdoc}"

[env]
CFLAGS = "%{build_cflags}"
CXXFLAGS = "%{build_cxxflags}"
LDFLAGS = "%{build_ldflags}"

[install]
root = "%{buildroot}%{_prefix}"

[term]
verbose = true

[source]

[source.local-registry]
directory = "%{cargo_registry}"

EOF
%{__rm} -f Cargo.toml.orig 
%global build_rustflags %build_rustflags %[%{with mold} ? "-C link-arg=-fuse-ld=mold" : ""]

%build
%cargo_build
set -euo pipefail
%{shrink:
    %{__cargo} tree
    -Z avoid-dev-deps
    --workspace
    --edges no-build,no-dev,no-proc-macro
    --no-dedupe
    --target all
    %{__cargo_parse_opts %{-n} %{-a} %{-f:-f%{-f*}}}
    --prefix none
    --format "{l}: {p}"
    | sed -e "s: ($(pwd)[^)]*)::g" -e "s: / :/:g" -e "s:/: OR :g"
    | sort -u
} > LICENSE.dependencies

%install
install -Dm755 target/rpm/%{name} %{buildroot}%{_bindir}/%{name}
install -Dm755 target/rpm/lib%{name}.so %{buildroot}%{_libdir}/lib%{name}.so
install -Dm644 target/rpm/lib%{name}.a %{buildroot}%{_libdir}/lib%{name}.a
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/
install -m 0644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/config
ln -sf %_bindir/pbcli %{buildroot}%{_bindir}/eggpaste
ln -sf %_bindir/pbcli %{buildroot}%{_bindir}/npaste

%files
%doc README.md
%license LICENSE-MIT
%license LICENSE-UNLICENSE
%license LICENSE.dependencies
%{_bindir}/%{name}

%files devel
%{_libdir}/lib%{name}.a
%{_libdir}/lib%{name}.so

%files nobara
%{_sysconfdir}/%{name}/config
%_bindir/eggpaste
%_bindir/npaste

%changelog
* Tue Apr 14 2026 LionHeartP <LionHeartP@proton.me> - 2.9.0-1
- Update to 2.9.0

* Mon Mar 09 2026 Radical <radical@radical.fun>
- Change ExclusiveArch to allow building for aarch64

* Sat Mar 15 2025 Gilver E. <rockgrub@disroot.org>
- Enable uniffi support
- Package development files

* Tue Feb 11 2025 LionHeartP <LionHeartP@proton.me>
- Adapt for Nobara

* Sat Dec 21 2024 Gilver E. <rockgrub@disroot.org>
- Initial package
