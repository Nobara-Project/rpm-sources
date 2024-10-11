%global _default_patch_fuzz 2
%global commit 58004bff8bda0ea36dce4b970a054b95800e3c3f
%global commitdate 20240405
%global shortcommit %(c=%{commit}; echo ${c:0:7})

%if 0%{?fedora}
%global buildforkernels akmod
%global debug_package %{nil}
%endif

Name:     xone
Version:  0.3
Release:  15%{?dist}
Summary:  Linux kernel driver for Xbox One and Xbox Series X|S accessories
License:  GPLv2
URL:      https://github.com/medusalix/xone
Source0:  %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
Source1:  modules-load-d-%{name}.conf
#Patch0:   0001-revert-powera-changes.patch
Patch1:   0001-convert-to-dongle-only-build.patch
Patch2:   elite-paddles.patch
Patch3:   https://github.com/medusalix/xone/pull/20.patch#/%{name}-%{version}-share-button.patch
Patch4:   https://github.com/medusalix/xone/pull/45.patch#/%{name}-%{version}-pairing-attrib.patch
Patch5:   6.11-fixup.patch

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  kmodtool
BuildRequires:  systemd-rpm-macros
BuildRequires:  sed

Requires:       bash
Requires:       lpf-xone-firmware

Provides:       %{name}-kmod-common = %{version}-%{release}
Requires:       %{name}-kmod >= %{version}

Conflicts:      xow <= 0.5
Obsoletes:      xow <= 0.5

# kmodtool does its magic here
%{expand:%(kmodtool --target %{_target_cpu} --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

%description
xone is a Linux kernel driver for Xbox One and Xbox Series X|S dongle.

%package kmod
Summary:  Kernel module (kmod) for %{name}
Requires: kernel-devel

%description kmod
kmod package for %{name}

%prep
# error out if there was something wrong with kmodtool
%{?kmodtool_check}

# print kmodtool output for debugging purposes:
kmodtool --target %{_target_cpu} --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null

%autosetup -c %{name}-%{commit} -N

pushd %{name}-%{commit}
%autopatch -m0 -p1
popd

for kernel_version  in %{?kernel_versions} ; do
  cp -a %{name}-%{commit} _kmod_build_${kernel_version%%___*}
done

%build
for kernel_version  in %{?kernel_versions} ; do
  make V=1 %{?_smp_mflags} -C ${kernel_version##*___} M=${PWD}/_kmod_build_${kernel_version%%___*} VERSION=v%{version} modules
done

%install
for kernel_version in %{?kernel_versions}; do
 mkdir -p %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/
 install -D -m 755 _kmod_build_${kernel_version%%___*}/%{name}-*.ko %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/
 chmod a+x %{buildroot}%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/%{name}-*.ko
done
%{?akmod_install}

install -D -m 0644 %{name}-%{commit}/install/modprobe.conf %{buildroot}%{_modprobedir}/60-%{name}.conf
install -D -m 0644 %{SOURCE1} %{buildroot}%{_modulesloaddir}/%{name}.conf

%files
%doc %{name}-%{commit}/README.md
%license %{name}-%{commit}/LICENSE
%{_modprobedir}/60-%{name}.conf
%{_modulesloaddir}/%{name}.conf

%changelog
* Sun Jan 28 2024 Jan Drögehoff <sentrycraft123@gmail.com> - 0.3-4
- Force bump release

* Tue Jun 06 2023 Jan Drögehoff <sentrycraft123@gmail.com> - 0.3-3
- Fix Linux 6.3 compilation, add some patches

* Sun Nov 13 2022 Jan Drögehoff <sentrycraft123@gmail.com> - 0.3-2
- correct modules

* Thu Jun 23 2022 Jan Drögehoff <sentrycraft123@gmail.com> - 0.3-1
- Update to 0.3

* Sat Mar 19 2022 Jan Drögehoff <sentrycraft123@gmail.com> - 0.2-2
- Obsolete xow and require firmware

* Sun Feb 27 2022 Jan Drögehoff <sentrycraft123@gmail.com> - 0.2-1
- Update to 0.2

* Fri Jul 02 2021 Jan Drögehoff <sentrycraft123@gmail.com> - 0.1-1
- Initial spec

