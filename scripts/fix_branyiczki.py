"""Set abstracts on 4 Branyiczki Réka papers."""
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
    "baro-branyiczki-elek-2022-eja": {
        "volume": "19", "issue": "3", "pages": "837-848",
        "doi": "10.1007/s10433-021-00636-4",
    },
    "cepaluni-dorsch-branyiczki-2022-jpfpc": {
        "volume": "37", "issue": "1", "pages": "27-53",
        "doi": "10.1332/251569121X16308265759642",
    },
    "gabos-branyiczki-et-al-2024-jesp": {
        "volume": "34", "issue": "3", "pages": "289-308",
        "doi": "10.1177/09589287241232272",
    },
}
for slug, fields in META.items():
    p = load(slug)
    for k, v in fields.items():
        p[k] = v
    save(slug, p)
    print(f"metadata fix: {slug}")

ABSTRACTS = {
    "baro-branyiczki-elek-2022-eja": (
        "Using data from the COVID-19 questionnaire of the Survey of Health, "
        "Ageing and Retirement in Europe (SHARE), we investigate the time "
        "patterns of precautionary health behaviours of individuals aged 50 "
        "years and above during the summer of 2020, an easing phase of the "
        "COVID-19 pandemic in Europe. We also examine how these health "
        "behaviours differ by the presence of chronic conditions such as "
        "hypertension, high cholesterol level, heart disease, diabetes or "
        "chronic bronchitis, which can be considered as risk factors for "
        "COVID-19. Our results suggest that while on average, people became "
        "less precautious during the analysed time period, this is less so "
        "for those who are at higher risk. We also document large regional "
        "differences in precautionary health behaviours and show that "
        "higher-risk individuals are on average more cautious in all "
        "regions. We conclude that people adjusted their health behaviours "
        "in line with the generally understood risk of the COVID-19 "
        "disease. At the same time, our results also point out divergences "
        "in the level of willingness to take different precautionary steps."
    ),
    "baro-branyiczki-et-al-2022-krtkwp-payroll-taxes": (
        "We study the impact of a large payroll tax cut for older workers "
        "in Hungary. Motivated by the predictions of a standard equilibrium "
        "job search model, we examine the heterogeneous impact of the "
        "policy. Employment increases most at low-productivity firms "
        "offering low-wage jobs, which tend to hire from unemployment, "
        "while the effects are more muted for high-productivity firms "
        "offering high-wage jobs. At the same time, wages only increase at "
        "high-productivity firms. These results point to important "
        "heterogeneity in the incidence of payroll tax cuts across firms "
        "and highlight that payroll taxes have a significant impact on the "
        "composition of jobs in the labor market."
    ),
    "cepaluni-dorsch-branyiczki-2022-jpfpc": (
        "The paper provides a quantitative examination of the link between "
        "political institutions and deaths during the first 100 days of the "
        "COVID-19 pandemic. The study demonstrates that countries with more "
        "democratic political institutions experienced deaths on a larger "
        "per capita scale than less democratic countries, with results "
        "robust to the inclusion of many relevant controls, a battery of "
        "estimation techniques, and estimation with instruments for the "
        "institutional measures. Additionally, the authors examine the "
        "extent to which COVID-19 deaths were impacted heterogeneously by "
        "policy responses across types of political institutions, finding "
        "that policy responses in democracies were less effective in "
        "reducing deaths in the early stages of the crisis."
    ),
    "gabos-branyiczki-et-al-2024-jesp": (
        "Despite the rise in employment, consistently high EU-average "
        "poverty rates continue to generate debates about the factors that "
        "explain the level and changes in the relative poverty rate, both "
        "within and across countries. Assuming a strong negative "
        "correlation between poverty and employment, the article "
        "investigates the role of four mechanisms responsible for this "
        "blurred relationship: changes in employment levels, the "
        "distribution of paid work between households, the within-household "
        "concentration of paid work, and the role of social transfers. The "
        "article shows that using a floating poverty threshold considerably "
        "underestimates the strength of the relationships between poverty, "
        "employment and social transfers."
    ),
}
for slug, abstract in ABSTRACTS.items():
    p = load(slug)
    p["abstract"] = abstract
    save(slug, p)
print(f"abstracts set on {len(ABSTRACTS)} Branyiczki papers")
