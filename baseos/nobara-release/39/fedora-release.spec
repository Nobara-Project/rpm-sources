## START: Set by rpmautospec
## (rpmautospec version 0.3.5)
## RPMAUTOSPEC: autorelease
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 31;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

%define release_name Thirty Nine
%define is_rawhide 0

%define eol_date 2025-05-13

%define dist_version 39
%define rhel_dist_version 10

%if %{is_rawhide}
%define bug_version rawhide
%define releasever rawhide
%define doc_version rawhide
%else
%define bug_version %{dist_version}
%define releasever %{dist_version}
%define doc_version f%{dist_version}
%endif

%if 0%{?eln}
%bcond_with basic
%bcond_without eln
%bcond_with kde
%bcond_with workstation
%else
%bcond_with eln
%bcond_without kde
%bcond_without workstation
%endif

%global dist %{?eln:.eln%{eln}}

Summary:        Nobara release files
Name:           nobara-release
Version:        39
# The numbering is 0.<r> before a given Fedora Linux release is released,
# with r starting at 1, and then just <r>, with r starting again at 1.
# Use '%%autorelease -p' before final, and then drop the '-p'.
Release:        %autorelease
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
Source26:       80-kde.preset
Source27:       81-desktop.preset
Source28:       longer-default-shutdown-timeout.conf
Source29:       org.gnome.settings-daemon.plugins.power.gschema.override

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
Requires:	nobara-login

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

%if %{with eln}
%package eln
Summary:        Base package for Nobara ELN specific default configurations

RemovePathPostfixes: .eln
Provides:       nobara-release = %{version}-%{release}
Provides:       nobara-release-variant = %{version}-%{release}
Provides:       fedora-release = %{version}-%{release}
Provides:       fedora-release-variant = %{version}-%{release}
Obsoletes:       fedora-release
Obsoletes:       fedora-release-variant
Provides:       system-release
Provides:       system-release(%{version})
Provides:       base-module(platform:eln)
Requires:       nobara-release-common = %{version}-%{release}
Provides:       system-release-product
Requires:       fedora-repos-eln

Obsoletes:      redhat-release
Provides:       redhat-release

# fedora-release-common Requires: fedora-release-identity, so at least one
# package must provide it. This Recommends: pulls in
# fedora-release-identity-eln if nothing else is already doing so.
Recommends:     nobara-release-identity-eln


%description eln
Provides a base package for Nobara ELN specific configuration files to
depend on.


%package identity-eln
Summary:        Package providing the identity for Nobara ELN

RemovePathPostfixes: .eln
Provides:       nobara-release-identity = %{version}-%{release}
Conflicts:      fedora-release-identity
Obsoletes:      fedora-release-identity


%description identity-eln
Provides the necessary files for a Nobara installation that is identifying
itself as Nobara ELN.
%endif


%if %{with kde}
%package kde
Summary:        Base package for Nobara KDE Plasma-specific default configurations

RemovePathPostfixes: .kde
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

RemovePathPostfixes: .kde
Provides:       nobara-release-identity = %{version}-%{release}
Provides:       nobara-release-identity-kde
Obsoletes:       fedora-release-identity
Obsoletes:       fedora-release-identity-kde
Conflicts:      fedora-release-identity


%description identity-kde
Provides the necessary files for a Nobara installation that is identifying
itself as Nobara KDE Plasma Spin.
%endif

%if %{with workstation}
%package workstation
Summary:        Base package for Nobara Workstation-specific default configurations

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
Requires(meta):	fedora-flathub-remote
Requires(meta):	fedora-workstation-repositories

# fedora-release-common Requires: fedora-release-identity, so at least one
# package must provide it. This Recommends: pulls in
# fedora-release-identity-workstation if nothing else is already doing so.
Recommends:     nobara-release-identity-workstation


%description workstation
Provides a base package for Nobara Workstation-specific configuration files to
depend on.


%package identity-workstation
Summary:        Package providing the identity for Nobara Workstation Edition

