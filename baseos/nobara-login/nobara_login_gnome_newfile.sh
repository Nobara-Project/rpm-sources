#!/usr/bin/sh

# fix gnome missing 'New file' option
if [ ! -f "$HOME/Templates/Text file" ]
then
    mkdir -p "$HOME/Templates"
    touch "$HOME/Templates/Text file"
fi
