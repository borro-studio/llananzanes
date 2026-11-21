// Mapas de rutas: se animan al verlos, sin errores; guarda capturas a mitad y al final
const p = require('puppeteer-core'); const W = ms => new Promise(r => setTimeout(r, ms));
(async () => {
  const U = (process.env.URL || 'http://localhost:4320/') + 'experiencias/senderismo-y-trekking.html', out = process.argv[2];
  const b = await p.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: 'new' });
  const pg = await b.newPage(); await pg.setViewport({ width: 1440, height: 900 }); const errs = []; pg.on('pageerror', e => errs.push(e.message));
  await pg.goto(U, { waitUntil: 'networkidle0' });
  const n = await pg.$$eval('.rmap', x => x.length);
  for (let i = 0; i < n; i++) {
    await pg.evaluate(i => { const m = document.querySelectorAll('.rmap')[i]; scrollTo(0, m.getBoundingClientRect().top + scrollY - 200); }, i);
    await W(1600); const el = (await pg.$$('.rmap'))[i];
    const mid = await pg.evaluate(i => document.querySelectorAll('.rmap')[i].querySelector('.rmap__km').textContent, i);
    if (out && i === 1) await el.screenshot({ path: `${out}-mitad.jpg`, type: 'jpeg', quality: 80 });
    await W(4500);
    const fin = await pg.evaluate(i => { const m = document.querySelectorAll('.rmap')[i]; return [m.querySelector('.rmap__km').textContent, m.querySelectorAll('.rmap__mk.is-on').length + '/' + m.querySelectorAll('.rmap__mk').length]; }, i);
    if (out) await el.screenshot({ path: `${out}-${i + 1}.jpg`, type: 'jpeg', quality: 80 });
    console.log(`mapa ${i + 1}: a 1,6 s ${mid} · al final ${fin[0]}, marcas ${fin[1]}`);
  }
  console.log(errs.length ? errs : 'sin errores'); await b.close();
})();
