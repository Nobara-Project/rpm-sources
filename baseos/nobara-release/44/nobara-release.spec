%define release_name Forty Four
%define is_rawhide 0

%define eol_date 2026-12-02

%define dist_version 44
%define rhel_dist_version 12

%if %{is_rawhide}
%define bug_version rawhide
%define releasever rawhide
%define doc_version rawhide
%else
%define bug_version %{dist_version}
%define releasever %{dist_version}
%define doc_version f%{dist_version}
%endif

%bcond basic 1
%bcond kde_desktop 1
%bcond workstation 1
%bcond server 1

Summary:        Nobara release files
Name:           nobara-release
Version:        44
# The numbering is 0.<r> before a given Fedora Linux release is released,
# with r starting at 1, and then just <r>, with r starting again at 1.
# Use '%%autorelease -p' before final, and then drop the '-p'.
Release:        %autorelease -b6
License:        MIT
URL:            https://www.nobaraproject.org/

Source1:        LICENSE
Source2:        Fedora-Legal-README.txt

Source10:       85-display-manager.preset
Source11:       90-default.preset
Source12:       90-default-user.preset
Source13:       99-default-disable.preset
Source14:       80-server.preset
Source15:       80-workstation.preset
Source17:       org.projectatomic.rpmostree1.rules
Source18:       80-iot.preset
Source19:       distro-template.swidtag
Source20:       distro-edition-template.swidtag
Source21:       fedora-workstation.conf
Source22:       80-coreos.preset
Source23:       zezere-ignition-url
Source24:       80-iot-user.preset
Source25:       plasma-desktop.conf
Source26:       80-kde-desktop.preset
Source27:       81-desktop.preset
Source28:       longer-default-shutdown-timeout.conf
Source29:       org.gnome.settings-daemon.plugins.power.gschema.override
Source31:       20-fedora-defaults.conf

BuildArch:      noarch

Provides:       nobara-release = %{version}-%{release}
Provides:       nobara-release-variant = %{version}-%{release}
Obsoletes:      fedora-release
Obsoletes:      fedora-release-variant

Provides:       system-release
Provides:	fedora-release = %{version}-%{release}
Provides:       system-release(%{version})
Provides:       base-module(platform:f%{version})
Requires:       nobara-release-common = %{version}-%{release}

# fedora-release-common Requires: fedora-release-identity, so at least one
# package must provide it. This Recommends: pulls in
# fedora-release-identity-basic if nothing else is already doing so.
Recommends:     nobara-release-identity-basic


BuildRequires:  redhat-rpm-config > 121-1
BuildRequires:  systemd-rpm-macros

%description
Nobara release files such as various /etc/ files that define the release
and systemd preset files that determine which services are enabled by default.
# See https://docs.fedoraproject.org/en-US/packaging-guidelines/DefaultServices/ for details.


%package common
Summary: Nobara release files

Requires:   nobara-release-variant = %{version}-%{release}
Suggests:   nobara-release

Requires:   fedora-repos(%{version})
Requires:   nobara-release-identity = %{version}-%{release}
Provides:	nobara-release-common = %{version}-%{release}
Provides:	fedora-release-common
Obsoletes:	fedora-release-common


%if %{is_rawhide}
# Make $releasever return "rawhide" on Rawhide
# https://pagure.io/releng/issue/7445
Provides:       system-release(releasever) = %{releasever}
Provides:	generic-release
%endif

# Fedora ships a generic-release package to make the creation of Remixes
# easier, but it cannot coexist with the fedora-release[-*] packages, so we
# will explicitly conflict with it.
Conflicts:  generic-release

# rpm-ostree count me is now enabled in 90-default.preset
Obsoletes: fedora-release-ostree-counting <= 36-0.7

%description common
Release files common to all Editions and Spins of Nobara


%if %{with basic}
%package identity-basic
Summary:        Package providing the basic Nobara identity

RemovePathPostfixes: .basic
Provides:       nobara-release-identity = %{version}-%{release}
Obsoletes:      fedora-release-identity
Conflicts:      nobara-release-identity


%description identity-basic
Provides the necessary files for a Nobara installation that is not identifying
itself as a particular Edition or Spin.
%endif


%if %{with kde_desktop}
%package kde
Summary:        Base package for Fedora KDE Plasma Desktop-specific default configurations

