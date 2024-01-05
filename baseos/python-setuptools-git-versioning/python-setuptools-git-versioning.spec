Name:           python-setuptools-git-versioning
Version:        1.10.0
Release:        1%{?dist}
Summary:        Use git repo data for building a version number according PEP-440

# Check if the automatically generated License and its spelling is correct for Fedora
# https://docs.fedoraproject.org/en-US/packaging-guidelines/LicensingGuidelines/
License:        MIT
URL:            https://setuptools-git-versioning.readthedocs.io
Source:         %{pypi_source setuptools-git-versioning}

BuildArch:      noarch
BuildRequires:  python3-devel


# Fill in the actual package description to submit package to Fedora
%global _description %{expand:
This is package 'setuptools-git-versioning' generated automatically by
pyp2spec.}


%description %_description

%package -n     python3-setuptools-git-versioning
Summary:        %{summary}

%description -n python3-setuptools-git-versioning %_description


%prep
%autosetup -p1 -n setuptools-git-versioning-%{version}


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
# For official Fedora packages, including files with '*' +auto is not allowed
# Replace it with a list of relevant Python modules/globs and list extra files in %%files
%pyproject_save_files '*' +auto


%check
%pyproject_check_import -t


%files -n python3-setuptools-git-versioning -f %{pyproject_files}


%changelog
* Wed Jul 20 2022 mockbuilder - 1.10.0-1
- Package generated with pyp2spec