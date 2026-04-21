#!/usr/bin/env python
"""Paper ingestion pipeline for Evidence for Hungary.

Stages (see docs/WORKFLOW.md):
  1. discover   — fetch paper list from OpenAlex for an author → stub JSONs
  2. metadata   — fill DOI, abstract, volume/issue from Crossref / OpenAlex
  3. draft      — have Claude write summary / data / policy / tags

Usage:
  python scripts/ingest.py discover <author_id>
  python scripts/ingest.py metadata <paper_id>
  python scripts/ingest.py draft <paper_id>
  python scripts/ingest.py run <author_id>              # all three, in order
  python scripts/ingest.py draft <paper_id> --dry-run   # print prompt, no API call
  python scripts/ingest.py status

Requires:
  pip install -r scripts/requirements.txt
  ANTHROPIC_API_KEY env var (draft stage only)

Policy:
  - Only affects data/papers/<slug>.json and data/authors/<slug>.json — never other files.
  - Skips papers that already have review_status other than `discovered` / `metadata-fetched`
    unless --force is passed. Human-reviewed content is not overwritten.
  - Rate-limits politely (sleeps 0.5s between OpenAlex calls).
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

try:
    import requests
except ImportError:
    print("ERROR: pip install requests anthropic", file=sys.stderr)
    sys.exit(1)

# Force UTF-8 stdout/stderr on Windows so Unicode in prompts / logs doesn't crash.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

ROOT = Path(__file__).parent.parent
DATA = ROOT / "data"
AUTHORS_DIR = DATA / "authors"
PAPERS_DIR = DATA / "papers"

OPENALEX_EMAIL = os.environ.get("OPENALEX_EMAIL", "bekesg@ceu.edu")
OPENALEX_HEADERS = {"User-Agent": f"EvidenceForHungary/0.1 (mailto:{OPENALEX_EMAIL})"}

CONTROLLED = {
    "topics": [
        "labor-markets", "education-skills", "health", "demographics-migration",
        "trade-fdi", "firms-productivity", "innovation-digital", "banking-finance",
        "fiscal-tax", "regional-urban", "energy-environment", "inequality-welfare",
        "political-economy", "transition-postcommunist", "methods",
    ],
    "methods": [
        "rct", "diff-in-diff", "iv", "rd", "panel-data", "synthetic-control",
        "structural", "theory", "time-series", "ml-text", "descriptive-survey",
    ],
    "data_types": [
        "admin-firm", "admin-tax", "admin-individual", "survey",
        "firm-level-dataset", "field-experiment", "macro-aggregate",
        "digital-trace", "historical",
    ],
}


# ---------------- helpers ----------------

def load_json(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def dump_json(path: Path, data: Any) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def slugify(s: str) -> str:
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s


def surname(name: str) -> str:
    """Extract surname. Accepts either a display name ('Gábor Békés') or one of our
    internal author IDs ('bekes-gabor') — internal IDs are `<surname>-<given>` so we
    take the first dash-segment."""
    if "-" in name and " " not in name:
        return name.split("-")[0]
    tokens = [t for t in re.split(r"\s+", name.strip()) if t]
    if not tokens:
        return "unknown"
    return slugify(tokens[-1])


def _normalize_journal(s: str) -> str:
    s = s.lower().strip()
    s = re.sub(r"^the\s+", "", s)   # OpenAlex sometimes includes a leading "The "
    s = re.sub(r"\s+", " ", s)
    return s


def journal_short(name: str, journals: list[dict]) -> str:
    if not name:
        return "wp"
    target = _normalize_journal(name)
    for j in journals:
        if _normalize_journal(j["name"]) == target:
            return j["short"].lower().replace(":", "").replace("&", "and")
    # Fallback: first letters of each word
    words = [w for w in re.split(r"[\s\-]+", name) if w and w[0].isalpha()]
    return slugify("".join(w[0] for w in words[:5]))


def build_paper_slug(title: str, authors: list[str], year: int | None, journal: str, journals: list[dict]) -> str:
    """Slug = <first-surname>[-<second-surname>|-et-al]-<year>-<outlet>."""
    year_s = str(year) if year else "nd"
    surnames = [surname(a) for a in authors[:3] if a]
    if not surnames:
        surnames = [slugify(title.split()[0])]
    if len(authors) == 1:
        prefix = surnames[0]
    elif len(authors) == 2:
        prefix = f"{surnames[0]}-{surnames[1]}"
    else:
        prefix = f"{surnames[0]}-{surnames[1]}-et-al"
    short = journal_short(journal, journals)
    return f"{prefix}-{year_s}-{short}"


def author_name(a: dict) -> str:
    return a.get("name_en") or a.get("name_hu") or a["id"]


def log(stage: str, msg: str) -> None:
    print(f"[{stage}] {msg}")


# ---------------- stage 1: OpenAlex author lookup ----------------

def openalex_find_author(author: dict) -> str | None:
    """Return an OpenAlex author ID (e.g., 'A5012345') for the given author JSON.
    Uses name + Hungarian affiliation heuristics. Cached back into author JSON."""
    if author.get("openalex_id"):
        return author["openalex_id"]

    q = author["name_en"]
    params = {
        "search": q,
        "per_page": 10,
        "mailto": OPENALEX_EMAIL,
    }
    r = requests.get("https://api.openalex.org/authors", params=params, headers=OPENALEX_HEADERS, timeout=30)
    r.raise_for_status()
    results = r.json().get("results", [])
    if not results:
        return None

    # Pick the best: prefer someone whose last-known institution mentions an
    # affiliation from our author JSON, else the highest-cited match.
    affil_strings = [x.get("name", "") for x in author.get("affiliations", [])]
    affil_strings = [s.lower() for s in affil_strings if s]

    def score(a):
        inst = (a.get("last_known_institution") or {}).get("display_name", "") or ""
        inst_l = inst.lower()
        overlap = sum(1 for s in affil_strings if any(w in inst_l for w in s.lower().split()))
        return (overlap, a.get("works_count", 0))

    results.sort(key=score, reverse=True)
    best = results[0]
    oid = best["id"].split("/")[-1]  # strip prefix → "A5012345"
    log("discover", f"matched {q} → {best['display_name']} ({best.get('last_known_institution', {}).get('display_name', '?')}) [{oid}]")
    return oid


def openalex_works(openalex_id: str, max_works: int = 60,
                   since_year: int | None = None,
                   sort: str = "cited_by_count:desc") -> list[dict]:
    """Return the list of works by this author from OpenAlex.

    sort options: 'cited_by_count:desc' (default, top-cited), 'publication_year:desc' (newest first).
    since_year: optional lower bound on publication_year, inclusive.
    """
    works = []
    cursor = "*"
    filter_parts = [f"author.id:{openalex_id}"]
    if since_year:
        filter_parts.append(f"publication_year:>{since_year - 1}")
    flt = ",".join(filter_parts)
    while True:
        params = {
            "filter": flt,
            "sort": sort,
            "per_page": 50,
            "cursor": cursor,
            "mailto": OPENALEX_EMAIL,
        }
        r = requests.get("https://api.openalex.org/works", params=params, headers=OPENALEX_HEADERS, timeout=30)
        r.raise_for_status()
        j = r.json()
        works.extend(j.get("results", []))
        cursor = j.get("meta", {}).get("next_cursor")
        if not cursor or len(works) >= max_works:
            break
        time.sleep(0.3)
    return works[:max_works]


# ---------------- stage 1b: map OpenAlex → our paper schema ----------------

def openalex_to_paper_stub(w: dict, author_id: str, journals: list[dict],
                            known_authors: dict[str, dict]) -> dict | None:
    """Convert one OpenAlex work into our paper schema (minimum fields).
    Returns None if the work is not eligible (no DOI and no strong venue, or wrong type)."""
    wtype = w.get("type", "")
    if wtype not in ("article", "book-chapter", "preprint"):
        return None
    title = w.get("title") or w.get("display_name")
    if not title:
        return None

    year = w.get("publication_year")
    doi = (w.get("doi") or "").replace("https://doi.org/", "") or None

    venue = w.get("primary_location", {}).get("source") or {}
    journal = (venue.get("display_name") or "") if venue.get("type") != "repository" else ""

    pub_type = "article"
    if wtype == "book-chapter":
        pub_type = "chapter"
    elif wtype == "preprint" or not journal:
        pub_type = "working_paper"
        journal = None

    # Authors: map to our known-author IDs where possible, else pass through name.
    oa_authors = []
    for a in w.get("authorships", []):
        dname = a.get("author", {}).get("display_name", "")
        if not dname:
            continue
        matched_id = _match_author_name(dname, known_authors)
        oa_authors.append(matched_id or dname)

    # Make sure the originating author is in the list.
    if author_id not in oa_authors:
        oa_authors.insert(0, author_id)

    biblio = w.get("biblio", {}) or {}
    abstract = _reconstruct_abstract(w.get("abstract_inverted_index"))

    slug = build_paper_slug(title, oa_authors, year, journal or "", journals)

    return {
        "id": slug,
        "title": title,
        "authors": oa_authors,
        "publication_type": pub_type,
        "journal": journal,
        "year": year,
        "volume": biblio.get("volume"),
        "issue": biblio.get("issue"),
        "pages": (f"{biblio.get('first_page')}-{biblio.get('last_page')}"
                  if biblio.get("first_page") else None),
        "doi": doi,
        "working_paper_series": None,
        "url_published": w.get("doi"),
        "url_pdf": (w.get("primary_location") or {}).get("pdf_url"),
        "url_replication": None,
        "abstract": abstract,
        "summary_en": None,
        "summary_hu": None,
        "data_used": None,
        "data_used_hu": None,
        "policy_relevance": None,
        "policy_relevance_hu": None,
        "topics": [],
        "methods": [],
        "countries_studied": [],
        "data_types": [],
        "featured": False,
        "added_at": time.strftime("%Y-%m-%d"),
        "last_reviewed_at": time.strftime("%Y-%m-%d"),
        "review_status": "discovered",
        "openalex_id": w.get("id", "").split("/")[-1],
    }


def _reconstruct_abstract(inv: dict | None) -> str | None:
    if not inv:
        return None
    pairs = []
    for word, positions in inv.items():
        for p in positions:
            pairs.append((p, word))
    pairs.sort()
    return " ".join(w for _, w in pairs)


def _match_author_name(name: str, known: dict[str, dict]) -> str | None:
    target = slugify(name)
    # try exact surname+given match
    for aid, a in known.items():
        if slugify(a["name_en"]) == target:
            return aid
    # try surname only (last token)
    tokens = target.split("-")
    if tokens:
        tail = tokens[-1]
        for aid, a in known.items():
            if slugify(a["name_en"]).split("-")[-1] == tail:
                return aid
    return None


# ---------------- stage commands ----------------

def cmd_discover(author_id: str, max_works: int, force: bool,
                 since_year: int | None = None,
                 sort: str = "cited_by_count:desc") -> list[str]:
    author_path = AUTHORS_DIR / f"{author_id}.json"
    if not author_path.exists():
        raise SystemExit(f"No author file at {author_path}")
    author = load_json(author_path)
    journals = load_json(DATA / "journals.json")
    known = {p.stem: load_json(p) for p in AUTHORS_DIR.glob("*.json")}

    oid = openalex_find_author(author)
    if not oid:
        log("discover", f"No OpenAlex match for {author_name(author)}")
        return []
    if author.get("openalex_id") != oid:
        author["openalex_id"] = oid
        dump_json(author_path, author)

    log("discover", f"Fetching up to {max_works} works for {author_name(author)} "
                    f"(sort={sort}" + (f", since={since_year})" if since_year else ")"))
    works = openalex_works(oid, max_works=max_works, since_year=since_year, sort=sort)
    log("discover", f"{len(works)} works returned by OpenAlex")

    created = 0
    existing = 0
    for w in works:
        stub = openalex_to_paper_stub(w, author_id, journals, known)
        if not stub:
            continue
        path = PAPERS_DIR / f"{stub['id']}.json"
        if path.exists() and not force:
            existing += 1
            continue
        dump_json(path, stub)
        created += 1

    log("discover", f"Created {created} paper stub(s); {existing} already existed (use --force to overwrite)")
    return [p.stem for p in PAPERS_DIR.glob("*.json")]


def cmd_metadata(paper_id: str, force: bool) -> None:
    path = PAPERS_DIR / f"{paper_id}.json"
    if not path.exists():
        raise SystemExit(f"No paper file at {path}")
    p = load_json(path)
    if p.get("review_status") in ("human-reviewed", "author-approved") and not force:
        log("metadata", f"{paper_id} is {p['review_status']} — skipping (use --force)")
        return

    if not p.get("doi"):
        log("metadata", f"{paper_id}: no DOI, skipping Crossref")
    else:
        r = requests.get(f"https://api.crossref.org/works/{p['doi']}", timeout=30)
        if r.ok:
            msg = r.json().get("message", {})
            p["volume"] = p.get("volume") or msg.get("volume")
            p["issue"] = p.get("issue") or (msg.get("issue"))
            if not p.get("pages") and msg.get("page"):
                p["pages"] = msg["page"]
            if not p.get("abstract") and msg.get("abstract"):
                # Crossref abstracts are JATS XML — strip tags.
                p["abstract"] = re.sub(r"<[^>]+>", "", msg["abstract"]).strip()
        else:
            log("metadata", f"Crossref {r.status_code} for {p['doi']}")

    p["review_status"] = "metadata-fetched" if p["review_status"] == "discovered" else p["review_status"]
    p["last_reviewed_at"] = time.strftime("%Y-%m-%d")
    dump_json(path, p)
    log("metadata", f"{paper_id}: abstract={'yes' if p.get('abstract') else 'no'}")


# ---------------- stage 4: Claude drafting ----------------

DRAFT_SYSTEM = """You are drafting a policy-facing entry for a Hungarian economics research catalogue called "Evidence for Hungary". The audience is Hungarian ministry staff — smart, educated, not necessarily economists.

