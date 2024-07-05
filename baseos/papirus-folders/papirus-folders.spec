#
# spec file for package papirus-folders
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


Name:           papirus-folders
Version:        1.13.1
Release:        0
Summary:        Change folders color of Papirus icon theme
License:        MIT
URL:            https://github.com/PapirusDevelopmentTeam/papirus-folders
Source:         https://github.com/PapirusDevelopmentTeam/papirus-folders/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildRequires:  fdupes
Requires:       coreutils
Requires:       papirus-icon-theme
BuildArch:      noarch

%description
Papirus Folders is a command-line utility that allows changing the color of folders in Papirus icon theme.
Type 'papirus-folders --help' to see all options available.

%prep
%autosetup

%build

%install
mkdir -p %{buildroot}%{_bindir}
install -m 755 papirus-folders %{buildroot}%{_bindir}/papirus-folders
%fdupes %{buildroot}

%files
%doc README.md
%license LICENSE
%{_bindir}/papirus-folders

%changelog