RemovePathPostfixes: .workstation
Provides:       nobara-release-identity = %{version}-%{release}
Provides:       nobara-release-identity-workstation
Obsoletes:       fedora-release-identity
Obsoletes:       fedora-release-identity-workstation
Conflicts:      fedora-release-identity


%description identity-workstation
Provides the necessary files for a Nobara installation that is identifying
itself as Nobara Workstation Edition.
%endif

%prep
sed -i 's|@@VERSION@@|%{dist_version}|g' %{SOURCE2}

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
%global dist_bug_report_url https://gitlab.com/gloriouseggroll/nobara-images

# debuginfod server, as used in elfutils.spec.
%global dist_debuginfod_url https://gitlab.com/gloriouseggroll/nobara-images
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
DOCUMENTATION_URL="https://www.nobaraproject.org/"
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
echo "Kernel \r on an \m (\l)" >> %{buildroot}%{_prefix}/lib/issue
echo >> %{buildroot}%{_prefix}/lib/issue
ln -s ../usr/lib/issue %{buildroot}%{_sysconfdir}/issue

# Create /etc/issue.net
echo "\S" > %{buildroot}%{_prefix}/lib/issue.net
echo "Kernel \r on an \m (\l)" >> %{buildroot}%{_prefix}/lib/issue.net
ln -s ../usr/lib/issue.net %{buildroot}%{_sysconfdir}/issue.net

# Create /etc/issue.d
mkdir -p %{buildroot}%{_sysconfdir}/issue.d

mkdir -p %{buildroot}%{_swidtagdir}

# Create os-release files for the different editions

%if %{with eln}
# ELN
cp -p os-release \
      %{buildroot}%{_prefix}/lib/os-release.eln
echo "VARIANT=\"ELN\"" >> %{buildroot}%{_prefix}/lib/os-release.eln
echo "VARIANT_ID=eln" >> %{buildroot}%{_prefix}/lib/os-release.eln
sed -i -e 's|PLATFORM_ID=.*|PLATFORM_ID="platform:eln"|' %{buildroot}/%{_prefix}/lib/os-release.eln
sed -i -e 's|PRETTY_NAME=.*|PRETTY_NAME="Nobara ELN"|' %{buildroot}/%{_prefix}/lib/os-release.eln
sed -i -e 's|DOCUMENTATION_URL=.*|DOCUMENTATION_URL="https://www.nobaraproject.org/en-US/eln/"|' %{buildroot}%{_prefix}/lib/os-release.eln
sed -i -e "/^DEFAULT_HOSTNAME=/d" %{buildroot}%{_prefix}/lib/os-release.eln
sed -e "s#\$version#%{bug_version}#g" -e 's/$edition/ELN/;s/<!--.*-->//;/^$/d' %{SOURCE20} > %{buildroot}%{_swidtagdir}/org.fedoraproject.Fedora-edition.swidtag.eln
%endif

%if %{with kde}
# KDE Plasma
cp -p os-release \
      %{buildroot}%{_prefix}/lib/os-release.kde
echo "VARIANT=\"KDE Plasma\"" >> %{buildroot}%{_prefix}/lib/os-release.kde
echo "VARIANT_ID=kde" >> %{buildroot}%{_prefix}/lib/os-release.kde
sed -i -e "s|(%{release_name}%{?prerelease})|(KDE Plasma%{?prerelease})|g" %{buildroot}%{_prefix}/lib/os-release.kde
sed -e "s#\$version#%{bug_version}#g" -e 's/$edition/KDE/;s/<!--.*-->//;/^$/d' %{SOURCE20} > %{buildroot}%{_swidtagdir}/org.fedoraproject.Fedora-edition.swidtag.kde
# Add plasma-desktop to dnf protected packages list for KDE
install -Dm0644 %{SOURCE25} -t %{buildroot}%{_sysconfdir}/dnf/protected.d/
%endif

%if %{with workstation}
# Workstation
cp -p os-release \
      %{buildroot}%{_prefix}/lib/os-release.workstation
