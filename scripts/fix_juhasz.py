"""Verify, fix, and set abstracts on the 8 Juhász stubs (3 Réka + 5 Sándor).

Verified each against canonical sources:
- Réka Juhász (UBC, industrial policy): rjuhasz.com/research, NBER profile
- Sándor Juhász (Corvinus / KRTK, economic geography): Scholar profile
  (xIQ6Wt8AAAAJ), IDEAS WP series (egu/wpaper).

All 8 titles match canonical sources. Year fixes needed for 2 Sándor papers
where slug-year reflects online/manuscript date but print-publication year
differs:
- juhasz-lengyel-2017-joeg: year 2017 -> 2018 (JoEG vol 18(6), 2018)
- juhasz-2019-sbe: year 2019 -> 2021 (SBE vol 56(4), 2021)

Slug names left unchanged.
"""
import json
from pathlib import Path

PAPERS = Path(__file__).resolve().parent.parent / "data" / "papers"


def load(slug):
    return json.loads((PAPERS / f"{slug}.json").read_text(encoding="utf-8"))


def save(slug, data):
    (PAPERS / f"{slug}.json").write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


YEAR_FIXES = {
    "juhasz-lengyel-2017-joeg": 2018,
    "juhasz-2019-sbe": 2021,
}
for slug, year in YEAR_FIXES.items():
    p = load(slug)
    p["year"] = year
    save(slug, p)
    print(f"year fix: {slug} -> {year}")

# pages/issues fix for the 2 Sándor papers
META = {
    "juhasz-lengyel-2017-joeg": {"volume": "18", "issue": "6", "pages": "1203-1226"},
    "juhasz-2019-sbe": {"volume": "56", "issue": "4", "pages": "1385-1404"},
}
for slug, fields in META.items():
    p = load(slug)
    for k, v in fields.items():
        p[k] = v
    save(slug, p)

