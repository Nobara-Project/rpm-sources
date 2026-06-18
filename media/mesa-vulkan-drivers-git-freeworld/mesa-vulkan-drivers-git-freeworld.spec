%global _default_patch_fuzz 2

%global commit 2b5dd5dca11ee27cc9ce31f3d378fd84fd300bf4
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global build_timestamp %(date +"%Y%m%d")
%global rel_build 5.git.%{build_timestamp}.%{shortcommit}%{?dist}

%ifnarch s390x
%global with_hardware 1
%global with_kmsro 1
%global with_nvk 1
%global with_radeonsi 1
%global with_spirv_tools 1
%global with_vmware 1
%global with_vulkan_hw 1
%global with_va 1
%if !0%{?rhel}
%global with_r300 1
%global with_r600 1
%global with_opencl 1
%endif
%global base_vulkan %{?with_vulkan_hw:,amd}%{!?with_vulkan_hw:%{nil}}
%endif

%ifnarch %{ix86}
%if !0%{?rhel}
%global with_teflon 1
%endif
%endif

%ifarch %{ix86} aarch64 x86_64
%global with_crocus 1
%global with_i915   1
%global with_iris   1
%global intel_platform_vulkan %{?with_vulkan_hw:,intel,intel_hasvk}%{!?with_vulkan_hw:%{nil}}
%endif
%ifarch aarch64 x86_64
%if 0%{?with_vulkan_hw}
%global with_intel_vk_rt 1
%endif
%endif

%ifarch aarch64 x86_64 %{ix86}
%if !0%{?rhel}
%global with_asahi     1
%global with_d3d12     1
%global with_etnaviv   1
%global with_lima      1
%global with_tegra     1
%global with_vc4       1
%global with_v3d       1
%endif
%global with_freedreno 1
%global with_panfrost  1
%if 0%{?with_asahi}
%global asahi_platform_vulkan %{?with_vulkan_hw:,asahi}%{!?with_vulkan_hw:%{nil}}
%endif
%global extra_platform_vulkan %{?with_vulkan_hw:,broadcom,freedreno,panfrost,imagination}%{!?with_vulkan_hw:%{nil}}
%endif

%if !0%{?rhel}
%global with_libunwind 1
%global with_lmsensors 1
%global with_virtio    1
%endif

%ifarch %{valgrind_arches}
%bcond_without valgrind
%else
%bcond_with valgrind
%endif

%global vulkan_drivers swrast%{?base_vulkan}%{?intel_platform_vulkan}%{?asahi_platform_vulkan}%{?extra_platform_vulkan}%{?with_nvk:,nouveau}%{?with_virtio:,virtio}%{?with_d3d12:,microsoft-experimental}

%if 0%{?with_nvk} && 0%{?rhel}
%global vendor_nvk_crates 1
%endif

Name:           mesa-vulkan-drivers-git-freeworld
Summary:        The mesa graphics vulkan driver stack.
%global ver 26.2.0
Version:        %{lua:ver = string.gsub(rpm.expand("%{ver}"), "-", "~"); print(ver)}
Release:        %{rel_build}
License:        MIT
URL:            http://www.mesa3d.org

Source0:        https://gitlab.freedesktop.org/mesa/mesa/-/archive/%{commit}/mesa-%{commit}.tar.gz
# src/gallium/auxiliary/postprocess/pp_mlaa* have an ... interestingly worded license.
# Source1 contains email correspondence clarifying the license terms.
# Fedora opts to ignore the optional part of clause 2 and treat that code as 2 clause BSD.
Source1:        Mesa-MLAA-License-Clarification-Email.txt

# In CentOS/RHEL, Rust crates required to build NVK are vendored.
# The minimum target versions are obtained from the .wrap files
# https://gitlab.freedesktop.org/mesa/mesa/-/tree/main/subprojects
# but we generally want the latest compatible versions
%global rust_paste_ver 1.0.15
%global rust_proc_macro2_ver 1.0.106
%global rust_quote_ver 1.0.44
%global rust_syn_ver 2.0.115
%global rust_unicode_ident_ver 1.0.23
%global rustc_hash_ver 2.1.1
Source10:       https://crates.io/api/v1/crates/paste/%{rust_paste_ver}/download#/paste-%{rust_paste_ver}.tar.gz
Source11:       https://crates.io/api/v1/crates/proc-macro2/%{rust_proc_macro2_ver}/download#/proc-macro2-%{rust_proc_macro2_ver}.tar.gz
Source12:       https://crates.io/api/v1/crates/quote/%{rust_quote_ver}/download#/quote-%{rust_quote_ver}.tar.gz
Source13:       https://crates.io/api/v1/crates/syn/%{rust_syn_ver}/download#/syn-%{rust_syn_ver}.tar.gz
Source14:       https://crates.io/api/v1/crates/unicode-ident/%{rust_unicode_ident_ver}/download#/unicode-ident-%{rust_unicode_ident_ver}.tar.gz
Source15:       https://crates.io/api/v1/crates/rustc-hash/%{rustc_hash_ver}/download#/rustc-hash-%{rustc_hash_ver}.tar.gz

