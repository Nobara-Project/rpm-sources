
# https://gitlab.archlinux.org/archlinux/packaging/packages/yabridge
# https://gitlab.archlinux.org/archlinux/packaging/packages/vst3sdk

##trace

# force single job compilation
%define _smp_mflags -j1

%undefine _hardened_build
%undefine _include_frame_pointers

%global debug_package    %{nil}
%global _lto_cflags      %{nil}

%global vst3sdkversion   v3.7.7_build_19-patched
#%%global vst3sdkversion   v3.7.12_build_20-patched
%global vst3ver          %(b=%{vst3sdkversion}; echo ${b:1:6})

%global gitdate          20260428
%global commit           48ea9749b682c48875366134a42073d6b3d0a8c4
%global shortcommit      %(c=%{commit}; echo ${c:0:7})

%global version          5.1.2
%global release          9

# set this to "1" if building a git/beta/rc release
%global beta_or_rc       1


#=============================================================================
# general
#-----------------------------------------------------------------------------
Name:           yabridge
Version:        %{version}
%if %{beta_or_rc}
Release:        0.%{release}.%{gitdate}.git%{shortcommit}%{?dist}
%else
Release:        %{release}%{?dist}
%endif
Summary:        Yet Another VST bridge, run Windows VST2 plugins under Linux
License:        GPLv3
URL:            https://github.com/robbert-vdh/yabridge
%if %{beta_or_rc}
Source0:        https://github.com/robbert-vdh/yabridge/archive/%{commit}/%{name}-%{version}-git%{shortcommit}.tar.gz
%else
Source0:        https://github.com/robbert-vdh/yabridge/archive/%{version}/%{name}-%{version}.tar.gz
%endif
# https://github.com/robbert-vdh/vst3sdk
# git clone --recursive https://github.com/steinbergmedia/vst3sdk
# git checkout v3.7.7_build_19-patched
# ~/bin/git-archive-all.sh --format=tar.gz --prefix=vst3/ -o ../vst3sdk-v3.7.7_build_19-patched.tar.gz v3.7.7_build_19-patched
## ~/bin/git-archive-all.sh --format=tar.gz --prefix=vst3/ -o ../vst3sdk-v3.7.9_build_61.tar.gz v3.7.9_build_61
Source4:        vst3sdk-%{vst3sdkversion}.tar.gz
#Source5:        vst3sdk-meson.build
#
Patch0:         0001-Change-version-to-5.1.2.patch
#
BuildRequires:  vim
BuildRequires:  cmake
BuildRequires:  cargo
BuildRequires:  git-core
BuildRequires:  meson >= 0.56
BuildRequires:  gcc
BuildRequires:  gcc-c++
#BuildRequires:  asio-devel
BuildRequires:  boost
BuildRequires:  boost-devel
BuildRequires:  boost-filesystem
BuildRequires:  dbus-devel
BuildRequires:  git-core
BuildRequires:  glibc-devel
BuildRequires:  libstdc++-devel
BuildRequires:  libxcb-devel
BuildRequires:  rust
BuildRequires:  wine-staging-devel
BuildRequires:  winehq-staging
BuildRequires:  xcb-util-wm-devel

BuildArch:      x86_64

Requires:       boost
Requires:       boost-filesystem
Requires:       libxcb
Requires:       libXau
Requires:       python3
Requires:       winehq-staging


%description
Yet Another way to use Windows VST plugins on Linux. Yabridge seamlessly
supports running both 64-bit Windows VST2 plugins as well as 32-bit Windows
VST2 plugins in a 64-bit Linux VST host. This project aims to be as
transparent as possible to achieve the best possible plugin compatibility
while also staying easy to debug and maintain.


#=============================================================================
# prep
#-----------------------------------------------------------------------------
%prep
%if %{beta_or_rc}
%autosetup -p1 -n %{name}-%{commit}
%else
%autosetup -p1 -n %{name}-%{version}
%endif

pushd subprojects/
# vst3sdk
tar -xzf %{SOURCE4}
#rm -rf vst3/.git vst3/.gitmodules
#cp -av %%{SOURCE5} vst3/meson.build
popd

# update vst version
#sed -i -e"s|version : .*$|version : '%%{vst3ver}')|" src/common/vst3/meson.build

## disable patching
#sed -i -e's|^patch_result|#patch_result|' src/common/vst3/meson.build
#sed -i -e's|^message(patch_result|#message(patch_result|' src/common/vst3/meson.build

# rename migration README.md for easier inclusion in the package
mv -v tools/migration/README.md tools/migration/README-migration.md

## only enable to debug failing builds
#echo "" >> cross-wine.conf
#echo "cpp_args = ['-v']" >> cross-wine.conf

