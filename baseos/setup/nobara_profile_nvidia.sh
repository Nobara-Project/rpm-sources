#!/usr/bin/sh

# nvidia rendering fixup
if [ -f /bin/lspci ]; then
  nvgpu=$(lspci | grep -iE 'VGA|3D' | grep -i nvidia | cut -d ":" -f 3)
  if [ -n "$nvgpu" ]; then
    export EGL_PLATFORM="$XDG_SESSION_TYPE"
    export GAMESCOPE_WSI_HIDE_PRESENT_WAIT_EXT=1
  fi
fi
