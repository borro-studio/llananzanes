#!/usr/bin/env python3
"""Genera las fichas de las tres casas (web/casa-i.html, casa-ii.html, casa-iii.html)
a partir de una plantilla común. Para cambiar textos o fotos, editar CASAS y volver a ejecutar."""
import os
WEB = os.path.expanduser("~/Downloads/llananzanes/web")
RESERVA = "https://bookonline.pro/es/property/405750"
VIDEO = "https://www.rural-llananzanes.com/wp-content/uploads/2026/06/casa-{n}-video.mp4"

CASAS = {
    "i": dict(
        nombre="Piedrafita", num="Casa I", personas=7,
        titular="90 m² de piedra y madera <em>para compartir sin prisas.</em>",
        intro="Dos plantas con techos abovedados de madera y grandes ventanales a las montañas, los valles y el bosque de castaños. Muros de piedra, estufa de leña y sitio para siete.",
        baja=[("casa-i-planta-baja-salon-comedor", "Salón comedor", "Muros de piedra y estufa de leña", "Salón comedor de Piedrafita con muros de piedra, sofá y mesa de madera"),
              ("casa-i-planta-baja-bano", "Baño", "Completo, con ducha", "Baño de la planta baja de Piedrafita con azulejo verde y lavabo redondo"),
              ("casa-i-planta-baja", "Cocina", "Abierta al salón", "Cocina de Piedrafita con azulejos de colores, junto a la escalera de madera")],
        arriba=[("casa-i-planta-arriba-habitacion-1", "Habitación de matrimonio", "20 m²", "Habitación de matrimonio de Piedrafita con techo de madera y mecedora"),
                ("casa-i-planta-arriba-bano", "Baño", "Completo, con ducha", "Baño de la planta de arriba de Piedrafita con claraboya"),
                ("casa-i-planta-arriba-habitacion-2", "Habitación doble", "Dos camas, 20 m²", "Habitación de Piedrafita con dos camas individuales y pared color teja")],
    ),
    "ii": dict(
        nombre="La Laguna", num="Casa II", personas=7,
        titular="Espacio para siete, <em>con la estufa encendida.</em>",
        intro="Dos plantas con techos abovedados de madera y grandes ventanales a las montañas, los valles y el bosque de castaños. Un salón amplio alrededor de la estufa de leña y sitio para siete.",
        baja=[("casa-ii-planta-baja-salon-comedor", "Salón comedor", "Con estufa de leña", "Salón comedor de La Laguna con estufa de leña y escalera de madera"),
              ("casa-ii-planta-baja-bano", "Baño", "Completo, con ducha", "Baño de la planta baja de La Laguna con lavabo redondo sobre encimera de madera"),
              ("casa-ii-planta-baja-cocina", "Cocina", "Totalmente equipada", "Cocina de La Laguna con encimera de granito, vitrocerámica y lavadora")],
        arriba=[("casa-ii-planta-arriba-habitacion-1", "Habitación de matrimonio", "20 m²", "Habitación de matrimonio de La Laguna con claraboya y techo de madera"),
                ("casa-ii-planta-arriba-bano", "Baño", "Completo, con ducha", "Baño de la planta de arriba de La Laguna con azulejo rosa"),
                ("casa-ii-planta-arriba-habitacion-2", "Habitación doble", "Dos camas, 20 m²", "Habitación de La Laguna con dos camas individuales y ventanal al bosque")],
    ),
    "iii": dict(
        nombre="Coto Bello", num="Casa III", personas=9,
        titular="Un balcón <em>sobre los valles asturianos.</em>",
        intro="Dos plantas con techos abovedados de madera y grandes ventanales a las montañas, los valles y el bosque de castaños. La más capaz de las tres: sitio para nueve alrededor de la estufa.",
        baja=[("casa-iii-planta-baja-salon-comedor", "Salón comedor", "Con estufa de leña", "Salón comedor de Coto Bello con la estufa de leña encendida"),
              ("casa-iii-planta-baja-bano", "Baño", "Completo, con ducha", "Baño de la planta baja de Coto Bello con azulejo rojo y lavabo redondo"),
              ("casa-iii-planta-baja-salon-cocina", "Cocina", "Abierta al salón", "Cocina de Coto Bello con muro de piedra y ventana al valle")],
        arriba=[("casa-iii-planta-arriba-habitacion-1", "Habitación de matrimonio", "20 m²", "Habitación de matrimonio de Coto Bello con ventanales y techo de madera"),
                ("casa-iii-planta-arriba-bano", "Baño", "Completo, con ducha", "Baño de la planta de arriba de Coto Bello con azulejo verde"),
                ("casa-iii-planta-arriba-habitacion-2", "Habitación doble", "Dos camas, 20 m²", "Habitación de Coto Bello con camas individuales y contraventanas de madera")],
    ),
}

