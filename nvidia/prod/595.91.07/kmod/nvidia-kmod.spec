# Build only the akmod package and no kernel module packages:
%define buildforkernels akmod
%global debug_package %{nil}
%define major_version %(printf '%s\n' %{version} | cut -d. -f1)

# Build flags are inherited from the kernel
%undefine _auto_set_build_flags

Name:           nvidia-kmod
Version:        595.91.07
Release:        2%{?dist}
Summary:        NVIDIA display driver kernel module
Epoch:          3
License:        NVIDIA License
URL:            http://www.nvidia.com/object/unix.html
ExclusiveArch:  x86_64 aarch64

Source0:        https://github.com/NVIDIA/open-gpu-kernel-modules/archive/refs/tags/%{version}.tar.gz
Patch0:         0001-Add-IBT-support.patch
Patch1:         0002-fix-dsc-correct-RC-parameter-tables-to-match-VESA-DS.patch
Patch2:         0003-fix-dsc-use-bits_per_component-for-flatnessDetThresh.patch
Patch3:         0004-fix-dp-add-Bigscreen-Beyond-VR-headset-to-WAR-databa.patch

# The run file contains precompiled C++ code for the open modules:
#   kernel-open/nvidia/nv-kernel.o_binary
#   kernel-open/nvidia-modeset/nv-modeset-kernel.o_binary
# The full open tarball requires also a c++ compiler to build those bits:

BuildRequires:  elfutils-libelf-devel
BuildRequires:  gcc-c++
BuildRequires:  kmodtool

%global AkmodsBuildRequires elfutils-libelf-devel, gcc-c++, kmodtool

