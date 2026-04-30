"""Set abstracts on Baráth (3 of 4), Benczúr (1 of 3), Darvas (3), Bárány (2)."""
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
    "barath-ferto-2024-jae": {
        "volume": "75", "issue": "1", "pages": "404-424",
        "doi": "10.1111/1477-9552.12563",
    },
    "barath-ferto-bojnec-2020-jae": {
        "volume": "71", "issue": "3", "pages": "853-876",
        "doi": "10.1111/1477-9552.12377",
    },
    "barath-ferto-bojnec-2025-scirep": {
        "volume": "15", "pages": "15895",
        "doi": "10.1038/s41598-025-00584-4",
    },
    "benczur-konya-2013-jimf": {
        "volume": "37", "pages": "260-281",
        "doi": "10.1016/j.jimonfin.2013.06.009",
    },
    "darvas-2008-jbf": {
        "year": 2009, "volume": "33", "issue": "5", "pages": "944-957",
        "doi": "10.1016/j.jbankfin.2008.10.007",
    },
    "darvas-2015-eclett": {
        "volume": "133", "pages": "123-126",
        "doi": "10.1016/j.econlet.2015.05.034",
    },
    "darvas-2019-wd": {
        "volume": "121", "pages": "16-32",
        "doi": "10.1016/j.worlddev.2019.04.011",
    },
    "barany-siegel-2020-labec": {
        "volume": "67", "pages": "101930",
        "doi": "10.1016/j.labeco.2020.101930",
    },
    "barany-siegel-2020-red": {
        "volume": "39", "pages": "304-343",
        "doi": "10.1016/j.red.2020.07.007",
    },
}
for slug, fields in META.items():
    p = load(slug)
    for k, v in fields.items():
        p[k] = v
    save(slug, p)
    print(f"metadata fix: {slug}")

