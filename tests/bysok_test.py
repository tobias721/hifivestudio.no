#!/usr/bin/env python3
"""N5: test av regnefunksjonene i js/bysok.js for begge dataskjemaene (dagens strenger og V1 {snitt, maaneder}).
Node finnes ikke på Macen, så testen kjører JavaScript-en i Google Chrome (headless) og leser resultatet.
Kjør: python3 tests/bysok_test.py   (kode 0 = alt ok)"""
import os, re, subprocess, sys, tempfile
ROT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
SAKER = [   # (uttrykk, forventet)
    ('H.verdi("100–1 000").tekst', "100–1 000"),
    ('H.perDag(H.verdi("100–1 000"))', "Det er omtrent 3–33 søk om dagen."),
    ('H.perDag(H.verdi("10–100"))', "Det er opptil 3 søk om dagen."),
    ('H.verdi({snitt:720, maaneder:[880,700,650,600,560,520,480,500,640,700,760,820]}).tekst', "720"),
    ('H.perDag(H.verdi({snitt:720}))', "≈ 24 om dagen."),
    ('H.mestI([880,700,650,600,560,520,480,500,640,700,760,820])', "Mest i januar: 880."),
    ('H.mestI({"mars": 1200, "april": 900})', "Mest i mars: 1 200."),
    ('H.verdi({lav:20, hoy:86}).tekst', "20–86"),
    ('String(H.verdi(null))', "null"),
    ('H.mestI(null)', ""),
]
def main():
    js = open(os.path.join(ROT, "js", "bysok.js"), encoding="utf-8").read()
    kropp = "<script>" + js + "</script><script>var H=window.HiFiveBy,r=[];" + "".join(
        f"try{{r.push(String({u}))}}catch(e){{r.push('FEIL '+e)}};" for u, _ in SAKER) + \
        "document.title='R'+JSON.stringify(r)</script>"
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as f:
        f.write("<!doctype html><meta charset=utf-8><body>" + kropp); sti = f.name
    ut = subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--dump-dom", "file://" + sti], capture_output=True, text=True, timeout=60).stdout
    os.remove(sti)
    import json, html
    m = re.search(r"<title>R(.*?)</title>", ut)
    if not m: sys.exit("Fant ikke resultat fra Chrome")
    svar = json.loads(html.unescape(m.group(1)))
    feil = 0
    for (u, venter), fikk in zip(SAKER, svar):
        ok = fikk == venter
        feil += not ok
        print(("ok  " if ok else "FEIL"), u, "→", repr(fikk), "" if ok else f"(ventet {venter!r})")
    print(f"\n{len(SAKER) - feil}/{len(SAKER)} passerte"); sys.exit(1 if feil else 0)
if __name__ == "__main__":
    main()
