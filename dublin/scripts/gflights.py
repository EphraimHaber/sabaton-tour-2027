"""Google Flights capture via headless Chrome.

Loads a search URL (3 adults, ILS by default), captures the GetShoppingResults RPC
responses the page itself makes, and parses every itinerary row (flight numbers,
times, layovers, price). Results are cached as JSON under ../data/raw/.

Prices are the totals Google shows for all passengers in the search.
"""

import base64
import datetime
import json
import os
import re
import time

from playwright.sync_api import sync_playwright

RAW = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "raw")
os.makedirs(RAW, exist_ok=True)


# --- minimal protobuf encoder for the ?tfs= parameter -----------------------
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
    if isinstance(payload, str):
        payload = payload.encode()
    return _varint(field << 3 | 2) + _varint(len(payload)) + payload


def _vi(field, n):
    return _varint(field << 3) + _varint(n)


def tfs(legs, trip, adults=3, max_stops=None):
    """legs: [(date, frm, to, selected)] where selected is a list of
    (frm, date, to, airline_code, flight_number) for an already-chosen itinerary, or None.
    trip: 'round-trip' | 'one-way' | 'multi-city'."""
    body = b""
    for date, frm, to, selected in legs:
        fd = _ld(2, date)
        for sf, sd, st, al, num in selected or []:
            fd += _ld(4, _ld(1, sf) + _ld(2, sd) + _ld(3, st) + _ld(5, al) + _ld(6, str(num)))
        if max_stops is not None:
            fd += _vi(5, max_stops)
        for a in frm.split("+"):
            fd += _ld(13, _vi(1, 1) + _ld(2, a))
        for a in to.split("+"):
            fd += _ld(14, _vi(1, 1) + _ld(2, a))
        body += _ld(3, fd)
    body += _ld(8, bytes([1] * adults))
    body += _vi(9, 1)
    body += _vi(19, {"round-trip": 1, "one-way": 2, "multi-city": 3}[trip])
    return base64.urlsafe_b64encode(body).decode().rstrip("=")


def url_for(legs, trip, adults=3, max_stops=None, page="search"):
    return f"https://www.google.com/travel/flights/{page}?tfs={tfs(legs, trip, adults, max_stops)}&hl=en&curr=ILS"


# --- response parsing --------------------------------------------------------
def _t(v):
    v = [*(v or []), None, None]
    return "%02d:%02d" % (v[0] or 0, v[1] or 0)


def _chunks(text):
    """Yield the decoded inner payload of every wrb.fr chunk in a batchexecute-style body."""
    for m in re.finditer(r"^\[\[\"wrb\.fr\".*$", text, re.M):
        try:
            outer = json.loads(m.group(0))
            if outer[0][2]:
                yield json.loads(outer[0][2])
        except Exception:
            continue


def parse_rows(inner):
    out = []
    for sec, name in ((2, "best"), (3, "other")):
        if len(inner) <= sec or not inner[sec] or not inner[sec][0]:
            continue
        for k in inner[sec][0]:
            f = k[0]
            try:
                price = k[1][0][1]
            except Exception:
                price = None
            segs = []
            for s in f[2]:
                segs.append(
                    dict(
                        fn=f"{s[22][0]}{s[22][1]}",
                        airline=s[22][3],
                        operated_by=s[2] or None,
                        frm=s[3],
                        to=s[6],
                        dep="%04d-%02d-%02d " % tuple(s[20]) + _t(s[8]),
                        arr="%04d-%02d-%02d " % tuple(s[21]) + _t(s[10]),
                        dur_min=s[11],
                        aircraft=s[17],
                    )
                )
            lay = []
            for l in f[13] or []:
                lay.append(dict(airport=l[1] if len(l) > 1 else None, dur_min=l[0]))
            out.append(
                dict(
                    section=name,
                    price_total=price,
                    dur_min=f[9],
                    segs=segs,
                    layovers=lay,
                    airlines=f[1],
                )
            )
    return out


class RateLimited(Exception):
    pass


