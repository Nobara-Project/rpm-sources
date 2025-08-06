### A port of linux-cachyos (https://github.com/CachyOS/linux-cachyos/tree/master/linux-cachyos) for the Fedora operating system.
# https://github.com/CachyOS/linux-cachyos
### The authors of linux-cachyos patchset:
# Peter Jung ptr1337 <admin@ptr1337.dev>
# Piotr Gorski sirlucjan <piotrgorski@cachyos.org>
### The author of BORE-EEVDF Scheduler:
# Masahito Suzuki <firelzrd@gmail.com>
### The port maintainer for Fedora:
# bieszczaders <zbyszek@linux.pl>
# https://copr.fedorainfracloud.org/coprs/bieszczaders/
%global _default_patch_fuzz 2
%global _is_rc 0

%define _build_id_links none
%define _disable_source_fetch 0

# See https://fedoraproject.org/wiki/Changes/SetBuildFlagsBuildCheck to why this has to be done
%if 0%{?fedora} >= 37
%undefine _auto_set_build_flags
%endif

%ifarch x86_64
%define karch x86
%define asmarch x86
%endif

# define git branch to make testing easier without merging to master branch
%define _git_branch master

# whether to build kernel with llvm compiler(clang)
%define llvm_kbuild 0
%if %{llvm_kbuild}
%define llvm_build_env_vars CC=clang CXX=clang++ LD=ld.lld LLVM=1 LLVM_IAS=1
%define ltoflavor 1
%endif

Name: kernel
Summary: The Linux Kernel with Cachyos and Nobara Patches

%define _basekver 6.15
%define _stablekver 8
%define _rcver rc7
%if %{_stablekver} == 0
%define _tarkver %{_basekver}
%else
%define _tarkver %{_basekver}.%{_stablekver}
%endif
%if 0%{?_is_rc}
%define _tarkver %{_basekver}-%{_rcver}
%endif

Version: %{_basekver}.%{_stablekver}

%if 0%{?_is_rc}
%define customver 0.%{_rcver}
%else
%define customver 200
%endif

Release:%{customver}.nobara%{?dist}

# Define rawhide fedora version
%define _rawhidever 43

%define rpmver %{version}-%{release}
%define rpmverobsolete 6.12.9-200.fsync%{?dist}
%define krelstr %{release}.%{_arch}
%define kverstr %{version}-%{krelstr}

License: GPLv2 and Redistributable, no modifications permitted
Group: System Environment/Kernel
Vendor: The Linux Community and CachyOS maintainer(s)
URL: https://cachyos.org
Source0: https://cdn.kernel.org/pub/linux/kernel/v6.x/linux-%{_tarkver}.tar.xz
%if 0%{?_is_rc}
Source1: https://raw.githubusercontent.com/CachyOS/linux-cachyos/master/linux-cachyos-rc/config
%else
Source1: https://raw.githubusercontent.com/CachyOS/linux-cachyos/master/linux-cachyos/config
%endif

# needed for kernel-tools
Source2: kvm_stat.logrotate

# https://fedoraproject.org/wiki/Changes/EncourageI686LeafRemoval
ExcludeArch:    %{ix86}

# Stable patches
Patch0: https://raw.githubusercontent.com/CachyOS/kernel-patches/master/%{_basekver}/all/0001-cachyos-base-all.patch
Patch1: https://raw.githubusercontent.com/CachyOS/kernel-patches/master/%{_basekver}/sched/0001-bore-cachy.patch
# For handhelds
Patch2: https://raw.githubusercontent.com/CachyOS/kernel-patches/master/%{_basekver}/misc/0001-handheld.patch

# Nobara
#surface
Patch3: linux-surface.patch
# Asus laptops
Patch4: asus-linux.patch
# rog ally/x
Patch5: ROG-ALLY-NCT6775-PLATFORM.patch
# ayaneo
Patch6: bmi160_ayaneo.patch
# Logitech wheel
Patch7: ps-logitech-wheel.patch
# give kernel taint warning when amdgpu power controls are enabled
Patch8: amdgpu.ppfeaturemask-taint_warning.patch
# fixes framerate control in gamescope
Patch9: valve-gamescope-framerate-control-fixups.patch
# fixes orientation on SuiPlay0X1
Patch10: suiplay0x1-orientation-quirk.patch
# fixes headphones on various Aya Neo devices
Patch11: ayaneo-headset-fix.patch

# temporary patches
# fixes HAINAN amdgpu card not being bootable
# https://gitlab.freedesktop.org/drm/amd/-/issues/1839
Patch12: amdgpu-HAINAN-variant-fixup.patch
# Allow to set custom USB pollrate for specific devices like so:
# usbcore.interrupt_interval_override=045e:00db:16,1bcf:0005:1
# useful for setting polling rate of wired PS4/PS5 controller to 1000Hz
# https://github.com/KarsMulder/Linux-Pollrate-Patch
# https://gitlab.com/GloriousEggroll/nobara-images/-/issues/64
Patch13: 0001-Allow-to-set-custom-USB-pollrate-for-specific-device.patch
# Add xpadneo as patch instead of using dkms module
Patch14: 0001-Add-xpadneo-bluetooth-hid-driver-module.patch
# https://gitlab.freedesktop.org/drm/amd/-/issues/4263
Patch15: drm-atomic-flip.1.patch

# aarch64 patches
Patch16: 0001-ampere-arm64-Add-a-fixup-handler-for-alignment-fault.patch
Patch17: 0002-ampere-arm64-Work-around-Ampere-Altra-erratum-82288-.patch
Patch18: xe-nonx86.patch

%define __spec_install_post /usr/lib/rpm/brp-compress || :
%define debug_package %{nil}
# Default compression algorithm
%global compression xz
%global compression_flags --compress
%global compext xz

