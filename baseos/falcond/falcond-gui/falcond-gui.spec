Name:           falcond-gui
Version:        1.0.3
Release:        %autorelease
Summary:        A GTK4/LibAdwaita application to control and monitor the Falcond gaming optimization daemon.

License:        MIT
URL:            https://git.pika-os.com/general-packages/%{name}
Source0:        %{URL}/archive/v%{version}.tar.gz

ExclusiveArch:	x86_64 aarch64

BuildRequires:	anda-srpm-macros
BuildRequires:  cargo-rpm-macros
BuildRequires:  desktop-file-utils
BuildRequires:  gcc
BuildRequires:  gtk4-devel
BuildRequires:  libadwaita-devel
BuildRequires:  mold
BuildRequires:  pkgconfig
BuildRequires:  rust

Requires:       falcond

%description
falcond-gui provides a user-friendly graphical interface for managing falcond. It allows users to view the status of the daemon and customize its behavior.

%prep
%autosetup -n %{name}
cd %{name}
%cargo_prep_online

%build
cd %{name}
%cargo_build
%{cargo_license_summary_online}
%{cargo_license_online} > ../LICENSE.dependencies

%install
cd %{name}
%cargo_install
install -Dpm 0644 res/com.pikaos.falcondgui.desktop %{buildroot}%{_datadir}/applications/com.pikaos.falcondgui.desktop
install -dm 0755 %{buildroot}%{_datadir}/icons/hicolor/512x512/apps
install -pm 0644 res/com.pikaos.falcondgui.png %{buildroot}%{_datadir}/icons/hicolor/512x512/apps/com.pikaos.falcondgui.png
desktop-file-validate %{buildroot}%{_datadir}/applications/com.pikaos.falcondgui.desktop

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor/ &>/dev/null || :

%files
%doc	 README.md
%license LICENSE.md
%license LICENSE.dependencies
%{_bindir}/%{name}
%{_datadir}/applications/com.pikaos.falcondgui.desktop
%{_datadir}/icons/hicolor/512x512/apps/com.pikaos.falcondgui.png

%changelog
* Fri May 22 2026 LionHeartP <LionHeartP@proton.me> - 1.0.3-1
- Update to 1.0.3

* Sat Mar 07 2026 Radical <radical@radical.fun> - 1.2.3-1
- Update specfile to allow aarch64 build

* Thu Feb 19 2026 LionHeartP <LionHeartP@proton.me> - 1.0.2-1
- Update to 1.0.2

* Mon Jan 12 2026 LionHeartP <LionHeartP@proton.me> - 1.0.1-1
- Update to 1.0.1

* Thu Jan 01 2026 LionHeartP <LionHeartP@proton.me> - 1.0.0-1
- Initial package for falcond-gui
