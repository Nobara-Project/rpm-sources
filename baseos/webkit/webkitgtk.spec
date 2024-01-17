## START: Set by rpmautospec
## (rpmautospec version 0.3.5)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 2;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

## NOTE: Lots of files in various subdirectories have the same name (such as
## "LICENSE") so this short macro allows us to distinguish them by using their
## directory names (from the source tree) as prefixes for the files.
%global add_to_license_files() \
        mkdir -p _license_files ; \
        cp -p %1 _license_files/$(echo '%1' | sed -e 's!/!.!g')

# No libmanette in RHEL
%if !0%{?rhel}
%global with_gamepad 1
%endif

%global _lto_cflags %{nil}

# Build documentation by default (use `rpmbuild --without docs` to override it).
# This is used by Coverity. Coverity injects custom compiler warnings, but
# any warning during WebKit docs build is fatal!
%bcond_without docs

# https://fedoraproject.org/wiki/Changes/Remove_webkit2gtk-4.0_API_Version
# ELN (RHEL 10) no longer needs 4.0
%if %{undefined rhel} || 0%{?rhel} < 10
%bcond_without api40
%endif

Name:           webkitgtk
Version:        2.42.4
Release:        %autorelease
Summary:        GTK web content engine library

License:        LGPLv2
URL:            https://www.webkitgtk.org/
Source0:        https://webkitgtk.org/releases/webkitgtk-%{version}.tar.xz
Source1:        https://webkitgtk.org/releases/webkitgtk-%{version}.tar.xz.asc
# Use the keys from https://webkitgtk.org/verifying.html
# $ gpg --import aperez.key carlosgc.key
# $ gpg --export --export-options export-minimal D7FCF61CF9A2DEAB31D81BD3F3D322D0EC4582C3 5AA3BC334FD7E3369E7C77B291C559DBE4C9123B > webkitgtk-keys.gpg
Source2:        webkitgtk-keys.gpg

BuildRequires:  bison
BuildRequires:  bubblewrap
BuildRequires:  cmake
BuildRequires:  flex
BuildRequires:  gcc-c++
BuildRequires:  gettext
BuildRequires:  gi-docgen
BuildRequires:  git
BuildRequires:  gnupg2
BuildRequires:  gperf
BuildRequires:  hyphen-devel
BuildRequires:  libatomic
BuildRequires:  ninja-build
BuildRequires:  openssl-devel
BuildRequires:  perl(English)
BuildRequires:  perl(FindBin)
BuildRequires:  perl(JSON::PP)
BuildRequires:  python3
BuildRequires:  ruby
BuildRequires:  rubygems
BuildRequires:  rubygem-json
BuildRequires:  unifdef
BuildRequires:  xdg-dbus-proxy

BuildRequires:  pkgconfig(atspi-2)
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(enchant-2)
BuildRequires:  pkgconfig(epoxy)
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gobject-introspection-1.0)
BuildRequires:  pkgconfig(gstreamer-1.0)
BuildRequires:  pkgconfig(gstreamer-plugins-bad-1.0)
BuildRequires:  pkgconfig(gstreamer-plugins-base-1.0)
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(gtk4)
BuildRequires:  pkgconfig(harfbuzz)
BuildRequires:  pkgconfig(icu-uc)
BuildRequires:  pkgconfig(lcms2)
BuildRequires:  pkgconfig(libavif)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libgcrypt)
BuildRequires:  pkgconfig(libjpeg)
BuildRequires:  pkgconfig(libjxl)
BuildRequires:  pkgconfig(libnotify)
BuildRequires:  pkgconfig(libopenjp2)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(libseccomp)
BuildRequires:  pkgconfig(libsecret-1)
%if %{with api40}
BuildRequires:  pkgconfig(libsoup-2.4)
%endif
BuildRequires:  pkgconfig(libsoup-3.0)
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:  pkgconfig(libtasn1)
BuildRequires:  pkgconfig(libwebp)
BuildRequires:  pkgconfig(libwoff2dec)
BuildRequires:  pkgconfig(libxslt)
%if 0%{?with_gamepad}
BuildRequires:  pkgconfig(manette-0.2)
%endif
BuildRequires:  pkgconfig(sqlite3)
BuildRequires:  pkgconfig(upower-glib)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-egl)
BuildRequires:  pkgconfig(wayland-protocols)
BuildRequires:  pkgconfig(wayland-server)
BuildRequires:  pkgconfig(wpe-1.0)
BuildRequires:  pkgconfig(wpebackend-fdo-1.0)
BuildRequires:  pkgconfig(xt)

# Filter out provides for private libraries
%global __provides_exclude_from ^(%{_libdir}/webkit2gtk-4\\.0/.*\\.so|%{_libdir}/webkit2gtk-4\\.1/.*\\.so|%{_libdir}/webkitgtk-6\\.0/.*\\.so)$

%description
WebKitGTK is the port of the WebKit web rendering engine to the
GTK platform.

