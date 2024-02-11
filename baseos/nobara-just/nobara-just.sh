# Add Nobara's justfiles to users with home directories which lack a justfile.

if [ ! -z "$HOME" ] && [ -d "$HOME" ] && [ ! -f "${HOME}/.justfile" ]; then
  cat > "${HOME}/.justfile" << EOF
import "/usr/share/nobara/justfile"
EOF
fi

if [ -f "${HOME}/.justfile" ]; then
  if ! grep -Fxq 'import "/usr/share/nobara/justfile"' "${HOME}/.justfile"; then
    # Remove any lines we may have added previously.
    sed -i '/!include \/usr\/share\/nobara\/just\/.*.just/d' "${HOME}/.justfile"
    sed -i '/!include \/usr\/share\/nobara\/justfile/d' "${HOME}/.justfile"

    # Point to the new main justfile, place it as the first line
    echo '# You can add your own commands here! For documentation, see: https://ublue.it/guide/just/' | tee -a "${HOME}/.justfile"
    echo 'import "/usr/share/nobara/justfile"' | tee -a "${HOME}/.justfile"
  fi
fi