echo "VARIANT=\"GNOME Edition\"" >> %{buildroot}%{_prefix}/lib/os-release.workstation
echo "VARIANT_ID=gnome" >> %{buildroot}%{_prefix}/lib/os-release.workstation
sed -i -e "s|(%{release_name}%{?prerelease})|(GNOME Edition%{?prerelease})|g" %{buildroot}%{_prefix}/lib/os-release.workstation
sed -e "s#\$version#%{bug_version}#g" -e 's/$edition/GNOME/;s/<!--.*-->//;/^$/d' %{SOURCE20} > %{buildroot}%{_swidtagdir}/org.fedoraproject.Fedora-edition.swidtag.workstation
# Add Nobara GNOME dnf protected packages list
install -Dm0644 %{SOURCE21} -t %{buildroot}%{_sysconfdir}/dnf/protected.d/
%endif

%if %{with silverblue} || %{with workstation}
# Silverblue and Workstation
install -Dm0644 %{SOURCE15} -t %{buildroot}%{_prefix}/lib/systemd/system-preset/
install -Dm0644 %{SOURCE27} -t %{buildroot}%{_prefix}/lib/systemd/system-preset/
%endif

%if %{with kde} || %{with kinoite}
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
%if 0%{?eln}
%%rhel              %{rhel_dist_version}
%%el%{rhel_dist_version}                1
# Although eln is set in koji tags, we put it in the macros.dist file for local and mock builds.
%%eln              %{eln}
%%dist                %%{!?distprefix0:%%{?distprefix}}%%{expand:%%{lua:for i=0,9999 do print("%%{?distprefix" .. i .."}") end}}.el%%{eln}%%{?with_bootstrap:%{__bootstrap}}
%else
%%fedora              %{dist_version}
%%fc%{dist_version}                1
%%dist                %%{!?distprefix0:%%{?distprefix}}%%{expand:%%{lua:for i=0,9999 do print("%%{?distprefix" .. i .."}") end}}.fc%%{fedora}%%{?with_bootstrap:%{__bootstrap}}
%endif
%%dist_vendor         %{dist_vendor}
%%dist_name           %{dist_name}
%%dist_home_url       %{dist_home_url}
%%dist_bug_report_url %{dist_bug_report_url}
%%dist_debuginfod_url %{dist_debuginfod_url}
EOF

# Install licenses
mkdir -p licenses
install -pm 0644 %{SOURCE1} licenses/LICENSE
install -pm 0644 %{SOURCE2} licenses/Fedora-Legal-README.txt

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
ln -s %{_swidtagdir} %{buildroot}%{_sysconfdir}/swid/swidtags.d/fedoraproject.org


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


%if %{with basic}
%files
%files identity-basic
%{_prefix}/lib/os-release.basic
%endif



%if %{with eln}
%files eln
%files identity-eln
%{_prefix}/lib/os-release.eln
%attr(0644,root,root) %{_swidtagdir}/org.fedoraproject.Fedora-edition.swidtag.eln
%endif


%if %{with kde}
%files kde
%files identity-kde
%{_prefix}/lib/os-release.kde
%{_prefix}/lib/systemd/system-preset/80-kde.preset
%{_prefix}/lib/systemd/system-preset/81-desktop.preset
%attr(0644,root,root) %{_swidtagdir}/org.fedoraproject.Fedora-edition.swidtag.kde
%{_sysconfdir}/dnf/protected.d/plasma-desktop.conf
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
* Thu Apr 06 2023 Kevin Fenzi <kevin@scrye.com> - 38-34
- Set release to start at 1 for final release.

* Mon Apr 03 2023 Kevin Fenzi <kevin@scrye.com> - 38-0.33
- server: also keep the old 90s default timeout for shutdown

* Mon Mar 27 2023 Timothée Ravier <tim@siosm.fr> - 38-0.32
- Revert "Enable preset for ssh-host-keys-migration.service"

* Mon Mar 27 2023 Stephen Gallagher <sgallagh@redhat.com> - 38-0.31
- Server: disable auto-suspend when on AC power

