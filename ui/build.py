"""Build the shareable trip page from the per-city research markdown.

Reads <city>/flights.md, sightseeing.md, sources.md, sightseeing-sources.md,
fact-check.md and dublin/data/itineraries.json, converts them to HTML
fragments plus a little structured metadata, and injects the result into
template.html. Read-only with respect to the research files.

Usage:
  python3 ui/build.py              fragment for publishing as a Claude artifact
  python3 ui/build.py --site DIR   standalone DIR/index.html (GitHub Pages)
"""

import argparse
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
UI = Path(__file__).resolve().parent
CITIES = [("dublin", "DUB"), ("lisbon", "LIS"), ("milan", "MIL")]
ID_RE = r"(?:DUB|LIS|MIL)-\d\d"

# ---------------------------------------------------------------- inline md

TOKEN_RE = re.compile(
    r"`([^`]+)`"
    r"|\[([^\]]+)\]\((https?://[^\s)]+)\)"
    r"|(https?://[^\s<>|`]+)"
)
STATUS_WORDS = {
    "verified": "ok", "verified-sum": "ok", "confirmed": "ok",
    "kayak-only": "warn", "schedule-only": "warn", "partly-confirmed": "warn",
    "secondary": "warn", "unverified": "bad", "not-confirmed": "bad",
}


def link_label(url):
    host = re.sub(r"^https?://(www\.)?", "", url).split("/")[0]
    return host


def inline(text):
    tokens = []

    def stash(m):
        if m.group(1) is not None:
            code = m.group(1)
            tone = STATUS_WORDS.get(code.strip().lower())
            cls = f' class="st st-{tone}"' if tone else ""
            out = f"<code{cls}>{html.escape(code)}</code>"
            tail = ""
        elif m.group(3) is not None:
            out = (f'<a href="{html.escape(m.group(3))}" target="_blank" rel="noopener">'
                   f"{html.escape(m.group(2))}</a>")
            tail = ""
        else:
            url = m.group(4)
            tail = ""
            while url and (url[-1] in ".,;:!?*" or (url[-1] == ")" and url.count("(") < url.count(")"))):
                tail = url[-1] + tail
                url = url[:-1]
            out = (f'<a class="bare" href="{html.escape(url)}" target="_blank" rel="noopener">'
                   f"{html.escape(link_label(url))}</a>")
        tokens.append(out)
        return f"\x00{len(tokens) - 1}\x00{tail}"

    s = TOKEN_RE.sub(stash, text)
    s = html.escape(s, quote=False)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![\w*])\*([^*\s][^*]*?)\*(?![\w*])", r"<em>\1</em>", s)
    s = re.sub(r"price not confirmed", '<mark class="unconf">price not confirmed</mark>', s, flags=re.I)
    s = re.sub(r"\x00(\d+)\x00", lambda m: tokens[int(m.group(1))], s)
    return s


def plain(text):
    s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    return re.sub(r"[*`]", "", s).strip()


# ----------------------------------------------------------------- block md

LIST_RE = re.compile(r"^(\s*)([-*]|\d+\.)\s+(.*)$")
KV_BOLD = re.compile(r"^\*\*([^*]{1,70}?):\*\*\s*(.*)$", re.S)
KV_PLAIN = re.compile(r"^([A-Za-z][A-Za-z0-9_ \-()/.+]{0,45}):(?:\s+(.*))?$", re.S)
ACRONYMS = {"nis": "NIS", "url": "URL", "pp": "pp", "id": "ID"}


def humanize(key):
    if "_" in key or key.islower():
        words = key.replace("_", " ").split()
        words = [ACRONYMS.get(w, w) for w in words]
        key = " ".join(words)
        key = key[0].upper() + key[1:]
    return key


def kv_split(text):
    m = KV_BOLD.match(text)
    if m:
        return m.group(1).strip(), m.group(2) or ""
    m = KV_PLAIN.match(text)
    if m and "http" not in m.group(1):
        return m.group(1).strip(), m.group(2) or ""
    return None


def split_row(line):
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    return [c.strip().replace("\\|", "|") for c in re.split(r"(?<!\\)\|", line)]


