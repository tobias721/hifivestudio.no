#!/usr/bin/env python3
"""N5: lager img/og.png (1200×630, delingsbilde) med Google Chrome headless. Ingen personer, ingen tall.
Kjør: python3 verktoy/lag_og.py"""
import os, re, subprocess, tempfile
ROT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
hand = re.search(r"HAND = '(<svg.*?</svg>)'", open(os.path.join(ROT, "build.py"), encoding="utf-8").read()).group(1)
hand = hand.replace('class="hero-hand"', 'style="position:absolute;right:70px;top:60px;height:510px;color:#2f5bff;opacity:.9"')
fonter = "".join(f'@font-face{{font-family:"{f}";src:url(file://{ROT}/fonts/{fil})}}' for f, fil in
                 (("DM Sans", "dm-sans.woff2"), ("Fraunces", "fraunces-400.woff2")))
side = f"""<!doctype html><meta charset="utf-8"><style>{fonter}
html,body{{margin:0;width:1200px;height:630px;background:#0b0c0e;color:rgba(246,243,240,.92);overflow:hidden}}
.r{{position:relative;width:1200px;height:630px;padding:84px 80px;box-sizing:border-box}}
.e{{font:600 22px "DM Sans";letter-spacing:.14em;text-transform:uppercase;color:rgba(246,243,240,.66)}}
h1{{font:400 76px/1.05 "Fraunces";margin:28px 0 0;max-width:720px}}
.u{{position:absolute;left:80px;bottom:72px;font:500 26px "DM Sans";color:rgba(246,243,240,.66)}}
</style><div class="r">{hand}<div class="e">HiFive Studio</div><h1>Google-synlighet for rørleggere</h1><div class="u">hifivestudio.no</div></div>"""
with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as f:
    f.write(side); sti = f.name
ut = os.path.join(ROT, "img", "og.png")
subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--window-size=1200,630",
                "--virtual-time-budget=2000", f"--screenshot={ut}", "file://" + sti], capture_output=True, timeout=60)
os.remove(sti)
print(ut, os.path.getsize(ut) // 1024, "kB")
