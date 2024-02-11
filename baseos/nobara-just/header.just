set allow-duplicate-recipes := true
set ignore-comments := true

_default:
    #!/usr/bin/bash
    source /usr/lib/ujust/libformatting.sh
    echo "$(Urllink "https://nobaraproject.org/docs/faq/faq/" "Click here to view the Nobara Steamdeck Edition just documentation")"
    /usr/bin/ujust --list --list-heading $'Available commands:\n' --list-prefix $' - '

# Imports