RemovePathPostfixes: .kde-desktop
Provides:       nobara-release = %{version}-%{release}
Provides:       nobara-release-kde
Provides:       nobara-release-variant = %{version}-%{release}
Provides:       fedora-release = %{version}-%{release}
Provides:       fedora-release-variant = %{version}-%{release}
Obsoletes:       fedora-release
Obsoletes:       fedora-release-variant
Obsoletes:       fedora-release-kde
Provides:       system-release
Provides:       system-release(%{version})
Provides:       base-module(platform:f%{version})
Requires:       nobara-release-common = %{version}-%{release}

# fedora-release-common Requires: fedora-release-identity, so at least one
# package must provide it. This Recommends: pulls in
# fedora-release-identity-kde if nothing else is already doing so.
Recommends:     nobara-release-identity-kde


%description kde
Provides a base package for Nobara KDE Plasma-specific configuration files to
depend on as well as KDE Plasma system defaults.


%package identity-kde
Summary:        Package providing the identity for Nobara KDE Plasma Spin

RemovePathPostfixes: .kde-desktop
Provides:       nobara-release-identity = %{version}-%{release}
Provides:       nobara-release-identity-kde
Obsoletes:       fedora-release-identity
Obsoletes:       fedora-release-identity-kde
Conflicts:      fedora-release-identity
Requires(meta): nobara-release-kde = %{version}-%{release}


%description identity-kde
Provides the necessary files for a Nobara installation that is identifying
itself as Nobara KDE Plasma Spin.
%endif

%if %{with workstation}
%package workstation
Summary:        Base package for Nobara GNOME-specific default configurations

RemovePathPostfixes: .workstation
Provides:       nobara-release = %{version}-%{release}
Provides:       nobara-release-variant = %{version}-%{release}
Provides:       fedora-release = %{version}-%{release}
Provides:       fedora-release-variant = %{version}-%{release}
Provides:       nobara-release-workstation
Obsoletes:       fedora-release
Obsoletes:       fedora-release-variant
Obsoletes:       fedora-release-workstation
Provides:       system-release
Provides:       system-release(%{version})
Provides:       base-module(platform:f%{version})
Requires:       nobara-release-common = %{version}-%{release}
Provides:       system-release-product

# Third-party repositories, disabled by default unless the user opts in through fedora-third-party
# Requires(meta) to avoid ordering loops - does not need to be installed before the release package
# Keep this in sync with silverblue above
#Requires(meta):	fedora-flathub-remote
Requires(meta):	fedora-workstation-repositories

# fedora-release-common Requires: fedora-release-identity, so at least one
# package must provide it. This Recommends: pulls in
# fedora-release-identity-workstation if nothing else is already doing so.
Recommends:     nobara-release-identity-workstation


%description workstation
Provides a base package for Nobara GNOME-specific configuration files to
depend on.


%package identity-workstation
Summary:        Package providing the identity for Nobara GNOME Edition

RemovePathPostfixes: .workstation
Provides:       nobara-release-identity = %{version}-%{release}
Provides:       nobara-release-identity-workstation
Obsoletes:       fedora-release-identity
Obsoletes:       fedora-release-identity-workstation
Conflicts:      fedora-release-identity


%description identity-workstation
Provides the necessary files for a Nobara installation that is identifying
itself as Nobara GNOME Edition.
%endif

%if %{with server}
%package server
Summary:        Base package for Fedora Server-specific default configurations

RemovePathPostfixes: .server
Provides:       fedora-release = %{version}-%{release}
Provides:       fedora-release-variant = %{version}-%{release}
Provides:       system-release
Provides:       system-release(%{version})
Requires:       fedora-release-common = %{version}-%{release}

# fedora-release-common Requires: fedora-release-identity, so at least one
# package must provide it. This Recommends: pulls in
# fedora-release-identity-server if nothing else is already doing so.
Recommends:     fedora-release-identity-server


%description server
Provides a base package for Fedora Server-specific configuration files to
depend on.


%package identity-server
Summary:        Package providing the identity for Fedora Server Edition

RemovePathPostfixes: .server
Provides:       fedora-release-identity = %{version}-%{release}
Conflicts:      fedora-release-identity
Requires(meta): fedora-release-server = %{version}-%{release}


%description identity-server
Provides the necessary files for a Fedora installation that is identifying
itself as Fedora Server Edition.
%endif


%prep
mkdir -p licenses
sed 's|@@VERSION@@|%{dist_version}|g' %{SOURCE2} >licenses/Fedora-Legal-README.txt

%build

%install
install -d %{buildroot}%{_prefix}/lib
echo "Nobara release %{version} (%{release_name})" > %{buildroot}%{_prefix}/lib/nobara-release
echo "cpe:/o:fedoraproject:fedora:%{version}" > %{buildroot}%{_prefix}/lib/system-release-cpe

