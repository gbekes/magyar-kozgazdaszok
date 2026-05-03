"""One-off: add starter paper records for the 4 newly-admitted authors
(Tasnádi, Takáts, Schindele, Vonnák) so the catalogue has at least
their qualifying / top works on file."""
import json
import os
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
PAPERS = ROOT / "data" / "papers"


PAPERS_TO_ADD = [
    {
        "id": "tasnadi-2005-ijio",
        "title": "Price vs. quantity in oligopoly games",
        "authors": ["tasnadi-attila"],
        "journal": "International Journal of Industrial Organization",
        "year": 2006,
        "volume": "24", "issue": "3", "pages": "541-554",
        "doi": "10.1016/j.ijindorg.2005.07.009",
        "topics": ["industrial-organization", "market-design"],
        "methods": ["theory"],
    },
    {
        "id": "burka-puppe-et-al-2022-ejor",
        "title": "Voting: A machine learning approach",
        "authors": ["Dávid Burka", "Clemens Puppe", "László Szepesváry", "tasnadi-attila"],
        "journal": "European Journal of Operational Research",
        "year": 2022,
        "volume": "299", "issue": "3", "pages": "1003-1017",
        "doi": "10.1016/j.ejor.2021.10.005",
        "topics": ["mechanism-design", "methods", "political-economy"],
        "methods": ["ml-text", "theory"],
    },
    {
        "id": "barbie-puppe-tasnadi-2006-et",
        "title": "Non-manipulable domains for the Borda count",
        "authors": ["Martin Barbie", "Clemens Puppe", "tasnadi-attila"],
        "journal": "Economic Theory",
        "year": 2006,
        "volume": "27", "issue": "2", "pages": "411-430",
        "doi": "10.1007/s00199-004-0603-4",
        "topics": ["mechanism-design", "political-economy", "methods"],
        "methods": ["theory"],
    },
    {
        "id": "takats-2012-jhe",
        "title": "Aging and house prices",
        "authors": ["takats-elod"],
        "journal": "Journal of Housing Economics",
        "year": 2012,
        "volume": "21", "issue": "2", "pages": "131-141",
        "doi": "10.1016/j.jhe.2012.04.001",
        "topics": ["demographics-migration", "macroeconomics", "regional-urban"],
        "methods": ["panel-data"],
        "data_types": ["macro-aggregate"],
    },
    {
        "id": "ferrari-rogantini-takats-2019-ecmod",
        "title": "Domestic and global output gaps as inflation drivers: What does the Phillips curve tell?",
        "authors": ["Massimo Ferrari", "Filippo Rogantini Picco", "takats-elod"],
        "journal": "Economic Modelling",
        "year": 2019,
        "volume": "87", "issue": None, "pages": "238-253",
        "doi": "10.1016/j.econmod.2019.07.025",
        "topics": ["macroeconomics"],
        "methods": ["time-series", "panel-data"],
        "data_types": ["macro-aggregate"],
    },
    {
        "id": "takats-temesvary-2020-jie",
        "title": "The currency dimension of the bank lending channel in international monetary transmission",
        "authors": ["takats-elod", "temesvary-judit"],
        "journal": "Journal of International Economics",
        "year": 2020,
        "volume": "125", "issue": None, "pages": "103309",
        "doi": "10.1016/j.jinteco.2020.103309",
        "topics": ["banking-finance", "macroeconomics", "trade-fdi"],
        "methods": ["panel-data"],
        "data_types": ["admin-firm"],
    },
    {
        "id": "norli-ostergaard-schindele-2014-rfs",
        "title": "Liquidity and Shareholder Activism",
        "authors": ["Øyvind Norli", "Charlotte Ostergaard", "schindele-ibolya"],
        "journal": "Review of Financial Studies",
        "year": 2014,
        "volume": "28", "issue": "2", "pages": "486-520",
        "doi": "10.1093/rfs/hhu070",
        "topics": ["banking-finance", "firms-productivity"],
        "methods": ["panel-data"],
        "countries_studied": ["US"],
        "data_types": ["firm-level-dataset"],
    },
    {
        "id": "boubakri-cosset-schindele-2007-jbf",
        "title": "Privatization and stock market liquidity",
        "authors": ["Narjess Boubakri", "Jean-Claude Cosset", "schindele-ibolya"],
        "journal": "Journal of Banking & Finance",
        "year": 2007,
        "volume": "31", "issue": "2", "pages": "297-316",
        "doi": "10.1016/j.jbankfin.2006.04.008",
        "topics": ["banking-finance", "transition-postcommunist", "firms-productivity"],
        "methods": ["panel-data"],
        "data_types": ["firm-level-dataset"],
    },
    {
        "id": "ferrell-liang-renneboog-schindele-2015-rof",
        "title": "Social Capital and the Viability of Stakeholder-Oriented Firms: Evidence from Workers Cooperatives",
        "authors": ["Allen Ferrell", "Hao Liang", "Luc Renneboog", "schindele-ibolya"],
        "journal": "European Finance Review",
        "year": 2015,
        "volume": "20", "issue": "5", "pages": "1673-1718",
        "doi": "10.1093/rof/rfv047",
        "topics": ["banking-finance", "firms-productivity"],
        "methods": ["panel-data"],
        "data_types": ["firm-level-dataset"],
    },
    {
        "id": "ongena-schindele-vonnak-2018-jimf",
        "title": "Why do firms default on their foreign currency loans? The case of Hungary",
        "authors": ["Steven Ongena", "schindele-ibolya", "vonnak-dzsamila"],
        "journal": "Journal of International Money and Finance",
        "year": 2018,
        "volume": "86", "issue": None, "pages": "207-222",
        "doi": "10.1016/j.jimonfin.2018.05.001",
        "topics": ["banking-finance", "transition-postcommunist"],
        "methods": ["panel-data"],
        "countries_studied": ["HU"],
        "data_types": ["admin-firm"],
    },
]


def make_record(p):
    out = {
        "id": p["id"],
        "title": p["title"],
        "authors": p["authors"],
        "publication_type": "article",
        "journal": p["journal"],
        "year": p["year"],
        "volume": p.get("volume"),
        "issue": p.get("issue"),
        "pages": p.get("pages"),
        "doi": p.get("doi"),
        "working_paper_series": None,
        "url_published": f'https://doi.org/{p["doi"]}' if p.get("doi") else None,
        "url_pdf": None,
        "url_replication": None,
        "abstract": None,
        "summary_en": None,
        "summary_hu": None,
        "data_used": None,
        "data_used_hu": None,
        "policy_relevance": None,
        "policy_relevance_hu": None,
        "topics": p.get("topics", []),
        "methods": p.get("methods", []),
        "countries_studied": p.get("countries_studied", []),
        "data_types": p.get("data_types", []),
        "featured": False,
        "added_at": "2026-05-03",
        "last_reviewed_at": "2026-05-03",
        "review_status": "metadata-fetched",
    }
    return out


written = 0
for p in PAPERS_TO_ADD:
    f = PAPERS / f'{p["id"]}.json'
    if f.exists():
        print(f"  exists, skip: {p['id']}")
        continue
    f.write_text(json.dumps(make_record(p), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    written += 1
    print(f"  + {p['id']}")
print(f"\nWrote {written} papers")
