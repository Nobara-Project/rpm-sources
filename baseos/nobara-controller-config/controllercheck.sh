#!/bin/bash
REBOOT_REQUIRED="no"
INTERNET="no"

### XBOX CONTROLLER FIRMWARE CHECK ####

internet_check() {
      # Check for internet connection
      wget -q --spider http://google.com
      if [ $? -eq 0 ]; then
          INTERNET="yes"
      fi
}

install_drivers() {
      (
      	echo "# Installing xone and xpadneo packages..."
        echo "20"; sleep 1
        echo "# Installing dnf5 fixes."
        pkexec bash -c 'dnf install -y "dnf5-command(builddep)"'
        echo "50"; sleep 1
        pkexec bash -c 'usermod -aG pkg-build $USER && dnf4 install -y lpf-xone-firmware xone xpadneo && dnf4 remove -y xone-firmware'
        echo "# Packages installed, press OK to begin firmware installation."
        echo "100"; sleep 1
      ) | zenity --title="Xbox One Controller setup" --progress --no-cancel --width=600 --percentage=0
      bash -c 'lpf reset xone-firmware'
      bash -c 'lpf update xone-firmware'
}

remove_drivers() {
      (
      	echo "# Xbox One Controller firmware remover running..."
      	echo "30"; sleep 1
        pkcon remove -y lpf-xone-firmware xone xpadneo xone-firmware
        echo "90"; sleep 1
        echo "# Xbox One Controller driver and firmware removal complete!"
        echo "100"; sleep 1
      ) | zenity --title="Xbox One Controller setup" --progress --no-cancel --width=600 --percentage=0
}

lpf=$(rpm -qa | grep 'lpf-xone-firmware')
xbfirmware=$(rpm -qa | grep 'xone-firmware'| wc -l)

if [[ -z $lpf ]]; then
  if [ "$xbfirmware" != "2" ]; then
    # Check for internet connection
    internet_check
    if [ "$INTERNET" == "yes" ]; then
      zenity --question\
        --title="Xbox One Controller setup" \
        --width=600 \
        --text="`printf "Xbox One Wireless controllers require driver and firmware updates in order to work with full functionality. This will install the xone driver and firmware for wireless dongle + usb cable support, and xpadneo for bluetooth support. Would you like to perform this now?\n\n"`"
        case $? in
          0)
            install_drivers
            REBOOT_REQUIRED="yes"
            ;;
          *)
            # User declined to install firmware
            exit 0
            ;;
        esac
    else
      # No internet connection found
      zenity --info\
        --title="No Internet connection." \
        --width=600 \
        --text="`printf "An internet connection is required to install the Xbox Controller firmware. Once your system is connected to the internet, run 'nobara-controller-config' to restart the installer.\n\n"`"
      exit 0
    fi
  fi
else
  zenity --question\
    --title="Xbox One Controller setup" \
    --width=600 \
    --text="`printf "Xbox xone and xpadneo driver have been detected as already installed, would you like to perform a clean removal?\n\n"`"
    case $? in
      0)
        remove_drivers
        REBOOT_REQUIRED="yes"
        zenity --info\
          --title="Xbox One Controller setup." \
          --width=600 \
          --text="`printf "Removal complete. To reinstall, run 'nobara-controller-config' to restart the installer.\n\n"`"
        ;;
      *)
        # User declined to remove firmware
        exit 0
        ;;
    esac
fi
### END XBOX CONTROLLER FIRMWARE CHECK ####

if [ "$REBOOT_REQUIRED" == "yes" ]; then

     zenity --question \
       --title="Reboot Required." \
       --width=600 \
       --text="`printf "The system requires a reboot before newly installed drivers and firmware can take effect. Would you like to reboot now?\n\n"`"

     if [ $? = 0 ]; then
       sleep 5
       reboot
     else
   	  exit 0
     fi
fi


exit 0
