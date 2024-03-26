%global libliftoff_minver 0.4.1

%define commit 7f112d556430e1f814c4646b427bf71ae5b0de77
%global shortcommit %(c=%{commit}; echo ${c:0:7})

%global build_timestamp %(date +"%Y%m%d")

%global rel_build 13.git.%{build_timestamp}.%{shortcommit}%{?dist}

Name:           gamescope
Version:        3.13.20
Release:        %{rel_build}
Summary:        Micro-compositor for video games on Wayland

License:        BSD
URL:            https://github.com/ChimeraOS/gamescope

# Create stb.pc to satisfy dependency('stb')
Source1:        stb.pc

BuildRequires:  meson >= 0.54.0
BuildRequires:  ninja-build
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  glm-devel
BuildRequires:  google-benchmark-devel
BuildRequires:  libXmu-devel
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xdamage)
BuildRequires:  pkgconfig(xcomposite)
BuildRequires:  pkgconfig(xcursor)
BuildRequires:  pkgconfig(xrender)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xfixes)
BuildRequires:  pkgconfig(xxf86vm)
BuildRequires:  pkgconfig(xtst)
BuildRequires:  pkgconfig(xres)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(vulkan)
BuildRequires:  pkgconfig(wayland-scanner)
BuildRequires:  pkgconfig(wayland-server)
BuildRequires:  pkgconfig(wayland-protocols) >= 1.17
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(sdl2)
BuildRequires:  pkgconfig(libpipewire-0.3)
BuildRequires:  pkgconfig(libdisplay-info)
BuildRequires:  pkgconfig(libcap)
BuildRequires:  pkgconfig(hwdata)
BuildRequires:  pkgconfig(xwayland)
BuildRequires:  pkgconfig(libavif)
BuildRequires:  libdecor-devel
BuildRequires:  /usr/bin/glslangValidator
BuildRequires:  git
BuildRequires:  stb_image-devel
BuildRequires:  stb_image_write-devel
BuildRequires:  stb_image_resize-devel

# For building wlroots
BuildRequires:  pkgconfig(pixman-1) >= 0.42.0
BuildRequires:  pkgconfig(libseat)
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(libinput) >= 1.21.0
BuildRequires:  pkgconfig(x11-xcb)
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(xcb-errors)
BuildRequires:  pkgconfig(xcb-icccm)
BuildRequires:  pkgconfig(xcb-renderutil)

# libliftoff hasn't bumped soname, but API/ABI has changed for 0.2.0 release
Requires:       libliftoff%{?_isa} >= %{libliftoff_minver}
Requires:       xorg-x11-server-Xwayland
Requires:       google-benchmark
Requires:	gamescope-libs = %{version}-%{release}
Recommends:     mesa-dri-drivers
Recommends:     mesa-vulkan-drivers

%description
%{name} is the micro-compositor optimized for running video games on Wayland.

%package libs
Summary:	libs for %{name}
%description libs
%summary

%prep
git clone --single-branch --branch master https://github.com/ValveSoftware/gamescope
cd gamescope
git submodule update --init --recursive
mkdir -p pkgconfig
cp %{SOURCE1} pkgconfig/stb.pc

%build
cd gamescope
export PKG_CONFIG_PATH=pkgconfig
%meson -Dpipewire=enabled -Denable_gamescope=true -Denable_gamescope_wsi_layer=true -Denable_openvr_support=true -Dforce_fallback_for=vkroots,wlroots,libliftoff
%meson_build

%install
cd gamescope
%meson_install --skip-subprojects

%files
%license gamescope/LICENSE
%doc gamescope/README.md
%attr(0755, root, root) %caps(cap_sys_nice=eip) %{_bindir}/gamescope

%files libs
%{_libdir}/*.so
%{_datadir}/vulkan/implicit_layer.d/

%changelog
