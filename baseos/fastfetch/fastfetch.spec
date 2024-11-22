Name:           fastfetch
Version:        2.29.0
Release:        2%{?dist}
Summary:        Like neofetch, but much faster because written in c

License:        MIT
URL:            https://github.com/fastfetch-cli/fastfetch
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  python3
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  hwdata-devel
BuildRequires:  wayland-devel
BuildRequires:  libxcb-devel
BuildRequires:  libXrandr-devel
BuildRequires:  dconf-devel
BuildRequires:  dbus-devel
BuildRequires:  sqlite-devel
BuildRequires:  ImageMagick-devel
BuildRequires:  zlib-devel
BuildRequires:  libglvnd-devel
BuildRequires:  mesa-libOSMesa-devel
BuildRequires:  xfconf-devel
BuildRequires:  glib2-devel
BuildRequires:  ocl-icd-devel
BuildRequires:  rpm-devel
BuildRequires:  libdrm-devel
BuildRequires:  pulseaudio-libs-devel
BuildRequires:  elfutils-libelf-devel
# not available on s390x
%if "%{_arch}" != "s390x"
BuildRequires:  libddcutil-devel
%endif
# vulkan-loader not available in el8 on some arches
%if 0%{?rhel} == 8
  %if "%{_arch}" != "s390x" && "%{_arch}" != "ppc64le"
BuildRequires:  vulkan-loader-devel
  %endif
%else
BuildRequires:  vulkan-loader-devel
%endif
BuildRequires:  chafa-devel
BuildRequires:  yyjson-devel

Recommends:     hwdata
Recommends:     libxcb
Recommends:     libXrandr
Recommends:     dconf
Recommends:     sqlite
Recommends:     zlib
Recommends:     libglvnd-glx
Recommends:     ImageMagick
Recommends:     glib2
Recommends:     ocl-icd
Recommends:     chafa
Recommends:     ddcutil
Recommends:     libdrm
Recommends:     pulseaudio-libs
Recommends:     elfutils-libelf

Provides: neofetch
Obsoletes: neofetch

ExcludeArch:    %{ix86}

%description
fastfetch is a neofetch-like tool for fetching system information and
displaying them in a pretty way. It is written in c to achieve much better
performance, in return only Linux and Android are supported. It also uses
mechanisms like multithreading and caching to finish as fast as possible.


%package bash-completion
Summary: Bash completion files for %{name}
Requires: bash-completion
Requires: %{name} = %{version}-%{release}
BuildArch: noarch


%description bash-completion
%{summary}


%package zsh-completion
Summary: ZSH completion files for %{name}
Requires: zsh
Requires: %{name} = %{version}-%{release}
BuildArch: noarch


%description zsh-completion
%{summary}


%package fish-completion
Summary: Fish completion files for %{name}
Requires: fish
Requires: %{name} = %{version}-%{release}
BuildArch: noarch


%description fish-completion
%{summary}


%prep
%autosetup -p1


%build
%cmake -DBUILD_TESTS=ON -DENABLE_SYSTEM_YYJSON=ON
%cmake_build

ln -s %{_bindir}/%{name} %{buildroot}%{_bindir}/neofetch


%check
%ctest


%install
%cmake_install


%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_bindir}/neofetch
%{_bindir}/flashfetch
%{_datadir}/%{name}/
%{_mandir}/man1/fastfetch.1*

%files bash-completion
%{_datadir}/bash-completion/completions/%{name}

%files fish-completion
%{_datadir}/fish/vendor_completions.d/%{name}.fish

%files zsh-completion
%{_datadir}/zsh/site-functions/_%{name}

%changelog
* Wed Nov 06 2024 Jonathan Wright <jonathan@almalinux.org> - 2.29.0-1
- update to 2.29.0 rhbz#2321319

* Fri Oct 11 2024 Jonathan Wright <jonathan@almalinux.org> - 2.27.1-1
- update to 2.271 rhbz#2311792

