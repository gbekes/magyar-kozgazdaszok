#!/usr/bin/env python
"""Manage DeepL EN->HU glossaries for the catalogue.

A glossary tells DeepL how to translate specific terms. Useful for
keeping econ jargon (minimum wage -> minimálbér), Hungarian institution
names, and policy program names stable across the 482-paper corpus.

Glossary format: TSV file, one entry per line:
    source<TAB>target
    minimum wage<TAB>minimálbér
    VAT<TAB>ÁFA

Usage:
  python scripts/deepl_glossary.py list
  python scripts/deepl_glossary.py create scripts/deepl_glossary_en_hu.tsv
  python scripts/deepl_glossary.py show <glossary_id>
  python scripts/deepl_glossary.py delete <glossary_id>

After creation, set the glossary ID for translation runs:
    export DEEPL_GLOSSARY_ID=<id>
or pass --glossary-id <id> to deepl_translate.py.

Glossaries persist on DeepL's side. To update, delete and recreate
(DeepL has no in-place edit). The glossary ID will change.

API key: not-shared/deepl_api_key.txt or $DEEPL_API_KEY.
"""
from __future__ import annotations
import argparse
import json
import os
import sys
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
KEY_FILE = ROOT / "not-shared" / "deepl_api_key.txt"

API_HOST_FREE = "https://api-free.deepl.com"
API_HOST_PRO  = "https://api.deepl.com"


def get_api_key() -> str:
    key = os.environ.get("DEEPL_API_KEY")
    if key:
        return key.strip()
    if KEY_FILE.exists():
        return KEY_FILE.read_text(encoding="utf-8").strip()
    sys.exit(f"DeepL API key not found. Set DEEPL_API_KEY or write to {KEY_FILE}.")


def api_host(key: str) -> str:
    return API_HOST_FREE if key.endswith(":fx") else API_HOST_PRO


def headers(key: str) -> dict:
    return {
        "Authorization": f"DeepL-Auth-Key {key}",
        "User-Agent": "magyar-kozgazdaszok/1.0",
    }


def cmd_list(args):
    key = get_api_key()
    r = requests.get(api_host(key) + "/v2/glossaries",
                     headers=headers(key), timeout=30)
    r.raise_for_status()
    glossaries = r.json().get("glossaries", [])
    if not glossaries:
        print("(no glossaries on this account)")
        return
    print(f"{'glossary_id':<40} {'name':<24} {'lang':<10} {'entries':>7} {'created'}")
    for g in glossaries:
        print(f"{g['glossary_id']:<40} {g['name'][:23]:<24} "
              f"{g['source_lang']}->{g['target_lang']:<6} "
              f"{g['entry_count']:>7}  {g.get('creation_time', '')[:10]}")


def cmd_create(args):
    key = get_api_key()
    tsv_path = Path(args.tsv)
    if not tsv_path.exists():
        sys.exit(f"Not found: {tsv_path}")
    entries = tsv_path.read_text(encoding="utf-8")
    # Strip blank lines / comments
    cleaned = []
    for line in entries.splitlines():
        line = line.rstrip()
        if not line or line.startswith("#"):
            continue
        if "\t" not in line:
            print(f"WARN: skipping malformed line: {line[:60]}", file=sys.stderr)
            continue
        cleaned.append(line)
    if not cleaned:
        sys.exit("No valid entries in TSV.")

    payload = {
        "name":           args.name,
        "source_lang":    "EN",
        "target_lang":    "HU",
        "entries":        "\n".join(cleaned),
        "entries_format": "tsv",
    }
    r = requests.post(api_host(key) + "/v2/glossaries",
                      headers=headers(key), data=payload, timeout=30)
    if r.status_code >= 400:
        sys.exit(f"DeepL error {r.status_code}: {r.text}")
    g = r.json()
    print(f"Created glossary {g['glossary_id']}  "
          f"({g['entry_count']} entries, EN->HU)")
    print(f"\nTo use it, run:")
    print(f"  export DEEPL_GLOSSARY_ID={g['glossary_id']}")


def cmd_show(args):
    key = get_api_key()
    r = requests.get(api_host(key) + f"/v2/glossaries/{args.glossary_id}",
                     headers=headers(key), timeout=30)
    if r.status_code == 404:
        sys.exit(f"Glossary {args.glossary_id} not found.")
    r.raise_for_status()
    print(json.dumps(r.json(), indent=2, ensure_ascii=False))
    print()
    # Fetch entries
    r2 = requests.get(api_host(key) + f"/v2/glossaries/{args.glossary_id}/entries",
                      headers={**headers(key), "Accept": "text/tab-separated-values"},
                      timeout=30)
    r2.raise_for_status()
    print("Entries (TSV):")
    print(r2.text)


def cmd_delete(args):
    key = get_api_key()
    r = requests.delete(api_host(key) + f"/v2/glossaries/{args.glossary_id}",
                        headers=headers(key), timeout=30)
    if r.status_code == 404:
        sys.exit(f"Glossary {args.glossary_id} not found.")
    if r.status_code >= 400:
        sys.exit(f"DeepL error {r.status_code}: {r.text}")
    print(f"Deleted {args.glossary_id}.")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("list", help="List all glossaries on this account")

    cp = sub.add_parser("create", help="Create a new EN->HU glossary from TSV")
    cp.add_argument("tsv", help="Path to TSV file (source<TAB>target)")
    cp.add_argument("--name", default="magyar-kozgazdaszok-en-hu",
                    help="Glossary name (default: magyar-kozgazdaszok-en-hu)")

    sp = sub.add_parser("show", help="Show metadata + entries of a glossary")
    sp.add_argument("glossary_id")

    dp = sub.add_parser("delete", help="Delete a glossary")
    dp.add_argument("glossary_id")

    args = ap.parse_args()
    {"list": cmd_list, "create": cmd_create,
     "show": cmd_show, "delete": cmd_delete}[args.cmd](args)


if __name__ == "__main__":
    main()
