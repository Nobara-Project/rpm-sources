%global _default_patch_fuzz 2

%ifnarch s390x
%global with_hardware 1
%global with_kmsro 1
%global with_nvk 1
%global with_vulkan_hw 1
%global with_va 1
%global with_spirv_tools 1
%if !0%{?rhel}
%global with_opencl 1
%endif
%global base_vulkan ,amd
%endif

%if 0%{?with_vulkan_hw}
%global with_nvk 1
%global vendor_nvk_crates 1
%endif

%ifarch %{ix86} x86_64
%global with_crocus 1
%global with_i915   1
%global with_iris   1
%global platform_vulkan ,intel,intel_hasvk
%endif

%ifarch aarch64
%if !0%{?rhel}
%global with_etnaviv   1
%global with_lima      1
%global with_vc4       1
%global with_v3d       1
%endif
%global with_crocus 1
%global with_i915   1
%global with_freedreno 1
%global with_kmsro     1
%global with_panfrost  1
%global with_tegra     1
%global platform_vulkan ,broadcom,freedreno,panfrost,intel,intel_hasvk
%endif

%ifnarch s390x
%if !0%{?rhel}
%global with_r300 1
%global with_r600 1
%endif
%global with_radeonsi 1
%global with_vmware 1
%endif

%ifarch %{valgrind_arches}
%bcond_without valgrind
%else
%bcond_with valgrind
%endif

%global with_vulkan_overlay 1

%global vulkan_drivers swrast%{?base_vulkan}%{?platform_vulkan}%{?with_nvk:,nouveau}

Name:           mesa-vulkan-drivers-freeworld
Summary:        The mesa graphics vulkan driver stack.
%global ver 25.3.2
Version:        %{lua:ver = string.gsub(rpm.expand("%{ver}"), "-", "~"); print(ver)}
Release:        %autorelease -b2
License:        MIT
URL:            http://www.mesa3d.org

Source0:        https://archive.mesa3d.org/mesa-%{ver}.tar.xz
# src/gallium/auxiliary/postprocess/pp_mlaa* have an ... interestingly worded license.
# Source1 contains email correspondence clarifying the license terms.
# Fedora opts to ignore the optional part of clause 2 and treat that code as 2 clause BSD.
Source1:        Mesa-MLAA-License-Clarification-Email.txt

%global rust_paste_ver 1.0.15
%global rust_proc_macro2_ver 1.0.101
%global rust_quote_ver 1.0.40
%global rust_syn_ver 2.0.106
%global rust_unicode_ident_ver 1.0.18
%global rustc_hash_ver 2.1.1
Source10:       https://crates.io/api/v1/crates/paste/%{rust_paste_ver}/download#/paste-%{rust_paste_ver}.tar.gz
Source11:       https://crates.io/api/v1/crates/proc-macro2/%{rust_proc_macro2_ver}/download#/proc-macro2-%{rust_proc_macro2_ver}.tar.gz
Source12:       https://crates.io/api/v1/crates/quote/%{rust_quote_ver}/download#/quote-%{rust_quote_ver}.tar.gz
Source13:       https://crates.io/api/v1/crates/syn/%{rust_syn_ver}/download#/syn-%{rust_syn_ver}.tar.gz
Source14:       https://crates.io/api/v1/crates/unicode-ident/%{rust_unicode_ident_ver}/download#/unicode-ident-%{rust_unicode_ident_ver}.tar.gz
Source15:       https://crates.io/api/v1/crates/rustc-hash/%{rustc_hash_ver}/download#/rustc-hash-%{rustc_hash_ver}.tar.gz

# SteamVR Fix
Patch20:	https://gitlab.freedesktop.org/mesa/mesa/-/merge_requests/38987.patch

# https://gitlab.com/evlaV/mesa/
Patch30:        valve.patch

