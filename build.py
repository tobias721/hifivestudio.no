#!/usr/bin/env python3
"""Bygger de statiske sidene for hifivestudio.no. Kjør: python3 build.py"""
from pathlib import Path
from urllib.parse import quote

OUT = Path(__file__).parent
TEL = "tel:+4791904010"
EPOST = "tobias@hifivestudio.no"   # N3 27.10: personlig adresse gir flere svar (post@ er alias til samme innboks)
MAILTEKST = "Hei Tobias!\n\nJeg er interessert i å høre mer om en gratis gjennomgang.\n\nFirma:\nBy/område:\nTelefon:\n\nMvh"


def mailto(emne="Gratis gjennomgang", tekst=MAILTEKST):
    """mailto med ferdig emne og tekst (URL-kodet). &amp; fordi lenken står i et HTML-attributt."""
    return f"mailto:{EPOST}?subject={quote(emne)}&amp;body={quote(tekst)}"


MAIL = mailto()
FONT = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,600&family=Fraunces:ital,opsz,wght@0,9..144,400;1,9..144,400&display=swap" rel="stylesheet">'

# Hånd-logoen som tynn linjetegning bak heroen (samme sti som img/logo-hand.svg)
HAND = '<svg class="hero-hand" aria-hidden="true" viewBox="100 90 265 320" fill="none" stroke="currentColor" stroke-width="1.2"><path d="M185,250 L185,130 L225,130 L225,105 L265,105 L265,130 L305,130 L305,185 L345,185 L345,330 L325,360 L325,392 L225,392 L225,380 C225,366 211.3,351.9 200,335.4 L121,223 C113,211 126,201 142,208 L185,250 Z"/><path d="M225,130 L225,220 L265,220 L265,130"/><path d="M305,130 L305,325"/><path d="M225,325 L225,255 L265,255 L265,325"/></svg>'

# Ekte bilde av Tobias: legg img/tobias.webp (eller .jpg), 1200 px bredt. Mangler fila, bygges seksjonen uten bilde.
PHOTO = next((p for p in ("tobias.webp", "tobias.jpg") if (OUT / "img" / p).exists()), None)

TRUST = '<ul class="trust"><li>Org.nr. 938 365 180</li><li>Ingen binding</li><li>Du eier alt: domene, nettside og Google-profil</li></ul>'


def page(slug, title, desc, body):
    canon = "https://hifivestudio.no/" + ("" if slug == "index" else slug)
    return f"""<!doctype html>
<html lang="no">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canon}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:url" content="{canon}">
<meta property="og:site_name" content="HiFive Studio">
<meta property="og:locale" content="nb_NO">
<meta name="twitter:card" content="summary">
<meta name="theme-color" content="#0b0c0e">
<link rel="icon" href="/img/favicon.svg" type="image/svg+xml">
{FONT}
<link rel="stylesheet" href="/style.css">
</head>
<body>
<nav class="nav" id="nav">
  <a class="logo" href="/"><img src="/img/logo-hand.svg" alt="" width="22" height="26">HiFive Studio</a>
  <button class="menu-btn" aria-expanded="false" aria-controls="links" onclick="var n=document.getElementById('nav');n.classList.toggle('open');this.setAttribute('aria-expanded',n.classList.contains('open'))">Meny</button>
  <ul class="nav-links" id="links">
    <li><a href="/tjenester">Tjenester</a></li>
    <li><a href="/priser-og-pakker">Priser og pakker</a></li>
    <li><a href="/#faq">Spørsmål</a></li>
    <li><a href="{TEL}">91 90 40 10</a></li>
    <li><a class="btn small" href="/kontakt">Kontakt</a></li>
  </ul>
</nav>
<main>
{body}
</main>
<footer>
  <div class="wrap">
    <div class="foot">
      <div>
        <a class="logo" href="/"><img src="/img/logo-hand.svg" alt="" width="22" height="26">HiFive Studio</a>
        <p style="margin-top:14px">Vi gjør håndverksbedrifter synlige der kundene leter: Google-profil, annonser og sosiale medier. Satt opp én gang, driftet av oss.</p>
      </div>
      <div>
        <span class="eyebrow">Snarveier</span>
        <ul>
          <li><a href="/tjenester">Tjenester</a></li>
          <li><a href="/priser-og-pakker">Priser</a></li>
          <li><a href="/#faq">Spørsmål</a></li>
          <li><a href="/kontakt">Kontakt</a></li>
          <li><a href="/om-oss">Om oss</a></li>
          <li><a href="/personvern">Personvern</a></li>
          <li><a href="/vilkar">Vilkår</a></li>
        </ul>
      </div>
    </div>
    <div class="legal">
      <span>HiFive Studio · Lilleakerveien 31B, 0283 Oslo · Org.nr. 938 365 180 · <a href="{MAIL}">{EPOST}</a> · <a href="{TEL}">91 90 40 10</a></span>
      <span>© 2026 HiFive Studio</span>
    </div>
  </div>
</footer>
</body>
</html>
"""


def cta(title="Klar for flere kunder?"):
    return f"""<section><div class="wrap"><div class="cta">
  <h2>{title}</h2>
  <p>Fortell oss om bedriften din, så gjør vi en gratis gjennomgang: dukker du opp når folk søker etter tjenesten din i området ditt, ikke bare på firmanavnet? Hvordan står Google-profilen din mot konkurrentene? Du får en ærlig prioritering av hva som bør fikses først, uten forpliktelser.</p>
  <div class="cta-actions"><a class="btn" href="{TEL}">Ring 91 90 40 10</a><a class="btn ghost" href="{MAIL}">Send e-post</a><a class="btn ghost" href="/priser-og-pakker">Se pakkene</a></div>
</div></div></section>"""


