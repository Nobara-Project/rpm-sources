%global with_python3 1

%global scrname  puremagic

Name:           python-%{scrname}
Version:        1.11
Release:        1%{?dist}
Summary:        identify a file based off it's magic numbers

License:        MIT
URL:            https://github.com/cdgriffith/puremagic
Source0:        https://github.com/cdgriffith/puremagic/archive/refs/tags/%{version}.tar.gz
Buildarch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

%description
puremagic is a pure python module that will identify a file based off it's magic numbers.

%if 0%{?with_python3}
%package -n python3-%{scrname}
Summary:        identify a file based off it's magic numbers

Requires:       python3
BuildArch:      noarch

%description -n python3-%{scrname}
puremagic is a pure python module that will identify a file based off it's magic numbers.
%endif

%prep
%setup -q -n %{scrname}-%{version}
rm -rf %{srcname}.egg-info
sed -i -e '/^#!\//, 1d' *.py

%build
%{__python3} setup.py build

%install
%{__python3} setup.py install --skip-build --root %{buildroot}

#%files

%files -n python3-%{scrname}
%{python3_sitelib}/%{scrname}
%{python3_sitelib}/%{scrname}*.egg-info
#%{python3_sitelib}/__pycache__/%{scrname}*

%changelog
* Sat Nov 27 2021 josef radinger <cheese@nosuchhost.net> - 1.11-1
- bump version to correct wrong dependency on python-argparse (which is now on python itself).
  thanks king.br@gmail.com for creating http://www.nosuchhost.net/bugzilla/show_bug.cgi?id=146

* Mon Sep 20 2021 josef radinger <cheese@nosuchhost.net> - 1.10-1
- bump version

