#!/usr/bin/env python3
"""
add_edition.py — prepend a new edition to The Design Wire.

Usage:  python3 add_edition.py editions/2026-08-26.json [index.html]

Non-destructive by design. It only ever INSERTS:
  * a new <article class="edition"> at the top of <div id="editions">
  * a new <li> at the top of <ul id="archive">
  * moves aria-current="true" onto the new rail button

It refuses to run if the edition already exists, and it verifies the
edition count went up by exactly one before writing anything to disk.
"""
import json, re, sys, html, datetime, pathlib

def esc(t):
    """Escape for HTML text nodes. Keeps <em>/<b> the author intentionally wrote."""
    t = html.escape(t, quote=False)
    for tag in ("em", "b", "i", "strong"):
        t = t.replace(f"&lt;{tag}&gt;", f"<{tag}>").replace(f"&lt;/{tag}&gt;", f"</{tag}>")
    return t

BEATS = [("ai", "AI &amp; Tooling"), ("ux", "UX Craft &amp; Research"),
         ("product", "Product &amp; Startups"), ("industry", "Industry &amp; Careers")]

def card(s):
    flag = f' <span class="flag">{esc(s["flag"])}</span>' if s.get("flag") else ""
    return f'''<article class="story">
              <div class="src eyebrow"><span class="pub">{esc(s["pub"])}</span> · <span>{esc(s["date"])}</span>{flag}</div>
              <h4 class="hed"><a href="{html.escape(s["url"], quote=True)}" target="_blank" rel="noopener">{esc(s["hed"])}</a></h4>
              <p class="fact">{esc(s["fact"])}</p>
              <p class="why"><b>Why it matters</b>{esc(s["why"])}</p>
              <div class="angle">
                <p class="hook">{esc(s["hook"])}</p>
                <div class="split">
                  <p class="teach"><span>Teach</span>{esc(s["teach"])}</p>
                  <p><span>Signal</span>{esc(s["signal"])}</p>
                </div>
                <div class="actions"><button class="copy" type="button">Copy angle</button><button type="button" class="filebtn">Create draft</button><p class="filenote" hidden=""></p></div>
              </div>
            </article>'''

def render(ed):
    date, label = ed["date"], ed["label"]
    out = [f'      <!-- ############ EDITION {date} ############ -->',
           f'      <article class="edition" data-ed="{date}" data-label="{label}">', '']
    for key, title in BEATS:
        stories = ed["beats"].get(key, [])
        if not stories:
            continue
        out += [f'        <section class="beat" data-beat="{key}">',
                f'          <div class="beat-head"><h3>{title}</h3><span class="rule"></span><span class="count"></span></div>',
                 '          <div class="grid">', '']
        for s in stories:
            out += ['            ' + card(s).split("\n")[0]] + card(s).split("\n")[1:] + ['']
        out += ['          </div>', '        </section>', '']
    out += ['      </article>', '']
    return "\n".join(out)

def main():
    data = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
    page = pathlib.Path(sys.argv[2] if len(sys.argv) > 2 else "index.html")
    src = page.read_text(encoding="utf-8")
    date = data["date"]

    if f'data-ed="{date}"' in src:
        sys.exit(f"REFUSING: edition {date} is already on the page.")

    before = len(re.findall(r'<article class="edition"', src))
    n = sum(len(v) for v in data["beats"].values())

    # 1. insert the edition
    anchor = '<div id="editions">'
    if anchor not in src:
        sys.exit("REFUSING: could not find <div id=\"editions\">.")
    src = src.replace(anchor, anchor + "\n\n" + render(data), 1)

    # 2. clear the old aria-current INSIDE THE RAIL ONLY (chips use it too), add the new entry
    rail_m = re.search(r'<ul class="archive" id="archive">.*?</ul>', src, re.S)
    if not rail_m:
        sys.exit("REFUSING: could not find the archive rail.")
    rail_html = rail_m.group(0)
    src = src.replace(rail_html, re.sub(r'\s+aria-current="true"', "", rail_html), 1)
    dt = datetime.date.fromisoformat(date)
    short = f'{dt.day} {dt.strftime("%b")} {dt.year}'
    meta = f'{dt.strftime("%a")} · {n} stories'
    li = (f'      <li>\n        <button class="ed-link" type="button" data-ed="{date}" aria-current="true">\n'
          f'          <span class="d">{short}</span>\n          <span class="m">{meta}</span>\n'
          f'        </button>\n      </li>')
    rail = '<ul class="archive" id="archive">'
    if rail not in src:
        sys.exit("REFUSING: could not find the archive rail.")
    src = src.replace(rail, rail + "\n" + li, 1)

    # 3. verify before writing
    after = len(re.findall(r'<article class="edition"', src))
    if after != before + 1:
        sys.exit(f"REFUSING: edition count went {before} -> {after}, expected {before + 1}.")
    rail_after = re.search(r'<ul class="archive" id="archive">.*?</ul>', src, re.S).group(0)
    if rail_after.count('aria-current="true"') != 1:
        sys.exit("REFUSING: aria-current is not on exactly one rail button.")
    if len(re.findall(r'class="ed-link"', rail_after)) != after:
        sys.exit("REFUSING: rail entries and editions are out of sync.")

    page.write_text(src, encoding="utf-8")
    print(f"Added edition {date}: {n} stories. Editions on page: {before} -> {after}.")

if __name__ == "__main__":
    main()
