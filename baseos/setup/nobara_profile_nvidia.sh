#!/usr/bin/sh

# nvidia rendering fixup
if [ -f /bin/lspci ]; then
  nvgpu=$(lspci | grep -iE 'VGA|3D' | grep -i nvidia | cut -d ":" -f 3)
  if [ -n "$nvgpu" ]; then
    export LIBVA_DRIVER_NAME=nvidia
    export MOZ_DISABLE_RDD_SANDBOX=1
    export EGL_PLATFORM="$XDG_SESSION_TYPE"
    export GAMESCOPE_WSI_HIDE_PRESENT_WAIT_EXT=1
    export __EGL_VENDOR_LIBRARY_FILENAMES=/usr/share/glvnd/egl_vendor.d/10_nvidia.json
    export __NV_PRIME_RENDER_OFFLOAD=1
    export __GLX_VENDOR_LIBRARY_NAME=nvidia
  fi
fi
