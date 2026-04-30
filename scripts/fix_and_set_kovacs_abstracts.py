"""Fix 4 wrong-titled Kovács stubs, then populate verbatim abstracts on all 9.

Title/journal corrections from canonical sources (Yale CV, IDEAS, publisher):
- sharkey-kovacs-2018-asq         -> RENAME to sharkey-kovacs-2018-mansci
                                     title + journal corrected (was wrong both).
- kovacs-jensen-sorenson-2018-natbiotech -> title corrected only.
- hsu-kovacs-kocak-2019-smj       -> title corrected only.
- lemens-kovacs-hannan-pros-2023-pnas -> title corrected only.
The other 5 (kovacs-carroll-lehman-2013-orgsci, lehman-kovacs-carroll-2014-mansci,
goldberg-hannan-kovacs-2016-asr, hsu-kocak-kovacs-2018-orgsci,
lehman-oconnor-kovacs-newman-2019-ama) are correct.
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


# ---------- 1. sharkey-kovacs-2018-asq → sharkey-kovacs-2018-mansci -----------
old = PAPERS / "sharkey-kovacs-2018-asq.json"
new = PAPERS / "sharkey-kovacs-2018-mansci.json"
if old.exists() and not new.exists():
    p = json.loads(old.read_text(encoding="utf-8"))
    p["id"] = "sharkey-kovacs-2018-mansci"
    p["title"] = "The Many Gifts of Status: How Attending to Audience Reactions Drives the Use of Status"
    p["authors"] = ["Amanda J. Sharkey", "kovacs-balazs"]
    p["journal"] = "Management Science"
    p["volume"] = "64"
    p["issue"] = "11"
    p["pages"] = "5422-5443"
    p["doi"] = "10.1287/mnsc.2017.2879"
    p["url_published"] = "https://doi.org/10.1287/mnsc.2017.2879"
    new.write_text(json.dumps(p, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    old.unlink()
    print("renamed: sharkey-kovacs-2018-asq -> sharkey-kovacs-2018-mansci (title + journal fixed)")

# ---------- 2. title-only fixes ----------
TITLE_FIXES = {
    "kovacs-jensen-sorenson-2018-natbiotech": {
        "title": "Gender differences in obtaining and maintaining patent rights",
        "authors": ["Kyle Jensen", "kovacs-balazs", "Olav Sorenson"],
        "doi": "10.1038/nbt.4120",
        "url_published": "https://doi.org/10.1038/nbt.4120",
        "volume": "36",
        "issue": "4",
        "pages": "307-309",
    },
    "hsu-kovacs-kocak-2019-smj": {
        "title": "Experientially diverse customers and organizational adaptation in changing demand landscapes: A study of US cannabis markets, 2014–2016",
        "authors": ["Greta Hsu", "kovacs-balazs", "Özgecan Koçak"],
        "doi": "10.1002/smj.3078",
        "url_published": "https://doi.org/10.1002/smj.3078",
        "volume": "40",
        "issue": "13",
        "pages": "2214-2241",
    },
    "lemens-kovacs-hannan-pros-2023-pnas": {
        "title": "Uncovering the semantics of concepts using GPT-4",
        "authors": ["Gaël Le Mens", "kovacs-balazs", "Michael T. Hannan", "Guillem Pros"],
        "doi": "10.1073/pnas.2309350120",
        "url_published": "https://doi.org/10.1073/pnas.2309350120",
        "volume": "120",
        "issue": "49",
        "pages": "e2309350120",
    },
}
for slug, fields in TITLE_FIXES.items():
    p = load(slug)
    for k, v in fields.items():
        p[k] = v
    save(slug, p)
    print(f"fixed metadata: {slug}")

# Also fix hsu-kocak-kovacs-2018-orgsci issue/volume/pages from IDEAS
p = load("hsu-kocak-kovacs-2018-orgsci")
p["volume"] = "29"
p["issue"] = "1"
p["pages"] = "172-190"
p["doi"] = "10.1287/orsc.2017.1167"
p["url_published"] = "https://doi.org/10.1287/orsc.2017.1167"
save("hsu-kocak-kovacs-2018-orgsci", p)

# ---------- 3. verbatim abstracts ----------
ABSTRACTS = {
    "kovacs-carroll-lehman-2013-orgsci": (
        "We present two studies that together test a fundamental yet rarely examined "
        "assumption underlying the contemporary appeal of authenticity\u2014namely, that "
        "consumers assign higher value ratings to organizations regarded as authentic. "
        "Study 1 conducts content analysis of unsolicited online restaurant reviews "
        "entered voluntarily by consumers in three major U.S. metropolitan areas from "
        "October 2004 to October 2011. The data contain information from 1,271,796 "
        "reviews written by 252,359 unique reviewers of 18,869 restaurants. The "
        "findings show that consumers assign higher ratings to restaurants regarded as "
        "authentic, even after controlling for restaurant quality in several ways. In "
        "addition, we find that consumers perceive independent, family-owned, and "
        "specialist (single-category) restaurants as more authentic than chain, "
        "non-family-owned, and generalist establishments. Study 2 uses a controlled "
        "experiment with fictitious restaurants to provide further evidence on the "
        "causal effect of authenticity on consumer ratings."
    ),
    "lehman-kovacs-carroll-2014-mansci": (
        "We examine how consumers evaluate restaurants when their evaluations are "
        "informed by competing schemes \u2014 a science-based code of hygiene involving "
        "compliance with local health regulations, and a context-activated code of "
        "authenticity involving conformity to cultural norms. We argue that violations "
        "of the hygiene code recede in importance when the authenticity code is "
        "activated. Empirical analyses of more than 442,000 online consumer reviews "
        "and approximately 52,740 governmental health inspections collected from 2004 "
        "to 2011 of restaurants located in three major U.S. metropolitan areas support "
        "our argument: violations of the hygiene code lead to lower restaurant ratings "
        "from consumers, but this negative effect is significantly weaker for "
        "restaurants viewed by consumers as authentic. Implications for theory and "
        "practice are discussed."
    ),
    "goldberg-hannan-kovacs-2016-asr": (
        "We propose a synthesis of two lines of sociological research on boundary "
        "spanning in cultural production and consumption. One, research on cultural "
        "omnivorousness, analyzes choice by heterogeneous audiences facing an array "
        "of crisp cultural offerings. The other, research on categories in markets, "
        "analyzes reactions by homogeneous audiences to objects that vary in the "
        "degree to which they conform to categorical codes. We develop a model of "
        "heterogeneous audiences evaluating objects that vary in typicality. This "
        "allows consideration of orientations on two dimensions of cultural "
        "preference: variety and typicality. We propose a novel analytic framework "
        "to map consumption behavior in these two dimensions. We argue that one "
        "audience type, those who value variety and typicality, are especially "
        "resistant to objects that span boundaries. We test this argument by "
        "developing a typicality measure based on the topic distributions of films "
        "and books on the Internet Movie Database (IMDb) and Goodreads."
    ),
    "hsu-kocak-kovacs-2018-orgsci": (
        "When recreational cannabis dispensaries first entered the U.S. market in "
        "2014, how did incumbent medical cannabis dispensaries react? Did they "
        "emphasize their distinct identity as medical providers, distancing themselves "
        "from recreational dispensaries and those consumers who consume cannabis "
        "recreationally? Or did they downplay their medical orientation to compete "
        "directly for potential resources? In this study, we propose that how "
        "incumbent organizations position their identities in response to increasing "
        "competition from an emerging rival form depends on key audiences' acceptance "
        "of the new form. Using data on the evolving cannabis markets in the states "
        "of Colorado and Washington during the year following the initial emergence "
        "of the recreational category, we find a sharpening of identity among medical "
        "dispensaries in communities with low voter support for recreational-use "
        "legalization. Medical dispensaries accentuated the medical orientation of "
        "their identities as recreational dispensaries increasingly set up operations "
        "and as buyers inclined more toward recreational use. In contrast, we find a "
        "blurring of medical/recreational identity in communities where voters "
        "demonstrated support for recreational-use legalization."
    ),
    "kovacs-jensen-sorenson-2018-natbiotech": (
        "An examination of the prosecution and maintenance histories of approximately "
        "2.7 million US patent applications indicates that women have less favorable "
        "outcomes than men. Although women make up half of the population, they "
        "represent just 10% of US patent inventors and only 15% of inventors in the "
        "life sciences. Patent applications by women inventors were found to be more "
        "likely to be rejected than those of men, and those rejections were less "
        "likely to be appealed by the applicant team (inventor, assignee, and "
        "prosecuting attorney). Conditional on being granted, patent applications by "
        "women inventors had a smaller fraction of their claims allowed, on average, "
        "than did applications by men."
    ),
    "sharkey-kovacs-2018-mansci": (
        "The majority of extant studies involving status argue that status enters "
        "into choice and evaluation because people personally believe that status "
        "serves as a signal of quality. However, this mechanism seems less plausible "
        "in cases when consensus on the meaning of quality is lacking. To understand "
        "how and why status often nonetheless enters into evaluation in those cases, "
        "this paper contributes to a growing body of work that proposes that "
        "individuals and organizations are particularly likely to base their choices "
        "and evaluations on status when they are concerned with the reactions of "
        "others. We provide an empirical test of this argument by analyzing how the "
        "sales gap between prizewinning books and their shortlisted-only peers (as "
        "well as a second similar-content control group) changes during the December "
        "holidays, when the purchase of books as gifts increases relative to "
        "purchases for one's own personal use. Results show that the sales gap "
        "widens with the increased orientation toward gift giving, consistent with "
        "our theoretical arguments about how attending to audience reactions drives "
        "the use of status. Analyses of two online experiments allow for further "
        "clarification of the mechanism behind our findings."
    ),
    "hsu-kovacs-kocak-2019-smj": (
        "In this study, we contribute to strategy and organizational theories of "
        "organizational adaptation by developing theory about the kinds of customers "
        "that facilitate an organization's ability to adapt to changing demand-side "
        "conditions. We propose that customers who have previously interacted with "
        "diverse types of organizations in the market convey informationally rich "
        "feedback that better enables organizations to understand and adapt to "
        "change\u2014particularly in more rapidly changing contexts. We further expect "
        "that organizations that position themselves congruently with market "
        "preferences will be stronger market competitors. We test and find support "
        "for our arguments using a unique dataset of over 8,000 cannabis dispensaries "
        "operating in seven states that were listed on Weedmaps.com between July "
        "2014 and June 2016."
    ),
    "lehman-oconnor-kovacs-newman-2019-ama": (
        "The concept of authenticity informs a number of central topics in management "
        "studies. On the surface, it might seem that a consensus exists about its "
        "meaning; there is indeed widespread agreement that authenticity refers to "
        "that which is \u201creal\u201d or \u201cgenuine\u201d or \u201ctrue.\u201d Below the surface, however, "
        "there is much less agreement; scholars use the same lexical term but often "
        "approach the concept from different perspectives and apply different "
        "meanings. This review outlines three fundamental but distinct perspectives "
        "found in the literature: authenticity as (1) consistency between an entity's "
        "internal values and its external expressions, (2) conformity of an entity to "
        "the norms of its social category, and (3) connection between an entity and "
        "a person, place, or time as claimed. The aim of this review was to "
        "critically appraise the various research themes within each perspective, "
        "highlighting similarities, differences, and relationships between them."
    ),
    "lemens-kovacs-hannan-pros-2023-pnas": (
        "The ability of recent Large Language Models (LLMs) such as GPT-3.5 and GPT-4 "
        "to generate human-like texts suggests that social scientists could use these "
        "LLMs to construct measures of semantic similarity that match human judgment. "
        "In this article, we provide an empirical test of this intuition. We use "
        "GPT-4 to construct a measure of typicality\u2014the similarity of a text "
        "document to a concept. We evaluate its performance against other "
        "model-based typicality measures in terms of the correlation with human "
        "typicality ratings. We conduct this comparative analysis in two domains: "
        "the typicality of books in literary genres (using an existing dataset of "
        "book descriptions) and the typicality of tweets authored by US Congress "
        "members in the Democratic and Republican parties (using a novel dataset). "
        "The typicality measure produced with GPT-4 meets or exceeds the performance "
        "of the previous state-of-the-art typicality measure. It accomplishes this "
        "without any training with the research data (it is zero-shot learning). "
        "This is a breakthrough because the previous state-of-the-art measure "
        "required fine-tuning an LLM on hundreds of thousands of text documents to "
        "achieve its performance."
    ),
}
for slug, abstract in ABSTRACTS.items():
    p = load(slug)
    p["abstract"] = abstract
    save(slug, p)
print(f"abstracts set on {len(ABSTRACTS)} Kovács papers")
