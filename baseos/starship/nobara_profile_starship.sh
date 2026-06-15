if test "$BASH"; then
    if command -v starship &>/dev/null; then
        if [ ! -f $HOME/.config/starship.toml ]; then
            if [ -f /usr/share/starship/starship.toml ]; then
                mkdir -p $HOME/.config
                cp /usr/share/starship/starship.toml $HOME/.config/
            fi
        fi
    fi
    eval "$(starship init bash)"
fi
