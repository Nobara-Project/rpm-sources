Name:           neofetch
Version:        7.1.0
Release:        13%{?dist}
Summary:        CLI system information tool written in Bash

License:        MIT
URL:            https://github.com/dylanaraps/%{name}
Source0:        %{URL}/archive/%{version}/%{name}-%{version}.tar.gz
Patch0:         nobara_logo.patch

BuildArch:      noarch
BuildRequires:  make
Requires:       bash >= 3.2
Requires:       bind-utils
Requires:       catimg
Requires:       coreutils
Requires:       gawk
Requires:       grep
Requires:       pciutils
Recommends:     caca-utils
Recommends:     ImageMagick
Recommends:     jp2a
Recommends:     w3m-img
Recommends:     xdpyinfo
Recommends:     xprop
Recommends:     xrandr
Recommends:     xrdb
Recommends:     xwininfo

%description
Neofetch displays information about your system next to an image,
your OS logo, or any ASCII file of your choice. The main purpose of Neofetch
is to be used in screenshots to show other users what OS/distribution you're
running, what theme/icons you're using and more.

%prep
%autosetup
sed 's,/usr/bin/env bash,/usr/bin/bash,g' -i neofetch

%build

%install
%make_install

%files
%{_bindir}/%{name}
%license LICENSE.md
%doc README.md
%{_mandir}/man1/%{name}.1*

%changelog
* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 7.1.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 7.1.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 7.1.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 7.1.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild


* Wed Oct 06 2021 K. de Jong <keesdejong@fedoraproject.org> - 7.1.0-6
- Applied patch to update the Fedora logo

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 7.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild


* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 7.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Oct 28 2020 K. de Jong <keesdejong@fedoraproject.org> - 7.1.0-3
- catimg package available again #1878514

* Tue Aug 25 2020 K. de Jong <keesdejong@fedoraproject.org> - 7.1.0-2
- catimg dependency removed, scheduled for removal #1872247

* Mon Aug 03 2020 K. de Jong <keesdejong@fedoraproject.org> - 7.1.0-1
- new version

* Tue Jul 28 2020 Adam Jackson <ajax@redhat.com> - 7.0.0-3
- Recommend xdpyinfo xprop xrandr xrdb xwininfo, not xorg-x11-{server-,}utils

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun Mar 08 2020 K. de Jong <keesdejong@fedoraproject.org> - 7.0.0-1
- New upstream release

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 6.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Sep 06 2019 K. de Jong <keesdejong@fedoraproject.org> - 6.1.0-1
- New upstream release

* Sat Aug 03 2019 K. de Jong <keesdejong@fedoraproject.org> - 6.0.0-4
- Red Hat Bugzilla - Bug 1736808

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 09 2019 K. de Jong <keesdejong@fedoraproject.org> - 6.0.0-1
- New upstream release

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 20 2018 K. de Jong <keesdejong@fedoraproject.org> - 5.0.0-1
- New upstream release

* Tue Jun 12 2018 K. de Jong <keesdejong@fedoraproject.org> - 4.0.2-1
- New upstream release
- Cleaned up dependencies

* Fri Apr 06 2018 Kees de Jong <keesdejong@fedoraproject.org> - 3.4.0-1
- New upstream release

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Feb 13 2017 Kees de Jong <keesdejong@fedoraproject.org> - 3.3.0-1
- Initial package
