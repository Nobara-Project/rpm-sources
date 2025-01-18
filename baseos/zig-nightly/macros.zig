%zig_arches x86_64 aarch64 riscv64 %{mips64}

%zig /usr/bin/zig

# expected features for each arch when targeting baseline
# found in https://github.com/ziglang/zig/tree/master/lib/std/target
#
# aarch64:
#   ete, fuse_aes, neon, perfmon, use_postra_scheduler,
#
# x86_64:
#   cx8 idivq_to_divl macrofusion slow_3ops_lea slow_incdec vzeroupper x87
#
# riscv64:
#   a, c, d, m
#
# mips64:
#   mips32
%_zig_cpu baseline
%_zig_target native

# seperated build options
%_zig_general_options --verbose
%_zig_project_options -Dtarget=%{_zig_target} -Dcpu=%{_zig_cpu} -Doptimize=ReleaseSafe
%_zig_advanced_options --cache-dir zig-cache

%_zig_build_options %{?_zig_general_options} %{?_zig_project_options} %{?_zig_advanced_options}
%_zig_install_options --prefix "%{_prefix}" --prefix-lib-dir "%{_libdir}" --prefix-exe-dir "%{_bindir}" --prefix-include-dir "%{_includedir}"

%zig_build %zig \\\
        build \\\
        %{?_zig_build_options}

%zig_install \
    DESTDIR="%{buildroot}" %zig_build \\\
        install \\\
        %{?_zig_install_options}

%zig_test \
    %zig_build \\\
        test
