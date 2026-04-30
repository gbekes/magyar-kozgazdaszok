"""Set abstracts on 6 Valentinyi papers and fix one year."""
import json
from pathlib import Path

PAPERS = Path(__file__).resolve().parent.parent / "data" / "papers"


def load(slug):
    return json.loads((PAPERS / f"{slug}.json").read_text(encoding="utf-8"))


def save(slug, data):
    (PAPERS / f"{slug}.json").write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


# Year fix: herrendorf-valentinyi-2005-joeda was published in JEDC vol 30(8) 2006
META = {
    "herrendorf-valentinyi-2005-joeda": {
        "year": 2006, "volume": "30", "issue": "8", "pages": "1339-1361",
    },
    "herrendorf-valentinyi-2003-roed": {
        "volume": "6", "issue": "3", "pages": "483-497",
        # title in stub says "Determinacy through intertemporal capital adjustment costs"
        # canonical title is "Determinacy Through Intertemporal Adjustment Costs"
        "title": "Determinacy through intertemporal adjustment costs",
    },
}
for slug, fields in META.items():
    p = load(slug)
    for k, v in fields.items():
        p[k] = v
    save(slug, p)
    print(f"metadata fix: {slug}")

ABSTRACTS = {
    "duernecker-herrendorf-et-al-2021-joeda": (
        "The productivity growth slowdown that started in the 1970s presents "
        "a challenge to Kaldor's growth facts and the one-sector growth model. "
        "We ask: What natural modification of the growth model can generate a "
        "prolonged productivity growth slowdown? We show that the two-sector "
        "version with separate consumption and investment sectors has a "
        "balanced growth path equilibrium along which productivity growth "
        "slows down if two conditions hold: real GDP is measured with the "
        "Fisher index; productivity growth in the consumption sector slows "
        "down. We also show that real GDP measured with the Fisher index is "
        "a welfare measure in the two-sector version."
    ),
    "herrendorf-rogerson-et-al-2013-ee": (
        "Structural transformation refers to the reallocation of economic "
        "activity across the broad sectors agriculture, manufacturing, and "
        "services. This handbook chapter synthesizes recent research on "
        "structural transformation, presenting stylized facts across time and "
        "space and developing a multi-sector extension of the growth model. "
        "The authors argue this multi-sector framework effectively explains "
        "many features of structural transformation and provides insights "
        "into economic development, regional convergence, productivity trends, "
        "hours worked, business cycles, wage inequality, and emissions."
    ),
    "herrendorf-valentinyi-2003-roed": (
        "It is well known that if there are mild sector-specific externalities, "
        "then the steady state of the standard two-sector real business cycle "
        "model can become indeterminate and endogenous business cycles can "
        "arise. We show that this result is not robust to the introduction of "
        "standard intertemporal capital adjustment costs, which may accrue "
        "when total capital is adjusted or when each sector's capital is "
        "adjusted. We find for both forms of adjustments costs that the "
        "steady state is determinate for all empirically plausible parameter "
        "values. We also find that determinacy occurs for a much larger range "
        "of parameter values when adjusting each sector's capital is costly."
    ),
    "herrendorf-valentinyi-2005-joeda": (
        "This paper explores the local stability properties of the steady "
        "state in the two-sector neoclassical growth model with sector-"
        "specific externalities. We show analytically that capital adjustment "
        "costs of any size preclude local indeterminacy nearby the steady "
        "state for every empirically plausible specification of the model "
        "parameters. More specifically, we show that when capital adjustment "
        "costs of any size are considered, a necessary condition for local "
        "indeterminacy is an upward-sloping labour demand curve in the "
        "capital-producing sector, which in turn requires an implausibly "
        "strong externality. We show numerically that capital adjustment "
        "costs of plausible size imply determinacy nearby the steady state "
        "for empirically plausible specifications of the other model "
        "parameters. These findings contrast sharply with the previous "
        "finding that local indeterminacy occurs in the two-sector model "
        "for a wide range of plausible parameter values when capital "
        "adjustment costs are abstracted from."
    ),
    "luintel-matthews-et-al-2020-em": (
        "China's development policy since 1978 has differed across regions. "
        "With rapid aggregate growth has come widening regional inequality. "
        "The fiscal decentralisation reforms in 1994 shifted political "
        "pressure onto provincial officials to boost local growth through "
        "local public investments. These investments affect regional "
        "convergence by counteracting regulatory frictions in factor "
        "accumulation, and can also determine steady-state growth. However, "
        "the effect of public spending allocations across physical and human "
        "capital on growth and convergence processes is empirically "
        "unexplored for Chinese provinces. We take provincial time-series "
        "data on public spending by category, finding local public spending "
        "and its components augment convergence rates differently across "
        "regions. Spending on education and health contributes significantly "
        "more to growth and convergence than capital spending, confirming "
        "that the public capital-spending bias is not a local growth-"
        "optimising strategy. We suggest a policy of aligning local "
        "government promotion incentives to human capital targets to "
        "correct local resource misallocation."
    ),
    "valentinyi-herrendorf-2008-roed": (
        "Many applications in economics use multi-sector versions of the "
        "growth model. In this paper, we measure the income shares of "
        "capital and labor at the sectoral level for the U.S. economy. We "
        "also decompose the capital shares into the income shares of land, "
        "structures, and equipment. We find that the capital shares differ "
        "across sectors. For example, the capital share of agriculture is "
        "more than two times that of construction and more than 50% larger "
        "than that of the aggregate economy. Moreover, agriculture has by "
        "far the largest land share, which mostly explains why it has the "
        "largest capital share. Our numbers can directly be used to "
        "calibrate standard multi-sector models. Alternatively, if one wants "
        "to abstract from differences in sector capital shares, our numbers "
        "can be used to establish that this is not crucial for the results."
    ),
}
for slug, abstract in ABSTRACTS.items():
    p = load(slug)
    p["abstract"] = abstract
    save(slug, p)
print(f"abstracts set on {len(ABSTRACTS)} Valentinyi papers")
