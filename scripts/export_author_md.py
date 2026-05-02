"""Export an author's full catalogue record as a single Markdown file
they can edit and send back (email or GitHub issue attachment).

Usage:
    python scripts/export_author_md.py --slug adamecz-anna
    python scripts/export_author_md.py --all

Output: exports/authors/<slug>.md (one file per author).

The Markdown is structured so an author can edit any field in place. Each
paper / policy / press item carries its slug as a hidden anchor so changes
can be matched back to the JSON file. The header explains what to do.
"""
import argparse
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
AUTHORS = ROOT / "data" / "authors"
PAPERS = ROOT / "data" / "papers"
POLICY = ROOT / "data" / "policy"
PRESS = ROOT / "data" / "press"
OUT_DIR = ROOT / "exports" / "authors"


def field(label, value, blank="—"):
    if value is None or value == "":
        return f"- **{label}:** {blank}"
    if isinstance(value, list):
        if not value:
            return f"- **{label}:** {blank}"
        value = ", ".join(str(v) for v in value)
    return f"- **{label}:** {value}"


def block(label, text):
    if not text:
        return f"### {label}\n\n_(empty)_\n"
    return f"### {label}\n\n{text}\n"


def render_author_header(a):
    name = a.get("name_hu") or a.get("name_en") or a["id"]
    name_en = a.get("name_en") or ""
    out = []
    out.append(f"# {name}")
    if name_en and name_en != name:
        out.append(f"_({name_en})_")
    out.append("")
    out.append(f"<!-- author-slug: {a['id']} -->")
    out.append("")
    out.append("> **How to use this file**")
    out.append(">")
    out.append("> This is a snapshot of everything we have on you in the catalogue.")
    out.append("> Edit any field directly. Add `[ADD]` to introduce a new item, mark")
    out.append("> `[REMOVE]` next to an item that is wrong or shouldn't be listed,")
    out.append("> and `[FIX]` next to anything that needs correction. Email the edited")
    out.append("> file back, or attach it to a GitHub issue. We'll apply the changes.")
    out.append("")
    out.append("---")
    out.append("")
    return "\n".join(out)


def render_personal(a):
    out = ["## Personal info", ""]
    out.append(field("Name (EN)", a.get("name_en")))
    out.append(field("Name (HU)", a.get("name_hu")))
    out.append(field("Website", a.get("website")))
    out.append(field("Email", a.get("email")))
    out.append(field("Photo URL", a.get("photo_url")))
    out.append(field("RePEc ID", a.get("repec_id")))
    out.append(field("Google Scholar ID", a.get("scholar_id")))
    out.append(field("ORCID", a.get("orcid")))
    out.append(field("OpenAlex ID", a.get("openalex_id")))
    out.append(field("Open to media (EN)", "Yes" if a.get("open_to_media_en") else "No"))
    out.append(field("Open to media (HU)", "Yes" if a.get("open_to_media_hu") else "No"))
    out.append(field("Media note", a.get("media_note")))
    out.append(field("Primary fields", a.get("primary_fields")))
    out.append("")

    out.append("### Affiliations")
    out.append("")
    affs = a.get("affiliations") or []
    if not affs:
        out.append("_(none recorded)_")
    else:
        for i, af in enumerate(affs, 1):
            name_en = af.get("name") or ""
            name_hu = af.get("name_hu") or ""
            role_en = af.get("role") or ""
            role_hu = af.get("role_hu") or ""
            line = f"{i}. **{name_en}**"
            if name_hu and name_hu != name_en:
                line += f" / {name_hu}"
            if role_en or role_hu:
                line += " — "
                if role_en:
                    line += role_en
                if role_hu and role_hu != role_en:
                    line += f" ({role_hu})"
            out.append(line)
    out.append("")

    out.append(block("Bio (EN)", a.get("bio_en")))
    out.append(block("Bio (HU)", a.get("bio_hu")))

    qp = a.get("qualifying_publication") or {}
    if qp:
        out.append("### Qualifying publication")
        out.append("")
        out.append(field("Title", qp.get("title")))
        out.append(field("Journal", qp.get("journal")))
        out.append(field("Year", qp.get("year")))
        out.append("")
    return "\n".join(out)


def author_display_name(slug, authors_index):
    a = authors_index.get(slug)
    if a:
        return a.get("name_en") or a.get("name_hu") or slug
    return slug  # fallback for non-slug strings (free-text co-authors)


def format_authors(items, authors_index):
    out = []
    for it in items or []:
        out.append(author_display_name(it, authors_index))
    return ", ".join(out)


def render_paper(p, authors_index):
    out = []
    out.append(f"### {p.get('title') or '(untitled)'}")
    out.append("")
    out.append(f"<!-- paper-slug: {p['id']} -->")
    out.append("")
    out.append(field("Authors", format_authors(p.get("authors"), authors_index)))
    out.append(field("Journal", p.get("journal")))
    out.append(field("Year", p.get("year")))
    out.append(field("Volume / Issue / Pages",
                     " / ".join(str(p.get(k) or "—") for k in ("volume", "issue", "pages"))))
    out.append(field("DOI", p.get("doi")))
    out.append(field("URL (published)", p.get("url_published")))
    out.append(field("PDF URL", p.get("url_pdf")))
    out.append(field("Replication URL", p.get("url_replication")))
    out.append(field("Working paper series", p.get("working_paper_series")))
    out.append(field("Topics", p.get("topics")))
    out.append(field("Methods", p.get("methods")))
    out.append(field("Countries studied", p.get("countries_studied")))
    out.append(field("Data types", p.get("data_types")))
    out.append(field("Policy instruments", p.get("policy_instruments")))
    out.append("")
    out.append(block("Abstract", p.get("abstract")))
    out.append(block("Summary (EN)", p.get("summary_en")))
    out.append(block("Summary (HU)", p.get("summary_hu")))
    out.append(block("Data used (EN)", p.get("data_used")))
    out.append(block("Data used (HU)", p.get("data_used_hu")))
    out.append(block("Policy relevance (EN)", p.get("policy_relevance")))
    out.append(block("Policy relevance (HU)", p.get("policy_relevance_hu")))
    return "\n".join(out)