SERVICES = [
    ("Google Bedriftsprofil", "Profilen din på Google Maps og Søk blir satt opp, verifisert og holdt aktiv, så du dukker opp når folk i området søker. Og når ChatGPT eller Googles AI anbefaler rørleggere, er det denne profilen de leser."),
    ("Google Ads og Meta-annonser", "Vi bygger og drifter annonsene som vises når folk i området ditt søker etter det du gjør. Annonsebudsjettet betaler du rett til Google . Vi tar ingen prosent."),
    ("Landingsside som gir henvendelser", "En side laget for én ting: at den som klikker tar kontakt. Kort, mobilvennlig, med skjema som kvalifiserer kunden."),
    ("Varsel under 30 sekunder", "Du får SMS og e-post med navn, telefon og hva det gjelder under 30 sekunder etter at skjemaet er sendt."),
    ("Sosiale medier", "Vi skriver innleggene og driver Facebook og Instagram. Du sender bilder fra jobbene . Vi tar resten."),
    ("Økonomisk rapport", "Tallene i kroner, ikke klikk og visninger: hva som er brukt, hvor mange henvendelser det ga, og hva hver kostet."),
]

STEPS = [
    ("Gratis gjennomgang", "Vi ser hvordan bedriften din ser ut på Google i dag: hvor mange som søker etter bad i ditt område, hva et klikk koster der, og hvem som ligger øverst. Tall, ikke gjetting."),
    ("Tre råd du kan gjøre selv", "Du får tre konkrete ting du kan fikse i dag – gratis, uansett om du bruker oss etterpå."),
    ("En meny, ikke en pakke", "Vi foreslår det som passer, og sier høyt hva du ikke trenger. Halvparten trenger bare det billigste."),
    ("Rapport i kroner", "Brukt, henvendelser, pris per henvendelse. Ingen klikk og visninger – tall du kan ta en beslutning på."),
]

# Helsesjekken – eksempeltall, typiske for et rørleggerfirma i en mellomstor by
HEALTH = [
    ("H1", "Søketall", "100–1 000", "søk i måneden på «rørlegger + din by»", "Hvor mange i byen din som leter etter det du gjør, hver måned."),
    ("H2", "Hva en ny kunde koster", "1 000–5 000 kr", "per henvendelse via Google (anslag)", "Klikkprisen i ditt område regnet om til kroner per henvendelse. Her: ca. 25–100 kr per klikk."),
    ("H3", "Mot de tre øverste", "0 mot 150", "Google-omtaler, mot nr. 1 på kartet", "Du mot de tre øverste i søket, punkt for punkt: omtaler, egen side, telefon, bilder av egne jobber."),
    ("H4", "AI-synlighet", "Svak", "lite for ChatGPT og Googles AI å lese (anslag)", "Om firmaet har det AI-tjenestene henter fra: komplett profil, omtaler og like opplysninger overalt."),
    ("H5", "Hva bør fikses først", "2 ulike", "telefonnumre på Google og nettsiden", "Tre konkrete tiltak sortert etter effekt. De du kan gjøre selv i dag, får du gratis."),
]

# N4 27.10: kortet er interaktivt – søk på byen øverst, js/bysok.js bytter eksempelet med Googles tall for byen
REPORT = """<aside class="report" id="hkort" aria-label="Helsesjekk – søk på byen din">
  <div class="report-sok" id="hsok" hidden>
    <label class="sr" for="hby">Skriv byen din</label>
    <input id="hby" list="hbyer" placeholder="Skriv byen din" autocomplete="off" enterkeyhint="search">
    <datalist id="hbyer"></datalist>
    <button class="btn" id="hsjekk" type="button">Sjekk</button>
  </div>
  <div class="report-top"><span class="eyebrow">Helsesjekk</span><span class="report-tag" id="htag">Eksempel</span></div>
  <div class="report-firm" id="htittel">Rørleggerfirma i en mellomstor norsk by</div>
  <div class="report-date" id="hdato">Oktober 2026</div>
  <div id="hinnhold" aria-live="polite">
  <dl>
    <div><dt>Søk i måneden, «rørlegger + din by»</dt><dd>100–1 000</dd></div>
    <div><dt>Klikkpris, toppen av siden</dt><dd>ca. 25–100 kr</dd></div>
    <div><dt>Telefonnumre i omløp</dt><dd>2 ulike</dd></div>
  </dl>
  <div class="bars">
    <div class="bars-label">Google-omtaler</div>
    <div class="bar low"><span>Dette firmaet</span><i style="--w:0%"></i><b>0</b></div>
    <div class="bar"><span>Nr. 1 i området</span><i style="--w:100%"></i><b>150</b></div>
    <div class="bar"><span>Nr. 2</span><i style="--w:40%"></i><b>60</b></div>
    <div class="bar"><span>Nr. 3</span><i style="--w:27%"></i><b>40</b></div>
  </div>
  <div class="report-fix"><span class="eyebrow">Fiks først</span><p>Samme telefonnummer overalt, og en fast rutine for å be om omtaler etter hver jobb.</p></div>
  </div>
</aside>"""


def tobias():
    text = """<div class="me-text">
    <span class="eyebrow">Hvem du snakker med</span>
    <p class="me-quote">Rørlegger i 14 år. Jeg vet hvordan kundene finner dere, for jeg har vært på den andre siden.</p>
    <p class="muted">Tobias Svendsen, HiFive Studio · <a class="link" href="/om-oss">Om oss</a></p>
  </div>"""
    if not PHOTO:
        return f'<section class="me"><div class="wrap">{text}</div></section>'
    img = f'<figure class="me-photo"><img src="/img/{PHOTO}" alt="Tobias Svendsen i arbeidstøy" width="1200" height="1500" loading="lazy" decoding="async"></figure>'
    return f'<section class="me"><div class="wrap me-grid">{img}{text}</div></section>'


