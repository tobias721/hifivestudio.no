// N2/N4 27.10: søk på byen i helsesjekk-kortet i heroen. Bare ekte tall fra /data/bysok.json
// (Google Ads Søkeordplanlegger). Ingen rammeverk, ingen sporing, ikke noe skjema.
// Uten JS står kortet som eksempel og søkefeltet er skjult.
(function () {
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
           '">Få gratis helsesjekk for ' + esc(by) + '</a></div>';
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
    function fmt(n) { return String(n).replace(/\B(?=(\d{3})+(?!\d))/g, " "); }
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
      return;
    }
    tag.textContent = "Tall fra Google"; dato.textContent = "Siste 12 måneder";
    var rad = function (dt, v) { return '<div><dt>' + dt + '</dt><dd class="tell" data-v="' + esc(v) + '">' + esc(v) + '</dd></div>'; };
    innhold.innerHTML = '<dl>' + rad("Søk i måneden, «rørlegger " + esc(by.toLowerCase()) + "»", b.rorlegger) +
      (b.baderom ? rad("Baderom " + esc(by), b.baderom) : "") +
      (b.klikkpris ? rad("Klikkpris, toppen av siden", b.klikkpris + " kr") : "") +
      '</dl><p class="report-kilde">Kilde: Google Ads Søkeordplanlegger</p>' +
      knapp_html("Hvor står ditt firma? Få gratis helsesjekk for " + esc(by) + ".", by);
    Array.prototype.forEach.call(innhold.querySelectorAll(".tell"), tell);
  }

  fetch("/data/bysok.json").then(function (r) { return r.json(); }).then(function (d) {
    byer = d.byer || [];
    liste.innerHTML = byer.map(function (b) { return '<option value="' + esc(b.by) + '">'; }).join("");
    sok.hidden = false;
    knapp.addEventListener("click", vis);
    felt.addEventListener("keydown", function (e) { if (e.key === "Enter") vis(); });
    var fra = new URLSearchParams(location.search).get("by");   // hifivestudio.no/?by=Hamar (lenke i e-post)
    if (fra) { felt.value = fra; vis(); }
  }).catch(function () { /* data utilgjengelig → kortet står som eksempel */ });
})();
