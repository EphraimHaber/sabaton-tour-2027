"""Load any URL in headless Chrome and print/save the visible text (used for second-source checks)."""

import sys
import time

from playwright.sync_api import sync_playwright

url, out, wait = sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 20
with sync_playwright() as p:
    b = p.chromium.launch(
        channel="chrome", headless=True, args=["--disable-blink-features=AutomationControlled"]
    )
    ctx = b.new_context(
        locale="en-US",
        viewport={"width": 1400, "height": 2400},
        user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36",
    )
    page = ctx.new_page()
    page.goto(url, wait_until="domcontentloaded", timeout=60000)
    page.wait_for_timeout(wait * 1000)
    text = page.inner_text("body")
    open(out, "w").write(page.url + "\n" + time.strftime("%Y-%m-%dT%H:%M:%S%z") + "\n" + text)
    page.screenshot(path=out + ".png")
    print(page.url[:150])
    print(text[:3000])
    b.close()
