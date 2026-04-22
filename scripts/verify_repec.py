#!/usr/bin/env python
"""Cross-check the catalogue against an author's RePEc/IDEAS profile.

RePEc lists WPs under their proper series (CEPR DP, NBER WP, IZA DP,
CESifo WP, …) and published articles with journal and year. That makes
it the cleanest source for verifying:
  - whether we have an author's real published-paper list
  - whether a WP is in a qualifying series (CEPR / NBER / IZA / CESifo)

This tool takes an author_id (with `repec_id` in the author JSON, or
passed as the 2nd arg) and prints a diff against `data/papers/`. It
does not modify any files — output guides the editor.

Usage:
  python scripts/verify_repec.py bekes-gabor
  python scripts/verify_repec.py attila-lindner pli582
  python scripts/verify_repec.py bekes-gabor --show-all
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.request import Request, urlopen

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).parent.parent
AUTHORS_DIR = ROOT / "data" / "authors"
PAPERS_DIR = ROOT / "data" / "papers"

# RePEc uses ISO-8859-1 sometimes; we read as latin1 and decode-fix on demand.
UA = "EvidenceForHungary/0.1 (mailto:bekesg@ceu.edu)"

QUALIFYING_WP_SERIES = {
    "cpr/ceprdp": "CEPR",
    "nbr/nberwo": "NBER",
    "iza/izadps": "IZA",
    "ces/ceswps": "CESifo",
}


def fetch(repec_id: str) -> str:
    url = f"https://ideas.repec.org/e/{repec_id}.html"
    req = Request(url, headers={"User-Agent": UA})
    raw = urlopen(req, timeout=30).read()
    # RePEc personal pages are often latin1-encoded with Hungarian accents
    # broken. Try utf-8 first, fall back to latin1.
    for enc in ("utf-8", "latin-1", "cp1252"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace")


def _strip_tags(s: str) -> str:
    return re.sub(r"<[^>]+>", "", s).strip()


def _section(html: str, header: str) -> str | None:
    """Extract the <OL> list following a given <h*>HEADER</h*>."""
    m = re.search(
        rf"(?is)<h[234][^>]*>\s*{re.escape(header)}\s*</h[234]>\s*(<OL.*?</OL>)",
        html,
    )
    return m.group(1) if m else None


def _split_items(ol: str) -> list[str]:
    """Split an <OL> into top-level <LI> item blocks (excluding nested list items
    in otherversion divs)."""
    # Find all <LI class="list-group-item down...">...  that are at the OL
    # top level. Strategy: split on <LI class="list-group-item down and keep
    # each chunk, filter to those that start with an article item.
    parts = re.split(r'(?=<LI class="list-group-item down(?:free|gate)">)', ol)
    return [p for p in parts if p.strip().startswith("<LI")]


def _parse_article_item(li: str) -> dict | None:
    """Parse one top-level <LI> from the Articles section."""
    # The OUTER article — take only the portion before <div class="otherversion">
    outer = re.split(r'(?i)<div\s+class="otherversion"', li, maxsplit=1)[0]
    # Year is in "Name, YYYY." before the title
    yr = re.search(r",\s*(19|20)\d{2}\.", outer)
    year = int(yr.group(0).strip(", .")) if yr else None
    # Title in <B><A href=/a/...>TITLE</A></B>
    t = re.search(r'<B>\s*<A\s+HREF="/a/[^"]+">\s*(.+?)\s*</A>\s*</B>', outer, re.S)
    title = _strip_tags(t.group(1)) if t else ""
    # Journal: first <A HREF="/s/..."> link
    j = re.search(r'<A\s+HREF="/s/[^"]+">\s*(.+?)\s*</A>', outer, re.S)
    journal = _strip_tags(j.group(1)) if j else ""
    if not title:
        return None
    return {"title": title, "journal": journal, "year": year}


def _parse_wp_item(li: str) -> dict | None:
    """Parse one <LI> from the Working Papers section."""
    outer = re.split(r'(?i)<div\s+class="otherversion"', li, maxsplit=1)[0]
    yr = re.search(r",\s*(19|20)\d{2}\.", outer)
    year = int(yr.group(0).strip(", .")) if yr else None
    t = re.search(r'<B>\s*<A\s+HREF="/p/([^"]+?)"[^>]*>\s*(.+?)\s*</A>\s*</B>', outer, re.S)
    if not t:
        return None
    paper_path, title = t.group(1), _strip_tags(t.group(2))
    # Series: paper_path looks like "cpr/ceprdp/17924" — first two components
    series_key = "/".join(paper_path.split("/")[:2])
    series_full = ""
    s = re.search(r'<A\s+HREF="/s/[^"]+">\s*(.+?)\s*</A>', outer, re.S)
    if s:
        series_full = _strip_tags(s.group(1))
    return {
        "title": title,
        "series_key": series_key,
        "series": series_full,
        "year": year,
        "qualifying": QUALIFYING_WP_SERIES.get(series_key),
    }


def _norm_title(t: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", (t or "").lower()).strip()


def parse_articles(html: str) -> list[dict]:
    ol = _section(html, "Articles")
    if not ol:
        return []
    return [a for a in (_parse_article_item(li) for li in _split_items(ol)) if a]


def parse_wps(html: str) -> list[dict]:
    ol = _section(html, "Working papers")
    if not ol:
        return []
    return [w for w in (_parse_wp_item(li) for li in _split_items(ol)) if w]


def catalogue_papers(author_id: str) -> list[dict]:
    out = []
    for p in PAPERS_DIR.glob("*.json"):
        d = json.loads(p.read_text(encoding="utf-8"))
        if author_id in (d.get("authors") or []):
            out.append(d)
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("author_id")
    ap.add_argument("repec_id", nargs="?", default=None)
    ap.add_argument("--show-all", action="store_true",
                    help="Show found articles even if we already have them.")
    args = ap.parse_args()

    ap_path = AUTHORS_DIR / f"{args.author_id}.json"
    if not ap_path.exists():
        sys.exit(f"No author JSON at {ap_path}")
    a = json.loads(ap_path.read_text(encoding="utf-8"))
    repec = args.repec_id or a.get("repec_id")
    if not repec:
        sys.exit(f"No repec_id on {args.author_id}. Pass one as 2nd arg.")

    print(f"=== {a.get('name_en') or args.author_id} — RePEc: {repec} ===\n")
    html = fetch(repec)

    arts = parse_articles(html)
    wps = parse_wps(html)
    print(f"RePEc: {len(arts)} articles, {len(wps)} working papers.\n")

    have = catalogue_papers(args.author_id)
    have_titles = {_norm_title(p.get("title", "")): p["id"] for p in have}

    def match(title: str) -> str | None:
        key = _norm_title(title)
        if not key:
            return None
        if key in have_titles:
            return have_titles[key]
        for t, pid in have_titles.items():
            if (key in t and len(key) >= 20) or (t in key and len(t) >= 20):
                return pid
        return None

    missing_arts = []
    have_arts = []
    for art in arts:
        hit = match(art["title"])
        (have_arts if hit else missing_arts).append((art, hit))

    print(f"Articles in catalogue: {len(have_arts)}")
    print(f"Articles possibly missing: {len(missing_arts)}\n")

    if missing_arts:
        print("-- MISSING ARTICLES --")
        for art, _ in missing_arts[:50]:
            y = art["year"] or "?"
            j = (art["journal"] or "")[:35]
            t = art["title"][:80]
            print(f"  {y} | {j:35s} | {t}")
        print()

    qualifying_wps = [w for w in wps if w["qualifying"]]
    print(f"Working papers in a qualifying series (CEPR/NBER/IZA/CESifo): "
          f"{len(qualifying_wps)}")
    if qualifying_wps:
        print("-- QUALIFYING WPs (potentially to add if year ≥ 2023 and not "
              "already published) --")
        for w in qualifying_wps:
            qual = w["qualifying"]
            y = w["year"] or "?"
            t = w["title"][:80]
            hit = match(w["title"])
            tag = f"(have: {hit})" if hit else "(missing)"
            print(f"  {y} | {qual:6s} | {t} {tag}")

    if args.show_all:
        print("\n-- HAVE (articles already in catalogue) --")
        for art, pid in have_arts:
            y = art["year"] or "?"
            t = art["title"][:70]
            print(f"  {y} | {pid:45s} | {t}")


if __name__ == "__main__":
    main()
