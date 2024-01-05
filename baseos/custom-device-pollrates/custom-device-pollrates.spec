%global _default_patch_fuzz 2
%global baserelease 7


Name:           custom-device-pollrates
Version:        1.0.0
Release:        %{baserelease}%{?dist}
Summary:        Allows setting custom polling rates for USB devices, requires kernel patch.

License:        GPLv2+
URL:            https://github.com/GloriousEggroll/Linux-Pollrate-Patch


# Sources for custom-device-pollrates
Source0: custom-device-pollrates.sh
Source2: custom-device-pollrates.service
Source3: custom-device-pollrates.conf

BuildRequires: systemd-rpm-macros

%description
This is a service that is built around the following kernel patch from:
https://github.com/KarsMulder/Linux-Pollrate-Patch
It allows to create a list of USB devices in 
/etc/custom-device-pollrates/custom-device-pollrates.conf
with different poll rate values. Once entries are added simply restart
the service with `systemctl restart custom-device-pollrates.service`
You can use a tool such as evhz (https://git.sr.ht/~iank/evhz) to check polling rates.

%install
# custom-device-pollrates
mkdir -p %{buildroot}%{_bindir}/
mkdir -p %{buildroot}%{_presetdir}/
mkdir -p %{buildroot}%{_unitdir}/
mkdir -p %{buildroot}%{_sysconfdir}/custom-device-pollrates
install -Dm755 %{SOURCE0} %{buildroot}%{_bindir}/custom-device-pollrates.sh
install -Dm644 %{SOURCE2} %{buildroot}%{_prefix}/lib/systemd/system/custom-device-pollrates.service
install -Dm644 %{SOURCE3} %{buildroot}%{_sysconfdir}/custom-device-pollrates/custom-device-pollrates.conf

%files
%{_bindir}/custom-device-pollrates.sh
%{_prefix}/lib/systemd/system/custom-device-pollrates.service
%{_sysconfdir}/custom-device-pollrates/custom-device-pollrates.conf

%changelog
