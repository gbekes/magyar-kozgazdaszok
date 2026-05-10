#!/usr/bin/env python
"""qa_sample.py — sampling-based content QA for Magyar Közgazdászok.

Picks one random item per test slot and reports PASS / FAIL / SKIP
with a one-line diagnostic. Same set of test SLOTS every run; the
items sampled in each slot vary. Slot count is whatever's listed in
run_all() — count is reported at the bottom of each run.

Eligibility filter: every test ignores items whose `review_status` is
`human-reviewed` or `author-approved`. The point is to spot-check the
ai-drafted / metadata-fetched layer, not to second-guess editor work.

Categories of failure (printed alongside each FAIL):
  - defect              : a real schema / cross-reference violation
  - format-warning      : SPEC length target not met (informative)
  - plausibility-flag   : looks suspicious; editor should glance at it
  - liveness-flag       : external URL or ID didn't resolve

Usage:
  python tests/qa_sample.py                # run all slots, print to stdout
  python tests/qa_sample.py --save         # also write to tests/reports/
  python tests/qa_sample.py --seed 42      # deterministic run

Dependencies: stdlib only (urllib for liveness tests).
"""
from __future__ import annotations
import argparse, json, random, re, sys, time, urllib.request, urllib.error
from pathlib import Path
from datetime import datetime

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
PAPERS_DIR = ROOT / "data" / "papers"
AUTHORS_DIR = ROOT / "data" / "authors"
POLICY_DIR = ROOT / "data" / "policy"
PRESS_DIR = ROOT / "data" / "press"
TOPICS_FILE = ROOT / "data" / "topics.json"
JOURNALS_FILE = ROOT / "data" / "journals.json"
MANIFEST_FILE = ROOT / "authors-seed.json"

# ---------- controlled vocabularies (mirrored from apply_drafts.py) -------
TOPIC_IDS = None  # loaded lazily
JOURNAL_NAMES = None
METHODS = {"rct", "diff-in-diff", "iv", "rd", "panel-data", "synthetic-control",
           "structural", "theory", "time-series", "ml-text", "descriptive-survey"}
DATA_TYPES = {"admin-firm", "admin-tax", "admin-individual", "survey",
              "firm-level-dataset", "field-experiment", "macro-aggregate",
              "digital-trace", "historical"}
SEMANTIC_COUNTRIES = {"GLOBAL", "global", "EU", "CEE", "TRANSITION"}
HU_INSTITUTIONS = {
    "MNB", "KSH", "NGM", "ITM", "NEAK", "NAV", "KRTK", "HIPA", "NKFIH",
    "AM", "EMMI", "BÉT", "MFB", "MÁK", "BM", "ÁKK", "OEP", "ONYF",
    "GVH", "KKM", "Pénzügyminisztérium", "Eximbank", "MEKH", "OFI",
    "Belügyminisztérium", "Egészségügyi", "Államtitkárság", "OKM",
    "PSZÁF", "Magyar Államkincstár", "Magyar Nemzeti Bank",
    "Köznevelési", "Oktatási Hivatal", "ETDA", "EBH", "ÁSZ",
}
REVIEW_STATUSES = {"metadata-fetched", "ai-drafted", "human-reviewed",
                   "author-approved"}
LOCKED_STATUSES = {"human-reviewed", "author-approved"}
TIMEOUT = 10  # seconds for liveness checks
USER_AGENT = "magyar-kozgazdaszok-qa/1.0 (+https://gbekes.github.io/magyar-kozgazdaszok)"


