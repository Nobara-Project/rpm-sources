#!/usr/bin/sh
DISPLAY_CHECK=$(echo $DISPLAY)
WHO=$(whoami)

newinstall=$(cat /etc/nobara/newinstall | grep yes)

if [[ $(which starship) == "/usr/bin/starship" ]]; then
    eval "$(starship init bash)"
    if [ ! -f $HOME/.config/starship.toml ]; then
        if [ -f /usr/share/starship/starship.toml ]; then
            cp /usr/share/starship/starship.toml $HOME/.config/
        fi
    fi
fi

if [[ $DISPLAY_CHECK ]] && [[ $WHO != "liveuser" ]] && [[ $WHO != "gnome-initial-setup" ]]; then
  sleep 1
  if [[ ! -z $newinstall ]]; then
	  # Perform system update on fresh install
	  /usr/bin/updatecheck
  fi
fi

/usr/bin/nobara-device-quirks
