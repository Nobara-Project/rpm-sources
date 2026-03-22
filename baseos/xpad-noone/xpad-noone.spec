%if 0%{?fedora}
%global buildforkernels akmod
%global debug_package %{nil}
%endif

%global short_commit c3d1610

Name:     xpad-noone
Version:  1
Release:  5%{?dist}
Summary:  xpad drivers without support for Xbox Controllers
License:  GPLv2
URL:      https://github.com/medusalix/xpad-noone
Source0:  %{url}/archive/%{short_commit}/%{name}-%{short_commit}.tar.gz

# Sync with upstream devices
Patch0:  https://github.com/medusalix/xpad-noone/pull/8.patch
# Fix for kernel 6.18
Patch1:  https://github.com/medusalix/xpad-noone/pull/9.patch

BuildArch:      noarch
BuildRequires:  systemd-rpm-macros
BuildRequires:  sed

Requires:	dkms
Requires:       bash
Requires:	gcc

Provides:       %{name}-kmod-common = %{version}-%{release}
Obsoletes:      akmod-xpad-noone < %{version}-%{release}
Conflicts:      xow <= 0.5
Obsoletes:      xow <= 0.5

%description
xpad drivers without support for Xbox Controllers
Intended to be used with xone

%prep
%autosetup -n %{name}-%{short_commit} -N
%autopatch -p1

sed -i 's/PACKAGE_VERSION=.*/PACKAGE_VERSION="%{version}"/' dkms.conf
sed -i 's|M=$PWD|M=$dkms_tree/$PACKAGE_NAME/$PACKAGE_VERSION/build|' dkms.conf

%build

%install
%global dkms_source_dir %{_usrsrc}/%{name}-%{version}
mkdir -p %{buildroot}%{dkms_source_dir}
cp -fr . %{buildroot}%{dkms_source_dir}

%post
dkms add -m %{name} -v %{version} --rpm_safe_upgrade || :
dkms build -m %{name} -v %{version} || :
dkms install -m %{name} -v %{version} || :

%preun
dkms remove -m %{name} -v %{version} --all --rpm_safe_upgrade || :

%files
%doc README.md 
%license LICENSE
%{_usrsrc}/%{name}-%{version}

%changelog
* Sun Mar 22 2026 LionHeartP <LionHeartP@proton.me> - 1-5
- Convert to DKMS

* Wed Dec 17 2025 LionHeartP <LionHeartP@proton.me> - 1-4
- Patch for kernels 6.18+
- Patch to add new devices
- Change spec prep process to accomodate for patching the files

* Tue Jul 23 2024 Jan200101 <sentrycraft123@gmail.com> - 1-3
- Initial build

