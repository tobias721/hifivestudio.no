// N2/N4/N5 27.10: søk på byen i helsesjekk-kortet i heroen. Bare ekte tall fra /data/bysok.json
// (Google Ads Søkeordplanlegger). Ingen rammeverk, ingen sporing, ikke noe skjema.
// Uten JS står kortet som eksempel og søkefeltet er skjult.
(function () {
  var MND = ["januar", "februar", "mars", "april", "mai", "juni", "juli", "august", "september", "oktober", "november", "desember"];
  function fmt(n) { return String(n).replace(/\B(?=(\d{3})+(?!\d))/g, " "); }
  function verdi(v) {   // → {tekst, min, maks, eksakt, maaneder}
    if (v && typeof v === "object" && typeof v.snitt === "number")
      return { tekst: fmt(v.snitt), min: v.snitt, maks: v.snitt, eksakt: true, maaneder: v.maaneder || null };
    if (v && typeof v === "object" && "lav" in v) return { tekst: v.lav + "–" + v.hoy, min: v.lav, maks: v.hoy, eksakt: false };
    if (v === null || v === undefined || v === "") return null;
    var t = String(v), n = (t.match(/\d+(?: \d{3})*/g) || []).map(function (x) { return parseInt(x.replace(/ /g, ""), 10); });
    return { tekst: t, min: n[0], maks: n[n.length - 1], eksakt: false, maaneder: null };
  }
  function perDag(v) {   // «Det er omtrent 3–33 søk om dagen.» / «≈ 24 om dagen.»
    if (!v || !v.maks) return "";
    if (v.eksakt) return "≈ " + fmt(Math.round(v.min / 30)) + " om dagen.";
    var a = Math.round(v.min / 30), b = Math.round(v.maks / 30);
    return a < 1 ? "Det er opptil " + fmt(b) + " søk om dagen." : "Det er omtrent " + fmt(a) + "–" + fmt(b) + " søk om dagen.";
  }
  function mestI(m) {   // maaneder = [12 tall, jan–des], {"januar": 880, …} eller V1-formatet {"2026-01": 880, …}
    if (!m) return "";
    var navn = function (k) { var d = /^(\d{4})-(\d{2})$/.exec(k); return d ? MND[parseInt(d[2], 10) - 1] + " " + d[1] : k; };
    var liste = Array.isArray(m) ? m.map(function (n, i) { return [MND[i], n]; }) : Object.keys(m).map(function (k) { return [navn(k), m[k]]; });
    if (!liste.length) return "";
    var best = liste.reduce(function (a, b) { return b[1] > a[1] ? b : a; });
    return "Mest i " + best[0] + ": " + fmt(best[1]) + ".";
  }
  // ---- B1 30.10: søk i ~580 steder (kommuner, tettsteder, bydeler) som tåler skrivefeil og æøå/ae-oe-aa ----
  function canon(s) {   // «Bærum kommune» / «Baerum» / «BÆRUM» → «baerum»; «Tromsø»/«Tromsoe» → «tromso»; «Ålesund»/«Aalesund» → «alesund»
    return String(s || "").toLowerCase().replace(/\s+(kommune|bydel|by|sentrum)$/, "")
      .replace(/æ/g, "ae").replace(/ø/g, "o").replace(/å/g, "a").replace(/oe/g, "o").replace(/aa/g, "a")
      .replace(/[^a-z0-9]+/g, " ").trim();
  }
  function avstand(a, b, maks) {   // redigeringsavstand (Levenshtein), stopper over maks
    if (Math.abs(a.length - b.length) > maks) return maks + 1;
    var f = [], i, j;
    for (j = 0; j <= b.length; j++) f[j] = j;
    for (i = 1; i <= a.length; i++) {
      var forrige = f[0], minst = f[0] = i;
      for (j = 1; j <= b.length; j++) {
        var tmp = f[j];
        f[j] = Math.min(f[j] + 1, f[j - 1] + 1, forrige + (a[i - 1] === b[j - 1] ? 0 : 1));
        forrige = tmp; if (f[j] < minst) minst = f[j];
      }
      if (minst > maks) return maks + 1;
    }
    return f[b.length];
  }
  function harTall(b) { return !!(b && verdi(b.rorlegger)); }
  function sokSteder(liste, q, maks) {   // → inntil maks steder, best først: eksakt, starten av navnet, ordstart, inni, skrivefeil
    q = canon(q); maks = maks || 8;
    if (!q) return [];
    var grense = q.length >= 7 ? 2 : q.length >= 4 ? 1 : 0, treff = [];
    liste.forEach(function (b) {
      var n = canon(b.by), p = -1;
      if (n === q) p = 0;
      else if (n.indexOf(q) === 0) p = 1;
      else if ((" " + n).indexOf(" " + q) > -1) p = 2;
      else if (q.length >= 3 && n.indexOf(q) > -1) p = 3;
      else if (grense) { var d = avstand(q, n, grense); if (d <= grense) p = 3 + d; }
      if (p > -1) treff.push([p, b]);
    });
    treff.sort(function (x, y) {
      return x[0] - y[0] || (harTall(y[1]) - harTall(x[1])) || ((y[1].folk || 0) - (x[1].folk || 0)) || (x[1].by < y[1].by ? -1 : 1);
    });
    return treff.slice(0, maks).map(function (t) { return t[1]; });
  }
  function etikett(b) {   // «Bekkestua (Bærum)» – kommunen i parentes når stedet ikke selv er kommunen
    return b.kommune && canon(b.kommune) !== canon(b.by) ? b.by + " (" + b.kommune + ")" : b.by;
  }
  function kildeFor(b, liste) {   // stedet selv hvis det har tall, ellers stedet med tall i samme kommune (tall_fra), ellers null
    if (harTall(b)) return b;
    if (!b || !b.tall_fra) return null;
    for (var i = 0; i < liste.length; i++) if (liste[i].by === b.tall_fra && harTall(liste[i])) return liste[i];
    return null;
  }
  function utenTallTekst(navn) {
    return "Vi har ikke tallet for <strong>" + escH(navn) + "</strong> ennå. Ring <a href=\"tel:+4791904010\">91 90 40 10</a> " +
           "eller send e-post, så henter vi det for deg.";
  }
  function escH(s) { return String(s).replace(/[&<>"']/g, function (c) { return "&#" + c.charCodeAt(0) + ";"; }); }
  window.HiFiveBy = { verdi: verdi, perDag: perDag, mestI: mestI, canon: canon, sok: sokSteder, etikett: etikett,
                      kildeFor: kildeFor, harTall: harTall, utenTallTekst: utenTallTekst };

  var kort = document.getElementById("hkort");
  if (!kort || !window.fetch) return;
  var sok = document.getElementById("hsok"), felt = document.getElementById("hby"), forslag = document.getElementById("hforslag"),
      knapp = document.getElementById("hsjekk"), tag = document.getElementById("htag"), tittel = document.getElementById("htittel"),
      dato = document.getElementById("hdato"), innhold = document.getElementById("hinnhold"), byer = [], valgt = null, aktiv = -1, viste = [];
  var rolig = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;

  var esc = escH;
  function mailto(by) {
    var tekst = "Hei Tobias!\n\nJeg vil gjerne ha en gratis helsesjekk for " + by + ".\n\nFirma:\nTelefon:\n\nMvh";
    return "mailto:tobias@hifivestudio.no?subject=" + encodeURIComponent("Helsesjekk for " + by) + "&body=" + encodeURIComponent(tekst);
  }
  function knapp_html(tekst, by) {
    return '<div class="report-fix"><p>' + tekst + '</p><a class="btn" href="' + esc(mailto(by)) +
           '">Få gratis helsesjekk for ' + esc(by) + ' <span class="btn-arrow" aria-hidden="true">→</span></a>' +
           '<button class="report-igjen" type="button" id="higjen">Prøv en annen by</button></div>';
  }
  function igjen() {   // «Prøv en annen by»: tøm feltet og sett fokus
    var b = document.getElementById("higjen");
    if (b) b.addEventListener("click", function () { felt.value = ""; valgt = null; felt.focus(); });
  }
  function adresse(by) {   // ?by=<By> så lenken kan deles (bare i svar til interesserte og i helsesjekk-PDF)
    try { var u = new URL(location.href); u.searchParams.set("by", by); history.replaceState(null, "", u); } catch (e) {}
  }
  // ---- forslagslista (combobox): maks 8, piltaster, Enter, Esc, klikk ----
  function lukk() { forslag.hidden = true; felt.setAttribute("aria-expanded", "false"); felt.removeAttribute("aria-activedescendant"); aktiv = -1; }
  function marker(i) {
    aktiv = i;
    Array.prototype.forEach.call(forslag.children, function (li, j) { li.setAttribute("aria-selected", j === i ? "true" : "false"); });
    if (i > -1) felt.setAttribute("aria-activedescendant", "hforslag-" + i); else felt.removeAttribute("aria-activedescendant");
  }
  function velg(b) { valgt = b; felt.value = b.by; lukk(); vis(); }
  function visForslag() {
    valgt = null;
    viste = sokSteder(byer, felt.value, 8);
    if (!viste.length) return lukk();
    forslag.innerHTML = viste.map(function (b, i) {
      return '<li role="option" id="hforslag-' + i + '" aria-selected="false">' + esc(etikett(b)) + "</li>";
    }).join("");
    Array.prototype.forEach.call(forslag.children, function (li, i) {
      li.addEventListener("mousedown", function (e) { e.preventDefault(); velg(viste[i]); });   // før feltet mister fokus
    });
    forslag.hidden = false; felt.setAttribute("aria-expanded", "true"); marker(-1);
  }
  function tell(el) {   // tellende tall på 300 ms: «1 000–10 000» teller fra 0 til hvert av tallene
    var mal = el.getAttribute("data-v");
    if (rolig) { el.textContent = mal; return; }
    var tall = (mal.match(/\d+(?: \d{3})*/g) || []).map(function (t) { return parseInt(t.replace(/ /g, ""), 10); }),
        start = Date.now(), ferdig = false;
    function slutt() { ferdig = true; el.textContent = mal; }
    function steg() {
      if (ferdig) return;
      var k = Math.min(1, (Date.now() - start) / 300), i = 0;
      if (k >= 1) return slutt();
      el.textContent = mal.replace(/\d+(?: \d{3})*/g, function () { return fmt(Math.round(tall[i++] * k)); });
      requestAnimationFrame(steg);
    }
    requestAnimationFrame(steg);
    setTimeout(slutt, 320);   // sikring: riktige tall selv om animasjonen ikke får kjøre (bakgrunnsfane o.l.)
  }
  function vis() {
    var q = felt.value.trim();
    if (!q && !valgt) return;
    lukk();
    var b = valgt || sokSteder(byer, q, 1)[0] || null, by = b ? b.by : q.charAt(0).toUpperCase() + q.slice(1);
    var k = kildeFor(b, byer);
    tittel.textContent = "Rørlegger i " + by;
    if (!k) {   // aldri et tall vi ikke har (B1)
      tag.textContent = "Ikke hentet ennå"; dato.textContent = b && b.kommune && b.kommune !== b.by ? b.kommune + " kommune" : "";
      innhold.innerHTML = knapp_html(utenTallTekst(by), by);
      igjen(); adresse(by);
      return;
    }
    var egne = k === b;
    tag.textContent = egne ? "Tall fra Google" : "Tall for " + k.by; dato.textContent = "Siste 12 måneder";
    var rad = function (dt, v) { return '<div><dt>' + dt + '</dt><dd class="tell" data-v="' + esc(v) + '">' + esc(v) + '</dd></div>'; };
    var ror = verdi(k.rorlegger), bad = verdi(k.baderom), kp = verdi(k.klikkpris);
    var ekstra = [perDag(ror), mestI(ror && ror.maaneder)].filter(Boolean).join(" ");
    innhold.innerHTML = (egne ? "" : '<p class="report-dag">Vi har ikke egne tall for ' + esc(by) + ' ennå. Tallene under gjelder søk på «rørlegger ' +
        esc(k.by.toLowerCase()) + '» i samme kommune.</p>') +
      '<dl>' + rad("Søk i måneden, «rørlegger " + esc(k.by.toLowerCase()) + "»", ror.tekst) +
      (bad ? rad("Baderom " + esc(k.by), bad.tekst) : "") +
      (kp ? rad("Klikkpris, toppen av siden", kp.tekst + " kr") : "") +
      '</dl>' + (ekstra ? '<p class="report-dag">' + esc(ekstra) + '</p>' : "") +
      '<p class="report-kilde">Kilde: Google Ads Søkeordplanlegger</p>' +
      knapp_html("Hvor står ditt firma? Få gratis helsesjekk for " + esc(by) + ".", by);
    igjen(); adresse(by);
    Array.prototype.forEach.call(innhold.querySelectorAll(".tell"), tell);
  }

  fetch("/data/bysok.json").then(function (r) { return r.json(); }).then(function (d) {
    byer = d.byer || [];
    sok.hidden = false;
    // høyden låses til eksempelkortets (med søkefeltet) på desktop, så siden ikke hopper når tallene byttes
    if (matchMedia("(min-width:981px)").matches) kort.style.setProperty("--hkort-h", kort.offsetHeight + "px");
    knapp.addEventListener("click", vis);
    felt.addEventListener("input", visForslag);
    felt.addEventListener("blur", function () { setTimeout(lukk, 120); });
    felt.addEventListener("keydown", function (e) {
      var n = forslag.hidden ? 0 : viste.length;
      if (e.key === "ArrowDown" && n) { e.preventDefault(); marker((aktiv + 1) % n); }
      else if (e.key === "ArrowUp" && n) { e.preventDefault(); marker((aktiv - 1 + n) % n); }
      else if (e.key === "Escape") lukk();
      else if (e.key === "Enter") { e.preventDefault(); if (aktiv > -1) velg(viste[aktiv]); else vis(); }
    });
    var fra = new URLSearchParams(location.search).get("by");   // hifivestudio.no/?by=Hamar (lenke i e-post)
    if (fra) { felt.value = fra; vis(); }
  }).catch(function () { /* data utilgjengelig → kortet står som eksempel */ });
})();