BuildRequires:  meson >= 1.3.0
BuildRequires:  cbindgen
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  gettext
%if 0%{?with_hardware}
BuildRequires:  kernel-headers
%endif
# We only check for the minimum version of pkgconfig(libdrm) needed so that the
# SRPMs for each arch still have the same build dependencies. See:
# https://bugzilla.redhat.com/show_bug.cgi?id=1859515
BuildRequires:  pkgconfig(libdrm) >= 2.4.122
BuildRequires:  pkgconfig(libunwind)
BuildRequires:  pkgconfig(expat)
BuildRequires:  pkgconfig(zlib) >= 1.2.3
BuildRequires:  pkgconfig(libzstd)
BuildRequires:  pkgconfig(libdisplay-info)
BuildRequires:  pkgconfig(libselinux)
BuildRequires:  pkgconfig(wayland-scanner)
BuildRequires:  pkgconfig(wayland-protocols) >= 1.8
BuildRequires:  pkgconfig(wayland-client) >= 1.11
BuildRequires:  pkgconfig(wayland-server) >= 1.11
BuildRequires:  pkgconfig(wayland-egl-backend) >= 3
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xdamage) >= 1.1
BuildRequires:  pkgconfig(xfixes)
BuildRequires:  pkgconfig(xcb-glx) >= 1.8.1
BuildRequires:  pkgconfig(xxf86vm)
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(x11-xcb)
BuildRequires:  pkgconfig(xcb-dri2) >= 1.8
BuildRequires:  pkgconfig(xcb-dri3)
BuildRequires:  pkgconfig(xcb-present)
BuildRequires:  pkgconfig(xcb-sync)
BuildRequires:  pkgconfig(xshmfence) >= 1.1
BuildRequires:  pkgconfig(dri2proto) >= 2.8
BuildRequires:  pkgconfig(glproto) >= 1.4.14
BuildRequires:  pkgconfig(xcb-xfixes)
BuildRequires:  pkgconfig(xcb-randr)
BuildRequires:  pkgconfig(xrandr) >= 1.3
BuildRequires:  python3-pycparser
BuildRequires:  python3-pyyaml
BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  lm_sensors-devel
%if 0%{?with_va}
BuildRequires:  pkgconfig(libva) >= 0.38.0
%endif
BuildRequires:  pkgconfig(libelf)
BuildRequires:  pkgconfig(libglvnd) >= 1.3.2
BuildRequires:  llvm-devel >= 7.0.0
%if 0%{?with_opencl} || 0%{?with_nvk}
BuildRequires:  clang-devel
BuildRequires:  bindgen
BuildRequires:  rust-packaging
BuildRequires:  pkgconfig(libclc)
BuildRequires:  pkgconfig(SPIRV-Tools)
BuildRequires:  pkgconfig(LLVMSPIRVLib)
%endif
%if 0%{?with_nvk}
BuildRequires:  (crate(paste) >= 1.0.14 with crate(paste) < 2)
BuildRequires:  (crate(proc-macro2) >= 1.0.56 with crate(proc-macro2) < 2)
BuildRequires:  (crate(quote) >= 1.0.25 with crate(quote) < 2)
BuildRequires:  (crate(syn/clone-impls) >= 2.0.15 with crate(syn/clone-impls) < 3)
BuildRequires:  (crate(unicode-ident) >= 1.0.6 with crate(unicode-ident) < 2)
BuildRequires:  (crate(rustc-hash) >= 2.1.1 with crate(rustc-hash) < 3)
BuildRequires:  rustfmt
%endif
%if %{with valgrind}
BuildRequires:  pkgconfig(valgrind)
%endif
BuildRequires:  python3-devel
BuildRequires:  python3-mako
BuildRequires:  vulkan-headers
BuildRequires:  glslang
%if 0%{?with_vulkan_hw}
BuildRequires:  pkgconfig(vulkan)
%endif
Requires:       vulkan%{_isa}
Obsoletes: mesa-vulkan-drivers-vulkan-devel
Obsoletes: mesa-vulkan-devel
Obsoletes:      mesa-omx-drivers < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       mesa-vulkan-drivers
Provides:       mesa-vulkan-drivers%{?_isa}
Obsoletes:      mesa-vulkan-drivers
%description
%{summary}.


%prep
%autosetup -n mesa-%{ver} -p1
cp %{SOURCE1} docs/