* Sat Mar 04 2023 Dusty Mabe <dusty@dustymabe.com> - 38-0.30
- Enable preset for ssh-host-keys-migration.service

* Thu Mar 02 2023 Dusty Mabe <dusty@dustymabe.com> - 38-0.29
- Fix invalid longer-default-shutdown-timeout.conf

* Thu Mar 02 2023 Dusty Mabe <dusty@dustymabe.com> - 38-0.28
- make recent shutdown timeout conf filename more appropriate

* Thu Mar 02 2023 Timothée Ravier <tim@siosm.fr> - 38-0.27
- Keep upstream default shutdown timeout for some variants

* Fri Feb 10 2023 Stephen Gallagher <sgallagh@redhat.com> - 38-0.26
- Fix typo in release_name

* Fri Feb 10 2023 Kevin Fenzi <kevin@scrye.com> - 38-0.25
- Do another fedora-release build to get past a branching issue

* Wed Feb 08 2023 Tomas Hrcka <thrcka@redhat.com> - 38-0.24
- Fedora 38 branched from rawhide

* Thu Feb 02 2023 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 38-0.21
- Use relative symlinks

* Sun Jan 29 2023 FAS Mershl <mweires@googlemail.com> - 38-0.20
- Workstation & Silverblue: Remove Flathub remote & third party repos

* Mon Jan 23 2023 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 38-0.19
- Replace iscsi.service with iscsi-starter.service

* Fri Jan 20 2023 Alessio <alciregi@posteo.net> - 38-0.18
- Update 80-iot.preset

* Fri Jan 20 2023 Stephen Gallagher <sgallagh@redhat.com> - 38-0.17
- Add Requires(meta) to release packages

* Wed Jan 18 2023 Jonathan Lebon <jonathan@jlebon.com> - 38-0.16
- Revert "Enable podman-restart.service"

* Mon Jan 09 2023 Stephen Gallagher <sgallagh@redhat.com> - 38-0.15
- Enable podman-restart.service

* Mon Jan 09 2023 Stephen Gallagher <sgallagh@redhat.com> - 38-0.14
- Enable waydroid-container.service

* Mon Jan 09 2023 Aleksei Bavshin <alebastr@fedoraproject.org> - 38-0.13
- Add Fedora Sericea (Sway OSTree) subpackages.

* Mon Jan 09 2023 Aleksei Bavshin <alebastr@fedoraproject.org> - 38-0.12
- Introduce %%with_ostree_desktop macro.

* Mon Jan 09 2023 Aleksei Bavshin <alebastr@fedoraproject.org> - 38-0.11
- Add Fedora Sway variant subpackages

* Fri Jan 06 2023 Jilayne Lovejoy <jlovejoy@redhat.com> - 38-0.10
- add US

* Thu Jan 05 2023 Jilayne Lovejoy <jlovejoy@redhat.com> - 38-0.9
- Update Fedora-Legal-README.txt

* Sun Dec 11 2022 Joshua Strobl <me@joshuastrobl.com> - 38-0.8
- Add Budgie

* Mon Nov 28 2022 Neal Gompa <ngompa@fedoraproject.org> - 38-0.7
- 90-default.preset: Enable the livesys and livesys-late services

* Sat Nov 19 2022 Ben Cotton <bcotton@fedoraproject.org> - 38-0.6
- Add anticipated EOL date

* Fri Oct 14 2022 Zamir SUN <sztsian@gmail.com> - 38-0.5
- Add LXQt spin to the fedora-release

* Sun Sep 18 2022 Davide Cavalca <dcavalca@fedoraproject.org> - 38-0.4
- Drop preset for update-vendor-firmware

* Mon Aug 22 2022 Dusty Mabe <dusty@dustymabe.com> - 38-0.3
- Fix sed command for DEFAULT_HOSTNAME changes

* Wed Aug 10 2022 Neal Gompa <ngompa@fedoraproject.org> - 38-0.2
- Ensure branded fallback hostname is set accordingly

