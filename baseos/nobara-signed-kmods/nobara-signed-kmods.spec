# Nobara-signed kernel modules for the Easy Anti-Cheat kernel (kernel-eac)
#
# kernel-eac enforces module signatures and only trusts the Nobara signer and
# its own build key, no MOK: modules built locally by DKMS or akmods don't
# load in it. This package builds the out-of-tree modules Nobara ships for
# specific kernel-eac builds (the normal kernel keeps using DKMS and akmods).
# The repo sync signs them with the Nobara EAC signer (secureboot/sb-resign.sh
# signs only the kmod-*-signed-* packages of this source package, for the
# modules in its KMOD_ALLOWED list), so they are built unsigned here.
#
# One module failing to build fails them all: when a new kernel breaks one,
# patch it or drop it from the lists below until fixed.
#
# The modules go to /lib/modules/<kernel>/updates/nobara/, which depmod
# prefers over the DKMS and akmods builds in extra/: those stay installed and
# keep serving kernels without a signed package.
#
# Build in the COPR project of the kernels, after kernel-eac:
#   linux-nobara-mainline  builds for %%{kernels_mainline}
#   linux-nobara-lts       builds for %%{kernels_lts}
# Locally: --define 'kernels <uname -r> ...'
# Update the kernel lists for every kernel release (keep the installed ones:
# an NVIDIA update needs new modules for every kernel that has the old ones),
# and the module versions with their DKMS/akmod packages.

%global debug_package %{nil}
# Build flags come from the kernel, not rpm (rpm's LDFLAGS break the NVIDIA link)
%undefine _auto_set_build_flags

%global kernels_mainline 7.3.1-202.eac.nobara%{?dist}.%{_target_cpu}
%global kernels_lts      6.18.60-200.lts.eac.nobara%{?dist}.%{_target_cpu}
%if "%{?copr_projectname}" == "linux-nobara-lts"
%{!?kernels:%global kernels %{kernels_lts}}
%else
%{!?kernels:%global kernels %{kernels_mainline}}
%endif

# Module versions, kept in step with their DKMS/akmod packages. v4l2loopback
# is not here: the Nobara kernels build it in-tree, signed with the kernel.
%global nvidia_prod_version   595.112.07
%global nvidia_nf_version     615.78.08
%global nvidia_epoch          3
%global xone_version          0.5.8
# Same fork commit as baseos/xone (xone_mtnet: new dongle on MediaTek's firmware, wake on wireless)
%global xone_commit           a8781c1e1ed53509fb117a9461ebf2f236347b47
%global xpad_noone_commit     c3d1610
%global openrazer_version     3.12.4
# Terra's dkms-/akmod-hid-tmff2, -hid-fanatecff and -new-lg4ff
%global tmff2_commit          d890a93105a0aa52028ac49282fa1b579e12566e
%global tmff2_version         0.83^20260826git.d890a93
%global tminit_commit         8c4547288a6c182ed4ff131e36f710f11a76c4a9
%global fanatecff_commit      54fb2988b68382fbe10dc57132175f27f1681ca1
%global fanatecff_version     0.2.3^20261102git.54fb298
%global lg4ff_commit          2092db19f7b40854e0427a1b2e39eda9f8d0c3cd
%global lg4ff_version         0.5.0^20250528git.2092db1
# Terra's dkms-/akmod-nct6687d
%global nct6687d_commit       25421f527f47007d95c310cfa6c2aa97c42edd81
%global nct6687d_version      1.0^20261102git.25421f5
# baseos/displaylink (evdi) and baseos/dkms-r8125
%global evdi_version          1.15.1
%global r8125_version         9.018.00
# OpenZFS's zfs-dkms (its own Fedora repository). LTS kernels only: OpenZFS
# releases lag behind new mainline kernels
%global zfs_version           2.4.4

Name:           nobara-signed-kmods
Version:        1
Release:        6%{?dist}
Summary:        Nobara-signed kernel modules for the Easy Anti-Cheat kernel
License:        GPL-2.0-only AND GPL-2.0-or-later AND MIT AND CDDL-1.0 AND NVIDIA License
URL:            https://nobaraproject.org
ExclusiveArch:  x86_64

