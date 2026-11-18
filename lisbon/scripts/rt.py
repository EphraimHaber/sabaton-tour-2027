"""Round-trip pricing with a pinned outbound: lists return options and RT totals.

Usage: rt.py ORIGIN DEST OUT_DATE RET_DATE "SEG;SEG" [--pax N] [--ret-sel "SEG;SEG"]
  SEG = FROM,YYYY-MM-DD,TO,AIRLINE,NUMBER  (one per outbound flight segment)
Prices are what Google Flights embeds for the page (currency ILS, all passengers).
"""

import argparse
import datetime as dt
import hashlib
import json
import pathlib
import sys
import time
from base64 import b64encode

import gf
from fast_flights import FlightQuery, Passengers, create_query
from fast_flights.pb.flights_pb2 import FlightData
from primp import Client
from selectolax.lexbor import LexborHTMLParser


def varint(n):
    out = b""
    while True:
        b = n & 0x7F
        n >>= 7
        if n:
            out += bytes([b | 0x80])
        else:
            return out + bytes([b])


def ld(field, payload: bytes):
    return varint((field << 3) | 2) + varint(len(payload)) + payload


def seg_bytes(spec):
    frm, date, to, al, num = spec.split(",")
    inner = (
        ld(1, frm.encode())
        + ld(2, date.encode())
        + ld(3, to.encode())
        + ld(5, al.encode())
        + ld(6, num.encode())
    )
    return ld(4, inner)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("origin")
    ap.add_argument("dest")
    ap.add_argument("out")
    ap.add_argument("ret")
    ap.add_argument("sel")
    ap.add_argument("--pax", type=int, default=3)
    ap.add_argument("--ret-sel")
    ap.add_argument("--oneway-dest", help="for open-jaw: return leg origin,dest e.g. LIS,ATH")
    a = ap.parse_args()
    rfrom, rto = a.oneway_dest.split(",") if a.oneway_dest else (a.dest, a.origin)
    q = create_query(
        flights=[
            FlightQuery(date=a.out, from_airport=a.origin, to_airport=a.dest),
            FlightQuery(date=a.ret, from_airport=rfrom, to_airport=rto),
        ],
        trip="multi-city" if a.oneway_dest else "round-trip",
        passengers=Passengers(adults=a.pax),
        language="en",
        currency="ILS",
    )
    extra = b"".join(seg_bytes(s) for s in a.sel.split(";"))
    q.flight_data[0] = FlightData.FromString(q.flight_data[0].SerializeToString() + extra)
    if a.ret_sel:
        extra2 = b"".join(seg_bytes(s) for s in a.ret_sel.split(";"))
        q.flight_data[1] = FlightData.FromString(q.flight_data[1].SerializeToString() + extra2)
    key = hashlib.md5(q.to_str().encode()).hexdigest()[:12]
    f = gf.CACHE / f"rt-{a.origin}-{a.dest}-{a.out}-{a.ret}-{key}.json"
    print(
        f"# RT {a.origin}-{a.dest} out {a.out} [{a.sel}] ret {a.ret} pax={a.pax} at {dt.datetime.now():%Y-%m-%d %H:%M}"
    )
    print("# " + q.url())
    if f.exists():
        payload = json.loads(f.read_text())
    else:
        client = Client(
            impersonate="chrome_145", impersonate_os="macos", referer=True, cookie_store=True
        )
        for attempt in range(4):
            html = client.get(
                "https://www.google.com/travel/flights/search", params=q.params()
            ).text
            script = LexborHTMLParser(html).css_first(r"script.ds\:1")
            if script is not None:
                break
            time.sleep(5 + 4 * attempt)
        if script is None:
            raise SystemExit("blocked (no ds:1)")
        payload = json.loads(script.text().split("data:", 1)[1].rsplit(",", 1)[0])
        f.write_text(json.dumps(payload))
    rs = gf.rows(payload)
    rs.sort(key=lambda r: (r["price"] is None, r["price"] or 0))
    for r in rs:
        print(gf.fmt(r))


main()
