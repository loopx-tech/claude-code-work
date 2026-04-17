#!/usr/bin/env bash
# End-to-end pipeline: index -> urls -> essays -> markdown.
# Run from repo root. Requires: curl, bash, python3, beautifulsoup4.
set -euo pipefail

cd "$(dirname "$0")/.."

scripts/fetch_articles_index.sh articles.html
scripts/extract_urls.sh articles.html urls.txt
scripts/fetch_essays.sh urls.txt essays
python3 scripts/to_markdown.py essays

echo
echo "done. $(ls essays/*.md 2>/dev/null | wc -l) markdown files in essays/"