FAQ = [
    ("Hva er HiFive Studio?", "Vi sørger for at folk som skal pusse opp havner hos deg, og bare deg. Vi kjører annonsene, lager siden de lander på, og sender henvendelsen rett på mobilen din sekunder etter at den kommer inn. Tobias som driver HiFive er rørlegger med 14 år i faget, så vi kjenner bransjen fra innsiden."),
    ("Hvorfor anbefaler dere minst 3 måneder med annonsering?", "Fordi Google og Meta må lære hvem som er riktig kunde for deg. Måned 1 samler systemet data og finner ut hvilke søk og hvilke folk som faktisk fører til jobber. Da er henvendelsene færre og dyrere. Måned 2 begynner vi å kutte det som ikke virker og legge pengene der de gir resultat. Måned 3 er kampanjen innkjørt, og det er da du ser hva den faktisk kan levere. Stopper du etter fire uker, betaler du for læringen uten å få gevinsten. Derfor anbefaler vi 90 dager. Men vi har ingen bindingstid, og du kan si opp når du vil."),
    ("Hvor mange henvendelser kan jeg forvente?", "Regnestykket er enkelt: et klikk på relevante søkeord koster typisk 20–40 kr i Norge, og omtrent 2–3 av 100 som klikker tar faktisk kontakt. Med 12.000 kr i annonsebudsjett får du rundt 350–450 klikk, som gir 8–12 kvalifiserte henvendelser i måneden. Første måned ligger normalt lavere mens kampanjen lærer hvem som er riktig kunde for deg. Det er et regnestykke, ikke et løfte. Det eneste vi garanterer står her: gir kampanjen færre enn 6 kvalifiserte henvendelser i perioden dag 31 til dag 90, refunderer vi oppsettet på Kundebooking og Eksklusiv. De første 30 dagene er datainnsamling og teller ikke med. Forutsetter annonsebudsjett fra 12.000 kr/mnd (Kundebooking) eller 18.000 kr/mnd (Eksklusiv) i hele perioden."),
    ("Hva er en kvalifisert henvendelse, og er det bindingstid?", "En kvalifisert henvendelse er en person med ekte navn og telefonnummer som svarer, innenfor ditt område, som eier boligen eller bestemmer, og som vil ha jobben gjort innen seks måneder. Feil nummer, selgere og folk utenfor området teller ikke. Du betaler fast pris, uten tillegg per henvendelse, uansett hvor mange du får. Og nei, det er ingen bindingstid og ingen oppsigelsestid: du kan si opp fra måned til måned. Vi jobber med én bedrift per område, så du konkurrerer aldri mot en annen av våre kunder om de samme henvendelsene."),
    ("Hva er annonsebudsjett, og hvor går pengene?", "Annonsebudsjettet er pengene som kjøper selve visningene på Google og Facebook. Når noen søker etter «bad renovering» i ditt område, er det en auksjon om hvem som vises øverst, og annonsebudsjettet er det du byr med. Du betaler kun når noen faktisk klikker seg inn til deg. 100 % av annonsebudsjettet går til Google og Meta, ikke til oss. Kontoen står i ditt navn med ditt kort, du betaler dem direkte, og du ser hver eneste krone i ditt eget dashbord. De fleste norske byråer tar 10–20 % av annonsebudsjettet i tillegg til månedsprisen. Det gjør ikke vi. Du betaler kun fastprisen. Den dekker at vi bygger kampanjen, skriver annonsene, lager landingssiden, setter opp varslingen og justerer alt løpende. To separate regninger, ingen skjulte påslag."),
]

OBJ = [
    ("«Vi har prøvd Google Ads før – det funket ikke.»", "Da er spørsmålet: hva ble målt? De fleste får satt opp en kampanje uten sporing, og så vet ingen om det var annonsene som sviktet eller om ingen så etter. Vi sporer hvert anrop og hvert skjema fra annonsene, og du ser tallene hver uke – i kroner, ikke klikk."),
    ("«Kan dere garantere resultater?»", "Nei. Ingen kan det, og de som sier det lyver. Det vi garanterer er oppsettet, målingen – og på Kundebooking og Eksklusiv et minimum av kvalifiserte henvendelser i perioden dag 31–90. Får du færre enn 6, refunderer vi oppsettet."),
    ("«Jeg trenger jobber allerede neste måned.»", "Da er Google Ads på bad feil produkt for deg, og det sier vi heller nå enn etterpå. Henvendelsene kommer fra måned én, men et bad er en beslutning folk bruker to til seks måneder på – signerte jobber ser du i måned tre til seks. Trenger du omsetning raskt, starter vi med Synlig (Google-profilen) eller ingenting."),
    ("«Vi er med i en kjede – trenger vi dette?»", "Kanskje ikke. Spør kjeden hva de gjør lokalt: kjører de annonser på «baderom» i byen din med ditt telefonnummer, eller stopper det ved en profilside? Gjør kjeden jobben, trenger du oss ikke – og det sier vi. Gjør de det ikke, konkurrerer du mot naboen om de samme kundene."),
    ("«Vi har ikke budsjett til dette.»", "Da er det enda viktigere å bruke det lille på riktig sted. Det billigste som virker er nesten gratis: Google-profilen din, riktig satt opp – det er Synlig til 1 490 kr i måneden, uten annonser. Annonser kan vente til det er penger til det. Halvparten av dem vi snakker med trenger bare det billigste, og det sier vi rett ut."),
    ("«Finner ChatGPT og Googles AI oss?»", "Det finnes ikke noe AI-triks, og vi lover ingen plassering. ChatGPT og Googles AI-modus anbefaler rørleggere ut fra det de kan lese: en komplett Google-profil med riktig kategori og område, mange og ferske anmeldelser, en nettside som svarer på spørsmål, og samme navn, adresse og telefon overalt. Det er nøyaktig det Synlig setter opp – og vi måler hvor mange som finner deg den veien."),
]


def faq_items(items):
    return "\n".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in items)