# --- browser -----------------------------------------------------------------
class Browser:
    pause_s = 12  # polite gap between uncached page loads

    def __enter__(self):
        self.pw = sync_playwright().start()
        self.b = self.pw.chromium.launch(channel="chrome", headless=True)
        self.ctx = self.b.new_context(locale="en-US", viewport={"width": 1400, "height": 2400})
        return self

    def __exit__(self, *a):
        self.b.close()
        self.pw.stop()

    def capture(self, url, key=None, wait_ms=7000, want_text=False, force=False):
        """Return dict(observed, url, rows, text). Cached by key."""
        path = os.path.join(RAW, key + ".json") if key else None
        if path and os.path.exists(path) and not force:
            return json.load(open(path))
        out = None
        for attempt in range(3):
            out = self._capture_once(url, wait_ms, want_text)
            if out["rows"] or "Booking options" in out["text"]:
                break
            if "/sorry/" in out["final_url"]:
                raise RateLimited("Google served its unusual-traffic page; stop and retry later")
            if "Oops, something went wrong" in out["text"] and attempt == 2:
                raise RateLimited(
                    "Google returned its generic error page three times; stop and retry later"
                )
            time.sleep(30)
        if path:
            json.dump(out, open(path, "w"), ensure_ascii=False, indent=1)
        time.sleep(self.pause_s)
        return out

    def _capture_once(self, url, wait_ms, want_text):
        page = self.ctx.new_page()
        bodies = []

        def on_resp(r):
            if "GetShoppingResults" in r.url or "GetBookingResults" in r.url:
                try:
                    bodies.append(r.text())
                except Exception:
                    pass

        page.on("response", on_resp)
        rows, text, expanded = [], "", False
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=45000)
            deadline = time.time() + wait_ms / 1000 + 12
            page.wait_for_timeout(wait_ms)
            while not bodies and time.time() < deadline:
                page.wait_for_timeout(1000)
            page.wait_for_timeout(1500)
            # the first response only carries the "top" list; expand to the full list
            try:
                btn = page.get_by_role(
                    "button", name=re.compile(r"(more|other) flights|View more", re.I)
                ).first
                if btn.is_visible(timeout=1500):
                    n0 = len(bodies)
                    btn.click()
                    t_end = time.time() + 12
                    while len(bodies) == n0 and time.time() < t_end:
                        page.wait_for_timeout(500)
                    page.wait_for_timeout(1500)
                    expanded = True
            except Exception:
                pass
            for b in bodies:
                for inner in _chunks(b):
                    rows.extend(parse_rows(inner))
            # short result lists are server-rendered into the page instead of fetched by RPC
            html = page.content()
            m = re.search(
                r"AF_initDataCallback\(\{key: 'ds:1'.*?data:(.*?), sideChannel: \{\}\}\);",
                html,
                re.S,
            )
            if m:
                try:
                    rows.extend(parse_rows(json.loads(m.group(1))))
                except Exception:
                    pass
            if want_text or not rows:
                text = page.inner_text("body")[:20000]
            final_url = page.url
        finally:
            page.close()
        # de-duplicate (same flights + price can appear in several chunks)
        seen, uniq = set(), []
        for r in rows:
            k = (tuple((s["fn"], s["dep"]) for s in r["segs"]), r["price_total"])
            if k not in seen:
                seen.add(k)
                uniq.append(r)
        out = dict(
            observed=datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
            url=url,
            final_url=final_url,
            expanded=expanded,
            rows=uniq,
            text=text,
        )
        return out


def fmt(r):
    s = " | ".join(
        f"{x['fn']} {x['frm']} {x['dep'][5:]}->{x['to']} {x['arr'][5:]}"
        + (f" (op {x['operated_by']})" if x["operated_by"] else "")
        for x in r["segs"]
    )
    lay = ",".join(
        f"{l['airport']}:{l['dur_min'] // 60}h{l['dur_min'] % 60:02d}" for l in r["layovers"]
    )
    return f"{r['price_total']!s:>7} {r['dur_min'] // 60}h{r['dur_min'] % 60:02d} [{lay}] {s}"
