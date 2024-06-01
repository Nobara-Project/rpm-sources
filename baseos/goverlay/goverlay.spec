## START: Set by rpmautospec
## (rpmautospec version 0.3.0)
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 2;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec
# commit d8e8e9e3a0a2d7c0127231c63b8ec355a1e2316b

Name:           goverlay
Version:        1.1.1
Release:        %autorelease
Epoch:          2
Summary:        Project that aims to create a Graphical UI to help manage Linux overlays
ExclusiveArch:  %{fpc_arches}

License:        GPLv3+
URL:            https://github.com/benjamimgois/goverlay
Source0:        %{url}/archive/%{version}/%{name}-main.tar.gz

Patch0:         goverlay-enable-debuginfo-generation.patch

BuildRequires:  desktop-file-utils
BuildRequires:  fpc-srpm-macros
BuildRequires:  lazarus
BuildRequires:  lazarus-lcl-qt6
BuildRequires:  libappstream-glib
BuildRequires:  libglvnd-devel
BuildRequires:  make

Requires:       hicolor-icon-theme
Requires:       mangohud%{?_isa}
Requires:       mesa-libGLU
Requires:       qt6pas%{?_isa}
Requires:       /usr/bin/lsb_release

# git - Clone reshade repository
Recommends:     git%{?_isa}

Recommends:     mesa-demos%{?_isa}
Recommends:     vkBasalt%{?_isa}
Recommends:     vulkan-tools%{?_isa}

%description
GOverlay is an open source project aimed to create a Graphical UI to manage
Vulkan/OpenGL overlays. It is still in early development, so it lacks a lot of
features.

This project was only possible thanks to the other maintainers and
contributors that have done the hard work. I am just a Network Engineer that
really likes Linux and Gaming.


%prep
%autosetup -p1 -n %{name}-%{version}


%build
%set_build_flags
%make_build


%install
%make_install prefix=%{_prefix}


%check
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/*.xml
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop


%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/*/*.png
%{_libexecdir}/%{name}
%{_mandir}/man1/*.1*
%{_metainfodir}/*.xml


%changelog
* Mon Nov 14 2022 Artem Polishchuk <ego.cordatus@gmail.com> 0.9-2
- build: Add mesa-libGLU dep (#2142356)

* Fri Jul 22 2022 Artem Polishchuk <ego.cordatus@gmail.com> 0.9-1
- chore(update): 0.9

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Mar 05 2022 Artem Polishchuk <ego.cordatus@gmail.com> - 0.8.1-1
- chore(update): 0.8.1

* Fri Feb 25 2022 Artem Polishchuk <ego.cordatus@gmail.com> - 0.8-1
- chore(update): 0.8

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Dec 16 2021 Artem Polishchuk <ego.cordatus@gmail.com> - 0.7.1-1
- chore(update): 0.7.1

* Mon Nov 29 2021 Artem Polishchuk <ego.cordatus@gmail.com> - 0.7-1
- chore(update): 0.7

* Wed Oct 27 2021 Artem Polishchuk <ego.cordatus@gmail.com> - 0.6.4-1
- chore(update): 0.6.4

* Mon Sep 13 2021 Artem Polishchuk <ego.cordatus@gmail.com> - 0.6.3-1
- build(update): 0.6.3

* Tue Aug 24 2021 Artem Polishchuk <ego.cordatus@gmail.com> - 0.6.2-1
- build(update): 0.6.2 | Thanks @zawertun for help with this update

* Wed Jul 28 2021 Artem Polishchuk <ego.cordatus@gmail.com> - 0.6.1-1
- build(update): 0.6.1

* Fri Jul 23 2021 Artem Polishchuk <ego.cordatus@gmail.com> - 0.6-1
- build(update): 0.6

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sun Jun 06 2021 Artem Polishchuk <ego.cordatus@gmail.com> - 0.5.1-1
- build(update): 0.5.1

* Sat Mar 20 2021 Artem Polishchuk <ego.cordatus@gmail.com> - 0.5-1
- build(update): 0.5

* Thu Feb 04 2021 Artem Polishchuk <ego.cordatus@gmail.com> - 0.4.4-1
- build(update): 0.4.4

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sun Dec 20 2020 Artem Polishchuk <ego.cordatus@gmail.com> - 0.4.3-1
- build(update): 0.4.3

* Fri Nov 20 2020 Artem Polishchuk <ego.cordatus@gmail.com> - 0.4.2-2
- build(add dep): git

* Fri Nov 20 2020 Artem Polishchuk <ego.cordatus@gmail.com> - 0.4.2-1
- build(update): 0.4.2

* Fri Nov  6 2020 Artem Polishchuk <ego.cordatus@gmail.com> - 0.4-2
- build(recommends): vkBasalt

* Tue Nov  3 2020 Artem Polishchuk <ego.cordatus@gmail.com> - 0.4-1
- Update to 0.4

* Thu Sep 10 2020 Artem Polishchuk <ego.cordatus@gmail.com> - 0.3.8-1
- Update to 0.3.8

* Tue Aug 04 2020 Artem Polishchuk <ego.cordatus@gmail.com> - 0.3.7-1
- Update 0.3.7

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 20 2020 Artem Polishchuk <ego.cordatus@gmail.com> - 0.3.6-1
- Update 0.3.6

* Mon Jun 22 2020 Artem Polishchuk <ego.cordatus@gmail.com> - 0.3.5-1
- Update 0.3.5

* Sat Jun 20 2020 Artem Polishchuk <ego.cordatus@gmail.com> - 0.3.4-1
- Update 0.3.4

* Fri May 29 2020 Artem Polishchuk <ego.cordatus@gmail.com> - 0.3.3-1
- Update 0.3.3

* Fri Apr 10 2020 Artem Polishchuk <ego.cordatus@gmail.com> - 0.3.1-1
- Update 0.3.1

* Sat Apr 04 2020 Artem Polishchuk <ego.cordatus@gmail.com> - 0.3-1
- Update 0.3
- Add few weak deps
- Update description to sync with upstream

* Sun Mar 29 2020 Artem Polishchuk <ego.cordatus@gmail.com> - 0.2.4-1
- Update 0.2.4

* Thu Mar 26 2020 Artem Polishchuk <ego.cordatus@gmail.com> - 0.2.3-1
- Update 0.2.3

* Mon Mar 16 2020 Artem Polishchuk <ego.cordatus@gmail.com> - 0.2.1-2
- Enable debuinfo generation. Thanks to Artur Iwicki for help with packaging.

* Sat Mar 14 2020 Artem Polishchuk <ego.cordatus@gmail.com> - 0.2.1-1
- Initial package