ICON = lambda n: f'<svg class="icon" aria-hidden="true"><use href="assets/icons/sprite.svg#{n}"/></svg>'

def fig(cls, f, lazy=True):
    src, t, d, alt = f
    return f'''<figure class="fig fig--{cls} reveal">
            <div class="fig__img"><img src="assets/img/{src}.jpg" alt="{alt}"{' loading="lazy"' if lazy else ''}></div>
            <figcaption><b>{t}</b><span>{d}</span></figcaption>
          </figure>'''

def card(n):
    c = CASAS[n]
    return f'''<article class="house reveal">
          <div class="house__img"><img src="assets/img/casa-{n}-planta-baja-salon-comedor.jpg" alt="Salón comedor de {c['nombre']}" loading="lazy"></div>
          <div class="house__meta">
            <h3>{c['nombre']}</h3>
            <a class="link-arrow house__link" href="casa-{n}.html">Ver {c['nombre']} {ICON('arrow-up-right')}</a>
            <ul>
              <li>{ICON('users')}Hasta {c['personas']} personas</li>
              <li>90 m²</li>
            </ul>
          </div>
        </article>'''

def pagina(n):
    c = CASAS[n]; otras = [k for k in CASAS if k != n]
    return f'''<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{c['nombre']} ({c['num']}) | El Mirador de Llananzanes</title>
  <meta name="description" content="{c['nombre']}: casa rural de 90 m² para hasta {c['personas']} personas en Llananzanes, Aller (Asturias). Dos habitaciones, dos baños, estufa de leña y vistas a los valles.">
  <meta name="robots" content="noindex">
  <meta name="theme-color" content="#15201a">
  <link rel="icon" href="assets/img/El-Mirador-de-Llananzanes-favicon.png">
  <link rel="preload" as="image" href="assets/img/casa-{n}-planta-baja-salon-comedor.jpg">
  <link rel="preload" as="font" type="font/woff2" href="assets/fonts/cormorant-normal-500-latin.woff2" crossorigin>
  <link rel="stylesheet" href="assets/fonts.css">
  <link rel="stylesheet" href="assets/styles.css">
  <script>
    (function (d, q) {{
      d.classList.add("js", "no-intro", "entered");
      var t = new URLSearchParams(q).get("theme");
      if (t === "light" || t === "dark") d.dataset.theme = t;
      if (/[?&]static/.test(q)) d.classList.add("static");
    }})(document.documentElement, location.search);
  </script>
</head>
<body>

<header class="nav">
  <div class="wrap">
    <a class="nav__logo" href="./" aria-label="El Mirador de Llananzanes, inicio">
      <img class="logo-l" src="assets/img/logo-light.png" alt="El Mirador de Llananzanes" width="381" height="100">
      <img class="logo-d" src="assets/img/El-Mirador-de-Llananzanes-logo.png" alt="" width="381" height="100">
    </a>
    <nav aria-label="Principal">
      <ul class="nav__links">
        <li><a href="./#casas">La casa</a></li>
        <li><a href="./#experiencias">Experiencias</a></li>
        <li><a href="./#donde">Dónde estamos</a></li>
        <li><a href="./#contacto">Contacto</a></li>
      </ul>
    </nav>
    <div class="nav__right">
      <a class="btn btn--solid" href="{RESERVA}" target="_blank" rel="noopener">Reservar</a>
      <button class="nav__burger" aria-label="Abrir menú" aria-expanded="false" aria-controls="menu">
        {ICON('list')}
      </button>
    </div>
  </div>
</header>

<div class="menu" id="menu" role="dialog" aria-modal="true" aria-label="Menú">
  <div class="menu__top">
    <img src="assets/img/logo-light.png" alt="El Mirador de Llananzanes" width="381" height="100">
    <button class="menu__close" aria-label="Cerrar menú">{ICON('x')}</button>
  </div>
  <ul>
    <li><a href="./#casas">La casa</a></li>
    <li><a href="./#experiencias">Experiencias</a></li>
    <li><a href="./#donde">Dónde estamos</a></li>
    <li><a href="{RESERVA}" target="_blank" rel="noopener"><em>Reservar</em></a></li>
  </ul>
  <div class="menu__foot">
    <a href="tel:+34661901664">+34 661 901 664</a>
    <a href="mailto:info@rural-llananzanes.com">info@rural-llananzanes.com</a>
  </div>
</div>

<main>

  <!-- Cabecera de la casa -->
  <section class="hero hero--casa">
    <div class="hero__media">
      <img src="assets/img/casa-{n}-planta-baja-salon-comedor.jpg" alt="{c['baja'][0][3]}" width="2200" height="1467" fetchpriority="high">
    </div>
    <div class="wrap hero__inner">
      <div class="hero__title">
        <span class="eyebrow"><a href="./#casas">Las casas</a> / {c['num']}</span>
        <h1><span class="line"><span style="--i:0">{c['nombre']}</span></span></h1>
      </div>
      <div class="hero__side">
        <ul class="cfacts">
          <li><span>Capacidad</span>Hasta {c['personas']} personas</li>
          <li><span>Superficie</span>90 m² en dos plantas</li>
          <li><span>Habitaciones</span>2, de 20 m²</li>
          <li><span>Baños</span>2 completos</li>
        </ul>
        <div class="hero__ctas">
          <a class="btn btn--solid" href="{RESERVA}" target="_blank" rel="noopener">Reservar {ICON('arrow-right')}</a>
          <a class="btn btn--ghost-light" href="#visita">Visita virtual</a>
        </div>
      </div>
    </div>
  </section>

  <!-- Presentación -->
  <div class="tone-forest welcome">
    <div class="watermark" aria-hidden="true"></div>
    <section class="cintro">
      <div class="wrap">
        <h2 class="reveal">{c['titular']}</h2>
        <div class="reveal" style="--d:.1s">
          <p>{c['intro']}</p>
        </div>
      </div>
    </section>
  </div>

  <!-- Planta baja -->
  <section class="floor" aria-labelledby="baja-t">
    <div class="wrap">
      <div class="floor__head reveal">
        <h2 id="baja-t">Planta <em>baja.</em></h2>
        <span class="eyebrow">01 / Para estar juntos</span>
      </div>
      <div class="floor__grid">
          {fig('a', c['baja'][0])}
          {fig('b', c['baja'][1])}
          <div class="floor__txt reveal">
            <p>El salón, la mesa grande y la cocina, todo alrededor de la estufa de leña.</p>
            <ul>
              <li>Salón comedor</li>
              <li>Cocina con vitrocerámica</li>
              <li>Baño completo con ducha</li>
            </ul>
          </div>
          {fig('c', c['baja'][2])}
      </div>
    </div>
  </section>

  <!-- Planta de arriba -->
  <section class="floor floor--flip tone-ochre" aria-labelledby="arriba-t">
    <div class="wrap">
      <div class="floor__head reveal">
        <h2 id="arriba-t">Planta <em>de arriba.</em></h2>
        <span class="eyebrow">02 / Para descansar</span>
      </div>
      <div class="floor__grid">
          {fig('a', c['arriba'][0])}
          {fig('b', c['arriba'][1])}
          {fig('c', c['arriba'][2])}
          <div class="floor__txt reveal">
            <p>Dos habitaciones de 20 m² bajo un techo de madera de casi tres metros, con ventanales al valle.</p>
            <ul>
              <li>Habitación con cama de matrimonio</li>
              <li>Habitación con dos camas individuales</li>
              <li>Baño completo con ducha</li>
            </ul>
          </div>
      </div>
    </div>
  </section>

  <!-- Equipamiento -->
  <section class="equip tone-night" aria-labelledby="equip-t">
    <div class="wrap">
      <div class="reveal">
        <h2 id="equip-t">Llegar y <em>no echar nada en falta.</em></h2>
        <p class="equip__lead">La casa está equipada por completo. Fuera, una finca de más de 3.000 m² compartida entre las tres casas.</p>
      </div>
      <div class="equip__cols reveal" style="--d:.1s">
        <div>
          <h3>En la casa</h3>
          <ul>
            <li>Estufa de leña</li>
            <li>Vitrocerámica, frigorífico y microondas</li>
            <li>Lavadora</li>
            <li>Vajilla y menaje completo</li>
            <li>Televisión</li>
            <li>Colchones viscoelásticos</li>
            <li>Ropa de cama</li>
          </ul>
        </div>
        <div>
          <h3>En la finca</h3>
          <ul>
            <li>Aparcamiento privado</li>
            <li>Zona de barbacoa</li>
            <li>Zonas verdes y bancos</li>
            <li>Fuente propia</li>
            <li>Diana de tiro con arco</li>
            <li>Rutas desde la puerta</li>
          </ul>
        </div>
      </div>
    </div>
  </section>

  <!-- Visita virtual -->
  <section class="tour" id="visita" aria-labelledby="tour-t">
    <video preload="none" playsinline poster="assets/img/casa-{n}-video-poster.jpg" src="{VIDEO.format(n=n)}"></video>
    <div class="wrap tour__ui">
      <h2 id="tour-t">Visita <em>virtual.</em></h2>
      <button class="tour__play" type="button" aria-label="Reproducir la visita virtual de {c['nombre']}">
        <svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M5 3l16 9-16 9z"/></svg>
      </button>
    </div>
  </section>

  <!-- Las otras casas -->
  <section class="others" aria-labelledby="others-t">
    <div class="wrap">
      <div class="others__head reveal">
        <h2 id="others-t">Las otras <em>casas.</em></h2>
        <a class="link-arrow" href="./#casas">Ver las tres {ICON('arrow-up-right')}</a>
      </div>
      <div class="others__grid">
        {card(otras[0])}
        {card(otras[1])}
      </div>
    </div>
  </section>

  <!-- CTA final -->
  <section class="cta cta--casa" aria-labelledby="cta-t">
    <img src="assets/img/home-reserva.jpg" alt="" loading="lazy">
    <div class="wrap reveal">
      <h2 id="cta-t">Reserva <em>{c['nombre']}.</em></h2>
      <div class="cta__row">
        <a class="btn btn--solid" href="{RESERVA}" target="_blank" rel="noopener">Reservar {ICON('arrow-right')}</a>
        <a href="tel:+34661901664">{ICON('phone')}O llámanos: +34 661 901 664</a>
      </div>
    </div>
  </section>

</main>

<footer class="footer tone-forest">
  <div class="wrap">
    <div class="footer__grid">
      <div>
        <img class="logo-d" src="assets/img/El-Mirador-de-Llananzanes-logo.png" alt="El Mirador de Llananzanes" width="381" height="100" loading="lazy">
        <img class="logo-l" src="assets/img/logo-light.png" alt="El Mirador de Llananzanes" width="381" height="100" loading="lazy">
        <p>Casas rurales en Llananzanes, Asturias. Naturaleza, tranquilidad y la Asturias más auténtica.</p>
      </div>
      <div>
        <h4>La casa</h4>
        <ul>
          <li><a href="casa-i.html">Piedrafita</a></li>
          <li><a href="casa-ii.html">La Laguna</a></li>
          <li><a href="casa-iii.html">Coto Bello</a></li>
          <li><a href="./#experiencias">Experiencias</a></li>
        </ul>
      </div>
      <div>
        <h4>Información</h4>
        <ul>
          <li><a href="condiciones-de-reserva.html">Condiciones de reserva</a></li>
          <li><a href="normas-de-la-casa.html">Normas de la casa</a></li>
          <li><a href="aviso-legal.html">Aviso legal</a></li>
          <li><a href="politica-de-privacidad.html">Privacidad</a></li>
          <li><a href="politica-de-cookies.html">Cookies</a></li>
        </ul>
      </div>
      <div>
        <h4>Contacto</h4>
        <ul>
          <li><a href="tel:+34661901664">+34 661 901 664</a></li>
          <li><a href="mailto:info@rural-llananzanes.com">info@rural-llananzanes.com</a></li>
          <li><a href="https://www.instagram.com/llananzanes" target="_blank" rel="noopener">Instagram</a></li>
        </ul>
      </div>
    </div>
    <p class="footer__mark" aria-hidden="true">Llananzanes</p>
    <div class="footer__legal">
      <span>© 2026 El Mirador de Llananzanes</span>
      <span>Llananzanes, Aller, Asturias</span>
    </div>
  </div>
</footer>

<script src="assets/main.js" defer></script>
</body>
</html>
'''

for n in CASAS:
    open(f"{WEB}/casa-{n}.html", "w").write(pagina(n))
    print(f"casa-{n}.html")