# ---------- loading helpers -----------------------------------------------
def load_json(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def load_all_papers():
    return [load_json(f) for f in sorted(PAPERS_DIR.glob("*.json"))]


def load_all_authors():
    return [load_json(f) for f in sorted(AUTHORS_DIR.glob("*.json"))]


def load_topic_ids():
    global TOPIC_IDS
    if TOPIC_IDS is None:
        TOPIC_IDS = {t["id"] for t in load_json(TOPICS_FILE)}
    return TOPIC_IDS


def load_journal_names():
    global JOURNAL_NAMES
    if JOURNAL_NAMES is None:
        JOURNAL_NAMES = {j["name"].strip().lower() for j in load_json(JOURNALS_FILE)}
    return JOURNAL_NAMES


def is_locked(item):
    return (item.get("review_status") or "") in LOCKED_STATUSES


def has(item, key):
    v = item.get(key)
    return bool(v) and bool(str(v).strip())


def is_slug(author_id: str) -> bool:
    """Slug authors are catalogued; non-slugs are external coauthors."""
    return bool(author_id) and author_id == author_id.lower() and " " not in author_id


def author_file_exists(author_id: str) -> bool:
    return (AUTHORS_DIR / f"{author_id}.json").exists()


def paper_file_exists(paper_id: str) -> bool:
    return (PAPERS_DIR / f"{paper_id}.json").exists()


def word_count(s: str) -> int:
    return len(re.findall(r"\S+", s or ""))


def looks_hungarian(s: str) -> bool:
    """Cheap heuristic: Hungarian text typically contains ő/ű/é/á/í/ó/ú."""
    if not s:
        return False
    return any(ch in s for ch in "őűéáíóúÖŐÜŰÉÁÍÓÚ")


def http_status(url: str, head: bool = False) -> int:
    """Return HTTP status code, or -1 if request failed."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        if head:
            req.get_method = lambda: "HEAD"
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception:
        return -1


# ---------- result dataclass-ish ------------------------------------------
class Result:
    __slots__ = ("tid", "name", "category", "outcome", "subject", "diagnostic")

    def __init__(self, tid, name, category, outcome, subject="", diagnostic=""):
        self.tid = tid
        self.name = name
        self.category = category  # defect | format-warning | plausibility-flag | liveness-flag
        self.outcome = outcome    # PASS | FAIL | SKIP
        self.subject = subject
        self.diagnostic = diagnostic

    def line(self) -> str:
        head = f"{self.tid}  {self.outcome:5}  {self.name:34}"
        if self.subject:
            head += f" — {self.subject}"
        if self.diagnostic:
            head += f" :: {self.diagnostic}"
        return head


def skip(tid, name, category, reason):
    return Result(tid, name, category, "SKIP", "", reason)


# ---------- the 25 tests --------------------------------------------------
def t01_author_ids(papers, rng):
    pool = [p for p in papers if not is_locked(p)
            and any(is_slug(a) for a in (p.get("authors") or []))]
    if not pool:
        return skip("T01", "Author-ID resolution", "defect", "pool empty")
    p = rng.choice(pool)
    bad = [a for a in p["authors"] if is_slug(a) and not author_file_exists(a)]
    if bad:
        return Result("T01", "Author-ID resolution", "defect", "FAIL",
                      f"paper {p['id']}", f"missing author files: {', '.join(bad)}")
    return Result("T01", "Author-ID resolution", "defect", "PASS",
                  f"paper {p['id']}")


def t02_topic_vocab(papers, rng):
    topics = load_topic_ids()
    pool = [p for p in papers if not is_locked(p) and (p.get("topics") or [])]
    if not pool:
        return skip("T02", "Topic vocabulary", "defect", "pool empty")
    p = rng.choice(pool)
    bad = [t for t in p["topics"] if t not in topics]
    if bad:
        return Result("T02", "Topic vocabulary", "defect", "FAIL",
                      f"paper {p['id']}", f"unknown topics: {', '.join(bad)}")
    return Result("T02", "Topic vocabulary", "defect", "PASS",
                  f"paper {p['id']}")


def t03_journal_whitelist(papers, rng):
    journals = load_journal_names()
    pool = [p for p in papers if not is_locked(p) and has(p, "journal")
            and (p.get("publication_type") in (None, "article"))]
    if not pool:
        return skip("T03", "Journal whitelist", "defect", "pool empty")
    p = rng.choice(pool)
    j = (p.get("journal") or "").strip().lower()
    if j not in journals:
        return Result("T03", "Journal whitelist", "defect", "FAIL",
                      f"paper {p['id']}", f"journal '{p['journal']}' not in journals.json")
    return Result("T03", "Journal whitelist", "defect", "PASS",
                  f"paper {p['id']}")


def t04_methods_vocab(papers, rng):
    pool = [p for p in papers if not is_locked(p) and (p.get("methods") or [])]
    if not pool:
        return skip("T04", "Methods vocabulary", "defect", "pool empty")
    p = rng.choice(pool)
    bad = [m for m in p["methods"] if m not in METHODS]
    if bad:
        return Result("T04", "Methods vocabulary", "defect", "FAIL",
                      f"paper {p['id']}", f"unknown methods: {', '.join(bad)}")
    return Result("T04", "Methods vocabulary", "defect", "PASS",
                  f"paper {p['id']}")


def t05_data_types_vocab(papers, rng):
    pool = [p for p in papers if not is_locked(p) and (p.get("data_types") or [])]
    if not pool:
        return skip("T05", "Data-types vocabulary", "defect", "pool empty")
    p = rng.choice(pool)
    bad = [d for d in p["data_types"] if d not in DATA_TYPES]
    if bad:
        return Result("T05", "Data-types vocabulary", "defect", "FAIL",
                      f"paper {p['id']}", f"unknown data_types: {', '.join(bad)}")
    return Result("T05", "Data-types vocabulary", "defect", "PASS",
                  f"paper {p['id']}")


def t06_country_codes(papers, rng):
    pool = [p for p in papers if not is_locked(p) and (p.get("countries_studied") or [])]
    if not pool:
        return skip("T06", "Country-code shape", "defect", "pool empty")
    p = rng.choice(pool)
    bad = [c for c in p["countries_studied"]
           if not (re.fullmatch(r"[A-Z]{2}", c) or c in SEMANTIC_COUNTRIES)]
    if bad:
        return Result("T06", "Country-code shape", "defect", "FAIL",
                      f"paper {p['id']}", f"non-ISO2 / non-semantic: {', '.join(bad)}")
    return Result("T06", "Country-code shape", "defect", "PASS",
                  f"paper {p['id']}")


def t07_summary_en_length(papers, rng):
    pool = [p for p in papers if not is_locked(p) and has(p, "summary_en")]
    if not pool:
        return skip("T07", "summary_en length", "format-warning", "pool empty")
    p = rng.choice(pool)
    n = word_count(p["summary_en"])
    if not (60 <= n <= 180):
        return Result("T07", "summary_en length", "format-warning", "FAIL",
                      f"paper {p['id']}", f"{n} words (target 60-180; SPEC 80-150)")
    return Result("T07", "summary_en length", "format-warning", "PASS",
                  f"paper {p['id']}", f"{n} words")


def t08_data_used_length(papers, rng):
    pool = [p for p in papers if not is_locked(p) and has(p, "data_used")]
    if not pool:
        return skip("T08", "data_used length", "format-warning", "pool empty")
    p = rng.choice(pool)
    n = word_count(p["data_used"])
    if not (25 <= n <= 110):
        return Result("T08", "data_used length", "format-warning", "FAIL",
                      f"paper {p['id']}", f"{n} words (target 25-110; SPEC 40-80)")
    return Result("T08", "data_used length", "format-warning", "PASS",
                  f"paper {p['id']}", f"{n} words")


def t09_policy_length(papers, rng):
    pool = [p for p in papers if not is_locked(p) and has(p, "policy_relevance")]
    if not pool:
        return skip("T09", "policy_relevance length", "format-warning", "pool empty")
    p = rng.choice(pool)
    n = word_count(p["policy_relevance"])
    if not (45 <= n <= 160):
        return Result("T09", "policy_relevance length", "format-warning", "FAIL",
                      f"paper {p['id']}", f"{n} words (target 45-160; SPEC 60-120)")
    return Result("T09", "policy_relevance length", "format-warning", "PASS",
                  f"paper {p['id']}", f"{n} words")


def t10_hu_en_ratio(papers, rng):
    pool = [p for p in papers if not is_locked(p)
            and has(p, "summary_en") and has(p, "summary_hu")]
    if not pool:
        return skip("T10", "HU/EN length ratio", "format-warning", "pool empty")
    p = rng.choice(pool)
    en, hu = len(p["summary_en"]), len(p["summary_hu"])
    if hu < 0.4 * en or hu > 1.6 * en:
        return Result("T10", "HU/EN length ratio", "format-warning", "FAIL",
                      f"paper {p['id']}", f"HU={hu} ch, EN={en} ch (ratio {hu/en:.2f})")
    return Result("T10", "HU/EN length ratio", "format-warning", "PASS",
                  f"paper {p['id']}", f"ratio {hu/en:.2f}")


def t11_qualifying_pub(authors, papers, rng):
    pool = [a for a in authors if not is_locked(a)
            and isinstance(a.get("qualifying_publication"), dict)
            and (a["qualifying_publication"].get("title") or "").strip()]
    if not pool:
        return skip("T11", "Qualifying publication exists", "defect", "pool empty")
    a = rng.choice(pool)
    qp = a["qualifying_publication"]
    qt = (qp.get("title") or "").strip().lower()
    qy = qp.get("year")
    qj = (qp.get("journal") or "").strip().lower()
    matches = [p for p in papers
               if a["id"] in (p.get("authors") or [])
               and (p.get("title") or "").strip().lower() == qt]
    if not matches:
        # second pass: same author + same year + same journal (title may have minor diffs)
        matches = [p for p in papers
                   if a["id"] in (p.get("authors") or [])
                   and (p.get("year") == qy)
                   and (p.get("journal") or "").strip().lower() == qj]
    if not matches:
        return Result("T11", "Qualifying publication exists", "defect", "FAIL",
                      f"author {a['id']}", f"qualifying paper '{qp.get('title','')[:40]}' ({qy}) not in data/papers/")
    return Result("T11", "Qualifying publication exists", "defect", "PASS",
                  f"author {a['id']}")


def t12_author_has_papers(authors, papers, rng):
    paper_authors = set()
    for p in papers:
        for a in (p.get("authors") or []):
            paper_authors.add(a)
    pool = [a for a in authors if not is_locked(a)]
    if not pool:
        return skip("T12", "Author has ≥1 paper", "defect", "pool empty")
    a = rng.choice(pool)
    if a["id"] not in paper_authors:
        return Result("T12", "Author has ≥1 paper", "defect", "FAIL",
                      f"author {a['id']}", "no paper lists this author id")
    return Result("T12", "Author has ≥1 paper", "defect", "PASS",
                  f"author {a['id']}")


def t13_press_link(rng):
    if not PRESS_DIR.exists():
        return skip("T13", "Press → paper link", "defect", "no press/ dir")
    items = [load_json(f) for f in PRESS_DIR.glob("*.json")]
    pool = [i for i in items if not is_locked(i) and (i.get("linked_paper_id") or "").strip()]
    if not pool:
        return skip("T13", "Press → paper link", "defect", "pool empty")
    item = rng.choice(pool)
    pid = item["linked_paper_id"]
    if not paper_file_exists(pid):
        return Result("T13", "Press → paper link", "defect", "FAIL",
                      f"press {item['id']}", f"linked_paper_id '{pid}' missing")
    return Result("T13", "Press → paper link", "defect", "PASS",
                  f"press {item['id']}")


def t14_policy_link(rng):
    if not POLICY_DIR.exists():
        return skip("T14", "Policy → paper link", "defect", "no policy/ dir")
    items = [load_json(f) for f in POLICY_DIR.glob("*.json")]
    pool = [i for i in items if not is_locked(i) and (i.get("linked_paper_id") or "").strip()]
    if not pool:
        return skip("T14", "Policy → paper link", "defect", "pool empty")
    item = rng.choice(pool)
    pid = item["linked_paper_id"]
    if not paper_file_exists(pid):
        return Result("T14", "Policy → paper link", "defect", "FAIL",
                      f"policy {item['id']}", f"linked_paper_id '{pid}' missing")
    return Result("T14", "Policy → paper link", "defect", "PASS",
                  f"policy {item['id']}")


def t15_review_status(papers, rng):
    pool = papers
    if not pool:
        return skip("T15", "review_status integrity", "defect", "pool empty")
    p = rng.choice(pool)
    rs = p.get("review_status")
    if rs not in REVIEW_STATUSES:
        return Result("T15", "review_status integrity", "defect", "FAIL",
                      f"paper {p['id']}", f"review_status='{rs}'")
    return Result("T15", "review_status integrity", "defect", "PASS",
                  f"paper {p['id']}", f"status={rs}")


def _hu_relevant(p):
    cs = p.get("countries_studied") or []
    blob = " ".join([
        (p.get("title") or "").lower(),
        (p.get("summary_en") or "").lower(),
        (p.get("data_used") or "").lower(),
        (p.get("abstract") or "").lower(),
    ])
    return ("HU" in cs) or ("hungar" in blob)


def t16_hu_country_consistency(papers, rng):
    pool = [p for p in papers if not is_locked(p)
            and "HU" in (p.get("countries_studied") or [])]
    if not pool:
        return skip("T16", "HU-country consistency", "plausibility-flag", "pool empty")
    p = rng.choice(pool)
    blob = " ".join([
        (p.get("title") or ""), (p.get("summary_en") or ""),
        (p.get("data_used") or ""), (p.get("abstract") or ""),
    ]).lower()
    if "hungar" not in blob:
        return Result("T16", "HU-country consistency", "plausibility-flag", "FAIL",
                      f"paper {p['id']}", "HU in countries_studied but no 'Hungar*' in title/summary/data/abstract")
    return Result("T16", "HU-country consistency", "plausibility-flag", "PASS",
                  f"paper {p['id']}")


def t17_hu_mention_consistency(papers, rng):
    pool = [p for p in papers if not is_locked(p)
            and has(p, "summary_en")
            and re.search(r"\bhungar", p["summary_en"], re.IGNORECASE)]
    if not pool:
        return skip("T17", "HU-mention consistency", "plausibility-flag", "pool empty")
    p = rng.choice(pool)
    if "HU" not in (p.get("countries_studied") or []):
        return Result("T17", "HU-mention consistency", "plausibility-flag", "FAIL",
                      f"paper {p['id']}", "summary mentions Hungary but HU not in countries_studied")
    return Result("T17", "HU-mention consistency", "plausibility-flag", "PASS",
                  f"paper {p['id']}")


def t18_hu_relevant_has_summary_hu(papers, rng):
    pool = [p for p in papers if not is_locked(p)
            and _hu_relevant(p) and has(p, "summary_en") and not has(p, "summary_hu")]
    # FAIL pool here is the items missing summary_hu — sample one to surface the gap.
    # If pool is empty, the whole catalogue passes; record PASS without subject.
    if not pool:
        return Result("T18", "HU-relevant has summary_hu", "plausibility-flag", "PASS",
                      "", "no HU-relevant papers missing summary_hu")
    p = rng.choice(pool)
    return Result("T18", "HU-relevant has summary_hu", "plausibility-flag", "FAIL",
                  f"paper {p['id']}", "HU-relevant paper has summary_en but no summary_hu")


def t19_summary_hu_is_hungarian(papers, rng):
    pool = [p for p in papers if not is_locked(p) and has(p, "summary_hu")]
    if not pool:
        return skip("T19", "summary_hu is Hungarian", "plausibility-flag", "pool empty")
    p = rng.choice(pool)
    if not looks_hungarian(p["summary_hu"]):
        return Result("T19", "summary_hu is Hungarian", "plausibility-flag", "FAIL",
                      f"paper {p['id']}", "no Hungarian-specific characters in summary_hu")
    return Result("T19", "summary_hu is Hungarian", "plausibility-flag", "PASS",
                  f"paper {p['id']}")


def t20_policy_is_concrete(papers, rng):
    pool = [p for p in papers if not is_locked(p)
            and _hu_relevant(p) and has(p, "policy_relevance")]
    if not pool:
        return skip("T20", "policy_relevance names HU actor", "plausibility-flag", "pool empty")
    p = rng.choice(pool)
    pr = p["policy_relevance"]
    if not any(inst in pr for inst in HU_INSTITUTIONS):
        return Result("T20", "policy_relevance names HU actor", "plausibility-flag", "FAIL",
                      f"paper {p['id']}", "no HU institution / actor named")
    return Result("T20", "policy_relevance names HU actor", "plausibility-flag", "PASS",
                  f"paper {p['id']}")


def t21_doi_resolves(papers, rng):
    pool = [p for p in papers if not is_locked(p) and has(p, "doi")]
    if not pool:
        return skip("T21", "DOI resolves", "liveness-flag", "pool empty")
    p = rng.choice(pool)
    url = f"https://doi.org/{p['doi']}"
    code = http_status(url)
    if code in (200, 301, 302, 303, 307, 308):
        return Result("T21", "DOI resolves", "liveness-flag", "PASS",
                      f"paper {p['id']}", f"HTTP {code}")
    return Result("T21", "DOI resolves", "liveness-flag", "FAIL",
                  f"paper {p['id']}", f"HTTP {code} for {url}")


def t22_author_website(authors, rng):
    pool = [a for a in authors if not is_locked(a) and has(a, "website")]
    if not pool:
        return skip("T22", "Author website resolves", "liveness-flag", "pool empty")
    a = rng.choice(pool)
    code = http_status(a["website"])
    if code in (200, 301, 302, 303, 307, 308):
        return Result("T22", "Author website resolves", "liveness-flag", "PASS",
                      f"author {a['id']}", f"HTTP {code}")
    return Result("T22", "Author website resolves", "liveness-flag", "FAIL",
                  f"author {a['id']}", f"HTTP {code} for {a['website']}")


def t23_photo_loads(authors, rng):
    pool = [a for a in authors if not is_locked(a) and has(a, "photo_url")]
    if not pool:
        return skip("T23", "Author photo loads", "liveness-flag", "pool empty")
    a = rng.choice(pool)
    code = http_status(a["photo_url"], head=True)
    if code in (200, 301, 302, 303, 307, 308):
        return Result("T23", "Author photo loads", "liveness-flag", "PASS",
                      f"author {a['id']}", f"HTTP {code}")
    return Result("T23", "Author photo loads", "liveness-flag", "FAIL",
                  f"author {a['id']}", f"HTTP {code} for {a['photo_url']}")


def t24_policy_url(rng):
    if not POLICY_DIR.exists():
        return skip("T24", "Policy URL resolves", "liveness-flag", "no policy/ dir")
    items = [load_json(f) for f in POLICY_DIR.glob("*.json")]
    pool = [i for i in items if not is_locked(i) and has(i, "url")]
    if not pool:
        return skip("T24", "Policy URL resolves", "liveness-flag", "pool empty")
    item = rng.choice(pool)
    code = http_status(item["url"])
    if code in (200, 301, 302, 303, 307, 308):
        return Result("T24", "Policy URL resolves", "liveness-flag", "PASS",
                      f"policy {item['id']}", f"HTTP {code}")
    return Result("T24", "Policy URL resolves", "liveness-flag", "FAIL",
                  f"policy {item['id']}", f"HTTP {code} for {item['url']}")


_HU_LEAK_RE = re.compile(r'href="\.\./([^"]+?\.html(?:[?#][^"]*)?)"')

def t26_hu_no_en_leak(rng):
    """`../<page>.html` links inside hu/*.html files take the user OUT of /hu/
    to the EN equivalent — see the regression caught manually on
    hu/index.html line 80 (topic-card link). The two `../` paths we
    legitimately keep are: ../assets/* (shared CSS/JS) and ../index.html
    (the explicit language-toggle anchor)."""
    hu_dir = ROOT / "hu"
    if not hu_dir.exists():
        return skip("T26", "HU pages don't leak to EN", "defect", "no hu/ dir")
    files = sorted(hu_dir.glob("*.html"))
    if not files:
        return skip("T26", "HU pages don't leak to EN", "defect", "no HU files")
    f = rng.choice(files)
    text = f.read_text(encoding="utf-8")
    leaks = []
    for m in _HU_LEAK_RE.finditer(text):
        target = m.group(1)
        # Permit shared-asset paths (no .html ones exist today, but be defensive)
        if target.startswith("assets/"):
            continue
        # Permit the explicit language-toggle to /index.html
        if target == "index.html" or target.startswith("index.html?") or target.startswith("index.html#"):
            continue
        leaks.append(target)
    if leaks:
        return Result("T26", "HU pages don't leak to EN", "defect", "FAIL",
                      f"file hu/{f.name}",
                      f"leaky links: {', '.join(leaks[:3])}{' …' if len(leaks) > 3 else ''}")
    return Result("T26", "HU pages don't leak to EN", "defect", "PASS",
                  f"file hu/{f.name}")


def t25_repec(authors, rng):
    pool = [a for a in authors if not is_locked(a) and has(a, "repec_id")]
    if not pool:
        return skip("T25", "RePEc page resolves", "liveness-flag", "pool empty")
    a = rng.choice(pool)
    # IDEAS/RePEc serves registered short IDs from BOTH /e/<id>.html and
    # /f/<id>.html — the former is the historical "registered" path, the
    # latter is the "filed" / migration path. Authors typically resolve at
    # one or the other, not both. PASS if either responds.
    rid = a["repec_id"]
    code_e = http_status(f"https://ideas.repec.org/e/{rid}.html")
    code_f = http_status(f"https://ideas.repec.org/f/{rid}.html") if code_e not in (200, 301, 302, 303, 307, 308) else None
    ok = lambda c: c in (200, 301, 302, 303, 307, 308)
    if ok(code_e):
        return Result("T25", "RePEc page resolves", "liveness-flag", "PASS",
                      f"author {a['id']}", f"HTTP {code_e} (/e/)")
    if ok(code_f):
        return Result("T25", "RePEc page resolves", "liveness-flag", "PASS",
                      f"author {a['id']}", f"HTTP {code_f} (/f/)")
    return Result("T25", "RePEc page resolves", "liveness-flag", "FAIL",
                  f"author {a['id']}", f"HTTP {code_e} (/e/) and {code_f} (/f/) for repec_id {rid}")


# ---------- runner --------------------------------------------------------
def run_all(seed: int | None = None):
    rng = random.Random(seed if seed is not None else time.time())
    papers = load_all_papers()
    authors = load_all_authors()

    tests = [
        ("T01", lambda: t01_author_ids(papers, rng)),
        ("T02", lambda: t02_topic_vocab(papers, rng)),
        ("T03", lambda: t03_journal_whitelist(papers, rng)),
        ("T04", lambda: t04_methods_vocab(papers, rng)),
        ("T05", lambda: t05_data_types_vocab(papers, rng)),
        ("T06", lambda: t06_country_codes(papers, rng)),
        ("T07", lambda: t07_summary_en_length(papers, rng)),
        ("T08", lambda: t08_data_used_length(papers, rng)),
        ("T09", lambda: t09_policy_length(papers, rng)),
        ("T10", lambda: t10_hu_en_ratio(papers, rng)),
        ("T11", lambda: t11_qualifying_pub(authors, papers, rng)),
        ("T12", lambda: t12_author_has_papers(authors, papers, rng)),
        ("T13", lambda: t13_press_link(rng)),
        ("T14", lambda: t14_policy_link(rng)),
        ("T15", lambda: t15_review_status(papers, rng)),
        ("T16", lambda: t16_hu_country_consistency(papers, rng)),
        ("T17", lambda: t17_hu_mention_consistency(papers, rng)),
        ("T18", lambda: t18_hu_relevant_has_summary_hu(papers, rng)),
        ("T19", lambda: t19_summary_hu_is_hungarian(papers, rng)),
        ("T20", lambda: t20_policy_is_concrete(papers, rng)),
        ("T21", lambda: t21_doi_resolves(papers, rng)),
        ("T22", lambda: t22_author_website(authors, rng)),
        ("T23", lambda: t23_photo_loads(authors, rng)),
        ("T24", lambda: t24_policy_url(rng)),
        ("T25", lambda: t25_repec(authors, rng)),
        ("T26", lambda: t26_hu_no_en_leak(rng)),
    ]

    results = []
    for tid, fn in tests:
        try:
            results.append(fn())
        except Exception as e:
            results.append(Result(tid, "UNCAUGHT", "defect", "FAIL", "", f"{type(e).__name__}: {e}"))
    return results


def render(results, seed) -> str:
    when = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [
        f"QA sample report — {when} (seed {seed})",
        "=" * 64,
    ]
    for r in results:
        lines.append(r.line())
    lines.append("")
    n_pass = sum(1 for r in results if r.outcome == "PASS")
    n_fail = sum(1 for r in results if r.outcome == "FAIL")
    n_skip = sum(1 for r in results if r.outcome == "SKIP")
    lines.append(f"Summary: {n_pass}/{len(results)} PASS, {n_fail} FAIL, {n_skip} SKIP")
    fails = [r for r in results if r.outcome == "FAIL"]
    if fails:
        lines.append("")
        lines.append("Failures by category:")
        for r in fails:
            lines.append(f"  [{r.category:18}] {r.tid} {r.subject} :: {r.diagnostic}")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--seed", type=int, default=None,
                    help="Deterministic RNG seed (default: time-based)")
    ap.add_argument("--save", action="store_true",
                    help="Also save report to tests/reports/")
    args = ap.parse_args()

    seed = args.seed if args.seed is not None else int(time.time())
    results = run_all(seed)
    report = render(results, seed)
    print(report)

    if args.save:
        reports_dir = ROOT / "tests" / "reports"
        reports_dir.mkdir(parents=True, exist_ok=True)
        f = reports_dir / f"qa-sample-{datetime.now().strftime('%Y-%m-%d-%H%M')}.txt"
        f.write_text(report, encoding="utf-8")
        print(f"\nSaved: {f.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
