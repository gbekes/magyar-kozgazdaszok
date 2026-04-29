"""Set abstract and EN draft on Fredriksson-Neumayer-Ujhelyi 2007 PubChoice."""
import json
from pathlib import Path

PAPERS = Path(__file__).resolve().parent.parent / "data" / "papers"
slug = "fredriksson-neumayer-et-al-2007-pc"
f = PAPERS / f"{slug}.json"
p = json.loads(f.read_text(encoding="utf-8"))
p["abstract"] = (
    "Does environmental lobbying affect the probability of environmental treaty "
    "ratification? Does the level of government corruption play a role for the "
    "success of such lobbying? In this paper, we propose that a more corruptible "
    "government may be more responsive to the demands of the environmental lobby. "
    "We use several stratified hazard models and panel data from 170 countries on "
    "the timing of Kyoto Protocol ratification to test this hypothesis. We find "
    "that increased environmental lobby group activity raises the probability of "
    "ratification, and the effect rises with the degree of corruption."
)
f.write_text(json.dumps(p, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"abstract set: {slug}")
