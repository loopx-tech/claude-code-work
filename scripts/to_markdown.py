#!/usr/bin/env python3
"""Convert paulgraham.com essay HTML into markdown.

PG's essays are laid out in nested <table> elements. The essay body is
inside the innermost <font> (or its descendants), with <br><br> for
paragraph breaks. This script extracts that body and writes markdown.

Usage:
    python3 to_markdown.py essays/          # convert all *.html in dir
    python3 to_markdown.py essays/foo.html  # convert single file

Writes <slug>.md alongside each input.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString, Tag  # pip install beautifulsoup4


def extract_title(soup: BeautifulSoup) -> str:
    # Title usually sits in a bold <font size=3> near the top.
    for font in soup.find_all("font"):
        b = font.find("b")
        if b and b.get_text(strip=True):
            return b.get_text(strip=True)
    if soup.title:
        return soup.title.get_text(strip=True)
    return "Untitled"


def find_body(soup: BeautifulSoup) -> Tag | None:
    # The widest <font> with the most text is the essay body.
    candidates = soup.find_all("font")
    if not candidates:
        return None
    return max(candidates, key=lambda f: len(f.get_text(strip=True)))


def node_to_md(node) -> str:
    if isinstance(node, NavigableString):
        return str(node)
    if not isinstance(node, Tag):
        return ""
    name = node.name.lower()
    if name == "br":
        return "\n"
    if name in ("b", "strong"):
        return f"**{''.join(node_to_md(c) for c in node.children)}**"
    if name in ("i", "em"):
        return f"*{''.join(node_to_md(c) for c in node.children)}*"
    if name == "a":
        text = "".join(node_to_md(c) for c in node.children)
        href = node.get("href", "")
        return f"[{text}]({href})" if href else text
    # font/span/other inline wrappers: just descend.
    return "".join(node_to_md(c) for c in node.children)


def html_to_markdown(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    title = extract_title(soup)
    body = find_body(soup)
    if body is None:
        return f"# {title}\n\n(empty body)\n"
    raw = node_to_md(body)
    # Collapse runs of 3+ newlines to paragraph breaks.
    text = re.sub(r"\n{2,}", "\n\n", raw).strip()
    # Drop the title if it appears at the very start (avoid duplication).
    if text.startswith(f"**{title}**"):
        text = text[len(f"**{title}**"):].lstrip()
    return f"# {title}\n\n{text}\n"


def convert_file(path: Path) -> Path:
    md = html_to_markdown(path.read_text(encoding="utf-8", errors="replace"))
    out = path.with_suffix(".md")
    out.write_text(md, encoding="utf-8")
    return out


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(__doc__, file=sys.stderr)
        return 2
    target = Path(argv[1])
    if target.is_dir():
        paths = sorted(target.glob("*.html"))
    else:
        paths = [target]
    for p in paths:
        out = convert_file(p)
        print(f"{p} -> {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