# ---------- Forside ----------
home = f"""
<section class="hero">{HAND}<div class="wrap hero-grid">
  <div>
    <div class="eyebrow">Gratis gjennomgang</div>
    <h1 style="margin-top:18px">Kundene dine googler. Vi sørger for at de finner deg.</h1>
    <p class="lead">Vi setter opp Google-annonsene, landingssiden og sporingen for håndverkerbedrifter, og drifter alt videre. Du tar telefonen. Fast månedspris, ingen bindingstid, og annonsebudsjettet betaler du rett til Google.</p>
    <div class="hero-actions">
      <a class="btn" href="/kontakt">Be om gratis gjennomgang</a>
      <a class="link" href="{TEL}">Eller ring 91 90 40 10</a>
    </div>
    <p class="hero-trust">Tobias Svendsen · rørlegger i 14 år · Org.nr 938 365 180</p>
  </div>
  {REPORT}
</div></section>

<script src="/js/bysok.js" defer></script>

<section id="helsesjekk"><div class="wrap">
  <div class="sec-head"><h2>Slik ser en helsesjekk ut</h2><p class="lead">Fem punkter, med tall fra ditt område. Slik ser resultatet ut. Tallene er typiske for et rørleggerfirma i en mellomstor by.</p></div>
  <ol class="health">
    {''.join(f'<li class="hcard"><div class="hcard-top"><span class="hnum">{n}</span><span class="ex">Eksempel</span></div><h3>{t}</h3><div class="hval">{v}</div><div class="hunit">{u}</div><p>{d}</p></li>' for n, t, v, u, d in HEALTH)}
  </ol>
</div></section>

{tobias()}

<section id="tjenester"><div class="wrap">
  <div class="sec-head"><h2>Dette gjør vi</h2><p class="lead">Du trenger ikke alt. Vi setter sammen det som passer bedriften din, og drifter det videre.</p></div>
  <div class="grid g3">
    {''.join(f'<div class="card"><h3>{t}</h3><p>{d}</p></div>' for t, d in SERVICES)}
  </div>
</div></section>

<section><div class="wrap">
  <div class="sec-head"><h2>Slik jobber vi</h2><p class="lead">Ingen pakke før diagnosen. Vi jobber som en rørlegger på befaring: se først, foreslå etterpå.</p></div>
  <div class="steps">
    <div>
      {''.join(f'<div class="step"><div class="num">{i}</div><div><h3>{t}</h3><p>{d}</p></div></div>' for i, (t, d) in enumerate(STEPS, 1))}
    </div>
    <figure>
      <img src="/img/rapport.webp" alt="Eksempel på ukesrapport fra HiFive Studio" width="1344" height="752" loading="lazy">
      <figcaption>Eksempel: illustrasjon av ukesrapporten, ikke ekte tall. Din rapport viser hva du brukte, hvor mange som tok kontakt og hva hver henvendelse kostet.</figcaption>
    </figure>
  </div>
</div></section>

<section><div class="wrap">
  <div class="sec-head"><h2>Priser og pakker</h2><p class="lead">Fast månedspris, ingen bindingstid. Annonsebudsjettet betaler du rett til Google og Meta . Vi tar ingen prosent.</p></div>
  <div class="prices">
    <div class="price"><h3>Synlig</h3><div class="meta">For deg under 4 mill. i omsetning</div><div class="amt">1.490 kr/mnd</div><div class="meta">Oppsett 4.900 kr · ingen annonser</div>
      <ul><li>Google Bedriftsprofil</li><li>Gule Sider, 1881, Proff, Mittanbud</li><li>QR og rutine for anmeldelser</li><li>Kvartalsvis gjennomgang</li></ul></div>
    <div class="price pop"><span class="tag">Mest populær</span><h3>Kundebooking</h3><div class="meta">4–8 mill. i omsetning</div><div class="amt">5.900 kr/mnd</div><div class="meta">Oppsett 9.900 kr · annonsebudsjett fra 12.000 kr</div>
      <ul><li>Alt i Synlig</li><li>Google Ads bygget og driftet</li><li>Landingsside og varsel på SMS</li><li>Eksklusivt i ditt område</li></ul></div>
    <div class="price"><h3>Eksklusiv</h3><div class="meta">8–15 mill. i omsetning</div><div class="amt">9.900 kr/mnd</div><div class="meta">Oppsett 14.900 kr · annonsebudsjett fra 18.000 kr</div>
      <ul><li>Alt i Kundebooking</li><li>To områder</li><li>Google + Meta-annonser</li><li>Ukentlig rapport</li></ul></div>
    <div class="price"><h3>Pro</h3><div class="meta">15 mill.+ i omsetning</div><div class="amt">fra 14.900 kr/mnd</div><div class="meta">Oppsett etter avtale · budsjett fra 25.000 kr</div>
      <ul><li>Alt i Eksklusiv</li><li>Flere områder</li><li>Månedlig strategimøte</li><li>Egen kontaktperson</li></ul></div>
  </div>
  {TRUST}
  <p style="margin-top:28px"><a class="link" href="/priser-og-pakker">Se alle priser og pakker →</a></p>
</div></section>

<section id="faq"><div class="wrap">
  <div class="sec-head"><h2>Spørsmål, besvart.</h2></div>
  <div class="faq">{faq_items(FAQ)}</div>
  <div class="eyebrow faq-sub">Det vi oftest får høre på telefon</div>
  <div class="faq">{faq_items(OBJ)}</div>
</div></section>
{cta()}
"""

