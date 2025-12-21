%global srcname mesa
%global _default_patch_fuzz 2

%global _description These drivers contains video acceleration codecs for decoding/encoding H.264 and H.265 \
algorithms and decoding only VC1 algorithm.
%ifnarch s390x
%global with_hardware 1
%global with_kmsro 1
%global with_nvk 1
%global with_radeonsi 1
%global with_spirv_tools 1
%global with_vmware 1
%global with_vulkan_hw 0
%global with_va 1
%if !0%{?rhel}
%global with_r300 1
%global with_r600 1
#%%if 0%%{?with_vulkan_hw}
%global with_nvk %{with_vulkan_hw}
#%%endif
%global with_opencl 0
%endif
#%%global base_vulkan %%{?with_vulkan_hw:,amd}%%{!?with_vulkan_hw:%%{nil}}
%endif

#%%ifnarch %%{ix86}
%if !0%{?rhel}
%global with_teflon 0
%endif
#%%endif

%ifarch %{ix86} x86_64
%global with_crocus 0
%global with_i915   0
%global with_iris   0
#%%global intel_platform_vulkan %%{?with_vulkan_hw:,intel,intel_hasvk}%%{!?with_vulkan_hw:%%{nil}}
%endif
#%%ifarch x86_64
#%%if !0%%{?with_vulkan_hw}
%global with_intel_vk_rt 0
#%%endif
#%%endif

%ifarch aarch64 x86_64 %{ix86}
%if !0%{?rhel}
%global with_asahi     0
%global with_d3d12     1
%global with_etnaviv   0
%global with_lima      0
%global with_tegra     0
%global with_vc4       0
%global with_v3d       0
%endif
%global with_freedreno 0
%global with_panfrost  0
#%%if 0%%{?with_asahi}
#%%global asahi_platform_vulkan %%{?with_vulkan_hw:,asahi}%%{!?with_vulkan_hw:%%{nil}}
#%%endif
#%%global extra_platform_vulkan %%{?with_vulkan_hw:,broadcom,freedreno,panfrost,imagination}%%{!?with_vulkan_hw:%%{nil}}
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

#%%global vulkan_drivers swrast,virtio%%{?base_vulkan}%%{?intel_platform_vulkan}%%{?asahi_platform_vulkan}%%{?extra_platform_vulkan}%%{?with_nvk:,nouveau}

Name:           %{srcname}-freeworld
Summary:        Mesa graphics libraries
%global ver 25.3.2
Version:        %{lua:ver = string.gsub(rpm.expand("%{ver}"), "-", "~"); print(ver)}
Release:        %autorelease -b2
License:        MIT AND BSD-3-Clause AND SGI-B-2.0
URL:            http://www.mesa3d.org

Source0:        https://archive.mesa3d.org/%{srcname}-%{ver}.tar.xz
# src/gallium/auxiliary/postprocess/pp_mlaa* have an ... interestingly worded license.
# Source1 contains email correspondence clarifying the license terms.
# Fedora opts to ignore the optional part of clause 2 and treat that code as 2 clause BSD.
Source1:        Mesa-MLAA-License-Clarification-Email.txt
Source2:        org.mesa3d.vaapi.freeworld.metainfo.xml

# In CentOS/RHEL, Rust crates required to build NVK are vendored.
# The minimum target versions are obtained from the .wrap files
# https://gitlab.freedesktop.org/mesa/mesa/-/tree/main/subprojects
# but we generally want the latest compatible versions
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

BuildRequires:  meson >= 1.3.0
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
%if 0%{?with_opencl} || 0%{?with_nvk}
BuildRequires:  rust-packaging
%endif
%ifarch %{ix86} x86_64
BuildRequires:  clang-devel
BuildRequires:  bindgen
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

%description
%{_description}

%package -n %{srcname}-libgallium-freeworld
Summary:        Mesa-based libgallium driver
Requires:       %{srcname}-filesystem%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
%if 0%{?with_va}
Recommends:     %{srcname}-va-drivers%{?_isa}
%endif
Provides:       %{srcname}-libgallium%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides:       %{srcname}-libgallium-freeworld%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      %{srcname}-libgallium

%description  -n %{srcname}-libgallium-freeworld
%{summary}.

