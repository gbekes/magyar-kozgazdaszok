"""Set abstracts on 4 Harasztosi papers that lack them."""
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
    "cede-chiriacescu-et-al-2018-rowe": (
        "The literature shows that openness to trade improves long-term growth "
        "but also that it may increase exposure to high output volatility. In "
        "this vein, our paper investigates whether exporting and export "
        "diversification at the firm level have an effect on the output "
        "volatility of firms. We use large representative firm-level databases "
        "from Estonia, Hungary, Romania, Slovakia and Slovenia over the last "
        "boom-bust cycle in 2004-2012. The results confirm that exporting is "
        "related to higher volatility at the firm level. There is also "
        "evidence that this effect increased during the Great Recession due "
        "to the large negative shocks in export markets. In contrast to the "
        "literature and empirical findings for large or advanced countries we "
        "do not find a statistically significant and consistent mitigating "
        "effect from export diversification in the Central and Eastern "
        "European countries. In addition, exporting more products or serving "
        "more markets does not necessarily result in higher stability of firm "
        "sales."
    ),
    "endresz-harasztosi-2014-emr": (
        "The paper investigates the impact of foreign currency lending on "
        "investment. Using Hungarian firm level data, we test whether foreign "
        "currency lending contributed to larger investment before the crisis "
        "and whether the depreciation during the Great Recession resulted in "
        "lower investment rate for firms with foreign currency loans. Results "
        "of OLS and matching estimations show that before the crisis FX "
        "lending increased investment rates and during the crisis the "
        "investment rate of firms with FX loans declined more because of the "
        "balance sheet effects triggered by the depreciation. These effects "
        "were found to be more pronounced for liquidity constrained firms."
    ),
    "harasztosi-2015-ee": (
        "Spillovers from peers in the immediate environment can encourage "
        "firms to engage in trade. This study examines whether there are "
        "spillover effects in exporting activity, using Hungarian product\u2013"
        "country-level manufacturing trade data used from 1993 to 2003. "
        "Evidence suggests that exporting activity exhibits spillovers and "
        "benefits that are country and product specific. In addition, export "
        "spillovers exhibit considerable heterogeneity. Foreign-owned firms "
        "benefit from peers generally and domestic firms only from the "
        "agglomeration of domestic exporters. Spillovers are positively "
        "related to country distance and negatively to market size."
    ),
    "teruel-coad-et-al-2021-tjott": (
        "This paper explores the relationship between new digital technologies, "
        "internationalisation activity and its impact on High Growth "
        "Enterprises (HGEs), using the EIB Group Survey of Investment and "
        "Investment Finance and ORBIS data for 27 EU Member States and the "
        "United Kingdom. After controlling for sample selection bias, our "
        "results suggest that being a HGE is positively associated with the "
        "probability that a firm conducts international activities, "
        "particularly FDI. Conversely, the internationalisation process seems "
        "to trigger strong subsequent firm-growth only for FDI, not for "
        "exports. Furthermore, we show evidence on the positive association "
        "between firms that are internationalised and those adopting new "
        "digital technologies."
    ),
}
for slug, abstract in ABSTRACTS.items():
    p = load(slug)
    p["abstract"] = abstract
    save(slug, p)
print(f"abstracts set on {len(ABSTRACTS)} Harasztosi papers")
