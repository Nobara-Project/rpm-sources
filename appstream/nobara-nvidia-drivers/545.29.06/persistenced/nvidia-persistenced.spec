Name:           nvidia-persistenced
Version:        545.29.06
Release:        5%{?dist}
Summary:        A daemon to maintain persistent software state in the NVIDIA driver
Epoch:          3
License:        GPLv2+
URL:            http://www.nvidia.com/object/unix.html
ExclusiveArch:  %{ix86} x86_64

Source0:        https://github.com/NVIDIA/%{name}/archive/refs/tags/%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        %{name}.service

BuildRequires:  gcc
BuildRequires:  libtirpc-devel
BuildRequires:  m4

# For Fedora systemd-rpm-macros would be enough:
BuildRequires:      systemd-devel
Requires(post):     systemd
Requires(preun):    systemd
Requires(postun):   systemd
Requires(pre):      shadow-utils
Requires:           nvidia-driver-cuda = %{?epoch}:%{version}

%description
The %{name} utility is used to enable persistent software state in the NVIDIA
driver. When persistence mode is enabled, the daemon prevents the driver from
releasing device state when the device is not in use. This can improve the
startup time of new clients in this scenario.

%prep
%setup -q
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

mv %{buildroot}%{_bindir} %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_sharedstatedir}/%{name}

# Systemd unit files
install -p -m 644 -D %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service

%pre
getent group %{name} >/dev/null || groupadd -r %{name}
getent passwd %{name} >/dev/null || \
    useradd -r -g %{name} -d /var/run/%{name} -s /sbin/nologin \
    -c "NVIDIA persistent software state" %{name}
exit 0

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files
%license COPYING
%{_mandir}/man1/%{name}.1.*
%{_sbindir}/%{name}
%{_unitdir}/%{name}.service
%attr(750,%{name},%{name}) %{_sharedstatedir}/%{name}

%changelog
* Tue Nov 29 2022 Simone Caronni <negativo17@gmail.com> - 3:525.60.11-1
- Update to 525.60.11.

* Thu Oct 13 2022 Simone Caronni <negativo17@gmail.com> - 3:520.56.06-1
- Update to 520.56.06.

* Wed Sep 21 2022 Simone Caronni <negativo17@gmail.com> - 3:515.76-1
- Update to 515.76.

* Mon Aug 08 2022 Simone Caronni <negativo17@gmail.com> - 3:515.65.01-1
- Update to 515.65.01.

* Wed Jun 29 2022 Simone Caronni <negativo17@gmail.com> - 3:515.57-1
- Update to 515.57.

* Wed Jun 01 2022 Simone Caronni <negativo17@gmail.com> - 3:515.48.07-1
- Update to 515.48.07.

* Thu May 12 2022 Simone Caronni <negativo17@gmail.com> - 3:515.43.04-1
- Update to 515.43.04.

* Mon May 02 2022 Simone Caronni <negativo17@gmail.com> - 3:510.68.02-1
- Update to 510.68.02.

* Mon Mar 28 2022 Simone Caronni <negativo17@gmail.com> - 3:510.60.02-1
- Update to 510.60.02.

* Mon Feb 14 2022 Simone Caronni <negativo17@gmail.com> - 3:510.54-1
- Update to 510.54.

* Wed Feb 02 2022 Simone Caronni <negativo17@gmail.com> - 3:510.47.03-1
- Update to 510.47.03.

* Tue Dec 14 2021 Simone Caronni <negativo17@gmail.com> - 3:495.46-1
- Update to 495.46.

* Tue Nov 02 2021 Simone Caronni <negativo17@gmail.com> - 3:495.44-1
- Update to 495.44.

* Tue Nov 02 2021 Simone Caronni <negativo17@gmail.com> - 3:470.82.00-1
- Update to 470.82.00.

* Tue Sep 21 2021 Simone Caronni <negativo17@gmail.com> - 3:470.74-1
- Update to 470.74.

* Wed Aug 11 2021 Simone Caronni <negativo17@gmail.com> - 3:470.63.01-1
- Update to 470.63.01.

* Tue Jul 20 2021 Simone Caronni <negativo17@gmail.com> - 3:470.57.02-1
- Update to 470.57.02.

* Wed Jun 30 2021 Simone Caronni <negativo17@gmail.com> - 3:470.42.01-1
- Update to 470.42.01.

* Wed May 26 2021 Simone Caronni <negativo17@gmail.com> - 3:465.31-1
- Update to 465.31.

* Sat May 01 2021 Simone Caronni <negativo17@gmail.com> - 3:465.27-1
- Update to 465.27.

* Sun Apr 18 2021 Simone Caronni <negativo17@gmail.com> - 3:465.24.02-1
- Update to 465.24.02.
- Switch to github sources.

