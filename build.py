"""Build script for Evidence for Hungary site.

Two jobs:
1. Verify authors-seed.json (a manifest of approved author IDs) against the
   per-author files in data/authors/. Per-author files are the source of
   truth for everything else.
2. Aggregate data/authors/*.json and data/papers/*.json + topics + journals
   into a single data/index.json the static site loads in one fetch.

Run:  python build.py
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).parent
DATA = ROOT / "data"
AUTHORS_DIR = DATA / "authors"
PAPERS_DIR = DATA / "papers"
POLICY_DIR = DATA / "policy"
PRESS_DIR = DATA / "press"
SEED_FILE = ROOT / "authors-seed.json"


def check_seed_manifest() -> tuple[int, list[str]]:
    """authors-seed.json is now a manifest of approved author IDs.

    The per-author file at data/authors/<id>.json is the single source of
    truth for everything else (name, bio, affiliations). This step just
    verifies that every ID in the manifest has a file; missing files are
    reported but do not block the build.
    """
    with open(SEED_FILE, "r", encoding="utf-8") as f:
        seed = json.load(f)

    missing = []
    for s in seed:
        aid = s["id"]
        if not (AUTHORS_DIR / f"{aid}.json").exists():
            missing.append(aid)
    return len(seed), missing


def load_json(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _load_dir(path: Path) -> list:
    if not path.exists():
        return []
    return [load_json(p) for p in sorted(path.glob("*.json"))]


def build_index() -> dict:
    authors = [load_json(p) for p in sorted(AUTHORS_DIR.glob("*.json"))]
    papers = [load_json(p) for p in sorted(PAPERS_DIR.glob("*.json"))]
    policy = _load_dir(POLICY_DIR)
    press = _load_dir(PRESS_DIR)
    topics = load_json(DATA / "topics.json")
    journals = load_json(DATA / "journals.json")

    # Attach counts to topics and authors. Counts are per-category so the
    # UI can show a "12 papers · 3 policy · 8 press" line without scanning
    # the full lists.
    topic_counts: dict[str, int] = {}
    author_paper_counts: dict[str, int] = {}
    author_policy_counts: dict[str, int] = {}
    author_press_counts: dict[str, int] = {}

    for p in papers:
        for t in p.get("topics", []):
            topic_counts[t] = topic_counts.get(t, 0) + 1
        for a in p.get("authors", []):
            author_paper_counts[a] = author_paper_counts.get(a, 0) + 1

    for p in policy:
        for t in p.get("topics", []):
            topic_counts[t] = topic_counts.get(t, 0) + 1
        for a in p.get("authors", []):
            author_policy_counts[a] = author_policy_counts.get(a, 0) + 1

    for p in press:
        for a in p.get("authors", []):
            author_press_counts[a] = author_press_counts.get(a, 0) + 1

    for t in topics:
        t["paper_count"] = topic_counts.get(t["id"], 0)
    for a in authors:
        a["paper_count"] = author_paper_counts.get(a["id"], 0)
        a["policy_count"] = author_policy_counts.get(a["id"], 0)
        a["press_count"] = author_press_counts.get(a["id"], 0)

    return {
        "authors": authors,
        "papers": papers,
        "policy": policy,
        "press": press,
        "topics": topics,
        "journals": journals,
        "counts": {
            "authors": len(authors),
            "papers": len(papers),
            "policy": len(policy),
            "press": len(press),
            "topics": len(topics),
        },
    }


def main() -> None:
    n_seed, missing = check_seed_manifest()
    index = build_index()
    with open(DATA / "index.json", "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)

    print(f"Manifest: {n_seed} author IDs.")
    if missing:
        print(f"  WARNING: {len(missing)} IDs in authors-seed.json have no per-author file:")
        for aid in missing:
            print(f"    - {aid}")
    print(
        f"Index: {index['counts']['authors']} authors, "
        f"{index['counts']['papers']} papers, "
        f"{index['counts']['policy']} policy, "
        f"{index['counts']['press']} press, "
        f"{index['counts']['topics']} topics."
    )


if __name__ == "__main__":
    main()
