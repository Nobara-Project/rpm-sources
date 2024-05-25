# DO NOT SUBMIT THIS TO A COPR REPO
# IT FUCKS WITH GLIBC DUE TO F37 PREBUILT GLIBC LIBRARIES INCLUDED
# THIS WILL CAUSE OTHER BUILDS TO FAIL WHICH RELY ON GLIBC
# ONLY SHIP IT IN EXTERNAL REPOS FOR END USERS

Summary: Contains libraries from Fedora 37 packages needed for Davinci Resolve to run
Name: nobara-resolve-runtime
Version: 1.0
Release: 5%{?dist}
License: Public Domain
URL:            https://github.com/nobara-project/nobara-core-packages
Source0:        %{URL}/releases/download/1.0/nobara-resolve-runtime.tar.gz


BuildRequires: filesystem
Provides: nobara-resolve-runtime

%description
Contains libraries from Fedora 37 packages needed for Davinci Resolve to run.

%prep
tar -xf %{SOURCE0}
rm nobara-resolve-runtime/*.rpm

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}/
install -d $RPM_BUILD_ROOT/opt/nobara-resolve-runtime/
install -m 0755 nobara-resolve-runtime/davinci-resolve $RPM_BUILD_ROOT%{_bindir}/
install -m 0644 nobara-resolve-runtime/* $RPM_BUILD_ROOT/opt/nobara-resolve-runtime/

%files
%{_bindir}/davinci-resolve
/opt/nobara-resolve-runtime/*


%changelog
* Thu Nov 25 2021 Thomas Crider <gloriouseggroll@gmail.com> - 1.0.0
- New version v1.0.0
