Summary: Configure automatic handling of removable storage media
Name: nobara-automount
Version: 1.1
Release: 10%{?dist}
License: Public Domain
Group: System Environment/Base
Source0: %{URL}/releases/download/1.0/nobara-automount.tar.gz

BuildArch: noarch
BuildRequires:  python3-devel
BuildRequires:  make
BuildRequires: filesystem
Requires: system-release
Requires: python
Requires: python3
Requires: python3-gobject
Requires: python3-psutil
Requires: python3-requests
Requires: python3-dnf
Requires: python3-libdnf5
Requires: python3-packaging
Requires: python3-dasbus
Requires: python3-cairo
Requires: python3-pillow
Requires: python3-evdev
Requires: systemd
Requires: fuse
Requires: ntfs-3g
Requires: glib2
Requires: gtk3
Requires: gtk4
Requires: libadwaita
Requires: adw-gtk3-theme
Requires: rpm
Requires: systemd
Requires: util-linux

%description
Configure automatic handling of removable storage media

%prep
%autosetup -p1 -n nobara-automount

%install
rm -rf $RPM_BUILD_ROOT
make all DESTDIR=%{buildroot}

install -d $RPM_BUILD_ROOT%{_sysconfdir}/nobara/automount/
echo '# list of enabled automount partitions' > enabled.conf
install -m 0755 enabled.conf $RPM_BUILD_ROOT%{_sysconfdir}/nobara/automount/enabled.conf

%files
%license %{_datadir}/licenses/nobara-automount/LICENSE
%{_libexecdir}/nobara-automount
%{_bindir}/nobara-drive-mount-manager
%config(noreplace) %{_sysconfdir}/nobara/automount/enabled.conf
%{_datadir}/polkit-1/actions/org.nobaraproject.automount.policy
%{_datadir}/applications/nobara-drive-mount-manager.desktop
%{_prefix}/lib/systemd/system/nobara-automount@.service

%changelog
