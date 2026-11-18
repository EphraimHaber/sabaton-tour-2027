"""Round-trip TLV<->DUB sweep, 3 adults, ILS.

For each outbound date, list every outbound itinerary Google returns, then select each
one in turn and list the return itineraries with the combined round-trip total.
Writes ../data/roundtrips_<origin>-<dest>.json.
Usage: run_roundtrips.py ORIGIN DEST OUT_DATE[,OUT_DATE...] RET_DATE[,RET_DATE...] [max_outbounds]
"""

import json
import os
import sys

import gflights as g

origin, dest, outs, rets = sys.argv[1], sys.argv[2], sys.argv[3].split(","), sys.argv[4].split(",")
max_out = int(sys.argv[5]) if len(sys.argv) > 5 else 40
combos = []
with g.Browser() as b:
    for od in outs:
        for rd in rets:
            tag = f"rt_{origin}-{dest}_{od[5:]}_{rd[5:]}"
            u = g.url_for([(od, origin, dest, None), (rd, dest, origin, None)], "round-trip")
            r = b.capture(u, tag + "_out")
            outb = sorted(r["rows"], key=lambda x: x["price_total"] or 9e9)[:max_out]
            print(tag, "outbounds:", len(r["rows"]), flush=True)
            for o in outb:
                sel = [
                    (s["frm"], s["dep"][:10], s["to"], s["fn"][:2], s["fn"][2:]) for s in o["segs"]
                ]
                key = tag + "_ret_" + "-".join(s["fn"] for s in o["segs"])
                u2 = g.url_for([(od, origin, dest, sel), (rd, dest, origin, None)], "round-trip")
                r2 = b.capture(u2, key)
                print("  ", g.fmt(o), "-> returns:", len(r2["rows"]), flush=True)
                for x in r2["rows"]:
                    sel2 = [
                        (s["frm"], s["dep"][:10], s["to"], s["fn"][:2], s["fn"][2:])
                        for s in x["segs"]
                    ]
                    combos.append(
                        dict(
                            out_date=od,
                            ret_date=rd,
                            outbound=o,
                            inbound=x,
                            rt_total=x["price_total"],
                            observed=r2["observed"],
                            search_url=u2,
                            booking_url=g.url_for(
                                [(od, origin, dest, sel), (rd, dest, origin, sel2)],
                                "round-trip",
                                page="booking",
                            ),
                        )
                    )
out = os.path.join(
    g.RAW,
    "..",
    f"roundtrips_{origin}-{dest}_{'_'.join(d[5:] for d in outs)}__{'_'.join(d[5:] for d in rets)}.json",
)
json.dump(combos, open(out, "w"), ensure_ascii=False, indent=1)
print("combos:", len(combos), "->", os.path.normpath(out))
