#!/usr/bin/sh

# this is a hack to allow steam input kb+ mouse emulation to work on wayland without prompting the user a million times to allow input in kde
flatpak permission-set kde-authorized remote-desktop "" yes
