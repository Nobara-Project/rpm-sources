Name:           python-accelerate
Version:        1.4.0
Release:        1%{?dist}
# Fill in the actual package summary to submit package to Fedora
Summary:        Accelerate

# Check if the automatically generated License and its spelling is correct for Fedora
# https://docs.fedoraproject.org/en-US/packaging-guidelines/LicensingGuidelines/
License:        Apache-2.0
URL:            https://github.com/huggingface/accelerate
Source:         %{pypi_source accelerate}

BuildArch:      noarch
BuildRequires:  python3-devel
# For passing the test suite
BuildRequires:	python3-rich
BuildRequires:	pyproject-rpm-macros
BuildRequires:	python3-packaging
BuildRequires:	python3-pip
BuildRequires:	python3-setuptools
BuildRequires:	python3-wheel
BuildRequires:	python3-safetensors

# Fill in the actual package description to submit package to Fedora
%global _description %{expand:
This is package 'accelerate' generated automatically by pyp2spec.}

%description %_description

%package -n     python3-accelerate
Summary:        %{summary}

%description -n python3-accelerate %_description


%prep
%autosetup -p1 -n accelerate-%{version}
# Delete all the test_utils with external deps
rm -r src/accelerate/test_utils/scripts/external_deps/*
# This particular utility tries to access something internal to pytorch?
rm src/accelerate/test_utils/scripts/test_merge_weights.py
# This particular utility uses pytest, but we don't package the test extras...
rm src/accelerate/test_utils/scripts/test_notebook.py


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel

%install
%pyproject_install
# Add top-level Python module names here as arguments, you can use globs
%pyproject_save_files -l accelerate


%check
export ACCELERATE_ENABLE_RICH=True
%pyproject_check_import
unset ACCELERATE_ENABLE_RICH


%files -n python3-accelerate -f %{pyproject_files}
%license LICENSE
%doc README.md
%{_bindir}/accelerate
%{_bindir}/accelerate-config
%{_bindir}/accelerate-estimate-memory
%{_bindir}/accelerate-launch
%{_bindir}/accelerate-merge-weights


%changelog
%autochangelog
