Name:           supergfxctl-plasmoid
Version:        1.2.0
Release:        1%{?dist}
Summary:        KDE Plasma plasmoid for supergfxctl

License:        MPL2
URL:            https://gitlab.com/Jhyub/supergfxctl-plasmoid
Source0:        https://gitlab.com/Jhyub/supergfxctl-plasmoid/-/archive/v%{version}/supergfxctl-plasmoid-v%{version}.tar.gz

BuildRequires:  cmake gcc-c++ extra-cmake-modules kf5-ki18n-devel kf5-plasma-devel qt5-qtdeclarative-devel
Requires:       hicolor-icon-theme kf5-plasma kf5-ki18n qt5-qtdeclarative supergfxctl

%description
KDE Plasma plasmoid for supergfxctl

%global debug_package %{nil}

%prep
%setup -n %{name}-v%{version}


%build
mkdir -p build
cd build
cmake -DCMAKE_INSTALL_PREFIX=/usr ..
make


%install
cd build
%make_install


%files
%license LICENSE
/usr/lib64/qt5/plugins/plasma/applets/plasma_applet_supergfxctl.so
/usr/share/icons/hicolor/scalable/status/supergfxctl-plasmoid-dgpu-active.svg
/usr/share/icons/hicolor/scalable/status/supergfxctl-plasmoid-dgpu-off.svg
/usr/share/icons/hicolor/scalable/status/supergfxctl-plasmoid-dgpu-suspended.svg
/usr/share/icons/hicolor/scalable/status/supergfxctl-plasmoid-gpu-asusmuxdiscrete-active.svg
/usr/share/icons/hicolor/scalable/status/supergfxctl-plasmoid-gpu-asusmuxdiscrete.svg
/usr/share/icons/hicolor/scalable/status/supergfxctl-plasmoid-gpu-compute-active.svg
/usr/share/icons/hicolor/scalable/status/supergfxctl-plasmoid-gpu-compute.svg
/usr/share/icons/hicolor/scalable/status/supergfxctl-plasmoid-gpu-egpu-active.svg
/usr/share/icons/hicolor/scalable/status/supergfxctl-plasmoid-gpu-egpu.svg
/usr/share/icons/hicolor/scalable/status/supergfxctl-plasmoid-gpu-hybrid-active.svg
/usr/share/icons/hicolor/scalable/status/supergfxctl-plasmoid-gpu-hybrid.svg
/usr/share/icons/hicolor/scalable/status/supergfxctl-plasmoid-gpu-integrated-active.svg
/usr/share/icons/hicolor/scalable/status/supergfxctl-plasmoid-gpu-integrated.svg
/usr/share/icons/hicolor/scalable/status/supergfxctl-plasmoid-gpu-vfio-active.svg
/usr/share/icons/hicolor/scalable/status/supergfxctl-plasmoid-gpu-vfio.svg
/usr/share/kservices5/plasma-applet-dev.jhyub.supergfxctl.desktop
/usr/share/metainfo/dev.jhyub.supergfxctl.appdata.xml
/usr/share/plasma/plasmoids/dev.jhyub.supergfxctl/contents/ui/main.qml
/usr/share/plasma/plasmoids/dev.jhyub.supergfxctl/contents/ui/configGeneral.qml
/usr/share/plasma/plasmoids/dev.jhyub.supergfxctl/contents/config/main.xml
/usr/share/plasma/plasmoids/dev.jhyub.supergfxctl/contents/config/config.qml
/usr/share/plasma/plasmoids/dev.jhyub.supergfxctl/metadata.desktop
/usr/share/plasma/plasmoids/dev.jhyub.supergfxctl/metadata.json
/usr/share/locale/ko/LC_MESSAGES/plasma_applet_dev.jhyub.supergfxctl.mo


%changelog
* Fri Jan 14 2022 Janghyub Seo
- 