# kmodtool does its magic here:
%{expand:%(kmodtool --target %{_target_cpu} --repo negativo17.org --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

%description
The NVidia %{version} display driver kernel module for kernel %{kversion}.

%prep
%{?kmodtool_check}
kmodtool --target %{_target_cpu} --repo negativo17.org --kmodname %{name} \
    %{?buildforkernels:--%{buildforkernels}} \
    %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null

%setup -T -c -n open-gpu-kernel-modules-%{version}
tar -xf %{SOURCE0} --strip-components=1
%autopatch -q -p1

rm -f dkms.conf

cd ..
for kernel_version in %{?kernel_versions}; do
    dest="_kmod_build_${kernel_version%%___*}"
    rm -rf "$dest"
    cp -a open-gpu-kernel-modules-%{version} "$dest"
done

%build
for kernel_version in %{?kernel_versions}; do
    pushd ../_kmod_build_${kernel_version%%___*}/
        make %{?_smp_mflags} KERNEL_UNAME="${kernel_version%%___*}" modules
    popd
done

%install
for kernel_version in %{?kernel_versions}; do
    mkdir -p %{buildroot}/%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/
    install -p -m 0755 ../_kmod_build_${kernel_version%%___*}/kernel-open/*.ko \
        %{buildroot}/%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/
done
%{?akmod_install}

%changelog
* Thu Mar 05 2026 Simone Caronni <negativo17@gmail.com> - 3:595.45.04-1
- Update to 595.45.04.

* Fri Feb 13 2026 Simone Caronni <negativo17@gmail.com> - 3:590.48.01-3
- Fix error that prevents building the module.

* Thu Feb 12 2026 Simone Caronni <negativo17@gmail.com> - 3:590.48.01-2
- Adjust BuildRequires for akmod package.
- Add 6.19 kernel patch.

* Thu Dec 18 2025 Simone Caronni <negativo17@gmail.com> - 3:590.48.01-1
- Update to 590.48.01.

* Wed Dec 10 2025 Simone Caronni <negativo17@gmail.com> - 3:590.44.01-2
- Bump release for broken updates on aarch64.

* Fri Dec 05 2025 Simone Caronni <negativo17@gmail.com> - 3:590.44.01-1
- Update to 590.44.01.
- Drop proprietary modules support (required only for vGPU).

* Fri Nov 07 2025 Simone Caronni <negativo17@gmail.com> - 3:580.105.08-1
- Update to 580.105.08.

* Wed Oct 01 2025 Simone Caronni <negativo17@gmail.com> - 3:580.95.05-1
- Update to 580.95.05.

* Thu Sep 11 2025 Simone Caronni <negativo17@gmail.com> - 3:580.82.09-1
- Update to 580.82.09.

* Mon Sep 01 2025 Simone Caronni <negativo17@gmail.com> - 3:580.82.07-1
- Update to 580.82.07.

* Thu Aug 14 2025 Simone Caronni <negativo17@gmail.com> - 3:580.76.05-1
- Update to 580.76.05.

* Tue Aug 05 2025 Simone Caronni <negativo17@gmail.com> - 3:580.65.06-1
- Update to 580.65.06.

* Wed Jul 23 2025 Simone Caronni <negativo17@gmail.com> - 3:575.64.05-1
- Update to 575.64.05.

* Tue Jul 01 2025 Simone Caronni <negativo17@gmail.com> - 3:575.64.03-1
- Update to 575.64.03.

* Wed Jun 18 2025 Simone Caronni <negativo17@gmail.com> - 3:575.64-1
- Update to 575.64.

* Thu May 29 2025 Simone Caronni <negativo17@gmail.com> - 3:575.57.08-1
- Update to 575.57.08.

* Tue May 20 2025 Simone Caronni <negativo17@gmail.com> - 3:575.51.02-1
- Update to 575.51.02.

* Tue May 20 2025 Simone Caronni <negativo17@gmail.com> - 3:570.153.02-1
- Update to 570.153.02.

* Tue Apr 22 2025 Simone Caronni <negativo17@gmail.com> - 3:570.144-1
- Update to 570.144.

* Sat Apr 12 2025 Simone Caronni <negativo17@gmail.com> - 3:570.133.07-2
- Convert EXTRA_CFLAGS to ccflags-y for kernel 6.15 and add -std=gnu17 to fix
  compilation on Fedora 42's 6.14.1 kernel.

* Wed Mar 19 2025 Simone Caronni <negativo17@gmail.com> - 3:570.133.07-1
- Update to 570.133.07.

* Fri Feb 28 2025 Simone Caronni <negativo17@gmail.com> - 3:570.124.04-1
- Update to 570.124.04.

* Fri Jan 31 2025 Simone Caronni <negativo17@gmail.com> - 3:570.86.16-1
- Update to 570.86.16.

* Mon Jan 27 2025 Simone Caronni <negativo17@gmail.com> - 3:570.86.15-1
- Update to 570.86.15.

* Thu Dec 05 2024 Simone Caronni <negativo17@gmail.com> - 3:565.77-1
- Update to 565.77.

* Mon Nov 25 2024 Simone Caronni <negativo17@gmail.com> - 3:565.57.01-2
- Add kernel 6.12 patch.

* Wed Oct 23 2024 Simone Caronni <negativo17@gmail.com> - 3:565.57.01-1
- Update to 565.57.01.

* Fri Oct 11 2024 Simone Caronni <negativo17@gmail.com> - 3:560.35.03-2
- Add kernel 6.11 patch.

* Wed Aug 21 2024 Simone Caronni <negativo17@gmail.com> - 3:560.35.03-1
- Update to 560.35.03.

* Tue Aug 06 2024 Simone Caronni <negativo17@gmail.com> - 3:560.31.02-1
- Update to 560.31.02.

* Mon Aug 05 2024 Simone Caronni <negativo17@gmail.com> - 3:560.28.03-1
- Update to 560.28.03.

* Tue Jul 02 2024 Simone Caronni <negativo17@gmail.com> - 3:555.58.02-1
- Update to 555.58.02.

* Thu Jun 27 2024 Simone Caronni <negativo17@gmail.com> - 3:555.58-1
- Update to 555.58.

* Thu Jun 06 2024 Simone Caronni <negativo17@gmail.com> - 3:555.52.04-1
- Update to 555.52.04.

* Wed May 22 2024 Simone Caronni <negativo17@gmail.com> - 3:555.42.02-1
- Update to 555.42.02.

* Fri Apr 26 2024 Simone Caronni <negativo17@gmail.com> - 3:550.78-1
- Update to 550.78.

* Thu Apr 18 2024 Simone Caronni <negativo17@gmail.com> - 3:550.76-1
- Update to 550.76.

* Sun Mar 24 2024 Simone Caronni <negativo17@gmail.com> - 3:550.67-1
- Update to 550.67.

* Sat Mar 09 2024 Simone Caronni <negativo17@gmail.com> - 3:550.54.14-2
- Enable aarch64.

* Sun Mar 03 2024 Simone Caronni <negativo17@gmail.com> - 3:550.54.14-1
- Update to 550.54.14.

* Tue Feb 06 2024 Simone Caronni <negativo17@gmail.com> - 3:550.40.07-1
- Update to 550.40.07.

* Tue Feb 06 2024 Simone Caronni <negativo17@gmail.com> - 3:545.29.06-2
- Add patch to fix build with the latest 6.6/6.7 kernels.

* Fri Dec 01 2023 Simone Caronni <negativo17@gmail.com> - 3:545.29.06-1
- Update to version 545.29.06.

* Tue Nov 14 2023 Simone Caronni <negativo17@gmail.com> - 3:545.29.02-3
- Update location of configuration file.

* Mon Nov 13 2023 Simone Caronni <negativo17@gmail.com> - 3:545.29.02-2
- Trim changelog.
- Drop custom signing and compressing in favour of kmodtool.
- Allow building proprietary or open source modules.
- Adjust compile command to match with what Nvidia ships nowadays.

* Tue Oct 31 2023 Simone Caronni <negativo17@gmail.com> - 3:545.29.02-1
- Update to 545.29.02.

* Wed Oct 18 2023 Simone Caronni <negativo17@gmail.com> - 3:545.23.06-1
- Update to 545.23.06.

* Fri Sep 22 2023 Simone Caronni <negativo17@gmail.com> - 3:535.113.01-1
- Update to 535.113.01.

* Thu Aug 24 2023 Simone Caronni <negativo17@gmail.com> - 3:535.104.05-1
- Update to 535.104.05.

* Wed Aug 09 2023 Simone Caronni <negativo17@gmail.com> - 3:535.98-1
- Update to 535.98.

* Wed Jul 19 2023 Simone Caronni <negativo17@gmail.com> - 3:535.86.05-1
- Update to 535.86.05.

* Thu Jun 15 2023 Simone Caronni <negativo17@gmail.com> - 3:535.54.03-1
- Update to 535.54.03.

* Tue Jun 13 2023 Simone Caronni <negativo17@gmail.com> - 3:535.43.02-1
- Update to 535.43.02.

* Fri Mar 24 2023 Simone Caronni <negativo17@gmail.com> - 3:530.41.03-1
- Update to 530.41.03.

* Wed Mar 08 2023 Simone Caronni <negativo17@gmail.com> - 3:530.30.02-1
- Update to 530.30.02.

* Fri Feb 10 2023 Simone Caronni <negativo17@gmail.com> - 3:525.89.02-1
- Update to 525.89.02.

* Fri Jan 20 2023 Simone Caronni <negativo17@gmail.com> - 3:525.85.05-1
- Update to 525.85.05.

* Mon Jan 09 2023 Simone Caronni <negativo17@gmail.com> - 3:525.78.01-1
- Update to 525.78.01.

* Tue Nov 29 2022 Simone Caronni <negativo17@gmail.com> - 3:525.60.11-1
- Update to 525.60.11.

* Thu Oct 13 2022 Simone Caronni <negativo17@gmail.com> - 3:520.56.06-1
- Update to 520.56.06.

* Wed Sep 21 2022 Simone Caronni <negativo17@gmail.com> - 3:515.76-1
- Update to 515.76.

* Mon Aug 08 2022 Simone Caronni <negativo17@gmail.com> - 3:515.65.01-1
- Update to 515.65.01.

* Wed Jun 29 2022 Simone Caronni <negativo17@gmail.com> - 3:515.57-1
- Update to 515.57.

* Wed Jun 01 2022 Simone Caronni <negativo17@gmail.com> - 3:515.48.07-1
- Update to 515.48.07.

* Thu May 12 2022 Simone Caronni <negativo17@gmail.com> - 3:515.43.04-1
- Update to 515.43.04.

* Mon May 02 2022 Simone Caronni <negativo17@gmail.com> - 3:510.68.02-1
- Update to 510.68.02.

* Mon Mar 28 2022 Simone Caronni <negativo17@gmail.com> - 3:510.60.02-1
- Update to 510.60.02.

* Mon Feb 14 2022 Simone Caronni <negativo17@gmail.com> - 3:510.54-1
- Update to 510.54.

* Wed Feb 02 2022 Simone Caronni <negativo17@gmail.com> - 3:510.47.03-1
- Update to 510.47.03.
