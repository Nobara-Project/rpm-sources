#!/usr/bin/sh
export LANG=C
DISPLAY_CHECK=$(echo $DISPLAY)
WHO=$(whoami)

### NVIDIA DRIVER CHECK ####
nvgpu=$(lspci -D | grep -iE 'VGA|3D' | grep -i nvidia | cut -d ":" -f 4)
nvkernmod=$(lspci -kD | grep -iEA3 '^[[:alnum:]]{4}:[[:alnum:]]{2}:[[:alnum:]]{2}.*VGA|3D' | grep -iA3 nvidia | grep -i 'kernel driver' | grep -iE 'vfio-pci|nvidia')


if [[ $DISPLAY_CHECK ]] && [[ $WHO != "liveuser" ]] && [[ $WHO != "gnome-initial-setup" ]]; then
  if [[ ! -z $nvgpu ]]; then
    if [[ -z $nvkernmod ]]; then
        # Check for internet connection
          wget -q --spider http://google.com
          if [ $? -eq 0 ]; then
                nobara-nvidia-wizard
          else
            # No internet connection found
            zenity --info\
              --title="No Internet connection." \
              --width=600 \
              --text="`printf "An internet connection is required to install Nvidia drivers. Once your system is connected to the internet, run 'hwcheck' from the terminal to restart the installer.\n\n"`"
            exit 0
          fi
    fi
  fi
fi

### END NVIDIA DRIVER CHECK ####

exit 0


