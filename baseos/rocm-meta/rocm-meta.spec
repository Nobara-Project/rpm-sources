%global ROCM_MAJOR_VERSION 6
%global ROCM_MINOR_VERSION 2
%global ROCM_PATCH_VERSION 1

Requires:      libc.so.6()(64bit)
Requires:      libc.so.6(GLIBC_2.2.5)(64bit)
Requires:      libgcc_s.so.1()(64bit)
Requires:      libm.so.6()(64bit)
Requires:      libstdc++.so.6()(64bit)

Requires:      rocm-comgr
Requires:      rocm-runtime
Requires:      rocm-smi
Requires:      rocm-clinfo
Requires:      rocm-cmake
Requires:      rocm-core
Requires:      rocm-rpm-macros
Requires:      python3-torch-rocm-gfx9
Requires:      python3-torchaudio-rocm-gfx9
Requires:      rocprim-devel
Requires:      rocblas
Requires:      rocsparse
Requires:      rocminfo
Requires:      rocrand
Requires:      hipblas
Requires:      hipfft
Requires:      hipsolver
Requires:      rocfft
Requires:      rocsolver
Requires:      hipblaslt
Requires:      rocalution
Requires:      roctracer
Requires:      rocm-opencl

Provides:      rocm-meta

BuildArch:     x86_64
Name:          rocm-meta
Version:       %{ROCM_MAJOR_VERSION}.%{ROCM_MINOR_VERSION}.%{ROCM_PATCH_VERSION}
Release:       4.copr%{?dist}
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