# https://gitlab.com/evlaV/mesa/
Patch10:        valve.patch

BuildRequires:  meson >= 1.3.0
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  gettext
%if 0%{?with_hardware}
BuildRequires:  kernel-headers
BuildRequires:  systemd-devel
%endif
# We only check for the minimum version of pkgconfig(libdrm) needed so that the
# SRPMs for each arch still have the same build dependencies. See:
# https://bugzilla.redhat.com/show_bug.cgi?id=1859515
BuildRequires:  pkgconfig(libdrm) >= 2.4.133
%if 0%{?with_libunwind}
BuildRequires:  pkgconfig(libunwind)
%endif
BuildRequires:  pkgconfig(expat)
BuildRequires:  pkgconfig(zlib) >= 1.2.3
BuildRequires:  pkgconfig(libzstd)
BuildRequires:  pkgconfig(libdisplay-info)
BuildRequires:  pkgconfig(wayland-scanner)
BuildRequires:  pkgconfig(wayland-protocols) >= 1.34
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
BuildRequires:  bison
BuildRequires:  flex
%if 0%{?with_lmsensors}
BuildRequires:  lm_sensors-devel
%endif
%if 0%{?with_va}
BuildRequires:  pkgconfig(libva) >= 0.38.0
%endif
BuildRequires:  pkgconfig(libelf)
BuildRequires:  pkgconfig(libglvnd) >= 1.3.2
BuildRequires:  llvm-devel >= 7.0.0
%if 0%{?with_teflon}
BuildRequires:  flatbuffers-devel
BuildRequires:  flatbuffers-compiler
BuildRequires:  xtensor-devel
%endif
%if 0%{?with_opencl} || 0%{?with_nvk} || 0%{?with_asahi} || 0%{?with_panfrost}
BuildRequires:  clang-devel
BuildRequires:  libstdc++-static
BuildRequires:  pkgconfig(libclc)
BuildRequires:  pkgconfig(SPIRV-Tools)
BuildRequires:  pkgconfig(LLVMSPIRVLib)
%endif
%if 0%{?with_opencl} || 0%{?with_nvk}
BuildRequires:  bindgen
%if 0%{?rhel}
BuildRequires:  rust-toolset
%else
BuildRequires:  cargo-rpm-macros
%endif
%endif
%if 0%{?with_nvk}
BuildRequires:  cbindgen
%endif
%if %{with valgrind}
BuildRequires:  pkgconfig(valgrind)
%endif
BuildRequires:  python3-devel
BuildRequires:  python3-mako
BuildRequires:  python3-pycparser
BuildRequires:  python3-pyyaml
BuildRequires:  vulkan-headers
BuildRequires:  glslang
%if 0%{?with_vulkan_hw}
BuildRequires:  pkgconfig(vulkan)
%endif
%if 0%{?with_d3d12}
BuildRequires:  pkgconfig(DirectX-Headers) >= 1.614.1
%endif
Requires:       vulkan%{_isa}
Obsoletes: 	mesa-vulkan-drivers-vulkan-devel
Obsoletes: 	mesa-vulkan-devel
Obsoletes:      mesa-omx-drivers < %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       mesa-vulkan-drivers
Provides:       mesa-vulkan-drivers%{?_isa}
Provides:       mesa-vulkan-drivers-git
Obsoletes:      mesa-vulkan-drivers-git

%description
%{summary}.

%prep
%autosetup -n mesa-%{commit} -p1
cp %{SOURCE1} docs/

# Extract Rust crates meson cache directory
%if 0%{?vendor_nvk_crates}
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
%endif

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
  -Dgallium-drivers=llvmpipe,virgl,nouveau%{?with_r300:,r300}%{?with_crocus:,crocus}%{?with_i915:,i915}%{?with_iris:,iris}%{?with_vmware:,svga}%{?with_radeonsi:,radeonsi}%{?with_r600:,r600}%{?with_freedreno:,freedreno}%{?with_etnaviv:,etnaviv}%{?with_tegra:,tegra}%{?with_vc4:,vc4}%{?with_v3d:,v3d}%{?with_lima:,lima}%{?with_panfrost:,panfrost}%{?with_vulkan_hw:,zink} \
