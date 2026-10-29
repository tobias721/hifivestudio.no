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
    ('H.mestI({"2025-11": 590, "2025-12": 480, "2026-01": 880})', "Mest i januar 2026: 880."),
    ('H.perDag(H.verdi({"snitt": 720, "maaneder": {"2026-01": 880}}))', "≈ 24 om dagen."),
    ('H.verdi({lav:20, hoy:86}).tekst', "20–86"),
    ('String(H.verdi(null))', "null"),
    ('H.mestI(null)', ""),
    # B1 30.10: søket i alle stedene (ekte data/bysok.json lastet inn som D)
    ('H.sok(D, "Bærum", 1)[0].by', "Bærum"),
    ('H.sok(D, "Baerum", 1)[0].by', "Bærum"),
    ('H.sok(D, "bærum kommune", 1)[0].by', "Bærum"),
    ('H.sok(D, "Bærun", 1)[0].by', "Bærum"),
    ('H.sok(D, "Sandvika", 1)[0].by', "Sandvika"),
    ('H.etikett(H.sok(D, "Bekkestua", 1)[0])', "Bekkestua (Bærum)"),
    ('H.etikett(H.sok(D, "Hamar", 1)[0])', "Hamar"),
    ('String(H.sok(D, "Tromsoe", 1)[0].by)', "Tromsø"),
    ('String(H.sok(D, "Aalesund", 1)[0].by)', "Ålesund"),
    ('String(H.sok(D, "be").length <= 8)', "true"),
    ('String(H.sok(D, "xqzv").length)', "0"),
    ('H.kildeFor(H.sok(D, "Bærum", 1)[0], D).by', "Sandvika"),
    ('H.kildeFor(H.sok(D, "Grünerløkka", 1)[0], D).by', "Oslo"),
    ('String(H.kildeFor(H.sok(D, "Nesbyen", 1)[0], D))', "null"),
    ('H.utenTallTekst("Nesbyen").indexOf("Vi har ikke tallet for <strong>Nesbyen</strong> ennå")', "0"),
    # ingen oppslag med tomt tall viser et intervall: kildeFor gir enten null eller et sted med ekte tall
    ('String(D.filter(function(b){var k=H.kildeFor(b,D);return k && !H.verdi(k.rorlegger);}).length)', "0"),
    ('String(D.filter(function(b){return !b.rorlegger && H.kildeFor(b,D)===b;}).length)', "0"),
]
def main():
    js = open(os.path.join(ROT, "js", "bysok.js"), encoding="utf-8").read()
    data = open(os.path.join(ROT, "data", "bysok.json"), encoding="utf-8").read()
    kropp = "<script>" + js + "</script><script>var D=(" + data + ").byer,H=window.HiFiveBy,r=[];" + "".join(
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
