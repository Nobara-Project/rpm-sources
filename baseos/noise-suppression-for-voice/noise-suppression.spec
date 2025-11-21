# Status: active
# Tag: Effect
# Type: Plugin, LADSPA, LV2, VST, VST3
# Category: Effect

Name: noise-suppression-for-voice
Version: 1.10
Release: 4%{?dist}
Summary: Real-time Noise Suppression LADSPA / LV2 Plugin
License: GPL-2.0-or-later
URL: https://github.com/werman/noise-suppression-for-voice
ExclusiveArch: x86_64 aarch64

Vendor:       Audinux
Distribution: Audinux

Source0: https://github.com/werman/noise-suppression-for-voice/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires: gcc gcc-c++
BuildRequires: cmake
BuildRequires: alsa-lib-devel
BuildRequires: lv2-devel
BuildRequires: ladspa-devel
BuildRequires: gtk3-devel
BuildRequires: libcurl-devel
BuildRequires: freetype-devel
BuildRequires: libubsan
BuildRequires: libatomic

%description
A real-time noise suppression LV2 /VST3 / VST / LADSPA plugin for voice
based on Xiph's RNNoise - https://github.com/xiph/rnnoise.
More info about the base library - https://people.xiph.org/~jm/demo/rnnoise/.

%package -n license-%{name}
Summary: License and documentation for %{name}

%package -n ladspa-%{name}
Summary: Real-time Noise Suppression LADSPA Plugin
Requires: license-%{name}

%package -n lv2-%{name}
Summary: Real-time Noise Suppression LV2 Plugin
Requires: license-%{name}

%package -n vst3-%{name}
Summary: Real-time Noise Suppression VST3 Plugin
Requires: license-%{name}

%package -n vst-%{name}
Summary: Real-time Noise Suppression VST Plugin
Requires: license-%{name}

%description -n license-%{name}
License and documentation for %{name}.

%description -n ladspa-%{name}
A real-time noise suppression LADSPA plugin for voice based on Xiph's RNNoise - https://github.com/xiph/rnnoise.
More info about the base library - https://people.xiph.org/~jm/demo/rnnoise/.

%description -n lv2-%{name}
A real-time noise suppression LV2 plugin for voice based on Xiph's RNNoise - https://github.com/xiph/rnnoise.
More info about the base library - https://people.xiph.org/~jm/demo/rnnoise/.

%description -n vst3-%{name}
A real-time noise suppression VST3 plugin for voice based on Xiph's RNNoise - https://github.com/xiph/rnnoise.
More info about the base library - https://people.xiph.org/~jm/demo/rnnoise/.

%description -n vst-%{name}
A real-time noise suppression VST plugin for voice based on Xiph's RNNoise - https://github.com/xiph/rnnoise.
More info about the base library - https://people.xiph.org/~jm/demo/rnnoise/.

%prep
%autosetup -p1 -n %{name}-%{version}

%build

%cmake -DLIBINSTDIR=%{_lib}

%cmake_build

%install

%cmake_install

# Rename vst directory
mv %{buildroot}/%{_libdir}/lxvst/ %{buildroot}/%{_libdir}/vst/

%files -n license-%{name}
%doc README.md
%license LICENSE

%files -n ladspa-%{name}
%{_libdir}/ladspa/*

%files -n lv2-%{name}
%{_libdir}/lv2/*

%files -n vst3-%{name}
%{_libdir}/vst3/*

%files -n vst-%{name}
%{_libdir}/vst/*

%changelog
* Fri Aug 22 2025 Yann Collette <ycollette.nospam@free.fr> - 1.10-4
- update to 1.10-4 - remove unused dep

* Sun May 19 2024 Yann Collette <ycollette.nospam@free.fr> - 1.10-3
- update to 1.10-3

* Mon Mar 06 2023 Yann Collette <ycollette.nospam@free.fr> - 1.03-3
- update to 1.03

* Thu Oct 1 2020 Yann Collette <ycollette.nospam@free.fr> - 0.0.0-3
- update to 0.9 - fix for Fedora 33

* Thu Apr 23 2020 Yann Collette <ycollette.nospam@free.fr> - 0.2.0-3
- fix for Fedora 32

* Mon Apr 15 2019 Yann Collette <ycollette.nospam@free.fr> - 0.2.0-2
- build ladspa and lv2 packages

* Mon Apr 15 2019 Yann Collette <ycollette.nospam@free.fr> - 0.2.0-1
- Initial version
