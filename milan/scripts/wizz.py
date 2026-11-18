"""Query the Wizz Air public search API for exact fares (3 adults)."""

import json
import re
import sys

from primp import Client

c = Client(impersonate="chrome_145", impersonate_os="macos", cookie_store=True)
r = c.get("https://wizzair.com/buildnumber")
print("buildnumber:", r.status_code, r.text[:200])
m = re.search(r"https://be\.wizzair\.com/[\d.]+", r.text)
if not m:
    sys.exit(1)
api = m[0] + "/Api"
c.get("https://wizzair.com/en-gb")
for frm, to, date in [a.split(",") for a in sys.argv[1:]]:
    body = {
        "isFlightChange": False,
        "flightList": [{"departureStation": frm, "arrivalStation": to, "departureDate": date}],
        "adultCount": 3,
        "childCount": 0,
        "infantCount": 0,
        "wdc": False,
    }
    r = c.post(
        api + "/search/search",
        json=body,
        headers={"origin": "https://wizzair.com", "referer": "https://wizzair.com/"},
    )
    print(frm, to, date, r.status_code)
    print(r.text[:6000])
