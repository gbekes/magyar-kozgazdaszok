"""Set abstracts on 6 Telegdy papers that lack them."""
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
    "brown-earle-et-al-2006-ces": (
        "The paper looks behind the standard, publicly available labor force "
        "statistics relied upon in most studies of transition economy labor "
        "markets. It analyzes microdata on detailed labor force survey "
        "responses in Russia, Romania, and Estonia to measure nonstandard, "
        "boundary forms and alternative definitions of employment and "
        "unemployment. The calculations show that measured rates are quite "
        "sensitive to definition, particularly in the treatment of household "
        "production (subsistence agriculture), unpaid family helpers, and "
        "discouraged workers, while the categories of part-time work and "
        "other forms of marginal attachment are still relatively unimportant. "
        "The authors find that tweaking the official definitions in apparently "
        "minor ways can produce alternative employment rates that are sharply "
        "higher in Russia but much lower in Romania and slightly lower in "
        "Estonia, and alternative unemployment rates that are sharply higher "
        "in Romania and moderately higher in Estonia and Russia."
    ),
    "brown-earle-et-al-2016-jocf": (
        "Why do the reported effects of privatization on firm performance vary "
        "so much? This paper provides new estimates of these effects and tests "
        "potential explanations for heterogeneity using comprehensive, "
        "long-panel data for 70,000 firms in five East European economies. We "
        "estimate that privatization raises measures of profitability, "
        "productivity, and growth by about 5\u201312% on average, but with "
        "substantial variation across countries and time periods. Analyzing "
        "heterogeneity in privatization effectiveness, we find little "
        "systematic role for firm size, financial dependence, exchange "
        "listing, or technological complexity, but important variation by "
        "fraction privatized, ownership concentration, firm quality, and the "
        "macroeconomic and institutional environment."
    ),
    "earle-telegdy-2002-joce": (
        "Comprehensive panel data on privatization transactions and labor "
        "productivity in Romanian industrial corporations are used to describe "
        "the post-privatization ownership structure, and to estimate the "
        "effect of Romania's diverse privatization policies on firm "
        "performance. The econometric results show consistently positive, "
        "highly significant effects of private ownership on labor productivity "
        "growth, the point estimates implying an increased 1.0 to 1.7 "
        "percentage growth for a 10 percent rise in private shareholding. The "
        "strongest estimated impacts are associated with sales to outside "
        "blockholders; insider transfers and mass privatization are estimated "
        "to have significantly smaller\u2014although still positive\u2014effects on firm "
        "performance."
    ),
    "goel-telegdy-et-al-2024-jocf": (
        "Subsidies should target firms with profitable opportunities and "
        "insufficient funding, but this is difficult due to information "
        "asymmetry between firms and the government. We study how credit "
        "history of firms can help design more efficient subsidies. To this "
        "end, we combine data on non-repayable firm subsidies and the credit "
        "registry from Hungary. Using subsidy winners and losers as treated "
        "and control groups and leveraging variation in access to loans, we "
        "identify the differential impact of subsidies. While subsidies lead "
        "to an incremental impact on assets of loan-deprived as compared to "
        "loan-acquiring firms, the impact is transitory and fades after a few "
        "years. The impact on profitability follows a similar pattern despite "
        "the higher expected marginal value of capital for loan-deprived "
        "firms. Thus, loan deprivation is likely caused by borrower "
        "shortcomings instead of credit rationing by banks. In such cases, "
        "subsidies need not target loan-deprived firms."
    ),
    "murakozy-telegdy-2016-eer": (
        "Using a comprehensive database on successful and rejected "
        "applications for the European Union's Structural and Cohesion Funds "
        "between 2004 and 2012 in Hungary, we study which grant types are "
        "susceptible to political favoritism and how this is achieved. With "
        "fixed-effects and matching estimators we study whether applicants "
        "from municipalities with a mayor endorsed by the governing coalition "
        "won a higher grant value than applicants where the mayor was "
        "affiliated with the opposition. We find limited evidence for such a "
        "difference for total grant value, but in cases when the applicant is "
        "a public entity or the purpose of the project is construction and, "
        "therefore, visible to voters and thus may bring about electoral "
        "benefits, we do find effects of 16\u201321%. The decomposition of the "
        "effect suggests that favoritism plays a role both in the application "
        "and the decision making process as applicants from aligned townships "
        "apply in larger numbers and have higher acceptance rates. When "
        "analyzing the effect of grants on votes, we show that voters indeed "
        "reward construction and public projects but not the other grant "
        "types."
    ),
    "telegdy-2018-labec": (
        "Using a large and unexpected public wage increase in Hungary, which "
        "changed the public wage premium from \u221217 to +7.5% from one "
        "month to the next, I study wage spillovers from the public to the "
        "corporate sector. I proxy the exposure of corporate workers to the "
        "public sector with the variation of the share of public sector "
        "employment within labor market segments defined by gender, "
        "experience, occupation and region. Controlling for worker-firm joint "
        "fixed effects and instrumenting the exposure variable with its past "
        "values, I estimate a wage differential of 9.6% around the wage "
        "increase between two workers situated at the 25th and the 75th "
        "percentile of the exposure measure. The firm's exposure to the "
        "public sector (measured as the average of individual exposures of "
        "the firm's workforce) produces a wage differential of 13.6%, "
        "suggesting that employers are concerned about wage tensions. The "
        "spillover affected primarily young, and therefore, mobile, workers "
        "and the highly educated, who are abundant in the public sector."
    ),
}
for slug, abstract in ABSTRACTS.items():
    p = load(slug)
    p["abstract"] = abstract
    save(slug, p)
print(f"abstracts set on {len(ABSTRACTS)} Telegdy papers")
