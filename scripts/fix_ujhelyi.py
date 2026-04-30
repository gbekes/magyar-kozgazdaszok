"""Fix year metadata + populate missing verbatim abstracts on Gergely Ujhelyi's
14 catalogued papers. All titles verified against IDEAS author profile puj2.

Year fixes (slug names left unchanged — they are stable identifiers):
- forand-ujhelyi-et-al-2022-jeea: 2022 -> 2023 (per IDEAS)
- juhn-ujhelyi-et-al-2013-jde:    2013 -> 2014 (per IDEAS)
- ujhelyi-2008-jpube:             2008 -> 2009 (per IDEAS)
- ujhelyi-chatterjee-et-al-2020-jeea: 2020 -> 2021 (per IDEAS)

Already-existing abstracts (donchev, forand-2021, forand-jeea-2023, juhn-aer-2013,
ujhelyi-chatterjee-2021, ujhelyi-2017-ks) left as-is.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAPERS = ROOT / "data" / "papers"


def load(slug):
    return json.loads((PAPERS / f"{slug}.json").read_text(encoding="utf-8"))


def save(slug, data):
    (PAPERS / f"{slug}.json").write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


YEAR_FIXES = {
    "forand-ujhelyi-et-al-2022-jeea": 2023,
    "juhn-ujhelyi-et-al-2013-jde": 2014,
    "ujhelyi-2008-jpube": 2009,
    "ujhelyi-chatterjee-et-al-2020-jeea": 2021,
}
for slug, year in YEAR_FIXES.items():
    p = load(slug)
    p["year"] = year
    save(slug, p)
    print(f"year fix: {slug} -> {year}")

ABSTRACTS = {
    "bostashvili-ujhelyi-2019-jpube": (
        "We study political budget cycles in infrastructure spending that are "
        "conditional on bureaucratic organization. Bureaucrats can facilitate or "
        "hinder politicians' ability to engage in voter-friendly spending around "
        "elections. To test this idea, we use civil service reforms undertaken by "
        "US states in the second half of the 20th century to study political "
        "budget cycles in highway spending under civil service and patronage. We "
        "find that under patronage, highway spending is 12% higher in election "
        "years and 9% higher in the year before an election. By contrast, under "
        "civil service highway spending is essentially smooth over the electoral "
        "cycle. These findings provide a novel way through which civil service "
        "rules can stabilize government activity."
    ),
    "glaeser-ujhelyi-2010-jpube": (
        "Governments have responded to misleading advertising by banning it, "
        "engaging in counter-advertising and taxing and regulating the product. "
        "In this paper, we consider the welfare effects of those different "
        "responses to misinformation. While misinformation lowers consumer "
        "surplus, its effect on social welfare is ambiguous. Misleading "
        "advertising leads to over-consumption but that may be offsetting the "
        "underconsumption associated with oligopoly outputs. If all advertising "
        "is misinformation then a tax or quantity restriction on advertising "
        "maximizes welfare, and other policy interventions are inferior. If "
        "firms undertake quality improving investments that are complementary "
        "to misinformation, then combining taxes or bans on misleading "
        "advertising with other policies can increase welfare."
    ),
    "juhn-ujhelyi-et-al-2013-jde": (
        "This paper studies the effect of trade liberalization on an "
        "under-explored aspect of wage inequality \u2014 gender inequality. We "
        "consider a model where firms differ in their productivity and workers "
        "are differentiated by skill as well as gender. A reduction in tariffs "
        "induces more productive firms to modernize their technology and enter "
        "the export market. New technologies involve computerized production "
        "processes and lower the need for physically demanding skills. As a "
        "result, the relative wage and employment of women improves in "
        "blue-collar tasks, but not in white-collar tasks. We test our model "
        "using a panel of establishment level data from Mexico exploiting "
        "tariff reductions associated with the North American Free Trade "
        "Agreement (NAFTA). Consistent with our theory we find that tariff "
        "reductions caused new firms to enter the export market, update their "
        "technology and replace male blue-collar workers with female "
        "blue-collar workers."
    ),
    "szabo-ujhelyi-2015-jde": (
        "Nonpayment for public utilities is an important constraint to expanding "
        "service access in developing countries. What are the causes of "
        "nonpayment and which policies are effective at addressing them? To "
        "study these questions, we implement and evaluate a randomized water "
        "education campaign in a low income peri-urban area in South Africa. We "
        "estimate substantial short-run treatment effects: on the order of a 25% "
        "increase in payments over a three-month period after which the effect "
        "dissipates. The evidence shows that the treatment did not operate by "
        "increasing consumers' information, or by creating reminders to pay or "
        "a threat of enforcement. Instead, households may have reciprocated the "
        "provider's efforts by paying more. Our findings provide evidence that "
        "strategies other than increased enforcement can lower nonpayment."
    ),
    "szabo-ujhelyi-2017-el": (
        "To study the usefulness of subjective well-being measures as a proxy "
        "for utility, Benjamin et al. (2012) ask whether people choose what "
        "makes them happy in US samples. We use their methodology in a sample "
        "from low-income South African townships. Here respondents almost "
        "always choose what makes them feel happy. In addition, they perceive "
        "little conflict between own happiness and other relevant determinants "
        "of choice such as sense of purpose and family happiness."
    ),
    "szabo-ujhelyi-2024-jpube": (
        "This paper studies the economic effects of the US National Park "
        "System, the largest national conservation entity in the world. We "
        "assemble a new dataset on the history of the system, and show that "
        "parks increase overall employment and income in the local economy. "
        "The data allows us to study several specific mechanisms. Economic "
        "effects appear to be driven by visitors, and they cannot be explained "
        "by direct government spending on park budgets or by various "
        "substitution effects. Our findings provide evidence relevant to "
        "conservation policy in the US and elsewhere."
    ),
    "ujhelyi-2008-jpube": (
        "Regulatory caps on contributions to political campaigns are the "
        "cornerstones of campaign finance legislation in many established "
        "democracies, and their introduction is considered by most emerging "
        "ones. Are these regulations desirable? This paper studies "
        "contribution caps in a menu auction lobbying model with limited "
        "budgets and costly entry. In the absence of entry, contribution caps "
        "improve welfare by \u201cleveling the political playing field\u201d. With "
        "entry, however, a competition effect and a bargaining effect may "
        "arise, resulting in inefficient entry and exit decisions. In "
        "particular, a cap may lead to worse policies than the status quo; and "
        "even if better policies are chosen, the resulting gain in welfare may "
        "be more than offset by the entry costs. Regulation can also lead to "
        "the simultaneous entry of competing groups, creating costly "
        "rent-seeking on issues previously unaffected by lobbying."
    ),
    "ujhelyi-2014-jpube": (
        "Civil service rules governing the selection and motivation of "
        "bureaucrats are among the defining institutions of modern democracies. "
        "Although this is an active area of reform in the US and elsewhere, "
        "economic analyses of the issue are virtually nonexistent. This paper "
        "provides a welfare evaluation of civil service reform. It describes "
        "the effect of reform on the interaction of politicians, voters, and "
        "bureaucrats, and shows that society often faces trade-offs between "
        "improving the bureaucracy and improving the performance of politicians. "
        "My results characterize the conditions under which merit-based "
        "recruitment and civil service protections such as tenure can improve "
        "welfare."
    ),
}
for slug, abstract in ABSTRACTS.items():
    p = load(slug)
    p["abstract"] = abstract
    save(slug, p)
print(f"abstracts set on {len(ABSTRACTS)} Ujhelyi papers")
