"""Set abstracts and fix titles on 6 Danis András papers."""
import json
from pathlib import Path

PAPERS = Path(__file__).resolve().parent.parent / "data" / "papers"


def load(slug):
    return json.loads((PAPERS / f"{slug}.json").read_text(encoding="utf-8"))


def save(slug, data):
    (PAPERS / f"{slug}.json").write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


# Title and metadata fixes per IDEAS:
META = {
    "chava-danis-hsu-2020-jfe": {
        "title": "The economic impact of right-to-work laws: Evidence from collective bargaining agreements and corporate policies",
        "volume": "137", "issue": "2", "pages": "451-469",
        "doi": "10.1016/j.jfineco.2020.02.005",
    },
    "danis-2017-ms": {
        "year": 2017, "volume": "63", "issue": "5", "pages": "1285-1301",
        "doi": "10.1287/mnsc.2015.2375",
    },
    "danis-2020-frl-shareholder-monitoring": {
        "title": "Shareholder activism with strategic investors",
        "volume": "33", "pages": "101230",
        "doi": "10.1016/j.frl.2019.06.007",
    },
    "danis-gamba-2018-jfe": {
        "volume": "127", "issue": "1", "pages": "51-76",
        "doi": "10.1016/j.jfineco.2017.10.005",
    },
    "danis-gamba-2023-ms": {
        "title": "Dark Knights: The Rise in Firm Intervention by Credit Default Swap Investors",
        "year": 2024, "volume": "70", "issue": "2", "pages": "952-970",
        "doi": "10.1287/mnsc.2023.4717",
    },
    "danis-rettl-whited-2014-jfe": {
        "volume": "114", "issue": "3", "pages": "424-443",
        "doi": "10.1016/j.jfineco.2014.07.010",
    },
}
for slug, fields in META.items():
    p = load(slug)
    for k, v in fields.items():
        p[k] = v
    save(slug, p)
    print(f"metadata fix: {slug}")

ABSTRACTS = {
    "chava-danis-hsu-2020-jfe": (
        "We analyze the economic and financial impact of right-to-work (RTW) "
        "laws in the US. Using data from collective bargaining agreements, "
        "we show that there is a decrease in wages for unionized workers "
        "after RTW laws. Firms increase investment and employment but "
        "reduce financial leverage. Labor-intensive firms experience higher "
        "profits and labor-to-asset ratios. Dividends and executive "
        "compensation also increase post-RTW. Our results are consistent "
        "with a canonical theory of the firm augmented with an exogenous "
        "bargaining power of labor and suggest that RTW laws impact "
        "corporate policies by decreasing that bargaining power."
    ),
    "danis-2017-ms": (
        "In this paper, I examine the effect of credit default swaps (CDSs) "
        "on the restructuring of distressed firms. Using a sample of U.S. "
        "distressed exchange offers during the period 2006\u20132011, I "
        "show that the participation rate among bondholders is "
        "significantly lower if the firm has CDSs traded on its debt. To "
        "address endogeneity concerns, I use the introduction of the Big "
        "Bang Protocol as a natural experiment. The results suggest that "
        "firms with CDSs find it difficult to reduce debt out of court. "
        "This is important because it can increase the likelihood of "
        "future bankruptcy, which is inefficient. The findings are "
        "consistent with the empty creditor hypothesis, which posits that "
        "bondholders who are hedged with CDSs are less likely to "
        "participate in a debt restructuring. The paper also contains "
        "direct evidence for the existence of empty creditors."
    ),
    "danis-2020-frl-shareholder-monitoring": (
        "Admati et al. (1994, Journal of Political Economy) predict that "
        "activist shareholders sell most of their shares to passive "
        "investors, which destroys the activist's incentive to engage in "
        "value-enhancing monitoring. I extend their theoretical framework "
        "by assuming a finite number of passive investors instead of a "
        "continuum. In my model, passive investors take into account the "
        "effect of their own demand for shares on the activist's "
        "incentives. As a result, they buy fewer shares from him, which "
        "increases his monitoring intensity. This is important because "
        "empirically, we observe activist investors with large blocks of "
        "shares."
    ),
    "danis-gamba-2018-jfe": (
        "We examine the effect of introducing credit default swaps (CDSs) "
        "on firm value. Our model allows for dynamic investment and "
        "financing, and bondholders can trade in the CDS market. The "
        "model incorporates both negative and positive effects of CDSs. "
        "CDS markets lead to more liquidations, but they also reduce the "
        "probability of costly debt renegotiation and reduce costly equity "
        "financing. After calibrating the model, we find that firm value "
        "increases by 2.9% on average with the introduction of a CDS "
        "market. Firms also invest more and increase leverage. The effect "
        "on firm value is strongest for small, financially constrained, "
        "and low productivity firms."
    ),
    "danis-gamba-2023-ms": (
        "There have been several cases in recent years where credit "
        "default swap (CDS) buyers and sellers intervene in the "
        "restructuring of a distressed firm. We show theoretically that "
        "this can increase firm value. Intervention by CDS buyers solves "
        "the commitment problem between equity and debt holders but "
        "increases the probability of inefficient liquidation. "
        "Intervention by CDS sellers reduces the issue of excessive "
        "liquidation while keeping the benefits of CDS buyer intervention. "
        "Having both types of intervention decouples the commitment "
        "problem from the liquidation problem. Under certain assumptions, "
        "the so-called empty creditor problem can be solved, and firm "
        "value reaches first best."
    ),
    "danis-rettl-whited-2014-jfe": (
        "We revisit the well-established puzzle that leverage is "
        "negatively correlated with measures of profitability. In "
        "contrast, we find that at times when firms are at or close to "
        "their optimal level of leverage, the cross-sectional correlation "
        "between profitability and leverage is positive. At other times, "
        "it is negative. These results are consistent with dynamic "
        "trade-off models in which infrequent capital structure "
        "rebalancing is optimal. The time series of market leverage and "
        "profitability in the quarters prior to rebalancing events match "
        "the patterns predicted by these models. Our results are not "
        "driven by investment layouts, market timing, payout, or "
        "mechanical mean reversion of leverage."
    ),
}
for slug, abstract in ABSTRACTS.items():
    p = load(slug)
    p["abstract"] = abstract
    save(slug, p)
print(f"abstracts set on {len(ABSTRACTS)} Danis papers")
