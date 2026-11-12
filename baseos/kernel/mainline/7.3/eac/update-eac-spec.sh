#!/usr/bin/bash
# Generate kernel-eac.spec from ../kernel.spec: the same spec with nobara_eac
# set to 1. Run it after every change to ../kernel.spec, then build the
# kernel-eac SRPM here with "fedpkg --release f44 srpm".
set -euo pipefail
cd "$(dirname "$(readlink -f "$0")")"
base=../kernel.spec
sha=$(sha256sum "$base" | cut -c1-64)
{
cat <<HDR
# GENERATED from ../kernel.spec by update-eac-spec.sh: don't edit this file.
# Edit ../kernel.spec and rerun ./update-eac-spec.sh.
#
# The sources are the ones in .., next to kernel.spec (fedpkg uses one .spec
# per directory). Rebuilding the SRPM, as COPR does, finds them in SOURCES.
%global _sourcedir %(d="%{_sourcedir}"; [ -f "\$d/genconfig.py" ] || d="\$d/.."; cd "\$d" && pwd)
%global nobara_eac 1
# Refuse to build from a kernel.spec this file wasn't generated from
%global nobara_eac_base_sha256 $sha
%if "%(f="%{_sourcedir}/kernel.spec"; [ -f "\$f" ] && sha256sum "\$f" | cut -c1-64 || echo %{nobara_eac_base_sha256})" != "%{nobara_eac_base_sha256}"
%{error:../kernel.spec changed since kernel-eac.spec was generated: run ./update-eac-spec.sh}
%endif

HDR
cat "$base"
} > kernel-eac.spec.tmp
mv -f kernel-eac.spec.tmp kernel-eac.spec
echo "kernel-eac.spec generated from $base ($sha)"
