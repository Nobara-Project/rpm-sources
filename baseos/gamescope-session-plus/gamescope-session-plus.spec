Name:           gamescope-session-plus
Version:        0.2.git.201.5538cd66
Release:        53%{?dist}
Summary:        Gamescope session plus based on Valve's gamescope

License:        MIT
URL:            https://github.com/nobara-project/steamdeck-edition-packages
Source0:        %{URL}/releases/download/1.0/gamescope-session-plus.tar.gz
BuildArch:      noarch

Requires:       gamescope
Requires:       edid-decode
Requires:       python3
Requires:       pulseaudio-utils
Requires:       steam
Requires:       gamescope-session-steam

BuildRequires:  systemd-rpm-macros

Obsoletes:      gamescope-session
Provides:       powerbuttond
Provides:       steam-powerbuttond
Obsoletes:      powerbuttond
Obsoletes:      steam-powerbuttond

%description
Gamescope session plus based on Valve's gamescope

# Disable debug packages
%define debug_package %{nil}

%prep
tar -xf %{SOURCE0}

%build

%install
mkdir -p %{buildroot}%{_bindir}/
mkdir -p %{buildroot}%{_datadir}/
mkdir -p %{buildroot}%{_sysconfdir}/
mkdir -p %{buildroot}%{_userunitdir}/
mkdir -p %{buildroot}%{_libexecdir}/
cp -rv gamescope-session-plus/usr/bin/* %{buildroot}%{_bindir}
cp -rv gamescope-session-plus/usr/share/* %{buildroot}%{_datadir}
cp -rv gamescope-session-plus/etc/* %{buildroot}%{_sysconfdir}
cp -rv gamescope-session-plus/usr/lib/systemd/user/* %{buildroot}%{_userunitdir}
cp -rv gamescope-session-plus/usr/libexec/* %{buildroot}%{_libexecdir}/
mv gamescope-session-plus/LICENSE .
mv gamescope-session-plus/README.md .

# Do post-installation
%post

# KDE/SDDM
if [[ ! -z $(systemctl status sddm | grep running) ]]; then
  if [[ -f /etc/sddm.conf ]]; then
    sed -i "s|Relogin=.*|Relogin=true|g" /etc/sddm.conf
    if [[ -z $(cat /etc/sddm.conf | grep Relogin) ]]; then
      sed -i '/\[Autologin\]/a\Relogin=true' /etc/sddm.conf
    fi
  fi
  if [[ -f /etc/sddm.conf.d/kde_settings.conf ]]; then
    sed -i "s|Relogin=.*|Relogin=true|g" /etc/sddm.conf.d/kde_settings.conf
    if [[ -z $(cat /etc/sddm.conf.d/kde_settings.conf | grep Relogin) ]]; then
      sed -i '/\[Autologin\]/a\Relogin=true' /etc/sddm.conf.d/kde_settings.conf
    fi
  fi
fi

# Do before uninstallation
%preun

# Do after uninstallation
%postun

# This lists all the files that are included in the rpm package and that
# are going to be installed into target system where the rpm is installed.
%files
%license LICENSE
%doc README.md
%{_bindir}/export-gpu
%{_bindir}/gamescope-session-plus
%{_bindir}/deckscale
%{_datadir}/gamescope-session-plus/device-quirks
%{_datadir}/gamescope-session-plus/gamescope-session-plus
%{_datadir}/polkit-1/actions/org.gamescope.start.policy
%{_sysconfdir}/xdg/autostart/deckscale.desktop
%{_sysconfdir}/gamescope-session-plus/*
%{_userunitdir}/gamescope-session-plus@.service
%{_libexecdir}/*

# Finally, changes from the latest release of your application are generated from
# your project's Git history. It will be empty until you make first annotated Git tag.
%changelog
{{{ git_dir_changelog }}}
