Name:           nvidia-settings
Version:        565.77
Release:        4%{?dist}
Summary:        Configure the NVIDIA graphics driver
Epoch:          3
License:        GPLv2+
URL:            http://www.nvidia.com/object/unix.html
ExclusiveArch:  x86_64 aarch64

Source0:        https://download.nvidia.com/XFree86/%{name}/%{name}-%{version}.tar.bz2
Source1:        %{name}-load.desktop
Source2:        %{name}.appdata.xml
Patch0:         %{name}-desktop.patch
Patch1:         %{name}-lib-permissions.patch
Patch2:         %{name}-link-order.patch
Patch3:         %{name}-libXNVCtrl.patch
Patch4:         %{name}-ld-dep-remove.patch

BuildRequires:  desktop-file-utils
BuildRequires:  dbus-devel
BuildRequires:  gcc
BuildRequires:  jansson-devel
BuildRequires:  libappstream-glib
BuildRequires:  libvdpau-devel >= 1.0
BuildRequires:  libXxf86vm-devel
BuildRequires:  libXext-devel
BuildRequires:  libXrandr-devel
BuildRequires:  libXv-devel
BuildRequires:  m4
BuildRequires:  mesa-libEGL-devel
BuildRequires:  mesa-libGL-devel
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  vulkan-headers

Requires:       nvidia-libXNVCtrl%{?_isa} = %{?epoch}:%{version}-%{release}
Requires:       nvidia-driver%{?_isa} = %{?epoch}:%{version}
# Loaded at runtime
Requires:       libvdpau%{?_isa} >= 0.9

%description
The %{name} utility is a tool for configuring the NVIDIA graphics
driver. It operates by communicating with the NVIDIA X driver, querying and
updating state as appropriate.

This communication is done with the NV-CONTROL X extension.

%package -n nvidia-libXNVCtrl
Summary:        Library providing the NV-CONTROL API
Obsoletes:      libXNVCtrl < %{?epoch}:%{version}-%{release}
Provides:       libXNVCtrl = %{?epoch}:%{version}-%{release}

%description -n nvidia-libXNVCtrl
This library provides the NV-CONTROL API for communicating with the proprietary
NVidia xorg driver. It is required for proper operation of the %{name} utility.

%package -n nvidia-libXNVCtrl-devel
Summary:        Development files for libXNVCtrl
Requires:       nvidia-libXNVCtrl = %{?epoch}:%{version}-%{release}
Requires:       libX11-devel

%description -n nvidia-libXNVCtrl-devel
This devel package contains libraries and header files for
developing applications that use the NV-CONTROL API.

%prep
%autosetup -p1

# Remove bundled jansson
rm -fr src/jansson

# Remove additional CFLAGS added when enabling DEBUG
sed -i '/+= -O0 -g/d' utils.mk src/libXNVCtrl/utils.mk

# Change all occurrences of destinations in each utils.mk.
sed -i -e 's|$(PREFIX)/lib|$(PREFIX)/%{_lib}|g' utils.mk src/libXNVCtrl/utils.mk

%build
export CFLAGS="%{optflags} -fPIC"
export LDFLAGS="%{?__global_ldflags}"
make \
    DEBUG=1 \
    NV_USE_BUNDLED_LIBJANSSON=0 \
    NV_VERBOSE=1 \
    PREFIX=%{_prefix} \
    XNVCTRL_LDFLAGS="-L%{_libdir}"

