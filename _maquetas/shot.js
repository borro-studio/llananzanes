// Captura cada maqueta (#A, #B, #C) de _maquetas/rutas.html
const p=require('../_tools/node_modules/puppeteer-core');
(async()=>{const b=await p.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:'new',args:['--allow-file-access-from-files']});
const pg=await b.newPage(); await pg.setViewport({width:1440,height:900});
await pg.goto('file://'+__dirname+'/rutas.html',{waitUntil:'networkidle0'}); await new Promise(r=>setTimeout(r,800));
for(const id of ['A','B','C']){const el=await pg.$('#'+id); await el.screenshot({path:`${__dirname}/../export/maqueta-rutas-${id}.jpg`,type:'jpeg',quality:82});}
await b.close(); console.log('ok');})();
