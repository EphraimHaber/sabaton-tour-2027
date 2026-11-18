"""One-way sweeps, 3 adults, ILS, for building self-transfer / deviation itineraries.

mode 'direct': TLV<->DUB one-way, any number of stops.
mode 'hubs':   nonstop TLV->X, X->DUB, DUB->X, X->TLV for candidate transfer airports X.
Writes ../data/oneways_<mode>.json (flat list of rows with query metadata).
"""

import json
import os
import sys

import gflights as g

GROUPS = [
    "LHR+LGW+LTN+STN+MAN+EDI",
    "BFS+BHX+LPL+GLA+BRS+NCL",
    "AMS+CDG+ORY+BRU+FRA+MUC",
    "ZRH+GVA+BSL+VIE+BUD+PRG",
    "WAW+KRK+KTW+GDN+WRO+POZ",
    "ATH+SKG+FCO+CIA+MXP+BGY",
    "NAP+VCE+BLQ+BCN+MAD+LIS",
    "BER+DUS+HAM+CGN+STR+CPH",
    "OTP+SOF+LCA+PFO+RIX+VNO",
    "MRS+NCE+MLA+BEG+IAS+CLJ",
]
mode = sys.argv[1]
jobs = []
if mode == "direct":
    for d in ("2027-04-04", "2027-04-05", "2027-04-06", "2027-04-07"):
        jobs.append(("TLV", "DUB", d, None))
    for d in ("2027-04-07", "2027-04-08", "2027-04-09"):
        jobs.append(("DUB", "TLV", d, None))
else:
    for grp in GROUPS:
        for d in ("2027-04-04", "2027-04-05", "2027-04-06"):
            jobs.append(("TLV", grp, d, 0))
        for d in ("2027-04-05", "2027-04-06", "2027-04-07"):
            jobs.append((grp, "DUB", d, 0))
        for d in ("2027-04-07", "2027-04-08"):
            jobs.append(("DUB", grp, d, 0))
        for d in ("2027-04-08", "2027-04-09"):
            jobs.append((grp, "TLV", d, 0))
rows = []
with g.Browser() as b:
    for frm, to, d, ms in jobs:
        key = f"ow_{frm}_{to}_{d[5:]}_{'ns' if ms == 0 else 'any'}"
        u = g.url_for([(d, frm, to, None)], "one-way", max_stops=ms)
        r = b.capture(u, key)
        print(key, len(r["rows"]), flush=True)
        for x in r["rows"]:
            rows.append(
                dict(
                    q_from=frm,
                    q_to=to,
                    date=d,
                    nonstop_only=(ms == 0),
                    observed=r["observed"],
                    search_url=u,
                    **x,
                )
            )
out = os.path.join(g.RAW, "..", f"oneways_{mode}.json")
json.dump(rows, open(out, "w"), ensure_ascii=False, indent=1)
print("rows:", len(rows))
