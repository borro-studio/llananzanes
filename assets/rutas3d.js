/* Rutas en 3D: relieve real (Terrarium, AWS Open Data) en los tonos de la web y una cámara que sobrevuela la ruta
   mientras se dibuja. Sustituye al mapa plano (.rmap svg) solo si el navegador puede con WebGL; si no, queda el plano. */
(() => {
  const ASSETS = ((document.currentScript && document.currentScript.src) || "").replace(/rutas3d\.js(\?.*)?$/, "") || "../assets/";
  const LIB = "https://unpkg.com/maplibre-gl@4.7.1/dist/maplibre-gl";
  const mapas = [...document.querySelectorAll(".rmap[data-slug]")];
  const quieto = matchMedia("(prefers-reduced-motion: reduce)").matches || document.documentElement.classList.contains("static");
  if (!mapas.length || quieto) return;
  const webgl = (() => { try { const c = document.createElement("canvas"); return !!(c.getContext("webgl2") || c.getContext("webgl")); } catch (e) { return false; } })();
  if (!webgl) return;

  let lib, datos;
  const cargar = () => lib || (lib = Promise.all([
    new Promise((ok, ko) => { const l = document.createElement("link"); l.rel = "stylesheet"; l.href = LIB + ".css"; l.onload = ok; l.onerror = ko; document.head.appendChild(l); }),
    new Promise((ok, ko) => { const s = document.createElement("script"); s.src = LIB + ".js"; s.onload = ok; s.onerror = ko; document.head.appendChild(s); }),
    fetch(ASSETS + "mapas.json").then((r) => r.json()).then((d) => (datos = d)),
  ]));

  // geometría
  const R = 6371000, rad = Math.PI / 180;
  const dist = (a, b) => { const dLa = (b[1] - a[1]) * rad, dLo = (b[0] - a[0]) * rad; const h = Math.sin(dLa / 2) ** 2 + Math.cos(a[1] * rad) * Math.cos(b[1] * rad) * Math.sin(dLo / 2) ** 2; return 2 * R * Math.asin(Math.sqrt(h)); };
  const rumbo = (a, b) => { const y = Math.sin((b[0] - a[0]) * rad) * Math.cos(b[1] * rad), x = Math.cos(a[1] * rad) * Math.sin(b[1] * rad) - Math.sin(a[1] * rad) * Math.cos(b[1] * rad) * Math.cos((b[0] - a[0]) * rad); return Math.atan2(y, x) / rad; };
  const suave = (x) => (x < 0.5 ? 4 * x * x * x : 1 - (-2 * x + 2) ** 3 / 2);

  const iniciar = (m) => {
    const d = datos[m.dataset.slug], ll = d.ll;
    const acum = [0]; for (let i = 1; i < ll.length; i++) acum.push(acum[i - 1] + dist(ll[i - 1], ll[i]));
    const total = acum[acum.length - 1];
    const punto = (s) => { let i = 1; while (i < acum.length - 1 && acum[i] < s) i++; const t = (s - acum[i - 1]) / (acum[i] - acum[i - 1] || 1); return [ll[i - 1][0] + (ll[i][0] - ll[i - 1][0]) * t, ll[i - 1][1] + (ll[i][1] - ll[i - 1][1]) * t, i]; };
    const tramo = (s) => { const p = punto(s); return ll.slice(0, p[2]).concat([[p[0], p[1]]]); };
    const lon = ll.map((p) => p[0]), lat = ll.map((p) => p[1]);
    const caja = [[Math.min(...lon), Math.min(...lat)], [Math.max(...lon), Math.max(...lat)]];

    const caja3d = document.createElement("div"); caja3d.className = "rmap__3d"; (m.querySelector(".ruta__lienzo") || m).prepend(caja3d);
    // en las rutas a pantalla completa la tarjeta tapa la izquierda: la ruta se encuadra a la derecha
    const hueco = () => m.classList.contains("ruta") && innerWidth > 900 ? { left: m.clientWidth * 0.44, right: Math.min(360, m.clientWidth * 0.24), top: 150, bottom: 120 } : { left: 40, right: 40, top: 40, bottom: 40 };
    const map = new maplibregl.Map({
      container: caja3d, interactive: false, attributionControl: false, fadeDuration: 0, maxPitch: 75,
      bounds: caja, fitBoundsOptions: { padding: hueco() },
      style: {
        version: 8,
        sources: {
          sombra: { type: "raster-dem", tiles: ["https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png"], encoding: "terrarium", tileSize: 256, maxzoom: 13 },
          dem: { type: "raster-dem", tiles: ["https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png"], encoding: "terrarium", tileSize: 256, maxzoom: 13 },
          ruta: { type: "geojson", data: { type: "Feature", geometry: { type: "LineString", coordinates: [ll[0], ll[0]] } } },
          yo: { type: "geojson", data: { type: "Feature", geometry: { type: "Point", coordinates: ll[0] } } },
          todo: { type: "geojson", data: { type: "Feature", geometry: { type: "LineString", coordinates: ll } } },
        },
        layers: [
          { id: "fondo", type: "background", paint: { "background-color": "#d9dccf" } },
          { id: "sombras", type: "hillshade", source: "sombra", paint: { "hillshade-shadow-color": "#1d3025", "hillshade-highlight-color": "#f6f4ec", "hillshade-accent-color": "#5e6b55", "hillshade-exaggeration": 0.75, "hillshade-illumination-direction": 315 } },
          { id: "todo", type: "line", source: "todo", paint: { "line-color": "#15201a", "line-width": 2, "line-opacity": 0.25, "line-dasharray": [2, 2] } },
          { id: "halo", type: "line", source: "ruta", layout: { "line-cap": "round", "line-join": "round" }, paint: { "line-color": "#fff", "line-width": 9, "line-opacity": 0.9 } },
          { id: "linea", type: "line", source: "ruta", layout: { "line-cap": "round", "line-join": "round" }, paint: { "line-color": "#bd4d1b", "line-width": 5 } },
          { id: "yo-halo", type: "circle", source: "yo", paint: { "circle-radius": 15, "circle-color": "#bd4d1b", "circle-opacity": 0.25, "circle-pitch-alignment": "map" } },
          { id: "yo", type: "circle", source: "yo", paint: { "circle-radius": 8, "circle-color": "#bd4d1b", "circle-stroke-color": "#fff", "circle-stroke-width": 3, "circle-pitch-alignment": "map" } },
        ],
        terrain: { source: "dem", exaggeration: 1.35 },
      },
    });

    // marcas: sitios de la historia, la casa y el caminante
    const etiqueta = (txt, cls) => { const e = document.createElement("div"), sp = document.createElement("span"); e.className = "rmap3__mk " + cls; sp.textContent = txt; e.append(document.createElement("i"), sp); return e; };
    const marcas = d.marcas.map((k) => {
      let s = 0, best = Infinity; ll.forEach((p, i) => { const x = dist(p, k.ll); if (x < best) { best = x; s = acum[i]; } });
      const el = etiqueta(k.n, ""); return { el, s, mk: new maplibregl.Marker({ element: el, anchor: "left", offset: [-7, 0] }).setLngLat(k.ll).addTo(map) };
    });
    if (d.casa_ll) new maplibregl.Marker({ element: etiqueta("La casa", "is-casa is-on"), anchor: "left", offset: [-8, 0] }).setLngLat(d.casa_ll).addTo(map);

    const kmEl = m.querySelector(".rmap__km"), kmTot = d.km;
    let raf, giro = null;
    const vuelo = () => {
      cancelAnimationFrame(raf);
      const dur = 9000 + Math.min(total / 1000, 20) * 700, t0 = performance.now();
      const cam = map.cameraForBounds(caja, { padding: hueco() }), zoom = Math.min(13.4, (cam && cam.zoom ? cam.zoom : map.getZoom()) + 0.35);
      // el caminante va en el hueco libre (entre la tarjeta y la foto), no en el centro
      const ancho = m.clientWidth, desvio = m.classList.contains("ruta") && innerWidth > 900 ? [ancho * 0.10, 0] : [0, 0];
      const paso = (t) => {
        const x = Math.min(1, (t - t0) / dur), f = suave(x), s = total * f, p = punto(s);
        map.getSource("ruta").setData({ type: "Feature", geometry: { type: "LineString", coordinates: tramo(s) } });
        map.getSource("yo").setData({ type: "Feature", geometry: { type: "Point", coordinates: [p[0], p[1]] } });
        kmEl.textContent = (kmTot * f).toFixed(1).replace(".", ",") + ("num" in kmEl.dataset ? "" : " km");
        marcas.forEach((k) => k.el.classList.toggle("is-on", s >= k.s - 30));
        // la cámara mira hacia donde va la ruta (rumbo suavizado) y se acerca en el centro del recorrido
        const ade = punto(Math.min(total, s + total * 0.06)), objetivo = rumbo([p[0], p[1]], [ade[0], ade[1]]);
        if (giro === null) giro = objetivo;
        let dif = ((objetivo - giro + 540) % 360) - 180; giro += dif * 0.035;
        const cerca = Math.sin(Math.PI * Math.min(1, x * 1.15));
        map.easeTo({ center: [p[0], p[1]], offset: desvio, bearing: giro, pitch: 42 + 16 * cerca, zoom: zoom - 0.8 + 0.8 * cerca, duration: 0 });
        if (x < 1) raf = requestAnimationFrame(paso);
        else {
          // vista final de toda la ruta, algo más abierta para que la inclinación no corte el fondo
          const fin = map.cameraForBounds(caja, { padding: hueco(), bearing: giro });
          map.easeTo({ center: fin.center, zoom: fin.zoom - 0.45, bearing: giro, pitch: 40, padding: { left: 0, right: 0, top: 0, bottom: 0 }, offset: m.classList.contains("ruta") && innerWidth > 900 ? [m.clientWidth * 0.10, 0] : [0, 0], duration: 2200 });
        }
      };
      raf = requestAnimationFrame(paso);
    };
    map.on("load", () => {
      m.classList.add("is-3d");
      map.once("idle", () => {
        new IntersectionObserver((es, io) => es.forEach((e) => { if (e.isIntersecting) { vuelo(); io.disconnect(); } }), { threshold: 0.5 }).observe(m);
      });
    });
    m.querySelector(".rmap__otra").addEventListener("click", (e) => { if (m.classList.contains("is-3d")) { e.stopImmediatePropagation(); giro = null; map.fitBounds(caja, { padding: hueco(), pitch: 0, bearing: 0, duration: 0 }); vuelo(); } }, true);
  };

  // se carga la librería al acercarse a la primera ruta y cada mapa se monta al acercarse a él
  const io = new IntersectionObserver((es) => es.forEach((e) => {
    if (!e.isIntersecting) return; io.unobserve(e.target);
    cargar().then(() => iniciar(e.target)).catch(() => {});
  }), { rootMargin: "600px 0px" });
  mapas.forEach((m) => io.observe(m));
})();