For each paper you will produce FOUR outputs in a single JSON object:

1. summary_en — 80 to 150 words, 2–3 sentences.
   - What question did the paper ask, what did they find, why is it interesting.
   - No jargon; define any term that must appear.
   - Name the country or setting studied explicitly ("In Hungary, …" not "We find …").
   - DO NOT paraphrase the abstract closely. Rewrite entirely for a non-economist reader.

2. data_used — 40 to 80 words.
   - What data? Source, years, scale (number of firms / people / observations), country.
   - Be concrete: "Hungarian firm-level tax data 2005–2020, ~12,000 firms, annual panel" is good; "administrative data" is not.
   - For theoretical papers, write "Theoretical paper; no empirical data."

3. policy_relevance — 60 to 120 words.
   - What should a Hungarian policymaker take from this? Be specific: which ministry, which program, which lever.
   - Include at least one caveat on generalisability — if the evidence is from another country, flag it.
   - For theoretical papers, discuss which empirical regularities would need to hold for the theory to apply to Hungary.

4. tags — a JSON object with keys:
   - topics: array of 1 to 3 IDs from {TOPICS}
   - methods: array of 1 to 2 IDs from {METHODS}
   - data_types: array of 1 to 3 IDs from {DATA_TYPES} (empty array [] for theory papers)
   - countries: array of ISO 3166-1 alpha-2 codes, or the group codes EU / EEA / CEE / V4 / GLOBAL / TRANSITION
   - policy_instruments: array of 0 to 5 concrete policy instruments, programs, or levers the paper studies or directly informs. Examples: "minimum wage", "family tax allowance", "EU structural funds", "unemployment insurance rules", "school tracking age", "cigarette excise tax", "occupational health screening", "state advertising allocation", "pension benefit formula". Short phrases. NOT generic labels like "tax policy" or "education policy" — those are already topics. Be specific: a policymaker should be able to map each entry to a real lever they control. For Hungarian-context papers, prefer Hungarian terms ("minimálbér", "családi adókedvezmény", "CSOK"). For theory papers with no direct instrument, return []. Omit entirely if the paper doesn't discuss specific instruments.

