%global debug_package %{nil}

Name:           plasma-rounded-corners
Version:        0.4.2
Release:        3%{?dist}
Summary:        Rounded corners Desktop Effect for KDE Plasma.

License:        GPLv3
URL:            https://github.com/matinlotfali/KDE-Rounded-Corners
Source0:        https://github.com/matinlotfali/KDE-Rounded-Corners/archive/refs/tags/v%{version}.tar.gz
Source1:        0001-use-some-sane-default-shadows-and-outlines.patch

BuildArch:      x86_64

BuildRequires:  nodejs-npm
BuildRequires:  git
BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qttools-devel
BuildRequires:  qt5-qttools-static
BuildRequires:  qt5-qtx11extras-devel
BuildRequires:  kf5-kconfigwidgets-devel
BuildRequires:  kf5-kcrash-devel
BuildRequires:  kf5-kguiaddons-devel
BuildRequires:  kf5-kglobalaccel-devel
BuildRequires:  kf5-kio-devel
BuildRequires:  kf5-ki18n-devel
BuildRequires:  kwin-devel
BuildRequires:  qt5-qtbase-devel
BuildRequires:  libepoxy-devel

Requires:       plasma-desktop


%description
This effect rounds the corners of your windows and adds an outline around them without much affecting the performance of the KDE Plasma desktop


%prep
%autosetup -n KDE-Rounded-Corners
patch -Np1 < %{SOURCE1}
cmake . --install-prefix /usr

%build
make
make DESTDIR=build install

%install
mkdir -p %{buildroot}%{_libdir}/
mkdir -p %{buildroot}%{_datadir}/
mv build/usr/lib64/* %{buildroot}%{_libdir}/
mv build/kwin %{buildroot}%{_datadir}/
rm -Rf build

%files
%license LICENSE
%{_libdir}/*
%{_datadir}/kwin

%changelog


