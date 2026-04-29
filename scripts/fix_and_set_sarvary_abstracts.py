"""Fix the wrongly-titled Sárváry 1999 stub and set verbatim abstracts on all 6 papers.

Issue: `sarvary-1999-marsci` was created with the title of a 1999 *California
Management Review* article (KM in consulting) but slugged for Marketing Science.
CMR is not on our journal whitelist (tier-C / business-press). The right paper
to catalogue under that slug is the genuinely tier-A/B Lal-Sárváry 1999
Marketing Science paper "When and How Is the Internet Likely to Decrease
Price Competition?" — same year, same journal, fits the slug.

Action: rename to lal-sarvary-1999-marsci with the correct paper details.
The other 5 stubs are correct as-is.
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


# 1. rename slug
old = PAPERS / "sarvary-1999-marsci.json"
new = PAPERS / "lal-sarvary-1999-marsci.json"
if old.exists() and not new.exists():
    p = json.loads(old.read_text(encoding="utf-8"))
    p["id"] = "lal-sarvary-1999-marsci"
    p["title"] = "When and How Is the Internet Likely to Decrease Price Competition?"
    p["authors"] = ["Rajiv Lal", "sarvary-miklos"]
    p["volume"] = "18"
    p["issue"] = "4"
    p["pages"] = "485-503"
    p["doi"] = "10.1287/mksc.18.4.485"
    p["url_published"] = "https://doi.org/10.1287/mksc.18.4.485"
    new.write_text(json.dumps(p, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    old.unlink()
    print("renamed: sarvary-1999-marsci -> lal-sarvary-1999-marsci (was wrong title from CMR paper)")

# 2. canonical metadata fixes (volume/issue/pages/DOI) where missing
META = {
    "ofek-sarvary-2001-mansci": {
        "volume": "47", "issue": "11", "pages": "1441-1456",
        "doi": "10.1287/mnsc.47.11.1441.10252",
        "url_published": "https://doi.org/10.1287/mnsc.47.11.1441.10252",
    },
    "atasu-sarvary-vanwassenhove-2008-mansci": {
        "volume": "54", "issue": "10", "pages": "1731-1746",
        "doi": "10.1287/mnsc.1080.0893",
        "url_published": "https://doi.org/10.1287/mnsc.1080.0893",
    },
    "katona-zubcsek-sarvary-2011-jmr": {
        "volume": "48", "issue": "3", "pages": "425-443",
        "doi": "10.1509/jmkr.48.3.425",
        "url_published": "https://doi.org/10.1509/jmkr.48.3.425",
    },
    "ofek-katona-sarvary-2011-marsci": {
        "volume": "30", "issue": "1", "pages": "42-60",
        "doi": "10.1287/mksc.1100.0588",
        "url_published": "https://doi.org/10.1287/mksc.1100.0588",
    },
    "bart-stephen-sarvary-2014-jmr": {
        "volume": "51", "issue": "3", "pages": "270-285",
        "doi": "10.1509/jmr.13.0503",
        "url_published": "https://doi.org/10.1509/jmr.13.0503",
    },
}
for slug, fields in META.items():
    p = load(slug)
    for k, v in fields.items():
        p[k] = v
    save(slug, p)

# 3. verbatim abstracts
ABSTRACTS = {
    "lal-sarvary-1999-marsci": (
        "We challenge the assumption that the Internet intensifies price competition. "
        "Instead, we develop conditions under which the Internet may decrease "
        "competition. We develop an analytic model showing that the introduction of "
        "the Internet might lead to monopoly pricing when (1) the proportion of "
        "Internet users is high enough, (2) when nondigital attributes are relevant "
        "but not overwhelming, (3) when consumers have a more favorable prior about "
        "the brand they currently own, and (4) when the purchase situation can be "
        "characterized by 'destination shopping'. The Internet can increase consumer "
        "loyalty by raising effective search costs for products requiring physical "
        "inspection. The paper concludes that stores may become more important for "
        "customer acquisition while the Internet handles demand fulfillment for "
        "certain product categories."
    ),
    "ofek-sarvary-2001-mansci": (
        "Professional services firms (e.g., consultants, accounting firms, or "
        "advertising agencies) generate and sell business solutions to their "
        "customers. In doing so, they can leverage the cumulative experience gained "
        "from serving their customer base to either reduce their variable costs or "
        "increase the quality of their products/services. In other words, their "
        "\u201cproduction technology\u201d exhibits some form of increasing returns to scale. "
        "Growth and globalization, coupled with recent advances in information "
        "technology, have led many of these firms to introduce sophisticated "
        "knowledge management (KM) systems in order to create sustainable competitive "
        "advantage. In this paper, the authors analyze how KM is likely to affect "
        "competition among such professional services firms. The results shed light "
        "on the current literature exploring the deployment of KM systems by "
        "suggesting that in a competitive setting, when firms' ability to leverage "
        "their customer base is high, KM should lead to quality improvement rather "
        "than cost reductions. In a dynamic setting, it is also shown that when "
        "firms use their KM system to improve product quality, higher ability to "
        "leverage the customer base may actually hurt profits and lead to industry "
        "shakeout."
    ),
    "atasu-sarvary-vanwassenhove-2008-mansci": (
        "The profitability of remanufacturing systems for different cost, "
        "technology, and logistics structures has been extensively investigated in "
        "the literature. We provide an alternative and somewhat complementary "
        "approach that considers demand-related issues, such as the existence of "
        "green segments, original equipment manufacturer competition, and product "
        "life-cycle effects. The profitability of a remanufacturing system strongly "
        "depends on these issues as well as on their interactions. For a monopolist, "
        "we show that there exist thresholds on the remanufacturing cost savings, "
        "the green segment size, market growth rate, and consumer valuations for "
        "the remanufactured products, above which remanufacturing is profitable. "
        "More important, we show that under competition remanufacturing can become "
        "an effective marketing strategy, which allows the manufacturer to defend "
        "its market share via price discrimination."
    ),
    "katona-zubcsek-sarvary-2011-jmr": (
        "This article discusses the diffusion process in an online social network "
        "given the individual connections between members. The authors model the "
        "adoption decision of individuals as a binary choice affected by three "
        "factors: (1) the local network structure formed by already adopted "
        "neighbors, (2) the average characteristics of adopted neighbors "
        "(influencers), and (3) the characteristics of the potential adopters. "
        "Focusing on the first factor, the authors find two marked effects. First, "
        "an individual who is connected to many adopters has a greater adoption "
        "probability (degree effect). Second, the density of connections in a group "
        "of already adopted consumers has a strong positive effect on the adoption "
        "of individuals connected to this group (clustering effect). The article "
        "also records significant effects for influencer and adopter "
        "characteristics. An interesting counterintuitive finding is that the "
        "average influential power of individuals decreases with the total number "
        "of their contacts. These results have practical implications for viral "
        "marketing."
    ),
    "ofek-katona-sarvary-2011-marsci": (
        "The Internet has increased the flexibility of retailers, allowing them to "
        "operate an online arm in addition to their physical stores. The online "
        "channel offers potential benefits in selling to customer segments that "
        "value the convenience of online shopping, but it also raises new "
        "challenges. These include the higher likelihood of costly product returns "
        "when customers' ability to \u201ctouch and feel\u201d products is important in "
        "determining fit. We study competing retailers that can operate dual "
        "channels (\u201cbricks and clicks\u201d) and examine how pricing strategies and "
        "physical store assistance levels change as a result of the additional "
        "Internet outlet. A central result we obtain is that when differentiation "
        "among competing retailers is not too high, having an online channel can "
        "actually increase investment in store assistance levels (e.g., greater "
        "shelf display, more-qualified sales staff, floor samples) and decrease "
        "profits. Consequently, when the decision to open an Internet channel is "
        "endogenized, there can exist an asymmetric equilibrium where only one "
        "retailer elects to operate an online arm but earns lower profits than its "
        "bricks-only rival."
    ),
    "bart-stephen-sarvary-2014-jmr": (
        "The authors examine which product characteristics are likely to be "
        "associated with mobile display advertising (MDA) campaigns that are "
        "effective in increasing consumers' favorable attitudes towards products "
        "and purchase intentions. Using data from a large-scale test-control field "
        "experiment covering 54 U.S. MDA campaigns run between 2007 and 2010 and "
        "involving 39,946 consumers, the results show that MDA campaigns "
        "significantly increased consumers' favorable attitudes and purchase "
        "intentions only when the campaigns advertised products that were higher "
        "(vs. lower) involvement and utilitarian (vs. hedonic). The authors discuss "
        "the implications of this finding for the design and evaluation of mobile "
        "advertising campaigns by marketers."
    ),
}
for slug, abstract in ABSTRACTS.items():
    p = load(slug)
    p["abstract"] = abstract
    save(slug, p)
print(f"abstracts set on {len(ABSTRACTS)} Sárváry papers")