* Tue Aug 09 2022 Tomas Hrcka <thrcka@redhat.com> - 38-0.1
- Rawhide is now f38

* Fri Jul 29 2022 Amit Shah <amit@kernel.org> - 37-0.9
- Add debuginfod_url to dist macros

* Wed Jul 27 2022 Amit Shah <amitshah@fedoraproject.org> - 37-0.8
- macros: add new distribution-specific macros for package configurations

* Tue Jun 28 2022 Sergio Arroutbi <sarroutb@redhat.com> - 37-0.7
- Add preset to enable clevis-luks-askpass.path

* Thu Jun 23 2022 Stephen Gallagher <sgallagh@redhat.com> - 37-0.6
- Pull in lorax-templates-rhel for ELN

* Fri Apr 29 2022 Stephen Gallagher <sgallagh@redhat.com> - 37-0.5
- Enable update-vendor-firmware.service

* Fri Apr 29 2022 Ben Cotton <bcotton@fedoraproject.org> - 37-0.4
- Remove the privacy policy URL.

* Wed Mar 09 2022 Timothée Ravier <tim@siosm.fr> - 37-0.3
- Set home and bug report URLs for Silverblue & Kinoite

* Tue Feb 08 2022 Mohan Boddu <mboddu@bhujji.com> - 37-0.2
- Rebuilding for fedora-repos-37

* Tue Feb 08 2022 Tomas Hrcka <thrcka@redhat.com> - 37-0.1
- Rawhide is now f37

* Tue Feb 01 2022 Michael Catanzaro <mcatanzaro@redhat.com> - 36-0.14
- Add NetworkManager to list of protected packages in Workstation

* Sun Jan 23 2022 Neal Gompa <ngompa@fedoraproject.org> - 36-0.13
- Enable rpmdb-migrate.service

* Tue Nov 30 2021 Timothée Ravier <tim@siosm.fr> - 36-0.12
- presets: Use a commmon desktop preset and spin specific ones

* Thu Nov 25 2021 Timothée Ravier <tim@siosm.fr> - 36-0.11
- Statically enable rpm-ostree-countme timer

* Thu Nov 25 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 36-0.10
- Enable plocate timer by default

* Wed Nov 10 2021 Neal Gompa <ngompa@fedoraproject.org> - 36-0.9
- kde: Identify plasma-desktop as a protected package for DNF

* Fri Aug 27 2021 Matthew Miller <mattdm@fedoraproject.org> - 36-0.8
- point SUPPORT_URL to Ask Fedora instead of to an obsolete and
  unmaintained wiki page

* Mon Aug 23 2021 Stephen Gallagher <sgallagh@redhat.com> - 36-0.7
- Fix ostree-counting Obsoletes

* Fri Aug 20 2021 Timothée Ravier <tim@siosm.fr> - 36-0.6
- 90-default.preset: Enable rpm-ostree count me by default

* Tue Aug 17 2021 Owen W. Taylor <otaylor@fishsoup.net> - 36-0.5
- workstation/silverblue: Add third-party repositories

* Mon Aug 16 2021 Dan Čermák <dan.cermak@cgc-instruments.com> - 36-0.4

- Add Fedora i3 variant subpackage

* Tue Aug 10 2021 Tomas Hrcka <thrcka@redhat.com> - 36-0.2
- Setup for rawhide being F36

* Wed Aug 04 2021 Stephen Gallagher <sgallagh@redhat.com> - 35-0.14
- Switch libvirt presets to use the new modular daemons
  https://fedoraproject.org/wiki/Changes/LibvirtModularDaemons

* Mon Jul 26 2021 Neal Gompa <ngompa@fedoraproject.org> - 35-0.13
- Shuffle some power/resource management presets so all variants can use them

* Fri Jul 23 2021 Neal Gompa <ngompa@fedoraproject.org> - 35-0.12
- user session: drop duplicate pipewire-pulse preset

* Wed Jul 14 2021 Kevin Fenzi <kevin@scrye.com> - 35-0.11
- user session: wireplumber.service and pipewire-pulse.socket

