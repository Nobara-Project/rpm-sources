%global updates_testing_enabled 0

Summary:        Nobara package repositories
Name:           nobara-repos
Version:        39
Release:        20%{?eln:.eln%{eln}}
License:        MIT
URL:            https://fedoraproject.org/

Provides:       nobara-repos(%{version}) = %{release}
Provides:       nobara-theming-repos
Provides:       fedora-workstation-repositories
Requires:       system-release(%{version})
#Obsoletes:      fedora-workstation-repositories
Obsoletes:      nobara-repos < %{version}
Obsoletes:      nobara-theming-repos
Requires:       nobara-gpg-keys >= %{version}-%{release}
BuildArch:      noarch
# Required by %%check
BuildRequires:  gnupg sed

Source1:       archmap
Source2:       nobara.repo
Source3:       RPM-GPG-KEY-nobara-appstream-pubkey
Source4:       RPM-GPG-KEY-nobara-baseos-pubkey-38
Source5:       RPM-GPG-KEY-nobara-baseos-pubkey-39
Source6:       RPM-GPG-KEY-nobara-baseos-pubkey-40
Source7:       RPM-GPG-KEY-nobara-multimedia-pubkey
Source8:       nobara-nvidia-new-feature.repo
Source9:       RPM-GPG-KEY-nobara-nvidia-new-feature-pubkey
Source10:      RPM-GPG-KEY-nobara-kde6-pubkey
Source11:      RPM-GPG-KEY-nobara-kde6-overrides-pubkey

%description
Nobara package repository files for yum and dnf along with gpg public keys.

%package -n nobara-gpg-keys
Summary:        Nobara RPM keys
Provides:       nobara-gpg-keys
Provides:       nobara-theming-gpg-keys
Obsoletes:      nobara-theming-gpg-keys


%description -n nobara-gpg-keys
This package provides the RPM signature keys.


%prep

%build

%install
# Install the keys
install -d -m 755 $RPM_BUILD_ROOT/etc/pki/rpm-gpg
install -m 644 %{_sourcedir}/RPM-GPG-KEY* $RPM_BUILD_ROOT/etc/pki/rpm-gpg/

# Link the primary/secondary keys to arch files, according to archmap.
# Ex: if there's a key named RPM-GPG-KEY-fedora-19-primary, and archmap
#     says "fedora-19-primary: i386 x86_64",
#     RPM-GPG-KEY-fedora-19-{i386,x86_64} will be symlinked to that key.
pushd $RPM_BUILD_ROOT/etc/pki/rpm-gpg/

