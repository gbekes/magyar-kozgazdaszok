"""Set abstracts on Csercsik (4), Bakó (2), Bencsik (2)."""
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
    "csercsik-2016-nse": {
        "volume": "16", "issue": "4", "pages": "1043-1073",
        "doi": "10.1007/s11067-015-9310-x",
    },
    "csercsik-habis-2015-nse": {
        "volume": "15", "issue": "1", "pages": "1-16",
        "doi": "10.1007/s11067-014-9265-3",
    },
    "csercsik-koczy-2017-nse": {
        "volume": "17", "issue": "4", "pages": "1161-1184",
        "doi": "10.1007/s11067-017-9363-0",
    },
    "bako-kalecz-simon-2012-eclett": {
        "volume": "116", "issue": "3", "pages": "301-303",
    },
    "bako-kalecz-simon-2013-eclett": {
        "volume": "119", "issue": "3", "pages": "316-320",
    },
    "bencsik-chuluun-2019-sbe": {
        "year": 2021, "volume": "56", "issue": "1", "pages": "355-384",
    },
    "bencsik-budhiraja-2025-joebo": {
        "volume": "238", "pages": "107202",
    },
}
for slug, fields in META.items():
    p = load(slug)
    for k, v in fields.items():
        p[k] = v
    save(slug, p)
    print(f"metadata fix: {slug}")