If a field cannot be determined confidently from the abstract alone, add a 5th field:
   uncertain: object mapping field name → one-sentence note.

RETURN VALID JSON ONLY. No prose before or after. No markdown fencing."""


def _fill_vocab(sys_prompt: str) -> str:
    return (sys_prompt
        .replace("{TOPICS}", ", ".join(CONTROLLED["topics"]))
        .replace("{METHODS}", ", ".join(CONTROLLED["methods"]))
        .replace("{DATA_TYPES}", ", ".join(CONTROLLED["data_types"])))


def _user_prompt(p: dict, authors_lookup: dict[str, dict]) -> str:
    author_names = []
    for a in p.get("authors", []):
        author_names.append(authors_lookup.get(a, {}).get("name_en") or a)
    return (
        f"TITLE: {p.get('title', '')}\n"
        f"AUTHORS: {', '.join(author_names)}\n"
        f"JOURNAL/OUTLET: {p.get('journal') or p.get('working_paper_series') or '(working paper)'}\n"
        f"YEAR: {p.get('year', '')}\n"
        f"ABSTRACT: {p.get('abstract') or '(no abstract available)'}\n"
    )


def cmd_draft(paper_id: str, force: bool, dry_run: bool, model: str = "claude-opus-4-7") -> None:
    path = PAPERS_DIR / f"{paper_id}.json"
    if not path.exists():
        raise SystemExit(f"No paper file at {path}")
    p = load_json(path)
    if p.get("review_status") in ("human-reviewed", "author-approved") and not force:
        log("draft", f"{paper_id} is {p['review_status']} — skipping (use --force)")
        return
    if not p.get("abstract") and not force:
        log("draft", f"{paper_id} has no abstract — skipping (run metadata first, or --force)")
        return

    authors_lookup = {pth.stem: load_json(pth) for pth in AUTHORS_DIR.glob("*.json")}
    system = _fill_vocab(DRAFT_SYSTEM)
    user = _user_prompt(p, authors_lookup)

    if dry_run:
        print("---- SYSTEM ----")
        print(system)
        print("---- USER ----")
        print(user)
        return

    try:
        import anthropic
    except ImportError:
        raise SystemExit("pip install anthropic (or run with --dry-run)")
    if not os.environ.get("ANTHROPIC_API_KEY"):
        raise SystemExit("Set ANTHROPIC_API_KEY in env to draft, or use --dry-run.")

    client = anthropic.Anthropic()
    log("draft", f"{paper_id}: calling Claude ({model}) …")
    msg = client.messages.create(
        model=model,
        max_tokens=1500,
        system=[{
            "type": "text",
            "text": system,
            "cache_control": {"type": "ephemeral"},
        }],
        messages=[{"role": "user", "content": user}],
    )
    raw = "".join(b.text for b in msg.content if getattr(b, "type", None) == "text").strip()

    # Strip any accidental code fences.
    raw = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw, flags=re.MULTILINE).strip()

    try:
        obj = json.loads(raw)
    except json.JSONDecodeError as e:
        log("draft", f"{paper_id}: JSON parse failed: {e}. Saving raw to {path.stem}.draft.txt")
        (PAPERS_DIR / f"{paper_id}.draft.txt").write_text(raw, encoding="utf-8")
        return

    tags = obj.get("tags", {}) or {}
    topics = [t for t in tags.get("topics", []) if t in CONTROLLED["topics"]][:3]
    methods = [m for m in tags.get("methods", []) if m in CONTROLLED["methods"]][:2]
    data_types = [d for d in tags.get("data_types", []) if d in CONTROLLED["data_types"]][:3]
    countries = [c for c in tags.get("countries", []) if isinstance(c, str)][:5]
    policy_instruments = [
        str(x).strip() for x in tags.get("policy_instruments", [])
        if isinstance(x, str) and x.strip()
    ][:5]

    if obj.get("summary_en"):
        p["summary_en"] = obj["summary_en"].strip()
    if obj.get("data_used"):
        p["data_used"] = obj["data_used"].strip()
    if obj.get("policy_relevance"):
        p["policy_relevance"] = obj["policy_relevance"].strip()

    # Only overwrite tag fields if the AI produced anything.
    if topics:
        p["topics"] = topics
    if methods:
        p["methods"] = methods
    if data_types:
        p["data_types"] = data_types
    if policy_instruments:
        p["policy_instruments"] = policy_instruments
    if countries:
        p["countries_studied"] = countries

    if obj.get("uncertain"):
        p["uncertain"] = obj["uncertain"]

    p["review_status"] = "ai-drafted"
    p["last_reviewed_at"] = time.strftime("%Y-%m-%d")
    dump_json(path, p)

    usage = getattr(msg, "usage", None)
    if usage:
        log("draft",
            f"{paper_id}: done. tokens in={usage.input_tokens} out={usage.output_tokens} "
            f"cache_create={getattr(usage, 'cache_creation_input_tokens', 0)} "
            f"cache_read={getattr(usage, 'cache_read_input_tokens', 0)}")
    else:
        log("draft", f"{paper_id}: done.")


# ---------------- run all / status ----------------

def cmd_run(author_id: str, max_works: int, dry_run: bool, force: bool, model: str) -> None:
    stubs = cmd_discover(author_id, max_works=max_works, force=force)
    # process only this author's new papers:
    affected = [p.stem for p in PAPERS_DIR.glob("*.json")
                if author_id in load_json(p).get("authors", [])]
    for pid in sorted(affected):
        p = load_json(PAPERS_DIR / f"{pid}.json")
        if p.get("review_status") == "discovered":
            try:
                cmd_metadata(pid, force=False)
            except Exception as e:
                log("metadata", f"{pid}: error {e}")
            time.sleep(0.3)
    for pid in sorted(affected):
        p = load_json(PAPERS_DIR / f"{pid}.json")
        if p.get("review_status") in ("discovered", "metadata-fetched"):
            try:
                cmd_draft(pid, force=False, dry_run=dry_run, model=model)
            except Exception as e:
                log("draft", f"{pid}: error {e}")
            time.sleep(0.3)


def cmd_status() -> None:
    papers = [load_json(p) for p in PAPERS_DIR.glob("*.json")]
    from collections import Counter
    by_status = Counter(p.get("review_status", "?") for p in papers)
    by_author = Counter()
    for p in papers:
        for a in p.get("authors", []):
            by_author[a] += 1
    print(f"Papers: {len(papers)}")
    for s, c in by_status.most_common():
        print(f"  {s}: {c}")
    print("\nPapers per known author (top 10):")
    known = {pth.stem for pth in AUTHORS_DIR.glob("*.json")}
    for aid, c in by_author.most_common(20):
        if aid in known:
            print(f"  {aid}: {c}")


# ---------------- CLI ----------------

def main() -> None:
    p = argparse.ArgumentParser(description="Evidence for Hungary — paper ingestion pipeline")
    sub = p.add_subparsers(dest="cmd", required=True)

    d = sub.add_parser("discover", help="fetch paper list for an author")
    d.add_argument("author_id")
    d.add_argument("--max-works", type=int, default=40)
    d.add_argument("--force", action="store_true")
    d.add_argument("--since-year", type=int, default=None,
                   help="only fetch works from this year onward")
    d.add_argument("--sort", default="cited_by_count:desc",
                   choices=["cited_by_count:desc", "publication_year:desc"],
                   help="OpenAlex sort order")

    m = sub.add_parser("metadata", help="fetch Crossref metadata for a paper")
    m.add_argument("paper_id")
    m.add_argument("--force", action="store_true")

    df = sub.add_parser("draft", help="have Claude draft summary / tags for a paper")
    df.add_argument("paper_id")
    df.add_argument("--force", action="store_true")
    df.add_argument("--dry-run", action="store_true")
    df.add_argument("--model", default="claude-opus-4-7")

    r = sub.add_parser("run", help="discover → metadata → draft for an author")
    r.add_argument("author_id")
    r.add_argument("--max-works", type=int, default=40)
    r.add_argument("--dry-run", action="store_true")
    r.add_argument("--force", action="store_true")
    r.add_argument("--model", default="claude-opus-4-7")

    sub.add_parser("status", help="summarise pipeline state")

    args = p.parse_args()
    if args.cmd == "discover":
        cmd_discover(args.author_id, args.max_works, args.force,
                     since_year=args.since_year, sort=args.sort)
    elif args.cmd == "metadata":
        cmd_metadata(args.paper_id, args.force)
    elif args.cmd == "draft":
        cmd_draft(args.paper_id, args.force, args.dry_run, args.model)
    elif args.cmd == "run":
        cmd_run(args.author_id, args.max_works, args.dry_run, args.force, args.model)
    elif args.cmd == "status":
        cmd_status()


if __name__ == "__main__":
    main()
