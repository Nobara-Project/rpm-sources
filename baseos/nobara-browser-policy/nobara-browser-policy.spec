Name: nobara-browser-policy
Version: 2.0.0
Release: 4%{?dist}
Summary: Web browser that lets you take control of your personal data
License: MPLv2.0
Group: Applications/Internet
URL: https://brave.com
BuildArch: x86_64
Requires: brave-browser
Provides: nobara-browser-policy
Obsoletes: brave

%define debug_package %{nil}

%description
Nobara chromium-based browser policy.

%prep
# No preparation needed for this package

%build
# No build phase needed

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/etc/brave/policies/managed

cat << EOF > %{buildroot}/etc/brave/policies/managed/brave_nobara-policies.json
{
    "BraveRewardsDisabled": true,
    "BraveWalletDisabled": true,
    "BraveVPNDisabled": 1,
    "BraveAIChatEnabled": false,
    "TorDisabled": true,
    "DnsOverHttpsMode": "automatic"
}
EOF

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
/etc/brave/policies/managed/brave_nobara-policies.json

%changelog
