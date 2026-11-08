%define debug_package %{nil}

Name:     webapp-manager
Summary: Web Application Manager
Version:  master.mint22
Release:  4%{?dist}
Group: admin
License: GPLv3
Source0: https://github.com/linuxmint/%{name}/archive/refs/tags/%{version}.tar.gz

BuildArch:	noarch
BuildRequires: make
BuildRequires:  python3-devel
BuildRequires: desktop-file-utils
BuildRequires: perl-Locale-Msgfmt
BuildRequires:	gettext
Requires:	python
Requires:	python3-beautifulsoup4
Requires:	python3-configobj
Requires:	python3-gobject
Requires:	python3-pillow
Requires:	python3-setproctitle
Requires:	python3-tldextract
Requires:	xapps
Requires: dconf
Requires: python3
Requires: python3-configobj
Requires: python3-gobject
Requires: python3-setproctitle
Requires: python3-tldextract
Requires: xapps
Requires: xapp-symbolic-icons


%description
Launch websites as if they were apps.

# Terra's builds up to master.mint22-2 packaged this path as a directory, and
# Terra's -3 changed it to a file. RPM cannot replace a directory with a file,
# so remove the old directory before RPM checks for file conflicts.
%pretrans -p <lua>
local path = "/usr/share/desktop-directories/webapps-webapps.directory"
local st = posix.stat(path)
if st and st.type == "directory" then
  os.remove(path .. "/webapps-webapps.directory")
  os.remove(path)
end

%prep
%autosetup

%build
make %{?_smp_mflags}

%install
mkdir -p %{buildroot}
cp -a usr %{buildroot}
# remove duplicate .desktop file
rm -rf %{buildroot}/%{_datadir}/applications/kde4
install -Dm 644 etc/xdg/menus/applications-merged/webapps.menu -t %{buildroot}%{_sysconfdir}/xdg/menus/applications-merged
# upstream hides the launcher on KDE, Nobara's default desktop
sed -i '/^NotShowIn=KDE;$/d' %{buildroot}%{_datadir}/applications/%{name}.desktop

%files
%doc README.md
%license LICENSE
%{_bindir}/%{name}
/usr/lib/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/glib-2.0/schemas/org.x.%{name}.gschema.xml
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg
%{_datadir}/locale/*/LC_MESSAGES/%{name}.mo
%{_datadir}/%{name}
%{_datadir}/desktop-directories/webapps-webapps.directory
%{_datadir}/icons/hicolor/scalable/categories/applications-webapps.svg
%{_sysconfdir}/xdg/menus/applications-merged/webapps.menu
