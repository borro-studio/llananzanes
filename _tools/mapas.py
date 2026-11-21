#!/usr/bin/env python3
"""Mapas animados de las rutas de senderismo.
Toma el trazado de cada ruta (OpenStreetMap / BRouter, guardado en _gen/rutas), lo ordena,
calcula distancia y desnivel, descarga el fondo topográfico (OpenTopoMap, con caché) y genera:
  web/assets/img/mapa-<slug>.jpg   fondo del mapa, en tonos de la web
  web/assets/mapas.json            trazado en píxeles del mapa + puntos + datos, para experiencias.py
Fondo: © OpenStreetMap contributors, SRTM | OpenTopoMap (CC BY-SA)."""
import json, math, os, io, time, subprocess, urllib.request
from PIL import Image, ImageEnhance, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "_gen", "rutas")
CACHE = os.path.join(SRC, "tiles")
OUT_IMG = os.path.join(ROOT, "web", "assets", "img")
CASA = (43.0645974, -5.5755936)
UA = "BorroStudio-web/1.0 (mapas de rutas)"
W, H = 1200, 900  # tamaño del mapa (4:3)

RUTAS = {
    "pena-mea": dict(fuente="penamea.geojson", puntos=[("Pelúgano", "ini"), ("Ojo de Buey", (43.1729584, -5.5670796)), ("Peña Mea · 1.557 m", "fin")]),
    "foces-del-pino": dict(fuente="foces.json", puntos=[("Casomera", "ini"), ("Valle de Caniecha", (43.1026248, -5.5327233), "izq"), ("Felechosa", "fin")]),
    "gumial": dict(fuente="gumial.json", invertir=True, puntos=[("Cuevas", "ini"), ("Braña del Gumial", (43.0675473, -5.4642072)), ("Los Coḷḷainos", "fin")]),
}

def dist(a, b):
    R = 6371000; la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 2 * R * math.asin(math.sqrt(h))

def ordenar(ways):
    """Une los tramos de una relación de OSM en una sola línea; prueba a empezar por cada tramo y se queda con la más larga."""
    ways = [list(w) for w in ways if len(w) > 1]
    largo = lambda l: sum(dist(l[i], l[i + 1]) for i in range(len(l) - 1))
    return max((encadenar(ways, i) for i in range(len(ways))), key=largo)

def encadenar(ways, inicio):
    ways = [list(w) for w in ways]
    linea = ways.pop(inicio)
    while ways:
        mejor = None
        for i, w in enumerate(ways):
            for inv_l in (False, True):
                for inv_w in (False, True):
                    a = linea[0] if inv_l else linea[-1]
                    b = w[-1] if inv_w else w[0]
                    d = dist(a, b)
                    if mejor is None or d < mejor[0]:
                        mejor = (d, i, inv_l, inv_w)
        d, i, inv_l, inv_w = mejor
        if d > 300:  # tramo suelto (variante o ramal): se descarta
            ways.pop(i); continue
        w = ways.pop(i)
        if inv_w: w = w[::-1]
        if inv_l: linea = linea[::-1]
        linea += w
    return linea

def leer(fuente):
    p = os.path.join(SRC, fuente)
    if fuente.endswith(".geojson"):
        c = json.load(open(p))["features"][0]["geometry"]["coordinates"]
        return [(y, x) for x, y, *_ in c], [z for *_, z in c]
    rel = json.load(open(p))["elements"][0]
    ways = [[(g["lat"], g["lon"]) for g in m["geometry"]] for m in rel["members"] if m["type"] == "way" and m.get("geometry")]
    return ordenar(ways), None

def alturas(pts):
    """Altitud punto a punto (modelo de terreno EU-DEM 25 m, OpenTopoData), un punto cada ~50 m."""
    muestra, acum = [pts[0]], 0
    for a, b in zip(pts, pts[1:]):
        acum += dist(a, b)
        if acum >= 50: muestra.append(b); acum = 0
    zs = []
    for i in range(0, len(muestra), 100):
        locs = "|".join(f"{la:.6f},{lo:.6f}" for la, lo in muestra[i:i + 100])
        r = subprocess.run(["curl", "-s", f"https://api.opentopodata.org/v1/eudem25m?locations={locs}"], capture_output=True, text=True)
        zs += [x["elevation"] for x in json.loads(r.stdout)["results"]]
        time.sleep(1.1)
    return zs

