// Mapas 3D de rutas: comprueba que se montan y vuelan, y guarda capturas: node mapa3d-test.js <n.º de mapa> <prefijo>
const p = require('puppeteer-core'); const W = ms => new Promise(r => setTimeout(r, ms));
(async () => {
  const i = +process.argv[2] - 1, out = process.argv[3];
  const b = await p.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: 'new', args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const pg = await b.newPage(); await pg.setViewport({ width: 1440, height: 900 }); const errs = [];
  pg.on('pageerror', e => errs.push(e.message)); pg.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await pg.goto((process.env.URL || 'http://localhost:4320/') + 'experiencias/senderismo-y-trekking.html', { waitUntil: 'networkidle2' });
  await pg.evaluate(i => { const m = document.querySelectorAll('.rmap')[i]; scrollTo(0, m.getBoundingClientRect().top + scrollY - 150); }, i);
  let t = 0; while (t < 40 && !(await pg.evaluate(i => document.querySelectorAll('.rmap')[i].classList.contains('is-3d'), i))) { await W(500); t++; }
  console.log('3D montado:', t < 40, `(${t / 2} s)`);
  const el = (await pg.$$('.rmap'))[i];
  for (const [n, ms] of [['a', 4000], ['b', 5000], ['c', 9000]]) {
    await W(ms); const km = await pg.evaluate(i => document.querySelectorAll('.rmap')[i].querySelector('.rmap__km').textContent, i);
    if (out) await el.screenshot({ path: `${out}-${n}.jpg`, type: 'jpeg', quality: 80 }); console.log(n, km);
  }
  console.log(errs.length ? errs.slice(0, 5) : 'sin errores'); await b.close();
})();
