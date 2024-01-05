#!/bin/bash
#
# Copyright (c) 2022      Andreas Schneider <asn@cryptomilk.org>
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
#
# shellcheck disable=2181

export LC_COLLATE="C.UTF-8"

FF_PKGNAME="ffmpeg"
FF_PKGNAME_SUFFIX="-free"
FF_VERSION="$(rpmspec -P ./*.spec | grep ^Version | sed -e 's/Version:[ ]*//g')"
FF_TARBALL_URL="https://ffmpeg.org/releases/${FF_PKGNAME}-${FF_VERSION}.tar.xz"
FF_TARBALL="$(basename "${FF_TARBALL_URL}")"
FF_GPG_ARMOR_FILE="${FF_TARBALL}.asc"
FF_PKG_DIR="$(pwd)"
FF_KEYRING="${FF_PKG_DIR}/ffmpeg.keyring"
FF_TMPDIR=$(mktemp --tmpdir -d ffmpeg-XXXXXXXX)
FF_PATH="${FF_TMPDIR}/${FF_PKGNAME}-${FF_VERSION}"

cleanup_tmpdir() {
    # shellcheck disable=2164
    popd 2>/dev/null
    rm -rf "${FF_TMPDIR}"
}
trap cleanup_tmpdir SIGINT

cleanup_and_exit()
{
    cleanup_tmpdir

    if test "$1" = 0 -o -z "$1"; then
        exit 0
    else
        # shellcheck disable=2086
        exit ${1}
    fi
}

if [[ ! -w "${FF_TARBALL}" ]]; then
    echo ">>> Downloading tarball"
    wget "${FF_TARBALL_URL}"
fi
if [[ ! -w "${FF_TARBALL}.asc" ]]; then
    echo ">>> Downloading signature"
    wget "${FF_TARBALL_URL}.asc"
fi

echo ">>> Verifying ${FF_TARBALL} GPG signature"
gpgv2 --quiet --keyring "${FF_KEYRING}" "${FF_GPG_ARMOR_FILE}" "${FF_TARBALL}"
if [ $? -ne 0 ]; then
    echo "ERROR: GPG signature verification failed"
    cleanup_and_exit 1
fi
echo

echo ">>> Unpacking ${FF_TARBALL}"

tar -xf "${FF_TARBALL}" -C "${FF_TMPDIR}"
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to unpack ${FF_TARBALL}"
    cleanup_and_exit 1
fi

if [[ ! -r ffmpeg_free_sources ]]; then
    echo "ERROR: ffmpeg_free_sources doesn't exist!"
    cleanup_and_exit 1
fi
readarray -t keepfiles < ffmpeg_free_sources

pushd "${FF_PATH}" || cleanup_and_exit 1

echo
echo ">>> Cleaning up sources for new tarball ..."

# Get file list from ffmpeg
mapfile -d '' filelist < <(find ./ -type f -printf '%P\0')

# Sort arrays
readarray -t keepfiles_sorted < <(printf '%s\0' "${keepfiles[@]}" | sort -z | xargs -0n1)
readarray -t filelist_sorted < <(printf '%s\0' "${filelist[@]}" | sort -z | xargs -0n1)

# Compare arrays and remove files which are left over
comm -2 -3 -z <(printf '%s\0' "${filelist_sorted[@]}") <(printf '%s\0' "${keepfiles_sorted[@]}") | xargs -0 rm -f

readarray -t removed_files < <(comm -1 -3 -z <(printf '%s\0' "${filelist_sorted[@]}") <(printf '%s\0' "${keepfiles_sorted[@]}") | xargs -0n1)
if [[ "${#removed_files[@]}" -ge 1 ]]; then
    if [[ "${#removed_files[@]}" -eq 1 ]] && [[ -z "${removed_files[0]}" ]]; then
        echo "... done"
    else
        echo "File not in upstream tarball anymore (please cleanup 'ffmpeg_free_sources'):"
        for f in "${removed_files[@]}"; do
            if [[ -z "${f}" ]]; then
                continue
            fi
            echo "  * ${f}"
        done
    fi
fi
echo

popd || cleanup_and_exit 1 # /FF_PATH

pushd "${FF_TMPDIR}" || cleanup_and_exit 1

echo ">>> Create new tarball ${FF_PKGNAME}${FF_PKGNAME_SUFFIX}-${FF_VERSION}.tar.xz ..."
tar -cJf "${FF_PKG_DIR}/${FF_PKGNAME}${FF_PKGNAME_SUFFIX}-${FF_VERSION}.tar.xz" "${FF_PKGNAME}-${FF_VERSION}"
if [ $? -ne 0 ]; then
    echo "ERROR: Creating tarball failed"
    cleanup_and_exit 1
fi

popd || cleanup_and_exit 1 # /FF_TMPDIR

du -sh "${FF_PKGNAME}${FF_PKGNAME_SUFFIX}-${FF_VERSION}.tar.xz"
echo

cleanup_and_exit 0
