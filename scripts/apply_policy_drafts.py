#!/usr/bin/env python
"""Apply draft summaries to data/policy/*.json.

Input JSON is an object keyed by policy id:
{
  "adamecz-2020-bi-youth-outreach": {
    "summary_en": "...",
    "policy_relevance": "...",
    "topics": ["labor-markets", "education-skills"],
    "summary_hu": "...",
    "policy_relevance_hu": "..."
  }
}

The script validates controlled topics, preserves fields not mentioned in the
draft, and sets review_status / last_reviewed_at unless --no-status is used.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Any

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
POLICY = ROOT / "data" / "policy"
TOPICS_PATH = ROOT / "data" / "topics.json"
TEXT_FIELDS = ("summary_en", "summary_hu", "policy_relevance", "policy_relevance_hu")
OPTIONAL_FIELDS = ("title", "title_hu", "policy_instruments", "linked_paper_id")


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8-sig") as f:
        return json.load(f)


def write_json(path: Path, data: Any) -> None:
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def topic_ids() -> set[str]:
    return {t["id"] for t in load_json(TOPICS_PATH)}


def clean_strings(values: Any, limit: int | None = None) -> list[str]:
    if not isinstance(values, list):
        return []
    cleaned = [str(v).strip() for v in values if isinstance(v, str) and str(v).strip()]
    return cleaned[:limit] if limit else cleaned


def apply_drafts(drafts_path: Path, *, dry_run: bool, no_status: bool) -> int:
    drafts = load_json(drafts_path)
    if not isinstance(drafts, dict):
        raise SystemExit("drafts file must be a JSON object keyed by policy id")

    allowed_topics = topic_ids()
    today = time.strftime("%Y-%m-%d")
    applied = 0
    missing = 0
    skipped = 0

    for policy_id, draft in drafts.items():
        if not isinstance(draft, dict):
            print(f"SKIP (draft is not object): {policy_id}")
            skipped += 1
            continue
        path = POLICY / f"{policy_id}.json"
        if not path.exists():
            print(f"MISSING: {policy_id}")
            missing += 1
            continue

        item = load_json(path)
        if item.get("review_status") in ("human-reviewed", "author-approved"):
            print(f"SKIP (reviewed): {policy_id}")
            skipped += 1
            continue

        for field in TEXT_FIELDS:
            value = draft.get(field)
            if isinstance(value, str) and value.strip():
                item[field] = value.strip()

        for field in OPTIONAL_FIELDS:
            if field in draft:
                if isinstance(draft[field], str):
                    item[field] = draft[field].strip() or None
                elif field == "policy_instruments":
                    item[field] = clean_strings(draft[field], limit=5)
                else:
                    item[field] = draft[field]

        if "topics" in draft:
            topics = [t for t in clean_strings(draft["topics"], limit=3) if t in allowed_topics]
            invalid = [t for t in clean_strings(draft["topics"]) if t not in allowed_topics]
            if invalid:
                print(f"WARN (invalid topics ignored): {policy_id}: {', '.join(invalid)}")
            if topics:
                item["topics"] = topics

        incomplete = [f for f in ("summary_en", "policy_relevance", "topics") if not item.get(f)]
        if incomplete:
            print(f"WARN (still incomplete): {policy_id}: {', '.join(incomplete)}")

        if not no_status:
            item["review_status"] = "ai-drafted"
            item["last_reviewed_at"] = today

        if dry_run:
            print(f"DRY RUN: would apply {policy_id}")
        else:
            write_json(path, item)
            print(f"APPLIED: {policy_id}")
        applied += 1

    print(f"\napplied: {applied}, missing: {missing}, skipped: {skipped}, dry_run: {dry_run}")
    return 0 if missing == 0 else 1


def main() -> None:
    parser = argparse.ArgumentParser(description="Apply draft summaries to policy JSON files.")
    parser.add_argument("drafts", type=Path, help="Draft JSON keyed by policy id.")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing files.")
    parser.add_argument("--no-status", action="store_true", help="Do not set review_status or last_reviewed_at.")
    args = parser.parse_args()
    raise SystemExit(apply_drafts(args.drafts, dry_run=args.dry_run, no_status=args.no_status))


if __name__ == "__main__":
    main()