%package -n     webkitgtk6.0
Summary:        WebKitGTK for GTK 4
Requires:       javascriptcoregtk6.0%{?_isa} = %{version}-%{release}
Requires:       bubblewrap
Requires:       libGLES
Requires:       xdg-dbus-proxy
Recommends:     geoclue2
Recommends:     gstreamer1-plugins-bad-free
Recommends:     gstreamer1-plugins-good
Recommends:     xdg-desktop-portal-gtk
Provides:       bundled(angle)
Provides:       bundled(pdfjs)
Provides:       bundled(xdgmime)
Obsoletes:      webkit2gtk5.0 < %{version}-%{release}

%description -n webkitgtk6.0
WebKitGTK is the port of the WebKit web rendering engine to the
GTK platform. This package contains WebKitGTK for GTK 4.

%package -n     webkit2gtk4.1
Summary:        WebKitGTK for GTK 3 and libsoup 3
Requires:       javascriptcoregtk4.1%{?_isa} = %{version}-%{release}
Requires:       bubblewrap
Requires:       libGLES
Requires:       xdg-dbus-proxy
Recommends:     geoclue2
Recommends:     gstreamer1-plugins-bad-free
Recommends:     gstreamer1-plugins-good
Recommends:     xdg-desktop-portal-gtk
Provides:       bundled(angle)
Provides:       bundled(pdfjs)
Provides:       bundled(xdgmime)

%description -n webkit2gtk4.1
WebKitGTK is the port of the WebKit web rendering engine to the
GTK platform. This package contains WebKitGTK for GTK 3 and libsoup 3.

%if %{with api40}
%package -n     webkit2gtk4.0
Summary:        WebKitGTK for GTK 3 and libsoup 2
Requires:       javascriptcoregtk4.0%{?_isa} = %{version}-%{release}
Requires:       bubblewrap
Requires:       xdg-dbus-proxy
Recommends:     geoclue2
Recommends:     gstreamer1-plugins-bad-free
Recommends:     gstreamer1-plugins-good
Recommends:     xdg-desktop-portal-gtk
Provides:       bundled(angle)
Provides:       bundled(pdfjs)
Provides:       bundled(xdgmime)
Obsoletes:      webkitgtk4 < %{version}-%{release}
Provides:       webkitgtk4 = %{version}-%{release}
Obsoletes:      webkit2gtk3 < %{version}-%{release}
Provides:       webkit2gtk3 = %{version}-%{release}

%description -n webkit2gtk4.0
WebKitGTK is the port of the WebKit web rendering engine to the
GTK platform. This package contains WebKitGTK for GTK 3 and libsoup 2.
%endif

%package -n     webkitgtk6.0-devel
Summary:        Development files for webkitgtk6.0
Requires:       webkitgtk6.0%{?_isa} = %{version}-%{release}
Requires:       javascriptcoregtk6.0%{?_isa} = %{version}-%{release}
Requires:       javascriptcoregtk6.0-devel%{?_isa} = %{version}-%{release}
Obsoletes:      webkit2gtk5.0-devel < %{version}-%{release}

%description -n webkitgtk6.0-devel
The webkitgtk6.0-devel package contains libraries, build data, and header
files for developing applications that use webkitgtk6.0.

%package -n     webkit2gtk4.1-devel
Summary:        Development files for webkit2gtk4.1
Requires:       webkit2gtk4.1%{?_isa} = %{version}-%{release}
Requires:       javascriptcoregtk4.1%{?_isa} = %{version}-%{release}
Requires:       javascriptcoregtk4.1-devel%{?_isa} = %{version}-%{release}

%description -n webkit2gtk4.1-devel
The webkit2gtk4.1-devel package contains libraries, build data, and header
files for developing applications that use webkit2gtk4.1.

%if %{with api40}
%package -n     webkit2gtk4.0-devel
Summary:        Development files for webkit2gtk4.0
Requires:       webkit2gtk4.0%{?_isa} = %{version}-%{release}
Requires:       javascriptcoregtk4.0%{?_isa} = %{version}-%{release}
Requires:       javascriptcoregtk4.0-devel%{?_isa} = %{version}-%{release}
Obsoletes:      webkitgtk4-devel < %{version}-%{release}
Provides:       webkitgtk4-devel = %{version}-%{release}
Obsoletes:      webkit2gtk3-devel < %{version}-%{release}
Provides:       webkit2gtk3-devel = %{version}-%{release}

%description -n webkit2gtk4.0-devel
The webkit2gtk4.0-devel package contains libraries, build data, and header
files for developing applications that use webkit2gtk4.0.
%endif

%if %{with docs}
%package -n     webkitgtk6.0-doc
Summary:        Documentation files for webkit2gtk5.0
BuildArch:      noarch
Requires:       webkitgtk6.0 = %{version}-%{release}
Obsoletes:      webkit2gtk5.0-doc < %{version}-%{release}
Recommends:     gi-docgen-fonts

%description -n webkitgtk6.0-doc
This package contains developer documentation for webkitgtk6.0.

%package -n     webkit2gtk4.1-doc
Summary:        Documentation files for webkit2gtk4.1
BuildArch:      noarch
Requires:       webkit2gtk4.1 = %{version}-%{release}
Recommends:     gi-docgen-fonts

%description -n webkit2gtk4.1-doc
This package contains developer documentation for webkit2gtk4.1.

