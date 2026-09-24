#!/usr/bin/env python3
"""Generate the static GIS Transporturi pages."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PAGES = json.loads(Path("/tmp/gis-pages.json").read_text())

NAV = """
<a href="/">Acasă</a>
<a href="/despre-noi/">Despre noi</a>
<div class="nav-drop">
  <a href="/servicii/">Servicii</a>
  <menu>
    <li><a href="/servicii/transport-autoturisme/">Transport autoturisme</a></li>
    <li><a href="/servicii/transport-marfuri/">Transport mărfuri</a></li>
    <li><a href="/servicii/intermediere-transport-marfuri-si-autoturisme/">Intermediere</a></li>
    <li><a href="/servicii/depozitare-si-logistica/">Depozitare și logistică</a></li>
  </menu>
</div>
<a href="/comanda-oferta/">Ofertă</a>
<a href="/contact/">Contact</a>
<a class="btn" href="/comanda-oferta/">Cere o ofertă</a>
"""

FOOT = """
<footer class="site-footer">
  <div class="wrap foot-grid">
    <div>
      <a class="logo-pill" href="/"><img src="/assets/img/logo.png" alt="GIS Transporturi"></a>
      <p>Grup Impex S.R.L. Transport intern și internațional de autoturisme și mărfuri, din Sibiu.</p>
    </div>
    <div>
      <h3>Servicii</h3>
      <ul>
        <li><a href="/servicii/transport-autoturisme/">Transport autoturisme</a></li>
        <li><a href="/servicii/transport-marfuri/">Transport mărfuri</a></li>
        <li><a href="/servicii/intermediere-transport-marfuri-si-autoturisme/">Intermediere</a></li>
        <li><a href="/servicii/depozitare-si-logistica/">Depozitare și logistică</a></li>
      </ul>
    </div>
    <div>
      <h3>Contact</h3>
      <ul>
        <li>Luni – Vineri, 08:00 – 16:00</li>
        <li><a href="tel:+40740099080">+40 740 099 080</a></li>
        <li><a href="tel:+40741035347">+40 741 035 347</a></li>
        <li><a href="tel:+40754048794">+40 754 048 794</a></li>
        <li><a href="mailto:office@gistransporturi.ro">office@gistransporturi.ro</a></li>
        <li>Sibiu, Str. Anul 1848 nr. 17</li>
      </ul>
    </div>
    <div>
      <h3>Social</h3>
      <ul>
        <li><a href="https://www.facebook.com/GIStransporturi/" target="_blank" rel="noreferrer">Facebook</a></li>
        <li><a href="https://www.instagram.com/grupimpexsrl/" target="_blank" rel="noreferrer">Instagram</a></li>
      </ul>
    </div>
  </div>
  <div class="wrap legal-row">
    <a href="/gdpr/">GDPR</a>
    <a href="/declaratie-privind-datele-cu-caracter-personal/">Date personale</a>
    <a href="/politica-privind-cookie-urile-ue/">Cookie-uri</a>
    <a href="/termeni-si-conditii/">Termeni</a>
    <a href="/politica-de-confidentialitate/">Confidențialitate</a>
    <span>© Grup Impex S.R.L.</span>
  </div>
</footer>
<a class="wa" href="https://wa.me/40740099080" aria-label="WhatsApp" target="_blank" rel="noreferrer">
  <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20.5 3.5A11 11 0 0 0 2.1 17.2L1 23l6-1.6A11 11 0 0 0 20.5 3.5zm-8.5 17a9.1 9.1 0 0 1-4.6-1.3l-.3-.2-3.6.9.9-3.5-.2-.3A9.1 9.1 0 1 1 12 20.5zm5-6.8c-.3-.1-1.6-.8-1.8-.9s-.4-.1-.6.1-.7.9-.8 1-.3.2-.6.1a7.4 7.4 0 0 1-2.2-1.4 8.2 8.2 0 0 1-1.5-1.9c-.2-.3 0-.4.1-.6l.4-.5.2-.3a.5.5 0 0 0 0-.5c0-.1-.6-1.4-.8-1.9s-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 2.9 2.9 0 0 0-.9 2.2 5 5 0 0 0 1.1 2.7 11.4 11.4 0 0 0 4.4 3.9 14 14 0 0 0 1.5.6 3.6 3.6 0 0 0 1.6.1 2.7 2.7 0 0 0 1.8-1.2 2.2 2.2 0 0 0 .2-1.2c-.1-.1-.3-.2-.6-.3z"/></svg>
