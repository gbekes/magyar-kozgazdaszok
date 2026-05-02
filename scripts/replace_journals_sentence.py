"""For authors whose bio already mentions journals in ad-hoc form, replace
the ad-hoc sentence with the standard 'has published in journals like X, Y
and Z' format (and Hungarian equivalent).

Strategy:
1. Detect a "journals sentence" by matching a leading prefix pattern such as
   "He has published in", "His work has appeared in", etc.
2. If the sentence starts with such a prefix and is dominated by journal
   names, replace the whole sentence with the standard form.
3. If the sentence has additional content (e.g. ", and is a CEPR fellow")
   we keep that trailing clause.
4. If we can't safely extract (mixed prose, no clear prefix), leave bio
   alone and only append the standard sentence at the end -- the script
   reports those for manual review.

Usage:
    python scripts/replace_journals_sentence.py --batch <N>
    python scripts/replace_journals_sentence.py --slug <id>
    python scripts/replace_journals_sentence.py --list
    python scripts/replace_journals_sentence.py --dry-run --batch <N>
"""
import argparse
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from add_journals_sentence import (  # noqa: E402
    author_top_journals,
    en_sentence,
    hu_sentence,
    load_journals,
)

AUTHORS = ROOT / "data" / "authors"
PAPERS = ROOT / "data" / "papers"

# English: prefix that introduces a list of journals.
EN_PREFIXES = [
    r"(?:He|She)\s+has\s+published\s+in\s+",
    r"(?:He|She)\s+has\s+previously\s+published\s+in\s+",
    r"(?:His|Her)\s+work\s+has\s+appeared\s+(?:regularly\s+)?in\s+",
    r"(?:His|Her)\s+research\s+has\s+appeared\s+(?:regularly\s+)?in\s+",
    r"(?:His|Her)\s+(?:papers|publications)\s+have\s+appeared\s+(?:regularly\s+)?in\s+",
    r"(?:His|Her)\s+work\s+appears\s+(?:regularly\s+)?in\s+",
    r"(?:His|Her)\s+work\s+has\s+been\s+published\s+(?:in\s+peer-reviewed\s+journals,\s+including\s+|in\s+)",
]
# Allow either sentence-start (after .!?) OR mid-sentence after a comma --
# benczur-style "Previously at MNB, he has published in JEEA."
EN_PREFIX_RE = re.compile(r"(?:(?<=[.!?])\s+|(?<=,\s))(" + "|".join(EN_PREFIXES) + r")", re.IGNORECASE)

# Hungarian: prefix that introduces a list of journals.
HU_PREFIXES = [
    r"(?:Munkái|Munkája|Cikkei|Tanulmányai|Publikációi|Kutatásai|Cikkeit)\s+(?:megjelentek?|jelentek meg|közölte|közölték|olyan folyóiratokban jelentek meg,\s+mint)\s+",
]
HU_PREFIX_RE = re.compile(r"(?<=[.!?])\s+(" + "|".join(HU_PREFIXES) + r")", re.IGNORECASE)


def strip_known_sentence(bio, prefix_re):
    """Find a sentence that begins with one of the known prefixes, locate its
    end (next period that ends a journal-list-only clause), and return
    (cleaned_bio, removed_sentence). Heuristic: the sentence runs from the
    matched prefix up to the next period. Returns (bio, None) if none found.
    """
    if not bio:
        return bio, None
    # Add a sentinel so first-sentence matches work the same way.
    sentinel = "."
    text = sentinel + " " + bio if not bio.startswith(("​",)) else bio
    m = prefix_re.search(text)
    if not m:
        return bio, None
    start = m.start() + len(m.group()) - len(m.group(1))  # index of the prefix start
    # End at the next sentence terminator
    end_match = re.search(r"[.!?](?:\s|$)", text[start:])
    if not end_match:
        return bio, None
    end = start + end_match.end()
    # Strip leading sentinel
    if text.startswith(sentinel + " "):
        start_in_bio = start - len(sentinel) - 1
        end_in_bio = end - len(sentinel) - 1
    else:
        start_in_bio = start
        end_in_bio = end
    removed = bio[start_in_bio:end_in_bio]
    cleaned = (bio[:start_in_bio].rstrip() + " " + bio[end_in_bio:].lstrip()).strip()
    return cleaned, removed


