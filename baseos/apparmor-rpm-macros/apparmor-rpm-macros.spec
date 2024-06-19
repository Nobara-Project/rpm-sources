#
# spec file for package apparmor-rpm-macros
#
# Copyright (c) 2024 SUSE LLC
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#


Name:           apparmor-rpm-macros
Version:        1.0
Release:        24.4
Summary:        RPM macros used to setup apparmor profiles
License:        LGPL-2.1-or-later
Group:          Development/Tools/Other
URL:            https://bugs.launchpad.net/apparmor
Source:         macros.apparmor
Requires:       coreutils
BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%define  macrodir /usr/lib/rpm/macros.d

%description
Package that provides RPM macros used to setup apparmor profiles for packaging.

%prep

%build

%install
mkdir -p %{buildroot}%{macrodir}
install -m644 %{S:0} %{buildroot}%{macrodir}/

%files
%defattr(-,root,root)
%{macrodir}/macros.apparmor

%changelog
* Tue Feb 20 2024 Frederic Crozat <fcrozat@suse.com>
- Update macro to detect when installing in chroot
  (transactional-update) and avoid calling apparmor_parser.
* Sat Jun  3 2023 Georg Pfuetzenreuter <georg.pfuetzenreuter@suse.com>
- No longer suppress stderr
* Mon Aug 19 2019 kukuk@suse.de
- Don't assume systemctl is already installed or available at all.
- Files in /usr/lib/rpm/macros.d are no config files
* Wed May  8 2019 Christian Boltz <suse-beta@cboltz.de>
- move macros.apparmor from /etc/rpm/ to /usr/lib/rpm/macros.d/
* Wed Feb 28 2018 tbechtold@suse.com
- Check if apparmor is active before reloading a profile (bsc#1083226)
  Otherwise a package using the %%apparmor_reload macro in %%post
  automatically enables the profile even if apparmor itself is
  not active.
* Sat Aug 26 2017 suse-beta@cboltz.de
- %%apparmor_reload: skip and regenerate cache to make sure the latest
  profile gets always used (even if the existing cache is newer)
* Wed Jan 11 2017 jengelh@inai.de
- RPM group fix
* Wed Jul 13 2016 ushamim@linux.com
- Initial creation of macro, only contains %%apparmor_reload
