#!/usr/bin/env python3
"""Genera las páginas de experiencias (web/experiencias/*.html).
La cabecera, el menú y el pie se toman de web/casa-i.html (generada por casas.py) y se
adaptan a la subcarpeta, así que hay que ejecutar casas.py antes si cambian.
Para cambiar textos o fotos, editar EXPERIENCIAS y volver a ejecutar."""
import os, re, json
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
    "senderismo-y-trekking": dict(
        titulo="Senderismo y trekking",
        descripcion="Rutas con historia cerca de El Mirador de Llananzanes, en Aller (Asturias): Peña Mea, las Foces del Pino y el hayedo del Gumial.",
        hero="experiencia-senderismo-y-trekking", hero_alt="Sendero de montaña entre bosques y prados en el concejo de Aller",
        etiqueta="Todo el año", ancla="rutas", historia_completa=False, formato="mapa",  # solo el resumen (texto completo del cliente guardado abajo) ver="Ver las rutas",
        entrada="Rutas para todos los niveles, desde paseos en familia hasta alta montaña. Y en cada una, una historia.",
        titular="Caminos que ya pisaron <em>otros antes que tú.</em>",
        intro="Bosques centenarios, ríos, brañas y cumbres con vistas inolvidables. Muy cerca de la casa salen rutas por los lugares más emblemáticos de Aller y de la Cordillera Cantábrica.",
        bloque="Rutas con <em>historia.</em>", bloque_eti="Aller de historias",
        creditos_eti="Foto", creditos_extra=" Mapas: © colaboradores de OpenStreetMap, SRTM | OpenTopoMap (CC BY-SA).",
        sitios=[
            dict(nombre="Peña Mea", mapa_id="pena-mea", km_eti="Hasta la cumbre", alto_eti="Cumbre", alto="1.557", foto_pie="El eclipse de 2026 en el Ojo de Buey", salida="Sale de Pelúgano (Aller), a 14 km de la casa en coche, unos 20 min.", ruta="43.1513631,-5.583405", foto="ruta-pena-mea-eclipse", foto_pos="44% 50%", alt="El eclipse de 2026 visto a través del Ojo de Buey de Peña Mea",
                 credito=("", "Gijs de Reijke", ""),
                 texto="Casi 1.000 metros de subida entre aldeas, cabañas y fuentes hasta el Ojo de Buey, un ventanal de roca de 20 metros que atraviesa la cresta de la peña. El fotógrafo holandés Gijs de Reijke pasó cuatro años preparando, sin haber pisado nunca Asturias, una foto imposible: el eclipse de 2026 encajado justo dentro de él.",
                 historia=[
                     "Peña Mea (1557 m) se alza majestuosa entre los concejos de Laviana y Aller. Su recortada silueta llama poderosamente la atención. La ascensión requiere esfuerzo, pues se remontan casi 1000 m de desnivel, pero la recompensa ya se obtiene durante el camino por las espectaculares vistas, y la contemplación del mítico Ojo de Buey, un contrafuerte de silueta inconfundible, fruto de la erosión en la roca caliza.",
                     "Gijs de Reijke, profesor de geografía y fotógrafo holandés descubrió en 2022 que la trayectoria de un eclipse solar iba a cruzar el norte de España cuatro años después. En lugar de conformarse con verlo desde cualquier lugar, se propuso un reto mayúsculo: fotografiar el eclipse alineado exactamente dentro del Ojo de Buey, el inmenso ventanal de roca de 20 metros de diámetro que acompaña la subida a Peña Mea. Desde su casa en los Países Bajos, y sin haber pisado Asturias en su vida, pasó estos años preparando lo que él mismo definió como «la sesión más meticulosa de su vida». Utilizó simuladores astronómicos y Google Earth para trazar líneas rectas que atravesaran la abertura de la roca, estudiando fotos y vídeos de montañeros para encontrar el punto exacto en la ladera desde el cual disparar.",
                     "La ruta a Peña Mea, señalizada como Sendero de Pequeño Recorrido (PR), discurre, al principio por valles verdes y arbolados, y al final por roca viva. Durante el trayecto se pasa por aldeas, cabañas dispersas con abrevaderos para el ganado y prados de los que brotan fuentes. A mitad de trayecto la pista se convierte en una senda estrecha hasta la base de Peña Mea. Desde aquí la subida en zigzag por la montaña impone por su gran pendiente, y sin rastro aún del Ojo de Buey.",
                     "El día del eclipse, el fotógrafo tuvo que enfrentarse a la dura realidad de esa ruta. Cargado con kilos de equipo fotográfico, abordó el exigente desnivel de las canales que suben hacia la peña. Él mismo confesó que el ascenso fue completamente extenuante por el peso que llevaba. Además, había un factor que ninguna aplicación podía controlar: la niebla y las nubes asturianas. Hasta la misma mañana de la expedición, no tuvo la certeza de si el cielo se despejaría lo suficiente para ver algo.",
                     "Y de golpe, tras un recodo, apareció la oquedad, ese ventanal rocoso que traspasa el crestón de Peña Mea y depara una visión inolvidable.",
                     "<strong>¿Te gustaría sentir la misma emoción que vivió Gijs al encontrarse con su escenario soñado, listo para conseguir una foto y un momento único?</strong>",
                 ],
                 datos=[("Salida", "Pelúgano (Aller)"), ("Hasta la cumbre", "5,9 km · unos 980 m de desnivel"), ("Cumbre", "1.557 m"), ("Desde la casa", "14 km · unos 20 min")]),
            dict(nombre="Foces del Pino", mapa_id="foces-del-pino", km_eti="PR-AS 31", foto_pie="Las Foces del Pino", nota="Pasa a 700 m de la casa: se empieza andando.", salida="Sendero señalizado entre Casomera y Felechosa. Las foces, junto a Pola del Pino (11 km en coche).", ruta="43.1141797,-5.5303052", foto="ruta-foces-del-pino", alt="Sendero tallado en la roca caliza de las Foces del Pino, junto al río",
                 texto="El río Pino tardó milenios en tallar este desfiladero: en algunos puntos sus paredes de caliza dejan menos de 6 metros de paso y guardan fósiles marinos de más de 300 millones de años. Su sendero es una antigua calzada romana que aún usan los vaqueros para subir el ganado a los puertos, y que recorrieron peregrinos camino de Santiago.",
                 historia=[
                     "La ruta que discurre desde Pola del Pino a los puertos pastoriles de Caniecha no es un bucólico paseo más de la extensa lista que nos ofrece el concejo de Aller.",
                     "El desfiladero que atraviesa, que en Asturias conocemos como «foces», fue esculpido a lo largo de milenios por la fuerza de las aguas del río Pino, que talló la roca formando un paso angosto cuyas paredes casi verticales llegan a dejar una anchura de menos de 6 metros en algunos puntos.",
                     "Sus impresionantes paredes de roca caliza guardan en su interior fósiles de algas y animales marinos con más de 300 millones de años de antigüedad, lo que demuestra que esta zona fue antaño un lecho marino.",
                     "Y el sendero tallado a tramos en dicha roca, no sólo es la vía tradicional que utilizan los vaqueros del concejo de Aller para subir el ganado a los puertos de montaña y a las brañas cuando finaliza el invierno. Su caja la delata como una antigua calzada romana, paso de comunicación secular, que también fue empleada como alternativa por los peregrinos que se dirigían hacia el Camino de Santiago.",
                     "<strong>¿Quieres vivir la experiencia que transmite atravesar estas foces que, a tenor de su importancia natural e histórica, han sido declaradas Monumento Natural?</strong>",
                 ],
                 datos=[("Sendero", "PR-AS 31 · Casomera – Felechosa"), ("Recorrido", "18 km · unos 1.070 m de desnivel"), ("Desde la casa", "Pasa a 700 m: se sale andando"), ("Protección", "Monumento Natural")]),
            dict(nombre="El Gumial", mapa_id="gumial", km_eti="PR-AS 48", salida="Sale de Cuevas (Aller), a 17 km de la casa en coche, unos 20 min.", ruta="43.0890804,-5.4702386", foto="ruta-gumial", alt="Arroyo en cascada entre hayas con colores de otoño",
                 texto="Desde Cuevas, uno de los hayedos más cerrados de Asturias sube hasta la braña del Gumial por un paso que ya se usaba hace más de 3.000 años: aquí aparecieron dos puñales de la Edad del Bronce, hoy en el Museo Arqueológico de Asturias. Arriba esperan las cabañas de piedra donde las familias del valle pasaban el verano con el ganado.",
                 historia=[
                     "Si decides adentrarte en la ruta que sube desde el pequeño pueblo de Cuevas hasta la braña del Gumial, no solo vas a caminar por uno de los bosques de hayas (hayedos) más impresionantes y cerrados de Asturias, sino que estarás pisando una auténtica «autopista» prehistórica.",
                     "Años atrás, se encontraron en este mismo paraje montañoso dos puñales de la Edad del Bronce, «los puñales del Gumial». Su hallazgo demostró de manera irrefutable que esta ruta no es un simple sendero moderno para excursionistas. Hace más de 3.000 años, viajeros, cazadores o guerreros prehistóricos ya se abrían paso a través de la espesura del bosque del Gumial, armados con sus puñales de bronce, probablemente utilizando este puerto como una vía crucial para cruzar la Cordillera Cantábrica. Hoy en día, si quieres ver estas armas milenarias que cayeron o fueron depositadas en la ruta que vas a caminar, puedes encontrarlas expuestas a buen recaudo en el Museo Arqueológico de Asturias, en Oviedo.",
                     "Cuando llegues al final de la ruta, al collado donde se abre el bosque y el paisaje te permite respirar frente a los picos que rondan los 1.800 metros de altitud, te encontrarás con la Braña del Gumial. Verás varias cabañas de piedra (corros y refugios). No son meras construcciones abandonadas; son el vestigio vivo de la trashumancia asturiana. Durante siglos, familias enteras de los pueblos del valle subían hasta aquí en los meses de verano con su ganado, viviendo aislados en la alta montaña para aprovechar los pastos frescos antes de que llegaran las nieves del duro invierno allerano.",
                     "<strong>¿Te apetece transitar por un bosque prístino, recreando el paso y la presencia de nuestros antecesores, hasta uno de los lugares más mágicos de nuestras montañas?</strong>",
                 ],
                 datos=[("Sendero", "PR-AS 48 · desde Cuevas"), ("Recorrido", "9,2 km · unos 890 m de desnivel"), ("Paisaje", "Hayedo y braña"), ("Desde la casa", "17 km · unos 20 min")]),
        ],
        nota="Distancias, desniveles y trazados orientativos, a partir de los senderos señalizados de OpenStreetMap; tiempos en coche desde Llananzanes (Aller). Antes de salir, consulta el parte meteorológico: en la montaña asturiana la niebla cambia rápido.",
        cierre="Reserva <em>tu ruta.</em>", cierre_foto="home-reserva",
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

def mapa_svg(slug, nombre, plano=False):
    """Mapa topográfico con la ruta que se dibuja al verlo (datos de _tools/mapas.py)."""
    m = json.load(open(os.path.join(WEB, "assets", "mapas.json")))[slug]
    def marca(k):
        tx, ancla = (k["x"] - 16, ' text-anchor="end"') if k.get("izq") else (k["x"] + 16, "")
        return f'<g class="rmap__mk" data-x="{k["x"]}" data-y="{k["y"]}"><circle cx="{k["x"]}" cy="{k["y"]}" r="9"/><text x="{tx}" y="{k["y"] + 7}"{ancla}>{k["n"]}</text></g>'
    marcas = "".join(marca(k) for k in m["marcas"])
    casa = ""
    if m["casa"]:
        c = m["casa"]
        casa = f'<g class="rmap__casa"><rect x="{c["x"] - 11}" y="{c["y"] - 11}" width="22" height="22" rx="3"/><text x="{c["x"] + 18}" y="{c["y"] + 7}">La casa</text></g>'
    km = f'{m["km"]:.1f}'.replace(".", ",")
    sube = f'{m["sube"]:,}'.replace(",", ".")
    ajuste = ' preserveAspectRatio="xMidYMid slice"' if plano else ""
    svg = f'''<svg class="rmap__plano" viewBox="0 0 {m["w"]} {m["h"]}"{ajuste} role="img" aria-label="Mapa de la ruta de {nombre}: {km} km y {sube} m de desnivel">
            <image href="../assets/img/mapa-{slug}.jpg" width="{m["w"]}" height="{m["h"]}"/>
            <path class="rmap__sombra" d="{m["d"]}"/><path class="rmap__ruta" d="{m["d"]}"/>
            {casa}{marcas}<circle class="rmap__yo" r="11" cx="-50" cy="-50"/>
          </svg>'''
    if plano: return svg
    return f'''<div class="rmap" data-slug="{slug}" data-km="{m["km"]}">
          {svg}
          <div class="rmap__bar"><span class="rmap__km">{km} km</span><span>+{sube} m</span><button type="button" class="rmap__otra">Ver de nuevo</button></div>
        </div>'''

def rutas_mapa(e, creditos):
    """Rutas a pantalla completa sobre su mapa (3D si se puede): tarjeta a la izquierda, foto tipo polaroid y barra para saltar entre rutas."""
    M = json.load(open(os.path.join(WEB, "assets", "mapas.json")))
    miles = lambda n: f"{n:,}".replace(",", ".")
    ON = ' class="on" aria-current="true"'
    nav = lambda act: "".join(f'<a href="#ruta-{x["mapa_id"]}"{ON if x is act else ""}><span>0{i + 1}</span>{x["nombre"]}</a>' for i, x in enumerate(e["sitios"]))
    secciones = []
    for i, x in enumerate(e["sitios"]):
        m = M[x["mapa_id"]]
        km = f'{m["km"]:.1f}'.replace(".", ",")
        nota = f'<p class="ruta__nota">{x["nota"]}</p>' if x.get("nota") else ""
        ir = f'https://www.google.com/maps/dir/?api=1&amp;origin={CASA}&amp;destination={x["ruta"]}&amp;travelmode=driving'
        secciones.append(f'''  <section class="ruta rmap" id="ruta-{x["mapa_id"]}" data-slug="{x["mapa_id"]}" data-km="{m["km"]}" aria-labelledby="ruta-{i}">
    <div class="ruta__lienzo">{mapa_svg(x["mapa_id"], x["nombre"], plano=True)}</div>
    <div class="ruta__velo" aria-hidden="true"></div>
    <div class="wrap ruta__in">
      <div class="ruta__card">
        <span class="eyebrow">0{i + 1} · {e["bloque_eti"]}</span>
        <h3 id="ruta-{i}">{x["nombre"]}</h3>
        <p>{x["texto"]}</p>
        <div class="ruta__datos">
          <div><b><span class="rmap__km" data-num>{km}</span><small> km</small></b><span>{x.get("km_eti", "Recorrido")}</span></div>
          <div><b>{miles(m["sube"])}<small> m</small></b><span>Desnivel</span></div>
          <div><b>{x.get("alto", miles(m["zmax"]))}<small> m</small></b><span>{x.get("alto_eti", "Punto más alto")}</span></div>
        </div>
        {nota}<p class="ruta__salida">{x["salida"]}</p>
        <div class="ruta__ctas"><a class="btn btn--solid" href="{ir}" target="_blank" rel="noopener">Cómo llegar desde la casa {ICON("arrow-up-right")}</a><button type="button" class="rmap__otra">Ver de nuevo</button></div>
      </div>
      <figure class="ruta__foto"><img src="../assets/img/{x["foto"]}.jpg" alt="{x["alt"]}" loading="lazy" style="object-position: {x.get("foto_pos", "50% 50%")}"><figcaption>{x.get("foto_pie", x["nombre"])}</figcaption></figure>
    </div>
    <nav class="ruta__nav" aria-label="Rutas">{nav(x)}</nav>
  </section>''')
    return f'''  <!-- Rutas -->
  <section class="stations stations--rutas" id="{e.get('ancla', 'rutas')}" aria-labelledby="st-t">
    <div class="wrap">
      <div class="floor__head reveal">
        <h2 id="st-t">{e['bloque']}</h2>
        <span class="eyebrow">{e['bloque_eti']}</span>
      </div>
    </div>
  </section>
{chr(10).join(secciones)}
  <div class="wrap rutas__pie">
    <p class="stations__note">{e['nota']}</p>
    {creditos}
  </div>'''

def pagina(slug, e, cab, pie):
    cab = re.sub(r"<title>.*?</title>", f"<title>{e['titulo']} | El Mirador de Llananzanes</title>", cab)
    cab = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{e["descripcion"]}">', cab)
    sitios = []
    for i, x in enumerate(e["sitios"]):
        datos = "".join(f"<li><span>{k}</span>{v}</li>" for k, v in x["datos"])
        historia = ""
        if x.get("historia") and e.get("historia_completa", True):
            ps = "".join(f"<p>{h}</p>" for h in x["historia"])
            historia = f'\n          <details class="station__story"><summary>Leer la historia completa</summary>{ps}</details>'
        if x.get("mapa"):
            ir = f'<a class="btn btn--line station__go" href="https://www.google.com/maps/search/?api=1&amp;query={x["mapa"]}" target="_blank" rel="noopener">Ver en el mapa {ICON("arrow-up-right")}</a>'
        else:
            ir = f'<a class="btn btn--line station__go" href="https://www.google.com/maps/dir/?api=1&amp;origin={CASA}&amp;destination={x["ruta"]}&amp;travelmode=driving" target="_blank" rel="noopener">Cómo llegar desde la casa {ICON("arrow-up-right")}</a>'
        sitios.append(f'''      <article class="station{' station--flip' if i % 2 else ''}{' station--story' if x.get('historia') else ''}">
        <figure class="station__img reveal"><img src="../assets/img/{x['foto']}.jpg" alt="{x['alt']}" loading="lazy">{mapa_svg(x['mapa_id'], x['nombre']) if x.get('mapa_id') else ''}</figure>
        <div class="station__txt reveal" style="--d:.1s">
          <span class="station__n">0{i + 1}</span>
          <h3>{x['nombre']}</h3>
          <p>{x['texto']}</p>
          <ul class="station__data">{datos}</ul>{historia}
          {ir}
        </div>
      </article>''')
    cr = [(f'<a href="{x["credito"][2]}" target="_blank" rel="noopener">{x["nombre"]}: {x["credito"][1]}</a>' if x["credito"][2] else f'{x["nombre"]}: {x["credito"][1]}') for x in e["sitios"] if x.get("credito") and len(x["credito"]) > 2]
    creditos = f'<p class="stations__credits">{e.get("creditos_eti", "Fotos de las estaciones")}: {" · ".join(cr)}.{e.get("creditos_extra", "")}</p>' if cr else ""
    estaciones = f'''  <!-- Estaciones -->
  <section class="stations" id="{e.get('ancla', 'estaciones')}" aria-labelledby="st-t">
    <div class="wrap">
      <div class="floor__head reveal">
        <h2 id="st-t">{e['bloque']}</h2>
        <span class="eyebrow">{e['bloque_eti']}</span>
      </div>
{chr(10).join(sitios)}
      <p class="stations__note">{e['nota']}</p>
      {creditos}
    </div>
  </section>'''
    x = e.get("extra")
    extra = f'''  <!-- Bloque extra -->
  <section class="xp-extra tone-night" aria-labelledby="ex-t">
    <div class="wrap">
      <div class="xp-extra__img reveal"><img src="../assets/img/{x['foto']}.jpg" alt="{x['alt']}" loading="lazy"></div>
      <div class="reveal" style="--d:.1s">
        <h2 id="ex-t">{x['titular']}</h2>
        <p>{x['texto']}</p>
        <a class="link-arrow" href="{WA}" target="_blank" rel="noopener">Escríbenos por WhatsApp {ICON('arrow-up-right')}</a>
      </div>
    </div>
  </section>''' if x else ""
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
          <a class="btn btn--ghost-light" href="#{e.get('ancla', 'estaciones')}">{e.get('ver', 'Ver las estaciones')}</a>
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

{rutas_mapa(e, creditos) if e.get("formato") == "mapa" else estaciones}

{extra}
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
    if "rmap" in main:  # mapas en 3D, solo en las páginas con rutas
        pie = pie.replace("</body>", '<script src="../assets/rutas3d.js" defer></script>\n</body>')
    return cab + main + pie

if __name__ == "__main__":
    os.makedirs(os.path.join(WEB, "experiencias"), exist_ok=True)
    cab, pie = concha()
    for slug, e in EXPERIENCIAS.items():
        open(os.path.join(WEB, "experiencias", f"{slug}.html"), "w").write(pagina(slug, e, cab, pie))
        print(f"experiencias/{slug}.html")
