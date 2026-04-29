"""Set abstracts on 2 Eső papers that have public abstracts."""
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
    "chung-eso-2013-el": (
        "We model countersignaling (i.e., very high types refraining from "
        "signaling) arising from the tradeoff between persuasion and learning "
        "in a signaling game. We assume that the agent has imperfect private "
        "information regarding his/her productivity, which the signaling "
        "action provides additional verifiable information about. A "
        "higher-type agent benefits more from providing such objective, "
        "albeit imprecise, \u201cproof\u201d for the market, but may also gain less "
        "from learning about his/her productivity. When the latter effect "
        "dominates the former for the very high types, the equilibrium "
        "exhibits countersignaling: very high and low types pool on "
        "refraining from signaling, and only the medium types signal. Under "
        "certain conditions, the countersignaling equilibrium is the unique "
        "pure-strategy perfect sequential equilibrium."
    ),
    "eso-galambos-2012-ijogt": (
        "We expand Crawford and Sobel's (Econometrica 50(6):1431\u20131451, 1982) "
        "model of information transmission to allow for the costly provision "
        "of 'hard evidence' in addition to conventional cheap talk. Under "
        "mild assumptions we prove that equilibria have an interval-partition "
        "structure, where types of the Sender belonging to the same interval "
        "either all induce the same action through cheap talk or reveal "
        "their types through hard evidence. We also show that the "
        "availability of costly hard signals may reverse one of the important "
        "implications of the classical cheap talk model, namely, that "
        "diverging preferences always lead to less communication."
    ),
}
for slug, abstract in ABSTRACTS.items():
    p = load(slug)
    p["abstract"] = abstract
    save(slug, p)
print(f"abstracts set on {len(ABSTRACTS)} Eso papers")
