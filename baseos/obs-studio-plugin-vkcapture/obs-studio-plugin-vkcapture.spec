# The i686 build only builds the game injection libraries
%ifarch i686
%global libs_only 1
%else
%global libs_only 0
%endif

%global srcname obs-vkcapture

Name:           obs-studio-plugin-vkcapture
Version:        1.5.6
Release:        1%{?dist}
Summary:        OBS plugin for Vulkan/OpenGL game capture

License:        GPL-2.0-or-later and Zlib
URL:            https://github.com/nowrep/obs-vkcapture
Source0:        %{url}/archive/v%{version}/%{srcname}-%{version}.tar.gz

# elfhacks FTBFS on IBM Z
ExcludeArch:    s390x

BuildRequires:  cmake
BuildRequires:  gcc

%if ! %{libs_only}
BuildRequires:  cmake(libobs)
%endif
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(xcb-xfixes)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-scanner)
BuildRequires:  libglvnd-devel
BuildRequires:  vulkan-loader-devel

Requires:       obs-studio%{?_isa}

Enhances:       obs-studio%{?_isa}

# Replace older packages
Obsoletes:      obs-studio-vkcapture < %{version}-%{release}
Provides:       obs-studio-vkcapture = %{version}-%{release}
Provides:       obs-studio-vkcapture%{?_isa} = %{version}-%{release}
Obsoletes:      obs-studio-gamecapture < %{version}-%{release}
Provides:       obs-studio-gamecapture = %{version}-%{release}
Provides:       obs-studio-gamecapture%{?_isa} = %{version}-%{release}

# Alternative name
Provides:       obs-studio-plugin-gamecapture = %{version}-%{release}
Provides:       obs-studio-plugin-gamecapture%{?_isa} = %{version}-%{release}

Recommends:     %{name}-hook-libs%{?_isa} = %{version}-%{release}

%description
%{name}.

%package hook-libs

Summary:        Hook libraries for OBS Vulkan/OpenGL game capture

# For directory ownership
Requires:       vulkan-loader%{?_isa}

# libs split, obsolete older packages
Obsoletes:      obs-studio-plugin-vkcapture < %{version}-%{release}
Obsoletes:      obs-studio-vkcapture < %{version}-%{release}
Obsoletes:      obs-studio-gamecapture < %{version}-%{release}

# Note that the hook-libs package does not require the base package. This is useful, for example, with Flatpak OBS+plugin.
# For this reason, the preload library wrappers are part of the hook-libs subpackage.
# However, recommend it, to ensure that after an upgrade through the obsoletes above, both end up installed
%if ! %{libs_only}
Recommends:     %{name}%{?_isa} = %{version}-%{release}
%endif

%description hook-libs
Hook libraries for %{name}.

%prep
%autosetup -n %{srcname}-%{version} -p1


%build
%cmake \
%if %{libs_only}
    -DBUILD_PLUGIN=OFF
%endif
%cmake_build


%install
%cmake_install


%if ! %{libs_only}
%files
%doc README.md
%license LICENSE
# OBS plugin
%{_libdir}/obs-plugins/linux-vkcapture.so
# OBS plugin data
%{_datadir}/obs/obs-plugins/linux-vkcapture/
%endif

%files hook-libs
%doc README.md
%license LICENSE
# Preload library wrappers
%{_bindir}/obs-gamecapture
%{_bindir}/obs-glcapture
%{_bindir}/obs-vkcapture
# Preload libraries
%{_libdir}/obs_glcapture/libobs_glcapture.so
%{_libdir}/libVkLayer_obs_vkcapture.so
%{_datadir}/vulkan/implicit_layer.d/obs_vkcapture_%{__isa_bits}.json

%changelog
* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Fri Nov 28 2025 Asahi Lina <lina@lina.yt> - 1.5.1-4
- Split off hook libraries into subpackage, build only those for i686

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Oct 05 2024 Neal Gompa <ngompa@fedoraproject.org> - 1.5.1-1
- Update to 1.5.1

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Sep 24 2023 Neal Gompa <ngompa@fedoraproject.org> - 1.4.3-3
- Fix obsoletes+provides of old package names and add -gamecapture virtual name

* Wed Sep 20 2023 Neal Gompa <ngompa@fedoraproject.org> - 1.4.3-2
- Fix build for 32-bit arches and exclude s390x

* Mon Sep 18 2023 Neal Gompa <ngompa@fedoraproject.org> - 1.4.3-1
- Update to 1.4.3

* Sun Sep 17 2023 Neal Gompa <ngompa@fedoraproject.org> - 1.4.2-1
- Initial package
