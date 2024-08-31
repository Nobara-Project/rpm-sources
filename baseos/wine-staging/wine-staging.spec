%global _default_patch_fuzz 2
# How to do version updates:
# bump one or more of the 3 defines below
# osc service localrun download_files
#	to download the tarballs.
# rm the old tarballs and signature
# osc addremove
# osc ci
# check buildresult after a while

%define _lto_cflags %{nil}
%define realver     9.16
%define stagingver  9.16
%define packagever  9.16

%global flavor %nil
%global build_type_safety_c 0

# defaults ..
%define pkg 		wine-staging
%define compat_package	winehq-staging
%define _prefix 	/opt/wine-staging
%define ver		%packagever

%define lib_major       1
%define lib_name        lib%{pkg}1
%define lib_name_devel  lib%{pkg}-devel
%undefine _hardened_build



Name:       %pkg
Version:    %ver
Release:    15
Epoch:      2
Summary:    WINE Is Not An Emulator - runs MS Windows programs
License:    LGPLv2+
Group:      Emulators
URL:        https://www.winehq.org/

%define wine    %{name}

%define mark64  ()(64bit)


Source0:	https://dl.winehq.org/wine/source/9.x/wine-%{realver}.tar.xz
Source1:	https://dl.winehq.org/wine/source/9.x/wine-%{realver}.tar.xz.sign

Source100:	https://github.com/wine-staging/wine-staging/archive/v%{realver}.tar.gz#/wine-staging-%{stagingver}.tar.xz

# Alexandres key
Source99:	wine.keyring

BuildRequires:  mingw32-gcc
BuildRequires:  mingw64-gcc
BuildRequires:  SDL2-devel
BuildRequires:  gcc
BuildRequires:  make
# BuildRequires:  openal-soft-devel
BuildRequires:  opencl-headers
BuildRequires:  ocl-icd-devel
BuildRequires:  pcsc-lite-devel
# BuildRequires:  libFAudio-devel
# BuildRequires:  libvkd3d-devel
# BuildRequires:  libvkd3d-shader-devel
# BuildRequires:  jxrlib-devel
BuildRequires:  samba-devel
BuildRequires:  libnetapi-devel
BuildRequires: libgcrypt-devel
BuildRequires:  icoutils
BuildRequires:  vulkan-devel
# BuildRequires:  lcms2-devel
BuildRequires:  gstreamer1-devel
BuildRequires:  gstreamer1-plugins-base-devel
# BuildRequires:  libmpg123-devel
BuildRequires:  gtk3-devel
BuildRequires:  libva-devel
BuildRequires:  fontforge
BuildRequires:  fontpackages-devel
# BuildRequires:  gsm-devel
# BuildRequires:  libjpeg-turbo-devel
BuildRequires:  libudev-devel
BuildRequires:  libv4l-devel
BuildRequires:  pulseaudio-libs-devel
BuildRequires:  lzma
BuildRequires:  audiofile-devel
BuildRequires:  giflib-devel
BuildRequires:  ImageMagick-devel
BuildRequires:  libpcap-devel
BuildRequires:  libXxf86dga-devel
BuildRequires:  mesa-libOSMesa-devel
BuildRequires:  libgphoto2-devel
BuildRequires:  libusb1-devel
BuildRequires:  alsa-lib-devel
BuildRequires:  autoconf
BuildRequires:  bison
BuildRequires:  coreutils
BuildRequires:  cups-devel
BuildRequires:  dbus-devel
BuildRequires:  desktop-file-utils
BuildRequires:  flex
BuildRequires:  fontconfig-devel
BuildRequires:  freetype-devel
BuildRequires:  freeglut-devel
BuildRequires:  gawk
BuildRequires:  xz
BuildRequires:  gettext-devel
BuildRequires:  gnutls-devel
BuildRequires:  krb5-devel
BuildRequires:  libattr-devel
BuildRequires:  libieee1284-devel
# BuildRequires:  libpng-devel
BuildRequires:  librsvg2
BuildRequires:  librsvg2-devel
BuildRequires:  libstdc++-devel
# BuildRequires:  libtiff-devel
BuildRequires:  libX11-devel
BuildRequires:  libXcomposite-devel
BuildRequires:  libXcursor-devel
BuildRequires:  libXext-devel
BuildRequires:  libXi-devel
BuildRequires:  libXinerama-devel
BuildRequires:  libxkbcommon-devel
# BuildRequires:  libxml2-devel
BuildRequires:  libXmu-devel
BuildRequires:  libXrandr-devel
BuildRequires:  libXrender-devel
# BuildRequires:  libxslt-devel
BuildRequires:  libXxf86vm-devel
BuildRequires:  mesa-libGL-devel
BuildRequires:  mesa-libGLU-devel
BuildRequires:  ncurses-devel
# BuildRequires:  openldap-devel
BuildRequires:  sane-backends-devel
BuildRequires:  unixODBC-devel
BuildRequires:  unzip
BuildRequires:  util-linux
# BuildRequires:  zlib-devel

