"""Google Flights query helper (ILS, N adults) that keeps flight numbers.

One-way:    gf2.py ow FROM TO DATE [--stops N] [--carry] [--adults N] [--dep-after H] [--arr-before H]
Round trip: gf2.py rt FROM TO OUT_DATE BACK_DATE [--pick FLIGHTNO[,FLIGHTNO]] [same options]
  Without --pick: lists outbound options with the "from" round-trip price.
  With --pick (outbound flight numbers, e.g. LY381): lists return options with the full round-trip price.
Raw payloads are saved under raw/.
"""

import argparse
import json
import re
import time
from base64 import b64encode
from datetime import datetime, timezone
from pathlib import Path

from fast_flights.pb.flights_pb2 import Airport, Baggage, FlightData, Info, Passenger, Seat, Trip
from primp import Client
from selectolax.lexbor import LexborHTMLParser

HERE = Path(__file__).parent
RAW = HERE / "raw"
RAW.mkdir(exist_ok=True)


def _varint(n):
    out = b""
    while True:
        b = n & 0x7F
        n >>= 7
        if n:
            out += bytes([b | 0x80])
        else:
            return out + bytes([b])


def _ld(field, payload):
    return _varint((field << 3) | 2) + _varint(len(payload)) + payload


def _selected_leg(frm, date, to, flightno):
    m = re.match(r"([A-Z0-9]{2})(\d+)$", flightno)
    return _ld(
        4,
        _ld(1, frm.encode())
        + _ld(2, date.encode())
        + _ld(3, to.encode())
        + _ld(5, m[1].encode())
        + _ld(6, m[2].encode()),
    )


def build_tfs(segments, adults, carry, picks):
    """segments: list of dicts(date, frm, to, stops, dep_after, arr_before); picks: selected legs for segment 0."""
    body = b""
    for i, s in enumerate(segments):
        fd = FlightData(
            date=s["date"],
            from_airport=Airport(airport=s["frm"]),
            to_airport=Airport(airport=s["to"]),
            max_stops=s.get("stops"),
            earliest_departure_hour=s.get("dep_after"),
            latest_arrival_hour=s.get("arr_before"),
        ).SerializeToString()
        if i == 0:
            for p in picks or []:
                fd += _selected_leg(*p)
        body += _ld(3, fd)
    rest = Info(
        seat=Seat.ECONOMY,
        trip=Trip.ROUND_TRIP if len(segments) == 2 else Trip.ONE_WAY,
        passengers=[Passenger.ADULT] * adults,
        baggage=Baggage(carry_on_bags=1) if carry else None,
    ).SerializeToString()
    return b64encode(body + rest).decode()


def t(v):
    v = [*(v or []), None, None]
    return f"{v[0] or 0:02d}:{v[1] or 0:02d}"


def fetch(tfs):
    client = Client(
        impersonate="chrome_145", impersonate_os="macos", referer=True, cookie_store=True
    )
    res = client.get(
        "https://www.google.com/travel/flights/search",
        params={"tfs": tfs, "hl": "en", "curr": "ILS"},
    )
    script = LexborHTMLParser(res.text).css_first(r"script.ds\:1")
    if script is None:
        raise RuntimeError(f"no ds:1 script; status={res.status_code} len={len(res.text)}")
    return json.loads(script.text().split("data:", 1)[1].rsplit(",", 1)[0])


def rows(payload):
    out = []
    for idx in (2, 3):
        block = payload[idx]
        if not block or not block[0]:
            continue
        for k in block[0]:
            f = k[0]
            price = k[1][0][1] if k[1] and k[1][0] else None
            legs = [
                {
                    "from": s[3],
                    "to": s[6],
                    "dep": f"{'-'.join(f'{x:02d}' for x in s[20])} {t(s[8])}",
                    "arr": f"{'-'.join(f'{x:02d}' for x in s[21])} {t(s[10])}",
                    "dur": s[11],
                    "flight": f"{s[22][0]}{s[22][1]}",
                    "airline": s[22][3],
                    "operated_by": s[2],
                    "plane": s[17],
                }
                for s in f[2]
            ]
            out.append({"best": idx == 2, "price_total": price, "total_dur": f[9], "legs": legs})
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["ow", "rt"])
    ap.add_argument("frm")
    ap.add_argument("to")
    ap.add_argument("dates", nargs="+")
    ap.add_argument("--stops", type=int)
    ap.add_argument("--carry", action="store_true")
    ap.add_argument("--adults", type=int, default=3)
    ap.add_argument("--dep-after", type=int)
    ap.add_argument("--arr-before", type=int)
    ap.add_argument("--pick")
    ap.add_argument(
        "--pick-route", help="for multi-leg picks: comma list of FROM-TO-DATE matching --pick"
    )
    a = ap.parse_args()

    segs = [
        dict(
            date=a.dates[0],
            frm=a.frm,
            to=a.to,
            stops=a.stops,
            dep_after=a.dep_after,
            arr_before=a.arr_before,
        )
    ]
    if a.mode == "rt":
        segs.append(dict(date=a.dates[1], frm=a.to, to=a.frm, stops=a.stops))
    picks = None
    if a.pick:
        nos = a.pick.split(",")
        if a.pick_route:
            routes = [r.split("-", 2) for r in a.pick_route.split(",")]
            picks = [(r[0], r[2], r[1], n) for r, n in zip(routes, nos)]
        else:
            picks = [(a.frm, a.dates[0], a.to, nos[0])]
    tfs = build_tfs(segs, a.adults, a.carry, picks)
    url = f"https://www.google.com/travel/flights/search?tfs={tfs}&hl=en&curr=ILS"
    payload = fetch(tfs)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
    tag = f"{a.mode}-{a.frm}-{a.to}-{'_'.join(a.dates)}-a{a.adults}-s{a.stops}-c{int(a.carry)}-p{a.pick or ''}-d{a.dep_after}"
    rs = rows(payload)
    (RAW / f"{tag}.rows.json").write_text(
        json.dumps({"observed_utc": now, "url": url, "rows": rs}, indent=1)
    )
    print(f"# {tag} observed {now}\n# {url}")
    for r in sorted(rs, key=lambda r: (r["price_total"] is None, r["price_total"] or 0)):
        legs = " | ".join(
            f"{l['flight']} {l['from']} {l['dep'][5:]} -> {l['to']} {l['arr'][5:]}"
            + (f" (op {l['operated_by']})" if l["operated_by"] else "")
            for l in r["legs"]
        )
        d = r["total_dur"]
        print(
            f"{r['price_total']!s:>7} | {d // 60}h{d % 60:02d} | {'BEST ' if r['best'] else ''}{legs}"
        )
    time.sleep(1.5)


if __name__ == "__main__":
    main()
