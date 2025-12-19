#!/bin/bash

if [ ! $1 ]; then
	echo "Usage: ./nvidia-download-extras.sh <version>"
	exit 1;
else
	VERSION="$1"
fi

download()
{
	BASEURL="https://download.nvidia.com/XFree86/$NAME/$NAME-$VERSION.tar.bz2"
	wget $BASEURL -O $NAME-$VERSION.tar.bz2
}

download_kernel_module()
{
	BASEURL="https://github.com/NVIDIA/open-gpu-kernel-modules/archive/$VERSION/open-gpu-kernel-modules-$VERSION.tar.gz"
	wget $BASEURL
}

NAME=nvidia-modprobe download
NAME=nvidia-persistenced download
NAME=nvidia-settings download
download_kernel_module
