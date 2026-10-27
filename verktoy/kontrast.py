#!/usr/bin/env python3
"""N5: WCAG-kontrast for tekstfargene på hifivestudio.no. Krav: ≥ 4,5:1 for tekst under 18 px (AA).
Kjør: python3 verktoy/kontrast.py   (kode 0 = alt ok)"""
import sys
def rgb(h): h = h.lstrip("#"); return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
def blend(fg, a, bg): return tuple(f * a + b * (1 - a) for f, b in zip(fg, bg))
def lum(c): return sum(w * (x / 12.92 if x <= .03928 else ((x + .055) / 1.055) ** 2.4) for w, x in zip((.2126, .7152, .0722), c))
def ratio(a, b): la, lb = sorted((lum(a), lum(b)), reverse=True); return (la + .05) / (lb + .05)
LYS = {"hvit": rgb("ffffff"), "lys grå (alt)": rgb("f6f7f9")}
MØRK = {"hero-kort": rgb("121318")}
TEKST_LYS = {"--ink #0f1623": rgb("0f1623"), "--ink-soft #4b5563": rgb("4b5563"), "--ink-mute #5b6472": rgb("5b6472"),
             "blå #2f5bff (lenker/etiketter)": rgb("2f5bff"), "hvit på blå knapp": None}
TEKST_MØRK = {"ink .92": (rgb("f6f3f0"), .92), "ink-soft .72": (rgb("f6f3f0"), .72), "ink-mute .66": (rgb("f6f3f0"), .66), "blå-ink #8aa4ff": (rgb("8aa4ff"), 1)}
feil = 0
def sjekk(navn, bg_navn, r):
    global feil
    ok = r >= 4.5; feil += not ok
    print(f"{'ok  ' if ok else 'FEIL'} {r:5.2f}:1  {navn} på {bg_navn}")
for bn, bg in LYS.items():
    for tn, t in TEKST_LYS.items():
        sjekk(tn, bn, ratio(rgb("ffffff"), rgb("2f5bff")) if t is None else ratio(t, bg))
for bn, bg in MØRK.items():
    for tn, (t, a) in TEKST_MØRK.items():
        sjekk(tn, bn, ratio(blend(t, a, bg), bg))
print(f"\n{'Alt ok' if not feil else f'{feil} under 4,5:1'}"); sys.exit(1 if feil else 0)