</a>
"""


def shell(title, description, path, body, active):
    nav = NAV
    for href, label in [
        ("/", "Acasă"),
        ("/despre-noi/", "Despre noi"),
        ("/servicii/", "Servicii"),
        ("/comanda-oferta/", "Ofertă"),
        ("/contact/", "Contact"),
    ]:
        if path == href or (href != "/" and path.startswith(href)):
            nav = nav.replace(f'href="{href}"', f'href="{href}" class="active"', 1)
    return f"""<!DOCTYPE html>
<html lang="ro">
<head>
  <meta charset="utf-8">
  <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
  <meta http-equiv="Pragma" content="no-cache">
  <meta http-equiv="Expires" content="0">
  <script>
  (function () {
    var build = "20260924e";
    fetch("/version.txt", { cache: "no-store" }).then(function (r) {
      return r.ok ? r.text() : "";
    }).then(function (text) {
      var remote = (text || "").trim();
      if (!remote || remote === build || location.search.indexOf("v=" + remote) !== -1) return;
      location.replace(location.pathname + location.search + (location.search ? "&" : "?") + "v=" + remote + location.hash);
    }).catch(function () {});
  })();
  </script>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <link rel="icon" href="/assets/img/favicon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&family=Syne:wght@600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/assets/css/styles.css?v=20260924e">
</head>
<body class="{'home' if path == '/' else ''}">
<header class="site-header">
  <div class="header-inner">
    <a class="logo" href="/"><img src="/assets/img/logo.png" alt="GIS Transporturi"></a>
    <button class="menu-toggle" aria-label="Meniu" aria-expanded="false"><span></span></button>
    <nav class="nav">{nav}</nav>
  </div>
</header>
{body}
{FOOT}
<script src="/assets/js/main.js?v=20260924e"></script>
</body>
</html>
"""


def write(rel, html):
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")
    print(rel)


def form(extra=""):
    return f"""
<form class="form" data-service-form>
  <p class="form-ok">Cererea a fost trimisă. Revenim în cel mai scurt timp.</p>
  <input class="hp" type="text" name="company" tabindex="-1" autocomplete="off">
  <div class="row">
    <label>Nume<input name="nume" required></label>
    <label>Prenume<input name="prenume" required></label>
  </div>
  <div class="row">
    <label>Telefon<input name="telefon" required></label>
    <label>Email<input type="email" name="email"></label>
  </div>
  <label>Nume societate<input name="societate"></label>
  <label>Cu ce servicii vă putem ajuta?
    <select name="serviciu" required>
      <option value="">Alege</option>
      <option>Transport mărfuri</option>
      <option>Transport autoturisme</option>
      <option>Intermediere transport mărfuri și autoturisme</option>
      <option>Depozitare logistica</option>
    </select>
  </label>
  <div class="row">
    <label>Locația încărcării<input name="incarcare"></label>
    <label>Locația descărcării<input name="descarcare"></label>
  </div>
  <div data-for="auto" hidden>
    <div class="row">
      <label>Modelul autoturismului<input name="model"></label>
      <label>Număr de autoturisme<input name="numar_auto"></label>
    </div>
    <label>Starea autoturismului
      <select name="stare"><option value="">Alege</option><option>funcțional</option><option>nefuncțional</option></select>
    </label>
  </div>
  <div data-for="marfa" hidden>
    <div class="row">
      <label>Număr de paleți<input name="paleti"></label>
      <label>Volumul paleților<input name="volum"></label>
    </div>
    <label>Greutatea paleților<input name="greutate"></label>
  </div>
  {extra}
  <label>Mesaj<textarea name="mesaj" required></textarea></label>
  <label class="checkline"><input type="checkbox" required> Prin trimiterea acestui formular ne dați consimțământul pentru folosirea datelor furnizate pentru a vă contacta. Datele nu vor fi folosite în alte scopuri. <a href="/declaratie-privind-datele-cu-caracter-personal/">Informare privind datele cu caracter personal</a>.</label>
  <p class="note">* câmpurile pentru autoturisme și paleți se completează doar pentru serviciul respectiv. Toate câmpurile marcate sunt obligatorii.</p>
  <button class="btn" type="submit">Trimite cererea</button>