def render_policy(p, authors_index):
    out = []
    out.append(f"### {p.get('title') or '(untitled)'}")
    out.append("")
    out.append(f"<!-- policy-slug: {p['id']} -->")
    out.append("")
    out.append(field("Authors", format_authors(p.get("authors"), authors_index)))
    out.append(field("Outlet kind", p.get("outlet_kind")))
    out.append(field("Outlet", p.get("outlet")))
    out.append(field("Outlet issue", p.get("outlet_issue")))
    out.append(field("Institution", p.get("institution")))
    out.append(field("Year", p.get("year")))
    out.append(field("Language", p.get("language")))
    out.append(field("URL", p.get("url")))
    out.append(field("DOI", p.get("doi")))
    out.append(field("Linked paper", p.get("linked_paper_id")))
    out.append(field("Topics", p.get("topics")))
    out.append(field("Countries", p.get("countries_studied")))
    out.append("")
    out.append(block("Summary (EN)", p.get("summary_en")))
    out.append(block("Summary (HU)", p.get("summary_hu")))
    out.append(block("Policy relevance (EN)", p.get("policy_relevance")))
    out.append(block("Policy relevance (HU)", p.get("policy_relevance_hu")))
    return "\n".join(out)


def render_press(p, authors_index):
    out = []
    out.append(f"### {p.get('title') or '(untitled)'}")
    if p.get("title_hu"):
        out.append(f"_{p['title_hu']}_")
    out.append("")
    out.append(f"<!-- press-slug: {p['id']} -->")
    out.append("")
    out.append(field("Authors", format_authors(p.get("authors"), authors_index)))
    out.append(field("Kind", p.get("kind")))
    out.append(field("Venue", p.get("venue")))
    out.append(field("Date", p.get("date")))
    out.append(field("Language", p.get("language")))
    out.append(field("URL", p.get("url")))
    out.append(field("Linked paper", p.get("linked_paper_id")))
    out.append("")
    out.append(block("Blurb", p.get("blurb")))
    return "\n".join(out)


def export_author(slug, authors_index, papers_by_author, policy_by_author, press_by_author):
    a = authors_index.get(slug)
    if not a:
        print(f"  SKIP {slug}: no author file")
        return None

    parts = []
    parts.append(render_author_header(a))
    parts.append(render_personal(a))

    papers = papers_by_author.get(slug, [])
    parts.append(f"## Papers ({len(papers)})\n")
    if papers:
        for p in sorted(papers, key=lambda x: -(x.get("year") or 0)):
            parts.append(render_paper(p, authors_index))
            parts.append("---\n")
    else:
        parts.append("_(none in catalogue)_\n")

    pol = policy_by_author.get(slug, [])
    parts.append(f"## Policy items ({len(pol)})\n")
    if pol:
        for p in sorted(pol, key=lambda x: -(x.get("year") or 0)):
            parts.append(render_policy(p, authors_index))
            parts.append("---\n")
    else:
        parts.append("_(none in catalogue)_\n")

    pr = press_by_author.get(slug, [])
    parts.append(f"## Press items ({len(pr)})\n")
    if pr:
        for p in sorted(pr, key=lambda x: x.get("date") or "", reverse=True):
            parts.append(render_press(p, authors_index))
            parts.append("---\n")
    else:
        parts.append("_(none in catalogue)_\n")

    return "\n".join(parts)


def load_all(directory):
    out = []
    if not directory.exists():
        return out
    for f in sorted(directory.glob("*.json")):
        out.append(json.loads(f.read_text(encoding="utf-8")))
    return out


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--slug", help="Single author slug")
    g.add_argument("--all", action="store_true", help="Export every author")
    args = ap.parse_args()

    authors = load_all(AUTHORS)
    papers = load_all(PAPERS)
    policy = load_all(POLICY)
    press = load_all(PRESS)

    authors_index = {a["id"]: a for a in authors}

    def index_by_author(items):
        idx = {}
        for it in items:
            for slug in it.get("authors") or []:
                if slug in authors_index:
                    idx.setdefault(slug, []).append(it)
        return idx

    papers_by_author = index_by_author(papers)
    policy_by_author = index_by_author(policy)
    press_by_author = index_by_author(press)

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    targets = [args.slug] if args.slug else sorted(authors_index)
    written = 0
    for slug in targets:
        md = export_author(slug, authors_index, papers_by_author, policy_by_author, press_by_author)
        if md is None:
            continue
        out = OUT_DIR / f"{slug}.md"
        out.write_text(md, encoding="utf-8")
        written += 1
        print(f"  wrote {out.relative_to(ROOT)}")

    print(f"\nWrote {written} file(s) to {OUT_DIR.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
