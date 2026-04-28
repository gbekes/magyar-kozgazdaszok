"""Add paper stubs for András Fülöp (ESSEC) and update authors-seed.json + journals."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAPERS_DIR = ROOT / "data" / "papers"
SEED = ROOT / "authors-seed.json"
JOURNALS = ROOT / "data" / "journals.json"

ADDED_AT = "2026-04-28"


def stub(pid, title, authors, journal, year):
    return {
        "id": pid,
        "title": title,
        "authors": authors,
        "publication_type": "article",
        "journal": journal,
        "year": year,
        "volume": None,
        "issue": None,
        "pages": None,
        "doi": None,
        "working_paper_series": None,
        "url_published": None,
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
    stub(
        "duan-fulop-2009-jeconometrics",
        "Estimating the Structural Credit Risk Model when Equity Prices Are Contaminated by Trading Noises",
        ["Jin-Chuan Duan", "fulop-andras"],
        "Journal of Econometrics",
        2009,
    ),
    stub(
        "duan-fulop-2011-statcomp",
        "A Stable Estimator of the Information Matrix Under EM for Dependent Data",
        ["Jin-Chuan Duan", "fulop-andras"],
        "Statistics and Computing",
        2011,
    ),
    stub(
        "fulop-li-2013-jeconometrics",
        "Efficient Learning via Simulation: A Marginalized Resample-Move Approach",
        ["fulop-andras", "Junye Li"],
        "Journal of Econometrics",
        2013,
    ),
    stub(
        "fulop-li-yu-2015-rfs",
        "Self-Exciting Jumps, Learning, and Asset Pricing Implications",
        ["fulop-andras", "Junye Li", "Jun Yu"],
        "Review of Financial Studies",
        2015,
    ),
    stub(
        "duan-fulop-2015-jbes",
        "Density-Tempered Marginalized Sequential Monte Carlo Samplers",
        ["Jin-Chuan Duan", "fulop-andras"],
        "Journal of Business and Economic Statistics",
        2015,
    ),
    stub(
        "fulop-li-2019-jeconometrics",
        "Bayesian Estimation of Dynamic Asset Pricing Models with Informative Observations",
        ["fulop-andras", "Junye Li"],
        "Journal of Econometrics",
        2019,
    ),
    stub(
        "fulop-heng-li-liu-2022-jeconometrics",
        "Bayesian Estimation of Long-Run Risk Models Using Sequential Monte Carlo",
        ["fulop-andras", "Jeremy Heng", "Junye Li", "Hening Liu"],
        "Journal of Econometrics",
        2022,
    ),
    stub(
        "wan-fulop-li-2022-jeconometrics",
        "Real-Time Bayesian Learning and Bond Return Predictability",
        ["Runqing Wan", "fulop-andras", "Junye Li"],
        "Journal of Econometrics",
        2022,
    ),
    stub(
        "daures-lescourret-fulop-2022-jfm",
        "Standardization, Transparency Initiatives, and Liquidity in the CDS Market",
        ["Laurence Daures-Lescourret", "fulop-andras"],
        "Journal of Financial Markets",
        2022,
    ),
    stub(
        "fulop-kocsis-2023-jbf",
        "News Indices on Country Fundamentals",
        ["fulop-andras", "Zalán Kocsis"],
        "Journal of Banking & Finance",
        2023,
    ),
    stub(
        "fulop-li-liu-yan-2025-mansci",
        "Estimating and Testing Long-Run Risk Models: International Evidence",
        ["fulop-andras", "Junye Li", "Hening Liu", "Cheng Yan"],
        "Management Science",
        2025,
    ),
]


def main():
    # Add Journal of Financial Markets to whitelist if missing
    journals = json.loads(JOURNALS.read_text(encoding="utf-8"))
    names = {j["name"] for j in journals}
    if "Journal of Financial Markets" not in names:
        journals.append({
            "short": "JFM",
            "name": "Journal of Financial Markets",
            "tier": "B",
            "field": "finance",
        })
        JOURNALS.write_text(json.dumps(journals, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print("journals: added Journal of Financial Markets")
    else:
        print("journals: Journal of Financial Markets already present")

    # Write paper stubs
    written = skipped = 0
    for paper in PAPERS:
        out = PAPERS_DIR / f"{paper['id']}.json"
        if out.exists():
            skipped += 1
            continue
        out.write_text(json.dumps(paper, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        written += 1
    print(f"papers: wrote {written}, skipped {skipped}")

    # Append to authors-seed.json
    seed = json.loads(SEED.read_text(encoding="utf-8"))
    existing_ids = {a["id"] for a in seed}
    if "fulop-andras" not in existing_ids:
        seed.append({
            "id": "fulop-andras",
            "name_en": "András Fülöp",
            "name_hu": "Fülöp András",
            "primary_affiliation": "ESSEC Business School",
            "primary_fields": ["banking-finance", "methods", "macroeconomics"],
            "bio_en": "András Fülöp is Professor of Finance at ESSEC Business School. His research is in financial econometrics and asset pricing, with a focus on Bayesian econometrics and sequential Monte Carlo methods applied to credit risk, long-run risk models, bond return predictability, and CDS markets. His work has appeared in the Review of Financial Studies, the Journal of Econometrics, the Journal of Business and Economic Statistics, the Journal of Banking & Finance, and Management Science.",
            "bio_review": "needs-verification",
        })
        SEED.write_text(json.dumps(seed, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print("authors-seed: appended fulop-andras")
    else:
        print("authors-seed: fulop-andras already present")


if __name__ == "__main__":
    main()
