Name:           pbcli
Version:        2.2.1
Release:        1%{?dist}

Summary:        pbcli - Command-line interface for pastebin uploads and downloads
License:        MIT
URL:            https://github.com/Mydayyy/pbcli

Source0:        https://github.com/Mydayyy/pbcli/releases/download/v%{version}/pbcli-v%{version}-linux.tar.gz
Source1:        pbcli.conf

BuildRequires:  tar

%description
Command-line interface for pastebin uploads and downloads

%prep
%setup -q -n pbcli-v%{version}-linux

%install
# Create necessary directories
mkdir -p %{buildroot}%{_bindir}

# Extract the tarball and copy the pbcli binary to the buildroot
tar -xzf %{SOURCE0} -C %{buildroot}%{_bindir} --strip-components=1

# Install Nobara-specific configuration file
install -Dm644 %{SOURCE1} %{buildroot}%{_sysconfdir}/pbcli.conf

%post
# Create or overwrite the pbcli.sh script in /etc/profile.d/
cat > /etc/profile.d/pbcli.sh << 'EOF'
#!/bin/bash
# Check if PBCLI_CONFIG_PATH is already set
if [ -z "$PBCLI_CONFIG_PATH" ]; then
    # If not set, define the default path for pbcli configuration
    export PBCLI_CONFIG_PATH="/etc/pbcli.conf"
fi
EOF
chmod +x /etc/profile.d/pbcli.sh

%postun
# Remove the pbcli.sh script if this is the last version of the package being removed
if [ $1 -eq 0 ]; then
    rm -f /etc/profile.d/pbcli.sh
fi
if [ -z "$PBCLI_CONFIG_PATH" ]; then
    unset PBCLI_CONFIG_PATH
fi


%files
%{_bindir}/pbcli
%config(noreplace) %{_sysconfdir}/pbcli.conf

%changelog
* Fri Mar 01 2024 Matthew Schwartz <njtransit215@gmail.com> - 2.2.1-1
- Initial package release