%install
# Install libXNVCtrl headers
mkdir -p %{buildroot}%{_includedir}/NVCtrl
cp -af src/libXNVCtrl/*.h %{buildroot}%{_includedir}/NVCtrl/

# Install main program
%make_install \
    DEBUG=1 \
    NV_USE_BUNDLED_LIBJANSSON=0 \
    NV_VERBOSE=1 \
    PREFIX=%{_prefix}

# Install desktop file
mkdir -p %{buildroot}%{_datadir}/{applications,pixmaps}
desktop-file-install --dir %{buildroot}%{_datadir}/applications/ doc/%{name}.desktop
cp doc/%{name}.png %{buildroot}%{_datadir}/pixmaps/

# Install autostart file to load settings at login
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/xdg/autostart/%{name}-load.desktop

# install AppData and add modalias provides
mkdir -p %{buildroot}%{_metainfodir}/
install -p -m 0644 %{SOURCE2} %{buildroot}%{_metainfodir}/

%check
desktop-file-validate %{buildroot}/%{_datadir}/applications/%{name}.desktop
desktop-file-validate %{buildroot}%{_sysconfdir}/xdg/autostart/%{name}-load.desktop
appstream-util validate-relax --nonet %{buildroot}/%{_metainfodir}/%{name}.appdata.xml

%files
%{_bindir}/%{name}
%{_metainfodir}/%{name}.appdata.xml
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.png
%{_libdir}/libnvidia-gtk3.so.%{version}
%{_libdir}/libnvidia-wayland-client.so.%{version}
%{_mandir}/man1/%{name}.*
%{_sysconfdir}/xdg/autostart/%{name}-load.desktop

%files -n nvidia-libXNVCtrl
%license COPYING
%{_libdir}/libXNVCtrl.so.*

%files -n nvidia-libXNVCtrl-devel
%doc doc/NV-CONTROL-API.txt doc/FRAMELOCK.txt
%{_includedir}/NVCtrl
%{_libdir}/libXNVCtrl.so

%changelog
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

* Sat Mar 09 2024 Simone Caronni <negativo17@gmail.com> - 3:550.54.14-3
- Enable aarch64.

* Fri Mar 08 2024 Simone Caronni <negativo17@gmail.com> - 3:550.54.14-2
- Add missing patch.

* Sun Mar 03 2024 Simone Caronni <negativo17@gmail.com> - 3:550.54.14-1
- Update to 550.54.14.

* Tue Feb 06 2024 Simone Caronni <negativo17@gmail.com> - 3:550.40.07-1
- Update to 550.40.07.

* Fri Dec 01 2023 Simone Caronni <negativo17@gmail.com> - 3:545.29.06-1
- Update to 545.29.06.

* Tue Oct 31 2023 Simone Caronni <negativo17@gmail.com> - 3:545.29.02-1
- Update to 545.29.02.

* Wed Oct 18 2023 Simone Caronni <negativo17@gmail.com> - 3:545.23.06-1
- Update to 545.23.06.

* Fri Sep 22 2023 Simone Caronni <negativo17@gmail.com> - 3:535.113.01-1
- Update to 535.113.01.

* Thu Aug 24 2023 Simone Caronni <negativo17@gmail.com> - 3:535.104.05-1
- Update to 535.104.05.

* Wed Aug 09 2023 Simone Caronni <negativo17@gmail.com> - 3:535.98-1
- Update to 535.98.

* Wed Jul 19 2023 Simone Caronni <negativo17@gmail.com> - 3:535.86.05-1
- Update to 535.86.05.

* Thu Jun 15 2023 Simone Caronni <negativo17@gmail.com> - 3:535.54.03-1
- Update to 535.54.03.

* Tue Jun 13 2023 Simone Caronni <negativo17@gmail.com> - 3:535.43.02-1
- Update to 535.43.02.

* Fri Mar 24 2023 Simone Caronni <negativo17@gmail.com> - 3:530.41.03-1
- Update to 530.41.03.

* Wed Mar 08 2023 Simone Caronni <negativo17@gmail.com> - 3:530.30.02-1
- Update to 530.30.02.

* Fri Feb 10 2023 Simone Caronni <negativo17@gmail.com> - 3:525.89.02-1
- Update to 525.89.02.

* Fri Jan 20 2023 Simone Caronni <negativo17@gmail.com> - 3:525.85.05-1
- Update to 525.85.05.

* Mon Jan 09 2023 Simone Caronni <negativo17@gmail.com> - 3:525.78.01-1
- Update to 525.78.01.

* Tue Nov 29 2022 Simone Caronni <negativo17@gmail.com> - 3:525.60.11-1
- Update to 525.60.11.
- Finally drop gtk2.

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
- Update SPEC file.
- Update patches from upstream.

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
- Do not generate AppData on CentOS/RHEL 7.

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

* Thu Apr 09 2020 Simone Caronni <negativo17@gmail.com> - 3:440.82-1
- Update to 440.82.

* Sat Mar 14 2020 Simone Caronni <negativo17@gmail.com> - 3:440.64-2
- Add patch for GCC 10.

* Fri Feb 28 2020 Simone Caronni <negativo17@gmail.com> - 3:440.64-1
- Update to 440.64.

* Tue Feb 04 2020 Simone Caronni <negativo17@gmail.com> - 3:440.59-1
- Update to 440.59.

* Sat Dec 14 2019 Simone Caronni <negativo17@gmail.com> - 3:440.44-1
- Update to 440.44.

* Sat Nov 30 2019 Simone Caronni <negativo17@gmail.com> - 3:440.36-1
- Update to 440.36.

* Sun Nov 17 2019 Simone Caronni <negativo17@gmail.com> - 3:440.31-2
- Fix full libXNVCtrl libraries instead of symlinks in CentOS/RHEL 6/7.

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
- Update AppData installation.

* Fri Jul 12 2019 Simone Caronni <negativo17@gmail.com> - 3:430.34-1
- Update to 430.34.

* Tue Jun 18 2019 Simone Caronni <negativo17@gmail.com> - 3:430.26-3
- Fix rpm message when upgrading from Fedora's libXNVCtrl.

* Sun Jun 16 2019 Simone Caronni <negativo17@gmail.com> - 3:430.26-2
- Revert libXNVCtrl soname to libXNVCtrl.so.0.

* Wed Jun 12 2019 Simone Caronni <negativo17@gmail.com> - 3:430.26-1
- Update to 430.26.
- Update patches.
- Update SPEC file.

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

* Thu Jan 17 2019 Simone Caronni <negativo17@gmail.com> - 3:415.27-1
- Update to 415.27.
