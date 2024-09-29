Name:           hhd
Version:        3.3.15
Release:        7%{?dist}
Summary:        Handheld Daemon, a tool for configuring handheld devices.

License:        GPL-3.0-or-later AND MIT
URL:            https://github.com/hhd-dev/hhd
Source0:        	https://pypi.python.org/packages/source/h/%{name}/%{name}-%{version}.tar.gz
Source1:        	hhd-run.sh
Source2:        	org.hhd.start.policy

Patch0:         0001-update-rog-ally-x-button-mapping-to-match-luke-patch.patch
Patch1:         0001-set-legion-go-and-ally-x-to-dualsense-by-default-for.patch

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
Requires:       python3-xlib
Requires:       libusb1
Requires:       hidapi

%description
Handheld Daemon is a project that aims to provide utilities for managing handheld devices. With features ranging from TDP controls, to controller remappings, and gamescope session management. This will be done through a plugin system and an HTTP(/d-bus?) daemon, which will expose the settings of the plugins in a UI agnostic way.

%prep
%autosetup -n %{name}-%{version} -p1

%build
%{python3} -m build --wheel --no-isolation

%install
%{python3} -m installer --destdir="%{buildroot}" dist/*.whl
mkdir -p %{buildroot}%{_udevrulesdir}
install -m644 usr/lib/udev/rules.d/83-%{name}.rules %{buildroot}%{_udevrulesdir}/83-%{name}.rules
mkdir -p %{buildroot}%{_sysconfdir}/udev/hwdb.d
install -m644 usr/lib/udev/hwdb.d/83-%{name}.hwdb %{buildroot}%{_sysconfdir}/udev/hwdb.d/83-%{name}.hwdb
mkdir -p %{buildroot}%{_unitdir}
install -m644 usr/lib/systemd/system/%{name}@.service %{buildroot}%{_unitdir}/%{name}@.service
mkdir -p %{buildroot}%{_bindir}
install -m775 %{SOURCE1} %{buildroot}%{_bindir}/hhd-run.sh
mkdir -p %{buildroot}%{_datadir}/polkit-1/actions/
install -m775 %{SOURCE2} %{buildroot}%{_datadir}/polkit-1/actions/org.hhd.start.policy

%files
%doc readme.md
%license LICENSE
%{_bindir}/%{name}*
%{_bindir}/hhd-run.sh
%{python3_sitelib}/%{name}*
%{_udevrulesdir}/83-%{name}.rules
%{_sysconfdir}/udev/hwdb.d/83-%{name}.hwdb
%{_unitdir}/%{name}@.service
%{_datadir}/polkit-1/actions/org.hhd.start.policy
