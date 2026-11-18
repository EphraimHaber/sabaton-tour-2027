"""Google Flights one-way / round-trip query helper.

Usage:
  gf.py ORIGIN DEST DATE [--ret DATE] [--pax N] [--stops N] [--top N]
        [--arr-before HH] [--dep-after HH] [--raw]

Prints one line per itinerary with flight numbers, local times and the price
Google shows (currency ILS). Raw payloads are cached in ./cache/.
"""

import argparse
import datetime as dt
import json
import pathlib
import sys
import time

from fast_flights import FlightQuery, Passengers, create_query
from fast_flights.fetcher import fetch_flights_html
from selectolax.lexbor import LexborHTMLParser

HERE = pathlib.Path(__file__).parent
CACHE = HERE / "cache"
CACHE.mkdir(exist_ok=True)


def fetch(
    origin, dest, date, ret=None, pax=3, stops=None, f1=None, f2=None, tag="", carry=0, checked=0
):
    legs = [FlightQuery(date=date, from_airport=origin, to_airport=dest, **(f1 or {}))]
    if ret:
        legs.append(FlightQuery(date=ret, from_airport=dest, to_airport=origin, **(f2 or {})))
    q = create_query(
        flights=legs,
        trip="round-trip" if ret else "one-way",
        passengers=Passengers(adults=pax),
        language="en",
        currency="ILS",
        max_stops=stops,
        carry_on_bags=carry,
        checked_bags=checked,
    )
    key = f"{origin}-{dest}-{date}-{ret or 'ow'}-p{pax}-s{stops}{tag}"
    f = CACHE / (key + ".json")
    if f.exists():
        return json.loads(f.read_text()), q.url()
    for attempt in range(4):
        html = fetch_flights_html(q)
        script = LexborHTMLParser(html).css_first(r"script.ds\:1")
        if script is not None:
            break
        time.sleep(4 + 4 * attempt)
    if script is None:
        (CACHE / (key + ".html")).write_text(html)
        raise SystemExit(f"no ds:1 script for {key}; html saved")
    js = script.text()
    data = js.split("data:", 1)[1].rsplit(",", 1)[0]
    payload = json.loads(data)
    f.write_text(json.dumps(payload))
    return payload, q.url()


def t(v):
    v = [*(v or []), None, None]
    return f"{v[0] or 0:02d}:{v[1] or 0:02d}"


def rows(payload):
    out = []
    for bucket in (2, 3):
        try:
            items = payload[bucket][0] or []
        except (IndexError, TypeError):
            continue
        for k in items:
            fl = k[0]
            try:
                price = k[1][0][1]
            except (IndexError, TypeError):
                price = None
            segs = []
            for s in fl[2]:
                segs.append(
                    dict(
                        frm=s[3],
                        to=s[6],
                        dep=t(s[8]),
                        arr=t(s[10]),
                        dep_date="-".join(f"{x:02d}" for x in s[20]),
                        arr_date="-".join(f"{x:02d}" for x in s[21]),
                        dur=s[11],
                        plane=s[17],
                        flt=f"{s[22][0]}{s[22][1]}",
                        airline=s[22][3],
                        operated_by=s[2],
                    )
                )
            layovers = [(l[0], l[3] if len(l) > 3 else None) for l in (fl[13] or [])]
            out.append(
                dict(
                    bucket="best" if bucket == 2 else "other",
                    price=price,
                    total_dur=fl[9],
                    segs=segs,
                    layovers=layovers,
                )
            )
    return out


def fmt(r):
    s = r["segs"]
    parts = []
    for i, g in enumerate(s):
        p = f"{g['flt']} {g['frm']} {g['dep_date'][5:]} {g['dep']}->{g['to']} {g['arr_date'][5:]} {g['arr']}"
        if g["operated_by"]:
            p += f" (op {g['operated_by']})"
        parts.append(p)
        if i < len(r["layovers"]):
            parts.append(f"[{r['layovers'][i][0]}m]")
    d = r["total_dur"]
    return f"ILS {r['price']!s:>6} | {d // 60}h{d % 60:02d} | " + " ".join(parts)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("origin")
    ap.add_argument("dest")
    ap.add_argument("date")
    ap.add_argument("--ret")
    ap.add_argument("--pax", type=int, default=3)
    ap.add_argument("--stops", type=int)
    ap.add_argument("--top", type=int, default=400)
    ap.add_argument(
        "--arr-before", help="keep itineraries arriving on/before DATE'T'HH:MM, e.g. 04-16T12:00"
    )
    ap.add_argument("--dep-after", help="keep itineraries departing at/after MM-DDTHH:MM")
    ap.add_argument("--sort", default="price")
    ap.add_argument("--carry", type=int, default=0)
    ap.add_argument("--checked", type=int, default=0)
    ap.add_argument("--dh", help="outbound departure hour window lo-hi (0-23)")
    ap.add_argument("--ah", help="outbound arrival hour window lo-hi")
    ap.add_argument("--via", help="comma list of connecting airports (outbound)")
    ap.add_argument("--al", help="comma list of airlines (outbound)")
    ap.add_argument("--rdh")
    ap.add_argument("--rah")
    ap.add_argument("--rvia")
    ap.add_argument("--ral")
    a = ap.parse_args()

    def mk(dh, ah, via, al):
        f = {}
        if dh:
            lo, hi = dh.split("-")
            f["earliest_departure_hour"] = int(lo)
            f["latest_departure_hour"] = int(hi)
        if ah:
            lo, hi = ah.split("-")
            f["earliest_arrival_hour"] = int(lo)
            f["latest_arrival_hour"] = int(hi)
        if via:
            f["connecting_airports"] = via.split(",")
        if al:
            f["airlines"] = al.split(",")
        return f

    f1 = mk(a.dh, a.ah, a.via, a.al)
    f2 = mk(a.rdh, a.rah, a.rvia, a.ral)
    tag = "".join(
        f"-{k}{v}"
        for k, v in [
            ("dh", a.dh),
            ("ah", a.ah),
            ("via", a.via),
            ("al", a.al),
            ("rdh", a.rdh),
            ("rah", a.rah),
            ("rvia", a.rvia),
            ("ral", a.ral),
        ]
        if v
    )
    tag += f"-c{a.carry}k{a.checked}" if (a.carry or a.checked) else ""
    payload, url = fetch(
        a.origin, a.dest, a.date, a.ret, a.pax, a.stops, f1, f2, tag, a.carry, a.checked
    )
    rs = rows(payload)
    print(
        f"# {a.origin}->{a.dest} {a.date} ret={a.ret} pax={a.pax} n={len(rs)} at {dt.datetime.now():%Y-%m-%d %H:%M}"
    )
    print("# " + url)

    def arr_key(r):
        g = r["segs"][-1]
        return g["arr_date"][5:] + "T" + g["arr"]

    def dep_key(r):
        g = r["segs"][0]
        return g["dep_date"][5:] + "T" + g["dep"]

    if a.arr_before:
        rs = [r for r in rs if arr_key(r) <= a.arr_before]
    if a.dep_after:
        rs = [r for r in rs if dep_key(r) >= a.dep_after]
    if a.sort == "price":
        rs.sort(key=lambda r: (r["price"] is None, r["price"] or 0))
    elif a.sort == "arr":
        rs.sort(key=arr_key)
    elif a.sort == "dep":
        rs.sort(key=dep_key)
    for r in rs[: a.top]:
        print(fmt(r))
