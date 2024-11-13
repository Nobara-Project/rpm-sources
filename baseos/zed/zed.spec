%global source_date_epoch_from_changelog 0
%global __brp_mangle_shebangs_exclude_from ^/usr/src/.*$

%global crate zed
%global app_id dev.zed.Zed


Name:           zed
Version:        0.160.7
Release:        0.1%{?dist}
Summary:        a high-performance multiplayer code editor

License:        GPL3 AGPL
URL:            https://github.com/zed-industries/zed
Source0:        %{name}-%{version}.tar.gz
#Patch0:         a2d83ec6195c0f3e254a16d4dc7d47f6c6a7bf18.patch

BuildRequires:  cargo-rpm-macros
BuildRequires:  gcc
BuildRequires:  g++
BuildRequires:  alsa-lib-devel
BuildRequires:  fontconfig-devel
BuildRequires:  wayland-devel
BuildRequires:  libxkbcommon-x11-devel
BuildRequires:  openssl-devel
BuildRequires:  libzstd-devel
BuildRequires:  perl-FindBin
BuildRequires:  perl-IPC-Cmd
BuildRequires:  perl-File-Compare
BuildRequires:  perl-File-Copy
BuildRequires:  perl-lib
BuildRequires:  vulkan-loader
BuildRequires:  libcurl-devel
BuildRequires:  cmake

### for the desktop file
BuildRequires:  desktop-file-utils

%description
Zed is a high-performance, multiplayer code editor from the creators of Atom and Tree-sitter. It's also open source.

%prep
%autosetup -n %{crate}-%{version} -p1

export DO_STARTUP_NOTIFY="true"
export APP_ID="%app_id"
export APP_ICON="%app_id"
export APP_NAME="Zed Editor"
export APP_CLI="zed"
export APP_ARGS="%U"
export ZED_RELEASE_CHANNEL=stable

envsubst < "crates/zed/resources/zed.desktop.in" > $APP_ID.desktop
envsubst < "crates/zed/resources/flatpak/zed.metainfo.xml.in" > $APP_ID.metainfo.xml

%cargo_prep -N

## can not build it offline yet
sed -i 's/offline = true/offline = false/g' .cargo/config.toml


%build
export ZED_UPDATE_EXPLANATION="Please use the package manager to update zed."

script/generate-licenses

# Build CLI
pushd crates/cli/
%{cargo_build}
popd

# Build Editor
pushd crates/zed/
%{cargo_build}
popd

%install
install -Dm755 target/release/zed %{buildroot}%{_libexecdir}/zed-editor
install -Dm755 target/release/cli %{buildroot}%{_bindir}/zed
#install -Dm755 target/release/zed %{buildroot}%{_bindir}/zed

desktop-file-install                                    \
--dir=%{buildroot}%{_datadir}/applications              \
%app_id.desktop

#install -Dm644 %app_id.desktop %{buildroot}%{_datadir}/applications/%app_id.desktop
#install -Dm644 crates/zed/resources/app-icon.png %{buildroot}%{_datadir}/pixmaps/%app_id.png
install -Dm644 assets/icons/logo_96.svg %{buildroot}%{_datadir}/pixmaps/%app_id.svg
install -Dm644 %app_id.metainfo.xml %{buildroot}%{_metainfodir}/%app_id.metainfo.xml


%files
%license LICENSE-* assets/licenses.md
%{_bindir}/zed
%{_libexecdir}/zed-editor
%{_datadir}/applications/%app_id.desktop
%{_datadir}/pixmaps/%app_id.svg
%{_metainfodir}/%app_id.metainfo.xml


%changelog
