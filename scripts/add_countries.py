"""Add country codes to authors based on their affiliations.

For each author, derive a list of ISO-3166 alpha-2 country codes from
their `affiliations` (deduped, in affiliation order). Write the result
to a top-level `countries` field on the author JSON.

Run: python scripts/add_countries.py
"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
AUTHORS = ROOT / "data" / "authors"

# Affiliation name -> country code(s). Compound affiliations (e.g.
# "Bruegel (Brussels) & Corvinus") get multiple codes.
INSTITUTION_COUNTRY = {
    # --- Hungary ---
    "KRTK Institute of Economics": ["HU"],
    "HUN-REN KRTK Institute of Economics": ["HU"],
    "HUN-REN Centre for Social Sciences": ["HU"],
    "Corvinus University of Budapest": ["HU"],
    "Corvinus University of Budapest (emeritus)": ["HU"],
    "Eötvös Loránd University": ["HU"],
    "Budapest University of Technology and Economics": ["HU"],
    "John von Neumann University": ["HU"],
    "University of Debrecen": ["HU"],
    "University of Pécs, Faculty of Business and Economics": ["HU"],
    "Magyar Nemzeti Bank": ["HU"],
    "Bank for International Settlements": ["CH"],

    # --- Austria (CEU is in Vienna since 2019) ---
    "Central European University": ["AT"],
    "Complexity Science Hub Vienna": ["AT"],
    "University of Vienna": ["AT"],

    # --- UK ---
    "London School of Economics": ["GB"],
    "University College London": ["GB"],
    "University of Oxford": ["GB"],
    "University of Bristol": ["GB"],
    "University of Manchester": ["GB"],
    "University of Liverpool": ["GB"],
    "Institute for Fiscal Studies": ["GB"],
    "CEPR": ["GB"],
    "Centre for Economic Policy Research (CEPR)": ["GB"],

    # --- US ---
    "Duke University": ["US"],
    "Princeton University": ["US"],
    "Vanderbilt University": ["US"],
    "Yale School of Management": ["US"],
    "Columbia Business School": ["US"],
    "University of Michigan": ["US"],
    "University of Houston": ["US"],
    "Syracuse University": ["US"],
    "Harvard University (emeritus)": ["US"],
    "Federal Reserve Board (Washington, DC)": ["US"],
    "National Bureau of Economic Research (NBER)": ["US"],
    "U.S. Census Bureau, Center for Economic Studies": ["US"],
    "Westat": ["US"],
    "International Monetary Fund (IMF)": ["US"],
    "World Bank": ["US"],

    # --- Italy (JRC main site is Ispra, IT) ---
    "Bocconi University": ["IT"],
    "Politecnico di Milano, School of Management": ["IT"],
    "European Commission Joint Research Centre (JRC)": ["IT"],

    # --- Spain ---
    "Universitat Pompeu Fabra": ["ES"],
    "Universitat Autònoma de Barcelona": ["ES"],
    "Barcelona School of Economics": ["ES"],
    "Centre de Recerca en Economia Internacional (CREI)": ["ES"],

    # --- Sweden / Norway / Netherlands ---
    "Stockholm University": ["SE"],
    "Norwegian School of Economics (NHH)": ["NO"],
    "Utrecht University": ["NL"],

    # --- Germany ---
    "University of Bonn": ["DE"],
    "Kiel Institute for the World Economy": ["DE"],
    "University of Göttingen": ["DE"],
    "IZA Institute of Labor Economics": ["DE"],

    # --- France / Belgium / Luxembourg ---
    "ESSEC Business School": ["FR"],
    "University of Luxembourg": ["LU"],

    # --- Eastern Europe ---
    "DSK Bank Bulgaria": ["BG"],
    "OTP Bank Romania": ["RO"],

    # --- Canada ---
    "University of British Columbia, Vancouver School of Economics": ["CA"],
    "University of Toronto": ["CA"],

    # --- Compound ---
    "Bruegel (Brussels) & Corvinus University of Budapest": ["BE", "HU"],
}


import re

# Institutions that are research networks / fellowships / supervisory
# board roles -- not "real jobs" in the sense the editor uses for the
# country flag. They DO appear on the page as affiliations, but they
# don't contribute a country flag.
NOT_PRIMARY_JOB = {
    "IZA Institute of Labor Economics",
    "Centre for Economic Policy Research (CEPR)",
    "CEPR",
    "National Bureau of Economic Research (NBER)",
    "DSK Bank Bulgaria",
    "OTP Bank Romania",
}

# Roles that are temporary / past / visiting -- excluded from flag derivation.
PAST_ROLE_RE = re.compile(r"\(\s*\d{4}\s*[–\-]\s*\d{4}\s*\)")
VISITING_ROLE_RE = re.compile(r"\bvisiting\b", re.IGNORECASE)


def is_primary_job(af):
    if (af.get("name") or "") in NOT_PRIMARY_JOB:
        return False
    role = af.get("role") or ""
    if PAST_ROLE_RE.search(role):
        return False
    if VISITING_ROLE_RE.search(role):
        return False
    return True


def derive_countries(author):
    out = []
    seen = set()
    for af in author.get("affiliations") or []:
        if not is_primary_job(af):
            continue
        name = af.get("name") or ""
        codes = INSTITUTION_COUNTRY.get(name, [])
        for c in codes:
            if c not in seen:
                seen.add(c)
                out.append(c)
        if len(out) >= 2:  # cap at 2 flags
            break
    return out


def main():
    authors = sorted(AUTHORS.glob("*.json"))
    unmapped_affs = set()
    written = 0
    no_country = []
    for f in authors:
        a = json.loads(f.read_text(encoding="utf-8"))
        countries = derive_countries(a)
        # Track unmapped affiliations
        for af in a.get("affiliations") or []:
            name = af.get("name") or ""
            if name and name not in INSTITUTION_COUNTRY:
                unmapped_affs.add(name)
        old = a.get("countries")
        if countries != old:
            a["countries"] = countries
            f.write_text(json.dumps(a, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            written += 1
        if not countries:
            no_country.append(a["id"])

    print(f"Updated countries on {written} of {len(authors)} authors.")
    if no_country:
        print(f"\n{len(no_country)} authors with no country derived (check affiliations):")
        for s in no_country:
            print(f"  - {s}")
    if unmapped_affs:
        print(f"\n{len(unmapped_affs)} unmapped affiliation names:")
        for n in sorted(unmapped_affs):
            print(f"  - {n}")


if __name__ == "__main__":
    main()