# ---------- Tjenester ----------
TJ = [
    ("Google Bedriftsprofil", "Vi setter opp og verifiserer profilen din på Google Maps og Søk, med riktige kategorier, åpningstider og tjenester. Så holder vi den aktiv med jevnlige innlegg, slik at du dukker opp når folk i området søker etter det du driver med. Det samme oppsettet gjør deg lesbar for ChatGPT og Googles AI-modus, og vi måler hvor mange som finner deg den veien."),
    ("Google Ads og Meta-annonser", "Vi bygger og styrer annonsene som vises når folk i området ditt søker etter tjenestene dine. Vi skriver annonsetekstene, velger søkeordene og justerer løpende. Annonsebudsjettet betaler du direkte til Google og Meta . Vi tar ingen prosent av det."),
    ("Landingsside som gir henvendelser", "En side laget for én ting: at den som klikker faktisk tar kontakt. Kort, tydelig og bygget for mobil, med et skjema som kvalifiserer kunden før du bruker tid på dem."),
    ("Varsel under 30 sekunder", "Når noen fyller ut skjemaet, får du SMS og e-post med en gang: navn, telefon, adresse og hva det gjelder. Du ringer tilbake mens de fortsatt sitter med telefonen i hånda, før konkurrenten rekker det."),
    ("Sosiale medier", "Vi skriver innleggene og driver Facebook og Instagram for deg. Du sender bilder og en kort beskrivelse fra jobbene dine . Vi tar resten."),
    ("Økonomisk rapport", "Du får tallene i kroner, ikke klikk og visninger: hva som er brukt, hvor mange henvendelser det ga, og hva hver henvendelse kostet."),
]
tjenester = f"""
<section class="page-head"><div class="wrap">
  <h1>Dette gjør vi</h1>
  <p class="lead">Vi sørger for at folk som skal pusse opp havner hos deg og bare deg, og at de får svar før konkurrenten rekker å ringe tilbake. Her er delene vi setter sammen.</p>
</div></section>
<section style="padding-top:0"><div class="wrap">
  <div class="grid g2">{''.join(f'<div class="card"><h3>{t}</h3><p>{d}</p></div>' for t, d in TJ)}</div>
  <p style="margin-top:32px">Se hva dette koster under <a class="link" href="/priser-og-pakker">Priser og pakker</a>.</p>
</div></section>
{cta()}
"""

# ---------- Priser ----------
def pkg(name, desc, amt, paras, pop=False):
    tag = '<span class="tag">Mest populær</span>' if pop else ""
    body = "".join(f"<p>{p}</p>" for p in paras)
    cls = "pkg pop-pkg" if pop else "pkg"
    return f'<div class="{cls}">{tag}<div class="pkg-head"><h2>{name}</h2><div class="amt">{amt}</div></div><p class="desc">{desc}</p>{body}</div>'

