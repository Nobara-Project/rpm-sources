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
regenerate-grub:
    #!/usr/bin/bash
    if [ -d /sys/firmware/efi ]; then
      sudo grub2-mkconfig -o /etc/grub2-efi.cfg
    else
      sudo grub2-mkconfig -o /etc/grub2.cfg
    fi

# Upload Nobara update log (.nobara-sync.log) to pastebin via fpaste
upload-nsync-logs:
    cat ~/.nobara-sync.log | fpaste
    echo 'Log uploaded. Please copy and paste the link by right clicking or by highlighting the link and using Ctrl + Shift + C.'