%if %{beta_or_rc}
# sync yabridgectl version with yabridge version
sed -i -e's|^version.*$|version = "%{version}"|' tools/yabridgectl/Cargo.toml
%endif

## change deprecated dialect option 'c++2a' to c++20 in meson.build 
## see https://gcc.gnu.org/onlinedocs/gcc/C-Dialect-Options.html#Options-Controlling-C-Dialect
#sed -i -e's|c++2a|c++20|g' meson.build

#=============================================================================
# build
#-----------------------------------------------------------------------------
%build
export LDFLAGS="%{build_ldflags}"

meson setup . \
  --buildtype=release \
  --cross-file cross-wine.conf \
  -D bitbridge=false \
  -D b_lto=false \
  -D b_pie=false \
  -D build.cpp_link_args="$LDFLAGS" \
  -D cpp_link_args="$LDFLAGS -mwindows" \
  --unity=on --unity-size=1000 \
  build

#  --unity=on --unity-size=1000 \

ninja -v %{_smp_mflags} -C build

pushd tools/yabridgectl
cargo build --release --all-features
popd


#=============================================================================
# check
#-----------------------------------------------------------------------------
%check
# there are no tests
# ninja test -v -j1 -C build test


#=============================================================================
# install
#-----------------------------------------------------------------------------
%install
# create directories
install -d -m0755 %{buildroot}%{_bindir}
install -d -m0755 %{buildroot}%{_libdir}

# install apps and libs
install -D -m 0755 build/yabridge-host*.exe* %{buildroot}%{_bindir}/
install -D -m 0755 build/libyabridge-chainloader-vst*.so %{buildroot}%{_libdir}/
install -D -m 0755 build/libyabridge-chainloader-clap*.so %{buildroot}%{_libdir}/
install -D -m 0755 build/libyabridge-vst*.so %{buildroot}%{_libdir}/
install -D -m 0755 build/libyabridge-clap*.so %{buildroot}%{_libdir}/

# install tool
install -D -m 0755 tools/yabridgectl/target/release/yabridgectl %{buildroot}%{_bindir}/

