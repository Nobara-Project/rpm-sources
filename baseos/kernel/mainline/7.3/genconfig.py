#!/usr/bin/env python3
import re
import sys
import platform
import os

def parse_config_file(filepath):
    config = {}

    with open(filepath, 'r', encoding='utf-8') as f:
        for lineno, raw_line in enumerate(f, 1):
            line = raw_line.strip()

            if not line:
                continue

            if line.startswith('# CONFIG_') and line.endswith('is not set'):
                config[line[2:-11]] = "unset"
                continue

            if line.startswith('#') or '=' not in line:
                continue

            key, _, value = line.partition('=')

            if not key.startswith('CONFIG_'):
                key = "CONFIG_" + key

            # Detect unterminated Kconfig string values
            if value.startswith('"') and not value.endswith('"'):
                raise ValueError(
                    f"{filepath}:{lineno}: "
                    f"unterminated string for {key}: {value}"
                )

            config[key] = value

    return config

if __name__ == '__main__':
    try:
        path = os.path.dirname(os.path.abspath(__file__)) + '/'

        config = parse_config_file(path + 'config')

        config.update(parse_config_file(path + 'config.generic'))

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
