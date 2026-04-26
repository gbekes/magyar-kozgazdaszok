# TAXONOMY — Evidence for Hungary

Tag vocabularies for papers. These are the controlled lists. Keep them stable; changes require updating JSON schemas and existing entries.

---

## 1. Policy topics (21)

Every paper gets **1–3** topic tags. These are the primary navigation. Descriptions are short and policy-facing by design.

| id | English | Hungarian | What it covers |
|---|---|---|---|
| `labor-markets` | Labor markets and employment | Munkaerőpiac és foglalkoztatás | Wages, unemployment, labor supply, job search, minimum wage, labor market programs, worker mobility |
| `education-skills` | Education and skills | Oktatás és készségek | Schools, tracking, teachers, higher education, vocational training, returns to education, test scores |
| `health` | Health and healthcare | Egészségügy | Health outcomes, healthcare access, hospitals, prevention, lifestyle, mental health, public health |
| `demographics-migration` | Demographics and migration | Demográfia és migráció | Fertility, ageing, pensions, emigration, immigration, return migration, brain drain |
| `trade-fdi` | Trade, FDI, global value chains | Kereskedelem, külföldi működő tőke | Exports, imports, multinational firms, FDI, offshoring, global value chains, trade policy |
| `firms-productivity` | Firms and productivity | Vállalatok és termelékenység | Firm dynamics, productivity, entry/exit, management practices, competitiveness, SME finance |
| `innovation-digital` | Innovation, R&D, digital economy | Innováció, K+F, digitális gazdaság | R&D, patents, technology adoption, AI, digitalization, open source, software |
| `banking-finance` | Banking, finance, monetary policy | Pénzügy, bankrendszer, monetáris politika | Banks, credit, financial stability, stock markets, corporate finance, central bank policy, exchange rates |
| `fiscal-tax` | Fiscal policy and taxation | Költségvetési politika és adózás | Government budget, taxes, public debt, tax evasion, fiscal multipliers, flat tax, VAT |
| `regional-urban` | Regional and urban economics | Regionális és városi gazdaságtan | Regional disparities, agglomeration, housing, urban policy, infrastructure, transport, commuting |
| `energy-environment` | Energy, environment, climate | Energia, környezet, klíma | Energy policy, emissions, climate, air quality, renewables, environmental regulation |
| `inequality-welfare` | Inequality, poverty, social policy | Egyenlőtlenség, szegénység, szociálpolitika | Income / wealth distribution, poverty, welfare programs, gender gaps, intergenerational mobility |
| `political-economy` | Political economy, institutions | Politikai gazdaságtan, intézmények | Institutions, rule of law, corruption, voting, populism, democracy, EU integration |
| `transition-postcommunist` | Transition and post-communist economics | Rendszerváltás és posztszocialista gazdaság | Transition dynamics, privatization, emerging Europe, CEE-specific research, economic history of the region |
| `behavioral` | Behavioral economics | Viselkedési közgazdaságtan | Reference-dependent preferences, present bias, overconfidence, loss aversion, self-control, naïveté, experimental and field-experimental work on decision-making |
| `industrial-organization` | Industrial organization, market structure | Iparági szervezet, piacszerkezet | Firm conduct, antitrust, market power, mergers, vertical integration, advertising, platform markets |
| `macroeconomics` | Macroeconomics and business cycles | Makrogazdaságtan és gazdasági ciklusok | Output, inflation, monetary and fiscal aggregates, growth, business cycles, exchange-rate regimes |
| `agriculture-food` | Agriculture and food economics | Agrár- és élelmiszer-gazdaság | Farm productivity, agricultural policy, food markets, rural development, CAP, farm structure |
| `market-design` | Market design and matching | Piactervezés és párosítás | Centralised and decentralised allocation mechanisms — kidney exchange, school choice, auctions, course allocation, residency matching, organ allocation |
| `mechanism-design` | Mechanism design and game theory | Mechanizmustervezés és játékelmélet | Designing rules and incentives so strategic agents reach a desired outcome — auctions, voting rules, contracts, principal-agent problems, cooperative game theory, bargaining, social choice |
| `methods` | Methods and econometrics | Módszertan és ökonometria | Papers whose primary contribution is methodological (estimation, identification, computation). Tag secondarily if paper is applied. |

