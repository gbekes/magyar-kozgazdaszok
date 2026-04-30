"""Set abstracts on 3 of 5 Ábrahám papers (2 are short comments/prefaces)."""
import json
from pathlib import Path

PAPERS = Path(__file__).resolve().parent.parent / "data" / "papers"


def load(slug):
    return json.loads((PAPERS / f"{slug}.json").read_text(encoding="utf-8"))


def save(slug, data):
    (PAPERS / f"{slug}.json").write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


# Year fix: abraham-carceles-poveda-2009-jet is JET vol 145, 2010 print
META = {
    "abraham-carceles-poveda-2009-jet": {
        "year": 2010, "volume": "145", "issue": "3", "pages": "974-1004",
    },
}
for slug, fields in META.items():
    p = load(slug)
    for k, v in fields.items():
        p[k] = v
    save(slug, p)
    print(f"metadata fix: {slug}")

ABSTRACTS = {
    "abraham-carceles-poveda-2009-jet": (
        "This paper endogenizes the borrowing constraints on capital in a "
        "production economy with incomplete markets. We find that these "
        "limits get looser with income, a property that is consistent with "
        "US data on credit limits. The framework with endogenous limits is "
        "then used to study the effects of a revenue neutral tax reform "
        "that eliminates capital income taxes. Our results illustrate that "
        "it is very important to take into account the effects of tax "
        "policies on the limits. Throughout the transition, these effects "
        "can be big enough to change the overall conclusion about the "
        "desirability of a tax reform."
    ),
    "abraham-koehne-et-al-2011-jet": (
        "We provide sufficient conditions for the validity of the first-order "
        "approach for two-period dynamic moral hazard problems where the "
        "agent can save and borrow secretly. The first-order approach is "
        "valid if the following conditions hold: (i) the agent has "
        "non-increasing absolute risk aversion utility (NIARA), (ii) the "
        "output technology has monotone likelihood ratios (MLR), and (iii) "
        "the distribution function of output is log-convex in effort (LCDF). "
        "Moreover, under these three conditions, the optimal contract is "
        "monotone in output. We also investigate a few possibilities of "
        "relaxing these requirements."
    ),
    "abraham-pavoni-2008-roed": (
        "We propose a tractable recursive framework to study the optimal "
        "allocation of consumption and effort in a dynamic setting with "
        "moral hazard where agents have secret access to the credit market "
        "or to storage. The recursive structure is based on a generalized "
        "first order approach, whose validity must be verified ex-post. "
        "Thanks to the recursive formulation of the optimal contract, the "
        "verification procedure turns out to be numerically parsimonious "
        "as it can be performed using standard dynamic programming "
        "techniques with only one endogenous state variable: the agent's "
        "level of assets. We study the performance of our ex-post "
        "verification test in practice by solving numerically three "
        "representative infinite horizon examples."
    ),
}
for slug, abstract in ABSTRACTS.items():
    p = load(slug)
    p["abstract"] = abstract
    save(slug, p)
print(f"abstracts set on {len(ABSTRACTS)} Abraham papers")
