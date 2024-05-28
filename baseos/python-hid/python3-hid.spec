%global pypi_name hid
%global pypi_version 1.0.6

Name:           python-%{pypi_name}
Version:        %{pypi_version}
Release:        1%{?dist}
Summary:        ctypes bindings for hidapi

License:        MIT
URL:            https://pypi.org/project/hid/
Source0:        %{pypi_source}

BuildRequires:  python3-devel
BuildRequires:  python3dist(setuptools)

Requires: hidapi

%global debug_package %{nil}

%description
ctypes bindings for hidapi

%package -n     python3-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pypi_name}}

%description -n python3-%{pypi_name}
ctypes bindings for hidapi

%prep
%autosetup -n %{pypi_name}-%{pypi_version}

%build
%py3_build

%install
%py3_install

%files -n python3-%{pypi_name}
%doc README.md
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{pypi_version}-py%{python3_version}.egg-info

%changelog
* Mon Aug 01 2022 <james@twiddlingbits.net> - 1.0.5-1
- Initial package