Source0:        https://github.com/NVIDIA/open-gpu-kernel-modules/archive/refs/tags/%{nvidia_prod_version}.tar.gz#/open-gpu-kernel-modules-%{nvidia_prod_version}.tar.gz
Source1:        https://github.com/NVIDIA/open-gpu-kernel-modules/archive/refs/tags/%{nvidia_nf_version}.tar.gz#/open-gpu-kernel-modules-%{nvidia_nf_version}.tar.gz
Source2:        https://github.com/GloriousEggroll/xone/archive/%{xone_commit}/xone-%{xone_commit}.tar.gz
Source3:        https://github.com/medusalix/xpad-noone/archive/%{xpad_noone_commit}/xpad-noone-%{xpad_noone_commit}.tar.gz
Source5:        https://github.com/openrazer/openrazer/releases/download/v%{openrazer_version}/openrazer-%{openrazer_version}.tar.xz
Source6:        https://github.com/Kimplul/hid-tmff2/archive/%{tmff2_commit}.tar.gz#/hid-tmff2-%{tmff2_commit}.tar.gz
Source7:        https://github.com/Kimplul/hid-tminit/archive/%{tminit_commit}.tar.gz#/hid-tminit-%{tminit_commit}.tar.gz
Source8:        https://github.com/gotzl/hid-fanatecff/archive/%{fanatecff_commit}.tar.gz#/hid-fanatecff-%{fanatecff_commit}.tar.gz
Source9:        https://github.com/berarma/new-lg4ff/archive/%{lg4ff_commit}.tar.gz#/new-lg4ff-%{lg4ff_commit}.tar.gz
Source10:       https://github.com/DisplayLink/evdi/archive/v%{evdi_version}.tar.gz#/evdi-%{evdi_version}.tar.gz
Source13:       https://github.com/awesometic/realtek-r8125-dkms/archive/refs/tags/%{r8125_version}-1.tar.gz#/realtek-r8125-dkms-%{r8125_version}-1.tar.gz
Source14:       https://github.com/Fred78290/nct6687d/archive/%{nct6687d_commit}.tar.gz#/nct6687d-%{nct6687d_commit}.tar.gz
# SHA-256 2a3c70d55a37cc71618a95a60e81ad66530201eb118d37741dc92efcf848c8b1, as
# in OpenZFS's signed zfs-%%{zfs_version}.sha256.asc
Source15:       https://github.com/openzfs/zfs/releases/download/zfs-%{zfs_version}/zfs-%{zfs_version}.tar.gz

# Same patches as nvidia/prod/<version>/kmod
Patch100:       nvidia-prod-0001-Add-IBT-support.patch
Patch101:       nvidia-prod-0002-fix-dsc-correct-RC-parameter-tables-to-match-VESA-DS.patch
Patch102:       nvidia-prod-0003-fix-dsc-use-bits_per_component-for-flatnessDetThresh.patch
Patch103:       nvidia-prod-0004-fix-dp-add-Bigscreen-Beyond-VR-headset-to-WAR-databa.patch
Patch104:       nvidia-prod-0005-nvidia-control-tunneled-PCIe-speed-during-active-epochs.patch
Patch105:       nvidia-prod-0006-add-CEC-support-via-DP-to-HDMI-dongles.patch
# Same patches as nvidia/new-feature/<version>/kmod
Patch200:       nvidia-nf-0001-nvidia-control-tunneled-PCIe-speed-during-active-epochs.patch
Patch201:       nvidia-nf-0002-add-CEC-support-via-DP-to-HDMI-dongles.patch
# Same patches as baseos/xone, baseos/xpad-noone and baseos/openrazer
Patch300:       xone-0002-fix-wired-usb-reset-race-condition.patch
Patch400:       xpad-noone-8.patch
Patch401:       xpad-noone-9.patch
Patch500:       openrazer-device-support.patch
Patch501:       openrazer-lts-reset-resume.patch
# Drop rtltool (the SIOCRTLTOOL ioctl): it gives root raw writes to the NIC's
# PCI config space, MMIO, PHY, EEPROM and OCP registers, which lockdown
# exists to remove. It is also the only way to enable the DASH firmware
# buffer ioctls (rtk_enable_diag), which stay disabled without it
Patch600:       r8125-remove-rtltool.patch

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  elfutils-libelf-devel
BuildRequires:  kmod
BuildRequires:  hostname
%{lua:
for kver in rpm.expand("%{kernels}"):gmatch("%S+") do
    print("BuildRequires:  kernel-devel-uname-r = " .. kver .. "\n")
end
}

%description
Out-of-tree kernel modules built for specific Nobara Easy Anti-Cheat kernels
(kernel-eac), signed by the Nobara Secure Boot signer when the repository is
synced: the only out-of-tree modules kernel-eac loads.

