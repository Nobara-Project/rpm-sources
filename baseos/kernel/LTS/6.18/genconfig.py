#!/usr/bin/env python3
import re
import sys
import platform
import os

def parse_config_file(filepath):
    config = {}

    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()

            if not line:
                continue

            if line.startswith('# CONFIG_') and line.endswith('is not set'):
                config[line[2:-11]] = "unset"
            
            if not line.startswith('#') and '=' in line:
                r = line.split('=')

                if not r[0].startswith('CONFIG_'):
                    r[0] = "CONFIG_" + r[0]

                config[r[0]] = r[1]

    return config

# aarch64: the kernel's own arm64 defconfig enables the drivers of every
# mainstream Arm platform (Qualcomm Snapdragon X laptops, Ampere, Tegra,
# Raspberry Pi, Rockchip, ...). The base config, CachyOS's x86 config, has none
# of them, and olddefconfig then also drops what config.aarch64 asks for when
# a parent option is off (CLK_X1E80100_GCC needs COMMON_CLK_QCOM). Take its
# platform and driver options, but none of the generic tuning, debug or
# security ones, so CachyOS's settings stay; config.aarch64 still comes last.
ARM64_DEFCONFIG_SKIP = re.compile(
    r"DEBUG|KASAN|KCOV|FTRACE|TRACE|PROVE|LOCKDEP|_HZ|^CONFIG_HZ|PREEMPT|NR_CPUS"
    r"|LOCALVERSION|DEFAULT_|SECURITY|MODULE_SIG|SYSTEM_TRUSTED|LSM|CMDLINE|SCHED"
    r"|CPU_FREQ_DEFAULT|NUMA|TRANSPARENT|PROFILING|PERF_EVENTS$|BPF|CGROUP"
    r"|NAMESPACES|AUDIT|IKCONFIG|KALLSYMS|EXPERT|COMPAT|ARM64_VA|ARM64_PA"
    r"|_MODULE_COMPRESS|INITRAMFS|BLK_DEV_INITRD|EFI_ZBOOT|ZBOOT|RANDOMIZE"
    r"|STACKPROTECTOR|HARDENED|FORTIFY|INIT_STACK|SLAB|SLUB|KVM|VIRTUALIZATION"
    r"|HOTPLUG_CPU|MEMORY_HOTPLUG|CRASH|KEXEC|HIBERNATION|SUSPEND")

def arm64_platform_options(config, defconfig):
    added = {}
    for k, v in parse_config_file(defconfig).items():
        if v in ('y', 'm') and not ARM64_DEFCONFIG_SKIP.search(k) \
                and config.get(k) not in ('y', 'm'):
            added[k] = v
    return added

if __name__ == '__main__':
    try:
        path = os.path.dirname(os.path.abspath(__file__)) + '/'

        config = parse_config_file(path + 'config')

        config.update(parse_config_file(path + 'config.generic'))

        if platform.machine() == 'aarch64' and os.path.exists('arch/arm64/configs/defconfig'):
            added = arm64_platform_options(config, 'arch/arm64/configs/defconfig')
            config.update(added)
            print(f"added {len(added)} platform options from arch/arm64/configs/defconfig")

        config.update(parse_config_file(path + 'config.' + platform.machine()))

        if len(sys.argv) > 1 and sys.argv[1] == "lto":
            config.update(parse_config_file(path + 'config.ltobuild'))

        output = ""

        for k,v in config.items():
            if v == "unset":
                output += f"# {k} is not set\n"
                continue
            
            output += f"{k}={v}\n"
        
        with open('.config', 'w', encoding='utf-8') as f:
            f.write(output)

        print("successfully merged configs")
    except Exception as e:
        print(e)
        print("unable to merge configs")
        exit(1)
