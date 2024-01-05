%global srcname obs-webkitgtk
%global commit 3c0978b399512440afdd4dccf744f2ffa0821317
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global commitdate 20231023

Name:           obs-studio-plugin-webkitgtk
Version:        0~git%{commitdate}.%{shortcommit}
Release:        5%{?dist}
Summary:        OBS Browser source plugin based on WebKitGTK

License:        GPL-2.0-or-later
URL:            https://github.com/fzwoch/obs-webkitgtk
Source0:        %{url}/archive/%{commit}/%{srcname}-%{shortcommit}.tar.gz
Patch0:         0001-Use-Browser-Source-WebKitGTK-plugin-name-to-keep-uni.patch

BuildRequires:  meson
BuildRequires:  gcc

BuildRequires:  pkgconfig(libobs)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gtk+-3.0)
%if 0%{?rhel} && 0%{?rhel} < 10
BuildRequires:  pkgconfig(webkit2gtk-4.0)
%else
BuildRequires:  pkgconfig(webkit2gtk-4.1)
%endif

Supplements:    obs-studio%{?_isa}

# Replace older packages
Obsoletes:      obs-webkitgtk < %{version}-%{release}
Provides:       obs-webkitgtk = %{version}-%{release}
Provides:       obs-webkitgtk%{?_isa} = %{version}-%{release}

%description
%{name}.

%prep
%autosetup -n %{srcname}-%{commit}

%if 0%{?rhel} && 0%{?rhel} < 10
# Use webkit2gtk-4.0 API module for older RHEL
sed -e 's/webkit2gtk-4.1/webkit2gtk-4.0/g' -i meson.build
%endif


%build
%meson
%meson_build


%install
%meson_install


%files
%license LICENSE
%{_libexecdir}/obs-plugins/%{srcname}*
%{_libdir}/obs-plugins/%{srcname}*


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
