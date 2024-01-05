#!/bin/bash

# Script to grab headers from existing packages to support dlopen() codec libraries
# Requires: bash, coreutils, curl, bsdtar, dnf, dnf-plugins-core, tar, xz
# Author: Neal Gompa <ngompa@fedoraproject.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

echo "Setting up..."
# Get local directory
LOCALDIR=$(realpath $(dirname $0))

# Create working area
TMPDIR=$(mktemp -d /tmp/mmheadersXXXXXX)
mkdir -pv $TMPDIR

echo "Fetching headers..."
# Get OpenH264 headers
OPENH264_DEVEL=$(dnf -q download --url 'pkgconfig(openh264)')
curl -L $OPENH264_DEVEL | bsdtar -xvf - --include "./usr/include/*" -C $TMPDIR

echo "Generating tarball..."
# Prep tarball tree
mv -v ${TMPDIR}/usr ${TMPDIR}/ffdlopenhdrs
# Generate tarball
tar --transform "s|^${TMPDIR#?}/||" -cJvf ${LOCALDIR}/ffmpeg-dlopen-headers.tar.xz ${TMPDIR}/ffdlopenhdrs
# Clean up
echo "Cleaning up..."
rm -rfv ${TMPDIR}

echo "Tarball created: ${LOCALDIR}/ffmpeg-dlopen-headers.tar.xz"