Summary:    WINE Is Not An Emulator - runs MS Windows programs
Group:      Emulators
Provides:  %{name}
Provides:  %{name}64
Obsoletes:  %{name}64
Provides:  %{name}-common
Provides:   %{lib_name} = %{epoch}:%{version}-%{release}
Obsoletes:  %{lib_name} <= %{epoch}:%{version}-%{release}
Provides:   %{name}-bin = %{epoch}:%{version}-%{release}


%define dlopenreq() %(F=/usr/%{_lib}/lib%{1}.so;[ -e $F ] && (file $F|grep -q ASCII && grep -o 'lib[^ ]*' $F|sed -e "s/\$/%{mark64}/"||objdump -p $F | grep SONAME | awk '{ print $2 "%{mark64}" }') || echo "wine-missing-buildrequires-on-%{1}")
Requires:   %dlopenreq asound
Requires:   %dlopenreq attr
Requires:   %dlopenreq cups
Requires:   %dlopenreq dbus-1
Requires:   %dlopenreq fontconfig
Requires:   %dlopenreq freetype
Requires:   %dlopenreq gnutls
# Requires:   %dlopenreq gsm
# Requires:   %dlopenreq jpeg
Requires:   %dlopenreq krb5
Requires:   %dlopenreq ncurses
Requires:   %dlopenreq odbc
Requires:   %dlopenreq OSMesa
# Requires:   %dlopenreq png
Requires:   %dlopenreq sane
Requires:   %dlopenreq SDL2
# Requires:   %dlopenreq tiff
Requires:   %dlopenreq v4l1
Requires:   %dlopenreq vulkan
Requires:   %dlopenreq Xcomposite
Requires:   %dlopenreq Xcursor
Requires:   %dlopenreq Xi
Requires:   %dlopenreq Xinerama
Requires:   %dlopenreq Xrandr
Requires:   %dlopenreq Xrender
# Requires:   %dlopenreq xslt
Requires:   %dlopenreq Xxf86vm
%if 0%{?fedora_version}
Suggests:   sane-frontends
%endif
Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils

%define desc Wine is a program which allows running Microsoft Windows programs \
(including DOS, Windows 3.x and Win32 executables) on Unix. It \
consists of a program loader which loads and executes a Microsoft \
Windows binary, and a library (called Winelib) that implements Windows \
API calls using their Unix or X11 equivalents.  The library may also \
be used for porting Win32 code into native Unix executables.

%description
%desc

%description -n %{wine}
%desc

%package -n %{wine}-devel
Summary:    Static libraries and headers for %{name} (64-bit)
Group:      Development/C
Requires:   %{wine} = %{epoch}:%{version}-%{release}
Obsoletes:  %{name}64-devel
Provides:   %{lib_name_devel} = %{epoch}:%{version}-%{release}
Obsoletes:  %{lib_name_devel} <= %{epoch}:%{version}-%{release}
%description -n %{wine}-devel
Wine is a program which allows running Microsoft Windows programs
(including DOS, Windows 3.x and Win32 executables) on Unix.

This package contains the libraries and header files needed to
develop programs which make use of Wine.

%package -n %compat_package
Summary:    WINE Is Not An Emulator - runs MS Windows programs
Group:      Emulators
Requires:   %{wine} = %{epoch}:%{version}-%{release}
Conflicts:  wine wine64 wine-core wine-common wine-desktop wine-devel

%description -n %compat_package
Wine is a program which allows running Microsoft Windows programs
(including DOS, Windows 3.x and Win32 executables) on Unix.

This compatibility package allows to use %{wine} system-wide as
the default Wine version.

%prep
# unpack tarball SOURCE0
%setup -n wine-%realver  -q -T -b0

# apply wine staging patch set on top of the wine release.
tar xf %{SOURCE100}
./wine-staging-%{stagingver}/staging/patchinstall.py --all -W shell32-IconCache -W server-Stored_ACLs

%build
%define debug_package %{nil}
export CFLAGS="$(echo "%{optflags}" | sed -e 's/-O2//' -e 's/-Wp,-D_FORTIFY_SOURCE=2//' -e 's/-fcf-protection//' -e 's/-fstack-protector-strong//' -e 's/-fstack-clash-protection//') -O2"
autoreconf -i -f
%configure \
    --with-gstreamer \
    --disable-tests \
    --with-xattr \
    --enable-archs=i386,x86_64 \
    --with-x

make -j4

%install
%makeinstall LDCONFIG=/bin/true

# Compat symlinks for bindir
mkdir -p "%{buildroot}/usr/bin"
for _file in $(ls "%{buildroot}/%{_bindir}"); do \
    ln -s "%{_bindir}/$_file" "%{buildroot}/usr/bin/$_file"; \
done

# Compat symlinks for desktop file
mkdir -p "%{buildroot}/usr/share/applications"
for _file in $(ls "%{buildroot}/%{_datadir}/applications"); do \
    ln -s "%{_datadir}/applications/$_file" "%{buildroot}/usr/share/applications/$_file"; \
