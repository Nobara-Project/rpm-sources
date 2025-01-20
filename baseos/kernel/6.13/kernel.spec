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

%define _basekver 6.13
%define _stablekver 0
%if %{_stablekver} == 0
%define _tarkver %{_basekver}
%else
%define _tarkver %{_basekver}.%{_stablekver}
%endif

Version: %{_basekver}.%{_stablekver}

%define customver 200

Release:%{customver}.nobara%{?dist}

# Define rawhide fedora version
%define _rawhidever 42

%define rpmver %{version}-%{release}
%define krelstr %{release}.%{_arch}
%define kverstr %{version}-%{krelstr}

License: GPLv2 and Redistributable, no modifications permitted
Group: System Environment/Kernel
Vendor: The Linux Community and CachyOS maintainer(s)
URL: https://cachyos.org
Source0: https://cdn.kernel.org/pub/linux/kernel/v6.x/linux-%{_tarkver}.tar.xz
Source1: https://raw.githubusercontent.com/CachyOS/linux-cachyos/master/linux-cachyos/config

# https://fedoraproject.org/wiki/Changes/EncourageI686LeafRemoval
ExcludeArch:    %{ix86}

# Stable patches
Patch0: https://raw.githubusercontent.com/CachyOS/kernel-patches/master/%{_basekver}/all/0001-cachyos-base-all.patch
Patch1: https://raw.githubusercontent.com/CachyOS/kernel-patches/master/%{_basekver}/sched/0001-bore-cachy.patch

# Nobara
#surface
Patch2: linux-surface.patch
# Steam deck
Patch3: steam-deck.patch
Patch4: steamdeck-oled-hw-quirks.patch
# Asus laptops
Patch5: asus-linux.patch
# rog ally/x
Patch6: asus-patch-series.patch
Patch7: ROG-ALLY-NCT6775-PLATFORM.patch
# ayaneo
Patch8: bmi160_ayaneo.patch
# minisforum v3
Patch9: amd-tablet-sfh.patch
# Legion laptops - disabled to test ASUS-wmi breakage
# Patch1: lenovo-legion-laptop.patch
# Logitech wheel
Patch10: ps-logitech-wheel.patch
# needed for some udev rules to apply properly
Patch11: uinput.patch
# give kernel taint warning when amdgpu power controls are enabled
Patch12: amdgpu.ppfeaturemask-taint_warning.patch
# fixes framerate control in gamescope
Patch13: valve-gamescope-framerate-control-fixups.patch

# temporary patches
# fixes HAINAN amdgpu card not being bootable
# https://gitlab.freedesktop.org/drm/amd/-/issues/1839
Patch14: amdgpu-HAINAN-variant-fixup.patch
Patch15: 0001-Revert-PCI-Add-a-REBAR-size-quirk-for-Sapphire-RX-56.patch
# Allow to set custom USB pollrate for specific devices like so:
# usbcore.interrupt_interval_override=045e:00db:16,1bcf:0005:1
# useful for setting polling rate of wired PS4/PS5 controller to 1000Hz
# https://github.com/KarsMulder/Linux-Pollrate-Patch
# https://gitlab.com/GloriousEggroll/nobara-images/-/issues/64
Patch16: 0001-Allow-to-set-custom-USB-pollrate-for-specific-device.patch
# Add xpadneo as patch instead of using dkms module
Patch17: 0001-Add-xpadneo-bluetooth-hid-driver-module.patch

%define __spec_install_post /usr/lib/rpm/brp-compress || :
%define debug_package %{nil}
BuildRequires: python3-devel
BuildRequires: make
BuildRequires: perl-generators
BuildRequires: perl-interpreter
BuildRequires: openssl-devel
BuildRequires: bison
BuildRequires: flex
BuildRequires: findutils
BuildRequires: git-core
BuildRequires: perl-devel
BuildRequires: openssl
BuildRequires: elfutils-devel
BuildRequires: gawk
BuildRequires: binutils
BuildRequires: m4
BuildRequires: tar
BuildRequires: hostname
BuildRequires: bzip2
BuildRequires: bash
BuildRequires: gzip
BuildRequires: xz
BuildRequires: bc
BuildRequires: diffutils
BuildRequires: redhat-rpm-config
BuildRequires: net-tools
BuildRequires: elfutils
BuildRequires: patch
BuildRequires: rpm-build
BuildRequires: dwarves
BuildRequires: kmod
BuildRequires: libkcapi-hmaccalc
BuildRequires: perl-Carp
BuildRequires: rsync
BuildRequires: grubby
BuildRequires: wget
BuildRequires: gcc
BuildRequires: gcc-c++
%if %{llvm_kbuild}
BuildRequires: llvm
BuildRequires: clang
BuildRequires: lld
%endif
Requires: %{name}-core-%{rpmver} = %{kverstr}
Requires: %{name}-modules-%{rpmver} = %{kverstr}
Provides: %{name}%{_basekver} = %{rpmver}
Provides: kernel-bore-eevdf >= 6.5.7-%{customver}
Provides: kernel-bore >= 6.5.7-%{customver}
Obsoletes: kernel-bore-eevdf <= 6.5.10-%{customver}
Obsoletes: kernel-bore <= 6.5.10-%{customver}

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
Provides: kernel-modules-uname-r = %{kverstr}
Provides: kernel-modules-%{_arch} = %{rpmver}
Provides: kernel-modules-%{rpmver} = %{kverstr}
Provides: %{name}-modules-%{rpmver} = %{kverstr}
Supplements: %{name} = %{rpmver}
Provides: kernel-bore-eevdf-modules >= 6.5.7-%{customver}
Provides: kernel-bore-modules >= 6.5.7-%{customver}
Obsoletes: kernel-bore-eevdf-modules <= 6.5.10-%{customver}
Obsoletes: kernel-bore-modules <= 6.5.10-%{customver}
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
patch -p1 -i %{PATCH16}
patch -p1 -i %{PATCH17}

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
#make %{?_smp_mflags} EXTRAVERSION=-%{krelstr} oldconfig
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

%clean
rm -rf %{buildroot}

%post core
if [ `uname -i` == "x86_64" -o `uname -i` == "i386" ] &&
   [ -f /etc/sysconfig/kernel ]; then
  /bin/sed -r -i -e 's/^DEFAULTKERNEL=kernel-smp$/DEFAULTKERNEL=kernel/' /etc/sysconfig/kernel || exit $?
fi
if [ -x /bin/kernel-install ] && [ -d /boot ]; then
/bin/kernel-install add %{kverstr} /lib/modules/%{kverstr}/vmlinuz || exit $?
fi

%posttrans core
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

%files
