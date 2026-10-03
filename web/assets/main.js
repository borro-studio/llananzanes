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

})();