mkdir subprojects/packagecache/
tar -xvf %{SOURCE10} -C subprojects/packagecache/
tar -xvf %{SOURCE11} -C subprojects/packagecache/
tar -xvf %{SOURCE12} -C subprojects/packagecache/
tar -xvf %{SOURCE13} -C subprojects/packagecache/
tar -xvf %{SOURCE14} -C subprojects/packagecache/
tar -xvf %{SOURCE15} -C subprojects/packagecache/
for d in subprojects/packagecache/*-*; do
    echo '{"files":{}}' > $d/.cargo-checksum.json
done

%if 0%{?with_nvk}
cat > Cargo.toml <<_EOF
[package]
name = "mesa"
version = "%{ver}"
edition = "2021"

[lib]
path = "src/nouveau/nil/lib.rs"

# only direct dependencies need to be listed here
[dependencies]
paste = "$(grep ^directory subprojects/paste*.wrap | sed 's|.*-||')"
syn = { version = "$(grep ^directory subprojects/syn*.wrap | sed 's|.*-||')", features = ["clone-impls"] }
rustc-hash = "$(grep ^directory subprojects/rustc-hash*.wrap | sed 's|.*-||')"
_EOF
%if 0%{?vendor_nvk_crates}
%cargo_prep -v subprojects/packagecache
%else
%cargo_prep

%generate_buildrequires
%cargo_generate_buildrequires
%endif
%endif

%build
# ensure standard Rust compiler flags are set
export RUSTFLAGS="%build_rustflags"

%if 0%{?with_nvk}
# So... Meson can't actually find them without tweaks
%if !0%{?vendor_nvk_crates}
export MESON_PACKAGE_CACHE_DIR="%{cargo_registry}/"
%endif
rewrite_wrap_file() {
   sed -e "/source.*/d" -e "s/^directory = ${1}-.*/directory = $(basename ${MESON_PACKAGE_CACHE_DIR:-subprojects/packagecache}/${1}-*)/" -i subprojects/${1}*.wrap
}

rewrite_wrap_file proc-macro2
rewrite_wrap_file quote
rewrite_wrap_file syn
rewrite_wrap_file unicode-ident
rewrite_wrap_file paste
rewrite_wrap_file rustc-hash
%endif

# We've gotten a report that enabling LTO for mesa breaks some games. See
# https://bugzilla.redhat.com/show_bug.cgi?id=1862771 for details.
# Disable LTO for now
%define _lto_cflags %{nil}

# notes:
# -Dlmsensors=enabled \ -- required for vulkan overlay
# -Dxlib-lease=enabled \ -- required for VR extension: VK_EXT_acquire_xlib_display
# %dir %{_datadir}/drirc.d/

%meson \
  -Dplatforms=x11,wayland \
  -Dvideo-codecs=all \
%if 0%{?with_hardware}
  -Dgallium-drivers=softpipe,llvmpipe,virgl,nouveau%{?with_r300:,r300}%{?with_crocus:,crocus}%{?with_i915:,i915}%{?with_iris:,iris}%{?with_vmware:,svga}%{?with_radeonsi:,radeonsi}%{?with_r600:,r600}%{?with_freedreno:,freedreno}%{?with_etnaviv:,etnaviv}%{?with_tegra:,tegra}%{?with_vc4:,vc4}%{?with_v3d:,v3d}%{?with_lima:,lima}%{?with_panfrost:,panfrost}%{?with_vulkan_hw:,zink} \
%else
  -Dgallium-drivers=softpipe,llvmpipe,virgl \
%endif
  -Dgallium-mediafoundation=disabled \
  -Dgallium-va=%{?with_va:enabled}%{!?with_va:disabled} \
%if 0%{?with_opencl}
  -Dgallium-rusticl=true \
%endif
  -Dvulkan-drivers=%{?vulkan_drivers} \
  -Dvulkan-layers=device-select,anti-lag \
  -Dgles1=enabled \
  -Dgles2=enabled \
  -Dopengl=true \
  -Dgbm=enabled \
  -Dglx=dri \
  -Degl=enabled \
  -Dglvnd=enabled \
%ifnarch aarch64 x86_64
  -Dintel-rt=disabled \
%endif
  -Dmicrosoft-clc=disabled \
  -Dllvm=enabled \
  -Dshared-llvm=enabled \
  -Dvalgrind=%{?with_valgrind:enabled}%{!?with_valgrind:disabled} \
  -Dbuild-tests=false \
  -Dandroid-libbacktrace=disabled \
%ifarch %{ix86}
  -Dglx-read-only-text=true \
%endif
  -Dspirv-tools=%{?with_spirv_tools:enabled}%{!?with_spirv_tools:disabled} \
  -Dlmsensors=enabled \
  -Dxlib-lease=enabled \
  %{nil}
%meson_build

%install
%meson_install

# likewise glvnd
rm -vf %{buildroot}%{_libdir}/libGLX_mesa.so
rm -vf %{buildroot}%{_libdir}/libEGL_mesa.so
# XXX can we just not build this
rm -vf %{buildroot}%{_libdir}/libGLES*

# glvnd needs a default provider for indirect rendering where it cannot
# determine the vendor
ln -s %{_libdir}/libGLX_mesa.so.0 %{buildroot}%{_libdir}/libGLX_system.so.0

