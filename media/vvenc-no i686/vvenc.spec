%global forgeurl0 https://github.com/fraunhoferhhi/vvenc
Version: 1.13.1
%global tag0 v%{version}

%forgemeta

Name:           vvenc
Release:        %autorelease
Summary:        The Fraunhofer Versatile Video Encoder

License:        BSD-3-Clause-Clear
URL:            %{forgeurl}
Source:         %{forgesource}

BuildRequires: cmake
BuildRequires: ninja-build
#ninja is faster
BuildRequires: gcc >= 5.0
BuildRequires: g++ >= 5.0
BuildRequires: simde-devel
BuildRequires: json-devel

Requires: %{name}-libs%{?_isa} = %{version}-%{release}


%description
VVenC, the Fraunhofer Versatile Video Encoder, is a fast and efficient
software H.266/VVC encoder implementation


%package devel
Summary: Header files for vvenc development

Requires: %{name}%{?_isa} = %{version}-%{release}
Requires:%{name}-libs%{?_isa} = %{version}-%{release}

%description devel
The vvenc-devel package contains the header files needed
to develop programs that use the vvenc.


%package libs
Summary: Library  files for vvenc

%description libs
The vvenc-libs package contains the library files

%prep
%forgesetup
#sanitize thirdparty
rm -rf ./thirdparty


%build
%cmake \
                -G Ninja \
                -DCMAKE_BUILD_TYPE=RelWithDebInfo \
                -DVVENC_ENABLE_THIRDPARTY_JSON=SYSTEM \
                -DVVENC_ENABLE_LINK_TIME_OPT=ON \
                -DVVENC_INSTALL_FULLFEATURE_APP=ON \
                -DCMAKE_SKIP_INSTALL_RPATH=1

%cmake_build


%install
%cmake_install


%check
%ctest


%files
%{_bindir}/vvencFFapp
%{_bindir}/vvencapp


%files devel
%{_libdir}/libvvenc.so
%{_libdir}/pkgconfig/libvvenc.pc
%{_libdir}/cmake/vvenc/
%{_includedir}/vvenc/


%files libs
%license LICENSE.txt
%doc README.md
%doc changelog.txt
%doc AUTHORS.md
%{_libdir}/libvvenc.so.1.*

%changelog
%autochangelog