def render_table(rows):
    head, body = rows[0], rows[2:] if len(rows) > 1 and re.match(r"^[\s|:\-]+$", rows[1]) else rows[1:]
    heads = split_row(head)
    labels = [html.escape(plain(c), quote=True) for c in heads]
    out = ['<div class="tw"><table><thead><tr>']
    out += [f"<th>{inline(c)}</th>" for c in heads]
    out.append("</tr></thead><tbody>")
    for r in body:
        # data-l carries the column name so narrow screens can stack each row as labelled lines.
        # The inner span keeps mixed text and links together as one grid item when stacked.
        cells = [f'<td data-l="{labels[n] if n < len(labels) else ""}"{"" if c else ' class="e"'}>'
                 f"<span>{inline(c)}</span></td>" for n, c in enumerate(split_row(r))]
        out.append("<tr>" + "".join(cells) + "</tr>")
    out.append("</tbody></table></div>")
    return "".join(out)


def parse_list(lines):
    """lines: list of raw list lines (with continuations). Returns nested items."""
    items = []  # each: [indent, ordered, text, children]
    stack = []
    for ln in lines:
        m = LIST_RE.match(ln)
        if not m:
            if stack:
                stack[-1][2] += " " + ln.strip()
            continue
        indent = len(m.group(1).replace("\t", "  "))
        node = [indent, m.group(2)[0].isdigit(), m.group(3), []]
        while stack and stack[-1][0] >= indent:
            stack.pop()
        (stack[-1][3] if stack else items).append(node)
        stack.append(node)
    return items


def render_list(items, top=True):
    if not items:
        return ""
    if top:
        kvs = [kv_split(it[2]) for it in items]
        if len(items) >= 2 and all(kvs):
            out = ['<dl class="kv">']
            for (k, v), it in zip(kvs, items):
                cls = ' class="shb"' if k.lower() == "shabbat" else ""
                out.append(f"<dt{cls}>{html.escape(humanize(k))}</dt>"
                           f"<dd{cls}>{inline(v)}{render_list(it[3], False)}</dd>")
            out.append("</dl>")
            return "".join(out)
    tag = "ol" if items[0][1] else "ul"
    out = [f"<{tag}>"]
    for it in items:
        out.append(f"<li>{inline(it[2])}{render_list(it[3], False)}</li>")
    out.append(f"</{tag}>")
    return "".join(out)


def md(text, base_level=4):
    lines = text.split("\n")
    out, para, i = [], [], 0

    def flush():
        if para:
            out.append("<p>" + inline(" ".join(p.strip() for p in para)) + "</p>")
            para.clear()

    while i < len(lines):
        ln = lines[i]
        st = ln.strip()
        if not st:
            flush()
            i += 1
        elif st.startswith("```"):
            flush()
            j = i + 1
            while j < len(lines) and not lines[j].strip().startswith("```"):
                j += 1
            out.append("<pre>" + html.escape("\n".join(lines[i + 1:j])) + "</pre>")
            i = j + 1
        elif re.match(r"^-{3,}$", st):
            flush()
            i += 1
        elif st.startswith("#"):
            flush()
            m = re.match(r"^(#+)\s*(.*)$", st)
            lvl = min(6, base_level + max(0, len(m.group(1)) - 3))
            out.append(f"<h{lvl}>{inline(m.group(2))}</h{lvl}>")
            i += 1
        elif st.startswith("|"):
            flush()
            j = i
            while j < len(lines) and lines[j].strip().startswith("|"):
                j += 1
            out.append(render_table(lines[i:j]))
            i = j
        elif LIST_RE.match(ln):
            flush()
            j = i
            while j < len(lines):
                s2 = lines[j]
                if LIST_RE.match(s2):
                    j += 1
                elif s2.strip() and s2.startswith((" ", "\t")) and not s2.strip().startswith("|"):
                    j += 1
                elif not s2.strip() and j + 1 < len(lines) and LIST_RE.match(lines[j + 1]):
                    j += 1
                else:
                    break
            out.append(render_list(parse_list([x for x in lines[i:j] if x.strip()])))
            i = j
        else:
            para.append(ln)
            i += 1
    flush()
    return "".join(out)


