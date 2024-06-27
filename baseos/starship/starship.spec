%global debug_package %{nil}
%undefine _package_note_file

Name: starship
Version: 1.19.0
Release: 2%{?dist}
Summary: â˜„ðŸŒŒï¸� The minimal, blazing-fast, and infinitely customizable prompt for any shell!

License: ISC
URL: https://github.com/starship/starship
Source0: %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
Source1: starship.toml

BuildRequires: cargo >= 1.74
BuildRequires: cmake3
BuildRequires: gcc
BuildRequires: rust >= 1.74

BuildRequires: pkgconfig(openssl)
BuildRequires: pkgconfig(zlib)
Requires:      nerd-fonts

%description
The minimal, blazing-fast, and infinitely customizable prompt for any shell!

  - Fast: it's fast â€“ really really fast! ðŸš€
  - Customizable: configure every aspect of your prompt.
  - Universal: works on any shell, on any operating system.
  - Intelligent: shows relevant information at a glance.
  - Feature rich: support for all your favorite tools.
  - Easy: quick to install â€“ start using it in minutes.


%prep
%autosetup


%install
export CARGO_PROFILE_RELEASE_BUILD_OVERRIDE_OPT_LEVEL=3
export CMAKE=cmake3
RUSTFLAGS='-C strip=symbols' cargo install --root=%{buildroot}%{_prefix} --path=.
rm -f %{buildroot}%{_prefix}/.crates.toml \
    %{buildroot}%{_prefix}/.crates2.json
mkdir -p %{buildroot}%{_datadir}/%{name}/
cp %{SOURCE1} %{buildroot}%{_datadir}/%{name}/


%files
%license LICENSE
%doc README.md CONTRIBUTING.md
%{_bindir}/%{name}
%{_datadir}/%{name}/starship.toml


%changelog
* Wed May 15 2024 Artem Polishchuk <ego.cordatus@gmail.com> - 1.19.0-1
- chore: Update to latest release

* Fri Mar 29 2024 Artem Polishchuk <ego.cordatus@gmail.com> - 1.18.2-1
- chore: Update to latest release

* Thu Mar 21 2024 Artem Polishchuk <ego.cordatus@gmail.com> - 1.18.0-1
- chore: Update to latest release

* Tue Jan 02 2024 Artem Polishchuk <ego.cordatus@gmail.com> - 1.17.1-1
- chore: Update to latest release

* Thu Dec 28 2023 Artem Polishchuk <ego.cordatus@gmail.com> - 1.17.0-1
- chore: Update to latest release

* Sun Jul 30 2023 Artem Polishchuk <ego.cordatus@gmail.com> - 1.16.0-2
- build: Switch to native Fedora Rust toolchain for EPEL

* Sun Jul 30 2023 Artem Polishchuk <ego.cordatus@gmail.com> - 1.16.0-1
- chore(update): 1.16.0

* Tue Jun 06 2023 Artem Polishchuk <ego.cordatus@gmail.com> - 1.15.0-1
- chore(update): 1.15.0

* Wed Apr 12 2023 Artem Polishchuk <ego.cordatus@gmail.com> - 1.14.2-1
- chore(update): 1.14.2

* Tue Apr 11 2023 Artem Polishchuk <ego.cordatus@gmail.com> - 1.14.1-1
- chore(update): 1.14.1

* Wed Dec 14 2022 Artem Polishchuk <ego.cordatus@gmail.com> - 1.12.0-1
- chore(update): 1.12.0

* Sat Oct 15 2022 Artem Polishchuk <ego.cordatus@gmail.com> - 1.11.0-1
- chore(update): 1.11.0

* Thu Sep 08 2022 Artem Polishchuk <ego.cordatus@gmail.com> - 1.10.3-1
- chore(update): 1.10.3

* Fri Aug 19 2022 Artem Polishchuk <ego.cordatus@gmail.com> - 1.10.2-1
- chore(update): 1.10.2

