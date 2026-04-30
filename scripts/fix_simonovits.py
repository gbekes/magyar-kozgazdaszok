"""Fix Simonovits András's catalogue: delete wrong-person + unverified stubs,
correct metadata errors, set abstracts where available, leave older
no-public-abstract papers with abstract=null.

Verification done against IDEAS author handle psi174 + KSz PDFs (real.mtak.hu).

Drops (2):
- simonovits-kezdi-et-al-2017-apsr  — Wrong person: this APSR 2017 paper is by
  *Gábor* Simonovits (CEU/NYU political scientist), not András Simonovits
  (KRTK/BME pension economist). Same surname only.
- simonovits-simonovits-1982-scandje — Unverified. Not in IDEAS profile,
  duplicate self-coauthored slug, suspicious 'pages 571-571'. Cannot confirm
  this paper exists; conservative removal.
- simonovits-2018-wp — This is chapter 12 ("Models of Political Economy") of
  Simonovits's own Palgrave book "Simple Models of Income Redistribution"
  (2018), not a journal article or standalone working paper. Including a
  single chapter from a 13-chapter monograph is arbitrary; drop.

Metadata fixes:
- garay-simonovits-et-al-2011-eclett: year 2011 → 2012 (paper printed 2012,
  manuscript ID dated Dec 2011).
- molnar-simonovits-1998-jedc: first author "József Molnár" → "György
  Molnár" (canonical IDEAS listing).
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAPERS = ROOT / "data" / "papers"


def load(slug):
    return json.loads((PAPERS / f"{slug}.json").read_text(encoding="utf-8"))


def save(slug, data):
    (PAPERS / f"{slug}.json").write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


# 1. drops
for slug in ["simonovits-kezdi-et-al-2017-apsr",
             "simonovits-simonovits-1982-scandje",
             "simonovits-2018-wp"]:
    f = PAPERS / f"{slug}.json"
    if f.exists():
        f.unlink()
        print(f"dropped: {slug}")

# 2. metadata fixes
slug = "garay-simonovits-et-al-2011-eclett"
p = load(slug)
p["year"] = 2012
p["issue"] = "3"
save(slug, p)
print(f"fixed year (2011->2012): {slug}")

slug = "molnar-simonovits-1998-jedc"
p = load(slug)
p["authors"] = ["György Molnár", "simonovits-andras"]
p["volume"] = "23"
p["issue"] = "2"
save(slug, p)
print(f"fixed first-author (József->György): {slug}")

# 3. set abstracts where verbatim is available
ABSTRACTS = {
    "simonovits-2011-eclett": (
        "The mandatory pension pillar is usually supplemented by a voluntary one. "
        "In our simple model, voluntary pensions partly replace mandatory ones "
        "without affecting the outcomes: the voluntary pensions are indifferent. "
        "This result may serve as benchmark."
    ),
    "garay-simonovits-et-al-2011-eclett": (
        "When individuals underreport their incomes, they take into account their "
        "private gains and moral losses, the latter depending on the acquaintances' "
        "previous underreports. We prove that under quite natural assumptions the "
        "process globally converges to the symmetric steady state."
    ),
    "simonovits-2017-ksz": (
        "Magyarországon korábban az átlag fölötti nyugdíjaknak a nettó keresetekhez "
        "viszonyított értékét erős degresszió csökkentette, ez ma már gyakorlatilag "
        "nincs így. A tanulmány bemutatja a magyar nyugdíjdegresszió történetét, "
        "elemzi a degresszió hiányának torzító hatásait, és javaslatot tesz a "
        "nyugdíjdegresszió fokozatos visszaállítására."
    ),
    "simonovits-2018-ksz": (
        "A 2016-ban elinduló reálbérrobbanás és a 2017-ben elinduló erőltetett "
        "járulékkulcs-csökkentés új megvilágításba helyezi az új nyugdíjak "
        "valorizációját és a régi nyugdíjak indexálását. Kívánatos, hogy két nagyon "
        "hasonló életpálya apró különbségek miatt ne adjon jelentősen különböző "
        "nyugdíjpályát, még ha a nettó átlagos reálkereset évről évre szeszélyesen "
        "változik is. Ennek a kívánalomnak csak a 2000-ben megszüntetett "
        "bérindexálás tesz eleget, de ez a szabály is a valorizációs arány "
        "évenkénti karbantartását igényli. Ezt a feladatot látja el a pontrendszer. "
        "Mivel adott évjáratban a várható élettartam együtt nő az életpálya-"
        "jövedelemmel, ezért minden életjáradék torz újraelosztást okoz, amit a "
        "pontrendszer még felnagyít. Tehát a nyugdíjdegressziót (vagy a progresszív "
        "személyi jövedelemadót) is újra be kell vezetni, vállalva a csökkentett "
        "munkavállalást és járulékfizetést."
    ),
    "simonovits-2019-ksz": (
        "Az öregedő társadalmak nyugdíjgondjainak megoldásában az egyik "
        "leghatékonyabb eszköz az átlagos nyugdíjba vonulási kor (az úgynevezett "
        "korcentrum) emelése. A járulékkulcs emelése vagy a nyugdíj/kereset arány "
        "csökkentése politikailag nehezebb, és gazdaságilag sem vonzó. Ehhez a "
        "minimális és az általános nyugdíjkorhatár párhuzamos emelésén kívül "
        "erősíteni kell az ösztönzőket is, például a rugalmas nyugdíjba vonulási "
        "kor bevezetésével."
    ),
    "simonovits-2020-ksz": (
        "A magyar nyugdíjrendszert jelenleg három fő középtávú feszültség "
        "jellemzi. 1. Az egymás utáni évjáratok közötti nyugdíjolló egyre jobban "
        "szétnyílik. 2. Az új évjáratok nyugdíjai a járulékplafon eltörlése s még "
        "inkább az arányos személyi jövedelemadó bevezetése miatt polarizálódnak. "
        "3. A nyugdíjkorhatár merevsége és a Nők40 lazasága egyre inkább "
        "szembekerül egymással. A tanulmány javaslatokat fogalmaz meg a "
        "feszültségek enyhítésére: a szocho-csökkentés leállítása, a járulékalap-"
        "plafon visszaállítása, a degresszió kiterjesztése, és a 2009-es "
        "csökkentett előrehozott nyugdíj visszaállítása."
    ),
}
for slug, abstract in ABSTRACTS.items():
    p = load(slug)
    p["abstract"] = abstract
    save(slug, p)
print(f"abstracts set on {len(ABSTRACTS)} Simonovits papers")