* Tue Jul 13 2021 Stephen Gallagher <sgallagh@redhat.com> - 35-0.10
- user session: enable pipewire-media-session.service

* Fri Apr 30 2021 Stephen Gallagher <sgallagh@redhat.com> - 35-0.9
- Change PRETTY_NAME to "Fedora Linux"

* Fri Apr 30 2021 Ben Cotton <bcotton@fedoraproject.org> - 35-0.8
- Automatically set the version in Fedora-Legal-README.txt

* Tue Apr 13 2021 Timothée Ravier <travier@redhat.com> - 35-0.7
- Add ostree-counting & ostree-desktop subpackages

* Thu Apr 01 2021 Stephen Gallagher <sgallagh@redhat.com> - 35-0.6
- Enable certbot-renew.timer (bz1942011)

* Wed Mar 17 2021 Timothée Ravier <travier@redhat.com> - 35-0.5
- Add Fedora Kinoite variant sub package

* Wed Mar 17 2021 Timothée Ravier <travier@redhat.com> - 35-0.4
- Enable Count Me timer for Silverblue and IoT

* Sat Feb 20 2021 Stephen Gallagher <sgallagh@redhat.com> - 35-0.3
- Update rhel_dist_version to track RHEL 10

* Tue Feb 16 2021 Michel Alexandre Salim <salimma@fedoraproject.org> - 35-0.2
- Remove earlyoom preset from workstation and kde identities
  (replaced by systemd-oomd)

* Tue Feb 09 2021 Tomas Hrcka <thrcka@redhat.com> - 35-0.1
- Setup for rawhide being F35

* Tue Jan 19 2021 Allison Karlitskaya <allison.karlitskaya@redhat.com> - 34-0.11
- Enable rpm-ostree repo-refresh for all active local users
- https://github.com/fedora-silverblue/issue-tracker/issues/55

* Tue Dec 15 2020 Mohan Boddu <mboddu@bhujji.com> - 34-0.10
- Enable pipewire-pulse socket-activated user service (ngompa)
- Fixing changelog

* Wed Oct 28 2020 Stephen Gallagher <sgallagh@redhat.com> - 34-0.9
- Spec file and ELN improvements
- Conditionalize the creation of the identity subpackages
- Allow ELN to skip building all of the other Fedora identities
- Have ELN be the provider of the `redhat-release` virtual provides

* Fri Oct 23 2020 Stephen Gallagher <sgallagh@redhat.com> - 34-0.8
- Enable power-profiles-daemon by default
- https://pagure.io/fedora-workstation/issue/191

* Wed Oct 14 2020 Mohan Boddu <mboddu@bhujji.com> - 34-0.7
- Enable low-memory-monitor for GMemoryMonitor API (hadess)

* Fri Oct 09 2020 Mohan Boddu <mboddu@bhujji.com> - 34-0.6
- Add ELN support to fedora-release (sgallagh)

* Thu Sep 17 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 34-0.5
- IoT: Enable parsec and dbus-parsec services

* Tue Aug 25 2020 Kalev Lember <klember@redhat.com> - 34-0.4
- Add gnome-shell to dnf protected packages list for Workstation

* Mon Aug 17 2020 Troy Dawson <tdawson@redhat.com> - 34-0.3
- Change release if building for eln

* Tue Aug 11 2020 Troy Dawson <tdawson@redhat.com> - 34-0.2
- Set %rhel and %eln when appropriate

* Mon Aug 10 2020 Tomas Hrcka <thrcka@redhat.com> - 34-0.1
- Setup for rawhide being F34

* Mon Aug 10 2020 Troy Dawson <tdawson@redhat.com> - 33-0.11
- No %fedora set for eln

* Thu Aug 06 2020 Ben Cotton <bcotton@fedoraproject.org> - 33-0.10
- KDE: Add EarlyOOM by default

* Fri Jun 05 2020 Mohan Boddu <mboddu@bhujji.com> - 33-0.9
- iot: Remove preset for greenboot.service (lorbus)

