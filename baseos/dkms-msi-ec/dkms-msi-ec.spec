%global debug_package %{nil}
%global modulename msi-ec
%global commit c8cbd48ed01f5c4fa7e34ff622a66f5a5380c705
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global commitdate 20261109

Name:           dkms-%{modulename}
Version:        0.18^%{commitdate}git.%{shortcommit}
Release:        1%{?dist}
Summary:        MSI laptop embedded controller driver (DKMS)
License:        GPL-2.0-or-later
URL:            https://github.com/BeardOverflow/msi-ec
Source0:        %{url}/archive/%{commit}.tar.gz#/%{modulename}-%{commit}.tar.gz
# Same patch as nobara-signed-kmods: no debug mode, which gives root raw
# writes to every embedded controller register
Patch0:         msi-ec-remove-debug.patch
Requires:       dkms
Requires:       gcc, make
Provides:       %{modulename}-kmod = %{version}
BuildArch:      noarch

%description
The out-of-tree msi-ec driver for MSI laptops' embedded controller, built by
DKMS for every installed kernel: cooler boost, shift (performance) and fan
modes, battery charge thresholds, webcam, Fn/Win key swap, keyboard backlight
and mute LEDs, and CPU/GPU temperature and fan speed. It supports more models
and features than the kernel's own msi-ec, which it replaces (DKMS installs
it in extra/, which depmod prefers over the kernel's module). Debug mode is
removed.

%prep
%autosetup -n %{modulename}-%{commit} -p1

%build

%install
mkdir -p %{buildroot}%{_usrsrc}/%{modulename}-%{version}
cp -a msi-ec.c ec_memory_configuration.h Makefile Makefile.vars LICENSE \
    %{buildroot}%{_usrsrc}/%{modulename}-%{version}/
cat > %{buildroot}%{_usrsrc}/%{modulename}-%{version}/dkms.conf <<'DKMS'
PACKAGE_NAME="%{modulename}"
PACKAGE_VERSION="%{version}"
MAKE[0]="'make' -C ${kernel_source_dir} M=${dkms_tree}/${PACKAGE_NAME}/${PACKAGE_VERSION}/build modules"
BUILT_MODULE_NAME[0]="msi-ec"
DEST_MODULE_LOCATION[0]="/extra"
AUTOINSTALL="yes"
DKMS
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
%doc README.md
%{_usrsrc}/%{modulename}-%{version}
%config(noreplace) %{_sysconfdir}/dkms/%{modulename}.conf

%changelog
* Thu Nov 12 2026 GloriousEggroll <gloriouseggroll@gmail.com> - 0.18^20261109git.c8cbd48-1
- Initial package. nobara-signed-kmods builds the signed module for the Easy
  Anti-Cheat kernel from the same source and patch