%if %{llvm_kbuild}
BuildRequires: llvm
BuildRequires: clang
BuildRequires: lld
%endif
BuildRequires: asciidoc
BuildRequires: audit-libs-devel python3-setuptools
BuildRequires: bash
BuildRequires: bc
BuildRequires: binutils
BuildRequires: binutils-%{_build_arch}-linux-gnu, gcc-%{_build_arch}-linux-gnu
BuildRequires: bzip2, xz, findutils, m4, perl-interpreter, perl-Carp, perl-devel, perl-generators, make, diffutils, gawk, %compression
BuildRequires: dracut
BuildRequires: dwarves
BuildRequires: gcc, binutils, redhat-rpm-config, hmaccalc, bison, flex, gcc-c++
BuildRequires: gettext ncurses-devel
BuildRequires: glibc-static
BuildRequires: grubby
BuildRequires: gzip
BuildRequires: hostname
BuildRequires: java-devel
BuildRequires: kabi-dw
BuildRequires: kernel-rpm-macros
BuildRequires: kmod, bash, coreutils, tar, git-core, which
BuildRequires: libbabeltrace-devel
BuildRequires: libbpf-devel >= 0.6.0-1
BuildRequires: libcap-devel libcap-ng-devel
BuildRequires: libcap-devel libcap-ng-devel rsync libmnl-devel
BuildRequires: libnl3-devel
BuildRequires: libtraceevent-devel
BuildRequires: libtracefs-devel
BuildRequires: lvm2
BuildRequires: net-tools, hostname, bc, elfutils-devel
BuildRequires: nss-tools
BuildRequires: numactl-devel
BuildRequires: opencsd-devel >= 1.0.0
BuildRequires: openssl
BuildRequires: openssl-devel
BuildRequires: pciutils-devel
BuildRequires: pesign >= 0.10-4
BuildRequires: python3
BuildRequires: python3-devel
BuildRequires: python3-docutils
BuildRequires: python3-pyyaml
BuildRequires: rpm-build, elfutils
BuildRequires: rsync
BuildRequires: rust, rust-src, bindgen
BuildRequires: sparse
BuildRequires: systemd-boot-unsigned
BuildRequires: systemd-udev >= 252-1
BuildRequires: systemd-ukify
BuildRequires: tpm2-tools
BuildRequires: wget
BuildRequires: xmlto
BuildRequires: xmlto, asciidoc, python3-sphinx, python3-sphinx_rtd_theme
BuildRequires: zlib-devel binutils-devel newt-devel perl(ExtUtils::Embed) bison flex xz-devel


Requires: %{name}-core-%{rpmver} = %{kverstr}
Requires: %{name}-modules-%{rpmver} = %{kverstr}
Provides: %{name}%{_basekver} = %{rpmver}
Provides: kernel-bore-eevdf >= 6.5.7-%{customver}
Provides: kernel-bore >= 6.5.7-%{customver}
Obsoletes: kernel-bore-eevdf <= 6.5.10-%{customver}
Obsoletes: kernel-bore <= 6.5.10-%{customver}
Provides: kernel-uki-vert = %{rpmver}
Obsoletes: kernel <= %{rpmverobsolete}
# v4l2loopback module is provided by cachy-base-all patch
Obsoletes: akmod-v4l2loopback

%description
The kernel-%{flaver} meta package

%package core
Summary: Kernel core package
Group: System Environment/Kernel
Provides: installonlypkg(kernel)
Provides: kernel = %{rpmver}
Provides: kernel-core = %{rpmver}
Provides: kernel-core-uname-r = %{kverstr}
Provides: kernel-uname-r = %{kverstr}
Provides: kernel-%{_arch} = %{rpmver}
Provides: kernel-core%{_isa} = %{rpmver}
Provides: kernel-core-%{rpmver} = %{kverstr}
Provides: %{name}-core-%{rpmver} = %{kverstr}
Provides:  kernel-drm-nouveau = 16
# multiver
Provides: %{name}%{_basekver}-core = %{rpmver}
Requires: bash
Requires: coreutils
Requires: linux-firmware
Requires: /usr/bin/kernel-install
Requires: kernel-modules-%{rpmver} = %{kverstr}
Supplements: %{name} = %{rpmver}
Provides: kernel-bore-eevdf-core >= 6.5.7-%{customver}
Provides: kernel-bore-core >= 6.5.7-%{customver}
Obsoletes: kernel-bore-eevdf-core <= 6.5.10-%{customver}
Obsoletes: kernel-bore-core <= 6.5.10-%{customver}
%description core
The kernel package contains the Linux kernel (vmlinuz), the core of any
Linux operating system.  The kernel handles the basic functions
of the operating system: memory allocation, process allocation, device
input and output, etc.

%package modules
Summary: Kernel modules to match the core kernel
Group: System Environment/Kernel
Provides: installonlypkg(kernel-module)
Provides: %{name}%{_basekver}-modules = %{rpmver}
Provides: kernel-modules = %{rpmver}
Provides: kernel-modules%{_isa} = %{rpmver}
Provides: kernel-modules-core = %{rpmver}
Provides: kernel-modules-extra = %{rpmver}
Provides: kernel-modules-uname-r = %{kverstr}
Provides: kernel-modules-%{_arch} = %{rpmver}
Provides: kernel-modules-core-uname-r = %{kverstr}
Provides: kernel-modules-extra-uname-r = %{kverstr}
Provides: kernel-modules-%{rpmver} = %{kverstr}
Provides: %{name}-modules-%{rpmver} = %{kverstr}
Supplements: %{name} = %{rpmver}
Provides: kernel-bore-eevdf-modules >= 6.5.7-%{customver}
Provides: kernel-bore-modules >= 6.5.7-%{customver}
Obsoletes: kernel-bore-eevdf-modules <= 6.5.10-%{customver}
Obsoletes: kernel-bore-modules <= 6.5.10-%{customver}
# kmod needed for depmod command in %%post
Requires: kmod
%description modules
This package provides kernel modules for the core %{?flavor:%{flavor}} kernel package.


%package headers
Summary: Header files for the Linux kernel for use by glibc
Group: Development/System
Provides: kernel-headers = %{kverstr}
Provides: glibc-kernheaders = 3.0-46
Provides: kernel-headers%{_isa} = %{kverstr}
Obsoletes: kernel-headers < %{kverstr}
Obsoletes: glibc-kernheaders < 3.0-46
Obsoletes: kernel-bore-eevdf-headers <= 6.5.10-%{customver}
Obsoletes: kernel-bore-headers <= 6.5.10-%{customver}
Provides: kernel-bore-eevdf-headers >= 6.5.7-%{customver}
Provides: kernel-bore-headers >= 6.5.7-%{customver}
%description headers
Kernel-headers includes the C header files that specify the interface
between the Linux kernel and userspace libraries and programs.  The
header files define structures and constants that are needed for
building most standard programs and are also needed for rebuilding the
glibc package.

