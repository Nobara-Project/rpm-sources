Name: python-tokenizers
Version: 0.21.0
Release: 1%{?dist}
Summary: Provides an implementation of today's most used tokenizers, with a focus on performance and versatility.

Group: Development/Libraries
License: MIT
URL: https://github.com/huggingface/tokenizers
Source0: https://files.pythonhosted.org/packages/source/t/tokenizers/tokenizers-%{version}.tar.gz

BuildRequires: python3-build
BuildRequires: python3-setuptools
BuildRequires: python3-wheel
BuildRequires: python3-pip
BuildRequires: python3-pdm-backend
BuildRequires: python3-devel
BuildRequires: python3-maturin
BuildRequires: cargo
BuildRequires: gcc-g++

Requires: python3-aiohttp
Requires: python3-numpy
Requires: python3-pydantic
Requires: python3-pyyaml
Requires: python3-requests
Requires: python3-sqlalchemy
Requires: python3-tenacity
Provides: python-tokenizers
Provides: python3-tokenizers


%description
Provides an implementation of today's most used tokenizers, with a focus on performance and versatility.

%prep
%autosetup -n tokenizers-%{version}

%build
python3 -m build --wheel --no-isolation

%install
python3 -m pip install --no-deps --prefix=%{_prefix} --root=%{buildroot} dist/*.whl

%files
%{python3_sitearch}/tokenizers*

%changelog
