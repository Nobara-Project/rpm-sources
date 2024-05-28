%global gitcommit 243c44a1fe4898fbc6a092529f16b8b7d0dc21af
Name:           sdgyrodsu
Version:        0.0.git.221.243c44a1
Release:        1%{?dist}
Summary:        DSU server for motion data running on Steam Deck.
License:        MIT
URL:            https://github.com/KyleGospo/SteamDeckGyroDSU

Source:         %{url}/archive/%{gitcommit}.tar.gz
Patch0:         fedora.patch

BuildRequires:  systemd-rpm-macros
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  ncurses-devel
BuildRequires:  systemd-devel
BuildRequires:  hidapi-devel

%global debug_package %{nil}

%description
DSU (cemuhook protocol) server for motion data for Steam Deck.

%prep
%setup -T -b 0 -q -n SteamDeckGyroDSU-%{gitcommit}
%patch 0

%build
%set_build_flags
%make_build

%install
install -Dsm 755 bin/release/%{name} %{buildroot}%{_bindir}/%{name}
install -Dm 755 pkg/%{name}.service %{buildroot}%{_userunitdir}/%{name}.service

%post
%systemd_user_post %{name}.service
%udev_rules_update

%preun
%systemd_user_preun %{name}.service

%postun
%udev_rules_update

%files
%license LICENSE
%{_bindir}/%{name}
%{_userunitdir}/%{name}.service

%changelog
