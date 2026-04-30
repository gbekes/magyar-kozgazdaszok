"""Verify, fix, and set abstracts on Kiss Hubert's 9 catalogued papers.

Verified each stub against IDEAS author profile pki288. All 9 titles match
canonical sources. Three need year fixes (slug-year reflects manuscript date
but print-publication year differs):

- kiss-rodriguez-lara-et-al-2015-jbee:    2015 -> 2016 (JBEE vol 64, 2016)
- kiss-rodriguez-lara-et-al-2017-eclett:  2017 -> 2018 (EconLet vol 162, 2018)
- kiss-selei-2017-edec:                   2017 -> 2018 (EduEcon vol 26(2), 2018)

The kiss-rodriguez-lara-et-al-2016-expecon paper is actually a chapter in the
Palgrave book "Experimental Economics" (Branas-Garza & Cabrales eds., 2016),
NOT a journal article in the Springer journal "Experimental Economics".
Journal field updated to clarify book context.

Slug names left as stable identifiers. Verbatim publisher abstracts populated
for the 3 papers that lacked them.
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
    "kiss-rodriguez-lara-et-al-2014-jbee": {
        "volume": "52", "pages": "40-51",
        "doi": "10.1016/j.socec.2014.06.003",
    },
    "kiss-rodriguez-lara-et-al-2014-joebo": {
        "volume": "101", "pages": "87-99",
        "doi": "10.1016/j.jebo.2014.01.019",
    },
    "kiss-rodriguez-lara-et-al-2015-jbee": {
        "year": 2016, "volume": "64", "pages": "12-19",
        "doi": "10.1016/j.socec.2016.04.001",
    },
    "kiss-rodriguez-lara-et-al-2017-eclett": {
        "year": 2018, "volume": "162", "pages": "146-149",
        "doi": "10.1016/j.econlet.2017.11.014",
    },
    "kiss-selei-2017-edec": {
        "year": 2018, "volume": "26", "issue": "2", "pages": "179-193",
        "doi": "10.1080/09645292.2017.1399359",
    },
    "kiss-rodriguez-lara-et-al-2016-expecon": {
        "journal": "Experimental Economics (Palgrave book chapter)",
        "publication_type": "book-chapter",
        "doi": "10.1057/9781137538161_5",
    },
}
for slug, fields in META.items():
    p = load(slug)
    for k, v in fields.items():
        p[k] = v
    save(slug, p)
    print(f"metadata fix: {slug}")

ABSTRACTS = {
    "kiss-rodriguez-lara-et-al-2014-jbee": (
        "We report experimental evidence on gender differences in financial "
        "decision-making that involves three depositors choosing whether to "
        "keep their money deposited or to withdraw it. We find that one's "
        "position in the line, the fact that one is being observed and "
        "observed decisions are key determinants in explaining the subjects' "
        "behavior. Our main result is that men and women do not react "
        "differently to what is observed. However, there are gender "
        "differences regarding the effect of being observed: women value the "
        "fact of being observed more, while men value the number of "
        "subsequent depositors who observe them. Interestingly, risk "
        "aversion has no predictive power on depositors' behavior."
    ),
    "kiss-rodriguez-lara-et-al-2014-joebo": (
        "We report experimental evidence on the effect of observability of "
        "actions on bank runs. We model depositors' decision-making in a "
        "sequential framework, with three depositors located at the nodes of "
        "a network. Depositors observe the other depositors' actions only if "
        "connected by the network. Theoretically, a sufficient condition to "
        "prevent bank runs is that the second depositor to act is able to "
        "observe the first one's action (no matter what is observed). "
        "Experimentally, we find that observability of actions affects the "
        "likelihood of bank runs, but depositors' choice is highly influenced "
        "by the particular action that is being observed. Depositors who are "
        "observed by others at the beginning of the line are more likely to "
        "keep their money deposited, leading to less bank runs. When "
        "withdrawals are observed, bank runs are more likely even when the "
        "mere observation of actions should prevent them."
    ),
    "kiss-rodriguez-lara-et-al-2015-jbee": (
        "We assess the effect of cognitive abilities on withdrawal decisions "
        "in a bank-run game. In our setup, depositors choose sequentially "
        "between withdrawing or keeping their funds deposited in a common "
        "bank. Depositors may observe previous decisions depending on the "
        "information structure. Theoretically, the last depositor in the "
        "sequence of decisions has a dominant strategy and should always "
        "keep the funds deposited, regardless of what she observes (if "
        "anything). Recognizing the dominant strategy, however, is not "
        "always straightforward. If there exists strategic uncertainty "
        "(e.g., if the last depositor has no information regarding the "
        "decisions of predecessors), then the identification of the "
        "dominant strategy is more difficult than in a situation with no "
        "strategic uncertainty. We find that cognitive abilities, as "
        "measured by the Cognitive Reflection Test (CRT), predict "
        "withdrawals in the presence of strategic uncertainty (participants "
        "with stronger abilities tend to identify the dominant strategy "
        "more easily) but that the CRT does not predict behavior when "
        "strategic uncertainty is absent."
    ),
}
for slug, abstract in ABSTRACTS.items():
    p = load(slug)
    p["abstract"] = abstract
    save(slug, p)
print(f"abstracts set on {len(ABSTRACTS)} Kiss-Hubert papers")