# this keeps breaking, check it early.  note that the exit from eu-ftr is odd.
pushd %{buildroot}%{_libdir}
for i in libGL*.so ; do
    sleep 1
    eu-findtextrel $i && exit 1
done
popd

# cleanup unused
rm -Rf %{buildroot}%{_libdir}/libGLX_mesa.so.0*
rm -Rf %{buildroot}%{_libdir}/libGLX_system.so.0*
rm -Rf %{buildroot}%{_includedir}/GL/
rm -Rf %{buildroot}%{_libdir}/pkgconfig/dri.pc
rm -Rf %{buildroot}%{_libdir}/libglapi.so
rm -Rf %{buildroot}%{_datadir}/glvnd/egl_vendor.d/50_mesa*.json
rm -Rf %{buildroot}%{_libdir}/libEGL_mesa.so.0*
rm -Rf %{buildroot}%{_includedir}/EGL/
rm -Rf %{buildroot}%{_libdir}/libglapi.so.0
rm -Rf %{buildroot}%{_libdir}/libglapi.so.0.*
rm -Rf %{buildroot}%{_libdir}/libgallium-*.so
rm -Rf %{buildroot}%{_libdir}/libgbm.so.1
rm -Rf %{buildroot}%{_libdir}/libgbm.so.1.*
rm -Rf %{buildroot}%{_libdir}/libgbm.so
rm -Rf %{buildroot}%{_includedir}/gbm.h
rm -Rf %{buildroot}%{_includedir}/gbm_backend_abi.h
rm -Rf %{buildroot}%{_libdir}/pkgconfig/gbm.pc
rm -Rf %{buildroot}%{_libdir}/libxatracker.so.2
rm -Rf %{buildroot}%{_libdir}/libxatracker.so.2.*
rm -Rf %{buildroot}%{_libdir}/libxatracker.so
rm -Rf %{buildroot}%{_includedir}/xa_tracker.h
rm -Rf %{buildroot}%{_includedir}/xa_composite.h
rm -Rf %{buildroot}%{_includedir}/xa_context.h
rm -Rf %{buildroot}%{_libdir}/pkgconfig/xatracker.pc
rm -Rf %{buildroot}%{_libdir}/libMesaOpenCL.so.*
rm -Rf %{buildroot}%{_sysconfdir}/OpenCL/vendors/mesa.icd
rm -Rf %{buildroot}%{_libdir}/libMesaOpenCL.so
rm -Rf %{buildroot}%{_libdir}/d3d/
rm -Rf %{buildroot}%{_libdir}/pkgconfig/d3d.pc
rm -Rf %{buildroot}%{_includedir}/d3dadapter/
rm -Rf %{buildroot}%{_libdir}/d3d/*.so
rm -Rf %{buildroot}%{_datadir}/drirc.d/00-mesa-defaults.conf
rm -Rf %{buildroot}%{_libdir}/dri/radeon_dri.so
rm -Rf %{buildroot}%{_libdir}/dri/r200_dri.so
rm -Rf %{buildroot}%{_libdir}/dri/nouveau_vieux_dri.so
rm -Rf %{buildroot}%{_libdir}/dri/r300_dri.so
rm -Rf %{buildroot}%{_libdir}/dri/r600_dri.so
rm -Rf %{buildroot}%{_libdir}/dri/radeonsi_dri.so
rm -Rf %{buildroot}%{_libdir}/dri/i830_dri.so
rm -Rf %{buildroot}%{_libdir}/dri/i915_dri.so
rm -Rf %{buildroot}%{_libdir}/dri/i965_dri.so
rm -Rf %{buildroot}%{_libdir}/dri/vc4_dri.so
rm -Rf %{buildroot}%{_libdir}/dri/kgsl_dri.so
rm -Rf %{buildroot}%{_libdir}/dri/msm_dri.so
rm -Rf %{buildroot}%{_libdir}/dri/etnaviv_dri.so
rm -Rf %{buildroot}%{_libdir}/dri/imx-drm_dri.so
rm -Rf %{buildroot}%{_libdir}/dri/tegra_dri.so
rm -Rf %{buildroot}%{_libdir}/dri/lima_dri.so
rm -Rf %{buildroot}%{_libdir}/dri/panfrost_dri.so
rm -Rf %{buildroot}%{_libdir}/dri/nouveau_dri.so
rm -Rf %{buildroot}%{_libdir}/dri/vmwgfx_dri.so
rm -Rf %{buildroot}%{_libdir}/dri/nouveau_drv_video.so
rm -Rf %{buildroot}%{_libdir}/dri/r600_drv_video.so
rm -Rf %{buildroot}%{_libdir}/dri/radeonsi_drv_video.so
rm -Rf %{buildroot}%{_libdir}/dri/iris_dri.so
rm -Rf %{buildroot}%{_libdir}/dri/zink_dri.so
rm -Rf %{buildroot}%{_libdir}/gallium-pipe
rm -Rf %{buildroot}%{_libdir}/gallium-pipe/*.so
rm -Rf %{buildroot}%{_libdir}/dri/armada-drm_dri.so
rm -Rf %{buildroot}%{_libdir}/dri/exynos_dri.so
rm -Rf %{buildroot}%{_libdir}/dri/hx8357d_dri.so
rm -Rf %{buildroot}%{_libdir}/dri/ili9225_dri.so
rm -Rf %{buildroot}%{_libdir}/dri/ili9341_dri.so
rm -Rf %{buildroot}%{_libdir}/dri/meson_dri.so
rm -Rf %{buildroot}%{_libdir}/dri/mi0283qt_dri.so
rm -Rf %{buildroot}%{_libdir}/dri/pl111_dri.so
rm -Rf %{buildroot}%{_libdir}/dri/repaper_dri.so
rm -Rf %{buildroot}%{_libdir}/dri/rockchip_dri.so
rm -Rf %{buildroot}%{_libdir}/dri/st7586_dri.so
rm -Rf %{buildroot}%{_libdir}/dri/st7735r_dri.so
rm -Rf %{buildroot}%{_libdir}/dri/sun4i-drm_dri.so
rm -Rf %{buildroot}%{_libdir}/dri/kms_swrast_dri.so
rm -Rf %{buildroot}%{_libdir}/dri/swrast_dri.so
rm -Rf %{buildroot}%{_libdir}/dri/virtio_gpu_dri.so
rm -Rf %{buildroot}%{_libdir}/dri/crocus_dri.so
rm -Rf %{buildroot}%{_libdir}/dri/virtio_gpu_drv_video.so
rm -Rf %{buildroot}%{_libdir}/dri/libdril_dri.so
rm -Rf %{buildroot}%{_libdir}/dri/libgallium.so
rm -Rf %{buildroot}%{_libdir}/dri/libgallium_drv_video.so
rm -Rf %{buildroot}%{_libdir}/dri/apple_dri.so
rm -Rf %{buildroot}%{_libdir}/dri/gm12u320_dri.so
rm -Rf %{buildroot}%{_libdir}/dri/hdlcd_dri.so
rm -Rf %{buildroot}%{_libdir}/dri/ili9163_dri.so
rm -Rf %{buildroot}%{_libdir}/dri/ili9486_dri.so
rm -Rf %{buildroot}%{_libdir}/dri/imx-dcss_dri.so
rm -Rf %{buildroot}%{_libdir}/dri/imx-lcdif_dri.so
rm -Rf %{buildroot}%{_libdir}/dri/ingenic-drm_dri.so
rm -Rf %{buildroot}%{_libdir}/dri/kirin_dri.so
rm -Rf %{buildroot}%{_libdir}/dri/komeda_dri.so
rm -Rf %{buildroot}%{_libdir}/dri/mali-dp_dri.so
rm -Rf %{buildroot}%{_libdir}/dri/mcde_dri.so
rm -Rf %{buildroot}%{_libdir}/dri/mediatek_dri.so
rm -Rf %{buildroot}%{_libdir}/dri/mxsfb-drm_dri.so
rm -Rf %{buildroot}%{_libdir}/dri/panel-mipi-dbi_dri.so
rm -Rf %{buildroot}%{_libdir}/dri/panthor_dri.so
rm -Rf %{buildroot}%{_libdir}/dri/rcar-du_dri.so
rm -Rf %{buildroot}%{_libdir}/dri/rzg2l-du_dri.so
rm -Rf %{buildroot}%{_libdir}/dri/ssd130x_dri.so
rm -Rf %{buildroot}%{_libdir}/dri/sti_dri.so
rm -Rf %{buildroot}%{_libdir}/dri/stm_dri.so
rm -Rf %{buildroot}%{_libdir}/dri/udl_dri.so
rm -Rf %{buildroot}%{_libdir}/dri/v3d_dri.so
rm -Rf %{buildroot}%{_libdir}/dri/vkms_dri.so
rm -Rf %{buildroot}%{_libdir}/dri/zynqmp-dpsub_dri.so
rm -Rf %{buildroot}%{_libdir}/libgallium-25.2.2.so
rm -Rf %{buildroot}%{_libdir}/libRusticlOpenCL*
rm -Rf %{buildroot}%{_sysconfdir}/OpenCL/vendors/rusticl.icd
rm -Rf %{buildroot}%{_libdir}/gbm/dri_gbm.so
rm -Rf %{buildroot}%{_libdir}/libgbm.so.1
rm -Rf %{buildroot}%{_libdir}/libgbm.so.1.*
rm -Rf %{buildroot}%{_libdir}/libgbm.so
rm -Rf %{buildroot}%{_includedir}/gbm.h
rm -Rf %{buildroot}%{_libdir}/pkgconfig/gbm.pc
%ifarch %{ix86}
rm -Rf %{buildroot}%{_datadir}/drirc.d/00-radv-defaults.conf
%endif

%if 0%{?with_nvk}
%cargo_license_summary
%{cargo_license} > LICENSE.dependencies.%{_arch}
%if 0%{?vendor_nvk_crates}
%cargo_vendor_manifest
install -Dpm0644 cargo-vendor.txt \
  %{buildroot}%{_licensedir}/%{name}/cargo-vendor.%{_arch}.txt
%endif
%endif

%files
%if 0%{?with_nvk}
%license LICENSE.dependencies.%{_arch}
%if 0%{?vendor_nvk_crates}
%license cargo-vendor.%{_arch}.txt
%endif
%endif
%{_libdir}/libvulkan_lvp.so
%{_datadir}/vulkan/icd.d/lvp_icd.*.json
%{_libdir}/libVkLayer_MESA_anti_lag.so
%{_libdir}/libVkLayer_MESA_device_select.so
%{_datadir}/vulkan/implicit_layer.d/VkLayer_MESA_anti_lag.json
%{_datadir}/vulkan/implicit_layer.d/VkLayer_MESA_device_select.json
%if 0%{?with_vulkan_hw}
%{_libdir}/libvulkan_radeon.so
%ifarch aarch64 x86_64
%{_datadir}/drirc.d/00-radv-defaults.conf
%endif
%{_datadir}/vulkan/icd.d/radeon_icd.*.json
%if 0%{?with_nvk}
%{_libdir}/libvulkan_nouveau.so
%{_datadir}/vulkan/icd.d/nouveau_icd.*.json
%endif
%ifarch %{ix86} aarch64 x86_64
%{_libdir}/libvulkan_intel.so
%{_datadir}/vulkan/icd.d/intel_icd.*.json
%{_libdir}/libvulkan_intel_hasvk.so
%{_datadir}/vulkan/icd.d/intel_hasvk_icd.*.json
%endif
%ifarch aarch64
%{_libdir}/libvulkan_broadcom.so
%{_datadir}/vulkan/icd.d/broadcom_icd.*.json
%{_libdir}/libvulkan_freedreno.so
%{_datadir}/vulkan/icd.d/freedreno_icd.*.json
%{_libdir}/libvulkan_panfrost.so
%{_datadir}/vulkan/icd.d/panfrost_icd.*.json
%endif
%endif

%changelog
* Thu Dec 18 2025 LionHeartP <LionHeartP@proton.me> - 25.3.2-1
- Update to 25.3.2
- Include #38987 for SteamVR

* Thu Dec 04 2025 LionHeartP <LionHeartP@proton.me> - 25.3.1-1
- Update to 25.3.1
- Enable AMD anti-lag

* Mon Nov 17 2025 LionHeartP <LionHeartP@proton.me> - 25.3.0-1
- Update to 25.3.0
- Drop min_image_count.patch

* Wed Nov 12 2025 LionHeartP <LionHeartP@proton.me> - 25.2.7-1
- Update to 25.2.7

* Wed Oct 29 2025 LionHeartP <LionHeartP@proton.me> - 25.2.6-1
- Update to 25.2.6

* Wed Oct 15 2025 LionHeartP <LionHeartP@proton.me> - 25.2.5-1
- Update to 25.2.5
- Drop vdpau (upstream Fedora change)
- Drop gnome-shell glthread patch (upstream Fedora change)

* Wed Oct 01 2025 LionHeartP <LionHeartP@proton.me> - 25.2.4-1
- Update to 25.2.4

* Wed Sep 17 2025 LionHeartP <LionHeartP@proton.me> - 25.2.3-1
- Update to 25.2.3-1
