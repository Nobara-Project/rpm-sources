Name:           hhd
Version:        1.3.6
Release:        2%{?dist}
Summary:        Handheld Daemon, a tool for configuring handheld devices.

License:        MIT
URL:            https://github.com/hhd-dev/hhd
Source:        	https://pypi.python.org/packages/source/h/%{name}/%{name}-%{version}.tar.gz
Patch0:         0001-add-files-for-autostart.patch
Patch1:         0001-fixup-steam-powerbutton-long-press-behavior.patch

BuildArch:      noarch
BuildRequires:  systemd-rpm-macros
BuildRequires:  python3-devel
BuildRequires:  python3-build
BuildRequires:  python3-installer
BuildRequires:  python3-setuptools
BuildRequires:  python3-wheel

Requires:       python3
Requires:       python3-evdev
Requires:       python3-rich
Requires:       python3-yaml
Requires:       python3-setuptools
Conflicts:      HandyGCCS
Conflicts:      lgcd
Conflicts:      rogue-enemy
Provides:	steam-powerbuttond
Obsoletes:	steam-powerbuttond

%description
Handheld Daemon is a project that aims to provide utilities for managing handheld devices. With features ranging from TDP controls, to controller remappings, and gamescope session management. This will be done through a plugin system and an HTTP(/d-bus?) daemon, which will expose the settings of the plugins in a UI agnostic way.

%prep
%autosetup -p1 -n %{name}-%{version}

%build
%{python3} -m build --wheel --no-isolation

%install
%{python3} -m installer --destdir="%{buildroot}" dist/*.whl
mkdir -p %{buildroot}%{_udevrulesdir}
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_libexecdir}/
mkdir -p %{buildroot}%{_sysconfdir}/xdg/autostart
mkdir -p %{buildroot}%{_sysconfdir}/udev/hwdb.d/
mkdir -p %{buildroot}%{_datadir}/polkit-1/actions/
install -m644 usr/lib/udev/rules.d/83-%{name}.rules %{buildroot}%{_udevrulesdir}/83-%{name}.rules
install -m644 usr/lib/systemd/system/%{name}@.service %{buildroot}%{_unitdir}/%{name}@.service
install -m775 usr/libexec/enable-hhd %{buildroot}%{_libexecdir}/enable-hhd
install -m775 etc/xdg/autostart/hhd.desktop %{buildroot}%{_sysconfdir}/xdg/autostart/hhd.desktop
install -m644 usr/share/polkit-1/actions/org.hhd.start.policy %{buildroot}%{_datadir}/polkit-1/actions/org.hhd.start.policy
install -m644 usr/lib/udev/hwdb.d/83-%{name}.hwdb %{buildroot}%{_sysconfdir}/udev/hwdb.d/83-%{name}.hwdb

%post
udevadm control --reload-rules
udevadm trigger

%files
%doc readme.md
%license LICENSE
%{_bindir}/%{name}*
%{python3_sitelib}/%{name}*
%{_udevrulesdir}/83-%{name}.rules
%{_unitdir}/%{name}@.service
%{_libexecdir}/enable-hhd
%{_sysconfdir}/xdg/autostart/hhd.desktop
%{_sysconfdir}/udev/hwdb.d/83-%{name}.hwdb
%{_datadir}/polkit-1/actions/org.hhd.start.policy

%changelog
* Sun Feb 4 2024 Matthew Schwartz <njtransit215@gmail.com> 1.3.6-1
- upgrades to new v1.3.6 release. support added for select devices from Ayaneo, AOKZOE, and GPD along with reduced system performance overhead.
