#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 || $# -gt 2 ]]; then
  echo "Usage: $0 <new_prefix> [root_dir]" >&2
  echo "Example: $0 6        # updates under current dir" >&2
  echo "Example: $0 6 /path  # updates under /path" >&2
  exit 2
fi

NEW_PREFIX="$1"
ROOT="${2:-.}"

# Portable sed in-place:
# GNU sed: sed -i ...
# BSD/macOS sed: sed -i '' ...
if sed --version >/dev/null 2>&1; then
  SED_INPLACE=(sed -i -E)
else
  SED_INPLACE=(sed -i '' -E)
fi

# Match: one or more digits right before %{?dist}
# Replace with: NEW_PREFIX%{?dist}
# (This targets patterns like 3%{?dist}, 12%{?dist}, etc.)
find "$ROOT" -type f -name '*.spec' -print0 |
while IFS= read -r -d '' file; do
  if grep -Eq '[0-9]+%\{\?dist\}' "$file"; then
    "${SED_INPLACE[@]}" "s/[0-9]+%\\{\\?dist\\}/${NEW_PREFIX}%{?dist}/g" "$file"
    echo "updated: $file"
  fi
done

