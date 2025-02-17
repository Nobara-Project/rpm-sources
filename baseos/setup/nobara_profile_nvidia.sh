#!/usr/bin/sh
# https://bugs.kde.org/show_bug.cgi?id=495260
export KWIN_DRM_DISABLE_TRIPLE_BUFFERING=0

# nvidia rendering fixup
if [ -f /bin/lspci ]; then
  nvgpu=$(lspci | grep -iE 'VGA|3D' | grep -i nvidia | cut -d ":" -f 3)
  if [ -n "$nvgpu" ]; then
    export LIBVA_DRIVER_NAME=nvidia
    export MOZ_DISABLE_RDD_SANDBOX=1
    export EGL_PLATFORM="$XDG_SESSION_TYPE"
    # https://bugs.kde.org/show_bug.cgi?id=488941,
    export KWIN_DRM_ALLOW_NVIDIA_COLORSPACE=1
    export GAMESCOPE_WSI_HIDE_PRESENT_WAIT_EXT=1
  fi
fi
