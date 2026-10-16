Name:           nobara-kernel-manager
Version:        0.1.1
Release:        1%{?dist}
Summary:        Graphical manager for Nobara Mainline, LTS, and rescue kernels
License:        MPL-2.0
URL:            https://github.com/nobara-project/nobara-kernel-manager
Source0:        %{url}/archive/refs/tags/%{version}/%{name}-%{version}.tar.gz

ExcludeArch:    %{ix86}

BuildRequires:  cargo
BuildRequires:  desktop-file-utils
BuildRequires:  glib2-devel
BuildRequires:  gtk4-devel
BuildRequires:  libadwaita-devel

Requires:       bash
Requires:       dnf5
Requires:       dracut
Requires:       grub2-tools
Requires:       polkit
Requires:       rpm
Requires:       sudo

%description
Nobara Kernel Manager switches between Nobara Mainline and LTS kernels and
rebuilds a minimal rescue kernel from the enabled Nobara kernel family.

%prep
%autosetup -p1

%build
cargo build --release

%check
cargo test --release

%install
DESTDIR=%{buildroot} make install_no_build

desktop-file-validate \
    %{buildroot}%{_datadir}/applications/com.github.cosmicfusion.nobara-kernel-manager.desktop

%files
%license LICENSE
%doc README.md
%{_bindir}/nobara-kernel-manager
%{_prefix}/lib/nobara-kernel-manager/kernel-manager
%{_prefix}/lib/nobara-kernel-manager/kernel-status
%{_datadir}/applications/com.github.cosmicfusion.nobara-kernel-manager.desktop
%{_datadir}/icons/hicolor/scalable/apps/com.github.cosmicfusion.nobara-kernel-manager.svg
%{_mandir}/man1/nobara-kernel-manager.1*
%{_datadir}/polkit-1/actions/org.nobaraproject.kernel-manager.manage.policy
%{_datadir}/polkit-1/actions/org.nobaraproject.kernel-manager.status.policy

%changelog
* Sun Aug 23 2026 Nobara Project <hello@nobaraproject.org> - 0.1.1-1
- Show booted, rescue, latest Mainline, and latest LTS kernel versions

* Sun Aug 23 2026 Nobara Project <hello@nobaraproject.org> - 0.1.0-3
- Keep the live operation log scrolled to its newest output

* Sun Aug 23 2026 Nobara Project <hello@nobaraproject.org> - 0.1.0-2
- Select the newest bootable kernel from the enabled family for rescue rebuilds
- Stream privileged backend progress in the graphical interface

* Sun Aug 23 2026 Nobara Project <hello@nobaraproject.org> - 0.1.0-1
- Initial Nobara-specific kernel manager
