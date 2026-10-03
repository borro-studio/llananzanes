(() => {
  const root = document.documentElement;
  const q = new URLSearchParams(location.search);
  if (q.has("static")) root.classList.add("static");
  const theme = q.get("theme");
  if (theme === "light" || theme === "dark") root.dataset.theme = theme;
  root.classList.add("js");

  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches || q.has("static");

  // Nav: sólida en cuanto el hero deja de verse
  const nav = document.querySelector(".nav");
  const hero = document.querySelector(".hero");
  new IntersectionObserver(([e]) => nav.classList.toggle("is-solid", !e.isIntersecting), {
    rootMargin: `-${nav.offsetHeight}px 0px 0px 0px`,
  }).observe(hero);

  // Menú móvil
  const menu = document.querySelector(".menu");
  const burger = document.querySelector(".nav__burger");
  const setMenu = (open) => {
    menu.classList.toggle("is-open", open);
    burger.setAttribute("aria-expanded", open);
    document.body.style.overflow = open ? "hidden" : "";
  };
  burger.addEventListener("click", () => setMenu(true));
  menu.querySelector(".menu__close").addEventListener("click", () => setMenu(false));
  menu.querySelectorAll("a").forEach((a) => a.addEventListener("click", () => setMenu(false)));
  addEventListener("keydown", (e) => e.key === "Escape" && setMenu(false));

  // Manifiesto: cada palabra en su span para el revelado ligado al scroll
  document.querySelectorAll(root.classList.contains("flat") ? "[data-none]" : "[data-words]").forEach((el) => {
    el.childNodes.forEach((node) => {
      if (node.nodeType !== 3 || !node.textContent.trim()) return;
      const frag = document.createDocumentFragment();
      node.textContent.split(/(\s+)/).forEach((part) => {
        if (!part) return;
        if (/^\s+$/.test(part)) return frag.append(part);
        const s = document.createElement("span");
        s.className = "w";
        s.textContent = part;
        frag.append(s);
      });
      node.replaceWith(frag);
    });
  });

  // Apariciones al entrar en pantalla
  const io = new IntersectionObserver(
    (entries) => entries.forEach((e) => e.isIntersecting && (e.target.classList.add("in"), io.unobserve(e.target))),
    { rootMargin: "0px 0px -12% 0px" }
  );
  document.querySelectorAll(".reveal").forEach((el) => io.observe(el));

  // Sonido: ambiente del valle en bucle y locución una vez por visita.
  // Se intenta al cargar; si el navegador lo bloquea, arranca con el primer toque o tecla.
  const sb = document.querySelector(".sound");
  if (sb && !root.classList.contains("flat")) {
    const KEY = "mll-sonido", VOZ = "mll-voz";
    const get = (st, k) => { try { return st.getItem(k); } catch (e) { return null; } };
    const set = (st, k, v) => { try { st.setItem(k, v); } catch (e) {} };
    const amb = new Audio("assets/audio/ambiente.mp3");
    const voz = new Audio("assets/audio/voz.mp3");
    amb.loop = true; amb.volume = 0; amb.preload = "auto"; voz.preload = "auto";
    let on = false, muted = get(localStorage, KEY) === "off", fade = 0, lvl = 0;
    // El nivel se lleva en `lvl` y no se lee de amb.volume: en iOS el volumen es de solo lectura.
    const fadeTo = (target) => {
      clearInterval(fade);
      fade = setInterval(() => {
        const d = target - lvl;
        lvl = Math.abs(d) < 0.03 ? target : lvl + Math.sign(d) * 0.03;
        amb.volume = lvl;
        if (lvl === target) { clearInterval(fade); if (!target) amb.pause(); }
      }, 60);
    };
    const ui = () => {
      sb.classList.toggle("is-on", on);
      sb.setAttribute("aria-pressed", on);
      sb.setAttribute("aria-label", on ? "Silenciar sonido" : "Activar sonido");
    };
    // Los dos play() se lanzan en la misma llamada, sin esperar entre ellos:
    // Safari solo permite arrancar un audio dentro del propio gesto del usuario.
    // Un toque dispara varios eventos seguidos y los primeros aún no cuentan como gesto:
    // cada intento lleva su número para que uno fallido no pare lo que otro posterior ya arrancó.
    let attempt = 0;
    const start = () => {
      if (on) return Promise.resolve(true);
      if (muted) return Promise.resolve(false);
      const id = ++attempt;
      const pa = amb.play();
      if (get(sessionStorage, VOZ) !== "1") voz.play().then(() => set(sessionStorage, VOZ, "1")).catch(() => {});
      return pa.then(() => { if (!on) { on = true; fadeTo(0.45); ui(); } return true; })
               .catch(() => { if (id === attempt && !on) voz.pause(); return false; });
    };
    const stop = () => { on = false; voz.pause(); fadeTo(0); ui(); };
    sb.addEventListener("click", () => {
      if (on) { muted = true; set(localStorage, KEY, "off"); stop(); }
      else { muted = false; set(localStorage, KEY, "on"); start(); }
    });
    start().then((ok) => {
      if (ok || muted) return;
      const evs = ["pointerdown", "pointerup", "mousedown", "touchend", "click", "keydown"];
      const first = (e) => {
        if (e.target.closest && e.target.closest(".sound")) return;
        start().then((ok2) => { if (ok2) evs.forEach((n) => removeEventListener(n, first, true)); });
      };
      evs.forEach((n) => addEventListener(n, first, true));
    });
    document.addEventListener("visibilitychange", () => {
      if (!on) return;
      if (document.hidden) { amb.pause(); voz.pause(); } else amb.play().catch(() => {});
    });
    ui();
  }

})();
