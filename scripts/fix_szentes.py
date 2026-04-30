"""Set abstracts on 4 of 6 Szentes papers (2 remain unavailable)."""
import json
from pathlib import Path

PAPERS = Path(__file__).resolve().parent.parent / "data" / "papers"


def load(slug):
    return json.loads((PAPERS / f"{slug}.json").read_text(encoding="utf-8"))


def save(slug, data):
    (PAPERS / f"{slug}.json").write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


# Year fix: doval-szentes-2024-gaeb is volume 150 (March 2025) per IDEAS
META = {
    "doval-szentes-2024-gaeb": {
        "year": 2025, "volume": "150", "pages": "106-130",
    },
    "gershkov-szentes-2008-jet": {
        "year": 2009, "volume": "144", "issue": "1", "pages": "36-68",
    },
    "szentes-2004-jet": {
        "year": 2005, "volume": "120", "issue": "2", "pages": "175-205",
    },
}
for slug, fields in META.items():
    p = load(slug)
    for k, v in fields.items():
        p[k] = v
    save(slug, p)
    print(f"metadata fix: {slug}")

ABSTRACTS = {
    "doval-szentes-2024-gaeb": (
        "We study a two-sided dynamic matching market where agents arrive "
        "randomly. An arriving agent is immediately matched if agents are "
        "waiting on the other side. Otherwise, the agent decides whether to "
        "exit the market or join a queue to wait for a match. Waiting is "
        "costly: agents discount the future and incur costs while they wait. "
        "We characterize the equilibrium and socially optimal queue sizes "
        "under first-come, first-served. Depending on the model parameters, "
        "equilibrium queues can be shorter or longer than efficiency would "
        "require them to be. Indeed, socially optimal queues may be "
        "unbounded, even if equilibrium queues are not. By contrast, when "
        "agents only incur flow costs while they wait, equilibrium queues "
        "are typically longer than socially optimal ones (cf. Baccara et "
        "al., 2020). Unlike one-sided markets, the comparison between "
        "equilibrium and socially optimal queues in two-sided markets "
        "depends on agents' time preferences."
    ),
    "garrett-georgiadis-et-al-2023-jet": (
        "This paper considers a moral hazard model with agent limited "
        "liability. Prior to interacting with the principal, the agent "
        "designs the production technology, which is a specification of his "
        "cost of generating each output distribution. After observing the "
        "production technology, the principal offers a payment scheme and "
        "then the agent chooses a distribution over outputs. We show that "
        "there is an optimal design involving only binary distributions "
        "(i.e., the cost of any other distribution is prohibitively high), "
        "and we characterize the equilibrium technology defined on the "
        "binary distributions. Notably, the equilibrium payoff of both "
        "players is 1/e."
    ),
    "gershkov-szentes-2008-jet": (
        "A group of individuals with identical preferences must make a "
        "decision under uncertainty about which decision is best. Before "
        "the decision is made, each agent can privately acquire a costly "
        "and imperfect signal. We discuss how to design a mechanism for "
        "eliciting and aggregating the collected information so as to "
        "maximize ex-ante social welfare. We first show that, of all "
        "mechanisms, a sequential one is optimal and works as follows. At "
        "random, one agent at a time is selected to acquire information and "
        "report the resulting signal. Agents are informed of neither their "
        "position in the sequence nor of other reports. Acquiring "
        "information when called upon and reporting truthfully is an "
        "equilibrium. We next characterize the ex-ante optimal scheme among "
        "all ex-post efficient mechanisms. In this mechanism, a decision is "
        "made when the precision of the posterior exceeds a cut-off that "
        "decreases with each additional report. The restriction to ex-post "
        "efficiency is shown to be without loss when the available signals "
        "are sufficiently imprecise. On the other hand, ex-post efficient "
        "mechanisms are shown to be suboptimal when the cost of information "
        "acquisition is sufficiently small."
    ),
    "robatto-szentes-2017-jet": (
        "This paper considers a continuous-time biological model in which "
        "the growth rate of a population is determined by the risk attitude "
        "of its individuals. We consider choices over lotteries which "
        "determine the number of offspring and involve both idiosyncratic "
        "and aggregate risks. We distinguish between two types of aggregate "
        "risk: environmental variations and natural disasters. Environmental "
        "variations influence the death and birth rates, while natural "
        "disasters result in instantaneous drops in population size."
    ),
}
for slug, abstract in ABSTRACTS.items():
    p = load(slug)
    p["abstract"] = abstract
    save(slug, p)
print(f"abstracts set on {len(ABSTRACTS)} Szentes papers")