%package devel
Summary: Development package for building kernel modules to match the %{?flavor:%{flavor}} kernel
Group: System Environment/Kernel
AutoReqProv: no
Requires: findutils
Requires: perl-interpreter
Requires: openssl-devel
Requires: flex
Requires: make
Requires: bison
Requires: elfutils-libelf-devel
Requires: gcc
%if %{llvm_kbuild}
Requires: clang
Requires: llvm
Requires: lld
%endif
Enhances: akmods
Enhances: dkms
Provides: installonlypkg(kernel)
Provides: kernel-devel = %{rpmver}
Provides: kernel-devel-uname-r = %{kverstr}
Provides: kernel-devel-%{_arch} = %{rpmver}
Provides: kernel-devel%{_isa} = %{rpmver}
Provides: kernel-devel-%{rpmver} = %{kverstr}
Provides: %{name}-devel-%{rpmver} = %{kverstr}
Provides: %{name}%{_basekver}-devel = %{rpmver}
Provides: kernel-bore-eevdf-devel >= 6.5.7-%{customver}
Provides: kernel-bore-devel >= 6.5.7-%{customver}
Obsoletes: kernel-bore-eevdf-devel <= 6.5.10-%{customver}
Obsoletes: kernel-bore-devel <= 6.5.10-%{customver}
%description devel
This package provides kernel headers and makefiles sufficient to build modules
against the %{?flavor:%{flavor}} kernel package.

%package devel-matched
Summary: Meta package to install matching core and devel packages for a given %{?flavor:%{flavor}} kernel
Requires: %{name}-devel = %{rpmver},
Requires: %{name}-core = %{rpmver}
Provides: kernel-devel-matched = %{rpmver}
Provides: kernel-devel-matched%{_isa} = %{rpmver}
Provides: kernel-bore-eevdf-devel-matched >= 6.5.7-%{customver}
Provides: kernel-bore-devel-matched >= 6.5.7-%{customver}
Obsoletes: kernel-bore-eevdf-devel-matched <= 6.5.10-%{customver}
Obsoletes: kernel-bore-devel-matched <= 6.5.10-%{customver}
%description devel-matched
This meta package is used to install matching core and devel packages for a given %{?flavor:%{flavor}} kernel.

%package -n perf
Summary: Performance monitoring for the Linux kernel
Requires: bzip2
%description -n perf
This package contains the perf tool, which enables performance monitoring
of the Linux kernel.

%package -n python3-perf
Summary: Python bindings for apps which will manipulate perf events
%description -n python3-perf
The python3-perf package contains a module that permits applications
written in the Python programming language to use the interface
to manipulate perf events.

%package -n libperf
Summary: The perf library from kernel source
%description -n libperf
This package contains the kernel source perf library.

%package -n libperf-devel
Summary: Developement files for the perf library from kernel source
Requires: libperf = %{version}-%{release}
%description -n libperf-devel
This package includes libraries and header files needed for development
of applications which use perf library from kernel source.

%package tools
Summary: Assortment of tools for the Linux kernel
Provides:  cpupowerutils = 1:009-0.6.p1
Obsoletes: cpupowerutils < 1:009-0.6.p1
Provides:  cpufreq-utils = 1:009-0.6.p1
Provides:  cpufrequtils = 1:009-0.6.p1
Obsoletes: cpufreq-utils < 1:009-0.6.p1
Obsoletes: cpufrequtils < 1:009-0.6.p1
Obsoletes: cpuspeed < 1:1.5-16
Requires: %{name}-tools-libs = %{version}-%{release}
%define __requires_exclude ^%{_bindir}/python
%description tools
This package contains the tools/ directory from the kernel source
and the supporting documentation.

%package tools-libs
Summary: Libraries for the kernels-tools
%description tools-libs
This package contains the libraries built from the tools/ directory
from the kernel source.

%package tools-libs-devel
Summary: Assortment of tools for the Linux kernel
Requires: %{name}-tools = %{version}-%{release}
Provides:  cpupowerutils-devel = 1:009-0.6.p1
Obsoletes: cpupowerutils-devel < 1:009-0.6.p1
Requires: %{name}-tools-libs = %{version}-%{release}
Provides: %{name}-tools-devel
%description tools-libs-devel
This package contains the development files for the tools/ directory from
the kernel source.

%package -n rtla
Summary: Real-Time Linux Analysis tools
Requires: libtraceevent
Requires: libtracefs
%description -n rtla
The rtla meta-tool includes a set of commands that aims to analyze
the real-time properties of Linux. Instead of testing Linux as a black box,
rtla leverages kernel tracing capabilities to provide precise information
about the properties and root causes of unexpected results.

%package -n rv
Summary: RV: Runtime Verification
%description -n rv
Runtime Verification (RV) is a lightweight (yet rigorous) method that
complements classical exhaustive verification techniques (such as model
checking and theorem proving) with a more practical approach for
complex systems.
The rv tool is the interface for a collection of monitors that aim
analysing the logical and timing behavior of Linux.


%prep
%setup -q -n linux-%{_tarkver}

# Apply CachyOS patch
patch -p1 -i %{PATCH0}

# Apply EEVDF and BORE patches
patch -p1 -i %{PATCH1}

# Apply Nobara patches:
patch -p1 -i %{PATCH2}
patch -p1 -i %{PATCH3}
patch -p1 -i %{PATCH4}
patch -p1 -i %{PATCH5}
patch -p1 -i %{PATCH6}
patch -p1 -i %{PATCH7}
patch -p1 -i %{PATCH8}
patch -p1 -i %{PATCH9}
patch -p1 -i %{PATCH10}
patch -p1 -i %{PATCH11}
patch -p1 -i %{PATCH12}
patch -p1 -i %{PATCH13}
patch -p1 -i %{PATCH14}
patch -p1 -i %{PATCH15}

# Apply aarch64 patches
patch -p1 -i %{PATCH16}
patch -p1 -i %{PATCH17}
patch -p1 -i %{PATCH18}

# Fetch the config and move it to the proper directory
cp %{SOURCE1} .config

# Remove CachyOS's localversion
find . -name "localversion*" -delete
scripts/config -u LOCALVERSION

# Enable CachyOS tweaks
scripts/config -e CACHY

# Enable BORE Scheduler
scripts/config -e SCHED_BORE

# Enable sched-ext
scripts/config -e SCHED_CLASS_EXT
scripts/config -e BPF
scripts/config -e BPF_EVENTS
scripts/config -e BPF_JIT
scripts/config -e BPF_SYSCALL
scripts/config -e DEBUG_INFO
scripts/config -e DEBUG_INFO_BTF
scripts/config -e DEBUG_INFO_BTF_MODULES
scripts/config -e FTRACE
scripts/config -e PAHOLE_HAS_SPLIT_BTF
scripts/config -e DEBUG_INFO_DWARF_TOOLCHAIN_DEFAULT
scripts/config -e SCHED_DEBUG

# Setting tick rate
scripts/config -d HZ_300
scripts/config -e HZ_1000
scripts/config --set-val HZ 1000

