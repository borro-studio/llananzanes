#!/usr/bin/env python3
"""Maquetas de tres formas de presentar las rutas (A, B, C) para elegir. Genera _maquetas/rutas.html."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
M = json.load(open(os.path.join(HERE, "..", "web", "assets", "mapas.json")))
A = "../web/assets/"

R = [
    dict(slug="pena-mea", n="Peña Mea", foto="ruta-pena-mea", d3="mea", km="5,9", sube="983", alto="1.557", salida="Pelúgano", sub="Hasta la cumbre",
         res="Casi 1.000 metros de subida entre aldeas, cabañas y fuentes hasta el Ojo de Buey, un ventanal de roca de 20 metros que atraviesa la cresta de la peña. El fotógrafo holandés Gijs de Reijke pasó cuatro años preparando una foto imposible: el eclipse de 2026 encajado justo dentro de él."),
    dict(slug="foces-del-pino", n="Foces del Pino", foto="ruta-foces-del-pino", d3="foces", km="18,2", sube="1.074", alto="1.538", salida="Casomera, junto a la casa", sub="PR-AS 31",
         res="El río Pino tardó milenios en tallar este desfiladero: en algunos puntos sus paredes de caliza dejan menos de 6 metros de paso y guardan fósiles marinos de más de 300 millones de años. Su sendero es una antigua calzada romana que aún usan los vaqueros."),
    dict(slug="gumial", n="El Gumial", foto="ruta-gumial", d3="gumial", km="9,2", sube="894", alto="1.620", salida="Cuevas", sub="PR-AS 48",
         res="Desde Cuevas, uno de los hayedos más cerrados de Asturias sube hasta la braña del Gumial por un paso que ya se usaba hace más de 3.000 años: aquí aparecieron dos puñales de la Edad del Bronce. Arriba esperan las cabañas de piedra de la trashumancia."),
]

def svg_mapa(slug, cls=""):
    m = M[slug]
    mk = "".join(f'<g><circle cx="{k["x"]}" cy="{k["y"]}" r="10" fill="#15201a" stroke="#fff" stroke-width="4"/><text x="{k["x"] + 18}" y="{k["y"] + 8}" class="lbl">{k["n"]}</text></g>' for k in m["marcas"])
    return f'''<svg class="{cls}" viewBox="0 0 {m["w"]} {m["h"]}" preserveAspectRatio="xMidYMid slice"><image href="{A}img/mapa-{slug}.jpg" width="{m["w"]}" height="{m["h"]}"/>
      <path d="{m["d"]}" fill="none" stroke="#fff" stroke-width="14" stroke-linecap="round" stroke-linejoin="round" opacity=".85"/><path d="{m["d"]}" fill="none" stroke="#bd4d1b" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>{mk}</svg>'''

def perfil(slug, w=360, h=90):
    z = M[slug]["perfil"]; lo, hi = 500, 1700
    pts = [(i * w / (len(z) - 1), h - (v - lo) / (hi - lo) * h) for i, v in enumerate(z)]
    line = " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    return f'''<svg class="perfil" viewBox="0 0 {w} {h}" preserveAspectRatio="none"><path d="M0,{h} L{line} L{w},{h} Z" fill="#e0a62c" opacity=".35"/><path d="M{line}" fill="none" stroke="#bd4d1b" stroke-width="2"/></svg>'''

def dato(v, u, t): return f'<div class="dt"><b>{v}<small>{u}</small></b><span>{t}</span></div>'

# A · el mapa como protagonista
r = R[0]
A_html = f'''<section class="va">
  {svg_mapa(r["slug"], "va__map")}
  <div class="va__veil"></div>
  <div class="wrap va__in">
    <div class="va__card">
      <span class="eyebrow">01 · Rutas con historia</span>
      <h3>{r["n"]}</h3>
      <p>{r["res"]}</p>
      <div class="dts">{dato(r["km"], " km", r["sub"])}{dato(r["sube"], " m", "Desnivel")}{dato(r["alto"], " m", "Cumbre")}</div>
      <a class="btn btn--solid">Cómo llegar desde la casa</a>
    </div>
    <figure class="va__foto"><img src="{A}img/{r["foto"]}.jpg"><figcaption>El Ojo de Buey</figcaption></figure>
  </div>
  <div class="va__nav"><span class="on">01 Peña Mea</span><span>02 Foces del Pino</span><span>03 El Gumial</span></div>
</section>'''

# B · un solo mapa con selector
act = R[1]
lista = ""
for i, r in enumerate(R):
    if r is act:
        lista += f'''<div class="vb__it on"><span class="vb__n">0{i + 1}</span><h3>{r["n"]}</h3><p>{r["res"]}</p>
          <div class="dts">{dato(r["km"], " km", r["sub"])}{dato(r["sube"], " m", "Desnivel")}{dato(r["alto"], " m", "Punto más alto")}</div>
          <p class="vb__casa">● Sale a 700 m de la casa: se empieza andando.</p></div>'''
    else:
        lista += f'<div class="vb__it"><span class="vb__n">0{i + 1}</span><h3>{r["n"]}</h3><span class="vb__mini">{r["km"]} km · +{r["sube"]} m</span></div>'
B_html = f'''<section class="vb"><div class="wrap">
  <div class="floor__head"><h2>Rutas con <em>historia.</em></h2><span class="eyebrow">Elige una ruta</span></div>
  <div class="vb__grid"><div class="vb__lista">{lista}</div>
  <div class="vb__map"><img src="3d-{act["d3"]}.jpg"><div class="vb__bar"><span>{act["km"]} km</span><span>+{act["sube"]} m</span><span class="vb__3d">Vista 3D · arrastra para girar</span></div></div></div>
</div></section>'''

# C · tres fichas en paralelo con perfil de desnivel
fichas = ""
for i, r in enumerate(R):
    fichas += f'''<article class="vc__f"><div class="vc__img"><img src="{A}img/{r["foto"]}.jpg"><span>0{i + 1}</span></div>
      <h3>{r["n"]}</h3><p>{r["res"]}</p>
      <div class="dts">{dato(r["km"], " km", r["sub"])}{dato(r["sube"], " m", "Desnivel")}{dato(r["alto"], " m", "Máx.")}</div>
      {perfil(r["slug"])}<div class="vc__ax"><span>Salida: {r["salida"]}</span><span>{r["km"]} km</span></div>
      <a class="link-arrow">Ver la ruta en el mapa ↗</a></article>'''
C_html = f'''<section class="vc"><div class="wrap">
  <div class="floor__head"><h2>Rutas con <em>historia.</em></h2><span class="eyebrow">Aller de historias</span></div>
  <div class="vc__grid">{fichas}</div></div></section>'''

html = f'''<!doctype html><html lang="es" class="static"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="stylesheet" href="{A}styles.css"><style>
body {{ background: var(--bg); }}
.dts {{ display: flex; gap: 28px; margin: 22px 0 26px; }}
.dt b {{ display: block; font: 500 40px/1 var(--f-display); }} .dt small {{ font-size: .5em; margin-left: 3px; }}
.dt span {{ display: block; margin-top: 6px; font-size: 12px; letter-spacing: .12em; text-transform: uppercase; opacity: .7; }}
.lbl {{ font: 600 26px var(--f-text); fill: #15201a; paint-order: stroke; stroke: #fff; stroke-width: 8px; }}
/* A */
.va {{ position: relative; height: 860px; overflow: hidden; color: #eef0e6; }}
.va__map {{ position: absolute; inset: 0; width: 100%; height: 100%; }}
.va__veil {{ position: absolute; inset: 0; background: linear-gradient(90deg, rgba(21,32,26,.94) 0%, rgba(21,32,26,.85) 34%, rgba(21,32,26,0) 62%); }}
.va__in {{ position: relative; height: 100%; display: flex; align-items: center; justify-content: space-between; }}
.va__card {{ max-width: 500px; }} .va__card h3 {{ font-size: 96px; line-height: .95; margin: 16px 0 22px; }} .va__card p {{ color: #c9d1c9; }}
.va .eyebrow {{ color: #e3a92b; }}
.va__foto {{ align-self: flex-end; margin: 0 0 90px; width: 260px; background: #fff; padding: 10px 10px 8px; transform: rotate(2deg); box-shadow: 0 20px 50px rgba(0,0,0,.35); }}
.va__foto img {{ aspect-ratio: 4/5; object-fit: cover; width: 100%; }} .va__foto figcaption {{ color: #15201a; font-size: 13px; padding-top: 8px; }}
.va__nav {{ position: absolute; left: 0; right: 0; bottom: 0; display: flex; gap: 0; background: rgba(21,32,26,.9); }}
.va__nav span {{ flex: 1; padding: 18px 56px; font-weight: 600; font-size: 14px; opacity: .55; border-top: 3px solid transparent; }}
.va__nav .on {{ opacity: 1; border-color: #bd4d1b; }}
/* B */
.vb {{ padding: 120px 0; }} .vb__grid {{ display: grid; grid-template-columns: 5fr 7fr; gap: 56px; margin-top: 40px; align-items: start; }}
.vb__it {{ border-top: 1px solid var(--line); padding: 22px 0; display: grid; grid-template-columns: 48px 1fr; align-items: baseline; }}
.vb__it > *:not(.vb__n) {{ grid-column: 2; }}
.vb__it h3 {{ font-size: 34px; }} .vb__it.on h3 {{ font-size: 56px; }} .vb__n {{ font-size: 12px; letter-spacing: .2em; color: var(--accent); font-weight: 600; }}
.vb__it p {{ color: var(--ink-2); margin-top: 14px; }} .vb__mini {{ color: var(--ink-2); font-size: 14px; }}
.vb__it:not(.on) {{ opacity: .6; }} .vb__casa {{ font-size: 14px; color: #bd4d1b !important; font-weight: 600; }}
.vb__map {{ position: sticky; top: 100px; }} .vb__map img {{ width: 100%; aspect-ratio: 4/3; object-fit: cover; display: block; }}
.vb__bar {{ display: flex; gap: 22px; padding: 14px 18px; background: #15201a; color: #eef0e6; font-size: 14px; }} .vb__3d {{ margin-left: auto; opacity: .7; }}
/* C */
.vc {{ padding: 120px 0; }} .vc__grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 32px; margin-top: 44px; }}
.vc__f {{ background: #fff; padding: 0 0 26px; }} .vc__f > *:not(.vc__img) {{ margin-left: 26px; margin-right: 26px; }}
.vc__img {{ position: relative; }} .vc__img img {{ width: 100%; aspect-ratio: 4/3; object-fit: cover; display: block; }}
.vc__img span {{ position: absolute; top: 16px; left: 16px; background: #bd4d1b; color: #fff; font-weight: 600; font-size: 13px; padding: 6px 10px; }}
.vc__f h3 {{ font-size: 44px; margin-top: 24px; }} .vc__f p {{ color: var(--ink-2); font-size: 15px; margin-top: 12px; }}
.vc__f .dts {{ gap: 18px; }} .vc__f .dt b {{ font-size: 30px; }}
.perfil {{ display: block; width: calc(100% - 52px); height: 90px; }}
.vc__ax {{ display: flex; justify-content: space-between; font-size: 12px; color: var(--ink-2); margin-top: 6px; margin-bottom: 20px; }}
.tag {{ font: 700 14px var(--f-text); background: #e0a62c; color: #15201a; padding: 10px 16px; display: inline-block; letter-spacing: .1em; }}
</style></head><body>
<div id="A">{A_html}</div><div id="B">{B_html}</div><div id="C">{C_html}</div></body></html>'''
open(os.path.join(HERE, "rutas.html"), "w").write(html)
print("ok")
