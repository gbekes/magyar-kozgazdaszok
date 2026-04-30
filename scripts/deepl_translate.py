#!/usr/bin/env python
"""Translate paper / policy summaries to Hungarian via DeepL.

Pipeline:
  EN summary fields  ->  DeepL  ->  HU fields written back to JSON
  ----------------       -----      --------------------------------
  data/papers/*.json     api        same files, summary_hu / data_used_hu /
  data/policy/*.json                policy_relevance_hu populated

Field map (only translates when EN side exists and HU side is empty):
  papers:  summary_en          -> summary_hu
           data_used           -> data_used_hu
           policy_relevance    -> policy_relevance_hu
  policy:  summary_en          -> summary_hu
           policy_relevance    -> policy_relevance_hu

API key:    not-shared/deepl_api_key.txt   or   $DEEPL_API_KEY
Endpoint:   auto (free if key ends with ':fx', otherwise pro)
Glossary:   --glossary-id ID    or   $DEEPL_GLOSSARY_ID

Usage:
  # See remaining DeepL quota
  python scripts/deepl_translate.py --usage

  # Preview what would be translated (no API call)
  python scripts/deepl_translate.py --dry-run
  python scripts/deepl_translate.py --dry-run --author szentes-balazs

  # Pilot: translate one author
  python scripts/deepl_translate.py --apply --author szentes-balazs

  # Pilot: translate first N items across the catalogue
  python scripts/deepl_translate.py --apply --limit 5

  # Two-stage: produce a staging JSON for editor review, then apply later
  python scripts/deepl_translate.py --produce out.json --author szentes-balazs
  # ... editor reads out.json, edits if needed ...
  python scripts/apply_summaries_hu.py out.json   # existing apply tool

  # Full sweep
  python scripts/deepl_translate.py --apply

State files (gitignored):
  not-shared/deepl_state.json   last-run summary
  not-shared/deepl_log.jsonl    one line per translated field

Notes:
  - Skips fields where target is already populated (resumable).
  - Refuses to run if queue exceeds remaining DeepL quota.
  - DeepL does not support formality for HU target; the parameter is omitted.
  - Requires `requests` (already in scripts/requirements.txt).
"""
from __future__ import annotations
import argparse
import json
import os
import sys
import time
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
PAPERS_DIR = ROOT / "data" / "papers"
POLICY_DIR = ROOT / "data" / "policy"
KEY_FILE   = ROOT / "not-shared" / "deepl_api_key.txt"
STATE_FILE = ROOT / "not-shared" / "deepl_state.json"
LOG_FILE   = ROOT / "not-shared" / "deepl_log.jsonl"

PAPER_FIELDS = [
    ("summary_en",        "summary_hu"),
    ("data_used",         "data_used_hu"),
    ("policy_relevance",  "policy_relevance_hu"),
]
POLICY_FIELDS = [
    ("summary_en",        "summary_hu"),
    ("policy_relevance",  "policy_relevance_hu"),
]

API_HOST_FREE = "https://api-free.deepl.com"
API_HOST_PRO  = "https://api.deepl.com"

BATCH_SIZE = 25          # DeepL accepts 50; stay conservative for retries
TIMEOUT_S  = 60


# ---------- key + endpoint -------------------------------------------------

def get_api_key() -> str:
    key = os.environ.get("DEEPL_API_KEY")
    if key:
        return key.strip()
    if KEY_FILE.exists():
        return KEY_FILE.read_text(encoding="utf-8").strip()
    sys.exit(
        f"DeepL API key not found.\n"
        f"  Set DEEPL_API_KEY env var, or write the key to {KEY_FILE}.\n"
        f"  Free-tier keys end with ':fx'."
    )


def api_host(key: str) -> str:
    return API_HOST_FREE if key.endswith(":fx") else API_HOST_PRO


def headers(key: str) -> dict:
    return {
        "Authorization": f"DeepL-Auth-Key {key}",
        "User-Agent": "magyar-kozgazdaszok/1.0",
    }


# ---------- DeepL calls ----------------------------------------------------

def get_usage(key: str) -> dict:
    r = requests.get(api_host(key) + "/v2/usage",
                     headers=headers(key), timeout=TIMEOUT_S)
    r.raise_for_status()
    return r.json()


def translate_batch(texts, key, glossary_id=None) -> list[str]:
    """Call DeepL /v2/translate. Returns list aligned with input texts."""
    data = [
        ("target_lang", "HU"),
        ("source_lang", "EN"),
        ("preserve_formatting", "1"),
        ("tag_handling", "html"),  # safer if any incidental HTML; ignored otherwise
    ]
    if glossary_id:
        data.append(("glossary_id", glossary_id))
    for t in texts:
        data.append(("text", t))
    r = requests.post(api_host(key) + "/v2/translate",
                      headers=headers(key), data=data, timeout=TIMEOUT_S)
    if r.status_code == 456:
        sys.exit("DeepL returned 456: quota exceeded for this billing period.")
    if r.status_code == 429:
        sys.exit("DeepL returned 429: too many requests. Try again in a minute.")
    r.raise_for_status()
    return [t["text"] for t in r.json()["translations"]]


