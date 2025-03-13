Name:           gamescope-session-ogui
Version:        0.2.git.201.5538cd66
Release:        62%{?dist}
Summary:        Steam Deck Mode session

License:        MIT
URL:            https://github.com/nobara-project/steamdeck-edition-packages
Source0:        %{URL}/releases/download/1.0/gamescope-session-ogui.tar.gz

BuildArch:      noarch

Requires:       gamescope-session-plus
Requires:       gamescope
Requires:       edid-decode
Requires:       python3
Requires:       pulseaudio-utils
Requires:       opengamepadui

BuildRequires:  systemd-rpm-macros
BuildRequires:  wget

%description
Steam Deck Mode session

# Disable debug packages
%define debug_package %{nil}

%prep
tar -xf %{SOURCE0}

%build

%install
mkdir -p %{buildroot}%{_bindir}/
mkdir -p %{buildroot}%{_datadir}/
mkdir -p %{buildroot}%{_datadir}/gamescope-session-plus/
mkdir -p %{buildroot}%{_libexecdir}/
mkdir -p %{buildroot}%{_sysconfdir}/skel/Desktop/
cp -rv gamescope-session-ogui/usr/bin/* %{buildroot}%{_bindir}
cp -rv gamescope-session-ogui/usr/share/* %{buildroot}%{_datadir}
cp -rf gamescope-session-ogui/usr/libexec/* %{buildroot}%{_libexecdir}/
cp -rf gamescope-session-ogui/etc/* %{buildroot}%{_sysconfdir}/
mv gamescope-session-ogui/LICENSE .

# Do before uninstallation
%preun

# Do after uninstallation
%postun

# This lists all the files that are included in the rpm package and that
# are going to be installed into target system where the rpm is installed.
%files
%license LICENSE
%{_bindir}/ogui-session-select
%{_bindir}/ogui-desktop-return
%{_datadir}/gamescope-session-plus/sessions.d/ogui
%{_datadir}/polkit-1/actions/org.nobaraproject.ogui.session.select.policy
%{_datadir}/wayland-sessions/gamescope-session-ogui.desktop
%{_sysconfdir}/skel/Desktop/ogui-return.desktop
%{_libexecdir}/ogui-os-session-select

# Finally, changes from the latest release of your application are generated from
# your project's Git history. It will be empty until you make first annotated Git tag.
%changelog
{{{ git_dir_changelog }}}
