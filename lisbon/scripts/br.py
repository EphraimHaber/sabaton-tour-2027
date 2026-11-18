"""Open a URL in headless system Chrome, wait, save visible text to ./web/<name>.txt.

Usage: br.py NAME URL [WAIT_SECONDS]
"""

import pathlib
import sys
import time

from playwright.sync_api import sync_playwright

name, url = sys.argv[1], sys.argv[2]
wait = float(sys.argv[3]) if len(sys.argv) > 3 else 20
out = pathlib.Path(__file__).parent / "web"
with sync_playwright() as p:
    b = p.chromium.launch(
        channel="chrome", headless=True, args=["--disable-blink-features=AutomationControlled"]
    )
    ctx = b.new_context(
        locale="en-US",
        viewport={"width": 1400, "height": 2200},
        user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36",
    )
    pg = ctx.new_page()
    pg.add_init_script("Object.defineProperty(navigator,'webdriver',{get:()=>undefined})")
    try:
        pg.goto(url, wait_until="domcontentloaded", timeout=60000)
    except Exception as e:
        print("goto err", e)
    time.sleep(wait)
    txt = pg.inner_text("body")
    (out / f"{name}.txt").write_text(txt)
    pg.screenshot(path=str(out / f"{name}.png"))
    print(pg.url)
    print(pg.title())
    print(len(txt))
    b.close()