</form>
"""


HOME = """
<section class="hero">
  <div class="hero-media"><img src="/assets/img/fleet-sun.jpg" alt="Platformă GIS Transporturi încărcată cu autoturisme"></div>
  <svg class="route" viewBox="0 0 420 180" aria-hidden="true"><path d="M10 140 C 80 140, 90 40, 170 48 S 260 150, 340 70 410 30 410 30"/></svg>
  <div class="hero-copy">
    <p class="eyebrow reveal">Grup Impex · Sibiu · din 2001</p>
    <h1 class="reveal d2">Servicii de <span>transport</span></h1>
    <ul class="checks reveal d3">
      <li>Simplu și rapid</li>
      <li>Costuri de transport corecte</li>
      <li>Asigurat CMR</li>
      <li>În toată țara, dar și pe teritoriul Uniunii Europene</li>
    </ul>
    <div class="hero-actions reveal d4">
      <a class="btn" href="/comanda-oferta/">Cere o ofertă</a>
      <a class="btn ghost" href="tel:+40740099080" style="color:white;box-shadow:inset 0 0 0 1.5px rgba(255,255,255,.4)">+40 740 099 080</a>
      <a class="btn ghost" href="tel:+40741035347" style="color:white;box-shadow:inset 0 0 0 1.5px rgba(255,255,255,.4)">+40 741 035 347</a>
      <a class="btn ghost" href="tel:+40754048794" style="color:white;box-shadow:inset 0 0 0 1.5px rgba(255,255,255,.4)">+40 754 048 794</a>
    </div>
  </div>
</section>
<div class="marquee" aria-hidden="true"><div class="marquee-track">
  <span>România</span><span>Ungaria</span><span>Austria</span><span>Italia</span><span>Franța</span><span>Germania</span><span>Belgia</span><span>Olanda</span><span>Danemarca</span><span>Cehia</span><span>Slovacia</span><span>Slovenia</span><span>Polonia</span><span>Lituania</span>
  <span>România</span><span>Ungaria</span><span>Austria</span><span>Italia</span><span>Franța</span><span>Germania</span><span>Belgia</span><span>Olanda</span><span>Danemarca</span><span>Cehia</span><span>Slovacia</span><span>Slovenia</span><span>Polonia</span><span>Lituania</span>
</div></div>
<section class="section">
  <div class="wrap">
    <p class="eyebrow">Ce facem</p>
    <h2>Patru servicii, același standard.</h2>
    <div class="services">
      <details class="service inview">
        <summary>
          <img src="/assets/img/fleet-snow.jpg" alt="Transport autoturisme pe platformă">
          <div><h3>Transport autoturisme</h3><p>De la o singură mașină până la loturi de 8–10 unități, din și spre Europa.</p></div>
          <span class="arrow">→</span>
        </summary>
        <div class="service-more">
          <p>Oferim servicii de transport mașini din și înspre Europa. Transportul pe platformă se face în siguranță, cu structuri profesionale pentru până la 10 autoturisme odată.</p>
          <p>Putem onora comenzi pentru o singură mașină, dar și loturi complete de 8–10 unități, de oriunde din Europa.</p>
          <a class="btn" href="/comanda-oferta/">Cere o ofertă</a>
        </div>
      </details>
      <details class="service inview">
        <summary>
          <img src="/assets/img/pallet.jpg" alt="Transport mărfuri paletate">
          <div><h3>Transport mărfuri</h3><p>Marfă asigurată, flotă urmărită GPS, șoferi profesioniști.</p></div>
          <span class="arrow">→</span>
        </summary>
        <div class="service-more">
          <p>Oferim soluții pentru afacerea dvs. cu o flotă modernă, întreținere tehnică periodică, șoferi profesioniști, urmărire prin satelit GPS și alerte de securitate către echipa noastră.</p>
          <p>Toate mărfurile transportate sunt asigurate.</p>
          <a class="btn" href="/comanda-oferta/">Cere o ofertă</a>
        </div>
      </details>
      <details class="service inview">
        <summary>
          <img src="/assets/img/courier.jpg" alt="Intermediere transport">
          <div><h3>Intermediere</h3><p>Cea mai potrivită soluție prin rețeaua de parteneri, cu asigurare.</p></div>
          <span class="arrow">→</span>
        </summary>
        <div class="service-more">
          <p>Oferim intermediere pentru transportul de mărfuri și de autoturisme. Prin rețeaua de parteneri găsim varianta sigură, rapidă și potrivită ca preț.</p>
          <p>Orice marfă sau autovehicul intermediat este asigurat prin polița societății pentru această activitate.</p>
          <a class="btn" href="/comanda-oferta/">Cere o ofertă</a>
        </div>
      </details>
      <details class="service inview">
        <summary>
          <img src="/assets/img/yard.jpg" alt="Depozitare autoturisme">
          <div><h3>Depozitare și logistică</h3><p>Sediu în centrul țării, pentru marfă și autoturisme între transporturi.</p></div>
          <span class="arrow">→</span>
        </summary>
        <div class="service-more">
          <p>Sediul din Sibiu, în centrul țării, poate găzdui atât marfa, cât și autoturismul, până la următorul transport.</p>
          <p>Pentru autoturisme, pe perioada depozitării oferim verificare și întreținere, ca să păstrăm tensiunea optimă a acumulatorului.</p>
          <a class="btn" href="/comanda-oferta/">Cere o ofertă</a>
        </div>
      </details>
    </div>
  </div>
