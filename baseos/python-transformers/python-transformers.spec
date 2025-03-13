Name: python-transformers
Version: 4.49.0
Release: 1%{?dist}
Summary: State-of-the-art Machine Learning for JAX, PyTorch and TensorFlow

Group: Development/Libraries
License: MIT
URL: https://github.com/huggingface/transformers
Source0: https://files.pythonhosted.org/packages/source/t/transformers/transformers-%{version}.tar.gz
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
Provides: python-transformers
Provides: python3-transformers


%description
State-of-the-art Machine Learning for JAX, PyTorch and TensorFlow

%prep
%autosetup -n transformers-%{version}

%build
python3 -m build --wheel --no-isolation

%install
python3 -m pip install --no-deps --prefix=%{_prefix} --root=%{buildroot} dist/*.whl

%files
%doc README.md
%license LICENSE
%{_bindir}/*
%{python3_sitelib}/transformers*

%changelog
