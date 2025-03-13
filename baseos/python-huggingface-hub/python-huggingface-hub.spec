Name: python-huggingface-hub
Version: 0.29.1
Release: 1%{?dist}
Summary: The official Python client for the Huggingface Hub.

Group: Development/Libraries
License: Apache Software License
URL: https://github.com/huggingface/huggingface_hub
Source0: https://files.pythonhosted.org/packages/source/h/huggingface_hub/huggingface_hub-%{version}.tar.gz
BuildArch: noarch

BuildRequires: python3-build
BuildRequires: python3-setuptools
BuildRequires: python3-wheel
BuildRequires: python3-pip
BuildRequires: python3-pdm-backend
BuildRequires: python3-devel

Requires: python3-aiohttp
Requires: python3-numpy
Requires: python3-pydantic
Requires: python3-pyyaml
Requires: python3-requests
Requires: python3-sqlalchemy
Requires: python3-tenacity
Provides: python-huggingface-hub
Provides: python3-huggingface-hub


%description
The official Python client for the Huggingface Hub.

%prep
%autosetup -n huggingface_hub-%{version}

%build
python3 -m build --wheel --no-isolation

%install
python3 -m pip install --no-deps --prefix=%{_prefix} --root=%{buildroot} dist/*.whl

%files
%doc README.md
%license LICENSE
%{_bindir}/*
%{python3_sitelib}/huggingface_hub*

%changelog