* Fri Apr 09 2021 Simone Caronni <negativo17@gmail.com> - 3:465.19.01-1
- Update to 465.19.01.

* Fri Mar 19 2021 Simone Caronni <negativo17@gmail.com> - 3:460.67-1
- Update to 460.67.

* Mon Mar 01 2021 Simone Caronni <negativo17@gmail.com> - 3:460.56-1
- Update to 460.56.

* Wed Jan 27 2021 Simone Caronni <negativo17@gmail.com> - 3:460.39-1
- Update to 460.39.

* Thu Jan  7 2021 Simone Caronni <negativo17@gmail.com> - 3:460.32.03-1
- Update to 460.32.03.

* Sun Dec 20 2020 Simone Caronni <negativo17@gmail.com> - 3:460.27.04-1
- Update to 460.27.04.
- Trim changelog.

* Mon Dec 07 2020 Simone Caronni <negativo17@gmail.com> - 3:455.45.01-2
- Remove RHEL/CentOS 6 support.

* Wed Nov 18 2020 Simone Caronni <negativo17@gmail.com> - 3:455.45.01-1
- Update to 455.45.01.

* Mon Nov 02 2020 Simone Caronni <negativo17@gmail.com> - 3:455.38-1
- Update to 455.38.

* Mon Oct 12 2020 Simone Caronni <negativo17@gmail.com> - 3:455.28-1
- Update to 455.28.

* Tue Oct 06 2020 Simone Caronni <negativo17@gmail.com> - 3:450.80.02-1
- Update to 450.80.02.

* Thu Aug 20 2020 Simone Caronni <negativo17@gmail.com> - 3:450.66-1
- Update to 450.66.

* Fri Jul 10 2020 Simone Caronni <negativo17@gmail.com> - 3:450.57-1
- Update to 450.57.

* Thu Jun 25 2020 Simone Caronni <negativo17@gmail.com> - 3:440.100-1
- Update to 440.100.

* Tue Apr 14 2020 Simone Caronni <negativo17@gmail.com> - 3:440.82-2
- Update requirements according to package guidelines.

* Thu Apr 09 2020 Simone Caronni <negativo17@gmail.com> - 3:440.82-1
- Update to 440.82.

* Fri Feb 28 2020 Simone Caronni <negativo17@gmail.com> - 3:440.64-1
- Update to 440.64.

* Tue Feb 04 2020 Simone Caronni <negativo17@gmail.com> - 3:440.59-1
- Update to 440.59.

* Sat Dec 14 2019 Simone Caronni <negativo17@gmail.com> - 3:440.44-1
- Update to 440.44.

* Sat Nov 30 2019 Simone Caronni <negativo17@gmail.com> - 3:440.36-1
- Update to 440.36.

* Sat Nov 09 2019 Simone Caronni <negativo17@gmail.com> - 3:440.31-1
- Update to 440.31.

* Thu Oct 17 2019 Simone Caronni <negativo17@gmail.com> - 3:440.26-1
- Update to 440.26.

* Mon Sep 02 2019 Simone Caronni <negativo17@gmail.com> - 3:435.21-1
- Update to 435.21.

* Thu Aug 22 2019 Simone Caronni <negativo17@gmail.com> - 3:435.17-1
- Update to 435.17.

* Wed Jul 31 2019 Simone Caronni <negativo17@gmail.com> - 3:430.40-1
- Update to 430.40.

* Fri Jul 12 2019 Simone Caronni <negativo17@gmail.com> - 3:430.34-1
- Update to 430.34.

* Wed Jun 12 2019 Simone Caronni <negativo17@gmail.com> - 3:430.26-1
- Update to 430.26.

* Sat May 18 2019 Simone Caronni <negativo17@gmail.com> - 3:430.14-1
- Update to 430.14.

* Thu May 09 2019 Simone Caronni <negativo17@gmail.com> - 3:418.74-1
- Update to 418.74.

* Sun Mar 24 2019 Simone Caronni <negativo17@gmail.com> - 3:418.56-1
- Update to 418.56.

* Fri Feb 22 2019 Simone Caronni <negativo17@gmail.com> - 3:418.43-1
- Update to 418.43.
- Trim changelog.

* Wed Feb 06 2019 Simone Caronni <negativo17@gmail.com> - 3:418.30-1
- Update to 418.30.

* Sun Feb 03 2019 Simone Caronni <negativo17@gmail.com> - 3:415.27-2
- Do not require nvidia-kmod-common, already required by nvidia-driver-cuda.

* Thu Jan 17 2019 Simone Caronni <negativo17@gmail.com> - 3:415.27-1
- Update to 415.27.
