"""Summarise a saved Kayak results text dump: one line per result card."""

import pathlib
import re
import sys

for fn in sys.argv[1:]:
    t = [l.strip() for l in pathlib.Path(fn).read_text().splitlines() if l.strip()]
    print("==", fn, "|", t[0], "|", t[1])
    i = 0
    while i < len(t):
        if re.match(r"^\d\d:\d\d – \d\d:\d\d(\+\d)?$", t[i]):
            j = i + 1
            blk = [t[i]]
            while j < len(t) and not t[j].startswith("Go to result details") and j - i < 80:
                blk.append(t[j])
                j += 1
            s = " ~ ".join(blk)
            price = re.search(r"(₪[\d,]+) ~ / person ~ (₪[\d,]+ total)", s)
            fl = re.findall(
                r"((?:Aegean Airlines|Wizz Air|TAP AIR PORTUGAL|EL AL|Arkia|ISRAIR|Sky Express|Lufthansa|Iberia|Iberia Express|Air Europa|SWISS|Smartwings|LOT|ITA Airways|Air France|KLM|Austrian Airlines|Bluebird Airways|TUS Airways|FlyOne|Vueling|Bulgaria Air|Air Serbia|TAROM|Cyprus Airways|Brussels Airlines) \d+(?: · Operated by [^~]+)?) ~ [^~]* ~ (\d\d:\d\d) ~ ([^~]+) ~ [^~]+ ~ (?:Overnight flight ~ )?(\d\d:\d\d)",
                s,
            )
            head = " | ".join(blk[:12])
            fare = re.search(r"total ~ ([^~]+) ~ Depart", s)
            print(
                "-",
                blk[0],
                "|",
                price.group(1) + " pp, " + price.group(2) if price else "?",
                "|",
                fare.group(1) if fare else "",
                "|",
                "; ".join(f"{a.strip()} {b}->{d}" for a, b, c, d in fl) or head,
            )
            i = j
        else:
            i += 1