# install migration scripts
install -D -m 0755 tools/migration/*.py %{buildroot}%{_bindir}/



#=============================================================================
# files
#-----------------------------------------------------------------------------
%files
%defattr(-,root,root)
%license COPYING
%doc CHANGELOG.md README.md ROADMAP.md tools/migration/README-migration.md
%attr(0755,root,root)        %{_bindir}/yabridgectl
%attr(0755,root,root)        %{_bindir}/yabridge-host.exe
%attr(0755,root,root)        %{_bindir}/yabridge-host.exe.so
# migration scripts
%attr(0755,root,root)        %{_bindir}/migrate-ardour.py
%attr(0755,root,root)        %{_bindir}/migrate-bitwig.py
%attr(0755,root,root)        %{_bindir}/migrate-reaper.py
%attr(0755,root,root)        %{_bindir}/migrate-renoise.py
%attr(0755,root,root)        %{_libdir}/libyabridge-chainloader-clap.so
%attr(0755,root,root)        %{_libdir}/libyabridge-chainloader-vst2.so
%attr(0755,root,root)        %{_libdir}/libyabridge-chainloader-vst3.so
%attr(0755,root,root)        %{_libdir}/libyabridge-clap.so
%attr(0755,root,root)        %{_libdir}/libyabridge-vst2.so
%attr(0755,root,root)        %{_libdir}/libyabridge-vst3.so


#=============================================================================
# post
#-----------------------------------------------------------------------------
%post
/sbin/ldconfig


#=============================================================================
# postun
#-----------------------------------------------------------------------------
%postun
/sbin/ldconfig


#=============================================================================
# changelog
#-----------------------------------------------------------------------------
%changelog
* Sat Jun 14 2025 Patrick Laimbock <patrick@laimbock.com> - 5.1.2-0.7
- use git rev 918d24a16e8eda9ac2eac692704770dfed96f6ee from master branch
- disable asio-devel BRs

* Mon Mar 17 2025 Patrick Laimbock <patrick@laimbock.com> - 5.1.2-0.6
- use git rev 0f3e7629539c7cfefca94086b677da31319eab16 from master branch

* Mon Mar 17 2025 Patrick Laimbock <patrick@laimbock.com> - 5.1.2-0.5
- sync with Arch's PKGBUILD

* Sun Mar 16 2025 Patrick Laimbock <patrick@laimbock.com> - 5.1.2-0.4
- build against wine-10.3 in the test copr
- enable 32 bit

* Sat Mar 01 2025 Patrick Laimbock <patrick@laimbock.com> - 5.1.2-0.3
- build against wine-10.3 in the test copr
- disable 32 bit, it does not build

* Sat Mar 01 2025 Patrick Laimbock <patrick@laimbock.com> - 5.1.2-0.2
- switch to branch new-wine10-embedding
- git rev be52c36ab74bc46ca69d0bef1597c5b327c1dab1
- no 32 bit support

* Sat Mar 01 2025 Patrick Laimbock <patrick@laimbock.com> - 5.1.2-0.1
- build git rev ca5343087f09e6267394d202d6caec5bafe0952e
- use vst3sdk v3.7.7_build_19-patched

* Fri Feb 28 2025 Patrick Laimbock <patrick@laimbock.com> - 5.1.1-2
- add PR 405. Thanks Rémi !!!

* Sun Nov 10 2024 Patrick Laimbock <patrick@laimbock.com> - 5.1.1-1
- update to version 5.1.1

* Mon Aug 26 2024 Patrick Laimbock <patrick@laimbock.com> - 5.1.0-11
- add patch from https://github.com/robbert-vdh/yabridge/pull/316

* Mon Aug 26 2024 Patrick Laimbock <patrick@laimbock.com> - 5.1.0-10
- update vst3-sdk-patch-3.7.12.diff
- update meson.build

* Mon Aug 26 2024 Patrick Laimbock <patrick@laimbock.com> - 5.1.0-9
- update vst3-sdk-patch-3.7.12.diff

* Mon Aug 26 2024 Patrick Laimbock <patrick@laimbock.com> - 5.1.0-8
- update vst3-sdk-patch-3.7.12.diff

* Mon Aug 26 2024 Patrick Laimbock <patrick@laimbock.com> - 5.1.0-7
- build against prepatched vst3sdk-v3.7.12_build_20

* Mon Aug 26 2024 Patrick Laimbock <patrick@laimbock.com> - 5.1.0-6
- rebuild against my (hopefully) fixed vst3sdk gh tree

* Sat Aug 24 2024 Patrick Laimbock <patrick@laimbock.com> - 5.1.0-5
- update VST3SDK to  3.7.12_build_20
- use updated vst3sdk in my gh git repo

* Sun Jun 09 2024 Patrick Laimbock <patrick@laimbock.com> - 5.1.0-4
- wine-tkg-dev build
- require wine-9.10

* Fri May 17 2024 Patrick Laimbock <patrick@laimbock.com> - 5.1.0-3
- require wine >= 9.8 so 9.9 and later are included

* Sun May 05 2024 Patrick Laimbock <patrick@laimbock.com> - 5.1.0-2
- build/require wine-9.8 from the wine-tkg-dev copr

* Wed Dec 27 2023 Patrick Laimbock <patrick@laimbock.com> - 5.1.0-1
- update to version 5.1.0
- require strictly wine-9.4 (nothing later)

* Sat Dec 16 2023 Patrick Laimbock <patrick@laimbock.com> - 5.0.5-7
- rebuild against wine-9.0(-rc2)

* Mon Nov 13 2023 Patrick Laimbock <patrick@laimbock.com> - 5.0.5-6
- build against wine-8.20

* Thu Oct 26 2023 Patrick Laimbock <patrick@laimbock.com> - 5.0.5-5
- build against wine-8.18
- add fix for https://bugzilla.redhat.com/show_bug.cgi?id=2246731

* Sun Jun 11 2023 Patrick Laimbock <patrick@laimbock.com> - 5.0.5-4
- build against wine-8.10

* Mon May 29 2023 Patrick Laimbock <patrick@laimbock.com> - 5.0.5-3
- build against wine-8.9.1
- require the latest stable wine version in the wine-tkg copr

* Mon May 15 2023 Patrick Laimbock <patrick@laimbock.com> - 5.0.5-2
- build against wine-8.8

* Sun May 07 2023 Patrick Laimbock <patrick@laimbock.com> - 5.0.5-1
- update to version 5.0.5
- require at least wine 8.6 so you can also use regular Fedora wine

* Sat Apr 29 2023 Patrick Laimbock <patrick@laimbock.com> - 5.0.4-5
- build against wine-8.7

* Wed Apr 19 2023 Patrick Laimbock <patrick@laimbock.com> - 5.0.4-4
- build against wine-8.6

* Tue Apr 04 2023 Patrick Laimbock <patrick@laimbock.com> - 5.0.4-3
- build against wine-8.5

* Thu Mar 30 2023 Patrick Laimbock <patrick@laimbock.com> - 5.0.4-2
- build against wine-8.4

* Thu Feb 23 2023 Patrick Laimbock <patrick@laimbock.com> - 5.0.4-1
- update to version 5.0.4
- build against wine-8.2

* Mon Jan 02 2023 Patrick Laimbock <patrick@laimbock.com> - 5.0.3-1
- update to version 5.0.3
- build against wine-8.0
- enable unity build
- build with vst3sdk-v3.7.7_build_19

* Mon Nov 28 2022 Patrick Laimbock <patrick@laimbock.com> - 5.0.2-1
- update to version 5.0.2
- disable unity build

* Mon Nov 14 2022 Patrick Laimbock <patrick@laimbock.com> - 5.0.1-1
- update to version 5.0.1
- hotfix for upcoming wine-7.21
- fix not correctly tracking moduleinfo.json files for VST 3.7.5 plugins

* Thu Nov 03 2022 Patrick Laimbock <patrick@laimbock.com> - 5.0.0-2
- add clap files

* Thu Nov 03 2022 Patrick Laimbock <patrick@laimbock.com> - 5.0.0-1
- update to version 5.0.0
- build against wine-7.20
- build with v3.7.5_build_44-patched-2

* Sat Oct 01 2022 Patrick Laimbock <patrick@laimbock.com> - 4.0.2-3
- build against wine-7.18

* Sat Sep 10 2022 Patrick Laimbock <patrick@laimbock.com> - 4.0.2-2
- build against wine-7.17

* Fri Sep 02 2022 Patrick Laimbock <patrick@laimbock.com> - 4.0.2-1
- release of 4.0.2 for yabridge-stable COPR
- build against wine-7.16

* Sun Aug 28 2022 Patrick Laimbock <patrick@laimbock.com> - 4.0.3-0.5
- update to git rev d614ef91b5a1c7611a681af4aad941b6b84f17f8
- build against wine-7.16

* Sun Aug 14 2022 Patrick Laimbock <patrick@laimbock.com> - 4.0.3-0.4
- build against wine-7.15

* Sat Jul 30 2022 Patrick Laimbock <patrick@laimbock.com> - 4.0.3-0.3
- build against wine-7.14

* Sat Jul 16 2022 Patrick Laimbock <patrick@laimbock.com> - 4.0.3-0.2
- update to git rev ef7a85eb10a2d34b6acfc464feede919279aecd5
- build against wine-7.13

* Sun Jul 10 2022 Patrick Laimbock <patrick@laimbock.com> - 4.0.3-0.1
- update to git rev 2a26014465b24834788b0b6b944406e9cc2c33b2
- build against wine-7.12

* Fri Jul 08 2022 Patrick Laimbock <patrick@laimbock.com> - 4.0.2-1
- update to version 4.0.2

* Sun Jun 26 2022 Patrick Laimbock <patrick@laimbock.com> - 4.0.2-0.1
- update to git rev d479f3fc0c7587c5d7500a8a150a4dbff8573d6c

* Sun Jun 26 2022 Patrick Laimbock <patrick@laimbock.com> - 4.0.1-1
- update to version 4.0.1
- build against wine-7.10
- build with v3.7.5_build_44-patched
- add migration scripts

* Sat Mar 26 2022 Patrick Laimbock <patrick@laimbock.com> - 3.8.2-0.1
- update to git rev 798b5179ef139e5faad50adb9efc842d325455f4
- build against wine-7.5

* Mon Feb 28 2022 Patrick Laimbock <patrick@laimbock.com> - 3.8.1-0.1
- update to git rev 7a5c4ab73efd4b90f5642857c1e7628cca13b8a6

* Sun Feb 27 2022 Patrick Laimbock <patrick@laimbock.com> - 3.8.0-2
- build against wine-7.3

* Sun Feb 27 2022 Patrick Laimbock <patrick@laimbock.com> - 3.8.0-1
- update to version 3.8.0
- build against wine-7.2
- add de470d345ab206b08f6d4a147b6af1d285a4211f.patch

* Sat Jan 01 2022 Patrick Laimbock <patrick@laimbock.com> - 3.7.1-0.3
- update to git rev e0ab24e64581dcd3c6367054ab670a8b7201b5d9
- require meson >= 0.55
- build against wine-7.0rc3

* Sun Dec 05 2021 Patrick Laimbock <patrick@laimbock.com> - 3.7.1-0.2
- build against wine-6.23

* Sun Dec 05 2021 Patrick Laimbock <patrick@laimbock.com> - 3.7.1-0.1
- update to git rev e4b2a383309dc6020945d2c2dbb5425a70f6e05b

* Sun Nov 21 2021 Patrick Laimbock <patrick@laimbock.com> - 3.7.0-1
- update to version 3.7.0

* Thu Nov 11 2021 Patrick Laimbock <patrick@laimbock.com> - 3.6.1-0.5
- update to git rev a94be5638781d962ee20c95afd216843e9e443d0
- let yabridge download bitsery, function2 and tomlplusplus since it
- already does the same for all the yabridgectl deps

* Sun Nov 07 2021 Patrick Laimbock <patrick@laimbock.com> - 3.6.1-0.4
- update to git rev dd6144333a6d065cda8fd38bab1f79e0dbaaed34
- build against wine-6.21

* Sat Oct 23 2021 Patrick Laimbock <patrick@laimbock.com> - 3.6.1-0.3
- update to git rev 5be149cb525a638f7fc3adf84918c8239ee50ecf
- counters https://bugs.winehq.org/show_bug.cgi?id=51919

* Sat Oct 23 2021 Patrick Laimbock <patrick@laimbock.com> - 3.6.1-0.2
- build against wine-6.20

* Thu Oct 21 2021 Patrick Laimbock <patrick@laimbock.com> - 3.6.1-0.1
- update to git rev 0382b0a475480779a968b81f713af3c58ac80884

* Sat Oct 09 2021 Patrick Laimbock <patrick@laimbock.com> - 3.5.3-0.6
- update to git rev cfc0591ca9dfa0b11cce6bb3fe699c455bcbc1a1
- build against wine-6.19

* Thu Oct 07 2021 Patrick Laimbock <patrick@laimbock.com> - 3.5.3-0.5
- update to git rev c18332f7d4178416152af5538881a091cdf819ca
- build against wine-6.18

* Sat Sep 11 2021 Patrick Laimbock <patrick@laimbock.com> - 3.5.3-0.4
- update to git rev f8703bb49c1820d9b1e8148d863a2d11166dcc09
- build against wine-6.17

* Sat Aug 28 2021 Patrick Laimbock <patrick@laimbock.com> - 3.5.3-0.3
- build against wine-6.16

* Tue Aug 24 2021 Patrick Laimbock <patrick@laimbock.com> - 3.5.3-0.2
- update to git rev a1cbf23f66166608174d57ec783f750caf0b2ff7

* Wed Aug 18 2021 Patrick Laimbock <patrick@laimbock.com> - 3.5.3-0.1
- update to git rev 5bf3b971189d64f098e89d64468a2c1ec81a56a6

* Sat Aug 14 2021 Patrick Laimbock <patrick@laimbock.com> - 3.5.2-2
- build against wine-6.15

* Sun Aug 08 2021 Patrick Laimbock <patrick@laimbock.com> - 3.5.2-1
- update to version 3.5.2

* Fri Aug 06 2021 Patrick Laimbock <patrick@laimbock.com> - 3.5.2-0.2
- update to git rev 9160de648365ddedfa8ae759ba6691ed7753ed0f

* Mon Aug 02 2021 Patrick Laimbock <patrick@laimbock.com> - 3.5.2-0.1
- update to git rev 2e6732c0e2932ee623c2a8cb9e2f1a17225ff941

* Sun Aug 01 2021 Patrick Laimbock <patrick@laimbock.com> - 3.5.1-1
- update to version 3.5.1

* Sat Jul 31 2021 Patrick Laimbock <patrick@laimbock.com> - 3.5.1-0.1
- update to git rev e430c5f0155417f1bb9572be0816d95155e3f2fd

* Sat Jul 24 2021 Patrick Laimbock <patrick@laimbock.com> - 3.5.0-1
- update to version 3.5.0

* Thu Jul 22 2021 Patrick Laimbock <patrick@laimbock.com> - 3.4.1-0.4
- update to git rev 8108e08dbfddf678f9505c2f854ae39d27e8319c

* Thu Jul 22 2021 Patrick Laimbock <patrick@laimbock.com> - 3.4.1-0.3
- build against wine-6.13
- update to git rev 1e47390edc2258a2aa1e7deccc3144dc5bf1370b

* Tue Jul 20 2021 Patrick Laimbock <patrick@laimbock.com> - 3.4.1-0.2
- update to git rev 640c188338acdbd5e21664fac4ab6827fdc9f8ac

* Mon Jul 19 2021 Patrick Laimbock <patrick@laimbock.com> - 3.4.1-0.1
- update to git rev 503720a9ca5782035ffbf41330e66fc9f4fbf045

* Thu Jul 15 2021 Patrick Laimbock <patrick@laimbock.com> - 3.4.0-1
- update to version 3.4.0

* Tue Jul 13 2021 Patrick Laimbock <patrick@laimbock.com> - 3.3.2-0.14
- update to git rev a2b877b101512e7dd621c30d123a0118467a889a

* Mon Jul 12 2021 Patrick Laimbock <patrick@laimbock.com> - 3.3.2-0.13
- update to git rev 11d3ec90108c2929abe69a44c50c3db39535abd3

* Sun Jul 11 2021 Patrick Laimbock <patrick@laimbock.com> - 3.3.2-0.12
- update to git rev 1b4c4ecfaddb585ec64dbc57b787a7658516ed01

* Sun Jul 11 2021 Patrick Laimbock <patrick@laimbock.com> - 3.3.2-0.11
- update to git rev b1b47ec80dc520e7feec83775910a84c5ec603c5

* Sun Jul 11 2021 Patrick Laimbock <patrick@laimbock.com> - 3.3.2-0.10
- update to git rev d21073f8660d77a798506857d9498d7490c86499

* Sun Jul 11 2021 Patrick Laimbock <patrick@laimbock.com> - 3.3.2-0.9
- update to git rev 4e67fa92128d54ab12544b489628482f404ba960

* Sun Jul 11 2021 Patrick Laimbock <patrick@laimbock.com> - 3.3.2-0.8
- update to git rev 6f3beca32af75a47255a5c9b37d17bbad50b24c4

* Sat Jul 10 2021 Patrick Laimbock <patrick@laimbock.com> - 3.3.2-0.7
- update to git rev 94125f9eab52093558294ef685095b7a36be2edc

* Sat Jul 10 2021 Patrick Laimbock <patrick@laimbock.com> - 3.3.2-0.6
- update to git rev 92daa33adfba7273f5ebd25544ebe242c5bf4c57

* Sat Jul 10 2021 Patrick Laimbock <patrick@laimbock.com> - 3.3.2-0.5
- update to git rev 1946693244f5f862c60805d733468dfc056b0b4a
- build against wine-6.12

* Wed Jul 07 2021 Patrick Laimbock <patrick@laimbock.com> - 3.3.2-0.4
- update to git rev a58a1ab111abd73b0cb014b9ac4c9edcf3a3f01b

* Sat Jul 03 2021 Patrick Laimbock <patrick@laimbock.com> - 3.3.2-0.3
- update to git rev c13d8f2ee3fcdb5beb6b8c9c5e8b1d421464ca86

* Sun Jun 27 2021 Patrick Laimbock <patrick@laimbock.com> - 3.3.2-0.2
- update to git rev e0713c5fe7da9d52268bcabf0ae90e14fd2e2345

* Sun Jun 13 2021 Patrick Laimbock <patrick@laimbock.com> - 3.3.2-0.1
- update to git rev 42e1e49ab983e909c0dcb9259aa140b5d7e57c06

* Thu Jun 10 2021 Patrick Laimbock <patrick@laimbock.com> - 3.3.1-1
- update to version 3.3.1

* Sun Jun 06 2021 Patrick Laimbock <patrick@laimbock.com> - 3.3.0-2
- build against wine-6.10

* Fri Jun 04 2021 Patrick Laimbock <patrick@laimbock.com> - 3.3.0-1
- update to version 3.3.0

* Tue Jun 01 2021 Patrick Laimbock <patrick@laimbock.com> - 3.2.1-0.9
- update to git rev 712ef41a7fc814fc873d398b7299ce971619cbda

* Mon May 31 2021 Patrick Laimbock <patrick@laimbock.com> - 3.2.1-0.8
- update to git rev 5f4ffed90bb4f0eed9731d020daa35fb2e34d0f2

* Sun May 30 2021 Patrick Laimbock <patrick@laimbock.com> - 3.2.1-0.7
- update to git rev db0f58d0009ead6ba7547f514032f25c5fda9e7e

* Tue May 25 2021 Patrick Laimbock <patrick@laimbock.com> - 3.2.1-0.6
- update to git rev 4d5b2fcb12c7f08f0f971c0873e554d8cb303740

* Sun May 23 2021 Patrick Laimbock <patrick@laimbock.com> - 3.2.1-0.5
- update to git rev 0b9b1330ad9aabc238f7d3c335d1485a74b36606
- build against wine-6.9
- more optimizations!

* Sat May 22 2021 Patrick Laimbock <patrick@laimbock.com> - 3.2.1-0.4
- update to git rev 7c49fe739df2a9b83984c8c4e0db926dd5b6067d
- performance enhancements!

* Wed May 19 2021 Patrick Laimbock <patrick@laimbock.com> - 3.2.1-0.3
- update to git rev 4d256e12e2b6d6180bf117d68e960cfd859e6719
- adds disable_pipes option to make UJAM/Loopmaster/Gorilla SDK plugins work

* Mon May 17 2021 Patrick Laimbock <patrick@laimbock.com> - 3.2.1-0.2
- update to git rev 09c2ed96adb0480a20eeaa8b03260c56e4c10956

* Sun May 09 2021 Patrick Laimbock <patrick@laimbock.com> - 3.2.1-0.1
- update to git rev db6ecdbbd4ae4452637a89e21e893570d78d0018

* Fri Apr 30 2021 Patrick Laimbock <patrick@laimbock.com> - 3.1.1-0.2
- update to git rev 89d6c1b2e0cc9253c745dc73f7c152cbc426eb4f
- fixes a segfault occuring in several but not all libstdc++ versions

* Sun Apr 25 2021 Patrick Laimbock <patrick@laimbock.com> - 3.1.1-0.1
- update to git rev 671c6a4c1812afb8261a83c3328ce064a7e88bc6
- build against wine-6.7

* Mon Apr 19 2021 Patrick Laimbock <patrick@laimbock.com> - 3.1.0-2
- rebuild against wine-6.6 with backported fix for BZ50996

* Thu Apr 15 2021 Patrick Laimbock <patrick@laimbock.com> - 3.1.0-1
- update to version 3.1.0

* Thu Apr 15 2021 Patrick Laimbock <patrick@laimbock.com> - 3.0.3-0.2
- update to git rev 4eb0490fdeb70270d70c4d0d60491d8b7d0e736c

* Mon Apr 12 2021 Patrick Laimbock <patrick@laimbock.com> - 3.0.3-0.1
- update to git rev 266d22b051ce7870dbc73045c91a0368fc3d78b8
- build against wine-6.5

* Mon Mar 15 2021 Patrick Laimbock <patrick@laimbock.com> - 3.0.2-2
- add patch for missing include

* Mon Mar 08 2021 Patrick Laimbock <patrick@laimbock.com> - 3.0.2-1
- update to version 3.0.2

* Sat Feb 27 2021 Patrick Laimbock <patrick@laimbock.com> - 3.0.1-1
- update to version 3.0.1
- build against wine-6.3

* Tue Feb 23 2021 Patrick Laimbock <patrick@laimbock.com> - 3.0.1-0.1
- update to git rev a6ac958bfb467e3e0e789cf0c64475bb32b383c6
- includes fix for a REAPER segfault
- includes fix for wine 6.3 regression

* Sun Feb 21 2021 Patrick Laimbock <patrick@laimbock.com> - 3.0.0-1
- update to version 3.0.0

* Sat Feb 13 2021 Patrick Laimbock <patrick@laimbock.com> - 2.2.2-0.12
- update to git rev 4e4ed3a6b46845a67eba90333309051bf1a9e672
- drop patch which is now in upstream

* Thu Feb 04 2021 Patrick Laimbock <patrick@laimbock.com> - 2.2.2-0.11
- add yabridgectl_use_usr_lib64.patch which makes yabridgectl look in /usr/lib64

* Tue Feb 02 2021 Patrick Laimbock <patrick@laimbock.com> - 2.2.2-0.10
- update to git rev 391206eea86eaffd91441ec2e1809d558f64fe14

* Sat Jan 30 2021 Patrick Laimbock <patrick@laimbock.com> - 2.2.2-0.9
- update to git rev 81d401f06a0d3908dbac0785dd2475545f43f8fa

* Sat Jan 30 2021 Patrick Laimbock <patrick@laimbock.com> - 2.2.2-0.8
- update to git rev 68bf2029b3100dd6e88876e607f7d444b729ba7a

* Wed Jan 27 2021 Patrick Laimbock <patrick@laimbock.com> - 2.2.2-0.7
- update to git rev 04d0ff094911edc9423001c8fd26d326e858f673

* Sat Jan 23 2021 Patrick Laimbock <patrick@laimbock.com> - 2.2.2-0.6
- update to git rev d5e44244631e7e31110d4e5c6f0ba09dc7d71b88

* Thu Jan 21 2021 Patrick Laimbock <patrick@laimbock.com> - 2.2.2-0.5
- update to git rev 2ca1d5b8caa53d65a052a97047e43f7551e42474
- add the yabridgectl utility

* Mon Jan 11 2021 Patrick Laimbock <patrick@laimbock.com> - 2.2.2-0.4
- test build from the feature/non-realtime-event-loop branch
- git rev 3ca70616590cc5161863d5647035d358534d1a53

* Sun Jan 10 2021 Patrick Laimbock <patrick@laimbock.com> - 2.2.2-0.3
- update to git rev c938068cf53a235bb6c85fbd922049ac14bd78d9
- use vst3sdk git rev e2fbb41f28a4b311f2fc7d28e9b4330eec1802b6
- build against wine-staging-6.0-rc6

* Sun Jan 03 2021 Patrick Laimbock <patrick@laimbock.com - 2.2.2-0.2
- update to git rev 71eadff1edd6f9e54ab608e828cdd6f4b9e9f28c
- build against wine-6.0-rc5

* Mon Dec 21 2020 Patrick Laimbock <patrick@laimbock.com> - 2.2.2-0.1
- update to git rev 6ef740e0b0a67fddfa19dcbf1c8d11a2f12ed103
- build against wine-6.0rc3

* Fri Dec 18 2020 Patrick Laimbock <patrick@laimbock.com> - 2.2.1-1
- update to version 2.1.2
- build against wine 6.0rc2

* Sun Nov 29 2020 Patrick Laimbock <patrick@laimbock.com> - 2.1.1-0.1
- update to git rev cbf276b7dc9d8a9b0d50c46fd48ebfc293dd809b

* Thu Nov 26 2020 Patrick Laimbock <patrick@laimbock.com> - 2.1.0-2
- build against wine 5.22

* Fri Nov 20 2020 Patrick Laimbock <patrick@laimbock.com> - 2.1.0-1
- update to version 2.1.0

* Sat Nov 14 2020 Patrick Laimbock <patrick@laimbock.com> - 2.0.3-0.1
- update to git rev 005ae61e0825500f5a71419b30d78e11382f8502
- from branch bitwig-3.3-beta-hack to work around plugin load issue

* Mon Nov 09 2020 Patrick Laimbock <patrick@laimbock.com> - 2.0.1-1
- update to version 2.0.1

* Sun Nov 08 2020 Patrick Laimbock <patrick@laimbock.com> - 1.7.2-0.3
- update to git rev 889d9d81c4c2033e229c831fa5e0d79b9b480293

* Sat Nov 07 2020 Patrick Laimbock <patrick@laimbock.com> - 1.7.2-0.2
- update to git rev 42032c5c2dfda0aa3844a67adc091a0994418822

* Sat Nov 07 2020 Patrick Laimbock <patrick@laimbock.com> - 1.7.2-0.1
- update to git rev 23cd2dd1933b628c4c33298deeac428bd90d1056

* Tue Oct 27 2020 Patrick Laimbock <patrick@laimbock.com> - 1.7.1-2
- build against wine 5.20

* Fri Oct 23 2020 Patrick Laimbock <patrick@laimbock.com> - 1.7.1-1
- update to version 1.7.1

* Fri Oct 23 2020 Patrick Laimbock <patrick@laimbock.com> - 1.7.1-0.2
- update to git rev c2ec1ce9943f2bf2efd8c705e786c5cb659a2499

* Sat Oct 17 2020 Patrick Laimbock <patrick@laimbock.com> - 1.7.1-0.1
- update to HEAD

* Sat Oct 17 2020 Patrick Laimbock <patrick@laimbock.com> - 1.7.0-1
- update to version 1.7.0

* Wed Sep 30 2020 Patrick Laimbock <patrick@laimbock.com> - 1.6.1-1
- update to version 1.6.1

* Wed Sep 09 2020 Patrick Laimbock <patrick@laimbock.com> - 1.6.0-1
- update to version 1.6.0
- build against wine 5.17

* Wed Sep 09 2020 Patrick Laimbock <patrick@laimbock.com> - 1.5.0-2
- build against wine 5.16

* Sun Aug 23 2020 Patrick Laimbock <patrick@laimbock.com> - 1.5.0-1
- update to version 1.5.0

* Sun Aug 16 2020 Patrick Laimbock <patrick@laimbock.com> - 1.4.2-0.1
- update to git rev ebe1a9c64962a2e41dc8df2e9f0f3bdad5aaf65e

* Sun Aug 16 2020 Patrick Laimbock <patrick@laimbock.com> - 1.4.1-1
- update to version 1.4.1

* Sun Jul 19 2020 Patrick Laimbock <patrick@laimbock.com> - 1.3.0-1
- update to version 1.3.0

* Sat Jun 06 2020 Patrick Laimbock <patrick@laimbock.com> - 1.2.1-0.1
- update to git rev 4403585a7075b1b06fd75a8ea31eb3bbf9101545

* Tue Jun 02 2020 Patrick Laimbock <patrick@laimbock.com> - 1.2.0-1
- update to version 1.2.0
- build against wine 5.9-2

* Sun May 17 2020 Patrick Laimbock <patrick@laimbock.com> - 1.1.5-0.1
- initial release for Fedora 32
- use git rev e728dbe5a2262d9df931c93c651b053d7a80b5e5