def link_ids(fragment):
    """Turn itinerary IDs in text nodes into in-page jump links."""
    parts = re.split(r"(<[^>]+>)", fragment)
    depth_a = 0
    for n, p in enumerate(parts):
        if p.startswith("<"):
            if re.match(r"<a\b", p):
                depth_a += 1
            elif p.startswith("</a"):
                depth_a = max(0, depth_a - 1)
        elif not depth_a:
            parts[n] = re.sub(rf"\b({ID_RE})\b", r'<a href="#" class="idref" data-it="\1">\1</a>', p)
    return "".join(parts)


def scrub(text):
    """Drop lines that expose local machine paths."""
    return "\n".join(l for l in text.split("\n") if "/private/tmp" not in l and "/Users/" not in l)


# ------------------------------------------------------------- sectioning


def split_sections(text, level):
    """Return (preamble, [(title, body)]) splitting on headings of exactly `level`."""
    pat = re.compile(rf"^{'#' * level} (?!#)(.*)$", re.M)
    ms = list(pat.finditer(text))
    if not ms:
        return text, []
    pre = text[:ms[0].start()]
    secs = []
    for a, b in zip(ms, ms[1:] + [None]):
        secs.append((a.group(1).strip(), text[a.end():b.start() if b else len(text)].strip("\n")))
    return pre, secs


def first_table(text):
    rows = []
    for ln in text.split("\n"):
        if ln.strip().startswith("|"):
            rows.append(ln)
        elif rows:
            break
    if len(rows) < 3:
        return []
    head = [plain(c) for c in split_row(rows[0])]
    return [dict(zip(head, split_row(r))) for r in rows[2:]]


def fields(body):
    out = {}
    for ln in body.split("\n"):
        m = LIST_RE.match(ln)
        if m and not m.group(1):
            kv = kv_split(m.group(3))
            if kv and kv[0].lower() not in out:
                out[kv[0].lower()] = kv[1]
    return out


def num(s):
    m = re.search(r"\d[\d,]*", s or "")
    return int(m.group(0).replace(",", "")) if m else None


def tone_rule(s):
    low = s.lower()
    if re.search(r"fail", low) and not low.startswith("ok"):
        return "bad"
    if re.search(r"borderline|tight|no fallback|on paper|risky|only if", low):
        return "warn"
    if low.startswith("ok"):
        return "ok"
    return "na"


def short(s, limit=64):
    s = plain(s)
    cut = re.split(r"(?<=[^(])\s\(|\.\s|;\s", s, maxsplit=1)[0] if not s.startswith("(") else s
    cut = cut.rstrip(".")
    return cut if len(cut) <= limit else cut[:limit - 1].rstrip() + "…"


def verif(s):
    low = plain(s).lower()
    head = low[:90]
    if low.startswith("verified-sum"):
        return "verified-sum", "ok"
    if low.startswith("verified per leg"):
        return "verified per leg", "ok"
    if low.startswith("verified"):
        if "discrepancy" in head:
            return "verified, with a discrepancy", "warn"
        if "only" in head.split(".")[0]:
            return short(s, 40), "warn"
        return "verified", "ok"
    for w in ("kayak-only", "schedule-only"):
        if low.startswith(w):
            return w, "warn"
    if low.startswith("unverified"):
        return "unverified", "bad"
    return "partly verified, see details", "warn"


# ----------------------------------------------------------------- flights

BG_SKIP = re.compile(r"recommended picks|all itineraries at a glance|how this was collected", re.I)