</section>
<section class="section" style="padding-top:0">
  <div class="wrap split">
    <div class="frame inview">
      <img src="/assets/img/fleet-12.jpg" alt="Camion GIS pe traseu">
      <div class="chip"><strong>110</strong> oameni în echipă</div>
    </div>
    <div class="inview">
      <p class="eyebrow">Flotă</p>
      <h2>Transportă rapid și în siguranță</h2>
      <p>Grup Impex S.R.L. asigură un transport rapid și în siguranță, punând la dispoziție o gamă largă de autoutilitare și autocamioane.</p>
      <p>Transportăm autovehicule și mărfuri din afara țării în țară, cât și pe teritoriul Uniunii Europene, sigur, rapid și eficient.</p>
      <a class="btn purple" href="/despre-noi/">Mai multe informații</a>
    </div>
  </div>
</section>
<section class="section" style="padding-top:0">
  <div class="wrap">
    <div class="stats">
      <div class="stat inview"><b data-since="2001-08">0</b><span>ani de activitate în transporturi</span></div>
      <div class="stat inview"><b data-count="110">0</b><span>angajați</span></div>
      <div class="stat inview"><b data-count="14">0</b><span>țări pe rute regulate</span></div>
      <div class="stat inview"><b data-count="10">0</b><span>autoturisme pe platformă</span></div>
    </div>
  </div>
</section>
<section class="section" style="padding-top:0">
  <div class="wrap">
    <p class="eyebrow">De ce GIS</p>
    <h2>Același drum, mai liniștit.</h2>
    <div class="reasons">
      <article class="reason inview"><em>Oriunde în Europa</em><p>Curse regulate și curse interne, cu frecvență ridicată.</p></article>
      <article class="reason inview"><em>Preț corect</em><p>Costul ține de rută, dimensiune și greutate. Îl afli dintr-o cerere de ofertă.</p></article>
      <article class="reason inview"><em>Transport în siguranță</em><p>CMR, asigurare și urmărire GPS pe camioane și autoutilitare.</p></article>
      <article class="reason inview"><em>Transport rapid</em><p>Centru de logistică în legătură directă cu colegii de pe traseu.</p></article>
      <article class="reason inview"><em>Depozitare</em><p>Marfă și autoturisme găzduite în Sibiu între curse, cu verificare a acumulatorului.</p></article>
      <article class="reason inview"><em>Parteneri stabili</em><p>Colaborări lungi, prin vremuri ușoare și prin vremuri mai grele.</p></article>
    </div>
  </div>
</section>
<section class="section" style="padding-top:0">
  <div class="wrap">
    <p class="eyebrow">Din flotă</p>
    <h2>Pe drum, în fiecare anotimp.</h2>
    <div class="gallery">
      <img src="/assets/img/fleet-sun.jpg" alt="Platformă încărcată, vară">
      <img src="/assets/img/fleet-snow.jpg" alt="Platformă pe zăpadă">
      <img src="/assets/img/fleet-15.jpg" alt="Transport GIS">
      <img src="/assets/img/fleet-21.jpg" alt="Transport GIS">
      <img src="/assets/img/fleet-24.jpg" alt="Transport GIS">
      <img src="/assets/img/fleet-30.jpg" alt="Transport GIS">
      <img src="/assets/img/fleet-05.jpg" alt="Transport GIS">
    </div>
  </div>
</section>
<section class="section" style="padding-top:0">
  <div class="wrap">
    <p class="eyebrow">Recenzii</p>
    <h2>Poți evalua experiența cu Grup Impex.</h2>
    <div class="quotes">
      <blockquote class="quote inview"><p>„Profesionalism, promptitudine, de încredere! Recomand!”</p><cite>Iulia Vintila</cite></blockquote>
      <blockquote class="quote inview"><p>„Profesional.”</p><cite>Muntean Ciprian</cite></blockquote>
      <blockquote class="quote inview"><p>„Seriozitate și profesionalism!”</p><cite>Chis Ioan-Cosmin</cite></blockquote>
    </div>
  </div>