# Enable x86_64_v3
# Just to be sure, check:
# /lib/ld-linux-x86-64.so.2 --help | grep supported
# and make sure if your processor supports it:
# x86-64-v3 (supported, searched)
#scripts/config --set-val X86_64_VERSION 3

# Set O3
scripts/config -d CC_OPTIMIZE_FOR_PERFORMANCE
scripts/config -e CC_OPTIMIZE_FOR_PERFORMANCE_O3

# Enable full ticks
scripts/config -d HZ_PERIODIC
scripts/config -d NO_HZ_IDLE
scripts/config -d CONTEXT_TRACKING_FORCE
scripts/config -e NO_HZ_FULL_NODEF
scripts/config -e NO_HZ_FULL
scripts/config -e NO_HZ
scripts/config -e NO_HZ_COMMON
scripts/config -e CONTEXT_TRACKING

# Enable full preempt
scripts/config -e PREEMPT_BUILD
scripts/config -d PREEMPT_NONE
scripts/config -d PREEMPT_VOLUNTARY
scripts/config -e PREEMPT
scripts/config -e PREEMPT_COUNT
scripts/config -e PREEMPTION
scripts/config -e PREEMPT_DYNAMIC

# Enable thin lto
%if %{llvm_kbuild}
scripts/config -e LTO
scripts/config -e LTO_CLANG
scripts/config -e ARCH_SUPPORTS_LTO_CLANG
scripts/config -e ARCH_SUPPORTS_LTO_CLANG_THIN
scripts/config -d LTO_NONE
scripts/config -e HAS_LTO_CLANG
scripts/config -d LTO_CLANG_FULL
scripts/config -e LTO_CLANG_THIN
scripts/config -e HAVE_GCC_PLUGINS
%endif

# Unset hostname
scripts/config -u DEFAULT_HOSTNAME

# Set kernel version string as build salt
scripts/config --set-str BUILD_SALT "%{kverstr}"

# Finalize the patched config
make %{?_smp_mflags} %{?llvm_build_env_vars} EXTRAVERSION=-%{krelstr} olddefconfig

# Save configuration for later reuse
cat .config > config-linux-bore

%build
make %{?_smp_mflags} %{?llvm_build_env_vars} EXTRAVERSION=-%{krelstr}
%if %{llvm_kbuild}
clang ./scripts/sign-file.c -o ./scripts/sign-file -lssl -lcrypto
%else
gcc ./scripts/sign-file.c -o ./scripts/sign-file -lssl -lcrypto
%endif

# non-kernel userspace packages -- disable LTO
%if "%{?_lto_cflags}" != ""
%global _lto_cflags %{nil}

# perf
%global perf_make \
  %{__make} %{?make_opts} EXTRA_CFLAGS="${RPM_OPT_FLAGS}" EXTRA_CXXFLAGS="${RPM_OPT_FLAGS}" LDFLAGS="%{__global_ldflags} -Wl,-E" %{?cross_opts} -C tools/perf V=1 NO_PERF_READ_VDSO32=1 NO_PERF_READ_VDSOX32=1 WERROR=0 NO_LIBUNWIND=1 HAVE_CPLUS_DEMANGLE=1 NO_GTK2=1 NO_STRLCPY=1 NO_BIONIC=1 LIBBPF_DYNAMIC=1 LIBTRACEEVENT_DYNAMIC=1 %{?perf_build_extra_opts} prefix=%{_prefix} PYTHON=%{__python3}
# perf
# make sure check-headers.sh is executable
chmod +x tools/perf/check-headers.sh
%{perf_make} DESTDIR=$RPM_BUILD_ROOT all

# libperf
%global libperf_make \
  %{__make} %{?make_opts} EXTRA_CFLAGS="${RPM_OPT_FLAGS}" LDFLAGS="%{__global_ldflags}" %{?cross_opts} -C tools/lib/perf V=1
%{libperf_make} DESTDIR=$RPM_BUILD_ROOT

%define make %{__make} %{?cross_opts} %{?make_opts} HOSTCFLAGS="%{?build_hostcflags}" HOSTLDFLAGS="%{?build_hostldflags}"

# kernel-tools
%global tools_make \
  CFLAGS="${RPM_OPT_FLAGS}" LDFLAGS="%{__global_ldflags}" EXTRA_CFLAGS="${RPM_OPT_FLAGS}" %{make} %{?make_opts}
# cpupower
# make sure version-gen.sh is executable.
chmod +x tools/power/cpupower/utils/version-gen.sh
%{tools_make} %{?_smp_mflags} -C tools/power/cpupower CPUFREQ_BENCH=false DEBUG=false
%ifarch x86_64
    pushd tools/power/cpupower/debug/x86_64
    %{tools_make} %{?_smp_mflags} centrino-decode powernow-k8-decode
    popd
%endif
%ifarch x86_64
   pushd tools/power/x86/x86_energy_perf_policy/
   %{tools_make}
   popd
   pushd tools/power/x86/turbostat
   %{tools_make}
   popd
   pushd tools/power/x86/intel-speed-select
   %{tools_make}
   popd
   pushd tools/arch/x86/intel_sdsi
   %{tools_make} CFLAGS="${RPM_OPT_FLAGS}"
   popd
%endif
pushd tools/thermal/tmon/
%{tools_make}
popd
pushd tools/bootconfig/
%{tools_make}
popd
pushd tools/iio/
%{tools_make}
popd
pushd tools/gpio/
%{tools_make}
popd
# build VM tools
pushd tools/mm/
%{tools_make} slabinfo page_owner_sort
popd
pushd tools/verification/rv/
%{tools_make}
popd
pushd tools/tracing/rtla
%{tools_make}
popd

%endif

%install

ImageName=$(make image_name | tail -n 1)

mkdir -p %{buildroot}/boot

cp -v $ImageName %{buildroot}/boot/vmlinuz-%{kverstr}
chmod 755 %{buildroot}/boot/vmlinuz-%{kverstr}

ZSTD_CLEVEL=19 make %{?_smp_mflags} %{?llvm_build_env_vars} INSTALL_MOD_PATH=%{buildroot} INSTALL_MOD_STRIP=1 modules_install mod-fw=
make %{?_smp_mflags} %{?llvm_build_env_vars} INSTALL_HDR_PATH=%{buildroot}/usr headers_install