%if %{with api40}
%package -n     webkit2gtk4.0-doc
Summary:        Documentation files for webkit2gtk4.0
BuildArch:      noarch
Requires:       webkit2gtk4.0 = %{version}-%{release}
Obsoletes:      webkitgtk4-doc < %{version}-%{release}
Provides:       webkitgtk4-doc = %{version}-%{release}
Obsoletes:      webkit2gtk3-doc < %{version}-%{release}
Provides:       webkit2gtk3-doc = %{version}-%{release}
Recommends:     gi-docgen-fonts

%description -n webkit2gtk4.0-doc
This package contains developer documentation for webkit2gtk4.0.
%endif
%endif

%package -n     javascriptcoregtk6.0
Summary:        JavaScript engine from webkitgtk6.0
Obsoletes:      javascriptcoregtk5.0 < %{version}-%{release}

%description -n javascriptcoregtk6.0
This package contains the JavaScript engine from webkitgtk6.0.

%package -n     javascriptcoregtk4.1
Summary:        JavaScript engine from webkit2gtk4.1
Obsoletes:      webkit2gtk4.1-jsc < %{version}-%{release}

%description -n javascriptcoregtk4.1
This package contains the JavaScript engine from webkit2gtk4.1.

%if %{with api40}
%package -n     javascriptcoregtk4.0
Summary:        JavaScript engine from webkit2gtk4.0
Obsoletes:      webkitgtk4-jsc < %{version}-%{release}
Provides:       webkitgtk4-jsc = %{version}-%{release}
Obsoletes:      webkit2gtk3-jsc < %{version}-%{release}
Provides:       webkit2gtk3-jsc = %{version}-%{release}

%description -n javascriptcoregtk4.0
This package contains the JavaScript engine from webkit2gtk4.0.
%endif

%package -n     javascriptcoregtk6.0-devel
Summary:        Development files for JavaScript engine from webkitgtk6.0
Requires:       javascriptcoregtk6.0%{?_isa} = %{version}-%{release}
Obsoletes:      javascriptcoregtk5.0-devel < %{version}-%{release}

%description -n javascriptcoregtk6.0-devel
The javascriptcoregtk6.0-devel package contains libraries, build data, and header
files for developing applications that use JavaScript engine from webkitgtk-6.0.

%package -n     javascriptcoregtk4.1-devel
Summary:        Development files for JavaScript engine from webkit2gtk4.1
Requires:       javascriptcoregtk4.1%{?_isa} = %{version}-%{release}
Obsoletes:      webkit2gtk4.1-jsc-devel < %{version}-%{release}

%description -n javascriptcoregtk4.1-devel
The javascriptcoregtk4.1-devel package contains libraries, build data, and header
files for developing applications that use JavaScript engine from webkit2gtk-4.1.

%if %{with api40}
%package -n     javascriptcoregtk4.0-devel
Summary:        Development files for JavaScript engine from webkit2gtk4.0
Requires:       javascriptcoregtk4.0%{?_isa} = %{version}-%{release}
Obsoletes:      webkitgtk4-jsc-devel < %{version}-%{release}
Provides:       webkitgtk4-jsc-devel = %{version}-%{release}
Obsoletes:      webkit2gtk3-jsc-devel < %{version}-%{release}
Provides:       webkit2gtk3-jsc-devel = %{version}-%{release}

%description -n javascriptcoregtk4.0-devel
The javascriptcoregtk4.0-devel package contains libraries, build data, and header
files for developing applications that use JavaScript engine from webkit2gtk-4.0.
%endif

%prep
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%autosetup -p1 -n webkitgtk-%{version}

%build
# Increase the DIE limit so our debuginfo packages can be size-optimized.
# This previously decreased the size for x86_64 from ~5G to ~1.1G, but as of
# 2022 it's more like 850 MB -> 675 MB. This requires lots of RAM on the
# builders, so only do this for x86_64 and aarch64 to avoid overwhelming
# builders with less RAM.
# https://bugzilla.redhat.com/show_bug.cgi?id=1456261
%global _dwz_max_die_limit_x86_64 250000000
%global _dwz_max_die_limit_aarch64 250000000

# Require 32 GB of RAM per vCPU for debuginfo processing. 16 GB is not enough.
%global _find_debuginfo_opts %limit_build -m 32768

# Reduce debuginfo verbosity 32-bit builds to reduce memory consumption even more.
# https://bugs.webkit.org/show_bug.cgi?id=140176
# https://lists.fedoraproject.org/archives/list/devel@lists.fedoraproject.org/thread/I6IVNA52TXTBRQLKW45CJ5K4RA4WNGMI/
%ifarch %{ix86}
%global optflags %(echo %{optflags} | sed 's/-g /-g1 /')
%endif

# JIT is broken on ARM systems with new ARMv8.5 BTI extension at the moment
# Cf. https://bugzilla.redhat.com/show_bug.cgi?id=2130009
# Cf. https://bugs.webkit.org/show_bug.cgi?id=245697
# Disable BTI until this is fixed upstream.
%ifarch aarch64
%global optflags %(echo %{optflags} | sed 's/-mbranch-protection=standard /-mbranch-protection=pac-ret /')
%endif