PK = [
    ("Synlig", "Bedriften blir synlig på Google og Google Maps og lett å finne. Satt opp én gang, målt hvert kvartal, ingen annonser.", "1.490 kr/mnd", [
        "<strong>Oppsett 4.900 kr.</strong> Ingen bindingstid og ingen oppsigelsestid.",
        "Google Bedriftsprofil satt opp, verifisert og optimalisert · riktig kategori, område, åpningstider og tjenesteliste på Google Maps · samme navn, adresse og telefon på Gule Sider, 1881, Proff og Mittanbud · bilder lagt inn og navngitt riktig · kvartalsvis gjennomgang med rapport på visninger, klikk og anrop fra Google.",
        "<strong>Kartmåling.</strong> Vi måler hvor du faktisk vises i Google Maps, punkt for punkt rundt området ditt, ikke bare fra din egen adresse. Målt ved oppstart, og på nytt i hver kvartalsrapport, så du ser kartet før og etter.",
        "<strong>Anmeldelser.</strong> QR-kode og SMS-lenke for Google-anmeldelser, og en fast rutine: samme lenke til alle kunder etter fullført jobb, én påminnelse. Ingen siling. Det er både Googles og Forbrukertilsynets regel, og det er det som gjør anmeldelsene troverdige.",
        "<strong>AI-søk er med.</strong> Det samme oppsettet gjør firmaet ditt lesbart for ChatGPT og Googles AI-modus: komplett profil med riktig kategori og område, ferske anmeldelser, samme navn, adresse og telefon overalt. Vi lover ingen plassering, for ingen kan det. Men vi måler hvor mange som finner deg via AI-assistenter, og det står i rapporten din.",
        "Ingen annonsekostnad. Ingen løpende arbeid for deg.",
        "<strong>Passer for:</strong> deg som driver alene eller med én ansatt, har nok å gjøre, men vil at de som søker skal finne deg, ikke konkurrenten.",
    ]),
    ("Synlig Start", "Nystartet? Alt på plass på én dag: Google, Gule Sider, 1881, Mittanbud, Finn og Facebook. Så blir du funnet fra første uke.", "990 kr/mnd", [
        "<strong>For bedrifter under ett år.</strong> Oppsett 9.990 kr hvis du har logo fra før, 13.990 kr hvis vi lager logoen for deg. Ingen bindingstid og ingen oppsigelsestid. For bedrifter registrert de siste 12 månedene.",
        "Alt i Synlig · Google Bedriftsprofil opprettet fra null og verifisert · profil på Finn.no, Mittanbud, Gule Sider, 1881 og Proff med samme navn, adresse og telefon overalt · Facebook-side · e-postsignatur og logofil · mal for å be om anmeldelse · kartmåling ved oppstart.",
        "<strong>Hvorfor høyt oppsett og lav måned:</strong> jobben er å få alt riktig fra start. Etterpå skal det gå av seg selv, og en nystartet bedrift skal ikke betale for mer enn den trenger i måned to.",
        "Nettside og online booking er ikke med. Det legges til når du er klar, som en del av Kundebooking.",
        "<strong>Passer for:</strong> deg som nettopp har startet og vil bruke tiden på jobbene, ikke på registreringer.",
    ]),
    ("Kundebooking", "For deg med kapasitet til flere jobber. Kvalifiserte henvendelser rett på mobilen, og kun du i ditt område.", "5.900 kr/mnd", [
        "<strong>Oppsett 9.900 kr.</strong> Fast pris, uten tillegg per henvendelse. Ingen bindingstid og ingen oppsigelsestid. Vi anbefaler minst 3 måneder. Det er tiden Google trenger for å lære hvem som er riktig kunde for deg.",
        "Annonsebudsjettet bestemmer du selv, og det betales direkte til Google på din egen konto. Vi tar ingen prosent av det. Vi anbefaler fra 12.000 kr/mnd, og det er forutsetningen for garantien under. Men du kan starte lavere hvis du vil prøve deg fram. Da sier vi bare tydelig fra at garantien ikke gjelder.",
        "Alt i Synlig · Google Ads-søkekampanje bygget og driftet av oss · landingsside laget for å gi henvendelser · skjema som kvalifiserer · varsel på SMS og e-post · 2 Google-innlegg i måneden · månedlig rapport i kroner · eksklusivitet i ditt område: vi jobber kun med én bedrift per område.",
        "<strong>Hva 12.000 kr typisk gir:</strong> 8–12 kvalifiserte henvendelser i måneden når kampanjen er innkjørt. Det er et regnestykke, ikke et løfte. Det eneste vi garanterer står under. Vi teller kun de som faktisk er aktuelle: eier boligen, riktig område, skal ha jobben gjort. Første måned ligger normalt lavere mens kampanjen lærer.",
        "<strong>Vår garanti:</strong> gir kampanjen færre enn 6 kvalifiserte henvendelser i perioden dag 31–90, refunderer vi oppsettet. De første 30 dagene er datainnsamling og teller ikke. Forutsetter annonsebudsjett på minst 12.000 kr/mnd i hele perioden.",
        "<strong>Passer for:</strong> deg som har folk nok til å ta flere jobber, og som vil ha jevn tilgang framfor tilfeldige forespørsler. <strong>Passer sammen med:</strong> Sosiale medier.",
    ]),
    ("Eksklusiv", "To områder, Google og Meta, større budsjett og flere henvendelser.", "9.900 kr/mnd", [
        "<strong>Oppsett 14.900 kr.</strong> Fast pris, uten tillegg per henvendelse. Ingen bindingstid og ingen oppsigelsestid. Annonsebudsjett fra 18.000 kr/mnd betales direkte til Google og Meta, på dine egne kontoer. Vi tar ingen prosent av det.",
        "Alt i Kundebooking, men for to områder · Google Ads + Meta-annonser · flere kampanjer · 4 Google-innlegg i måneden · ukentlig rapport i kroner og kvartalsvis gjennomgang.",
        "<strong>Hva 18.000 kr typisk gir:</strong> 12–18 kvalifiserte henvendelser i måneden når kampanjene er innkjørt. Et regnestykke, ikke et løfte.",
        "<strong>Vår garanti:</strong> gir kampanjene færre enn 6 kvalifiserte henvendelser i perioden dag 31–90, refunderer vi oppsettet. De første 30 dagene er datainnsamling og teller ikke. Forutsetter annonsebudsjett på minst 18.000 kr/mnd i hele perioden.",
        "<strong>Passer for:</strong> deg som dekker flere områder og har kapasitet til volum.",
    ]),
    ("Pro", "For de største. Flere områder, flere kampanjer og tettest oppfølging. På forespørsel.", "fra 14.900 kr/mnd", [
        "<strong>Oppsett etter avtale.</strong> Fast pris, uten tillegg per henvendelse. Ingen bindingstid og ingen oppsigelsestid. Annonsebudsjett fra 25.000 kr/mnd betales direkte.",
        "Alt i Eksklusiv · flere områder · hjelp til å samle Google-anmeldelser etter fullført jobb · ukentlig rapport · månedlig strategimøte · egen kontaktperson.",
        "<strong>Passer for:</strong> bedrifter med flere lag og kapasitet til å ta imot volum. Vi setter opp Pro etter en gjennomgang av bedriften. Ta kontakt.",
    ]),
    ("Sosiale medier", "Vi skriver innleggene og driver Facebook og Instagram for deg. Du sender bilder og en kort beskrivelse . Vi tar resten.", "3.990 kr/mnd", [
        "<strong>Oppsett 4.900 kr.</strong> Tillegg som kan legges til alle pakker. Ingen bindingstid.",
        "8 innlegg i måneden på Facebook og 8 på Instagram · vi skriver all tekst · vi planlegger og publiserer på tidspunktene som gir mest · løpende drift av kontoene.",
        "<strong>Slik fungerer det:</strong> Du sender oss bilder og videoer fra jobbene dine, sammen med en kort beskrivelse av hva som er gjort, for eksempel «komplett bad på Majorstuen, nytt røropplegg og varmekabler». Noen setninger holder. Mobilbilder holder fint.",
        "Send materiale annenhver uke eller én gang i måneden. Vi bruker samme materiale på begge kanaler. Produksjon av nytt bilde- og videomateriale er ikke inkludert.",
        "<strong>Passer sammen med:</strong> Kundebooking og oppover. Innleggene gir mest verdi når folk allerede finner deg.",
    ]),
]
priser = f"""
<section class="page-head"><div class="wrap">
  <h1>Priser og pakker</h1>
  <p class="lead">Velg det du trenger, eller la oss sette sammen en pakke etter en gratis gjennomgang. Prisene er uten mva – HiFive Studio er foreløpig ikke mva-registrert, så det kommer ingenting i tillegg. Vi anbefaler aldri mer enn det som faktisk gir deg flere kunder.</p>
</div></section>
<section style="padding-top:0"><div class="wrap">
  {''.join(pkg(n, d, a, p, pop=(n == 'Kundebooking')) for n, d, a, p in PK)}
  {TRUST}
</div></section>
{cta()}
"""

