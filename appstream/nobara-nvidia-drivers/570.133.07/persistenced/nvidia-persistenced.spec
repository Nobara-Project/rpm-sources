
Name:           nvidia-persistenced
Version:        570.133.07
Release:        1%{?dist}
Summary:        A daemon to maintain persistent software state in the NVIDIA driver
Epoch:          3
License:        GPLv2+
URL:            http://www.nvidia.com/object/unix.html
ExclusiveArch:  x86_64 aarch64

Source0:        https://download.nvidia.com/XFree86/%{name}/%{name}-%{version}.tar.bz2
Source1:        %{name}.service

BuildRequires:  gcc
BuildRequires:  libtirpc-devel
BuildRequires:  m4

# For Fedora systemd-rpm-macros would be enough:
BuildRequires:      systemd-devel
Requires(post):     systemd
Requires(preun):    systemd
Requires(postun):   systemd
Requires:           libnvidia-cfg%{?_isa} >= %{?epoch:%{epoch}:}%{version}

%description
The %{name} utility is used to enable persistent software state in the NVIDIA
driver. When persistence mode is enabled, the daemon prevents the driver from
releasing device state when the device is not in use. This can improve the
startup time of new clients in this scenario.

%prep
%autosetup
# Remove additional CFLAGS added when enabling DEBUG
sed -i -e '/+= -O0 -g/d' utils.mk

%build
export CFLAGS="%{optflags} -I%{_includedir}/tirpc"
make %{?_smp_mflags} \
    DEBUG=1 \
    LIBS="-ldl -ltirpc" \
    NV_VERBOSE=1 \
    PREFIX=%{_prefix} \
    STRIP_CMD=true

%install
%make_install \
    NV_VERBOSE=1 \
    PREFIX=%{_prefix} \
    STRIP_CMD=true

mkdir -p %{buildroot}%{_sharedstatedir}/%{name}

# Systemd unit files
install -p -m 644 -D %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files
%license COPYING
%{_mandir}/man1/%{name}.1.*
%{_bindir}/%{name}
%{_unitdir}/%{name}.service
%{_sharedstatedir}/%{name}

%changelog
* Wed Mar 19 2025 Simone Caronni <negativo17@gmail.com> - 3:570.133.07-1
- Update to 570.133.07.

* Mon Mar 10 2025 Simone Caronni <negativo17@gmail.com> - 3:570.124.04-2
- Move nvidia-persistenced binary to _bindir (as per original sources).

* Fri Feb 28 2025 Simone Caronni <negativo17@gmail.com> - 3:570.124.04-1
- Update to 570.124.04.

* Fri Jan 31 2025 Simone Caronni <negativo17@gmail.com> - 3:570.86.16-1
- Update to 570.86.16.

* Mon Jan 27 2025 Simone Caronni <negativo17@gmail.com> - 3:570.86.15-1
- Update to 570.86.15.

* Thu Dec 05 2024 Simone Caronni <negativo17@gmail.com> - 3:565.77-1
- Update to 565.77.

* Wed Oct 23 2024 Simone Caronni <negativo17@gmail.com> - 3:565.57.01-1
- Update to 565.57.01.

* Wed Aug 21 2024 Simone Caronni <negativo17@gmail.com> - 3:560.35.03-1
- Update to 560.35.03.

* Tue Aug 06 2024 Simone Caronni <negativo17@gmail.com> - 3:560.31.02-1
- Update to 560.31.02.

* Mon Aug 05 2024 Simone Caronni <negativo17@gmail.com> - 3:560.28.03-1
- Update to 560.28.03.

* Tue Jul 02 2024 Simone Caronni <negativo17@gmail.com> - 3:555.58.02-1
- Update to 555.58.02.
- Require dynamically loaded library libnvidia-cfg.

* Thu Jun 27 2024 Simone Caronni <negativo17@gmail.com> - 3:555.58-1
- Update to 555.58.

* Thu Jun 06 2024 Simone Caronni <negativo17@gmail.com> - 3:555.52.04-1
- Update to 555.52.04.

* Wed May 22 2024 Simone Caronni <negativo17@gmail.com> - 3:555.42.02-1
- Update to 555.42.02.

* Tue Apr 30 2024 Simone Caronni <negativo17@gmail.com> - 3:550.78-2
- Switch to Nvidia provided tarball.

* Fri Apr 26 2024 Simone Caronni <negativo17@gmail.com> - 3:550.78-1
- Update to 550.78.

* Thu Apr 18 2024 Simone Caronni <negativo17@gmail.com> - 3:550.76-1
- Update to 550.76.

* Sun Mar 24 2024 Simone Caronni <negativo17@gmail.com> - 3:550.67-1
- Update to 550.67.

* Mon Mar 18 2024 Simone Caronni <negativo17@gmail.com> - 3:550.54.14-4
- Clean up build requirements.

* Sat Mar 09 2024 Simone Caronni <negativo17@gmail.com> - 3:550.54.14-3
- Enable aarch64.

* Thu Mar 07 2024 Simone Caronni <negativo17@gmail.com> - 3:550.54.14-2
- Run nvidia-persistenced as root as Nvidia does.

* Sun Mar 03 2024 Simone Caronni <negativo17@gmail.com> - 3:550.54.14-1
- Update to 550.54.14.

* Tue Feb 06 2024 Simone Caronni <negativo17@gmail.com> - 3:550.40.07-1
- Update to 550.40.07.
