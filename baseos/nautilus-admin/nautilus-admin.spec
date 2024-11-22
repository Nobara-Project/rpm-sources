%global git_commit_hash 3cad8dff209b65653988f7f596a05ccf4cbe2a59

Name:           nautilus-admin
Version:        1.2.0
Release:        1%{?dist}
Summary:        Extension for Nautilus to do administrative operations

License:        GPL-3.0
URL:            https://github.com/MacTavishAO/nautilus-admin-gtk4 
Source0:        https://github.com/MacTavishAO/nautilus-admin-gtk4/archive/%{git_commit_hash}.zip

BuildRequires:  cmake
BuildRequires:  gettext
Requires:       python3
Requires:       nautilus-python
Requires:       gedit
Requires:       nautilus
BuildArch:      noarch


%description
Nautilus Admin is a simple Python extension for the Nautilus file
manager that adds some administrative actions to the right-click menu:
* Open as Administrator: opens a folder in a new Nautilus window running
with administrator (root) privileges.
* Edit as Administrator: opens a file in a Gedit window running with
administrator (root) privileges.

Please remember to restart Nautilus after installation.
You can use `nautilus -q` command.


%prep
%autosetup -n %{name}-gtk4-%{git_commit_hash}


%build
%cmake
%cmake_build


%install
%cmake_install
%find_lang %{name}


%files -f %{name}.lang
/%{_datadir}/nautilus-python/extensions/%{name}.py


%changelog
* Sun Jan 10 2021 Tomasz Gąsior
- Change upstream from abandoned repository to fork,
  making this package working with current Python.
* Mon Nov 18 2019 Tomasz Gąsior
- Initial