%else
  -Dgallium-drivers=llvmpipe,virgl \
%endif
  -Dgallium-mediafoundation=disabled \
  -Dgallium-va=%{?with_va:enabled}%{!?with_va:disabled} \
%if 0%{?with_opencl}
  -Dgallium-rusticl=true \
%endif
  -Dvulkan-drivers=%{?vulkan_drivers} \
  -Dvulkan-layers=device-select%{?with_vulkan_overlay:,overlay},anti-lag \
  -Dgles1=enabled \
  -Dgles2=enabled \
  -Dopengl=true \
  -Dgbm=enabled \
  -Dglx=dri \
  -Degl=enabled \
  -Dglvnd=enabled \
  -Dintel-rt=%{?with_intel_vk_rt:enabled}%{!?with_intel_vk_rt:disabled} \
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

%if 0%{?with_nvk}
%cargo_license_summary
%{cargo_license} > LICENSE.dependencies.%{_arch}
%if 0%{?vendor_nvk_crates}
%cargo_vendor_manifest
install -Dpm0644 cargo-vendor.txt \
  %{buildroot}%{_licensedir}/%{name}/cargo-vendor.%{_arch}.txt
%endif
%endif

%install
%meson_install

# glvnd opens the versioned name, don't bother including the unversioned
rm -vf %{buildroot}%{_libdir}/libGLX_mesa.so
rm -vf %{buildroot}%{_libdir}/libEGL_mesa.so
# XXX can we just not build this
rm -vf %{buildroot}%{_libdir}/libGLES*

# glvnd needs a default provider for indirect rendering where it cannot
# determine the vendor
ln -s libGLX_mesa.so.0 %{buildroot}%{_libdir}/libGLX_system.so.0

# cleanup unused
rm -Rf %{buildroot}%{_bindir}/spirv2dxil
rm -Rf %{buildroot}%{_libdir}/libspirv_to_dxil.*
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
rm -Rf %{buildroot}%{_libdir}/libgallium-*-devel.so
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
rm -Rf %{buildroot}%{_datadir}/drirc.d/00-crocus-defaults.conf
rm -Rf %{buildroot}%{_datadir}/drirc.d/00-iris-defaults.conf
rm -Rf %{buildroot}%{_datadir}/drirc.d/00-msm-defaults.conf
rm -Rf %{buildroot}%{_datadir}/drirc.d/00-panfrost-defaults.conf
rm -Rf %{buildroot}%{_datadir}/drirc.d/00-r300-defaults.conf
rm -Rf %{buildroot}%{_datadir}/drirc.d/00-r600-defaults.conf
rm -Rf %{buildroot}%{_datadir}/drirc.d/00-radeonsi-defaults.conf
rm -Rf %{buildroot}%{_datadir}/drirc.d/00-v3d-defaults.conf
rm -Rf %{buildroot}%{_datadir}/drirc.d/00-virtio_gpu-defaults.conf
rm -Rf %{buildroot}%{_datadir}/drirc.d/00-vmwgfx-defaults.conf
rm -Rf %{buildroot}%{_datadir}/drirc.d/00-zink-defaults.conf
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
%if 0%{?with_virtio}
%{_libdir}/libvulkan_virtio.so
%{_datadir}/vulkan/icd.d/virtio_icd.*.json
%endif
%if 0%{?with_vulkan_hw}
%{_libdir}/libvulkan_radeon.so
%ifarch aarch64 x86_64
%{_datadir}/drirc.d/00-radv-defaults.conf
%endif
%{_datadir}/vulkan/icd.d/radeon_icd.*.json
%if 0%{?with_nvk}
%{_libdir}/libvulkan_nouveau.so
%{_datadir}/vulkan/icd.d/nouveau_icd.*.json
%{_datadir}/drirc.d/00-nvk-defaults.conf
%{_datadir}/drirc.d/00-hk-defaults.conf
%endif
%if 0%{?with_d3d12}
%{_libdir}/libvulkan_dzn.so
%{_datadir}/vulkan/icd.d/dzn_icd.*.json
%{_datadir}/drirc.d/00-dzn-defaults.conf
%endif
%ifarch %{ix86} aarch64 x86_64
%{_libdir}/libvulkan_intel.so
%{_datadir}/vulkan/icd.d/intel_icd.*.json
%{_datadir}/drirc.d/00-anv-defaults.conf
%{_libdir}/libvulkan_intel_hasvk.so
%{_datadir}/vulkan/icd.d/intel_hasvk_icd.*.json
%{_datadir}/drirc.d/00-hasvk-defaults.conf
%endif
%ifarch aarch64 x86_64 %{ix86}
%if 0%{?with_asahi}
%{_libdir}/libvulkan_asahi.so
%{_datadir}/vulkan/icd.d/asahi_icd.*.json
%endif
%{_libdir}/libvulkan_broadcom.so
%{_datadir}/vulkan/icd.d/broadcom_icd.*.json
%{_libdir}/libvulkan_freedreno.so
%{_datadir}/vulkan/icd.d/freedreno_icd.*.json
%{_datadir}/drirc.d/00-turnip-defaults.conf
%{_libdir}/libvulkan_panfrost.so
%{_datadir}/vulkan/icd.d/panfrost_icd.*.json
%{_datadir}/drirc.d/00-panvk-defaults.conf
%{_libdir}/libvulkan_powervr_mesa.so
%{_datadir}/vulkan/icd.d/powervr_mesa_icd.*.json
%endif
%if 0%{?with_vulkan_overlay}
%{_bindir}/mesa-overlay-control.py
%{_libdir}/libVkLayer_MESA_overlay.so
%{_datadir}/vulkan/explicit_layer.d/VkLayer_MESA_overlay.json
%endif
%endif

