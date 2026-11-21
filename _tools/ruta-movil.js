// Recorre en móvil la sección de rutas y guarda una captura por pantalla: node ruta-movil.js <prefijo>
const p = require('puppeteer-core'); const W = ms => new Promise(r => setTimeout(r, ms));
(async () => {
  const out = process.argv[2];
  const b = await p.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: 'new', args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const pg = await b.newPage(); await pg.setViewport({ width: 390, height: 844, deviceScaleFactor: 2, isMobile: true, hasTouch: true });
  await pg.goto((process.env.URL || 'http://localhost:4320/') + 'experiencias/senderismo-y-trekking.html', { waitUntil: 'networkidle2' });
  const y0 = await pg.evaluate(() => document.querySelector('.ruta').getBoundingClientRect().top + scrollY - 70);
  const y1 = await pg.evaluate(() => { const r = document.querySelectorAll('.ruta')[1]; return r.getBoundingClientRect().top + scrollY; });
  let n = 0;
  for (let y = y0; y < y1 + 300; y += 700) {
    await pg.evaluate(y => scrollTo(0, y), y); await W(n === 0 ? 14000 : 1500);
    await pg.screenshot({ path: `${out}-${++n}.jpg`, type: 'jpeg', quality: 75 });
  }
  console.log(n, 'capturas'); await b.close();
})();