# ---------- Kontakt ----------
kontakt = f"""
<section class="page-head"><div class="wrap">
  <h1>Kontakt oss</h1>
  <p class="lead">Ring 91 90 40 10, eller send en e-post. Vi svarer innen én virkedag.</p>
</div></section>
<section style="padding-top:0"><div class="wrap">
  <div class="contact-grid">
    <div class="card"><span class="eyebrow">Telefon</span><a href="{TEL}">91 90 40 10</a></div>
    <div class="card"><span class="eyebrow">E-post</span><a href="{MAIL}">{EPOST}</a></div>
  </div>
  <div class="prose" style="margin-top:48px">
    <h2>Be om gratis gjennomgang</h2>
    <p>Skriv kort i e-posten: firmanavn, fag (rørlegger, elektriker, tømrer …), hvilket område du jobber i, og hva du lurer på. Bilder er velkomne. Du får svar direkte på e-posten din.</p>
    <p><a class="btn" href="{MAIL}">Skriv e-post</a></p>
  </div>
</div></section>
"""

# ---------- Om oss ----------
omoss = f"""
<section class="page-head"><div class="wrap">
  <h1>Om HiFive Studio</h1>
  <p class="lead">Vi gjør håndverkerbedrifter synlige der kundene faktisk leter, og drifter det videre, så du slipper.</p>
</div></section>
<section style="padding-top:0"><div class="wrap">
  <div class="prose"><p style="font-size:19px">HiFive Studio er startet av Tobias Svendsen, rørlegger med 14 års erfaring fra håndverksbransjen. Jeg vet hvordan det er å drive en liten bedrift der jobben tar all tid, og nettside, Google og sosiale medier blir liggende. Derfor bygde jeg HiFive: vi setter opp synligheten din én gang, og drifter den etterpå, så du kan bruke tiden på kundene dine i stedet for på skjermen.</p></div>
  <h2 style="margin:64px 0 28px">Hvorfor velge oss?</h2>
  <div class="grid g2">
    <div class="card"><h3>Erfaring</h3><p>Vi kjenner bransjen din fra innsiden, ikke bare fra et byråkontor.</p></div>
    <div class="card"><h3>Fast pris</h3><p>Fast månedspris, ingen bindingstid, og vi tar aldri prosent av annonsebudsjettet ditt.</p></div>
    <div class="card"><h3>Raskt</h3><p>Fra ja til live på ti arbeidsdager. Du bruker under en time på oppstarten.</p></div>
    <div class="card"><h3>Fleksibelt</h3><p>Fra Google-profil og annonser til sosiale medier. Én kontaktperson, én faktura.</p></div>
  </div>
</div></section>
{cta()}
"""

ADR = f'<p>HiFive Studio<br>Lilleakerveien 31B<br>0283 Oslo<br>Org.nr. 938 365 180<br><a class="link" href="{MAIL}">{EPOST}</a></p>'

vilkar = f"""
<section class="page-head"><div class="wrap"><h1>Vilkår</h1><p class="muted" style="margin-top:16px">Sist oppdatert: 21. oktober 2026</p></div></section>
<section style="padding-top:0"><div class="wrap prose">
<h2>Om nettsiden</h2><p>hifivestudio.no drives av HiFive Studio (HIFIVESTUDIO SVENDSEN, org.nr. 938 365 180), Lilleakerveien 31B, 0283 Oslo. Ved å bruke nettsiden godtar du disse vilkårene.</p>
<h2>Henvendelser og gratis gjennomgang</h2><p>Når du tar kontakt på e-post eller telefon og ber om en gjennomgang, ber du oss om en uforpliktende vurdering av bedriftens digitale synlighet. Vurderingen er gratis og medfører ingen forpliktelse til kjøp. Vi tar kontakt på e-post eller telefon innen tre virkedager.</p>
<h2>Tjenester og avtaler</h2><p>Kjøp av tjenester reguleres av egen avtale som inngås skriftlig før oppstart. Priser på nettsiden er veiledende og oppgitt eksklusiv merverdiavgift. Vi forbeholder oss retten til å endre priser for nye avtaler.</p>
<h2>Annonsebudsjett</h2><p>Annonsebudsjett betales direkte av kunden til Google og Meta, på kundens egen konto. HiFive Studio tar ingen prosentandel av annonsebudsjettet. Månedsprisen dekker oppsett, drift og justering av kampanjene.</p>
<h2>Oppsigelse</h2><p>Driftsavtaler løper fra måned til måned uten bindingstid og uten oppsigelsestid, med mindre annet er skriftlig avtalt. Oppsettsgebyr refunderes ikke ved oppsigelse, med unntak av det som følger av garantien under.</p>
<h2>Garanti</h2><p>På pakkene Kundebooking og Eksklusiv gjelder følgende: gir kampanjen færre enn seks kvalifiserte henvendelser i perioden dag 31 til dag 90, refunderes oppsettsgebyret. De første 30 dagene er datainnsamling og teller ikke med. Garantien forutsetter at avtalt annonsebudsjett er innbetalt i hele perioden, og at kunden svarer på henvendelser. Garantien gjelder ikke ved lavere annonsebudsjett enn pakkens angitte minimum.</p>
<h2>Ansvar</h2><p>Innholdet på nettsiden er gitt etter beste evne, men vi garanterer ikke at det til enhver tid er fullstendig eller feilfritt. HiFive Studio er ikke ansvarlig for tap som følge av bruk av informasjon på nettsiden.</p>
<h2>Immaterielle rettigheter</h2><p>Tekst, bilder og design på hifivestudio.no tilhører HiFive Studio og kan ikke kopieres uten tillatelse.</p>
<h2>Personvern</h2><p>Se vår <a class="link" href="/personvern">personvernerklæring</a> for hvordan vi behandler personopplysninger.</p>
<h2>Lovvalg</h2><p>Vilkårene er underlagt norsk rett.</p>
<h2>Kontakt</h2>{ADR}
</div></section>
"""

