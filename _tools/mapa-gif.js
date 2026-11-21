// Graba en GIF la animación de un mapa de ruta: node mapa-gif.js <n.º de mapa> <salida.gif> <carpeta de fotogramas>
const p = require('puppeteer-core'), fs = require('fs'), { execFileSync } = require('child_process');
(async () => {
  const i = +process.argv[2] - 1, out = process.argv[3], tmp = process.argv[4]; fs.mkdirSync(tmp, { recursive: true });
  const b = await p.launch({ executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless: 'new' });
  const pg = await b.newPage(); await pg.setViewport({ width: 1440, height: 900 });
  await pg.goto('http://localhost:4320/experiencias/senderismo-y-trekking.html', { waitUntil: 'networkidle0' });
  await pg.evaluate(i => { const m = document.querySelectorAll('.rmap')[i]; scrollTo(0, m.getBoundingClientRect().top + scrollY - 150); }, i);
  await new Promise(r => setTimeout(r, 300)); const el = (await pg.$$('.rmap'))[i];
  for (let f = 0; f < 40; f++) { await el.screenshot({ path: `${tmp}/${String(f).padStart(3, '0')}.png` }); await new Promise(r => setTimeout(r, 120)); }
  await b.close();
  execFileSync('python3', ['-c', `
import glob
from PIL import Image
fs = sorted(glob.glob('${tmp}/*.png')); ims = [Image.open(f).convert('RGB') for f in fs]
ims = [im.resize((640, int(im.height * 640 / im.width))) for im in ims]
ims[0].save('${out}', save_all=True, append_images=ims[1:] + [ims[-1]] * 12, duration=120, loop=0, optimize=True)`]);
  console.log('ok', out);
})();
