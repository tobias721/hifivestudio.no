// N5 27.10: liv på siden uten rammeverk, sporing eller eksterne skript. Alt virker også uten JS:
// kort åpnes/lukkes med <details>, innhold er synlig, bunnlinja på mobil vises bare ikke.
(function () {
  var rot = document.documentElement, rolig = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  rot.classList.add("js");

  // 1) Rolig innsving når man scroller (ikke heroen). Kort i samme rutenett får 40 ms forskyvning hver.
  var deler = document.querySelectorAll("[data-reveal]");
  if (rolig || !("IntersectionObserver" in window)) {
    Array.prototype.forEach.call(deler, function (el) { el.classList.add("in"); });
  } else {
    var obs = new IntersectionObserver(function (inn) {
      inn.forEach(function (e) {
        if (!e.isIntersecting) return;
        var el = e.target, søsken = el.parentNode ? Array.prototype.filter.call(el.parentNode.children, function (c) { return c.hasAttribute("data-reveal"); }) : [];
        el.style.setProperty("--d", Math.min(søsken.indexOf(el), 6) * 40 + "ms");
        el.classList.add("in");
        obs.unobserve(el);
      });
    }, { threshold: 0.15 });
    Array.prototype.forEach.call(deler, function (el) { obs.observe(el); });
  }

  // 2) Kort som kan åpnes: animert lukking (åpning animeres av CSS når [open] settes)
  Array.prototype.forEach.call(document.querySelectorAll(".xcard summary, .hcard summary, .faq summary"), function (sum) {
    var det = sum.parentNode, kropp = det.querySelector(".xcard-body");
    if (!kropp) return;
    sum.addEventListener("click", function (ev) {
      if (!det.open || rolig) return;            // åpning og redusert bevegelse: la nettleseren gjøre det
      ev.preventDefault();
      det.classList.add("lukker");
      var ferdig = function () { det.classList.remove("lukker"); det.removeAttribute("open"); kropp.removeEventListener("transitionend", ferdig); };
      kropp.addEventListener("transitionend", ferdig);
      setTimeout(ferdig, 400);                   // sikring hvis transitionend ikke kommer
    });
  });

  // 3) ?open=<slug> åpner ett kort (lenke fra svar til interesserte)
  var åpne = new URLSearchParams(location.search).get("open");
  if (åpne) {
    var kort = document.getElementById(åpne);
    if (kort && kort.tagName === "DETAILS") { kort.open = true; setTimeout(function () { kort.scrollIntoView({ block: "center" }); }, 50); }
  }

  // 4) Prissiden: «Hva er med» står åpent på desktop, foldes sammen på mobil
  if (matchMedia("(max-width:760px)").matches)
    Array.prototype.forEach.call(document.querySelectorAll(".pkg-more"), function (d) { d.removeAttribute("open"); });

  // 5) Nav-pillen får bakgrunn etter 40 px scroll
  var nav = document.getElementById("nav");
  var oppdater = function () { if (nav) nav.classList.toggle("scrolled", window.scrollY > 40); };
  window.addEventListener("scroll", oppdater, { passive: true });
  oppdater();

  // 6) Mobil: fast bunnlinje når toppen av siden er ute av bildet, skjult igjen når bunnteksten vises
  var sticky = document.getElementById("sticky"), topp = document.querySelector(".hero, .page-head"), fot = document.querySelector("footer");
  if (sticky && topp && fot && "IntersectionObserver" in window) {
    var toppSynlig = true, fotSynlig = false;
    var sett = function () { sticky.classList.toggle("vis", !toppSynlig && !fotSynlig); };
    new IntersectionObserver(function (e) { toppSynlig = e[0].isIntersecting; sett(); }).observe(topp);
    new IntersectionObserver(function (e) { fotSynlig = e[0].isIntersecting; sett(); }).observe(fot);
  }
})();