# Symlink the -release files
install -d %{buildroot}%{_sysconfdir}
ln -s ../usr/lib/nobara-release %{buildroot}%{_sysconfdir}/nobara-release
ln -s ../usr/lib/system-release-cpe %{buildroot}%{_sysconfdir}/system-release-cpe
ln -s nobara-release %{buildroot}%{_sysconfdir}/redhat-release
ln -s nobara-release %{buildroot}%{_sysconfdir}/system-release

# Create the common os-release file
%{lua:
  function starts_with(str, start)
   return str:sub(1, #start) == start
  end
}
%define starts_with(str,prefix) (%{expand:%%{lua:print(starts_with(%1, %2) and "1" or "0")}})
%if %{starts_with "a%{release}" "a0"}
  %global prerelease \ Prerelease
%endif

# -------------------------------------------------------------------------
# Definitions for /etc/os-release and for macros in macros.dist.  These
# macros are useful for spec files where distribution-specific identifiers
# are used to customize packages.

# Name of vendor / name of distribution. Typically used to identify where
# the binary comes from in --help or --version messages of programs.
# Examples: gdb.spec, clang.spec
%global dist_vendor Nobara
%global dist_name   Nobara Linux

# URL of the homepage of the distribution
# Example: gstreamer1-plugins-base.spec
%global dist_home_url https://nobaraproject.org/

# Bugzilla / bug reporting URLs shown to users.
# Examples: gcc.spec
%global dist_bug_report_url https://github.com/nobara-project/rpm-baseos

# debuginfod server, as used in elfutils.spec.
%global dist_debuginfod_url https://github.com/nobara-project/rpm-baseos
# -------------------------------------------------------------------------

cat << EOF >> os-release
NAME="Nobara Linux"
VERSION="%{dist_version} (%{release_name}%{?prerelease})"
ID=nobara
ID_LIKE="rhel centos fedora"
VERSION_ID=%{dist_version}
VERSION_CODENAME=""
PLATFORM_ID="platform:f%{dist_version}"
PRETTY_NAME="Nobara Linux %{dist_version} (%{release_name}%{?prerelease})"
ANSI_COLOR="0;38;2;60;110;180"
LOGO=nobara-logo-icon
CPE_NAME="cpe:/o:nobaraproject:nobara:%{dist_version}"
DEFAULT_HOSTNAME="nobara"
HOME_URL="%{dist_home_url}"
DOCUMENTATION_URL="https://wiki.nobaraproject.org/"
SUPPORT_URL="https://www.nobaraproject.org/"
BUG_REPORT_URL="%{dist_bug_report_url}"
REDHAT_BUGZILLA_PRODUCT="Nobara"
REDHAT_BUGZILLA_PRODUCT_VERSION=%{bug_version}
REDHAT_SUPPORT_PRODUCT="Nobara"
REDHAT_SUPPORT_PRODUCT_VERSION=%{bug_version}
SUPPORT_END=%{eol_date}
EOF

# Create the common /etc/issue
echo "\S" > %{buildroot}%{_prefix}/lib/issue
echo "Kernel \r on \m (\l)" >> %{buildroot}%{_prefix}/lib/issue
echo >> %{buildroot}%{_prefix}/lib/issue
ln -s ../usr/lib/issue %{buildroot}%{_sysconfdir}/issue

# Create /etc/issue.net
echo "\S" > %{buildroot}%{_prefix}/lib/issue.net
echo "Kernel \r on \m (\l)" >> %{buildroot}%{_prefix}/lib/issue.net
ln -s ../usr/lib/issue.net %{buildroot}%{_sysconfdir}/issue.net

# Create /etc/issue.d
mkdir -p %{buildroot}%{_sysconfdir}/issue.d

mkdir -p %{buildroot}%{_swidtagdir}

# Create os-release files for the different editions

%if %{with basic}
# Basic
cp -p os-release \
      %{buildroot}%{_prefix}/lib/os-release.basic
%endif

%if %{with kde_desktop}
# KDE Plasma Desktop
cp -p os-release \
      %{buildroot}%{_prefix}/lib/os-release.kde-desktop
echo "VARIANT=\"KDE Plasma Desktop Edition\"" >> %{buildroot}%{_prefix}/lib/os-release.kde-desktop
# kept as-is from the spin to prevent third-party stuff from breaking
echo "VARIANT_ID=kde" >> %{buildroot}%{_prefix}/lib/os-release.kde-desktop
sed -i -e "s|(%{release_name}%{?prerelease})|(KDE Plasma Desktop Edition%{?prerelease})|g" %{buildroot}%{_prefix}/lib/os-release.kde-desktop
sed -e "s#\$version#%{bug_version}#g" -e 's/$edition/KDE Desktop/;s/<!--.*-->//;/^$/d' %{SOURCE20} > %{buildroot}%{_swidtagdir}/org.fedoraproject.Fedora-edition.swidtag.kde-desktop
# Add plasma-desktop to dnf protected packages list for KDE Desktop
install -Dm0644 %{SOURCE25} -t %{buildroot}%{_sysconfdir}/dnf/protected.d/
%endif

%if %{with server}
# Server
cp -p os-release \
      %{buildroot}%{_prefix}/lib/os-release.server
echo "VARIANT=\"Server Edition\"" >> %{buildroot}%{_prefix}/lib/os-release.server
echo "VARIANT_ID=server" >> %{buildroot}%{_prefix}/lib/os-release.server
sed -i -e "s|(%{release_name}%{?prerelease})|(Server Edition%{?prerelease})|g" %{buildroot}%{_prefix}/lib/os-release.server
sed -e "s#\$version#%{bug_version}#g" -e 's/$edition/Server/;s/<!--.*-->//;/^$/d' %{SOURCE20} > %{buildroot}%{_swidtagdir}/org.fedoraproject.Fedora-edition.swidtag.server
sed -i -e "/^DEFAULT_HOSTNAME=/d" %{buildroot}%{_prefix}/lib/os-release.server
install -Dm0644 %{SOURCE14} -t %{buildroot}%{_prefix}/lib/systemd/system-preset/
install -Dm0644 %{SOURCE28} -t %{buildroot}%{_prefix}/lib/systemd/system.conf.d/
install -Dm0644 %{SOURCE28} -t %{buildroot}%{_prefix}/lib/systemd/user.conf.d/
%endif


%if %{with workstation}
# GNOME
cp -p os-release \
      %{buildroot}%{_prefix}/lib/os-release.workstation
echo "VARIANT=\"GNOME Edition\"" >> %{buildroot}%{_prefix}/lib/os-release.workstation
echo "VARIANT_ID=workstation" >> %{buildroot}%{_prefix}/lib/os-release.workstation
sed -i -e "s|(%{release_name}%{?prerelease})|(GNOME Edition%{?prerelease})|g" %{buildroot}%{_prefix}/lib/os-release.workstation
sed -e "s#\$version#%{bug_version}#g" -e 's/$edition/GNOME/;s/<!--.*-->//;/^$/d' %{SOURCE20} > %{buildroot}%{_swidtagdir}/org.fedoraproject.Fedora-edition.swidtag.workstation
# Add Fedora GNOME dnf protected packages list
install -Dm0644 %{SOURCE21} -t %{buildroot}%{_sysconfdir}/dnf/protected.d/
%endif

%if %{with silverblue} || %{with workstation}
# Silverblue and GNOME
install -Dm0644 %{SOURCE15} -t %{buildroot}%{_prefix}/lib/systemd/system-preset/
install -Dm0644 %{SOURCE27} -t %{buildroot}%{_prefix}/lib/systemd/system-preset/
%endif

%if %{with kde_desktop} || %{with kinoite}
# Common desktop preset and spin specific preset
install -Dm0644 %{SOURCE26} -t %{buildroot}%{_prefix}/lib/systemd/system-preset/
install -Dm0644 %{SOURCE27} -t %{buildroot}%{_prefix}/lib/systemd/system-preset/
%endif


# Create the symlink for /etc/os-release
ln -s ../usr/lib/os-release %{buildroot}%{_sysconfdir}/os-release

# Set up the dist tag macros
install -d -m 755 %{buildroot}%{_rpmconfigdir}/macros.d
cat >> %{buildroot}%{_rpmconfigdir}/macros.d/macros.dist << EOF
# dist macros.

%%__bootstrap         ~bootstrap
%%fedora              %{dist_version}
%%fc%{dist_version}                1
%%distcore            .fc%%{fedora}
%%dist                %%{!?distprefix0:%%{?distprefix}}%%{expand:%%{lua:for i=0,9999 do print("%%{?distprefix" .. i .."}") end}}%%{distcore}%%{?with_bootstrap:%%{__bootstrap}}
%%dist_vendor         %{dist_vendor}
%%dist_name           %{dist_name}
%%dist_home_url       %{dist_home_url}
%%dist_bug_report_url %{dist_bug_report_url}
%%dist_debuginfod_url %{dist_debuginfod_url}
EOF

# Install licenses
install -pm 0644 %{SOURCE1} licenses/LICENSE

# Default system wide
install -Dm0644 %{SOURCE10} -t %{buildroot}%{_prefix}/lib/systemd/system-preset/
install -Dm0644 %{SOURCE11} -t %{buildroot}%{_prefix}/lib/systemd/system-preset/
install -Dm0644 %{SOURCE12} -t %{buildroot}%{_prefix}/lib/systemd/user-preset/
# The same file is installed in two places with identical contents
install -Dm0644 %{SOURCE13} -t %{buildroot}%{_prefix}/lib/systemd/system-preset/
install -Dm0644 %{SOURCE13} -t %{buildroot}%{_prefix}/lib/systemd/user-preset/

# Create distro-level SWID tag file
install -d %{buildroot}%{_swidtagdir}
sed -e "s#\$version#%{bug_version}#g" -e 's/<!--.*-->//;/^$/d' %{SOURCE19} > %{buildroot}%{_swidtagdir}/org.fedoraproject.Fedora-%{bug_version}.swidtag
install -d %{buildroot}%{_sysconfdir}/swid/swidtags.d
ln -s --relative %{buildroot}%{_swidtagdir} %{buildroot}%{_sysconfdir}/swid/swidtags.d/fedoraproject.org

# Install DNF 5 configuration defaults
install -Dm0644 %{SOURCE31} -t %{buildroot}%{_prefix}/share/dnf5/libdnf.conf.d/


%files common
%license licenses/LICENSE licenses/Fedora-Legal-README.txt
%{_prefix}/lib/nobara-release
%{_prefix}/lib/system-release-cpe
%{_sysconfdir}/os-release
%{_sysconfdir}/nobara-release
%{_sysconfdir}/redhat-release
%{_sysconfdir}/system-release
%{_sysconfdir}/system-release-cpe
%attr(0644,root,root) %{_prefix}/lib/issue
%config(noreplace) %{_sysconfdir}/issue
%attr(0644,root,root) %{_prefix}/lib/issue.net
%config(noreplace) %{_sysconfdir}/issue.net
%dir %{_sysconfdir}/issue.d
%attr(0644,root,root) %{_rpmconfigdir}/macros.d/macros.dist
%dir %{_prefix}/lib/systemd/user-preset/
%{_prefix}/lib/systemd/user-preset/90-default-user.preset
%{_prefix}/lib/systemd/user-preset/99-default-disable.preset
%dir %{_prefix}/lib/systemd/system-preset/
%{_prefix}/lib/systemd/system-preset/85-display-manager.preset
%{_prefix}/lib/systemd/system-preset/90-default.preset
%{_prefix}/lib/systemd/system-preset/99-default-disable.preset
%dir %{_swidtagdir}
%{_swidtagdir}/org.fedoraproject.Fedora-%{bug_version}.swidtag
%dir %{_sysconfdir}/swid
%{_sysconfdir}/swid/swidtags.d
%{_prefix}/share/dnf5/libdnf.conf.d/20-fedora-defaults.conf


%if %{with basic}
%files
%files identity-basic
%{_prefix}/lib/os-release.basic
%endif



%if %{with kde_desktop}
%files kde
%files identity-kde
%{_prefix}/lib/os-release.kde-desktop
%{_prefix}/lib/systemd/system-preset/80-kde-desktop.preset
%{_prefix}/lib/systemd/system-preset/81-desktop.preset
%attr(0644,root,root) %{_swidtagdir}/org.fedoraproject.Fedora-edition.swidtag.kde-desktop
%{_sysconfdir}/dnf/protected.d/plasma-desktop.conf
%endif

%if %{with server}
%files server
%files identity-server
%{_prefix}/lib/os-release.server
%{_prefix}/lib/systemd/system-preset/80-server.preset
%{_prefix}/lib/systemd/system.conf.d/longer-default-shutdown-timeout.conf
%{_prefix}/lib/systemd/user.conf.d/longer-default-shutdown-timeout.conf
%attr(0644,root,root) %{_swidtagdir}/org.fedoraproject.Fedora-edition.swidtag.server
%endif

%if %{with workstation}
%files workstation
%files identity-workstation
%{_prefix}/lib/os-release.workstation
%attr(0644,root,root) %{_swidtagdir}/org.fedoraproject.Fedora-edition.swidtag.workstation
%{_sysconfdir}/dnf/protected.d/fedora-workstation.conf
# Keep this in sync with silverblue above
%{_prefix}/lib/systemd/system-preset/80-workstation.preset
%{_prefix}/lib/systemd/system-preset/81-desktop.preset
%endif

%changelog
%autochangelog
