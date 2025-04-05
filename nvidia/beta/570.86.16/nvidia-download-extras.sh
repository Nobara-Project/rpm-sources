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

NAME=nvidia-modprobe download
NAME=nvidia-persistenced download
NAME=nvidia-settings download
NAME=nvidia-xconfig download
NAME=open-gpu-kernel-modules download


