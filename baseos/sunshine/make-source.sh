#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"
version=$(rpmspec -q --qf '%{VERSION}' sunshine.spec)
workdir=$(mktemp -d)
trap 'rm -rf "$workdir"' EXIT

git clone --depth 1 --branch "v${version}" --recurse-submodules --shallow-submodules \
  https://github.com/LizardByte/Sunshine.git "$workdir/Sunshine-${version}"

# Sunshine uses prebuilt FFmpeg libraries; only the nested Vulkan headers are
# needed from build-deps. Exclude the other FFmpeg source trees from the RPM.
tar --exclude-vcs \
  --exclude="Sunshine-${version}/third-party/build-deps/third-party/FFmpeg/AMF" \
  --exclude="Sunshine-${version}/third-party/build-deps/third-party/FFmpeg/FFmpeg" \
  --exclude="Sunshine-${version}/third-party/build-deps/third-party/FFmpeg/SVT-AV1" \
  --exclude="Sunshine-${version}/third-party/build-deps/third-party/FFmpeg/Vulkan-Loader" \
  --exclude="Sunshine-${version}/third-party/build-deps/third-party/FFmpeg/x264" \
  --exclude="Sunshine-${version}/third-party/build-deps/third-party/FFmpeg/x265_git" \
  -C "$workdir" -czf "sunshine-${version}-vendored.tar.gz" \
  "Sunshine-${version}"
