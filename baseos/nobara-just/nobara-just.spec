Name:           nobara-just
Packager:       nobara
Vendor:         nobara
Version:        0.1
Release:        1%{?dist}
Summary:        nobara just integration
License:        MIT
URL:            https://github.com/ublue-os/config

BuildArch:      noarch
Requires:       just

Source0:        nobara-just.sh
Source1:        00-default.just
Source7:        60-custom.just
Source8:        85-nobara-image.just
Source9:        ujust
Source10:       ugum
Source11:       header.just
Source12:       ujust.sh
Source13:       libcolors.sh
Source14:       libformatting.sh
Source15:       libfunctions.sh

%global sub_name %{lua:t=string.gsub(rpm.expand("%{NAME}"), "^nobara%-", ""); print(t)}

%description
Adds nobara just integration for easier setup

%prep
%setup -q -c -T

%build

mkdir -p -m0755  %{buildroot}%{_datadir}/%{VENDOR}/%{sub_name}
install -Dm755 %{SOURCE0}  %{buildroot}%{_sysconfdir}/profile.d/nobara-just.sh
cp %{SOURCE1} %{SOURCE7} %{SOURCE8} %{buildroot}%{_datadir}/%{VENDOR}/%{sub_name}

# Create justfile which contains all .just files included in this package
# Apply header first due to default not working in included justfiles
cp %{SOURCE11} "%{buildroot}%{_datadir}/%{VENDOR}/justfile"
for justfile in %{buildroot}%{_datadir}/%{VENDOR}/%{sub_name}/*.just; do
	echo "import \"%{_datadir}/%{VENDOR}/%{sub_name}/$(basename ${justfile})\"" >> "%{buildroot}%{_datadir}/%{VENDOR}/justfile"
done

# Add global "ujust" script to run just with --unstable
mkdir -p -m0755  %{buildroot}%{_bindir}
install -Dm755 %{SOURCE9} %{buildroot}%{_bindir}/ujust
install -Dm755 %{SOURCE10} %{buildroot}%{_bindir}/ugum

# Add bash library for use in just
mkdir -p -m0755 %{buildroot}/%{_exec_prefix}/lib/ujust/
install -Dm644 %{SOURCE12} %{buildroot}/%{_exec_prefix}/lib/ujust
install -Dm644 %{SOURCE13} %{buildroot}/%{_exec_prefix}/lib/ujust
install -Dm644 %{SOURCE14} %{buildroot}/%{_exec_prefix}/lib/ujust
install -Dm644 %{SOURCE15} %{buildroot}/%{_exec_prefix}/lib/ujust


%files
%dir %attr(0755,root,root) %{_datadir}/%{VENDOR}/%{sub_name}
%attr(0755,root,root) %{_sysconfdir}/profile.d/nobara-just.sh
%attr(0644,root,root) %{_datadir}/%{VENDOR}/%{sub_name}/*.just
%attr(0644,root,root) %{_datadir}/%{VENDOR}/justfile
%attr(0755,root,root) %{_bindir}/ujust
%attr(0755,root,root) %{_bindir}/ugum
%attr(0644,root,root) %{_exec_prefix}/lib/ujust/ujust.sh
%attr(0644,root,root) %{_exec_prefix}/lib/ujust/lib*.sh

%post
# Generate ujust bash completion
just --completions bash | sed -E 's/([\(_" ])just/\1ujust/g' > %{_datadir}/bash-completion/completions/ujust
chmod 644 %{_datadir}/bash-completion/completions/ujust

%changelog
* Mon Jan 29 2024 Matthew Schwartz <njtransit215@gmail.com> - 0.1
- Initial package import from Bazzite (thanks!)
