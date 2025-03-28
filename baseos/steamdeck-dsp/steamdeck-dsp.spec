Name:           steamdeck-dsp
Version:        0.49.2
Release:        1%{?dist}
Summary:        Steamdeck Audio Processing
License:        GPLv2
URL:            https://github.com/ublue-os/bazzite
Source0:        https://gitlab.com/evlaV/valve-hardware-audio-processing/-/archive/main/valve-hardware-audio-processing-main.tar.gz
Patch0:         fedora.patch
Patch1:         nobara.patch

Requires:       pipewire-module-filter-chain-lv2
Requires:       ladspa-noise-suppression-for-voice
Requires:       boost

BuildRequires:  make
BuildRequires:  faust
BuildRequires:  faust-tools
BuildRequires:  boost-devel
BuildRequires:  lv2-devel
BuildRequires:  g++
BuildRequires:  ladspa-devel
BuildRequires:  xz
BuildRequires:  systemd-rpm-macros

%description
Steamdeck Audio Processing

# Disable debug packages
%define debug_package %{nil}

%prep
%autosetup -n valve-hardware-audio-processing-main -p1

%build
%make_build FAUSTINC="/usr/include/faust"  FAUSTLIB="/usr/share/faust"

%install
%make_install DEST_DIR="%{buildroot}" LIB_DIR="%{buildroot}%{_libdir}"
mkdir -p %{buildroot}%{_datadir}/licenses/%{name}/
cp LICENSE %{buildroot}%{_datadir}/licenses/%{name}/LICENSE
xz --check=crc32 %{buildroot}%{_prefix}/lib/firmware/amd/sof/*
xz --check=crc32 %{buildroot}%{_prefix}/lib/firmware/amd/sof-tplg/*
rm -f %{buildroot}%{_sysconfdir}/wireplumber
mkdir -p %{buildroot}%{_libexecdir}/hwsupport
mv %{buildroot}%{_datadir}/wireplumber/hardware-profiles/wireplumber-hwconfig %{buildroot}%{_libexecdir}/hwsupport/wireplumber-hwconfig
mv %{buildroot}%{_datadir}/pipewire/hardware-profiles/pipewire-hwconfig %{buildroot}%{_libexecdir}/hwsupport/pipewire-hwconfig
rm %{buildroot}%{_datadir}/wireplumber/hardware-profiles/default
rm %{buildroot}%{_datadir}/pipewire/hardware-profiles/default

# This lists all the files that are included in the rpm package and that
# are going to be installed into target system where the rpm is installed.
%files
%license LICENSE
%{_prefix}/lib/firmware/amd/*
%{_libexecdir}/hwsupport/wireplumber-hwconfig
%{_libexecdir}/hwsupport/pipewire-hwconfig
%{_libdir}/lv2/*
%{_datadir}/alsa/ucm2/conf.d/acp5x/*.conf
%{_datadir}/alsa/ucm2/conf.d/sof-nau8821-max/*.conf
%{_datadir}/wireplumber/hardware-profiles/*
%{_datadir}/pipewire/hardware-profiles/*
%{_unitdir}/wireplumber-sysconf.service
%{_unitdir}/multi-user.target.wants/wireplumber-sysconf.service
%{_unitdir}/pipewire-sysconf.service
%{_unitdir}/multi-user.target.wants/pipewire-sysconf.service

%post
%systemd_post wireplumber-sysconf.service
%systemd_post pipewire-sysconf.service

%preun
%systemd_preun wireplumber-sysconf.service
%systemd_preun pipewire-sysconf.service

%postun
%systemd_postun_with_restart wireplumber-sysconf.service
%systemd_postun_with_restart pipewire-sysconf.service

# Finally, changes from the latest release of your application are generated from
# your project's Git history. It will be empty until you make first annotated Git tag.
%changelog
{{{ git_dir_changelog }}}