def build_flights(folder, prefix):
    text = scrub((ROOT / folder / "flights.md").read_text())
    title_m = re.match(r"# (.*)", text)
    pre, secs = split_sections(text, 2)
    intro = md(re.sub(r"^# .*\n", "", pre, count=1))
    itins, background, picks_html, pick_map, pick_rule, glance = [], [], "", {}, {}, {}
    for title, body in secs:
        if re.match(ID_RE, title):
            itins.append((title, body))
            continue
        if re.search(r"recommended picks", title, re.I):
            for row in first_table(body):
                if row.get("ID"):
                    pick_map[plain(row["ID"])] = plain(row.get("Pick", ""))
                    pick_rule[plain(row["ID"])] = row.get("Friday rule", "")
            picks_html = link_ids(md(body))
        if re.search(r"at a glance", title, re.I):
            glance = {plain(r.get("ID", "")): r for r in first_table(body)}
        sub_pre, subs = split_sections(body, 3)
        keep = [sub_pre]
        for st, sb in subs:
            if re.match(ID_RE, st):
                itins.append((st, sb))
            else:
                keep.append(f"### {st}\n{sb}")
        if not BG_SKIP.search(title):
            content = "\n\n".join(k for k in keep if k.strip())
            if content.strip():
                background.append({"title": plain(title), "html": link_ids(md(content))})

    dub_json = {}
    if prefix == "DUB":
        data = json.loads((ROOT / "dublin/data/itineraries.json").read_text())
        dub_json = {i["id"]: i for i in data["itineraries"]}

    out = []
    for title, body in itins:
        m = re.match(rf"({ID_RE})\s*-\s*(.*)", title, re.S)
        iid, name = m.group(1), plain(m.group(2))
        f = fields(body)
        name_flags = ""
        it = {"id": iid, "title": name, "pick": pick_map.get(iid, ""), "allin": "", "ruleLabel": "Friday rule"}
        if prefix == "DUB":
            j, g = dub_json[iid], glance.get(iid, {})
            it["pp"] = plain(g.get("NIS pp", "")) or f"{j['price_pp_nis']:,}"
            it["total"] = plain(g.get("NIS total (3)", "")) or f"{j['price_total_nis']:,}"
            rule, ver = g.get("Friday rule") or j["friday_rule"], j["verification"]
            dev = bool(j.get("deviation")) or "DEVIATION" in name or "EXTENDED" in name
            name_flags = g.get("Summary", "")
        elif prefix == "LIS":
            price = f.get("price (g)", "")
            pp = re.search(r"₪([\d,]+) pp", price)
            tot = re.search(r"₪([\d,]+) total", price)
            if not pp:
                tabs = re.findall(r"\|[^\n]*\|\s*₪([\d,]+)\s*\|\s*₪([\d,]+)\s*\|\s*$", body, re.M)
                if tabs:
                    tot_s, pp_s = tabs[0]
                    it["pp"], it["total"] = pp_s, tot_s
                    it["note"] = "Price depends on the version chosen; see the table inside."
            else:
                it["pp"] = pp.group(1)
                it["total"] = tot.group(1) if tot else ""
            rule, ver = f.get("friday rule", ""), f.get("verification", "")
            if rule.startswith("("):
                rule = pick_rule.get(iid, rule)
            dev = "deviation" in f or "deviation" in name.lower()
        else:
            it["pp"] = plain(f.get("price_nis_pp", ""))
            it["total"] = re.sub(r"\s*\([^)]*\)", "", plain(f.get("price_nis_total_3", ""))).split(". ")[0]
            it["allin"] = plain(f.get("all_in_pp_with_trolley", ""))
            it["ruleLabel"] = "Rules"
            rule, ver = f.get("constraint_status", ""), f.get("verification", "")
            dev = "DEVIATION" in name
        it["ppNum"] = num(it.get("pp", ""))
        it["rule"] = short(rule) or "see details"
        it["ruleTone"] = tone_rule(plain(rule))
        it["ver"], it["verTone"] = verif(ver)
        it["dev"] = dev
        it["risky"] = bool(re.search(r"risky", name + " " + name_flags, re.I))
        it["html"] = link_ids(md(body)).replace(f'data-it="{iid}"', f'data-it="{iid}" data-self="1"')
        out.append(it)
    return {
        "heading": plain(title_m.group(1)) if title_m else "",
        "intro": link_ids(intro), "picks": picks_html, "itineraries": out, "background": background,
    }


# ------------------------------------------------------------- sightseeing

SHB_TITLE = re.compile(r"kosher|shabbat", re.I)
SHB_ID = re.compile(r"^(SHB|SAT|KOS)-")
SIGHT_SKIP = re.compile(r"^entry format$", re.I)
ENTRY_ID = re.compile(r"^([A-Z]{2,5}-[A-Z0-9]{1,3})\s*(?:-\s*)?(.*)$", re.S)


