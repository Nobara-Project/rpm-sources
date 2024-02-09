Name:           python-grapejuice
Version:        7.20.12
Release:        2%{?dist}
Summary:        A simple wine+roblox management application

# Check if the automatically generated License and its spelling is correct for Fedora
# https://docs.fedoraproject.org/en-US/packaging-guidelines/LicensingGuidelines/
License:        GPL-3
URL:            https://gitlab.com/brinkervii/grapejuice
Source0:        https://gitlab.com/brinkervii/grapejuice/-/archive/v7.20.12/grapejuice-v7.20.12.tar.gz
Patch0:         0001-Add-support-for-using-ULWGL-as-wine_home.patch

BuildArch:      noarch
BuildRequires:  python3-devel


# Fill in the actual package description to submit package to Fedora
%global _description %{expand:
This is package 'grapejuice' generated automatically by pyp2spec.}


%description %_description

%package -n     python3-grapejuice
Summary:        %{summary}

%description -n python3-grapejuice %_description


%prep
%autosetup -p1 -n grapejuice-v%{version}


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


%files -n python3-grapejuice -f %{pyproject_files}


%changelog
* Wed Jan 12 2022 mockbuilder - 3.40.14-1
- Package generated with pyp2spec
