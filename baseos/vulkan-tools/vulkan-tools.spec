Name:           vulkan-tools
Version:        1.3.280
Release:        1%{?dist}
Summary:        Vulkan tools

License:        ASL 2.0
URL:            https://github.com/KhronosGroup/Vulkan-Tools
Source0:        %url/archive/v%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  cmake3
BuildRequires:  glslang
BuildRequires:  ninja-build
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  vulkan-loader-devel
BuildRequires:  vulkan-volk-devel
BuildRequires:  vulkan-volk-static
BuildRequires:  wayland-protocols-devel
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-cursor)
BuildRequires:  pkgconfig(wayland-server)
BuildRequires:  pkgconfig(wayland-egl)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xrandr)
BuildRequires:  pkgconfig(xcb)

Provides:       vulkan-demos%{?_isa} = %{version}-%{release}
Obsoletes:      vulkan-demos < %{version}-%{release}

%description
Vulkan tools

%prep
%autosetup -n Vulkan-Tools-%{version}


%build
%cmake3 -GNinja -DCMAKE_BUILD_TYPE=Release -DGLSLANG_INSTALL_DIR=%{_prefix}
%cmake3_build


%install
%cmake3_install

%files
%doc README.md CONTRIBUTING.md
%{_bindir}/*

%changelog


