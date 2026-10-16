%global forgeurl https://github.com/alex-courtis/way-displays
%global version 2.0.0
%global tag %{version}
%forgemeta

Name:           way-displays
Version:        %{version}
Release:        %autorelease -b4
Summary:        Auto Manage Your Wayland Displays
URL:            %{forgeurl}
License:        MIT
Source0:         %{forgesource}
Patch0:         0001-don-t-put-XDG_VTNR-in-socket-name.patch
Patch1:         0002-don-t-enable-auto-scale-by-default.patch
Patch2:         0003-change-log-threshold-default-to-WARNING-instead-of-I.patch
Patch3:         0004-fix-aarch64-va-list-portability.patch

BuildRequires:  gcc
BuildRequires:  bash
BuildRequires:  sed
BuildRequires:  make
BuildRequires:  wayland-devel
BuildRequires:  wayland-protocols-devel
BuildRequires:  libinput-devel
BuildRequires:  libudev-devel
BuildRequires:  libyaml-devel
BuildRequires:  valgrind
BuildRequires:  libcmocka-devel

%description

%prep
%autosetup -p1

%build
%make_build

%install
%make_install PREFIX="/usr" PREFIX_ETC="/"

# The tests rely on linker --wrap mocks that are defeated by Fedora's LTO flags.
#%check
#%{__make} test

%files
%license LICENSE
%doc README.md
%{_bindir}/way-displays
%config(noreplace) /etc/way-displays/cfg.yaml
%{_mandir}/man1/way-displays.1.*
%{_mandir}/man5/way-displays.5.*
%changelog
%autochangelog