</section>
<section class="section" style="padding-top:0">
  <div class="wrap split">
    <div>
      <p class="eyebrow">Întrebări frecvente</p>
      <h2>Înainte de cursă.</h2>
      <div class="faq">
        <details open><summary>Cum pot să transport o mașină din UE către România?</summary><p>Se face o cerere cu ajutorul formularului de pe pagina Comandă/Ofertă și noi îți vom răspunde în cel mai scurt timp.</p></details>
        <details><summary>Cât costă să transport o mașină?</summary><p>Costul unui transport diferă în funcție de locul de ridicare și locul de livrare, dar și în funcție de dimensiunile și greutatea acesteia. Pentru a afla, completează o cerere de ofertă.</p></details>
        <details><summary>Cum pot să îmi transport o mașină în țară?</summary><p>Dacă ai o mașină pe care vrei să o transporți dintr-o locație în alta pe teritoriul țării, te putem ajuta cu autocamioanele noastre sau ale partenerilor noștri.</p></details>
        <details><summary>Am marfă, cu cine pot să o transport?</summary><p>În funcție de nevoile tale, marfa va fi transportată cât mai rapid, atât paletată, cât și ca un colet singular.</p></details>
      </div>
    </div>
    <div class="inview">
      <p class="eyebrow">Contactează-ne</p>
      <h2>Luni – vineri, 8–16.</h2>
      <p><a href="tel:+40740099080">+40 740 099 080</a><br><a href="tel:+40741035347">+40 741 035 347</a><br><a href="tel:+40754048794">+40 754 048 794</a><br><a href="mailto:office@gistransporturi.ro">office@gistransporturi.ro</a><br>Sibiu, Str. Anul 1848 nr. 17, județul Sibiu</p>
      <a class="btn" href="/contact/">Scrie-ne</a>
    </div>
  </div>
</section>
"""

ABOUT = """
<section class="page-hero"><div class="wrap">
  <p class="eyebrow">Despre noi</p>
  <h1>Din 2001, pe același drum cu partenerii.</h1>
</div></section>
<section class="section" style="padding-top:10px">
  <div class="wrap split">
    <div class="frame"><img src="/assets/img/about.jpg" alt="Echipa GIS Transporturi"><div class="chip"><strong>2001</strong> august, începutul</div></div>
    <div class="prose">
      <p>Societatea s-a înființat în august 2001, fiind axată pe transportul de mărfuri generale pe teritoriul național. În scurt timp, datorită cererii, societatea s-a dezvoltat și înspre transportul internațional de mărfuri, dar și în livrarea de colete door-to-door. Pe parcursul desfășurării activității, compania noastră a avut parteneri stabili. În activitatea companiei se atribuie întotdeauna o atenție și importanță deosebită partenerilor noștri, colaborarea fiind de lungă durată și bazându-se pe relații comerciale clare.</p>
      <p>Din luna noiembrie 2018 ne-am hotărât să începem activitatea de transport autovehicule. Dezvoltarea acestei ramuri se bazează pe desfășurarea activității la un standard cât mai înalt, respectând proceduri, condiții, termene și legislație în vigoare.</p>
    </div>
  </div>
</section>
<section class="section" style="padding-top:0">
  <div class="wrap split">
    <div class="prose">
      <p>Echipa noastră este formată din 110 angajați, fiecare fiind instruit să respecte procedurile impuse pe ramura în care își desfășoară activitatea zilnică. Centrul de logistică are rolul de a rezolva cât mai rapid și eficient cerințele clienților. Suntem tot timpul în strânsă legătură cu colegii de pe traseu — indiferent că aceștia livrează sau transportă mașini ori colete — pentru a-i ajuta în caz de necesitate.</p>
      <p>În activitatea noastră tot timpul am încercat să ne îndeplinim misiunea cât mai aproape de excelență. În colaborările noastre tot timpul am căutat și ales un partener serios și de încredere, astfel acesta putându-se baza pe noi, dar și noi pe acesta totodată. Am fost și suntem adepți ai colaborărilor stabile și de lungă durată, ca și parteneri trecând atât prin vremuri ușoare, dar și prin vremuri mai grele împreună.</p>
      <a class="btn" href="/comanda-oferta/">Cere o ofertă</a>
    </div>
    <div class="frame"><img src="/assets/img/inginer.jpg" alt="Coordonare logistică"></div>
  </div>
