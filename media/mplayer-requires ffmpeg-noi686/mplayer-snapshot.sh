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
svn=$(date +%Y-%m-%d)
#svn=2019-04-16
dirname=mplayer-export-$svn
mplayer_rev={$svn}
#mplayer_rev=HEAD

cd "$tmp"
svn checkout -r ${mplayer_rev} svn://svn.mplayerhq.hu/mplayer/trunk $dirname
cd $dirname

svn_revision=`LC_ALL=C svn info 2> /dev/null | grep Revision | cut -d' ' -f2`
sed -i -e 's/\(SVN-r[0-9]* \)/\1rpmfusion /' -e "s/UNKNOWN/SVN-r$svn_revision/" version.sh
find . -type d -name .svn -print0 | xargs -0r rm -rf
cd ..
tar Jcf "$pwd"/$dirname.tar.xz $dirname
cd - >/dev/null
