"""Run a named list of ad-hoc Google Flights queries (3 adults unless stated), slowly, with caching.

Each job: key, trip, adults, max_stops, legs. Prints a compact listing per job.
Usage: run_queue.py <jobs.json> [top_n]
"""

import json
import sys

import gflights as g

jobs = json.load(open(sys.argv[1]))
top = int(sys.argv[2]) if len(sys.argv) > 2 else 12
with g.Browser() as b:
    for j in jobs:
        legs = [
            (l[0], l[1], l[2], [tuple(x) for x in l[3]] if len(l) > 3 and l[3] else None)
            for l in j["legs"]
        ]
        u = g.url_for(
            legs, j["trip"], j.get("adults", 3), j.get("max_stops"), j.get("page", "search")
        )
        try:
            r = b.capture(u, j["key"], want_text=j.get("text", False))
        except g.RateLimited as e:
            print("STOP:", e)
            break
        print("##", j["key"], len(r["rows"]), r["observed"], u, flush=True)
        for x in sorted(r["rows"], key=lambda x: x["price_total"] or 9e9)[:top]:
            print(g.fmt(x)[:240], flush=True)
        if j.get("text"):
            print(r["text"][: j.get("text_chars", 3000)])
