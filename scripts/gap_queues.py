#!/usr/bin/env python
"""Generate English backfill queues for the Magyar Kozgazdaszok catalogue.

The script is intentionally read-only. It scans the JSON catalogue and writes
small Markdown/CSV queues that make the next drafting session mechanical.

Examples:
  python scripts/gap_queues.py
  python scripts/gap_queues.py --out reports/gaps --limit 20
  python scripts/gap_queues.py --format csv
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
PAPERS = DATA / "papers"
POLICY = DATA / "policy"
AUTHORS = DATA / "authors"
DEFAULT_OUT = ROOT / "reports" / "gaps"

CORE_PAPER_FIELDS = ("summary_en", "data_used", "policy_relevance")
CORE_POLICY_FIELDS = ("summary_en", "policy_relevance", "topics")
AUTHOR_FIELDS = ("repec_id", "photo_url", "qualifying_publication")


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8-sig") as f:
        return json.load(f)


def load_dir(path: Path) -> list[tuple[Path, dict[str, Any]]]:
    if not path.exists():
        return []
    return [(p, load_json(p)) for p in sorted(path.glob("*.json"))]


def missing(value: Any) -> bool:
    return value is None or value == "" or value == [] or value == {}


def missing_fields(item: dict[str, Any], fields: Iterable[str]) -> list[str]:
    return [field for field in fields if missing(item.get(field))]


def first_present(item: dict[str, Any], fields: Iterable[str]) -> str:
    for field in fields:
        value = item.get(field)
        if not missing(value):
            return str(value)
    return ""


@dataclass
class QueueItem:
    id: str
    title: str
    authors: str
    year: str
    outlet: str
    missing: str
    source_status: str
    file: str
    priority: int

    def row(self) -> dict[str, str | int]:
        return {
            "priority": self.priority,
            "id": self.id,
            "title": self.title,
            "authors": self.authors,
            "year": self.year,
            "outlet": self.outlet,
            "missing": self.missing,
            "source_status": self.source_status,
            "file": self.file,
        }


def source_status(item: dict[str, Any]) -> str:
    if not missing(item.get("abstract")):
        return "has abstract"
    if not missing(item.get("url_pdf")):
        return "needs PDF extraction"
    if not missing(item.get("url_published")) or not missing(item.get("doi")) or not missing(item.get("url")):
        return "needs web lookup"
    return "needs source"


def author_names(author_ids: list[str], authors_by_id: dict[str, dict[str, Any]]) -> str:
    names = []
    for author_id in author_ids:
        if author_id in authors_by_id:
            names.append(authors_by_id[author_id].get("name_en") or author_id)
        else:
            names.append(author_id)
    return "; ".join(names)


def paper_priority(paper: dict[str, Any], miss: list[str]) -> int:
    score = len(miss) * 10
    if missing(paper.get("abstract")):
        score += 5
    if paper.get("featured"):
        score -= 8
    year = paper.get("year") or 0
    if isinstance(year, int) and year >= 2020:
        score -= 2
    return score


def policy_priority(item: dict[str, Any], miss: list[str]) -> int:
    score = len(miss) * 10
    if missing(item.get("summary_en")) or missing(item.get("policy_relevance")):
        score -= 5
    if item.get("language") == "en":
        score -= 2
    year = item.get("year") or 0
    if isinstance(year, int) and year >= 2020:
        score -= 1
    return score


def make_paper_queues(papers: list[tuple[Path, dict[str, Any]]], authors_by_id: dict[str, dict[str, Any]]) -> tuple[list[QueueItem], list[QueueItem]]:
    ready: list[QueueItem] = []
    needs_source: list[QueueItem] = []
    for path, paper in papers:
        miss = missing_fields(paper, CORE_PAPER_FIELDS)
        if not miss:
            continue
        item = QueueItem(
            id=paper.get("id", path.stem),
            title=paper.get("title", ""),
            authors=author_names(paper.get("authors", []), authors_by_id),
            year=str(paper.get("year") or ""),
            outlet=paper.get("journal") or paper.get("working_paper_series") or "",
            missing=", ".join(miss),
            source_status=source_status(paper),
            file=str(path.relative_to(ROOT)).replace("\\", "/"),
            priority=paper_priority(paper, miss),
        )
        if item.source_status == "has abstract":
            ready.append(item)
        else:
            needs_source.append(item)
    ready.sort(key=lambda x: (x.priority, x.year), reverse=False)
    needs_source.sort(key=lambda x: (x.source_status, x.priority, x.year))
    return ready, needs_source


def make_policy_queue(policy: list[tuple[Path, dict[str, Any]]], authors_by_id: dict[str, dict[str, Any]]) -> list[QueueItem]:
    queue: list[QueueItem] = []
    for path, item in policy:
        miss = missing_fields(item, CORE_POLICY_FIELDS)
        if not miss:
            continue
        queue.append(QueueItem(
            id=item.get("id", path.stem),
            title=item.get("title") or item.get("title_hu") or "",
            authors=author_names(item.get("authors", []), authors_by_id),
            year=str(item.get("year") or ""),
            outlet=" · ".join(str(x) for x in (item.get("institution"), item.get("outlet")) if x),
            missing=", ".join(miss),
            source_status=source_status(item),
            file=str(path.relative_to(ROOT)).replace("\\", "/"),
            priority=policy_priority(item, miss),
        ))
    queue.sort(key=lambda x: (x.priority, x.year), reverse=False)
    return queue


def make_author_queue(authors: list[tuple[Path, dict[str, Any]]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for path, author in authors:
        miss = missing_fields(author, AUTHOR_FIELDS)
        if not miss:
            continue
        rows.append({
            "id": author.get("id", path.stem),
            "name": author.get("name_en", ""),
            "missing": ", ".join(miss),
            "paper_count": str(author.get("paper_count") or ""),
            "review_status": author.get("review_status", ""),
            "file": str(path.relative_to(ROOT)).replace("\\", "/"),
        })
    rows.sort(key=lambda r: (-int(r["paper_count"] or 0), r["id"]))
    return rows


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def md_table(headers: list[str], rows: list[list[str]], limit: int | None = None) -> str:
    if limit is not None:
        rows = rows[:limit]
    out = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        escaped = [str(cell).replace("|", "\\|").replace("\n", " ") for cell in row]
        out.append("| " + " | ".join(escaped) + " |")
    return "\n".join(out)


def write_markdown(out_dir: Path, ready: list[QueueItem], needs_source: list[QueueItem], policy: list[QueueItem], authors: list[dict[str, str]], limit: int | None) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)

    def q_table(items: list[QueueItem]) -> str:
        return md_table(
            ["priority", "id", "year", "authors", "outlet", "missing", "source", "file"],
            [[str(i.priority), i.id, i.year, i.authors, i.outlet, i.missing, i.source_status, i.file] for i in items],
            limit,
        )

    (out_dir / "paper-drafts-ready.md").write_text(
        "# Paper Drafts Ready\n\n"
        "Research records missing English fields where an abstract is already in JSON. Start here.\n\n"
        + q_table(ready) + "\n",
        encoding="utf-8",
    )
    (out_dir / "paper-drafts-need-source.md").write_text(
        "# Paper Drafts Needing Source\n\n"
        "Research records missing English fields that need a DOI/page/PDF lookup before drafting.\n\n"
        + q_table(needs_source) + "\n",
        encoding="utf-8",
    )
    (out_dir / "policy-drafts.md").write_text(
        "# Policy Drafts\n\n"
        "Policy records missing English summary, policy relevance, or topics. These are the fastest public-facing wins.\n\n"
        + q_table(policy) + "\n",
        encoding="utf-8",
    )
    (out_dir / "author-metadata.md").write_text(
        "# Author Metadata\n\n"
        "Author records missing RePEc, photo, or qualifying publication metadata.\n\n"
        + md_table(
            ["id", "name", "paper_count", "missing", "review_status", "file"],
            [[r["id"], r["name"], r["paper_count"], r["missing"], r["review_status"], r["file"]] for r in authors],
            limit,
        ) + "\n",
        encoding="utf-8",
    )

    summary = [
        "# English Gap Queues",
        "",
        "Generated by `python scripts/gap_queues.py`.",
        "",
        f"- Paper drafts ready from existing abstracts: {len(ready)}",
        f"- Paper drafts needing source lookup: {len(needs_source)}",
        f"- Policy drafts: {len(policy)}",
        f"- Author metadata rows: {len(authors)}",
        "",
        "Recommended order:",
        "1. `policy-drafts.md`",
        "2. `paper-drafts-ready.md`",
        "3. `paper-drafts-need-source.md`",
        "4. `author-metadata.md`",
        "",
    ]
    (out_dir / "README.md").write_text("\n".join(summary), encoding="utf-8")


def print_author_clusters(ready: list[QueueItem], needs_source: list[QueueItem]) -> None:
    counts: Counter[str] = Counter()
    for item in ready + needs_source:
        for name in item.authors.split("; "):
            if name:
                counts[name] += 1
    print("\nTop paper-gap clusters:")
    for name, total in counts.most_common(12):
        print(f"  {name}: {total}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate English content-gap queues.")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT, help="Output directory for queue files.")
    parser.add_argument("--limit", type=int, default=None, help="Limit rows written per Markdown queue.")
    parser.add_argument("--format", choices=("md", "csv", "both"), default="md", help="Output format.")
    args = parser.parse_args()

    authors = load_dir(AUTHORS)
    authors_by_id = {a.get("id", path.stem): a for path, a in authors}
    papers = load_dir(PAPERS)
    policy = load_dir(POLICY)

    paper_ready, paper_needs_source = make_paper_queues(papers, authors_by_id)
    policy_queue = make_policy_queue(policy, authors_by_id)
    author_queue = make_author_queue(authors)

    if args.format in ("md", "both"):
        write_markdown(args.out, paper_ready, paper_needs_source, policy_queue, author_queue, args.limit)
    if args.format in ("csv", "both"):
        write_csv(args.out / "paper-drafts-ready.csv", [i.row() for i in paper_ready], list(QueueItem("", "", "", "", "", "", "", "", 0).row().keys()))
        write_csv(args.out / "paper-drafts-need-source.csv", [i.row() for i in paper_needs_source], list(QueueItem("", "", "", "", "", "", "", "", 0).row().keys()))
        write_csv(args.out / "policy-drafts.csv", [i.row() for i in policy_queue], list(QueueItem("", "", "", "", "", "", "", "", 0).row().keys()))
        write_csv(args.out / "author-metadata.csv", author_queue, ["id", "name", "paper_count", "missing", "review_status", "file"])

    print(f"Wrote queues to {args.out}")
    print(f"paper drafts ready:        {len(paper_ready)}")
    print(f"paper drafts need source:  {len(paper_needs_source)}")
    print(f"policy drafts:             {len(policy_queue)}")
    print(f"author metadata rows:      {len(author_queue)}")
    print_author_clusters(paper_ready, paper_needs_source)


if __name__ == "__main__":
    main()
