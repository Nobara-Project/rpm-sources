# bytecompile with Python 3
%global __python %{__python3}

%define version_string 0.2.0
%global build_timestamp 11.%(date +"%Y%m%d")
%global rel_build %{build_timestamp}.%{shortcommit}%{?dist}

# vulkan capture version and commit
%global commit fc72792835773d958f7dad801cff6b5ee766c27d
%global shortcommit %(c=%{commit}; echo ${c:0:7})


Name:           obs-studio-gstreamer-vaapi
Version:        %{version_string}
Release:        %{rel_build}
Summary:        Gstreamer VAAPI encoder for OBS

License:        GPLv2+
URL:            https://github.com/fzwoch/obs-vaapi
Source0:        https://github.com/fzwoch/obs-vaapi/archive/%{commit}/obs-vaapi-%{shortcommit}.tar.gz
Patch0:		encoder_rename.patch
Patch1:		revert_lib_build_path_for_nobara.patch
BuildRequires:  meson
BuildRequires:  gcc
BuildRequires:  obs-studio-devel
BuildRequires:  gstreamer1-devel
BuildRequires:  gstreamer1-plugins-base-devel
BuildRequires:  libappstream-glib
BuildRequires:  pciutils-devel
Requires:	obs-studio
Requires:	obs-studio-libs
Requires:	gstreamer1-vaapi
Requires:	gstreamer1-plugins-bad-free-extras



%description
OBS plugin for Gstreamer VAAPI encoder for Linux.
Requires OBS 27.

%prep
%setup -n obs-vaapi-%{commit} -q
patch -Np1 < %{PATCH0}
patch -Np1 < %{PATCH1}

# Remove -Werror from compiler flags
sed -i '/-Werror/d' meson.build

%build
%meson --buildtype=release \
  %{nil}
%{meson_build}

%install
%meson_install

%files
%{_libdir}/obs-plugins/obs-vaapi.so

%changelog
* Thu Mar 10 2022 Thomas Crider <fedorauser@fedoraproject.org> - 0.10.1-0.1
- Initial .spec file
