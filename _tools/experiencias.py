#!/usr/bin/env python3
"""Genera las páginas de experiencias (web/experiencias/*.html).
La cabecera, el menú y el pie se toman de web/casa-i.html (generada por casas.py) y se
adaptan a la subcarpeta, así que hay que ejecutar casas.py antes si cambian.
Para cambiar textos o fotos, editar EXPERIENCIAS y volver a ejecutar."""
import os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WEB = os.path.join(ROOT, "web")
RESERVA = "https://bookonline.pro/es/property/405750"
CASA = "43.0645974,-5.5755936"  # Llananzanes (enlace "Cómo llegar" de la home)
WA = "https://wa.me/34660867462?text=Hola%2C%20quer%C3%ADa%20informaci%C3%B3n%20sobre%20El%20Mirador%20de%20Llananzanes"
ICON = lambda n: f'<svg class="icon" aria-hidden="true"><use href="../assets/icons/sprite.svg#{n}"/></svg>'

EXPERIENCIAS = {
    "esqui-y-nieve": dict(
        titulo="Esquí y nieve",
        descripcion="Fuentes de Invierno, San Isidro y Valgrande-Pajares: las tres estaciones de esquí cerca de El Mirador de Llananzanes, en Aller (Asturias).",
        hero="experiencia-temporada-esqui", hero_alt="Cumbres nevadas de la cordillera en plena temporada de esquí",
        etiqueta="Invierno",
        entrada="Tres estaciones en la misma cordillera. Dos de ellas, a media hora de casa.",
        titular="Bajar la pista por la mañana, <em>volver a la estufa por la tarde.</em>",
        intro="Desde Llananzanes se sube en media hora al puerto de San Isidro, donde se tocan Fuentes de Invierno y San Isidro. Pistas para todos los niveles, escuelas de esquí y snowboard, alquiler de material y zonas pensadas para familias.",
        bloque="Tres <em>estaciones.</em>", bloque_eti="Cordillera Cantábrica",
        sitios=[
            dict(nombre="Fuentes de Invierno", ruta="43.0558428,-5.3934367", foto="esqui-fuentes", alt="Pistas nevadas vistas desde el telesilla de La Llomba, en Fuentes de Invierno",
                 credito=("", "NibasH, CC BY-SA 3.0", "https://commons.wikimedia.org/wiki/File:San_Isidro_-_Riopinos_desde_TSF4_Picu_La_Llomba_en_Fuentes_de_Invierno_-_panoramio.jpg"),
                 texto="La más cercana, en el propio concejo de Aller. Manejable y tranquila: perfecta para familias y para quien empieza.",
                 datos=[("Dónde", "Aller, Asturias"), ("Desde la casa", "28 km · unos 35 min"), ("Cotas", "1.500 – 1.950 m"), ("Pistas", "Unos 9 km")]),
            dict(nombre="San Isidro", ruta="43.0612889,-5.3798697", foto="esqui-san-isidro", alt="Telesilla y pista de la estación de San Isidro bajo un cielo azul",
                 credito=("", "Wikimedia Commons, dominio público", "https://commons.wikimedia.org/wiki/File:Estaci%C3%B3n_de_esqu%C3%AD_de_San_Isidro.JPG"),
                 texto="Pegada a Fuentes de Invierno, en la vertiente leonesa del puerto. La de más recorrido: cuatro sectores y pistas de todos los colores.",
                 datos=[("Dónde", "Puebla de Lillo, León"), ("Desde la casa", "28 km · unos 35 min"), ("Cotas", "1.500 – 2.100 m"), ("Pistas", "Unos 30 km")]),
            dict(nombre="Valgrande-Pajares", ruta="42.9688144,-5.7872938", foto="esqui-pajares", alt="Edificios de Brañillín y laderas nevadas de la estación de Valgrande-Pajares",
                 credito=("", "Foltrikas, CC BY-SA 4.0 (reescalada)", "https://commons.wikimedia.org/wiki/File:Estaci%C3%B3n_de_Valgrande-Pajares.JPG"),
                 texto="La estación clásica de Asturias, en el puerto de Pajares. Tres sectores, telecabina y nieve artificial en parte de sus pistas.",
                 datos=[("Dónde", "Lena, Asturias"), ("Desde la casa", "70 km · 1 h 20 min"), ("Cotas", "1.450 – 1.890 m"), ("Pistas", "Unos 30 km")]),
        ],
        nota="Datos orientativos: distancias y tiempos en coche desde Llananzanes (Aller), y kilómetros de pistas que cambian con la nieve de cada temporada. Antes de subir, mira el parte de la estación.",
        extra=dict(foto="esqui-raquetas", alt="Montañero subiendo por una ladera nevada bajo un cielo azul intenso",
                   titular="Sin esquís, <em>también.</em>",
                   texto="Rutas guiadas con raquetas por el entorno del puerto de San Isidro: bosques, lagos helados y cumbres de la cordillera, a tu ritmo. Te ayudamos a organizar la salida."),
        cierre="Reserva <em>tu invierno.</em>", cierre_foto="experiencia-esqui",
    ),
}

