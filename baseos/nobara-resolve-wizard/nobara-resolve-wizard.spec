Summary: A set of scripts to install and update Davinci Resolve with better compatibility.
Name: nobara-resolve-wizard
Version: 1.3
Release: 9%{?dist}
License: Public Domain
Group: System Environment/Base
Source0: nobara-resolve-wizard.tar.gz

BuildArch: noarch
BuildRequires: filesystem
Provides: nobara-resolve-runtime
Obsoletes: nobara-resolve-runtime

%description
A set of scripts to install and update Davinci Resolve with better compatibility.

%prep
%autosetup -p1 -n nobara-resolve-wizard

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}/
install -d $RPM_BUILD_ROOT%{_libexecdir}
install -d $RPM_BUILD_ROOT%{_datadir}/polkit-1/actions/
install -m 0755 .%{_bindir}/nobara-resolve-wizard $RPM_BUILD_ROOT%{_bindir}/nobara-resolve-wizard
install -m 0755 .%{_libexecdir}/nobara-resolve-pkexec $RPM_BUILD_ROOT%{_libexecdir}/nobara-resolve-pkexec
install -m 0755 .%{_datadir}/polkit-1/actions/org.nobaraproject.resolvewizard.policy $RPM_BUILD_ROOT%{_datadir}/polkit-1/actions/org.nobaraproject.resolvewizard.policy


%files
%{_bindir}/nobara-resolve-wizard
%{_libexecdir}/nobara-resolve-pkexec
%{_datadir}/polkit-1/actions/org.nobaraproject.resolvewizard.policy



%changelog
* Mon May 5 2025 LionHeartP <LionHeartP@proton.me> - 1.2-2
- Add udev rule for MangoHud power reading

* Thu Nov 25 2021 Thomas Crider <gloriouseggroll@gmail.com> - 1.0.0
- New version v1.0.0
