# claude-code-work

Scraper for paulgraham.com essays.

## Pipeline

```
articles.html  ->  urls.txt  ->  essays/*.html  ->  essays/*.md
```

1. `scripts/fetch_articles_index.sh` — downloads the essay index page.
2. `scripts/extract_urls.sh` — parses it into `urls.txt`.
3. `scripts/fetch_essays.sh` — downloads each essay as HTML (1s delay, skips existing).
4. `scripts/to_markdown.py` — converts each `essays/*.html` to `essays/*.md`.
5. `scripts/run_all.sh` — runs the whole pipeline.

## Requirements

- `bash`, `curl`, `grep`, `sed`, `awk`
- `python3` with `beautifulsoup4` (`pip install beautifulsoup4`)

## Usage

```bash
scripts/run_all.sh
```

Re-runs are safe: existing essay HTML files are skipped.

## Sandbox note

This repo was first set up inside the Claude Code web sandbox, which
blocks outbound traffic to paulgraham.com at the network layer
(`x-deny-reason: host_not_allowed`). The scripts therefore must be run
from an environment with unrestricted internet access (local machine,
CI runner, etc.). See `/root/.claude/plans/hey-are-you-on-gentle-sloth.md`
for the original plan.
