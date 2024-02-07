Name:           nobara-just
Version:        0.2
Release:        1%{?dist}
Summary:        nobara just integration
License:        MIT
URL:            https://github.com/ublue-os/config

BuildArch:      noarch
Requires:       just

Source0:        nobara-just.sh
Source1:        00-nobara-base.just
Source2:        85-nobara-deck.just
Source3:        njust
Source4:        ngum
Source5:        header.just
Source6:        njust.sh
Source7:        libcolors.sh
Source8:        libformatting.sh
Source9:        libfunctions.sh

%description
Adds nobara just integration for easier setup

%prep
%setup -q -c -T

%build
mkdir -p -m0755  %{buildroot}%{_datadir}
install -Dm755 %{SOURCE0}  %{buildroot}%{_sysconfdir}/profile.d/nobara-just.sh
cp %{SOURCE1} %{SOURCE7} %{SOURCE2} %{buildroot}%{_datadir}

# Create justfile which contains all .just files included in this package
# Apply header first due to default not working in included justfiles
cp %{SOURCE5} "%{buildroot}%{_datadir}/justfile"
for justfile in %{buildroot}%{_datadir}/*.just; do
	echo "import \"%{_datadir}/$(basename ${justfile})\"" >> "%{buildroot}%{_datadir}/justfile"
done

# Add global "njust" script to run just with --unstable
mkdir -p -m0755  %{buildroot}%{_bindir}
install -Dm755 %{SOURCE3} %{buildroot}%{_bindir}/njust
install -Dm755 %{SOURCE4} %{buildroot}%{_bindir}/ngum

# Add bash library for use in just
mkdir -p -m0755 %{buildroot}/%{_exec_prefix}/lib/njust/
install -Dm644 %{SOURCE6} %{buildroot}/%{_exec_prefix}/lib/njust
install -Dm644 %{SOURCE7} %{buildroot}/%{_exec_prefix}/lib/njust
install -Dm644 %{SOURCE8} %{buildroot}/%{_exec_prefix}/lib/njust
install -Dm644 %{SOURCE9} %{buildroot}/%{_exec_prefix}/lib/njust


%files
%dir %attr(0755,root,root) %{_datadir}
%attr(0755,root,root) %{_sysconfdir}/profile.d/nobara-just.sh
%attr(0644,root,root) %{_datadir}/*.just
%attr(0644,root,root) %{_datadir}/justfile
%attr(0755,root,root) %{_bindir}/njust
%attr(0755,root,root) %{_bindir}/ngum
%attr(0644,root,root) %{_exec_prefix}/lib/njust/njust.sh
%attr(0644,root,root) %{_exec_prefix}/lib/njust/lib*.sh

%post
# Generate njust bash completion
just --completions bash | sed -E 's/([\(_" ])just/\1njust/g' > %{_datadir}/bash-completion/completions/njust
chmod 644 %{_datadir}/bash-completion/completions/njust

%changelog
* Tue Fed 6 2024 Matthew Schwartz <njtransit215@gmail.com> - 0.2
- migrate from ujust to njust

* Mon Jan 29 2024 Matthew Schwartz <njtransit215@gmail.com> - 0.1
- Initial package import from Bazzite (thanks!)
