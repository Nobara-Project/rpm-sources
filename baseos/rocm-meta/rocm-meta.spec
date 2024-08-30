%global ROCM_MAJOR_VERSION 6
%global ROCM_MINOR_VERSION 2
%global ROCM_PATCH_VERSION 0

Requires:      libc.so.6()(64bit)
Requires:      libc.so.6(GLIBC_2.2.5)(64bit)
Requires:      libgcc_s.so.1()(64bit)
Requires:      libm.so.6()(64bit)
Requires:      libstdc++.so.6()(64bit)
Requires:      comgr
Requires:      hip-runtime-amd
Requires:      hsa-rocr
Requires:      openmp-extras-runtime
Requires:      rocm-core
Requires:      rocm-device-libs
Requires:      rocm-hip-runtime
Requires:      rocm-language-runtime
Requires:      rocm-llvm
Requires:      rocm-ocl-icd
Requires:      rocm-opencl
Requires:      rocm-opencl-runtime
Requires:      rocm-smi-lib
Requires:      rocminfo



Provides:      rocm-meta

BuildArch:     x86_64
Name:          rocm-meta
Version:       %{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}
Release:       1.copr%{?dist}
License:       MIT
Group:         System Environment/Libraries
Summary:       Radeon Open Compute (ROCm) Runtime software stack
Source0:       rocm-meta.sh

%description
Radeon Open Compute (ROCm) Runtime software stack

%build
mkdir -p %{buildroot}/etc/profile.d
touch %{buildroot}/etc/profile.d/rocm-meta.sh
cp %{SOURCE0} %{buildroot}/etc/profile.d/rocm-meta.sh
mkdir -p %{buildroot}/etc/udev/rules.d/
touch %{buildroot}/etc/udev/rules.d/70-kfd.rules
echo 'SUBSYSTEM=="kfd", KERNEL=="kfd", TAG+="uaccess", GROUP="video"' | tee %{buildroot}/etc/udev/rules.d/70-kfd.rules
chmod +x %{buildroot}/etc/profile.d/rocm-meta.sh
echo 'ADD_EXTRA_GROUPS=1' > %{buildroot}/etc/adduser.conf
echo 'EXTRA_GROUPS=video' >> %{buildroot}/etc/adduser.conf
echo 'EXTRA_GROUPS=render' >> %{buildroot}/etc/adduser.conf

%pre
if [[ ! -z $(dnf list installed | grep 5.2.3.50203) ]] && [[ ! -d "/opt/rocm" ]] ;then
	rm -rf /opt/rocm*
fi

%post
IFS=', ' read -r -a array <<< "$(getent group | grep wheel | cut -d ":" -f 4)"
for i in "${array[@]}"
do
   usermod -a -G video ${array[$i]}
   usermod -a -G render ${array[$i]}
done


%files
/etc/udev/rules.d/70-kfd.rules
/etc/profile.d/rocm-meta.sh
/etc/adduser.conf

