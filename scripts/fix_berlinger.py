"""Fix Berlinger Edina's catalogue per author feedback (2026-04-30).

Edina wrote: 'My block bleeds from many wounds. Could we use my personal
site somehow? www.eberlinger.eu'

Cross-checked against her IDEAS profile (pbe896), which lists 32 published
journal articles. We had 14 — 18 missing, 6 year mismatches, plus a
clunky Corvinus-repository search URL as her 'website'.

Changes:
1. Author file:
   - website: clunky search URL → https://www.eberlinger.eu/
   - qualifying_publication.year: 2021 → 2022 (JIFMIM vol 77, 2022)
   - Add Luxembourg affiliation (Research Scientist 2023-2024)
   - Add DSK Bank Bulgaria board role (since 2024)

2. Year fixes on 6 existing stubs (slug-year stays as identifier, year
   field corrected to print year):
   - berlinger-2016-frl: 2016 → 2017 (FRL vol 21, 2017)
   - berlinger-bihary-et-al-2016-frl: 2016 → 2017 (FRL vol 22, 2017)
   - berlinger-domotor-et-al-2018-frl: 2018 → 2019 (FRL vol 31, 2019)
   - berlinger-gosztonyi-et-al-2022-emr: 2022 → 2023 (EMR vol 54, 2023)
   - berlinger-kereszturi-et-al-2021-jifmim: 2021 → 2022 (JIFMIM vol 77, 2022)
   - kereszturi-berlinger-et-al-2022-ae: 2022 → 2023 (AE vol 55, 2023)

3. Add 18 new paper stubs for the missing journal articles. All have
   IDEAS-verified metadata. Abstracts left null for cowork.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAPERS = ROOT / "data" / "papers"
AUTHORS = ROOT / "data" / "authors"


def load(p):
    return json.loads(p.read_text(encoding="utf-8"))


def save(p, data):
    p.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


# ---- 1. author file ----
af = AUTHORS / "berlinger-edina.json"
a = load(af)
a["website"] = "https://www.eberlinger.eu/"
if a.get("qualifying_publication") and a["qualifying_publication"].get("year") == 2021:
    a["qualifying_publication"]["year"] = 2022

# Add Luxembourg + DSK affiliations if not present
existing_aff_names = {x.get("name") for x in (a.get("affiliations") or [])}
if "University of Luxembourg" not in existing_aff_names:
    a["affiliations"].append({
        "name": "University of Luxembourg",
        "name_hu": "Luxemburgi Egyetem",
        "role": "Research Scientist (2023–2024)",
        "role_hu": "kutató (2023–2024)",
        "start": None,
    })
if "DSK Bank Bulgaria" not in existing_aff_names:
    a["affiliations"].append({
        "name": "DSK Bank Bulgaria",
        "name_hu": "DSK Bank Bulgária",
        "role": "Independent Member of Supervisory Board, Chair of Risk Committee (since 2024)",
        "role_hu": "felügyelőbizottsági tag, kockázatkezelési bizottság elnöke (2024 óta)",
        "start": "2024",
    })
save(af, a)
print(f"author file updated: berlinger-edina.json")

# ---- 2. year fixes on existing stubs ----
YEAR_FIXES = {
    "berlinger-2016-frl": 2017,
    "berlinger-bihary-et-al-2016-frl": 2017,
    "berlinger-domotor-et-al-2018-frl": 2019,
    "berlinger-gosztonyi-et-al-2022-emr": 2023,
    "berlinger-kereszturi-et-al-2021-jifmim": 2022,
    "kereszturi-berlinger-et-al-2022-ae": 2023,
}
for slug, new_year in YEAR_FIXES.items():
    f = PAPERS / f"{slug}.json"
    p = load(f)
    p["year"] = new_year
    save(f, p)
    print(f"year fix: {slug} -> {new_year}")

# Also add page on optimal margin which had pages: None
p = load(PAPERS / "berlinger-domotor-et-al-2018-frl.json")
if not p.get("pages"):
    p["pages"] = "101194"  # FRL 2019 vol 31, article number
    save(PAPERS / "berlinger-domotor-et-al-2018-frl.json", p)


# ---- 3. add 18 missing paper stubs ----
ADDED_AT = "2026-04-30"


def stub(pid, title, authors, journal, year, **extra):
    base = {
        "id": pid,
        "title": title,
        "authors": authors,
        "publication_type": extra.get("publication_type", "article"),
        "journal": journal,
        "year": year,
        "volume": extra.get("volume"),
        "issue": extra.get("issue"),
        "pages": extra.get("pages"),
        "doi": extra.get("doi"),
        "working_paper_series": None,
        "url_published": extra.get("url_published"),
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
    return base


NEW_PAPERS = [
    # 2025
    stub("berlinger-kereszturi-lubloy-2025-eap",
         "Self-regulation, media pressure, and corporate catastrophes",
         ["berlinger-edina", "Judit Lilla Keresztúri", "Ágnes Lublóy"],
         "Economic Analysis and Policy", 2025,
         volume="85", issue="C", pages="1337-1356",
         doi="10.1016/j.eap.2025.01.014"),
    stub("kereszturi-berlinger-lubloy-2025-csrem",
         "Environmental policy and stakeholder engagement: Incident-based, cross-country analysis of firm-level greenwashing practices",
         ["Judit Lilla Keresztúri", "berlinger-edina", "Ágnes Lublóy"],
         "Corporate Social Responsibility and Environmental Management", 2025,
         volume="32", issue="1", pages="192-211",
         doi="10.1002/csr.2945"),
    stub("lovas-berlinger-toth-2025-ejdr",
         "Social Enterprise Under Moral Hazard: Who Gets State Subsidies and Active Financing?",
         ["Anita Lovas", "berlinger-edina", "Fanni Tóth"],
         "European Journal of Development Research", 2025,
         volume="37", issue="1", pages="55-78",
         doi="10.1057/s41287-024-00665-6"),

    # 2022
    stub("banai-berlinger-domotor-2022-plosone",
         "Adjustable-rate mortgages in the era of global reflation: How to model additional default risk?",
         ["Ádám Banai", "berlinger-edina", "Barbara Dömötör"],
         "PLOS ONE", 2022,
         volume="17", issue="3", pages="e0264268",
         doi="10.1371/journal.pone.0264268"),

    # 2021
    stub("berlinger-domotor-szucs-2021-rmgmt",
         "Irrational risk-taking of professionals? The relationship between risk exposures and previous profits",
         ["berlinger-edina", "Barbara Dömötör", "Balázs Árpád Szűcs"],
         "Risk Management", 2021,
         volume="23", issue="3", pages="243-259",
         doi="10.1057/s41283-021-00078-3"),
    stub("berlinger-dobranszky-bartus-molnar-2021-risks",
         "Overdue Debts and Financial Exclusion",
         ["berlinger-edina", "Katalin Dobránszky-Bartus", "György Molnár"],
         "Risks", 2021,
         volume="9", issue="9", pages="158",
         doi="10.3390/risks9090158"),
    stub("berlinger-kereszturi-et-al-2021-soceco",
         "Does governance matter? Country-level determinants of operational risk",
         ["berlinger-edina", "Judit Lilla Keresztúri", "Ágnes Lublóy", "Zsuzsanna Tamásné Vőneki"],
         "Society and Economy", 2021,
         volume="43", issue="4", pages="289-313",
         doi="10.1556/204.2021.00018"),

    # 2019
    stub("berlinger-2019-cogent",
         "Why APRC is misleading and how it should be reformed",
         ["berlinger-edina"],
         "Cogent Economics & Finance", 2019,
         volume="7", issue="1", pages="1609766",
         doi="10.1080/23322039.2019.1609766"),

    # 2018
    stub("berlinger-bihary-walter-2018-sef",
         "Corporate cash-pool valuation: a Monte Carlo approach",
         ["berlinger-edina", "Zsolt Bihary", "György Walter"],
         "Studies in Economics and Finance", 2018,
         volume="35", issue="1", pages="153-162",
         doi="10.1108/SEF-04-2017-0078"),

    # 2017
    stub("berlinger-lovas-juhasz-2017-cejor",
         "State subsidy and moral hazard in corporate financing",
         ["berlinger-edina", "Anita Lovas", "Péter Juhász"],
         "Central European Journal of Operations Research", 2017,
         volume="25", issue="4", pages="743-770",
         doi="10.1007/s10100-016-0461-8"),

    # 2016
    stub("berlinger-domotor-et-al-2016-cebr",
         "Stress Indicator for Clearing Houses",
         ["berlinger-edina", "Barbara Dömötör", "Ferenc Illés", "Kata Váradi"],
         "Central European Business Review", 2016,
         volume="2016", issue="4", pages="47-60",
         doi="10.18267/j.cebr.165"),
    stub("berlinger-walter-2016-cebr",
         "Income Contingent Repayments: How Can We Get into a Debt Trap?",
         ["berlinger-edina", "György Walter"],
         "Central European Business Review", 2016,
         volume="2016", issue="2", pages="37-46",
         doi="10.18267/j.cebr.149"),

    # 2015
    stub("berlinger-walter-2015-acta",
         "Income Contingent Repayment Scheme for Non-Performing Mortgage Loans in Hungary",
         ["berlinger-edina", "György Walter"],
         "Acta Oeconomica", 2015,
         volume="65", issue="s1", pages="123-147",
         doi="10.1556/032.65.2015.s1.7"),
    stub("megyeri-berlinger-2015-ksz",
         "Mélyszegénységből a felsőoktatásba",
         ["Krisztina Megyeri", "berlinger-edina"],
         "Közgazdasági Szemle", 2015,
         volume="62", issue="6", pages="674-699",
         doi="10.18414/ksz.2015.6.674"),
    stub("berlinger-juhasz-lovas-2015-ksz",
         "Az állami támogatás hatása a projektfinanszírozásra erkölcsi kockázat és pozitív externáliák mellett",
         ["berlinger-edina", "Péter Juhász", "Anita Lovas"],
         "Közgazdasági Szemle", 2015,
         volume="62", issue="2", pages="139-171",
         doi="10.18414/ksz.2015.2.139"),

    # 2011
    stub("berlinger-szenes-michaletzky-2011-ksz",
         "A fedezetlen bankközi forintpiac hálózati dinamikájának vizsgálata",
         ["berlinger-edina", "Márk Szenes", "Márton Michaletzky"],
         "Közgazdasági Szemle", 2011,
         volume="58", issue="3", pages="229-252"),

    # 2005
    stub("berlinger-2005-ksz",
         "A nyugdíjrendszer és a diákhitelrendszer összekapcsolása",
         ["berlinger-edina"],
         "Közgazdasági Szemle", 2005,
         volume="52", issue="9", pages="631-647"),

    # 2002
    stub("berlinger-2002-ksz",
         "A jövedelemarányos törlesztésű diákhitel egyszerű modellje",
         ["berlinger-edina"],
         "Közgazdasági Szemle", 2002,
         volume="49", issue="12", pages="1042-1062"),
]

# Set url_published from DOI when DOI is set
for p in NEW_PAPERS:
    if p["doi"] and not p["url_published"]:
        p["url_published"] = f"https://doi.org/{p['doi']}"

added = 0
for p in NEW_PAPERS:
    f = PAPERS / f"{p['id']}.json"
    if f.exists():
        print(f"skip (exists): {p['id']}")
        continue
    save(f, p)
    added += 1
print(f"\nadded {added} new Berlinger paper stubs")
