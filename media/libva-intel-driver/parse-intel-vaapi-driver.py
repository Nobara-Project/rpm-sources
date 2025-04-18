#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 Nicolas Chauvet <kwizart@gmail.com>
# Licensed under the GNU General Public License Version or later

import sys

def main():
    if len(sys.argv) != 2:
        print("usage: %s src/i965_pciids.h" % sys.argv[0])
        return 1

    # open file
    f = open(sys.argv[1])
    pids = []
    for line in f.readlines():

        # remove Windows and Linux line endings
        line = line.replace('\r', '')
        line = line.replace('\n', '')

        # Only look at line with CHIPSET
        if len(line) > 0 and not line.startswith('CHIPSET'):
            continue

        # empty line
        if len(line) == 0:
            continue

        # get name
        pid = int(line[10:14], 16)
        if not pid in pids:
            pids.append(pid)

    # output
    for pid in pids:
        vid = 0x8086
        print("pci:v%08Xd%08Xsv*sd*bc*sc*i*" % (vid, pid))

if __name__ == "__main__":
    main()
