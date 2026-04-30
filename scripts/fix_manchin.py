"""Set abstracts on 6 Manchin papers."""
import json
from pathlib import Path

PAPERS = Path(__file__).resolve().parent.parent / "data" / "papers"


def load(slug):
    return json.loads((PAPERS / f"{slug}.json").read_text(encoding="utf-8"))


def save(slug, data):
    (PAPERS / f"{slug}.json").write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


ABSTRACTS = {
    "bekkers-francois-et-al-2012-eer": (
        "We compare three theoretical explanations for the positive empirical "
        "relationship between importer income per capita and traded goods "
        "prices. A first explanation is that consumers with higher incomes "
        "demand higher quality goods with higher prices. A second explanation "
        "is that wealthier people exhibit an increased willingness to pay for "
        "necessary goods as more goods enter the consumption set in a "
        "hierarchic demand system, and can thus be charged higher markups. A "
        "third explanation is that consumers with higher incomes are more "
        "finicky regarding their preferred variety in an ideal variety "
        "framework and can thus be charged higher markups. We discriminate "
        "between these three theories by focusing on the effect of income "
        "inequality on trade prices. Based on a large dataset with bilateral "
        "HS6 level data on 1260 final goods categories from more than 100 "
        "countries between 2000 and 2004, we find a highly significant "
        "negative effect of income inequality on unit values."
    ),
    "brenton-manchin-2014-wssii": (
        "A key element of the EU's free trade and preferential trade "
        "agreements is the extent to which they deliver improved market "
        "access and so contribute to the EU's foreign policy objectives "
        "towards developing countries and neighbouring countries in Europe, "
        "including the countries of the Balkans. Previous preferential trade "
        "schemes have been ineffective in delivering improved access to the "
        "EU market since only a small proportion of the available preferences "
        "have actually been utilised. The main reason for this is probably "
        "the very restrictive rules of origin that the EU imposes, coupled "
        "with the costs of proving consistency with these rules. If the EU "
        "wants the 'Everything but Arms' agreement and free trade agreements "
        "with countries in the Balkans to generate substantial improvements "
        "in access to the EU market for products from these countries then "
        "it will have to reconsider the current rules of origin and "
        "implement less restrictive rules backed up by a careful safeguards "
        "policy."
    ),
    "francois-manchin-2013-wd": (
        "We work with a panel of bilateral trade, exploring the influence of "
        "infrastructure and institutional quality on patterns of trade with "
        "a Poisson estimator, extended with the Baier and Berstrand method "
        "for multilateral resistance and accounting for firm heterogeneity "
        "and selection. Trade depends on institutional quality and exporter "
        "and importer access to well developed transport and communications "
        "infrastructure. While we emphasize exports of developing countries, "
        "low institutional and infrastructure quality in the South also "
        "limits market access for exports from the North. The pattern of "
        "results implies that policy emphasis on developing country market "
        "access while not providing enough support for trade facilitation, "
        "may be misplaced."
    ),
    "francois-manchin-et-al-2013-hocge": (
        "We provide an overview of several approaches to modeling market "
        "structure in multisector general equilibrium (MSGE) models, "
        "including both oligopoly and monopolistic competition. We emphasize "
        "open economy models and applications to international economic "
        "policy. We map out practical strategies for implementing variations "
        "on market structure, including functional forms and calibration "
        "strategies. We also identify areas that, in our view, are promising "
        "for further research. This includes both exploring the implications "
        "of moving away from average cost pricing models (including "
        "monopolistic competition) for labor market outcomes and inequality, "
        "and better methods for econometric estimation of parameters and "
        "confronting alternative forms of market structure against measures "
        "of model performance (specification testing)."
    ),
    "hijzen-gorg-et-al-2007-eer": (
        "Cross-border mergers and acquisitions (M&As) have increased "
        "dramatically over the last two decades. This paper analyses the "
        "role of trade costs in explaining the increase in the number of "
        "cross-border M&As. In particular, we distinguish horizontal and "
        "non-horizontal M&As and investigate whether trade costs affect "
        "these two types of mergers differently. We analyse this question "
        "using industry data for 23 OECD countries for the period 1990-2001. "
        "Our findings suggest that while in the aggregate trade costs affect "
        "cross-border merger activity negatively its impact differs "
        "importantly across horizontal and non-horizontal mergers. The "
        "impact of trade costs is less negative for horizontal mergers, "
        "which is consistent with the tariff-jumping argument."
    ),
    "manchin-orazbayev-2018-wd": (
        "Using a large individual-level survey spanning several years and "
        "more than 150 countries, we examine the importance of social "
        "networks in influencing individuals' intention to migrate "
        "internationally and locally. We distinguish close social networks "
        "(composed of friends and family) abroad and at the current "
        "location, and broad social networks (composed of same-country "
        "residents with intention to migrate, either internationally or "
        "locally). We find that social networks abroad are the most "
        "important driving forces of international migration intentions, "
        "with close and broad networks jointly explaining about 37% of "
        "variation in the probability intentions. Social networks are found "
        "to be more important factors driving migration intentions than "
        "work-related aspects or wealth (wealth accounts for less than 3% "
        "of the variation). In addition, we find that having stronger close "
        "social networks at home has the opposite effect by reducing the "
        "likelihood of migration intentions, both internationally and "
        "locally."
    ),
}
for slug, abstract in ABSTRACTS.items():
    p = load(slug)
    p["abstract"] = abstract
    save(slug, p)
print(f"abstracts set on {len(ABSTRACTS)} Manchin papers")