</section>
"""

SERVICES = """
<section class="page-hero"><div class="wrap">
  <p class="eyebrow">Servicii</p>
  <h1>Servicii oferite</h1>
  <p class="lead" style="max-width:640px">Ne angajăm să vă oferim soluții flexibile și suport profesionist pe întregul flux al transporturilor mărfurilor dumneavoastră.</p>
</div></section>
<section class="section" style="padding-top:0"><div class="wrap services">
  <details class="service">
    <summary><img src="/assets/img/fleet-snow.jpg" alt=""><div><h3>Transport autoturisme</h3><p>Platforme pentru 1 până la 10 autoturisme, intern și în Europa.</p></div><span class="arrow">→</span></summary>
    <div class="service-more"><p>Transport pe platformă, de la o singură mașină până la loturi de 8–10 unități, din și spre Europa.</p><a class="btn" href="/comanda-oferta/">Cere o ofertă</a></div>
  </details>
  <details class="service">
    <summary><img src="/assets/img/pallet.jpg" alt=""><div><h3>Transport mărfuri generale</h3><p>Flotă modernă, întreținere periodică, urmărire prin satelit.</p></div><span class="arrow">→</span></summary>
    <div class="service-more"><p>Marfă asigurată, șoferi profesioniști și urmărire GPS pe tot parcursul cursei.</p><a class="btn" href="/comanda-oferta/">Cere o ofertă</a></div>
  </details>
  <details class="service">
    <summary><img src="/assets/img/courier.jpg" alt=""><div><h3>Intermediere transport mărfuri și autoturisme</h3><p>Rețeaua de parteneri, cu asigurarea societății.</p></div><span class="arrow">→</span></summary>
    <div class="service-more"><p>Găsim soluția sigură, rapidă și potrivită ca preț. Transportul intermediat este asigurat.</p><a class="btn" href="/comanda-oferta/">Cere o ofertă</a></div>
  </details>
  <details class="service">
    <summary><img src="/assets/img/yard.jpg" alt=""><div><h3>Depozitare și logistică</h3><p>Autoturisme și mărfuri, în Sibiu, între curse.</p></div><span class="arrow">→</span></summary>
    <div class="service-more"><p>Găzduim marfa și autoturismul în Sibiu. Pentru mașini, verificăm și acumulatorul pe perioada depozitării.</p><a class="btn" href="/comanda-oferta/">Cere o ofertă</a></div>
  </details>
</div></section>
<section class="section" style="padding-top:0"><div class="wrap split">
  <div class="prose">
    <p>În acest scop, organizăm atât curse regulate din și către Europa (Ungaria, Austria, Italia, Franța, Germania, Belgia, Olanda, Danemarca, Cehia, Slovacia, Slovenia, Polonia, Lituania etc.), cât și curse interne, cu frecvență ridicată.</p>
    <p>Toate camioanele și autoutilitarele noastre sunt echipate cu aparate GPS pentru tracking, astfel pe tot parcursul transportului putem afla locația autocamioanelor sau autoutilitarelor.</p>
    <a class="btn" href="/comanda-oferta/">Vezi o ofertă</a>
  </div>
  <div class="frame"><img src="/assets/img/fleet-21.jpg" alt="Camion pe cursă"></div>
</div></section>
"""

AUTO = """
<section class="page-hero"><div class="wrap">
  <p class="eyebrow">Servicii</p>
  <h1>Transport autoturisme</h1>
</div></section>
<section class="section" style="padding-top:0"><div class="wrap split">
  <div class="frame"><img src="/assets/img/fleet-sun.jpg" alt="Platformă auto GIS"></div>
  <div class="prose">
    <p>Oferim servicii de transport mașini din și înspre Europa.</p>
    <p>Serviciile de transport mașini pe platformă se desfășoară în deplină siguranță datorită structurilor profesionale pentru transport a până la 10 autoturisme odată.</p>
    <p>Putem onora comenzi pentru o singură unitate (1 mașină), dar și loturi complete de 8–10 unități, de oriunde din Europa.</p>
  </div>
</div></section>
<section class="section" style="padding-top:0"><div class="wrap two-col"><div><h2>Formular de cerere ofertă</h2><p>Spune-ne de unde pleacă mașina și unde trebuie să ajungă.</p></div>""" + form() + """</div></section>
"""

FREIGHT = """
<section class="page-hero"><div class="wrap">
  <p class="eyebrow">Servicii</p>
  <h1>Transport mărfuri</h1>
