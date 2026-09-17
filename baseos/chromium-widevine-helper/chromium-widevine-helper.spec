%global helper_version 1.0.9
%global extension_id mkgjnlllemldgamnbcgemcecicgmeaid
%global debug_package %{nil}

Name:    chromium-widevine-helper
Summary: Native helper for installing Google Widevine in Chromium-based linux browsers
Version: %{helper_version}
Release: 2%{?dist}
License: GPL-3.0-only
URL:     https://github.com/GloriousEggroll/chromium-widevine-helper
BuildArch: noarch
BuildRequires: python3

Source0: chromium-widevine-helper.tar.gz

Requires: python3
Requires: procps-ng
Recommends: ca-certificates

%description
Native messaging helper and optional packaged extension assets for installing
and managing Google's Widevine CDM in Chromium-based browser profiles.

The helper does not bundle Widevine. When enabled by the extension or CLI, it
downloads the official Google Widevine component and installs it into the active
browser profile.

%prep
%autosetup -n chromium-widevine-helper

%build
# No build step is required.

%check
python3 -m unittest discover -s tests -v

%install
%define widevine_base %{_datadir}/chromium-widevine
%define widevinedir %{buildroot}%{widevine_base}
%define widevine_libexec %{_libexecdir}/chromium-widevine
%define widevinelibexecdir %{buildroot}%{widevine_libexec}

mkdir -p %{widevinedir}/extension \
         %{widevinelibexecdir} \
         %{buildroot}%{_bindir} \
         %{buildroot}%{_datadir}/chromium/extensions \
         %{buildroot}%{_sysconfdir}/helium/native-messaging-hosts \
         %{buildroot}%{_sysconfdir}/net.imput.helium/native-messaging-hosts \
         %{buildroot}%{_sysconfdir}/chromium/native-messaging-hosts \
         %{buildroot}%{_sysconfdir}/chromium-browser/native-messaging-hosts \
         %{buildroot}%{_sysconfdir}/opt/chrome/native-messaging-hosts \
         %{buildroot}%{_sysconfdir}/opt/edge/native-messaging-hosts \
         %{buildroot}%{_sysconfdir}/brave/native-messaging-hosts \
         %{buildroot}%{_sysconfdir}/vivaldi/native-messaging-hosts \
         %{buildroot}%{_sysconfdir}/opera/native-messaging-hosts \
         %{buildroot}%{_sysconfdir}/thorium/native-messaging-hosts \
         %{buildroot}%{_sysconfdir}/iridium/native-messaging-hosts

install -m 755 helper/chromium-widevine \
    %{widevinelibexecdir}/chromium-widevine

for hostdir in \
    %{buildroot}%{_sysconfdir}/helium/native-messaging-hosts \
    %{buildroot}%{_sysconfdir}/net.imput.helium/native-messaging-hosts \
    %{buildroot}%{_sysconfdir}/chromium/native-messaging-hosts \
    %{buildroot}%{_sysconfdir}/chromium-browser/native-messaging-hosts \
    %{buildroot}%{_sysconfdir}/opt/chrome/native-messaging-hosts \
    %{buildroot}%{_sysconfdir}/opt/edge/native-messaging-hosts \
    %{buildroot}%{_sysconfdir}/brave/native-messaging-hosts \
    %{buildroot}%{_sysconfdir}/vivaldi/native-messaging-hosts \
    %{buildroot}%{_sysconfdir}/opera/native-messaging-hosts \
    %{buildroot}%{_sysconfdir}/thorium/native-messaging-hosts \
    %{buildroot}%{_sysconfdir}/iridium/native-messaging-hosts
do
    install -m 644 helper/chromium-widevine-native-host.json \
        "$hostdir/org.chromium.widevine.json"
done

cp -a extension/. %{widevinedir}/extension/
find %{widevinedir}/extension -type d -exec chmod 755 {} +
find %{widevinedir}/extension -type f -exec chmod 644 {} +

install -m 644 Packaging/rpm/chromium-widevine.crx \
    %{widevinedir}/chromium-widevine.crx
install -m 644 Packaging/rpm/%{extension_id}.json \
    %{buildroot}%{_datadir}/chromium/extensions/%{extension_id}.json

ln -sf %{widevine_libexec}/chromium-widevine \
    %{buildroot}%{_bindir}/chromium-widevine

%files
%defattr(-,root,root,-)
%doc README.md
%{widevine_base}/
%{widevine_libexec}/
%{_bindir}/chromium-widevine
%dir %{_datadir}/chromium
%dir %{_datadir}/chromium/extensions
%{_datadir}/chromium/extensions/%{extension_id}.json
%config(noreplace) %{_sysconfdir}/helium/native-messaging-hosts/org.chromium.widevine.json
%config(noreplace) %{_sysconfdir}/net.imput.helium/native-messaging-hosts/org.chromium.widevine.json
%config(noreplace) %{_sysconfdir}/chromium/native-messaging-hosts/org.chromium.widevine.json
%config(noreplace) %{_sysconfdir}/chromium-browser/native-messaging-hosts/org.chromium.widevine.json
%config(noreplace) %{_sysconfdir}/opt/chrome/native-messaging-hosts/org.chromium.widevine.json
%config(noreplace) %{_sysconfdir}/opt/edge/native-messaging-hosts/org.chromium.widevine.json
%config(noreplace) %{_sysconfdir}/brave/native-messaging-hosts/org.chromium.widevine.json
%config(noreplace) %{_sysconfdir}/vivaldi/native-messaging-hosts/org.chromium.widevine.json
%config(noreplace) %{_sysconfdir}/opera/native-messaging-hosts/org.chromium.widevine.json
%config(noreplace) %{_sysconfdir}/thorium/native-messaging-hosts/org.chromium.widevine.json
%config(noreplace) %{_sysconfdir}/iridium/native-messaging-hosts/org.chromium.widevine.json

%changelog
%if "%{_vendor}" != "debbuild"
%autochangelog
%endif
