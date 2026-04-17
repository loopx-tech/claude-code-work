#!/usr/bin/env bash
set -euo pipefail

UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
URLS="${1:-urls.txt}"
OUTDIR="${2:-essays}"
DELAY="${DELAY:-1}"

mkdir -p "$OUTDIR"

total=$(wc -l <"$URLS")
i=0
while IFS= read -r url; do
  i=$((i+1))
  slug=$(basename "$url" .html)
  dest="$OUTDIR/$slug.html"
  if [[ -s "$dest" ]]; then
    echo "[$i/$total] skip $slug (exists)"
    continue
  fi
  echo "[$i/$total] fetch $slug"
  curl -fsSL -A "$UA" "$url" -o "$dest" || { echo "  failed: $url" >&2; rm -f "$dest"; }
  sleep "$DELAY"
done < "$URLS"
