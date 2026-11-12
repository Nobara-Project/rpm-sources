%global debug_package %{nil}
%global modulename r8125
%global srcver 9.018.00
%global pkgrel 1

Name:           dkms-%{modulename}
Version:        %{srcver}
Release:        2%{?dist}
Summary:        Realtek RTL8125 2.5 Gigabit Ethernet driver (DKMS)
License:        GPL-2.0-or-later
URL:            https://github.com/awesometic/realtek-r8125-dkms
Source0:        %{url}/archive/refs/tags/%{srcver}-%{pkgrel}.tar.gz#/realtek-r8125-dkms-%{srcver}-%{pkgrel}.tar.gz
Source1:        r8125.modprobe.conf
Requires:       dkms
Requires:       gcc, make
Provides:       %{modulename}-kmod = %{version}
BuildArch:      noarch

%description
Realtek's out-of-tree r8125 driver for the RTL8125 family of 2.5 Gigabit PCI
Express Ethernet controllers, built by DKMS for every installed kernel. The
in-kernel r8169 driver also supports these controllers. With this package,
r8125 is loaded first and takes the RTL8125 controllers, and r8169 keeps the
other Realtek controllers.

%prep
%autosetup -n realtek-r8125-dkms-%{srcver}-%{pkgrel}

%build

%install
mkdir -p %{buildroot}%{_usrsrc}/%{modulename}-%{version}
cp -a src/* %{buildroot}%{_usrsrc}/%{modulename}-%{version}/
cat > %{buildroot}%{_usrsrc}/%{modulename}-%{version}/dkms.conf <<'DKMS'
PACKAGE_NAME="%{modulename}"
PACKAGE_VERSION="%{version}"
MAKE[0]="'make' -C ${kernel_source_dir} M=${dkms_tree}/${PACKAGE_NAME}/${PACKAGE_VERSION}/build modules"
CLEAN="'make' -C ${kernel_source_dir} M=${dkms_tree}/${PACKAGE_NAME}/${PACKAGE_VERSION}/build clean"
BUILT_MODULE_NAME[0]="r8125"
DEST_MODULE_LOCATION[0]="/extra"
AUTOINSTALL="yes"
DKMS
install -Dpm644 %{SOURCE1} %{buildroot}%{_prefix}/lib/modprobe.d/r8125.conf
# Do not enable weak modules support in Fedora (no kABI)
install -d %{buildroot}%{_sysconfdir}/dkms
echo 'NO_WEAK_MODULES="yes"' > %{buildroot}%{_sysconfdir}/dkms/%{modulename}.conf

%post
dkms add -m %{modulename} -v %{version} -q --rpm_safe_upgrade || :
dkms build -m %{modulename} -v %{version} -q || :
dkms install -m %{modulename} -v %{version} -q --force || :

%preun
dkms remove -m %{modulename} -v %{version} -q --all --rpm_safe_upgrade || :

%files
%license LICENSE
%doc README.md REALTEK_README.txt
%{_usrsrc}/%{modulename}-%{version}
%{_prefix}/lib/modprobe.d/r8125.conf
%config(noreplace) %{_sysconfdir}/dkms/%{modulename}.conf

%changelog
* Mon Nov 02 2026 GloriousEggroll <gloriouseggroll@gmail.com> - 9.018.00-2
- Install the modprobe.d file to %{_prefix}/lib/modprobe.d: %%{_modprobedir}
  needs systemd-rpm-macros, which the buildroot doesn't have

* Mon Nov 02 2026 GloriousEggroll <gloriouseggroll@gmail.com> - 9.018.00-1
- Initial package. nobara-signed-kmods builds the signed module for the Easy
  Anti-Cheat kernel from the same source
