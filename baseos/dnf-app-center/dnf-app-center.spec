Name:           dnf-app-center
Version:        0.1.0
Release:        6%{?dist}
Summary:        GTK App Center for DNF/AppStream with updater tray service

# Replace this with your real SPDX license identifier before distributing publicly.
License:        GPL-2.0-only
URL:            https://github.com/Nobara-Project/dnf-app-center
Source0:        %{url}/archive/refs/tags/0.1.0.tar.gz
%global _update_feed_url https://updates.nobaraproject.org/updates.txt

BuildArch:      noarch

BuildRequires:  desktop-file-utils
BuildRequires:  pyproject-rpm-macros
BuildRequires:  python3-devel
BuildRequires:  gettext

Requires:       appstream
Requires:       python3-dbus
Requires:       gtk3
Requires:       gtk4
Requires:       libadwaita
Requires:       libayatana-appindicator-gtk3
Requires:       pbcli
Requires:       python3-gobject
Requires:       python3-libdnf5
Requires:       xdg-utils

Provides:       dnf-app-center
Provides:       yumex
Provides:       yumex-dnf
Provides:       yumex-updater
Obsoletes:      yumex
Obsoletes:      yumex-dnf
Obsoletes:      yumex-updater

%description
DNF App Center is a GTK-based App Center for Fedora-family systems that uses
AppStream for catalog metadata and libdnf5 for package state and transactions.

This package installs:
- the main GUI app (dnf-app-center)
- the updater tray service (dnf-app-center-updater)
- a desktop launcher
- a session autostart entry for the updater service

%prep
%autosetup -n %{name}-%{version}
sed -i "s#@UPDATE_FEED_URL@#%{_update_feed_url}#g" appcenter/updater_config.py


%generate_buildrequires
%pyproject_buildrequires -r

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files appcenter

for lang in $(cat po/LINGUAS); do
install -d %{buildroot}%{_datadir}/locale/${lang}/LC_MESSAGES
msgfmt po/${lang}.po -o %{buildroot}%{_datadir}/locale/${lang}/LC_MESSAGES/org.dnf.AppCenter.mo
done

install -d %{buildroot}%{_datadir}/applications
install -pm 0644 org.dnf.AppCenter.desktop \
  %{buildroot}%{_datadir}/applications/org.dnf.AppCenter.desktop

install -d %{buildroot}%{_datadir}/icons/hicolor/scalable/apps
install -pm 0644 appcenter/assets/org.dnf.AppCenter.svg \
  %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/org.dnf.AppCenter.svg

install -d %{buildroot}%{_sysconfdir}/xdg/autostart
install -pm 0644 org.dnf.AppCenter.Updater.desktop \
  %{buildroot}%{_sysconfdir}/xdg/autostart/org.dnf.AppCenter.Updater.desktop

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/org.dnf.AppCenter.desktop
# The updater autostart entry is also a desktop file.
desktop-file-validate %{buildroot}%{_sysconfdir}/xdg/autostart/org.dnf.AppCenter.Updater.desktop

%files -f %{pyproject_files}
%doc README.md
%license COPYING
%{_bindir}/dnf-app-center
%{_bindir}/dnf-app-center-updater
%{_datadir}/applications/org.dnf.AppCenter.desktop
%{_datadir}/icons/hicolor/scalable/apps/org.dnf.AppCenter.svg
%config(noreplace) %{_sysconfdir}/xdg/autostart/org.dnf.AppCenter.Updater.desktop

%lang(de) %{_datadir}/locale/de/LC_MESSAGES/org.dnf.AppCenter.mo
%lang(es) %{_datadir}/locale/es/LC_MESSAGES/org.dnf.AppCenter.mo
%lang(fr) %{_datadir}/locale/fr/LC_MESSAGES/org.dnf.AppCenter.mo
%lang(it) %{_datadir}/locale/it/LC_MESSAGES/org.dnf.AppCenter.mo
%lang(pt_BR) %{_datadir}/locale/pt_BR/LC_MESSAGES/org.dnf.AppCenter.mo
%lang(ru) %{_datadir}/locale/ru/LC_MESSAGES/org.dnf.AppCenter.mo
%lang(ja) %{_datadir}/locale/ja/LC_MESSAGES/org.dnf.AppCenter.mo
%lang(ko) %{_datadir}/locale/ko/LC_MESSAGES/org.dnf.AppCenter.mo
%lang(zh_CN) %{_datadir}/locale/zh_CN/LC_MESSAGES/org.dnf.AppCenter.mo
%lang(zh_TW) %{_datadir}/locale/zh_TW/LC_MESSAGES/org.dnf.AppCenter.mo

%changelog
* Sat Mar 14 2026 Tom Crider <gloriouseggroll@gmail.com> - 0.1.0-1
- Initial RPM packaging draft for DNF App Center
