"""Load a URL in system Chrome (fresh temporary profile) and dump visible text + screenshot.

Usage: browse.py NAME URL [wait_seconds] [--headed]
Writes pages/NAME.txt and pages/NAME.png.
"""

import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).parent
OUT = HERE / "pages"
OUT.mkdir(exist_ok=True)


def main():
    name, url = sys.argv[1:3]
    wait = int(sys.argv[3]) if len(sys.argv) > 3 and sys.argv[3].isdigit() else 20
    headed = "--headed" in sys.argv
    with sync_playwright() as p:
        b = p.chromium.launch(
            channel="chrome",
            headless=not headed,
            args=["--disable-blink-features=AutomationControlled"],
        )
        ctx = b.new_context(
            locale="en-IL",
            timezone_id="Asia/Jerusalem",
            viewport={"width": 1400, "height": 2200},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36",
        )
        page = ctx.new_page()
        page.add_init_script("Object.defineProperty(navigator,'webdriver',{get:()=>undefined})")
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=60000)
        except Exception as e:
            print("goto error:", e)
        time.sleep(wait)
        try:
            text = page.inner_text("body")
        except Exception as e:
            text = f"ERR {e}"
        (OUT / f"{name}.txt").write_text(f"URL: {page.url}\nTITLE: {page.title()}\n\n{text}")
        page.screenshot(path=str(OUT / f"{name}.png"), full_page=False)
        print(page.url, "|", page.title(), "| chars:", len(text))
        b.close()


if __name__ == "__main__":
    main()
