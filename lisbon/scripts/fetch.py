"""Fetch a URL with a browser-like TLS fingerprint; save body under ./web/ and print status + size."""

import hashlib
import pathlib
import sys

from primp import Client

c = Client(
    impersonate="chrome_145",
    impersonate_os="macos",
    cookie_store=True,
    follow_redirects=True,
    timeout=40,
)
for u in sys.argv[1:]:
    try:
        r = c.get(u)
        name = hashlib.md5(u.encode()).hexdigest()[:10]
        p = pathlib.Path(__file__).parent / "web" / (name + ".html")
        p.write_text(r.text)
        print(r.status_code, len(r.text), p.name, u)
    except Exception as e:
        print("ERR", e, u)
