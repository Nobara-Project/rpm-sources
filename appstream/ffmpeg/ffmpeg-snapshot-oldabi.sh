#!/bin/bash

set -e

tmp=$(mktemp -d)

trap cleanup EXIT
cleanup() {
    set +e
    [ -z "$tmp" -o ! -d "$tmp" ] || rm -rf "$tmp"
}

unset CDPATH
pwd=$(pwd)
date=$(date +%Y%m%d)

pushd "$tmp"
git clone git://git.videolan.org/ffmpeg.git -b oldabi
cd ffmpeg
git archive --prefix="ffmpeg-oldabi-${date}/" --format=tar oldabi | bzip2 > "$pwd"/ffmpeg-oldabi-${date}.tar.bz2
popd