* Mon May 04 2020 Stephen Gallagher <sgallagh@redhat.com> - 33-0.8
- Fix incorrect prerelease labeling for Editions and Spins
- Resolves: rhbz#1831102

* Tue Apr 21 2020 Stephen Gallagher <sgallagh@redhat.com> - 33-0.7
- Add new "identity" subpackages to allow Edition and Spin environment groups
  to be installed together.

* Mon Apr 20 2020 Stephen Gallagher <sgallagh@redhat.com> - 33-0.6
- Add "Prerelease" notation to PRETTY_NAME and VERSION in os-release

* Sun Apr 12 2020 Kevin Fenzi <kevin@scrye.com> - 33-0.5
- Update color to Fedora blue. Fixes bug #1823099

* Wed Apr 01 2020 Christian Glombek <cglombek@redhat.com> 33-0.4
- Add IoT user preset to disable grub-boot-success.timer
- Update links in 80-coreos.preset

* Fri Mar 20 2020 Patrick Uiterwijk <puiterwijk@redhat.com> 33-0.3
- Enable IoT provisioning service

* Wed Mar 18 2020 Peter Robinson <pbrobinson@fedoraproject.org> 33-0.2
- Add IoT provisioning URL config
- Enable fstrim.timer (crobinso)
- Enable kata-osbuilder-generate.service (crobinso)

* Tue Feb 11 2020 Mohan Boddu <mboddu@bhujji.com> - 33-0.1
- Setup for rawhide being F33

