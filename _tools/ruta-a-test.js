// Rutas a pantalla completa: captura una ruta a mitad de vuelo y al final: node ruta-a-test.js <n.º> <prefijo> [movil]
const p = require('puppeteer-core'); const W = ms => new Promise(r => setTimeout(r, ms));
(async () => {
  const i = +process.argv[2] - 1, out = process.argv[3], movil = process.argv[4] === 'movil';
  const b = await p.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: 'new', args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const pg = await b.newPage(); await pg.setViewport(movil ? { width: 390, height: 844, deviceScaleFactor: 2, isMobile: true, hasTouch: true } : { width: 1440, height: 900 });
  const errs = []; pg.on('pageerror', e => errs.push(e.message));
  await pg.goto((process.env.URL || 'http://localhost:4320/') + 'experiencias/senderismo-y-trekking.html', { waitUntil: 'networkidle2' });
  await pg.evaluate(i => document.querySelectorAll('.ruta')[i].scrollIntoView(), i);
  let t = 0; while (t < 40 && !(await pg.evaluate(i => document.querySelectorAll('.ruta')[i].classList.contains('is-3d'), i))) { await W(500); t++; }
  await pg.evaluate(i => document.querySelectorAll('.ruta')[i].scrollIntoView(), i);
  for (const [n, ms] of [['mitad', 6000], ['final', 16000]]) {
    await W(ms); const km = await pg.evaluate(i => document.querySelectorAll('.ruta')[i].querySelector('.rmap__km').textContent, i);
    await pg.screenshot({ path: `${out}-${n}.jpg`, type: 'jpeg', quality: 80 }); console.log(n, km);
  }
  console.log('3D:', t < 40, errs.length ? errs : 'sin errores'); await b.close();
})();
