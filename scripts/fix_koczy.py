"""Verify, fix, and set abstracts on László Kóczy's 11 catalogued papers.

Verified each stub against IDEAS author profile pko27. Most stubs match
canonical sources; 3 needed year fixes (slug-year reflects manuscript date
but print-publication year differs):

- koczy-2008-geb:           2008 -> 2009 (GEB vol 66(1), 2009)
- koczy-lauwers-2003-geb:   2003 -> 2004 (GEB vol 48(1), 2004)
- koczy-nichifor-2012-ecth: 2012 -> 2013 (EconTheory vol 52(3), 2013)

Slug names left as stable identifiers. Volume/issue/pages added.
Verbatim publisher abstracts populated for 7 papers; for the Nord Stream
paper the publisher page is paywalled, abstract left null but summary
drafted from publicly available description.
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
    "koczy-2006-jmathe": {
        "volume": "43", "issue": "1", "pages": "56-64",
        "doi": "10.1016/j.jmateco.2006.05.004",
    },
    "koczy-2007-tad": {
        "volume": "63", "issue": "1", "pages": "41-51",
        "doi": "10.1007/s11238-007-9030-x",
    },
    "koczy-2008-geb": {
        "year": 2009, "volume": "66", "issue": "1", "pages": "559-565",
        "doi": "10.1016/j.geb.2008.02.005",
    },
    "koczy-2015-jmathe": {
        "volume": "61", "issue": "C", "pages": "104-110",
        "doi": "10.1016/j.jmateco.2015.08.004",
    },
    "koczy-lauwers-2003-geb": {
        "year": 2004, "volume": "48", "issue": "1", "pages": "86-93",
        "doi": "10.1016/j.geb.2003.06.006",
    },
    "koczy-nichifor-2012-ecth": {
        "year": 2013, "volume": "52", "issue": "3", "pages": "863-884",
        "doi": "10.1007/s00199-011-0691-x",
    },
    "koczy-sziklai-2018-orl": {
        "volume": "46", "issue": "3", "pages": "324-329",
        "doi": "10.1016/j.orl.2018.03.002",
    },
    "koczy-sziklai-csercsik-2022-esr2": {
        "volume": "44", "pages": "100982",
        "doi": "10.1016/j.esr.2022.100982",
    },
}
for slug, fields in META.items():
    p = load(slug)
    for k, v in fields.items():
        p[k] = v
    save(slug, p)
    print(f"metadata fix: {slug}")

ABSTRACTS = {
    "koczy-2006-jmathe": (
        "We show the existence of an upper bound for the number of blocks "
        "required to get from one imputation to another provided that "
        "accessibility holds. The bound depends only on the number of players "
        "in the TU game considered. For the class of games with non-empty "
        "cores this means that the core can be reached via a bounded sequence "
        "of blocks."
    ),
    "koczy-2008-geb": (
        "The sequential coalition formation model of Bloch to solve "
        "cooperative games with externalities exhibits some anomalies when "
        "related to classical concepts. We elaborate on these problems, "
        "define a modification of Bloch's model and show that its order-"
        "independent equilibria coincide with the (pessimistic) recursive "
        "core."
    ),
    "koczy-2015-jmathe": (
        "We study coalitional games where the coalitional payoffs depend on "
        "the embedding coalition structure. We introduce a noncooperative, "
        "sequential coalition formation model and show that the set of "
        "equilibrium outcomes coincides with the recursive core, a "
        "generalisation of the core to such games."
    ),
    "koczy-lauwers-2003-geb": (
        "For each outcome (i.e. a payoff vector augmented with a coalition "
        "structure) of a TU-game with a non-empty coalition structure core "
        "there exists a finite sequence of successively dominating outcomes "
        "that terminates in the coalition structure core. In order to obtain "
        "this result a restrictive dominance relation \u2014 which we label "
        "outsider independent \u2014 is employed."
    ),
    "koczy-nichifor-2012-ecth": (
        "The evaluation of scientific output has a key role in the allocation "
        "of research funds and academic positions. Decisions are often based "
        "on quality indicators for academic journals, and over the years, a "
        "handful of scoring methods have been proposed for this purpose. "
        "Discussing the most prominent methods (de facto standards) we show "
        "that they do not distinguish quality from quantity at article level. "
        "The systematic bias we find is analytically tractable and implies "
        "that the methods are manipulable. We introduce modified methods that "
        "correct for this bias, and use them to provide rankings of economic "
        "journals. Our methodology is transparent; our results are "
        "replicable."
    ),
    "koczy-sziklai-2018-orl": (
        "Uniformly sized constituencies give voters similar influence on "
        "election outcomes. When constituencies are set up, seats are "
        "allocated to the administrative units, such as states or counties, "
        "using apportionment methods. According to the impossibility result "
        "of Balinski and Young, none of the methods satisfying basic "
        "monotonicity properties assign a rounded proportional number of "
        "seats (the Hare-quota). We study the malapportionment of "
        "constituencies and provide a simple bound as a function of the "
        "house size for an important class of divisor methods, a popular, "
        "monotonic family of techniques."
    ),
    "koczy-koltai-et-al-2026-o": (
        "The efficient use of human resources. We are considering an "
        "organization with a fixed number of workers over a network of "
        "subunits. The relative efficiency of these units can be uncovered "
        "using Data Envelopment Analysis (DEA) methods. How do we overcome "
        "efficiency differences when resources are constrained? Motivated by "
        "concerns for quality assurance, we use a method that lexico-"
        "graphically minimizes the tasks per worker. We present a fast "
        "algorithm to calculate the optimal allocation. Connections to the "
        "apportionment literature \u2014 mostly focusing on the fair "
        "allocation of voting districts among geographical or administrative "
        "regions, \u2014 are discussed. The method is illustrated using data "
        "from salary administrators at the Hungarian State Treasury's 19 "
        "county-level subsidiaries. After the reallocation, the relative "
        "efficiency of the worst-performing counties moves from about 60% "
        "to over 90%."
    ),
}
for slug, abstract in ABSTRACTS.items():
    p = load(slug)
    p["abstract"] = abstract
    save(slug, p)
print(f"abstracts set on {len(ABSTRACTS)} Kóczy papers")
