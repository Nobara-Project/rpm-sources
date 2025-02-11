%global __brp_mangle_shebangs %{nil}
%bcond_without mold

%global _description %{expand:
pbcli is a command line client which allows to upload and download pastes from privatebin directly from the command line.}

Name:           pbcli
Version:        2.6.0
Release:        1%?dist
Summary:        A PrivateBin commandline upload and download utility
SourceLicense:  Unlicense OR MIT
License:        (0BSD OR MIT OR Apache-2.0) AND Apache-2.0 AND (Apache-2.0 OR BSL-1.0) AND (Apache-2.0 OR ISC OR MIT) AND (Apache-2.0 OR MIT) AND ((Apache-2.0 OR MIT) AND BSD-3-Clause) AND (Apache-2.0 WITH LLVM-exception OR Apache-2.0 OR MIT) AND (BSD-2-Clause OR Apache-2.0 OR MIT) AND BSD-3-Clause AND ISC AND MIT AND (MIT OR Apache-2.0) AND (MIT OR Apache-2.0 OR Zlib) AND (MIT OR Zlib OR Apache-2.0) AND MPL-2.0 AND (Unlicense OR MIT) AND (Zlib OR Apache-2.0 OR MIT)
URL:            https://github.com/Mydayyy/pbcli
Source0:        %url/archive/refs/tags/v%version.tar.gz
Source1:	config

ExclusiveArch:	x86_64

BuildRequires:  cargo-rpm-macros >= 24
BuildRequires:  mold
BuildRequires:  perl-IPC-Cmd perl-ExtUtils-MM-Utils perl-FindBin perl-lib perl-File-Compare perl-File-Copy
BuildRequires:  openssl-libs openssl-devel
Packager:       ShinyGil <rockgrub@protonmail.com>

%description 	%_description

%package	nobara
Summary:	paste.gloriouseggroll.tv config file
Requires:	%{name}

%description	nobara
%summary.

%prep
%autosetup -n pbcli-%version
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
install -Dm755 target/rpm/pbcli %{buildroot}%{_bindir}/pbcli
install -Dm755 target/rpm/libpbcli.so %{buildroot}%{_libdir}/libpbcli.so
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/
install -m 0644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/config
ln -sf %_bindir/pbcli %{buildroot}%{_bindir}/eggpaste

%files
%doc README.md
%license LICENSE-MIT
%license LICENSE-UNLICENSE
%license LICENSE.dependencies
%_bindir/pbcli
%_libdir/libpbcli.so

%files nobara
%{_sysconfdir}/%{name}/config
%_bindir/eggpaste

%changelog
* Tue Feb 11 2025 LionHeartP <LionHeartP@proton.me>
- Adapt for Nobara

* Sat Dec 21 2024 ShinyGil <rockgrub@protonmail.com>
- Initial package