%{lua:
-- One subpackage per module and kernel. The modules are installed in
-- updates/nobara/<dir>, which depmod prefers over DKMS and akmods in extra/.
-- lts_only: built for the LTS kernels only.
local modules = {
  { name = "nvidia-prod", dir = "nvidia-prod", epoch = rpm.expand("%{nvidia_epoch}"),
    version = rpm.expand("%{nvidia_prod_version}"),
    summary = "NVIDIA %{nvidia_prod_version} (production branch) kernel modules",
    extra = "Requires:       nvidia-kmod-common = %{nvidia_epoch}:%{nvidia_prod_version}\n" ..
            "Provides:       nvidia-kmod = %{nvidia_epoch}:%{nvidia_prod_version}\n" ..
            "Provides:       nvidia-signed-kmod-KVER = %{nvidia_epoch}:%{nvidia_prod_version}\n" ..
            "Conflicts:      kmod-nvidia-nf-signed-KVER\n" },
  { name = "nvidia-nf", dir = "nvidia-nf", epoch = rpm.expand("%{nvidia_epoch}"),
    version = rpm.expand("%{nvidia_nf_version}"),
    summary = "NVIDIA %{nvidia_nf_version} (new feature branch) kernel modules",
    extra = "Requires:       nvidia-kmod-common = %{nvidia_epoch}:%{nvidia_nf_version}\n" ..
            "Provides:       nvidia-kmod = %{nvidia_epoch}:%{nvidia_nf_version}\n" ..
            "Provides:       nvidia-signed-kmod-KVER = %{nvidia_epoch}:%{nvidia_nf_version}\n" ..
            "Conflicts:      kmod-nvidia-prod-signed-KVER\n" },
  { name = "xone", dir = "xone", version = rpm.expand("%{xone_version}"),
    summary = "xone (Xbox One and Series X|S accessories) kernel modules",
    extra = "Requires:       xone >= %{xone_version}-4\n" },
  { name = "xpad-noone", dir = "xpad-noone", version = "1",
    summary = "xpad-noone (Xbox 360 controller) kernel module",
    extra = "Requires:       xpad-noone\n" },
  { name = "openrazer", dir = "openrazer", version = rpm.expand("%{openrazer_version}"),
    summary = "OpenRazer (Razer devices) kernel modules",
    extra = "Requires:       openrazer-kernel-modules-dkms\n" },
  { name = "hid-tmff2", dir = "hid-tmff2", version = rpm.expand("%{tmff2_version}"),
    summary = "hid-tmff2 (Thrustmaster wheels force feedback) kernel modules",
    extra = "Requires:       hid-tmff2\n" },
  { name = "hid-fanatecff", dir = "hid-fanatecff", version = rpm.expand("%{fanatecff_version}"),
    summary = "hid-fanatecff (Fanatec wheels and pedals) kernel module",
    extra = "Requires:       hid-fanatecff\n" },
  { name = "new-lg4ff", dir = "new-lg4ff", version = rpm.expand("%{lg4ff_version}"),
    summary = "new-lg4ff (Logitech wheels force feedback) kernel module",
    extra = "Requires:       new-lg4ff\n" },
  { name = "evdi", dir = "evdi", version = rpm.expand("%{evdi_version}"),
    summary = "evdi (DisplayLink) kernel module",
    extra = "Requires:       displaylink = %{evdi_version}\n" },
  { name = "r8125", dir = "r8125", version = rpm.expand("%{r8125_version}"),
    summary = "Realtek r8125 (RTL8125 2.5GbE) kernel module",
    extra = "Requires:       dkms-r8125\n" },
  -- nct6687d has the nct6683 blacklist and the modules-load.d entry
  { name = "nct6687d", dir = "nct6687d", version = rpm.expand("%{nct6687d_version}"),
    summary = "nct6687d (Nuvoton NCT6687-R sensors) kernel module",
    extra = "Requires:       nct6687d\n" },
  { name = "zfs", dir = "zfs", version = rpm.expand("%{zfs_version}"), lts_only = true,
    summary = "OpenZFS (zfs and spl) kernel modules",
    extra = "Requires:       zfs-dkms\n" },
}
for kver in rpm.expand("%{kernels}"):gmatch("%S+") do
  for _, m in ipairs(modules) do
    if m.lts_only and not kver:find(".lts.", 1, true) then goto continue end
    local pkg = "kmod-" .. m.name .. "-signed-" .. kver
    local extra = m.extra:gsub("KVER", kver)
    print(rpm.expand(
      "%package -n " .. pkg .. "\n" ..
      "Summary:        " .. m.summary .. " for kernel " .. kver .. "\n" ..
      (m.epoch and ("Epoch:          " .. m.epoch .. "\n") or "") ..
      "Version:        " .. m.version .. "\n" ..
      "Requires:       kernel-uname-r = " .. kver .. "\n" ..
      "Requires(post): kmod\n" ..
      "Requires(postun): kmod\n" ..
      extra ..
      "%description -n " .. pkg .. "\n" ..
      m.summary .. " for the Easy Anti-Cheat kernel " .. kver .. ", signed by\n" ..
      "Nobara: the only out-of-tree modules that kernel loads.\n" ..
      "%post -n " .. pkg .. "\n" ..
      "/usr/sbin/depmod -a " .. kver .. " || :\n" ..
      "%postun -n " .. pkg .. "\n" ..
      "[ -d /lib/modules/" .. kver .. "/kernel ] && /usr/sbin/depmod -a " .. kver .. " || :\n" ..
      "%files -n " .. pkg .. "\n" ..
      "%dir /lib/modules/" .. kver .. "/updates/nobara\n" ..
      "/lib/modules/" .. kver .. "/updates/nobara/" .. m.dir .. "\n"))
    ::continue::
  end
end
}