**Tagging conventions:**
- Up to 3 topics per paper. Don't pad; if only one fits, use one.
- `methods` is secondary — apply to papers whose _main contribution_ is a method. Also keep the applied topic tag.
- `market-design` and `mechanism-design` are conceptually adjacent but distinct: use `market-design` when the paper is about a specific running allocation system (kidney exchange, school choice, auctions); use `mechanism-design` for theory papers about incentive-compatible rules in general.
- If a paper is about Hungary specifically and the policy framing is strong, add `transition-postcommunist` as a secondary tag.

---

## 2. Methods (11)

Tag each paper with the dominant empirical/analytical method. Up to 2.

| id | Label | Notes |
|---|---|---|
| `rct` | Randomized experiment (RCT, field experiment) | Lab-in-the-field counts if primary |
| `diff-in-diff` | Difference-in-differences | Including event study, staggered DiD |
| `iv` | Instrumental variables | |
| `rd` | Regression discontinuity | Sharp or fuzzy |
| `panel-data` | Panel / fixed effects | Workhorse observational |
| `synthetic-control` | Synthetic control | |
| `structural` | Structural model | Dynamic, estimated structural, DSGE |
| `theory` | Theory | No empirical content, or minor |
| `time-series` | Time series / VAR / macro | |
| `ml-text` | Machine learning / text analysis | ML for prediction, NLP on documents |
| `descriptive-survey` | Descriptive / survey evidence | New data, stylized facts, no identification claim |

---

## 3. Data types (9)

Signals what kind of evidence the paper brings. Up to 3 tags.

| id | Label | Examples |
|---|---|---|
| `admin-firm` | Administrative firm data | NAV corporate tax, balance sheets, registers |
| `admin-tax` | Administrative tax / social-security data | PIT, social contributions, pension records |
| `admin-individual` | Administrative individual-level data | Education records, health records, welfare, matched employer-employee |
| `survey` | Survey data | HCSO/KSH surveys, TÁRKI, LFS, EU-SILC, household panels |
| `firm-level-dataset` | Proprietary / commercial firm data | Orbis, Amadeus, Compustat, Capital IQ |
| `field-experiment` | Experimental data | RCTs, lab-in-the-field |
| `macro-aggregate` | Macro / aggregate | National accounts, central bank data, Eurostat, IMF |
| `digital-trace` | Digital trace / platform data | GitHub, Twitter, app logs, web scrape, search |
| `historical` | Historical / archival | Pre-1950 sources |

---

## 4. Country / region tags

Use ISO 3166-1 alpha-2 for countries (HU, DE, US, …).

For regions/groups, use these shortcodes:
- `EU` — European Union (current)
- `EEA` — European Economic Area
- `CEE` — Central and Eastern Europe (broadly: HU, PL, CZ, SK, RO, BG, Baltics, SI, HR)
- `V4` — Visegrád Four
- `GLOBAL` — global / cross-country analysis spanning multiple regions
- `TRANSITION` — post-communist transition countries

Multi-country papers get multiple tags. A paper on HU + PL + CZ gets `HU`, `PL`, `CZ`, `V4`.

---

## 5. Taxonomy governance

- The 15 topics are **stable**. Adding a new topic requires a PR and thinking.
- Method and data-type lists can grow as needed; add and document.
- Country list grows naturally.
- If a paper doesn't fit any of the 15 topics, the right response is almost always "pick the closest one and argue for adding a new topic in a PR." Don't leave papers untagged.

---

## 6. Auto-tagging guidance (for AI workflow)

When the AI ingestion pipeline (`docs/WORKFLOW.md`) suggests tags from an abstract:

- Start from topic. One primary topic is usually obvious; the 2nd and 3rd are where judgment comes in.
- Method tag: look at the abstract for trigger words (RCT, randomize, difference-in-differences, regression discontinuity, instrument, structural, equilibrium, estimate, calibrate, panel, time series, VAR).
- Data type: often requires reading beyond the abstract — check the paper's "Data" section if available.
- Countries: usually in the abstract, but check the data section.
- **Policy relevance tag heuristic**: if the paper's empirical setting is Hungary, automatically flag for policymaker attention regardless of topic. Add `transition-postcommunist` as a secondary tag when appropriate.

When uncertain, propose 2–3 candidates and leave for human review. Don't overtag.