ABSTRACTS = {
    "csercsik-hubert-et-al-2019-enerecon": (
        "Existing cooperative game theoretic studies of bargaining power in "
        "gas pipeline systems are based on the so called characteristic "
        "function form (CFF). This approach is potentially misleading if "
        "some pipelines fall under regulated third party access (TPA). TPA, "
        "which is by now the norm in the EU, obliges the owner of a "
        "pipeline to transport gas for others, provided they pay a "
        "regulated transport fee. From a game theoretic perspective, this "
        "institutional setting creates so called \u201cexternalities\u201d, "
        "the description of which requires partition function form (PFF) "
        "games. In this paper we propose a method to compute payoffs, "
        "reflecting the power structure, for a pipeline system with "
        "regulated TPA. The method is based on an iterative flow mechanism "
        "to determine gas flows and transport fees for individual players "
        "and uses the recursive core and the minimal claim function to "
        "convert the PPF game back into a CFF game, which can be solved by "
        "standard methods. We illustrate the approach with a simple "
        "stylized numerical example of the gas network in Central Eastern "
        "Europe with a focus on Ukraine's power index as a major transit "
        "country."
    ),
    "csercsik-2016-nse": (
        "A cooperative game-theoretic framework is introduced to study the "
        "behavior of cooperating and competing electrical-energy providers "
        "in the wholesale market considering price-preference rational "
        "consumers. The paper studies the physical and economic aspects of "
        "the power transmission system operation focusing on the "
        "incentives for group formation, analyzing the interactions of "
        "generators in an idealized environment described by a DC load "
        "flow model where the network is lossless and is operated by an "
        "independent network operator who ensures network stability and "
        "fulfillment of consumption needs while taking into account the "
        "preferences of consumers over generators."
    ),
    "csercsik-habis-2015-nse": (
        "We introduce a new solution concept to problems with externalities, "
        "which is the first in the literature to take into account "
        "economic, regulatory and physical stability aspects of network "
        "problems in the very same model. A new class of cooperative games "
        "is defined where the worth of a coalition depends on the behavior "
        "of other players and on the state of nature as well. We allow for "
        "coalitions to form both before and after the resolution of "
        "uncertainty, hence agreements must be stable against both types "
        "of deviations. The appropriate extension of the classical core "
        "concept, the Sustainable Core, is defined for this new setup to "
        "test the stability of allocations in such a complex environment. "
        "A prominent application, a game of consumers and generators on "
        "an electrical energy transmission network is examined in details, "
        "where the power in- and outlets of the nodes have to be "
        "determined in a way, that if any line instantaneously fails, "
        "none of the remaining lines may be overloaded."
    ),
    "csercsik-koczy-2017-nse": (
        "The users of electricity networks are organized into groups where "
        "the production and consumption of electricity is in balance. The "
        "study examines the formation of these balancing groups using a "
        "cooperative game in partition function form defined over an ideal "
        "(lossless) DC load flow model of the power grid. The games "
        "contain widespread externalities that can be both negative and "
        "positive. The stability of certain partitions is studied using "
        "the concept of the recursive core. While the game is clearly "
        "cohesive, it is not necessarily superadditive, and subadditivity "
        "may be a barrier to achieve full cooperation."
    ),
    "bako-kalecz-simon-2012-eclett": (
        "In this article we examine the effects of third degree price "
        "discrimination in asymmetric Cournot oligopolies. We show that "
        "the average price is not affected by the extent of price "
        "discrimination. We find that the asymmetry between firms is "
        "reflected only by the output produced for the lowest-valuation "
        "consumers and firms produce equal quantities to the other "
        "consumer groups."
    ),
    "bako-kalecz-simon-2013-eclett": (
        "Theoretical articles on incentive systems almost exclusively "
        "focus on linear compensations, while, in practice, nonlinear "
        "elements, such as quota bonuses, are not uncommon. Our article "
        "tries to bridge that gap; it shows how the use of quotas can "
        "increase the owners' profits, which agents are targeted by these "
        "incentives, and which factors determine the optimal bonus."
    ),
    "bencsik-chuluun-2019-sbe": (
        "Drawing upon the job demand-control model and analyzing more than "
        "600,000 responses from the nationally representative Gallup "
        "survey data over the 2010\u20132016 period, we find that "
        "self-employed individuals in the USA report lower life "
        "satisfaction than paid employees (i.e., evaluative well-being). "
        "The self-employed also experience both positive feelings such as "
        "happiness and enjoyment and negative feelings such as anger and "
        "stress more than their wage-earning peers, leading to a stark "
        "emotional dichotomy in how they experience their daily lives "
        "(i.e., hedonic well-being) consistent with both high job control "
        "and high job demand that are prevalent in self-employment. "
        "Lastly, the self-employed also report more health problems and "
        "lower physical well-being. Income (and low local unemployment to "
        "some extent) successfully mitigates the negative effects of "
        "self-employment on subjective well-being while enhancing the "
        "positive, but education does not do so. Overall, the results "
        "suggest that self-employment is associated with predominantly "
        "negative well-being effects in the USA."
    ),
    "bencsik-budhiraja-2025-joebo": (
        "Drug crimes continue to make up a large share of the offenses for "
        "which individuals interact with the criminal justice system in "
        "the United States, with Black Americans arrested at four times "
        "the rate of white Americans despite similar drug usage rates. In "
        "recent years, policymakers in jurisdictions across the country "
        "have deregulated recreational cannabis use, often with the "
        "explicit intention of reducing drug crime arrest disparities. Yet, "
        "causal evidence about the impact of deregulation on who police "
        "arrest is limited. In this paper, we exploit the rollout of the "
        "most widespread deregulatory approach related to recreational "
        "cannabis use\u2014the decriminalization of cannabis possession\u2014"
        "across the three largest US cities, New York City, Los Angeles, "
        "and Chicago, using a difference-in-differences design. We find "
        "that decriminalization significantly reduced cannabis possession "
        "arrests. We observe that decriminalization narrowed racial "
        "disparities in arrests in Chicago by reducing small quantity "
        "possession arrests for Black individuals and in Los Angeles by "
        "reducing large quantity possession arrests for both Black and "
        "Hispanic residents. Lastly, we extend our analysis to "
        "legalization of recreational cannabis use and observe that "
        "legalization decreased arrests for every racial and ethnic group "
        "we consider, with similarly large impacts across groups."
    ),
}
for slug, abstract in ABSTRACTS.items():
    p = load(slug)
    p["abstract"] = abstract
    save(slug, p)
print(f"abstracts set on {len(ABSTRACTS)} papers")
