%define debug_package %{nil}

Name:     webapp-manager
Summary: Web Application Manager
Version:  master.mint21
Release:  1%{?dist}
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


%description
Launch websites as if they were apps.

%prep
%setup -q

%build
make %{?_smp_mflags}

%install
mkdir -p %{buildroot}
cp -a usr %{buildroot}

%files
%{_bindir}/%{name}
/usr/lib/%{name}
%{_datadir}/applications/kde4/%{name}.desktop
%{_datadir}/applications/%{name}.desktop
#%{_datadir}/doc/%{name}
%{_datadir}/glib-2.0/schemas/org.x.%{name}.gschema.xml
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg
%{_datadir}/locale/*/LC_MESSAGES/%{name}.mo
%{_datadir}/%{name}
%{_datadir}/desktop-directories/webapps-webapps.directory
%{_datadir}/icons/hicolor/scalable/categories/applications-webapps.svg
