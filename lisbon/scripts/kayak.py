"""Load a Kayak results URL in headless system Chrome, expand every result card, save visible text.

Usage: kayak.py NAME URL [WAIT_SECONDS]
"""

import datetime
import pathlib
import sys
import time

from playwright.sync_api import sync_playwright

name, url = sys.argv[1], sys.argv[2]
wait = float(sys.argv[3]) if len(sys.argv) > 3 else 25
out = pathlib.Path(__file__).parent / "web"
with sync_playwright() as p:
    b = p.chromium.launch(
        channel="chrome", headless=True, args=["--disable-blink-features=AutomationControlled"]
    )
    ctx = b.new_context(
        locale="en-US",
        viewport={"width": 1400, "height": 2600},
        user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36",
    )
    pg = ctx.new_page()
    pg.add_init_script("Object.defineProperty(navigator,'webdriver',{get:()=>undefined})")
    pg.goto(url, wait_until="domcontentloaded", timeout=60000)
    time.sleep(wait)
    n = 0
    for sel in ["div[class*='nrc6-main']", "div[data-resultid] div[class*='main']"]:
        cards = pg.query_selector_all(sel)
        if cards:
            for c in cards:
                try:
                    c.click(timeout=3000, position={"x": 200, "y": 30})
                    n += 1
                    time.sleep(1.2)
                except Exception as e:
                    pass
            break
    time.sleep(3)
    txt = pg.inner_text("body")
    (out / f"{name}.txt").write_text(
        f"URL: {pg.url}\nFETCHED: {datetime.datetime.now():%Y-%m-%d %H:%M}\n" + txt
    )
    print(pg.url, "| expanded", n, "| chars", len(txt))
    b.close()