</div></section>
<section class="section" style="padding-top:0"><div class="wrap split">
  <div class="prose">
    <p>Fiind o companie de transport modernă și dinamică, cu personal calificat, oferim cele mai bune servicii și soluții pentru afacerea dvs. Ne îndeplinim promisiunile cu ajutorul unei flote moderne, cu întreținere tehnică periodică (având parteneriate cu reprezentanțe de marcă); avem șoferi profesioniști, urmărire prin satelit GPS și alerte de securitate către echipa noastră, toate acestea concepute pentru a garanta calitatea transportului dumneavoastră.</p>
    <p>Toate mărfurile transportate sunt asigurate.</p>
  </div>
  <div class="frame"><img src="/assets/img/pallet.jpg" alt="Marfă paletată"></div>
</div></section>
<section class="section" style="padding-top:0"><div class="wrap two-col"><div><h2>Formular de cerere ofertă</h2></div>""" + form() + """</div></section>
"""

BROKER = """
<section class="page-hero"><div class="wrap">
  <p class="eyebrow">Servicii</p>
  <h1>Intermediere transport mărfuri și autoturisme</h1>
</div></section>
<section class="section" style="padding-top:0"><div class="wrap split">
  <div class="frame"><img src="/assets/img/fleet-15.jpg" alt="Transport intermediat"></div>
  <div class="prose">
    <p>Oferim servicii de intermediere pentru transportul de mărfuri, cât și pentru transportul de autoturisme.</p>
    <p>Putem găsi cea mai bună soluție de transport pentru dumneavoastră folosind rețeaua partenerilor noștri, astfel vă putem oferi cel mai sigur transport, cea mai rapidă soluție și cea mai bună alegere privind prețul.</p>
    <p>De asemenea, orice marfă sau autovehicul intermediat este asigurat prin polița deținută de societatea noastră pentru această activitate.</p>
  </div>
</div></section>
<section class="section" style="padding-top:0"><div class="wrap two-col"><div><h2>Formular de cerere ofertă</h2></div>""" + form() + """</div></section>
"""

STORE = """
<section class="page-hero"><div class="wrap">
  <p class="eyebrow">Servicii</p>
  <h1>Depozitare și logistică</h1>
</div></section>
<section class="section" style="padding-top:0"><div class="wrap split">
  <div class="prose">
    <p>Sediul nostru se află în municipiul Sibiu. Orașul este un important centru cultural și economic cu un remarcabil potențial de dezvoltare economică din sudul Transilvaniei, aflat în centrul României (coordonate 45°47′45″N 24°9′8″E).</p>
    <p>Cu o locație aflată în centrul țării vă putem oferi cea mai bună soluție de logistică și depozitare. Sediul nostru, având o suprafață considerabilă, este disponibil să vă găzduiască atât marfa cât și autoturismul dumneavoastră, pentru a putea fi pregătite pentru următorul transport.</p>
    <p>În ceea ce privește autoturismele, pe perioada depozitării putem oferi servicii de verificare și întreținere pentru a asigura tensiunea optimă a acumulatorului.</p>
  </div>
  <div class="frame"><img src="/assets/img/yard.jpg" alt="Autoturisme depozitate"></div>
</div></section>
<section class="section" style="padding-top:0"><div class="wrap two-col"><div><h2>Formular de cerere ofertă</h2></div>""" + form() + """</div></section>
"""

OFFER = """
<section class="page-hero"><div class="wrap">
  <p class="eyebrow">Comandă</p>
  <h1>Cere o ofertă</h1>
  <p>Răspundem în cel mai scurt timp, luni–vineri, 08:00–16:00.</p>
</div></section>
<section class="section" style="padding-top:0"><div class="wrap" style="max-width:760px">""" + form() + """</div></section>
"""

CONTACT = """
<section class="page-hero"><div class="wrap">
  <p class="eyebrow">Contact</p>
  <h1>Suntem în Sibiu.</h1>
</div></section>
<section class="section" style="padding-top:0"><div class="wrap contact-grid">
  <div class="contact-card">
    <p class="eyebrow" style="color:#9fdfff">Date contact</p>
    <h2>GRUP IMPEX SRL</h2>
    <p>Sibiu, Str. Anul 1848 nr. 17, județul Sibiu</p>
    <p><a href="tel:+40740099080">+40 740 099 080</a><br><a href="tel:+40741035347">+40 741 035 347</a><br><a href="tel:+40754048794">+40 754 048 794</a></p>
    <p><a href="mailto:office@gistransporturi.ro">office@gistransporturi.ro</a></p>
    <p>Luni – Vineri, 08:00 – 16:00</p>
  </div>
  """ + form() + """
