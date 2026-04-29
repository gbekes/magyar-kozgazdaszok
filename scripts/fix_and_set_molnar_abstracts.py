"""Fix 4 wrong-titled Molnár Krisztina stubs, then set verbatim abstracts on all 5.

The original metadata seeding fabricated coauthors and titles for several
of Molnár's papers. The canonical author profile (IDEAS pmo468 + her
NHH/personal site) lists the following peer-reviewed journal articles:

1. Molnár (single author), "Learning with Expert Advice", JEEA 2007.
2. Molnár & Santoro, "Optimal monetary policy when agents are learning", EER 2014.
3. Ormeño & Molnár, "Using Survey Data of Inflation Expectations...", JMCB 2015.
4. Attanasio, Kovács & Molnár, "Euler Equations, Subjective Expectations and
   Income Shocks", Economica 2020.
5. Mele, Molnár & Santoro, "On the perils of stabilizing prices when agents
   are learning", JoME 2020.

Three slugs need renaming because the coauthor list changes; the JEEA 2007
slug stays but its content is rewritten.
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


# 1. Fix solo-authored JEEA 2007 paper (slug stays, content rewritten)
slug = "molnar-kriszta-2007-jeea"
p = load(slug)
p["title"] = "Learning with Expert Advice"
p["authors"] = ["molnar-kriszta"]
p["volume"] = "5"
p["issue"] = "2-3"
p["pages"] = "420-432"
p["doi"] = "10.1162/jeea.2007.5.2-3.420"
p["url_published"] = "https://doi.org/10.1162/jeea.2007.5.2-3.420"
save(slug, p)
print(f"updated content: {slug}")

# 2. Fix Santoro coauthorship metadata (slug fine)
slug = "molnar-santoro-2014-eer"
p = load(slug)
p["authors"] = ["molnar-kriszta", "Sergio Santoro"]
p["volume"] = "66"
p["issue"] = "C"
p["pages"] = "39-62"
p["doi"] = "10.1016/j.euroecorev.2013.11.012"
p["url_published"] = "https://doi.org/10.1016/j.euroecorev.2013.11.012"
save(slug, p)

# 3. RENAME molnar-eusepi-preston-2015-jmcb -> ormeno-molnar-2015-jmcb
old = PAPERS / "molnar-eusepi-preston-2015-jmcb.json"
new = PAPERS / "ormeno-molnar-2015-jmcb.json"
if old.exists() and not new.exists():
    p = json.loads(old.read_text(encoding="utf-8"))
    p["id"] = "ormeno-molnar-2015-jmcb"
    p["title"] = "Using Survey Data of Inflation Expectations in the Estimation of Learning and Rational Expectations Models"
    p["authors"] = ["Arturo Ormeño", "molnar-kriszta"]
    p["volume"] = "47"
    p["issue"] = "4"
    p["pages"] = "673-699"
    p["doi"] = "10.1111/jmcb.12219"
    p["url_published"] = "https://doi.org/10.1111/jmcb.12219"
    new.write_text(json.dumps(p, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    old.unlink()
    print("renamed: molnar-eusepi-preston-2015-jmcb -> ormeno-molnar-2015-jmcb (was wrong coauthors+title)")

# 4. RENAME molnar-reppa-2020-economica -> attanasio-kovacs-molnar-2020-economica
old = PAPERS / "molnar-reppa-2020-economica.json"
new = PAPERS / "attanasio-kovacs-molnar-2020-economica.json"
if old.exists() and not new.exists():
    p = json.loads(old.read_text(encoding="utf-8"))
    p["id"] = "attanasio-kovacs-molnar-2020-economica"
    p["title"] = "Euler Equations, Subjective Expectations and Income Shocks"
    p["authors"] = ["Orazio Attanasio", "Agnes Kovács", "molnar-kriszta"]
    p["volume"] = "87"
    p["issue"] = "346"
    p["pages"] = "406-441"
    p["doi"] = "10.1111/ecca.12318"
    p["url_published"] = "https://doi.org/10.1111/ecca.12318"
    new.write_text(json.dumps(p, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    old.unlink()
    print("renamed: molnar-reppa-2020-economica -> attanasio-kovacs-molnar-2020-economica (was wrong coauthors+title)")

# 5. RENAME molnar-tortorice-2020-jome -> mele-molnar-santoro-2020-jome
old = PAPERS / "molnar-tortorice-2020-jome.json"
new = PAPERS / "mele-molnar-santoro-2020-jome.json"
if old.exists() and not new.exists():
    p = json.loads(old.read_text(encoding="utf-8"))
    p["id"] = "mele-molnar-santoro-2020-jome"
    p["title"] = "On the Perils of Stabilizing Prices when Agents are Learning"
    p["authors"] = ["Antonio Mele", "molnar-kriszta", "Sergio Santoro"]
    p["volume"] = "115"
    p["issue"] = "C"
    p["pages"] = "339-353"
    p["doi"] = "10.1016/j.jmoneco.2019.09.005"
    p["url_published"] = "https://doi.org/10.1016/j.jmoneco.2019.09.005"
    new.write_text(json.dumps(p, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    old.unlink()
    print("renamed: molnar-tortorice-2020-jome -> mele-molnar-santoro-2020-jome (was wrong coauthors+title)")

# 6. verbatim abstracts
ABSTRACTS = {
    "molnar-kriszta-2007-jeea": (
        "Surveys of inflation forecasts show that expectations combine "
        "forward-looking and backward-looking elements. This contradicts "
        "conventional wisdom: in the presence of rational agents, adaptive "
        "agents would be driven out of the market. In our paper, we rationalize "
        "this finding in an equilibrium framework. Our model has two types of "
        "agents, one having rational expectations and the other using adaptive "
        "learning. The proportion of these agents in the population evolves "
        "according to their past forecasting performance. We show that even an "
        "underparameterized learning algorithm survives competition with "
        "rational expectations."
    ),
    "molnar-santoro-2014-eer": (
        "We derive optimal monetary policy in a sticky price model when private "
        "agents follow adaptive learning. We show that this slight departure "
        "from rationality has important implications for policy design. The "
        "central bank faces a new intertemporal trade-off, not present under "
        "rational expectations: it is optimal to forego stabilizing the economy "
        "in the present in order to facilitate private sector learning and thus "
        "ease the future intratemporal inflation-output gap trade-offs. The "
        "policy recommendation is robust: the welfare loss entailed by optimal "
        "policy under learning if the private sector actually has rational "
        "expectations is much smaller than if the central bank mistakenly "
        "assumes rational expectations when in fact agents are learning."
    ),
    "ormeno-molnar-2015-jmcb": (
        "Does survey data contain useful information for estimating "
        "macroeconomic models? We address this question by using survey data "
        "of inflation expectations to estimate the New Keynesian model by "
        "Smets and Wouters and compare its performance under rational "
        "expectations and adaptive learning. The survey information serves as "
        "an additional moment restriction and helps us to determine the "
        "learning agents' forecasting model for inflation. Adaptive learning "
        "fares similarly to rational expectations in fitting macro data, but "
        "clearly outperforms rational expectations in fitting macro and survey "
        "data simultaneously. In other words, survey data contain additional "
        "information that is not present in the macro data alone."
    ),
    "attanasio-kovacs-molnar-2020-economica": (
        "In this paper, we make three substantive contributions. First, we use "
        "elicited subjective income expectations to identify the levels of "
        "permanent and transitory income shocks in a lifecycle framework. "
        "Second, we use these shocks to assess whether households' consumption "
        "is insulated from them. Third, we use the shock data to estimate an "
        "Euler equation for consumption. We find that households are able to "
        "smooth transitory shocks, but adjust their consumption in response to "
        "permanent shocks, albeit not fully. The estimates of the Euler "
        "equation parameters with and without expectational errors are similar, "
        "which is consistent with rational expectations."
    ),
    "mele-molnar-santoro-2020-jome": (
        "The main advantage of price level stabilization compared with "
        "inflation stabilization rests on the central bank's ability to shape "
        "expectations. We show that stabilizing prices is no longer optimal "
        "when the central bank can shape expectations of agents with incomplete "
        "knowledge, who have to learn about the policy implemented. "
        "Disinflating in the short run more than agents expect generates "
        "short-term gains without triggering an abrupt loss of confidence, "
        "because agents update expectations sluggishly. Following this policy, "
        "in the long run, the central bank loses the ability to shape agents' "
        "beliefs, and the economy converges to a rational expectations "
        "equilibrium in which policy does not stabilize prices, economic "
        "volatility is high, and agents suffer the corresponding welfare "
        "losses. However, these losses are outweighed by short-term gains from "
        "the learning phase."
    ),
}
for slug, abstract in ABSTRACTS.items():
    p = load(slug)
    p["abstract"] = abstract
    save(slug, p)
print(f"abstracts set on {len(ABSTRACTS)} Molnár papers")
