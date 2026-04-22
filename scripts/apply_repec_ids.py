"""Write repec_id values from a map into data/authors/*.json.

Input: a JSON file of {author_id: repec_id}. Default path:
  not-shared/repec_ids.json (gitignored — populate by hand or via
  a batch search).

Usage:
  python scripts/apply_repec_ids.py
  python scripts/apply_repec_ids.py --file path/to/map.json
  python scripts/apply_repec_ids.py --dry-run
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).parent.parent
AUTHORS_DIR = ROOT / "data" / "authors"
DEFAULT_FILE = ROOT / "not-shared" / "repec_ids.json"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--file", default=str(DEFAULT_FILE))
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    path = Path(args.file)
    if not path.exists():
        sys.exit(f"Not found: {path}")

    mapping = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(mapping, dict):
        sys.exit("Expected a JSON object mapping author_id → repec_id.")

    updated = 0
    for aid, rid in mapping.items():
        ap_path = AUTHORS_DIR / f"{aid}.json"
        if not ap_path.exists():
            print(f"  skip (no author JSON): {aid}")
            continue
        d = json.loads(ap_path.read_text(encoding="utf-8"))
        current = d.get("repec_id")
        if current == rid:
            continue
        if current and not args.dry_run:
            print(f"  CHANGE {aid}: {current} → {rid}")
        elif not current:
            print(f"  SET    {aid}: {rid}")
        if not args.dry_run:
            d["repec_id"] = rid
            ap_path.write_text(
                json.dumps(d, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
        updated += 1

    action = "would update" if args.dry_run else "updated"
    print(f"\n{action} {updated} author file(s).")


if __name__ == "__main__":
    main()
