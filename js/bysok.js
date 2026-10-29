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
  window.HiFiveBy = { verdi: verdi, perDag: perDag, mestI: mestI };

  var kort = document.getElementById("hkort");
  if (!kort || !window.fetch) return;
  var sok = document.getElementById("hsok"), felt = document.getElementById("hby"), liste = document.getElementById("hbyer"),
      knapp = document.getElementById("hsjekk"), tag = document.getElementById("htag"), tittel = document.getElementById("htittel"),
      dato = document.getElementById("hdato"), innhold = document.getElementById("hinnhold"), byer = [];
  var rolig = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;

  function norm(s) { return (s || "").toLowerCase().replace(/\s+/g, " ").trim(); }
  function esc(s) { return String(s).replace(/[&<>"']/g, function (c) { return "&#" + c.charCodeAt(0) + ";"; }); }
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
    if (b) b.addEventListener("click", function () { felt.value = ""; felt.focus(); });
  }
  function adresse(by) {   // ?by=<By> så lenken kan deles (bare i svar til interesserte og i helsesjekk-PDF)
    try { var u = new URL(location.href); u.searchParams.set("by", by); history.replaceState(null, "", u); } catch (e) {}
  }
  function finn(q) {   // eksakt, så starten av navnet, så delord («Lillestr» → Lillestrøm)
    q = norm(q);
    if (!q) return null;
    var f = function (t) { for (var i = 0; i < byer.length; i++) if (t(norm(byer[i].by))) return byer[i]; return null; };
    return f(function (n) { return n === q; }) || f(function (n) { return n.indexOf(q) === 0; }) || f(function (n) { return n.indexOf(q) > -1; });
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
    if (!q) return;
    var b = finn(q), by = b ? b.by : q.charAt(0).toUpperCase() + q.slice(1);
    tittel.textContent = "Rørlegger i " + by;
    if (!b) {
      tag.textContent = "Ikke hentet ennå"; dato.textContent = "";
      innhold.innerHTML = knapp_html("Vi har ikke tallene for <strong>" + esc(by) + "</strong> klare – vi henter dem gratis.", by);
      igjen(); adresse(by);
      return;
    }
    tag.textContent = "Tall fra Google"; dato.textContent = "Siste 12 måneder";
    var rad = function (dt, v) { return '<div><dt>' + dt + '</dt><dd class="tell" data-v="' + esc(v) + '">' + esc(v) + '</dd></div>'; };
    var ror = verdi(b.rorlegger), bad = verdi(b.baderom), kp = verdi(b.klikkpris);
    var ekstra = [perDag(ror), mestI(ror && ror.maaneder)].filter(Boolean).join(" ");
    innhold.innerHTML = '<dl>' + rad("Søk i måneden, «rørlegger " + esc(by.toLowerCase()) + "»", ror.tekst) +
      (bad ? rad("Baderom " + esc(by), bad.tekst) : "") +
      (kp ? rad("Klikkpris, toppen av siden", kp.tekst + " kr") : "") +
      '</dl>' + (ekstra ? '<p class="report-dag">' + esc(ekstra) + '</p>' : "") +
      '<p class="report-kilde">Kilde: Google Ads Søkeordplanlegger</p>' +
      knapp_html("Hvor står ditt firma? Få gratis helsesjekk for " + esc(by) + ".", by);
    igjen(); adresse(b.by);
    Array.prototype.forEach.call(innhold.querySelectorAll(".tell"), tell);
  }

  fetch("/data/bysok.json").then(function (r) { return r.json(); }).then(function (d) {
    byer = d.byer || [];
    liste.innerHTML = byer.map(function (b) { return '<option value="' + esc(b.by) + '">'; }).join("");
    sok.hidden = false;
    // høyden låses til eksempelkortets (med søkefeltet) på desktop, så siden ikke hopper når tallene byttes
    if (matchMedia("(min-width:981px)").matches) kort.style.setProperty("--hkort-h", kort.offsetHeight + "px");
    knapp.addEventListener("click", vis);
    felt.addEventListener("keydown", function (e) { if (e.key === "Enter") vis(); });
    var fra = new URLSearchParams(location.search).get("by");   // hifivestudio.no/?by=Hamar (lenke i e-post)
    if (fra) { felt.value = fra; vis(); }
  }).catch(function () { /* data utilgjengelig → kortet står som eksempel */ });
})();