done

# Compat manpages
%if  0%{?fedora_version} || 0%{?scientificlinux_version} || 0%{?centos_version} >= 700 || 0%{?rhel_version} >= 700
for _dir in man1 de.UTF-8/man1 fr.UTF-8/man1 pl.UTF-8/man1; do \
	if [ -d "%{buildroot}/%{_mandir}/$_dir" ]; then \
        mkdir -p "$(dirname "%{buildroot}/usr/share/man/$_dir")"; \
		cp -pr "%{buildroot}/%{_mandir}/$_dir" "%{buildroot}/usr/share/man/$_dir"; \
	else \
		mkdir -p "%{buildroot}/usr/share/man/$_dir"; \
	fi; \
done
%else
for _dir in man1 de.UTF-8/man1 fr.UTF-8/man1 pl.UTF-8/man1; do \
        mkdir -p "%{buildroot}/usr/share/man/$_dir"; \
done
%endif

install -p -m 0644 loader/wine.man          "%{buildroot}/usr/share/man/man1/wine.1"
install -p -m 0644 loader/wine.de.UTF-8.man "%{buildroot}/usr/share/man/de.UTF-8/man1/wine.1"
install -p -m 0644 loader/wine.fr.UTF-8.man "%{buildroot}/usr/share/man/fr.UTF-8/man1/wine.1"
install -p -m 0644 loader/wine.pl.UTF-8.man "%{buildroot}/usr/share/man/pl.UTF-8/man1/wine.1"


%files -n %{wine}
%doc ANNOUNCE.md AUTHORS README.md

%{_bindir}/function_grep.pl
%{_bindir}/msidb
%{_bindir}/msiexec
%{_bindir}/notepad
%{_bindir}/regedit
%{_bindir}/regsvr32
%{_bindir}/widl
%{_bindir}/wineboot
%{_bindir}/winebuild
%{_bindir}/winecfg
%{_bindir}/wineconsole*
%{_bindir}/winecpp
%{_bindir}/winedbg
%{_bindir}/winedump
%{_bindir}/winefile
%{_bindir}/wineg++
%{_bindir}/winegcc
%{_bindir}/winemaker
%{_bindir}/winemine
%{_bindir}/winepath
%{_bindir}/wineserver
%{_bindir}/wmc
%{_bindir}/wrc
%lang(de) %{_mandir}/de.UTF-8/man?/winemaker.?*
%lang(de) %{_mandir}/de.UTF-8/man?/wineserver.?*
%lang(fr) %{_mandir}/fr.UTF-8/man?/winemaker.?*
%lang(fr) %{_mandir}/fr.UTF-8/man?/wineserver.?*
%{_mandir}/man?/widl.1*
%{_mandir}/man?/winebuild.1*
%{_mandir}/man?/winecpp.1*
%{_mandir}/man?/winedbg.1*
%{_mandir}/man?/winedump.1*
%{_mandir}/man?/wineg++.1*
%{_mandir}/man?/winegcc.1*
%{_mandir}/man?/winemaker.1*
%{_mandir}/man?/wmc.1*
%{_mandir}/man?/wrc.1*
%{_mandir}/man?/msiexec.?*
%{_mandir}/man?/notepad.?*
%{_mandir}/man?/regedit.?*
%{_mandir}/man?/regsvr32.?*
%{_mandir}/man?/wineboot.?*
%{_mandir}/man?/winecfg.?*
%{_mandir}/man?/wineconsole.?*
%{_mandir}/man?/winefile.?*
%{_mandir}/man?/winemine.?*
%{_mandir}/man?/winepath.?*
%{_mandir}/man?/wineserver.?*
%dir %{_datadir}/wine
%{_datadir}/wine/wine.inf
%{_datadir}/wine/nls/*.nls
%{_datadir}/applications/*.desktop
%dir %{_datadir}/wine/fonts
%{_datadir}/wine/fonts/*
# %{_datadir}/wine/color/*

%{_bindir}/wine
%{_bindir}/wine-preloader
%{_mandir}/man?/wine.?*
%lang(de) %{_mandir}/de.UTF-8/man?/wine.?*
%lang(fr) %{_mandir}/fr.UTF-8/man?/wine.?*
%lang(pl) %{_mandir}/pl.UTF-8/man?/wine.?*


%{_libdir}/wine/i386-windows/*.*
%{_libdir}/wine/x86_64-unix/*.*
%{_libdir}/wine/x86_64-windows/*.*

%files -n %{wine}-devel
%{_includedir}/*

%files -n %compat_package
/usr/bin/*
/usr/share/applications/*.desktop
/usr/share/man/man?/*
%lang(de) /usr/share/man/de.UTF-8/man?/*
%lang(fr) /usr/share/man/fr.UTF-8/man?/*
%lang(pl) /usr/share/man/pl.UTF-8/man?/*