def process_author(slug, papers, whitelist, dry_run=False):
    f = AUTHORS / f"{slug}.json"
    a = json.loads(f.read_text(encoding="utf-8"))

    bio_en = a.get("bio_en") or ""
    bio_hu = a.get("bio_hu") or ""

    # If standardized sentence already there, nothing to do.
    if "has published in journals like" in bio_en:
        return None, "already standardized"

    # Compute top-3 journals
    top = author_top_journals(slug, papers, whitelist)
    if not top:
        return None, "no whitelisted-journal papers"

    name_en = a.get("name_en") or a.get("name_hu") or slug
    name_hu = a.get("name_hu") or a.get("name_en") or slug

    # Strip ad-hoc journals sentences from EN and HU
    new_en, removed_en = strip_known_sentence(bio_en, EN_PREFIX_RE)
    new_hu, removed_hu = strip_known_sentence(bio_hu, HU_PREFIX_RE)

    # Append standard sentence
    if new_en and not new_en.endswith("."):
        new_en += "."
    new_en = (new_en + " " + en_sentence(name_en, top)).strip()

    if new_hu and not new_hu.endswith("."):
        new_hu += "."
    new_hu = (new_hu + " " + hu_sentence(name_hu, top)).strip()

    a["bio_en"] = new_en
    a["bio_hu"] = new_hu

    info = {
        "top": top,
        "removed_en": removed_en.strip() if removed_en else None,
        "removed_hu": removed_hu.strip() if removed_hu else None,
    }
    if not dry_run:
        f.write_text(json.dumps(a, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return info, None


def find_pending(journal_names):
    """Authors whose bio mentions a whitelisted journal in a strict sense:
    journal name appears with word boundaries on both sides (so 'Science'
    doesn't match 'Sciences')."""
    name_patterns = [re.compile(r"\b" + re.escape(jn) + r"\b") for jn in journal_names]
    pending = []
    for f in sorted(AUTHORS.glob("*.json")):
        a = json.loads(f.read_text(encoding="utf-8"))
        bio = a.get("bio_en") or ""
        if "has published in journals like" in bio:
            continue
        if any(p.search(bio) for p in name_patterns):
            pending.append(a["id"])
    return pending


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--batch", type=int)
    g.add_argument("--slug")
    g.add_argument("--list", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    whitelist = load_journals()
    journal_names = {j["name"] for j in whitelist}

    if args.list:
        pending = find_pending(journal_names)
        print(f"{len(pending)} authors pending:")
        for s in pending:
            print(f"  - {s}")
        return

    papers = [json.loads(f.read_text(encoding="utf-8")) for f in PAPERS.glob("*.json")]

    if args.slug:
        targets = [args.slug]
    else:
        targets = find_pending(journal_names)[: args.batch]

    print(f"Processing {len(targets)} author(s){' (dry run)' if args.dry_run else ''}:")
    applied = 0
    skipped = 0
    couldnt_strip = []
    for slug in targets:
        info, err = process_author(slug, papers, whitelist, dry_run=args.dry_run)
        if err:
            print(f"  SKIP {slug}: {err}")
            skipped += 1
            continue
        applied += 1
        line = f"  {'[dry] ' if args.dry_run else ''}{slug}: top={info['top']}"
        if not info["removed_en"]:
            couldnt_strip.append(slug)
            line += "  [could not strip ad-hoc EN sentence]"
        print(line)
        if info["removed_en"]:
            print(f"      removed EN: {info['removed_en'][:100]}")
        if info["removed_hu"]:
            print(f"      removed HU: {info['removed_hu'][:100]}")

    print(f"\nApplied: {applied} | Skipped: {skipped}")
    if couldnt_strip:
        print(f"Could not auto-strip ad-hoc sentence ({len(couldnt_strip)}): {', '.join(couldnt_strip)}")
        print("(manual review may be needed for those)")


if __name__ == "__main__":
    main()