* Tue Aug 16 2022 Artem Polishchuk <ego.cordatus@gmail.com> - 1.10.1-1
- chore(update): 1.10.1

* Tue Aug 16 2022 Artem Polishchuk <ego.cordatus@gmail.com> - 1.9.1-1
- chore(update): 1.9.1

* Tue Jun 21 2022 Artem Polishchuk <ego.cordatus@gmail.com> - 1.8.0-1
- chore(update): 1.8.0

* Thu May 26 2022 Artem Polishchuk <ego.cordatus@gmail.com> - 1.7.1-1
- chore(update): 1.7.1

* Tue May 24 2022 Artem Polishchuk <ego.cordatus@gmail.com> - 1.7.0-1
- chore(update): 1.7.0

* Tue Apr 26 2022 Artem Polishchuk <ego.cordatus@gmail.com> - 1.6.3-1
- chore(update): 1.6.3

* Fri Apr 15 2022 Artem Polishchuk <ego.cordatus@gmail.com> - 1.6.2-1
- chore(update): 1.6.2

* Fri Apr 15 2022 Artem Polishchuk <ego.cordatus@gmail.com> - 1.6.0-1
- chore(update): 1.6.0

* Fri Mar 25 2022 Artem Polishchuk <ego.cordatus@gmail.com> - 1.5.4-1
- chore(update): 1.5.4

* Thu Mar 10 2022 Artem Polishchuk <ego.cordatus@gmail.com> - 1.4.2-1
- chore(update): 1.4.2

* Thu Mar 10 2022 Artem Polishchuk <ego.cordatus@gmail.com> - 1.4.1-1
- chore(update): 1.4.1

* Wed Mar 09 2022 Artem Polishchuk <ego.cordatus@gmail.com> - 1.4.0-2
- chore(update): 1.4.0

* Tue Feb 08 2022 Artem Polishchuk <ego.cordatus@gmail.com> - 1.3.0-1
- chore(update): 1.3.0

* Sat Jan 15 2022 Artem Polishchuk <ego.cordatus@gmail.com> - 1.2.1-1
- chore(update): 1.2.1

* Fri Jan 14 2022 Artem Polishchuk <ego.cordatus@gmail.com> - 1.2.0-1
- chore(update): 1.2.0

* Wed Dec 22 2021 Artem Polishchuk <ego.cordatus@gmail.com> - 1.1.1-1
- chore(update): 1.1.1

* Wed Nov 10 2021 Artem Polishchuk <ego.cordatus@gmail.com> - 1.0.0-1
- chore(update): 1.0.0

* Tue Sep 21 2021 Artem Polishchuk <ego.cordatus@gmail.com> - 0.58.0-1
- build(update): 0.58.0

* Wed Jul 14 2021 Artem Polishchuk <ego.cordatus@gmail.com> - 0.56.0-1
- build(update): 0.56.0

* Mon Jun 21 2021 Artem Polishchuk <ego.cordatus@gmail.com> - 0.55.0-1
- build(update): 0.55.0

* Sat May 15 2021 Artem Polishchuk <ego.cordatus@gmail.com> - 0.54.0-1
- build(update): 0.54.0

* Sat May 01 2021 Artem Polishchuk <ego.cordatus@gmail.com> - 0.53.0-1
- build(update): 0.53.0

* Thu Apr 22 2021 Artem Polishchuk <ego.cordatus@gmail.com> - 0.52.1-1
- build(update): 0.52.1

* Tue Mar 23 2021 Artem Polishchuk <ego.cordatus@gmail.com> - 0.51.0-1
- build(update): 0.51.0

* Wed Feb 03 2021 Artem Polishchuk <ego.cordatus@gmail.com> - 0.50.0-1
- build(update): 0.50.0

* Fri Jan 29 2021 Artem Polishchuk <ego.cordatus@gmail.com> - 0.49.0-1
- build(update): 0.49.0

