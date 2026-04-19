# SEED_ECONOMISTS — starter roster

A starting list of Hungarian economists for admission to the site. **This is a seed, not the final list.** Gábor to verify, prune, and expand using RePEc Hungary + CEPR + personal networks.

**Draft bios for each name are in `/data/authors-seed.json`**, with a `bio_review` flag indicating confidence (`confident` / `needs-verification` / `stub`). Claude Code will split this array into individual `data/authors/[slug].json` files during the build.

Each name includes: primary affiliation, a guess at primary field, and source links (RePEc / website) to verify their qualifying publication(s).

**Eligibility reminder:** at least one publication in a Tier A or Tier B journal (see `docs/SPEC.md` § 1.2). Some names below are _probable_ but need the qualifying-pub check before admission.

Names use the "surname first" Hungarian convention where the person writes it that way; otherwise Western order.

---

## Senior (established career, multiple top publications expected)

| Name | Affiliation | Field | RePEc / notes |
|---|---|---|---|
| Péter Kondor | LSE | Finance / theory | ideas.repec.org/e/pko265 · JoF, RFS publications |
| Botond Kőszegi | Northwestern / CEU | Behavioral economics | QJE, AER; moved to Northwestern |
| Ádám Szeidl | CEU | Networks, development finance | QJE, AER, ECMA |
| Balázs Szentes | LSE | Theory, game theory | REStud, JET |
| Miklós Koren | CEU / KRTK | Trade, firms | ideas.repec.org/e/pko42 · QJE, RESTUD |
| Gábor Békés | CEU / KRTK | Trade, FDI, firms | ideas.repec.org/e/pbe115 · JIE, SMJ (forthcoming) |
| László Halpern | KRTK | Trade, productivity | AER (with Koren, Szeidl) |
| Róbert Lieli | CEU | Econometrics | J of Econometrics |
| Ádám Réka | ? | ? | _verify_ |
| János Kornai† | Harvard / Corvinus | Transition, systems | 1928–2021, include posthumously; canonical transition work |
| Attila Ambrus | Duke | Theory, game theory | Hungarian-American; AER, ECMA |
| Gábor Kézdi | Michigan | Labor, health, education | Formerly CEU; AEJ: Applied, REStat |
| Péter Benczúr | JRC / MNB | Macro, inequality | JEEA |
| István Kónya | KRTK / MNB | Macro | RED |
| Ákos Valentinyi | Manchester / CEPR | Macro | JME, REStud |
| Zsolt Darvas | Bruegel / Corvinus | Macro, European economy | |
| Balázs Égert | OECD | Macro, applied | |
| Arpad Abraham | Bristol | Macro, public | JME, AEJ:Macro |

## Mid-career (assistant / associate professor at research universities)

| Name | Affiliation | Field | Notes |
|---|---|---|---|
| Attila Lindner | UCL | Labor | AER, QJE (minimum wage); strong Hungarian focus |
| Dániel Horn | KRTK / Corvinus | Education economics | Labour Economics |
| Réka Juhász | UBC | Trade, economic history | AER; Hungarian-British |
| Ágnes Szabó-Morvai | KRTK / Debrecen | Labor, health | _verify qualifying pub_ |
| Anna Adamecz | UCL / KRTK | Education, labor | _verify_ |
| Mónika Mrázová | Geneva | Trade, theory | AER, EER |
| Áron Tóbiás | Syracuse | Theory, applied micro | _verify_ |
| Balázs Muraközy | Liverpool | IO, firms | EER |
| Álmos Telegdy | Corvinus / KRTK | Labor, firms | Labour Economics |
| László Mátyás | CEU | Econometrics | J of Econometrics |
| Péter Harasztosi | JRC | Trade, firms | Ec Inquiry; co-author with Békés |
| Gergely Csorba | KRTK / GVH | IO, competition | Int J IO |
| Ágnes Timár | ? | ? | _check_ |

## Rising stars (recent PhDs, early career)

| Name | Affiliation | Field | Notes |
|---|---|---|---|
| Áron Tóbiás | Syracuse | Theory | _verify qualifying pub_ |
| Anna Naszódi | MNB / KRTK | Finance, marriage markets | _verify_ |
| Pálma Mosberger | ? | Labor | PhD at LSE |
| Réka Branyiczki | Central bank of Ireland / TÁRKI | Labor, gender | _verify_ |
| Dávid Koczó | ? | ? | add if qualifies |
| Bálint Menyhért | JRC / KRTK | Labor, poverty | _verify_ |
| Tamás Vonyó | Bocconi | Economic history | _verify_ |
| Julianna Krizan | ? | ? | _fill_ |
| Ágnes Horváth | MNB | Macro | _verify_ |
| Zsuzsa Munkácsi | ECB | Finance | _verify_ |
| Viktor Tsyrennikov | Cornell / CEU | Macro | Hungarian-trained, not Hungarian-born — check eligibility |

## Diaspora — Hungarian-origin at major universities, worth chasing

| Name | Affiliation | Field |
|---|---|---|
| Xavier Jaravel | LSE | Trade, inequality — _check Hungarian origin_ |
| László Sándor | Harvard Business School / LSE | Econ |
| György Kocziszky | Various | Regional |
| Iván Werning | MIT | Macro — _Argentinian, not Hungarian; drop_ |
| Andrew Atkeson | UCLA | — _not Hungarian; example of name-check false positive_ |

_Diaspora search strategy:_ ask each admitted senior economist for 5 names of Hungarian-origin economists at research universities abroad. Snowball.

---

## Verification checklist per candidate

For each name:

- [ ] Find a RePEc profile; copy the ID
- [ ] List their top 3 publications by journal prestige
- [ ] Confirm at least one is in Tier A or Tier B (`data/journals.json`)
- [ ] Check eligibility criteria in `SPEC.md` § 1.1 (nationality / birthplace / HU affiliation ≥ 3 years)
- [ ] If all three pass: create `data/authors/[slug].json`
- [ ] Mark `qualifying_publication` field with the one that got them in
- [ ] If any fail: note reason, set aside — revisit in a year

---

## Sources used to assemble this list

- [RePEc Hungary author list](https://ideas.repec.org/g/hungary.html) — curated registry, ~50 names
- [RePEc Hungary ranking](https://ideas.repec.org/top/top.hungary.html) — ranked by aggregated score
- Memory: CEU, KRTK, Corvinus, MNB Research rosters
- Not yet checked (do before admitting): CEPR member directory, IZA fellows, NBER affiliates, Royal Economic Society fellows

## Priorities for the MVP

For the afternoon Claude Code session, pick **5 authors** to seed the site with real content. Suggested picks (geographically and field-wise diverse):

1. **Gábor Békés** (trade, FDI, HU-based)
2. **Attila Lindner** (labor, UK-based, very HU-relevant minimum-wage work)
3. **Péter Kondor** (finance, UK-based, theory)
4. **Botond Kőszegi** (behavioral, US-based, broad appeal)
5. **Réka Juhász** (trade / history, CA-based)

One paper each for the demo = 5 papers for the MVP. Pick recent, high-impact, ideally Hungary-relevant where possible.
