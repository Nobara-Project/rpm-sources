#!/bin/bash
# Wrapper script for find-debuginfo.sh
#
# Usage:
#  wrap-find-debuginfo.sh LDSO-PATH SCRIPT-PATH SCRIPT-ARGS...
#
# The wrapper saves the original versions of the file at LDSO-PATH,
# invokes SCRIPT-PATH with SCRIPT-ARGS, and then restores the
# LDSO-PATH file.  As a result, LDSO-PATH has unchanged debuginfo even
# after debuginfo extraction.

set -ex

ldso_tmp="$(mktemp)"

# Prefer a separately installed debugedit over the RPM-integrated one.
if command -v debugedit >/dev/null ; then
    debugedit=debugedit
else
    debugedit=/usr/lib/rpm/debugedit
fi

cleanup () {
    rm -f "$ldso_tmp"
}
trap cleanup 0

ldso_path="$1"
shift
script_path="$1"
shift

# Preserve the original file.
cp "$ldso_path" "$ldso_tmp"

# Run the debuginfo extraction.
"$script_path" "$@"

# Restore the original file.
cp "$ldso_tmp" "$ldso_path"

# Reduce the size of notes.  Primarily for annobin.
objcopy --merge-notes "$ldso_path"

# Rewrite the source file paths to match the extracted locations.
# First compute the arguments for invoking debugedit.  See
# find-debuginfo.sh.
debug_dest_name="/usr/src/debug"
last_arg=
while true ; do
    arg="$1"
    shift || break
    case "$arg" in
	(--unique-debug-src-base)
	    debug_dest_name="/usr/src/debug/$1"
	    shift
	    ;;
	(-*)
	    ;;
	(*)
	    last_arg="$arg"
	    ;;
    esac
done
debug_base_name=${last_arg:-$RPM_BUILD_ROOT}
$debugedit -b "$debug_base_name" -d "$debug_dest_name" -n $ldso_path

# Apply single-file DWARF optimization.
dwz $ldso_path
