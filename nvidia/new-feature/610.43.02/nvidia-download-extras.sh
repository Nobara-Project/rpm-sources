#!/bin/bash

if [ ! $1 ]; then
	echo "Usage: ./nvidia-download-extras.sh <version>"
	exit 1;
else
	VERSION="$1"
	MAJOR_VERSION="${VERSION%%.*}"

fi

download()
{
	BASEURL="https://download.nvidia.com/XFree86/$NAME/$NAME-$VERSION.tar.bz2"
	wget $BASEURL -O $NAME-$VERSION.tar.bz2
}

download_kernel_modules()
{
	BASEURL="https://github.com/CachyOS/$NAME/archive/refs/heads/$MAJOR_VERSION-cachyos.tar.gz"
	wget $BASEURL -O $MAJOR_VERSION-cachyos.tar.gz
}

NAME=nvidia-modprobe download
NAME=nvidia-persistenced download
NAME=nvidia-settings download
NAME=open-gpu-kernel-modules download_kernel_modules