* Fri Feb  7 2020 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 32-0.5
- Add 'disable *' default preset for user units (#1468501)

* Wed Oct 30 2019 Peter Robinson <pbrobinson@fedoraproject.org> 32-0.4
- Drop clevis IoT defaults change

* Mon Oct 21 2019 Michael Nguyen <mnguyen@redhat.com> - 32-0.3
- Update os-release information for Fedora CoreOS

* Thu Aug 15 2019 Miro Hrončok <mhroncok@redhat.com> - 32-0.2
- RPM macros: Redefining %%fedora now changes %%dist

* Tue Aug 13 2019 Mohan Boddu <mboddu@bhujji.com> - 32-0.1
- Setup for rawhide being F32
- Disable zram-swap service (sgallagh)

* Sat Aug 10 2019 Tom Callaway <spot@fedoraproject.org> - 31-0.9
- update legal text (reflect current release, refer to Fedora OS instead of Fedora)

* Sat Jul 13 2019 Colin Walters <walters@verbum.org> - 31-0.8
- Sync Silverblue with Workstation
  In particular, it should have the same "ssh disabled by default" etc.
  https://discussion.fedoraproject.org/t/strange-etc-os-release-contents-on-silverblue/2024/2
- Enable zram-swap on workstation installations
- Enable the session agent for snaps

* Thu Jun 06 2019 Stephen Gallagher <sgallagh@redhat.com> - 31-0.7
- Work around upgrade bug
- Resolves: rhbz#1710543

* Tue May 14 2019 Robert Fairley <rfairley@redhat.com> - 31-0.6
- Remove presets from 80-coreos.preset and add note referring to FCOS overlay RPM

* Wed Apr 10 2019 Stephen Gallagher <sgallagh@redhat.com> - 31-0.5
- Add Provides for the base module for Fedora (BZ #1688462)

* Mon Apr 8 2019 Michael Nguyen <mnguyen@redhat.com> - 31-0.4
- Add presets for CoreOS

* Thu Apr 04 2019 Kalev Lember <klember@redhat.com> - 31-0.3
- Enable the Fedora flatpak repos service (#1696225)

* Wed Mar 20 2019 Jason L Tibbitts III <tibbs@math.uh.edu> - 31-0.2
- Allow bootstrap suffix to be overridden.

* Tue Feb 19 2019 Tomas Hrcka <thrcka@redhat.com> - 31-0.1
- Setup for rawhide being f30

* Fri Feb 15 2019 Sinny Kumari <skumari@redhat.com> - 30-0.23
- Don't build AtomicHost from F30 and onward releases in favor of coreos

* Fri Feb 08 2019 David Rheinsberg <david.rheinsberg@gmail.com> - 30-0.22
- Enable dbus-broker over dbus-daemon, to make new installs use the broker as
  new system- and user-bus implementation.

* Sun Feb 03 2019 Neal Gompa <ngompa13@gmail.com> - 30-0.21
- Add snappy variant

* Fri Jan 18 2019 Robert Fairley <rfairley@redhat.com> - 30-0.20
- Own /etc/issue.d directory.

* Fri Dec 28 2018 Kevin Fenzi <kevin@scrye.com> - 30-0.19
- Own /etc/swid directory.

* Wed Dec 12 2018 Stephen Gallagher <sgallagh@redhat.com> - 30-0.18
- Include empty VERSION_CODENAME= field in os-release

* Tue Dec 11 2018 Mohan Boddu <mboddu@bhujji.com> 30-0.17
- Use the icon logo for `LOGO`

* Mon Dec 03 2018 Mohan Boddu <mboddu@bhujji.com> 30-0.16
- Add 'LOGO' to os-release(5) for Fedora
- Enable the Docker daemon socket

* Tue Nov 27 2018 Peter Robinson <pbrobinson@fedoraproject.org> 30-0.15
- Add IoT config to fix policy around TPM2 requirements

* Thu Nov 15 2018 Jan Pazdziora <jpazdziora@redhat.com> - 30-0.14
- Fix the supplemental edition SWID tag, add the supplemental attribute.

* Sun Nov 11 2018 Stephen Gallagher <sgallagh@redhat.com> - 30-0.13
- Drop unneeded Requires(post) and Requires(postun) dependencies causing
  loops. The glib-compile-schemas dependency is now handled by file triggers
  and the systemd requirement was just completely erroneous.
- Also drop strict dependencies on edition packages. They are causing
  un-breakable dependency loops.

* Tue Oct 23 2018 Stephen Gallagher <sgallagh@redhat.com> - 30-0.12
- Convert to more maintainable implementation of variant-handling

* Thu Oct 11 2018 Jan Pazdziora <jpazdziora@redhat.com> 30-0.10
- Add edition supplemental .swidtag files, and amend convert-to-edition.lua
  to keep symlink to the correct one in sync with os-release.
- Produce distro-level SWID tag in /usr/lib/swidtag/fedoraproject.org.
- Enable ostree-finalize-staged.path

* Mon Sep 24 2018 Mohan Boddu <mboddu@bhujji.com> 30-0.9
- Enable the stratis daemon for managing stratis storage

* Fri Sep 14 2018 Mohan Boddu <mboddu@bhujji.com> 30-0.8
- Set cpi.service as enabled in the systemd presets
- Set device_cio_free service as enabled

* Mon Aug 27 2018 Stephen Gallagher <sgallagh@redhat.com> - 30-0.7
- Remove specialized handling for /etc/issue.
- Drop convert-to-edition script

* Fri Aug 24 2018 Matthew Miller <mattdm@fedoraproject.org> - 30-0.6
- add container
- add coreos
- add desktop spins

* Thu Aug 23 2018 Peter Robinson <pbrobinson@fedoraproject.org> 30-0.5
- Add Fedora IoT edition components

* Mon Aug 20 2018 Jun Aruga <jaruga@redhat.com> - 30-0.4
- Update dist macro to consider bootstrapping.

* Sat Aug 18 2018 Jason L Tibbitts III <tibbs@math.uh.edu> - 30-0.3
- Escape use of the distprefix macro, so it makes it into the macro
  file instead of being expanded in the spec.

* Wed Aug 15 2018 David Herrmann <dh.herrmann@gmail.com> - 30-0.2
- Enable dbus user units explicitly

* Tue Aug 14 2018 Mohan Boddu <mboddu@bhujji.com> - 30-0.1
- Setup for rawhide being f30