%changelog
* Thu Jun 18 2026 LionHeartP <LionHeartP@proton.me> - 26.2.0-5
- Update to latest commit

* Thu Jun 04 2026 LionHeartP <LionHeartP@proton.me> - 26.2.0-4
- Update to latest commit

* Fri May 22 2026 LionHeartP <LionHeartP@proton.me> - 26.2.0-3
- Update to latest commit

* Thu May 07 2026 LionHeartP <LionHeartP@proton.me> - 26.2.0-2
- Update to latest commit

* Thu Apr 30 2026 LionHeartP <LionHeartP@proton.me> - 26.2.0-1
- Update to latest commit

* Wed Apr 15 2026 LionHeartP <LionHeartP@proton.me> - 26.1.0-9
- Update to latest commit

* Thu Apr 02 2026 LionHeartP <LionHeartP@proton.me> - 26.1.0-8
- Update to latest commit

* Wed Mar 25 2026 LionHeartP <LionHeartP@proton.me> - 26.1.0-7
- Update to latest commit

* Wed Mar 18 2026 LionHeartP <LionHeartP@proton.me> - 26.1.0-6
- Update to latest commit

* Thu Mar 12 2026 LionHeartP <LionHeartP@proton.me> - 26.1.0-5
- Update to latest commit

* Thu Feb 26 2026 LionHeartP <LionHeartP@proton.me> - 26.1.0-4
- Update to latest commit

* Thu Feb 12 2026 LionHeartP <LionHeartP@proton.me> - 26.1.0-3
- Update to latest commit

* Sat Feb 07 2026 LionHeartP <LionHeartP@proton.me> - 26.1.0-2
- Update to latest commit

* Sun Feb 01 2026 LionHeartP <LionHeartP@proton.me> - 26.1.0-1
- Version bump
- Update to latest commit

* Sat Jan 24 2026 LionHeartP <LionHeartP@proton.me> - 26.0.0-2
- Update to latest commit

* Thu Jan 22 2026 LionHeartP <LionHeartP@proton.me> - 26.0.0-1
- Version bump
- Update to latest commit
- Remove #39314 + #39116 (upstreamed

* Sat Jan 17 2026 LionHeartP <LionHeartP@proton.me> - 25.4.0-11
- Update to latest commit
- Pull #39314 + #39116 for RT improvements
- Enable Intel RT driver

* Fri Jan 09 2026 LionHeartP <LionHeartP@proton.me> - 25.4.0-10
- Update to latest commit

* Thu Jan 01 2026 LionHeartP <LionHeartP@proton.me> - 25.4.0-9
- Update to latest commit

* Sun Dec 21 2025 LionHeartP <LionHeartP@proton.me> - 25.4.0-8
- Update to latest commit
- Update #38987 with fix for Monado

* Wed Dec 17 2025 LionHeartP <LionHeartP@proton.me> - 25.4.0-7
- Update to latest commit
- Include #38987 for SteamVR

* Thu Dec 11 2025 LionHeartP <LionHeartP@proton.me> - 25.4.0-4
- Update to latest commit

* Thu Dec 04 2025 LionHeartP <LionHeartP@proton.me> - 25.4.0-3
- Update to latest commit

* Thu Nov 27 2025 LionHeartP <LionHeartP@proton.me> - 25.4.0-2
- Update to latest commit

