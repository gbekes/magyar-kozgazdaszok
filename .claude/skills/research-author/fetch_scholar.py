#!/usr/bin/env python
"""Helper to enumerate authors needing Scholar snapshots.

This script can't fetch Scholar pages itself (no auth, no headless
browser); it lists what to fetch. The actual fetching is done via
Claude Code's WebFetch tool, one author at a time, prompted with
the URL this script outputs.

Usage:
  python .claude/skills/research-author/fetch_scholar.py
      → list all authors with scholar_id and snapshot status

  python .claude/skills/research-author/fetch_scholar.py --missing
      → list authors WITHOUT scholar_id (need lookup first)

  python .claude/skills/research-author/fetch_scholar.py --urls
      → emit fetchable URLs for snapshot work, one per line

  python .claude/skills/research-author/fetch_scholar.py <slug>
      → emit URL for one author (or "no scholar_id" if missing)

Snapshots are saved at not-shared/scholar-snapshots/<slug>.md by
Claude using the WebFetch tool.
"""
from __future__ import annotations
import sys, json, glob, argparse
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[3]
AUTHORS = ROOT / "data" / "authors"
SNAP_DIR = ROOT / "not-shared" / "scholar-snapshots"


def load(p):
    return json.load(open(p, encoding="utf-8"))


def scholar_url(sid: str) -> str:
    return f"https://scholar.google.com/citations?user={sid}&hl=en"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slug", nargs="?")
    ap.add_argument("--missing", action="store_true",
                    help="list authors without scholar_id")
    ap.add_argument("--urls", action="store_true",
                    help="emit URLs only, one per line")
    args = ap.parse_args()

    rows = []
    for f in sorted(AUTHORS.glob("*.json")):
        a = load(f)
        slug = a["id"]
        sid = a.get("scholar_id")
        snap = SNAP_DIR / f"{slug}.md"
        rows.append({
            "slug": slug,
            "name": a.get("name_en") or slug,
            "scholar_id": sid,
            "snapped": snap.exists(),
        })

    if args.slug:
        match = next((r for r in rows if r["slug"] == args.slug), None)
        if not match:
            print(f"no author found: {args.slug}")
            sys.exit(2)
        if not match["scholar_id"]:
            print(f"{args.slug}: no scholar_id in author JSON")
            sys.exit(1)
        print(scholar_url(match["scholar_id"]))
        return

    if args.missing:
        miss = [r for r in rows if not r["scholar_id"]]
        for r in miss:
            print(f'  {r["slug"]:24s} | {r["name"]}')
        print(f"\n{len(miss)} authors without scholar_id.")
        return

    if args.urls:
        for r in rows:
            if r["scholar_id"] and not r["snapped"]:
                print(scholar_url(r["scholar_id"]))
        return

    # default: status table
    have = [r for r in rows if r["scholar_id"]]
    miss = [r for r in rows if not r["scholar_id"]]
    print(f"{'slug':24s} | scholar_id              | snapped | name")
    print("-" * 90)
    for r in rows:
        sid = r["scholar_id"] or "—"
        snapped = "Y" if r["snapped"] else " "
        print(f'{r["slug"]:24s} | {sid:24s} | {snapped:^7s} | {r["name"]}')
    print(f"\nTotals: {len(have)} with scholar_id ({sum(1 for r in have if r['snapped'])} snapped), {len(miss)} need lookup.")


if __name__ == "__main__":
    main()
