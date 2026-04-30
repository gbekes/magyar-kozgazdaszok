"""Populate the verbatim `abstract` field on Fülöp papers from IDEAS / WP fetches."""
import json
from pathlib import Path

PAPERS = Path(__file__).resolve().parent.parent / "data" / "papers"

ABSTRACTS = {
    "fulop-li-yu-2015-rfs": (
        "The paper proposes a self-exciting asset pricing model that takes into account "
        "co-jumps between prices and volatility and self-exciting jump clustering. We "
        "employ a Bayesian learning approach to implement real-time sequential analysis. "
        "We find evidence of self-exciting jump clustering since the 1987 market crash, "
        "and its importance becomes more obvious at the onset of the 2008 global "
        "financial crisis. We also find that learning affects the tail behaviors of the "
        "return distributions and has important implications for risk management, "
        "volatility forecasting, and option pricing."
    ),
    "duan-fulop-2009-jeconometrics": (
        "This paper extends the maximum likelihood estimation method for structural "
        "credit risk models developed by Duan (1994) to account for the fact that "
        "observed equity prices may have been contaminated by trading noises. The "
        "estimation method is implemented using a particle filtering algorithm. The "
        "method is applied to estimate the Merton (1974) structural credit risk model "
        "on the Dow Jones 30 firms and on 100 randomly selected firms. The results "
        "indicate that ignoring trading noises can lead to significantly over-estimating "
        "the firm's asset volatility. The estimated magnitude of trading noise is in "
        "line with the predictions of three standard liquidity proxies. A simulation "
        "study is also conducted to verify the performance of the proposed estimation "
        "method."
    ),
    "fulop-li-2013-jeconometrics": (
        "In state\u2013space models, parameter learning is practically difficult and is "
        "still an open issue. This paper proposes an efficient simulation-based "
        "parameter learning method. First, the approach breaks up the interdependence "
        "of the hidden states and the static parameters by marginalizing out the states "
        "using a particle filter. Second, it applies a Bayesian resample-move approach "
        "to this marginalized system. The methodology is generic and needs little "
        "design effort. Different from batch estimation methods, it provides posterior "
        "quantities necessary for full sequential inference and recursive model "
        "monitoring. The algorithm is implemented both on simulated data in a linear "
        "Gaussian model for illustration and comparison and on real data in a L\u00e9vy "
        "jump stochastic volatility model and a structural credit risk model."
    ),
    "duan-fulop-2015-jbes": (
        "We propose a density-tempered marginalized sequential Monte Carlo (SMC) "
        "sampler, a new class of samplers for full Bayesian inference of general "
        "state-space models. The dynamic states are approximately marginalized out "
        "using a particle filter, and the parameters are sampled via a sequential "
        "Monte Carlo sampler over a density-tempered bridge between the prior and the "
        "posterior. Our approach delivers exact draws from the joint posterior of the "
        "parameters and the latent states for any given number of state particles and "
        "is thus easily parallelizable in implementation. We also build into the "
        "proposed method a device that can automatically select a suitable number of "
        "state particles. Since the method incorporates sample information in a smooth "
        "fashion, it delivers good performance in the presence of outliers. We check "
        "the performance of the density-tempered SMC algorithm using simulated data "
        "based on a linear Gaussian state-space model with and without misspecification. "
        "We also apply it on real stock prices using a GARCH-type model with "
        "microstructure noise."
    ),
    "fulop-li-2019-jeconometrics": (
        "In dynamic asset pricing models, when the model structure becomes complex and "
        "derivatives data are introduced in estimation, traditional MCMC methods "
        "converge slowly, are difficult to design efficient proposals for parameters, "
        "and have large computational cost. We propose a two-stage sequential Monte "
        "Carlo sampler based on common random numbers and a smooth particle filter. "
        "This method is robust to potential model misspecification and can deliver "
        "almost full-likelihood-based inference at a much smaller computational cost. "
        "It is applied to estimate a class of volatility models that take into account "
        "price-volatility co-jumps, non-affineness, and self-excitation. An empirical "
        "study using S&P 500 index and variance swap rates shows that both "
        "non-affineness and self-excitation need to be introduced in modeling "
        "volatility dynamics."
    ),
    "wan-fulop-li-2022-jeconometrics": (
        "The paper examines statistical and economic evidence of out-of-sample bond "
        "return predictability for a real-time Bayesian investor who learns about "
        "parameters, hidden states, and predictive models over time. We find some "
        "statistical evidence using information contained in forward rates. However, "
        "such statistical predictability can hardly generate any economic value for "
        "investors. Furthermore, we find that strong statistical and economic evidence "
        "of bond return predictability from fully-revised macroeconomic data vanishes "
        "when real-time macroeconomic information is used. We also show that highly "
        "levered investments in bonds can improve short-run bond return predictability."
    ),
    "daures-lescourret-fulop-2022-jfm": (
        "We investigate liquidity changes in the credit default swap (CDS) market "
        "around two events that increased market transparency and standardization "
        "during the Great Financial Crisis: the dissemination of CDS positions starting "
        "in November 2008, and the implementation of the Small Bang in July 2009. We "
        "build an econometric model based on bid and ask quotes to measure liquidity "
        "in thinly traded CDSs. We find that, after the release of CDS positions, the "
        "market-wide deterioration in liquidity is less important for banks, consistent "
        "with information revelation alleviating systemic risk uncertainty. The Small "
        "Bang also improved liquidity, particularly for more illiquid CDSs."
    ),
    "fulop-heng-li-liu-2022-jeconometrics": (
        "We propose a likelihood-based Bayesian method that exploits up-to-date "
        "sequential Monte Carlo methods to efficiently estimate long-run risk models "
        "in which the conditional variance of consumption growth follows either an "
        "autoregressive (AR) process or an autoregressive gamma (ARG) process. We use "
        "the U.S. quarterly consumption and asset returns data from the postwar period "
        "to implement estimation. Our findings are: (1) informative priors on the "
        "preference parameters can help to improve model performance; (2) expected "
        "consumption growth has a very persistent component, whereas consumption "
        "volatility is less persistent; (3) while the ARG-based model performs better "
        "than the AR-based one statistically, the latter could fit asset returns "
        "better; and (4) the solution method matters more for estimation in the "
        "AR-based model than in the ARG-based model."
    ),
    "fulop-li-liu-yan-2025-mansci": (
        "We estimate and test long-run risk models using international macroeconomic "
        "and financial data. The benchmark model features a representative agent who "
        "has recursive preferences with a time preference shock, a persistent component "
        "in expected consumption growth, and stochastic volatility in fundamentals "
        "characterized by an autoregressive Gamma process. We construct a comprehensive "
        "dataset with quarterly frequency in the post-war period for ten developed "
        "countries and employ an efficient likelihood-based Bayesian method that "
        "exploits up-to-date sequential Monte Carlo methods to make full econometric "
        "inference. Our estimation provides international evidence in support of "
        "long-run risks, time-varying preference shocks, and countercyclicality of the "
        "stochastic discount factor."
    ),
    "fulop-kocsis-2023-jbf": (
        "This paper revisits the discussion about the role that fundamentals play in "
        "asset prices using sovereign credit spread data. We augment the standard "
        "macroeconomic proxy set by text-based measures of country and global "
        "fundamentals from a database of Reuters news articles between 2007 and 2016. "
        "We use a novel methodology that matches fundamental topic expressions and "
        "directly links them to tonality and geography information within the text. "
        "Our approach resolves several problems of extant text mining methods. We "
        "verify that our news indices capture fundamental information within news "
        "articles and are uncorrelated with measures of liquidity and investor "
        "sentiment. These news indices explain a large part of sovereign credit spread "
        "changes not captured by traditional fundamental proxies and thus support a "
        "significantly larger role for fundamentals. This additional information "
        "derives primarily from omitted expectations and concerns about global "
        "fundamentals. We also show that a large part of the covariance between the "
        "VIX index and sovereign spreads is related to these global fundamentals."
    ),
}

n = 0
for slug, abstract in ABSTRACTS.items():
    f = PAPERS / f"{slug}.json"
    p = json.loads(f.read_text(encoding="utf-8"))
    p["abstract"] = abstract
    f.write_text(json.dumps(p, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    n += 1
print(f"abstracts set on {n} Fülöp papers")
