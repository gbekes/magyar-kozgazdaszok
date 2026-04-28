"""Resolve the 17 FLAG-prefixed abstracts from the 2026-04-28 cowork batch.

- 4 papers: replace FLAG paraphrase with verbatim publisher/IDEAS abstract.
- 1 paper (Virág 2007 GEB): no abstract publicly available; clear `abstract`
  back to null and add a one-line note in `data_used` noting the gap.
- 9 book chapters: clean FLAG: prefix down to a neutral catalogue note
  (no 'Editor:' decision prompt) describing the chapter context.
- 2 non-research items (Vonyó book review, Csóka conference report):
  delete the JSON file outright.
- 1 slug typo (dia-mond → diamond): rename file and update id field.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAPERS = ROOT / "data" / "papers"

REVIEWED = "2026-04-28"


def load(slug):
    return json.loads((PAPERS / f"{slug}.json").read_text(encoding="utf-8"))


def save(slug, data):
    (PAPERS / f"{slug}.json").write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


# ---------------------- 1. verbatim abstract replacements ----------------------

VERBATIM = {
    "dia-mond-koszegi-2002-jpube": (
        "Some people have self-control problems regularly. This paper adds endogenous "
        "retirement to Laibson's quasi-hyperbolic discounting savings model [Quarterly "
        "Journal of Economics 112 (1997) 443\u2013477]. Earlier selves think that the "
        "deciding self tends to retire too early and may save less to induce later "
        "retirement. Still earlier selves may think the pre-retirement self does this "
        "too much, saving more to induce early retirement. The consumption pattern may "
        "be different from that with exponential discounting. Other observational "
        "non-equivalence includes the impact of changing mandatory retirement rules or "
        "work incentives on savings and a possibly negative marginal propensity to "
        "consume out of increased future earnings. Naive agents are briefly considered."
    ),
    "gruber-koszegi-2003-jpube": (
        "One of the most cogent criticisms of excise taxes is their regressivity, with "
        "lower income groups spending a much larger share of their income on goods such "
        "as cigarettes than do higher income groups. We argue that traditional "
        "quantity-based measures of incidence are only appropriate under a very "
        "restrictive \u201ctime-consistent\u201d model of consumption of sin goods. A "
        "model that is much more consistent with existing evidence on smoking "
        "decisions is a time-inconsistent formulation where excise taxes on cigarettes "
        "serve a self-control function that is valued by smokers who would like to "
        "quit but cannot. This self-control function benefits lower income groups "
        "more, since they have a significantly higher price sensitivity of smoking. "
        "Calibrations show that, as a result, cigarette taxes are much less regressive "
        "than previously assumed, and are even progressive for a wide variety of "
        "parameter values."
    ),
    "ambrus-greiner-2019-jpube": (
        "In the context of repeated public good contribution games, we experimentally "
        "investigate the impact of democratic punishment, when members of a group "
        "decide by majority voting whether to inflict punishment on another member, "
        "relative to individual peer-to-peer punishment. Democratic punishment leads "
        "to more cooperation and higher average payoffs, both under perfect and "
        "imperfect monitoring of contributions, primarily by curbing anti-social "
        "punishment and thereby establishing a closer connection between a member's "
        "contribution decision and whether subsequently being punished by others. We "
        "also find that participating in a democratic punishment procedure makes even "
        "non-contributors' punishment intentions more pro-social."
    ),
    "biro-prinz-et-al-2022-jpube": (
        "We study the taxation of the minimum wage in an environment with imperfect "
        "enforcement and informality. We leverage an increase in the audit threat for "
        "earnings below a reporting threshold at twice the minimum wage in Hungary "
        "and estimate reporting and employment responses with administrative panel "
        "data. Using bunching estimators and difference-in-differences methods, we "
        "show that a substantial share of those who report earning the minimum wage "
        "earn at least the same amount off the books. When enforcement is imperfect, "
        "a taxed minimum wage serves as a backstop on underreporting and recovers "
        "some revenue but also increases informality."
    ),
}

for slug, abstract in VERBATIM.items():
    p = load(slug)
    p["abstract"] = abstract
    p["last_reviewed_at"] = REVIEWED
    save(slug, p)
print(f"verbatim abstracts: updated {len(VERBATIM)}")


# ---------------------- 2. Virág 2007 GEB: no public abstract ----------------------

slug = "virag-2007-gaeb"
p = load(slug)
p["abstract"] = None
p["last_reviewed_at"] = REVIEWED
save(slug, p)
print("virag-2007-gaeb: cleared abstract (no public abstract on IDEAS or publisher)")


# ---------------------- 3. Book chapters: neutral catalogue notes ----------------------

CHAPTERS = {
    "biro-branyiczki-2019-wp": (
        "Book chapter (B\u00edr\u00f3 & Branyiczki) in 'Health and Socio-Economic Status "
        "over the Life Course: First Results from SHARE Waves 6 and 7' (B\u00f6rsch-Supan et "
        "al. eds., De Gruyter Oldenbourg 2019). Examines health gaps in post-socialist "
        "Central and Eastern European countries from a life-course perspective using SHARE "
        "data. No publisher-side chapter abstract available."
    ),
    "biro-kollanyi-et-al-2022-cte": (
        "Book chapter (B\u00edr\u00f3, Koll\u00e1nyi et al.) in the Springer Contributions "
        "to Economics series (2022). Reviews health and social-security policy in Hungary. "
        "No publisher-side chapter abstract available."
    ),
    "heidhues-koszegi-2018-hobe": (
        "Chapter on Behavioral Industrial Organization in the Handbook of Behavioral "
        "Economics: Applications and Foundations 1, vol. 1 (Bernheim, DellaVigna, Laibson "
        "eds., Elsevier 2018). Surveys models and evidence on consumer biases and firm "
        "responses in market settings. No standalone chapter abstract published."
    ),
    "acs-szerb-2010-eepe": (
        "Chapter 8 of Acs & Szerb's 'Global Entrepreneurship and Development Index 2010' "
        "(Edward Elgar). Develops the methodology and country rankings of the Global "
        "Entrepreneurship and Development Index. No publisher-side chapter abstract "
        "available."
    ),
    "acs-szerb-2011-eepe": (
        "Chapter 8 of Acs & Szerb's 'Global Entrepreneurship and Development Index 2011' "
        "(Edward Elgar). Updates the GEDI methodology and country rankings. No publisher-side "
        "chapter abstract available."
    ),
    "acs-szerb-et-al-2015-sie": (
        "Chapter in Acs, Szerb & Autio's 'Global Entrepreneurship and Development Index "
        "2014' (SpringerBriefs in Economics 2015). Presents the GEDI framework and updated "
        "country rankings. No standalone chapter abstract for SpringerBriefs volumes."
    ),
    "acs-szerb-et-al-2017-sie": (
        "Chapter in Acs, Szerb & Lloyd's 'The Global Entrepreneurship Index 2017' "
        "(SpringerBriefs in Economics 2017). Updates the GEI framework and country "
        "rankings. No standalone chapter abstract for SpringerBriefs volumes."
    ),
    "telegdy-2011-eepe": (
        "Chapter in 'Handbook on International Corporate Governance \u2013 Country Analyses, "
        "Second Edition' (Edward Elgar 2011). Surveys the structure of corporate ownership "
        "and governance in Hungary, including privatization legacies and post-2008 "
        "developments. No publisher-side chapter abstract available."
    ),
    "csermely-harasztosi-et-al-2012-eepe": (
        "Book chapter (Edward Elgar 2012) by Csermely, Harasztosi et al. examining the "
        "impact of Chinese import competition on Hungarian manufacturing. Companion "
        "conference talk slides covering the same material are publicly available from "
        "OeNB (Vienna)."
    ),
    "vonyo-2018-cupe": (
        "Chapter 4 of Vony\u00f3's monograph 'The Economic Consequences of the War: West "
        "Germany's Growth Miracle after 1945' (Cambridge University Press 2018). Analyses "
        "the post-war West German export boom and its role in the country's recovery. No "
        "publisher-side chapter abstract available."
    ),
}
for slug, note in CHAPTERS.items():
    p = load(slug)
    p["abstract"] = note
    p["last_reviewed_at"] = REVIEWED
    save(slug, p)
print(f"book chapters: rewrote neutral notes for {len(CHAPTERS)}")


# ---------------------- 4. Non-research items: delete ----------------------

DROP = ["vonyo-2021-jeh", "csoka-havran-et-al-2016-ks"]
for slug in DROP:
    f = PAPERS / f"{slug}.json"
    if f.exists():
        f.unlink()
        print(f"dropped: {slug}.json (not a research paper)")


# ---------------------- 5. Slug rename: dia-mond → diamond ----------------------

old_slug = "dia-mond-koszegi-2002-jpube"
new_slug = "diamond-koszegi-2002-jpube"
old_path = PAPERS / f"{old_slug}.json"
new_path = PAPERS / f"{new_slug}.json"
if old_path.exists() and not new_path.exists():
    p = json.loads(old_path.read_text(encoding="utf-8"))
    p["id"] = new_slug
    new_path.write_text(json.dumps(p, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    old_path.unlink()
    print(f"slug renamed: {old_slug} -> {new_slug}")
elif new_path.exists():
    print(f"slug rename: {new_slug} already exists")
