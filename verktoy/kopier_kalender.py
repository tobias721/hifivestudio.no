#!/usr/bin/env python3
"""K2/N7 30.10: kopier chat-Claudes kalender-demo inn som /kalender/ på nettsiden – samme ramme hver gang.

  python3 verktoy/kopier_kalender.py [kilde]      # standard kilde: vaultets Fra-Chat/kalender-demo/index.html

Kilden er en side uten <head> (laget for Claude-appen). Skriptet:
  1. legger nettsidens egen <head> rundt (lang, viewport, beskrivelse, noindex, favicon, safe-area-stil)
  2. bytter Google Fonts mot den lokale /fonts/dm-sans.woff2 (ingen forespørsler til Google fra besøkende – N5-regelen)
  3. fjerner meta-linjen som bare gjelder Claude-appen
  4. legger «← hifivestudio.no» foran merket øverst, med stil
  5. avslutter med </body></html>
Rediger aldri kalender/index.html for hånd – endringer gjøres i kilden (K2-regelen), så kjøres skriptet på nytt.
"""
import os, re, sys
from pathlib import Path

ROT = Path(__file__).resolve().parent.parent
UT = ROT / "kalender/index.html"
KILDE = Path(os.path.expanduser("~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Claude/Fra-Chat/kalender-demo/index.html"))

HODE = """<!doctype html>
<html lang="no">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="description" content="Demo av arbeidskalenderen fra HiFive Studio: dra jobber på montører, dag- og ukevisning, legg inn jobber fra tekst eller bilde. Oppdiktede navn.">
<meta name="robots" content="noindex">
<link rel="icon" href="/img/favicon.svg" type="image/svg+xml">
<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)} [hidden]{display:none!important} img{max-width:100%}</style>
"""
FONT = ('<link rel="preload" href="/fonts/dm-sans.woff2" as="font" type="font/woff2" crossorigin>\n'
        '<style>@font-face{font-family:"DM Sans";src:url(/fonts/dm-sans.woff2) format("woff2");font-weight:400 700;font-style:normal;font-display:swap}</style>')
TILBAKE_CSS = (".tilbake{font-size:13px;color:var(--fg2);text-decoration:none;border-right:1px solid var(--linje);padding-right:12px}\n"
               ".tilbake:hover{color:var(--fg)}\n")
TILBAKE = '<a class="tilbake" href="/">← hifivestudio.no</a>'


def pakk_inn(kilde):
    s = kilde
    if re.search(r"<!doctype|<html|<head>", s[:500], re.I):
        sys.exit("Kilden har alt egen <head> – sjekk den før kopiering (ikke laget som K2-demo).")
    s = re.sub(r'^\s*<meta name="claude:[^"]*"[^>]*>\n', "", s, flags=re.M)
    s = re.sub(r'^\s*<link[^>]+fonts\.(?:googleapis|gstatic)\.com[^>]*>\n', "", s, flags=re.M)   # preconnect + stilark
    if "fonts.googleapis" in s or "fonts.gstatic" in s:
        sys.exit("Google Fonts finnes fortsatt i kilden på en form skriptet ikke kjenner – sjekk for hånd.")
    i = s.find("<style>")
    s = s[:i] + FONT + "\n" + s[i:] if i > -1 else FONT + "\n" + s
    slutt = s.find("</style>", i + len(FONT) + 1 if i > -1 else 0)   # første stilblokk i kilden (den store)
    s = s[:slutt] + TILBAKE_CSS + s[slutt:]
    app = s.find('<div class="app">')
    if app < 0:
        sys.exit('Fant ikke <div class="app"> i kilden – sjekk strukturen.')
    s = s[:app] + "</head>\n<body>\n" + s[app:]
    if '<div class="merke">' not in s:
        sys.exit('Fant ikke <div class="merke"> – tilbake-lenken trenger et sted.')
    s = s.replace('<div class="merke">', TILBAKE + '<div class="merke">', 1)
    return HODE + s.rstrip("\n") + "\n\n</body>\n</html>\n"


def main():
    kilde = Path(sys.argv[1]) if len(sys.argv) > 1 else KILDE
    ut = pakk_inn(kilde.read_text(encoding="utf-8"))
    UT.write_text(ut, encoding="utf-8")
    print(f"{kilde.name} → {UT.relative_to(ROT)} ({len(ut.encode())} byte, googleapis: {ut.count('googleapis')})")


if __name__ == "__main__":
    main()