personvern = f"""
<section class="page-head"><div class="wrap"><h1>Personvernerklæring</h1><p class="muted" style="margin-top:16px">Sist oppdatert: 27. oktober 2026</p></div></section>
<section style="padding-top:0"><div class="wrap prose">
<p>HiFive Studio (HIFIVESTUDIO SVENDSEN, org.nr. 938 365 180) er behandlingsansvarlig for personopplysninger som samles inn gjennom hifivestudio.no og i kundeforhold. Denne erklæringen forklarer hvilke opplysninger vi samler inn, hvorfor, og hvilke rettigheter du har.</p>
<h2>Hvilke opplysninger vi samler inn</h2>
<p>Når du tar kontakt på e-post eller telefon: navn, firmanavn, e-postadresse, telefonnummer og det du skriver om bedriften din.</p>
<p>Når du blir kunde: i tillegg fakturaadresse, organisasjonsnummer og opplysninger som er nødvendige for å levere tjenesten (tilganger til Google Bedriftsprofil, annonsekontoer og nettside).</p>
<p>Når du besøker nettsiden: vår driftsleverandør kan registrere teknisk informasjon som IP-adresse og nettlesertype i serverlogger, for sikkerhet og drift.</p>
<h2>Hvorfor vi behandler opplysningene</h2>
<p>For å svare på henvendelsen din og gi deg en gjennomgang (berettiget interesse), for å inngå og oppfylle avtalen med deg som kunde (avtale), og for å oppfylle krav i bokføringsloven (rettslig forpliktelse).</p>
<h2>Når vi kontakter bedrifter</h2>
<p>Vi bruker offentlige firmaopplysninger (Brønnøysundregistrene, bedriftens nettside og Google-profil) og bedriftens generelle e-postadresse for å kontakte bedrifter om våre tjenester. Grunnlaget er berettiget interesse (personvernforordningen art. 6 nr. 1 f). Si fra, så kontakter vi dere ikke igjen.</p>
<h2>Hvem vi deler opplysninger med</h2>
<p>Vi bruker følgende leverandører som behandler opplysninger på våre vegne (databehandlere):</p>
<ul>
<li>GitHub: drift av nettsiden</li>
<li>Google (Workspace, Ads, Bedriftsprofil): e-post og annonsering</li>
<li>Meta: annonsering, når det inngår i tjenesten</li>
<li>Zoho Bigin: kundeoppfølging (CRM)</li>
<li>Tripletex: fakturering og regnskap</li>
<li>Vipps: betaling, når det er avtalt</li>
</ul>
<p>Noen av disse leverandørene behandler data utenfor EØS. Overføring skjer på grunnlag av EU-kommisjonens standardkontrakter eller tilsvarende godkjente mekanismer.</p>
<p>Vi selger aldri personopplysninger, og vi deler dem ikke med andre enn de som er nødvendige for å levere tjenesten.</p>
<h2>Hvor lenge vi lagrer opplysningene</h2>
<ul>
<li>Henvendelser som ikke fører til kundeforhold: slettes etter 12 måneder</li>
<li>Kundeopplysninger: så lenge kundeforholdet varer, deretter 12 måneder</li>
<li>Regnskapsbilag: 5 år, i henhold til bokføringsloven</li>
</ul>
<h2>Informasjonskapsler (cookies)</h2>
<p>Nettsiden bruker ikke informasjonskapsler til sporing eller annonsering, og vi kjører ikke analyseverktøy på siden.</p>
<h2>Dine rettigheter</h2>
<p>Du har rett til å be om innsyn i hvilke opplysninger vi har om deg, få dem rettet eller slettet, kreve begrensning av behandlingen, protestere mot behandling basert på berettiget interesse, og få opplysningene utlevert i et vanlig format (dataportabilitet).</p>
<p>Behandling basert på samtykke kan du trekke tilbake når som helst.</p>
<p>Send forespørsler til {EPOST}. Vi svarer innen 30 dager.</p>
<p>Er du uenig i hvordan vi behandler opplysningene dine, kan du klage til Datatilsynet: datatilsynet.no.</p>
<h2>Kontakt</h2>{ADR}
</div></section>
"""

notfound = f"""
<section class="page-head"><div class="wrap"><h1>Siden finnes ikke</h1><p class="lead">Lenken kan være gammel. Gå til <a class="link" href="/">forsiden</a>, eller ring <a class="link" href="{TEL}">91 90 40 10</a>.</p></div></section>
"""

PAGES = [
    ("index", "HiFive Studio – Google-synlighet for håndverkere", "Vi setter opp Google-profil, annonser og landingsside for håndverkerbedrifter – og drifter det videre. Fast månedspris, ingen bindingstid.", home),
    ("tjenester", "Tjenester – HiFive Studio", "Google Bedriftsprofil, Google Ads og Meta-annonser, landingsside, varsel under 30 sekunder, sosiale medier og rapport i kroner.", tjenester),
    ("priser-og-pakker", "Priser og pakker – HiFive Studio", "Synlig fra 1.490 kr/mnd, Kundebooking 5.900 kr/mnd, Eksklusiv 9.900 kr/mnd. Ingen bindingstid, ingen prosent av annonsebudsjettet.", priser),
    ("kontakt", "Kontakt – HiFive Studio", "Ring 91 90 40 10 eller send e-post til tobias@hifivestudio.no for en gratis gjennomgang.", kontakt),
    ("om-oss", "Om oss – HiFive Studio", "HiFive Studio drives av Tobias Svendsen, rørlegger med 14 år i faget. Vi gjør håndverksbedrifter synlige på Google og sender henvendelsene rett på mobilen.", omoss),
    ("vilkar", "Vilkår – HiFive Studio", "Vilkår for bruk av hifivestudio.no og tjenestene til HiFive Studio.", vilkar),
    ("personvern", "Personvernerklæring – HiFive Studio", "Hvordan HiFive Studio behandler personopplysninger.", personvern),
    ("404", "Siden finnes ikke – HiFive Studio", "Siden finnes ikke.", notfound),
]

for slug, title, desc, body in PAGES:
    if slug in ("index", "404"):
        (OUT / f"{slug}.html").write_text(page(slug, title, desc, body), encoding="utf-8")
    else:
        d = OUT / slug
        d.mkdir(exist_ok=True)
        (d / "index.html").write_text(page(slug, title, desc, body), encoding="utf-8")
print("ok")
