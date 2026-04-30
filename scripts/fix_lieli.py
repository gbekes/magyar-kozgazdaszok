"""Verify, fix, and set abstracts on Lieli Róbert's 7 catalogued papers.

Verified each stub against IDEAS author profile pli759. All titles and
coauthors match canonical sources. Five stubs need year fixes (slug-year
reflected manuscript/online date but print-publication year differs):

- lieli-nieto-barthaburu-2009-jbes: 2009 -> 2010
- lieli-nieto-barthaburu-2019-jeea: 2019 -> 2020
- lieli-springborn-2012-restat:    2012 -> 2013
- lieli-stinchcombe-2012-et:       2012 -> 2013
- lieli-white-2009-joem:           2009 -> 2010

Slug names left unchanged as stable identifiers. Volume/issue/pages added.
Verbatim publisher abstracts populated for the 4 papers that lacked them.
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
    "lieli-nieto-barthaburu-2009-jbes": {
        "year": 2010, "volume": "28", "issue": "2", "pages": "308-319",
    },
    "lieli-nieto-barthaburu-2019-jeea": {
        "year": 2020, "volume": "18", "issue": "3", "pages": "1521-1552",
    },
    "lieli-springborn-2012-restat": {
        "year": 2013, "volume": "95", "issue": "2", "pages": "632-645",
    },
    "lieli-stinchcombe-2012-et": {
        "year": 2013, "volume": "29", "issue": "3", "pages": "517-544",
    },
    "lieli-white-2009-joem": {
        "year": 2010, "volume": "157", "issue": "1", "pages": "110-119",
    },
    "lieli-stinchcombe-et-al-2019-ijof": {
        "volume": "35", "issue": "3", "pages": "878-890",
    },
    "lieli-hsu-et-al-2022-asita": {
        "pages": "79-109", "doi": "10.1007/978-3-031-15149-1_3",
        "url_published": "https://doi.org/10.1007/978-3-031-15149-1_3",
    },
}
for slug, fields in META.items():
    p = load(slug)
    for k, v in fields.items():
        p[k] = v
    save(slug, p)
    print(f"metadata fix: {slug}")

ABSTRACTS = {
    "lieli-stinchcombe-et-al-2019-ijof": (
        "The property that the conditional mean is the unrestricted optimal "
        "forecast characterizes the Bregman class of loss functions, while the "
        "property that the \u03b1-quantile is the unrestricted optimal forecast "
        "characterizes the generalized \u03b1-piecewise linear (\u03b1-GPL) "
        "class. However, in settings where the forecaster's choice of "
        "forecasts is limited to the support of the predictive distribution, "
        "different Bregman losses lead to different forecasts. This is not "
        "true for the \u03b1-GPL class: the failure of identification is more "
        "fundamental. We state simple conditions that can be used to ascertain "
        "whether loss functions that are consistent for the same statistical "
        "functional become identifiable when off-support forecasts are "
        "disallowed. We also study the identifying power of unrestricted "
        "forecasts within the class of smooth, convex loss functions. For any "
        "such loss \u2113, the set of losses that are consistent for the same "
        "statistical functional as \u2113 is a tiny subset of this class in a "
        "precise mathematical sense."
    ),
    "lieli-white-2009-joem": (
        "We examine the econometric implications of the decision problem "
        "faced by a profit/utility-maximizing lender operating in a simple "
        "\u201cdouble-binary\u201d environment, where the two actions available "
        "are \u201capprove\u201d or \u201creject\u201d, and the two states of the "
        "world are \u201cpay back\u201d or \u201cdefault\u201d. In practice, such "
        "decisions are often made by applying a fixed cutoff to the maximum "
        "likelihood estimate of a parametric model of the default probability. "
        "Following Elliott and Lieli (2007), we argue that this practice might "
        "contradict the lender's economic objective and, using German loan "
        "data, we illustrate the use of \u201ccontext-specific\u201d cutoffs and "
        "an estimation method derived directly from the lender's problem. We "
        "also provide a brief discussion of how to incorporate legal "
        "constraints, such as the prohibition of disparate treatment of "
        "potential borrowers, into the lender's problem."
    ),
    "lieli-hsu-et-al-2022-asita": (
        "Treatment effect estimation from observational data relies on "
        "auxiliary prediction exercises. This chapter presents recent "
        "developments in the econometrics literature showing that machine "
        "learning methods can be fruitfully applied for this purpose. The "
        "double machine learning (DML) approach is concerned primarily with "
        "selecting the relevant control variables and functional forms "
        "necessary for the consistent estimation of an average treatment "
        "effect. We explain why the use of orthogonal moment conditions is "
        "crucial in this setting. Another, somewhat distinct, strand of the "
        "literature focuses on treatment effect heterogeneity through the "
        "discovery of the conditional average treatment effect (CATE) "
        "function. Here we distinguish between methods aimed at estimating the "
        "entire function and those that project it on a pre-specified "
        "coordinate."
    ),
}
for slug, abstract in ABSTRACTS.items():
    p = load(slug)
    p["abstract"] = abstract
    save(slug, p)
print(f"abstracts set on {len(ABSTRACTS)} Lieli papers")
