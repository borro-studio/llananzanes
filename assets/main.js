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

  // Vídeo de portada: arranca al entrar (o al cargar si no hay pantalla de entrada)
  const vid = document.querySelector(".hero__video");
  const playVideo = () => {
    if (!vid || reduce || root.classList.contains("flat") || (navigator.connection && navigator.connection.saveData)) return;
    if (!vid.src) {
      // móvil vertical: recorte propio; pantallas grandes o retina: 1080p; resto: 720p
      const big = innerWidth * (devicePixelRatio || 1) >= 1700;
      vid.src = "assets/video/" + (matchMedia("(max-width: 700px)").matches ? "portada-movil.mp4" : big ? "portada-1080.mp4" : "portada.mp4");
    }
    vid.addEventListener("playing", () => vid.classList.add("is-on"), { once: true });
    vid.play().catch(() => {});
  };

  // Sonido: ambiente del valle en bucle y, al entrar, música + saludo con el nombre + locución.
  const sb = document.querySelector(".sound");
  if (sb && !root.classList.contains("flat")) {
    const KEY = "mll-sonido-2", DIR = "assets/audio/";
    const get = (st, k) => { try { return st.getItem(k); } catch (e) { return null; } };
    const set = (st, k, v) => { try { st.setItem(k, v); } catch (e) {} };
    const mk = (f, loop) => { const a = new Audio(DIR + f); a.preload = "auto"; a.loop = !!loop; return a; };
    const amb = mk("ambiente.mp3", true), mus = mk("musica.mp3"), loc = mk("locucion.mp3");
    amb.volume = 0;
    // Saludos pregrabados ("Hola… Nombre."). Todos duran lo mismo y acaban en el mismo instante,
    // así que música, saludo y locución arrancan a la vez en el mismo gesto y quedan sincronizados.
    let names = new Set(), sal = mk("saludos/generico.mp3"), salKey = "generico";
    fetch(DIR + "saludos/index.json").then((r) => r.json()).then((l) => { names = new Set(l); }).catch(() => {});
    const keyOf = (txt) => {
      const k = (txt || "").trim().split(/\s+/)[0].toLowerCase().normalize("NFD").replace(/[^a-z]/g, "");
      return names.has(k) ? k : "generico";
    };
    const useGreeting = (txt) => {
      const k = keyOf(txt);
      if (k !== salKey) { salKey = k; sal = mk("saludos/" + k + ".mp3"); }
    };
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
      sb.querySelector(".sound__label").textContent = on ? "" : "Activar sonido";
    };
    // Todos los play() se lanzan en la misma llamada, sin esperar entre ellos:
    // Safari solo permite arrancar un audio dentro del propio gesto del usuario.
    // Un toque dispara varios eventos seguidos y los primeros aún no cuentan como gesto:
    // cada intento lleva su número para que uno fallido no pare lo que otro posterior ya arrancó.
    let attempt = 0, vozDone = false;
    loc.addEventListener("ended", () => { vozDone = true; });
    const seq = () => [mus, sal, loc];
    const start = () => {
      if (on) return Promise.resolve(true);
      if (muted) return Promise.resolve(false);
      const id = ++attempt;
      const pa = amb.play();
      if (!vozDone) seq().forEach((a) => { if (!a.ended) a.play().catch(() => {}); });
      return pa.then(() => { if (!on) { on = true; fadeTo(0.45); ui(); } return true; })
               .catch(() => { if (id === attempt && !on) seq().forEach((a) => { a.pause(); a.currentTime = 0; }); return false; });
    };
    const stop = () => { on = false; vozDone = true; seq().forEach((a) => a.pause()); fadeTo(0); ui(); };
    sb.addEventListener("click", () => {
      if (on) { muted = true; set(localStorage, KEY, "off"); stop(); }
      else { muted = false; set(localStorage, KEY, "on"); start(); }
    });
    // Si el navegador bloquea el sonido al cargar, arranca con el primer toque o tecla
    const autoStart = () => start().then((ok) => {
      if (ok || muted) return;
      const evs = ["pointerdown", "pointerup", "mousedown", "touchend", "click", "keydown"];
      const first = (e) => {
        if (e.target.closest && e.target.closest(".sound")) return;
        start().then((ok2) => { if (ok2) evs.forEach((n) => removeEventListener(n, first, true)); });
      };
      evs.forEach((n) => addEventListener(n, first, true));
    });
    // Pantalla de entrada: el clic en "Entrar" es el gesto que los navegadores exigen para sonar
    const intro = document.querySelector(".intro");
    if (intro && !root.classList.contains("entered")) {
      const input = intro.querySelector(".intro__input"), hello = document.querySelector(".hero__hello");
      let t = 0;
      input.addEventListener("input", () => { clearTimeout(t); t = setTimeout(() => useGreeting(input.value), 250); });
      const enter = (withSound) => {
        const name = input.value.trim().replace(/\s+/g, " ").slice(0, 24);
        useGreeting(name);
        root.classList.add("entered");
        muted = !withSound;
        set(localStorage, KEY, withSound ? "on" : "off");
        if (withSound) start(); else ui();
        playVideo();
        if (name && hello && /^[\p{L} .'-]+$/u.test(name)) {
          hello.textContent = "Hola, " + name.toLowerCase().replace(/(^|[\s-])\p{L}/gu, (c) => c.toUpperCase()) + ".";
          setTimeout(() => hello.classList.add("is-on"), 900);
        }
        input.blur();
        setTimeout(() => intro.remove(), 1100);
      };
      intro.querySelector("form").addEventListener("submit", (e) => { e.preventDefault(); enter(true); });
      intro.querySelector(".intro__mute").addEventListener("click", () => enter(false));
    } else { autoStart(); playVideo(); }
    document.addEventListener("visibilitychange", () => {
      if (!on) return;
      if (document.hidden) { amb.pause(); seq().forEach((a) => a.pause()); }
      else { amb.play().catch(() => {}); if (!vozDone) seq().forEach((a) => { if (!a.ended && a.currentTime > 0) a.play().catch(() => {}); }); }
    });
    ui();
  } else playVideo();

})();
