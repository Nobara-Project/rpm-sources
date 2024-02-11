# buildforkernels macro hint: when you build a new version or a new release
# that contains bugfixes or other improvements then you must disable the
# "buildforkernels newest" macro for just that build; immediately after
# queuing that build enable the macro again for subsequent builds; that way
# a new akmod package will only get build when a new one is actually needed
%define buildforkernels akmod
%global _default_patch_fuzz 2
%global debug_package %{nil}

Name:           nvidia-open-kmod
Version:        550.40.07
Release:        6%{?dist}
Summary:        NVIDIA OpenSource display driver kernel module
Epoch:          3
License:        NVIDIA License
URL:            http://www.nvidia.com/object/unix.html
ExclusiveArch:  x86_64

Source0:        https://github.com/NVIDIA/open-gpu-kernel-modules/archive/%{version}/open-gpu-kernel-modules-%{version}.tar.gz

# get the needed BuildRequires (in parts depending on what we build for)
BuildRequires:  kmodtool

# kmodtool does its magic here
%{expand:%(kmodtool --target %{_target_cpu} --repo negativo17.org --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

%description
The NVidia %{version} display driver kernel module for kernel %{kversion}.

%prep
# error out if there was something wrong with kmodtool
%{?kmodtool_check}
# print kmodtool output for debugging purposes:
kmodtool  --target %{_target_cpu}  --repo negativo17.org --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null

%autosetup -p1 -n open-gpu-kernel-modules-%{version}

for kernel_version in %{?kernel_versions}; do
    mkdir _kmod_build_${kernel_version%%___*}
    cp -fr * _kmod_build_${kernel_version%%___*}
done

%build
for kernel_version in %{?kernel_versions}; do
    pushd _kmod_build_${kernel_version%%___*}/
        make %{?_smp_mflags} \
            IGNORE_XEN_PRESENCE=1 \
            IGNORE_PREEMPT_RT_PRESENCE=1 \
            IGNORE_CC_MISMATCH=1 \
            SYSSRC="${kernel_version##*___}" \
            module
    popd
done

%install
for kernel_version in %{?kernel_versions}; do
    mkdir -p %{buildroot}/%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/
    install -p -m 0755 _kmod_build_${kernel_version%%___*}/*.ko \
        %{buildroot}/%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/
done
%{?akmod_install}

%changelog
* Tue Oct 31 2023 Simone Caronni <negativo17@gmail.com> - 3:545.29.02-1
- First build of open source modules.
