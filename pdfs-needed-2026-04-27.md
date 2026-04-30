# PDFs needed for catalogue drafts — 2026-04-27

**247 papers** still need EN summary, and either lack an abstract in the catalogue JSON or have a known-bad one.

Grouped below by priority. For each, the slug is the file at `data/papers/<slug>.json`. Once you obtain the PDF, dropping the abstract text into that file (under `abstract`) is enough — Claude can then draft from there in the next session.

## Priority breakdown

| Group | Count | Note |
|---|---|---|
| **Flagged bad abstract** (re-fetch) | 9 | Already in catalogue; abstract is wrong (book-overall blurb / truncated / section list). Highest priority. |
| Tier A | 8 | Top general-interest journals + AEJ family. Very high policy value. |
| Tier B | 193 | Top field journals. Bulk of the work. |
| Tier C | 15 | Peer-reviewed but lower-tier; lower priority. |
| Tier B-hu | 0 | Hungarian-language outlets. |
| Off-list / chapters / WPs | 22 | Need editor decision — some may not warrant catalogue inclusion. |

## 1. Flagged bad-abstract — re-fetch (highest priority)

Each of these has a JSON entry but the `abstract` field is wrong (book-overall blurb, truncated, section list, or empty for a book review). Replacing the abstract with the actual paper abstract makes them immediately draftable.

