Name:           sdgyrodsu
Version:        0.0.git.220.66115fc8
Release:        1%{?dist}
Summary:        DSU server for motion data running on Steam Deck. 
License:        MIT
URL:            https://github.com/KyleGospo/SteamDeckGyroDSU

VCS:            git+https://github.com/KyleGospo/SteamDeckGyroDSU.git#66115fc8a23a14c7484bc79d98c1dd06ac711ffe:
Source:         SteamDeckGyroDSU-66115fc8.tar.gz
Patch0:         fedora.patch

BuildRequires:  systemd-rpm-macros
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  ncurses-devel

%global debug_package %{nil}

%description
DSU (cemuhook protocol) server for motion data for Steam Deck.

%prep
%setup -T -b 0 -q -n SteamDeckGyroDSU
%patch 0

%build
%set_build_flags
%make_build

%install
install -Dsm 755 bin/release/%{name} %{buildroot}%{_bindir}/%{name}
install -Dm 755 pkg/%{name}.service %{buildroot}%{_userunitdir}/%{name}.service
install -Dm 644 pkg/51-deck-controls.rules %{buildroot}%{_udevrulesdir}/51-deck-controls.rules

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
%{_udevrulesdir}/51-deck-controls.rules

%changelog