</div>
<div class="wrap" style="margin-top:28px">
  <iframe class="map" title="Sediu GIS Transporturi" src="https://maps.google.com/maps?q=Strada%20Anul%201848%2017%20Sibiu&z=15&output=embed" loading="lazy"></iframe>
</div>
</section>
"""


def legal_html(slug):
    raw = next(p for p in PAGES if p["slug"] == slug)["content"]["rendered"]
    raw = re.sub(r"<script[\s\S]*?</script>", "", raw, flags=re.I)
    raw = re.sub(r"<style[\s\S]*?</style>", "", raw, flags=re.I)
    raw = re.sub(r"</?div[^>]*>", "", raw, flags=re.I)
    raw = re.sub(r"</?span[^>]*>", "", raw, flags=re.I)
    raw = re.sub(r"\sclass=\"[^\"]*\"", "", raw)
    raw = re.sub(r"\sstyle=\"[^\"]*\"", "", raw)
    raw = re.sub(r"\sid=\"[^\"]*\"", "", raw)
    return raw.strip()


def legal_page(title, path, inner):
    body = f"""
<section class="page-hero"><div class="wrap"><h1>{title}</h1></div></section>
<section class="section" style="padding-top:0"><div class="wrap legal">{inner}</div></section>
"""
    return shell(f"{title} - GIS Transporturi", title, path, body, "")


pages = {
    "index.html": shell("Acasă - GIS Transporturi", "Transport autoturisme și mărfuri în România și Uniunea Europeană. Grup Impex S.R.L., Sibiu.", "/", HOME, "/"),
    "despre-noi/index.html": shell("Despre noi - GIS Transporturi", "Grup Impex S.R.L., înființată în 2001, transport mărfuri și autoturisme.", "/despre-noi/", ABOUT, ""),
    "servicii/index.html": shell("Servicii - GIS Transporturi", "Transport autoturisme, mărfuri, intermediere, depozitare și logistică.", "/servicii/", SERVICES, ""),
    "servicii/transport-autoturisme/index.html": shell("Transport autoturisme - GIS Transporturi", "Transport mașini pe platformă, 1 până la 10 autoturisme, în Europa.", "/servicii/transport-autoturisme/", AUTO, ""),
    "servicii/transport-marfuri/index.html": shell("Transport mărfuri - GIS Transporturi", "Transport mărfuri asigurate, flotă GPS, intern și internațional.", "/servicii/transport-marfuri/", FREIGHT, ""),
    "servicii/intermediere-transport-marfuri-si-autoturisme/index.html": shell("Intermediere - GIS Transporturi", "Intermediere transport mărfuri și autoturisme, cu asigurare.", "/servicii/intermediere-transport-marfuri-si-autoturisme/", BROKER, ""),
    "servicii/depozitare-si-logistica/index.html": shell("Depozitare și logistică - GIS Transporturi", "Depozitare autoturisme și mărfuri în Sibiu.", "/servicii/depozitare-si-logistica/", STORE, ""),
    "comanda-oferta/index.html": shell("Comandă / Ofertă - GIS Transporturi", "Cere o ofertă de transport sau depozitare.", "/comanda-oferta/", OFFER, ""),
    "contact/index.html": shell("Contact - GIS Transporturi", "GRUP IMPEX SRL, Sibiu, Str. Anul 1848 nr. 17. Telefon +40 740 099 080.", "/contact/", CONTACT, ""),
}

decl = legal_html("declaratie-privind-datele-cu-caracter-personal")
pages["gdpr/index.html"] = legal_page("GDPR", "/gdpr/", decl)
pages["declaratie-privind-datele-cu-caracter-personal/index.html"] = legal_page("Declarație privind datele cu caracter personal", "/declaratie-privind-datele-cu-caracter-personal/", decl)
pages["politica-privind-cookie-urile-ue/index.html"] = legal_page("Politica privind cookie-urile", "/politica-privind-cookie-urile-ue/", legal_html("politica-privind-cookie-urile-ue"))
pages["termeni-si-conditii/index.html"] = legal_page("Termeni și condiții", "/termeni-si-conditii/", legal_html("termeni-si-conditii"))
pages["politica-de-confidentialitate/index.html"] = legal_page("Politică de confidențialitate", "/politica-de-confidentialitate/", legal_html("politica-de-confidentialitate"))

for rel, html in pages.items():
    write(rel, html)
