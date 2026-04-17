#!/usr/bin/env bash
set -euo pipefail

IN="${1:-articles.html}"
OUT="${2:-urls.txt}"

# PG essays are linked as relative .html paths from articles.html.
# Skip the index page itself and any anchor-only links.
grep -oEi 'href="[^"#]+\.html"' "$IN" \
  | sed -E 's/^href="//; s/"$//' \
  | grep -viE '^(articles|index|rss|https?:)' \
  | awk '!seen[$0]++' \
  | sed 's|^|https://paulgraham.com/|' \
  > "$OUT"

echo "wrote $OUT ($(wc -l <"$OUT") urls)"
