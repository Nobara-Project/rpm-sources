#!/bin/bash

# Script to identify trivial new headers for new sources added
# Requires: bash, coreutils, tar, xz
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


FFMPEG_VERSION=$1
FF_SRC_DIFF=$2

if [ -z $1 -o -z $2 ]; then
	echo "No arguments provided, quitting!"
	exit 1
fi

echo "Setting up..."
# Get local directory
LOCALDIR=$(realpath $(dirname $0))

# Create working area
TMPDIR=$(mktemp -d /tmp/ffsrchdrsXXXXXX)
mkdir -pv $TMPDIR

# Extract ffmpeg sources
if [ ! -f "ffmpeg-${FFMPEG_VERSION}.tar.xz" ]; then
	echo "No ffmpeg tarball, exiting!"
	exit 2
fi
if [ ! -f "$FF_SRC_DIFF" ]; then
	echo "No ffmpeg sources diff, exiting!"
	exit 2
fi
echo "Extracting upstream ffmpeg sources..."
tar -C ${TMPDIR} -xf ffmpeg-${FFMPEG_VERSION}.tar.xz

echo "Generating header list from diff..."
# Read in ffmpeg_free_sources diff
while IFS= read -r line
do
	if [[ $line = \+* ]]; then
		ffmpeg_src_file="${line:1}"
		if [ -f "${TMPDIR}/ffmpeg-${FFMPEG_VERSION}/${ffmpeg_src_file}" ]; then
			ffmpeg_hdr_file="${ffmpeg_src_file%.c}.h"
			[ -f "${TMPDIR}/ffmpeg-${FFMPEG_VERSION}/${ffmpeg_hdr_file}" ] && echo "${ffmpeg_hdr_file}" >> ${LOCALDIR}/ffmpeg_free_sources
			ffmpeg_hdr_file="${ffmpeg_src_file%.c}_cb.h"
			[ -f "${TMPDIR}/ffmpeg-${FFMPEG_VERSION}/${ffmpeg_hdr_file}" ] && echo "${ffmpeg_hdr_file}" >> ${LOCALDIR}/ffmpeg_free_sources
			ffmpeg_hdr_file="${ffmpeg_src_file%.c}data.h"
			[ -f "${TMPDIR}/ffmpeg-${FFMPEG_VERSION}/${ffmpeg_hdr_file}" ] && echo "${ffmpeg_hdr_file}" >> ${LOCALDIR}/ffmpeg_free_sources
			ffmpeg_hdr_file="${ffmpeg_src_file%.c}_data.h"
			[ -f "${TMPDIR}/ffmpeg-${FFMPEG_VERSION}/${ffmpeg_hdr_file}" ] && echo "${ffmpeg_hdr_file}" >> ${LOCALDIR}/ffmpeg_free_sources
			ffmpeg_hdr_file="${ffmpeg_src_file%.c}_tablegen.h"
			[ -f "${TMPDIR}/ffmpeg-${FFMPEG_VERSION}/${ffmpeg_hdr_file}" ] && echo "${ffmpeg_hdr_file}" >> ${LOCALDIR}/ffmpeg_free_sources
		fi
	fi
done < <(cat $FF_SRC_DIFF)

# Clean up
echo "Clean up workspace..."
rm -rf ${TMPDIR}
