"""Apply the 2026-05-03 author-driven media scan output for
Kertesi Gabor, Koren Miklos, and Murakozy Balazs."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PRESS = ROOT / "data" / "press"
POLICY = ROOT / "data" / "policy"

TODAY = "2026-05-03"


def press(d):
    return {
        "id": d["id"],
        "title": d["title"],
        "title_hu": d.get("title_hu"),
        "authors": d["authors"],
        "kind": d["kind"],
        "venue": d["venue"],
        "date": d["date"],
        "language": d["language"],
        "url": d["url"],
        "blurb": None,
        "linked_paper_id": d.get("linked_paper_id"),
        "added_at": TODAY,
        "last_reviewed_at": TODAY,
        "review_status": "ai-drafted",
    }


def policy(d):
    return {
        "id": d["id"],
        "title": d["title"],
        "title_hu": d.get("title_hu"),
        "authors": d["authors"],
        "outlet_kind": d["outlet_kind"],
        "outlet": d["outlet"],
        "outlet_issue": d.get("outlet_issue"),
        "institution": d["institution"],
        "year": d["year"],
        "language": d["language"],
        "url": d["url"],
        "doi": None,
        "summary_en": None,
        "summary_hu": None,
        "policy_relevance": None,
        "policy_relevance_hu": None,
        "topics": [],
        "countries_studied": d.get("countries_studied", []),
        "policy_instruments": [],
        "linked_paper_id": d.get("linked_paper_id"),
        "added_at": TODAY,
        "last_reviewed_at": TODAY,
        "review_status": "ai-drafted",
    }


PRESS_ITEMS = [
    {"id": "kertesi-2024-telex-foster-care",
     "title": "Jobb esélyekkel kezdik felnőtt életüket azok az állami gondozottak, akik nevelőszülőknél nőnek fel",
     "title_hu": "Jobb esélyekkel kezdik felnőtt életüket azok az állami gondozottak, akik nevelőszülőknél nőnek fel",
     "authors": ["kertesi-gabor", "Anna Bárdits"],
     "kind": "column", "venue": "Telex (Defacto)", "date": "2024-04-22", "language": "hu",
     "url": "https://telex.hu/defacto/2024/04/22/allami-gondozott-gyerekek-intezet-vs-neveloszulok"},
    {"id": "kertesi-2021-telex-life-expectancy",
     "title": "Magyarországon a szegények rövidebb ideig élnek, de ennek nem feltétlenül kellene így lennie",
     "title_hu": "Magyarországon a szegények rövidebb ideig élnek, de ennek nem feltétlenül kellene így lennie",
     "authors": ["kertesi-gabor", "biro-aniko", "hajdu-tamas", "prinz-daniel"],
     "kind": "column", "venue": "Telex (Defacto)", "date": "2021-12-07", "language": "hu",
     "url": "https://telex.hu/defacto/2021/12/07/magyarorszagon-a-szegenyek-rovidebb-ideig-elnek-de-ennek-nem-feltetlenul-kellene-igy-lennie"},
    {"id": "kertesi-2023-portfolio-children-dental",
     "title": "Hatalmas a különbség a szegény és gazdag gyerekek fogainak állapota között",
     "title_hu": "Hatalmas a különbség a szegény és gazdag gyerekek fogainak állapota között",
     "authors": ["kertesi-gabor", "hajdu-tamas", "Petra Fadgyas-Freyler"],
     "kind": "column", "venue": "Portfolio.hu", "date": "2023-07-05", "language": "hu",
     "url": "https://www.portfolio.hu/krtk/20230705/hatalmas-a-kulonbseg-a-szegeny-es-gazdag-gyerekek-fogainak-allapota-kozott-625847"},

    {"id": "koren-2025-telex-stagflation",
     "title": "Nem nő, csak drágul. Hogy juthat ki a csapdából a magyar gazdaság?",
     "title_hu": "Nem nő, csak drágul. Hogy juthat ki a csapdából a magyar gazdaság?",
     "authors": ["koren-miklos", "Attila Rátfai"],
     "kind": "op-ed", "venue": "Telex.hu", "date": "2025-06-06", "language": "hu",
     "url": "https://telex.hu/nevertek/2025/06/06/makrogazdasag-stagflacio-gdp-inflacio"},
    {"id": "koren-2020-indexdefacto-school-closures-value",
     "title": "Mennyit érnek az iskolabezárások?",
     "title_hu": "Mennyit érnek az iskolabezárások?",
     "authors": ["koren-miklos"],
     "kind": "blog", "venue": "Index.hu (Defacto)", "date": "2020-03-10", "language": "hu",
     "url": "https://index.hu/gazdasag/defacto/2020/03/10/mennyit_ernek_az_iskolabezarasok/"},
    {"id": "koren-2020-indexdefacto-nurses-childcare",
     "title": "Sok ápoló kiesik most, mert a gyerekeikre kell vigyázniuk",
     "title_hu": "Sok ápoló kiesik most, mert a gyerekeikre kell vigyázniuk",
     "authors": ["koren-miklos", "biro-aniko", "János Köllő"],
     "kind": "blog", "venue": "Index.hu (Defacto)", "date": "2020-03-17", "language": "hu",
     "url": "https://index.hu/gazdasag/defacto/2020/03/17/iskolabezarasok_a_jo_a_rossz_es_a_csuf/"},
    {"id": "koren-2022-qubit-pete-peter-obit",
     "title": "Pete Péter a közgazdaságtan szerelmese és a sarlatánok ádáz ellenfele volt",
     "title_hu": "Pete Péter a közgazdaságtan szerelmese és a sarlatánok ádáz ellenfele volt",
     "authors": ["koren-miklos"],
     "kind": "op-ed", "venue": "Qubit.hu", "date": "2022-10-30", "language": "hu",
     "url": "https://qubit.hu/2022/10/30/pete-peter-a-kozgazdasagtan-szerelmese-es-a-sarlatanok-adaz-ellenfele-volt"},
    {"id": "koren-2025-qubit-ai-labor",
     "title": "Az AI munkaerőpiaci hatása az internet elterjedéséhez lesz hasonló",
     "title_hu": "Az AI munkaerőpiaci hatása az internet elterjedéséhez lesz hasonló",
     "authors": ["koren-miklos"],
     "kind": "podcast", "venue": "Qubit.hu (Dollárpapa)", "date": "2025-08-25", "language": "hu",
     "url": "https://qubit.hu/2025/08/25/az-ai-munkaeropiaci-hatasa-az-internet-elterjedesehez-lesz-hasonlo"},
    {"id": "koren-2013-index-erc-interview",
     "title": "Fontos, hogy visszavár-e az ország",
     "title_hu": "Fontos, hogy visszavár-e az ország",
     "authors": ["koren-miklos"],
     "kind": "interview", "venue": "Index.hu", "date": "2013-01-06", "language": "hu",
     "url": "https://index.hu/gazdasag/2013/01/06/koren_miklos/"},
    {"id": "koren-2020-portfolio-elemzo-kozgazdasz",
     "title": "Ha érteni akarsz, mérj!",
     "title_hu": "Ha érteni akarsz, mérj!",
     "authors": ["koren-miklos"],
     "kind": "interview", "venue": "Portfolio.hu", "date": "2020-12-15", "language": "hu",
     "url": "https://www.portfolio.hu/krtk/20201215/ha-erteni-akarsz-merj-460886"},

    {"id": "murakozy-2025-telex-trump-tariffs",
     "title": "Sok dolgozó vesztette el állását Trump vámháborúja miatt, mégis rá szavaztak",
     "title_hu": "Sok dolgozó vesztette el állását Trump vámháborúja miatt, mégis rá szavaztak",
     "authors": ["murakozy-balazs"],
     "kind": "column", "venue": "Telex (Defacto)", "date": "2025-03-24", "language": "hu",
     "url": "https://telex.hu/defacto/2025/03/24/sok-dolgozo-vesztette-el-allasat-trump-vamhaboruja-miatt-megis-ra-szavaztak"},
    {"id": "murakozy-2025-telex-chronic-illness-labor",
     "title": "Keményen bünteti a munkaerőpiac azokat, akik valamilyen krónikus betegséggel élnek",
     "title_hu": "Keményen bünteti a munkaerőpiac azokat, akik valamilyen krónikus betegséggel élnek",
     "authors": ["murakozy-balazs", "peto-rita", "bisztray-marta"],
     "kind": "column", "venue": "Telex (Defacto)", "date": "2025-09-02", "language": "hu",
     "url": "https://telex.hu/defacto/2025/09/02/kronikus-betegseg-kevesebb-munka-kisebb-fizetes"},
    {"id": "murakozy-2019-indexdefacto-innovation-skilled-workers",
     "title": "Nem csoda kell az innovációhoz, hanem jól képzett dolgozók",
     "title_hu": "Nem csoda kell az innovációhoz, hanem jól képzett dolgozók",
     "authors": ["murakozy-balazs", "lindner-attila"],
     "kind": "blog", "venue": "Index.hu (Defacto)", "date": "2019-07-04", "language": "hu",
     "url": "https://index.hu/gazdasag/defacto/2019/07/04/nem_csoda_kell_az_innovaciohoz_hanem_jol_kepzett_dolgozok/"},
    {"id": "murakozy-2019-g7-podcast-competitiveness",
     "title": "Mit mondanak a közgazdasági kutatások a versenyképességről?",
     "title_hu": "Mit mondanak a közgazdasági kutatások a versenyképességről?",
     "authors": ["murakozy-balazs"],
     "kind": "podcast", "venue": "G7 Beszélgetések", "date": "2019-02-23", "language": "hu",
     "url": "https://telex.hu/podcast/20190223/murakozy-balazs-palyazatot-sem-lehet-nyerni-ha-nincs-aram-a-konnektorban/"},
    {"id": "bekes-murakozy-2008-portfolio-krugman",
     "title": "A pénzügyi válságok legfontosabb modellje Krugman nevéhez fűződik",
     "title_hu": "A pénzügyi válságok legfontosabb modellje Krugman nevéhez fűződik",
     "authors": ["bekes-gabor", "murakozy-balazs"],
     "kind": "column", "venue": "Portfolio.hu", "date": "2008-10-14", "language": "hu",
     "url": "https://www.portfolio.hu/gazdasag/20081014/a-penzugyi-valsagok-legfontosabb-modellje-krugman-nevehez-fuzodik-104151"},
]

POLICY_ITEMS = [
    {"id": "biro-kertesi-hajdu-2025-mt-life-expectancy",
     "title": "A várható élettartam jövedelmi egyenlőtlenségei Magyarországon 1992–1993 és 2022–2023 között",
     "authors": ["biro-aniko", "kertesi-gabor", "hajdu-tamas"],
     "outlet_kind": "chapter",
     "outlet": "Munkaerőpiaci Tükör 2023–2024",
     "outlet_issue": "2023–2024",
     "institution": "KRTK Institute of Economics",
     "year": 2025,
     "language": "hu",
     "url": "https://real.mtak.hu/219679/",
     "countries_studied": ["HU"]},
]


written = 0
for it in PRESS_ITEMS:
    f = PRESS / f'{it["id"]}.json'
    if f.exists():
        print(f"  exists, skip: {it['id']}")
        continue
    f.write_text(json.dumps(press(it), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    written += 1
    print(f"  + press/{it['id']}")
for it in POLICY_ITEMS:
    f = POLICY / f'{it["id"]}.json'
    if f.exists():
        print(f"  exists, skip: {it['id']}")
        continue
    f.write_text(json.dumps(policy(it), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    written += 1
    print(f"  + policy/{it['id']}")
print(f"\nWrote {written} files")
