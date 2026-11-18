"""Build ../flights.md and ../data/itineraries.json from the captured raw data.

Leg times, flight numbers and durations are read from ../data/raw/*.json (never typed by hand);
prices are the figures recorded on the cited capture and are asserted against the raw data where
the raw data carries them.
"""

import datetime as dt
import glob
import json
import os
import re

import gflights as g

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "..", "data", "raw")
USD_ILS = 3.2463  # Frankfurter (ECB reference rates), 2026-11-17
GBP_ILS = round(3.2463 / 0.75808, 4)
TZ = dict(
    TLV=3, ATH=3, CLJ=3, DUB=1, LHR=1, LGW=1, LTN=1, STN=1, FRA=2, MUC=2, CDG=2, AMS=2, FCO=2, ZRH=2
)
AIRLINE_SITE = dict(
    LH="https://www.lufthansa.com/il/en/homepage",
    AF="https://wwws.airfrance.co.il/",
    KL="https://www.klm.co.il/",
    BA="https://www.britishairways.com/",
    A3="https://en.aegeanair.com/",
    AZ="https://www.ita-airways.com/",
    FR="https://www.ryanair.com/ie/en",
    W4="https://www.wizzair.com/",
    W9="https://www.wizzair.com/",
    **{"6H": "https://www.israir.co.il/"},
)

# ---- index every captured segment and every captured row ---------------------
SEG, ROWS = {}, []
for f in glob.glob(os.path.join(RAW, "*.json")):
    d = json.load(open(f))
    for r in d.get("rows", []):
        ROWS.append((os.path.basename(f), d["observed"], d["url"], r))
        for s in r["segs"]:
            SEG.setdefault((s["fn"], s["dep"][:10]), s)


def segs(spec):
    """spec: 'LH687@04-06 LH982@04-06' -> list of segment dicts from the raw captures."""
    out = []
    for tok in spec.split():
        fn, d = tok.split("@")
        out.append(SEG[(fn, "2027-" + d)])
    return out


def find_row(spec, file_prefix):
    want = [(s["fn"], s["dep"]) for s in segs(spec)]
    hits = [
        (f, o, u, r)
        for f, o, u, r in ROWS
        if f.startswith(file_prefix) and [(s["fn"], s["dep"]) for s in r["segs"]] == want
    ]
    assert hits, (spec, file_prefix)
    return hits[0]


def utc(local, ap):
    return dt.datetime.strptime(local, "%Y-%m-%d %H:%M") - dt.timedelta(hours=TZ[ap])


def elapsed(ss):
    m = int(
        (utc(ss[-1]["arr"], ss[-1]["to"]) - utc(ss[0]["dep"], ss[0]["frm"])).total_seconds() // 60
    )
    return m


def hm(m):
    return f"{m // 60}h{m % 60:02d}"


def sel(ss):
    return [
        (
            s["frm"],
            s["dep"][:10],
            s["to"],
            re.match(r"([A-Z0-9]{2})(\d+)$", s["fn"]).group(1),
            re.match(r"([A-Z0-9]{2})(\d+)$", s["fn"]).group(2),
        )
        for s in ss
    ]


def gf_booking(dirs, trip):
    legs = [(ss[0]["dep"][:10], ss[0]["frm"], ss[-1]["to"], sel(ss)) for ss in dirs]
    return g.url_for(legs, trip, page="booking")


def gf_search(frm, to, d1, d2=None):
    legs = [(d1, frm, to, None)] + ([(d2, to, frm, None)] if d2 else [])
    return g.url_for(legs, "round-trip" if d2 else "one-way")


def booking_obs(key):
    d = json.load(open(os.path.join(RAW, f"booking_{key}.json")))
    t = d["text"]
    head = t[t.find("passenger") : t.find("Selected flights")]
    price = int(re.search(r"₪([\d,]+)", head).group(1).replace(",", ""))
    opts = t[t.find("Booking options") : t.find("Prices include")]
    sellers = re.findall(r"Book with (.+?)\n(₪[\d,]+)\n([^\n]*\d)", opts)
    bags = [
        l.strip()
        for l in t.split("\n")
        if re.search(r"carry-on|checked bag per passenger", l) and "costs between" not in l
    ]
    return dict(
        price=price,
        sellers=[
            dict(seller=re.sub(r"Airline$", " (airline direct)", a), ils=b, native=c)
            for a, b, c in sellers
        ],
        bags=bags,
        observed=d["observed"],
        url=d["url"],
    )


