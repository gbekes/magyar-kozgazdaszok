"""Build script for Evidence for Hungary site.

Two jobs:
1. Expand authors-seed.json into data/authors/<id>.json (only creates new ones; does
   not overwrite files that already exist).
2. Aggregate data/authors/*.json and data/papers/*.json + topics + journals into a
   single data/index.json the static site loads in one fetch.

Run:  python build.py
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).parent
DATA = ROOT / "data"
AUTHORS_DIR = DATA / "authors"
PAPERS_DIR = DATA / "papers"
SEED_FILE = ROOT / "authors-seed.json"


def expand_seed_authors() -> int:
    """Turn each seed entry into data/authors/<id>.json (skip existing)."""
    with open(SEED_FILE, "r", encoding="utf-8") as f:
        seed = json.load(f)

    created = 0
    for s in seed:
        aid = s["id"]
        out = AUTHORS_DIR / f"{aid}.json"
        if out.exists():
            continue

        author = {
            "id": aid,
            "name_en": s.get("name_en"),
            "name_hu": s.get("name_hu"),
            "affiliations": [
                {"name": s.get("primary_affiliation", ""), "role": None, "start": None}
            ]
            if s.get("primary_affiliation")
            else [],
            "website": None,
            "email": None,
            "repec_id": None,
            "scholar_id": None,
            "orcid": None,
            "primary_fields": s.get("primary_fields", []),
            "bio_en": s.get("bio_en"),
            "bio_hu": None,
            "photo_url": None,
            "qualifying_publication": None,
            "review_status": s.get("bio_review", "stub"),
        }

        with open(out, "w", encoding="utf-8") as f:
            json.dump(author, f, ensure_ascii=False, indent=2)
        created += 1

    return created


def load_json(path: Path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_index() -> dict:
    authors = [load_json(p) for p in sorted(AUTHORS_DIR.glob("*.json"))]
    papers = [load_json(p) for p in sorted(PAPERS_DIR.glob("*.json"))]
    topics = load_json(DATA / "topics.json")
    journals = load_json(DATA / "journals.json")

    # Attach paper counts to topics and authors for quick rendering.
    topic_counts: dict[str, int] = {}
    author_counts: dict[str, int] = {}
    for p in papers:
        for t in p.get("topics", []):
            topic_counts[t] = topic_counts.get(t, 0) + 1
        for a in p.get("authors", []):
            author_counts[a] = author_counts.get(a, 0) + 1

    for t in topics:
        t["paper_count"] = topic_counts.get(t["id"], 0)
    for a in authors:
        a["paper_count"] = author_counts.get(a["id"], 0)

    return {
        "authors": authors,
        "papers": papers,
        "topics": topics,
        "journals": journals,
        "counts": {
            "authors": len(authors),
            "papers": len(papers),
            "topics": len(topics),
        },
    }


def main() -> None:
    created = expand_seed_authors()
    index = build_index()
    with open(DATA / "index.json", "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)

    print(f"Created {created} new author file(s).")
    print(
        f"Index: {index['counts']['authors']} authors, "
        f"{index['counts']['papers']} papers, "
        f"{index['counts']['topics']} topics."
    )


if __name__ == "__main__":
    main()
