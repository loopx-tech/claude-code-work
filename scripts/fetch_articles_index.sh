#!/usr/bin/env bash
set -euo pipefail

UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
OUT="${1:-articles.html}"

curl -fsSL -A "$UA" https://paulgraham.com/articles.html -o "$OUT"
echo "wrote $OUT ($(wc -c <"$OUT") bytes)"
