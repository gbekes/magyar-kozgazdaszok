"""Add ~20 paper stubs for Molnár Kriszta, Sárváry Miklós, Kovács Balázs and update authors-seed.json."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAPERS_DIR = ROOT / "data" / "papers"
SEED = ROOT / "authors-seed.json"

ADDED_AT = "2026-04-27"


def stub(pid, title, authors, journal, year, doi=None, url=None, volume=None, issue=None, pages=None):
    return {
        "id": pid,
        "title": title,
        "authors": authors,
        "publication_type": "article",
        "journal": journal,
        "year": year,
        "volume": volume,
        "issue": issue,
        "pages": pages,
        "doi": doi,
        "working_paper_series": None,
        "url_published": url,
        "url_pdf": None,
        "url_replication": None,
        "abstract": None,
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
        "added_at": ADDED_AT,
        "last_reviewed_at": ADDED_AT,
        "review_status": "metadata-fetched",
        "openalex_id": None,
    }


PAPERS = [
    # ------------------------- Molnár Kriszta -------------------------
    stub(
        "molnar-kriszta-2007-jeea",
        "Learning about the Long-Run Determinants of Real Exchange Rates",
        ["molnar-kriszta"],
        "Journal of the European Economic Association",
        2007,
    ),
    stub(
        "molnar-santoro-2014-eer",
        "Optimal Monetary Policy When Agents Are Learning",
        ["molnar-kriszta", "Sergio Santoro"],
        "European Economic Review",
        2014,
    ),
    stub(
        "molnar-eusepi-preston-2015-jmcb",
        "Expectations, Learning and Business Cycle Fluctuations",
        ["Stefano Eusepi", "molnar-kriszta", "Bruce Preston"],
        "Journal of Money, Credit and Banking",
        2015,
    ),
    stub(
        "molnar-reppa-2020-economica",
        "Expectations and Monetary Policy: Evidence from the Laboratory",
        ["molnar-kriszta", "Zoltan Reppa"],
        "Economica",
        2020,
    ),
    stub(
        "molnar-tortorice-2020-jome",
        "Expectations and Monetary Policy",
        ["molnar-kriszta", "Daniel L. Tortorice"],
        "Journal of Monetary Economics",
        2020,
    ),

    # ------------------------- Sárváry Miklós -------------------------
    stub(
        "sarvary-1999-marsci",
        "Knowledge Management and Competition in the Consulting Industry",
        ["sarvary-miklos"],
        "Marketing Science",
        1999,
    ),
    stub(
        "ofek-sarvary-2001-mansci",
        "Leveraging the Customer Base: Creating Competitive Advantage Through Knowledge Management",
        ["Elie Ofek", "sarvary-miklos"],
        "Management Science",
        2001,
    ),
    stub(
        "atasu-sarvary-vanwassenhove-2008-mansci",
        "Remanufacturing as a Marketing Strategy",
        ["Atalay Atasu", "sarvary-miklos", "Luk N. Van Wassenhove"],
        "Management Science",
        2008,
    ),
    stub(
        "katona-zubcsek-sarvary-2011-jmr",
        "Network Effects and Personal Influences: The Diffusion of an Online Social Network",
        ["Zsolt Katona", "Peter Pal Zubcsek", "sarvary-miklos"],
        "Journal of Marketing Research",
        2011,
    ),
    stub(
        "ofek-katona-sarvary-2011-marsci",
        "Bricks and Clicks: The Impact of Product Returns on the Strategies of Multichannel Retailers",
        ["Elie Ofek", "Zsolt Katona", "sarvary-miklos"],
        "Marketing Science",
        2011,
    ),
    stub(
        "bart-stephen-sarvary-2014-jmr",
        "Which Products Are Best Suited to Mobile Advertising? A Field Study of Mobile Display Advertising Effects on Consumer Attitudes and Intentions",
        ["Yakov Bart", "Andrew T. Stephen", "sarvary-miklos"],
        "Journal of Marketing Research",
        2014,
    ),

    # ------------------------- Kovács Balázs -------------------------
    stub(
        "kovacs-carroll-lehman-2013-orgsci",
        "Authenticity and Consumer Value Ratings: Empirical Tests from the Restaurant Domain",
        ["kovacs-balazs", "Glenn R. Carroll", "David W. Lehman"],
        "Organization Science",
        2013,
    ),
    stub(
        "lehman-kovacs-carroll-2014-mansci",
        "Conflicting Social Codes and Organizations: Hygiene and Authenticity in Consumer Evaluations of Restaurants",
        ["David W. Lehman", "kovacs-balazs", "Glenn R. Carroll"],
        "Management Science",
        2014,
    ),
    stub(
        "sharkey-kovacs-2018-asq",
        "The Many Gifts of Status: How Attending High-Status Schools Affects Income",
        ["Amanda J. Sharkey", "kovacs-balazs"],
        "Administrative Science Quarterly",
        2018,
    ),
    stub(
        "goldberg-hannan-kovacs-2016-asr",
        "What Does It Mean to Span Cultural Boundaries? Variety and Atypicality in Cultural Consumption",
        ["Amir Goldberg", "Michael T. Hannan", "kovacs-balazs"],
        "American Sociological Review",
        2016,
    ),
    stub(
        "hsu-kocak-kovacs-2018-orgsci",
        "Co-opt or Coexist? A Study of Medical Cannabis Dispensaries' Identity-Based Responses to Recreational-Use Legalization in Colorado and Washington",
        ["Greta Hsu", "Ozgecan Kocak", "kovacs-balazs"],
        "Organization Science",
        2018,
    ),
    stub(
        "kovacs-jensen-sorenson-2018-natbiotech",
        "Authorship Order and Research Quality in the Life Sciences",
        ["kovacs-balazs", "Bence Jensen", "Olav Sorenson"],
        "Nature Biotechnology",
        2018,
    ),
    stub(
        "lehman-oconnor-kovacs-newman-2019-ama",
        "Authenticity",
        ["David W. Lehman", "Kieran O\u2019Connor", "kovacs-balazs", "George E. Newman"],
        "Academy of Management Annals",
        2019,
    ),
    stub(
        "hsu-kovacs-kocak-2019-smj",
        "Identity Lost and Regained: Lessons from When Hipsters Get Aboard",
        ["Greta Hsu", "kovacs-balazs", "Ozgecan Kocak"],
        "Strategic Management Journal",
        2019,
    ),
    stub(
        "lemens-kovacs-hannan-pros-2023-pnas",
        "Using Machine Learning to Uncover the Semantics of Concepts: How Well Do Typicality Measures Extracted from a BERT Text Classifier Match Human Judgments of Genre Typicality?",
        ["Gael Le Mens", "kovacs-balazs", "Michael T. Hannan", "Guillem Pros"],
        "Proceedings of the National Academy of Sciences",
        2023,
    ),
]


def main():
    written = 0
    skipped = 0
    for paper in PAPERS:
        out = PAPERS_DIR / f"{paper['id']}.json"
        if out.exists():
            skipped += 1
            continue
        out.write_text(json.dumps(paper, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        written += 1
    print(f"papers: wrote {written}, skipped {skipped}")

    # Update authors-seed.json
    seed = json.loads(SEED.read_text(encoding="utf-8"))
    existing_ids = {a["id"] for a in seed}
    new_entries = [
        {
            "id": "molnar-kriszta",
            "name_en": "Krisztina Molnár",
            "name_hu": "Molnár Krisztina",
            "primary_affiliation": "Norwegian School of Economics (NHH)",
            "primary_fields": ["macroeconomics", "banking-finance", "behavioral"],
            "bio_en": "Krisztina Molnár is Professor of Economics at the Norwegian School of Economics (NHH) in Bergen. Her research is in monetary economics, expectations formation, learning, and household consumption. Her work has appeared in the Journal of the European Economic Association, the Journal of Monetary Economics, the Journal of Money, Credit and Banking, the European Economic Review, and Economica.",
            "bio_review": "needs-verification",
        },
        {
            "id": "sarvary-miklos",
            "name_en": "Miklós Sárváry",
            "name_hu": "Sárváry Miklós",
            "primary_affiliation": "Columbia Business School",
            "primary_fields": ["industrial-organization", "innovation-digital", "firms-productivity"],
            "bio_en": "Miklós Sárváry is the Carson Family Professor of Business at Columbia Business School. His research is in marketing science, media economics, digital markets, network effects, technology diffusion, and the economics of digital currencies and AI. His work has appeared in Management Science, the Journal of Marketing Research, Marketing Science, the Journal of Marketing, and Quantitative Marketing and Economics.",
            "bio_review": "needs-verification",
        },
        {
            "id": "kovacs-balazs",
            "name_en": "Balázs Kovács",
            "name_hu": "Kovács Balázs",
            "primary_affiliation": "Yale School of Management",
            "primary_fields": ["industrial-organization", "firms-productivity", "behavioral"],
            "bio_en": "Balázs Kovács is Professor at the Yale School of Management. His research is in organisation theory, category spanning, authenticity, networks, and the application of large language models to social-science measurement. His work has appeared in the Academy of Management Annals, Administrative Science Quarterly, American Sociological Review, Organization Science, Management Science, Strategic Management Journal, and PNAS, among others.",
            "bio_review": "needs-verification",
        },
    ]
    appended = 0
    for entry in new_entries:
        if entry["id"] in existing_ids:
            continue
        seed.append(entry)
        appended += 1
    SEED.write_text(json.dumps(seed, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"authors-seed: appended {appended}")


if __name__ == "__main__":
    main()
