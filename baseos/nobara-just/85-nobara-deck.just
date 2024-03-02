
# Install Decky Loader (https://github.com/SteamDeckHomebrew/decky-loader)
install-decky:
    #!/usr/bin/bash
    export HOME=$(getent passwd ${SUDO_USER:-$USER} | cut -d: -f6)
    curl -L https://github.com/SteamDeckHomebrew/decky-installer/releases/latest/download/install_release.sh | sh

# Install SimpleDeckyTDP, a simple TDP plugin for alternative PC handhelds
install-simpledeckytdp:
    #!/usr/bin/bash
    if [[ -d $HOME/homebrew/plugins ]]; then
      sudo rm -rf $HOME/homebrew/plugins/SimpleDeckyTDP
      curl -L $(curl -s https://api.github.com/repos/aarron-lee/SimpleDeckyTDP/releases/latest | grep "browser_download_url" | cut -d '"' -f 4) -o /tmp/SimpleDeckyTDP.tar.gz
      sudo tar -xzf /tmp/SimpleDeckyTDP.tar.gz -C $HOME/homebrew/plugins
      rm /tmp/SimpleDeckyTDP.tar.gz
      echo 'Installed. Please reboot to apply needed changes.'
    else
      echo 'Please install Decky Loader by running ujust get-decky first.'
    fi

# Install HHD Decky Plugin for customizing input on the Lenovo Legion Go, ROG Ally, and alternative handhelds
install-hhd-decky:
    #!/usr/bin/bash
    if [[ -d $HOME/homebrew/plugins ]]; then
      sudo rm -rf $HOME/homebrew/plugins/hhd-decky
      curl -L $(curl -s https://api.github.com/repos/hhd-dev/hhd-decky/releases/latest | grep "browser_download_url" | cut -d '"' -f 4) -o /tmp/hhd-decky.tar.gz
      sudo tar -xzf /tmp/hhd-decky.tar.gz -C $HOME/homebrew/plugins
      rm /tmp/hhd-decky.tar.gz
      echo 'Installed.'
    else
      echo 'Please install Decky Loader by running ujust get-decky first.'
    fi

# Install ROG Ally Theme for CSS Loader (https://github.com/semakusut/SBP-ROG-Ally)
install-rog-ally-theme:
    #!/usr/bin/bash
    if [ -d "$HOME/homebrew/themes" ]; then
        rm -rf "$HOME/homebrew/themes/SBP-ROG-Ally"
        git clone https://github.com/semakusut/SBP-ROG-Ally.git --single-branch "$HOME/homebrew/themes/SBP-ROG-Ally"
    else
        echo 'Please install Decky Loader & CSS Loader first'
    fi

# Install Lenovo Legion Go for CSS Loader (https://github.com/frazse/SBP-Legion-Go-Theme)
install-legion-go-theme:
    #!/usr/bin/bash
    if [ -d "$HOME/homebrew/themes" ]; then
        rm -rf "$HOME/homebrew/themes/SBP-Legion-Go-Theme"
        git clone https://github.com/frazse/SBP-Legion-Go-Theme.git --single-branch "$HOME/homebrew/themes/SBP-Legion-Go-Theme"
    else
        echo 'Please install Decky Loader & CSS Loader first'
    fi

# Install PS5-to-Xbox glyph theme for hhd & CSS Loader (https://github.com/frazse/PS5-to-Xbox-glyphs)
install-hhd-xbox-glyph-theme:
    #!/usr/bin/bash
    if [ -d "$HOME/homebrew/themes" ]; then
        rm -rf "$HOME/homebrew/themes/PS5-to-Xbox-glyphs"
        git clone https://github.com/frazse/PS5-to-Xbox-glyphs.git --single-branch "$HOME/homebrew/themes/PS5-to-Xbox-glyphs"
    else
        echo 'Please install Decky Loader & CSS Loader first'
    fi

# Remove Decky Loader (note: this will leave plugins and themes behind)
remove-decky:
    #!/usr/bin/bash
    export HOME=$(getent passwd ${SUDO_USER:-$USER} | cut -d: -f6)
    curl -L https://github.com/SteamDeckHomebrew/decky-installer/releases/latest/download/uninstall.sh | sh > /dev/null
    echo 'Decky Loader removed'

# Wipe Decky Loader and the *entire* /homebrew folder it creates, including plugins and themes.
wipe-decky:
    #!/usr/bin/bash
    export HOME=$(getent passwd ${SUDO_USER:-$USER} | cut -d: -f6)
    curl -L https://github.com/SteamDeckHomebrew/decky-installer/releases/latest/download/uninstall.sh | sh > /dev/null
    sudo rm -rf $HOME/homebrew
    echo 'Decky Loader and /homebrew folder removed.'


# Remove SimpleDeckyTDP
remove-simpledeckytdp:
    #!/usr/bin/bash
    if [[ -d $HOME/homebrew/plugins/SimpleDeckyTDP ]]; then
      sudo rm -rf $HOME/homebrew/plugins/SimpleDeckyTDP
      sudo rm -rf $HOME/homebrew/data/SimpleDeckyTDP
      sudo rm -rf $HOME/homebrew/settings/SimpleDeckyTDP
      sudo rm -rf $HOME/homebrew/logs/SimpleDeckyTDP
      echo 'Removed. Please reboot to apply needed changes.'
    else
      echo 'SimpleDeckyTDP is not installed.'
    fi

# Remove HHD Decky Plugin
remove-hhd-decky:
    #!/usr/bin/bash
    if [[ -d $HOME/homebrew/plugins/hhd-decky ]]; then
      sudo rm -rf $HOME/homebrew/plugins/hhd-decky
      echo 'Removed.'
    else
      echo 'HHD Decky Plugin is not installed.'
    fi

# Remove ROG Ally Theme
remove-rog-ally-theme:
    #!/usr/bin/bash
    if [ -d "$HOME/homebrew/themes/SBP-ROG-Ally" ]; then
        rm -rf "$HOME/homebrew/themes/SBP-ROG-Ally"
    else
        echo 'ROG Ally Theme is not installed.'
    fi

# Remove Lenovo Legion Go Theme
remove-legion-go-theme:
    #!/usr/bin/bash
    if [ -d "$HOME/homebrew/themes/SBP-Legion-Go-Theme" ]; then
        rm -rf "$HOME/homebrew/themes/SBP-Legion-Go-Theme"
    else
        echo 'Lenovo Legion Go Theme is not installed.'
    fi

# Remove PS5-to-Xbox glyph theme for hhd & CSS Loader
remove-hhd-xbox-glyph-theme:
    #!/usr/bin/bash
    if [ -d "$HOME/homebrew/themes/PS5-to-Xbox-glyphs" ]; then
        rm -rf "$HOME/homebrew/themes/PS5-to-Xbox-glyphs"
    else
        echo 'PS5-to-Xbox glyph theme is not installed.'
    fi

# Enable BIOS & Firmware update services for the Steam Deck
enable-deck-bios-firmware-updates:
    #!/usr/bin/bash
    SYS_ID="$(cat /sys/devices/virtual/dmi/id/product_name)"
    if [[ ":Jupiter:" =~ ":$SYS_ID:" || ":Galileo:" =~ ":$SYS_ID:" ]]; then
      RESOLUTION=$(sudo lshw -json -c display | jq -r .[]."configuration"."resolution")
        sudo systemctl enable jupiter-biosupdate.service
      fi
      sudo systemctl enable jupiter-controller-update.service
    else
      echo "This is only applicable to Valve's Steam Deck. Aborting..."
    fi

# Disable Steam Deck BIOS updates
disable-bios-updates:
    #!/usr/bin/bash
    sudo systemctl mask --now jupiter-biosupdate.service

# Disable Steam Deck controller firmware updates
disable-firmware-updates:
    #!/usr/bin/bash
    sudo systemctl mask --now jupiter-controller-update.service

# Disable SDGyroDSU
disable-sdgyrodsu:
    #!/usr/bin/bash
    sudo systemctl mask --user sdgyrodsu.service

# Upload Deck edition's Game Mode (gamescope-session) logs to pastebin via pbcli
share-deck-logs:
    #!/usr/bin/bash
    combined_log=$(echo "===== GAMESCOPE CMD LOG ====="; cat $HOME/.gamescope-cmd.log; \
    echo; echo "===== GAMESCOPE STDOUT LOG ====="; cat $HOME/.gamescope-stdout.log)
    link=$(echo "$combined_log" | pbcli)
    echo "Logs uploaded to: $link"
    # Prompt the user after uploading
    read -p "Do you want to copy the link to the clipboard? [y/n] " choice
    if [[ "$choice" =~ ^[Yy]$ ]]; then
        if [[ "$XDG_SESSION_TYPE" == "wayland" ]]; then
            echo "$link" | wl-copy
            echo "Link copied to clipboard using wl-clipboard."
        elif [[ "$XDG_SESSION_TYPE" == "x11" ]]; then
            echo "$link" | xclip -selection clipboard
            echo "Link copied to clipboard using xclip."
        else
            echo "Unable to determine desktop session. Please copy the link manually."
        fi
    else
        echo "Please copy and paste the link manually."
    fi

# Upload hhd logs to pastebin via fpaste
share-hhd-logs:
    #!/usr/bin/bash
    combined_log=$(echo "===== HHD LOG ====="; cat $HOME/.config/hhd/log/hhd.log)
    link=$(echo "$combined_log" | pbcli)
    echo "Log uploaded to: $link"
    # Prompt the user after uploading
    read -p "Do you want to copy the link to the clipboard? [y/n] " choice
    if [[ "$choice" =~ ^[Yy]$ ]]; then
        if [[ "$XDG_SESSION_TYPE" == "wayland" ]]; then
            echo "$link" | wl-copy
            echo "Link copied to clipboard using wl-clipboard."
        elif [[ "$XDG_SESSION_TYPE" == "x11" ]]; then
            echo "$link" | xclip -selection clipboard
            echo "Link copied to clipboard using xclip."
        else
            echo "Unable to determine desktop session. Please copy the link manually."
        fi
    else
        echo "Please copy and paste the link manually."
    fi