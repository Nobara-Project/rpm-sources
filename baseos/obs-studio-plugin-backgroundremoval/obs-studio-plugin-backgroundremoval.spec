Name:           obs-studio-plugin-backgroundremoval
Version:        1.1.13
Release:        1%{?dist}
Summary:        A plugin for OBS Studio that allows you to replace the background in portrait images and video, as well as enhance low-light scenes.

License:        GPL-2.0-or-later
URL:            https://github.com/occ-ai/obs-backgroundremoval
Source0:        https://github.com/occ-ai/obs-backgroundremoval/archive/refs/tags/%{version}.tar.gz
# ROCM support
Patch0:         545.patch
BuildRequires:  cmake
BuildRequires:  gcc-c++

BuildRequires:  cmake(libobs)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  curl-devel
BuildRequires:  opencv-devel
BuildRequires:  onnxruntime-devel

# ROCM
#BuildRequires:  rocm-hip-sdk
#BuildRequires:  miopen-hip-devel
#BuildRequires:  roctracer-devel
#BuildRequires:  rocm-dev

Requires:  opencv-core
Requires:  onnxruntime
# Requires:  rocm-meta
Supplements:    obs-studio%{?_isa}

%description
%{name}.

%prep
%autosetup -n obs-backgroundremoval-%{version} -p1


%build
%cmake \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_POSITION_INDEPENDENT_CODE=ON \
  -DENABLE_FRONTEND_API=ON \
  -DENABLE_QT=OFF \
  -DENABLE_ROCM=OFF \
  -DUSE_SYSTEM_ONNXRUNTIME=ON \
  -DDISABLE_ONNXRUNTIME_GPU=ON \
  -DUSE_SYSTEM_OPENCV=ON
%cmake_build


%install
%cmake_install --prefix /usr

%files
%license LICENSE
%{_libdir}/obs-plugins/obs-backgroundremoval*
%{_datadir}/obs/obs-plugins/obs-backgroundremoval*

%changelog
* Wed Jun 05 2024 Tom Crider <gloriouseggroll@gmail.com>
- Initial build 1.1.13