%prep
%setup -q -c -T
mkdir nvidia-prod nvidia-nf xone xpad-noone openrazer hid-tmff2 hid-fanatecff new-lg4ff evdi r8125 nct6687d zfs
tar -xf %{SOURCE0} -C nvidia-prod --strip-components=1
tar -xf %{SOURCE1} -C nvidia-nf --strip-components=1
tar -xf %{SOURCE2} -C xone --strip-components=1
tar -xf %{SOURCE3} -C xpad-noone --strip-components=1
tar -xf %{SOURCE5} -C openrazer --strip-components=1
tar -xf %{SOURCE6} -C hid-tmff2 --strip-components=1
rm -rf hid-tmff2/deps/hid-tminit
mkdir -p hid-tmff2/deps/hid-tminit
tar -xf %{SOURCE7} -C hid-tmff2/deps/hid-tminit --strip-components=1
tar -xf %{SOURCE8} -C hid-fanatecff --strip-components=1
tar -xf %{SOURCE9} -C new-lg4ff --strip-components=1
tar -xf %{SOURCE10} -C evdi --strip-components=1
tar -xf %{SOURCE13} -C r8125 --strip-components=1
tar -xf %{SOURCE14} -C nct6687d --strip-components=1
tar -xf %{SOURCE15} -C zfs --strip-components=1
# The same options as rpm's %%patch, so the patches apply as in their own specs
apply() { %{__patch} -p1 -s --fuzz=2 --no-backup-if-mismatch -f -d "$1" -i "$2"; }
for p in %{P:100} %{P:101} %{P:102} %{P:103} %{P:104} %{P:105}; do apply nvidia-prod $p; done
for p in %{P:200} %{P:201}; do apply nvidia-nf $p; done
apply xone %{P:300}
apply xpad-noone %{P:400}
apply xpad-noone %{P:401}
apply openrazer %{P:500}
apply openrazer %{P:501}
apply r8125 %{P:600}

%build
# The modules built for a kernel (zfs: LTS kernels only)
modules_for() {
    echo nvidia-prod nvidia-nf xone xpad-noone openrazer hid-tmff2 hid-fanatecff new-lg4ff evdi r8125 nct6687d
    case "$1" in *.lts.*) echo zfs ;; esac
}
for kver in %{kernels}; do
    kdir=/usr/src/kernels/$kver
    for m in $(modules_for $kver); do
        rm -rf "build-$kver/$m"
        mkdir -p "build-$kver"
        cp -a "$m" "build-$kver/$m"
    done
    pushd "build-$kver"
    for m in nvidia-prod nvidia-nf; do
        make -C $m %{?_smp_mflags} SYSSRC=$kdir KERNEL_UNAME=$kver modules
    done
    make %{?_smp_mflags} -C $kdir M=$PWD/xone modules
    make %{?_smp_mflags} -C $kdir M=$PWD/xpad-noone modules
    make %{?_smp_mflags} -C $kdir M=$PWD/openrazer/driver modules
    make %{?_smp_mflags} -C hid-tmff2 KDIR=$kdir
    make %{?_smp_mflags} -C $kdir M=$PWD/hid-fanatecff modules
    make %{?_smp_mflags} -C $kdir M=$PWD/new-lg4ff modules
    make %{?_smp_mflags} -C $kdir M=$PWD/evdi/module modules
    make %{?_smp_mflags} -C $kdir M=$PWD/r8125/src modules
    make %{?_smp_mflags} -C $kdir M=$PWD/nct6687d modules
    if [ -d zfs ]; then
        # As zfs-dkms (scripts/dkms.mkconf): only the kernel modules
        pushd zfs
        ./configure --disable-dependency-tracking --prefix=/usr --with-config=kernel \
            --with-linux=$kdir --with-linux-obj=$kdir
        make %{?_smp_mflags}
        popd
    fi
    popd
