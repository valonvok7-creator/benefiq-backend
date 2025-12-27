#!/usr/bin/env bash
set -euo pipefail

shopt -s nullglob
mkdir -p corpus_clean processed

for f in corpus_raw/*.txt; do
  [ -f "$f" ] || continue
  fname=$(basename "$f")
  tmp="corpus_clean/${fname}.tmp"
  out="corpus_clean/$fname"

  sed '/^[[:space:]]*$/d;s/^[[:space:]]*//;s/[[:space:]]*$//' "$f" > "$tmp"

  mv "$tmp" "$out"
  mv "$f" processed/
done
