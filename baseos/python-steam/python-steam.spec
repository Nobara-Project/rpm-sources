## START: Set by rpmautospec
## (rpmautospec version 0.3.1)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 1;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

%global pypi_name steam

Name:       python-%{pypi_name}
Version:    1.4.4
Release:    %autorelease
Summary:    Python package for interacting with Steam
BuildArch:  noarch

License:    MIT
URL:        https://github.com/ValvePython/steam

# Tests works only woth GitHub sources
Source0:    %{url}/archive/v%{version}/%{pypi_name}-%{version}.tar.gz

BuildRequires: python3-devel
BuildRequires: python3dist(setuptools)
BuildRequires: python3-pyyaml >= 5.4

BuildRequires: python3dist(cachetools) >= 3.0.0
BuildRequires: python3dist(gevent-eventemitter) >= 2.1
BuildRequires: python3dist(gevent) >= 1.3.0
BuildRequires: python3dist(mock)
BuildRequires: python3dist(protobuf) >= 3.0.0
BuildRequires: python3dist(pycryptodomex) >= 3.7.0
BuildRequires: python3dist(pytest-cov)
BuildRequires: python3dist(pytest)
BuildRequires: python3dist(requests) >= 2.9.1
BuildRequires: python3dist(vcrpy)
BuildRequires: python3dist(vdf) >= 3.3

# For client
Requires:   python3dist(gevent-eventemitter) >= 2.1
Requires:   python3dist(gevent) >= 1.3.0
Requires:   python3dist(protobuf) >= 3.0.0

%global _description %{expand:
A python module for interacting with various parts of Steam.

Features

  - SteamClient - communication with the steam network based on gevent.
  - CDNClient - access to Steam content depots
  - WebAuth - authentication for access to store.steampowered.com and
    steamcommunity.com
  - WebAPI - simple API for Steam's Web API with automatic population of
    interfaces
  - SteamAuthenticator - enable/disable/manage two factor authentication for
    Steam accounts
  - SteamID - convert between the various ID representations with ease
  - Master Server Query Protocol - query masters servers directly or via
    SteamClient}

%description %{_description}


%package -n python3-%{pypi_name}
Summary:    %{summary}
%{?python_provide:%python_provide python3-%{pypi_name}}

%description -n python3-%{pypi_name} %{_description}


%prep
%autosetup -n %{pypi_name}-%{version}

%build
%py3_build


%install
%py3_install


%check
%{python3} -m pytest -v


%files -n python3-%{pypi_name}
%license LICENSE
%doc README.rst CHANGES.md
%{python3_sitelib}/%{pypi_name}/
%{python3_sitelib}/%{pypi_name}-%{version}-*.egg-info


%changelog
* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Oct 10 2022 Artem Polishchuk <ego.cordatus@gmail.com> - 1.4.3-1
- chore(update): 1.4.3

* Thu Oct 06 2022 Artem Polishchuk <ego.cordatus@gmail.com> - 1.4.1-1
- chore(update): 1.4.1

* Wed Oct 05 2022 Artem Polishchuk <ego.cordatus@gmail.com> - 1.4.0-1
- chore(update): 1.4.0

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jun 14 2022 Python Maint <python-maint@redhat.com> - 1.3.0-2
- Rebuilt for Python 3.11

* Tue May 17 2022 Artem Polishchuk <ego.cordatus@gmail.com> - 1.3.0-1
- chore(update): 1.3.0

* Sun May 08 2022 Artem Polishchuk <ego.cordatus@gmail.com> - 1.2.1-1
- chore(update): 1.2.1

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jun 23 2021 Artem Polishchuk <ego.cordatus@gmail.com> - 1.2.0-1
- build(update): 1.2.0

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.1.1-2
- Rebuilt for Python 3.10

* Mon Jan 25 2021 Artem Polishchuk <ego.cordatus@gmail.com> - 1.1.1-1
- build: Update to 1.1.1 and polish to conform Fedora guidelines

* Wed Sep 16 2020 gasinvein <gasinvein@gmail.com> - 1.0.2-0.1
- Initial package