%if 0%{?with_va}
%package        -n %{srcname}-va-drivers-freeworld
Summary:        Mesa-based VA-API drivers
Requires:       %{srcname}-filesystem%{?_isa} = %{?epoch:%{epoch}:}%{version}
Requires:       %{srcname}-libgallium-freeworld%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes:      %{srcname}-vdpau-drivers-freeworld < %{?epoch:%{epoch}:}%{version}-%{release}

Conflicts:      %{srcname}-va-drivers%{?_isa}

%description    -n %{srcname}-va-drivers-freeworld
%{_description}
%endif

%prep
%autosetup -n %{srcname}-%{ver} -p1
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

%meson \
  -Dplatforms=x11,wayland \
%if 0%{?with_hardware}
  -Dgallium-drivers=llvmpipe,virgl,nouveau%{?with_r300:,r300}%{?with_crocus:,crocus}%{?with_i915:,i915}%{?with_iris:,iris}%{?with_vmware:,svga}%{?with_radeonsi:,radeonsi}%{?with_r600:,r600}%{?with_asahi:,asahi}%{?with_freedreno:,freedreno}%{?with_etnaviv:,etnaviv}%{?with_tegra:,tegra}%{?with_vc4:,vc4}%{?with_v3d:,v3d}%{?with_lima:,lima}%{?with_panfrost:,panfrost}%{?with_vulkan_hw:,zink}%{?with_d3d12:,d3d12} \
%else
  -Dgallium-drivers=llvmpipe,virgl \
%endif
  -Dgallium-va=%{?with_va:enabled}%{!?with_va:disabled} \
  -Dgallium-mediafoundation=disabled \
  -Dteflon=false \
%if 0%{?with_opencl}
  -Dgallium-rusticl=true \
%endif
  -Dvideo-codecs=all \
  -Dvulkan-drivers=%{?vulkan_drivers} \
  -Dvulkan-layers=device-select \
  -Dshared-glapi=enabled \
  -Dgles1=enabled \
  -Dgles2=enabled \
  -Dopengl=true \
  -Dgbm=enabled \
  -Dglx=dri \
  -Degl=enabled \
  -Dglvnd=enabled \
  -Dintel-rt=%{!?with_intel_vk_rt:enabled}%{?with_intel_vk_rt:disabled} \
  -Dmicrosoft-clc=disabled \
  -Dllvm=enabled \
  -Dshared-llvm=enabled \
  -Dvalgrind=%{?with_valgrind:enabled}%{!?with_valgrind:disabled} \
  -Dbuild-tests=false \
%if !0%{?with_libunwind}
  -Dlibunwind=disabled \
%endif
%if !0%{?with_lmsensors}
  -Dlmsensors=disabled \
%endif
  -Dandroid-libbacktrace=disabled \
%ifarch %{ix86}
  -Dglx-read-only-text=true \
%endif
  -Dspirv-tools=%{?with_spirv_tools:enabled}%{!?with_spirv_tools:disabled} \
  %{nil}
%meson_build

%install
%meson_install

# install Appdata files
mkdir -p %{buildroot}%{_metainfodir}
install -pm 0644 %{SOURCE2} %{buildroot}%{_metainfodir}

# likewise glvnd
rm -vf %{buildroot}%{_libdir}/libGLX_mesa.so
rm -vf %{buildroot}%{_libdir}/libEGL_mesa.so
# XXX can we just not build this
rm -vf %{buildroot}%{_libdir}/libGLES*

%if ! 0%{?with_asahi}
# This symlink is unconditionally created when any kmsro driver is enabled
# We don't want this one so delete it
rm -vf %{buildroot}%{_libdir}/dri/apple_dri.so
%endif

# glvnd needs a default provider for indirect rendering where it cannot
# determine the vendor
ln -s %{_libdir}/libGLX_mesa.so.0 %{buildroot}%{_libdir}/libGLX_system.so.0

# this keeps breaking, check it early.  note that the exit from eu-ftr is odd.
pushd %{buildroot}%{_libdir}
for i in libGL.so ; do
    eu-findtextrel $i && exit 1
done
popd

