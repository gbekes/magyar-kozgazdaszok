"""Set abstracts on 5 of 6 Benk Szilárd papers (1 book chapter deferred)."""
import json
from pathlib import Path

PAPERS = Path(__file__).resolve().parent.parent / "data" / "papers"


def load(slug):
    return json.loads((PAPERS / f"{slug}.json").read_text(encoding="utf-8"))


def save(slug, data):
    (PAPERS / f"{slug}.json").write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


# Year fix: benk-gillman-2019-jimf was JIMF vol 101, 2020 print
META = {
    "benk-gillman-2019-jimf": {"year": 2020, "volume": "101", "pages": "102100"},
    "benk-gillman-et-al-2009-jedc": {
        "year": 2010, "volume": "34", "issue": "4", "pages": "765-779",
    },
    "benk-gillman-et-al-2005-red": {
        "volume": "8", "issue": "3", "pages": "668-687",
    },
}
for slug, fields in META.items():
    p = load(slug)
    for k, v in fields.items():
        p[k] = v
    save(slug, p)
    print(f"metadata fix: {slug}")

ABSTRACTS = {
    "benk-gillman-2019-jimf": (
        "Real oil prices surged from 2009 through 2014, comparable to the "
        "1970's oil shock period. Standard explanations based on monopoly "
        "markup fall short since inflation remained low after 2009. This "
        "paper contributes strong evidence of Granger (1969) predictability "
        "of nominal factors to oil prices, using one adjustment to monetary "
        "aggregates. This adjustment is the subtraction from the monetary "
        "aggregates of the 2008-2009 Federal Reserve borrowing of reserves "
        "from other Central Banks (Swaps), made after US reserves turned "
        "negative. This adjustment is key in that Granger predictability "
        "from standard monetary aggregates is found only with the Swaps "
        "subtracted."
    ),
    "benk-gillman-2023-enerecon": (
        "The paper adds money supply and inflation expectations shocks to a "
        "well-known three-variable structural model that identifies oil "
        "price shocks through fundamentals affecting the oil market. "
        "Impulse responses show the significance of our two additional "
        "monetary shocks in impacting real oil prices. By subtracting from "
        "the money supply the temporary Federal Reserve swaps that were "
        "used to increase liquidity during the 2008 and 2020 bank crises, "
        "shocks upwards in both the adjusted M1 money supply and to "
        "inflation expectations significantly increase real oil prices; "
        "with the unadjusted M1 aggregate there is no significant effect of "
        "money supply shocks on real oil prices. Decomposition of "
        "historical oil price shocks shows a significant role played by "
        "inflation expectations and the money supply shocks during major "
        "oil shock episodes. These shocks partially replace roles "
        "previously attributed to the precautionary oil demand shock and "
        "the aggregate demand shock during the three major oil shock "
        "periods of the 1970s-1980s, post-2008 and during the 2020-2021 "
        "pandemic. The results show that both real oil price shocks and "
        "expected inflation shocks cause real GDP to fall."
    ),
    "benk-gillman-et-al-2005-red": (
        "The paper constructs credit shocks using data and the solution to "
        "a monetary business cycle model. The model extends the standard "
        "stochastic cash-in-advance economy by including the production of "
        "credit that serves as an alternative to money in exchange. Shocks "
        "to goods productivity, money, and credit productivity are "
        "constructed robustly using the solution to the model and quarterly "
        "US data on key variables. The contribution of the credit shock to "
        "US GDP movements is found, and this is interpreted in terms of "
        "changes in banking legislation during the US financial "
        "deregulation era. The results put forth the credit shock as a "
        "candidate shock that matters in determining GDP, including in the "
        "sense of Uhlig (2003)."
    ),
    "benk-gillman-et-al-2009-jedc": (
        "The paper shows that US GDP velocity of M1 money has exhibited "
        "long cycles around a 1.25% per year upward trend, during the "
        "1919-2004 period. It explains the velocity cycles through shocks "
        "constructed from a DSGE model and annual time series data. Model "
        "velocity is stable along the balanced growth path, which features "
        "endogenous growth and decentralized banking that produces exchange "
        "credit. Positive shocks to credit productivity and money supply "
        "increase velocity, as money demand falls, while a positive goods "
        "productivity shock raises temporary output and velocity. The paper "
        "explains velocity volatility at both business cycle and long run "
        "frequencies, with results suggesting that money and credit shocks "
        "appear to be more important for velocity during less stable times "
        "(such as the 1930s and 1987 crashes, and around 2003) and goods "
        "productivity shocks more important during stable times."
    ),
    "gillman-csabafi-et-al-2025-ecmod": (
        "The paper contributes new theory and econometric panel data "
        "estimation of output growth for twenty-one countries for annual "
        "data averaging almost four decades. Using the returns to human "
        "and physical capital that determine economic growth in the model, "
        "we specify the baseline econometric model with variables that "
        "most directly affect these returns. The inflation rate and the "
        "physical capital capacity utilization rate robustly result as the "
        "two main significant variables with opposite signs as expected "
        "from theory across a set of advanced panel econometric models "
        "using Mean Group and Common Correlated Effects. The theory-guided "
        "specification of the econometric model advances shows the "
        "importance of the return to capital in explaining economic growth. "
        "Using tax smoothing principles to interpret results implies that "
        "inflation surges detrimentally affect growth policies, so that "
        "more crisis financing of public debt by the private sector "
        "remains preferable but risks a tradeoff of lower capital "
        "utilization."
    ),
}
for slug, abstract in ABSTRACTS.items():
    p = load(slug)
    p["abstract"] = abstract
    save(slug, p)
print(f"abstracts set on {len(ABSTRACTS)} Benk papers")