# ---------- discovery ------------------------------------------------------

def discover(author=None, kinds=("papers", "policy"), only_fields=None):
    """Yield (path, kind, src_field, tgt_field, src_text) for every untranslated field."""
    sources = []
    if "papers" in kinds:
        sources.append(("paper",  PAPERS_DIR, PAPER_FIELDS))
    if "policy" in kinds:
        sources.append(("policy", POLICY_DIR, POLICY_FIELDS))

    for kind, d, fields in sources:
        if not d.exists():
            continue
        for path in sorted(d.glob("*.json")):
            try:
                obj = json.loads(path.read_text(encoding="utf-8"))
            except Exception as e:
                print(f"WARN: skipping unreadable {path.name}: {e}", file=sys.stderr)
                continue
            if author:
                authors = obj.get("authors", [])
                if author not in authors:
                    continue
            for src, tgt in fields:
                if only_fields and tgt not in only_fields:
                    continue
                src_text = (obj.get(src) or "").strip()
                tgt_text = (obj.get(tgt) or "").strip()
                if src_text and not tgt_text:
                    yield path, kind, src, tgt, src_text


# ---------- application ----------------------------------------------------

def apply_translations_to_files(items_by_path: dict[Path, list[tuple[str, str]]]) -> int:
    """items_by_path: {path: [(target_field, translated_text), ...]}.
    Writes each file once after collecting all its edits.
    Returns number of files updated.
    """
    today = time.strftime("%Y-%m-%d")
    n = 0
    for path, edits in items_by_path.items():
        obj = json.loads(path.read_text(encoding="utf-8"))
        for tgt, val in edits:
            obj[tgt] = val.strip()
        if "last_reviewed_at" in obj:
            obj["last_reviewed_at"] = today
        path.write_text(
            json.dumps(obj, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        n += 1
    return n


def write_produce_json(items_by_path: dict[Path, list[tuple[str, str]]], out: Path):
    """Write a staging JSON in the format apply_summaries_hu.py consumes:
         {"<paper-id>": {"summary_hu": "...", ...}, ...}
    """
    out_obj: dict = {}
    for path, edits in items_by_path.items():
        pid = path.stem
        out_obj.setdefault(pid, {})
        for tgt, val in edits:
            out_obj[pid][tgt] = val.strip()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(out_obj, ensure_ascii=False, indent=2) + "\n",
                   encoding="utf-8")


# ---------- state + log ----------------------------------------------------

def write_state(usage_before, usage_after, batches, items, files):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    state = {
        "last_run":         time.strftime("%Y-%m-%d %H:%M:%S"),
        "chars_before":     usage_before["character_count"],
        "chars_after":      usage_after["character_count"],
        "chars_used":       usage_after["character_count"] - usage_before["character_count"],
        "char_limit":       usage_after["character_limit"],
        "fields_translated": items,
        "files_updated":    files,
        "batches":          batches,
    }
    STATE_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8")


def log_append(records):
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with LOG_FILE.open("a", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")


# ---------- main -----------------------------------------------------------

def fmt_int(n: int) -> str:
    return f"{n:,}".replace(",", " ")


def main():
    ap = argparse.ArgumentParser(
        description="Translate paper/policy summaries to Hungarian via DeepL.")
    mode = ap.add_mutually_exclusive_group()
    mode.add_argument("--apply", action="store_true",
                      help="Translate and write results back to data/*.json")
    mode.add_argument("--dry-run", action="store_true",
                      help="Show queue + char count, no API call")
    mode.add_argument("--produce", metavar="OUT.json",
                      help="Translate and write a staging JSON for editor review "
                           "(apply later via apply_summaries_hu.py)")
    mode.add_argument("--usage", action="store_true",
                      help="Show DeepL quota and exit")

    ap.add_argument("--author", help="Only entries authored by this slug "
                                     "(e.g. szentes-balazs)")
    ap.add_argument("--limit", type=int, default=0,
                    help="Stop after N field translations (0 = unlimited)")
    ap.add_argument("--max-chars", type=int, default=0,
                    help="Stop after N source chars queued (0 = unlimited)")
    ap.add_argument("--kinds", default="papers,policy",
                    help="Comma list: papers, policy (default: both)")
    ap.add_argument("--fields", default="",
                    help="Comma list of target fields to fill, e.g. "
                         "summary_hu,data_used_hu,policy_relevance_hu "
                         "(default: all applicable)")
    ap.add_argument("--glossary-id",
                    default=os.environ.get("DEEPL_GLOSSARY_ID"),
                    help="DeepL glossary ID (or $DEEPL_GLOSSARY_ID)")
    args = ap.parse_args()

    # Defer key lookup -- dry-run doesn't need one.
    needs_key = args.usage or args.apply or args.produce
    key = get_api_key() if needs_key else None

    # Usage-only mode -------------------------------------------------------
    if args.usage:
        u = get_usage(key)
        used, lim = u["character_count"], u.get("character_limit") or 0
        pct = 100.0 * used / lim if lim else 0.0
        print(f"DeepL usage: {fmt_int(used)} / {fmt_int(lim)} chars  ({pct:.1f}%)")
        print(f"Remaining:   {fmt_int(lim - used)} chars")
        print(f"Endpoint:    {api_host(key)}")
        return

    # Discovery -------------------------------------------------------------
    only_fields = {f.strip() for f in args.fields.split(",") if f.strip()} or None
    kinds = tuple(k.strip() for k in args.kinds.split(",") if k.strip())

    queue = list(discover(author=args.author, kinds=kinds, only_fields=only_fields))

    # Trim by --max-chars before --limit, so cost cap dominates.
    if args.max_chars > 0:
        running = 0
        trimmed = []
        for item in queue:
            running += len(item[4])
            if running > args.max_chars:
                break
            trimmed.append(item)
        queue = trimmed
    if args.limit > 0:
        queue = queue[:args.limit]

    n_files = len({p for p, *_ in queue})
    total_chars = sum(len(t) for *_, t in queue)
    print(f"Queue: {len(queue)} field translations across {n_files} files. "
          f"{fmt_int(total_chars)} chars.")

    if not queue:
        print("Nothing to do.")
        return

    # Preview
    for path, kind, src, tgt, text in queue[:5]:
        preview = text[:100].replace("\n", " ")
        print(f"  [{kind}] {path.name}  {src} -> {tgt}  "
              f"({len(text)} ch)  {preview}...")
    if len(queue) > 5:
        print(f"  ... and {len(queue) - 5} more.")

    # Dry-run mode ----------------------------------------------------------
    if args.dry_run or (not args.apply and not args.produce):
        print("\n(dry run -- pass --apply to translate, or --produce out.json "
              "for two-stage review)")
        return

    # Quota guard -----------------------------------------------------------
    usage_before = get_usage(key)
    avail = (usage_before.get("character_limit") or 0) - usage_before["character_count"]
    if avail and total_chars > avail:
        sys.exit(f"Refusing to run: queue {fmt_int(total_chars)} chars > "
                 f"available {fmt_int(avail)} chars.\n"
                 f"  Tip: --limit or --max-chars to reduce, or --produce "
                 f"(no extra cost) to inspect.")

    # Translate -------------------------------------------------------------
    flat = list(queue)
    items_by_path: dict[Path, list[tuple[str, str]]] = {}
    log_records = []
    n_done, n_batches = 0, 0
    started = time.time()

    for i in range(0, len(flat), BATCH_SIZE):
        chunk = flat[i:i + BATCH_SIZE]
        texts = [t for *_, t in chunk]
        translations = translate_batch(texts, key, glossary_id=args.glossary_id)
        for (path, kind, src, tgt, src_text), translated in zip(chunk, translations):
            items_by_path.setdefault(path, []).append((tgt, translated))
            log_records.append({
                "ts":        time.strftime("%Y-%m-%d %H:%M:%S"),
                "kind":      kind,
                "file":      str(path.relative_to(ROOT)).replace("\\", "/"),
                "src_field": src,
                "tgt_field": tgt,
                "src_chars": len(src_text),
                "tgt_chars": len(translated),
            })
        n_done += len(chunk)
        n_batches += 1
        elapsed = time.time() - started
        print(f"  batch {n_batches:>3}: {len(chunk):>2} fields  "
              f"({n_done}/{len(flat)})  {elapsed:5.1f}s")

    # Write back ------------------------------------------------------------
    if args.produce:
        out_path = Path(args.produce)
        write_produce_json(items_by_path, out_path)
        n_files = len(items_by_path)
        print(f"\nProduced {out_path} -- {n_done} translations across {n_files} files.")
        print(f"Apply with: python scripts/apply_summaries_hu.py {out_path}")
    else:
        n_files = apply_translations_to_files(items_by_path)
        print(f"\nApplied to {n_files} files.")

    # Log + state -----------------------------------------------------------
    log_append(log_records)
    usage_after = get_usage(key)
    write_state(usage_before, usage_after, n_batches, n_done, len(items_by_path))
    used = usage_after["character_count"] - usage_before["character_count"]
    print(f"\nDeepL chars charged: {fmt_int(used)}")
    print(f"DeepL quota now:     {fmt_int(usage_after['character_count'])} / "
          f"{fmt_int(usage_after.get('character_limit') or 0)}")


if __name__ == "__main__":
    main()
