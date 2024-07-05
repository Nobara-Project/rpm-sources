# With Fedora, nothing is bundled. For everything else, bundling is used.
# Amazon-linux 2023 is based on fedora but it is bundled
# To use bundled stuff, use "--with vendorized" on rpmbuild
%bcond_with vendorized

# A switch to allow building the package with support for testkeys which
# are used for the spread test suite of snapd.
%bcond_with testkeys

# takes an absolute path with slashes and turns it into an AppArmor profile path
%define as_apparmor_path() %(echo "%1" | tr / . | cut -c2-)

%global with_devel 1
%global with_debug 1
%global with_check 0
%global with_unit_test 0
%global with_test_keys 0
%global with_snap_symlink 1

# For the moment, we don't support all golang arches...
%global with_goarches 0

# Set if multilib is enabled for supported arches
%ifarch x86_64 aarch64 %{power64} s390x
%global with_multilib 1
%endif

# Set if valgrind is to be run
%ifnarch ppc64le
%global with_valgrind 1
%endif

%if ! %{with vendorized}
%global with_bundled 0
%else
%global with_bundled 1
%endif

%if ! %{with testkeys}
%global with_test_keys 0
%else
%global with_test_keys 1
%endif

%if 0%{?with_debug}
%global _dwz_low_mem_die_limit 0
%else
%global debug_package   %{nil}
%endif

%global provider        github
%global provider_tld    com
%global project         snapcore
%global repo            snapd
# https://github.com/snapcore/snapd
%global provider_prefix %{provider}.%{provider_tld}/%{project}/%{repo}
%global import_path     %{provider_prefix}

%global snappy_svcs      snapd.service snapd.socket snapd.autoimport.service snapd.seeded.service snapd.apparmor.service snapd.mounts.target snapd.mounts-pre.target
%global snappy_user_svcs snapd.session-agent.service snapd.session-agent.socket

# Until we have a way to add more extldflags to gobuild macro...
# Always use external linking when building static binaries.
%define gobuild_static(o:) go build -buildmode pie -compiler gc -tags="rpm_crashtraceback ${BUILDTAGS:-}" -ldflags "-B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \\n') -linkmode external -extldflags '%__global_ldflags -static'" -a -v -x %{?**};
%if 0%{?rhel} == 7
# no pass PIE flags due to https://bugzilla.redhat.com/show_bug.cgi?id=1634486
%define gobuild_static(o:) go build -compiler gc -tags="rpm_crashtraceback ${BUILDTAGS:-}" -ldflags "-B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \\n') -linkmode external -extldflags '%__global_ldflags -static'" -a -v -x %{?**};
%endif

# These macros are missing BUILDTAGS in RHEL 8/9, see RHBZ#1825138
%if 0%{?rhel} >= 8 || 0%{?amzn2023}
%define gobuild(o:) go build -buildmode pie -compiler gc -tags="rpm_crashtraceback ${BUILDTAGS:-}" -ldflags "-B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \\n') -linkmode external -extldflags '%__global_ldflags'" -a -v -x %{?**};
%endif

# These macros are not defined in RHEL 7
%if 0%{?rhel} == 7
%define gobuild(o:) go build -compiler gc -tags="rpm_crashtraceback ${BUILDTAGS:-}" -ldflags "-B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \\n') -linkmode external -extldflags '%__global_ldflags'" -a -v -x %{?**};
%define gotest() go test -compiler gc %{?**};
%endif

# Compat path macros
%{!?_environmentdir: %global _environmentdir %{_prefix}/lib/environment.d}
%{!?_systemdgeneratordir: %global _systemdgeneratordir %{_prefix}/lib/systemd/system-generators}
%{!?_systemd_system_env_generator_dir: %global _systemd_system_env_generator_dir %{_prefix}/lib/systemd/system-environment-generators}
%{!?_tmpfilesdir: %global _tmpfilesdir %{_prefix}/lib/tmpfiles.d}

# path to snap-confine encoded as AppArmor profile
%define apparmor_snapconfine_profile %as_apparmor_path %{_libexecdir}/snapd/snap-confine

Name:           snapd
Version:        2.63
Release:        1%{?dist}
Summary:        A transactional software package manager
License:        GPLv3
URL:            https://%{provider_prefix}
Source0:        https://%{provider_prefix}/releases/download/%{version}/%{name}_%{version}.no-vendor.tar.xz
Source1:        https://%{provider_prefix}/releases/download/%{version}/%{name}_%{version}.only-vendor.tar.xz
Patch0:         trick_snapd_into_thinking_nobara_is_fedora.patch

%if 0%{?with_goarches}
# e.g. el6 has ppc64 arch without gcc-go, so EA tag is required
ExclusiveArch:  %{?go_arches:%{go_arches}}%{!?go_arches:%{ix86} x86_64 %{arm}}
%else
# Verified arches from snapd upstream
ExclusiveArch:  %{ix86} x86_64 %{arm} aarch64 ppc64le s390x
%endif

# If go_compiler is not set to 1, there is no virtual provide. Use golang instead.
BuildRequires: make
BuildRequires:  %{?go_compiler:compiler(go-compiler)}%{!?go_compiler:golang >= 1.9}
BuildRequires:  systemd
%{?systemd_requires}
Requires:       snap-confine%{?_isa} = %{version}-%{release}
Requires:       squashfs-tools

BuildRequires:  apparmor-devel
BuildRequires:  apparmor-rpm-macros
BuildRequires:  apparmor-parser
Requires:       apparmor-parser
Requires:       apparmor-profiles

%if 0%{?rhel} && 0%{?rhel} < 8
# Rich dependencies not available, always pull in squashfuse
# snapd will use squashfs.ko instead of squashfuse if it's on the system
# NOTE: Amazon Linux 2 does not have squashfuse, squashfs.ko is part of the kernel package
%if ! 0%{?amzn2}
Requires:       squashfuse
Requires:       fuse
%endif
%else
# snapd will use squashfuse in the event that squashfs.ko isn't available (cloud instances, containers, etc.)
Requires:       ((squashfuse and fuse) or kmod(squashfs.ko))
%endif

