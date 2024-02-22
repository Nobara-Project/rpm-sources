set allow-duplicate-recipes := true
set ignore-comments := true

_default:
    #!/usr/bin/bash
    source /usr/lib/njust/libformatting.sh
    echo "Welcome to Nobara's njust shortcut system! All just files are sourced from here: /usr/share/nobara/just. If you have any suggestions, drop them in the Discord server's #nobara channel!
    /usr/bin/njust --list --list-heading $'Available commands:\n' --list-prefix $' - '

# Imports