# prepare -devel files
### all of the things here are derived from the Fedora kernel.spec
### see
##### https://src.fedoraproject.org/rpms/kernel/blob/rawhide/f/kernel.spec
cd %{_builddir}/linux-%{_tarkver}
rm -f %{buildroot}/lib/modules/%{kverstr}/build
rm -f %{buildroot}/lib/modules/%{kverstr}/source
mkdir -p %{buildroot}/lib/modules/%{kverstr}/build
(cd %{buildroot}/lib/modules/%{kverstr} ; ln -s build source)
# dirs for additional modules per module-init-tools, kbuild/modules.txt
mkdir -p %{buildroot}/lib/modules/%{kverstr}/updates
mkdir -p %{buildroot}/lib/modules/%{kverstr}/weak-updates
# CONFIG_KERNEL_HEADER_TEST generates some extra files in the process of
# testing so just delete
find . -name *.h.s -delete
# first copy everything
cp --parents `find  -type f -name "Makefile*" -o -name "Kconfig*"` %{buildroot}/lib/modules/%{kverstr}/build
if [ ! -e Module.symvers ]; then
touch Module.symvers
fi
cp Module.symvers %{buildroot}/lib/modules/%{kverstr}/build
cp System.map %{buildroot}/lib/modules/%{kverstr}/build
if [ -s Module.markers ]; then
cp Module.markers %{buildroot}/lib/modules/%{kverstr}/build
fi

# create the kABI metadata for use in packaging
# NOTENOTE: the name symvers is used by the rpm backend
# NOTENOTE: to discover and run the /usr/lib/rpm/fileattrs/kabi.attr
# NOTENOTE: script which dynamically adds exported kernel symbol
# NOTENOTE: checksums to the rpm metadata provides list.
# NOTENOTE: if you change the symvers name, update the backend too
echo "**** GENERATING kernel ABI metadata ****"
gzip -c9 < Module.symvers > %{buildroot}/boot/symvers-%{kverstr}.gz
cp %{buildroot}/boot/symvers-%{kverstr}.gz %{buildroot}/lib/modules/%{kverstr}/symvers.gz

# then drop all but the needed Makefiles/Kconfig files
rm -rf %{buildroot}/lib/modules/%{kverstr}/build/scripts
rm -rf %{buildroot}/lib/modules/%{kverstr}/build/include
cp .config %{buildroot}/lib/modules/%{kverstr}/build
cp -a scripts %{buildroot}/lib/modules/%{kverstr}/build
rm -rf %{buildroot}/lib/modules/%{kverstr}/build/scripts/tracing
rm -f %{buildroot}/lib/modules/%{kverstr}/build/scripts/spdxcheck.py

%ifarch s390x
# CONFIG_EXPOLINE_EXTERN=y produces arch/s390/lib/expoline/expoline.o
# which is needed during external module build.
if [ -f arch/s390/lib/expoline/expoline.o ]; then
cp -a --parents arch/s390/lib/expoline/expoline.o %{buildroot}/lib/modules/%{kverstr}/build
fi
%endif

# Files for 'make scripts' to succeed with kernel-devel.
mkdir -p %{buildroot}/lib/modules/%{kverstr}/build/tools/include/tools
cp -a --parents tools/include/tools/be_byteshift.h %{buildroot}/lib/modules/%{kverstr}/build
cp -a --parents tools/include/tools/le_byteshift.h %{buildroot}/lib/modules/%{kverstr}/build

# Files for 'make prepare' to succeed with kernel-devel.
cp -a --parents tools/include/linux/compiler* %{buildroot}/lib/modules/%{kverstr}/build
cp -a --parents tools/include/linux/types.h %{buildroot}/lib/modules/%{kverstr}/build
cp -a --parents tools/build/Build.include %{buildroot}/lib/modules/%{kverstr}/build
cp --parents tools/build/fixdep.c %{buildroot}/lib/modules/%{kverstr}/build
cp --parents tools/objtool/sync-check.sh %{buildroot}/lib/modules/%{kverstr}/build
cp -a --parents tools/bpf/resolve_btfids %{buildroot}/lib/modules/%{kverstr}/build