# Require xdelta for delta updates of snap packages.
Requires:       xdelta

# bash-completion owns /usr/share/bash-completion/completions
Requires:       bash-completion

%if 0%{?fedora} && 0%{?fedora} < 30
# snapd-login-service is no more
# Note: Remove when F29 is EOL
Obsoletes:      %{name}-login-service < 1.33
Provides:       %{name}-login-service = 1.33
Provides:       %{name}-login-service%{?_isa} = 1.33
%endif

%if ! 0%{?with_bundled}
BuildRequires: golang(go.etcd.io/bbolt)
BuildRequires: golang(github.com/coreos/go-systemd/activation)
BuildRequires: golang(github.com/godbus/dbus)
BuildRequires: golang(github.com/godbus/dbus/introspect)
BuildRequires: golang(github.com/gorilla/mux)
BuildRequires: golang(github.com/jessevdk/go-flags)
BuildRequires: golang(github.com/juju/ratelimit)
BuildRequires: golang(github.com/kr/pretty)
BuildRequires: golang(github.com/kr/text)
BuildRequires: golang(github.com/mvo5/goconfigparser)
BuildRequires: golang(github.com/seccomp/libseccomp-golang)
BuildRequires: golang(github.com/snapcore/go-gettext)
BuildRequires: golang(golang.org/x/crypto/openpgp/armor)
BuildRequires: golang(golang.org/x/crypto/openpgp/packet)
BuildRequires: golang(golang.org/x/crypto/sha3)
BuildRequires: golang(golang.org/x/crypto/ssh/terminal)
BuildRequires: golang(golang.org/x/xerrors)
BuildRequires: golang(golang.org/x/xerrors/internal)
BuildRequires: golang(gopkg.in/check.v1)
BuildRequires: golang(gopkg.in/macaroon.v1)
BuildRequires: golang(gopkg.in/mgo.v2/bson)
BuildRequires: golang(gopkg.in/retry.v1)
BuildRequires: golang(gopkg.in/tomb.v2)
BuildRequires: golang(gopkg.in/yaml.v2)
BuildRequires: golang(gopkg.in/yaml.v3)
%endif

%description
Snappy is a modern, cross-distribution, transactional package manager
designed for working with self-contained, immutable packages.

%package -n snap-confine
Summary:        Confinement system for snap applications
License:        GPLv3
BuildRequires:  autoconf
BuildRequires:  autoconf-archive
BuildRequires:  automake
BuildRequires:  make
BuildRequires:  libtool
BuildRequires:  gcc
BuildRequires:  gettext
BuildRequires:  gnupg
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(libcap)
BuildRequires:  pkgconfig(libseccomp)
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(systemd)
BuildRequires:  pkgconfig(udev)
BuildRequires:  xfsprogs-devel
BuildRequires:  glibc-static
%if ! 0%{?rhel}
BuildRequires:  libseccomp-static
%endif
%if 0%{?with_valgrind}
BuildRequires:  valgrind
%endif
BuildRequires:  %{_bindir}/rst2man
BuildRequires:  %{_bindir}/shellcheck

# Ensures older version from split packaging is replaced
Obsoletes:      snap-confine < 2.19

%description -n snap-confine
This package is used internally by snapd to apply confinement to
the started snap applications.

%if 0%{?with_devel}
%package devel
Summary:       Development files for %{name}
BuildArch:     noarch

%if 0%{?with_check} && ! 0%{?with_bundled}
%endif

%if ! 0%{?with_bundled}
Requires:      golang(go.etcd.io/bbolt)
Requires:      golang(github.com/coreos/go-systemd/activation)
Requires:      golang(github.com/godbus/dbus)
Requires:      golang(github.com/godbus/dbus/introspect)
Requires:      golang(github.com/gorilla/mux)
Requires:      golang(github.com/jessevdk/go-flags)
Requires:      golang(github.com/juju/ratelimit)
Requires:      golang(github.com/kr/pretty)
Requires:      golang(github.com/kr/text)
Requires:      golang(github.com/mvo5/goconfigparser)
Requires:      golang(github.com/seccomp/libseccomp-golang)
Requires:      golang(github.com/snapcore/go-gettext)
Requires:      golang(golang.org/x/crypto/openpgp/armor)
Requires:      golang(golang.org/x/crypto/openpgp/packet)
Requires:      golang(golang.org/x/crypto/sha3)
Requires:      golang(golang.org/x/crypto/ssh/terminal)
Requires:      golang(golang.org/x/xerrors)
Requires:      golang(golang.org/x/xerrors/internal)
Requires:      golang(gopkg.in/check.v1)
Requires:      golang(gopkg.in/macaroon.v1)
Requires:      golang(gopkg.in/mgo.v2/bson)
Requires:      golang(gopkg.in/retry.v1)
Requires:      golang(gopkg.in/tomb.v2)
Requires:      golang(gopkg.in/yaml.v2)
Requires:      golang(gopkg.in/yaml.v3)
%else
# These Provides are unversioned because the sources in
# the bundled tarball are unversioned (they go by git commit)
# *sigh*... I hate golang...
Provides:      bundled(golang(go.etcd.io/bbolt))
Provides:      bundled(golang(github.com/coreos/go-systemd/activation))
Provides:      bundled(golang(github.com/godbus/dbus))
Provides:      bundled(golang(github.com/godbus/dbus/introspect))
Provides:      bundled(golang(github.com/gorilla/mux))
Provides:      bundled(golang(github.com/jessevdk/go-flags))
Provides:      bundled(golang(github.com/juju/ratelimit))
Provides:      bundled(golang(github.com/kr/pretty))
Provides:      bundled(golang(github.com/kr/text))
Provides:      bundled(golang(github.com/mvo5/goconfigparser))
Provides:      bundled(golang(github.com/seccomp/libseccomp-golang))
Provides:      bundled(golang(github.com/snapcore/go-gettext))
Provides:      bundled(golang(golang.org/x/crypto/openpgp/armor))
Provides:      bundled(golang(golang.org/x/crypto/openpgp/packet))
Provides:      bundled(golang(golang.org/x/crypto/sha3))
Provides:      bundled(golang(golang.org/x/crypto/ssh/terminal))
Provides:      bundled(golang(golang.org/x/xerrors))
Provides:      bundled(golang(golang.org/x/xerrors/internal))
Provides:      bundled(golang(gopkg.in/check.v1))
Provides:      bundled(golang(gopkg.in/macaroon.v1))
Provides:      bundled(golang(gopkg.in/mgo.v2/bson))
Provides:      bundled(golang(gopkg.in/retry.v1))
Provides:      bundled(golang(gopkg.in/tomb.v2))
Provides:      bundled(golang(gopkg.in/yaml.v2))
Provides:      bundled(golang(gopkg.in/yaml.v3))
%endif

