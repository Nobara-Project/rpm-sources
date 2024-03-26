Name:           vk_hdr_layer
Version:        0.0.git.29.869199cd
Release:        2%{?dist}
Summary:        Vulkan layer utilizing work-in-progress versions of the color management/representation protocols.

License:        MIT
URL:            https://github.com/Drakulix/VK_hdr_layer
Source:         VK_hdr_layer-869199cd.tar.gz

BuildRequires:  meson >= 0.54.0
BuildRequires:  ninja-build
BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(vulkan)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(wayland-scanner)
BuildRequires:  pkgconfig(vkroots)

%description
Hacks. Don't use for serious color work. - Vulkan layer utilizing work-in-progress versions of the color management/representation protocols.

%prep
%setup -T -b 0 -q -n VK_hdr_layer

%build
%meson
%meson_build

%install
%meson_install

%files
%license LICENSE
%doc README.md
%{_datadir}/vulkan/implicit_layer.d/*
%{_libdir}/*.so
