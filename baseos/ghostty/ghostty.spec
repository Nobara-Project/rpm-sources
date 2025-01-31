# Signing key from https://github.com/ghostty-org/ghostty/blob/main/PACKAGING.md
%global public_key RWQlAjJC23149WL2sEpT/l0QKy7hMIFhYdQOFy0Z7z7PbneUgvlsnYcV

%global cache_dir %{builddir}/zig-cache

Name:           ghostty
Version:        1.1.0
Release:        1%{?dist}
Summary:        Fast, native, feature-rich terminal emulator pushing modern features.


License:        MIT AND MPL-2.0 AND OFL-1.1
URL:            https://github.com/ghostty-org/ghostty
Source0:        https://release.files.ghostty.org/%{version}/ghostty-%{version}.tar.gz
Source1:        https://release.files.ghostty.org/%{version}/ghostty-%{version}.tar.gz.minisig

ExclusiveArch: x86_64

BuildRequires:  gtk4-devel
BuildRequires:  libadwaita-devel
BuildRequires:  ncurses
BuildRequires:  ncurses-devel
BuildRequires:  pandoc-cli
BuildRequires:  zig
BuildRequires:  minisign
BuildRequires:  pkgconfig(bzip2)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(harfbuzz)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  pkgconfig(oniguruma)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(gtk4)
BuildRequires:  pkgconfig(libadwaita-1)
BuildRequires:  libX11-devel

Requires:       %{name}-terminfo = %{version}-%{release}
Requires:       %{name}-shell-integration = %{version}-%{release}
Requires:       fontconfig
Requires:       freetype
Requires:       glib2
Requires:       gtk4
Requires:       harfbuzz
Requires:       libadwaita
Requires:       libpng
Requires:       oniguruma
Requires:       pixman
Requires:       zlib-ng

%description
Ghostty is a terminal emulator that differentiates itself by being fast, feature-rich, and native. While there are many excellent terminal emulators available, they all force you to choose between speed, features, or native UIs. Ghostty provides all three.

In all categories, I am not trying to claim that Ghostty is the best (i.e. the fastest, most feature-rich, or most native). But Ghostty is competitive in all three categories and Ghostty doesn't make you choose between them.

Ghostty also intends to push the boundaries of what is possible with a terminal emulator by exposing modern, opt-in features that enable CLI tool developers to build more feature rich, interactive applications.

While aiming for this ambitious goal, our first step is to make Ghostty one of the best fully standards compliant terminal emulator, remaining compatible with all existing shells and software while supporting all of the latest terminal innovations in the ecosystem. You can use Ghostty as a drop-in replacement for your existing terminal emulator.

%package        bash-completion
Summary:        Ghostty Bash completion
Requires:       bash-completion
Supplements:    (%{name} and bash-completion)

%description    bash-completion
%summary.

%package        fish-completion
Summary:        Ghostty Fish completion
Requires:       fish
Supplements:    (%{name} and fish)

%description    fish-completion
%summary.

%package        zsh-completion
Summary:        Ghostty Zsh completion
Requires:       zsh
Supplements:    (%{name} and zsh)

%description    zsh-completion
%summary.

%package        shell-integration
Summary:        Ghostty shell integration
Supplements:    %{name}

%description    shell-integration
%summary.

%package        terminfo
Summary:        Ghostty terminfo
Requires:       %{name}
Supplements:    %{name}

%description    terminfo
%summary.

%prep
/usr/bin/minisign -V -m %{SOURCE0} -x %{SOURCE1} -P %{public_key}
%autosetup

# Download everything ahead of time so we can enable system integration mode
ZIG_GLOBAL_CACHE_DIR="%{cache_dir}" ./nix/build-support/fetch-zig-cache.sh

%build

%install
DESTDIR="%{buildroot}" \
zig build \
    --summary all \
    --release=fast \
    --system "%{cache_dir}/p" \
    --prefix "%{_prefix}" --prefix-lib-dir "%{_libdir}" \
    --prefix-exe-dir "%{_bindir}" --prefix-include-dir "%{_includedir}" \
    --verbose \
    -Dversion-string=%{version}-%{release} \
    -Dcpu=baseline \
    -Dstrip=false \
    -Dpie=true \
    -Demit-docs \
    -Demit-termcap \
    -Demit-terminfo
    
%files
%doc README.md
%license LICENSE
%_bindir/ghostty
%_datadir/applications/com.mitchellh.ghostty.desktop
%_datadir/bat/syntaxes/ghostty.sublime-syntax
%_datadir/ghostty/
%_datadir/kio/servicemenus/com.mitchellh.ghostty.desktop
%_datadir/nautilus-python/extensions/com.mitchellh.ghostty.py
%_datadir/nvim/site/compiler/ghostty.vim
%_datadir/nvim/site/ftdetect/ghostty.vim
%_datadir/nvim/site/ftplugin/ghostty.vim
%_datadir/nvim/site/syntax/ghostty.vim
%_datadir/vim/vimfiles/compiler/ghostty.vim
%_datadir/vim/vimfiles/ftdetect/ghostty.vim
%_datadir/vim/vimfiles/ftplugin/ghostty.vim
%_datadir/vim/vimfiles/syntax/ghostty.vim
%_iconsdir/hicolor/16x16/apps/com.mitchellh.ghostty.png
%_iconsdir/hicolor/16x16@2/apps/com.mitchellh.ghostty.png
%_iconsdir/hicolor/32x32/apps/com.mitchellh.ghostty.png
%_iconsdir/hicolor/32x32@2/apps/com.mitchellh.ghostty.png
%_iconsdir/hicolor/128x128/apps/com.mitchellh.ghostty.png
%_iconsdir/hicolor/128x128@2/apps/com.mitchellh.ghostty.png
%_iconsdir/hicolor/256x256/apps/com.mitchellh.ghostty.png
%_iconsdir/hicolor/256x256@2/apps/com.mitchellh.ghostty.png
%_iconsdir/hicolor/512x512/apps/com.mitchellh.ghostty.png
%_iconsdir/hicolor/1024x1024/apps/com.mitchellh.ghostty.png
%_mandir/man1/ghostty.1.gz
%_mandir/man5/ghostty.5.gz

%files bash-completion
%bash_completions_dir/ghostty.bash

%files fish-completion
%fish_completions_dir/ghostty.fish

%files zsh-completion
%zsh_completions_dir/_ghostty

%files shell-integration
%_datadir/ghostty/shell-integration/bash/bash-preexec.sh
%_datadir/ghostty/shell-integration/bash/ghostty.bash
%_datadir/ghostty/shell-integration/elvish/lib/ghostty-integration.elv
%_datadir/ghostty/shell-integration/fish/vendor_conf.d/ghostty-shell-integration.fish
%_datadir/ghostty/shell-integration/zsh/.zshenv
%_datadir/ghostty/shell-integration/zsh/ghostty-integration

%files terminfo
%_datadir/terminfo/ghostty.termcap
%_datadir/terminfo/ghostty.terminfo
%_datadir/terminfo/g/ghostty
%_datadir/terminfo/x/xterm-ghostty

%changelog
%autochangelog
