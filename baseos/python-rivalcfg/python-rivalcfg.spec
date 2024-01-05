Name:           python-rivalcfg
Version:        4.7.0
Release:        1%{?dist}
Summary:        Configure SteelSeries gaming mice

# Check if the automatically generated License and its spelling is correct for Fedora
# https://docs.fedoraproject.org/en-US/packaging-guidelines/LicensingGuidelines/
License:        WTFPL
URL:            https://github.com/flozz/rivalcfg
Source0:        %{pypi_source rivalcfg}

BuildArch:      noarch
BuildRequires:  python3-devel
Provides:	rivalcfg


# Fill in the actual package description to submit package to Fedora
%global _description %{expand:
This is package 'rivalcfg' generated automatically by pyp2spec.}


%description %_description

%package -n     python3-rivalcfg
Summary:        %{summary}

%description -n python3-rivalcfg %_description


%prep
%autosetup -p1 -n rivalcfg-%{version}


%generate_buildrequires
%pyproject_buildrequires -r


%build
%pyproject_wheel


%install
%pyproject_install
# For official Fedora packages, including files with '*' +auto is not allowed
# Replace it with a list of relevant Python modules/globs and list extra files in %%files
%pyproject_save_files '*' +auto


%check
%pyproject_check_import -t


%files -n python3-rivalcfg -f %{pyproject_files}


%changelog
* Wed Jan 12 2022 mockbuilder - 4.5.0-1
- Package generated with pyp2spec
