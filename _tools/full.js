// Captura de página completa: node full.js <url> <ancho> <alto> <salida.jpg> [movil]
const p=require('puppeteer-core');
(async()=>{
 const [,,url,w,h,out,mov]=process.argv;
 const b=await p.launch({executablePath:'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',headless:'new'});
 const pg=await b.newPage(); await pg.setViewport({width:+w,height:+h,isMobile:!!mov,hasTouch:!!mov,deviceScaleFactor:mov?1.5:1});
 await pg.goto(url,{waitUntil:'networkidle0'});
 // dvh fijo y carga de imágenes diferidas antes de capturar
 await pg.addStyleTag({content:`.hero{min-height:${h}px!important}.hero--casa{min-height:${Math.round(h*.94)}px!important}.tour{min-height:${Math.round(h*(mov?.72:.88))}px!important}.cta{min-height:${Math.round(h*.88)}px!important}.nav{position:absolute!important}body::after{display:none}`});
 await pg.evaluate(async()=>{document.querySelectorAll('img[loading=lazy]').forEach(i=>i.loading='eager'); await Promise.all([...document.images].map(i=>i.decode().catch(()=>{})))});
 await new Promise(r=>setTimeout(r,800));
 const H=await pg.evaluate(()=>document.documentElement.scrollHeight); await pg.screenshot({path:out,type:'jpeg',quality:80,fullPage:true}); console.log(H);
 await b.close();
})();