def build_sights(folder):
    text = scrub((ROOT / folder / "sightseeing.md").read_text())
    pre, secs = split_sections(text, 2)
    intro = md(re.sub(r"^# .*\n", "", pre, count=1))
    cats = []
    for title, body in secs:
        ctitle = plain(re.sub(r"^\d+\.\s*", "", title))
        if SIGHT_SKIP.match(ctitle):
            continue
        cat_shb = bool(SHB_TITLE.search(ctitle))
        sub_pre, subs = split_sections(body, 3)
        entries = []
        for st, sb in subs:
            m = ENTRY_ID.match(st)
            eid, name = (m.group(1), plain(m.group(2))) if m else ("", plain(st))
            f = fields(sb)
            why = plain(f.get("why", ""))
            shb = cat_shb or bool(SHB_TITLE.search(name)) or bool(SHB_ID.match(eid)) or \
                bool(re.match(r"\s*- See SHB-", sb))
            entries.append({"id": eid, "title": name, "why": why, "shb": shb,
                            "html": link_ids(md(sb, base_level=5))})
        cats.append({"title": ctitle, "shb": cat_shb, "intro": link_ids(md(sub_pre)), "entries": entries})
    return {"intro": link_ids(intro), "cats": cats}


# ------------------------------------------------------- sources and checks


def build_refs(folder):
    refs = []
    for fname, label in (("sources.md", "Flight sources"), ("sightseeing-sources.md", "Things-to-do sources")):
        text = scrub((ROOT / folder / fname).read_text())
        refs.append({"title": label, "html": md(re.sub(r"^# .*\n", "", text, count=1))})
    fc = scrub((ROOT / folder / "fact-check.md").read_text())
    _, secs = split_sections(fc, 2)
    for title, body in secs:
        if re.search(r"remaining unknowns|resolved open items", title, re.I):
            refs.append({"title": "Fact-check: " + plain(title).lower(), "html": link_ids(md(body))})
    return refs


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--site", metavar="DIR", help="write a standalone DIR/index.html for static hosting")
    args = ap.parse_args()
    data = {}
    for folder, prefix in CITIES:
        data[folder] = {
            "flights": build_flights(folder, prefix),
            "sights": build_sights(folder),
            "refs": build_refs(folder),
        }
    blob = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    page = (UI / "template.html").read_text().replace("/*__DATA__*/null", blob)
    if args.site:
        # Standalone document for static hosting: the template is a head-less
        # fragment, so split it at the first body element and wrap it.
        cut = page.index("<header")
        doc = (
            '<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            '<meta name="robots" content="noindex">\n'
            "<style>:root{color-scheme:light}body{margin:0}img{max-width:100%}"
            "[hidden]{display:none!important}</style>\n"
            + page[:cut] + "</head>\n<body>\n" + page[cut:] + "\n</body>\n</html>\n"
        )
        site = Path(args.site)
        site.mkdir(parents=True, exist_ok=True)
        out = site / "index.html"
        out.write_text(doc)
        (site / ".nojekyll").write_text("")
    else:
        out = UI / "sabaton-2027-trip.html"
        out.write_text(page)
    print(f"wrote {out} ({out.stat().st_size // 1024} KB)")
    for folder, _ in CITIES:
        d = data[folder]
        print(f"\n{folder}: {len(d['flights']['itineraries'])} itineraries, "
              f"{sum(len(c['entries']) for c in d['sights']['cats'])} entries, "
              f"{len(d['flights']['background'])} background sections")
        for it in d["flights"]["itineraries"]:
            print(f"  {it['id']} pp={it.get('pp')!r} total={it.get('total')!r} rule={it['rule']!r}/{it['ruleTone']} "
                  f"ver={it['ver']!r}/{it['verTone']} dev={it['dev']} pick={it['pick']!r}")
        print("  shabbat-flagged:", [e["id"] or e["title"] for c in d["sights"]["cats"] for e in c["entries"] if e["shb"]])
        print("  cats:", [(c["title"], len(c["entries"])) for c in d["sights"]["cats"]])


if __name__ == "__main__":
    main()