cp -a --parents tools/include/asm-generic %{buildroot}/lib/modules/%{kverstr}/build
cp -a --parents tools/include/linux %{buildroot}/lib/modules/%{kverstr}/build
cp -a --parents tools/include/uapi/asm %{buildroot}/lib/modules/%{kverstr}/build
cp -a --parents tools/include/uapi/asm-generic %{buildroot}/lib/modules/%{kverstr}/build
cp -a --parents tools/include/uapi/linux %{buildroot}/lib/modules/%{kverstr}/build
cp -a --parents tools/include/vdso %{buildroot}/lib/modules/%{kverstr}/build
cp --parents tools/scripts/utilities.mak %{buildroot}/lib/modules/%{kverstr}/build
cp -a --parents tools/lib/subcmd %{buildroot}/lib/modules/%{kverstr}/build
cp --parents tools/lib/*.c %{buildroot}/lib/modules/%{kverstr}/build
cp --parents tools/objtool/*.[ch] %{buildroot}/lib/modules/%{kverstr}/build
cp --parents tools/objtool/Build %{buildroot}/lib/modules/%{kverstr}/build
cp --parents tools/objtool/include/objtool/*.h %{buildroot}/lib/modules/%{kverstr}/build
cp -a --parents tools/lib/bpf %{buildroot}/lib/modules/%{kverstr}/build
cp --parents tools/lib/bpf/Build %{buildroot}/lib/modules/%{kverstr}/build

if [ -f tools/objtool/objtool ]; then
  cp -a tools/objtool/objtool %{buildroot}/lib/modules/%{kverstr}/build/tools/objtool/ || :
fi
if [ -f tools/objtool/fixdep ]; then
  cp -a tools/objtool/fixdep %{buildroot}/lib/modules/%{kverstr}/build/tools/objtool/ || :
fi
if [ -d arch/%{karch}/scripts ]; then
  cp -a arch/%{karch}/scripts %{buildroot}/lib/modules/%{kverstr}/build/arch/%{_arch} || :
fi
if [ -f arch/%{karch}/*lds ]; then
  cp -a arch/%{karch}/*lds %{buildroot}/lib/modules/%{kverstr}/build/arch/%{_arch}/ || :
fi
if [ -f arch/%{asmarch}/kernel/module.lds ]; then
  cp -a --parents arch/%{asmarch}/kernel/module.lds %{buildroot}/lib/modules/%{kverstr}/build/
fi
find %{buildroot}/lib/modules/%{kverstr}/build/scripts \( -iname "*.o" -o -iname "*.cmd" \) -exec rm -f {} +
%ifarch ppc64le
cp -a --parents arch/powerpc/lib/crtsavres.[So] %{buildroot}/lib/modules/%{kverstr}/build/
%endif
if [ -d arch/%{asmarch}/include ]; then
  cp -a --parents arch/%{asmarch}/include %{buildroot}/lib/modules/%{kverstr}/build/
fi
%ifarch aarch64
# arch/arm64/include/asm/xen references arch/arm
cp -a --parents arch/arm/include/asm/xen %{buildroot}/lib/modules/%{kverstr}/build/
# arch/arm64/include/asm/opcodes.h references arch/arm
cp -a --parents arch/arm/include/asm/opcodes.h %{buildroot}/lib/modules/%{kverstr}/build/
%endif
# include the machine specific headers for ARM variants, if available.
%ifarch %{arm}
if [ -d arch/%{asmarch}/mach-${Variant}/include ]; then
  cp -a --parents arch/%{asmarch}/mach-${Variant}/include %{buildroot}/lib/modules/%{kverstr}/build/
fi
# include a few files for 'make prepare'
cp -a --parents arch/arm/tools/gen-mach-types %{buildroot}/lib/modules/%{kverstr}/build/
cp -a --parents arch/arm/tools/mach-types %{buildroot}/lib/modules/%{kverstr}/build/

%endif
cp -a include %{buildroot}/lib/modules/%{kverstr}/build/include

%ifarch i686 x86_64
# files for 'make prepare' to succeed with kernel-devel
cp -a --parents arch/x86/entry/syscalls/syscall_32.tbl %{buildroot}/lib/modules/%{kverstr}/build/
cp -a --parents arch/x86/entry/syscalls/syscall_64.tbl %{buildroot}/lib/modules/%{kverstr}/build/
cp -a --parents arch/x86/tools/relocs_32.c %{buildroot}/lib/modules/%{kverstr}/build/
cp -a --parents arch/x86/tools/relocs_64.c %{buildroot}/lib/modules/%{kverstr}/build/
cp -a --parents arch/x86/tools/relocs.c %{buildroot}/lib/modules/%{kverstr}/build/
cp -a --parents arch/x86/tools/relocs_common.c %{buildroot}/lib/modules/%{kverstr}/build/
cp -a --parents arch/x86/tools/relocs.h %{buildroot}/lib/modules/%{kverstr}/build/
cp -a --parents arch/x86/purgatory/purgatory.c %{buildroot}/lib/modules/%{kverstr}/build/
cp -a --parents arch/x86/purgatory/stack.S %{buildroot}/lib/modules/%{kverstr}/build/
cp -a --parents arch/x86/purgatory/setup-x86_64.S %{buildroot}/lib/modules/%{kverstr}/build/
cp -a --parents arch/x86/purgatory/entry64.S %{buildroot}/lib/modules/%{kverstr}/build/
cp -a --parents arch/x86/boot/string.h %{buildroot}/lib/modules/%{kverstr}/build/
cp -a --parents arch/x86/boot/string.c %{buildroot}/lib/modules/%{kverstr}/build/
cp -a --parents arch/x86/boot/ctype.h %{buildroot}/lib/modules/%{kverstr}/build/

cp -a --parents scripts/syscalltbl.sh %{buildroot}/lib/modules/%{kverstr}/build/
cp -a --parents scripts/syscallhdr.sh %{buildroot}/lib/modules/%{kverstr}/build/

cp -a --parents tools/arch/x86/include/asm %{buildroot}/lib/modules/%{kverstr}/build
cp -a --parents tools/arch/x86/include/uapi/asm %{buildroot}/lib/modules/%{kverstr}/build
cp -a --parents tools/objtool/arch/x86/lib %{buildroot}/lib/modules/%{kverstr}/build
cp -a --parents tools/arch/x86/lib/ %{buildroot}/lib/modules/%{kverstr}/build
cp -a --parents tools/arch/x86/tools/gen-insn-attr-x86.awk %{buildroot}/lib/modules/%{kverstr}/build
cp -a --parents tools/objtool/arch/x86/ %{buildroot}/lib/modules/%{kverstr}/build

%endif
# Clean up intermediate tools files
find %{buildroot}/lib/modules/%{kverstr}/build/tools \( -iname "*.o" -o -iname "*.cmd" \) -exec rm -f {} +

# Make sure the Makefile, version.h, and auto.conf have a matching
# timestamp so that external modules can be built
touch -r %{buildroot}/lib/modules/%{kverstr}/build/Makefile \
%{buildroot}/lib/modules/%{kverstr}/build/include/generated/uapi/linux/version.h \
%{buildroot}/lib/modules/%{kverstr}/build/include/config/auto.conf

find %{buildroot}/lib/modules/%{kverstr} -name "*.ko" -type f >modnames

# mark modules executable so that strip-to-file can strip them
xargs --no-run-if-empty chmod u+x < modnames

# Generate a list of modules for block and networking.

grep -F /drivers/ modnames | xargs --no-run-if-empty nm -upA |
sed -n 's,^.*/\([^/]*\.ko\):  *U \(.*\)$,\1 \2,p' > drivers.undef

collect_modules_list()
{
  sed -r -n -e "s/^([^ ]+) \\.?($2)\$/\\1/p" drivers.undef |
LC_ALL=C sort -u > %{buildroot}/lib/modules/%{kverstr}/modules.$1
  if [ ! -z "$3" ]; then
sed -r -e "/^($3)\$/d" -i %{buildroot}/lib/modules/%{kverstr}/modules.$1
  fi
}

collect_modules_list networking \
  'register_netdev|ieee80211_register_hw|usbnet_probe|phy_driver_register|rt(l_|2x00)(pci|usb)_probe|register_netdevice'
collect_modules_list block \
  'ata_scsi_ioctl|scsi_add_host|scsi_add_host_with_dma|blk_alloc_queue|blk_init_queue|register_mtd_blktrans|scsi_esp_register|scsi_register_device_handler|blk_queue_physical_block_size' 'pktcdvd.ko|dm-mod.ko'
collect_modules_list drm \
  'drm_open|drm_init'
collect_modules_list modesetting \
  'drm_crtc_init'

# detect missing or incorrect license tags
( find %{buildroot}/lib/modules/%{kverstr} -name '*.ko' | xargs /sbin/modinfo -l | \
grep -E -v 'GPL( v2)?$|Dual BSD/GPL$|Dual MPL/GPL$|GPL and additional rights$' ) && exit 1

remove_depmod_files()
{
# remove files that will be auto generated by depmod at rpm -i time
pushd %{buildroot}/lib/modules/%{kverstr}/
rm -f modules.{alias,alias.bin,builtin.alias.bin,builtin.bin} \
  modules.{dep,dep.bin,devname,softdep,symbols,symbols.bin}
popd
}

remove_depmod_files

mkdir -p %{buildroot}%{_prefix}/src/kernels
mv %{buildroot}/lib/modules/%{kverstr}/build %{buildroot}%{_prefix}/src/kernels/%{kverstr}

