"""Print one line per result card from a saved Kayak page text (see page_text.py)."""

import re
import sys

t = open(sys.argv[1]).read()
print(t.split("\n")[0], t.split("\n")[1])
parts = t.split("/ person")
for i, p in enumerate(parts[:-1][: int(sys.argv[2]) if len(sys.argv) > 2 else 14]):
    lines = [l.strip() for l in p.split("\n") if l.strip()]
    card = [
        l
        for l in lines[-34:]
        if re.search(r"\d:\d\d [ap]m|layover|^\$\d+$", l)
        or re.fullmatch(
            r"[A-Za-z ,]+(Air|Airlines|Lufthansa|KLM|France|Ryanair|AL|ISRAIR|Airways|SWISS|Lingus|Express)[A-Za-z ,]*",
            l,
        )
    ]
    nxt = [x.strip() for x in parts[i + 1].split("\n")[1:3]]
    print(" | ".join(card), "|", " ".join(nxt))