* Fri Sep 06 2024 Jonathan Wright <jonathan@almalinux.org> - 2.23.0-1
- update to 2.23.0 rhbz#2308109

* Thu Aug 22 2024 Jonathan Wright <jonathan@almalinux.org> - 2.21.3-1
- update to 2.21.3 rhbz#2304804

* Sat Aug 10 2024 Jonathan Wright <jonathan@almalinux.org> - 2.21.1-1
- update to 1.21.1 rhbz#2303930

* Thu Aug 08 2024 Jonathan Wright <jonathan@almalinux.org> - 2.21.0-1
- update to 2.21.0 rhbz#2299617

* Fri Jul 26 2024 Jonathan Wright <jonathan@almalinux.org> - 2.20.0-1
- update to 2.20.0 rhbz#2299617

* Mon Jul 22 2024 Jonathan Wright <jonathan@almalinux.org> - 2.19.0-1
- update to 2.19.0 rhbz#2295466

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.17.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jul 04 2024 Jonathan Wright <jonathan@almalinux.org> - 2.17.2-1
- update to 2.17.2 rhbz#2295466

* Fri Jun 21 2024 Jonathan Wright <jonathan@almalinux.org> - 2.16.0-1
- update to 2.16.0 rhbz#2293527

* Sat Jun 08 2024 Jonathan Wright <jonathan@almalinux.org> - 2.15.0-1
- update to 2.15.0 rhbz#2291027

* Thu May 30 2024 Jonathan Wright <jonathan@almalinux.org> - 2.14.0-1
- update to 2.14.0 rhbz#2283073

* Tue May 21 2024 Jonathan Wright <jonathan@almalinux.org> - 2.13.1-1
- update to 2.13.1 rhbz#2279431

* Tue May 07 2024 Jonathan Wright <jonathan@almalinux.org> - 2.11.5-1
- update to 2.11.5 rhbz#2279077

* Fri May 03 2024 Jonathan Wright <jonathan@almalinux.org> - 2.11.2-1
- update to 2.11.2 rhbz#2278847

* Tue Apr 30 2024 Jonathan Wright <jonathan@almalinux.org> - 2.11.0-1
- update to 2.11.0 rhbz#2275393

* Fri Apr 26 2024 Felix Wang <topazus@outlook.com> - 2.9.1-3
- Use yyjson system dependency

* Sat Apr 13 2024 Jonathan Wright <jonathan@almalinux.org> - 2.9.1-2
- swap pciutils to hwdata per upstream

* Sat Apr 13 2024 Jonathan Wright <jonathan@almalinux.org> - 2.9.1-1
- update to 2.9.1 rhbz#2273299

* Tue Mar 26 2024 Jonathan Wright <jonathan@almalinux.org> - 2.8.10-1
- update to 2.8.10 rhbz#2266773

* Tue Feb 27 2024 Jonathan Wright <jonathan@almalinux.org> - 2.8.5-1
- update to 2.8.5 rhbz#2263621

* Thu Feb 01 2024 jonathanspw <jonathan@almalinux.org> - 2.7.1-1
- Update to 2.7.1 rhbz#2260426

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Jonathan Wright <jonathan@almalinux.org> - 2.6.3-1
- Update to 2.6.3 rhbz#2256373

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jan 04 2024 Onuralp Sezer <thunderbirdtr@fedoraproject.org> - 2.5.0-1
- update to 2.5.0 rhbz#2256373

* Mon Dec 18 2023 Jonathan Wright <jonathan@almalinux.org> - 2.4.0-1
- update to 2.4.0 rhbz#2255169

* Thu Dec 14 2023 Jonathan Wright <jonathan@almalinux.org> - 2.3.4-1
- Update to 2.3.4 rhbz#2253586 rhbz#2253389

* Wed Dec 06 2023 Jonathan Wright <jonathan@almalinux.org> - 2.3.3-1
- Update to 2.3.3 rhbz#2253389