# This is going to create a broken link during the build, but we don't use
# it after this point.  We need the link to actually point to something
# when kernel-devel is installed, and a relative link doesn't work across
# the F17 UsrMove feature.
ln -sf %{_prefix}/src/kernels/%{kverstr} %{buildroot}/lib/modules/%{kverstr}/build

find %{buildroot}%{_prefix}/src/kernels -name ".*.cmd" -delete
#

cp -v System.map %{buildroot}/boot/System.map-%{kverstr}
cp -v System.map %{buildroot}/lib/modules/%{kverstr}/System.map
cp -v .config %{buildroot}/boot/config-%{kverstr}
cp -v .config %{buildroot}/lib/modules/%{kverstr}/config

(cd "%{buildroot}/boot/" && sha512hmac "vmlinuz-%{kverstr}" > ".vmlinuz-%{kverstr}.hmac")

cp -v  %{buildroot}/boot/vmlinuz-%{kverstr} %{buildroot}/lib/modules/%{kverstr}/vmlinuz
(cd "%{buildroot}/lib/modules/%{kverstr}" && sha512hmac vmlinuz > .vmlinuz.hmac)

# create dummy initramfs image to inflate the disk space requirement for the initramfs. 48M seems to be the right size nowadays with more and more hardware requiring initramfs-located firmware to work properly (for reference, Fedora has it set to 20M)
dd if=/dev/zero of=%{buildroot}/boot/initramfs-%{kverstr}.img bs=1M count=48

# perf tool binary and supporting scripts/binaries
%{perf_make} DESTDIR=$RPM_BUILD_ROOT lib=%{_lib} install-bin
# remove the 'trace' symlink.
rm -f %{buildroot}%{_bindir}/trace

# For both of the below, yes, this should be using a macro but right now
# it's hard coded and we don't actually want it anyway right now.
# Whoever wants examples can fix it up!

# remove examples
rm -rf %{buildroot}/usr/lib/perf/examples
rm -rf %{buildroot}/usr/lib/perf/include

# python-perf extension
%{perf_make} DESTDIR=$RPM_BUILD_ROOT install-python_ext

# perf man pages (note: implicit rpm magic compresses them later)
mkdir -p %{buildroot}/%{_mandir}/man1
%{perf_make} DESTDIR=$RPM_BUILD_ROOT install-man

# remove any tracevent files, eg. its plugins still gets built and installed,
# even if we build against system's libtracevent during perf build (by setting
# LIBTRACEEVENT_DYNAMIC=1 above in perf_make macro). Those files should already
# ship with libtraceevent package.
rm -rf %{buildroot}%{_libdir}/traceevent

# perf/libperf
%{libperf_make} DESTDIR=%{buildroot} prefix=%{_prefix} libdir=%{_libdir} install install_headers
# This is installed on some arches and we don't want to ship it
rm -rf %{buildroot}%{_libdir}/libperf.a

# kernel-tools
%{make} -C tools/power/cpupower DESTDIR=$RPM_BUILD_ROOT libdir=%{_libdir} mandir=%{_mandir} CPUFREQ_BENCH=false install
%find_lang cpupower
cp cpupower.lang ../../
%ifarch x86_64
    pushd tools/power/cpupower/debug/x86_64
    install -m755 centrino-decode %{buildroot}%{_bindir}/centrino-decode
    install -m755 powernow-k8-decode %{buildroot}%{_bindir}/powernow-k8-decode
    popd
%endif
chmod 0755 %{buildroot}%{_libdir}/libcpupower.so*
%ifarch x86_64
   mkdir -p %{buildroot}%{_mandir}/man8
   pushd tools/power/x86/x86_energy_perf_policy
   %{tools_make} DESTDIR=%{buildroot} install
   popd
   pushd tools/power/x86/turbostat
   %{tools_make} DESTDIR=%{buildroot} install
   popd
   pushd tools/power/x86/intel-speed-select
   %{tools_make} DESTDIR=%{buildroot} install
   popd
   pushd tools/arch/x86/intel_sdsi
   %{tools_make} CFLAGS="${RPM_OPT_FLAGS}" DESTDIR=%{buildroot} BINDIR=%{_sbindir} install
   popd
%endif
pushd tools/thermal/tmon
%{tools_make} INSTALL_ROOT=%{buildroot} install
popd
pushd tools/bootconfig
%{tools_make} DESTDIR=%{buildroot} install
popd
pushd tools/iio
%{tools_make} DESTDIR=%{buildroot} install
popd
pushd tools/gpio
%{tools_make} DESTDIR=%{buildroot} install
popd
install -m644 -D %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/kvm_stat
pushd tools/kvm/kvm_stat
%{__make} INSTALL_ROOT=%{buildroot} install-tools
%{__make} INSTALL_ROOT=%{buildroot} install-man
install -m644 -D kvm_stat.service %{buildroot}%{_unitdir}/kvm_stat.service
popd
# install VM tools
pushd tools/mm/
install -m755 slabinfo %{buildroot}%{_bindir}/slabinfo
install -m755 page_owner_sort %{buildroot}%{_bindir}/page_owner_sort
popd
pushd tools/verification/rv/
%{tools_make} DESTDIR=%{buildroot} install
popd
pushd tools/tracing/rtla/
%{tools_make} DESTDIR=%{buildroot} install
rm -f %{buildroot}%{_bindir}/hwnoise
rm -f %{buildroot}%{_bindir}/osnoise
rm -f %{buildroot}%{_bindir}/timerlat
(cd %{buildroot}

        ln -sf rtla ./%{_bindir}/hwnoise
        ln -sf rtla ./%{_bindir}/osnoise
        ln -sf rtla ./%{_bindir}/timerlat
)
popd


%clean
rm -rf %{buildroot}

%post core
if [ `uname -i` == "x86_64" -o `uname -i` == "i386" ] &&
   [ -f /etc/sysconfig/kernel ]; then
  /bin/sed -r -i -e 's/^DEFAULTKERNEL=kernel-smp$/DEFAULTKERNEL=kernel/' /etc/sysconfig/kernel || exit $?
fi

%posttrans core
/bin/kernel-install add %{kverstr} /lib/modules/%{kverstr}/vmlinuz || exit $?
if [ ! -z $(rpm -qa | grep grubby) ]; then
  grubby --set-default="/boot/vmlinuz-%{kverstr}"
fi

%preun core
/bin/kernel-install remove %{kverstr} /lib/modules/%{kverstr}/vmlinuz || exit $?
if [ -x /usr/sbin/weak-modules ]
then
/usr/sbin/weak-modules --remove-kernel %{kverstr} || exit $?
fi