%define _vpath_builddir %{_vendor}-%{_target_os}-build/webkitgtk-6.0
%cmake \
  -GNinja \
  -DPORT=GTK \
  -DCMAKE_BUILD_TYPE=Release \
  -DUSE_GTK4=ON \
%if %{without docs}
  -DENABLE_DOCUMENTATION=OFF \
%endif
%if !0%{?with_gamepad}
  -DENABLE_GAMEPAD=OFF \
%endif
%if 0%{?rhel}
%ifarch aarch64
  -DUSE_64KB_PAGE_BLOCK=ON \
%endif
%endif
  %{nil}

%define _vpath_builddir %{_vendor}-%{_target_os}-build/webkit2gtk-4.1
%cmake \
  -GNinja \
  -DPORT=GTK \
  -DCMAKE_BUILD_TYPE=Release \
  -DENABLE_WEBDRIVER=OFF \
%if %{without docs}
  -DENABLE_DOCUMENTATION=OFF \
%endif
%if !0%{?with_gamepad}
  -DENABLE_GAMEPAD=OFF \
%endif
%if 0%{?rhel}
%ifarch aarch64
  -DUSE_64KB_PAGE_BLOCK=ON \
%endif
%endif
  %{nil}

%if %{with api40}
%define _vpath_builddir %{_vendor}-%{_target_os}-build/webkit2gtk-4.0
%cmake \
  -GNinja \
  -DPORT=GTK \
  -DCMAKE_BUILD_TYPE=Release \
  -DUSE_SOUP2=ON \
  -DENABLE_WEBDRIVER=OFF \
%if %{without docs}
  -DENABLE_DOCUMENTATION=OFF \
%endif
%if !0%{?with_gamepad}
  -DENABLE_GAMEPAD=OFF \
%endif
%if 0%{?rhel}
%ifarch aarch64
  -DUSE_64KB_PAGE_BLOCK=ON \
%endif
%endif
  %{nil}
%endif

%define _vpath_builddir %{_vendor}-%{_target_os}-build/webkitgtk-6.0
export NINJA_STATUS="[1/3][%f/%t %es] "
%cmake_build %limit_build -m 3072

%define _vpath_builddir %{_vendor}-%{_target_os}-build/webkit2gtk-4.1
export NINJA_STATUS="[2/3][%f/%t %es] "
%cmake_build %limit_build -m 3072

%if %{with api40}
%define _vpath_builddir %{_vendor}-%{_target_os}-build/webkit2gtk-4.0
export NINJA_STATUS="[3/3][%f/%t %es] "
%cmake_build %limit_build -m 3072
%endif

%install
%define _vpath_builddir %{_vendor}-%{_target_os}-build/webkitgtk-6.0
%cmake_install

%define _vpath_builddir %{_vendor}-%{_target_os}-build/webkit2gtk-4.1
%cmake_install

%if %{with api40}
%define _vpath_builddir %{_vendor}-%{_target_os}-build/webkit2gtk-4.0
%cmake_install
%endif

%find_lang WebKitGTK-6.0
%find_lang WebKitGTK-4.1
%if %{with api40}
%find_lang WebKitGTK-4.0
%endif

# Finally, copy over and rename various files for %%license inclusion
%add_to_license_files Source/JavaScriptCore/COPYING.LIB
%add_to_license_files Source/ThirdParty/ANGLE/LICENSE
%add_to_license_files Source/ThirdParty/ANGLE/src/third_party/libXNVCtrl/LICENSE
%add_to_license_files Source/WebCore/LICENSE-APPLE
%add_to_license_files Source/WebCore/LICENSE-LGPL-2
%add_to_license_files Source/WebCore/LICENSE-LGPL-2.1
%add_to_license_files Source/WebInspectorUI/UserInterface/External/CodeMirror/LICENSE
%add_to_license_files Source/WebInspectorUI/UserInterface/External/Esprima/LICENSE
%add_to_license_files Source/WebInspectorUI/UserInterface/External/three.js/LICENSE
%add_to_license_files Source/WTF/icu/LICENSE
%add_to_license_files Source/WTF/wtf/dtoa/COPYING
%add_to_license_files Source/WTF/wtf/dtoa/LICENSE

