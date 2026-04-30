"""Set abstracts on Halpern (1), Elekes (1), Gáspár (1)."""
import json
from pathlib import Path

PAPERS = Path(__file__).resolve().parent.parent / "data" / "papers"


def load(slug):
    return json.loads((PAPERS / f"{slug}.json").read_text(encoding="utf-8"))


def save(slug, data):
    (PAPERS / f"{slug}.json").write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


META = {
    "egert-halpern-2005-jobf": {
        "year": 2006, "volume": "30", "issue": "5", "pages": "1359-1374",
        "doi": "10.1016/j.jbankfin.2005.07.001",
    },
    "elekes-stojkoski-et-al-2022-eg": {
        "volume": "98", "issue": "4", "pages": "355-378",
        "doi": "10.1080/00130095.2022.2035715",
    },
    "gaspar-giommoni-et-al-2025-jde": {
        "volume": "177", "pages": "103526",
        "doi": "10.1016/j.jdeveco.2025.103459",
    },
}
for slug, fields in META.items():
    p = load(slug)
    for k, v in fields.items():
        p[k] = v
    save(slug, p)
    print(f"metadata fix: {slug}")

ABSTRACTS = {
    "egert-halpern-2005-jobf": (
        "This paper analyses the ever-growing literature on equilibrium "
        "exchange rates in the new EU member states of Central and Eastern "
        "Europe in a quantitative manner using meta-regression analysis. "
        "The results indicate that the real misalignments reported in the "
        "literature are systematically influenced, inter alia, by the "
        "underlying theoretical concepts (Balassa-Samuelson effect, "
        "Behavioural Equilibrium Exchange Rate, Fundamental Equilibrium "
        "Exchange Rate) and by the econometric estimation methods. The "
        "important implication of these findings is that a systematic "
        "analysis is needed in terms of both alternative economic and "
        "econometric specifications to assess equilibrium exchange rates."
    ),
    "elekes-stojkoski-et-al-2022-eg": (
        "This paper assesses the network robustness of the technological "
        "capability base of 269 European metropolitan areas against the "
        "potential elimination of some of their capabilities. By doing so "
        "it provides systematic evidence on how network robustness "
        "conditioned the economic resilience of these regions in the "
        "context of the 2008 economic crisis. The analysis concerns calls "
        "in the relevant literature for more in-depth analysis on the link "
        "between regional economic network structures and the resilience "
        "of regions to economic shocks. By adopting a network science "
        "approach that is novel to economic geographic inquiry, the "
        "objective is to stress-test the technological resilience of "
        "regions by utilizing information on the co-classification of CPC "
        "classes listed on European Patent Office patent documents. "
        "Findings from a regression analysis indicate that metropolitan "
        "regions with a more robust technological knowledge network "
        "structure exhibit higher levels of resilience with respect to "
        "changes in employment rates. Regions with high levels of "
        "employment in industry but with vulnerable technological "
        "capability base are particularly challenged by this aspect of "
        "regional economic resilience."
    ),
    "gaspar-giommoni-et-al-2025-jde": (
        "This paper shows that corruption generates extremism, but mainly "
        "on the opposition side. While corruption hurts all citizens, only "
        "voters on the minority side may desire to switch to a more "
        "extreme representative when they perceive a more corrupt "
        "political system. In our model, campaigning on a corruption "
        "scandal against the incumbent gives a higher winning probability "
        "for the opposition politician but simultaneously reduces expected "
        "future rents from office. As extremist politicians normally are "
        "less likely to win against a moderate opponent, they have a "
        "stronger incentive to take a stand against corruption. Given that "
        "the side of the political minority has a lower chance of having "
        "their representative elected to office, they face a smaller "
        "opportunity cost of voting for extremists. Our main result is "
        "that minorities are more likely to react to corruption with more "
        "extremism. We provide causal evidence for this novel asymmetric "
        "prediction from Indonesia and Brazil."
    ),
}
for slug, abstract in ABSTRACTS.items():
    p = load(slug)
    p["abstract"] = abstract
    save(slug, p)
print(f"abstracts set on {len(ABSTRACTS)} papers")
