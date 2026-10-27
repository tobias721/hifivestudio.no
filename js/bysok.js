// N2 27.10: «Søk på din by». Bare ekte tall fra /data/bysok.json (Google Ads Søkeordplanlegger).
// Ingen rammeverk, ingen sporing, ikke noe skjema. Uten JS forblir seksjonen skjult (hidden).
(function () {
  var sek = document.getElementById("bysok");
  if (!sek || !window.fetch) return;
  var felt = document.getElementById("by"), liste = document.getElementById("byer"),
      knapp = document.getElementById("vis"), svar = document.getElementById("bysvar"), byer = [];

  function norm(s) { return (s || "").toLowerCase().replace(/\s+/g, " ").trim(); }
  function esc(s) { return String(s).replace(/[&<>"']/g, function (c) { return "&#" + c.charCodeAt(0) + ";"; }); }
  function mailto(by) {
    var tekst = "Hei Tobias!\n\nJeg vil gjerne ha en gratis helsesjekk for " + by + ".\n\nFirma:\nTelefon:\n\nMvh";
    return "mailto:tobias@hifivestudio.no?subject=" + encodeURIComponent("Helsesjekk for " + by) +
           "&body=" + encodeURIComponent(tekst);
  }
  function knapper(by) {
    return '<div class="hero-actions"><a class="btn" href="' + esc(mailto(by)) + '">Få full helsesjekk for ' + esc(by) +
           ' – gratis</a><a class="link" href="tel:+4791904010">eller ring 91 90 40 10</a></div>';
  }
  function finn(q) {   // eksakt først, så starten av navnet, så delord («Lillestr» → Lillestrøm)
    q = norm(q);
    if (!q) return null;
    for (var i = 0; i < byer.length; i++) if (norm(byer[i].by) === q) return byer[i];
    for (i = 0; i < byer.length; i++) if (norm(byer[i].by).indexOf(q) === 0) return byer[i];
    for (i = 0; i < byer.length; i++) if (norm(byer[i].by).indexOf(q) > -1) return byer[i];
    return null;
  }
  function vis() {
    var q = felt.value.trim();
    if (!q) return;
    var b = finn(q);
    if (!b) {
      svar.innerHTML = '<div class="report bysok-kort"><p>Vi har ikke tallene for <strong>' + esc(q) +
        '</strong> klare – men vi henter dem gratis for deg.</p>' + knapper(q) + "</div>";
      return;
    }
    var rader = '<div><dt>Rørlegger ' + esc(b.by) + '</dt><dd>' + esc(b.rorlegger) + ' søk i måneden</dd></div>';
    if (b.baderom) rader += '<div><dt>Baderom ' + esc(b.by) + '</dt><dd>' + esc(b.baderom) + ' søk i måneden</dd></div>';
    if (b.klikkpris) rader += '<div><dt>Klikkpris, toppen av siden</dt><dd>' + esc(b.klikkpris) + ' kr</dd></div>';
    svar.innerHTML = '<div class="report bysok-kort"><div class="report-top"><span class="eyebrow">Søk i ' + esc(b.by) +
      '</span><span class="report-tag">Tall fra Google</span></div><dl>' + rader + '</dl><p class="report-date">Kilde: Google Ads Søkeordplanlegger, siste 12 mnd.</p>' +
      knapper(b.by) + "</div>";
  }

  fetch("/data/bysok.json").then(function (r) { return r.json(); }).then(function (d) {
    byer = d.byer || [];
    liste.innerHTML = byer.map(function (b) { return '<option value="' + esc(b.by) + '">'; }).join("");
    sek.hidden = false;
    knapp.addEventListener("click", vis);
    felt.addEventListener("keydown", function (e) { if (e.key === "Enter") vis(); });
    var fra = new URLSearchParams(location.search).get("by");   // hifivestudio.no/?by=Bergen (lenke i e-post)
    if (fra) { felt.value = fra; vis(); }
  }).catch(function () { /* data utilgjengelig → seksjonen forblir skjult */ });
})();
