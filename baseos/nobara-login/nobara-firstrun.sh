#!/bin/bash

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
        # Perform system update on fresh install
        /usr/bin/updatecheck
    fi

    # Get the rpm info
    rpm_output=$(get_rpm_info)

    # Parse the rpm info
    parse_rpm_info "$rpm_output"

    # Check if the version is 6.1.3
    if [[ "$version" != "6.1.3" ]]; then
        echo "Version is not 6.1.3"
        exit 1
    fi

    # Convert the installation date to epoch
    install_date_epoch=$(date_to_epoch "$install_date")

    # Get the list of all user home directories
    home_directories=$(awk -F: '{ if ($3 >= 1000) print $6 }' /etc/passwd)

    # Iterate over each user's home directory
    for home_dir in $home_directories; do
        qmlcache_dir="$home_dir/.cache/plasmashell/qmlcache"
        if [[ -d "$qmlcache_dir" ]]; then
            qmlcache_mtime=$(stat -c %Y "$qmlcache_dir")
            if [[ "$qmlcache_mtime" -lt "$install_date_epoch" ]]; then
                rm -rf "$qmlcache_dir"
                echo "Deleted '$qmlcache_dir' directory successfully"
            else
                echo "'$qmlcache_dir' is not older than the install date"
            fi
        else
            echo "Directory '$qmlcache_dir' does not exist"
        fi
    done
fi

/usr/bin/nobara-device-quirks
