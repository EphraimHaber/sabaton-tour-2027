"""Scrape il.kayak.com result lists (ILS, 3 adults) as a second price source.

Usage: kayak.py SPEC [SPEC...]   where SPEC = FROM-TO/OUT[/BACK][?nonstop]
Example: kayak.py TLV-MXP/2027-04-18/2027-04-20?nonstop MXP-TLV/2027-04-20
Writes pages/kayak_<spec>.txt and prints parsed result rows.
"""

import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).parent
OUT = HERE / "pages"
OUT.mkdir(exist_ok=True)


def parse(text):
    rows = []
    for block in text.split("Go to result details")[1:]:
        block = block.split("Select")[0]
        lines = [l.strip() for l in block.splitlines() if l.strip()]
        legs = [l for l in lines if re.match(r"\d{2}:\d{2} – \d{2}:\d{2}", l)]
        price = next((l for l in lines if l.startswith("₪") and "total" not in l), None)
        total = next((l for l in lines if "total" in l), None)
        stops = [l for l in lines if l == "nonstop" or re.match(r"\d stops?", l)]
        durs = [l for l in lines if re.match(r"\d+h \d+m$", l)]
        airports = [l for l in lines if re.match(r"[A-Z]{3}.* - $|^[A-Z]{3}[A-Z][a-z]", l)]
        idx_last_dur = max(
            (i for i, l in enumerate(lines) if re.match(r"\d+h \d+m$", l)), default=0
        )
        airline = next(
            (
                l
                for l in lines[idx_last_dur + 1 :]
                if not l.startswith("₪") and l not in ("0", "1", "2")
            ),
            "",
        )
        rows.append((price, total, airline, list(zip(legs, stops, durs)), airports))
    return rows


def main():
    with sync_playwright() as p:
        b = p.chromium.launch(
            channel="chrome", headless=True, args=["--disable-blink-features=AutomationControlled"]
        )
        ctx = b.new_context(
            locale="en-IL",
            timezone_id="Asia/Jerusalem",
            viewport={"width": 1400, "height": 2200},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36",
        )
        page = ctx.new_page()
        page.add_init_script("Object.defineProperty(navigator,'webdriver',{get:()=>undefined})")
        for spec in sys.argv[1:]:
            nonstop = spec.endswith("?nonstop")
            path = spec.replace("?nonstop", "")
            url = f"https://www.il.kayak.com/flights/{path}/3adults?sort=price_a" + (
                "&fs=stops=0" if nonstop else ""
            )
            try:
                page.goto(url, wait_until="domcontentloaded", timeout=60000)
            except Exception as e:
                print("goto error", e)
            time.sleep(28)
            text = page.inner_text("body")
            now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
            name = "kayak_" + re.sub(r"[^A-Za-z0-9]+", "_", spec)
            (OUT / f"{name}.txt").write_text(f"URL: {url}\nOBSERVED: {now}\n\n{text}")
            print(f"# {spec} observed {now}\n# {url}")
            if "₪" not in text:
                print("  !! no prices; first 200 chars:", text[:200].replace("\n", " "))
            for price, total, airline, legs, airports in parse(text):
                print(
                    f"  {price} pp | {total} | {airline} | "
                    + " || ".join(" ".join(x) for x in legs)
                    + " | "
                    + " ".join(airports)
                )
        b.close()


if __name__ == "__main__":
    main()