for keyfile in RPM-GPG-KEY*; do
    # resolve symlinks, so that we don't need to keep duplicate entries in archmap
    real_keyfile=$(basename $(readlink -f $keyfile))
    key=${real_keyfile#RPM-GPG-KEY-} # e.g. 'fedora-20-primary'
    if ! grep -q "^${key}:" %{_sourcedir}/archmap; then
        echo "ERROR: no archmap entry for $key"
        exit 1
    fi
    arches=$(sed -ne "s/^${key}://p" %{_sourcedir}/archmap)
    for arch in $arches; do
        # replace last part with $arch (fedora-20-primary -> fedora-20-$arch)
        ln -s $keyfile $keyfile-$arch # NOTE: RPM replaces %% with %
    done
done
popd

# Install repo files
install -d -m 755 $RPM_BUILD_ROOT/etc/yum.repos.d
install -m 644 %{_sourcedir}/nobara.repo $RPM_BUILD_ROOT/etc/yum.repos.d
install -m 644 %{_sourcedir}/nobara-nvidia-new-feature.repo $RPM_BUILD_ROOT/etc/yum.repos.d

%files
%dir /etc/yum.repos.d
%config(noreplace) /etc/yum.repos.d/nobara.repo
%config(noreplace) /etc/yum.repos.d/nobara-nvidia-new-feature.repo

%files -n nobara-gpg-keys
%dir /etc/pki/rpm-gpg
/etc/pki/rpm-gpg/RPM-GPG-KEY-*


%changelog
* Mon Oct 11 2021 Kevin Fenzi <kevin@scrye.com> - 35-1
- Disable updates-testing for GA. (#2012948)

* Tue Aug 17 2021 Adam Williamson <awilliam@redhat.com> - 35-0.6
- Remove spurious space in RPM-GPG-KEY-fedora-37-primary (cgwalters)

* Tue Aug 10 2021 Tomas Hrcka <thrcka@redhat.com> - 35-0.5
- Update Rawhide definition, enable updates-testing for Branched

* Wed Apr 28 2021 Dusty Mabe <dusty@dustymabe.com> - 35-0.4
- Enable the updates archive repo on non-rawhide.

* Fri Feb 19 2021 Petr Menšík <pemensik@redhat.com> - 35-0.3
- Check arch key imports during build (#1872248)

* Wed Feb 17 2021 Mohan Boddu <mboddu@bhujji.com> - 35-0.2
- Support $releasever=rawhide on Rawhide (kparal)
- Make archmap entries mandatory, except symlinks (kparal)
- Fixing F36 key

* Tue Feb 09 2021 Tomas Hrcka <thrcka@redhat.com> - 35-0.1
- Setup for rawhide being F35

* Tue Feb 09 2021 Mohan Boddu <mboddu@bhujji.com> - 34-0.10
- Fixing archmap for F35

* Thu Feb 04 2021 Mohan Boddu <mboddu@bhujji.com> - 34-0.9
- Adding F35 key

* Wed Oct 14 2020 Stephen Gallagher <sgallagh@redhat.com> - 34-0.8
- ELN: Drop dependency on fedora-repos-rawhide-modular

* Tue Oct 13 2020 Stephen Gallagher <sgallagh@redhat.com> - 34-0.7
- Ensure that the ELN GPG key always points at the Rawhide key

* Tue Oct 13 2020 Stephen Gallagher <sgallagh@redhat.com> - 34-0.6
- Drop the fedora-eln-modular.repo

* Thu Oct 08 2020 Stephen Gallagher <sgallagh@redhat.com> - 34-0.5
- Update the ELN repos for the BaseOS and AppStream split

* Mon Oct 05 2020 Dusty Mabe <dusty@dustymabe.com> - 34-0.4
- Add the fedora-repos-archive subpackage.

* Fri Aug 21 2020 Miro Hrončok <mhroncok@redhat.com> - 34-0.3
- Fix a copy-paste error in eln repo name
- Drop fedora-modular from base package since it's in the modular subpackage
- Fixes: rhbz#1869150

* Wed Aug 19 2020 Stephen Gallagher <sgallagh@redhat.com> - 34-0.2
- Enable rebuilding of fedora-repos in ELN
- Drop unused modularity-specific release information

* Mon Aug 10 2020 Tomas Hrcka <thrcka@redhat.com> - 34-0.1
- Setup for rawhide being F34

* Thu Aug 06 2020 Mohan Boddu <mboddu@bhujji.com> - 33-0.9
- Adding F34 key

* Tue Jun 30 2020 Stephen Gallagher <sgallagh@redhat.com> - 33-0.8
- Add optional repositories for ELN

* Mon Jun 29 21:10:15 CEST 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 33-0.7
- Split modular repos to the separate packages

* Mon Jun 01 2020 Dusty Mabe <dusty@dustymabe.com> - 33-0.6
- Add fedora compose ostree repo to fedora-repos-ostree

* Mon Apr 13 2020 Stephen Gallagher <sgallagh@redhat.com> - 33-0.5
- Add the release to the fedora-repos(NN) Provides:

* Thu Apr 09 2020 Kalev Lember <klember@redhat.com> - 33-0.4
- Switch to metalink for fedora-cisco-openh264 and disable repo gpgcheck
  (#1768206)
- Use the same metadata_expire time for fedora-cisco-openh264 and -debuginfo
- Remove enabled_metadata key for fedora-cisco-openh264

* Sat Feb 22 2020 Neal Gompa <ngompa13@gmail.com> - 33-0.3
- Enable fedora-cisco-openh264 repo by default

* Wed Feb 19 2020 Adam Williamson <awilliam@redhat.com> - 33-0.2
- Restore baseurl lines, but with example domain

* Tue Feb 11 2020 Mohan Boddu <mboddu@bhujji.com> - 33-0.1
- Setup for rawhide being F33

* Tue Feb 11 2020 Mohan Boddu <mboddu@bhujji.com> - 32-0.4
- Remove baseurl download.fp.o (puiterwijk)
- Enabling dnf countme

* Tue Jan 28 2020 Mohan Boddu <mboddu@bhujji.com> - 32-0.3
- Adding F33 key

* Mon Aug 19 2019 Kevin Fenzi <kevin@scrye.com> - 32-0.2
- Fix f32 key having extra spaces.

* Tue Aug 13 2019 Mohan Boddu <mboddu@bhujji.com> - 32-0.1
- Adding F32 key
- Setup for rawhide being f32

* Tue Mar 12 2019 Vít Ondruch <vondruch@redhat.com> - 31-0.3
- Allow to use newer GPG keys, so Rawhide can be updated after branch.

* Thu Mar 07 2019 Sinny Kumari <skumari@redhat.com> - 31-0.2
- Create fedora-repos-ostree sub-package

* Tue Feb 19 2019 Tomas Hrcka <thrcka@redhat.com> - 31-0.1
- Setup for rawhide being f31

* Mon Feb 18 2019 Mohan Boddu <mboddu@bhujji.com> - 30-0.4
- Adding F31 key

* Sat Jan 05 2019 Kevin Fenzi <kevin@scrye.com> - 30-0.3
- Add fedora-7-primary to archmap. Fixes bug #1531957
- Remove failovermethod option in repos (augenauf(Florian H))

* Tue Nov 13 2018 Mohan Boddu <mboddu@bhujji.com> - 30-0.2
- Adding fedora-iot-2019 key
- Enable skip_if_unavailable for cisco-openh264 repo

* Tue Aug 14 2018 Mohan Boddu <mboddu@bhujji.com> - 30-0.1
- Setup for rawhide being f30