* Wed Nov 19 2025 LionHeartP <LionHeartP@proton.me> - 25.4.0-1
- Update to latest commit
- Bump version
- Drop min_image_count.patch
- Switch to Fedora packaging for rust crates

* Wed Nov 12 2025 LionHeartP <LionHeartP@proton.me> - 25.3.0-19
- Update to latest commit

* Fri Nov 07 2025 LionHeartP <LionHeartP@proton.me> - 25.3.0-18
- Update to latest commit
- Add #29580 and #37883 MRs for RT improvements

* Wed Nov 05 2025 LionHeartP <LionHeartP@proton.me> - 25.3.0-17
- Update to latest commit

* Wed Oct 29 2025 LionHeartP <LionHeartP@proton.me> - 25.3.0-16
- Update to latest commit

* Thu Oct 23 2025 LionHeartP <LionHeartP@proton.me> - 25.3.0-15
- Update to latest commit

* Wed Oct 15 2025 LionHeartP <LionHeartP@proton.me> - 25.3.0-14
- Update to latest commit
- Drop gnome-shell glthread patch (upstream Fedora change)

* Wed Oct 08 2025 LionHeartP <LionHeartP@proton.me> - 25.3.0-13
- Update to latest commit

* Wed Oct 01 2025 LionHeartP <LionHeartP@proton.me> - 25.3.0-12
- Update to latest commit

* Wed Sep 24 2025 LionHeartP <LionHeartP@proton.me> - 25.3.0-11
- Update to latest commit

* Wed Sep 17 2025 LionHeartP <LionHeartP@proton.me> - 25.3.0-10
- Update to latest commit
- Drop vdpau (https://gitlab.freedesktop.org/mesa/mesa/-/commit/4b54277d2e9420e37cdce98b3a09e6cecf87300d)

* Wed Sep 10 2025 LionHeartP <LionHeartP@proton.me> - 25.3.0-9
- Update to latest commit

* Wed Sep 03 2025 LionHeartP <LionHeartP@proton.me> - 25.3.0-8
- Update to latest commit

* Sun Aug 31 2025 LionHeartP <LionHeartP@proton.me> - 25.3.0-7
- Update to latest commit

* Sun Aug 24 2025 LionHeartP <LionHeartP@proton.me> - 25.3.0-6
- Update to latest commit
- Rebase min_image_count.patch

* Wed Aug 20 2025 LionHeartP <LionHeartP@proton.me> - 25.3.0-5
- Update to latest commit

* Thu Aug 14 2025 LionHeartP <LionHeartP@proton.me> - 25.3.0-4
- Update to latest commit

* Fri Aug 08 2025 LionHeartP <LionHeartP@proton.me> - 25.3.0-3
- Update to latest commit

* Thu Jul 31 2025 LionHeartP <LionHeartP@proton.me> - 25.3.0-2
- Update to latest commit

* Sat Jul 26 2025 LionHeartP <LionHeartP@proton.me> - 25.3.0-1
- Update to latest commit
- Bump version to 25.3.0
- Adapt rewrite_wrap_file macro to upstream changes
- Enable anti-lag

* Sun Jul 20 2025 LionHeartP <LionHeartP@proton.me> - 25.2.0-13
- Update to latest commit

* Wed Jul 16 2025 LionHeartP <LionHeartP@proton.me> - 25.2.0-12
- Update to latest commit
- Remove upstreamed #35269

* Thu Jul 10 2025 LionHeartP <LionHeartP@proton.me> - 25.2.0-10
- Update to latest commit

* Sun Jul 06 2025 LionHeartP <LionHeartP@proton.me> - 25.2.0-9
- Update to latest commit

* Tue Jul 01 2025 LionHeartP <LionHeartP@proton.me> - 25.2.0-8
- Update to latest commit
- Remove no longer needed #34918

* Wed Jun 25 2025 LionHeartP <LionHeartP@proton.me> - 25.2.0-7
- Update to latest commit
- Remove fsr4.patch due to upstream solution
- Add #35269 MR patch

* Thu Jun 19 2025 LionHeartP <LionHeartP@proton.me> - 25.2.0-6
- Update to latest commit

* Sun Jun 15 2025 LionHeartP <LionHeartP@proton.me> - 25.2.0-5
- Update to latest commit

* Sat Jun 7 2025 LionHeartP <LionHeartP@proton.me> - 25.2.0-4
- Update to latest commit

* Wed Jun 4 2025 LionHeartP <LionHeartP@proton.me> - 25.2.0-3
- Update to latest commit
- Stop building xa and nine due to upstream changes
- Disable mediafoundation