* Wed Dec 06 2023 Jonathan Wright <jonathan@almalinux.org> - 2.3.2-1
- Update to 2.3.2 rhbz#2253219
- Add fish completions and new optional deps rhbz#2252977

* Wed Nov 08 2023 Jonathan Wright <jonathan@almalinux.org> - 2.2.3-1
- Update to 2.2.3 rhbz#2248630

* Thu Nov 02 2023 Jonathan Wright <jonathan@almalinux.org> - 2.2.1-1
- Update to 2.2.1 rhbz#2247683

* Tue Oct 17 2023 Jonathan Wright <jonathan@almalinux.org> - 2.1.2-1
- Update to 2.1.2 rhbz#2244539

* Sat Oct 14 2023 Jonathan Wright <jonathan@almalinux.org> - 2.1.1-1
- Update to 2.1.1 rhbz#2235036

* Sun Aug 27 2023 Jonathan Wright <jonathan@almalinux.org> - 2.0.5-1
- Update to 2.0.5 rhbz#2235036
- Add new optional dependency rhbz#2235137

* Tue Aug 22 2023 Jonathan Wright <jonathan@almalinux.org> - 2.0.2-1
- Update to 2.0.2 rhbz#2232058

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jul 05 2023 Jonathan Wright <jonathan@almalinux.org> - 1.12.2-1
- Update to 1.12.2 rhbz#2219791

* Mon Jul 03 2023 Jonathan Wright <jonathan@almalinux.org> - 1.12.1-1
- Update to 1.12.1 rhbz#2219147

* Mon Jun 26 2023 Jonathan Wright <jonathan@almalinux.org> - 1.11.3-1
- Update to 1.11.3 rhbz#2210504

* Sat Mar 25 2023 Jonathan Wright <jonathan@almalinux.org> - 1.11.0-1
- Update to 1.11.0 rhbz#2181737

* Thu Mar 02 2023 Jonathan Wright <jonathan@almalinux.org> - 1.10.3-1
- Update to 1.10.3 rhbz#2173294

* Wed Feb 22 2023 Jonathan Wright <jonathan@almalinux.org> - 1.10.2-1
- Update to 1.10.2 rhbz#2172629

* Wed Jan 25 2023 Jonathan Wright <jonathan@almalinux.org> - 1.9.1-1
- Update to 1.9.1 rhbz#2163335

* Mon Jan 23 2023 Jonathan Wright <jonathan@almalinux.org> - 1.9.0-1
- Update to 1.9.0 rhbz#2163335

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Jan 02 2023 Jonathan Wright <jonathan@almalinux.org> - 1.8.2-1
- Update to 1.8.2 rhbz#2156978

* Tue Oct 11 2022 Jonathan Wright <jonathan@almalinux.org> - 1.7.5-1
- Update to 1.7.5 rhbz#2133467

* Fri Sep 16 2022 Jonathan Wright <jonathan@almalinux.org> - 1.7.2-1
- Update to 1.7.2 rhbz#2127329

* Wed Sep 07 2022 Jonathan Wright <jonathan@almalinux.org> - 1.7.0-1
- Update to 1.7.0
- rhbz#2124866

* Tue Aug 23 2022 Jonathan Wright <jonathan@almalinux.org> - 1.6.5-1
- Update to 1.6.5
- rhbz#2120472
- Fix typo in first changelog citing "khbz" instead of "rhbz"

* Mon Aug 22 2022 Jonathan Wright <jonathan@almalinux.org> - 1.6.4-3
- Compile with rpm support for listing package counts

* Mon Aug 22 2022 Jonathan Wright <jonathan@almalinux.org> - 1.6.4-2
- Fix spec for EPEL8 builds

* Tue Aug 16 2022 Jonathan Wright <jonathan@almalinux.org> - 1.6.4-1
- Initial package build
- rhbz#2118887