WD = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def when(local):
    d = dt.datetime.strptime(local, "%Y-%m-%d %H:%M")
    return f"{WD[d.weekday()]} {d.day} Apr {d:%H:%M}"


def friday_status(ss):
    arr = ss[-1]["arr"]
    if arr[:10] != "2027-04-09":
        return (
            "not applicable"
            if arr[:10] < "2027-04-09"
            else "not applicable (extended weekend - see label)"
        )
    return "OK" if arr <= "2027-04-09 12:00" else "FAIL"


def leg_table(ss):
    lines = [
        "| # | Flight | Operated by | From | Departs (local) | To | Arrives (local) | Flight time | Layover after |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for i, s in enumerate(ss):
        lay = ""
        if i + 1 < len(ss):
            n = ss[i + 1]
            lm = int((utc(n["dep"], n["frm"]) - utc(s["arr"], s["to"])).total_seconds() // 60)
            lay = f"{hm(lm)} at {s['to']}" + (
                f" -> {n['frm']} (airport change)" if n["frm"] != s["to"] else ""
            )
        op = s["operated_by"] or s["airline"]
        lines.append(
            f"| {i + 1} | {s['fn']} | {op} | {s['frm']} | {when(s['dep'])} | {s['to']} | {when(s['arr'])} | {hm(s['dur_min'])} | {lay} |"
        )
    return "\n".join(lines)


# ---- itinerary definitions ---------------------------------------------------
LH_BAGS = dict(
    included="Personal item (40x30x15 cm) + 1 cabin bag up to 8 kg (55x40x23 cm). Fare brand on Kayak for the Lufthansa options in the 5 and 6 Apr searches: Economy Light. No checked bag.",
    trolley_nis="0 (cabin trolley included)",
    checked_nis="0-553 per passenger for the whole round trip (Google Flights range; exact fee set on lufthansa.com)",
)
LH_OW_BAGS = dict(
    LH_BAGS, checked_nis="0-251 per passenger (Google Flights range for this one-way)"
)
AFKL_BAGS = dict(
    included="1 free carry-on per passenger (Google Flights). Fare brand on Kayak in the 6 Apr search: Light. Checked bag not included.",
    trolley_nis="0 (carry-on included per Google Flights)",
    checked_nis="available for a fee - amount not shown, not verified",
)
FR_BAGS = "Ryanair Basic: one small under-seat bag 40x30x20 cm only."


def RT(
    id_,
    title,
    tags,
    out,
    ret,
    total,
    bk,
    bags,
    kayak=None,
    notes=(),
    deviation=None,
    risk=None,
    verification="verified",
    extra_checks=(),
):
    return dict(
        id=id_,
        title=title,
        tags=tags,
        kind="round-trip (one ticket)",
        out=out,
        ret=ret,
        total=total,
        bk=bk,
        bags=bags,
        kayak=kayak,
        notes=list(notes),
        deviation=deviation,
        risk=risk,
        verification=verification,
        extra_checks=list(extra_checks),
    )


ITINS = [
    RT(
        "DUB-01",
        "Lufthansa via Frankfurt, Tue 6 Apr -> Thu 8 Apr",
        ["best overall", "cheapest single-ticket"],
        "LH687@04-06 LH982@04-06",
        "LH979@04-08 LH690@04-08",
        4681,
        "DUB-01_LH687-LH982__LH979-LH690",
        LH_BAGS,
        kayak=dict(usd_pp=461, usd_total=1381, file="kayak_TLV-DUB_0406_0408_LH.txt"),
        notes=[
            "1 night before the show. The 1h00 connection at FRA outbound is short; it is one ticket, so a missed connection is rebooked by Lufthansa - LH982 (21:10) is the latest FRA-DUB flight seen in any capture, so a misconnect most likely means the next morning's LH976 (lands Dublin 08:05) - still before the show.",
            "Same price whether searched with 1, 2 or 3 adults (1,560 pp) - no group penalty.",
        ],
    ),
    RT(
        "DUB-02",
        "Lufthansa via Frankfurt, Mon 5 Apr -> Thu 8 Apr",
        ["2 nights before"],
        "LH687@04-05 LH982@04-05",
        "LH979@04-08 LH690@04-08",
        5081,
        "DUB-02_LH_0405",
        LH_BAGS,
        kayak=dict(usd_pp=499, usd_total=1496, file="kayak_TLV-DUB_0405_0408_LH.txt"),
        notes=[
            "Same flights as DUB-01 one day earlier: +133 pp, plus one more hotel night. A full buffer day against the short FRA connection."
        ],
    ),
    RT(
        "DUB-03",
        "Lufthansa via Frankfurt, fastest both ways, Tue 6 Apr -> Thu 8 Apr (05:55 departure)",
        ["fastest"],
        "LH687@04-06 LH982@04-06",
        "LH983@04-08 LH686@04-08",
        5569,
        "LH_0406_retFast",
        LH_BAGS,
        kayak=dict(usd_pp=526, usd_total=1578, file="kayak_TLV-DUB_0406_0408_LH.txt"),
        notes=[
            "Shortest total travel time found (7h45 out, 7h30 back) and home Thursday 15:25. The return leaves Dublin 05:55 - about 7 hours after the show ends, so effectively no sleep.",
            "The quickest outbound of all, KL462+KL1137 (7h40), costs 3,258-3,920 pp as a round trip and is listed under rejected.",
        ],
    ),
    RT(
        "DUB-04",
        "Lufthansa via Frankfurt, daytime arrival Tue 6 Apr -> Thu 8 Apr",
        ["best-timed"],
        "LH691@04-06 LH978@04-06",
        "LH979@04-08 LH690@04-08",
        5569,
        "LH_0406early_ret",
        LH_BAGS,
        notes=[
            "Lands Dublin Tue 11:55 instead of 22:15: a usable afternoon and evening in Dublin the day before the show, and a 2h25 FRA connection instead of 1h00. Costs +296 pp over DUB-01. Leaves TLV 04:45."
        ],
    ),
    RT(
        "DUB-05",
        "Air France out / KLM back, Mon 5 Apr -> Thu 8 Apr evening (lands Fri 02:35)",
        ["most time in Dublin", "2 nights before"],
        "AF963@04-05 AF1016@04-05",
        "KL1142@04-08 KL461@04-08",
        5887,
        "AFKL_0405",
        AFKL_BAGS,
        notes=[
            "Leaves Dublin Thu 17:20, so Thursday is a full sightseeing day; lands TLV Fri 02:35 (Friday rule OK with 9h25 to spare before the 12:00 cutoff).",
            "1h15 connection at AMS on the way home, and KL461 is the only KLM AMS-TLV flight seen in the captures: a misconnect would push arrival into Friday daytime or later - the Friday-rule risk of this option.",
        ],
    ),
    RT(
        "DUB-06",
        "Air France out / KLM back, Tue 6 Apr -> Thu 8 Apr evening (lands Fri 02:35)",
        ["most time in Dublin"],
        "AF963@04-06 AF1016@04-06",
        "KL1142@04-08 KL461@04-08",
        6649,
        "AFKL_0406",
        AFKL_BAGS,
        kayak=dict(usd_pp=682, usd_total=2044, file="kayak_TLV-DUB_0406_0408_AFKL.txt"),
        notes=["Tuesday version of DUB-05; oddly 254 pp more expensive than leaving Monday."],
    ),
    RT(
        "DUB-07",
        "British Airways via Heathrow, Tue 6 Apr -> Thu 8 Apr (lands Fri 03:55)",
        ["most comfortable"],
        "BA405@04-06 BA830@04-06",
        "BA831@04-08 BA404@04-08",
        8525,
        "BA_0406",
        dict(
            included="1 free carry-on and 1st checked bag free per passenger (Google Flights).",
            trolley_nis="0 (included)",
            checked_nis="0 (first checked bag included)",
        ),
        notes=[
            "Only option found with a checked bag included, and long, relaxed connections (3h30 at LHR both ways). Lands Dublin Tue 14:30; leaves Dublin Thu 15:30.",
            "Connection at Heathrow is airside on one ticket. gov.uk says an ETA is needed when 'passing through border control'; whether an airside connection needs one was not confirmed - check before booking.",
            "The same round trip appeared at 8,525 and 8,527 in different captures (rounding).",
        ],
    ),
    RT(
        "DUB-08",
        "Lufthansa via Frankfurt, show-day arrival Wed 7 Apr 11:55 -> Thu 8 Apr",
        ["RISKY: arrives on show day"],
        "LH691@04-07 LH978@04-07",
        "LH979@04-08 LH690@04-08",
        6770,
        "LH_0407showday",
        LH_BAGS,
        risk="Arrives 11:55 on show day (inside the 13:00 limit) but any misconnect at FRA means the next flights land 16:50 or 22:15. It is also 697 pp MORE expensive than DUB-01, so there is no reason to pick it unless Tuesday is impossible.",
        notes=[
            "Other show-day arrivals by 13:00 (one-way prices, 3 adults): KL462+KL1137 10:25 (8,943), BA405+BA826 12:05 (5,110), LX257+LX400 12:10 (4,960), RO156+RO361+KL1139 12:40 (3,659)."
        ],
    ),
]


def custom(
    id_, title, tags, tickets, bags, notes, deviation, risk, verification, kind, extra_pp=None
):
    return dict(
        id=id_,
        title=title,
        tags=tags,
        kind=kind,
        tickets=tickets,
        bags=bags,
        notes=notes,
        deviation=deviation,
        risk=risk,
        verification=verification,
        extra_pp=extra_pp,
    )


def T(direction, spec, bk=None, row_file=None, price=None, note=""):
    return dict(direction=direction, spec=spec, bk=bk, row_file=row_file, price=price, note=note)


CUSTOM = [
    custom(
        "DUB-09",
        "Cheapest with protected connections: Aegean out Mon 5 Apr, Lufthansa/ITA back Thu 8 Apr (two one-way tickets)",
        ["cheapest protected", "2 nights before"],
        [
            T("out", "A3925@04-05 A3630@04-05", bk="OW_A3_0405"),
            T("ret", "LH983@04-08 AZ403@04-08 AZ812@04-08", bk="OW_LHAZ_ret_0408"),
        ],
        dict(
            included="Aegean: 1 free carry-on (Google Flights). Lufthansa/ITA ticket: 1 free carry-on.",
            trolley_nis="0 (carry-on included on both tickets per Google Flights)",
            checked_nis="Aegean: fee, amount not shown; Lufthansa ticket: 0-251 per passenger",
        ),
        [
            "Two separate one-way tickets, but each ticket's own connection is protected by its airline. Saves 165 pp against DUB-01.",
            "Price of the saving: lands Dublin Mon 23:05 (extra hotel night versus DUB-01), and the return leaves 05:55 after the show with two stops, 12h25 door to door.",
            "Swap the return for LH979+LH690 (12:40 -> 23:15, one-way 3,195 for 3) and the total becomes 5,078 = 1,693 pp - the same as DUB-02, so no saving.",
        ],
        None,
        None,
        "verified",
        "two one-way tickets",
    ),
    custom(
        "DUB-10",
        "Cheapest found: self-transfer via Athens out Tue 6 Apr, via Cluj back Thu 8 Apr (lands Fri 08:35)",
        ["cheapest overall", "self-transfer", "DEVIATION"],
        [
            T("out", "6H563@04-06", bk="OW_6H563"),
            T("out", "FR5652@04-06", bk="OW_FR5652"),
            T("ret", "FR9589@04-08", bk="OW_FR9589"),
            T("ret", "W43311@04-09", bk="OW_W43311"),
        ],
        dict(
            included="Israir: 1 free carry-on (Google Flights). "
            + FR_BAGS
            + " Wizz Basic: under-seat item only.",
            trolley_nis="Ryanair 45-129 per passenger per flight (x2 flights); Wizz: charged, amount not shown by Google - not verified; Israir 0",
            checked_nis="Ryanair 77-215 per passenger per flight; Israir and Wizz: fee, amount not shown",
        ),
        [
            "Four separate tickets on three airlines. 348 pp cheaper than DUB-01 before bags; adding a cabin trolley on the two Ryanair flights (90-258 pp) plus Wizz erases most of the saving.",
            "Outbound: 2h50 between landing at ATH and the Ryanair departure - you enter Greece (Schengen), collect any bags and re-check. Return: 6h55 overnight in Cluj airport (22:45 -> 05:40).",
            "Kayak sold the same pattern as a 'self-transfer hack' (Aegean 05:00 + Ryanair via ATH out; Ryanair + Wizz via CLJ back) at $423 pp / $1,268 total = 1,373 pp, and this exact Israir 07:45 + Ryanair outbound with the Cluj return at $434 pp = 1,409 pp. Kayak's totals are higher than the sum of the airline-direct prices in the ticket table.",
        ],
        "Cheaper than every single-ticket option, at the cost of four unprotected flights.",
        "Self-transfer: separate tickets, no rebooking or compensation if one leg is late, bags re-checked at each stop. The return lands Friday 08:35 (rule OK, 3h25 margin) on the only nonstop Cluj-TLV flight Google lists for that day: if FR9589 or W43311 is cancelled or badly delayed there is no way home before Shabbat. Greece and Romania are Schengen entries (check ETIAS status before travel).",
        "verified (each leg and price seen on Google Flights for 3 adults; the combination is self-built)",
        "four separate one-way tickets",
    ),
    custom(
        "DUB-11",
        "London stopover: nonstop TLV-London Mon 5 Apr, a day in London, Ryanair to Dublin Tue night; home via Gatwick Thu 8 Apr",
        ["fun deviation", "self-transfer", "DEVIATION"],
        [
            T("out", "6H115@04-05", bk="OW_6H115"),
            T("out", "FR117@04-06", bk="OW_FR117", note="next day"),
            T("ret", "FR306@04-08", bk="OW_FR306"),
            T("ret", "W95621@04-08", bk="OW_W95621"),
        ],
        dict(
            included="Israir: 1 free carry-on (Google Flights). "
            + FR_BAGS
            + " Wizz Basic: under-seat item only.",
            trolley_nis="Ryanair 54-155 (LGW-DUB) and 45-129 (DUB-LGW) per passenger; Wizz: charged, amount not shown by Google - not verified; Israir 0",
            checked_nis="Ryanair 77-258 per passenger per flight; Israir and Wizz: fee, amount not shown",
        ),
        [
            "Only nonstop flights (5h25, 1h25, 1h30, 5h00). Monday evening and all of Tuesday in London, Wednesday in Dublin, home Thursday 20:50 - no Friday exposure at all.",
            "Needs one hotel night in London (Mon) and a transfer from Luton to central London and on to Gatwick. Cheaper Tuesday alternative from Luton itself: FR331 LTN 19:00 -> DUB 20:20 at 349 for 3 (search-list price).",
            "Thursday: FR306 lands Gatwick 09:20, Wizz leaves 13:50 from the same airport - 4h30 self-transfer through UK border control.",
        ],
        "Costs about 220 pp more than DUB-01 (before the UK ETA) but replaces two connections with a day in London.",
        "Self-transfer: four separate tickets, no protection if a leg is late, bags re-checked. Israeli passports need a UK ETA to enter the UK (gov.uk: GBP 20 each; the checker returns 'ETA or Standard Visitor visa' for Israel). Ireland is outside Schengen and has its own passport control; the UK ETA does not cover it and Ireland is visa-free for Israelis.",
        "verified (each leg and price seen on Google Flights for 3 adults; the combination is self-built)",
        "four separate one-way tickets",
        extra_pp=dict(label="UK ETA", gbp=20),
    ),
    custom(
        "DUB-12",
        "Athens day: Aegean TLV 05:00, 13h30 in Athens, on to Dublin Mon 5 Apr night; Lufthansa back Thu 8 Apr",
        ["fun deviation", "DEVIATION", "2 nights before"],
        [
            T(
                "out",
                "A3929@04-05 A3630@04-05",
                bk="OW_A3_0405_athensday",
                row_file="ow_TLV_DUB_04-05_any",
            ),
            T("ret", "LH979@04-08 LH690@04-08", bk="OW_LH_ret_0408"),
        ],
        dict(
            included="Aegean: 1 free carry-on (Google Flights). Lufthansa: personal item + 8 kg cabin bag.",
            trolley_nis="0 (carry-on included on both tickets)",
            checked_nis="Aegean: fee, amount not shown; Lufthansa 0-251 per passenger",
        ),
        [
            "One Aegean ticket covers both outbound flights, so the long Athens layover is a protected connection: land 07:10, metro to the Acropolis/Plaka, back for the 20:40 to Dublin (arrives 23:05).",
            "PRICE DISCREPANCY: the search list showed this outbound at 2,586 for 3; its booking page offered only the agency Gotogate at 2,367 (no airline-direct option). The lower figure is used below; treat the outbound price as 2,367-2,586.",
        ],
        "A free day in Athens on the way, on a single protected ticket, for about 290 pp more than DUB-01.",
        "Two separate one-way tickets (out and back are independent). Greece is a Schengen entry (check ETIAS status before travel). Very early 05:00 start.",
        "verified with discrepancy (outbound price differs between search list and booking page; not offered airline-direct)",
        "two one-way tickets",
    ),
]

EXT = RT(
    "DUB-13",
    "EXTENDED WEEKEND: Lufthansa Tue 6 Apr -> Sun 11 Apr",
    ["extended weekend", "DEVIATION"],
    "LH687@04-06 LH982@04-06",
    "LH977@04-11 LH694@04-11",
    4681,
    None,
    LH_BAGS,
    deviation="Extended weekend: stays in Dublin through Shabbat (Fri 9 - Sat 10 Apr) and flies Sunday. Three extra hotel nights. Flight price equals DUB-01; the cheapest Sunday return (LH983 05:55 + LH694, lands 19:10) drops the round trip to 4,085 = 1,362 pp.",
    notes=[
        "Saturday-night departure is not possible: the last Dublin departures on Sat 10 Apr are 18:35 (LX405), 18:45/20:15 (BA) and 20:35 (EY48), all before nightfall in Dublin (sunset there is roughly 20:10 local in mid-April - approximate, not verified).",
        "Other Sunday returns on the same ticket: LH983+LH686 05:55 -> 15:25 (4,378), LH2517+LH682 10:40 -> Mon 00:35 (4,604), LH979+LH690 12:40 -> 23:15 (5,569).",
    ],
    verification="verified on the Google Flights search list (3 adults); booking page not opened",
)


# ---- rendering ---------------------------------------------------------------
def render_rt(it):
    out, ret = segs(it["out"]), segs(it["ret"])
    pp = round(it["total"] / 3)
    L = [f"## {it['id']} - {it['title']}", ""]
    L.append(f"- **Tags:** {', '.join(it['tags'])}")
    L.append(f"- **Ticket type:** {it['kind']}")
    if it.get("deviation"):
        L.append(f"- **Deviation:** {it['deviation']}")
    if it.get("risk"):
        L.append(f"- **Risk flag:** {it['risk']}")
    L += [
        "",
        f"**Outbound** - total {hm(elapsed(out))}",
        "",
        leg_table(out),
        "",
        f"**Return** - total {hm(elapsed(ret))}",
        "",
        leg_table(ret),
        "",
    ]
    L.append(
        f"- **Price (3 adults, shown in ILS):** NIS {it['total']:,} total = **NIS {pp:,} per person**"
    )
    rec = dict(
        id=it["id"],
        title=it["title"],
        tags=it["tags"],
        ticket_type=it["kind"],
        outbound=out,
        inbound=ret,
        outbound_elapsed_min=elapsed(out),
        inbound_elapsed_min=elapsed(ret),
        price_total_nis=it["total"],
        price_pp_nis=pp,
        friday_rule=friday_status(ret),
        verification=it["verification"],
        bags=it["bags"],
        deviation=it.get("deviation"),
        risk=it.get("risk"),
        notes=it["notes"],
    )
    if it["bk"]:
        b = booking_obs(it["bk"])
        assert abs(b["price"] - it["total"]) <= 2, (it["id"], b["price"], it["total"])
        sellers = "; ".join(f"{s['seller']} {s['ils']} ({s['native']})" for s in b["sellers"])
        L.append(f"- **Sellers on the Google booking page:** {sellers}")
        L.append(
            f"- **Observed:** {b['observed']} (Google Flights booking page, 3 adults, curr=ILS)"
        )
        L.append(f"- **Google Flights deep link (these exact flights):** {b['url']}")
        rec.update(observed=b["observed"], google_booking_url=b["url"], sellers=b["sellers"])
    else:
        f, o, u, r = find_row(it["ret"], "rt_TLV-DUB_04-06_04-11")
        assert r["price_total"] == it["total"]
        L.append(
            f"- **Observed:** {o} (Google Flights return list after selecting the outbound, 3 adults, curr=ILS)"
        )
        L.append(f"- **Google Flights deep link (outbound selected, return list):** {u}")
        L.append(
            f"- **Google Flights booking link (not opened):** {gf_booking([out, ret], 'round-trip')}"
        )
        rec.update(observed=o, google_search_url=u)
    d1, d2 = out[0]["dep"][:10], ret[0]["dep"][:10]
    L.append(f"- **Google Flights date search:** {gf_search('TLV', 'DUB', d1, d2)}")
    carriers = sorted({s["fn"][:2] for s in out + ret})
    L.append(
        "- **Airline site (home page only - no deep link was tested):** "
        + ", ".join(AIRLINE_SITE[c] for c in carriers)
    )
    L.append(f"- **Fare includes:** {it['bags']['included']}")
    L.append(f"- **Cabin trolley add-on (NIS):** {it['bags']['trolley_nis']}")
    L.append(f"- **Checked bag (NIS):** {it['bags']['checked_nis']}")
    if it.get("kayak"):
        k = it["kayak"]
        conv = round(k["usd_pp"] * USD_ILS)
        L.append(
            f"- **Cross-check (Kayak, 3 adults):** ${k['usd_pp']} pp / ${k['usd_total']:,} total = NIS {conv:,} pp at 1 USD = {USD_ILS} ILS -> Google is {pp - conv:+,} pp ({(pp - conv) / conv:+.1%}). File: `data/crosscheck/{k['file']}`"
        )
        rec["crosscheck"] = dict(
            source="Kayak",
            usd_pp=k["usd_pp"],
            usd_total=k["usd_total"],
            nis_pp_converted=conv,
            rate=USD_ILS,
        )
    else:
        L.append("- **Cross-check:** none (single source)")
    L.append(f"- **Friday rule:** {friday_status(ret)}" + (f" (lands TLV {when(ret[-1]['arr'])})"))
    L.append(f"- **Verification:** {it['verification']}")
    for n in it["notes"]:
        L.append(f"- Note: {n}")
    L.append("")
    return "\n".join(L), rec


def render_custom(it):
    L = [
        f"## {it['id']} - {it['title']}",
        "",
        f"- **Tags:** {', '.join(it['tags'])}",
        f"- **Ticket type:** {it['kind']}",
    ]
    if it["deviation"]:
        L.append(f"- **Deviation:** {it['deviation']}")
    if it["risk"]:
        L.append(f"- **Risk flag:** {it['risk']}")
    total, tickets_rec, all_out, all_ret = 0, [], [], []
    price_lines = []
    for t in it["tickets"]:
        ss = segs(t["spec"])
        (all_out if t["direction"] == "out" else all_ret).extend(ss)
        b = booking_obs(t["bk"])
        total += b["price"]
        sellers = "; ".join(f"{s['seller']} {s['ils']} ({s['native']})" for s in b["sellers"])
        price_lines.append(
            f"| {' + '.join(s['fn'] for s in ss)} | {ss[0]['frm']} -> {ss[-1]['to']} | {b['price']:,} | {round(b['price'] / 3):,} | {sellers} | {b['observed']} | {b['url']} |"
        )
        tickets_rec.append(
            dict(
                direction=t["direction"],
                segments=ss,
                price_total_nis=b["price"],
                price_pp_nis=round(b["price"] / 3),
                sellers=b["sellers"],
                observed=b["observed"],
                google_booking_url=b["url"],
            )
        )
    L += [
        "",
        f"**Outbound** - total {hm(elapsed(all_out))} from first departure to last arrival",
        "",
        leg_table(all_out),
        "",
        f"**Return** - total {hm(elapsed(all_ret))} from first departure to last arrival",
        "",
        leg_table(all_ret),
        "",
    ]
    L += (
        [
            "| Ticket | Route | NIS total (3 adults) | NIS pp | Sellers on Google booking page | Observed | Google Flights deep link |",
            "|---|---|---|---|---|---|---|",
        ]
        + price_lines
        + [""]
    )
    pp = round(total / 3)
    L.append(
        f"- **Price (3 adults, shown in ILS, sum of the tickets above):** NIS {total:,} total = **NIS {pp:,} per person**"
    )
    extra = None
    if it.get("extra_pp"):
        e = it["extra_pp"]
        nis = round(e["gbp"] * GBP_ILS)
        extra = dict(label=e["label"], gbp=e["gbp"], nis_pp=nis, rate=GBP_ILS)
        L.append(
            f"- **Mandatory extra:** {e['label']} GBP {e['gbp']} = NIS {nis} pp at 1 GBP = {GBP_ILS} ILS (Frankfurter/ECB, 17 Nov 2026) -> **NIS {pp + nis:,} pp / NIS {total + 3 * nis:,} total including it**"
        )
    carriers = sorted({s["fn"][:2] for s in all_out + all_ret})
    L.append(
        "- **Airline sites (home pages only - no deep link was tested):** "
        + ", ".join(AIRLINE_SITE[c] for c in carriers)
    )
    L.append(f"- **Fare includes:** {it['bags']['included']}")
    L.append(f"- **Cabin trolley add-on (NIS):** {it['bags']['trolley_nis']}")
    L.append(f"- **Checked bag (NIS):** {it['bags']['checked_nis']}")
    L.append(
        "- **Cross-check:** see notes"
        if any("Kayak" in n for n in it["notes"])
        else "- **Cross-check:** none (single source)"
    )
    L.append(f"- **Friday rule:** {friday_status(all_ret)} (lands TLV {when(all_ret[-1]['arr'])})")
    L.append(f"- **Verification:** {it['verification']}")
    for n in it["notes"]:
        L.append(f"- Note: {n}")
    L.append("")
    rec = dict(
        id=it["id"],
        title=it["title"],
        tags=it["tags"],
        ticket_type=it["kind"],
        outbound=all_out,
        inbound=all_ret,
        outbound_elapsed_min=elapsed(all_out),
        inbound_elapsed_min=elapsed(all_ret),
        tickets=tickets_rec,
        price_total_nis=total,
        price_pp_nis=pp,
        mandatory_extra=extra,
        friday_rule=friday_status(all_ret),
        verification=it["verification"],
        bags=it["bags"],
        deviation=it["deviation"],
        risk=it["risk"],
        notes=it["notes"],
    )
    return "\n".join(L), rec


sections, recs = [], []
for it in ITINS:
    s, r = render_rt(it)
    sections.append(s)
    recs.append(r)
for it in CUSTOM:
    s, r = render_custom(it)
    sections.append(s)
    recs.append(r)
s, r = render_rt(EXT)
sections.append(s)
recs.append(r)

json.dump(
    dict(
        generated=dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        passengers=3,
        currency="ILS",
        fx=dict(
            USD_ILS=USD_ILS,
            GBP_ILS=GBP_ILS,
            source="https://api.frankfurter.dev/v1/latest?base=USD&symbols=ILS,EUR,GBP",
            date="2026-11-17",
        ),
        itineraries=recs,
    ),
    open(os.path.join(HERE, "..", "data", "itineraries.json"), "w"),
    ensure_ascii=False,
    indent=1,
)

head = open(os.path.join(HERE, "flights_head.md")).read()
tail = open(os.path.join(HERE, "flights_tail.md")).read()
by = {r["id"]: r for r in recs}


def fill(m):
    r = by[m.group(1)]
    return {"pp": f"{r['price_pp_nis']:,}", "total": f"{r['price_total_nis']:,}"}[m.group(2)]


head = re.sub(r"\{(DUB-\d\d)\.(pp|total)\}", fill, head)
tail = re.sub(r"\{(DUB-\d\d)\.(pp|total)\}", fill, tail)
open(os.path.join(HERE, "..", "flights.md"), "w").write(
    head + "\n" + "\n".join(sections) + "\n" + tail
)
for r in recs:
    print(
        r["id"],
        r["price_total_nis"],
        r["price_pp_nis"],
        r["friday_rule"],
        hm(r["outbound_elapsed_min"]),
        hm(r["inbound_elapsed_min"]),
    )
