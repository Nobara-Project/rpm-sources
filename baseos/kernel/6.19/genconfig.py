#!/usr/bin/env python3
import re
import sys
import platform

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

if __name__ == '__main__':

    config = parse_config_file('config')

    config.update(parse_config_file('config.generic'))

    config.update(parse_config_file(f'config.{platform.machine()}'))

    if len(sys.argv) > 1 and sys.argv[1] == "lto":
        config.update(parse_config_file('config.ltobuild'))

    output = ""

    for k,v in config.items():
        if v == "unset":
            output += f"# {k} is not set\n"
            continue
        
        output += f"{k}={v}\n"
    
    with open('full_config', 'w', encoding='utf-8') as f:
        f.write(output)

    