%post devel
if [ -f /etc/sysconfig/kernel ]
then
. /etc/sysconfig/kernel || exit $?
fi
if [ "$HARDLINK" != "no" -a -x /usr/bin/hardlink -a ! -e /run/ostree-booted ]
then
(cd /usr/src/kernels/%{kverstr} &&
 /usr/bin/find . -type f | while read f; do
   hardlink -c /usr/src/kernels/*%{?dist}.*/$f $f 2>&1 >/dev/null
 done)
fi

%post modules
/sbin/depmod -a %{kverstr}

%post tools-libs
/sbin/ldconfig

%postun tools-libs
/sbin/ldconfig

%files core
%ghost %attr(0600, root, root) /boot/vmlinuz-%{kverstr}
%ghost %attr(0600, root, root) /boot/System.map-%{kverstr}
%ghost %attr(0600, root, root) /boot/initramfs-%{kverstr}.img
%ghost %attr(0600, root, root) /boot/symvers-%{kverstr}.gz
%ghost %attr(0644, root, root) /boot/config-%{kverstr}
/boot/.vmlinuz-%{kverstr}.hmac
%dir /lib/modules/%{kverstr}/
/lib/modules/%{kverstr}/.vmlinuz.hmac
/lib/modules/%{kverstr}/config
/lib/modules/%{kverstr}/vmlinuz
/lib/modules/%{kverstr}/System.map
/lib/modules/%{kverstr}/symvers.gz

%files modules
/lib/modules/%{kverstr}/
%exclude /lib/modules/%{kverstr}/.vmlinuz.hmac
%exclude /lib/modules/%{kverstr}/config
%exclude /lib/modules/%{kverstr}/vmlinuz
%exclude /lib/modules/%{kverstr}/System.map
%exclude /lib/modules/%{kverstr}/symvers.gz
%exclude /lib/modules/%{kverstr}/build
%exclude /lib/modules/%{kverstr}/source

%files headers
%defattr (-, root, root)
/usr/include/*

%files devel
%defattr (-, root, root)
/usr/src/kernels/%{kverstr}
/lib/modules/%{kverstr}/build
/lib/modules/%{kverstr}/source

%files devel-matched

%files -n perf
%{_bindir}/perf
%{_libdir}/libperf-jvmti.so
%dir %{_libexecdir}/perf-core
%{_libexecdir}/perf-core/*
%{_mandir}/man[1-8]/perf*
%{_sysconfdir}/bash_completion.d/perf
%doc tools/perf/Documentation/examples.txt
%{_docdir}/perf-tip/tips.txt
%{_includedir}/perf/perf_dlfilter.h

%files -n python3-perf
%{python3_sitearch}/*

%files -n libperf
%{_libdir}/libperf.so.0
%{_libdir}/libperf.so.0.0.1

%files -n libperf-devel
%{_libdir}/libperf.so
%{_libdir}/pkgconfig/libperf.pc
%{_includedir}/internal/*.h
%{_includedir}/perf/bpf_perf.h
%{_includedir}/perf/core.h
%{_includedir}/perf/cpumap.h
%{_includedir}/perf/event.h
%{_includedir}/perf/evlist.h
%{_includedir}/perf/evsel.h
%{_includedir}/perf/mmap.h
%{_includedir}/perf/threadmap.h
%{_mandir}/man3/libperf.3.gz
%{_mandir}/man7/libperf-counting.7.gz
%{_mandir}/man7/libperf-sampling.7.gz
%{_docdir}/libperf/examples/sampling.c
%{_docdir}/libperf/examples/counting.c
%{_docdir}/libperf/html/libperf.html
%{_docdir}/libperf/html/libperf-counting.html
%{_docdir}/libperf/html/libperf-sampling.html

%files tools -f cpupower.lang
%{_bindir}/cpupower
%{_datadir}/bash-completion/completions/cpupower
%ifarch x86_64
%{_bindir}/centrino-decode
%{_bindir}/powernow-k8-decode
%endif
%{_mandir}/man[1-8]/cpupower*
%ifarch x86_64
%{_bindir}/x86_energy_perf_policy
%{_mandir}/man8/x86_energy_perf_policy*
%{_bindir}/turbostat
%{_mandir}/man8/turbostat*
%{_bindir}/intel-speed-select
%{_sbindir}/intel_sdsi
%endif
%{_bindir}/tmon
%{_bindir}/bootconfig
%{_bindir}/iio_event_monitor
%{_bindir}/iio_generic_buffer
%{_bindir}/lsiio
%{_bindir}/lsgpio
%{_bindir}/gpio-hammer
%{_bindir}/gpio-event-mon
%{_bindir}/gpio-watch
%{_mandir}/man1/kvm_stat*
%{_bindir}/kvm_stat
%{_unitdir}/kvm_stat.service
%config(noreplace) %{_sysconfdir}/logrotate.d/kvm_stat
%{_bindir}/page_owner_sort
%{_bindir}/slabinfo

%files tools-libs
%{_libdir}/libcpupower.so.1
%{_libdir}/libcpupower.so.1.0.1

%files tools-libs-devel
%{_libdir}/libcpupower.so
%{_includedir}/cpufreq.h
%{_includedir}/cpuidle.h
%{_includedir}/powercap.h

%files -n rtla
%{_bindir}/rtla
%{_bindir}/hwnoise
%{_bindir}/osnoise
%{_bindir}/timerlat
%{_mandir}/man1/rtla-hwnoise.1.gz
%{_mandir}/man1/rtla-osnoise-hist.1.gz
%{_mandir}/man1/rtla-osnoise-top.1.gz
%{_mandir}/man1/rtla-osnoise.1.gz
%{_mandir}/man1/rtla-timerlat-hist.1.gz
%{_mandir}/man1/rtla-timerlat-top.1.gz
%{_mandir}/man1/rtla-timerlat.1.gz
%{_mandir}/man1/rtla.1.gz

%files -n rv
%{_bindir}/rv
%{_mandir}/man1/rv-list.1.gz
%{_mandir}/man1/rv-mon-wip.1.gz
%{_mandir}/man1/rv-mon-wwnr.1.gz
%{_mandir}/man1/rv-mon.1.gz
%{_mandir}/man1/rv-mon-sched.1.gz
%{_mandir}/man1/rv.1.gz

%files

%changelog
* Thu Jul 24 2025 LionHeartP <LionHeartP@proton.me> - 6.15.8-200
- Update to 6.15.8

* Fri Jul 18 2025 LionHeartP <LionHeartP@proton.me> - 6.15.7-200
- Update to 6.15.7
- Start keeping changelog entries