* Sat Jan  2 2021 Artem Polishchuk <ego.cordatus@gmail.com> - 0.48.0-1
- build(update): 0.48.0

* Sun Nov 15 2020 Artem Polishchuk <ego.cordatus@gmail.com> - 0.47.0-1
- build(update): 0.47.0

* Wed Oct 14 2020 Artem Polishchuk <ego.cordatus@gmail.com> - 0.46.2-1
- build(update): 0.46.2

* Thu Oct  8 2020 Artem Polishchuk <ego.cordatus@gmail.com> - 0.46.0-1
- build(update): 0.46.0

* Thu Oct  1 2020 Artem Polishchuk <ego.cordatus@gmail.com> - 0.45.2-1
- Update to 0.45.2

* Wed Sep 30 2020 Artem Polishchuk <ego.cordatus@gmail.com> - 0.45.1-1
- Update to 0.45.1

* Tue Sep 29 2020 Artem Polishchuk <ego.cordatus@gmail.com> - 0.45.0-1
- Update to 0.45.0

* Mon Jul 06 2020 Artem Polishchuk <ego.cordatus@gmail.com> - 0.44.0-1
- Update to 0.44.0

* Fri Jun 26 2020 Artem Polishchuk <ego.cordatus@gmail.com> - 0.43.0-1
- Update to 0.43.0

* Tue Jun 09 2020 Artem Polishchuk <ego.cordatus@gmail.com> - 0.42.0-1
- Update to 0.42.0

* Fri May 15 2020 Artem Polishchuk <ego.cordatus@gmail.com> - 0.41.3-1
- Update to 0.41.3

* Fri May 15 2020 Artem Polishchuk <ego.cordatus@gmail.com> - 0.41.2-1
- Update to 0.41.2

* Thu May 14 2020 Artem Polishchuk <ego.cordatus@gmail.com> - 0.41.1-1
- Update to 0.41.1

* Tue Apr 28 2020 Artem Polishchuk <ego.cordatus@gmail.com> - 0.41.0-1
- Update to 0.41.0

* Sat Apr 11 2020 Artem Polishchuk <ego.cordatus@gmail.com> - 0.40.1-1
- Update to 0.40.1

* Sat Apr 11 2020 Artem Polishchuk <ego.cordatus@gmail.com> - 0.40.0-1
- Update to 0.40.0

* Mon Apr 06 2020 Artem Polishchuk <ego.cordatus@gmail.com> - 0.39.0-1
- Update to 0.39.0

* Mon Mar 23 2020 Artem Polishchuk <ego.cordatus@gmail.com> - 0.38.1-1
- Update to 0.38.1

* Fri Mar 20 2020 Artem Polishchuk <ego.cordatus@gmail.com> - 0.38.0-1
- Update to 0.38.0

* Thu Feb 06 2020 Artem Polishchuk <ego.cordatus@gmail.com> - 0.35.1-1
- Update to 0.35.1

* Fri Dec 20 2019 Artem Polishchuk <ego.cordatus@gmail.com> - 0.32.1-1
- Update to 0.32.1

* Fri Dec 20 2019 Artem Polishchuk <ego.cordatus@gmail.com> - 0.31.0-1
- Update to 0.31.0

* Wed Dec 18 2019 Artem Polishchuk <ego.cordatus@gmail.com> - 0.30.1-1
- Update to 0.30.1
- Note: starship packaged for official repos now and availabe in Rawhide at this moment

* Wed Dec 11 2019 Artem Polishchuk <ego.cordatus@gmail.com> - 0.29.0-1
- Update to 0.29.0

* Wed Dec 04 2019 Artem Polishchuk <ego.cordatus@gmail.com> - 0.27.0-1
- Update to 0.27.0

* Sat Nov 23 2019 Artem Polishchuk <ego.cordatus@gmail.com> - 0.26.4-1
- Initial package