ABSTRACTS = {
    "barath-ferto-2024-jae": (
        "The European Green Deal aims to mitigate the environmental impact "
        "of food production while improving the income of primary producers "
        "and strengthening the EU's competitiveness. We examine how the "
        "degree of ecologisation affects farms' total factor productivity "
        "(TFP). Our analysis combines a random-parameter stochastic "
        "production frontier model with a composite indicator and a dose-"
        "response function approach. Results show a monotonically "
        "decreasing relationship between ecologisation and expected TFP "
        "level. On average, a one-step increase in the degree of "
        "ecologisation results in a 12% decrease in TFP. However, the "
        "results indicate a non-linear relationship. Three regions of the "
        "dose-response function can be distinguished; associated with "
        "high, medium and low degrees of ecologisation. In a region with "
        "a low degree of ecologisation, farms can increase the degree of "
        "ecologisation without reducing TFP. Both efficiency and "
        "technological differences contribute to these differences, but "
        "the main reason is technological. With increasing ecologisation, "
        "farm technology becomes more 'land using'. Therefore, farms can "
        "increase their TFP and degree of ecologisation simultaneously by "
        "using land-saving technologies or through sustainable "
        "intensification."
    ),
    "barath-ferto-bojnec-2020-jae": (
        "The effect of subsidies on the performance of farms has received "
        "a great deal of attention in the literature, although results are "
        "inconclusive. Furthermore, much of the related literature examines "
        "the effect of subsidies only on technical efficiency (TE). We "
        "examine the effect of different types of subsidies on the "
        "different components of total factor productivity (TFP) in "
        "Slovenian agriculture over the period 2006-2013. We first "
        "estimate a Random Parameter Stochastic production frontier model. "
        "Then, based on the estimates of this model, we calculate and "
        "decompose the TFP index into TE, scale efficiency and "
        "technological change. Third, we apply combined difference-in-"
        "difference and a matching estimator to examine the effect of "
        "investment, less favoured area (LFA) and agri-environmental (AE) "
        "subsidies on the different components of TFP. In our case, these "
        "subsidies are found to have no significant effect on either TFP "
        "or on its components."
    ),
    "barath-ferto-bojnec-2025-scirep": (
        "This study investigates gender-based differences in eco-efficiency "
        "among Hungarian field crop farms, using data from the Farm "
        "Accountancy Data Network between 2015 and 2020. Applying Data "
        "Envelopment Analysis and Blinder-Oaxaca decompositions, we reveal "
        "a consistent eco-efficiency advantage for women-headed farms, "
        "particularly at mid-quantiles of eco-efficiency distribution. "
        "This advantage is largely attributed to women's ability to "
        "optimize resource use effectively, though unexplained factors "
        "also contribute, suggesting potential differences in management "
        "practices. Results highlight that women-led farms often adopt "
        "eco-efficient practices that may contribute to sustainability "
        "goals. These findings highlight the need for policies that "
        "support women farmers' access to resources, knowledge, and "
        "innovation in eco-friendly farming practices, helping to enhance "
        "sustainability in agricultural production."
    ),
    "benczur-konya-2013-jimf": (
        "This paper develops a flexible price, two-sector growth model "
        "with a nominal side to study the role of the exchange rate in "
        "transition dynamics. We adopt a standard small open economy "
        "model with traded and nontraded goods, where the engines of "
        "growth are exogenous productivity improvements and capital "
        "accumulation. We enhance this standard framework by adding a "
        "preference for real money holdings, captured by money-in-the-"
        "utility. We follow Schmitt-Groh\u00e9 and Uribe (2003) and assume "
        "that the interest rate on bonds issued by the small open economy "
        "is debt-dependent, and interpret it as a simple financial "
        "friction. We show analytically that the choice of the exchange "
        "rate regime influences the transition dynamics of a small open "
        "economy through the balance sheet of the central bank. We then "
        "calibrate the model to explore the quantitative significance of "
        "our results. We find that the choice of the exchange rate regime "
        "has significant and lasting effects on prices, consumption, "
        "investment and sectoral allocations, and the composition of "
        "financial assets."
    ),
    "darvas-2008-jbf": (
        "Studying all possible pairs of 11 major currencies and 11 "
        "portfolios in 1976-2008 we show that, when there is no leverage, "
        "carry trade is significantly profitable for most currency pairs "
        "and portfolios. Positive returns do not diminish in time "
        "providing a strong case against the hypothesis of uncovered "
        "interest rate parity. We explain these findings with the "
        "leveraged nature of carry trade: leverage may increase "
        "profitability but it materially increases downside risk. We "
        "argue that market inefficiency is related to the level of "
        "leverage."
    ),
    "darvas-2015-eclett": (
        "We create a euro-area Divisia-money dataset and estimate "
        "theoretically correct responses to money, user cost and interest "
        "rate shocks using structural vector-autoregressions. Our findings "
        "suggest that money matters for output, prices and interest "
        "rates, while the European Central Bank can influence monetary "
        "developments."
    ),
    "darvas-2019-wd": (
        "While various methodologies have been used in the literature to "
        "estimate global interpersonal income inequality, the accuracy of "
        "these methods has not so far been tested. The study compares "
        "four methods for measuring global income inequality, finding the "
        "Lorenz curve regression approach most reliable. Using the "
        "two-parameter distribution method, the paper demonstrates that "
        "global income inequality among 145 countries declined between "
        "1988 and 2015, primarily due to income convergence across "
        "nations. However, this decline masks diverging trends: while "
        "within-country inequalities increased and developing Asia saw "
        "regional inequality rise, China and India's income convergence "
        "was instrumental in reducing overall global inequality. "
        "Critically, when excluding these two nations, global "
        "interpersonal income inequality actually increased across the "
        "remaining 143 countries during this period."
    ),
    "barany-siegel-2020-labec": (
        "To study the drivers of the employment reallocation across "
        "sectors and occupations between 1960 and 2017 in the US we "
        "present a model where technology evolves at the sector-"
        "occupation cell level. Drawing on key equations of the "
        "production side we infer technologies directly from the data. "
        "We assess the magnitude of neutral, sector-, and occupation-"
        "specific components in technological change and study their "
        "consequences for labor market outcomes in general equilibrium "
        "where occupational choice and demands for sectoral outputs "
        "change endogenously with technology. Our findings indicate a "
        "major role for occupation-specific technological changes."
    ),
    "barany-siegel-2020-red": (
        "We study the origins of labor productivity growth and its "
        "differences across sectors. In our model, sectors employ workers "
        "of different occupations and various forms of capital, none of "
        "which are perfect substitutes, and technology evolves at the "
        "sector-factor cell level. Using the model we infer technologies "
        "from US data over 1960-2017. We find sector-specific routine "
        "labor augmenting technological change to be crucial. It is the "
        "most important driver of sectoral differences, and has a large "
        "and increasing contribution to aggregate labor productivity "
        "growth. Neither capital accumulation nor the occupational "
        "employment structure within sectors explains much of the "
        "sectoral differences."
    ),
}
for slug, abstract in ABSTRACTS.items():
    p = load(slug)
    p["abstract"] = abstract
    save(slug, p)
print(f"abstracts set on {len(ABSTRACTS)} papers")