def concha():
    """Cabecera y pie de las fichas de casa, con las rutas pasadas a la subcarpeta."""
    s = open(os.path.join(WEB, "casa-i.html")).read()
    cab, pie = s.split("<main>")[0], s.split("</main>")[1]
    def rutas(t):
        t = t.replace('src="assets/', 'src="../assets/').replace('href="assets/', 'href="../assets/').replace('use href="assets/', 'use href="../assets/')
        t = t.replace('href="./', 'href="../')
        t = re.sub(r'href="(casa-[iv]+\.html|condiciones-de-reserva\.html|normas-de-la-casa\.html|aviso-legal\.html|politica-de-privacidad\.html|politica-de-cookies\.html)"', r'href="../\1"', t)
        return t
    cab, pie = rutas(cab), rutas(pie)
    cab = re.sub(r'<link rel="preload" as="image" href="[^"]+">\n', "", cab)
    return cab, pie

def pagina(slug, e, cab, pie):
    cab = re.sub(r"<title>.*?</title>", f"<title>{e['titulo']} | El Mirador de Llananzanes</title>", cab)
    cab = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{e["descripcion"]}">', cab)
    sitios = []
    for i, x in enumerate(e["sitios"]):
        datos = "".join(f"<li><span>{k}</span>{v}</li>" for k, v in x["datos"])
        sitios.append(f'''      <article class="station{' station--flip' if i % 2 else ''}">
        <figure class="station__img reveal"><img src="../assets/img/{x['foto']}.jpg" alt="{x['alt']}" loading="lazy"></figure>
        <div class="station__txt reveal" style="--d:.1s">
          <span class="station__n">0{i + 1}</span>
          <h3>{x['nombre']}</h3>
          <p>{x['texto']}</p>
          <ul class="station__data">{datos}</ul>
          <a class="btn btn--line station__go" href="https://www.google.com/maps/dir/?api=1&amp;origin={CASA}&amp;destination={x['ruta']}&amp;travelmode=driving" target="_blank" rel="noopener">Cómo llegar desde la casa {ICON('arrow-up-right')}</a>
        </div>
      </article>''')
    cr = [f'<a href="{x["credito"][2]}" target="_blank" rel="noopener">{x["nombre"]}: {x["credito"][1]}</a>' for x in e["sitios"] if x.get("credito") and len(x["credito"]) > 2]
    creditos = f'<p class="stations__credits">Fotos de las estaciones: {" · ".join(cr)}.</p>' if cr else ""
    x = e["extra"]
    main = f'''<main>

  <!-- Cabecera -->
  <section class="hero hero--casa hero--xp">
    <div class="hero__media">
      <img src="../assets/img/{e['hero']}.jpg" alt="{e['hero_alt']}" fetchpriority="high">
    </div>
    <div class="wrap hero__inner">
      <div class="hero__title">
        <span class="eyebrow"><a href="../#experiencias">Experiencias</a> / {e['etiqueta']}</span>
        <h1><span class="line"><span style="--i:0">{e['titulo']}.</span></span></h1>
      </div>
      <div class="hero__side">
        <p>{e['entrada']}</p>
        <div class="hero__ctas">
          <a class="btn btn--solid" href="{RESERVA}" target="_blank" rel="noopener">Reservar {ICON('arrow-right')}</a>
          <a class="btn btn--ghost-light" href="#estaciones">Ver las estaciones</a>
        </div>
      </div>
    </div>
  </section>

  <!-- Presentación -->
  <div class="tone-forest welcome">
    <div class="watermark" aria-hidden="true"></div>
    <section class="cintro">
      <div class="wrap">
        <h2 class="reveal">{e['titular']}</h2>
        <div class="reveal" style="--d:.1s"><p>{e['intro']}</p></div>
      </div>
    </section>
  </div>

  <!-- Estaciones -->
  <section class="stations" id="estaciones" aria-labelledby="st-t">
    <div class="wrap">
      <div class="floor__head reveal">
        <h2 id="st-t">{e['bloque']}</h2>
        <span class="eyebrow">{e['bloque_eti']}</span>
      </div>
{chr(10).join(sitios)}
      <p class="stations__note">{e['nota']}</p>
      {creditos}
    </div>
  </section>

  <!-- Bloque extra -->
  <section class="xp-extra tone-night" aria-labelledby="ex-t">
    <div class="wrap">
      <div class="xp-extra__img reveal"><img src="../assets/img/{x['foto']}.jpg" alt="{x['alt']}" loading="lazy"></div>
      <div class="reveal" style="--d:.1s">
        <h2 id="ex-t">{x['titular']}</h2>
        <p>{x['texto']}</p>
        <a class="link-arrow" href="{WA}" target="_blank" rel="noopener">Escríbenos por WhatsApp {ICON('arrow-up-right')}</a>
      </div>
    </div>
  </section>

  <!-- CTA final -->
  <section class="cta cta--casa" aria-labelledby="cta-t">
    <img src="../assets/img/{e.get('cierre_foto', 'home-reserva')}.jpg" alt="" loading="lazy">
    <div class="wrap reveal">
      <h2 id="cta-t">{e['cierre']}</h2>
      <div class="cta__row">
        <a class="btn btn--solid" href="{RESERVA}" target="_blank" rel="noopener">Reservar {ICON('arrow-right')}</a>
        <a href="../#experiencias">{ICON('arrow-up-right')}Ver todas las experiencias</a>
      </div>
    </div>
  </section>

</main>'''
    return cab + main + pie

if __name__ == "__main__":
    os.makedirs(os.path.join(WEB, "experiencias"), exist_ok=True)
    cab, pie = concha()
    for slug, e in EXPERIENCIAS.items():
        open(os.path.join(WEB, "experiencias", f"{slug}.html"), "w").write(pagina(slug, e, cab, pie))
        print(f"experiencias/{slug}.html")
