"""Query Google Flights (one-way, N adults, ILS) and print every itinerary with flight numbers.

Usage: gf.py FROM TO YYYY-MM-DD [adults] [max_stops]
Saves the raw payload JSON under raw/ next to this script.
"""

import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from fast_flights import FlightQuery, Passengers, create_query
from primp import Client
from selectolax.lexbor import LexborHTMLParser

HERE = Path(__file__).parent
RAW = HERE / "raw"
RAW.mkdir(exist_ok=True)


def t(v):
    v = [*(v or []), None, None]
    return f"{v[0] or 0:02d}:{v[1] or 0:02d}"


def fetch(frm, to, date, adults=3, max_stops=None, trip="one-way", ret=None):
    flights = [FlightQuery(date=date, from_airport=frm, to_airport=to)]
    if ret:
        flights.append(FlightQuery(date=ret, from_airport=to, to_airport=frm))
    q = create_query(
        flights=flights,
        trip=trip,
        passengers=Passengers(adults=adults),
        language="en",
        currency="ILS",
        max_stops=max_stops,
    )
    client = Client(
        impersonate="chrome_145", impersonate_os="macos", referer=True, cookie_store=True
    )
    res = client.get("https://www.google.com/travel/flights", params=q.params())
    html = res.text
    script = LexborHTMLParser(html).css_first(r"script.ds\:1")
    if script is None:
        raise RuntimeError(f"no ds:1 script; status={res.status_code} len={len(html)}")
    data = script.text().split("data:", 1)[1].rsplit(",", 1)[0]
    payload = json.loads(data)
    return q.url(), payload


def rows(payload):
    out = []
    for idx in (2, 3):
        block = payload[idx]
        if not block or not block[0]:
            continue
        for k in block[0]:
            f = k[0]
            price = k[1][0][1] if k[1] and k[1][0] else None
            legs = []
            for s in f[2]:
                legs.append(
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
                )
            out.append({"best": idx == 2, "price_total": price, "total_dur": f[9], "legs": legs})
    return out


def main():
    frm, to, date = sys.argv[1:4]
    adults = int(sys.argv[4]) if len(sys.argv) > 4 else 3
    max_stops = int(sys.argv[5]) if len(sys.argv) > 5 and sys.argv[5] != "-" else None
    url, payload = fetch(frm, to, date, adults, max_stops)
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
    (RAW / f"{frm}-{to}-{date}-a{adults}-s{max_stops}.json").write_text(json.dumps(payload))
    rs = rows(payload)
    (RAW / f"{frm}-{to}-{date}-a{adults}-s{max_stops}.rows.json").write_text(
        json.dumps({"observed_utc": now, "url": url, "rows": rs}, indent=1)
    )
    print(f"# {frm}->{to} {date} adults={adults} stops<={max_stops} observed {now}\n# {url}")
    for r in sorted(rs, key=lambda r: (r["price_total"] is None, r["price_total"] or 0)):
        legs = " | ".join(
            f"{l['flight']} {l['from']} {l['dep'][5:]} -> {l['to']} {l['arr'][5:]}"
            + (f" (op {l['operated_by']})" if l["operated_by"] else "")
            for l in r["legs"]
        )
        d = r["total_dur"]
        print(
            f"{r['price_total']!s:>7} total | {d // 60}h{d % 60:02d} | {'BEST ' if r['best'] else ''}{legs}"
        )


if __name__ == "__main__":
    main()
    time.sleep(1)
