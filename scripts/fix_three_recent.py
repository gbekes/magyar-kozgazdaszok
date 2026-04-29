"""Verify, fix, and set abstracts for 3 recent author batches:
Wolf Zoltán (5), Kis-Katos Krisztina (3), Gyöngyösi Győző (2).

All 10 stubs have correct titles. One year fix needed:
- blackwood-foster-et-al-2016-aejm: 2016 -> 2021 (AEJ:Mac vol 13(3), 2021)

Also: cunningham-foster-et-al-2021-riw print-published 2023 not 2021.

Slug names left as stable identifiers.
Verbatim abstracts populated for all 10 papers from IDEAS.
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


META = {
    # Wolf
    "bartelsman-wolf-2014-restat": {
        "volume": "96", "issue": "4", "pages": "745-755",
        "doi": "10.1162/REST_a_00395",
    },
    "blackwood-foster-et-al-2016-aejm": {
        "year": 2021, "volume": "13", "issue": "3", "pages": "142-172",
        "doi": "10.1257/mac.20170282",
    },
    "cunningham-foster-et-al-2021-riw": {
        "year": 2023, "volume": "69", "issue": "4", "pages": "999-1032",
        "doi": "10.1111/roiw.12616",
    },
    "dinlersoz-wolf-2024-eint": {
        "volume": "33", "issue": "4", "pages": "604-626",
        "doi": "10.1080/10438599.2023.2233081",
    },
    "foster-grim-et-al-2016-aer": {
        "volume": "106", "issue": "5", "pages": "95-98",
        "doi": "10.1257/aer.p20161102",
    },
    # Kis-Katos
    "kis-katos-pieters-et-al-2018-imfer": {
        "doi": "10.1057/s41308-018-0065-5",
        "url_published": "https://doi.org/10.1057/s41308-018-0065-5",
    },
    "kis-katos-pieters-et-al-2025-jhr": {
        "year": 2024, "volume": "59", "issue": "6", "pages": "1830-1864",
        "doi": "10.3368/jhr.0521-11697R1",
    },
    "kis-katos-sparrow-2015-jde": {
        "doi": "10.1016/j.jdeveco.2015.06.003",
        "url_published": "https://doi.org/10.1016/j.jdeveco.2015.06.003",
    },
    # Gyöngyösi
    "verner-gyongyosi-2020-aer": {
        "volume": "110", "issue": "9", "pages": "2667-2702",
        "doi": "10.1257/aer.20181585",
    },
    "gyongyosi-verner-2022-jof": {
        "issue": "4", "pages": "2471-2523",
        "doi": "10.1111/jofi.13138",
    },
}
for slug, fields in META.items():
    p = load(slug)
    for k, v in fields.items():
        p[k] = v
    save(slug, p)
    print(f"metadata fix: {slug}")

ABSTRACTS = {
    "bartelsman-wolf-2014-restat": (
        "In this paper, we explore whether information from firm-level data "
        "can improve forecasts of aggregate productivity growth. We generate "
        "firm-level productivity measures and aggregate them into time-series "
        "components that capture within-firm productivity and the "
        "productivity contribution of reallocation. We show that these "
        "components improve aggregate total factor productivity forecasts in "
        "a simple univariate setting, even when firm-level data are available "
        "with a time lag. Lagged firm-level information also improves "
        "aggregate productivity forecasts when we combine results from a "
        "variety of different multivariate forecasting models using Bayesian "
        "model averaging techniques."
    ),
    "blackwood-foster-et-al-2016-aejm": (
        "Firm-level, revenue-based productivity measures are ubiquitous in "
        "studies of firm dynamics and aggregate outcomes. One common measure "
        "is increasingly interpreted as reflecting \u201cdistortions\u201d "
        "since in distortions' absence, equalization of marginal revenue "
        "products should yield no dispersion in this measure. Another common "
        "but distinct measure is the residual of the firm-level revenue "
        "function, which reflects \u201cfundamentals.\u201d Using micro-level "
        "US manufacturing data, we find these alternative measures are highly "
        "correlated, exhibit similar dispersion, and have similar "
        "relationships with growth and survival. However, the distinction "
        "between these alternative measures is critically important for "
        "quantitative assessment of the level and decline of allocative "
        "efficiency."
    ),
    "foster-grim-et-al-2016-aer": (
        "We explore current interpretations of firm-level dispersion in "
        "revenue-based productivity measures. Since revenue function "
        "estimates using proxy methods differ from factor elasticities, the "
        "residual emerging from this method remains a combination of demand "
        "and technical efficiency shocks, and is not equal to the concept of "
        "revenue productivity that plays an important role in recent "
        "literature on misallocation. This has implications for applications "
        "where measured revenue productivity dispersion is used as an "
        "indicator of misallocation. Our empirical evidence suggests, under "
        "iso-elastic demand, measured dispersion may indicate either "
        "distortions or variation in demand shocks and technical efficiency "
        "or all of the above."
    ),
    "cunningham-foster-et-al-2021-riw": (
        "We describe new experimental productivity dispersion statistics, "
        "Dispersion Statistics on Productivity (DiSP), jointly produced by "
        "the Bureau of Labor Statistics (BLS) and the Census Bureau, that "
        "complement the official BLS industry-level productivity statistics. "
        "Dispersion in productivity across businesses can provide information "
        "about the nature of competition and frictions within sectors and "
        "the sources of rising wage inequality across businesses. DiSP data "
        "show enormous differences in productivity across establishments "
        "within industries in the manufacturing sector. We find substantial "
        "variation in dispersion across industries, increasing dispersion "
        "from 1997 to 2016, and countercyclical total factor productivity "
        "dispersion."
    ),
    "dinlersoz-wolf-2024-eint": (
        "This paper provides direct evidence of automation's role in "
        "production using establishment-level data from the U.S. Census "
        "Bureau's Survey of Manufacturing Technology. The data indicate that "
        "more automated plants have lower production labor share and higher "
        "capital share, higher labor productivity, and a smaller fraction of "
        "workers in production who receive higher wages. To understand the "
        "connection between automation and total factor productivity, we "
        "estimate a CES model of production where a plant chooses the degree "
        "of automation by adjusting the relative weight of capital and "
        "production labor given their relative price. Overall, broad and "
        "deep automation is concentrated in larger plants with higher total "
        "factor productivity and lower labor share, consistent with a role "
        "for automation in contributing to dispersion in input utilization "
        "and market share."
    ),
    "kis-katos-pieters-et-al-2018-imfer": (
        "We analyze the gender-specific effects of trade liberalization on "
        "participation in market work, domestic duties, and marriage rates "
        "in Indonesia. We show that female work participation increased and "
        "participation in domestic duties declined in regions that were more "
        "exposed to input tariff reductions. The effects of output tariff "
        "reductions were much less pronounced, and we find little impacts on "
        "men. Among the potential channels, we find that reductions in input "
        "tariffs led to a relative expansion of more female-intensive sectors "
        "as well as a decrease in sectoral gender segregation, especially "
        "among the low skilled. Liberalization also led to delayed marriage "
        "among both sexes and reduced fertility among less educated women."
    ),
    "kis-katos-pieters-et-al-2025-jhr": (
        "Combining data from China's population and firm censuses between "
        "1990 and 2005, this paper relates prefecture-level employment by "
        "gender to the regionalized measure of exposure to tariff reductions. "
        "We find that increasing import competition kept more females in the "
        "workforce, reducing an otherwise growing gender employment gap in "
        "the long run. These dynamics were present both in local economies "
        "as a whole and among private firms in the formal industrial sector. "
        "The gendered employment effects of trade-induced competitive "
        "pressures can be attributed to an expansion of female-intensive "
        "industries, a reduction in gender discrimination, and technology "
        "upgrades through computerization."
    ),
    "kis-katos-sparrow-2015-jde": (
        "We measure the effects of trade liberalization over the period of "
        "1993\u20132002 on regional poverty levels in 259 Indonesian "
        "districts, and investigate the labor market mechanisms behind these "
        "effects. The identification strategy relies on combining information "
        "on initial regional labor and product market structure with the "
        "exogenous tariff reduction schedule over four three-year periods. We "
        "add to the literature on local labor market effects of trade "
        "policies by distinguishing between tariffs for output markets and "
        "for intermediate inputs, and finding that poverty reduced especially "
        "in districts with a greater sector exposure to input tariff "
        "liberalization. Among the potential channels behind this effect, we "
        "show that low-skilled work participation and middle-skilled wages "
        "were more responsive to reductions in import tariffs on intermediate "
        "goods than to reductions in import tariffs on final outputs."
    ),
    "verner-gyongyosi-2020-aer": (
        "We examine the consequences of a sudden increase in household debt "
        "burdens by exploiting variation in exposure to household foreign "
        "currency debt during Hungary's late-2008 currency crisis. The "
        "revaluation of debt burdens causes higher default rates and a "
        "collapse in spending. These responses lead to a worse local "
        "recession, driven by a decline in local demand, and negative "
        "spillover effects on nearby borrowers without foreign currency debt. "
        "The estimates translate into an output multiplier on higher debt "
        "service of 1.67. The impact of debt revaluation is particularly "
        "severe when foreign currency debt is concentrated on household, "
        "rather than firm, balance sheets."
    ),
    "gyongyosi-verner-2022-jof": (
        "We study the impact of debtor distress on support for a populist "
        "far-right political party during a financial crisis. Our empirical "
        "approach exploits variation in exposure to foreign currency "
        "household loans during a currency crisis in Hungary. Foreign "
        "currency debt exposure leads to a large, persistent increase in "
        "support for the populist far right. We document that the far right "
        "advocated for foreign currency debtors' interests by proposing "
        "aggressive debt relief and was rewarded with support from these "
        "voters. Our findings are consistent with theories emphasizing that "
        "conflict between creditors and debtors can shape political outcomes "
        "after financial crises."
    ),
}
for slug, abstract in ABSTRACTS.items():
    p = load(slug)
    p["abstract"] = abstract
    save(slug, p)
print(f"abstracts set on {len(ABSTRACTS)} papers")