- `vonyo-2021-jeh` · **Technology and the Environment in State-Socialist Hungary: An Economic History. By Viktor Pál. London: Palgrave Macmillan, 2017. Pp. xiv, 263. $151.53, cloth; $116.92, eBook.** · _vonyo-tamas_ · Journal of Economic History 2021 · [link](https://doi.org/10.1017/s0022050721000231)
- `acs-szerb-et-al-2014-regstud` · **The Regional Application of the Global Entrepreneurship and Development Index (GEDI): The Case of Spain** · _Zoltán J. Ács, szerb-laszlo, Raquel Ortega‐Argilés..._ · Regional Studies 2014 · [link](https://doi.org/10.1080/00343404.2014.888712)
- `ertl-2022-ksz` · **Méltányos és méltánytalan különbségek az egyéni döntéshozatalban** · _ertl-antal_ · Közgazdasági Szemle 2022 · [link](https://doi.org/10.18414/ksz.2022.10.1170)
- `csoka-havran-et-al-2016-ks` · **Konferencia a pénzügyi piacok likviditásáról. Sixth Annual Financial Market Liquidity Conference, 2015** · _csoka-peter, Dániel Havran, Kata Váradi_ · Közgazdasági Szemle 2016 · [link](https://doi.org/10.18414/ksz.2016.4.461)
- `vonyo-2018-cupe` · **Made in Germany: The Post-War Export Boom** · _vonyo-tamas_ · Cambridge University Press eBooks 2018 · [link](https://doi.org/10.1017/9781316414927.006)
- `csermely-harasztosi-et-al-2012-eepe` · **Opportunities and challenges – the impact of Chinese competition on Hungarian manufacturing** · _Ágnes Csermely, harasztosi-peter, Gábor Pellényi_ · Edward Elgar Publishing eBooks 2012 · [link](https://doi.org/10.4337/9781781009505.00019)
- `acs-szerb-2011-eepe` · **Entrepreneurship and Economic Development** · _Zoltán J. Ács, szerb-laszlo_ · Edward Elgar Publishing eBooks 2011 · [link](https://doi.org/10.4337/9781781001158.00008)
- `telegdy-2011-eepe` · **Corporate governance and the structure of ownership of Hungarian corporations** · _telegdy-almos_ · Edward Elgar Publishing eBooks 2011 · [link](https://doi.org/10.4337/9781849808293.00016)
- `brenton-manchin-2014-wssii` · **Making EU Trade Agreements Work: The Role of Rules of Origin** · _Paul Brenton, manchin-miriam_ · World Scientific Studies in International Economics 2014 · [link](https://doi.org/10.1142/9789814603386_0014)

## 2. Tier A — top general-interest + AEJ family

- `ambrus-greiner-2012-aer` · **Imperfect Public Monitoring with Costly Punishment: An Experimental Study** · _ambrus-attila, Ben Greiner_ · American Economic Review 2012
- `gierlinger-laczo-2018-ej` · **Matching to Share Risk without Commitment** · _Johannes Gierlinger, laczo-sarolta_ · Economic Journal 2018
- `greulich-laczo-marcet-2023-jpe` · **Pareto-Improving Optimal Capital and Labor Taxes** · _Katharina Greulich, laczo-sarolta, Albert Marcet_ · Journal of Political Economy 2023 · [link](https://www.journals.uchicago.edu/doi/10.1086/722982)
- `laczo-2015-jeea` · **Risk Sharing with Limited Commitment and Preference Heterogeneity: Structural Estimation and Testing** · _laczo-sarolta_ · Journal of the European Economic Association 2015 · [link](https://doi.org/10.1111/jeea.12115)
- `brodeur-et-al-2026-nature` · **Reproducibility and robustness of economics and political science research** · _Abel Brodeur, et al., gaspar-attila_ · Nature 2026
- `ambrus-chaney-salitskiy-2018-qe` · **Pirates of the Mediterranean: An Empirical Investigation of Bargaining with Asymmetric Information** · _ambrus-attila, Eric Chaney, Igor Salitskiy_ · Quantitative Economics 2018
- `ambrus-gao-milan-2022-restud` · **Informal Risk Sharing with Local Information** · _ambrus-attila, Wayne Yuan Gao, Pau Milán_ · Review of Economic Studies 2022
- `ambrus-takahashi-2008-te` · **Multi-Sender Cheap Talk with Restricted State Spaces** · _ambrus-attila, Satoru Takahashi_ · Theoretical Economics 2008

## 3. Tier B — top field journals (grouped by lead catalogue author)

### temesvary-judit (14 papers)

- `sapriza-temesvary-2024-jbf` · **Economic activity and the bank credit channel** · _Horacio Sapriza, temesvary-judit_ · Journal of Banking & Finance 2024 · [link](https://doi.org/10.1016/j.jbankfin.2024.107216)
- `temesvary-wei-2024-jimf` · **Domestic lending and the pandemic: How does banks’ exposure to COVID-19 abroad affect their lending in the United States?** · _temesvary-judit, Andrew Wei_ · Journal of International Money and Finance 2024 · [link](https://doi.org/10.1016/j.jimonfin.2024.103054)
- `passmore-temesvary-2022-jfs` · **How investor demands for safety influence bank capital and liquidity trade-offs** · _Wayne Passmore, temesvary-judit_ · Journal of Financial Stability 2022 · [link](https://doi.org/10.1016/j.jfs.2022.100987)
- `takats-temesvary-2021-jie` · **How does the interaction of macroprudential and monetary policies affect cross-border bank lending?** · _Előd Takáts, temesvary-judit_ · Journal of International Economics 2021 · [link](https://doi.org/10.1016/j.jinteco.2021.103521)
- `sapriza-temesvary-2020-eclett` · **Asymmetries in the bank lending channel of monetary policy in the United States** · _Horacio Sapriza, temesvary-judit_ · Economics Letters 2020 · [link](https://doi.org/10.1016/j.econlet.2020.109050)
- `takats-temesvary-2020-jie` · **The currency dimension of the bank lending channel in international monetary transmission** · _Előd Takáts, temesvary-judit_ · Journal of International Economics 2020 · [link](https://doi.org/10.1016/j.jinteco.2020.103309)
- `owen-temesvary-2018-frl` · **CEO compensation, pay inequality, and the gender diversity of bank board of directors** · _Ann L. Owen, temesvary-judit_ · Finance Research Letters 2018 · [link](https://doi.org/10.1016/j.frl.2018.10.010)
- `owen-temesvary-2018-jbf` · **The performance effects of gender diversity on bank boards** · _Ann L. Owen, temesvary-judit_ · Journal of Banking & Finance 2018 · [link](https://doi.org/10.1016/j.jbankfin.2018.02.015)
- `temesvary-2018-jfs` · **The transmission of foreign monetary policy shocks into the United States through foreign banks** · _temesvary-judit_ · Journal of Financial Stability 2018 · [link](https://doi.org/10.1016/j.jfs.2018.09.003)
- `temesvary-ongena-et-al-2018-jie` · **A global lending channel unplugged? Does U.S. monetary policy affect cross-border and affiliate lending by global U.S. banks?** · _temesvary-judit, Steven Ongena, Ann L. Owen_ · Journal of International Economics 2018 · [link](https://doi.org/10.1016/j.jinteco.2018.02.004)
- `temesvary-banai-2017-jimf` · **The drivers of foreign bank lending in Central and Eastern Europe: The roles of parent, subsidiary and host market traits** · _temesvary-judit, Ádám Banai_ · Journal of International Money and Finance 2017 · [link](https://doi.org/10.1016/j.jimonfin.2017.08.005)
- `temesvary-2015-ijio` · **Dynamic branching and interest rate competition of commercial banks: Evidence from Hungary** · _temesvary-judit_ · International Journal of Industrial Organization 2015 · [link](https://doi.org/10.1016/j.ijindorg.2015.09.003)
- `temesvary-2014-jbf` · **The determinants of U.S. banks’ international activities** · _temesvary-judit_ · Journal of Banking & Finance 2014 · [link](https://doi.org/10.1016/j.jbankfin.2014.04.014)
- `temesvary-2014-jimf` · **Foreign activities of U.S. banks since 1997: The roles of regulations and market conditions in crises and normal times** · _temesvary-judit_ · Journal of International Money and Finance 2014 · [link](https://doi.org/10.1016/j.jimonfin.2014.09.008)

### virag-gabor (10 papers)

- `cumbul-virag-2018-gaeb` · **Multilateral limit pricing in price-setting games** · _Eray Cumbul, virag-gabor_ · Games and Economic Behavior 2018 · [link](https://doi.org/10.1016/j.geb.2018.06.008)
- `galasso-mitchell-et-al-2017-rp` · **A theory of grand innovation prizes** · _Alberto Galasso, Matthew Mitchell, virag-gabor_ · Research Policy 2017 · [link](https://doi.org/10.1016/j.respol.2017.11.009)
- `virag-2016-gaeb` · **Auctions with resale: Reserve prices and revenues** · _virag-gabor_ · Games and Economic Behavior 2016 · [link](https://doi.org/10.1016/j.geb.2016.07.009)
- `galasso-mitchell-et-al-2016-ijio` · **Market outcomes and dynamic patent buyouts** · _Alberto Galasso, Matthew Mitchell, virag-gabor_ · International Journal of Industrial Organization 2016 · [link](https://doi.org/10.1016/j.ijindorg.2016.06.007)
- `virag-2011-ecth` · **First-price auctions with resale: the case of many bidders** · _virag-gabor_ · Economic Theory 2011 · [link](https://doi.org/10.1007/s00199-011-0666-y)
- `virag-2010-gaeb` · **High profit equilibria in directed search models** · _virag-gabor_ · Games and Economic Behavior 2010 · [link](https://doi.org/10.1016/j.geb.2010.08.006)
- `virag-2008-gaeb` · **Efficiency and competition in the long run: The survival of the unfit** · _virag-gabor_ · Games and Economic Behavior 2008 · [link](https://doi.org/10.1016/j.geb.2008.10.008)
- `raviv-virag-2008-ijio` · **Gambling by auctions** · _Yaron Raviv, virag-gabor_ · International Journal of Industrial Organization 2008 · [link](https://doi.org/10.1016/j.ijindorg.2008.10.005)
- `molnar-virag-2007-el` · **Revenue maximizing auctions with market interaction and signaling** · _József Molnár, virag-gabor_ · Economics Letters 2007 · [link](https://doi.org/10.1016/j.econlet.2007.08.010)
- `virag-2007-gaeb` · **Repeated common value auctions with asymmetric bidders** · _virag-gabor_ · Games and Economic Behavior 2007 · [link](https://doi.org/10.1016/j.geb.2007.01.001)

### csoka-peter (9 papers)

- `csoka-erb-et-al-2025-frl` · **Who is still in line? How bank beliefs drive fragility under runs** · _csoka-peter, Tamás Erb, kiss-hubert_ · Finance Research Letters 2025 · [link](https://doi.org/10.1016/j.frl.2025.109110)
- `csoka-herings-2019-gaeb` · **Liability games** · _csoka-peter, P. Jean‐Jacques Herings_ · Games and Economic Behavior 2019 · [link](https://doi.org/10.1016/j.geb.2019.05.007)
- `csoka-hever-2018-frl` · **Portfolio valuation under liquidity constraints with permanent price impact** · _csoka-peter, Judit Hevér_ · Finance Research Letters 2018 · [link](https://doi.org/10.1016/j.frl.2018.02.019)
- `balog-batyi-et-al-2016-ejoor` · **Properties and comparison of risk capital allocation methods** · _Dóra Balog, Tamás László Bátyi, csoka-peter..._ · European Journal of Operational Research 2016 · [link](https://doi.org/10.1016/j.ejor.2016.10.052)
- `csoka-2016-frl` · **Fair risk allocation in illiquid markets** · _csoka-peter_ · Finance Research Letters 2016 · [link](https://doi.org/10.1016/j.frl.2016.11.007)
- `csoka-herings-2014-jobf` · **Risk allocation under liquidity constraints** · _csoka-peter, P. Jean‐Jacques Herings_ · Journal of Banking & Finance 2014 · [link](https://doi.org/10.1016/j.jbankfin.2014.08.017)
- `csoka-herings-et-al-2010-ejor` · **Convex and exact games with non-transferable utility** · _csoka-peter, P. Jean‐Jacques Herings, koczy-laszlo..._ · European Journal of Operational Research 2010 · [link](https://doi.org/10.1016/j.ejor.2010.08.004)
- `csoka-herings-et-al-2008-geb` · **Stable allocations of risk** · _csoka-peter, P. Jean‐Jacques Herings, koczy-laszlo_ · Games and Economic Behavior 2008 · [link](https://doi.org/10.1016/j.geb.2008.11.001)
- `csoka-herings-et-al-2007-jbf` · **Coherent measures of risk from a general equilibrium perspective** · _csoka-peter, P. Jean‐Jacques Herings, koczy-laszlo_ · Journal of Banking & Finance 2007 · [link](https://doi.org/10.1016/j.jbankfin.2006.10.026)

### ambrus-attila (8 papers)

- `ambrus-greiner-zednik-2025-jpube` · **The Effect of a 'None of the Above' Ballot Paper Option on Voting Behavior and Election Outcomes** · _ambrus-attila, Ben Greiner, Anita Zednik_ · Journal of Public Economics 2025
- `ambrus-greiner-2019-jpube` · **Individual, Dictator, and Democratic punishment in public good games with perfect and imperfect observability** · _ambrus-attila, Ben Greiner_ · Journal of Public Economics 2019 · [link](https://doi.org/10.1016/j.jpubeco.2019.104053)
- `ambrus-egorov-2017-jet` · **Delegation and nonmonetary incentives** · _ambrus-attila, Georgy Egorov_ · Journal of Economic Theory 2017 · [link](https://doi.org/10.1016/j.jet.2017.06.002)
- `ambrus-greiner-et-al-2017-jpube` · **The case for nil votes: Voter behavior under asymmetric information in compulsory and voluntary voting systems** · _ambrus-attila, Ben Greiner, Anne Sastro_ · Journal of Public Economics 2017 · [link](https://doi.org/10.1016/j.jpubeco.2017.08.006)
- `ambrus-lu-2014-gaeb` · **Almost fully revealing cheap talk with imperfectly informed senders** · _ambrus-attila, Shih En Lu_ · Games and Economic Behavior 2014 · [link](https://doi.org/10.1016/j.geb.2014.09.001)
- `ambrus-azevedo-et-al-2013-joebo` · **Legislative committees as information intermediaries: A unified theory of committee selection and amendment rules** · _ambrus-attila, Eduardo M. Azevedo, Yuichiro Kamada..._ · Journal of Economic Behavior & Organization 2013 · [link](https://doi.org/10.1016/j.jebo.2013.08.003)
- `ambrus-pathak-2010-jpube` · **Cooperation over finite horizons: A theory and experiments** · _ambrus-attila, Parag A. Pathak_ · Journal of Public Economics 2011 · [link](https://doi.org/10.1016/j.jpubeco.2010.11.016)
- `ambrus-2008-jet` · **Theories of coalitional rationality** · _ambrus-attila_ · Journal of Economic Theory 2008 · [link](https://doi.org/10.1016/j.jet.2007.03.010)

### bekes-gabor (7 papers)

- `bekes-murakozy-2018-rowe` · **The ladder of internationalization modes: evidence from European firms** · _bekes-gabor, murakozy-balazs_ · Review of World Economics 2018 · [link](https://doi.org/10.1007/s10290-018-0305-9)
- `bekes-fontagne-et-al-2017-rowe` · **Shipment frequency of exporters and demand uncertainty** · _bekes-gabor, Lionel Fontagné, murakozy-balazs..._ · Review of World Economics 2017 · [link](https://doi.org/10.1007/s10290-017-0286-0)
- `bekes-harasztosi-2017-taors` · **Grid and shake: spatial aggregation and the robustness of regionally estimated elasticities** · _bekes-gabor, harasztosi-peter_ · The Annals of Regional Science 2017 · [link](https://doi.org/10.1007/s00168-017-0849-y)
- `bekes-murakozy-2015-el` · **Measuring productivity premia with many modes of internationalization** · _bekes-gabor, murakozy-balazs_ · Economics Letters 2015 · [link](https://doi.org/10.1016/j.econlet.2015.12.016)
- `bekes-murakozy-2012-jie` · **Temporary trade and heterogeneous firms** · _bekes-gabor, murakozy-balazs_ · Journal of International Economics 2012 · [link](https://doi.org/10.1016/j.jinteco.2011.12.007)
- `bekes-harasztosi-2012-rsue` · **Agglomeration premium and trading activity of firms** · _bekes-gabor, harasztosi-peter_ · Regional Science and Urban Economics 2012 · [link](https://doi.org/10.1016/j.regsciurbeco.2012.11.004)
- `bekes-murakozy-et-al-2011-es` · **Firms and products in international trade: Evidence from Hungary** · _bekes-gabor, murakozy-balazs, harasztosi-peter_ · Economic Systems 2011 · [link](https://doi.org/10.1016/j.ecosys.2010.11.005)

### koczy-laszlo (6 papers)

- `koczy-sziklai-2018-orl` · **Bounds on Malapportionment** · _koczy-laszlo, sziklai-balazs_ · Operations Research Letters 2018 · [link](https://doi.org/10.1016/j.orl.2018.03.002)
- `koczy-2015-jmathe` · **Stationary consistent equilibrium coalition structures constitute the recursive core** · _koczy-laszlo_ · Journal of Mathematical Economics 2015 · [link](https://doi.org/10.1016/j.jmateco.2015.08.006)
- `koczy-nichifor-2012-ecth` · **The intellectual influence of economic journals: quality versus quantity** · _koczy-laszlo, Alexandru Nichifor_ · Economic Theory 2012 · [link](https://doi.org/10.1007/s00199-012-0708-0)
- `koczy-2008-geb` · **Sequential coalition formation and the core in the presence of externalities** · _koczy-laszlo_ · Games and Economic Behavior 2008 · [link](https://doi.org/10.1016/j.geb.2008.04.002)
- `koczy-2006-jmathe` · **The core can be accessed with a bounded number of blocks** · _koczy-laszlo_ · Journal of Mathematical Economics 2006 · [link](https://doi.org/10.1016/j.jmateco.2006.09.002)
- `koczy-lauwers-2003-geb` · **The coalition structure core is accessible** · _koczy-laszlo, Luc Lauwers_ · Games and Economic Behavior 2003 · [link](https://doi.org/10.1016/j.geb.2003.06.006)

### koszegi-botond (6 papers)

- `heidhues-koszegi-2015-roio` · **On the Welfare Costs of Naiveté in the US Credit-Card Market** · _Paul Heidhues, koszegi-botond_ · Review of Industrial Organization 2015 · [link](https://doi.org/10.1007/s11151-015-9473-0)
- `koszegi-2009-ecth` · **Utility from anticipation and personal equilibrium** · _koszegi-botond_ · Economic Theory 2009 · [link](https://doi.org/10.1007/s00199-009-0465-x)
- `koszegi-rabin-2008-jpube` · **Choices, situations, and happiness** · _koszegi-botond, Matthew Rabin_ · Journal of Public Economics 2008 · [link](https://doi.org/10.1016/j.jpubeco.2008.03.010)
- `koszegi-2003-jhe` · **Health anxiety and patient behavior** · _koszegi-botond_ · Journal of Health Economics 2003 · [link](https://doi.org/10.1016/j.jhealeco.2003.06.002)
- `gruber-koszegi-2003-jpube` · **Tax incidence when individuals are time-inconsistent: the case of cigarette excise taxes** · _Jonathan Gruber, koszegi-botond_ · Journal of Public Economics 2003 · [link](https://doi.org/10.1016/j.jpubeco.2003.06.001)
- `dia-mond-koszegi-2002-jpube` · **Quasi-hyperbolic discounting and retirement** · _Peter Dia­mond, koszegi-botond_ · Journal of Public Economics 2002 · [link](https://doi.org/10.1016/s0047-2727(02)00041-5)

### ujhelyi-gergely (6 papers)

- `szabo-ujhelyi-2024-jpube` · **National parks and economic development** · _Andrea Szabó, ujhelyi-gergely_ · Journal of Public Economics 2024 · [link](https://doi.org/10.1016/j.jpubeco.2024.105073)
- `szabo-ujhelyi-2017-el` · **Choice and happiness in South Africa** · _Andrea Szabó, ujhelyi-gergely_ · Economics Letters 2017 · [link](https://doi.org/10.1016/j.econlet.2017.02.002)
- `szabo-ujhelyi-2015-jde` · **Reducing nonpayment for public utilities: Experimental evidence from South Africa** · _Andrea Szabó, ujhelyi-gergely_ · Journal of Development Economics 2015 · [link](https://doi.org/10.1016/j.jdeveco.2015.06.002)
- `juhn-ujhelyi-et-al-2013-jde` · **Men, women, and machines: How trade impacts gender inequality** · _Chinhui Juhn, ujhelyi-gergely, Carolina Villegas‐Sánchez_ · Journal of Development Economics 2013 · [link](https://doi.org/10.1016/j.jdeveco.2013.09.009)
- `ujhelyi-2008-jpube` · **Campaign finance regulation with competing interest groups** · _ujhelyi-gergely_ · Journal of Public Economics 2008 · [link](https://doi.org/10.1016/j.jpubeco.2008.09.009)
- `fredriksson-neumayer-et-al-2007-pc` · **Kyoto Protocol cooperation: Does government corruption facilitate environmental lobbying?** · _Per G. Fredriksson, Eric Neumayer, ujhelyi-gergely_ · Public Choice 2007 · [link](https://doi.org/10.1007/s11127-007-9187-4)

### eso-peter (6 papers)

- `chung-eso-2013-el` · **Persuasion and learning by countersignaling** · _Kim‐Sau Chung, eso-peter_ · Economics Letters 2013 · [link](https://doi.org/10.1016/j.econlet.2013.10.002)
- `eso-galambos-2012-ijogt` · **Disagreement and evidence production in strategic information transmission** · _eso-peter, Ádám Galambos_ · International Journal of Game Theory 2012 · [link](https://doi.org/10.1007/s00182-012-0344-8)
- `eso-schummer-2009-ijogt` · **Credible deviations from signaling equilibria** · _eso-peter, James Schummer_ · International Journal of Game Theory 2009 · [link](https://doi.org/10.1007/s00182-009-0161-x)
- `eso-2004-jet` · **An optimal auction with correlated values and risk aversion** · _eso-peter_ · Journal of Economic Theory 2004 · [link](https://doi.org/10.1016/j.jet.2004.06.005)
- `eso-schummer-2003-gaeb` · **Bribing and signaling in second price auctions** · _eso-peter, James Schummer_ · Games and Economic Behavior 2003 · [link](https://doi.org/10.1016/j.geb.2003.06.005)
- `eso-futo-1999-el` · **Auction design with a risk averse seller** · _eso-peter, Gábor Futó_ · Economics Letters 1999 · [link](https://doi.org/10.1016/s0165-1765(99)00115-9)

### simonovits-andras (6 papers)

- `garay-simonovits-et-al-2011-eclett` · **Local interaction in tax evasion** · _Barnabás M. Garay, simonovits-andras, István János Tóth_ · Economics Letters 2011 · [link](https://doi.org/10.1016/j.econlet.2011.12.066)
- `simonovits-2011-eclett` · **When are voluntary pensions indifferent?** · _simonovits-andras_ · Economics Letters 2011 · [link](https://doi.org/10.1016/j.econlet.2011.01.031)
- `molnar-simonovits-1998-jedc` · **Expectations, (in)stability and (in)viability in realistic overlapping cohorts models** · _József Molnár, simonovits-andras_ · Journal of Economic Dynamics and Control 1998 · [link](https://doi.org/10.1016/s0165-1889(97)00121-8)
- `hommes-nusse-et-al-1995-jedc` · **Cycles and chaos in a socialist economy** · _Cars Hommes, Helena E. Nusse, simonovits-andras_ · Journal of Economic Dynamics and Control 1995 · [link](https://doi.org/10.1016/0165-1889(93)00778-3)
- `simonovits-1991-jce` · **Investments, starts, and cycles in socialist economies: A mathematical model** · _simonovits-andras_ · Journal of Comparative Economics 1991 · [link](https://doi.org/10.1016/0147-5967(91)90026-p)
- `simonovits-1981-jedc` · **Maximal convergence speed of decentralized control** · _simonovits-andras_ · Journal of Economic Dynamics and Control 1981 · [link](https://doi.org/10.1016/0165-1889(81)90004-x)

### biro-aniko (6 papers)

- `biro-prinz-et-al-2022-jpube` · **The minimum wage, informal pay, and tax enforcement** · _biro-aniko, prinz-daniel, László Sándor_ · Journal of Public Economics 2022 · [link](https://doi.org/10.1016/j.jpubeco.2022.104728)
- `biro-prinz-2020-hp` · **Healthcare spending inequality: Evidence from Hungarian administrative data** · _biro-aniko, prinz-daniel_ · Health Policy 2020 · [link](https://doi.org/10.1016/j.healthpol.2020.01.006)
- `biro-hellowell-2016-hp` · **Public–private sector interactions and the demand for supplementary health insurance in the United Kingdom** · _biro-aniko, Mark Hellowell_ · Health Policy 2016 · [link](https://doi.org/10.1016/j.healthpol.2016.05.002)
- `biro-2013-ee` · **Supplementary private health insurance and health care utilization of people aged 50+** · _biro-aniko_ · Empirical Economics 2013 · [link](https://doi.org/10.1007/s00181-013-0689-2)
- `biro-2013-hp` · **Copayments, gatekeeping, and the utilization of outpatient public and private care at age 50 and above in Europe** · _biro-aniko_ · Health Policy 2013 · [link](https://doi.org/10.1016/j.healthpol.2013.03.009)
- `biro-2012-jope` · **Subjective mortality hazard shocks and the adjustment of consumption expenditures** · _biro-aniko_ · Journal of Population Economics 2012 · [link](https://doi.org/10.1007/s00148-012-0461-5)

### danis-andras (6 papers)

- `danis-gamba-2023-ms` · **Dark Knights: The Rise in Firm Intervention by CDS Investors** · _danis-andras, Andrea Gamba_ · Management Science 2023
- `danis-2020-frl-shareholder-monitoring` · **Shareholder Monitoring with Strategic Investors** · _danis-andras_ · Finance Research Letters 2020 · [link](https://doi.org/10.1016/j.frl.2019.06.007)
- `chava-danis-hsu-2020-jfe` · **The Impact of Right-to-Work Laws on Worker Wages: Evidence from Collective Bargaining Agreements** · _Sudheer Chava, danis-andras, Alex Hsu_ · Journal of Financial Economics 2020
- `danis-gamba-2018-jfe` · **The Real Effects of Credit Default Swaps** · _danis-andras, Andrea Gamba_ · Journal of Financial Economics 2018
- `danis-2017-ms` · **Do Empty Creditors Matter? Evidence from Distressed Exchange Offers** · _danis-andras_ · Management Science 2017
- `danis-rettl-whited-2014-jfe` · **Refinancing, Profitability, and Capital Structure** · _danis-andras, Daniel Rettl, Toni Whited_ · Journal of Financial Economics 2014

### szentes-balazs (6 papers)

- `doval-szentes-2024-gaeb` · **On the efficiency of queueing in dynamic matching markets** · _Laura Doval, szentes-balazs_ · Games and Economic Behavior 2024 · [link](https://doi.org/10.1016/j.geb.2024.11.019)
- `garrett-georgiadis-et-al-2023-jet` · **Optimal technology design** · _Daniel F. Garrett, George Georgiadis, Alex Smolin..._ · Journal of Economic Theory 2023 · [link](https://doi.org/10.1016/j.jet.2023.105621)
- `robatto-szentes-2017-jet` · **On the biological foundation of risk preferences** · _Roberto Robatto, szentes-balazs_ · Journal of Economic Theory 2017 · [link](https://doi.org/10.1016/j.jet.2017.10.002)
- `gershkov-szentes-2008-jet` · **Optimal voting schemes with costly information acquisition** · _Alex Gershkov, szentes-balazs_ · Journal of Economic Theory 2008 · [link](https://doi.org/10.1016/j.jet.2008.02.004)
- `szentes-2004-jet` · **Equilibrium transformations and the Revenue Equivalence Theorem** · _szentes-balazs_ · Journal of Economic Theory 2004 · [link](https://doi.org/10.1016/j.jet.2003.11.001)
- `szentes-rosenthal-2003-gaeb` · **Three-object two-bidder simultaneous auctions: chopsticks and tetrahedra** · _szentes-balazs, Robert W. Rosenthal_ · Games and Economic Behavior 2003 · [link](https://doi.org/10.1016/s0899-8256(02)00530-4)

### telegdy-almos (5 papers)

- `goel-telegdy-et-al-2024-jocf` · **Subsidy-driven firm growth: Does loan history matter? Evidence from a European Union subsidy program** · _Tirupam Goel, telegdy-almos, Ádám Banai..._ · Journal of Corporate Finance 2024 · [link](https://doi.org/10.1016/j.jcorpfin.2024.102592)
- `telegdy-2023-el` · **The effects of enterprise relief grants during COVID-19** · _telegdy-almos_ · Economics Letters 2023 · [link](https://doi.org/10.1016/j.econlet.2023.111482)
- `telegdy-2018-labec` · **Public wage spillovers: The role of individual characteristics and employer wage policies** · _telegdy-almos_ · Labour Economics 2018 · [link](https://doi.org/10.1016/j.labeco.2018.08.008)
- `brown-earle-et-al-2006-ces` · **Nonstandard Forms and Measures of Employment and Unemployment in Transition: A Comparative Study of Estonia, Romania, and Russia** · _Jason Brown, John S. Earle, Vladimir Gimpelson..._ · Comparative Economic Studies 2006 · [link](https://doi.org/10.1057/palgrave.ces.8100181)
- `earle-telegdy-2002-joce` · **Privatization Methods and Productivity Effects in Romanian Industrial Enterprises** · _John S. Earle, telegdy-almos_ · Journal of Comparative Economics 2002 · [link](https://doi.org/10.1006/jcec.2002.1798)

### benk-szilard (5 papers)

- `gillman-csabafi-et-al-2025-ecmod` · **Revisiting neoclassical growth theory: A primary role for inflation and capacity utilization** · _Max Gillman, Tamas Csabafi, benk-szilard..._ · Economic Modelling 2025 · [link](https://doi.org/10.1016/j.econmod.2025.107358)
- `benk-gillman-2023-enerecon` · **Identifying money and inflation expectation shocks to real oil prices** · _benk-szilard, Max Gillman_ · Energy Economics 2023 · [link](https://doi.org/10.1016/j.eneco.2023.106878)
- `benk-gillman-2019-jimf` · **Granger predictability of oil prices after the Great Recession** · _benk-szilard, Max Gillman_ · Journal of International Money and Finance 2019 · [link](https://doi.org/10.1016/j.jimonfin.2019.102100)
- `benk-gillman-et-al-2009-jedc` · **A banking explanation of the US velocity of money: 1919–2004** · _benk-szilard, Max Gillman, Michal Kejak_ · Journal of Economic Dynamics and Control 2009 · [link](https://doi.org/10.1016/j.jedc.2009.11.005)
- `benk-gillman-et-al-2005-red` · **Credit shocks in the financial deregulatory era: Not the usual suspects** · _benk-szilard, Max Gillman, Michal Kejak_ · Review of Economic Dynamics 2005 · [link](https://doi.org/10.1016/j.red.2005.01.012)

### valentinyi-akos (5 papers)

- `duernecker-herrendorf-et-al-2021-joeda` · **The productivity growth slowdown and Kaldor’s growth facts** · _Georg Duernecker, Berthold Herrendorf, valentinyi-akos_ · Journal of Economic Dynamics and Control 2021 · [link](https://doi.org/10.1016/j.jedc.2021.104200)
- `luintel-matthews-et-al-2020-em` · **The role of Provincial Government Spending Composition in growth and convergence in China** · _Kul B. Luintel, Kent Matthews, Lucy Minford..._ · Economic Modelling 2020 · [link](https://doi.org/10.1016/j.econmod.2020.04.024)
- `valentinyi-herrendorf-2008-roed` · **Measuring factor income shares at the sectoral level** · _valentinyi-akos, Berthold Herrendorf_ · Review of Economic Dynamics 2008 · [link](https://doi.org/10.1016/j.red.2008.02.003)
- `herrendorf-valentinyi-2005-joeda` · **On the stability of the two-sector neoclassical growth model with externalities** · _Berthold Herrendorf, valentinyi-akos_ · Journal of Economic Dynamics and Control 2005 · [link](https://doi.org/10.1016/j.jedc.2005.05.006)
- `herrendorf-valentinyi-2003-roed` · **Determinacy through intertemporal capital adjustment costs** · _Berthold Herrendorf, valentinyi-akos_ · Review of Economic Dynamics 2003 · [link](https://doi.org/10.1016/s1094-2025(03)00020-6)

### tobias-aron (5 papers)

- `tobias-2022-gaeb` · **Equilibrium non-existence in generalized games** · _tobias-aron_ · Games and Economic Behavior 2022 · [link](https://doi.org/10.1016/j.geb.2022.06.012)
- `tobias-2021-ijogt` · **Meet meets join: the interaction between pooled and common knowledge** · _tobias-aron_ · International Journal of Game Theory 2021 · [link](https://doi.org/10.1007/s00182-021-00778-w)
- `tobias-2020-tad` · **A unified epistemological theory of information processing** · _tobias-aron_ · Theory and Decision 2020 · [link](https://doi.org/10.1007/s11238-020-09769-x)
- `tobias-2018-gaeb` · **Non-linear pricing and optimal shipping policies** · _tobias-aron_ · Games and Economic Behavior 2018 · [link](https://doi.org/10.1016/j.geb.2018.08.008)
- `tobias-2015-jpube` · **Income Redistribution in Open Economies** · _tobias-aron_ · Journal of Public Economics 2015 · [link](https://doi.org/10.1016/j.jpubeco.2015.12.005)

### abraham-arpad (5 papers)

- `abraham-cavalcanti-2015-tbejo` · **Preface to “Reflections on Macroeconometric Modeling” by Ray C. Fair** · _abraham-arpad, Tiago Cavalcanti_ · The B.E. Journal of Macroeconomics 2015 · [link](https://doi.org/10.1515/bejm-2014-0144)
- `abraham-koehne-et-al-2011-jet` · **On the first-order approach in principal–agent models with hidden borrowing and lending** · _abraham-arpad, Sebastian Koehne, Nicola Pavoni_ · Journal of Economic Theory 2011 · [link](https://doi.org/10.1016/j.jet.2011.03.002)
- `abraham-carceles-poveda-2009-jet` · **Endogenous trading constraints with incomplete asset markets** · _abraham-arpad, Eva Cárceles‐Poveda_ · Journal of Economic Theory 2009 · [link](https://doi.org/10.1016/j.jet.2009.10.006)
- `abraham-pavoni-2008-roed` · **Efficient allocations with moral hazard and hidden borrowing and lending: A recursive formulation** · _abraham-arpad, Nicola Pavoni_ · Review of Economic Dynamics 2008 · [link](https://doi.org/10.1016/j.red.2008.05.001)
- `abraham-2007-jme` · **Comment on: “Altruism, incomplete markets, and tax reform” by Fuster, İmrohoroğlu and İmrohoroğlu** · _abraham-arpad_ · Journal of Monetary Economics 2007 · [link](https://doi.org/10.1016/j.jmoneco.2007.11.009)

### szerb-laszlo (5 papers)

- `acs-song-et-al-2021-sbe` · **The evolution of the global digital platform economy: 1971–2021** · _Zoltán J. Ács, Abraham K. Song, szerb-laszlo..._ · Small Business Economics 2021 · [link](https://doi.org/10.1007/s11187-021-00561-x)
- `lafuente-szerb-et-al-2015-jtt` · **Country level efficiency and national systems of entrepreneurship: a data envelopment analysis approach** · _Esteban Lafuente, szerb-laszlo, Zoltán J. Ács_ · Journal of Technology Transfer 2015 · [link](https://doi.org/10.1007/s10961-015-9440-9)
- `acs-autio-et-al-2013-rp` · **National Systems of Entrepreneurship: Measurement issues and policy implications** · _Zoltán J. Ács, Erkko Autio, szerb-laszlo_ · Research Policy 2013 · [link](https://doi.org/10.1016/j.respol.2013.08.016)
- `acs-o-gorman-et-al-2007-sbe` · **Could the Irish Miracle be Repeated in Hungary?** · _Zoltán J. Ács, Colm O’Gorman, szerb-laszlo..._ · Small Business Economics 2007 · [link](https://doi.org/10.1007/s11187-006-9027-9)
- `acs-szerb-2006-sbe` · **Entrepreneurship, Economic Growth and Public Policy** · _Zoltán J. Ács, szerb-laszlo_ · Small Business Economics 2006 · [link](https://doi.org/10.1007/s11187-006-9012-3)

### sziklai-balazs (4 papers)

- `segal-halevi-sziklai-2018-ecth` · **Monotonicity and competitive equilibrium in cake-cutting** · _Erel Segal-Halevi, sziklai-balazs_ · Economic Theory 2018 · [link](https://doi.org/10.1007/s00199-018-1128-6)
- `sziklai-2017-ijogt` · **How to identify experts in a community?** · _sziklai-balazs_ · International Journal of Game Theory 2017 · [link](https://doi.org/10.1007/s00182-017-0582-x)
- `sziklai-fleiner-et-al-2016-mathprog` · **On the core and nucleolus of directed acyclic graph games** · _sziklai-balazs, fleiner-tamas, Tamás Solymosi_ · Mathematical Programming 2016 · [link](https://doi.org/10.1007/s10107-016-1062-y)
- `solymosi-sziklai-2016-orl` · **Characterization sets for the nucleolus in balanced games** · _Tamás Solymosi, sziklai-balazs_ · Operations Research Letters 2016 · [link](https://doi.org/10.1016/j.orl.2016.05.014)

### manchin-miriam (4 papers)

- `manchin-orazbayev-2018-wd` · **Social networks and the intention to migrate** · _manchin-miriam, Sultan Orazbayev_ · World Development 2018 · [link](https://doi.org/10.1016/j.worlddev.2018.05.011)
- `francois-manchin-2013-wd` · **Institutions, Infrastructure, and Trade** · _Joseph François, manchin-miriam_ · World Development 2013 · [link](https://doi.org/10.1016/j.worlddev.2013.02.009)
- `bekkers-francois-et-al-2012-eer` · **Import prices, income, and inequality** · _Eddy Bekkers, Joseph François, manchin-miriam_ · European Economic Review 2012 · [link](https://doi.org/10.1016/j.euroecorev.2012.02.005)
- `hijzen-gorg-et-al-2007-eer` · **Cross-border mergers and acquisitions and the role of trade costs** · _Alexander Hijzen, Holger Görg, manchin-miriam_ · European Economic Review 2007 · [link](https://doi.org/10.1016/j.euroecorev.2007.07.002)

### lieli-robert (4 papers)

- `lieli-stinchcombe-et-al-2019-ijof` · **Unrestricted and controlled identification of loss functions: Possibility and impossibility results** · _lieli-robert, Maxwell B. Stinchcombe, Viola M. Grolmusz_ · International Journal of Forecasting 2019 · [link](https://doi.org/10.1016/j.ijforecast.2018.11.007)
- `khan-lieli-2018-ijof` · **Information flow between prediction markets, polls and media: Evidence from the 2008 presidential primaries** · _Urmee Khan, lieli-robert_ · International Journal of Forecasting 2018 · [link](https://doi.org/10.1016/j.ijforecast.2018.04.002)
- `elliott-lieli-2013-joem` · **Predicting binary outcomes** · _Graham Elliott, lieli-robert_ · Journal of Econometrics 2013 · [link](https://doi.org/10.1016/j.jeconom.2013.01.003)
- `lieli-white-2009-joem` · **The construction of empirical credit scoring rules based on maximization principles** · _lieli-robert, Halbert White_ · Journal of Econometrics 2009 · [link](https://doi.org/10.1016/j.jeconom.2009.10.028)

### darvas-zsolt (3 papers)

- `darvas-2019-wd` · **Global interpersonal income inequality decline: The role of China and India** · _darvas-zsolt_ · World Development 2019 · [link](https://doi.org/10.1016/j.worlddev.2019.04.011)
- `darvas-2015-eclett` · **Does money matter in the euro area? Evidence from a new Divisia index** · _darvas-zsolt_ · Economics Letters 2015 · [link](https://doi.org/10.1016/j.econlet.2015.05.034)
- `darvas-2008-jbf` · **Leveraged carry trade portfolios** · _darvas-zsolt_ · Journal of Banking & Finance 2008 · [link](https://doi.org/10.1016/j.jbankfin.2008.10.007)

### harasztosi-peter (3 papers)

- `teruel-coad-et-al-2021-tjott` · **The birth of new HGEs: internationalization through new digital technologies** · _Mercedes Teruel, Alex Coad, Clemens Domnick..._ · Journal of Technology Transfer 2021 · [link](https://doi.org/10.1007/s10961-021-09861-6)
- `cede-chiriacescu-et-al-2018-rowe` · **Export characteristics and output volatility: comparative firm-level evidence for CEE countries** · _Urška Čede, Bogdan Chiriacescu, harasztosi-peter..._ · Review of World Economics 2018 · [link](https://doi.org/10.1007/s10290-018-0312-x)
- `harasztosi-2015-ee` · **Export spillovers in Hungary** · _harasztosi-peter_ · Empirical Economics 2015 · [link](https://doi.org/10.1007/s00181-015-0965-4)

### halpern-laszlo (3 papers)

- `dobrinsky-korosi-et-al-2006-joce` · **Price markups and returns to scale in imperfect markets: Bulgaria and Hungary** · _Rumen Dobrinsky, Gábor Kőrösi, Nikolay Markov..._ · Journal of Comparative Economics 2006 · [link](https://doi.org/10.1016/j.jce.2005.11.006)
- `egert-halpern-2005-jobf` · **Equilibrium exchange rates in Central and Eastern Europe: A meta-regression analysis** · _Balázs Égert, halpern-laszlo_ · Journal of Banking & Finance 2005 · [link](https://doi.org/10.1016/j.jbankfin.2005.07.001)
- `halpern-piazolo-et-al-1998-rowe` · **Book reviews** · _halpern-laszlo, Daniel Piazolo, Horst Siebert..._ · Review of World Economics 1998 · [link](https://doi.org/10.1007/bf02707931)

### kiss-hubert (3 papers)

- `kiss-rodriguez-lara-et-al-2015-jbee` · **Think twice before running! Bank runs and cognitive abilities** · _kiss-hubert, Ismael Rodríguez-Lara, Alfonso Rosa-García_ · Journal of Behavioral and Experimental Economics 2015 · [link](https://doi.org/10.1016/j.socec.2015.01.006)
- `kiss-rodriguez-lara-et-al-2014-jbee` · **Do women panic more than men? An experimental study of financial decisions** · _kiss-hubert, Ismael Rodríguez-Lara, Alfonso Rosa-García_ · Journal of Behavioral and Experimental Economics 2014 · [link](https://doi.org/10.1016/j.socec.2014.06.003)
- `kiss-rodriguez-lara-et-al-2014-joebo` · **Do social networks prevent or promote bank runs?** · _kiss-hubert, Ismael Rodríguez-Lara, Alfonso Rosa-García_ · Journal of Economic Behavior & Organization 2014 · [link](https://doi.org/10.1016/j.jebo.2014.01.019)

### loranth-gyongyi (3 papers)

- `arping-loranth-et-al-2009-jofs` · **Public initiatives to support entrepreneurs: Credit guarantees versus co-funding** · _Stefan Arping, loranth-gyongyi, Alan D. Morrison_ · Journal of Financial Stability 2009 · [link](https://doi.org/10.1016/j.jfs.2009.05.009)
- `freixas-loranth-et-al-2007-jofi` · **Regulating financial conglomerates** · _Xavier Freixas, loranth-gyongyi, Alan D. Morrison_ · Journal of Financial Intermediation 2007 · [link](https://doi.org/10.1016/j.jfi.2007.03.004)
- `calzolari-loranth-2005-jofi` · **Regulation of Multinational Banks: A Theoretical Inquiry** · _Giacomo Calzolari, loranth-gyongyi_ · Journal of Financial Intermediation 2005 · [link](https://doi.org/10.1016/j.jfi.2010.02.002)

### elekes-zoltan (2 papers)

- `elekes-2024-rs-resilience` · **Regional resilience and the network structure of inter-industry labour flows** · _elekes-zoltan_ · Regional Studies 2024
- `elekes-stojkoski-et-al-2022-eg` · **Technology Network Structure Conditions the Economic Resilience of Regions** · _elekes-zoltan_ · Economic Geography 2022

### bako-barna (2 papers)

- `bako-kalecz-simon-2013-eclett` · **Quota bonuses with heterogeneous agents** · _bako-barna, András Kálecz‐Simon_ · Economics Letters 2013 · [link](https://doi.org/10.1016/j.econlet.2013.03.008)
- `bako-kalecz-simon-2012-eclett` · **Price discrimination in asymmetric Cournot oligopoly** · _bako-barna, András Kálecz‐Simon_ · Economics Letters 2012 · [link](https://doi.org/10.1016/j.econlet.2012.03.016)

### szabo-morvai-agnes (2 papers)

- `szabo-lovasz-2023-ee` · **Where can childcare expansion increase maternal labor supply? A comparison of quasi-experimental estimates from seven countries** · _szabo-morvai-agnes, Anna Lovász_ · Empirical Economics 2023 · [link](https://doi.org/10.1007/s00181-023-02531-6)
- `lovasz-szabo-2018-ee` · **Childcare availability and maternal labor supply in a setting of high potential impact** · _Anna Lovász, szabo-morvai-agnes_ · Empirical Economics 2018 · [link](https://doi.org/10.1007/s00181-018-1423-x)

### keller-tamas (2 papers)

- `keller-2023-esr` · **Peer effects on academic self-concept: a large randomized field experiment** · _keller-tamas_ · European Sociological Review 2023
- `keller-szakal-2022-socforces` · **Yes, you can! Effects of transparent admission standards** · _keller-tamas, Péter Szakál_ · Social Forces 2022

### barath-lajos (2 papers)

- `barath-ferto-2024-jae` · **The relationship between the ecologisation of farms and total factor productivity** · _barath-lajos, ferto-imre_ · Journal of Agricultural Economics 2024
- `barath-ferto-bojnec-2020-jae` · **The effect of investment, LFA and agri-environmental subsidies on productivity components** · _barath-lajos, ferto-imre, Štefan Bojnec_ · Journal of Agricultural Economics 2020

### gaspar-attila (2 papers)

- `gaspar-giommoni-et-al-2025-jde` · **Corruption and Extremism** · _gaspar-attila, Tommaso Giommoni, Massimo Morelli..._ · Journal of Development Economics 2025 · [link](https://www.sciencedirect.com/science/article/pii/S030438782500077X)
- `cervone-gaspar-et-al-2024-jecinq` · **Inequality Perception and Preferences Globally and Locally** · _Carmen Cervone, gaspar-attila, et al._ · Journal of Economic Inequality 2024

### bencsik-panka (2 papers)

- `bencsik-budhiraja-2025-joebo` · **Cannabis deregulation and policing** · _bencsik-panka, Saayili Budhiraja_ · Journal of Economic Behavior & Organization 2025 · [link](https://doi.org/10.1016/j.jebo.2025.107202)
- `bencsik-chuluun-2019-sbe` · **Comparative well-being of the self-employed and paid employees in the USA** · _bencsik-panka, Tuugi Chuluun_ · Small Business Economics 2019 · [link](https://doi.org/10.1007/s11187-019-00221-1)

### lychagin-sergey (2 papers)

- `frisancho-krishna-et-al-2016-joebo` · **Better luck next time: Learning through retaking** · _Verónica Frisancho, Kala Krishna, lychagin-sergey..._ · Journal of Economic Behavior & Organization 2016 · [link](https://doi.org/10.1016/j.jebo.2016.01.012)
- `lychagin-2016-jue` · **Spillovers, absorptive capacity and agglomeration** · _lychagin-sergey_ · Journal of Urban Economics 2016 · [link](https://doi.org/10.1016/j.jue.2016.08.005)

### laczo-sarolta (2 papers)

- `laczo-rossi-2020-jome` · **Time-consistent consumption taxation** · _laczo-sarolta, Raffaele Rossi_ · Journal of Monetary Economics 2020 · [link](https://doi.org/10.1016/j.jmoneco.2019.07.005)
- `laczo-2014-jedc` · **Does risk sharing increase with risk aversion and risk when commitment is limited?** · _laczo-sarolta_ · Journal of Economic Dynamics and Control 2014 · [link](https://doi.org/10.1016/j.jedc.2014.07.003)

### lorincz-laszlo (2 papers)

- `lorincz-2023-joeg` · **Residential mobility and labour market dynamics** · _lorincz-laszlo_ · Journal of Economic Geography 2023
- `csafordi-lorincz-et-al-2018-jtt` · **Productivity spillovers through labor flows: productivity gap, multinational experience and industry relatedness** · _Zsolt Csáfordi, lorincz-laszlo, lengyel-balazs..._ · Journal of Technology Transfer 2018 · [link](https://doi.org/10.1007/s10961-018-9670-8)

### benczur-peter (2 papers)

- `benczur-konya-2013-jimf` · **Convergence, capital accumulation and the nominal exchange rate** · _benczur-peter, konya-istvan_ · Journal of International Money and Finance 2013 · [link](https://doi.org/10.1016/j.jimonfin.2013.06.009)
- `benczur-simon-et-al-2006-jopm` · **Social costs of consumer impatience in Hungary** · _benczur-peter, András Simon, Viktor Várpalotai_ · Journal of Policy Modeling 2006 · [link](https://doi.org/10.1016/j.jpolmod.2006.04.012)

### barany-zsofia (2 papers)

- `barany-siegel-2020-labec` · **Biased technological change and employment reallocation** · _barany-zsofia, Christian Siegel_ · Labour Economics 2020 · [link](https://doi.org/10.1016/j.labeco.2020.101930)
- `barany-siegel-2020-red` · **Engines of sectoral labor productivity growth** · _barany-zsofia, Christian Siegel_ · Review of Economic Dynamics 2020 · [link](https://doi.org/10.1016/j.red.2020.07.007)

### fleiner-tamas (2 papers)

- `fleiner-frank-et-al-2003-orl` · **A constrained independent set problem for matroids** · _fleiner-tamas, András Frank, Satoru Iwata_ · Operations Research Letters 2003 · [link](https://doi.org/10.1016/s0167-6377(03)00063-4)
- `fleiner-jordan-1999-mathprog` · **Coverings and structure of crossing families** · _fleiner-tamas, Tibor Jordán_ · Mathematical Programming 1999 · [link](https://doi.org/10.1007/s101070050035)

### vonyo-tamas (1 papers)

- `vonyo-2014-ehr` · **DavidGreasley and LesOxley, eds., Economics and history: surveys in cliometrics (Oxford, Wiley‐Blackwell, 2012. Pp. 304. ISBN 9781444337808 Pbk. £19.99)** · _vonyo-tamas_ · Economic History Review 2014 · [link](https://doi.org/10.1111/1468-0289.12076_35)

### adamecz-anna (1 papers)

- `adamecz-adamecz-volgyi-et-al-2020-eoer` · **Is ‘first in family’ a good indicator for widening university participation?** · _adamecz-anna, Anna Adamecz-Völgyi, Morag Henderson..._ · Economics of Education Review 2020 · [link](https://doi.org/10.1016/j.econedurev.2020.102038)

### csercsik-david (1 papers)

- `csercsik-hubert-et-al-2019-enerecon` · **Modeling transfer profits as externalities in a cooperative game-theoretic model of natural gas networks** · _csercsik-david, Franz Hubert, sziklai-balazs..._ · Energy Economics 2019 · [link](https://doi.org/10.1016/j.eneco.2019.01.013)

### murakozy-balazs (1 papers)

- `murakozy-telegdy-2016-eer` · **Political incentives and state subsidy allocation: Evidence from Hungarian municipalities** · _murakozy-balazs, telegdy-almos_ · European Economic Review 2016 · [link](https://doi.org/10.1016/j.euroecorev.2016.07.003)

### biro-peter (1 papers)

- `biro-cechlarova-et-al-2007-ijgt` · **The dynamics of stable matchings and half-matchings for the stable marriage and roommates problems** · _biro-peter, Kataŕına Cechlárová, fleiner-tamas_ · International Journal of Game Theory 2007 · [link](https://doi.org/10.1007/s00182-007-0084-3)

### somogyi-robert (1 papers)

- `gautier-somogyi-2020-ijio` · **Prioritization vs zero-rating: Discrimination on the internet** · _Axel Gautier, somogyi-robert_ · International Journal of Industrial Organization 2020 · [link](https://doi.org/10.1016/j.ijindorg.2020.102662)

### hornok-cecilia (1 papers)

- `abagna-hornok-mulyukova-2025-jde` · **Place-based Policies and Household Wealth in Africa** · _Matthew Abagna, hornok-cecilia, Alina Mulyukova_ · Journal of Development Economics 2025 · [link](https://www.sciencedirect.com/science/article/pii/S0304387825000331)

### kondor-peter (1 papers)

- `kondor-zawadowski-2019-jet` · **Learning in crowded markets** · _kondor-peter, zawadowski-adam_ · Journal of Economic Theory 2019 · [link](https://doi.org/10.1016/j.jet.2019.08.006)

### kornai-janos (1 papers)

- `kornai-simonovits-1977-jet` · **Decentralized control problems in neumann-economies** · _kornai-janos, simonovits-andras_ · Journal of Economic Theory 1977 · [link](https://doi.org/10.1016/0022-0531(77)90084-9)

### branyiczki-reka (1 papers)

- `gabos-branyiczki-et-al-2024-jesp` · **Unravelling the relationship between employment, social transfers and income poverty** · _András Gábos, branyiczki-reka, Bori Binder..._ · Journal of European Social Policy 2024

### juhasz-reka (1 papers)

- `ducruet-juhasz-et-al-2024-jie` · **All aboard: The effects of port development** · _César Ducruet, juhasz-reka, nagy-david..._ · Journal of International Economics 2024 · [link](https://doi.org/10.1016/j.jinteco.2024.103963)

### szeidl-adam (1 papers)

- `grossman-helpman-et-al-2005-jie` · **Optimal integration strategies for the multinational firm** · _Gene M. Grossman, Elhanan Helpman, szeidl-adam_ · Journal of International Economics 2005 · [link](https://doi.org/10.1016/j.jinteco.2005.07.011)

### konya-istvan (1 papers)

- `konya-vary-2024-jimf` · **Which sectors go on when there is a sudden stop? An empirical analysis** · _konya-istvan, Miklós Váry_ · Journal of International Money and Finance 2024 · [link](https://doi.org/10.1016/j.jimonfin.2024.103110)

### prinz-daniel (1 papers)

- `kong-prinz-2020-jpube` · **Disentangling policy effects using proxy data: Which shutdown policies affected unemployment during the COVID-19 pandemic?** · _Edward Kong, prinz-daniel_ · Journal of Public Economics 2020 · [link](https://doi.org/10.1016/j.jpubeco.2020.104257)

## 4. Tier C — peer-reviewed, lower-tier

- `elekes-2023-cjres` · **Regional diversification and labour market upgrading: local access to skill-related high-income jobs helps workers escaping low-wage employment** · _elekes-zoltan_ · Cambridge Journal of Regions, Economy and Society 2023
- `barath-bokusheva-ferto-2017-easternee` · **Demand for farm insurance under financial constraints** · _barath-lajos, Raushan Bokusheva, ferto-imre_ · Eastern European Economics 2017
- `koczy-sziklai-csercsik-2022-esr2` · **Nord Stream 2: A prelude to war** · _koczy-laszlo, sziklai-balazs, csercsik-david_ · Energy Strategy Reviews 2022
- `baro-branyiczki-elek-2022-eja` · **Time patterns of precautionary health behaviours during an easing phase of the COVID-19 pandemic in Europe** · _Anita Báró, branyiczki-reka, elek-peter_ · European Journal of Ageing 2022
- `elekes-2021-eps-collab` · **Repeated collaboration of inventors across European regions** · _elekes-zoltan_ · European Planning Studies 2021
- `cepaluni-dorsch-branyiczki-2022-jpfpc` · **Political regimes and deaths in the early stages of the COVID-19 pandemic** · _Gabriele Cepaluni, Michael T. Dorsch, branyiczki-reka_ · Journal of Public Finance and Public Choice 2022
- `lorincz-2024-netsci` · **Business transactions and ownership ties between firms** · _lorincz-laszlo_ · Network Science 2024
- `csercsik-koczy-2017-nse` · **Efficiency and stability in electrical power transmission networks: A partition function form approach** · _csercsik-david, koczy-laszlo_ · Networks and Spatial Economics 2017
- `csercsik-2016-nse` · **Competition and cooperation in a bidding model of electrical energy trade** · _csercsik-david_ · Networks and Spatial Economics 2016
- `csercsik-habis-2015-nse` · **Cooperation with externalities and uncertainty** · _csercsik-david, Helga Habis_ · Networks and Spatial Economics 2015
- `lorincz-2023-plosone` · **Firm production adjustment after demand shocks** · _lorincz-laszlo_ · PLOS ONE 2023
- `keller-szakal-2021-plosone-encouragement` · **Effects of a light-touch randomized encouragement intervention on students' exam grades, self-efficacy, motivation, and test anxiety** · _keller-tamas, Péter Szakál_ · PLOS ONE 2021
- `keller-takacs-2021-plosone-proximity` · **Proximity can induce diverse friendships: A large randomized classroom experiment** · _keller-tamas, Károly Takács_ · PLOS ONE 2021
- `barath-ferto-bojnec-2025-scirep` · **Gender-based differences in eco-efficient farming** · _barath-lajos, ferto-imre, Štefan Bojnec_ · Scientific Reports 2025
- `cervone-gaspar-et-al-2023-sir` · **A Twofold-Subjective Measure of Income Inequality** · _Carmen Cervone, gaspar-attila, et al._ · Social Indicators Research 2023

## 6. Off-list / chapters / working papers (editor review needed)

These are not on `data/journals.json`. Editor may choose to drop some entirely rather than draft.

- `lindner-dellavigna-et-al-2025-nber` · **Using Multiple Outcomes to Adjust Standard Errors for Spatial Correlation** · _lindner-attila, Stefano DellaVigna, Guido W. Imbens..._ · NBER 2025 · [link](https://doi.org/10.3386/w33716)
- `akyol-krishna-et-al-2024-nber` · **Targeting the Gender Placement Gap: Marks Versus Money** · _Pelin Akyol, Kala Krishna, lychagin-sergey_ · NBER 2024 · [link](https://doi.org/10.3386/w33074)
- `baro-branyiczki-et-al-2022-krtkwp-payroll-taxes` · **Firm heterogeneity and the impact of payroll taxes** · _Anita Báró, branyiczki-reka, lindner-attila..._ · KRTK-KTI Working Papers 2022
- `biro-branyiczki-2019-wp` · **17. Health gap in post-socialist Central and Eastern Europe: A life-course perspective** · _biro-aniko, branyiczki-reka_ · ? 2019 · [link](https://doi.org/10.1515/9783110617245-017)
- `konya-2018-wp` · **The Neoclassical Growth Model** · _konya-istvan_ · ? 2018 · [link](https://doi.org/10.1007/978-3-319-69317-0_6)
- `simonovits-2018-wp` · **Models of Political Economy** · _simonovits-andras_ · ? 2018 · [link](https://doi.org/10.1007/978-3-319-72502-4_12)
- `halpern-2013-wp` · **EU accession as an instrument for speeding up transition** · _halpern-laszlo_ · ? 2013 · [link](https://doi.org/10.4324/9780203067901-29)
- `lengyel-2012-wp` · **Regional Clustering Tendencies of the Hungarian Automotive and ICT Industries in the First Half of the 2000s** · _lengyel-balazs_ · ? 2012 · [link](https://doi.org/10.1007/978-3-642-25816-9_4)
- `lieli-hsu-et-al-2022-asita` · **The Use of Machine Learning in Treatment Effect Estimation** · _lieli-robert, Yu‐Chin Hsu, Ágoston Reguly_ · Advanced studies in theoretical and applied econometrics 2022 · [link](https://doi.org/10.1007/978-3-031-15149-1_3)
- `broadberry-vonyo-2025-cupe` · **Blockading Britain and Germany during World War I** · _Stephen Broadberry, vonyo-tamas_ · Cambridge University Press eBooks 2025 · [link](https://doi.org/10.1017/9781009474887.005)
- `benk-horvath-et-al-2024-cte` · **Inflation Shock and Monetary Policy** · _benk-szilard, P. Horváth, Norbert Szepesi_ · Contributions to economics 2024 · [link](https://doi.org/10.1007/978-3-031-61561-0_4)
- `benczur-konya-2022-cte` · **Convergence to the Centre** · _benczur-peter, konya-istvan_ · Contributions to economics 2022 · [link](https://doi.org/10.1007/978-3-030-93963-2_1)
- `biro-kollanyi-et-al-2022-cte` · **Health and Social Security** · _biro-aniko, Zsófia Kollányi, Piotr Romaniuk..._ · Contributions to economics 2022 · [link](https://doi.org/10.1007/978-3-030-93963-2_8)
- `horn-keller-et-al-2016-eepe` · **Early tracking and competition – A recipe for major inequalities in Hungary** · _horn-daniel, keller-tamas, Péter Róbert_ · Edward Elgar Publishing eBooks 2016 · [link](https://doi.org/10.4337/9781785367267.00017)
- `acs-szerb-2010-eepe` · **Entrepreneurship and Economic Development** · _Zoltán J. Ács, szerb-laszlo_ · Edward Elgar Publishing eBooks 2010 · [link](https://doi.org/10.4337/9780857935540.00008)
- `herrendorf-rogerson-et-al-2013-ee` · **Growth and Structural Transformation** · _Berthold Herrendorf, Richard Rogerson, valentinyi-akos_ · Elsevier eBooks 2013 · [link](https://doi.org/10.1016/b978-0-444-53540-5.00006-9)
- `heidhues-koszegi-2018-hobe` · **Behavioral Industrial Organization** · _Paul Heidhues, koszegi-botond_ · Handbook of behavioral economics 2018 · [link](https://doi.org/10.1016/bs.hesbe.2018.07.006)
- `francois-manchin-et-al-2013-hocge` · **Market Structure in Multisector General Equilibrium Models of Open Economies** · _Joseph François, manchin-miriam, Will Martín_ · Handbook of computable general equilibrium modeling 2013 · [link](https://doi.org/10.1016/b978-0-444-59568-3.00024-9)
- `kertesi-koll-2002-rile` · **Economic transformation and the revaluation of human capital — Hungary, 1986–1999** · _kertesi-gabor, János Köll_ · Research in labor economics 2002 · [link](https://doi.org/10.1016/s0147-9121(02)21013-4)
- `acs-szerb-et-al-2017-sie` · **The Global Entrepreneurship Index** · _Zoltán J. Ács, szerb-laszlo, Erkko Autio_ · SpringerBriefs in economics 2017 · [link](https://doi.org/10.1007/978-3-319-63844-7_3)
- `acs-szerb-et-al-2015-sie` · **The Global Entrepreneurship and Development Index** · _Zoltán J. Ács, szerb-laszlo, Erkko Autio_ · SpringerBriefs in economics 2015 · [link](https://doi.org/10.1007/978-3-319-14932-5_4)
- `czibik-fazekas-et-al-2021-ucs` · **Networked Corruption Risks in European Defense Procurement** · _Ágnes Czibik, Mihály Fazekas, Alfredo Hernández Sánchez..._ · Understanding complex systems 2021 · [link](https://doi.org/10.1007/978-3-030-81484-7_5)

---

## Workflow once a PDF is obtained

Two paths:

**Quick (just paste abstract):**
1. Open the PDF, copy the abstract.
2. Edit `data/papers/<slug>.json` — set the `abstract` field.
3. Next Claude session can draft from there.

**Full (Claude reads the PDF):**
1. Save the PDF to `not-shared/pdfs/<slug>.pdf` (folder is gitignored).
2. Tell Claude "draft from the PDF at not-shared/pdfs/<slug>.pdf" — it can read the full text via the `pdf` skill, which gives a richer summary than abstract-alone.

## Out of scope

Working papers and chapters that genuinely don't belong in the catalogue should be flagged for removal rather than fetched. Use `audit-author <slug>` to see each author's catalogue and decide which papers to drop.