# vim: set ft=make :

uid := `id -u`
shell := `grep :$(id -u): /etc/passwd | cut -d: -f7`

# Boot into this device's BIOS/UEFI screen
bios:
    systemctl reboot --firmware-setup

# Show all messages from this boot
logs-this-boot:
    sudo journalctl -b 0

# Show all messages from last boot
logs-last-boot:
    sudo journalctl -b -1

# Regenerate GRUB config, useful in dual-boot scenarios where a second operating system isn't listed
update-grub:
    #!/usr/bin/bash
    if [ -d /sys/firmware/efi ]; then
      sudo grub2-mkconfig -o /etc/grub2-efi.cfg
    else
      sudo grub2-mkconfig -o /etc/grub2.cfg
    fi

# Upload Nobara update log (.nobara-sync.log) to pastebin via fpaste
share-update-logs:
    #!/usr/bin/bash
    link=$(cat ~/.nobara-sync.log | fpaste)
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