"""Set abstracts on Keller (4), Laczó (2), Szabó-Morvai (2) papers."""
import json
from pathlib import Path

PAPERS = Path(__file__).resolve().parent.parent / "data" / "papers"


def load(slug):
    return json.loads((PAPERS / f"{slug}.json").read_text(encoding="utf-8"))


def save(slug, data):
    (PAPERS / f"{slug}.json").write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


# Year fix for childcare 2018 paper which is actually vol 56, 2019 print
META = {
    "lovasz-szabo-2018-ee": {
        "year": 2019, "volume": "56", "issue": "6", "pages": "2127-2165",
    },
    "szabo-lovasz-2023-ee": {
        "year": 2024, "volume": "66", "issue": "6", "pages": "2823-2879",
    },
}
for slug, fields in META.items():
    p = load(slug)
    for k, v in fields.items():
        p[k] = v
    save(slug, p)
    print(f"metadata fix: {slug}")

ABSTRACTS = {
    "keller-2023-esr": (
        "Social theories posit that peers affect students' academic "
        "self-concept (ASC). Most prominently, Big-Fish-Little-Pond, invidious "
        "comparison, and relative deprivation theories predict that exposure "
        "to academically stronger peers decreases students' ASC, and exposure "
        "to academically weaker peers increases students' ASC. These "
        "propositions have not yet been tested experimentally. We executed a "
        "large and pre-registered field experiment that randomized students "
        "to deskmates within 195 classrooms of 41 schools (N = 3,022). Our "
        "primary experimental analysis found no evidence of an effect of "
        "peer achievement on ASC in either direction. Exploratory analyses "
        "hinted at a subject-specific deskmate effect on ASC in verbal "
        "skills, and that sitting next to a lower-achieving boy increased "
        "girls' ASC (but not that sitting next to a higher-achieving boy "
        "decreased girls' ASC). Critically, however, none of these group-"
        "specific results held up to even modest corrections for multiple "
        "hypothesis testing. Contrary to theory, our randomized field "
        "experiment thus provides no evidence for an effect of peer "
        "achievement on students' ASC."
    ),
    "keller-szakal-2021-plosone-encouragement": (
        "Motivated by the self-determination theory of psychology, we "
        "investigate how simple school practices can forge students' "
        "engagement with the academic aspect of school life. We carried out "
        "a large-scale preregistered randomized field experiment with a "
        "crossover design, involving all the students of the University of "
        "Szeged in Hungary. Our intervention consisted of an automated "
        "encouragement message that praised students' past achievements and "
        "signaled trust in their success. The treated students received "
        "encouragement messages before their exam via two channels: e-mail "
        "and SMS message. The control students did not receive any "
        "encouragement. Our primary analysis compared the treated and "
        "control students' end-of-semester exam grades. We did not find an "
        "average treatment effect on students' exam grades. However, in the "
        "subsample of those who answered the endline survey, the treated "
        "students reported higher self-efficacy than the control students. "
        "The treatment affected students' motivation before their first "
        "exam—but not before their second—and did not affect students' test "
        "anxiety."
    ),
    "keller-szakal-2022-socforces": (
        "High school track choice determines college access in many "
        "countries. We hypothesize that some qualified students avoid the "
        "college-bound track in high school simply because they overestimate "
        "admission requirements. To test this hypothesis, we conducted a "
        "randomized field experiment that communicated the admission "
        "standards of local secondary schools on the academic track to "
        "students in Hungary before the application deadline. We targeted "
        "the subset of students (\u201cseeds\u201d) who occupied the most "
        "central position in the classroom-social networks, aiming to detect "
        "both direct effects on the track choice of targeted seeds and "
        "spillover effects on their untreated peers. We found neither a "
        "direct effect nor a spillover effect on students' applications or "
        "admissions on average. Further analyses, however, revealed "
        "theoretically plausible heterogeneity in the direct causal effect "
        "of the intervention on the track choice of targeted seeds. "
        "Providing information about admission standards increased "
        "applications and admissions to secondary schools on the academic "
        "track among seeds who had a pre-existing interest in the academic "
        "track but were unsure of their chances of admission."
    ),
    "keller-takacs-2021-plosone-proximity": (
        "Can outside interventions foster socio-culturally diverse "
        "friendships? We executed a large field experiment that randomized "
        "the seating charts of 182 3rd through 8th grade classrooms (N = "
        "2,966 students) for the duration of one semester. We found that "
        "being seated next to each other increased the probability of a "
        "mutual friendship from 15% to 22% on average. Furthermore, induced "
        "proximity increased the latent propensity toward friendship "
        "equally for all students, regardless of students' dyadic similarity "
        "with respect to educational achievement, gender, and ethnicity. "
        "However, the probability of a manifest friendship increased more "
        "among similar than among dissimilar students—a pattern mainly "
        "driven by gender. Our findings demonstrate that a scalable "
        "light-touch intervention can affect face-to-face networks and "
        "foster diverse friendships in groups that already know each other, "
        "but they also highlight that transgressing boundaries, especially "
        "those defined by gender, remains an uphill battle."
    ),
    "laczo-2014-jedc": (
        "I consider a risk-sharing game with limited commitment, and study "
        "how the discount factor above which perfect risk sharing is "
        "self-enforcing in the long run depends on agents' risk aversion "
        "and the riskiness of their endowment. When agents face no aggregate "
        "risk, a mean-preserving spread may destroy the sustainability of "
        "perfect risk sharing if each agent's endowment may take more than "
        "three values. With aggregate risk the same can happen with only "
        "two possible endowment realizations. With respect to risk aversion "
        "the intuitive comparative statics result holds without aggregate "
        "risk, but it holds only under strong assumptions in the presence "
        "of aggregate risk."
    ),
    "laczo-rossi-2020-jome": (
        "We characterise optimal tax policies when the government has "
        "access to consumption taxation and cannot credibly commit to "
        "future policies. We consider a neoclassical economy where factor "
        "income taxation is distortionary within the period, due to "
        "endogenous labour and capital utilisation and non-tax-deductibility "
        "of depreciation. Contrary to the case where only labour and "
        "capital income are taxed, the optimal time-consistent policies "
        "with consumption taxation are remarkably similar to their Ramsey "
        "counterparts. The welfare gains from commitment are negligible, "
        "while they are substantial without consumption taxation. Further, "
        "the welfare gains from taxing consumption are much higher without "
        "commitment."
    ),
    "lovasz-szabo-2018-ee": (
        "We estimate the effect of subsidized childcare availability on "
        "Hungarian mothers' labor supply, using a discontinuity in "
        "kindergarten eligibility at age 3 of children. The effect is "
        "identified in a setting where policy intervention has a high "
        "potential impact, since maternal labor supply is very low under "
        "age 3 of children, but high for mothers with older children. We "
        "find that access to subsidized childcare increases maternal labor "
        "supply by 11.7 percentage points or 24%, an impact that is higher "
        "than what has been found in previous quasi-experimental studies "
        "from most other countries. However, the potential effectiveness "
        "of future childcare expansion under age 3 may be constrained by "
        "further institutional factors, such as very long parental leave, "
        "traditional cultural views regarding maternal employment and "
        "institutional childcare, and the lack of flexible work forms."
    ),
    "szabo-lovasz-2023-ee": (
        "The estimated effect of childcare availability on maternal labor "
        "supply varies highly in previous single-country estimates. We "
        "provide comparable quasi-experimental estimates of the childcare "
        "effect for seven countries, using harmonized data and a uniform "
        "method based on country-specific childcare eligibility cutoffs. "
        "We evaluate the estimates in light of key institutional factors "
        "to determine under what conditions childcare expansion is likely "
        "to be effective. We propose a measure that captures childcare "
        "scarcity and predicts the effectiveness of childcare expansion: "
        "the gap between the participation rate of mothers with older "
        "children (aged 6–14) and childcare coverage under the age of 3. "
        "In countries with a high gap, we find that childcare availability "
        "has a significant positive impact on maternal labor supply "
        "(Austria, Czech Republic, Hungary, Slovak Republic). No "
        "significant impact is found in countries where the gap is low "
        "due to either already high childcare coverage (France) or the "
        "low participation of mothers with older children (Greece, Italy)."
    ),
}
for slug, abstract in ABSTRACTS.items():
    p = load(slug)
    p["abstract"] = abstract
    save(slug, p)
print(f"abstracts set on {len(ABSTRACTS)} papers")