done

%install
for kver in %{kernels}; do
    b="build-$kver"
    d=%{buildroot}/lib/modules/$kver/updates/nobara
    install -d $d/nvidia-prod $d/nvidia-nf $d/xone $d/xpad-noone $d/openrazer \
        $d/hid-tmff2 $d/hid-fanatecff $d/new-lg4ff $d/evdi $d/r8125 $d/nct6687d
    install -m 0644 $b/nvidia-prod/kernel-open/*.ko $d/nvidia-prod/
    install -m 0644 $b/nvidia-nf/kernel-open/*.ko $d/nvidia-nf/
    install -m 0644 $b/xone/*.ko $d/xone/
    install -m 0644 $b/xpad-noone/*.ko $d/xpad-noone/
    install -m 0644 $b/openrazer/driver/*.ko $d/openrazer/
    install -m 0644 $b/hid-tmff2/hid-tmff-new.ko $b/hid-tmff2/deps/hid-tminit/*.ko $d/hid-tmff2/
    install -m 0644 $b/hid-fanatecff/hid-fanatec.ko $d/hid-fanatecff/
    # As dkms-new-lg4ff: it replaces the in-kernel hid-logitech
    install -m 0644 $b/new-lg4ff/hid-logitech-new.ko $d/new-lg4ff/hid-logitech.ko
    install -m 0644 $b/evdi/module/evdi.ko $d/evdi/
    install -m 0644 $b/r8125/src/r8125.ko $d/r8125/
    install -m 0644 $b/nct6687d/nct6687.ko $d/nct6687d/
    if [ -d $b/zfs ]; then
        install -d $d/zfs
        install -m 0644 $b/zfs/module/zfs.ko $b/zfs/module/spl.ko $d/zfs/
    fi
done
# Unsigned and uncompressed: secureboot/sb-resign.sh signs them at repo sync
find %{buildroot}/lib/modules -name '*.ko' -exec strip --strip-debug {} +

%changelog
* Tue Nov 10 2026 GloriousEggroll <gloriouseggroll@gmail.com> - 1-6
- xone: build from the GloriousEggroll/xone fork (same commit as baseos/xone
  0.5.8-4), which adds xone_mtnet with wake on wireless and moves the new
  dongle (045e:02fe) off Microsoft's firmware; require xone >= 0.5.8-4 for
  its udev rule and modprobe changes

* Thu Nov 05 2026 GloriousEggroll <gloriouseggroll@gmail.com> - 1-5
- r8125: remove rtltool (the SIOCRTLTOOL ioctl), which gives root raw access
  to the NIC's PCI config space and registers

* Wed Nov 04 2026 GloriousEggroll <gloriouseggroll@gmail.com> - 1-4
- Build for kernel-eac 7.3.1-202 and 6.18.60-200, the first signed by the
  Nobara EAC hierarchy; sb-resign.sh signs the modules with the Nobara EAC signer
- Add zfs %{zfs_version} (as OpenZFS's zfs-dkms), for the LTS kernels only

* Mon Nov 02 2026 GloriousEggroll <gloriouseggroll@gmail.com> - 1-3
- Build for kernel-eac 7.3.1-201 and 6.18.55-202
- Add nct6687d (as Terra's DKMS/akmod package)

* Mon Nov 02 2026 GloriousEggroll <gloriouseggroll@gmail.com> - 1-2
- Add hid-tmff2, hid-fanatecff and new-lg4ff (as Terra's DKMS/akmod packages),
  evdi (DisplayLink) and r8125

* Mon Nov 02 2026 GloriousEggroll <gloriouseggroll@gmail.com> - 1-1
- Initial package: NVIDIA %{nvidia_prod_version} and %{nvidia_nf_version}, xone,
  xpad-noone and OpenRazer modules for the Easy Anti-Cheat kernels (kernel-eac),
  signed at repo sync