ABSTRACTS = {
    "juhasz-2018-aer": (
        "This paper uses a natural experiment to estimate the causal effect of "
        "temporary trade protection on long-term economic development. I find "
        "that regions in the French Empire which became better protected from "
        "trade with the British for exogenous reasons during the Napoleonic "
        "Wars (1803-1815) increased capacity in mechanized cotton spinning to "
        "a larger extent than regions which remained more exposed to trade. In "
        "the long run, regions with exogenously higher spinning capacity had "
        "higher activity in mechanized cotton spinning. They also had higher "
        "value added per capita in industry up to the second half of the "
        "nineteenth century, but not later."
    ),
    "juhasz-squicciarini-et-al-2024-jpe": (
        "New technologies tend to be adopted slowly and\u2014even after being "
        "adopted\u2014take time to be reflected in higher aggregate "
        "productivity. One prominent explanation is that major technological "
        "breakthroughs create the need to reorganize production. We study a "
        "unique setting that allows us to examine this mechanism: the adoption "
        "of mechanized cotton spinning during the first Industrial Revolution "
        "in France. Using a novel hand-collected, plant-level dataset from "
        "French archival sources, we show that a process of \u201ctrial and "
        "error\u201d in reorganizing production led to initially low and widely "
        "dispersed productivity across firms operating the new technology. In "
        "the subsequent decades, we observe high productivity growth as "
        "knowledge diffused through the economy and new entrants adopted "
        "improved methods of organizing production."
    ),
    "juhasz-steinwender-2024-aroe": (
        "We discuss recent work evaluating the role of the government in "
        "shaping the economy during the long nineteenth century, a practice we "
        "refer to as industrial policy. States deployed a vast variety of "
        "different policies aimed primarily, but not exclusively, at fostering "
        "industrialization. A thin but growing literature has started to "
        "evaluate the economic effects of these policies, but many questions "
        "remain open for study."
    ),
    "juhasz-lengyel-2017-joeg": (
        "Triadic closure and geographical proximity are consistently found to "
        "be the strongest factors influencing the formation of intra-cluster "
        "knowledge ties. Less is known, however, about the persistence of such "
        "knowledge ties. We use a unique longitudinal dataset on knowledge "
        "ties in the printing and paper-products cluster of Kecskemét, "
        "Hungary, to investigate the formation versus the persistence of "
        "knowledge ties. We find that triadic closure and geographical "
        "proximity increase the probability of tie creation but do not affect "
        "tie persistence. Cognitive proximity, in contrast, is associated "
        "with longer-lasting ties. The results suggest that the formation "
        "and persistence of cluster knowledge ties are governed by different "
        "mechanisms."
    ),
    "juhasz-2019-sbe": (
        "It is generally acknowledged that in order to have access to locally "
        "accumulated industrial knowledge, firms have to collaborate and take "
        "part in cluster knowledge networks. This study argues that the "
        "inherited capabilities of spinoff enable them to cooperate and "
        "exchange knowledge more easily and to gain more from positive "
        "knowledge externalities in clusters. The basis of the analysis is a "
        "relational dataset on a printing and paper product cluster in "
        "Hungary, and I use exponential random graph models to explain the "
        "formation of knowledge ties. I demonstrate that besides geographical "
        "proximity, ownership similarity and network structural effects, "
        "being a spinoff company enhances tie formation in the local network. "
        "Results suggest that spinoffs are indeed more likely to collaborate "
        "and take advantage of knowledge concentration."
    ),
    "juhasz-elekes-et-al-2026-joeg": (
        "Strong local clusters help firms compete on global markets. One "
        "explanation for this is that firms benefit from locating close to "
        "their suppliers and customers. However, the emergence of global "
        "supply chains shows that physical proximity is not necessarily a "
        "prerequisite to successfully manage customer-supplier relations "
        "anymore. This raises the question when firms need to colocate in "
        "value chains and when they can coordinate over longer distances. We "
        "hypothesize that one important aspect is the extent to which supply "
        "chain partners exchange not just goods but also know-how. We exploit "
        "detailed micro-data for the Hungarian economy between 2015 and 2017, "
        "linking firm registries, employer-employee matched data and "
        "firm-to-firm transaction data from value-added tax records. We show "
        "that supply chains are more likely to support coagglomeration when "
        "the industries involved are also skill related. That is, "
        "input-output and labor market channels reinforce each other, but "
        "supplier connections only matter for colocation when industries "
        "have similar labor requirements, suggesting that they employ similar "
        "types of know-how."
    ),
    "juhasz-wachs-et-al-2026-respol": (
        "Despite the growing importance of the digital sector, research on "
        "economic complexity and its implications continues to rely mostly on "
        "administrative records, e.g. data on exports, patents, and "
        "employment, that have blind spots when it comes to the digital "
        "economy. In this paper we use data on the geography of programming "
        "languages used in open-source software to extend economic complexity "
        "ideas to the digital economy. We estimate a country's software "
        "economic complexity index (ECIsoftware) and show that it complements "
        "the ability of measures of complexity based on trade, patents, and "
        "research to account for international differences in GDP per capita, "
        "income inequality, and emissions. We also show that open-source "
        "software follows the principle of relatedness, meaning that a "
        "country's entries and exits in programming languages are partly "
        "explained by its current pattern of specialization. Together, these "
        "findings help extend economic complexity ideas and their policy "
        "implications to the digital economy."
    ),
    "juhasz-elekes-et-al-2016-ks": (
        "A tanulmány célja, hogy felhívja a hazai közgazdász szakma figyelmét "
        "a hálózatok dinamikus szemléletű elemzésének fontosságára és hazai "
        "kutatási lehetőségeire. A szerzők áttekintik, hogyan jönnek létre a "
        "gazdasági szereplők közötti kapcsolatok, milyen tényezők alakítják "
        "ezeket, és vajon a kooperációk tartósak-e. A regionális klaszterszintű "
        "tudáshálózatokat a beágyazottság és a kohézió erősíti, míg az "
        "iparági szintű hálózatok az ágazati tapasztalat, a földrajzi "
        "közelség és a közös partnerek mentén szerveződnek. A dinamikus "
        "hálózatelemzés eszközeinek és eredményeinek hazai adaptálása "
        "lényegesen hozzájárulhat a gazdasági szereplők közötti kapcsolatok "
        "rendszerének megértéséhez."
    ),
}
for slug, abstract in ABSTRACTS.items():
    p = load(slug)
    p["abstract"] = abstract
    save(slug, p)
print(f"abstracts set on {len(ABSTRACTS)} Juhász papers")