# Generated by gofed
Provides:      golang(%{import_path}/advisor) = %{version}-%{release}
Provides:      golang(%{import_path}/arch) = %{version}-%{release}
Provides:      golang(%{import_path}/asserts) = %{version}-%{release}
Provides:      golang(%{import_path}/asserts/assertstest) = %{version}-%{release}
Provides:      golang(%{import_path}/asserts/internal) = %{version}-%{release}
Provides:      golang(%{import_path}/asserts/signtool) = %{version}-%{release}
Provides:      golang(%{import_path}/asserts/snapasserts) = %{version}-%{release}
Provides:      golang(%{import_path}/asserts/sysdb) = %{version}-%{release}
Provides:      golang(%{import_path}/asserts/systestkeys) = %{version}-%{release}
Provides:      golang(%{import_path}/boot) = %{version}-%{release}
Provides:      golang(%{import_path}/boot/boottest) = %{version}-%{release}
Provides:      golang(%{import_path}/bootloader) = %{version}-%{release}
Provides:      golang(%{import_path}/bootloader/androidbootenv) = %{version}-%{release}
Provides:      golang(%{import_path}/bootloader/assets) = %{version}-%{release}
Provides:      golang(%{import_path}/bootloader/assets/genasset) = %{version}-%{release}
Provides:      golang(%{import_path}/bootloader/bootloadertest) = %{version}-%{release}
Provides:      golang(%{import_path}/bootloader/efi) = %{version}-%{release}
Provides:      golang(%{import_path}/bootloader/grubenv) = %{version}-%{release}
Provides:      golang(%{import_path}/bootloader/lkenv) = %{version}-%{release}
Provides:      golang(%{import_path}/bootloader/ubootenv) = %{version}-%{release}
Provides:      golang(%{import_path}/client) = %{version}-%{release}
Provides:      golang(%{import_path}/client/clientutil) = %{version}-%{release}
Provides:      golang(%{import_path}/cmd/snap) = %{version}-%{release}
Provides:      golang(%{import_path}/cmd/snap-bootstrap) = %{version}-%{release}
Provides:      golang(%{import_path}/cmd/snap-bootstrap/triggerwatch) = %{version}-%{release}
Provides:      golang(%{import_path}/cmd/snap-exec) = %{version}-%{release}
Provides:      golang(%{import_path}/cmd/snap-failure) = %{version}-%{release}
Provides:      golang(%{import_path}/cmd/snap-preseed) = %{version}-%{release}
Provides:      golang(%{import_path}/cmd/snap-recovery-chooser) = %{version}-%{release}
Provides:      golang(%{import_path}/cmd/snap-repair) = %{version}-%{release}
Provides:      golang(%{import_path}/cmd/snap-seccomp) = %{version}-%{release}
Provides:      golang(%{import_path}/cmd/snap-seccomp/syscalls) = %{version}-%{release}
Provides:      golang(%{import_path}/cmd/snap-update-ns) = %{version}-%{release}
Provides:      golang(%{import_path}/cmd/snapctl) = %{version}-%{release}
Provides:      golang(%{import_path}/cmd/snapd) = %{version}-%{release}
Provides:      golang(%{import_path}/cmd/snaplock) = %{version}-%{release}
Provides:      golang(%{import_path}/cmd/snaplock/runinhibit) = %{version}-%{release}
Provides:      golang(%{import_path}/daemon) = %{version}-%{release}
Provides:      golang(%{import_path}/dbusutil) = %{version}-%{release}
Provides:      golang(%{import_path}/dbusutil/dbustest) = %{version}-%{release}
Provides:      golang(%{import_path}/desktop/notification) = %{version}-%{release}
Provides:      golang(%{import_path}/desktop/notification/notificationtest) = %{version}-%{release}
Provides:      golang(%{import_path}/dirs) = %{version}-%{release}
Provides:      golang(%{import_path}/docs) = %{version}-%{release}
Provides:      golang(%{import_path}/features) = %{version}-%{release}
Provides:      golang(%{import_path}/gadget) = %{version}-%{release}
Provides:      golang(%{import_path}/gadget/edition) = %{version}-%{release}
Provides:      golang(%{import_path}/gadget/install) = %{version}-%{release}
Provides:      golang(%{import_path}/gadget/internal) = %{version}-%{release}
Provides:      golang(%{import_path}/gadget/quantity) = %{version}-%{release}
Provides:      golang(%{import_path}/httputil) = %{version}-%{release}
Provides:      golang(%{import_path}/i18n) = %{version}-%{release}
Provides:      golang(%{import_path}/i18n/xgettext-go) = %{version}-%{release}
Provides:      golang(%{import_path}/image) = %{version}-%{release}
Provides:      golang(%{import_path}/interfaces) = %{version}-%{release}
Provides:      golang(%{import_path}/interfaces/apparmor) = %{version}-%{release}
Provides:      golang(%{import_path}/interfaces/backends) = %{version}-%{release}
Provides:      golang(%{import_path}/interfaces/builtin) = %{version}-%{release}
Provides:      golang(%{import_path}/interfaces/dbus) = %{version}-%{release}
Provides:      golang(%{import_path}/interfaces/hotplug) = %{version}-%{release}
Provides:      golang(%{import_path}/interfaces/ifacetest) = %{version}-%{release}
Provides:      golang(%{import_path}/interfaces/kmod) = %{version}-%{release}
Provides:      golang(%{import_path}/interfaces/mount) = %{version}-%{release}
Provides:      golang(%{import_path}/interfaces/policy) = %{version}-%{release}
Provides:      golang(%{import_path}/interfaces/seccomp) = %{version}-%{release}
Provides:      golang(%{import_path}/interfaces/systemd) = %{version}-%{release}
Provides:      golang(%{import_path}/interfaces/udev) = %{version}-%{release}
Provides:      golang(%{import_path}/interfaces/utils) = %{version}-%{release}
Provides:      golang(%{import_path}/jsonutil) = %{version}-%{release}
Provides:      golang(%{import_path}/jsonutil/safejson) = %{version}-%{release}
Provides:      golang(%{import_path}/kernel) = %{version}-%{release}
Provides:      golang(%{import_path}/logger) = %{version}-%{release}
Provides:      golang(%{import_path}/metautil) = %{version}-%{release}
Provides:      golang(%{import_path}/netutil) = %{version}-%{release}
Provides:      golang(%{import_path}/osutil) = %{version}-%{release}
Provides:      golang(%{import_path}/osutil/disks) = %{version}-%{release}
Provides:      golang(%{import_path}/osutil/mount) = %{version}-%{release}
Provides:      golang(%{import_path}/osutil/squashfs) = %{version}-%{release}
Provides:      golang(%{import_path}/osutil/strace) = %{version}-%{release}
Provides:      golang(%{import_path}/osutil/sys) = %{version}-%{release}
Provides:      golang(%{import_path}/osutil/udev/crawler) = %{version}-%{release}
Provides:      golang(%{import_path}/osutil/udev/netlink) = %{version}-%{release}
Provides:      golang(%{import_path}/overlord) = %{version}-%{release}
Provides:      golang(%{import_path}/overlord/assertstate) = %{version}-%{release}
Provides:      golang(%{import_path}/overlord/assertstate/assertstatetest) = %{version}-%{release}
Provides:      golang(%{import_path}/overlord/auth) = %{version}-%{release}
Provides:      golang(%{import_path}/overlord/cmdstate) = %{version}-%{release}
Provides:      golang(%{import_path}/overlord/configstate) = %{version}-%{release}
Provides:      golang(%{import_path}/overlord/configstate/config) = %{version}-%{release}
Provides:      golang(%{import_path}/overlord/configstate/configcore) = %{version}-%{release}
Provides:      golang(%{import_path}/overlord/configstate/proxyconf) = %{version}-%{release}
Provides:      golang(%{import_path}/overlord/configstate/settings) = %{version}-%{release}
Provides:      golang(%{import_path}/overlord/devicestate) = %{version}-%{release}
Provides:      golang(%{import_path}/overlord/devicestate/devicestatetest) = %{version}-%{release}
Provides:      golang(%{import_path}/overlord/devicestate/fde) = %{version}-%{release}
Provides:      golang(%{import_path}/overlord/devicestate/internal) = %{version}-%{release}
Provides:      golang(%{import_path}/overlord/healthstate) = %{version}-%{release}
Provides:      golang(%{import_path}/overlord/hookstate) = %{version}-%{release}
Provides:      golang(%{import_path}/overlord/hookstate/ctlcmd) = %{version}-%{release}
Provides:      golang(%{import_path}/overlord/hookstate/hooktest) = %{version}-%{release}
Provides:      golang(%{import_path}/overlord/ifacestate) = %{version}-%{release}
Provides:      golang(%{import_path}/overlord/ifacestate/ifacerepo) = %{version}-%{release}
Provides:      golang(%{import_path}/overlord/ifacestate/udevmonitor) = %{version}-%{release}
Provides:      golang(%{import_path}/overlord/patch) = %{version}-%{release}
Provides:      golang(%{import_path}/overlord/servicestate) = %{version}-%{release}
Provides:      golang(%{import_path}/overlord/snapshotstate) = %{version}-%{release}
Provides:      golang(%{import_path}/overlord/snapshotstate/backend) = %{version}-%{release}
Provides:      golang(%{import_path}/overlord/snapstate) = %{version}-%{release}
Provides:      golang(%{import_path}/overlord/snapstate/backend) = %{version}-%{release}
Provides:      golang(%{import_path}/overlord/snapstate/policy) = %{version}-%{release}
Provides:      golang(%{import_path}/overlord/snapstate/snapstatetest) = %{version}-%{release}
Provides:      golang(%{import_path}/overlord/standby) = %{version}-%{release}
Provides:      golang(%{import_path}/overlord/state) = %{version}-%{release}
Provides:      golang(%{import_path}/overlord/storecontext) = %{version}-%{release}
Provides:      golang(%{import_path}/polkit) = %{version}-%{release}
Provides:      golang(%{import_path}/progress) = %{version}-%{release}
Provides:      golang(%{import_path}/progress/progresstest) = %{version}-%{release}
Provides:      golang(%{import_path}/randutil) = %{version}-%{release}
Provides:      golang(%{import_path}/release) = %{version}-%{release}
Provides:      golang(%{import_path}/sandbox) = %{version}-%{release}
Provides:      golang(%{import_path}/sandbox/apparmor) = %{version}-%{release}
Provides:      golang(%{import_path}/sandbox/cgroup) = %{version}-%{release}
Provides:      golang(%{import_path}/sandbox/seccomp) = %{version}-%{release}
Provides:      golang(%{import_path}/sandbox/selinux) = %{version}-%{release}
Provides:      golang(%{import_path}/sanity) = %{version}-%{release}
Provides:      golang(%{import_path}/secboot) = %{version}-%{release}
Provides:      golang(%{import_path}/seed) = %{version}-%{release}
Provides:      golang(%{import_path}/seed/internal) = %{version}-%{release}
Provides:      golang(%{import_path}/seed/seedtest) = %{version}-%{release}
Provides:      golang(%{import_path}/seed/seedwriter) = %{version}-%{release}
Provides:      golang(%{import_path}/snap) = %{version}-%{release}
Provides:      golang(%{import_path}/snap/channel) = %{version}-%{release}
Provides:      golang(%{import_path}/snap/internal) = %{version}-%{release}
Provides:      golang(%{import_path}/snap/naming) = %{version}-%{release}
Provides:      golang(%{import_path}/snap/pack) = %{version}-%{release}
Provides:      golang(%{import_path}/snap/snapdir) = %{version}-%{release}
Provides:      golang(%{import_path}/snap/snapenv) = %{version}-%{release}
Provides:      golang(%{import_path}/snap/snapfile) = %{version}-%{release}
Provides:      golang(%{import_path}/snap/snaptest) = %{version}-%{release}
Provides:      golang(%{import_path}/snap/squashfs) = %{version}-%{release}
Provides:      golang(%{import_path}/snapdenv) = %{version}-%{release}
Provides:      golang(%{import_path}/snapdtool) = %{version}-%{release}
Provides:      golang(%{import_path}/spdx) = %{version}-%{release}
Provides:      golang(%{import_path}/store) = %{version}-%{release}
Provides:      golang(%{import_path}/store/storetest) = %{version}-%{release}
Provides:      golang(%{import_path}/strutil) = %{version}-%{release}
Provides:      golang(%{import_path}/strutil/chrorder) = %{version}-%{release}
Provides:      golang(%{import_path}/strutil/quantity) = %{version}-%{release}
Provides:      golang(%{import_path}/strutil/shlex) = %{version}-%{release}
Provides:      golang(%{import_path}/sysconfig) = %{version}-%{release}
Provides:      golang(%{import_path}/systemd) = %{version}-%{release}
Provides:      golang(%{import_path}/testutil) = %{version}-%{release}
Provides:      golang(%{import_path}/timeout) = %{version}-%{release}
Provides:      golang(%{import_path}/timeutil) = %{version}-%{release}
Provides:      golang(%{import_path}/timings) = %{version}-%{release}
Provides:      golang(%{import_path}/usersession/agent) = %{version}-%{release}
Provides:      golang(%{import_path}/usersession/autostart) = %{version}-%{release}
Provides:      golang(%{import_path}/usersession/client) = %{version}-%{release}
Provides:      golang(%{import_path}/usersession/userd) = %{version}-%{release}
Provides:      golang(%{import_path}/usersession/userd/ui) = %{version}-%{release}
Provides:      golang(%{import_path}/usersession/xdgopenproxy) = %{version}-%{release}
Provides:      golang(%{import_path}/wrappers) = %{version}-%{release}
Provides:      golang(%{import_path}/x11) = %{version}-%{release}

