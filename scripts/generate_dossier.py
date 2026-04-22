#!/usr/bin/env python
"""Generate an author outreach dossier (Markdown) for editorial review.

The dossier is a single self-contained Markdown file with everything the
site shows about one author — bio, affiliations, per-paper summaries and
tags — plus instructions for the author to edit and return. The returned
file drops into `submissions/YYYY-MM-DD-<surname>.md` and is processed by
the existing author-correction workflow (see `submissions/README.md`).

Output goes to `outreach/<author_id>.md` (gitignored).

Usage:
  python scripts/generate_dossier.py <author_id>
  python scripts/generate_dossier.py bekes-gabor
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
DATA = ROOT / "data"
AUTHORS_DIR = DATA / "authors"
PAPERS_DIR = DATA / "papers"
OUT_DIR = ROOT / "outreach"

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass


def load(p: Path) -> dict:
    return json.loads(p.read_text(encoding="utf-8"))


def _load_coauthor_lookup() -> dict[str, str]:
    """author_id → display name, for rendering paper author lines."""
    out = {}
    for p in AUTHORS_DIR.glob("*.json"):
        a = load(p)
        out[a["id"]] = a.get("name_en") or a.get("name_hu") or a["id"]
    return out


def _author_name(aid_or_name: str, lookup: dict[str, str]) -> str:
    return lookup.get(aid_or_name, aid_or_name)


def _fmt_tags(p: dict) -> str:
    bits = []
    for key in ("topics", "methods", "data_types", "countries_studied"):
        vals = p.get(key) or []
        if vals:
            bits.append(f"{key}: {', '.join(vals)}")
    pi = p.get("policy_instruments") or []
    if pi:
        bits.append(f"policy_instruments: {', '.join(pi)}")
    return " | ".join(bits) if bits else "(none set)"


def _fmt_affiliations(affs: list) -> str:
    if not affs:
        return "_(none listed)_"
    lines = []
    for a in affs:
        name = a.get("name", "")
        role = a.get("role")
        start = a.get("start")
        extras = " ".join(filter(None, [
            f"— {role}" if role else None,
            f"(from {start})" if start else None,
        ]))
        lines.append(f"- {name} {extras}".rstrip())
    return "\n".join(lines)


def render_dossier(author_id: str) -> str:
    author_path = AUTHORS_DIR / f"{author_id}.json"
    if not author_path.exists():
        raise SystemExit(f"No author file at {author_path}")
    a = load(author_path)
    coauthors = _load_coauthor_lookup()

    papers = sorted(
        (load(p) for p in PAPERS_DIR.glob("*.json")),
        key=lambda p: -(p.get("year") or 0),
    )
    mine = [p for p in papers if author_id in (p.get("authors") or [])]

    name_en = a.get("name_en") or author_id
    name_hu = a.get("name_hu") or ""
    n = len(mine)

    lines = [
        f"# Dossier — {name_en}",
        "",
        f"_For: {name_en}_  ",
        f"_Catalogue: Evidence for Hungary / Magyar Közgazdászok_  ",
        f"_Editor: Gábor Békés — bekesg@ceu.edu_",
        "",
        "---",
        "",
        f"Dear {name_en.split()[0]},",
        "",
        "You are listed in **Evidence for Hungary** (*Magyar Közgazdászok*), "
        "a curated, policy-facing catalogue of research by top Hungarian "
        "economists and the Hungarian diaspora — built for Hungarian "
        "ministry staff and analysts.",
        "",
        "Below is **everything we currently have about you and your papers**. "
        "Please review and send corrections. Three ways to reply, whichever "
        "is easiest:",
        "",
        "1. Edit this file inline and send it back as an email attachment "
        "or paste;",
        "2. Reply with a bulleted list of changes;",
        "3. Write a short prose note — e.g. \"replace the bio with: …\" or "
        "\"drop paper X, add paper Y (DOI …), and reword the policy "
        "relevance of Z to …\".",
        "",
        "**One language is enough.** If you edit only the English, we leave "
        "the Hungarian alone (and vice versa). Flag anywhere you want us to "
        "translate across.",
        "",
        "A few things worth checking specifically:",
        "",
        "- Bio — accurate? phrased the way you'd phrase it?",
        "- Affiliations — current?",
        "- Paper list — complete? missing anything? any paper you'd rather "
        "not feature?",
        "- Non-technical summaries — land for a smart non-economist reader?",
        "- Tags (topics / methods / policy instruments) — fit? too broad?",
        "- If you want a short \"Open to media\" note on your page, tell "
        "us — default is off.",
        "",
        "Return to **bekesg@ceu.edu**. Thanks in advance.",
        "",
        "---",
        "",
        "## Your profile",
        "",
        f"- **Name (English):** {name_en}",
        f"- **Name (Hungarian):** {name_hu or '_(not set)_'}",
        f"- **Website:** {a.get('website') or '_(not set)_'}",
        f"- **RePEc:** {a.get('repec_id') or '_(not set)_'}   "
        f"**Google Scholar:** {a.get('scholar_id') or '_(not set)_'}   "
        f"**ORCID:** {a.get('orcid') or '_(not set)_'}",
        f"- **Primary fields:** {', '.join(a.get('primary_fields') or []) or '_(none set)_'}",
        "",
        "**Affiliations**",
        "",
        _fmt_affiliations(a.get("affiliations") or []),
        "",
        "### Bio — English",
        "",
        (a.get("bio_en") or "_(no English bio yet — please provide one, "
         "3–4 sentences, third person)_"),
        "",
        "### Bio — Hungarian",
        "",
        (a.get("bio_hu") or "_(no Hungarian bio yet — "
         "ha szeretnél, írj egyet 3–4 mondatban, E/3.-ben)_"),
        "",
        "---",
        "",
        f"## Your papers ({n})",
        "",
        "For each paper, the **abstract** is for your reference only (not "
        "shown on the site). The **summary**, **data**, **policy "
        "relevance**, and **tags** *are* shown. Flag anything wrong or "
        "off-key. Tell us about missing papers at the end.",
        "",
    ]

    for i, p in enumerate(mine, 1):
        authors = ", ".join(_author_name(x, coauthors) for x in p.get("authors", []))
        journal = p.get("journal") or p.get("working_paper_series") or "(working paper)"
        year = p.get("year") or "?"
        doi = p.get("doi") or ""
        status = p.get("review_status", "?")

        lines += [
            f"### {i}. {p.get('title', '(no title)')}",
            "",
            f"- **Slug:** `{p['id']}`  (status: _{status}_)",
            f"- **Authors:** {authors}",
            f"- **Outlet:** {journal}, {year}",
            f"- **DOI:** {doi or '_(none)_'}",
            "",
            "**Abstract** _(reference only, not on the site)_",
            "",
            f"> {p.get('abstract') or '_(no abstract on file — please paste one if handy)_'}",
            "",
            "**Summary — English** _(shown on site)_",
            "",
            p.get("summary_en") or "_(not yet drafted)_",
            "",
            "**Summary — Hungarian** _(shown on site)_",
            "",
            p.get("summary_hu") or "_(not yet drafted)_",
            "",
            "**Data used** _(shown on site)_",
            "",
            p.get("data_used") or "_(not yet drafted)_",
            "",
            "**Policy relevance** _(shown on site)_",
            "",
            p.get("policy_relevance") or "_(not yet drafted)_",
            "",
            f"**Tags:** {_fmt_tags(p)}",
            "",
            "---",
            "",
        ]

    lines += [
        "## Missing papers?",
        "",
        "If we're missing a paper you'd like included (peer-reviewed article "
        "in an economics / finance journal, or a CEPR / NBER / IZA working "
        "paper), list it here with title, co-authors, outlet, year, and a "
        "DOI or URL. We'll add it.",
        "",
        "_(add here)_",
        "",
        "## Anything else",
        "",
        "_(free text)_",
        "",
    ]

    return "\n".join(lines) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("author_id", help="Author slug, e.g. bekes-gabor")
    ap.add_argument(
        "--output-dir", default=str(OUT_DIR),
        help=f"Output directory (default: {OUT_DIR.relative_to(ROOT)}/)",
    )
    args = ap.parse_args()

    out_dir = Path(args.output_dir)
    out_dir.mkdir(exist_ok=True)
    out = out_dir / f"{args.author_id}.md"
    out.write_text(render_dossier(args.author_id), encoding="utf-8")
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
