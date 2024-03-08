Name:           obs-studio-plugin-media-playlist-source
Version:        0.0.4
Release:        1%{?dist}
Summary:        An OBS Plugin that serves as an alternative to VLC Video Source. It uses the Media Source internally.

License:        GPL-2.0-or-later
URL:            https://github.com/CodeYan01/media-playlist-source
Source0:        https://github.com/CodeYan01/media-playlist-source/archive/refs/tags/0.0.4.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++

BuildRequires:  cmake(libobs)
BuildRequires:  pkgconfig(glib-2.0)

Supplements:    obs-studio%{?_isa}

%description
%{name}.

%prep
%autosetup -n media-playlist-source-0.0.4 -p1


%build
%cmake
%cmake_build


%install
%cmake_install

mkdir -p %{buildroot}%{_libdir}/obs-plugins/
mkdir -p %{buildroot}%{_datadir}/obs/obs-plugins/

mv %{buildroot}/usr/obs-plugins/64bit/media-playlist-source.so %{buildroot}%{_libdir}/obs-plugins/
mv %{buildroot}/usr/data/obs-plugins/media-playlist-source/ %{buildroot}%{_datadir}/obs/obs-plugins/

%files
%license LICENSE
%{_libdir}/obs-plugins/media-playlist-source*
%{_datadir}/obs/obs-plugins/media-playlist-source*

%changelog
* Thu Nov 02 2023 Neal Gompa <ngompa@fedoraproject.org> - 0~git20231023.3c0978b-1
- Update to new git snapshot

* Sat Sep 16 2023 Neal Gompa <ngompa@fedoraproject.org> - 0~git20230910.a2bc475-2
- Use webkit2gtk-4.0 API module for older RHEL

* Mon Sep 11 2023 Neal Gompa <ngompa@fedoraproject.org> - 0~git20230910.a2bc475-1
- Update to new git snapshot

* Fri Sep 08 2023 Neal Gompa <ngompa@fedoraproject.org> - 0~git20201202.0e32b92-4
- Add patch to fix load path for webkitgtk helper (RH#2225973)

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0~git20201202.0e32b92-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed May 03 2023 Neal Gompa <ngompa@fedoraproject.org> - 0~git20201202.0e32b92-2
- Adapt for Fedora

* Wed Dec 28 2022 Neal Gompa <ngompa@fedoraproject.org> - 0~git20201202.0e32b92-1
- Initial packaging