%description devel
This package contains library source intended for
building other packages which use import path with
%{import_path} prefix.
%endif

%if 0%{?with_unit_test} && 0%{?with_devel}
%package unit-test-devel
Summary:         Unit tests for %{name} package

%if 0%{?with_check}
#Here comes all BuildRequires: PACKAGE the unit tests
#in %%check section need for running
%endif

# test subpackage tests code from devel subpackage
Requires:        %{name}-devel = %{version}-%{release}

%description unit-test-devel
This package contains unit tests for project
providing packages with %{import_path} prefix.
%endif

%prep
%if ! 0%{?with_bundled}
%setup -q
# Ensure there's no bundled stuff accidentally leaking in...
rm -rf vendor/*
%else
# Extract each tarball properly
%setup -q -D -b 1
%endif
# Apply patches
%autopatch -p1

# Build snapd
mkdir -p src/github.com/snapcore
ln -s ../../../ src/github.com/snapcore/snapd

%if ! 0%{?with_bundled}
export GOPATH=$(pwd):%{gopath}
# FIXME: move spec file really to a go.mod world instead of this hack
rm -f go.mod
export GO111MODULE=off
#%else
#export GOPATH=$(pwd):$(pwd)/Godeps/_workspace:%{gopath}
%endif

# Generate version files
./mkversion.sh "%{version}-%{release}"

# see https://github.com/gofed/go-macros/blob/master/rpm/macros.d/macros.go-compilers-golang
BUILDTAGS=
%if 0%{?with_test_keys}
BUILDTAGS="withtestkeys nosecboot"
%else
BUILDTAGS="nosecboot"
%endif

%if ! 0%{?with_bundled}
# We don't need the snapcore fork for bolt - it is just a fix on ppc
sed -e "s:github.com/snapcore/bolt:github.com/boltdb/bolt:g" -i advisor/*.go
%endif

# We have to build snapd first to prevent the build from
# building various things from the tree without additional
# set tags.
%gobuild -o bin/snapd $GOFLAGS %{import_path}/cmd/snapd
BUILDTAGS="${BUILDTAGS} nomanagers"
%gobuild -o bin/snap $GOFLAGS %{import_path}/cmd/snap
%gobuild -o bin/snap-failure $GOFLAGS %{import_path}/cmd/snap-failure

# To ensure things work correctly with base snaps,
# snap-exec, snap-update-ns, and snapctl need to be built statically
(
%if 0%{?rhel} >= 7
    # since RH Developer tools 2018.4 (and later releases),
    # the go-toolset module is built with FIPS compliance that
    # defaults to using libcrypto.so which gets loaded at runtime via dlopen(),
    # disable that functionality for statically built binaries
    BUILDTAGS="${BUILDTAGS} no_openssl"
%endif
    %gobuild_static -o bin/snap-exec $GOFLAGS %{import_path}/cmd/snap-exec
    %gobuild_static -o bin/snap-update-ns $GOFLAGS %{import_path}/cmd/snap-update-ns
    %gobuild_static -o bin/snapctl $GOFLAGS %{import_path}/cmd/snapctl
    %gobuild_static -o bin/snapd-apparmor $GOFLAGS %{import_path}/cmd/snapd-apparmor
)

%if 0%{?rhel}
# There's no static link library for libseccomp in RHEL/CentOS...
sed -e "s/-Bstatic -lseccomp/-Bstatic/g" -i cmd/snap-seccomp/*.go
%endif
%gobuild -o bin/snap-seccomp $GOFLAGS %{import_path}/cmd/snap-seccomp

# Build snap-confine
pushd ./cmd
autoreconf --force --install --verbose
# FIXME: add --enable-caps-over-setuid as soon as possible (setuid discouraged!)
HAVE_SELINUX=0 %configure \
    --enable-apparmor \
    --libexecdir=%{_libexecdir}/snapd/ \
    --enable-nvidia-biarch \
    %{?with_multilib:--with-32bit-libdir=%{_prefix}/lib} \
    --with-snap-mount-dir=%{_sharedstatedir}/snapd/snap \
    --enable-merged-usr

%make_build %{!?with_valgrind:HAVE_VALGRIND=}
popd

# Build systemd units, dbus services, and env files
pushd ./data
make BINDIR="%{_bindir}" LIBEXECDIR="%{_libexecdir}" DATADIR="%{_datadir}" \
     SYSTEMDSYSTEMUNITDIR="%{_unitdir}" \
     SNAP_MOUNT_DIR="%{_sharedstatedir}/snapd/snap" \
     SNAPD_ENVIRONMENT_FILE="%{_sysconfdir}/sysconfig/snapd" \
     SNAPD_DEFINES_DIR=%{_builddir}
popd

%install
install -d -p %{buildroot}%{_bindir}
install -d -p %{buildroot}%{_libexecdir}/snapd
install -d -p %{buildroot}%{_mandir}/man8
install -d -p %{buildroot}%{_environmentdir}
install -d -p %{buildroot}%{_systemdgeneratordir}
install -d -p %{buildroot}%{_systemd_system_env_generator_dir}
install -d -p %{buildroot}%{_tmpfilesdir}
install -d -p %{buildroot}%{_unitdir}
install -d -p %{buildroot}%{_userunitdir}
install -d -p %{buildroot}%{_sysconfdir}/profile.d
install -d -p %{buildroot}%{_sysconfdir}/sysconfig
install -d -p %{buildroot}%{_sharedstatedir}/snapd/assertions
install -d -p %{buildroot}%{_sharedstatedir}/snapd/cookie
install -d -p %{buildroot}%{_sharedstatedir}/snapd/cgroup
install -d -p %{buildroot}%{_sharedstatedir}/snapd/dbus-1/services
install -d -p %{buildroot}%{_sharedstatedir}/snapd/dbus-1/system-services
install -d -p %{buildroot}%{_sharedstatedir}/snapd/desktop/applications
install -d -p %{buildroot}%{_sharedstatedir}/snapd/device
install -d -p %{buildroot}%{_sharedstatedir}/snapd/hostfs
install -d -p %{buildroot}%{_sharedstatedir}/snapd/inhibit
install -d -p %{buildroot}%{_sharedstatedir}/snapd/lib/gl
install -d -p %{buildroot}%{_sharedstatedir}/snapd/lib/gl32
install -d -p %{buildroot}%{_sharedstatedir}/snapd/lib/glvnd
install -d -p %{buildroot}%{_sharedstatedir}/snapd/lib/vulkan
install -d -p %{buildroot}%{_sharedstatedir}/snapd/mount
install -d -p %{buildroot}%{_sharedstatedir}/snapd/seccomp/bpf
install -d -p %{buildroot}%{_sharedstatedir}/snapd/snaps
install -d -p %{buildroot}%{_sharedstatedir}/snapd/snap/bin
install -d -p %{buildroot}%{_localstatedir}/snap
install -d -p %{buildroot}%{_localstatedir}/cache/snapd
install -d -p %{buildroot}%{_datadir}/polkit-1/actions

# Install snap and snapd
install -p -m 0755 bin/snap %{buildroot}%{_bindir}
install -p -m 0755 bin/snap-exec %{buildroot}%{_libexecdir}/snapd
install -p -m 0755 bin/snap-failure %{buildroot}%{_libexecdir}/snapd
install -p -m 0755 bin/snapd %{buildroot}%{_libexecdir}/snapd
install -p -m 0755 bin/snap-update-ns %{buildroot}%{_libexecdir}/snapd
install -p -m 0755 bin/snap-seccomp %{buildroot}%{_libexecdir}/snapd
install -p -m 0755 bin/snapd-apparmor %{buildroot}%{_libexecdir}/snapd
# Ensure /usr/bin/snapctl is a symlink to /usr/libexec/snapd/snapctl
install -p -m 0755 bin/snapctl %{buildroot}%{_libexecdir}/snapd/snapctl
ln -sf %{_libexecdir}/snapd/snapctl %{buildroot}%{_bindir}/snapctl

# Install snap(8) man page
bin/snap help --man > %{buildroot}%{_mandir}/man8/snap.8

# Install the "info" data file with snapd version
install -m 644 -D data/info %{buildroot}%{_libexecdir}/snapd/info

# Install bash completion for "snap"
install -m 644 -D data/completion/bash/snap %{buildroot}%{_datadir}/bash-completion/completions/snap
install -m 644 -D data/completion/bash/complete.sh %{buildroot}%{_libexecdir}/snapd
install -m 644 -D data/completion/bash/etelpmoc.sh %{buildroot}%{_libexecdir}/snapd
# Install zsh completion for "snap"
install -d -p %{buildroot}%{_datadir}/zsh/site-functions
install -m 644 -D data/completion/zsh/_snap %{buildroot}%{_datadir}/zsh/site-functions/_snap

# Install snap-confine
pushd ./cmd
%make_install
# Fixup snap-confine apparmor profile:
sed -i '/\/{,usr\/}lib{,32,64,x32}\/{,@{multiarch}\/}libgcc_s.so\* mr,/a \    /{,usr\/}lib{,32,64,x32}\/{,@{multiarch}\/}libgcc_s*.so\* mr,' %{buildroot}%{_sysconfdir}/apparmor.d/usr.libexec.snapd.snap-confine

# Undo the 0111 permissions, they are restored in the files section
chmod 0755 %{buildroot}%{_sharedstatedir}/snapd/void
# ubuntu-core-launcher is dead
rm -fv %{buildroot}%{_bindir}/ubuntu-core-launcher
popd

# Install all systemd and dbus units, and env files
pushd ./data
%make_install BINDIR="%{_bindir}" LIBEXECDIR="%{_libexecdir}" DATADIR="%{_datadir}" \
              SYSTEMDSYSTEMUNITDIR="%{_unitdir}" SYSTEMDUSERUNITDIR="%{_userunitdir}" \
              TMPFILESDIR="%{_tmpfilesdir}" \
              SNAP_MOUNT_DIR="%{_sharedstatedir}/snapd/snap" \
              SNAPD_ENVIRONMENT_FILE="%{_sysconfdir}/sysconfig/snapd"
popd

%if 0%{?rhel} == 7
# Install kernel tweaks
# See: https://access.redhat.com/articles/3128691
install -m 644 -D data/sysctl/rhel7-snap.conf %{buildroot}%{_sysctldir}/99-snap.conf
%endif

# Remove snappy core specific units
rm -fv %{buildroot}%{_unitdir}/snapd.system-shutdown.service
rm -fv %{buildroot}%{_unitdir}/snapd.snap-repair.*
rm -fv %{buildroot}%{_unitdir}/snapd.core-fixup.*
rm -fv %{buildroot}%{_unitdir}/snapd.recovery-chooser-trigger.service

# Remove snappy core specific scripts and binaries
rm %{buildroot}%{_libexecdir}/snapd/snapd.core-fixup.sh
rm %{buildroot}%{_libexecdir}/snapd/system-shutdown

# Install Polkit configuration
install -m 644 -D data/polkit/io.snapcraft.snapd.policy %{buildroot}%{_datadir}/polkit-1/actions

# Disable re-exec by default
echo 'SNAP_REEXEC=0' > %{buildroot}%{_sysconfdir}/sysconfig/snapd

# Create state.json and the README file to be ghosted
touch %{buildroot}%{_sharedstatedir}/snapd/state.json
touch %{buildroot}%{_sharedstatedir}/snapd/snap/README

# When enabled, create a symlink for /snap to point to /var/lib/snapd/snap
%if 0%{?with_snap_symlink}
ln -sr %{buildroot}%{_sharedstatedir}/snapd/snap %{buildroot}/snap
%endif

# source codes for building projects
%if 0%{?with_devel}
install -d -p %{buildroot}/%{gopath}/src/%{import_path}/
echo "%%dir %%{gopath}/src/%%{import_path}/." >> devel.file-list
# find all *.go but no *_test.go files and generate devel.file-list
for file in $(find . -iname "*.go" -o -iname "*.s" \! -iname "*_test.go") ; do
    echo "%%dir %%{gopath}/src/%%{import_path}/$(dirname $file)" >> devel.file-list
    install -d -p %{buildroot}/%{gopath}/src/%{import_path}/$(dirname $file)
    cp -pav $file %{buildroot}/%{gopath}/src/%{import_path}/$file
    echo "%%{gopath}/src/%%{import_path}/$file" >> devel.file-list
done
%endif

# testing files for this project
%if 0%{?with_unit_test} && 0%{?with_devel}
install -d -p %{buildroot}/%{gopath}/src/%{import_path}/
# find all *_test.go files and generate unit-test.file-list
for file in $(find . -iname "*_test.go"); do
    echo "%%dir %%{gopath}/src/%%{import_path}/$(dirname $file)" >> devel.file-list
    install -d -p %{buildroot}/%{gopath}/src/%{import_path}/$(dirname $file)
    cp -pav $file %{buildroot}/%{gopath}/src/%{import_path}/$file
    echo "%%{gopath}/src/%%{import_path}/$file" >> unit-test-devel.file-list
done

# Install additional testdata
install -d %{buildroot}/%{gopath}/src/%{import_path}/cmd/snap/test-data/
cp -pav cmd/snap/test-data/* %{buildroot}/%{gopath}/src/%{import_path}/cmd/snap/test-data/
echo "%%{gopath}/src/%%{import_path}/cmd/snap/test-data" >> unit-test-devel.file-list
%endif

%if 0%{?with_devel}
sort -u -o devel.file-list devel.file-list
%endif

%check
for binary in snap-exec snap-update-ns snapctl; do
    ldd bin/$binary 2>&1 | grep 'not a dynamic executable'
done

# snapd tests
%if 0%{?with_check} && 0%{?with_unit_test} && 0%{?with_devel}
%if ! 0%{?with_bundled}
export GOPATH=%{buildroot}/%{gopath}:%{gopath}
%else
export GOPATH=%{buildroot}/%{gopath}:$(pwd)/Godeps/_workspace:%{gopath}
%endif
# FIXME: we are in the go.mod world now but without this things fall apart
export GO111MODULE=off
%gotest %{import_path}/...
%endif

# snap-confine tests (these always run!)
pushd ./cmd
make check
popd

%files
#define license tag if not already defined
%{!?_licensedir:%global license %doc}
%license COPYING
%doc README.md docs/*
%{_bindir}/snap
%{_bindir}/snapctl
%{_environmentdir}/990-snapd.conf
%if 0%{?rhel} == 7
%{_sysctldir}/99-snap.conf
%endif
%dir %{_libexecdir}/snapd
%{_libexecdir}/snapd/snapctl
%{_libexecdir}/snapd/snapd
%{_libexecdir}/snapd/snap-exec
%{_libexecdir}/snapd/snap-failure
%{_libexecdir}/snapd/info
%{_libexecdir}/snapd/snap-mgmt
%{_mandir}/man8/snap.8*
%{_datadir}/applications/snap-handle-link.desktop
%{_datadir}/bash-completion/completions/snap
%{_libexecdir}/snapd/complete.sh
%{_libexecdir}/snapd/etelpmoc.sh
%{_datadir}/zsh/site-functions/_snap
%{_libexecdir}/snapd/snapd.run-from-snap
%{_sysconfdir}/profile.d/snapd.sh
%{_mandir}/man8/snapd-env-generator.8*
%{_systemd_system_env_generator_dir}/snapd-env-generator
%{_unitdir}/snapd.socket
%{_unitdir}/snapd.service
%{_unitdir}/snapd.autoimport.service
%{_unitdir}/snapd.failure.service
%{_unitdir}/snapd.seeded.service
%{_unitdir}/snapd.mounts.target
%{_unitdir}/snapd.mounts-pre.target
%{_userunitdir}/snapd.session-agent.service
%{_userunitdir}/snapd.session-agent.socket
%{_tmpfilesdir}/snapd.conf
%{_datadir}/dbus-1/services/io.snapcraft.Launcher.service
%{_datadir}/dbus-1/services/io.snapcraft.SessionAgent.service
%{_datadir}/dbus-1/services/io.snapcraft.Settings.service
%{_datadir}/dbus-1/session.d/snapd.session-services.conf
%{_datadir}/dbus-1/system.d/snapd.system-services.conf
%{_datadir}/polkit-1/actions/io.snapcraft.snapd.policy
%{_datadir}/applications/io.snapcraft.SessionAgent.desktop
%{_datadir}/fish/vendor_conf.d/snapd.fish
%{_datadir}/snapd/snapcraft-logo-bird.svg
%{_sysconfdir}/xdg/autostart/snap-userd-autostart.desktop
%config(noreplace) %{_sysconfdir}/sysconfig/snapd
%dir %{_sharedstatedir}/snapd
%dir %{_sharedstatedir}/snapd/assertions
%dir %{_sharedstatedir}/snapd/cookie
%dir %{_sharedstatedir}/snapd/cgroup
%dir %{_sharedstatedir}/snapd/dbus-1
%dir %{_sharedstatedir}/snapd/dbus-1/services
%dir %{_sharedstatedir}/snapd/dbus-1/system-services
%dir %{_sharedstatedir}/snapd/desktop
%dir %{_sharedstatedir}/snapd/desktop/applications
%dir %{_sharedstatedir}/snapd/device
%dir %{_sharedstatedir}/snapd/hostfs
%dir %{_sharedstatedir}/snapd/inhibit
%dir %{_sharedstatedir}/snapd/lib
%dir %{_sharedstatedir}/snapd/lib/gl
%dir %{_sharedstatedir}/snapd/lib/gl32
%dir %{_sharedstatedir}/snapd/lib/glvnd
%dir %{_sharedstatedir}/snapd/lib/vulkan
%dir %{_sharedstatedir}/snapd/mount
%dir %{_sharedstatedir}/snapd/seccomp
%dir %{_sharedstatedir}/snapd/seccomp/bpf
%dir %{_sharedstatedir}/snapd/snaps
%dir %{_sharedstatedir}/snapd/snap
%ghost %dir %{_sharedstatedir}/snapd/snap/bin
%dir %{_localstatedir}/cache/snapd
%dir %{_localstatedir}/snap
%ghost %{_sharedstatedir}/snapd/state.json
%ghost %{_sharedstatedir}/snapd/snap/README
%if 0%{?with_snap_symlink}
/snap
%endif
# this is typically owned by zsh, but we do not want to explicitly require zsh
%dir %{_datadir}/zsh
%dir %{_datadir}/zsh/site-functions
# similar case for fish
%dir %{_datadir}/fish/vendor_conf.d

%files -n snap-confine
%doc cmd/snap-confine/PORTING
%license COPYING
%dir %{_libexecdir}/snapd
# For now, we can't use caps
# FIXME: Switch to "%%attr(0755,root,root) %%caps(cap_sys_admin=pe)" asap!
%attr(4755,root,root) %{_libexecdir}/snapd/snap-confine
%{_libexecdir}/snapd/snap-device-helper
%{_libexecdir}/snapd/snap-discard-ns
%{_libexecdir}/snapd/snap-gdb-shim
%{_libexecdir}/snapd/snap-gdbserver-shim
%{_libexecdir}/snapd/snap-seccomp
%{_libexecdir}/snapd/snap-update-ns
%{_mandir}/man8/snap-confine.8*
%{_mandir}/man8/snap-discard-ns.8*
%{_systemdgeneratordir}/snapd-generator
%attr(0111,root,root) %{_sharedstatedir}/snapd/void
%config %{_sysconfdir}/apparmor.d
%{_libexecdir}/snapd/snapd-apparmor
%{_sysconfdir}/apparmor.d/%{apparmor_snapconfine_profile}
%{_unitdir}/snapd.apparmor.service


%if 0%{?with_devel}
%files devel -f devel.file-list
%license COPYING
%doc README.md
%dir %{gopath}/src/%{provider}.%{provider_tld}/%{project}
%endif

%if 0%{?with_unit_test} && 0%{?with_devel}
%files unit-test-devel -f unit-test-devel.file-list
%license COPYING
%doc README.md
%endif

%post
%if 0%{?rhel} == 7
%sysctl_apply 99-snap.conf
%endif
%apparmor_reload /etc/apparmor.d/%{apparmor_snapconfine_profile}
%systemd_post %{snappy_svcs}
%systemd_user_post %{snappy_user_svcs}
if [ -x /usr/bin/systemctl ]; then
    if systemctl is-enabled snapd.service >/dev/null 2>&1 || systemctl is-enabled snapd.socket >/dev/null 2>&1; then
        # either the snapd.service or the snapd.socket are enabled, meaning snapd is
        # being actively used
        if ! systemctl is-enabled snapd.apparmor.service >/dev/null 2>&1; then
            # also apparmor appears to be enabled, but loading of apparmor profiles
            # of the snaps is not, so enable that now so that the snaps continue to
            # work after the update
            systemctl enable --now snapd.apparmor.service || :
        fi
    fi
fi


%preun
%systemd_preun %{snappy_svcs}
%systemd_user_preun %{snappy_user_svcs}

# Remove all Snappy content if snapd is being fully uninstalled
if [ $1 -eq 0 ]; then
   %{_libexecdir}/snapd/snap-mgmt --purge || :
fi

%postun
%systemd_postun_with_restart %{snappy_svcs}
%systemd_user_postun_with_restart %{snappy_user_svcs}

%posttrans
# install snap store if it does not exist
if [[ -n $(which snap) ]]; then
    if [[ -z $(snap list | grep snap-store) ]]; then
        sleep 5
        snap install snap-store
    fi
fi

%changelog
