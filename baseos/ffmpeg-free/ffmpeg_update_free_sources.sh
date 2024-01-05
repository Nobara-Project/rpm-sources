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

cleanup_and_exit()
{
    if test "$1" = 0 -o -z "$1"; then
        exit 0
    else
        # shellcheck disable=2086
        exit ${1}
    fi
}

echo ">>> Collect information from ${1}"
build_log="$(readlink -f "${1}")"
if [[ -z "${build_log}" ]] || [[ ! -r "${build_log}" ]]; then
    echo "Build log doesn't exist: %{build_log}"
    cleanup_and_exit 1
fi

asm_files="$(grep "^gcc.*\.c$" "${build_log}" | awk 'NF>1{print $NF}' | sort)"
c_files="$(grep "^nasm.*\.asm$" "${build_log}" | awk 'NF>1{print $NF}' | sort)"

# shellcheck disable=2206
new_sources=(${asm_files}
             ${c_files})

# Sort arrays
readarray -t new_sources_sorted < <(printf '%s\0' "${new_sources[@]}" | sort -z | xargs -0n1)

# Create a backup for a diff
cp -a ffmpeg_free_sources ffmpeg_free_sources.orig
cp -a ffmpeg_free_sources ffmpeg_free_sources.new
printf "%s\n" "${new_sources_sorted[@]}" >> ffmpeg_free_sources.new
# Update ffmpeg_free_sources
echo ">>> Updating ffmpeg_free_sources"
sort < ffmpeg_free_sources.new | uniq | sed '/^$/d' > ffmpeg_free_sources
echo ">>> Differences in file list"
diff -u ffmpeg_free_sources.orig ffmpeg_free_sources
rm -f ffmpeg_free_sources.new

cleanup_and_exit 0
