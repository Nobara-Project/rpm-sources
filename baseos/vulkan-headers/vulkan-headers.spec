%global __python %{__python3}
Name:           vulkan-headers
Version:        1.3.280
Release:        1%{?dist}
Summary:        Vulkan Header files and API registry

License:        ASL 2.0
URL:            https://github.com/KhronosGroup/Vulkan-Headers
Source0:        %url/archive/v%{version}.tar.gz

BuildRequires:  cmake3 gcc
BuildArch:      noarch       

%description
Vulkan Header files and API registry

%prep
%autosetup -n Vulkan-Headers-%{version} -p1


%build
%cmake3 -DCMAKE_INSTALL_LIBDIR=%{_libdir} .
%cmake_build


%install
%cmake_install


%files
%doc README.md
%{_includedir}/vulkan/
%{_includedir}/vk_video/
%dir %{_datadir}/vulkan/
%{_datadir}/vulkan/registry/
%dir %{_datadir}/cmake/VulkanHeaders
%{_datadir}/cmake/VulkanHeaders/*.cmake

%changelog

