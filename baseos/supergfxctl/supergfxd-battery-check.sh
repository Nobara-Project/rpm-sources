#!/bin/sh

# add hybrid/integrated swapper for laptops
LEVEL="$(upower -i $(upower -e | grep 'BAT') | grep -E "percentage" | awk '{print $2}' | sed 's/\%//g')"
DEVICES="$(lspci | cut -c8- | grep -i -E '(vga|display|3d)' | grep -vi 'non-vga' | wc -l)"

if [ $? -eq 0 ]; then
       if [[ $DEVICES > 1 ]] && [[ ! -z $LEVEL ]]; then
               /usr/bin/supergfxd
       else
               echo "No battery detected. Supergfxctl is intended for laptops and portable devices with multiple gpus only. Quitting."
               systemctl stop supergfxd
               exit 0
       fi
fi
