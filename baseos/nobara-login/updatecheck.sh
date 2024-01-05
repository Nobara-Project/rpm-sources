#!/usr/bin/sh
export LANG=C
DISPLAY_CHECK=$(echo $DISPLAY)
WHO=$(whoami)
### SYSTEM UPDATE CHECK ####

newinstall=$(cat /etc/nobara/newinstall | grep yes)


if [[ $DISPLAY_CHECK ]] && [[ $WHO != "liveuser" ]] && [[ $WHO != "gnome-initial-setup" ]]; then
      if [[ ! -z $newinstall ]]; then
          # Check for internet connection
          wget -q --spider http://google.com
          if [ $? -eq 0 ]; then
            if zenity --question --width=600 --text="We've detected this is a new Nobara installation. Before moving on it is required that you perform a system update. Would you like to do this now?"; then
    			nobara-sync
            else
    			zenity --info --text="Please note a system update is required before installing any new drivers or system packages."
                echo 1 > /home/$USER/.config/updatesystem-declined
                exit 0
            fi
          else
            # No internet connection found
            zenity --info\
              --title="No Internet connection." \
              --width=600 \
              --text="`printf "An internet connection is required to update the system. Once your system is connected to the internet, run 'Update System' from the menu or Nobara Welcome App to update the system.\n\n"`"
            echo 1 > /home/$USER/.config/updatesystem-declined
            exit 0
          fi
      fi
      # Perform AMD/Nvidia driver check after system update
      /usr/bin/hwcheck
fi

### END SYSTEM UPDATE CHECK ####


exit 0


