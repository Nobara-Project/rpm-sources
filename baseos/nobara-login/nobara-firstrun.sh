#!/usr/bin/bash

DISPLAY_CHECK=$(echo "$DISPLAY")
WHO=$(whoami)

newinstall=$(grep yes /etc/nobara/newinstall)

if which starship > /dev/null 2>&1; then
    eval "$(starship init bash)"
    if [ ! -f "$HOME/.config/starship.toml" ]; then
        if [ -f /usr/share/starship/starship.toml ]; then
            cp /usr/share/starship/starship.toml "$HOME/.config/"
        fi
    fi
fi

# Function to get the rpm info
get_rpm_info() {
    rpm -qi plasma-workspace
}

# Function to parse the rpm info
parse_rpm_info() {
    local rpm_output="$1"
    version=$(echo "$rpm_output" | grep "Version" | awk '{print $3}')
    install_date=$(echo "$rpm_output" | grep "Install Date" | sed 's/Install Date\s*:\s*//')
}

# Function to convert date to seconds since epoch
date_to_epoch() {
    date -d "$1" +%s
}

if [[ -n "$DISPLAY_CHECK" ]] && [[ "$WHO" != "liveuser" ]] && [[ "$WHO" != "gnome-initial-setup" ]]; then
    sleep 1
    if [[ -n "$newinstall" ]]; then

        /usr/bin/nobara_login_discord.sh
        /usr/bin/nobara_login_extest_wayland_input.sh
        /usr/bin//nobara_login_gnome_newfile.sh

        # Initiate flatpak search for the first time
        flatpak search chrome
        # Perform system update on fresh install
        /usr/bin/updatecheck
    fi
fi