%files -n webkitgtk6.0 -f WebKitGTK-6.0.lang
%license _license_files/*ThirdParty*
%license _license_files/*WebCore*
%license _license_files/*WebInspectorUI*
%license _license_files/*WTF*
%{_libdir}/libwebkitgtk-6.0.so.4*
%dir %{_libdir}/girepository-1.0
%{_libdir}/girepository-1.0/WebKit-6.0.typelib
%{_libdir}/girepository-1.0/WebKitWebProcessExtension-6.0.typelib
%{_libdir}/webkitgtk-6.0/
%{_libexecdir}/webkitgtk-6.0/
%exclude %{_libexecdir}/webkitgtk-6.0/MiniBrowser
%exclude %{_libexecdir}/webkitgtk-6.0/jsc
%{_bindir}/WebKitWebDriver

%files -n webkit2gtk4.1 -f WebKitGTK-4.1.lang
%license _license_files/*ThirdParty*
%license _license_files/*WebCore*
%license _license_files/*WebInspectorUI*
%license _license_files/*WTF*
%{_libdir}/libwebkit2gtk-4.1.so.0*
%dir %{_libdir}/girepository-1.0
%{_libdir}/girepository-1.0/WebKit2-4.1.typelib
%{_libdir}/girepository-1.0/WebKit2WebExtension-4.1.typelib
%{_libdir}/webkit2gtk-4.1/
%{_libexecdir}/webkit2gtk-4.1/
%exclude %{_libexecdir}/webkit2gtk-4.1/MiniBrowser
%exclude %{_libexecdir}/webkit2gtk-4.1/jsc

%if %{with api40}
%files -n webkit2gtk4.0 -f WebKitGTK-4.0.lang
%license _license_files/*ThirdParty*
%license _license_files/*WebCore*
%license _license_files/*WebInspectorUI*
%license _license_files/*WTF*
%{_libdir}/libwebkit2gtk-4.0.so.37*
%dir %{_libdir}/girepository-1.0
%{_libdir}/girepository-1.0/WebKit2-4.0.typelib
%{_libdir}/girepository-1.0/WebKit2WebExtension-4.0.typelib
%{_libdir}/webkit2gtk-4.0/
%{_libexecdir}/webkit2gtk-4.0/
%exclude %{_libexecdir}/webkit2gtk-4.0/MiniBrowser
%exclude %{_libexecdir}/webkit2gtk-4.0/jsc
%endif

%files -n webkitgtk6.0-devel
%{_libexecdir}/webkitgtk-6.0/MiniBrowser
%{_includedir}/webkitgtk-6.0/
%exclude %{_includedir}/webkitgtk-6.0/jsc
%{_libdir}/libwebkitgtk-6.0.so
%{_libdir}/pkgconfig/webkitgtk-6.0.pc
%{_libdir}/pkgconfig/webkitgtk-web-process-extension-6.0.pc
%dir %{_datadir}/gir-1.0
%{_datadir}/gir-1.0/WebKit-6.0.gir
%{_datadir}/gir-1.0/WebKitWebProcessExtension-6.0.gir

%files -n webkit2gtk4.1-devel
%{_libexecdir}/webkit2gtk-4.1/MiniBrowser
%{_includedir}/webkitgtk-4.1/
%exclude %{_includedir}/webkitgtk-4.1/JavaScriptCore
%exclude %{_includedir}/webkitgtk-4.1/jsc
%{_libdir}/libwebkit2gtk-4.1.so
%{_libdir}/pkgconfig/webkit2gtk-4.1.pc
%{_libdir}/pkgconfig/webkit2gtk-web-extension-4.1.pc
%dir %{_datadir}/gir-1.0
%{_datadir}/gir-1.0/WebKit2-4.1.gir
%{_datadir}/gir-1.0/WebKit2WebExtension-4.1.gir

%if %{with api40}
%files -n webkit2gtk4.0-devel
%{_libexecdir}/webkit2gtk-4.0/MiniBrowser
%{_includedir}/webkitgtk-4.0/
%exclude %{_includedir}/webkitgtk-4.0/JavaScriptCore
%exclude %{_includedir}/webkitgtk-4.0/jsc
%{_libdir}/libwebkit2gtk-4.0.so
%{_libdir}/pkgconfig/webkit2gtk-4.0.pc
%{_libdir}/pkgconfig/webkit2gtk-web-extension-4.0.pc
%dir %{_datadir}/gir-1.0
%{_datadir}/gir-1.0/WebKit2-4.0.gir
%{_datadir}/gir-1.0/WebKit2WebExtension-4.0.gir
%endif

%files -n javascriptcoregtk6.0
%license _license_files/*JavaScriptCore*
%{_libdir}/libjavascriptcoregtk-6.0.so.1*
%dir %{_libdir}/girepository-1.0
%{_libdir}/girepository-1.0/JavaScriptCore-6.0.typelib

%files -n javascriptcoregtk4.1
%license _license_files/*JavaScriptCore*
%{_libdir}/libjavascriptcoregtk-4.1.so.0*
%dir %{_libdir}/girepository-1.0
%{_libdir}/girepository-1.0/JavaScriptCore-4.1.typelib

%if %{with api40}
%files -n javascriptcoregtk4.0
%license _license_files/*JavaScriptCore*
%{_libdir}/libjavascriptcoregtk-4.0.so.18*
%dir %{_libdir}/girepository-1.0
%{_libdir}/girepository-1.0/JavaScriptCore-4.0.typelib
%endif

%files -n javascriptcoregtk6.0-devel
%{_libexecdir}/webkitgtk-6.0/jsc
%dir %{_includedir}/webkitgtk-6.0
%{_includedir}/webkitgtk-6.0/jsc/
%{_libdir}/libjavascriptcoregtk-6.0.so
%{_libdir}/pkgconfig/javascriptcoregtk-6.0.pc
%dir %{_datadir}/gir-1.0
%{_datadir}/gir-1.0/JavaScriptCore-6.0.gir

%files -n javascriptcoregtk4.1-devel
%{_libexecdir}/webkit2gtk-4.1/jsc
%dir %{_includedir}/webkitgtk-4.1
%{_includedir}/webkitgtk-4.1/JavaScriptCore/
%{_includedir}/webkitgtk-4.1/jsc/
%{_libdir}/libjavascriptcoregtk-4.1.so
%{_libdir}/pkgconfig/javascriptcoregtk-4.1.pc
%dir %{_datadir}/gir-1.0
%{_datadir}/gir-1.0/JavaScriptCore-4.1.gir

%if %{with api40}
%files -n javascriptcoregtk4.0-devel
%{_libexecdir}/webkit2gtk-4.0/jsc
%dir %{_includedir}/webkitgtk-4.0
%{_includedir}/webkitgtk-4.0/JavaScriptCore/
%{_includedir}/webkitgtk-4.0/jsc/
%{_libdir}/libjavascriptcoregtk-4.0.so
%{_libdir}/pkgconfig/javascriptcoregtk-4.0.pc
%dir %{_datadir}/gir-1.0
%{_datadir}/gir-1.0/JavaScriptCore-4.0.gir
%endif

%if %{with docs}
%files -n webkitgtk6.0-doc
%dir %{_datadir}/gtk-doc
%dir %{_datadir}/gtk-doc/html
%{_datadir}/gtk-doc/html/javascriptcoregtk-6.0/
%{_datadir}/gtk-doc/html/webkitgtk-6.0/
%{_datadir}/gtk-doc/html/webkitgtk-web-process-extension-6.0/

%files -n webkit2gtk4.1-doc
%dir %{_datadir}/gtk-doc
%dir %{_datadir}/gtk-doc/html
%{_datadir}/gtk-doc/html/javascriptcoregtk-4.1/
%{_datadir}/gtk-doc/html/webkit2gtk-4.1/
%{_datadir}/gtk-doc/html/webkit2gtk-web-extension-4.1/

%if %{with api40}
%files -n webkit2gtk4.0-doc
%dir %{_datadir}/gtk-doc
%dir %{_datadir}/gtk-doc/html
%{_datadir}/gtk-doc/html/javascriptcoregtk-4.0/
%{_datadir}/gtk-doc/html/webkit2gtk-4.0/
%{_datadir}/gtk-doc/html/webkit2gtk-web-extension-4.0/
%endif
%endif

%changelog
* Fri Dec 15 2023 Michael Catanzaro <mcatanzaro@redhat.com> - 2.42.4-1
- Update to 2.42.4

* Tue Dec 05 2023 Michael Catanzaro <mcatanzaro@redhat.com> - 2.42.3-1
- Update to 2.42.3

* Fri Nov 10 2023 Michael Catanzaro <mcatanzaro@redhat.com> - 2.42.2-1
- Update to 2.42.2

* Wed Sep 27 2023 Michael Catanzaro <mcatanzaro@redhat.com> - 2.42.1-1
- Update to 2.40.1 and fix GL dependencies

* Fri Sep 15 2023 Michael Catanzaro <mcatanzaro@redhat.com> - 2.42.0-1
- Update to WebKitGTK 2.42.0

* Fri Sep 08 2023 Michael Catanzaro <mcatanzaro@redhat.com> - 2.41.92-1
- Update to 2.41.92

* Sat Aug 19 2023 Michael Catanzaro <mcatanzaro@redhat.com> - 2.41.91-2
- Disable LTO again to fix build

* Sat Aug 19 2023 Michael Catanzaro <mcatanzaro@redhat.com> - 2.41.91-1
- Update to 2.41.91

* Fri Jul 21 2023 Adam Williamson <awilliam@redhat.com> - 2.41.6-4
- Backport PR #15929 to fix content not shown on llvmpipe

* Wed Jul 12 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 2.41.6-3
- Only BuildRequires libsoup-devel when building 4.0 API

* Tue Jul 11 2023 František Zatloukal <fzatlouk@redhat.com> - 2.41.6-2
- Rebuilt for ICU 73.2

* Wed Jul 05 2023 Michael Catanzaro <mcatanzaro@redhat.com> - 2.41.6-1
- Upgrade to 2.41.6

* Thu Jun 22 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 2.41.5-5
- Disable 4.0 API in RHEL 10 builds

* Wed Jun 21 2023 Michael Catanzaro <mcatanzaro@redhat.com> - 2.41.5-4
- Revert "Remove all RHEL-related conditionals"

* Sun Jun 18 2023 Sérgio M. Basto <sergio@serjux.com> - 2.41.5-3
- Mass rebuild for jpegxl-0.8.1

* Wed Jun 14 2023 Tomas Popela <tpopela@redhat.com> - 2.41.5-2
- Drop the unneeded BR on pcre

* Wed Jun 14 2023 Michael Catanzaro <mcatanzaro@redhat.com> - 2.41.5-1
- Upgrade to 2.41.5

* Tue Jun 13 2023 Michael Catanzaro <mcatanzaro@redhat.com> - 2.41.4-2
- Remove all RHEL-related conditionals

* Wed May 17 2023 Michael Catanzaro <mcatanzaro@redhat.com> - 2.41.4-1
- Upgrade to WebKitGTK 2.41.4

* Fri Apr 21 2023 Michael Catanzaro <mcatanzaro@redhat.com> - 2.41.3-1
- Upgrade to 2.41.3

* Mon Apr 17 2023 Michael Catanzaro <mcatanzaro@redhat.com> - 2.41.2-3
- Add patch to fix GPU permissions errors

* Mon Apr 17 2023 Michael Catanzaro <mcatanzaro@redhat.com> - 2.41.2-2
- Add patch to fix rendering errors

* Fri Apr 14 2023 Michael Catanzaro <mcatanzaro@redhat.com> - 2.41.2-1
- Upgrade to 2.41.2

* Fri Mar 31 2023 Michael Catanzaro <mcatanzaro@redhat.com> - 2.41.1-1
- Upgrade to 2.41.1

* Sat Mar 18 2023 Michael Catanzaro <mcatanzaro@redhat.com> - 2.40.0-3
- Explicitly specify some required build deps

* Fri Mar 17 2023 Michael Catanzaro <mcatanzaro@redhat.com> - 2.40.0-2
- Add user content manager patch and reenable LTO

* Fri Mar 17 2023 Michael Catanzaro <mcatanzaro@redhat.com> - 2.40.0-1
- Upgrade to 2.40.0

* Wed Mar 08 2023 Michael Catanzaro <mcatanzaro@redhat.com> - 2.39.91-1
- Upgrade to 2.39.91

* Tue Mar 07 2023 Eric Curtin <ecurtin@redhat.com> - 2.39.90-2
- Turn on mbranch-protection=pac-ret only, JIT is broken with BTI enabled

* Tue Feb 21 2023 Michael Catanzaro <mcatanzaro@redhat.com> - 2.39.90-1
- Upgrade to 2.39.90

* Tue Jan 31 2023 Michael Catanzaro <mcatanzaro@redhat.com> - 2.39.7-1
- Upgrade to WebKitGTK 2.39.7

* Sat Jan 28 2023 Kalev Lember <klember@redhat.com> - 2.39.5-3
- Revert "Disable debuginfo dwz optimization on ppc64le and s390x"

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.39.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jan 20 2023 Michael Catanzaro <mcatanzaro@redhat.com> - 2.39.5-1
- Upgrade to 2.39.5

* Fri Jan 20 2023 Kalev Lember <klember@redhat.com> - 2.39.4-4
- Re-enable full debuginfo on s390x again

* Fri Jan 20 2023 Kalev Lember <klember@redhat.com> - 2.39.4-3
- Disable debuginfo dwz optimization on ppc64le and s390x

* Fri Jan 20 2023 Kalev Lember <klember@redhat.com> - 2.39.4-2
- Increase dwz optimization DIE limit for aarch64

* Fri Jan 20 2023 Michael Catanzaro <mcatanzaro@redhat.com> - 2.39.4-1
- Revert "Upgrade to 2.39.5"

* Thu Jan 19 2023 Michael Catanzaro <mcatanzaro@redhat.com> - 2.39.5-1
- Upgrade to 2.39.5

* Tue Jan 17 2023 Michael Catanzaro <mcatanzaro@redhat.com> - 2.39.4-4
- Revert "Re-enable full debuginfo on s390x"

* Tue Jan 17 2023 Michael Catanzaro <mcatanzaro@redhat.com> - 2.39.4-3
- Fix installed headers

* Mon Jan 16 2023 Michael Catanzaro <mcatanzaro@redhat.com> - 2.39.4-2
- Add patch to fix ANGLE build

* Mon Jan 16 2023 Michael Catanzaro <mcatanzaro@redhat.com> - 2.39.4-1
- Upgrade to 2.39.4

* Fri Jan 13 2023 Kalev Lember <klember@redhat.com> - 2.39.3-6
- Re-enable full debuginfo on s390x

* Sun Jan 08 2023 Neal Gompa <ngompa@fedoraproject.org> - 2.39.3-5
- Disable JSC JIT for Asahi SIG builds while it is broken with BTI enabled

* Sat Dec 31 2022 Pete Walter <pwalter@fedoraproject.org> - 2.39.3-4
- Rebuild for ICU 72

* Tue Dec 20 2022 Michael Catanzaro <mcatanzaro@redhat.com> - 2.39.3-3
- Sabotage debuginfo on s390x

* Thu Dec 15 2022 Michael Catanzaro <mcatanzaro@redhat.com> - 2.39.3-2
- Disable LTO again

* Wed Dec 14 2022 Michael Catanzaro <mcatanzaro@redhat.com> - 2.39.3-1
- Upgrade to 2.39.3

* Tue Dec 13 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.39.2-7
- Backport upstream fix for ruby3.2 File.exists? removal

* Fri Dec 02 2022 David King <amigadave@amigadave.com> - 2.39.2-6
- Fix javascriptcore5 Requires in webkitgtk6.0

* Tue Nov 29 2022 Michael Catanzaro <mcatanzaro@redhat.com> - 2.39.2-5
- Update comment regarding debuginfo size

* Tue Nov 29 2022 Michael Catanzaro <mcatanzaro@redhat.com> - 2.39.2-4
- Request 32 GB per vCPU when processing debuginfo

* Mon Nov 28 2022 Michael Catanzaro <mcatanzaro@redhat.com> - 2.39.2-3
- Drop upstreamed patches

* Mon Nov 28 2022 Michael Catanzaro <mcatanzaro@redhat.com> - 2.39.2-2
- Experimentally tweak debuginfo generation settings some more

* Mon Nov 28 2022 Michael Catanzaro <mcatanzaro@redhat.com> - 2.39.2-1
- Update to 2.39.2

* Fri Nov 18 2022 Michael Catanzaro <mcatanzaro@redhat.com> - 2.39.1-4
- Add patches to fix build

* Thu Nov 17 2022 Michael Catanzaro <mcatanzaro@redhat.com> - 2.39.1-3
- Revert "Add GL prototypes patch"

* Thu Nov 17 2022 Michael Catanzaro <mcatanzaro@redhat.com> - 2.39.1-2
- Add GL prototypes patch

* Wed Nov 16 2022 Michael Catanzaro <mcatanzaro@redhat.com> - 2.39.1-1
- Upgrade to 2.39.1 and webkitgtk-6.0

* Tue Nov 15 2022 Michael Catanzaro <mcatanzaro@redhat.com> - 2.38.2-2
- Adjust %%limit_build to request 3 GB of RAM per CPU

* Fri Nov 04 2022 Michael Catanzaro <mcatanzaro@redhat.com> - 2.38.2-1
- Update to 2.38.2

* Tue Oct 25 2022 Michael Catanzaro <mcatanzaro@redhat.com> - 2.38.1-1
- Update to 2.38.1

* Tue Oct 25 2022 Michael Catanzaro <mcatanzaro@redhat.com> - 2.38.0-4
- Disable abidiff

* Fri Sep 30 2022 Kalev Lember <klember@redhat.com> - 2.38.0-3
- Use -g1 rather than -g0 for i686 builds

* Mon Sep 19 2022 Michael Catanzaro <mcatanzaro@redhat.com> - 2.38.0-2
- Disable WebDriver in GTK 4 build

* Fri Sep 16 2022 Michael Catanzaro <mcatanzaro@redhat.com> - 2.38.0-1
- Upgrade to 2.38.0

* Fri Sep 02 2022 Michael Catanzaro <mcatanzaro@redhat.com> - 2.37.91-1
- Update to 2.37.91

* Sat Aug 20 2022 Michael Catanzaro <mcatanzaro@redhat.com> - 2.37.90-1
- Update to 2.37.90

* Wed Aug 10 2022 Kalev Lember <klember@redhat.com> - 2.37.1-18
- Re-enable debuginfo for ppc64le and s390x builds
- Require 8 GB of RAM per vCPU for debuginfo processing

* Wed Aug 10 2022 Kalev Lember <klember@redhat.com> - 2.37.1-17
- Disable debuginfo for ppc64le and s390x builds

* Tue Aug 09 2022 Michael Catanzaro <mcatanzaro@redhat.com> - 2.37.1-16
- Request 4 GB of RAM per vCPU

* Mon Aug 08 2022 Michael Catanzaro <mcatanzaro@redhat.com> - 2.37.1-15
- Add Obsoletes for webkitgtk4.1-jsc

* Mon Aug 08 2022 Michael Catanzaro <mcatanzaro@redhat.com> - 2.37.1-14
- Enable GTK 4

* Fri Aug 05 2022 Michael Catanzaro <mcatanzaro@redhat.com> - 2.37.1-13
- Empty commit to bump revision: -13

* Fri Aug 05 2022 Michael Catanzaro <mcatanzaro@redhat.com> - 2.37.1-12
- Empty commit to bump revision: -12

* Fri Aug 05 2022 Michael Catanzaro <mcatanzaro@redhat.com> - 2.37.1-11
- Empty commit to bump revision: -11

* Fri Aug 05 2022 Michael Catanzaro <mcatanzaro@redhat.com> - 2.37.1-10
- Empty commit to bump revision: -10

* Fri Aug 05 2022 Michael Catanzaro <mcatanzaro@redhat.com> - 2.37.1-9
- Empty commit to bump revision: -9

* Fri Aug 05 2022 Michael Catanzaro <mcatanzaro@redhat.com> - 2.37.1-8
- Empty commit to bump revision: -8

* Fri Aug 05 2022 Michael Catanzaro <mcatanzaro@redhat.com> - 2.37.1-7
- Empty commit to bump revision: -7

* Fri Aug 05 2022 Michael Catanzaro <mcatanzaro@redhat.com> - 2.37.1-6
- Empty commit to bump revision: -6

* Fri Aug 05 2022 Michael Catanzaro <mcatanzaro@redhat.com> - 2.37.1-5
- Empty commit to bump revision: -5

* Fri Aug 05 2022 Michael Catanzaro <mcatanzaro@redhat.com> - 2.37.1-4
- Empty commit to bump revision: -4

* Fri Aug 05 2022 Michael Catanzaro <mcatanzaro@redhat.com> - 2.37.1-3
- Empty commit to bump revision: -3

* Fri Aug 05 2022 Michael Catanzaro <mcatanzaro@redhat.com> - 2.37.1-2
- Empty commit to bump revision: -2

* Thu Aug 04 2022 Michael Catanzaro <mcatanzaro@redhat.com> - 2.37.1-12
- Initial import. This manual changelog entry hides the repo's long git history from rpm-autospec.