# strip unneeded files from va-api
rm -rf %{buildroot}%{_datadir}/{drirc.d,glvnd,vulkan}
rm -rf %{buildroot}%{_libdir}{,/dri}/{d3d,EGL,gallium-pipe,libGLX,pkgconfig}
rm -rf %{buildroot}%{_includedir}/{d3dadapter,EGL,GL,KHR}
rm -fr %{buildroot}%{_sysconfdir}/OpenGL
rm -fr %{buildroot}%{_libdir}{,/dri}/libGL.so*
rm -fr %{buildroot}%{_libdir}{,/dri}/libglapi.so*
rm -fr %{buildroot}%{_libdir}/libOSMesa.so*
rm -fr %{buildroot}%{_libdir}/pkgconfig/osmesa.pc
rm -fr %{buildroot}%{_libdir}/libgbm.so*
rm -fr %{buildroot}%{_includedir}/gbm.h
rm -fr %{buildroot}%{_includedir}/gbm_backend_abi.h
rm -fr %{buildroot}%{_libdir}{,/dri}/libxatracker.so*
rm -fr %{buildroot}%{_includedir}/xa_*.h
rm -fr %{buildroot}%{_libdir}/libMesaOpenCL.so*
rm -fr %{buildroot}%{_libdir}/dri/*_dri.so
rm -fr %{buildroot}%{_libdir}/libvulkan*.so
rm -fr %{buildroot}%{_libdir}{,/dri}/libVkLayer_MESA_device_select.so
rm -fr %{buildroot}%{_includedir}/GLES*
rm -fr %{buildroot}%{_libdir}{,/dri}/libGLES*
rm -fr %{buildroot}%{_libdir}{,/dri}/libGLESv2*
rm -fr %{buildroot}%{_libdir}/gbm
rm -fr %{buildroot}%{_libdir}/libEGL*
rm -fr %{buildroot}%{_libdir}/libGLX*
rm -fr %{buildroot}%{_libdir}/libteflon*

%if 0%{?with_va}
%files -n %{srcname}-va-drivers-freeworld
%{_libdir}/dri/nouveau_drv_video.so
%if 0%{?with_r600}
%{_libdir}/dri/r600_drv_video.so
%endif
%if 0%{?with_radeonsi}
%{_libdir}/dri/radeonsi_drv_video.so
%endif
%if 0%{?with_d3d12}
%{_libdir}/dri/d3d12_drv_video.so
%endif
%{_libdir}/dri/virtio_gpu_drv_video.so
%{_metainfodir}/org.mesa3d.vaapi.freeworld.metainfo.xml
%license docs/license.rst
%endif

%files -n %{srcname}-libgallium-freeworld
%{_libdir}/libgallium-*.so

%changelog
* Thu Dec 18 2025 LionHeartP <LionHeartP@proton.me> - 25.3.2-1
- Update to 25.3.2

* Thu Dec 04 2025 LionHeartP <LionHeartP@proton.me> - 25.3.1-1
- Update to 25.3.1

* Mon Nov 17 2025 LionHeartP <LionHeartP@proton.me> - 25.3.0-1
- Update to 25.3.0

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
- Update to 25.2.3

* Wed Sep 03 2025 LionHeartP <LionHeartP@proton.me> - 25.2.2-1
- Update to 25.2.2
- Rework spec according to Fedora changes

* Wed Aug 20 2025 LionHeartP <LionHeartP@proton.me> - 25.2.1-1
- Update to 25.2.1
- Drop intel-clc https://gitlab.freedesktop.org/mesa/mesa/-/merge_requests/36625

* Fri Aug 08 2025 LionHeartP <LionHeartP@proton.me> - 25.2.0-1
- Update to 25.2.0
- Fixup spec for packaging changes

* Thu Jul 31 2025 LionHeartP <LionHeartP@proton.me> - 25.1.7-1
- Update to 25.1.7

* Wed Jul 16 2025 LionHeartP <LionHeartP@proton.me> - 25.1.6-1
- Update to 25.1.6

* Wed Jul 02 2025 LionHeartP <LionHeartP@proton.me> - 25.1.5-1
- Update to 25.1.5

* Thu May 8 2025 Thorsten Leemhuis <fedora@leemhuis.info> - 25.1.0-1
- Update to 25.1.0
- Sync new bits with Fedora

* Fri Apr 25 2025 Thorsten Leemhuis <fedora@leemhuis.info> - 25.1.0~rc2-1
- Update to 25.1.0~rc2
- Sync new bits with Fedora, which includes enabling of the asahi driver

* Tue Apr 22 2025 Thorsten Leemhuis <fedora@leemhuis.info> - 25.0.4-1
- Update to 25.0.4
- Sync a few bits with Fedora

* Thu Apr 3 2025 Thorsten Leemhuis <fedora@leemhuis.info> - 25.0.3-1
- Update to 25.0.3

* Thu Mar 27 2025 Thorsten Leemhuis <fedora@leemhuis.info> - 25.0.2-2
- pick up backport and fixes from Fedora for clover/llvm20 and
  vulkan/wsi: implement the Wayland color management protocol

* Thu Mar 20 2025 Thorsten Leemhuis <fedora@leemhuis.info> - 25.0.2-1
- Update to 25.0.2

* Thu Mar 06 2025 Thorsten Leemhuis <fedora@leemhuis.info> - 25.0.1-1
- Update to 25.0.1
- drop 0001-vulkan-wsi-x11-fix-use-of-uninitialised-xfixes-regio.patch

* Thu Feb 20 2025 Björn Esser <besser82@fedoraproject.org> - 25.0.0-4
- Add archless provides for mesa-vulkan-drivers

* Thu Feb 20 2025 Björn Esser <besser82@fedoraproject.org> - 25.0.0-3
- Fix mesa-filesystem requires in mesa-vulkan-drivers-freeworld

* Thu Feb 20 2025 Björn Esser <besser82@fedoraproject.org> - 25.0.0-2
- Fix general installability of mesa-vulkan-drivers-freeworld

* Wed Feb 19 2025 Thorsten Leemhuis <fedora@leemhuis.info> - 25.0.0-1
- Update to 25.0.0
- add 0001-vulkan-wsi-x11-fix-use-of-uninitialised-xfixes-regio.patch

* Thu Feb 13 2025 Thorsten Leemhuis <fedora@leemhuis.info> - 25.0.0~rc3-1
- Update to 25.0.0~rc3

* Tue Feb 11 2025 Thorsten Leemhuis <fedora@leemhuis.info> - 25.0.0~rc2-2
- create mesa-vulkan-drivers-freeworld, conflicting with mesa-vulkan-drivers

* Thu Feb 06 2025 Thorsten Leemhuis <fedora@leemhuis.info> - 25.0.0~rc2-1
- Update to 25.0.0~rc2
- drop upstreamed patch

* Tue Jan 28 2025 Björn Esser <besser82@fedoraproject.org> - 24.3.4-8
- Add patch for radeonsi to disallow compute queues on Raven/Raven2
  due to hangs

* Mon Jan 27 2025 Thorsten Leemhuis <fedora@leemhuis.info> - 24.3.4-7
- Drop conflicts with mesa-va-drivers, as its files do not conclict
  anymore with the ones in mesa-va-drivers-freeworld
- Drop now unneeded BR on a specific LLVM version

* Fri Jan 24 2025 Thorsten Leemhuis <fedora@leemhuis.info> - 24.3.4-6
- Rebuild due to mishap with the release number

* Fri Jan 24 2025 Thorsten Leemhuis <fedora@leemhuis.info> - 24.3.4-2
- Reapply ldconfig changes from Leigh
- Enable GLES stuff and exclude some of the files now getting build

* Fri Jan 24 2025 Thorsten Leemhuis <fedora@leemhuis.info> - 24.3.4-1
- Update to 24.3.4

* Fri Jan 17 2025 Leigh Scott <leigh123linux@gmail.com> - 24.3.3-5
- Remove ldconfig as it breaks some apps

* Sat Jan 11 2025 Leigh Scott <leigh123linux@gmail.com> - 24.3.3-4
- Fix ldconfig scriptlets

* Sat Jan 11 2025 Leigh Scott <leigh123linux@gmail.com> - 24.3.3-3
- Add ldconfig scriptlets

* Fri Jan 10 2025 Leigh Scott <leigh123linux@gmail.com> - 24.3.3-2
- Fix tearing due to fedora libgallium

* Fri Jan 10 2025 Thorsten Leemhuis <fedora@leemhuis.info> - 24.3.3-1
- Update to 24.3.3

* Fri Dec 20 2024 Thorsten Leemhuis <fedora@leemhuis.info> - 24.3.2-1
- Update to 24.3.2

* Thu Dec 05 2024 Thorsten Leemhuis <fedora@leemhuis.info> - 24.3.1-1
- Update to 24.3.1

* Fri Nov 22 2024 Thorsten Leemhuis <fedora@leemhuis.info> - 24.3.0-1
- Update to 24.3.0

* Thu Nov 14 2024 Thorsten Leemhuis <fedora@leemhuis.info> - 24.3.0~rc2-1
- Update to 24.3.0-rc2

* Tue Nov 12 2024 Thorsten Leemhuis <fedora@leemhuis.info> - 24.3.0~rc1-1
- Update to 24.3.0-rc1
- Drop unneeded omx support

* Thu Oct 31 2024 Thorsten Leemhuis <fedora@leemhuis.info> - 24.2.6-1
- Update to 24.2.6

* Mon Oct 28 2024 Thorsten Leemhuis <fedora@leemhuis.info> - 24.2.5-1
- Update to 24.2.5

* Fri Oct 04 2024 Thorsten Leemhuis <fedora@leemhuis.info> - 24.2.4-1
- Update to 24.2.4
- drop 0001-gallium-Don-t-pass-avx512er-and-avx512pf-features-on.patch

* Sun Sep 29 2024 Thorsten Leemhuis <fedora@leemhuis.info> - 24.2.3-5
- rebuild for -Ehuman-not-enough-tee-error

* Sun Sep 29 2024 Thorsten Leemhuis <fedora@leemhuis.info> - 24.2.3-4
- add 0001-gallium-Don-t-pass-avx512er-and-avx512pf-features-on.patch

* Wed Sep 25 2024 Thorsten Leemhuis <fedora@leemhuis.info> - 24.2.3-3
- temporarily require llvm 19 for Fedora 41 and up

* Fri Sep 20 2024 Nicolas Chauvet <kwizart@gmail.com> - 24.2.3-2
- Attempt to complement Fedora

* Thu Sep 19 2024 Thorsten Leemhuis <fedora@leemhuis.info> - 24.2.3-1
- Update to 24.2.3
- Sync a few bits with mesa.spec from fedora

* Fri Sep 6 2024 Thorsten Leemhuis <fedora@leemhuis.info> - 24.2.2-1
- Update to 24.2.2
- Sync a few bits with mesa.spec from fedora

* Thu Aug 29 2024 Thorsten Leemhuis <fedora@leemhuis.info> - 24.2.1-1
- Update to 24.2.1
- Sync a few bits with mesa.spec from fedora

* Mon Aug 19 2024 Thorsten Leemhuis <fedora@leemhuis.info> - 24.2.0-1
- Update to 24.2.0

* Thu Aug 8 2024 Thorsten Leemhuis <fedora@leemhuis.info> - 24.2.0~rc4-1
- Update to 24.2.0-rc4

* Fri Aug 02 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 24.2.0~rc3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Aug 1 2024 Thorsten Leemhuis <fedora@leemhuis.info> - 24.2.0~rc3-1
- Update to 24.2.0-rc3
- Drop upstreamed patch

* Fri Jul 19 2024 Thorsten Leemhuis <fedora@leemhuis.info> - 24.1.4-2
- add revert-6746d4df-to-fix-av1-slice_data_offset.patch

* Thu Jul 18 2024 Thorsten Leemhuis <fedora@leemhuis.info> - 24.1.4-1
- Update to 24.1.4
- Drop upstreamed patch

* Mon Jul 01 2024 Leigh Scott <leigh123linux@gmail.com> - 24.1.2-2
- Fix mutter crash when calling eglQueryDmaBufModifiersEXT
- Fix GNOME and KDE crash with some AMD GPUs

* Thu Jun 20 2024 Thorsten Leemhuis <fedora@leemhuis.info> - 24.1.2-1
- Update to 24.1.2

* Thu Jun 06 2024 Thorsten Leemhuis <fedora@leemhuis.info> - 24.1.1-1
- Update to 24.1.1

* Thu May 23 2024 Thorsten Leemhuis <fedora@leemhuis.info> - 24.1.0-1
- Update to 24.1.0

* Fri May 17 2024 Thorsten Leemhuis <fedora@leemhuis.info> - 24.1.0~rc4-2
- disable teflon on ix86, too

* Thu May 16 2024 Thorsten Leemhuis <fedora@leemhuis.info> - 24.1.0~rc4-1
- Update to 24.1.0-rc4
- Sync a few more bits with mesa.spec from fedora

* Thu May 9 2024 Thorsten Leemhuis <fedora@leemhuis.info> - 24.1.0~rc3-1
- Update to 24.1.0-rc3
- Sync with_intel_vk_rt bits with mesa.spec from fedora
- Unconditionally BR clang-devel, bindgen, libclc, SPIRV-Tools, and
  LLVMSPIRVLib which are needed now

* Tue May 7 2024 Thorsten Leemhuis <fedora@leemhuis.info> - 24.1.0~rc2-1
- Update to 24.1.0-rc2

* Thu Apr 25 2024 Thorsten Leemhuis <fedora@leemhuis.info> - 24.0.6-1
- Update to 24.0.6

* Thu Apr 11 2024 Thorsten Leemhuis <fedora@leemhuis.info> - 24.0.5-1
- Update to 24.0.5

* Mon Apr 1 2024 Thorsten Leemhuis <fedora@leemhuis.info> - 24.0.4-1
- Update to 24.0.4

* Thu Mar 14 2024 Thorsten Leemhuis <fedora@leemhuis.info> - 24.0.3-1
- Update to 24.0.3

* Wed Mar 6 2024 Thorsten Leemhuis <fedora@leemhuis.info> - 24.0.2-3
- Disable nvk explicitly to avoid BR on rust-packaging

* Wed Mar 6 2024 Thorsten Leemhuis <fedora@leemhuis.info> - 24.0.2-2
- Update to 24.0.2

* Thu Feb 22 2024 Thorsten Leemhuis <fedora@leemhuis.info> - 24.0.0-2
- enable vp9, av1 codecs due to new meson build flag (#6873)

* Fri Feb 02 2024 Thorsten Leemhuis <fedora@leemhuis.info> - 24.0.0-1
- Update to 24.0.0

* Fri Jan 19 2024 Thorsten Leemhuis <fedora@leemhuis.info> - 24.0.0~rc2-1
- Update to 24.0.0-rc2

* Thu Jan 11 2024 Thorsten Leemhuis <fedora@leemhuis.info> - 23.3.3-1
- Update to 23.3.3

* Wed Jan 3 2024 Thorsten Leemhuis <fedora@leemhuis.info> - 23.3.2-1
- Update to 23.3.2

* Mon Dec 18 2023 Thorsten Leemhuis <fedora@leemhuis.info> - 23.3.1-1
- Update to 23.3.1

* Fri Dec 15 2023 Thorsten Leemhuis <fedora@leemhuis.info> - 23.3.0-2
- sync a few bit with fedora's mesa.spec

* Fri Dec 1 2023 Thorsten Leemhuis <fedora@leemhuis.info> - 23.3.0-1
- Update to 23.3.0

* Thu Nov 30 2023 Thorsten Leemhuis <fedora@leemhuis.info> - 23.3.0~rc5-1
- Update to 23.3.0-rc5

* Thu Nov 2 2023 Thorsten Leemhuis <fedora@leemhuis.info> - 23.3.0~rc2-1
- Update to 23.3.0-rc2

* Thu Oct 26 2023 Thorsten Leemhuis <fedora@leemhuis.info> - 23.3.0~rc1-1
- Update to 23.3.0-rc1

* Tue Oct 10 2023 Thorsten Leemhuis <fedora@leemhuis.info> - 23.2.1-2
- follow Fedora: backport MR #24045 to fix Iris crashes (RHBZ#2238711)
- temporarily hard require llvm16, as that's what's used by fedora

* Sat Sep 30 2023 Thorsten Leemhuis <fedora@leemhuis.info> - 23.2.1-1
- Update to 23.2.1

* Wed Sep 6 2023 Thorsten Leemhuis <fedora@leemhuis.info> - 23.2.0~rc3.1
- Update to 23.2.0-rc3
- sync a few spec file bits with Fedora's mesa package

* Fri Aug 11 2023 Thorsten Leemhuis <fedora@leemhuis.info> - 23.2.0~rc1.1
- Update to 23.2.0-rc2

* Thu Aug 3 2023 Thorsten Leemhuis <fedora@leemhuis.info> - 23.1.5-1
- Update to 23.1.5

* Sun Jul 23 2023 Thorsten Leemhuis <fedora@leemhuis.info> - 23.1.4-1
- Update to 23.1.4

* Fri Jun 23 2023 Thorsten Leemhuis <fedora@leemhuis.info> - 23.1.3-1
- Update to 23.1.3

* Mon Jun 12 2023 Thorsten Leemhuis <fedora@leemhuis.info> - 23.1.2-1
- Update to 23.1.2
- sync a few spec file bits with Fedora's mesa package

* Fri May 26 2023 Thorsten Leemhuis <fedora@leemhuis.info> - 23.1.1-1
- Update to 23.1.1

* Tue May 23 2023 Thorsten Leemhuis <fedora@leemhuis.info> - 23.1.0-1
- Update to 23.1.0
- sync a few spec file bits with Fedora's mesa package

* Tue Apr 25 2023 Thorsten Leemhuis <fedora@leemhuis.info> - 23.0.3-1
- Update to 23.0.3

* Thu Apr 20 2023 Thorsten Leemhuis <fedora@leemhuis.info> - 23.0.2-1.1
- Re-introduce Conflicts (rfbz#6612, kwizart)
- Enforces version to avoid miss-match with fedora (rfbz#6613, kwizart)

* Thu Apr 13 2023 Thorsten Leemhuis <fedora@leemhuis.info> - 23.0.2-1
- Update to 23.0.2

* Tue Apr 11 2023 Thorsten Leemhuis <fedora@leemhuis.info> - 23.0.1-2
- Rebuild for LLVM 16

* Sat Mar 25 2023 Thorsten Leemhuis <fedora@leemhuis.info> - 23.0.1-1
- Update to 23.0.1

* Thu Feb 23 2023 Thorsten Leemhuis <fedora@leemhuis.info> - 23.0.0-1
- Update to 23.0.0

* Thu Feb 16 2023 Luya Tshimbalanga <luya@fedoraproject.org> - 23.0.0~rc4-2
- Remove trailed .1 in release tag

* Thu Feb 2 2023 Thorsten Leemhuis <fedora@leemhuis.info> - 23.0.0~rc4-1
- Update to 23.0.0-rc4

* Mon Jan 30 2023 Thorsten Leemhuis <fedora@leemhuis.info> - 23.0.0~rc3-1
- Update to 23.0.0-rc3

* Wed Jan 18 2023 Luya Tshimbalanga <luya@fedoraproject.org> - 22.3.3-2.1
- Drop conflicts with provides

* Tue Jan 17 2023 Luya Tshimbalanga <luya@fedoraproject.org> - 22.3.3-2
- Fix dependencies issues between Fedora and RPM Fusion

* Thu Jan 12 2023 Thorsten Leemhuis <fedora@leemhuis.info> - 22.3.3-1
- Update to 22.3.3

* Wed Jan 4 2023 Luya Tshimbalanga <luya@fedoraproject.org> - 22.3.2-3
- fix typo on conflict condition for vdpau sub-package

* Sun Jan 1 2023 Luya Tshimbalanga <luya@fedoraproject.org> - 22.3.2-2
- Add conflicts to resolve dependencies from Fedora repo on update

* Sat Dec 31 2022 Thorsten Leemhuis <fedora@leemhuis.info> - 22.3.2-1
- Update to 22.3.2

* Mon Dec 19 2022 Thorsten Leemhuis <fedora@leemhuis.info> - 22.3.1-1
- adjust placement of a few files entries to stay in sync with Fedora; while at it
  make it more obvious that the license files are specific to rpmfusion

* Mon Dec 19 2022 Thorsten Leemhuis <fedora@leemhuis.info> - 22.3.1-1
- Update to 22.3.1
- sync a few bits with Fedora's mesa.spec

* Sun Nov 13 2022 Vitaly Zaitsev <vitaly@easycoding.org> - 22.3.0~rc2-2
- Updated to version 22.3.0-rc2.

* Sun Nov 13 2022 Vitaly Zaitsev <vitaly@easycoding.org> - 22.2.3-1
- Updated to version 22.2.3.

* Sun Nov 6 2022 Luya Tshimbalanga <luya@fedoraproject.org> - 22.2.2-1
- Update to 22.2.2

* Thu Oct 13 2022 Luya Tshimbalanga <luya@fedoraproject.org> - 22.2.1-1
- Update to 22.2.1
- Add appdata files for each subpackage

* Wed Oct 5 2022 Luya Tshimbalanga <luya@fedoraproject.org> - 22.2.0-4
- Drop unneeded omx support
- Add missing license for each files

* Sun Oct 2 2022 Luya Tshimbalanga <luya@fedoraproject.org> - 22.2.0-3
- Rename vaapi to va
- Broaden description
- Add Enhancement line
- Clean up spec file

* Sat Oct 1 2022 Luya Tshimbalanga <luya@fedoraproject.org> - 22.2.0-2
- Drop unsupported autospec in rpmfusion infra
- Enable h264, h265 and vc1 codecs
- Re-enable vdpau and omx (OpenMax) support

* Sat Oct 1 2022 Luya Tshimbalanga <luya@fedoraproject.org> - 22.2.0-1
- Initial release