def desnivel(zs, umbral=8):
    sube, ref = 0, zs[0]
    for z in zs[1:]:
        if z > ref + umbral: sube += z - ref; ref = z
        elif z < ref - umbral: ref = z
    return sube

def merc(la, lo, z):
    n = 2 ** z; x = (lo + 180) / 360 * n
    y = (1 - math.log(math.tan(math.radians(la)) + 1 / math.cos(math.radians(la))) / math.pi) / 2 * n
    return x * 256, y * 256

def tesela(z, x, y):
    os.makedirs(CACHE, exist_ok=True)
    f = os.path.join(CACHE, f"{z}-{x}-{y}.png")
    if not os.path.exists(f):
        url = f"https://{'abc'[(x + y) % 3]}.tile.opentopomap.org/{z}/{x}/{y}.png"
        data = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=60).read()
        open(f, "wb").write(data); time.sleep(0.3)
    return Image.open(f).convert("RGB")

def mapa(slug, pts):
    la = [p[0] for p in pts]; lo = [p[1] for p in pts]
    # zoom más alto en el que la ruta cabe con margen
    for z in range(16, 11, -1):
        x0, y1 = merc(min(la), min(lo), z); x1, y0 = merc(max(la), max(lo), z)
        if (x1 - x0) < W * 0.72 and (y1 - y0) < H * 0.72: break
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    ox, oy = cx - W / 2, cy - H / 2
    img = Image.new("RGB", (W, H))
    for tx in range(int(ox // 256), int((ox + W) // 256) + 1):
        for ty in range(int(oy // 256), int((oy + H) // 256) + 1):
            img.paste(tesela(z, tx, ty), (int(tx * 256 - ox), int(ty * 256 - oy)))
    # tono de la web: menos color, cálido y claro
    img = ImageEnhance.Color(img).enhance(0.35)
    img = Image.blend(img, Image.new("RGB", (W, H), (236, 238, 231)), 0.28)
    img.save(os.path.join(OUT_IMG, f"mapa-{slug}.jpg"), quality=80, optimize=True, progressive=True)
    px = lambda p: (round(merc(p[0], p[1], z)[0] - ox, 1), round(merc(p[0], p[1], z)[1] - oy, 1))
    return z, px

def main():
    datos = {}
    for slug, r in RUTAS.items():
        pts, zs = leer(r["fuente"])
        if r.get("invertir"): pts = pts[::-1]
        km = sum(dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1)) / 1000
        if zs is None: zs = alturas(pts)
        z, px = mapa(slug, pts)
        camino = [px(p) for p in pts]
        d = "M" + " L".join(f"{x},{y}" for x, y in camino)
        marcas = []
        for nombre, donde, *lado in r["puntos"]:
            p = pts[0] if donde == "ini" else pts[-1] if donde == "fin" else min(pts, key=lambda q: dist(q, donde))
            x, y = px(p); marcas.append(dict(n=nombre, x=x, y=y, izq=bool(lado)))
        cx, cy = px(CASA)
        casa = dict(x=cx, y=cy) if 0 < cx < W and 0 < cy < H else None
        cerca = min(dist(CASA, p) for p in pts)
        datos[slug] = dict(w=W, h=H, d=d, marcas=marcas, casa=casa, km=round(km, 1),
                           sube=round(desnivel(zs)), zmin=round(min(zs)), zmax=round(max(zs)), casa_m=round(cerca))
        print(f"{slug}: {km:.1f} km, +{datos[slug]['sube']} m ({datos[slug]['zmin']}–{datos[slug]['zmax']} m), zoom {z}, "
              f"a {cerca/1000:.1f} km de la casa{', casa en el mapa' if casa else ''}")
    json.dump(datos, open(os.path.join(ROOT, "web", "assets", "mapas.json"), "w"), ensure_ascii=False)

if __name__ == "__main__":
    main()
