%define _disable_source_fetch 0

Name:           scx-scheds
Version:        1.1.0
Release:        1%{?dist}
Summary:        Sched_ext Schedulers and Tools

License:        GPL=2.0
URL:            https://github.com/sched-ext/scx
Source0:        %{URL}/archive/refs/tags/v%{version}.tar.gz

# https://fedoraproject.org/wiki/Changes/EncourageI686LeafRemoval
ExcludeArch:    %{ix86}

BuildRequires:  gcc
BuildRequires:  git
BuildRequires:  python
BuildRequires:  cargo
BuildRequires:  rust
BuildRequires:  clang >= 17
BuildRequires:  llvm >= 17
BuildRequires:  lld >= 17
BuildRequires:  elfutils-libelf
BuildRequires:  elfutils-libelf-devel
BuildRequires:  zlib
BuildRequires:  jq
BuildRequires:  jq-devel
BuildRequires:  systemd
BuildRequires:  bpftool
BuildRequires:  protobuf-compiler
BuildRequires:  libseccomp-devel
Requires:  elfutils-libelf
Requires:  libseccomp
Requires:  protobuf
Requires:  zlib
Requires:  jq
Requires:  scx-tools
Conflicts: scx-scheds-git
Conflicts: scx_layered
Conflicts: scx_rustland
Conflicts: scx_rusty
Conflicts: rust-scx_utils-devel
Provides: scx_layered
Provides: scx_rustland
Provides: scx_rusty
Provides: rust-scx_utils-devel

%description
sched_ext is a Linux kernel feature which enables implementing kernel thread schedulers in BPF and dynamically loading them. This repository contains various scheduler implementations and support utilities.

%prep
%autosetup -n scx-%{version}


%build
export CARGO_HOME=%{_builddir}/.cargo
cargo fetch --locked
cargo build \
     --release \
     --frozen \
     --all-features \
     --workspace \
     --exclude scx_rlfifo \
     --exclude scx_mitosis \
     --exclude scx_wd40 \
     --exclude xtask \
     --exclude scxcash \
     --exclude vmlinux_docify \
     --exclude scx_arena_selftests

%install

# Install all built executables (skip .so and .d files)
find target/release \
    -maxdepth 1 -type f -executable ! -name '*.so' \
    -exec install -Dm755 -t %{buildroot}%{_bindir} {} +

%files

# Binaries
%{_bindir}/*

%changelog
* Sat Mar 07 2026 LionHeartP <LionHeartP@proton.me> - 1.1.0-1
- Update to 1.1.0

* Sat Feb 07 2026 LionHeartP <LionHeartP@proton.me> - 1.0.20-1
- Update to 1.0.20

* Wed Dec 03 2025 LionHeartP <LionHeartP@proton.me> - 1.0.19-1
- Update to 1.0.19
- Remove explicit version requirement with scx-tools

* Wed Nov 12 2025 LionHeartP <LionHeartP@proton.me> - 1.0.18-1
- Update to 1.0.18
- Swap to cargo build

* Wed Oct 08 2025 LionHeartP <LionHeartP@proton.me> - 1.0.17-1
- Update to 1.0.17

* Sat Sep 06 2025 LionHeartP <LionHeartP@proton.me> - 1.0.16-1
- Update to 1.0.16

* Mon Aug 18 2025 LionHeartP <LionHeartP@proton.me> - 1.0.15-2
- Add patch for forced scx setting

* Wed Aug 13 2025 LionHeartP <LionHeartP@proton.me> - 1.0.15-1
- Update to 1.0.15
- Drop libalpm from meson build opts due to https://github.com/sched-ext/scx/pull/2458
- Add config.toml to file list

* Tue Jul 08 2025 LionHeartP <LionHeartP@proton.me> - 1.0.14-1
- Update to 1.0.14

* Fri Jun 13 2025 LionHeartP <LionHeartP@proton.me> - 1.0.13-1
- Update to 1.0.13
- Add new runtime dependencies

* Sun May 11 2025 LionHeartP <LionHeartP@proton.me> - 1.0.12-1
- Update to 1.0.12
- Add new runtime dependencies
