## START: Set by rpmautospec
## (rpmautospec version 0.2.5)
%define autorelease(e:s:pb:) %{?-p:0.}%{lua:
    release_number = 1;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{?dist}
## END: Set by rpmautospec

Name:           nobara-bookmarks
Version:        40
Release:        %autorelease
Summary:        Nobara bookmarks
License:        GFDL
URL:            http://fedoraproject.org/
# I had to strip the embedded icons out of the bookmarks file, because they are not 
# distributable under the GFDL. See https://bugzilla.redhat.com/show_bug.cgi?id=433471
Source0:        default-bookmarks.html
BuildArch:      noarch
Provides:       fedora-bookmarks
Obsoletes:      fedora-bookmarks
Provides:       system-bookmarks


%description
This package contains the default bookmarks for Fedora.

%prep
# We are nihilists, Lebowski.  We believe in nassing.

%build
# We are nihilists, Lebowski.  We believe in nassing.

%install
%{__rm} -rf $RPM_BUILD_ROOT
%{__mkdir_p} $RPM_BUILD_ROOT%{_datadir}/bookmarks
install -p -m 644 %{SOURCE0} $RPM_BUILD_ROOT%{_datadir}/bookmarks



%files
%dir %{_datadir}/bookmarks
%{_datadir}/bookmarks/default-bookmarks.html

%changelog
* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> 28-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sun Oct 03 2021 Matthew Miller <mattdm@fedoraproject.org> 28-23
- RPMAUTOSPEC: unresolvable merge
