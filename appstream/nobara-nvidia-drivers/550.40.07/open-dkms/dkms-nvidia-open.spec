%global debug_package %{nil}
%global dkms_name nvidia-open
%global _default_patch_fuzz 2

Name:           dkms-%{dkms_name}
Version:        550.40.07
Release:        6%{?dist}
Summary:        NVIDIA OpenSource display driver kernel module
Epoch:          3
License:        NVIDIA License
URL:            http://www.nvidia.com/object/unix.html
ExclusiveArch:  x86_64

Source0:        https://github.com/NVIDIA/open-gpu-kernel-modules/archive/%{version}/open-gpu-kernel-modules-%{version}.tar.gz
Source1:        %{name}.conf
Source2:        dkms-no-weak-modules.conf

BuildRequires:  sed

Provides:       nvidia-kmod = %{?epoch:%{epoch}:}%{version}
Requires:       nvidia-kmod-common = %{?epoch:%{epoch}:}%{version}
Requires:       dkms

Conflicts:      akmod-nvidia
Conflicts:      kmod-nvidia
Conflicts:      dkms-nvidia

%description
This package provides the proprietary Nvidia kernel driver modules.
The modules are rebuilt through the DKMS system when a new kernel or modules
become available.

%prep
%autosetup -p1 -n open-gpu-kernel-modules-%{version}

cp -f %{SOURCE1} dkms.conf

sed -i -e 's/__VERSION_STRING/%{version}/g' dkms.conf

%build

%install
# Create empty tree:
mkdir -p %{buildroot}%{_usrsrc}/%{dkms_name}-%{version}/
cp -fr * %{buildroot}%{_usrsrc}/%{dkms_name}-%{version}/

%if 0%{?fedora}
# Do not enable weak modules support in Fedora (no kABI):
install -p -m 644 -D %{SOURCE2} %{buildroot}%{_sysconfdir}/dkms/%{dkms_name}.conf
%endif

%post
dkms add -m %{dkms_name} -v %{version} -q || :
# Rebuild and make available for the currently running kernel:
dkms build -m %{dkms_name} -v %{version} -q || :
dkms install -m %{dkms_name} -v %{version} -q --force || :

%preun
# Remove all versions from DKMS registry:
dkms remove -m %{dkms_name} -v %{version} -q --all || :

%files
%{_usrsrc}/%{dkms_name}-%{version}
%if 0%{?fedora}
%{_sysconfdir}/dkms/%{dkms_name}.conf
%endif

%changelog
* Tue Oct 31 2023 Simone Caronni <negativo17@gmail.com> - 3:545.29.02-1
- First build of open source modules.
