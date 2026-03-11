%global debug_package %{nil}
%global openvr_ver 2.12.14

Name:           opentrack
Version:        2026.1.0
Release:        1%{?dist}
Summary:        Head tracking software for MS Windows, Linux, and Apple OSX

License:        ISC and BSD-3-Clause
URL:            https://github.com/%{name}/%{name}
Source0:        %{url}/archive/refs/tags/%{name}-%{version}.tar.gz
Source1:        https://github.com/ValveSoftware/openvr/archive/refs/tags/v%{openvr_ver}.tar.gz
Patch0:         fix-qt6-resolve.patch

ExcludeArch:    %{ix86}

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  faust
BuildRequires:  faust-osclib-devel
BuildRequires:  libevdev-devel
BuildRequires:  librealsense-devel
BuildRequires:  libX11-devel
BuildRequires:  libXtst-devel
BuildRequires:  ninja-build
BuildRequires:  onnxruntime-devel
BuildRequires:  opencv-devel
BuildRequires:  procps-ng-devel
BuildRequires:  qt6-qt5compat-devel
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qtbase-private-devel
BuildRequires:  qt6-qtserialport-devel
BuildRequires:  qt6-qttools-devel
BuildRequires:  winehq-staging
BuildRequires:  wine-staging-devel

Requires:       qt6-qtbase
Requires:       qt6-qt5compat
Requires:       qt6-qtserialport
Requires:       opencv
Requires:       faust-osclib
Requires:       onnxruntime

%description
opentrack is a program for tracking user's head rotation and transmitting it to flight simulation software and military-themed video games

%prep
%autosetup -n %{name}-%{name}-%{version} -p1
tar -xf %{SOURCE1}

# Copy the OpenVR license so we can include it in the RPM
cp openvr-%{openvr_ver}/LICENSE LICENSE-OpenVR

mkdir -p external-include/include/oscpack/osc
mkdir -p external-include/lib
ln -s /usr/include/faust/osc/*.h external-include/include/oscpack/osc/
ln -s /usr/share/faust/osclib/oscpack/osc/*.h external-include/include/oscpack/osc/
ln -s /usr/lib/libOSCFaust.so external-include/lib/liboscpack.so

%build
%cmake -G Ninja \
    -DCMAKE_BUILD_TYPE=Release \
    -DSDK_HIERARCHY=ON \
    -DSDK_WINE=ON \
    -DSDK_LIBDIR=%{_lib}/%{name} \
    -DSDK_PLUGINDIR=%{_lib}/%{name} \
    -DSDK_OSCPACK=$PWD/external-include \
    -DSDK_ONNX=ON \
    -DONNXRuntime_DIR=%{_libdir} \
    -DONNXRuntime_INCLUDE_DIRS=%{_includedir}/onnxruntime \
    -DSDK_OPENCV=ON \
    -DSDK_VALVE_STEAMVR=$PWD/openvr-%{openvr_ver} \
    -DOPENCV_PREFIX=%{_prefix}

%cmake_build

%install
%cmake_install

mkdir -p %{buildroot}%{_libdir}/%{name}
cp openvr-%{openvr_ver}/bin/linux64/libopenvr_api.so %{buildroot}%{_libdir}/%{name}/

# Generate a desktop file manually since it's missing from source
mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/opentrack.desktop <<EOF
[Desktop Entry]
Type=Application
Name=Opentrack
Comment=Head tracking for games and simulation
Exec=opentrack
Icon=opentrack
Terminal=false
Categories=Game;Settings;
EOF

%files
%doc %{_datadir}/doc/%{name}/
%license OPENTRACK-LICENSING.txt WARRANTY.txt LICENSE-OpenVR
%{_bindir}/%{name}
%{_libexecdir}/%{name}/
%{_libdir}/%{name}/libopenvr_api.so
%{_datadir}/%{name}/
%{_datadir}/applications/%{name}.desktop

%changelog
* Wed Mar 11 2026 LionHeartP <LionHeartP@proton.me> - 2026.1.0-1
- Initial Nobara package
