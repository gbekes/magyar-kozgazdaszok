"""For each author whose bio doesn't yet mention a journal from
data/journals.json, append a sentence:

    "<Author> has published in journals like <J1>, <J2> and <J3>."

(and the Hungarian equivalent in bio_hu).

Top 3 journals are chosen from the author's papers in data/papers/, filtered
to the whitelist, ranked by tier (A > B) then by frequency.

Usage:
    python scripts/add_journals_sentence.py --batch <N>     # next batch of 10
    python scripts/add_journals_sentence.py --slug <id>     # single author
    python scripts/add_journals_sentence.py --list          # show pending list
    python scripts/add_journals_sentence.py --dry-run --batch <N>
"""
import argparse
import json
import sys
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
AUTHORS = ROOT / "data" / "authors"
PAPERS = ROOT / "data" / "papers"
JOURNALS = ROOT / "journals.json"


def load_journals():
    return json.loads(JOURNALS.read_text(encoding="utf-8"))


def needs_sentence(author, journal_names):
    bio = author.get("bio_en") or ""
    # Already-added template counts as "has it"
    if "has published in journals like" in bio:
        return False
    return not any(jn in bio for jn in journal_names)


HUNGARIAN_ONLY = {
    "Közgazdasági Szemle",
    "Statisztikai Szemle",
    "Külgazdaság",
    "Magyar Tudomány",
    "Demográfia",
    "Szociológiai Szemle",
    "Society and Economy",
    "Acta Oeconomica",
    "Hungarian Statistical Review",
    "Területi Statisztika",
}


def author_top_journals(slug, papers, whitelist):
    """Return up to 3 journal names where this author has published.

    Ranking: whitelist tier A > whitelist tier B > other international
    (non-Hungarian-only) journals; within tier by frequency. As a last
    resort, fall back to Hungarian-only journals if nothing else exists.
    """
    by_name = {j["name"]: j for j in whitelist}
    counts = Counter()
    for p in papers:
        if slug not in (p.get("authors") or []):
            continue
        jname = p.get("journal")
        if jname:
            counts[jname] += 1
    if not counts:
        return []

    def tier_of(name):
        if name in by_name:
            t = by_name[name].get("tier")
            return 0 if t == "A" else 1 if t == "B" else 2
        if name in HUNGARIAN_ONLY:
            return 4  # last resort
        return 3  # other international

    ranked = sorted(counts.items(), key=lambda kv: (tier_of(kv[0]), -kv[1], kv[0]))
    return [name for name, _ in ranked[:3]]


def join_journals_en(journals):
    if len(journals) == 1:
        return journals[0]
    if len(journals) == 2:
        return f"{journals[0]} and {journals[1]}"
    return f"{', '.join(journals[:-1])} and {journals[-1]}"


def hu_article(name):
    """Hungarian definite article: 'az' before vowel, 'a' before consonant."""
    if not name:
        return "a"
    return "az" if name[0].lower() in "aeiouáéíóöőúüű" else "a"


def with_article(name):
    return f"{hu_article(name)} {name}"


def join_journals_hu(journals):
    if len(journals) == 1:
        return with_article(journals[0])
    if len(journals) == 2:
        return f"{with_article(journals[0])} és {with_article(journals[1])}"
    return f"{', '.join(with_article(j) for j in journals[:-1])} és {with_article(journals[-1])}"


def en_sentence(name_en, journals):
    return f"{name_en} has published in journals like {join_journals_en(journals)}."


def hu_sentence(name_hu, journals):
    return f"{name_hu} tanulmányai olyan folyóiratokban jelentek meg, mint {join_journals_hu(journals)}."


def find_pending(journal_names):
    pending = []
    for f in sorted(AUTHORS.glob("*.json")):
        a = json.loads(f.read_text(encoding="utf-8"))
        if needs_sentence(a, journal_names):
            pending.append(a["id"])
    return pending


def apply_to_author(slug, journal_names, whitelist, papers, dry_run=False):
    f = AUTHORS / f"{slug}.json"
    a = json.loads(f.read_text(encoding="utf-8"))
    if not needs_sentence(a, journal_names):
        return None, "already mentions a journal"

    top = author_top_journals(slug, papers, whitelist)
    if not top:
        return None, "no whitelisted-journal papers"

    name_en = a.get("name_en") or a.get("name_hu") or slug
    name_hu = a.get("name_hu") or a.get("name_en") or slug

    new_en = en_sentence(name_en, top)
    new_hu = hu_sentence(name_hu, top)

    bio_en = (a.get("bio_en") or "").rstrip()
    if bio_en and not bio_en.endswith("."):
        bio_en += "."
    bio_en = (bio_en + " " + new_en).strip() if bio_en else new_en

    bio_hu = (a.get("bio_hu") or "").rstrip()
    if bio_hu and not bio_hu.endswith("."):
        bio_hu += "."
    bio_hu = (bio_hu + " " + new_hu).strip() if bio_hu else new_hu

    a["bio_en"] = bio_en
    a["bio_hu"] = bio_hu

    if not dry_run:
        f.write_text(json.dumps(a, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return top, None


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--batch", type=int, help="Process next N pending authors")
    g.add_argument("--slug", help="Single author")
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

    targets = []
    if args.slug:
        targets = [args.slug]
    else:
        targets = find_pending(journal_names)[: args.batch]

    print(f"Processing {len(targets)} author(s){' (dry run)' if args.dry_run else ''}:")
    applied = 0
    skipped = 0
    for slug in targets:
        top, err = apply_to_author(slug, journal_names, whitelist, papers, dry_run=args.dry_run)
        if err:
            print(f"  SKIP {slug}: {err}")
            skipped += 1
        else:
            print(f"  {'[dry] ' if args.dry_run else ''}{slug}: top journals = {top}")
            applied += 1
    print(f"\nApplied: {applied} | Skipped: {skipped}")


if __name__ == "__main__":
    main()
